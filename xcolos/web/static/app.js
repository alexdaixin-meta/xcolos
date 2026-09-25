/* XColos operator console.
 *
 * The UI holds no game state. It posts a table, then polls the match log and
 * renders records. Everything authoritative stays on the server, which is the
 * same rule a real client follows.
 */

const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
};

/* Seats are numbered from one, on the server and here. A row's position in
 * this list is zero-based; its seat number is not. */
const FIRST_SEAT = 1;

/* How long the built-in bots pause before answering. A whole game finishes in
 * milliseconds otherwise, which is hard to watch. Connected agents are
 * unaffected — they answer at their own speed. */
const DEFAULT_PACE_MS = 150;
const seatNo = (row) => row + FIRST_SEAT;

const NAMES = ["Ada", "Blaise", "Curie", "Dirac", "Euler", "Fermi", "Gauss",
               "Hopper", "Ito", "Julia", "Kepler", "Lovelace"];

const state = {
  games: [],
  agentTypes: [],
  seats: [],
  matchId: null,
  operatorToken: "",
  since: 0,
  records: [],
  poll: null,
  view: "timeline",
  open: null,   // live seat info once the table exists
  started: false,
  snap: null,
  seatFocus: FIRST_SEAT,
};

/* ---------------------------------------------------------------- setup */

async function boot() {
  state.games = await (await fetch("/api/games")).json();
  state.agentTypes = await (await fetch("/api/agent_types")).json();

  const sel = $("game");
  state.games.forEach((g) => sel.append(new Option(g.name, g.id)));
  sel.onchange = describeGame;
  describeGame();

  for (let i = 0; i < 5; i++) addSeat();

  $("add-seat").onclick = () => addSeat();
  $("fill").onclick = fillWithBots;
  $("play").onclick = onPlay;
  $("reset").onclick = () => location.reload();
  document.querySelectorAll(".tab").forEach((t) => {
    t.onclick = () => switchView(t.dataset.view);
  });
  $("modal-close").onclick = () => $("modal").classList.add("hidden");
  $("modal-copy").onclick = async () => {
    const box = $("modal-text");
    box.select();
    try {
      await navigator.clipboard.writeText(box.value);
      $("modal-copy").textContent = "Copied";
      setTimeout(() => ($("modal-copy").textContent = "Copy"), 1500);
    } catch (e) {
      document.execCommand("copy");
    }
  };
}

function currentGame() {
  return state.games.find((g) => g.id === $("game").value) || state.games[0];
}

function describeGame() {
  const g = currentGame();
  /* Which engine is running is the thing being tested right now, so it is on
   * screen rather than in a log. */
  const engine =
    g.engine === "flow"
      ? "definition-driven"
      : "hardcoded Python";
  const judge = g.needs_judge ? " \u00b7 needs a model to judge its rules" : "";
  $("game-blurb").textContent =
    `${g.blurb} ${g.min_seats} to ${g.max_seats} seats \u00b7 ${engine}${judge}`;
  renderSeats();
}

/* A seat is somebody's to connect to by default. Bots are a convenience for
 * filling a table you want to watch alone, not the normal case. */
function addSeat(kind = "connector") {
  const g = currentGame();
  if (state.seats.length >= g.max_seats) return;
  state.seats.push({
    name: NAMES[state.seats.length] || `Seat ${state.seats.length}`,
    kind,
  });
  renderSeats();
}

function fillWithBots() {
  for (const s of state.seats) if (s.kind === "connector") s.kind = "random";
  const g = currentGame();
  while (state.seats.length < g.min_seats) addSeat("random");
  renderSeats();
}

