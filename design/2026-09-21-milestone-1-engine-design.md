# XColos Milestone 1 Design: Local AI Engine

**Status:** Draft, revision 2
**Date:** 2026-09-21
**Scope:** Milestone 1 only. Milestones 2 and 3 appear solely as forward-compatibility constraints.

> Revision 2 restructures the system into three layers, introduces the generic message
> protocol, and replaces the deterministic rule interpreter with a hybrid LLM orchestrator
> over a strict kernel. See section 18 for what changed and why.

---

## 1. Scope

Milestone 1 delivers a headless runtime that plays a full hidden-role social deduction match with every seat occupied by an LLM, driven by a game file, and writes a fully replayable transcript.

**In scope**

- The kernel: message protocol, state model, visibility enforcement, turn bookkeeping, recording
- The orchestrator: reads the game file, drives flow, issues validated directives
- Uniform agent interface with an in-process transport
- Strict structured-action contract and failure ladder
- Append-only event log, seeded determinism, record and replay of every model call
- A command line entry point to run one match or a batch

**Out of scope**

- Web UI, human seats, typing pacing (Milestone 2)
- Lobbies, network transports, remote agents, matchmaking (Milestone 3)
- Leaderboards and rating computation

**Non-goals**

- A general game description language. See section 8.
- Agent quality. The runtime supplies the smallest viable scaffold and stays out of the way.

### Staging

Milestone 1 splits in two, and the split exists to keep the hard part honest.

**Stage 1a, the system.** One game is hardcoded in Python behind the orchestrator interface. No game file, no parsing, no LLM orchestrator. This proves the kernel, the message protocol, the turn loop, visibility, and recording, with everything deterministic and free to run. A scripted baseline agent means a full match costs nothing.

**Stage 1b, the game file and the LLM orchestrator.** Section 8 lands here. The hardcoded orchestrator is replaced by one that reads a YAML template, and it implements the same interface, so nothing below it changes.

Doing 1a first means the kernel's guarantees are tested before any nondeterminism enters the system. If visibility or replay is wrong, it is wrong deterministically and a test catches it. Adding an LLM first would mean debugging the kernel and the model at the same time.

---

## 2. Decisions

| Decision | Choice |
|---|---|
| Engine language | Python |
| Client language | TypeScript, Milestone 2 onward |
| Orchestrator | LLM, constrained by a deterministic kernel |
| Game file | One YAML template. Declarative fields the kernel parses, prose fields the LLM reads |
| Rule execution | The LLM calls system functions as tools, once per turn |
| Turn model | Strictly turn-based, one agent acts at a time |
| Delivery | Eager push to every entitled agent, not lazy pull |
| Message types | Generic, owned by the kernel, not by the game |
| Agent interface | Synchronous. Nothing is ever in flight concurrently |
| Orchestrator shape | Yields an action request, is sent back the action |
| Rendering | Per-seat, from templates. No model call in the delivery path |
| Persistence | Append-only JSON Lines log per match, no database |
| Log purpose | Observation and debugging only. Not read back at runtime |
| Replay | Deferred. Revisit only if errors start appearing |
| Model transport | Wrap an existing multi-provider gateway, do not build one |

The same design must serve a local single-process run and an online multi-agent battle. Nothing above changes between the two. Only the transport behind the agent interface changes, so the protocol is specified before the internals.

---

## 3. Three layers

**The kernel (game-agnostic).** Owns the message type taxonomy, the state model, the event log, turn bookkeeping, visibility enforcement, and the agent transport. It knows nothing about Mafia or Secret Hitler. It knows about seats, turns, facts, audiences, zones, and offices. It is deterministic code, and it is the only component trusted with secrets.

**The orchestrator (game-aware).** Reads the game file, understands the rules, and decides what happens next. It is an LLM. It never talks to an agent directly and never writes to state directly. It issues structured directives to the kernel, which validates and executes them.

**The agents (seats).** Receive typed messages and return typed responses. A uniform interface with no knowledge of the game beyond what the kernel tells them.

