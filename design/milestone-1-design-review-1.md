VERDICT: NEEDS_REVISION

## Summary Assessment

The dispatch model (§3–4) is a genuinely good architectural call and most of the document around it is sound, but the YAML vocabulary in §5 cannot express Secret Hitler — the game the document itself names as the design driver — missing roughly six whole categories of construct, not a few keywords. Separately, the determinism and exact-replay guarantees in §9 do not survive contact with `simultaneous`/`consensus` mode, wall-clock deadlines, summarizer calls, or the unverified sidecar digest.

---

## Critical Issues (must fix)

### C1. The §5 vocabulary cannot express Secret Hitler. Six construct categories are missing.

§5 says "Write Secret Hitler in the YAML before the schema is declared stable." I attempted it. The schema does not survive the first phase. Working attempt with failure points marked: it bottoms out on nomination, before any policy is ever drawn.

What is missing, in dependency order:

**(a) Globals / counters.** There is no top-level `counters:` section and no `set_counter`/`increment_counter` primitive. `set_player_attribute` writes only to seats. Secret Hitler needs `liberal_track`, `fascist_track`, `election_tracker`, `president_index`, and a saved return index for special election. Without these, three of the four win conditions are unwritable: `liberal_track >= 5`, `fascist_track >= 6`, and the Hitler-chancellor condition all reference global state. The only expressible win condition is "Hitler executed" (`count(role == 'hitler' and alive) == 0`). §5's sandbox paragraph mentions "public counters" in the eval context, but counters appear nowhere in the schema, the primitive list, or the visibility model.

**(b) Ordered hidden zones (the policy deck).** There is no way to declare a deck. 6 Liberal + 11 Fascist tiles, shuffled from the match PRNG, drawn 3 at a time, discarded face-down, reshuffled from discard when fewer than 3 remain. `set_player_attribute` cannot hold an ordered list, and the sandbox explicitly forbids subscripting, so a rule cannot even reference `deck[0]`. Needs: a `zones:` declaration (id, ordered, hidden, composition) plus `shuffle_zone`, `draw(zone → dest, n)`, `move_card`, `reveal_zone_to(seat, n)`. Every shuffle and draw must emit an event with `rng_state_after`, or the deck is a silent replay-divergence source (see C3).

**(c) Actions whose argument domain is not a seat.** Every `prompt_action` in the doc targets seats; the move record's own validation error is `"target must be a living seat"`, a hardcoded engine notion. The President discards one of three private cards and the Chancellor discards one of two. There is no way to declare "the argument domain is an element of zone X currently held by seat S", and therefore no way for the gateway to generate the per-dispatch action JSON schema that §8 says is the highest-value part of the system. There is also no event type meaning "you, and only you, now hold these three cards" — the audience model supports it but the vocabulary has no primitive that produces it.

**(d) Guarded transitions and guarded steps.** `next:` is a single static phase id, and `steps` have no `when:`. Secret Hitler's control flow is entirely conditional:
- election passes → (Hitler chancellor ∧ `fascist_track >= 3`) → fascist win; else → legislative session
- election fails → `election_tracker++` → (== 3) → chaos enactment → nomination; else → nomination
- policy enacted → look up the power for this track position *and this player count* → jump to that power phase → return

The last one is a data-driven jump table (5–6 players: peek/exec/exec; 7–8: investigate/special/exec/exec; 9–10: investigate/investigate/special/exec/exec). None of this is expressible. Minimum fix: `next` becomes an ordered list of `{ when: <expr>, goto: <phase> }` with a mandatory default, and `steps` entries accept `when:`.

**(e) Sub-phase call/return.** Presidential power phases must return to the nomination flow, and Special Election must temporarily override the next president then revert to the original rotation. With only a static `next` and no return address, you have to clone the phase graph once per call site. Needs either a `call`/`return` construct or an explicit return-target global (which requires (a) and (d)).

**(f) Offices and rotation.** "The current President" is not a role — it rotates clockwise, skips the dead, and is overridden once by Special Election. The schema has roles and `speaking_order: orchestrator`, neither of which expresses this. The sandbox has no arithmetic operators (whitelist is "literals, names, comparisons, boolean operators, and calls"), so no `(i + 1) % n`. Needs an engine-maintained seat order, an `assign_office(name, seat)` primitive, an `is_president`-style office attribute readable from expressions, and a `next_in_rotation(from, predicate)` helper.

