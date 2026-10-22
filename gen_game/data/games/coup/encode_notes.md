# Coup (XColos): encoding notes

## Rules text
- `rules` follows the design's own wording, step by step. As the last attempt's guidance asked, the Coup and Assassinate lines read "(only if you have 7 or more)" and "(only if you have 3 or more)".
- Two sentences were added for R49/R50. Step 4 now says a failed challenge costs the challenger a card and the action still goes ahead (so a target who challenges a true Assassinate still loses a card). A paragraph after step 5 says shown cards go to the bottom of the deck, the replacement is drawn first from the top, and the deck is shuffled once at the end of the turn.

## Offers
- `action_offer` is a player list attribute built at the start of the turn from the player's coins:
  - `['coup']` only, if `coins >= forced_coup_threshold`;
  - otherwise income, foreign_aid, tax, steal and exchange, plus coup if `coins >= coup_cost` and assassinate if `coins >= assassinate_cost`.
  - No literal numbers are used. A forced Coup has one option, so the engine answers it automatically and logs it as a move.
- `target_offer` (a hidden table list) holds the living seats other than the active seat.
- `reaction_offer` is a player list built after the action is known. It offers pass/block_duke for foreign_aid and pass/challenge otherwise. Only the target gets block_contessa (against assassinate) or block_captain/block_ambassador (against steal).
- No answer is ever refused after it is given.

## Deck: "top" and "bottom" (R46, R47, R49)
- The deck is a list. Drawing takes a random card from the part of the deck not put back this turn. A shuffled deck makes that the same as taking the top card.
- Cards put in this turn are appended at the end (the bottom) and counted in a hidden `bottom_n`. Draws skip those cards unless nothing else is left.
- `bottom_n` resets to 0 in Resolve, which stands for the end-of-turn shuffle.
- On a proven claim or block, the replacement is drawn first and only then is the shown card moved to the deck. So the replacement can never be the shown card.

## Card choice (step 7): one poll, not two
- The script says a player who both loses a card and owes an Exchange return answers twice. That cannot happen in this game:
  - only the active player can owe a return;
  - the active player only takes a pending loss when their claim is falsely made, which cancels the Exchange;
  - Exchange cannot be blocked, so there is no block challenge to lose either.
- So one poll asks each eligible player for one hidden card, stored in `card_choice`. Resolve copies it into `reveal_choice` (pending_loss = 1 and hidden_count = 2) or `return_choice` (must_return = 1).
- This kept the round at exactly 20 steps.

## Other choices
- Step 3 ("send each player their hidden_cards") and the setup deal message are per-reader `tell`s (`{hidden_cards}`), not `sync`s. A `sync` also printed the public table fields that are empty early in the turn (action, claimed_role, block_role, winner). The verifier flagged them, and the interface requires them to stay public.
- Script steps 10 and 11 (find the challenger/blocker, resolve the action challenge) are one `update`.
- A scratch flag `claim_true` records whether the claim being challenged was true. It is used for the action challenge and again, recomputed, for a challenged block. It has to be computed before the shown card leaves the hand.
- `winner` is set in the Resolve update, because a `check` cannot set attributes. The cap tiebreak uses a hidden `top_key = hidden_count * 1000 + coins` over living seats; more than one seat at the top is a draw.
- An eliminated player gets the platform status `out` as well as `alive = false`, `coins = 0` and `hidden_count = 0`.
- Ask prompts are rendered without the asking seat, so they cannot use `{you.…}`. The card-choice prompt therefore explains both uses (reveal or return) in one text.

Nothing the rules require was left out.