function renderSeats() {
  const g = currentGame();
  const list = $("seats");
  const open = state.open; // live info once the table exists
  list.textContent = "";

  state.seats.forEach((seat, i) => {
    const info = open ? open.byIndex[seatNo(i)] : null;
    const li = el("li", info && info.claimed ? "done" : "");
    li.append(el("span", "idx", String(seatNo(i))));

    const name = el("input");
    name.value = seat.name;
    name.disabled = !!open;
    name.oninput = () => (seat.name = name.value);
    li.append(name);

    li.append(seatAction(seat, i, info));

    if (!open) {
      const drop = el("button", "drop", "\u00d7");
      drop.title = "Remove this seat";
      drop.onclick = () => {
        state.seats.splice(i, 1);
        renderSeats();
      };
      li.append(drop);
    } else {
      li.append(el("span"));
    }
    list.append(li);
  });

  const n = state.seats.length;
  $("seat-count").textContent = `${n}`;
  const ok = n >= g.min_seats && n <= g.max_seats;

  const btn = $("play");
  const hint = $("hint");
  if (!open) {
    btn.textContent = "Open table";
    btn.disabled = !ok;
    btn.title = "";
    hint.textContent = ok
      ? "Opens the table so each seat can be connected to."
      : "";
  } else if (state.snap && state.snap.started && state.snap.status === "running") {
    btn.textContent = "Running";
    btn.disabled = true;
    btn.title = "";
    hint.textContent = "";
  } else if (state.snap && state.snap.started) {
    // The game is over but the table is not. Same people, same seats, deal again.
    btn.textContent = `Start game ${state.snap.game_no + 1}`;
    btn.disabled = false;
    btn.title = "";
    hint.textContent = "Everyone stays connected. A new game deals fresh roles.";
  } else {
    const unfilled = state.seats
      .map((s, i) => [s, open.byIndex[seatNo(i)]])
      .filter(([s, info]) => s.kind === "connector" && !(info && info.claimed))
      .map(([s]) => s.name);
    btn.textContent = "Start game";
    btn.disabled = unfilled.length > 0;
    btn.title = unfilled.length
      ? `Still waiting for: ${unfilled.join(", ")}`
      : "Everyone is seated";
    hint.textContent = unfilled.length
      ? `Waiting for ${unfilled.join(", ")} to connect.`
      : "Everyone is seated. Press to deal roles and begin round 1.";
  }
  $("add-seat").disabled = n >= g.max_seats || !!open;
  $("fill").disabled = n >= g.max_seats && !state.seats.some((s) => s.kind === "connector");
  $("role-plan").textContent = ok
    ? planLine(g, n)
    : `Add at least ${g.min_seats} seats to open the table.`;
}

/* The one control per seat. Before the table is open it just says who will
 * play it. After, it is a Connect button that hands over the instructions,
 * and turns into a green Connected once a session actually calls in. */
function seatAction(seat, i, info) {
  const cell = el("span", "act");

  if (seat.kind !== "connector") {
    cell.append(el("span", "seat-state bot", "bot"));
    return cell;
  }
  if (!info) {
    // No table yet. Opening one is what the click is for, so the button is
    // live from the start rather than making the operator find it elsewhere.
    const b = el("button", "primary", "Connect");
    b.onclick = () => connectSeat(i);
    cell.append(b);
    return cell;
  }
  const label = {
    connecting: ["Connecting\u2026", "wait"],
    connected: [
      info.acked ? `Connected \u00b7 ${info.reads}` : `Polling \u00b7 ${info.reads}`,
      "ok",
    ],
    stalled: [
      `Stopped polling \u00b7 ${Math.round(info.seconds_since_read || 0)}s`,
      "bad",
    ],
  }[info.state];

  if (label) cell.append(el("span", `seat-state ${label[1]}`, label[0]));

  if (info.state === "connected") {
    // It acknowledged, or it is calling in a loop. Nothing left to hand over.
    const b = el("button", "ghost", "Connected");
    b.disabled = true;
    cell.append(b);
    return cell;
  }

  // Open, still connecting, or gone quiet: the instructions stay reachable so
  // the operator can hand them over again.
  const b = el("button", info.state === "stalled" ? "ghost" : "primary",
               info.state === "stalled" ? "Reconnect" : "Connect");
  b.onclick = () => showInvite(info.player_id);
  cell.append(b);
  return cell;
}

/* The main button does one of two jobs depending on where you are: open the
 * table so seats can be connected to, then start play once they are. Nothing
 * starts itself, so the last person to connect does not begin the game for
 * everybody else. */
async function onPlay() {
  if (!state.open) return void (await openTable());
  await startGame();
}