```
        game file
            |
            v
      +-------------+   directives    +-------------+
      | ORCHESTRATOR | -------------> |   KERNEL    |
      |    (LLM)     | <------------- | (det. code) |
      +-------------+   state digest  +------+------+
                                             |
                          typed messages     |  (kernel is the only
                       +---------------------+   component that ever
                       |          |          |   touches an agent)
                       v          v          v
                    Agent 1    Agent 2    Agent N
```

The critical property: the orchestrator decides, the kernel enforces. An orchestrator that hallucinates a rule, targets a dead seat, or tries to send a secret to the wrong audience is rejected by the kernel, and the rejection is recorded.

---

## 4. Message protocol

Message types are generic and defined by the kernel. A game never invents a message type. This is what keeps one agent implementation playing every game, and what lets a local agent and a remote agent share one contract.

### Kernel to agent

| Type | Response expected | Purpose |
|---|---|---|
| `GAME_START` | no | Game explanation, your seat, your role, private setup knowledge, the response format you must use |
| `SITUATION` | no | Something happened that you are entitled to know. Wait for your turn. |
| `YOUR_TURN` | yes | What the situation is, what you may do now, what you must answer, and by when |
| `GAME_END` | no | Outcome, final reveals |

### Agent to kernel

| Type | Purpose |
|---|---|
| `ACTION` | A structured action conforming to the schema the turn request declared |
| `ERROR` | The agent could not act |

Only `YOUR_TURN` costs an inference call. A `SITUATION` appends to the agent's context and returns immediately, so pushing an update to every entitled agent after each move stays cheap. This is what makes eager delivery affordable.

### Kernel to orchestrator

| Type | Purpose |
|---|---|
| `DECIDE` | Here is the current state digest and what just happened. What should happen next? |

### Orchestrator to kernel: the system functions

These are the system's function library, exposed to the orchestrator as tool definitions. The LLM drives the game by calling them. It has no other way to affect anything. This list is fixed and game-agnostic, which is what lets one orchestrator run any game.

| System function | Effect |
|---|---|
| `request_action(seat, schema, deadline)` | Send `YOUR_TURN` to one named seat |
| `request_action(where, schema, deadline)` | Send `YOUR_TURN` to every seat matching a predicate, in index order |
| `next_in_rotation(skip)` | Advance the rotation cursor to the next eligible seat and return it |
| `set_rotation_cursor(seat)` | Move the cursor, for special elections and similar overrides |
| `emit_fact(payload, audience)` | Record a fact and push `SITUATION` to its audience |
| `set_global(key, value)` | Update a counter or flag |
| `zone_op(op, zone, args)` | Draw, discard, shuffle, peek, move between zones |
| `assign_office(office, seat)` | Set the holder of a named office |
| `set_attribute(seat, key, value)` | Update a seat attribute |
| `eliminate(seat)` | Remove a seat from play |
| `end_game(winner, reason)` | Terminate the match |

Every call is validated against the frozen manifest before execution: the seat exists and is alive when required, the zone exists and holds enough tokens, the office was declared, the audience is expressible, and the action schema is one the manifest defines. A rejected call is recorded and returned to the orchestrator as a tool error, with a bounded retry budget before the match is abandoned. The orchestrator can therefore be wrong, but it cannot be wrong silently and it cannot be wrong in a way that corrupts state.

---

## 5. Turn loop and ordering

The game is always turn-based. One agent acts at a time. There is no simultaneous mode.

```
loop:
  kernel  -> orchestrator : DECIDE(state digest, last event)
  orchest -> kernel       : directive[]
  kernel                  : validate, execute, append events
  kernel  -> agents       : SITUATION to each entitled seat   (no inference)
  kernel  -> one agent    : YOUR_TURN                          (one inference)
  agent   -> kernel       : ACTION
  kernel                  : validate action, append move record
  until end_game or turn cap reached
```

Strict sequencing gives a total order by construction. Sequence numbers are assigned by the kernel at execution time, not by message arrival, so nothing depends on latency and golden replays cannot be flaky.

### Seat registry

