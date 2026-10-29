# Air, Land and Sea: Three Fronts

Two commanders fight a series of 6-round battles over three theaters, placing cards face-up or face-down and deciding each round whether to withdraw; the first to 12 VP wins.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 18
- `theaters` = 3
- `min_strength` = 1
- `max_strength` = 6
- `hand_size` = 6
- `max_match_rounds` = 36
- `battle_rounds` = 6
- `last_battle_start_round` = 31
- `withdraw_base_vp` = 2
- `facedown_strength` = 3
- `battle_win_vp` = 4
- `sweep_vp` = 6
- `target_vp` = 12

## Round

1. **update** (all players): When battle_round == 1: deck is set to all 18 cards; each player's hand, faceup_played and facedown_played are emptied and air, land and sea are set to 0; then 6 random cards are moved from deck to each player's hand (6 draws each). The 6 cards left in deck stay unseen.
2. **sync** (all players): Each player sees their own hand in the order dealt, their facedown_played, and all public state.
3. **poll** (all players): Sets withdraw_choice for each player; nobody sees the other's answer until both are in.
4. **update** (all players): If exactly one player's withdraw_choice is Withdraw, the other player's vp += 2 + floor((battle_round - 1) / 2). If at least one player withdrew, battle_over = true. Both choices are announced.
5. **poll** (all players): When battle_over is false: sets card_choice for each player; it stays secret until placement.
6. **poll** (all players): When battle_over is false: sets theater_choice for each player; it stays secret until placement.
7. **update** (all players): When battle_over is false: card_choice is removed from each player's hand. If its theater equals theater_choice, it is appended to faceup_played and its printed strength is added to that player's attribute for theater_choice (air, land or sea). Otherwise it is appended to facedown_played and 3 is added to that attribute.
8. **tell** (all players): When battle_over is false: both new placements are announced. A face-up card shows its identity and theater. A face-down card shows only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced (each player's air, land and sea).
9. **update** (all players): When battle_round == 6 and battle_over is false: in each theater the player with the higher strength controls it, and a tie means nobody does. The player controlling more theaters wins. If both control the same number, the player with the higher air+land+sea wins. If that is also equal, the battle is drawn and nobody scores. The winner's vp += 6 if they control all 3 theaters, otherwise += 4. battle_over = true.
10. **tell** (all players): When the battle was just resolved at battle_round 6: the battle result is announced and every card in both players' facedown_played is revealed to both players.
11. **update** (all players): match_round += 1. If battle_over is true: battle_round = 1 and battle_over = false, and if match_round > 31 then match_over = true. Otherwise battle_round += 1.
12. **check** (all players): End the game if any player's vp >= 12, or match_over is true, or match_round > 36. Otherwise continue with the next round.

## Ending

- ends when: any player's vp >= 12 OR match_over == true OR match_round > 36
- ranked by: `you.vp` (the highest wins; players level at the top share the win)
- decided by: A player's standing is their VP. The first player to reach 12 VP wins; only one player can score in a battle, so both cannot reach 12 together. If the match ends on the round limit, the player with more VP wins, and equal VP is a draw (both share the result).

## Choices the source did not make

- 2 players (min 2, max 2, suggested 2): The designer fixed the game at 2. It is a head-to-head duel of bluffing and tempo: theater control is a two-sided comparison, and withdrawal VP go to 'the other player'. More seats would break both.
- No talk step: The source has no communication. With two opponents in a zero-sum duel, talk would only add bluffing words that the rules do not call for.
- Card choice and theater choice are two separate simultaneous polls: The source lists them as separate simultaneous steps. Neither answer is revealed until placement.
- Steps after the withdrawal are skipped with a `when battle_over is false` condition: This ends the battle immediately within a flat step list.
- The round limit is enforced through match_over, set when the next match round after a battle ends would be greater than 31: This states the rule that only a full battle may start.
- Card names are written as text like 'Air 4': Each card is identified by its theater and strength.

## Simplifications

- A drawn match (equal VP at the round limit) is shown as both players sharing the top rank: The engine has no separate draw; players level at the top share the result.
- The battle resolution (controls, tie-break by total strength, 4 or 6 VP) is computed in one update step with conditional operations: It is all arithmetic on air, land and sea, so it needs no referee.

## Unsupported (needs engine work)

- none
