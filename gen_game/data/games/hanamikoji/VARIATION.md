# Variation: Hanamikoji: Five Geisha

Two players play 4 hands of 8 alternating turns. Each turn they draw an Item and use one of four one-shot actions to place Items beside 5 Geisha. After hands 2 and 4, Geisha markers move to whoever has strictly more Items of that Geisha. Reaching 11 Charm or 3 Geisha wins.

Players: 2 to 2, best with 2

## Review of the original

Hanamikoji is a two-player card game. Over several rounds, players use four one-shot actions (Secret, Trade-off, Gift, Competition) to place hidden Item cards beside 7 Geisha. A Geisha goes to whoever has more of its Items. The first player to win 4 Geisha or 11 Charm wins.

- **non_degenerate**: good. No fixed action order wins. 'Always Secret first' gives away your Gift and Competition splits at the end, when the opponent knows most of the cards. 'Always take the highest Charm card offered' is beaten by an opponent who builds splits that bait it. The starting seat alternates each round. Ties leave the marker in place, so both players have something to fight for in every round.
- **skill_sensitive**: good. The deal matters, but every hand is played through the same four actions. Those actions force each player to give the opponent part of their cards and to choose a split the opponent will pick from. Good splitting (offering a pair the opponent does not want to take but cannot afford to leave) and good card counting decide most games.
- **headroom**: good. A weak player still wins some Geisha simply by holding cards. A strong player can keep improving: they track the 21 known Items against the 1 removed card and the opponent's Secret, order their actions, and plan a marker swing across rounds.
- **reasoning_dependent**: good. Hidden hands, a hidden removed card, a hidden Secret and hidden Trade-off discards mean players must infer what the opponent holds from what they reveal and in what order. Gift and Competition reward modelling which option the opponent will choose.
- **verifiable**: good. Geisha are won by strict count comparison, and the winner follows from Charm sums and Geisha counts. All of it is arithmetic.
- **fits_platform**: weak. The game is text-only and turn-based. As written, though, it has 7 Geisha and an open-ended number of rounds, which strains the attribute and round limits. The previous build also failed in practice: the 'Trade-off' option was never offered to a seat, so end-of-hand Secret reveals, marker moves, charm recomputation and the win check could never be reached in tests.

## Problems

- P1: The original has no fixed length (it repeats rounds until a goal is met), but the platform needs a fixed maximum number of rounds and a defined result if no one reaches a goal.
- P2: Seven Geisha plus per-player per-Geisha tracking pushes the attribute count past the limit.
- P3 (build failure): The action option 'Trade-off' was never offered to a player. The likely causes are a spelling mismatch ('Tradeoff', 'Trade off') or an option list rebuilt from a round counter instead of from the player's actual unused actions. As a result, round 8 of a hand never completed correctly.
- P4 (build failure): Because round 8 could not complete, the step that adds each player's Secret card to their kept cards never ran.
- P5 (build failure): Because the hand could not end, the end-of-pair marker comparison, the charm and geisha_count recomputation, and the win check (charm 11 beats Geisha count) never ran. The order of these steps was also not stated tightly enough.
- P6: The original's 'enough cards' guarantee is implicit. The rules must state that the card counts always let a player complete their remaining action, so no action ever has to be skipped.

## Changes

- Play exactly 4 hands of 8 turns (32 rounds), grouped into two scoring pairs (hands 1–2 and hands 3–4). Add a final tiebreak by Charm, then Geisha count, else a draw. (fixes: P1): This gives a fixed, buildable length that still contains two marker-moving scorings, so a player can lose the first scoring and come back.
- Use 5 Geisha with Charm 3, 3, 4, 5, 6. Each Geisha has as many Items as its Charm, 21 Items in total. The goals become 11 Charm or 3 Geisha. (fixes: P2): This keeps 21 Items and the 11-Charm goal while cutting attributes. Neither goal can be reached by both players at once: 11+11 exceeds 21, and 3+3 exceeds 5.
- Name the actions with these exact strings: Secret, Trade-off, Gift, Competition (capital first letter, hyphen in Trade-off). The options put to the active player are exactly the current contents of their unused_actions list, read at that moment. The list is reset only when a hand starts and is never recomputed from a round counter. (fixes: P3): This makes the option list match the rules and any state a test sets, so Trade-off is offered whenever it is unused, including in round 8.
- Add an explicit statement that in round 8 the active player has exactly one action left and must take it. If that action is Trade-off, they discard 2 cards from hand. (fixes: P3): This guarantees the hand always reaches its end.
- Add an explicit end-of-hand step after round 8: each player's Secret card is revealed and appended to their kept list. (fixes: P4): Secrets count toward the scoring.
- Fix the end-of-pair order after hands 2 and 4: (a) compare per Geisha, where a strictly higher count moves the marker and a tie leaves it; (b) recompute charm, geisha_count and standing; (c) run the win check. (fixes: P5): A deterministic order makes the scoring testable.
- State the card budget: a player holds 6 cards and draws 4, which is 10 cards, and the four actions use exactly 1+2+3+4 = 10. Every action is therefore always affordable. (fixes: P6): This removes any need for a skip or fallback branch, which the flat step list cannot express.

## Kept from the original

