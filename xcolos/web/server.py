"""HTTP server for the operator console.

Standard library only. No package index is reachable from this machine, and a
console that cannot be installed is not much of a console.

Matches run on a background thread. The log grows as they play, and the browser
polls for new records. Because the log is append-only and complete, the UI is
purely a reader: it renders records and holds no game state of its own.
"""

from __future__ import annotations

import json
import mimetypes
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from xcolos.agents import (
    BrokenAgent,
    LLMAgent,
    RandomAgent,
    ScriptedAgent,
    SilentAgent,
    offline_model,
)
from xcolos.game import Game, RunStatus
from xcolos.identity import OPERATOR, AccessDenied, Player
from xcolos.protocol import Action
from xcolos.host import LocalAgentHost, Registry
from xcolos.log import MatchLog
from xcolos.orchestrators.mafia import MAX_SEATS, MIN_SEATS, MafiaOrchestrator, role_plan
from xcolos.remote import ConnectorHost, RemoteAgentHost
from xcolos.runner import Runner
from xcolos.tools import PLAY_PATH, TableTools, invite_text

STATIC = Path(__file__).parent / "static"

GAMES = [
    {
        "id": "mafia",
        "name": "Mafia",
        "min_seats": MIN_SEATS,
        "max_seats": MAX_SEATS,
        "blurb": "Hidden-role social deduction. Mafia kill by night, the town votes by day.",
    }
]

AGENT_TYPES = [
    {
        "id": "random",
        "label": "Random",
        "blurb": "Picks uniformly among legal moves. Varied and reproducible.",
    },
    {
        "id": "scripted",
        "label": "Scripted",
        "blurb": "Always takes the first legal move. Fully deterministic.",
    },
    {
        "id": "broken",
        "label": "Broken",
        "blurb": "Always answers invalidly. Exercises the repair ladder.",
    },
    {
        "id": "silent",
        "label": "Silent",
        "blurb": "Never answers. Carried by the declared default action.",
    },
    {
        "id": "llm",
        "label": "Model",
        "blurb": "Prompted from its own session. Uses the offline stub until a provider is wired in.",
    },
    {
        "id": "remote",
        "label": "Remote player",
        "blurb": "Held by a client on someone else's machine. They bring their own model.",
    },
    {
        "id": "connector",
        "label": "Your assistant",
        "blurb": "Played by your own Claude or ChatGPT session through the game tools.",
    },
]


def make_agent(kind: str, name: str, seed: int, index: int, persona: str = ""):
    """Build one agent. Each gets its own session when the server binds its seat."""
    # Seeded from the match and the seat, never from the kernel's generator, so
    # agents are reproducible without perturbing the game's own draws.
    own_seed = seed * 1000 + index
    if kind == "scripted":
        return ScriptedAgent(name=name)
    if kind == "broken":
        return BrokenAgent(name=name)
    if kind == "silent":
        return SilentAgent(name=name)
    if kind == "llm":
        return LLMAgent(
            name=name,
            completion=offline_model(own_seed),
            persona=persona,
            model="offline-stub",
        )
    return RandomAgent(name=name, seed=own_seed)


class PacedHost(LocalAgentHost):
    """A local client that takes its time, so a match is watchable.

    Pacing belongs on the client. A slow agent is a slow client, and the kernel
    should not know or care.
    """

    host_id = "console"

    def __init__(self, agents, pace_ms: int = 0, player=None) -> None:
        super().__init__(agents, player=player)
        self.pace_ms = pace_ms

    def deliver(self, env):
        from xcolos.protocol import RESPONSE_REQUIRED

        if self.pace_ms and env.type in RESPONSE_REQUIRED:
            time.sleep(self.pace_ms / 1000)
        return super().deliver(env)