async function startGame() {
  $("error").textContent = "";
  const res = await fetch(`/api/matches/${state.matchId}/start`, { method: "POST" });
  const data = await res.json();
  if (!res.ok) {
    $("error").textContent = data.error || "could not start";
    return;
  }
  state.started = true;
  state.since = 0;
  state.records = [];
  ["view-timeline", "view-messages", "seat-world", "view-sessions",
   "view-judge"].forEach((id) => ($(id).textContent = ""));
  $("result").classList.add("hidden");
  setStatus("running", data.game_no > 1 ? `running game ${data.game_no}` : "running");
  stopPolling();
  state.poll = setInterval(pump, 700);
  pump();
}

/* Clicking Connect on a table that does not exist yet opens it first, then
 * shows that seat's instructions. One click, whichever state you were in. */
async function connectSeat(i) {
  if (!state.open) {
    const ok = await openTable();
    if (!ok) return;
  }
  const info = state.open && state.open.byIndex[seatNo(i)];
  if (info && info.player_id) showInvite(info.player_id);
  else $("error").textContent = "that seat is not open to a connection";
}

/* What the table will look like once roles are dealt.
 *
 * This used to mirror the Mafia role plan in JavaScript, which meant the
 * console confidently announced "2 mafia" for a seven-player table that the
 * game file deals one mafia to. A console cannot know a game's roster without
 * reading its definition, so it no longer pretends to: it reports the shape of
 * the round, which the server does send, and leaves the deal to the deal. */
function planLine(g, n) {
  const steps = (g.steps || []).join(" \u2192 ");
  const bits = [`${n} seats`];
  if (g.engine === "flow") bits.push("roles dealt from the game file");
  if (steps) bits.push(steps);
  return bits.join(" \u2014 ");
}

/* ----------------------------------------------------------------- play */

async function openTable() {
  if (state.open) return true;
  $("error").textContent = "";
  $("play").disabled = true;
  stopPolling();

  const res = await fetch("/api/matches", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      game: $("game").value,
      // No seed and no pace from the console. The server draws a fresh seed
      // per table; an explicit one is still accepted over the API, which is
      // how a match is replayed for comparison against the arithmetic game.
      pace_ms: DEFAULT_PACE_MS,
      seats: state.seats.map((s) => ({ name: s.name, kind: s.kind })),
    }),
  });
  const data = await res.json();

  if (!res.ok) {
    $("error").textContent = data.error || "could not open the table";
    $("play").disabled = false;
    renderSeats();
    return false;
  }

  state.matchId = data.match_id;
  state.operatorToken = data.operator_token || "";
  state.since = 0;
  state.records = [];
  ["view-timeline", "view-messages", "seat-world"].forEach((id) => ($(id).textContent = ""));
  $("result").classList.add("hidden");
  $("reset").classList.remove("hidden");

  absorb(data);
  setStatus("idle", data.waiting ? "waiting for players to connect" : "ready to start");
  state.poll = setInterval(pump, 700);
  pump();
  return true;
}

/* Fold the server's view of who is connected back into the seat rows. */
function absorb(snap) {
  state.snap = snap;
  const byIndex = {};
  for (const p of snap.connected || []) byIndex[p.seat] = { ...p };
  for (const c of snap.join_codes || []) {
    byIndex[c.seat] = { ...(byIndex[c.seat] || {}), ...c };
  }
  state.open = { byIndex, waiting: !!snap.waiting };
  renderSeats();
}

function stopPolling() {
  if (state.poll) clearInterval(state.poll);
  state.poll = null;
}

async function pump() {
  if (!state.matchId) return;
  const res = await fetch(`/api/matches/${state.matchId}/events?since=${state.since}`);
  if (!res.ok) return stopPolling();
  const data = await res.json();

  if (data.state) absorb(data.state);
  state.since = data.next;
  state.records.push(...data.records);
  if (data.records.length) render();

  if (data.state && !data.state.started) {
    state.started = false;
    setStatus("idle", data.state.ready ? "ready to start" : "waiting for players to connect");
    return; // nothing has begun, so there is nothing to render yet
  }
  state.started = true;

  if (data.done) {
    stopPolling();
    $("play").disabled = false;
    setStatus("done", "finished");
    showResult(data.state);
    if (data.state.error) $("error").textContent = data.state.error;
  }
}