At registration each agent is assigned a fixed integer index. It is assigned once, never reused within a match, and never changes. The index is the agent's identity in every message, so seats refer to each other by number. Display names and personas are metadata that never affect ordering, which keeps turn order independent of anything an agent controls.

The kernel maintains per seat:

| Field | Values |
|---|---|
| `index` | Immutable integer, assigned at registration |
| `status` | `active`, `eliminated`, `abandoned` |
| `eligibility` | Per-phase flags such as `silenced` or `blocked`, for a living seat that may not act right now |
| `degraded_streak` | Consecutive failed turns, feeding the termination bound |

Skipping is a predicate over these fields rather than a single dead flag, because a living player who is silenced this round must be skipped without being eliminated.

### Turn selection

The kernel owns a rotation cursor and offers three deterministic ways to choose who acts next. The orchestrator picks the mode, the kernel computes the seat.

| Mode | Used for |
|---|---|
| **Rotation.** Advance the cursor to the next eligible seat | Discussion rounds, presidency rotation |
| **Named seat.** The orchestrator names an index | A president nominating a chancellor |
| **Filtered set.** Every seat matching a predicate acts, in index order | Night actions, voting |

The cursor survives phase transitions. That is what makes presidency rotation expressible without the orchestrator doing modular arithmetic, and what lets a special election move the cursor and later revert it.

**Free discussion default.** One pass in index order per round, bounded by a turn cap. The orchestrator may grant an extra turn by naming a seat, which covers letting an accused player respond. Nothing about ordering depends on latency, on model output, or on arithmetic the LLM has to get right, so discussion order is reproducible.

### Voting is not a kernel concept

There is no vote primitive, no tally function, and no majority resolver in the kernel. A vote is an ordinary action schema, and asking for one is an ordinary message. The word "vote" is content, not machinery.

What follows from that is the important part. Why a vote is needed, what counts as a result, what a tie means, and what happens next are all decided by the orchestrator from the game's own rules. A game where ties re-run, or where the chair breaks them, or where a vote merely advises, needs no kernel change.

Mechanically this makes a vote a run of consecutive turns with results withheld. Each answer is recorded as a fact visible only to the seat that gave it, and the orchestrator emits the tally as one public fact once every voter has acted. That is also how this design does anything that looks simultaneous elsewhere.

The same reasoning rules out a kernel-maintained record of vote history and public claims. The orchestrator decides what a seat is told and when.

**Termination.** Two bounds, both hard. A per-match turn cap, and a consecutive-degraded-turn cap. Hitting either ends the match with an `abandoned` outcome rather than looping forever.

---

## 6. The Game object and the kernel state model

### The Game object

One object holds an entire match: its process, its state, and its log. It is the aggregate root, the only thing a runner needs, and the unit that gets serialized, replayed, and inspected.

| Holds | Contents |
|---|---|
| **Identity** | Match id, seed, game id, manifest hash |
| **State** | Seats, globals, zones, offices, the PRNG, the rotation cursor |
| **Process** | Turn sequence, round number, run status, outcome |
| **Logging** | The append-only fact log and every move record |

The system functions are methods on this object. Nothing else may write to it. That is what makes the kernel's guarantees checkable in one place rather than spread across the runtime.

Two rules keep it honest. Every mutation goes through a system function, so nothing changes without being validated and recorded. And the object exposes a read-only digest for the orchestrator and a per-seat view for agents, never itself, so no caller can reach past the visibility layer to the raw state.

### State constructs

The kernel provides general state constructs so the orchestrator never needs an escape hatch. These exist because a review attempt to express Secret Hitler found each one missing.

**Globals.** Named scalars and counters. The liberal and fascist policy tracks, the election tracker, the veto-unlocked flag.

**Zones.** Ordered collections of opaque tokens, each with a visibility rule. The policy deck is an ordered hidden zone, a discard pile is an ordered hidden zone, a president's drawn cards are a zone visible to one seat. Zone operations are kernel primitives, so shuffling draws from the seeded PRNG and is reproducible.

**Seats.** Identity, alive flag, role, and arbitrary attributes.

