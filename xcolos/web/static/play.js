/* XColos player client, in the browser.
 *
 * The server drives. It tells this seat what happened, and when it is this
 * seat's turn it asks for exactly one action. This page answers.
 *
 * A person typing is the reference implementation. A linked agent is just
 * something that fills the same box faster. The server cannot tell which
 * answered, and never learns how the answer was reached.
 */

const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
};

/* ------------------------------------------------------------------ *
 * LINK YOUR AGENT HERE.
 *
 * Return a string. It is read exactly the way typed text is read, so a bare
 * seat number, a sentence, or a JSON object all work.
 *
 * Whatever you call inside this function stays in this browser. The server
 * never sees it, and has no way to find out what it was.
 * ------------------------------------------------------------------ */
async function linkedAgent(request) {
  // Replace this body with a call to your own model or local session.
  // `request` carries this seat's whole conversation and the current ask:
  //   request.messages       the conversation so far, in chat shape
  //   request.question       what the server just asked, as prose
  //   request.legal_targets  the seat numbers you may name, if any
  //   request.answer_with    "text" | "seat" | "enum" | "none"
  await new Promise((r) => setTimeout(r, 400 + Math.random() * 600));

  if (request.answer_with === "text") {
    const others = request.legal_seats.filter((s) => s !== state.seat);
    const who = others[Math.floor(Math.random() * others.length)];
    return `I am still reading the table. Seat ${who} is the one I would watch.`;
  }
  if (request.legal_targets.length) {
    const pick = request.legal_targets[
      Math.floor(Math.random() * request.legal_targets.length)
    ];
    return String(pick);
  }
  return "ok";
}

/* ------------------------------------------------------------------ */

const state = {
  name: "Player",
  playerId: "",
  token: "",
  matchId: "",
  seat: null,
  credential: "",
  mode: "human",
  polling: false,
  pending: null, // the turn we owe an answer to
  deadlineAt: 0,
  // This seat's own conversation. It lives here and nowhere else.
  session: [],
};

/* -------------------------------------------------------------- lobby */

async function boot() {
  $("mode-human").onclick = () => setMode("human");
  $("mode-agent").onclick = () => setMode("agent");
  $("submit").onclick = submitTyped;
  $("say").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) submitTyped();
  });
  setMode("human");
  await refreshLobby();
  setInterval(() => {
    if (state.seat === null) refreshLobby();
  }, 3000);
}

async function refreshLobby() {
  const res = await fetch("/api/open");
  const tables = await res.json();
  const box = $("lobby");
  box.textContent = "";
  $("lobby-empty").classList.toggle("hidden", tables.length > 0);

  for (const t of tables) {
    const row = el("div", "table-row");
    row.append(el("span", "who", t.match_id));
    row.append(el("span", "meta", `${t.seats} seats · ${t.open} open`));
    const btn = el("button", "primary", "Take a seat");
    btn.onclick = () => join(t.match_id);
    row.append(btn);
    box.append(row);
  }
}

async function join(matchId) {
  $("join-error").textContent = "";
  state.name = $("player-name").value || "Player";

  const res = await fetch(`/api/matches/${matchId}/join`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_name: state.name, seats: [state.name] }),
  });
  const data = await res.json();
  if (!res.ok) {
    $("join-error").textContent = data.error || "could not join";
    return;
  }

  state.matchId = matchId;
  state.playerId = data.player_id;
  state.token = data.token;
  state.seat = data.seats[0].index;
  state.credential = data.seats[0].credential;

  $("lobby-view").classList.add("hidden");
  $("table-view").classList.remove("hidden");
  $("seat-badge").textContent = `seat ${state.seat}`;
  setStatus("running", `seated at ${matchId}`);

  state.polling = true;
  pump();
  setInterval(tickDeadline, 250);
}

/* --------------------------------------------------------------- play */

