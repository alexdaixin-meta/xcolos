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
  seatFocus: 0,
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
  $("game-blurb").textContent = `${g.blurb} ${g.min_seats} to ${g.max_seats} seats.`;
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
    const info = open ? open.byIndex[i] : null;
    const li = el("li", info && info.claimed ? "done" : "");
    li.append(el("span", "idx", String(i)));

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
  } else if (state.started) {
    btn.textContent = "Running";
    btn.disabled = true;
    btn.title = "";
    hint.textContent = "";
  } else {
    const unfilled = state.seats
      .map((s, i) => [s, open.byIndex[i]])
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
    ? `${rolePlan(n)} \u2014 assigned at random when play begins.`
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
  setStatus("running", "running");
  renderSeats();
}

/* Clicking Connect on a table that does not exist yet opens it first, then
 * shows that seat's instructions. One click, whichever state you were in. */
async function connectSeat(i) {
  if (!state.open) {
    const ok = await openTable();
    if (!ok) return;
  }
  const info = state.open && state.open.byIndex[i];
  if (info && info.player_id) showInvite(info.player_id);
  else $("error").textContent = "that seat is not open to a connection";
}

/* Mirrors the server's role plan, for a preview only. The server decides. */
function rolePlan(n) {
  const mafia = n <= 6 ? 1 : n <= 9 ? 2 : 3;
  return `${mafia} mafia, 1 detective, ${n - mafia - 1} villagers`;
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
      seed: Number($("seed").value),
      pace_ms: Number($("pace").value),
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
  ["timeline", "messages", "seats", "sessions"].forEach((v) =>
    $(`view-${v}`).classList.toggle("hidden", v !== view)
  );
  render();
}

function render() {
  if (state.view === "timeline") renderTimeline();
  else if (state.view === "messages") renderMessages();
  else if (state.view === "seats") renderSeatViews();
  else renderSessions();
}

/* Each agent's own memory, fetched from its client rather than derived from
 * the log. After a long game these diverge, because the client applies its own
 * context budget. That divergence is the thing worth looking at. */
async function renderSessions() {
  const box = $("view-sessions");
  if (!state.matchId) {
    box.textContent = "";
    box.append(el("div", "empty", "Play a match to see agent sessions."));
    return;
  }
  const res = await fetch(
    `/api/matches/${state.matchId}/sessions?player=operator&token=${encodeURIComponent(state.operatorToken)}`
  );
  if (!res.ok) return;
  const sessions = await res.json();

  box.textContent = "";
  box.append(
    el("div", "blurb",
       "Every seat holds its own session. No two are shared, and none contains anything the server did not send it.")
  );

  for (const s of sessions) {
    const card = el("div", "session");
    const head = el("div", "session-head");
    head.append(el("span", "who", `seat ${s.seat} · ${s.name}`));
    head.append(el("span", "meta",
      `${s.kind} · ${s.turns} turns · ~${s.estimated_tokens}/${s.token_budget} tokens` +
      (s.dropped ? ` · ${s.dropped} dropped` : "")));
    head.append(el("span", "meta", s.session_id));
    head.append(el("span", "meta", `owner ${s.owner}`));
    card.append(head);

    const body = el("div", "session-body");
    for (const t of s.history) {
      const row = el("div", `turn turn-${t.role}${t.pinned ? " pinned" : ""}`);
      row.append(el("span", "kind", t.pinned ? `${t.kind || t.role} ·pinned` : (t.kind || t.role)));
      row.append(el("span", "body", t.content));
      body.append(row);
    }
    card.append(body);
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

  const shown = state.records.filter((r) =>
    ["process", "fact", "orchestrator", "turn", "result"].includes(r.category)
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
      line(box, r.log_seq, `${r.type} → ${who}: ${JSON.stringify(r.payload)}`,
           secret ? "ev-fact ev-secret" : "ev-fact");
    } else if (r.category === "orchestrator") {
      line(box, r.log_seq, `orchestrator asks seat ${r.seat} to ${r.action_schema} (${r.reason})`, "ev-orch");
    } else if (r.category === "turn") {
      const a = r.action || {};
      const value = a.text || a.target;
      const flag = r.degraded ? "  [degraded]" : "";
      line(box, r.log_seq, `seat ${r.seat} (${r.role}) ${a.type}: ${value}${flag}`,
           r.degraded ? "ev-turn ev-degraded" : "ev-turn");
    } else if (r.category === "process") {
      const detail = r.type === "set_phase" ? `${r.was} → ${r.now}`
                   : r.type === "end_game" ? `${r.winner}: ${r.reason}`
                   : "";
      line(box, r.log_seq, `${r.type} ${detail}`.trim(), "ev-process");
    }
  }
  box.scrollTop = box.scrollHeight;
}

function renderMessages() {
  const box = $("view-messages");
  box.textContent = "";
  const msgs = state.records.filter((r) => r.category === "message");
  if (!msgs.length) return void box.append(el("div", "empty", "No messages yet."));

  for (const r of msgs) {
    if (r.type === "to_agent") {
      line(box, r.log_seq, `→ seat ${r.seat} [${r.msg_type}] ${r.body.replace(/\n/g, " | ")}`, "ev-msg-out");
    } else if (r.type === "from_agent") {
      line(box, r.log_seq, `← seat ${r.seat} ${JSON.stringify(r.response)}`, "ev-msg-in");
    } else {
      line(box, r.log_seq, `× seat ${r.seat} ${r.error}`, "ev-degraded");
    }
  }
  box.scrollTop = box.scrollHeight;
}

function renderSeatViews() {
  const picker = $("seat-picker");
  picker.textContent = "";
  state.seats.forEach((s, i) => {
    const b = el("button", i === state.seatFocus ? "on" : "", `${i} ${s.name}`);
    b.onclick = () => {
      state.seatFocus = i;
      renderSeatViews();
    };
    picker.append(b);
  });

  const box = $("seat-world");
  box.textContent = "";
  const mine = state.records.filter(
    (r) => r.category === "message" && r.seat === state.seatFocus
  );
  if (!mine.length) return void box.append(el("div", "empty", "This seat has seen nothing yet."));

  box.append(
    el("div", "blurb",
       "Everything this seat was sent, and nothing else. If something here was not meant for it, the kernel leaked.")
  );

  for (const r of mine) {
    const m = el("div", "msg");
    if (r.type === "to_agent") {
      m.append(el("div", "kind", r.msg_type));
      m.append(el("div", "body", r.body));
    } else if (r.type === "from_agent") {
      m.append(el("div", "reply", `↳ ${JSON.stringify(r.response)}`));
    } else {
      m.append(el("div", "reply", `× unreachable: ${r.error}`));
    }
    box.append(m);
  }
  box.scrollTop = box.scrollHeight;
}

boot();
