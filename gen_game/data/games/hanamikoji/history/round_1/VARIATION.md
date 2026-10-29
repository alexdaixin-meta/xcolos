# Variation: Hanamikoji: Compact Build

Two players fight over seven Geisha across up to 4 hands of 8 alternating turns. They use four one-shot actions to place, hide, discard or offer Item cards. Gift and Competition force the opponent to split revealed cards. Majorities win Geisha markers, and the first to 11 Charm or 4 Geisha wins.

Players: 2 to 2, best with 2

## Review of the original

Hanamikoji is a two-player card game. Over repeated hands, players use four one-shot actions (Secret, Trade-off, Gift, Competition) to place Item cards beside seven Geisha. Gift and Competition force the opponent to split revealed cards. Winning a majority of a Geisha's Items wins her marker, and the first to 11 Charm or 4 Geisha wins.

- **non_degenerate**: good. No fixed policy works. Always offering your best cards in Gift or Competition hands them to the opponent. Always hoarding by using Secret and Trade-off early leaves forced, transparent Gift and Competition offers late in the hand. Every player must use all four actions each hand, so there is no pass. The seat edge from moving first is removed by alternating the starting player each hand, which over 4 hands gives each seat two starts.
- **skill_sensitive**: good. The deal varies, but each player sees 10 of their own cards per hand and controls their timing. Offers can be built so that every split favours the offerer, for example a Competition with two contested-Geisha pairs. A careless player loses Geisha systematically. The previous playtest found the rules sound; luck in the deal is spread over several hands.
- **headroom**: good. Players can improve by sequencing actions, by tracking the 21-card composition to infer the opponent's hand and secret card, and by valuing Geisha differently by Charm and current marker. Ties keep markers, so marker holdings carry over between hands. A weak player still wins Geisha through the opponent's forced offers.
- **reasoning_dependent**: good. Hands, the secret card, the removed card and Trade-off discards are hidden. Picking from a Gift or Competition means inferring what the offerer is keeping back and what their secret card is likely to be. Making an offer means modelling which split the opponent will take.
- **verifiable**: good. Majority counts per Geisha, markers, Charm sums and the 11-Charm or 4-Geisha thresholds are all arithmetic.
- **fits_platform**: weak. The game is turn-based, text-only, has no board and is decided by arithmetic. The previous variation exceeded the limits: about 21 or more attributes against 20, and about 25–30 flat steps against 20. It also left the hand order for the illegal-choice fallback unspecified. The game fits only when the state is packed into list attributes and the end-of-hand work is folded into one calculation.

## Problems

- Attribute count exceeded the limit: 14 per-Geisha count attributes and 7 marker attributes, plus action flags, hand and turn numbers, Charm and Geisha held, the deck, hands, secrets and pile, came to well over 20 while 19 was declared.
- Steps per round exceeded the limit: the start-of-hand, turn and end-of-hand steps, with a separate conditional update per Geisha comparison, totalled roughly 25–30 against a declared 15.
- Hidden elements were not listed explicitly, so it was unclear that they fit within 3.
- Hand order for the illegal-choice fallback was unspecified, so 'the first cards of their hand' was ambiguous.
- The declared complexity block was not credible.

## Changes