Two smaller but still blocking items:

- **`knows` is unconditional and symmetric.** Real Secret Hitler: Fascists always know Hitler and each other; Hitler knows the Fascists only at 5–6 players. `knows: [mafia]` cannot express either the conditionality or the direction. Minimum: `knows: [{ role: fascist, when: "seats <= 6", direction: one_way }]`, or replace it with a `setup:` step list of guarded `reveal_to` calls.
- **`resolve_majority_vote` is hardwired to elimination** (`on_tie: no_elimination`). The Secret Hitler election resolves to pass/fail with tie=fail, eliminates nobody, and advances a counter. Needs a generic `tally_vote` that writes a counter plus guarded branches, with `resolve_majority_vote` retained as sugar. Note also that "majority" itself needs arithmetic (`count(ja) * 2 > count(alive)`), which the sandbox cannot express — so the majority rule is engine-hardcoded and unconfigurable today.

Also undefined and needed: the win-condition **evaluation moment** (after every primitive? every phase? the Hitler-chancellor win must fire at election resolution and pre-empt the legislative session), and an **`end_game`** primitive — there is none.

**Fix:** do the exercise the doc prescribes, before writing engine code. Land a `games/secret_hitler.yaml` that a reader can follow end to end, and let the vocabulary fall out of it. Expect the primitive list and the schema to roughly double: counters, zones, guarded transitions, guarded steps, offices/rotation, call/return, non-seat action domains, conditional `knows`, generic vote resolution, `end_game`. This is the single largest gap in the design and everything downstream (action-schema generation, the static validator, the expression type system) depends on the answer.

---

### C2. `simultaneous` and `consensus` have no specified commit order, which breaks seeded determinism.

§3 says the orchestrator dispatches one seat at a time and control returns to it. §6 then introduces `simultaneous` ("collects from several seats before revealing any result") and `consensus` ("bounded negotiation until they agree"). The doc never says whether these are concurrent in flight.

**Failure scenario.** `day_voting` dispatches 5 votes in parallel. Seat 4's provider is slow. If sequence numbers are assigned on arrival, the event log interleaving is a function of network latency. The golden-replay test in §11 ("assert an identical event log") is then flaky on the first day of the project, for reasons that look like an engine bug. Worse: if any in-flight dispatch draws from the shared PRNG — ladder step 3 is explicitly "a random legal move" — then draw order is latency-ordered and `rng_state_after` diverges non-reproducibly. A re-run of the same seed produces a different match.

**Fix.** Specify explicitly:
1. **Commit order is independent of completion order.** Responses are buffered; after the barrier, actions are applied in ascending seat index (or a `commit_order` declared in YAML). `seq` is assigned at commit, never at arrival.
2. **No PRNG draws during an in-flight dispatch.** Random defaults and tie-breaks are resolved at commit time, in commit order. Alternatively give each dispatch a deterministic substream derived from `(match_seed, dispatch_seq)` so draw order does not matter.
3. Emit an explicit `barrier` event so replay has an anchor.
4. Timeouts and failures occupy their commit slot with the declared default, so the slot is never skipped.

For `consensus`: it is undefined (Open Question 2 admits the turn budget is unresolved, and "what happens when a faction cannot agree" is unanswered). "Agree" is not defined either — agree on what, detected how, exact equality of a proposed target or a separate confirm action? Under the serialized no-broadcast model it is not a mode at all, it is a loop of sequential dispatches. **Cut it** (see S1); neither Mafia nor Secret Hitler needs it.

---

### C3. Replay can silently falsely pass, and can silently diverge.

§9 claims "re-running a match against its own log reproduces it exactly." Several holes:

**(a) `messages_digest` is recorded but nothing says replay verifies it.** The repair prompt in ladder step 1 contains the validator's error string. Change a validation message between versions and attempt 2's prompt changes — but the replay adapter is keyed by seat and dispatch sequence, so it serves the recorded attempt-2 response regardless and the replay *passes*. You have a green test over a prompt that no longer exists. **Fix:** on every replayed call, recompute `messages_digest` and hard-fail on mismatch. This is the single highest-value line of code in the replay module.