**Offices.** Named slots holding a seat reference, with rotation helpers. The presidency is an office, not a role. This is what makes "the current President" addressable and makes special elections expressible.

**Facts.** The append-only event record. Every fact carries an audience descriptor.

Action targets are not restricted to seats. A target domain may be a seat, a zone position, a token, an office, or an enumerated choice, which is what lets a president discard one of three private cards.

---

## 7. Visibility

Visibility is a selection relation, not redaction. Every fact carries an audience produced when the fact is created, resolved against the state as it stood at that moment.

```
sees(seat, fact) := seat ∈ resolve_audience(fact.audience, state_at(fact.seq))
```

A message sent to the mafia channel stays visible to whoever was in that channel then, even after someone is eliminated.

### The orchestrator leak problem

The orchestrator sees everything. If it also authored the prose sent to agents, one careless sentence would leak a secret and no deterministic check could catch it, because the kernel cannot judge meaning.

**The fix is a two-stage composition.** The full-view orchestrator decides only *what happens*, and emits it as structured facts with explicit audiences. It never writes text that reaches an agent. A separate per-recipient renderer turns entitled facts into the prose that agent receives, and that renderer runs with only that recipient's entitled subset in its context. It cannot leak what it was never given.

This is the same fail-closed argument as the selection model, applied one layer up. It costs one cheap render call per recipient per update, and the renderer can be a small model or a template for most fact types.

**Invariant, enforced by test.** For every seat, the set of facts that seat received equals the set of facts whose audience includes it. Equality in both directions. A subset test alone would pass silently when a seat dies before delivery and never receives what it was owed.

**Known side channels.** Each needs a specific guard.

- A prompt cache shared across seats. Key it by seat.
- Any summarizer or renderer reading global state. Both run inside a seat's context.
- Retry and error text echoing rejected content to the wrong seat.
- Token count as a side channel. Accepted for now, revisit at Milestone 3.

---

## 8. The game file

> **Deferred to stage 1b.** Stage 1a hardcodes one game in Python behind the orchestrator
> interface. This section is the target shape, not the immediate build.

A game is one YAML file following a fixed template. The template has two kinds of field, and the split is the whole design.

**Declarative fields** are parsed directly by the kernel. No model is involved. They enumerate everything the kernel must validate against: roles, offices, zones, globals, and action schemas. They become the frozen manifest.

**Prose fields** are human language, read by the orchestrator each turn. Phase flow, powers, branching, and win conditions live here, because these are what a formal language cannot express without becoming a bad programming language.

Neither half works alone. Prose alone leaves the kernel nothing to validate against, so a call naming a nonexistent office could not be rejected and the kernel's strictness would evaporate. Declarations alone recreate the rule language that could not express Secret Hitler.

### The template