- State is packed into 17 named attributes. Each player's placed counts are one 7-entry list. All seven markers are one 7-entry list. Each player's unused actions are one list. Charm held and Geisha held for both players are one 4-entry 'standing' list. One 'offer' list, one 'chosen action' and one 'pick' hold the current turn. (fixes: Attribute count exceeded the limit.): This replaces 14 count attributes and 7 marker attributes with 3, and keeps every tracked number within 20.
- Start-of-hand work is two conditioned steps: one shuffle, then one update that sets aside, deals, builds the deck and resets actions and counts. End-of-hand work is one step that adds the secrets, one calculation that compares the two count lists, updates the marker list and computes the standing list, one announcement, and one winner step that holds the win check and the hand-4 tiebreak. The fallback and the placement each become one step. (fixes: Steps per round exceeded the limit.): This brings the flat step list to 17 per round with 2 choice steps.
- The rules name exactly three hidden elements. (1) The hidden pile: the deck order plus the out-of-play pile, which holds the removed card and Trade-off cards. (2) The two private hands. (3) The two secret cards. (fixes: Hidden elements were not listed explicitly.): This makes the information structure explicit and verifiably within 3.
- Hand order is defined. Dealt cards are kept in deal order, each drawn card is added at the end, and removing cards keeps the order of the rest. The fallback uses the first cards in this order. The rules also show that a legal fallback always exists, because hand size always covers the remaining actions. (fixes: Hand order for the illegal-choice fallback was unspecified.): This removes the ambiguity in the illegal-choice rule.
- The complexity block is restated from an explicit count of steps and attributes, both listed in the rules. (fixes: The declared complexity block was not credible.): This makes the declared numbers match the build.

## Kept from the original

- Seven Geisha with Charm values 2,2,2,3,3,4,5 and 21 matching Item cards.
- The four one-shot actions per hand: Secret, Trade-off, Gift (opponent takes 1 of 3) and Competition (opponent takes 1 of 2 pairs).
- One card removed unseen each hand, 6-card hands and an 8-card deck with one draw per turn.
- Majority per Geisha wins her marker, ties leave the marker where it is, and markers carry over between hands.
- The win at 11 Charm or 4 Geisha, with Charm taking precedence.
- The alternating starting player, and all the gameplay rules that the previous test found complete and sound.

## The variation's rules

COMPONENTS
- Seven Geisha, G1 to G7. Charm values: G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5 (21 in total).
- 21 Item cards. Each Geisha has as many Items as her Charm value: two G1, two G2, two G3, three G4, three G5, four G6, five G7. A card is named by its Geisha (for example 'G6').
- Each player has four action types: Secret, Trade-off, Gift, Competition.

TRACKED STATE (17 attributes)
1. deck: ordered list of cards, hidden.
2. pile: the out-of-play list, hidden from everyone forever.
3. hand_A: Player A's ordered hand, seen only by A.
4. hand_B: Player B's ordered hand, seen only by B.
5. secret_A: seen only by A until the end of the hand.
6. secret_B: seen only by B until the end of the hand.
7. counts_A: 7 numbers, A's placed cards per Geisha.
8. counts_B: 7 numbers, B's placed cards per Geisha.
9. markers: 7 entries, each 'A', 'N' or 'B'. All start 'N'.
10. actions_A: A's unused actions this hand.
11. actions_B: B's unused actions this hand.
12. hand_number: 1 to 4.
13. turn_number: 1 to 8 within the hand.
14. standing: [Charm held by A, Charm held by B, Geisha held by A, Geisha held by B], all starting 0.
15. chosen_action.
16. offer: the cards revealed this turn, in order, split into Pair 1 and Pair 2 for Competition.
17. pick.

HIDDEN ELEMENTS (3)
(1) The hidden pile: the deck order plus the out-of-play pile, which holds the removed card and all Trade-off cards.
(2) The private hands.
(3) The secret cards.

STRUCTURE
- One engine round is one turn. A hand has 8 turns, and the game lasts at most 4 hands, so at most 32 rounds.
- Active player: in hands 1 and 3, Player A acts on odd turns and B on even turns. In hands 2 and 4, Player B acts on odd turns and A on even turns.

HAND ORDER
- Cards dealt to a hand keep the order they were dealt in.
- A drawn card goes to the end of the hand.
- When cards leave a hand, the remaining cards keep their order.

