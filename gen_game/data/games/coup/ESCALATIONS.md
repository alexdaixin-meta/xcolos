
2026-10-12 ## Play review of match w0002 (4 seats, suggested size): infra finding, waiting for a decision

**What happened.** The ending announcement told seat 1 the literal text `false`. Seats 2, 3 and 4 got proper summaries. The platform's own result and seat statuses were correct.

**Cause, checked in the log.** The game file's ending `llm` asks the model to "quote the final hidden cards and coins". The summary is written once for each listener, from that listener's own view, and an eliminated seat cannot see the winner's hidden cards.
The model answered `{"answer": {"type": "info", "text": "false"}, "reason": "final hidden cards ... are not shown ... cannot quote them as required"}`. The engine accepted `text: "false"` as the announcement and sent it.

**Three separate things, none changed yet:**
1. **Engine.** An announcement written by a model is not checked. A reply that is empty, a bare `true`/`false`/`None`, or only a few characters should fall back to the ending's own `text` (which is correct and complete). Fix in `xcolos/flow/executor.py` (`_say`).
2. **Engine.** An ending that every seat hears the same is written once for each seat: four calls, four different accounts of the same match (and about 55 seconds when the backend is slow). Proposed: one call for the whole table when the announcement is public.
3. **Generator.** Our rule for the ending `llm` ("ask for a short summary of how the game went") lets the coder add demands the model cannot meet from `history`. Proposed: the rule says the `llm` may ask only for what is in `history` and the final public state, and never for hidden information.
Also proposed: a trace-lint check that flags an ending announcement that is not prose.

**Why it stopped here.** Items 1 and 2 are engine changes and 3 changes the generator's own rules; by the loop policy these need review before another iteration.

2026-10-12 **Decision: approved items 1 and 2 (the engine). Done.** In `xcolos/flow/executor.py`: a model's announcement that is not prose (empty, or a bare true/false/none/null) is no longer sent; the ending's own `text` is sent instead.
A public ending is now written once, from a new public view (`FlowState.public_view`: public attributes only), and told to everyone, instead of once per seat. Tests in `tests/test_talk_and_store.py`.
2026-10-12 **Item 3 resolved differently (user decision):** a game-over only announces the result (winner and final figures), it does not retell the game. The generator rule now forbids `llm` in endings, `model_use` flags it, and Coup's endings use `text` only.
