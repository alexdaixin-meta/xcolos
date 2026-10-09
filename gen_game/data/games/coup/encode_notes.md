# Coup (XColos): encoding notes

`verify coup game` and `verify coup rules` both print ok (43 of 43 scenarios). Random 3, 4 and 5 player matches all end. A round is 20 steps, counting the steps inside the `repeat` blocks.

## What the platform could not do directly, and what I chose

- **Illegal answers are offered, then refused and re-asked.** The rule scenarios expect options such as `coup` (under 7 coins), `challenge` (against Income or Foreign Aid), a block by a non-target, and a self or eliminated seat as a target to be put to the seat. The game then has to refuse them. So:
  - The action and the target are each asked inside a `repeat`. An illegal action is re-asked from the legal list.
  - An illegal target is dropped from the offer and the seat is asked again.
  - The reaction poll is a `repeat` too. A player whose answer is not allowed is re-asked, with that answer removed from their offer, until it is valid.
  - Everyone except the target of a Coup, Assassinate or Steal is offered every reaction. The target sees only the options that are legal for them. This was needed so that a scripted card name could not match a block option at the target's reveal question.
  - Net effect: the action is always legal. Coup is compulsory at 10 or more coins. A reply that is not allowed cannot affect the game.
- **The reaction poll runs for every action**, including Income and Coup. Illegal answers are refused as above, so those turns resolve with no challenge or block. Reactions are announced after all answers are in.
- **Exchange**: the script draws first and returns afterwards, and the draw is a random card, not the top card. `hidden_count` stays 2 during the exchange while the list holds 3 cards. The return is chosen in the same poll as the reveal.
- **Reveal and return share one poll** (stored in `reveal_choice`) to stay within 20 steps. The resolve step copies `reveal_choice` into `return_choice` for the player who owes an Exchange return. A player cannot both lose a card and owe a return in the same turn: a failed challenge cancels the Exchange, and an Exchange cannot be blocked.
- **Shuffling is implicit**: a card returned to the deck is a list entry, and every draw takes a random card. The script's "shuffle if a card was put into the deck" has no separate step.
- **Challenge resolution order** follows the script: the proven card goes to the deck first, then a random draw, which may be the same card. The block challenge does its pending-loss and status work before it moves cards.
- **Seat order uses a modulo trick** (`((seat - from) % players) * 10 + seat`), which holds for up to 9 seats. The next active seat is picked among players with `alive = true` and is advanced in the resolve update, before the end check, since nothing reads it after a win.
- **Winner**: the resolve update computes `top_score` (hidden cards x 100000 + coins, among players with a hidden card), `top_count`, `leader` and `winner`. A tie on that score is a draw, which matches "most hidden cards, then most coins, then draw". Winner text is `seat N` or `draw`. The five seat endings and `draw` fire from `check`, with `living_count == 1 or turn_count >= turn_cap`. `limits.rounds` is 40 and `rounds_max` is 60, so the turn cap always ends the game first.
- **Parameters** are game attributes. `deck_size`, `copies_per_role`, `exchange_draw`, and the Exchange return count are declared but only partly used. The deck list, the single Exchange draw and `exchange_return` are written out, because the calc language has no way to build a list from a count.
- Setup deals 2 cards to each seat with explicit draw blocks per seat (up to 5), gated on the player count.
- Free talk is not offered, per the rules.