**(b) The replay key is wrong.** The ladder makes multiple provider calls per dispatch. The key must be `(dispatch_seq, attempt)`, not `(seat, dispatch_seq)`.

**(c) Unconsumed keys are not detected.** If the engine stops making a call it used to make, the replay adapter is simply never asked and nothing complains. **Fix:** at end of replay, assert every recorded response key was consumed exactly once.

**(d) `rng_state_after` only appears on move records.** Role assignment, deck shuffles (once C1 lands), and tie-breaks inside `resolve_majority_vote` all consume randomness outside a move and have no digest anchor. Divergence there surfaces many moves later, at the wrong place, defeating the stated "fail loudly at the exact move" property. **Fix:** emit an `rng_draw` event (purpose, value, `rng_state_after`) for every draw, not just moves.

**(e) "Assert an identical event log" is false as written.** `ts`, `latency_ms`, and `cost_usd_estimate` cannot match. **Fix:** define a canonical *replay-relevant projection* of each event (`seq`, `type`, `audience`, `action`, `emitted_event_seqs`, `rng_state_after`, `validation.final_outcome`) and compare that; document which fields are informational.

**(f) No config identity check.** "A match is identified by its seed plus its configuration hash" — but the config hash appears in no logged record. Replay will happily run a recorded log against a modified rule pack and report success or a confusing divergence. **Fix:** see C10.

**(g) Response fidelity.** `finish_reason: "tool_use"` with only `raw_text_ref` recorded. A structured tool-call block will not round-trip through a text file. **Fix:** record the full normalized response object, not just text.

Also worth stating plainly in the doc, because people conflate them: `"seed": null` means *re-running* a match against live providers is not reproducible. Only *replay* is. The §9 claim "deterministic engine tests" is true only in the replay sense.

---

### C4. Summarizer and belief-graph calls are model calls that are not dispatches, so they are unreplayable.

§7 says compression happens "inside the seat's own context" and inferred beliefs are "an extra inference call per turn." §9's replay adapter serves "recorded responses keyed by seat and dispatch sequence." A summarizer call has no dispatch sequence and produces no move record. It is a nondeterministic input to the very next prompt.

**Failure scenario.** A long Mafia match crosses the context budget at dispatch 60. Original run summarizes rounds 1–3 one way; replay has no recording for that call and either calls the live provider (token spend during "no token spend" replay) or crashes. Either way the §11 golden replay is unusable on exactly the long matches that need debugging most.

**Fix:** every model call the engine makes gets a move-like record and a replay key, including summarizer and belief calls. Key them `(dispatch_seq, purpose, n)`. Better for M1: make compression deterministic (rolling window / structured truncation) and ship the LLM summarizer behind the same off-by-default flag as beliefs. See S1.

---

### C5. Wall-clock deadlines are a nondeterministic engine input with no recorded outcome.

`deadline_ms: 30000` is in the dispatch. The validation attempt vocabulary is `schema_error` / `ok` — there is no `timeout` outcome. Under replay, recorded responses are served instantly, so a deadline that fired in the original run never fires in replay, and the match takes a different branch.

Also unspecified: is the in-flight request cancelled at the deadline? If a response arrives after the default action was already applied, is it discarded? If not, you have a race that can apply two actions for one dispatch. Streaming responses truncated at the deadline: discard or parse the partial?

**Fix:** (1) add `timeout` and `transport_error` to the attempt outcome enum; (2) a timeout is a *recorded decision* — replay replays the decision and never re-evaluates the clock; (3) specify that late responses are dropped and logged as `late_response` (informational, excluded from the replay projection); (4) forbid any other wall-clock input to control flow — the overview's §5B "duration timers" must be logical turn counts, not seconds, or replay is dead.

---

### C6. No global termination bound, and `default_action` is named but never declared.

§8 ladder step 3 is "apply the phase's declared default action, such as abstain or a random legal move." No `default_action` key exists anywhere in the §5 schema. It is referenced but undeclared.

