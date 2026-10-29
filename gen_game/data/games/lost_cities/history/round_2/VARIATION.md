# Variation: Lost Cities: Three Expeditions

A one-deal, three-colour Lost Cities for two players. Players hold hidden hands, build rising expeditions with wagers, and draw from a shared face-up discard row in which each colour shows at most one card. Both players always get equal turns.

Players: 2 to 2, best with 2

## Review of the original

Lost Cities is a two-player card game of hidden hands and timing. Each turn a player plays a card to a rising single-colour expedition or discards it face-up, then draws from the deck or a discard pile. Started expeditions cost points, wagers multiply the result, and the higher total over three deals wins.

- **non_degenerate**: good. Simple policies all lose. Always discarding scores 0 and loses to any positive score. Always playing the lowest card opens every colour, takes the cost on each, and ends up negative. Always wagering early multiplies losses as well as gains. The first player has only a small edge, because the game ends the instant the deck runs out, which can cost the second player a turn.
- **skill_sensitive**: good. Experienced players beat novices reliably over three deals. The skill lies in counting cards, deciding when to commit to a colour, denying discards the opponent wants, and controlling the pace of the deck. The draw adds variance within one deal.
- **headroom**: good. A weak player can still score by opening one or two strong colours. A strong player keeps gaining from tracking the opponent's colours, sizing wagers, and running the deck out at the right time.
- **reasoning_dependent**: good. Hands and deck order are hidden. Players must infer the opponent's colours from what they play, discard and pick up, and plan which colours to commit to over many turns.
- **verifiable**: good. Scoring is pure arithmetic: the sum of numbers, minus a cost, times the wager multiplier, plus a length bonus.
- **fits_platform**: weak. It is turn-based and text-only, but it is too large to build. Five colours, three deals and per-colour columns and discard piles for each player exceed the attribute and round limits. The board of discard spaces has to become state. The earlier build attempt failed on blank discard fields and on a {hand} placeholder.

## Problems

- P1: Five colours, three deals and about 44 turns per deal exceed the limits of 20 attributes and 40 rounds.
- P2: The previous variation stored the discard row as four text fields that started as blank strings. Players were shown empty internal fields and the build failed.
- P3: The previous variation put the hand into a prompt as a {hand} placeholder that the step cannot fill.
- P4: Separate discard piles with buried cards that can be dug back up need a stack per colour. That is too much state for the engine.
- P5: The game ends the instant the last card is drawn, so the second player can lose a turn. That is a seat edge, and it grows in a shortened single-deal game.
- P6: With fewer cards per player, the original cost of 20 and the 8-card bonus would make almost every expedition lose points and the bonus unreachable, which pushes play toward discarding everything.
- P7: The 'just discarded' restriction needs a bookkeeping value. If it is stored as a blank text field it reproduces P2.

## Changes

- Use 3 colours (Red, Blue, Green), each with numbers 2-10 and 2 wagers: 33 cards in total. Hands are 6 cards. Play a single deal instead of three. (fixes: P1): This brings the state to 17 attributes and the length to at most 20 rounds, while keeping full colour suits.
- Replace the per-colour discard text fields with one public list attribute, discard_tops. It holds the face-up cards, at most one per colour, and starts as an empty list (never a blank string). Discarding a card of a colour already shown removes the old card from the game and appends the new one. (fixes: P2, P4): A list has no blank fields to print, and keeping only the top card per colour removes the need for stacks.
- Each player's hand is a hidden list attribute, hand, which the engine shows only to its owner as part of their state. Prompts use only {seat} and {value}. (fixes: P3): The hand reaches the player through state the engine already displays, not through an unfillable placeholder.
- Store the just-discarded card in a hidden bookkeeping attribute, last_discard. It starts as the sentinel 'none', is never printed to players, and is reset to 'none' after each draw. (fixes: P7, P2): This enforces the no-retake rule without a blank field appearing in the state.
- Expedition state is held as per-colour numbers: sum, top number, wager count and card count, all starting at 0. (fixes: P1, P2): Numbers starting at 0 never print as blank, and scoring becomes direct arithmetic.
- The game ends at the end of the round in which the deck becomes empty, so both players always get the same number of turns. There is also a cap of 20 rounds. (fixes: P5, P1): This removes the second seat's lost-turn disadvantage and bounds the game's length.
- Rescale scoring. The cost per started expedition is 15. The length bonus is +10 for 5 or more cards. The multiplier stays at 1 plus the number of wagers. (fixes: P6): With about 11 turns each, good columns of 4-6 cards can still score positively, so committing to colours pays.

