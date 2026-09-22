"""The player's client. Runs on the player's machine, not the server's.

This is how a player links a real model to a seat. They do not give the server a
key. They run this, claim their seats, and answer the turns. What sits behind
each seat is theirs: a local model, their own agent harness, a script, or a
person reading the prompt.

    from xcolos.client import XColosClient
    from xcolos.agents import BaseAgent
    from xcolos.protocol import Action

    class MyAgent(BaseAgent):
        def decide(self, env):
            # Call whatever you like here. It never leaves your machine.
            return Action(type=env.schema.id, target=env.legal_targets[0])

    client = XColosClient("http://127.0.0.1:8000", "Alex")
    client.join("w0001", [MyAgent("my-bot")])
    client.run()

Standard library only, so a player needs nothing installed to play.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from xcolos.agents import Agent
from xcolos.protocol import Action, ActionSchema, Envelope, MsgType


class ClientError(Exception):
    pass


@dataclass
class SeatTicket:
    """What the server hands back when a seat is claimed."""

    index: int
    name: str
    credential: str


class XColosClient:
    """One player, one or more seats, one process."""

    def __init__(
        self,
        base_url: str,
        player_name: str,
        poll_timeout_s: float = 20.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.player_name = player_name
        self.poll_timeout_s = poll_timeout_s

        self.player_id: str = ""
        self.token: str = ""
        self.match_id: str = ""
        self.tickets: dict[int, SeatTicket] = {}
        self.agents: dict[int, Agent] = {}
        self.finished = threading.Event()

    # ------------------------------------------------------------------
    # Joining
    # ------------------------------------------------------------------

    def join(self, match_id: str, agents: list[Agent]) -> list[SeatTicket]:
        """Claim seats in a waiting match, one per agent supplied."""
        self.match_id = match_id
        body = self._post(
            f"/api/matches/{match_id}/join",
            {"player_name": self.player_name, "seats": [a.name for a in agents]},
        )
        self.player_id = body["player_id"]
        self.token = body["token"]

        for agent, seat in zip(agents, body["seats"]):
            ticket = SeatTicket(seat["index"], seat["name"], seat["credential"])
            self.tickets[ticket.index] = ticket
            self.agents[ticket.index] = agent
            # The session opens here, on this machine. It never goes anywhere.
            agent.bind(ticket.index, match_id, owner=self.player_id)

        return list(self.tickets.values())

    # ------------------------------------------------------------------
    # Playing
    # ------------------------------------------------------------------

    def run(self, max_seconds: float = 300.0) -> None:
        """Answer turns until the match ends. Blocks.

        One thread per seat, because each seat long-polls independently. Within
        a seat everything is sequential, which is all the engine requires.
        """
        threads = [
            threading.Thread(target=self._serve_seat, args=(index,), daemon=True)
            for index in sorted(self.tickets)
        ]
        for t in threads:
            t.start()

        deadline = time.time() + max_seconds
        while not self.finished.is_set() and time.time() < deadline:
            if not any(t.is_alive() for t in threads):
                break
            time.sleep(0.05)

        self.finished.set()
        for t in threads:
            t.join(timeout=2.0)

    def _serve_seat(self, index: int) -> None:
        ticket = self.tickets[index]
        agent = self.agents[index]

        while not self.finished.is_set():
            try:
                wire = self._post(
                    f"/api/matches/{self.match_id}/poll",
                    {
                        "player_id": self.player_id,
                        "token": self.token,
                        "seat": index,
                        "credential": ticket.credential,
                        "timeout_ms": int(self.poll_timeout_s * 1000),
                    },
                )
            except ClientError:
                return

            message = wire.get("message")
            if message is None:
                continue  # the poll simply timed out; ask again

            env = _envelope_from(message)
            action = agent.handle(env)

            if message.get("reply_required"):
                self._post(
                    f"/api/matches/{self.match_id}/reply",
                    {
                        "player_id": self.player_id,
                        "token": self.token,
                        "seat": index,
                        "credential": ticket.credential,
                        "action": action.to_json() if action else None,
                    },
                )

            if env.type is MsgType.GAME_END:
                self.finished.set()
                return

    # ------------------------------------------------------------------

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        req = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.poll_timeout_s + 15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise ClientError(e.read().decode()[:300]) from None
        except (urllib.error.URLError, TimeoutError) as e:
            raise ClientError(str(e)) from None


def _envelope_from(wire: dict[str, Any]) -> Envelope:
    schema = wire.get("schema")
    return Envelope(
        type=MsgType(wire["type"]),
        match_id=wire["match_id"],
        seat=wire["seat"],
        body=wire["body"],
        turn_seq=wire.get("turn_seq"),
        schema=ActionSchema(
            id=schema["id"],
            target=schema["target"],
            choices=tuple(schema.get("choices", ())),
        )
        if schema
        else None,
        legal_targets=tuple(wire.get("legal_targets", ())),
        deadline_ms=wire.get("deadline_ms"),
    )


# ----------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Run a client from the command line, so a player needs to write nothing.

    The default agent is the built-in random one. Point `--agent` at your own
    class to put a real model in the seat.
    """
    import argparse
    import importlib

    from xcolos.agents import RandomAgent

    ap = argparse.ArgumentParser(
        prog="xcolos.client", description="Play XColos seats from your own machine."
    )
    ap.add_argument("match", help="the match to join")
    ap.add_argument("--server", default="http://127.0.0.1:8000")
    ap.add_argument("--name", default="player")
    ap.add_argument("--seats", type=int, default=1, help="how many seats to claim")
    ap.add_argument(
        "--agent",
        default="",
        help="dotted path to your agent class, e.g. mypkg.bots:Cunning",
    )
    args = ap.parse_args(argv)

    if args.agent:
        module_name, _, class_name = args.agent.partition(":")
        factory = getattr(importlib.import_module(module_name), class_name)
    else:
        factory = RandomAgent

    agents = [factory(name=f"{args.name}-{i}") for i in range(args.seats)]
    client = XColosClient(args.server, args.name)

    tickets = client.join(args.match, agents)
    print(f"joined {args.match} as {client.player_id}")
    for t in tickets:
        print(f"  seat {t.index}: {t.name}")
    print("waiting for the match to start...")

    client.run()
    print("match over")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