**Failure scenario.** Five-seat Mafia. All seats degrade and default to abstain. `resolve_majority_vote: { on_tie: no_elimination }` eliminates nobody. Night: the mafia kill also defaults to abstain. State is unchanged, no win condition fires, `next: night` loops forever. A batch of 100 matches hangs on match 3 with no output. `max_turns: 10` exists on one discussion phase only; there is no match-level bound.

**Fix:** (1) declare `default_action` per `prompt_action` (required, statically validated to be in `legal_actions`); (2) add match-level limits — `max_rounds`, `max_dispatches`, `max_wall_clock_s`, `max_cost_usd` — with a declared terminal outcome (`draw` / `aborted`) written as a `match_end` event; (3) add a degraded-rate circuit breaker: if more than X% of dispatches in a window are degraded, abort with outcome `void` so batch analysis can exclude the match rather than scoring garbage as play.

---

### C7. The visibility invariant is one-sided; under-delivery and starvation are undetectable.

§4's invariant is *received ⊆ entitled*. That is trivially satisfied by delivering nothing. It catches leaks and is blind to the opposite bug.

**Failure scenario.** `speaking_order: orchestrator` never selects Seat 5 during a 10-turn discussion. Seat 5's first sight of all ten turns is the same dispatch in which it must vote — a large, uncompressed, single-shot delta, and a context shape driven purely by turn order. Worse: Seat 5 is eliminated at the end of the night phase before its next dispatch. Under the no-broadcast model a dead seat is never dispatched again, so it never receives its entitled delta at all. The log shows the events with Seat 5 in the audience; `delta_event_seqs` shows they were never delivered. No test fails.

**Fix:** (1) add a completeness invariant — at each seat's final dispatch, and again at match end, `union(delivered) == entitled(up to last dispatch)`, with any residual recorded explicitly as an `undelivered_at_termination` event so the gap is visible rather than silent; (2) bound the delta — if a single delta exceeds the seat's prompt budget, that is an engine-level condition needing a declared policy (compress, truncate-oldest, or fail), not an implicit provider 400; (3) if `speaking_order` can starve a seat, say so and either round-robin as the default policy or add a `min_turns_per_seat`.

---

### C8. "The spectator view is a seat whose audience resolution returns everything" does not work under this model.

§12's claim contradicts §3. A seat receives data only when dispatched, and a dispatch requires "exactly one structured action" in reply. A spectator takes no actions and appears in no `seats:` predicate, so it is never dispatched and receives nothing. Making it work requires either dispatching no-op turns (contradicting the dispatch contract) or a push/tail mechanism — which is the broadcast bus §3 exists to avoid.

**Fix:** for Milestone 1, say the honest thing: the JSONL log *is* the god view, and spectating is tailing it with a renderer. Drop the spectator-as-seat framing. For M2/M3, the correct seam is the one §12 already hints at — separate the payload builder from the dispatch trigger — so an observer can pull a materialized view at any `seq` without a dispatch. Also add `phase_start` / `phase_end` / `match_start` / `match_end` events so a tailing renderer and a batch progress indicator have something to key on; a headless 100-match batch with 30s deadlines currently emits no progress signal at all.

---

### C9. There is no static cross-reference validator, and Pydantic will not give you one.

§1 lists "schema validation." Pydantic validates shapes, not references. Nothing catches: `channels_open: [twon]`, `knows: [detectiv]`, `next: day_votting`, an `action:` name with no declared action schema, an expression free variable that resolves to nothing, `sum(role.count) != seats`, a phase unreachable from the start phase, a `goto` with no matching phase, or a `default_action` not in `legal_actions`.

**Failure scenario.** A typo in `channels_open` silently opens no channel. The mafia never get a night chat. The match runs to completion and looks like bad play. You debug the model.

**Fix:** a named resolution pass after schema parse, with an explicit enumerated check list, surfaced as `xcolos validate <pack>` in the CLI and run in CI over every shipped pack. Every expression is parsed at load time and its free variables resolved against a declared symbol table — no runtime name errors. This becomes load-bearing in Milestone 3 when packs come from strangers.

---

### C10. No log header, no schema version, no config hash; sidecar integrity is unprotected.

The log has no version field and no header. `match_id`, `seed`, `config_hash`, `engine_version`, `context_policy`, and the seat→model bindings appear nowhere as a record (`context_policy` appears per-dispatch, which is redundant and still not authoritative). Golden replay fixtures will rot silently across engine versions.