## Kept from the original

- Play-or-discard followed by drawing from the deck or a face-up discard.
- Strictly increasing number columns per colour.
- Wagers allowed only before any number, multiplying the column's result, including losses.
- A fixed cost for each started expedition, so committing to a colour is a risk.
- A length bonus.
- Hidden hands and a hidden deck order.
- Denying the opponent useful discards, and controlling the pace of the deck by taking discards.
- Two players, with the higher total winning.

## The variation's rules

CARDS. There are 33 cards in 3 colours: Red (R), Blue (B) and Green (G). Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9 and 10, written like R7 or B10, plus 2 wager cards, written RW, BW and GW (two of each).

SETUP. Shuffle all 33 cards into a face-down deck. This is the only random event in the game. Deal 6 cards to each player. Each player's hand is a hidden list that only its owner can see; the engine shows it to its owner as part of that player's state.

Table state:
- deck: hidden list, 21 cards remaining after the deal.
- discard_tops: public list of face-up cards, at most one per colour. It starts as an empty list.
- last_discard: hidden bookkeeping value, never shown to players. It starts as 'none'.

Player state, for each player and each colour c in R, B, G:
- sum_c: total of the numbers played in that colour. Starts at 0.
- top_c: highest number played in that colour, 0 meaning no number yet. Starts at 0.
- wag_c: number of wagers played in that colour. Starts at 0.
- cnt_c: number of cards in that colour's expedition, wagers included. Starts at 0.
- score: the player's current score. Starts at 0.
All player state is public except hand.

ROUND. Seat 1 is chosen at random. Each round, seat 1 takes a turn and then seat 2 takes a turn.

A TURN has two choices.

(1) PLAY OR DISCARD. The active player answers with one of:
- 'PLAY X', where X is a card in their hand.
- 'DISCARD X', where X is a card in their hand.

A PLAY is legal if:
- X is a number greater than top_c of its colour; or
- X is a wager and top_c of its colour is still 0.

When a play is legal, remove X from the hand, add 1 to cnt_c, then:
- for a number: add X to sum_c and set top_c to X;
- for a wager: add 1 to wag_c.

An illegal PLAY, or a card not in the hand, is treated as DISCARD of the first card in the hand.

A DISCARD removes X from the hand. If discard_tops already contains a card of X's colour, that old card is removed from the game permanently. Then X is appended to discard_tops, and last_discard is set to X.

(2) DRAW. The active player answers one of:
- 'DECK': take the top card of the deck into the hand.
- The name of a card in discard_tops other than last_discard: move that card from discard_tops into the hand.

An invalid answer, or naming last_discard, means DECK. If the deck is empty, the player must take a card from discard_tops other than last_discard. If none is available, the player draws nothing.

After the draw, last_discard is reset to 'none'. Both players always see discard_tops, both players' expedition numbers, and how many cards remain in the deck.

END OF ROUND. Recompute both scores. For each colour:
- if cnt_c = 0, the colour scores 0;
- otherwise it scores (sum_c - 15) x (1 + wag_c), plus 10 if cnt_c is 5 or more.
A player's score is the total of their three colours.

The game ends at the end of the round in which the deck became empty, or at the end of round 20, whichever comes first. Seat 2 always finishes the round, so both players take the same number of turns.

Objective: When the game ends, the player with the higher score wins. If the scores are equal, the game is a draw.

Expected effect: Players must decide which of three colours to commit to, given a hidden hand and knowledge of which cards are already gone. They must judge whether to wager before seeing enough numbers, infer the opponent's colours from what they play and pick up, avoid discarding cards the opponent wants, and use discard pickups to slow the deck when they need more turns or draw from the deck to speed the end. Because columns cost 15 points, blind openings lose points, and always discarding scores 0, so neither simple policy is safe. Equal turn counts remove the seat edge. The deck order adds variance, but card counting and denial let the stronger player win most games. Talk is omitted because with two players and opposed interests it adds nothing to reason about. Build notes: there are no blank fields, since discard_tops is a list (possibly empty), last_discard uses the sentinel 'none' and is hidden as bookkeeping, and every counter starts at 0. Prompts use only {seat} and {value}; hands reach players through the hidden hand attribute.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 20 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