async function showInvite(playerId) {
  const res = await fetch(`/api/invite/${encodeURIComponent(playerId)}`);
  if (!res.ok) return;
  const data = await res.json();
  $("modal-title").textContent = `Seat ${data.seat} · ${data.name}`;
  const facts = $("modal-facts");
  facts.textContent = "";
  for (const [k, v] of [["Endpoint", data.url], ["Your id", data.player_id]]) {
    facts.append(el("span", "k", k));
    facts.append(el("span", "v", v));
  }
  $("modal-text").value = data.text;
  $("modal").classList.remove("hidden");
}

function setStatus(cls, text) {
  $("status").className = `status ${cls}`;
  $("status").textContent = text;
}

function showResult(snap) {
  const box = $("result");
  const faction = snap.winner === "good" ? "good" : snap.winner === "evil" ? "evil" : "";
  box.className = `result ${faction}`;
  box.textContent = "";

  const head = el("div");
  head.append(el("b", null, snap.winner ? `${snap.winner} wins` : snap.status));
  head.append(document.createTextNode(` — ${snap.reason || ""}`));
  box.append(head);

  const roles = snap.seats
    .map((s) => `${s.index} ${s.name} (${s.role})`)
    .join("  ·  ");
  box.append(el("div", "meta", `${snap.turn} turns, ${snap.round} rounds`));
  box.append(el("div", "meta", roles));
  box.classList.remove("hidden");
}

/* --------------------------------------------------------------- render */

function switchView(view) {
  state.view = view;
  document.querySelectorAll(".tab").forEach((t) =>
    t.classList.toggle("active", t.dataset.view === view)
  );
  /* Every pane in the DOM, not a list written here. The list was the bug: a
   * new tab rendered its contents into a div that nothing ever unhid, so the
   * feature looked unimplemented while working perfectly. Asking the document
   * what panes exist means adding one cannot miss this step. */
  document.querySelectorAll("#stage .view").forEach((pane) =>
    pane.classList.toggle("hidden", pane.id !== `view-${view}`)
  );
  render();
}

function render() {
  if (state.view === "timeline") renderTimeline();
  else if (state.view === "messages") renderMessages();
  else if (state.view === "seats") renderSeatViews();
  else if (state.view === "judge") renderJudge();
  else renderSessions();
}

/* Every call the orchestrator made to a model, in full.
 *
 * Not a summary. The system prompt, the user prompt, the model's unparsed
 * reply, and what the system decided that reply meant. A verdict on its own
 * tells you nothing when it looks wrong: the question is always whether the
 * model said something odd or the parser read it wrongly, and only the two
 * texts side by side answer that.
 *
 * This is the one view that shows every hidden role, because the judge is sent
 * the whole table. It is an operator view and says so. Nothing here is ever
 * sent to a seat. */
function renderJudge() {
  const box = $("view-judge");
  box.textContent = "";

  const calls = state.records.filter((r) => r.type === "judge_call");
  if (!calls.length) {
    /* Three different reasons for an empty list, and saying the wrong one is
     * worse than saying nothing. The first version asserted "this game states
     * its rules as arithmetic" without checking, which was simply false for a
     * game that had just not reached its first decision yet. The table now
     * reports which game it is running and whether anything in it is decided
     * by a model, so this reads that instead of guessing. */
    const snap = state.snap || {};
    let why;
    if (!state.started) {
      why = "Nothing has begun. Press Play.";
    } else if (snap.needs_judge === false) {
      why =
        `No model calls, and there will be none: ${snap.game || "this game"} ` +
        "states every rule as arithmetic, so the system answers them itself. " +
        "Write a rule as a sentence and it will appear here.";
    } else {
      why =
        "No model calls yet. The first comes at the round's check step, " +
        "after the night is resolved and the death announced.";
    }
    box.append(el("div", "empty", why));
    return;
  }

  for (const r of calls) {
    const card = el("div", "call");
    const ok = r.value !== null && r.value !== undefined;
    card.append(
      el("div", "call-head",
        `round ${r.round} · ${(r.where && r.where.tag) || "?"} · ${r.output}` +
        ` · ${r.seconds}s · ${r.model || r.source || "?"}`)
    );
    card.append(
      el("div", ok ? "call-verdict" : "call-verdict bad",
        `${ok ? JSON.stringify(r.value) : "no usable answer"}` +
        (r.reason ? ` — ${r.reason}` : ""))
    );
    fold(card, "system prompt (cached, same every call)", r.system);
    fold(card, "user prompt (the table right now)", r.prompt);
    fold(card, "raw reply from the model", r.raw || "(nothing recorded)");
    box.append(card);
  }
}