STEPS OF EACH ROUND
1. (Turn 1 only) Shuffle all 21 Items.
2. (Turn 1 only) The first card goes to the pile. Cards 2–7 go to the first player's hand and cards 8–13 to the second player's hand, where the first player is the one who acts on turn 1. Cards 14–21 form the deck in that order. Both action lists are reset to all four actions. Both count lists are reset to seven zeros. Both secrets are emptied. Markers and standing are NOT reset.
3. The active player moves the first card of the deck to the end of their hand.
4. Show both players: the markers, both count lists, both unused-action lists, the standing, the hand number and the turn number. Each player privately sees their own hand and their own secret.
5. CHOICE: the active player names one unused action and the cards for it:
   - Secret: 1 card.
   - Trade-off: 2 cards.
   - Gift: 3 cards.
   - Competition: 4 cards, the first two being Pair 1 and the last two Pair 2.
6. FALLBACK: the choice is illegal if it names a spent action, a card not held (counting duplicates), or the wrong number of cards. In that case the engine uses the active player's first unused action in the order Secret, Trade-off, Gift, Competition, filled with the first cards of their hand in hand order. A legal fallback always exists, because a player's hand always holds at least as many cards as their remaining actions need: 7 cards against at most 4 needed on their first turn, and exactly the number needed on their last.
7. The chosen cards leave the hand:
   - Secret: the card becomes the active player's secret.
   - Trade-off: both cards go face-down to the pile.
   - Gift or Competition: the cards go to the offer.
8. (Gift or Competition only) The offer is revealed to both players.
9. (Gift or Competition only) CHOICE: the opponent picks. For Gift they pick card 1, 2 or 3 of the offer. For Competition they pick Pair 1 or Pair 2.
10. (Gift or Competition only) An invalid pick becomes option 1.
11. Placement:
   - Gift: the picked card adds 1 to the opponent's count for its Geisha, and the other two cards add 1 each to the active player's counts.
   - Competition: the picked pair adds to the opponent's counts and the other pair to the active player's counts.
   Placed cards are public.
12. The used action is removed from the active player's action list. The offer, chosen action and pick are cleared. The turn number goes up by 1.
13. (After turn 8 only) Both secrets are revealed, each adds 1 to its owner's count for its Geisha, and both secrets are emptied.
14. (After turn 8 only) One calculation, for each Geisha i from 1 to 7:
   - if counts_A[i] > counts_B[i], markers[i] becomes 'A';
   - if counts_B[i] > counts_A[i], markers[i] becomes 'B';
   - otherwise markers[i] is unchanged.
   Then standing is set to [sum of Charm of the 'A' markers, sum of Charm of the 'B' markers, number of 'A' markers, number of 'B' markers].
15. (After turn 8 only) Announce the markers and the standing.
16. (After turn 8 only) Winner check:
   - A player with 11 or more Charm wins. Only one player can, since the total Charm is 21.
   - Otherwise, a player with 4 or more Geisha wins. Only one player can.
   - Otherwise, if this was hand 4, the game ends: higher Charm wins, then more Geisha, else a draw.
17. (After turn 8 only, if the game has not ended) The hand number goes up by 1 and the turn number is set back to 1. The next hand's first player is the other player.

INFORMATION
- Public: placed cards and counts, revealed offers, picks, markers, standing, and spent actions.
- Private: each hand, and each secret until the end of the hand.
- Never revealed: the pile.
- Players may use the known 21-card composition to deduce unseen cards.

Objective: At the end of each hand, a player whose markers total 11 or more Charm wins. Otherwise, a player holding 4 or more Geisha markers wins. If neither has happened after hand 4, higher Charm held wins, then more Geisha held, and if both are equal the game is a draw.

Expected effect: Play is unchanged from the previously tested version, which was strategically sound: players sequence their four actions, build offers whose every split favours them, and infer hidden secrets and hands from the 21-card composition. The changes only make the game buildable within 17 attributes, 17 steps, 2 choice steps, 3 hidden elements and 1 random draw per round, and they remove the fallback ambiguity. There are two players, so there is no talk phase.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 32 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