async function pump() {
  while (state.polling) {
    let data;
    try {
      const res = await fetch(`/api/matches/${state.matchId}/poll`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          player_id: state.playerId,
          token: state.token,
          seat: state.seat,
          credential: state.credential,
          timeout_ms: 15000,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      data = await res.json();
    } catch (e) {
      await new Promise((r) => setTimeout(r, 1000));
      continue;
    }

    const msg = data.message;
    if (!msg) continue; // the poll simply timed out; ask again

    receive(msg);
  }
}

function receive(msg) {
  // Everything the server sends goes into this seat's own conversation.
  state.session.push({ role: "user", content: msg.body, kind: msg.type });
  renderFeed(msg);
  renderStats();

  if (msg.type === "GAME_END") {
    state.polling = false;
    setStatus("done", "match over");
    clearTurn("The match is over.");
    return;
  }

  if (msg.reply_required) {
    openTurn(msg);
  }
}

function openTurn(msg) {
  state.pending = msg;
  state.deadlineAt = Date.now() + (msg.deadline_ms || 30000);

  $("turn-box").classList.remove("waiting");
  $("prompt").textContent = lastLine(msg.body);

  const targets = $("targets");
  targets.textContent = "";
  const wantsText = msg.schema && msg.schema.target === "text";
  $("say").classList.toggle("hidden", !wantsText);

  if (wantsText) {
    $("say").value = "";
    $("say").focus();
  } else {
    for (const t of msg.legal_targets || []) {
      const b = el("button", "target", String(t));
      b.onclick = () => {
        [...targets.children].forEach((c) => c.classList.remove("on"));
        b.classList.add("on");
        targets.dataset.chosen = String(t);
        $("submit").disabled = false;
      };
      targets.append(b);
    }
    delete targets.dataset.chosen;
  }
  $("submit").disabled = wantsText ? false : true;

  if (state.mode === "agent") runLinkedAgent(msg);
}

function clearTurn(note) {
  state.pending = null;
  $("turn-box").classList.add("waiting");
  $("prompt").textContent = note;
  $("targets").textContent = "";
  $("say").classList.add("hidden");
  $("submit").disabled = true;
  $("deadline").textContent = "";
}

function submitTyped() {
  if (!state.pending) return;
  const msg = state.pending;
  const wantsText = msg.schema && msg.schema.target === "text";
  const answer = wantsText ? $("say").value.trim() : $("targets").dataset.chosen;
  if (!answer) {
    $("act-error").textContent = "Choose an answer first.";
    return;
  }
  send(answer);
}

async function runLinkedAgent(msg) {
  $("prompt").textContent = "Linked agent is deciding...";
  try {
    const answer = await linkedAgent(buildRequest(msg));
    if (state.pending === msg) send(String(answer));
  } catch (e) {
    // A failed agent is a seat that did not answer. The server's failure
    // ladder handles it, so there is nothing to do but say so.
    $("act-error").textContent = `linked agent failed: ${e}`;
  }
}

/* What a linked agent is handed. This seat's conversation and the ask. */
function buildRequest(msg) {
  return {
    seat: state.seat,
    messages: state.session.map((t) => ({ role: t.role, content: t.content })),
    question: msg.body,
    action: msg.schema ? msg.schema.id : null,
    answer_with: msg.schema ? msg.schema.target : null,
    legal_targets: msg.legal_targets || [],
    legal_seats: livingSeats(msg.body),
    deadline_ms: msg.deadline_ms,
  };
}

async function send(answer) {
  const msg = state.pending;
  if (!msg) return;
  $("act-error").textContent = "";

  const action = { type: msg.schema.id };
  if (msg.schema.target === "text") action.text = answer;
  else action.target = coerce(answer, msg.legal_targets);

  state.session.push({ role: "assistant", content: answer, kind: action.type });
  clearTurn("Answered. Waiting for the table.");
  renderFeed({ type: "YOU", body: `You answered: ${answer}` });
  renderStats();

  await fetch(`/api/matches/${state.matchId}/reply`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      player_id: state.playerId,
      token: state.token,
      seat: state.seat,
      credential: state.credential,
      action,
    }),
  });
}

/* ------------------------------------------------------------ helpers */

function coerce(answer, legal) {
  if (legal && legal.length && typeof legal[0] === "number") {
    const n = parseInt(String(answer).match(/-?\d+/)?.[0] ?? "", 10);
    return Number.isNaN(n) ? answer : n;
  }
  return answer;
}

function livingSeats(body) {
  const m = /Living seats: \[([\d, ]*)\]/.exec(body || "");
  return m ? m[1].split(",").filter((x) => x.trim()).map(Number) : [];
}

function lastLine(body) {
  const lines = (body || "").trim().split("\n").filter((l) => l.trim());
  return lines.slice(-2).join(" ") || "Your turn.";
}

function setMode(mode) {
  state.mode = mode;
  $("mode-human").classList.toggle("on", mode === "human");
  $("mode-agent").classList.toggle("on", mode === "agent");
  $("mode-blurb").textContent =
    mode === "human"
      ? "You read the table and type the answer yourself."
      : "An agent in this browser answers for you. Edit linkedAgent() in play.js to point it at your own model.";
  if (mode === "agent" && state.pending) runLinkedAgent(state.pending);
}

function setStatus(cls, text) {
  $("status").className = `status ${cls}`;
  $("status").textContent = text;
}

function tickDeadline() {
  if (!state.pending) return;
  const left = Math.max(0, state.deadlineAt - Date.now());
  $("deadline").textContent = `${(left / 1000).toFixed(0)}s left`;
  if (left === 0) clearTurn("Time ran out. The server used the default.");
}

function renderFeed(msg) {
  const box = $("feed");
  const card = el("div", `note note-${(msg.type || "").toLowerCase()}`);
  card.append(el("div", "kind", msg.type));
  card.append(el("div", "body", msg.body));
  box.append(card);
  box.scrollTop = box.scrollHeight;
}

function renderStats() {
  const chars = state.session.reduce((n, t) => n + t.content.length, 0);
  $("session-stats").textContent =
    `${state.session.length} turns · about ${Math.round(chars / 4)} tokens · held in this browser`;
}

boot();