Sidecars: `messages_digest` protects prompts; `raw_text_ref` and `reasoning_ref` have **no digest**. A response file that is edited, truncated, or lost is undetectable. Write ordering is unspecified — a crash between appending the log line and writing the sidecar leaves a dangling ref.

**Fix:** (1) line 0 of every log is a `match_header` event carrying `log_schema_version`, `engine_version`, `rules_pack_sha256`, `seed`, `context_policy`, seat bindings, and limits; replay refuses to run on a header mismatch with a clear message. (2) Add `raw_text_sha256` / `reasoning_sha256`. (3) Specify write order: sidecar written and fsynced *before* the log line is appended, so a dangling ref is impossible and a torn trailing line is the only crash artifact (which the reader should tolerate by truncation). (4) A log without a `match_end` event is incomplete by definition. (5) Add `xcolos verify <match_dir>`.

---

### C11. The failure ladder conflates transport failure with model failure, corrupting the one metric §8 says matters.

§8 correctly notes that "a large share of apparent losses are malformed or illegal output rather than bad play." But the ladder treats a 429, a 503, and a connection reset identically to a schema violation: repair prompt → retry → default → **degraded**. A provider having a bad ten minutes will mark seats degraded and be indistinguishable in the summary from a model that cannot follow a schema.

**Fix:** two distinct ladders. Transport errors (HTTP 5xx, 429, timeouts at the socket level) get exponential backoff with jitter and a separate retry budget, are recorded as `transport_error` attempts, and do **not** count toward the degraded metric. Only schema/legality failures count. Persistent transport failure escalates to aborting the match as `void`, not to playing a default move — a match where a provider was down is not a data point.

---

### C12. The expression language has two binding scopes and two syntaxes with nothing distinguishing them, and no stated type system.

Compare:
- `members: alive` — a bare name in a seat-set slot
- `members: "role == 'mafia' and alive"` — a per-seat boolean predicate
- `seats: alive` — the same bare name again
- `count(faction == 'evil' and alive)` — an argument that must be a per-seat predicate, evaluated in an implicit per-seat scope
- `when: "count(...) >= count(...)"` — evaluated in a global scope

So `alive` is sometimes a seat-set and sometimes a per-seat boolean, and `count` takes an unquoted predicate that binds a seat variable that is invisible in the source. The same string means different things depending on which key it sits under, with no marker. Authors will get this wrong constantly and the errors will be semantic, not syntactic.

Other gaps: no arithmetic operators are whitelisted (blocks `count(ja) * 2 > count(alive)` and any counter math); `any`/`all` arity and semantics are unstated; `count` over what domain — alive seats, all seats, or a declared collection; behavior on an unresolvable name is unspecified (must be load-time, per C9).

**Fix:** declare a small type system — `SeatSet`, `Bool`, `Int`, `Str` — and give every schema slot a declared type. Make the per-seat binding explicit (`count(seat: seat.faction == 'evil' and seat.alive)` or an equivalent) so the scope is visible in the source. Add arithmetic (`+ - * //`) to the whitelist. Type-check every expression at load time against the symbol table.

---

## Suggestions (nice to have)

**S1. Cut these from Milestone 1.**
- **`mode: consensus`.** Undefined (OQ2), needed by neither reference game, and the primary source of the determinism conflict in C2. Replace with sequential dispatch plus a vote.
- **The claim verifier (§4).** "Checks every factual assertion a seat made" requires NL claim extraction — an unreliable LLM subsystem. As a sanitizer test it is strictly weaker than the deterministic `delta_event_seqs` invariant, which is exact and free. Ship the deterministic invariant; defer the claim verifier to M2 as an analysis tool, not a correctness mechanism.
- **The inferred-beliefs code path.** Already off by default; delete it for M1. It also breaks replay keying (C4).
- **The model-driven speaker selector (OQ1).** Policy only in M1. Keep the interface, skip the implementation. The doc's own reasoning here is correct — commit to it.
- **TypeScript type emission (§2).** A Milestone 2 concern. Generating TS types now freezes the wire schema before it is stable and buys nothing headless. Keep the Pydantic models as source of truth; defer the emit pipeline.
- **LLM-based compression.** Use a deterministic rolling window for M1 (see C4).

