# Kobayakawa: Held Cards

A bluffing and betting game over 10 rounds. Each player holds one secret card and may keep, swap or shift the bonus card, then decides in seat order whether to fight for the kamon pot. A passer may carry their card into later rounds.

Players: 3 to 5, best with 4

## Parameters

- `starting_kamons` = 4
- `centre_kamons` = 11
- `starting_pot` = 0
- `card_min` = 1
- `card_max` = 15
- `total_rounds` = 10
- `min_stake_rounds_1_to_9` = 1
- `min_stake_round_10` = 2
- `high_stake_extra` = 1
- `centre_feed_rounds_1_to_9` = 1
- `first_start_seat` = 1

## Round

1. **update** (engine): Set min_stake = 1 if round <= 9, else 2. Set high_fought = false and winner_seat = 0. Clear face_up_discards, and clear each player's draw_choice, keep_choice, fight_choice, stake, shown_card, total and reserve_seen. Set deck = the cards 1..15 minus every active player's hand (where hand > 0), then shuffle it.
2. **update** (each active player with hand = 0): Draw one card at random from deck into hand (visible only to the owner) and remove it from deck.
3. **update** (each active player): Draw one card at random from deck and append it to reserves at that seat's position; remove it from deck. Nobody sees it.
4. **update** (engine): Draw one card from deck into kobayakawa (public) and one into alternate (hidden), removing each from deck.
5. **tell** (all players): Announce round, kobayakawa, pot, every player's kamons, every player with held_rounds > 0 and their held_rounds, start_seat, and min_stake.
6. **sync** (all players): Each player is sent their own state, including their hand.
7. **poll** (all active players): Store the answer in draw_choice. It is not shown until step 6.
8. **update** (each active player with draw_choice = DRAW): Set reserve_seen = that seat's card in reserves; only the owner sees it.
9. **poll** (active players with draw_choice = DRAW): Store the answer in keep_choice. If NEW: append hand to face_up_discards, then set hand = reserve_seen. If OLD: append reserve_seen to face_up_discards. Then clear reserves; undrawn reserves are discarded face down, unseen. If a player chose NEW, set held_rounds = 0.
10. **tell** (all players): Announce every active player's draw_choice and the contents of face_up_discards.
11. **update** (engine): If the count of players with draw_choice = SHIFT is >= 1, set kobayakawa = alternate and announce the new kobayakawa.
12. **poll** (all active players): Broadcast every message to all as {"to": "all", "text": "Seat {seat} says: {value}"}. Talk is not binding.
13. **ask** (each active player in turn, in seat order starting at start_seat and wrapping around): Store the answer in fight_choice. If LOW, set stake = min_stake. If HIGH, set stake = min_stake + 1 and high_fought = true. If PASS, set stake = 0.
14. **update** (engine): For each player: kamons -= stake and pot += stake. Then the centre feeds the pot: if round <= 9, move min(1, centre) from centre to pot; if round = 10, move all of centre to pot.
15. **update** (engine): Let F = the number of players with fight_choice in {LOW, HIGH}. If F = 1, set winner_seat = that fighter and move the whole pot to their kamons; their card is not revealed. If F >= 2: for each fighter set shown_card = hand and total = hand, and add kobayakawa to the total of the fighter with the lowest hand. If exactly one fighter has the highest total, move the whole pot to them and set winner_seat to their seat. If F = 0, the pot carries.
16. **update** (engine): If F >= 2 and two or more fighters share the highest total: if round <= 9, the pot carries. If round = 10, each tied fighter gains floor(pot / number tied), and pot is set to 0 (the remainder leaves the game).
17. **tell** (all players): Announce every fight_choice, every shown_card and total, the pot result, and every player's kamons.
18. **update** (engine): Each fighter sets hand = 0 and held_rounds = 0. Each active passer keeps hand and adds 1 to held_rounds. For each active player with kamons = 0, set active = false and hand = 0 (their card is discarded unseen). Then set start_seat = winner_seat if winner_seat > 0; otherwise the next active seat after the old start_seat, wrapping. Then add 1 to round.
19. **check** (engine): End the game if round > 10 or the count of active players <= 1. Otherwise continue.

## Ending

- ends when: round > 10 or count(active players) <= 1
- ranked by: `you.kamons` (the highest wins; players level at the top share the win)
- decided by: The player with the most kamons wins. Eliminated players have 0. If only one player remains active, that player has the most kamons and wins. Players tied for the most share the result, which stands for the source's draw.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer chose 4. Three is the smallest table where fight order, reads and pot competition work. Five fits the 15-card deck: up to 5 hands, 5 reserves and 2 table cards is 12 cards, and more players would stretch the fight sequence.
- Talk kept as one simultaneous poll: The source specifies it. Bluffing about hand strength gives players something to disagree about.
- A SHIFT voter keeps their hand card: SHIFT replaces neither the hand nor the reserve, so the hand stays.
- Next start seat chosen after eliminations, skipping eliminated seats: The source says 'next active seat'.
- Centre feed in rounds 1-9 is limited by what remains: The centre cannot go negative.
- A drawer who keeps NEW has held_rounds reset to 0: Their card is no longer one kept from an earlier round.

## Simplifications

- A tie for the most kamons is a shared win rather than a declared draw: The engine treats players level at the top as sharing the win, with no separate draw.
- Reserve cards are kept in a hidden table list, indexed by seat: A player attribute cannot be hidden from its own owner, and the rules say the reserve is unseen until drawn.

## Unsupported (needs engine work)

- none