```yaml
meta:
  id: secret_hitler
  name: Secret Hitler
  seats: { min: 5, max: 10 }

# ---------- declarative: kernel-parsed, becomes the frozen manifest ----------

roles:
  - id: liberal
    faction: liberal
    counts: { 5: 3, 6: 4, 7: 4, 8: 5, 9: 5, 10: 6 }
  - id: fascist
    faction: fascist
    counts: { 5: 1, 6: 1, 7: 2, 8: 2, 9: 3, 10: 3 }
    knows: [fascist, hitler]           # sees these roles at setup
  - id: hitler
    faction: fascist
    counts: { 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1 }
    knows_if: { seats_max: 6, knows: [fascist] }   # one-way, size-conditional

offices:
  - { id: president, rotates: true }
  - { id: chancellor }
  - { id: last_president }
  - { id: last_chancellor }

zones:
  - id: policy_deck
    ordered: true
    visibility: none
    initial: { liberal: 6, fascist: 11 }
    shuffle_on_init: true
  - { id: discard, ordered: true, visibility: none }
  - { id: president_hand, ordered: true, visibility: holder }
  - { id: chancellor_hand, ordered: true, visibility: holder }

globals:
  liberal_track: 0
  fascist_track: 0
  election_tracker: 0
  veto_unlocked: false

actions:
  - { id: speak,           target: text,                          default: pass }
  - { id: nominate,        target: seat,                          default: first_eligible }
  - { id: vote,            target: enum[ja, nein],                default: nein }
  - { id: discard_policy,  target: zone_position(president_hand), default: random }
  - { id: investigate,     target: seat,                          default: random }
  - { id: execute,         target: seat,                          default: random }

# ---------- prose: read by the orchestrator each turn ----------

rules:
  overview: |
    Secret Hitler is a hidden-identity game. Liberals outnumber fascists but do
    not know who anyone is. Fascists know each other...

  turn_flow: |
    Each round the presidency passes to the next living player in seat order.
    The president nominates a chancellor, who may not be the previous elected
    chancellor, nor the previous president when six or more players remain...

  powers: |
    Presidential powers trigger on the fascist track and depend on player count.
    With seven or more players, the third fascist policy grants investigation...

  win_conditions: |
    Liberals win when five liberal policies are enacted, or Hitler is executed.
    Fascists win when six fascist policies are enacted, or Hitler is elected
    chancellor once three or more fascist policies are on the board. Check the
    Hitler-as-chancellor condition immediately after a successful election,
    before any legislative session begins.

  edge_cases: |
    If the election tracker reaches three, the top policy is enacted immediately
    with no presidential power and no veto, and term limits reset...
```

### Loading a game

1. **Parse.** The kernel reads the declarative sections directly. Deterministic, free, no model call.
2. **Cross-check.** A one-time model pass reads the prose and reports every noun it references that the declarative sections do not define. An unresolved reference is an authoring error surfaced before the first match, not a mystery on turn forty.
3. **Freeze and hash.** The manifest is frozen. The hash joins the seed in match identity, so two matches are comparable only when built from the same file.

Runtime declaration is allowed only where the template marks a type extensible, such as ad-hoc private channels. Everything else is closed.

### What this costs

Rule fidelity is not guaranteed by construction. It is bought by testing. Every game needs a conformance suite of scripted scenarios with known-correct outcomes, run against the real orchestrator. That suite, not the prose, is the operational specification of correct play. Budget it as a deliverable. It is the only thing standing between prose rules and a game that quietly plays itself wrong.

---

## 9. Client and server

### The split

**Agents live on the client.** A client registers the seats it owns, holds their model configuration or their human interface, and handles the actual message traffic to them.

**Everything authoritative lives on the server.** State, the orchestrator, every decision, and the log. The client sends everything back; the server decides and records.

The boundary is exactly the agent interface, which is why nothing in the layers above has to change:

```python
class AgentHost(Protocol):
    """A client. Hosts one or more seats and relays messages to them."""

    def register(self, server) -> list[SeatBinding]: ...
    def deliver(self, env: Envelope) -> Action | None: ...
```

A client is a remote implementation of that protocol hosting several seats. A local run is an in-process implementation hosting all of them. One code path, two deployments.

### What each side owns

| Server | Client |
|---|---|
| Authoritative state and all mutations | Agent configuration and credentials |
| The orchestrator and every decision | Message traffic to its own agents |
| Seat index assignment and turn order | Local presentation, for a human seat |
| Audience resolution and rendering | Nothing authoritative |
| Sequence numbers and the log | A cache at most |

The client never decides anything. It cannot skip a turn, reorder, or invent state. Its only power is to answer, badly or not at all, and the failure ladder already covers both.

### The trust boundary is the seat, not the client

The server's unit of entitlement is the seat. A client hosting several seats necessarily sees the union of what those seats are entitled to. That is fine when one operator owns all of them, and it is exactly what a local run is. It is a leak when the seats belong to different people.

So the rule is: **a client may host multiple seats only when one principal controls them all.** Online, a competitor's seats belong on their own client. This is the one place where local and online differ in trust despite sharing a protocol, and it should be enforced at registration rather than assumed.

Registration therefore issues a per-seat credential. A reconnecting client proves it owns seat three; it cannot ask for seat five's traffic.

### Disconnection and resume