**S2. Consolidate sidecars.** One file per prompt and per response attempt means a 10-seat, 200-dispatch match with retries produces ~1000 files; a 100-match batch produces 100k inodes. Use `prompts.jsonl` and `responses.jsonl` per match, referenced by `(seq, attempt)` plus byte offset. Same greppability, one file handle.

**S3. Make the phase schema a tagged union.** `day_discussion` has `speaking_order` + `max_turns` and no `steps`; the others have `steps` and neither. These are two different phase kinds sharing one shape with no discriminator. Add `kind: scripted | discussion`.

**S4. Snapshot the resolved audience eagerly.** §4 defines `resolve_audience(event.audience, state_at(event.seq))`. Implemented literally that requires retaining full historical state, which is expensive and a replay hazard. Resolve at creation time and store the literal seat set on the event; keep the descriptor alongside for audit and for the invariant test. State this explicitly — it is the difference between an O(1) and an O(history) visibility check.

**S5. Make `emit_event`'s audience mandatory.** §3's fail-closed argument only holds if there is no default. An omitted audience must be a load-time error, never an implicit `all`. Also reconcile naming: the overview says `broadcast_event`, §6 says `emit_event`, §3 says nothing is ever broadcast. Pick one and note the rename in the overview addenda.

**S6. Keep model bindings out of the rules pack.** The YAML has no model references today, which is correct, but say so normatively — rule packs must be portable and, in M3, untrusted. Seat→model binding belongs in the run config.

**S7. Role assignment needs stated constraints.** The overview promises "role assignment constraints"; §5 offers only `count`. At minimum specify that assignment is independent of seat model binding, that it draws from the match PRNG, and that batch runs support counterbalancing (rotating which model gets which role across seeds), since otherwise a 100-match batch confounds role with model. `max_turns: 10` also needs defining: total dispatches in the phase, or per seat?

**S8. Define `reveal_to`'s granularity.** Secret Hitler's investigate reveals *party membership*, not role — Hitler shows as Fascist. So `reveal_to` must take a field selector (`faction`), not reveal a whole role. Once-per-game targeting is fine via `set_player_attribute`.

**S9. Per-match cost cap.** `cost_usd_estimate` is logged but never enforced. §8's seat token budget and the dispatch `prompt_tokens_budget` have no stated overflow behavior. For a batch CLI this is a real footgun; add `max_cost_usd` with a hard abort (see C6).

---

## Verified Claims (things I confirmed are correct)

- **The fail-closed argument in §3 is sound.** Additive selection genuinely does fail closed where subtractive redaction fails open, and the claim that adding a new field cannot leak is correct *given* S5 (mandatory explicit audience). This is the strongest idea in the document.
- **Serializing group conversation is a real simplification, not a dodge.** Dispatching mafia seats one at a time with the prior message included collapses faction chat and town discussion into one mechanism with different audience sets. No state is lost relative to a room model, and it removes the hardest concurrency case outright.
- **Audience-resolved-at-creation is the right semantics.** A message to the mafia channel staying visible to the then-members after an elimination is correct, and it also correctly prevents a later channel joiner from seeing backlog.
- **The move record shape is good.** Recording every ladder attempt separately is the right call and directly supports the §8 claim about malformed output being mistaken for bad play. `delta_event_seqs` as the audit anchor for both the visibility invariant and the claim verifier is a clean piece of design.
- **PRNG in game state rather than module globals** is correct and is the necessary precondition for everything in §9.
- **The replay adapter satisfying the model adapter interface** is the right seam — it makes replay a configuration choice rather than a separate code path.
- **The testing strategy in §11 is well chosen**, particularly scripted baseline seats. A rule-based agent that plays adequately with zero model calls is the cheapest possible way to get the engine under continuous test, and it is the thing that would have surfaced C6 immediately.
- **§5's own prediction is accurate.** "The policy deck with secret draws and discards, the chained presidential powers, the special election, and veto unlocking are what will actually break the vocabulary." That is exactly what happens — the document correctly identified the risk and then shipped the schema without running the test it prescribed. C1 is the cost of that gap, not a disagreement with the author's judgment.
