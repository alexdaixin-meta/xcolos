# Three Fronts

Two players fight 4 battles of 6 rounds over three theaters (Air, Land, Sea). Each round a player deploys a card face-up, improvises it face-down for strength 2, or withdraws to give up fewer VP; winning 2 of 3 theaters scores 6 VP.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 18
- `suits` = 3
- `ranks_per_suit` = 6
- `min_rank` = 1
- `max_rank` = 6
- `battles` = 4
- `rounds_per_battle` = 6
- `total_rounds` = 24
- `hand_size` = 6
- `set_aside_cards` = 6
- `improvise_strength` = 2
- `withdraw_min_cards_held` = 1
- `withdraw_vp_4_or_more_cards` = 4
- `withdraw_vp_value_4_or_more` = 2
- `withdraw_vp_value_2_or_3` = 3
- `withdraw_vp_value_1` = 4
- `theaters_to_win_battle` = 2
- `battle_win_vp` = 6
- `starting_vp` = 0

## Round

1. **update** (all players): When round_in_battle == 1: the deck is reset to all 18 cards. Each player's hand, face_up_cards, face_down_theaters and face_down_cards are emptied, and air_strength, land_strength and sea_strength are set to 0. battle_over is set to false. Each player then draws 6 cards at random: each card is removed from deck and appended to that player's hand. The remaining 6 deck cards are moved to set_aside, unseen.
2. **sync** (all players): Each player is sent their own hand and the public state: strengths, face-up cards, face-down theaters, vp, battle, round_in_battle and first_player.
3. **ask** (the seat equal to first_player): Only when battle_over == false. DEPLOY: the card is removed from hand and appended to face_up_cards, and the strength attribute of the card's suit rises by its rank. IMPROVISE: the card is removed from hand, '<card> in <theater>' is appended to face_down_cards, the theater is appended to face_down_theaters, and that theater's strength rises by 2. WITHDRAW: with n = the number of cards in the withdrawer's hand, the opponent's vp rises by 2 if n >= 4, by 3 if n is 2 or 3, and by 4 if n == 1; battle_over is set to true.
4. **tell** (all players): Only when that action was taken: everyone is told the result. A deploy names the card and its theater. An improvise names only the theater ('a face-down card was placed in X'). A withdraw states the VP awarded. The updated strengths are shown.
5. **ask** (the seat not equal to first_player): Only when battle_over == false. The effects are the same as for the first player's action.
6. **tell** (all players): Only when that action was taken: everyone is told the result in the same way, with face-down card identities hidden.
7. **update** (all players): When round_in_battle == 6 and battle_over == false: for each theater, seat 1 controls it if seat 1's strength > seat 2's strength. On an equal sum, including 0-0, the seat equal to first_player controls it. Otherwise seat 2 controls it. seat1_theaters and seat2_theaters are set to these counts. The seat with 2 or more theaters gains 6 vp.
8. **tell** (all players): When round_in_battle == 6 and battle_over == false: the control of each theater and the battle winner are announced, and each player's face_down_cards are revealed to everyone for the record.
9. **update** (all players): If round_in_battle == 6: battle rises by 1, round_in_battle becomes 1 and first_player becomes 3 - first_player. Otherwise round_in_battle rises by 1.
10. **check** (all players): The game ends if battle > 4, which is after round 24. Otherwise play continues.

## Ending

- ends when: battle > 4
- ranked by: `you.vp` (the highest wins; players level at the top share the win)
- decided by: After 4 battles (24 rounds), the player with more VP wins. Equal VP is a draw, in which both players share the win.

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed the game at 2. It is a head-to-head duel over who controls each theater, and the first-player alternation and the withdrawal payoffs are built for two sides.
- No talk step before actions: The source has no negotiation. In a two-player zero-sum duel, talk would only add words, and bluffing already happens through face-down cards and withdrawal timing.
- Seat 1 is Player A and seat 2 is Player B: The source names A and B but does not say who is who.
- Strength totals are public: Face-down cards always count 2, so each side's strength sum is known to both players. Only the identity of face-down cards is hidden.
- Strategy at the table: A thoughtful player decides which theaters to contest and which to concede, uses improvise to bluff or to shore up a theater, and withdraws early (giving up 2 VP) when the battle is lost rather than giving up 6.

## Simplifications

- The three possible actions are offered as one choice list combining action, card and theater: The engine takes one choice per question. A single list keeps each action to one step.
- The stacking order of cards is not tracked: Every card counts whether or not it is covered, so the order has no effect on play.
- Theater control is compared through the table scratch values seat1_theaters and seat2_theaters: This is the engine's workaround for comparing two players' attributes.

## Unsupported (needs engine work)

- none