Delivery is eager push, so a client that drops misses pushes. The server already tracks, per seat, how far delivery has reached, which is exactly the cursor a resume needs. On reconnect the server pushes that seat's undelivered entitled facts and play continues.

A disconnect during a seat's own turn is a transport failure, and it enters the failure ladder one tier above a malformed answer: wait for the deadline, then apply the declared default and mark the turn degraded. Seat status gains `disconnected` alongside `active` and `eliminated`, so a dropped client is skipped without being eliminated.

Because the turn model is strictly sequential, only one response is ever outstanding. Nothing about ordering depends on which client answers first, and the server stamps every sequence number itself.

### What goes over the wire

A dispatch carries both the structured entitled facts and the rendered prose. Both are filtered identically, so neither leaks. An LLM seat reads the prose; a human client builds an interface from the structure. Sending only prose would make a good human client impossible, and sending only structure would push rendering to the client, where it would sit outside the entitlement boundary.

Agents never talk to each other. There is no peer channel. A client relays only between the server and its own seats.

### The operator console

The first surface built on this split is an operator console: a local web UI to build a table, choose a game, press play, and watch the match run.

It is deliberately **not a player's client.** It holds the full view, the way a spectator seat does, and it shows every seat's role. A player-facing client, where one person occupies one seat and sees only what that seat is entitled to, is a different surface and belongs to Milestone 2. Conflating them would put a full-information UI in front of someone who is supposed to be guessing.

The console holds no game state. It posts a table, then polls the match log and renders records. That is the same discipline a real client follows, and it is only possible because the log is complete.

Three views read the same records. A timeline of what happened, marking which facts were secret and to whom. Every message in both directions. And a per-seat view showing exactly what one seat was sent, which makes the entitlement model something you can look at rather than take on trust.

**Pacing lives on the client.** A match with scripted agents finishes in milliseconds, which is unwatchable, so the console delays before answering a turn. A slow agent is a slow client. The kernel neither knows nor cares, which is the same reason a real model's latency needs no special handling.

### Transport

In-process for stage 1a. WebSocket for a connected client, and an HTTP webhook for a bring-your-own-model seat that prefers to be called. The envelope is versioned from the first commit, because Milestone 3 exposes it to third-party implementations that will lag behind the server.

**Seat binding.** A seat maps to a model identifier, sampling parameters, a system prompt, a persona, and a token budget. The binding lives on the client; the server knows only that the seat exists and answers.

**Action contract.** Every `YOUR_TURN` declares a JSON schema for the legal action. Responses are validated against it. This is where real engineering effort goes, because in prior benchmarks a large share of apparent losses were malformed output rather than bad play.

**Failure ladder.** Applied in order, every step recorded.

1. Validation fails, so send a repair prompt containing the validation error and nothing else.
2. Retry up to a bounded count.
3. Apply the default action declared in the game file header for that schema.
4. Mark the turn degraded and continue.

A match never stalls on a bad response. When step three draws randomly it draws from the seeded PRNG at a point fixed by turn order, not by arrival time.

**Token accounting is ours.** Count locally rather than trusting a gateway's reported usage.

---

## 10. The log

**The log is not in the gameplay path.** Nothing in the runtime reads it back. It exists for observation, debugging and analysis. Replay is explicitly not a near-term goal: the assumption is that runs succeed, and reconstructing a match from its log is something to reach for only if errors start appearing.

That makes completeness the requirement, not reproducibility. Because the log is the only durable record, anything absent from it is gone. And because nothing reads it, no test fails when it drifts, so its structure has to be asserted directly.

**Format.** One JSON Lines file per match, append-only. The log is the god view: it holds every secret, and entitlement is a field on each record rather than a filter applied to the file.

**Every record has the same leading shape**, so a file can be scanned, filtered, and diffed without knowing any specific record type.

| Field | Meaning |
|---|---|
| `log_seq` | Monotonic from zero, unique per line |
| `ts` | Wall clock, for humans, never read by the runtime |
| `category` | The coarse bucket, from the fixed list below |
| `type` | The specific event within that bucket |
| `round`, `phase`, `turn_seq` | Where in the match this happened |