/* A collapsed block. Prompts run to thousands of characters, so the default is
 * shut: the list is meant to be scannable, and one call expanded at a time. */
function fold(parent, label, text) {
  const d = el("details", "fold");
  d.append(el("summary", null, `${label} · ${(text || "").length} chars`));
  d.append(el("pre", "fold-body", text || ""));
  parent.append(d);
}

/* Each agent's own memory, fetched from its client rather than derived from
 * the log. After a long game these diverge, because the client applies its own
 * context budget. That divergence is the thing worth looking at. */
/* Agents: how each runner is doing, not what it remembers.
 *
 * A connected session keeps its own history on the player's machine, so the
 * server genuinely does not have it. What it does know is whether that session
 * is keeping up: how often it pulls, how far it has confirmed, and how much it
 * is behind. That is the thing worth watching when a table stops moving. */
async function renderSessions() {
  const box = $("view-sessions");
  if (!state.matchId) {
    box.textContent = "";
    box.append(el("div", "empty", "Open a table to see its agents."));
    return;
  }
  const res = await fetch(
    `/api/matches/${state.matchId}/sessions?player=operator&token=${encodeURIComponent(state.operatorToken)}`
  );
  if (!res.ok) return;
  const agents = await res.json();

  box.textContent = "";
  box.append(
    el("div", "blurb",
       "One card per seat. A session played from somebody's own assistant keeps " +
       "its memory there, so what is shown is how well it is keeping up.")
  );

  for (const a of agents) {
    const card = el("div", "session");
    const head = el("div", "session-head");
    head.append(el("span", "who", `seat ${a.seat} · ${a.name}`));

    if (a.remote) {
      const behind = (a.unacked || 0);
      head.append(el("span", `meta ${behind > 0 ? "" : ""}`, a.kind));
      head.append(el("span", "meta", `${a.reads} pulls`));
      head.append(el("span", "meta",
        behind ? `${behind} unconfirmed` : "fully caught up"));
      head.append(el("span", "meta",
        a.seconds_since_read == null ? "never pulled"
                                     : `last pull ${a.seconds_since_read}s ago`));
      card.append(head);
      // append() returns undefined, so chaining off it threw and killed the
      // render for this card and every one after it.
      const body = el("div", "session-body");
      body.append(
        el("div", "blurb",
           `Confirmed ${a.confirmed} of ${a.entitled} facts. Its conversation ` +
           "lives in that session, not here.")
      );
      card.append(body);
    } else {
      head.append(el("span", "meta",
        `${a.kind} · ${a.turns} turns · ~${a.estimated_tokens}/${a.token_budget} tokens` +
        (a.dropped ? ` · ${a.dropped} dropped` : "")));
      head.append(el("span", "meta", a.session_id));
      card.append(head);
      const body = el("div", "session-body");
      for (const t of a.history || []) {
        const row = el("div", `turn turn-${t.role}${t.pinned ? " pinned" : ""}`);
        row.append(el("span", "kind", t.pinned ? `${t.kind || t.role} ·pinned` : (t.kind || t.role)));
        row.append(el("span", "body", t.content));
        body.append(row);
      }
      card.append(body);
    }
    box.append(card);
  }
}
function line(parent, n, text, cls) {
  const row = el("div", `line ${cls || ""}`);
  row.append(el("span", "n", `${n}`));
  row.append(el("span", "t", text));
  parent.append(row);
  return row;
}

