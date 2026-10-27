# 03 design

- time: 2026-10-27T09:45:42+00:00 (68.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 227ede2203277967, reply sha256 ab32d5534e7a7cfe

## Sent

````
Original game: Hanamikoji
Players in the original: 2 to 2

Original rules:
Two players compete for 7 Geisha cards. Each Geisha has a Charm value and a set of Item cards (total 21 Items across types). First to win 4 Geisha or 11+ Charm points from won Geisha wins; 11 Charm beats 4 Geisha if both achieved same scoring.
Each round: shuffle 21 Items, secretly remove 1 card from play, deal 6 cards each as hidden hands, remaining 8 form a deck. Players alternate turns for 4 turns each: draw 1 from deck, then use one unused Action marker. Secret: set aside 1 hand card face-down for final scoring. Trade-off: set aside 2 hand cards face-down discarded this round. Gift: reveal 3 hand cards, opponent takes 1 to his side, you keep 2. Competition: reveal 4 hand cards as two pairs of 2, opponent chooses one pair, you keep the other. All kept cards are placed by their Geisha. After 8 turns, reveal Secret cards and compare counts per Geisha: higher count wins that Geisha and moves its Victory Marker; ties leave marker. If winning goal met, game ends. Otherwise collect all Item cards, retain Victory Markers, flip Action markers up, swap starting player, and start new round.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: The rules themselves are complete. Hand order for the illegal-choice fallback is unspecified, which is a minor gap. The game is finite (at most 32 rounds, within 40) and is decided by arithmetic. Two players, so no talk is needed.

The declared complexity is not credible.

Attributes: the rules say the game keeps placed counts per player per Geisha (2×7 = 14) and 7 markers. That is already 21, over the limit of 20, before adding:
- unused actions for 2 players (up to 8 flags or 2 lists),
- the hand number,
- the turn number,
- Charm held and Geisha held for each player,
- the deck, the 2 hands, the 2 secret cards and the out-of-play pile.
The stated 19 is an undercount.

Steps per round: every round's flat step list must contain the conditioned start-of-hand, turn and end-of-hand steps.
- Start of hand: shuffle, remove 1, deal ×2, reset tokens, reset 14 counts. That is at least 5 steps.
- Turn: draw, show state, active choice, Gift resolution, Competition resolution, placement into counts, spend token. That is about 7 steps.
- End of hand: reveal both secrets and add them to counts, compare 7 Geisha and move markers, compute Charm and Geisha held for both players, win check, hand-4 tiebreak. Each Geisha compare is a separate conditional update, and the engine has no lookup or attribute-compare operand, so this needs extra calc steps. That is well over 10 steps.
The total is roughly 25–30 steps, over 20, against a declared 15.

Hidden elements: hands, secret cards, deck order, removed card and Trade-off pile. These are 3 only if grouped generously.

As specified, the design exceeds the attribute and step limits.
- change: Cut attributes to 20 or fewer. Store each player's placed counts as one list attribute indexed G1–G7 (2 attributes instead of 14). Store all 7 markers as one list (1 attribute instead of 7). Store each player's unused actions as one list. Then recount honestly, including hand number, turn number, Charm held and Geisha held.
- change: Cut the per-round flat step list to 20 or fewer, counting every `when`-conditioned step. Do the end-of-hand work in a single calc step that compares the two count lists, updates the marker list, and computes Charm and Geisha held for both players. Fold the win check and the hand-4 tiebreak into one conditional winner step. Merge the start-of-hand reset into one step that resets the count lists and token lists.
- change: Restate the complexity block accurately (steps_per_round, attributes, hidden_elements). List the hidden elements explicitly: deck plus removed or Trade-off pile, the two hands, and the two secret cards. Show that they fit within 3.
- change: Define hand order for the illegal-choice fallback, e.g. cards kept in the order dealt or drawn.
The variation that was reviewed: Hanamikoji: Turn by Turn: COMPONENTS
- Seven Geisha, G1 to G7, with Charm values G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5 (21 in total).
- 21 Item cards. Each Geisha has as many Items as her Charm value: two G1, two G2, two G3, three G4, three G5, four G6, five G7.
- Each Geisha has a marker that is Neutral, on Player A's side, or on Player B's side. All markers start Neutral.
- Each player has four action tokens: Secret, Trade-off, Gift, Competition.

STRUCTURE
- The game has at most 4 hands. Each hand has 8 turns, alternating between players, so each player takes 4 turns per hand.
- Player A takes the first turn of hands 1 and 3. Player B takes the first turn of hands 2 and 4.
- One engine round is one turn, so the game lasts at most 32 rounds.

START OF EACH HAND (first turn of the hand only)
1. Shuffle all 21 Items.
2. Put the top card face-down in the out-of-play pile. Nobody sees it, ever.
3. Deal 6 cards to each player as a private hand. The remaining 8 cards form the deck, in shuffled order.
4. Each player gets back all four action tokens.
5. Every player's placed counts are reset to 0 for all seven Geisha. Markers are NOT reset.

EACH TURN
1. The active player takes the top card of the deck into their hand.
2. Both players are shown the public state: markers, both players' placed counts per Geisha, each player's unused actions, the hand number and the turn number. Each player privately sees their own hand.
3. The active player chooses one unused action and the cards for it:
   - SECRET: choose 1 card. It is set aside face-down as your secret card for this hand.
   - TRADE-OFF: choose 2 cards. They go face-down into the out-of-play pile, unseen by the opponent, and never score.
   - GIFT: choose 3 cards and reveal them.
   - COMPETITION: choose 4 cards and reveal them, arranged as Pair 1 (two cards) and Pair 2 (two cards).
4. If the action was Gift: the opponent chooses 1 of the 3 revealed cards. That card is placed on the opponent's side of its Geisha, and the other 2 go on the active player's side of their Geisha.
5. If the action was Competition: the opponent chooses Pair 1 or Pair 2. The chosen pair goes on the opponent's side, and the other pair goes on the active player's side.
6. Each placed card adds 1 to its owner's placed count for that card's Geisha. Placed cards are public.
7. The used action token is spent for this hand.
8. ILLEGAL CHOICES: if the active player names a spent action, a card they do not hold, or the wrong number of cards, the engine instead uses their lowest-numbered unused action (order: Secret, Trade-off, Gift, Competition) filled with the first cards of their hand in hand order. If an opponent's Gift or Competition pick is invalid, option 1 (the first card, or Pair 1) is used.

END OF EACH HAND (after the 8th turn only)
1. Both secret cards are revealed and added to their owners' placed counts.
2. For each Geisha, compare the two players' placed counts:
   - The player with the higher count moves that Geisha's marker to their side.
   - On a tie the marker stays where it is.
3. For each player, compute Geisha held (the number of markers on their side) and Charm held (the sum of Charm values of those Geisha).
4. Win check:
   - If a player has Charm held of 11 or more, that player wins immediately. Only one player can, since the total Charm is 21.
   - Otherwise, if a player has 4 or more Geisha held, that player wins. Only one player can, since there are 7 Geisha.
5. If nobody has won and this was hand 4, the game ends and the tiebreak decides.
6. Otherwise the next hand begins, with the other player starting.

INFORMATION
- Public: placed cards, revealed Gift and Competition cards, markers, and spent actions.
- Private: each hand (to its owner), and each secret card (to its owner, until the hand ends).
- Never revealed: the removed card and Trade-off cards.
- Players may use the known composition of the 21 Items to deduce what is still unaccounted for. Winner: After each hand, a player whose Geisha markers total 11 or more Charm wins. Otherwise, a player holding 4 or more Geisha markers wins. If neither has happened after hand 4, the player with the higher Charm held wins. If Charm is equal, the player with more Geisha held wins. If both are equal, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Hanamikoji is a two-player card game. Over repeated hands, players use four one-shot actions (Secret, Trade-off, Gift, Competition) to place Item cards beside seven Geisha. Gift and Competition force the opponent to split revealed cards. Winning a majority of a Geisha's Items wins her marker, and the first to 11 Charm or 4 Geisha wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy works. Always offering your best cards in Gift or Competition hands them to the opponent. Always hoarding by using Secret and Trade-off early leaves forced, transparent Gift and Competition offers late in the hand. Every player must use all four actions each hand, so there is no pass. The seat edge from moving first is removed by alternating the starting player each hand, which over 4 hands gives each seat two starts."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The deal varies, but each player sees 10 of their own cards per hand and controls their timing. Offers can be built so that every split favours the offerer, for example a Competition with two contested-Geisha pairs. A careless player loses Geisha systematically. The previous playtest found the rules sound; luck in the deal is spread over several hands."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Players can improve by sequencing actions, by tracking the 21-card composition to infer the opponent's hand and secret card, and by valuing Geisha differently by Charm and current marker. Ties keep markers, so marker holdings carry over between hands. A weak player still wins Geisha through the opponent's forced offers."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands, the secret card, the removed card and Trade-off discards are hidden. Picking from a Gift or Competition means inferring what the offerer is keeping back and what their secret card is likely to be. Making an offer means modelling which split the opponent will take."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Majority counts per Geisha, markers, Charm sums and the 11-Charm or 4-Geisha thresholds are all arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only, has no board and is decided by arithmetic. The previous variation exceeded the limits: about 21 or more attributes against 20, and about 25–30 flat steps against 20. It also left the hand order for the illegal-choice fallback unspecified. The game fits only when the state is packed into list attributes and the end-of-hand work is folded into one calculation."
    }
  ],
  "problems": [
    "Attribute count exceeded the limit: 14 per-Geisha count attributes and 7 marker attributes, plus action flags, hand and turn numbers, Charm and Geisha held, the deck, hands, secrets and pile, came to well over 20 while 19 was declared.",
    "Steps per round exceeded the limit: the start-of-hand, turn and end-of-hand steps, with a separate conditional update per Geisha comparison, totalled roughly 25–30 against a declared 15.",
    "Hidden elements were not listed explicitly, so it was unclear that they fit within 3.",
    "Hand order for the illegal-choice fallback was unspecified, so 'the first cards of their hand' was ambiguous.",
    "The declared complexity block was not credible."
  ],
  "changes": [
    {
      "what": "State is packed into 17 named attributes. Each player's placed counts are one 7-entry list. All seven markers are one 7-entry list. Each player's unused actions are one list. Charm held and Geisha held for both players are one 4-entry 'standing' list. One 'offer' list, one 'chosen action' and one 'pick' hold the current turn.",
      "why": "This replaces 14 count attributes and 7 marker attributes with 3, and keeps every tracked number within 20.",
      "fixes": "Attribute count exceeded the limit."
    },
    {
      "what": "Start-of-hand work is two conditioned steps: one shuffle, then one update that sets aside, deals, builds the deck and resets actions and counts. End-of-hand work is one step that adds the secrets, one calculation that compares the two count lists, updates the marker list and computes the standing list, one announcement, and one winner step that holds the win check and the hand-4 tiebreak. The fallback and the placement each become one step.",
      "why": "This brings the flat step list to 17 per round with 2 choice steps.",
      "fixes": "Steps per round exceeded the limit."
    },
    {
      "what": "The rules name exactly three hidden elements. (1) The hidden pile: the deck order plus the out-of-play pile, which holds the removed card and Trade-off cards. (2) The two private hands. (3) The two secret cards.",
      "why": "This makes the information structure explicit and verifiably within 3.",
      "fixes": "Hidden elements were not listed explicitly."
    },
    {
      "what": "Hand order is defined. Dealt cards are kept in deal order, each drawn card is added at the end, and removing cards keeps the order of the rest. The fallback uses the first cards in this order. The rules also show that a legal fallback always exists, because hand size always covers the remaining actions.",
      "why": "This removes the ambiguity in the illegal-choice rule.",
      "fixes": "Hand order for the illegal-choice fallback was unspecified."
    },
    {
      "what": "The complexity block is restated from an explicit count of steps and attributes, both listed in the rules.",
      "why": "This makes the declared numbers match the build.",
      "fixes": "The declared complexity block was not credible."
    }
  ],
  "keeps": [
    "Seven Geisha with Charm values 2,2,2,3,3,4,5 and 21 matching Item cards.",
    "The four one-shot actions per hand: Secret, Trade-off, Gift (opponent takes 1 of 3) and Competition (opponent takes 1 of 2 pairs).",
    "One card removed unseen each hand, 6-card hands and an 8-card deck with one draw per turn.",
    "Majority per Geisha wins her marker, ties leave the marker where it is, and markers carry over between hands.",
    "The win at 11 Charm or 4 Geisha, with Charm taking precedence.",
    "The alternating starting player, and all the gameplay rules that the previous test found complete and sound."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game is strategically rich and its rules were found complete. Only the build footprint was over the limits, and packing the state into lists plus one end-of-hand calculation brings it within them without changing play."
  },
  "variation": {
    "name": "Hanamikoji: Compact Build",
    "summary": "Two players fight over seven Geisha across up to 4 hands of 8 alternating turns. They use four one-shot actions to place, hide, discard or offer Item cards. Gift and Competition force the opponent to split revealed cards. Majorities win Geisha markers, and the first to 11 Charm or 4 Geisha wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS\n- Seven Geisha, G1 to G7. Charm values: G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5 (21 in total).\n- 21 Item cards. Each Geisha has as many Items as her Charm value: two G1, two G2, two G3, three G4, three G5, four G6, five G7. A card is named by its Geisha (for example 'G6').\n- Each player has four action types: Secret, Trade-off, Gift, Competition.\n\nTRACKED STATE (17 attributes)\n1. deck: ordered list of cards, hidden.\n2. pile: the out-of-play list, hidden from everyone forever.\n3. hand_A: Player A's ordered hand, seen only by A.\n4. hand_B: Player B's ordered hand, seen only by B.\n5. secret_A: seen only by A until the end of the hand.\n6. secret_B: seen only by B until the end of the hand.\n7. counts_A: 7 numbers, A's placed cards per Geisha.\n8. counts_B: 7 numbers, B's placed cards per Geisha.\n9. markers: 7 entries, each 'A', 'N' or 'B'. All start 'N'.\n10. actions_A: A's unused actions this hand.\n11. actions_B: B's unused actions this hand.\n12. hand_number: 1 to 4.\n13. turn_number: 1 to 8 within the hand.\n14. standing: [Charm held by A, Charm held by B, Geisha held by A, Geisha held by B], all starting 0.\n15. chosen_action.\n16. offer: the cards revealed this turn, in order, split into Pair 1 and Pair 2 for Competition.\n17. pick.\n\nHIDDEN ELEMENTS (3)\n(1) The hidden pile: the deck order plus the out-of-play pile, which holds the removed card and all Trade-off cards.\n(2) The private hands.\n(3) The secret cards.\n\nSTRUCTURE\n- One engine round is one turn. A hand has 8 turns, and the game lasts at most 4 hands, so at most 32 rounds.\n- Active player: in hands 1 and 3, Player A acts on odd turns and B on even turns. In hands 2 and 4, Player B acts on odd turns and A on even turns.\n\nHAND ORDER\n- Cards dealt to a hand keep the order they were dealt in.\n- A drawn card goes to the end of the hand.\n- When cards leave a hand, the remaining cards keep their order.\n\nSTEPS OF EACH ROUND\n1. (Turn 1 only) Shuffle all 21 Items.\n2. (Turn 1 only) The first card goes to the pile. Cards 2–7 go to the first player's hand and cards 8–13 to the second player's hand, where the first player is the one who acts on turn 1. Cards 14–21 form the deck in that order. Both action lists are reset to all four actions. Both count lists are reset to seven zeros. Both secrets are emptied. Markers and standing are NOT reset.\n3. The active player moves the first card of the deck to the end of their hand.\n4. Show both players: the markers, both count lists, both unused-action lists, the standing, the hand number and the turn number. Each player privately sees their own hand and their own secret.\n5. CHOICE: the active player names one unused action and the cards for it:\n   - Secret: 1 card.\n   - Trade-off: 2 cards.\n   - Gift: 3 cards.\n   - Competition: 4 cards, the first two being Pair 1 and the last two Pair 2.\n6. FALLBACK: the choice is illegal if it names a spent action, a card not held (counting duplicates), or the wrong number of cards. In that case the engine uses the active player's first unused action in the order Secret, Trade-off, Gift, Competition, filled with the first cards of their hand in hand order. A legal fallback always exists, because a player's hand always holds at least as many cards as their remaining actions need: 7 cards against at most 4 needed on their first turn, and exactly the number needed on their last.\n7. The chosen cards leave the hand:\n   - Secret: the card becomes the active player's secret.\n   - Trade-off: both cards go face-down to the pile.\n   - Gift or Competition: the cards go to the offer.\n8. (Gift or Competition only) The offer is revealed to both players.\n9. (Gift or Competition only) CHOICE: the opponent picks. For Gift they pick card 1, 2 or 3 of the offer. For Competition they pick Pair 1 or Pair 2.\n10. (Gift or Competition only) An invalid pick becomes option 1.\n11. Placement:\n   - Gift: the picked card adds 1 to the opponent's count for its Geisha, and the other two cards add 1 each to the active player's counts.\n   - Competition: the picked pair adds to the opponent's counts and the other pair to the active player's counts.\n   Placed cards are public.\n12. The used action is removed from the active player's action list. The offer, chosen action and pick are cleared. The turn number goes up by 1.\n13. (After turn 8 only) Both secrets are revealed, each adds 1 to its owner's count for its Geisha, and both secrets are emptied.\n14. (After turn 8 only) One calculation, for each Geisha i from 1 to 7:\n   - if counts_A[i] > counts_B[i], markers[i] becomes 'A';\n   - if counts_B[i] > counts_A[i], markers[i] becomes 'B';\n   - otherwise markers[i] is unchanged.\n   Then standing is set to [sum of Charm of the 'A' markers, sum of Charm of the 'B' markers, number of 'A' markers, number of 'B' markers].\n15. (After turn 8 only) Announce the markers and the standing.\n16. (After turn 8 only) Winner check:\n   - A player with 11 or more Charm wins. Only one player can, since the total Charm is 21.\n   - Otherwise, a player with 4 or more Geisha wins. Only one player can.\n   - Otherwise, if this was hand 4, the game ends: higher Charm wins, then more Geisha, else a draw.\n17. (After turn 8 only, if the game has not ended) The hand number goes up by 1 and the turn number is set back to 1. The next hand's first player is the other player.\n\nINFORMATION\n- Public: placed cards and counts, revealed offers, picks, markers, standing, and spent actions.\n- Private: each hand, and each secret until the end of the hand.\n- Never revealed: the pile.\n- Players may use the known 21-card composition to deduce unseen cards.",
    "objective": "At the end of each hand, a player whose markers total 11 or more Charm wins. Otherwise, a player holding 4 or more Geisha markers wins. If neither has happened after hand 4, higher Charm held wins, then more Geisha held, and if both are equal the game is a draw.",
    "expected_effect": "Play is unchanged from the previously tested version, which was strategically sound: players sequence their four actions, build offers whose every split favours them, and infer hidden secrets and hands from the 21-card composition. The changes only make the game buildable within 17 attributes, 17 steps, 2 choice steps, 3 hidden elements and 1 random draw per round, and they remove the fallback ambiguity. There are two players, so there is no talk phase."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 2,
    "attributes": 17,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 32
  }
}
```
````