Fields are written in insertion order rather than sorted, so the identifying fields come first when a human reads the file.

**Categories are a small fixed vocabulary**, because filtering by category is the first thing anyone reading a log wants to do.

| Category | Contents |
|---|---|
| `setup` | Seats registered, roles assigned, zones and offices declared |
| `process` | Phase and round transitions, start, termination |
| `state` | Mutations to seats, globals, zones, offices |
| `fact` | Something happened, with the audience entitled to know it |
| `delivery` | Which facts were pushed to which seat |
| `orchestrator` | What the orchestrator asked for, and why |
| `message` | Every envelope out to a seat, every response back |
| `turn` | The move record, one per turn, end to end |
| `result` | The final summary, including the role reveal |

**What completeness means here.** Every state change, every fact with its audience, every orchestrator request with the reason that seat was chosen, every envelope sent to a seat with its rendered body, and every response returned including the ones rejected by the repair ladder. The log alone explains what each seat was told and what it said back.

**The move record** captures one turn end to end: what the seat was shown, what was asked of it, every attempt through the failure ladder, how it resolved, and the generator state afterwards. A seat that played badly is therefore distinguishable from one that could not produce valid output at all.

**Two structural guarantees, both enforced.**

1. Every record survives a round trip through its own file. This is checked when the record is written, because the usual failure is an integer dictionary key, which JSON silently turns into a string so that the file and memory disagree.
2. A validator checks any log for contiguous sequence numbers, known categories, required fields, deliveries that reference real facts, and the presence of a result record.

**Views, not formats.** One structured record supports many readings. A timeline groups everything by round and phase. A per-seat transcript shows exactly what one seat was sent and replied, which is also the sharpest leak check available: if a seat's whole world contains something it was not entitled to, the kernel leaked.

**Seeded randomness.** The generator state lives inside game state, not module globals, so role assignment, shuffles, ordering and random defaults all draw from it. Wall-clock stamps are the only field that differs between two runs of the same seed, which is asserted by test.


## 11. Module layout

```
xcolos/
  kernel/     state model, zones, offices, facts, audience resolution, turn loop
  protocol/   message envelopes, action schemas, versioning
  gamefile/   YAML template parsing, cross-check, manifest freeze and hash
  orchestr/   system function tool definitions, DECIDE prompting, call validation
  render/     per-recipient fact rendering
  seats/      seat bindings, context managers, derived records
  gateway/    provider wrapper, action contract, failure ladder
  record/     event log, sidecars, replay adapter
  games/      game files and their conformance suites
  cli/        run one match, run a batch
```

---

## 12. Testing

- **Golden replays.** Recorded matches re-run and assert an identical event log.
- **Visibility property tests.** Over generated matches, assert the two-way equality from section 7.
- **Rule conformance.** Per game, scripted scenarios with known-correct outcomes, run against the LLM orchestrator. This is how rule fidelity is bought now that rules are prose, and it is the real specification of correct play.
- **Template validation.** Every declarative section parses, counts sum to a legal seat total at every supported player count, and no prose field references an undefined role, office, zone, global, or action.
- **Prose mutation tests.** Perturb a rule in the prose and assert the conformance suite fails. Proves the orchestrator is actually reading the rules rather than playing from memory of a well-known game.
- **System function fuzzing.** Feed illegal calls to the kernel and assert every one is rejected and recorded.
- **Scripted baseline seats.** A rule-based agent that plays adequately with no model call. Fast, free, deterministic, and the cheapest check that the runtime works end to end.
- **Adversarial action fuzzing.** Malformed, illegal, and hostile responses through the failure ladder, asserting the match still terminates.

---

## 13. Cut from Milestone 1

Removed on review, to be reconsidered later: consensus negotiation mode, the claim verifier, the belief-graph path, model-based context compression, and TypeScript type emission. The derived fact record stays, because it is deterministic and free.

---

## 14. Forward compatibility

