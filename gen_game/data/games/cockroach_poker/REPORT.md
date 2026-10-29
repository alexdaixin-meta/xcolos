# cockroach_poker: ready for review

Built from the variation **Cockroach Poker: Straight Calls** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Drop PASS entirely. Each round the sender chooses a card, chooses a claimed creature and chooses a receiver, and the receiver calls TRUE or FALSE. That is exactly 4 choice steps. (fixes: The PASS mechanic pushes choice steps per round to 7, over the limit of 4, and needs a conditional sub-sequence the engine lacks.): This keeps the core bluff-and-call duel inside the limit, and the step list becomes flat.
- Choose the first sender at random during setup instead of always seat 1. After that, whoever takes a card sends next, as in the original. (fixes: Seat imbalance against random play (seat 2 won 20, seat 3 won 11, seat 1 won 11 outright), most likely from a fixed first sender and fixed seat order.): This removes the built-in seat advantage while keeping the original's rule that the loser of a card starts the next round.
- Shrink the deck to 4 creatures x 6 copies (24 cards). Deal 7 to each of 3 players and set 3 aside unseen. A player loses on 3 face-up cards of one creature. (fixes: A 64-card, 8-creature deck makes hands large and card-counting too diffuse for a short text game. With few creatures face-up, the inference is weak until very late.): Fewer creatures make face-up information and card-counting meaningful and the game short. The 3 hidden cards keep counting from becoming certain.
- Use a chain of arithmetic tie-breaks among non-losers. First, fewest face-up cards. Then fewest cards of their single most common face-up creature. Then most cards still in hand. Only after that is it a draw. (fixes: Many shared wins between the two non-losers (18 of 60 random games), so the ending often fails to separate players.): Outright winners become far more common, and every tie-break is a count the engine tracks.

Objective: Avoid being the loser, who ends the game with 3 face-up cards of one creature or must send with an empty hand. Among the players who did not lose, the one with the fewest face-up cards wins. Ties are broken by the smaller count of their most common face-up creature, then by more cards left in hand. Players tied on all three draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. CORE EXCHANGE. Each round reduces to the sender choosing Truth or Lie and the receiver calling TRUE or FALSE. 'Takes' means who receives the card face-up, which is bad.

| Sender \ Receiver | TRUE | FALSE |
|---|---|---|
| Truth | sender takes | receiver takes |
| Lie | receiver takes | sender takes
- playable: pass. COMPLETENESS. The rules cover every case:
- Card choice, claim (any of 4 creatures, including ones visibly exhausted, which is simply a lie), receiver (either other player), call, reveal and correctness are all defined.
- Who takes the card and who sends next are defined.
- The order of checks is de
- reasoning_over_luck: pass. WHAT A RECEIVER CAN INFER. The receiver knows their own 7 cards and all face-up cards, with 6 copies of each creature and 3 unknown set-aside cards. From that they can compute how many copies of the claimed creature could still be in the sender's hand.
- Worked case: the receiver holds 4 Rats and 1 

## Complexity

- steps_per_round: designed 12, built 18, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 14, built 30, limit 20 (built: 80)
- hidden_elements: designed 2, built 6, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup deals 7 cards to each seat and sets 3 aside (seat 1's hand after it sends one)
- pass: Setup starts everyone with no face-up cards and not lost (uninvolved seat stays at 0)
- pass: Sender passes one card and hand_size falls by 1
- pass: Claim may differ from the card and any creature can be claimed
- pass: Receiver is one of the other two seats, never the sender
- pass: TRUE call on a true claim: sender takes the card
- pass: FALSE call on a bluff: sender takes the card
- pass: TRUE call on a bluff: receiver takes the card
- pass: FALSE call on a true claim: receiver takes the card
- pass: Card is revealed and taker's creature count and total rise by 1
- pass: The taker becomes the next sender
- pass: Third face-up Rat makes the taker lose and ends the game
- pass: Next sender with an empty hand loses
- pass: Round 24 finishing ends the game with no loser
- pass: A seat that lost cannot win despite the fewest face-up cards
- pass: Fewest face-up cards wins over a bigger hand
- pass: Tied face_total: smaller max_face wins over larger hand
- pass: Tied face_total and max_face: larger hand wins, full tie shares the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 9, 'seat 3': 2, 'seat 1': 9}, 20-76 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 48.0 decisions, prompts of 101 characters on average (longest 215)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 23, 'seat 3': 17, 'seat 1': 18, 'seats 2 and 3': 2}
- always `first@seat1`: won 10, lost 49, drew 1
- always `first@seat2`: won 8, lost 49, drew 3
- always `last@seat1`: won 26, lost 30, drew 4
- always `last@seat2`: won 28, lost 30, drew 2

## Triage (whose problem each failure was)

- round 1: revise_rules: The game is built correctly and behaves as specified, but the design needs 7 choice steps per round against a limit of 4. Those steps are the sender's card, claim and receiver, the receiver's response, then the passer's new claim, new receiver and the final judgment. That is a flaw in the rules, not in the file.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3. The deal of 7 + 7 + 7 + 3 aside uses the 24-card deck exactly, so another count would break the deal. Three seats also give the sender a real choice of whom to target.
- No talk phase: The rules say the claim is the only message.
- Single rank_by expression with weights 1000000 / 10000 / 100: This encodes not-lost first, then fewest face_total, then smaller max_face, then more hand_size. Each weight exceeds the largest possible value of the next term (face_total <= 24, max_face <= 6, hand_size <= 7).
- Strategy at the table: The sender reads which creatures each player already shows and steers cards toward the player closest to 3 of a kind, bluffing or telling the truth unpredictably. The receiver weighs the sender's hand and the creatures already exposed when calling.

## Simplifications

- A card is chosen by naming its creature: Copies of a creature are identical, so naming the creature is equivalent to picking the card.
- The sender's three decisions are three sequential asks: Only the sender answers them and the receiver does not see the card, so splitting them changes nothing.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (call, claim, revealed_card) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (call, claim, revealed_card) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