function renderTimeline() {
  const box = $("view-timeline");
  box.textContent = "";
  let header = null;

  const shown = state.records.filter(
    (r) =>
      ["process", "fact", "orchestrator", "turn", "result"].includes(r.category) ||
      (r.category === "message" && ["offered", "expired"].includes(r.type))
  );
  if (!shown.length) return void box.append(el("div", "empty", "No events yet."));

  for (const r of shown) {
    const key = `${r.round}/${r.phase}`;
    if (r.phase && key !== header) {
      header = key;
      box.append(el("div", "phase", `round ${r.round} · ${r.phase}`));
    }

    if (r.category === "fact") {
      const who = r.audience.kind === "all" ? "everyone" : `seats ${r.entitled.join(", ")}`;
      const secret = r.audience.kind !== "all";
      line(box, r.log_seq, `${r.type} → ${who}: ${factText(r)}`,
           secret ? "ev-fact ev-secret" : "ev-fact");
    } else if (r.category === "orchestrator") {
      // Not every orchestrator record is a turn request. A judge call carries
      // no seat and no schema, so printing it as one produced
      // "asks seat undefined to undefined" with the model's reasoning left
      // dangling in brackets behind it.
      if (r.type === "judge_call") {
        const where = (r.where && r.where.tag) || "?";
        const got = r.value === null || r.value === undefined
          ? "no usable answer"
          : JSON.stringify(r.value);
        line(box, r.log_seq,
             `model · ${where} · ${r.output} · ${r.seconds}s → ${got}` +
             (r.reason ? ` — ${r.reason}` : ""), "ev-orch");
      } else if (r.type === "dealt") {
        const who = r.by === "seed" ? "dealt by seed" : "assigned by the model";
        const seats = Object.entries(r.assigned || {})
          .map(([seat, row]) => `${seat}=${Object.values(row)[0]}`).join("  ");
        line(box, r.log_seq, `${who} — ${seats}`, "ev-orch");
      } else if (r.type === "roster_rejected") {
        line(box, r.log_seq,
             `model's roster refused at ${r.step} — ${r.reason}`, "ev-orch");
      } else {
        line(box, r.log_seq,
             `orchestrator asks seat ${r.seat} to ${r.action_schema} (${r.reason})`,
             "ev-orch");
      }
    } else if (r.category === "turn") {
      const a = r.action || {};
      const value = a.text || a.target;
      const flag = r.degraded ? "  [degraded]" : "";
      line(box, r.log_seq, `seat ${r.seat} (${r.role}) ${a.type}: ${value}${flag}`,
           r.degraded ? "ev-turn ev-degraded" : "ev-turn");
    } else if (r.category === "message" && r.type === "offered") {
      line(box, r.log_seq,
           `turn written for seat ${r.seat} (${r.action_schema}) — waiting for it to pull`,
           "ev-offer");
    } else if (r.category === "message" && r.type === "expired") {
      line(box, r.log_seq,
           `seat ${r.seat} did not answer in ${r.after_s}s — default applied`,
           "ev-degraded");
    } else if (r.category === "process") {
      const detail = r.type === "set_phase" ? `${r.was} → ${r.now}`
                   : r.type === "end_game" ? `${r.winner}: ${r.reason}`
                   : "";
      line(box, r.log_seq, `${r.type} ${detail}`.trim(), "ev-process");
    }
  }
  box.scrollTop = box.scrollHeight;
}

/* Polls are not traffic.
 *
 * Every connected agent asks "anything new?" every two seconds, so reads
 * outnumber real messages by orders of magnitude and say only that the
 * transport is alive — which the Agents tab already reports, with timings.
 * They stay in the log, because that is the delivery audit trail and the
 * record of who was shown what. They just are not something to read.
 *
 * What survives here is what somebody said or was told: pushes, turns,
 * answers, and acknowledgements. */
/* What a fact says, as its recipients see it.
 *
 * `rendered` is the whole of what reaches an agent. Everything else on a
 * payload is bookkeeping the engine kept for itself — the structured state
 * behind a sync, the seat and raw value behind an echo. Dumping the lot made
 * the console look like it was sending players a wall of JSON, which it was
 * not. A fact with no rendered text falls back to the payload, and that is a
 * fact nobody should be able to emit. */
function factText(r) {
  const p = r.payload || {};
  return p.rendered !== undefined ? p.rendered : JSON.stringify(p);
}

function isTraffic(r) {
  return r.type !== "read";
}