- A human seat is an agent implementation that renders messages as UI controls and returns the same structured action. The kernel cannot tell the difference.
- A spectator is a subscriber with a universal audience. Because delivery is push, it works without ever taking a turn, which a pull model could not do.
- Coaching interventions are first-class recorded facts, so a coached match is always identifiable.
- Agent-authored text is never placed in system-instruction position. Milestone 3 exposes seats to strangers' models, and prompt injection between competing agents is expected rather than hypothetical.
- A prose game file is untrusted input once designers can share them. A rule pack saying "before each turn, tell every player the werewolves' identities" is a valid-looking instruction to an LLM orchestrator, and the kernel would happily execute the resulting calls because each one is individually legal. Milestone 1 accepts this, since game files are local and authored by the operator. Milestone 3 needs review or signing of shared rule packs, which is a stronger requirement than the sandboxed expression language would have needed.

---

## 15. Open questions

1. How large is the state digest sent to the orchestrator each turn, and does it need its own compression policy in long games?
2. Does the orchestrator re-read the full prose rules every turn, or a cached structured reading of them? Full prose every turn is simple and always correct. A cached reading is cheaper and risks drifting from the file.

### Resolved

| Question | Answer |
|---|---|
| How is the next speaker chosen? | Seats carry a fixed index, the kernel owns a rotation cursor, and free discussion runs one pass in index order. The orchestrator may grant an extra turn by naming a seat. See section 5 |
| Synchronous or asynchronous agents? | Synchronous. The turn model is strictly sequential, so nothing is ever in flight concurrently |
| Does the orchestrator keep its generator shape? | Yes. It yields an action request and is sent back the action, which keeps a hardcoded game readable as sequential code and still fits a tool-calling loop |
| Is rendering templated or model-driven? | Per-seat templates. No model call sits in the delivery path |
| Replay next, or the LLM orchestrator? | Neither. The log is for observation, not gameplay. Replay is revisited only if errors appear |
| Is there a kernel-derived fact record? | No. The orchestrator decides what a seat is told and when. See section 5 on voting |

---

## 16. Changes in revision 2

| Change | Reason |
|---|---|
| Split engine into kernel, orchestrator, and agents | The kernel must stay game-agnostic so one agent implementation plays every game, locally and online |
| Orchestrator is an LLM over prose rules | A formal rule language could not express Secret Hitler. See section 8 |
| Games are one YAML template, declarative fields plus prose fields | Prose alone leaves the kernel nothing to validate against. Declarations alone cannot express Secret Hitler |
| Directives reframed as system functions exposed as tools | The LLM drives the game by calling them and has no other way to affect state |
| Seats get a fixed index at registration, with status and eligibility | Turn order becomes kernel-computed and reproducible, and the LLM never does arithmetic |
| Kernel owns a rotation cursor that survives phase changes | Makes presidency rotation and special elections expressible without orchestrator arithmetic |
| Added the generic message protocol | Message types are system-owned, which is what makes the agent contract uniform |
| Delivery corrected from lazy pull to eager push | Agents are told the situation when it happens, then told to wait |
| Voting demoted from a primitive to an action schema | A vote is message content. Why one happens and what follows is game content the orchestrator reads |
| Dropped the kernel-derived fact record | Same reason. The orchestrator decides what a seat is told |
| Log repositioned from replay substrate to observation record | Nothing reads it back at runtime, so the requirement is completeness and clarity, not reproducibility |
| Milestone 1 split into stages 1a and 1b | Prove the kernel deterministically before any model enters the system |
| Removed simultaneous and consensus modes | Strictly turn-based play gives a total order and removes replay flakiness |
| Added globals, zones, offices, and non-seat targets | Each was found missing when Secret Hitler was attempted |
| Added two-stage rendering | Closes the leak an all-seeing LLM orchestrator would otherwise introduce |
| Replay now verifies digests and unconsumed keys | Replay could previously pass while serving stale responses |
| Every model call has a replay key | Orchestrator and renderer calls were previously unreplayable |
| Added hard turn and degradation caps | An all-degraded match could previously loop forever |
| Visibility invariant is now two-way equality | The subset form missed undelivered entitled facts |