- The four one-shot actions Secret, Trade-off, Gift and Competition, each used once per hand.
- Gift (opponent takes 1 of 3) and Competition (opponent takes one of two pairs): the I-split-you-choose heart of the game.
- 21 Items, 1 removed unseen per deal, hidden hands, 8-card draw deck.
- Victory markers that move only on a strictly higher count and stay on a tie, and that carry over between scorings.
- The win goal of 11 Charm (beating the Geisha-count goal), with the starting player alternating.

## The variation's rules

COMPONENTS.
- There are 5 Geisha, numbered 1 to 5, with Charm 3, 3, 4, 5, 6.
- There are 21 Item cards. Each card shows a Geisha number: three 1s, three 2s, four 3s, five 4s and six 5s.
- Each Geisha has a marker. Each marker is on Player 1's side, Player 2's side, or in the middle. All markers start in the middle.

PLAYER STATE.
- hand: private cards.
- secret: 0 or 1 face-down card.
- unused_actions: a list.
- kept: the cards placed on the player's side, visible to both.
- charm.
- geisha_count.
- standing.

GAME STATE.
- deck, removed_card, discard (hidden).
- hand_number (1–4), round_in_hand (1–8), starting_seat.
- marker_1 to marker_5.

ACTION NAMES.
The four actions are spelled exactly: Secret, Trade-off, Gift, Competition.

STRUCTURE.
The game is 4 hands of 8 rounds, 32 rounds in total. Hands 1 and 2 form Pair 1; hands 3 and 4 form Pair 2. Player 1 is the starting seat in hands 1 and 3; Player 2 is the starting seat in hands 2 and 4.

START OF A HAND (round_in_hand = 1, before anything else).
1. Shuffle all 21 Items and set 1 aside face-down as removed_card. Nobody sees it.
2. Deal 6 cards privately to each player. The remaining 8 cards form the deck.
3. Empty both secrets. Empty the discard.
4. Set both players' unused_actions to [Secret, Trade-off, Gift, Competition].
5. If this is hand 1 or hand 3, empty both players' kept lists. In hands 2 and 4, kept lists carry over unchanged. Markers always carry over.

EACH ROUND (one turn).
1. The active player is the starting seat in odd rounds (1, 3, 5, 7) and the other player in even rounds (2, 4, 6, 8). Each player therefore takes 4 turns per hand.
2. The active player draws the top card of the deck into their hand.
3. The active player chooses one action. The options offered are exactly the actions currently in their unused_actions list. The list is never rebuilt from the round number.
4. That action is removed from their unused_actions list.
5. The active player names the hand cards the action uses, by Geisha number, from cards they actually hold.
6. The action is resolved:
   - Secret: move 1 hand card face-down to the player's secret.
   - Trade-off: move 2 hand cards face-down to the discard. They are out of play for this hand.
   - Gift: reveal 3 hand cards. The opponent chooses 1 of them, and it goes to the opponent's kept. The other 2 go to the active player's kept.
   - Competition: reveal 4 hand cards split into Pair A (2 cards) and Pair B (2 cards). The opponent chooses Pair A or Pair B, and it goes to the opponent's kept. The other pair goes to the active player's kept.

CARD BUDGET.
Each player holds 6 cards and draws 4 per hand, 10 in total. The actions use exactly 1+2+3+4 = 10 cards, so the chosen action is always affordable. In round 8 the active player has exactly one action left, which may be Trade-off, and must take it.

END OF A HAND (after round 8).
Each player's secret card is revealed and appended to their kept list.

END OF A PAIR (after hands 2 and 4 only, after the step above). Run these steps in this order:
(a) For each Geisha g, count the cards of number g in each player's kept. If one player's count is strictly higher, marker_g moves to that player's side. On a tie the marker stays where it is.
(b) For each player, charm is the total Charm of the Geisha whose markers are on their side, and geisha_count is the number of markers on their side. standing = charm.
(c) Win check:
   - A player with charm 11 or more wins.
   - Otherwise, a player with geisha_count 3 or more wins.
   - Both players cannot reach the same goal. If one reaches 11 charm and the other reaches 3 Geisha, the 11-charm player wins.
   - If someone wins, the game ends.

AFTER HAND 4.
If no one has won, the player with the higher charm wins. If charm is tied, the player with the higher geisha_count wins. Otherwise the game is a draw.

Objective: The win check runs at the end of each pair, after hand 2 and after hand 4. A player whose markers total 11 or more Charm wins. Otherwise, a player holding 3 or more markers wins; if one player has 11 Charm and the other has 3 markers, the 11-Charm player wins. If no one has won after hand 4, the higher Charm wins, then the higher Geisha count; otherwise the game is a draw.

Expected effect: Play keeps Hanamikoji's tension: every Gift and Competition is a split the opponent exploits, so players must read the opponent's needs from the open kept cards and the order of actions so far, and hide their own plan in Secret and Trade-off. Two scorings with sticky markers reward planning across hands: you can concede a Geisha in Pair 1 knowing a tie in Pair 2 keeps your marker. The rules now fix the option names and the end-of-hand and end-of-pair order, so the build reaches round 8, reveals Secrets, moves markers and runs the win check as the tests require. This is a two-player game, so there is no talk phase.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 32 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