@dataclass
class MatchHandle:
    match_id: str
    game: Game
    registry: Any = None
    operator: Any = None
    thread: threading.Thread | None = None
    error: str | None = None
    config: dict[str, Any] = field(default_factory=dict)
    #: Seats reserved for players who have not connected yet.
    open_seats: list[dict[str, Any]] = field(default_factory=list)
    remote_hosts: dict[str, Any] = field(default_factory=dict)
    start: Any = None
    waiting: bool = False
    runner: Any = None
    tools: Any = None
    #: Every seat has someone behind it. The operator still has to say go.
    ready: bool = False
    started: bool = False

    def snapshot(self) -> dict[str, Any]:
        g = self.game
        return {
            "match_id": self.match_id,
            "status": g.status.value,
            "winner": g.winner,
            "reason": g.reason,
            "round": g.round,
            "turn": g.turn_seq,
            "phase": g.phase,
            "running": bool(self.thread and self.thread.is_alive()),
            "waiting": self.waiting,
            "ready": self.ready,
            "started": self.started,
            "open_seats": list(self.open_seats),
            "join_codes": (
                self.tools.summary()["open_seats"] if self.tools else []
            ),
            "connected": (
                self.tools.summary()["connected"] if self.tools else []
            ),
            "error": self.error,
            "config": self.config,
            # The console is the operator. It is handed the operator token so
            # it can read sessions, exactly as any other client would.
            "operator_token": self.operator.token if self.operator else "",
            "seats": [
                {
                    "index": s.index,
                    "name": s.name,
                    "status": s.status.value,
                    # Roles are the operator's to see. This console is a
                    # spectator surface, not a player's client.
                    "role": s.role,
                    "faction": s.faction,
                    "kind": self.config.get("seats", [{}] * (s.index + 1))[s.index].get(
                        "kind"
                    )
                    if s.index < len(self.config.get("seats", []))
                    else None,
                }
                for s in self.game.seats.values()
            ],
        }