function renderMessages() {
  const box = $("view-messages");
  box.textContent = "";
  // Under a pull model the traffic is four things, not two: a turn written
  // into a seat's state, the runner fetching, the runner confirming what it
  // took in, and the runner answering.
  const rows = state.records.filter(
    (r) => (r.category === "message" || r.category === "delivery") && isTraffic(r)
  );
  if (!rows.length) return void box.append(el("div", "empty", "No traffic yet."));

  for (const r of rows) {
    if (r.category === "delivery") {
      if (r.type === "ack") {
        line(box, r.log_seq,
             `seat ${r.seat} confirmed through ${r.acked_upto - 1}`, "ev-ack");
      } else {
        line(box, r.log_seq,
             `seat ${r.seat} pushed ${(r.fact_seqs || []).length} facts`, "ev-msg-out");
      }
    } else if (r.type === "offered") {
      line(box, r.log_seq,
           `written for seat ${r.seat} [${r.action_schema}] ${(r.body || "").replace(/\n/g, " | ")}`,
           "ev-offer");
    } else if (r.type === "to_agent") {
      line(box, r.log_seq,
           `→ seat ${r.seat} [${r.msg_type}] ${(r.body || "").replace(/\n/g, " | ")}`, "ev-msg-out");
    } else if (r.type === "from_agent") {
      const said = r.response || {};
      const note = r.rejected ? ` (refused: ${r.rejected})` : "";
      const value = said.text || said.target;
      line(box, r.log_seq, `← seat ${r.seat} ${said.type}: ${value}${note}`,
           r.rejected ? "ev-degraded" : "ev-msg-in");
      if (said.reason) {
        // Private thinking. Visible here because the console is the operator's
        // view; never sent to another seat.
        line(box, r.log_seq, `    reason: ${said.reason}`, "ev-reason");
      }
    } else {
      line(box, r.log_seq, `× seat ${r.seat} ${r.error || r.type}`, "ev-degraded");
    }
  }
  box.scrollTop = box.scrollHeight;
}

function renderSeatViews() {
  const picker = $("seat-picker");
  picker.textContent = "";
  state.seats.forEach((s, i) => {
    const seat = seatNo(i);
    const b = el("button", seat === state.seatFocus ? "on" : "", `${seat} ${s.name}`);
    b.onclick = () => {
      state.seatFocus = seat;
      renderSeatViews();
    };
    picker.append(b);
  });

  const box = $("seat-world");
  box.textContent = "";
  const me = state.seatFocus;

  // Built from entitlement, not from pushed messages: a seat that pulls is
  // never pushed anything, so the old view was empty for it.
  const mine = state.records.filter((r) => {
    if (r.category === "fact") return (r.entitled || []).includes(me);
    if (r.category === "message" || r.category === "delivery") return r.seat === me && isTraffic(r);
    return false;
  });
  if (!mine.length) {
    return void box.append(el("div", "empty", "This seat has been told nothing yet."));
  }

  box.append(
    el("div", "blurb",
       "Everything this seat is entitled to, and nothing else. If something " +
       "here was not meant for it, the kernel leaked.")
  );

  for (const r of mine) {
    const m = el("div", "msg");
    if (r.category === "fact") {
      const secret = r.audience && r.audience.kind !== "all";
      m.append(el("div", "kind", secret ? `${r.type} · private` : r.type));
      m.append(el("div", "body", factText(r)));
    } else if (r.type === "offered") {
      m.append(el("div", "kind", `your turn · ${r.action_schema}`));
      m.append(el("div", "body", r.body));
    } else if (r.type === "to_agent") {
      m.append(el("div", "kind", r.msg_type));
      m.append(el("div", "body", r.body));
    } else if (r.type === "from_agent") {
      const said = r.response || {};
      m.append(el("div", "reply",
        `answered ${said.type}: ${said.text || said.target}` +
        (r.rejected ? ` — refused: ${r.rejected}` : "")));
      if (said.reason) m.append(el("div", "reason", `reason: ${said.reason}`));
    } else if (r.type === "ack") {
      m.append(el("div", "kind", "confirmed"));
      m.append(el("div", "body", `through fact ${r.acked_upto - 1}`));
    } else {
      m.append(el("div", "reply", `${r.type}: ${r.error || ""}`));
    }
    box.append(m);
  }
  box.scrollTop = box.scrollHeight;
}

boot();
