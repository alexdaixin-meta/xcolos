# Cash and Guns: Standoff

Over 8 rounds, gangsters bluff with a private hand of 3 Bang and 5 Click bullets, aim at each other, then Stand or Duck; the unwounded players who Stand split the pot, and three wounds eliminate a player.

Players: 3 to 5, best with 4

## Parameters

- `rounds` = 8
- `starting_cash` = 0
- `starting_wounds` = 0
- `bang_cards` = 3
- `click_cards` = 5
- `hand_size` = 8
- `pot_min` = 6
- `pot_max` = 14
- `pot_unit_dollars` = 1000
- `wounds_per_bang` = 1
- `wounds_to_eliminate` = 3
- `talk_messages_per_round` = 1
- `rank_alive_weight` = 1000000
- `rank_cash_weight` = 1000
- `rank_wound_weight` = 1

## Round

1. **update** (all players): round += 1. pot = a random whole number from 6 to 14. Each living player's target, aim_target, bullet and stance are set to empty, fired to false and hit_this_round to 0. Announce: 'Round {round}: the pot is {pot} thousand dollars.'
2. **poll** (all living players): Nothing changes. Every message is broadcast to all players as 'Seat {seat} says: {value}'. Nothing said is binding.
3. **poll** (all living players): The chosen seat is stored in aim_target, which stays hidden from the others for now.
4. **poll** (all living players): The chosen card is stored in bullet, which stays hidden.
5. **update** (all living players): GUNS SHOWN: target = aim_target for every living player. Announce every seat's target. Bullets stay hidden.
6. **poll** (all living players): The choice is stored in stance. Announce every seat's stance once all are in.
7. **update** (all living players): FIRE: For each living player, one card equal to bullet is removed from hand. fired = (stance == Stand and the target's stance == Stand). If fired, bullet is appended to revealed_bullets and announced publicly. Then each living player's hit_this_round = the number of players with target == this seat, fired == true and bullet == Bang, and wounds += hit_this_round. All shots resolve at once.
8. **update** (all living players): ELIMINATION: if wounds >= 3, then alive = false and the elimination is announced. Afterwards, living = the count of players with alive == true.
9. **update** (all players): SPLIT: sharers = the count of players with alive == true, stance == Stand and hit_this_round == 0. If sharers > 0, then each of those players gets cash += pot / sharers. Otherwise the pot is lost. Announce the gains.
10. **check** (all players): The game ends if living <= 1 or round >= 8. Otherwise the next round starts.

## Ending

- ends when: living <= 1 or round >= 8
- ranked by: `you.alive * 1000000 + you.cash * 1000 + you.wounds` (the highest wins; players level at the top share the win)
- min_to_win: `1000000` (a player below it cannot win; if none reaches it, nobody wins)
- decided by: Only living players can win. Among them, the highest cash wins, and if cash is tied, the most wounds wins. Players still tied share the win, which is the source's draw. A lone survivor wins. If nobody is alive, no one reaches the bar, so the game has no winner and is a draw.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer chose 4, so it is kept. The minimum is 3, because with 2 players aiming has no choice and splitting the pot is trivial. The maximum is 5, because beyond that a single gun matters little and the talk is long.
- Keep a simultaneous talk poll each round, broadcast to all: The source requires it. Players disagree about who should duck and who gets shot, so non-binding threats and bluffs about bullets give them something to reason about.
- Target and bullet are taken in two consecutive polls, with the target held in a hidden aim_target until GUNS SHOWN: A step takes one answer. Holding the target hidden keeps both choices simultaneous and secret, as the source requires.
- rank_by = alive*1000000 + cash*1000 + wounds, with min_to_win 1000000: Only living players can win, cash comes first and wounds break ties. Cash differences are multiples of 1/60, so the weight 1000 keeps them above the maximum wound gap of 2. The bar makes an all-eliminated game end with no winner.

## Simplifications

- A tie on both cash and wounds is a shared win: The engine has no separate draw: players level at the top share the win, which stands for the source's draw.
- Comparing a player's stance with their target's stance, and counting the Bangs aimed at a seat, uses the player-attribute-compare workaround: The engine has no direct operand for another player's attribute, so this costs extra steps.

## Unsupported (needs engine work)

- none