class MatchManager:
    """Creates, runs and serves matches. Server side, in process."""

    def __init__(self) -> None:
        self._matches: dict[str, MatchHandle] = {}
        self._hosts: dict[str, PacedHost] = {}
        self._counter = 0
        self._lock = threading.Lock()

    def create(self, config: dict[str, Any]) -> MatchHandle:
        """Build a match. Local seats are filled now; remote seats wait.

        A remote seat belongs to a player's own process, so the match cannot
        start until they connect. Everything else is identical either way: the
        runner cannot tell a laptop from an in-process agent.
        """
        seats = config.get("seats") or []
        if not MIN_SEATS <= len(seats) <= MAX_SEATS:
            raise ValueError(
                f"a table needs between {MIN_SEATS} and {MAX_SEATS} seats, got {len(seats)}"
            )
        game_id = config.get("game", "mafia")
        if game_id not in {g["id"] for g in GAMES}:
            raise ValueError(f"unknown game '{game_id}'")

        with self._lock:
            self._counter += 1
            match_id = f"w{self._counter:04d}"

        seed = int(config.get("seed") or self._counter)
        pace_ms = int(config.get("pace_ms") or 0)
        deadline_ms = int(config.get("deadline_ms") or 0) or None

        log = MatchLog(match_id)
        game = Game(match_id=match_id, game_id=game_id, seed=seed, log=log)
        registry = Registry(match_id)
        operator = Player(player_id=OPERATOR, display_name="console")

        kind_of = [sp.get("kind", "random") for sp in seats]
        remote_indices = [i for i, k in enumerate(kind_of) if k == "remote"]
        connector_indices = [i for i, k in enumerate(kind_of) if k == "connector"]
        local_indices = [
            i for i, k in enumerate(kind_of) if k not in {"remote", "connector"}
        ]

        # Seats are registered in table order regardless of who holds them, so
        # the seat numbering a player sees matches the console exactly.
        host = PacedHost(
            [
                make_agent(
                    seats[i].get("kind", "random"),
                    seats[i].get("name") or f"Seat {i}",
                    seed,
                    i,
                    seats[i].get("persona", ""),
                )
                for i in local_indices
            ],
            pace_ms=pace_ms,
            player=operator,
        )
        local_bindings = iter(host.register())

        connector_host = ConnectorHost(
            Player.new("table"), [seats[i].get("name") or f"Seat {i}" for i in connector_indices]
        )
        connector_bindings = iter(connector_host.register())

        handle = MatchHandle(
            match_id=match_id,
            game=game,
            registry=registry,
            operator=operator,
            config={
                **config,
                "seed": seed,
                "pace_ms": pace_ms,
                "deadline_ms": deadline_ms,
            },
            waiting=bool(remote_indices or connector_indices),
        )

        connector_slots: list[tuple[int, str]] = []
        for i, spec in enumerate(seats):
            name = spec.get("name") or f"Seat {i}"
            if i in remote_indices:
                index = game.register_seat(name, "remote", {"kind": "remote"})
                handle.open_seats.append({"index": index, "name": name})
            elif i in connector_indices:
                binding = next(connector_bindings)
                index = game.register_seat(
                    name, connector_host.host_id, binding.profile
                )
                registry.attach(index, connector_host, binding)
                connector_slots.append((index, name))
            else:
                binding = next(local_bindings)
                index = game.register_seat(name, host.host_id, binding.profile)
                registry.attach(index, host, binding)

        runner = Runner(
            game,
            MafiaOrchestrator(),
            registry,
            deadline_ms=deadline_ms or (600_000 if connector_slots else None),
        )
        handle.runner = runner
        handle.tools = TableTools(
            game,
            runner,
            registry,
            poll_seconds=int(config.get("poll_seconds") or 8),
            # Attaching makes the table ready. Starting is the operator's call.
            on_ready=lambda: self._mark_ready(handle),
        )
        for index, name in connector_slots:
            handle.tools.offer(index, name)

        self._matches[match_id] = handle
        self._hosts[match_id] = host

        if not remote_indices and not connector_indices:
            # Nothing to wait for, but the operator still presses start.
            handle.ready = True
        return handle

    def _mark_ready(self, handle: MatchHandle) -> None:
        """Every offered seat has a session behind it. Note it and wait.

        Deliberately does not start the match. Whoever set the table decides
        when play begins; otherwise the last person to connect starts the game
        for everybody else, which is not theirs to do.
        """
        if handle.open_seats:
            return
        handle.ready = True

    def start_match(self, match_id: str) -> dict[str, Any]:
        """Begin play. The operator's call, not the last connector's."""
        handle = self._require(match_id)
        if handle.started:
            return {"started": True, "already": True}
        if not handle.ready and handle.tools and handle.tools.open_seats:
            unfilled = [
                s.name for s in handle.tools.open_seats.values() if not s.taken
            ]
            if unfilled:
                raise ValueError(
                    "these seats have nobody behind them yet: " + ", ".join(unfilled)
                )
        if handle.open_seats:
            raise ValueError("some seats are still waiting for a remote client")
        handle.started = True
        self._launch(handle)
        return {"started": True, "match_id": match_id}

    def _launch(self, handle: MatchHandle) -> None:
        """Start the runner. Called once every seat has someone behind it.

        A table with a pulling seat needs no thread at all. The runner advances
        until that seat is due, then parks, and the seat's own tool calls drive
        it onward. Only a table of push seats needs somewhere to run.
        """
        handle.waiting = False
        has_pull = any(
            getattr(h, "pull", False) for h in handle.registry.host_of.values()
        )

        if has_pull:
            try:
                handle.runner.start()
            except Exception as exc:  # noqa: BLE001
                handle.error = f"{type(exc).__name__}: {exc}"
            return

        def run() -> None:
            try:
                handle.runner.run()
            except Exception as exc:  # noqa: BLE001
                handle.error = f"{type(exc).__name__}: {exc}"

        handle.thread = threading.Thread(
            target=run, daemon=True, name=handle.match_id
        )
        handle.thread.start()

    # ------------------------------------------------------------------
    # Remote players
    # ------------------------------------------------------------------

    def join(
        self, match_id: str, player_name: str, seat_names: list[str]
    ) -> dict[str, Any]:
        """A player claims open seats and is issued credentials for them.

        The server learns a display name and nothing else. It never asks what
        is behind the seat, and has no way to find out.
        """
        handle = self._require(match_id)
        with self._lock:
            if not handle.waiting:
                raise ValueError("this match is not waiting for players")
            wanted = len(seat_names)
            if wanted > len(handle.open_seats):
                raise ValueError(
                    f"{len(handle.open_seats)} seats are open, you asked for {wanted}"
                )
            taken = [handle.open_seats.pop(0) for _ in range(wanted)]

        player = Player.new(player_name)
        host = RemoteAgentHost(player, [s["name"] for s in taken])
        bindings = host.register()

        issued = []
        for slot, binding in zip(taken, bindings):
            handle.registry.attach(slot["index"], host, binding)
            host.claim(slot["index"], binding.credential)
            handle.remote_hosts[str(slot["index"])] = host
            issued.append(
                {
                    "index": slot["index"],
                    "name": slot["name"],
                    "credential": binding.credential,
                }
            )

        handle.game.log.record(
            "setup",
            "player_joined",
            player=player.player_id,
            display_name=player_name,
            seats=[s["index"] for s in issued],
        )

        if not handle.open_seats:
            self._launch(handle)

        return {
            "player_id": player.player_id,
            "token": player.token,
            "match_id": match_id,
            "seats": issued,
            "started": not handle.waiting,
        }

    def poll(
        self, match_id: str, seat: int, player_id: str, token: str,
        credential: str, timeout_ms: int,
    ) -> dict[str, Any]:
        handle = self._require(match_id)
        handle.registry.ownership.check_act(seat, player_id, token, credential)
        host = handle.remote_hosts.get(str(seat))
        if host is None:
            raise AccessDenied(f"seat {seat} is not held by a remote client")
        message = host.poll(seat, min(max(timeout_ms, 100), 60_000) / 1000)
        return {"message": message}

    def reply(
        self, match_id: str, seat: int, player_id: str, token: str,
        credential: str, action: dict[str, Any] | None,
    ) -> dict[str, Any]:
        handle = self._require(match_id)
        handle.registry.ownership.check_act(seat, player_id, token, credential)
        host = handle.remote_hosts.get(str(seat))
        if host is None:
            raise AccessDenied(f"seat {seat} is not held by a remote client")
        parsed = (
            Action(
                type=action.get("type", ""),
                target=action.get("target"),
                text=action.get("text", ""),
            )
            if action
            else None
        )
        return {"accepted": host.reply(seat, parsed)}

    # ------------------------------------------------------------------
    # Game tools
    # ------------------------------------------------------------------

    def tools_for_player(self, player_id: str) -> tuple[MatchHandle, TableTools]:
        """Find the seat a player id belongs to.

        One endpoint serves every table and every player. Nothing is registered
        in advance, so the number of players is unlimited.
        """
        wanted = (player_id or "").strip()
        for handle in self._matches.values():
            if handle.tools and wanted in handle.tools.open_seats:
                return handle, handle.tools
        raise AccessDenied("unknown player id")

    def play(self, body: dict[str, Any]) -> dict[str, Any]:
        _, tools = self.tools_for_player(body.get("id", ""))
        return tools.play(
            body.get("id", ""),
            body.get("ack"),
            body.get("answer"),
            body.get("name", ""),
        )

    def open_tables(self) -> list[dict[str, Any]]:
        out = []
        for h in self._matches.values():
            if not h.tools:
                continue
            summary = h.tools.summary()
            free = [s for s in summary["open_seats"] if not s["taken"]]
            if free:
                out.append({**summary, "open_seats": free})
        return out

    def invite(self, player_id: str, base_url: str) -> dict[str, Any]:
        """The paste-ready block for one seat, carrying its player id."""
        handle, tools = self.tools_for_player(player_id)
        slot = tools.open_seats[player_id.strip()]
        return {
            "match_id": handle.match_id,
            "seat": slot.seat,
            "name": slot.name,
            "player_id": slot.key,
            "url": f"{base_url.rstrip('/')}{PLAY_PATH}",
            "text": invite_text(
                base_url, handle.match_id, slot.seat, slot.key, tools.poll_seconds
            ),
        }

    def get(self, match_id: str) -> MatchHandle | None:
        return self._matches.get(match_id)

    def events(self, match_id: str, since: int) -> dict[str, Any]:
        handle = self._matches.get(match_id)
        if handle is None:
            raise KeyError(match_id)
        # The log list is append-only, so a slice is a consistent read even
        # while the match thread is still writing.
        records = handle.game.log.records
        new = records[since:]
        # Done means the match is over, not that no thread is running. A table
        # with a pulling seat has no thread at all: it advances on the agents'
        # own calls, so judging by the thread stopped the console dead on its
        # first poll.
        over = handle.started and handle.game.status is not RunStatus.RUNNING
        return {
            "records": new,
            "next": since + len(new),
            "done": bool(over),
            "state": handle.snapshot(),
        }

    def sessions(
        self, match_id: str, player_id: str, token: str
    ) -> list[dict[str, Any]]:
        """Sessions this caller is allowed to read, and no others.

        A session holds a seat's secrets, so this is authorised rather than
        open. The operator sees every seat, because the console is a spectator
        surface and says so. A player sees only the seats it owns.
        """
        handle = self._require(match_id)
        registry = handle.registry
        out = []
        for index in registry.readable_seats(player_id, token):
            host = registry.host_of[index]
            try:
                session = registry.session_of(index, player_id, token)
            except AccessDenied:
                continue
            except KeyError:
                # Held by a player's own process. Its memory is on their
                # machine, so we report the seat and say why it is empty
                # rather than omitting it or inventing one.
                out.append(
                    {
                        "seat": index,
                        "name": handle.game.seats[index].name,
                        "kind": "remote",
                        "remote": True,
                        "owner": registry.ownership.owner_of.get(index, ""),
                        "session_id": f"{handle.match_id}:seat{index}",
                        "turns": 0,
                        "dropped": 0,
                        "estimated_tokens": 0,
                        "token_budget": 0,
                        "history": [],
                    }
                )
                continue
            agent = host.agent(index)
            snap = session.snapshot()
            snap["name"] = agent.name
            snap["kind"] = type(agent).__name__
            snap["remote"] = False
            out.append(snap)
        return out

    def ownership(self, match_id: str) -> list[dict[str, Any]]:
        """Who holds which seat. Tokens and credentials never appear."""
        return self._require(match_id).registry.ownership.summary()

    def resume(
        self, match_id: str, seat: int, player_id: str, token: str, credential: str
    ) -> dict[str, Any]:
        """Everything this seat is entitled to, for a client rebuilding itself.

        Acting needs the seat credential as well as the player token, so a
        reconnecting client proves both who it is and which seat it speaks for.
        The server owns the delivery cursor, which is why a resume is a read
        rather than a negotiation.
        """
        handle = self._require(match_id)
        handle.registry.ownership.check_act(seat, player_id, token, credential)
        game = handle.game
        facts = game.entitled_facts(seat)
        return {
            "match_id": match_id,
            "seat": seat,
            "session_id": f"{match_id}:seat{seat}",
            "status": game.status.value,
            "round": game.round,
            "phase": game.phase,
            "entitled_facts": [f.to_fields() | {"fact_type": f.type} for f in facts],
            "messages": [
                {"msg_type": r["msg_type"], "body": r["body"]}
                for r in game.log.where("message", "to_agent", seat=seat)
            ],
        }

    def _require(self, match_id: str) -> MatchHandle:
        handle = self._matches.get(match_id)
        if handle is None:
            raise KeyError(match_id)
        return handle

    def list(self) -> list[dict[str, Any]]:
        return [h.snapshot() for h in self._matches.values()]


