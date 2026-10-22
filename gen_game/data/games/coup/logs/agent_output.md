# What the coding agent printed

ok: True

error: 

````
I wrote `gen_game/data/games/coup/game.json` and `encode_notes.md`. Both checks now pass: `verify coup game` prints `ok`, and `verify coup rules` reports that all 58 rule scenarios play correctly.

The previous attempt's `game.json` had been deleted, so I couldn't just edit two lines. The version committed in git used the "refuse the answer and ask again" loop that is now flagged as a failure, so I rebuilt the file from scratch.

**Last attempt's guidance:**
- The rules text players read follows the design's wording. The Coup line now says "(only if you have 7 or more)" and the Assassinate line "(only if you have 3 or more)".
- The action options use `coins >= coup_cost` and `coins >= assassinate_cost`, with no literal numbers.
- A player starting the turn with `coins >= forced_coup_threshold` is offered only `coup`, and the engine answers that single-option question automatically.

**Other choices** (all explained in `encode_notes.md`):
- **One card poll instead of two.** The script says a player who both loses a card and owes an Exchange return answers twice. That can't actually happen in this game, so one poll asks for one card and the game files it as the card to reveal or the card to return. This keeps the round at exactly 20 steps.
- **Top and bottom of the deck (R49).** Cards put into the deck during a turn go to the bottom, and draws skip them unless nothing else is left. The skip resets at the end of the turn, which stands for the shuffle. A replacement is always drawn before the shown card goes into the deck, so it can never be the same card.
- **Script steps 10 and 11 are one step**, and the cost payment is its own step.
- **Sending each player their cards** uses a message addressed to each player rather than the built-in state send. The built-in version also printed the empty public table fields (`action`, `claimed_role`, `block_role`, `winner`), and the verifier rejected that.
- **The winner is set during the Resolve step**, because the end-check step can't change attributes.

Nothing the rules require was left out.

````
