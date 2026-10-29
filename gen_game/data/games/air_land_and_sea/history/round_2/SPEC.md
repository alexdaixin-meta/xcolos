# Air, Land and Sea: Four Battles

Two commanders fight 4 battles of 6 rounds over three theaters, playing cards face-up for their strength or face-down for 2, and may withdraw early to limit the VP the opponent gains.

Players: 2 to 2, best with 2

## Parameters

- `total_cards` = 18
- `theaters` = 3
- `min_strength` = 1
- `max_strength` = 6
- `total_rounds` = 24
- `battles` = 4
- `rounds_per_battle` = 6
- `hand_size` = 6
- `set_aside_count` = 6
- `improvise_strength` = 2
- `withdraw_vp_4_plus_cards` = 2
- `withdraw_vp_2_or_3_cards` = 3
- `withdraw_vp_1_card` = 4
- `battle_win_vp` = 6
- `theaters_to_win_battle` = 2

## Round

1. **update** (all players): Set battle = floor((round-1)/6)+1. Set round_in_battle = round - 6*(battle-1). Set first_seat = 1 if battle is 1 or 3, and 2 if battle is 2 or 4. Announce the round, the battle and the first player.
2. **update** (all players): Only when round_in_battle = 1 (battle start): set battle_over = false. Set every player's air, land and sea to 0. Return every card in each hand, face_up, face_down and set_aside to deck, so deck holds all 18 cards. Draw 6 cards at random from deck into each player's hand, removing each from deck. Move the remaining 6 deck cards to set_aside.
3. **sync** (all players): Each player privately sees their own hand and face_down, plus every public attribute: all air, land and sea strengths, all face_up cards, vp, round, battle, first_seat and battle_over.
4. **ask** (the seat named by first_seat, only when battle_over is false): Deploy: remove the card from hand, append it to face_up, and add its number to the player's strength in the theater named on the card. Improvise: remove the card from hand, append it with the chosen theater to face_down, and add 2 to the player's strength in the chosen theater; only the theater and the +2 are announced. Withdraw: let n = length of the player's hand; the opponent's vp += 4 if n = 1, 3 if n is 2 or 3, and 2 if n >= 4; set battle_over = true.
5. **ask** (the seat that is not first_seat, only when battle_over is false): Same effects as the first player's action, applied to this player.
6. **update** (all players): Only when round_in_battle = 6 and battle_over is false (battle end): in each of air, land and sea, the player with the higher strength controls that theater, and a tie goes to the first_seat player. The player who controls 2 or more theaters gains vp += 6. Set battle_over = true. Announce the strengths and the battle winner.
7. **check** (all players): If round = 24, end the game. Otherwise continue.
8. **update** (all players): round += 1.

## Ending

- ends when: round = 24 after that round's steps have run
- ranked by: `you.vp` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total VP after round 24. The player with more VP wins. Equal VP is a draw, and both players share the win.

## Choices the source did not make

- Exactly 2 players: The designer fixed the table at 2. Theater control is a head-to-head comparison, the tie rule names the battle's first player, and withdrawal VP goes to 'the opponent', so the game is defined only for two.
- No talk step: The source has none. With two directly opposed players there is no coalition to form, so talk would only add words. The strategy lies in bluffing with face-down cards, reading the opponent's public strengths and judging when to withdraw cheaply.
- Actions use sequential ask: The rules order the first player before the second, and the second player reacts to the first player's public play.
- Withdrawal VP for 0 cards is not defined: A player always holds at least 1 card when acting, since 6 cards cover 6 actions, so the 0-card case never occurs.

## Simplifications

- Theater control compares two players' attributes: The engine has no player-attribute operand. The comparison of seat 1's and seat 2's air, land and sea is done with a table-attribute mirror beside the strengths, the listed workaround; the outcome is unchanged.
- Battle start is a single update with operations guarded by round_in_battle = 1: The step list is flat, so conditional operations replace a separate block. The behavior is identical.
- Shuffling is modeled as random draws from the deck list: Drawing at random is equivalent to shuffling and then dealing.

## Unsupported (needs engine work)

- none