# ----------------------------------------------------------------------


class Handler(BaseHTTPRequestHandler):
    manager: MatchManager
    server_version = "xcolos"

    def log_message(self, fmt: str, *args: Any) -> None:  # quieter console
        pass

    # -- helpers -------------------------------------------------------

    def _json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, name: str) -> None:
        path = (STATIC / name).resolve()
        if not str(path).startswith(str(STATIC.resolve())) or not path.is_file():
            self._json({"error": "not found"}, 404)
            return
        body = path.read_bytes()
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _base_url(self) -> str:
        """The address the caller reached us on, so an invite is pasteable."""
        host = self.headers.get("Host") or f"127.0.0.1:{self.server.server_address[1]}"
        return f"http://{host}"

    def _identity(self, query: dict[str, list[str]]) -> tuple[str, str]:
        """Who is asking.

        A header is the real channel; the query string exists so the local
        console can ask without a request library. Both carry the same pair.
        """
        player = self.headers.get("X-Player") or (query.get("player") or [OPERATOR])[0]
        token = self.headers.get("X-Token") or (query.get("token") or [""])[0]
        return player, token

    def _body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        return json.loads(self.rfile.read(length) or b"{}")

    # -- routes --------------------------------------------------------

    def do_GET(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        query = parse_qs(url.query)

        if not parts:
            return self._static("index.html")
        if parts[0] != "api":
            # STATIC already points at the static directory, so a leading
            # "static/" in the URL must not be repeated in the filesystem path.
            if parts[0] == "static":
                parts = parts[1:]
            return self._static("/".join(parts))

        if parts[1:] == ["games"]:
            return self._json(GAMES)
        if parts[1:] == ["agent_types"]:
            return self._json(AGENT_TYPES)
        if parts[1:] == ["matches"]:
            return self._json(self.manager.list())
        if parts[1:] == ["open"]:
            return self._json(self.manager.open_tables())
        if parts[1:2] == ["tools"] and parts[2:] == ["tables"]:
            return self._json(self.manager.open_tables())
        if parts[1:2] == ["invite"] and len(parts) == 3:
            try:
                return self._json(self.manager.invite(parts[2], self._base_url()))
            except AccessDenied as exc:
                return self._json({"error": str(exc)}, 404)

        if len(parts) >= 3 and parts[1] == "matches":
            match_id = parts[2]
            if len(parts) == 3:
                handle = self.manager.get(match_id)
                if handle is None:
                    return self._json({"error": "no such match"}, 404)
                return self._json(handle.snapshot())
            if parts[3] == "sessions":
                player_id, token = self._identity(query)
                try:
                    return self._json(
                        self.manager.sessions(match_id, player_id, token)
                    )
                except KeyError:
                    return self._json({"error": "no such match"}, 404)
                except AccessDenied as exc:
                    return self._json({"error": str(exc)}, 403)
            if parts[3] == "ownership":
                try:
                    return self._json(self.manager.ownership(match_id))
                except KeyError:
                    return self._json({"error": "no such match"}, 404)
            if parts[3] == "events":
                since = int((query.get("since") or ["0"])[0])
                try:
                    return self._json(self.manager.events(match_id, since))
                except KeyError:
                    return self._json({"error": "no such match"}, 404)

        self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        if len(parts) == 5 and parts[1] == "matches" and parts[3] == "resume":
            body = self._body()
            try:
                return self._json(
                    self.manager.resume(
                        parts[2],
                        int(parts[4]),
                        body.get("player_id", ""),
                        body.get("token", ""),
                        body.get("credential", ""),
                    )
                )
            except KeyError:
                return self._json({"error": "no such match"}, 404)
            except AccessDenied as exc:
                return self._json({"error": str(exc)}, 403)

        if len(parts) == 4 and parts[1] == "matches" and parts[3] == "start":
            try:
                return self._json(self.manager.start_match(parts[2]))
            except KeyError:
                return self._json({"error": "no such match"}, 404)
            except ValueError as exc:
                return self._json({"error": str(exc)}, 400)

        if len(parts) == 4 and parts[1] == "matches" and parts[3] in {
            "join", "poll", "reply"
        }:
            match_id, verb = parts[2], parts[3]
            body = self._body()
            try:
                if verb == "join":
                    return self._json(
                        self.manager.join(
                            match_id,
                            body.get("player_name", "player"),
                            body.get("seats") or ["seat"],
                        )
                    )
                common = (
                    match_id,
                    int(body.get("seat", -1)),
                    body.get("player_id", ""),
                    body.get("token", ""),
                    body.get("credential", ""),
                )
                if verb == "poll":
                    return self._json(
                        self.manager.poll(*common, int(body.get("timeout_ms", 20000)))
                    )
                return self._json(self.manager.reply(*common, body.get("action")))
            except KeyError:
                return self._json({"error": "no such match"}, 404)
            except AccessDenied as exc:
                return self._json({"error": str(exc)}, 403)
            except ValueError as exc:
                return self._json({"error": str(exc)}, 400)

        # The one endpoint every player uses. Any table, any number of players.
        if parts == ["api", "play"]:
            try:
                return self._json(self.manager.play(self._body()))
            except AccessDenied as exc:
                return self._json({"error": str(exc)}, 403)

        if parts == ["api", "matches"]:
            try:
                handle = self.manager.create(self._body())
            except ValueError as exc:
                return self._json({"error": str(exc)}, 400)
            return self._json(handle.snapshot(), 201)
        self._json({"error": "not found"}, 404)


def build_server(port: int = 8000, manager: MatchManager | None = None):
    handler = type("BoundHandler", (Handler,), {"manager": manager or MatchManager()})
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def serve(port: int = 8000) -> None:
    httpd = build_server(port)
    print(f"XColos console on http://127.0.0.1:{port}")
    print("Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(prog="xcolos.web")
    ap.add_argument("--port", type=int, default=8000)
    serve(ap.parse_args().port)
