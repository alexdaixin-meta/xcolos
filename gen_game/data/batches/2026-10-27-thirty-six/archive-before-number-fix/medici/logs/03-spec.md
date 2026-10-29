# 03 spec

- time: 2026-10-27T16:40:41+00:00 (62.4s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0c3fdf2fc913cf43, reply sha256 f112d0dc615c3ec3

## Sent

````
Game: Medici: Sealed Ledgers
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP. Each player starts with 40 florins. Florin totals are private to each player, and the engine tracks them. The deck has 48 cards: 4 goods (Grain, Cloth, Spice, Dye) with 12 cards each. Each good has the card values 0,1,1,2,2,3,3,3,4,4,5,5. Each player is secretly dealt a different favoured good, chosen at random from the 4, and only that player knows it. Seats are numbered 1 to N. The active player in round r is seat ((r-1) mod N)+1.

DAYS AND ROUNDS. The game lasts 3 days. Each day has 2N rounds: 6 rounds with 3 players, 8 with 4. The game therefore has 6N rounds in total (18 or 24). At the start of each day, all 48 cards are shuffled into a fresh deck, and every ship is empty. A ship holds at most 5 cards.

EACH ROUND:
1. Reveal. The top 3 cards of the deck are revealed to everyone, in order, as cards A, B and C.
2. Lot size. The active player chooses 1, 2 or 3. The lot is card A, cards A and B, or cards A, B and C. Unchosen revealed cards are discarded. The lot is announced.
3. Sealed bids. All players, including the active player, at the same moment secretly bid a whole number of florins from 0 up to their own current florins. A bid of 0 is a pass.
4. Validity. A bid is treated as 0 if loading the lot would put that player's ship over 5 cards.
5. Winner. The highest valid bid above 0 wins. Ties go to the active player if tied. Otherwise they go to the tied player who comes first in seating order starting after the active player. If every bid is 0, the lot is discarded.
6. Payment and loading. The winner pays the bid to the bank and loads the lot onto their ship. The winner's ship value rises by the sum of the lot's card values. Their ship card count rises by the lot size. Their game-long count of each good rises by the number of cards of that good in the lot.
7. Announcement. The engine announces the winner, the price paid, and every player's ship card count. It does not announce florin totals.

END OF DAY (after the last round of each day):
- The highest ship value earns 15 florins. The second-highest earns 7. If several players tie for highest, they split 22 florins equally, rounded down, and no second place is paid. If several tie for second, they split 7 equally, rounded down. A ship value of 0 earns nothing.
- Then all ships are emptied: value 0, card count 0. The game-long good counts are kept.

END OF GAME (after day 3 scoring):
- Majorities. For each good, the player with the most cards of it over the whole game earns 10 florins. Ties split 10 equally, rounded down. If nobody has any cards of a good, nothing is paid for it.
- Favoured good. Each player earns 3 florins per card of their own favoured good collected over the game. Favoured goods are then revealed.

There is no talk phase.

How the winner is decided: After the end-of-game scoring, the player with the most florins wins. If several tie for most, the tied player with more total cards collected over the game wins. If still tied, the game is a draw.
````

## Reply

````
```json
{
  "name": "Medici: Sealed Ledgers",
  "summary": "Over 3 days the active player picks a lot of 1 to 3 revealed goods cards, everyone bids for it in a sealed auction, the best ship each day pays out, and at the end good majorities and secret favoured goods pay out. Most florins wins.",
  "players": {"min": 3, "max": 4, "suggested": 4},
  "parameters": {
    "starting_florins": 40,
    "goods_count": 4,
    "cards_per_good": 12,
    "deck_size": 48,
    "card_values_per_good": "0,1,1,2,2,3,3,3,4,4,5,5",
    "days": 3,
    "rounds_per_day_per_player": 2,
    "rounds_per_day": "2*N",
    "total_rounds": "6*N",
    "cards_revealed_per_round": 3,
    "min_lot_size": 1,
    "max_lot_size": 3,
    "ship_capacity": 5,
    "min_bid": 0,
    "day_first_prize": 15,
    "day_second_prize": 7,
    "day_tied_first_pool": 22,
    "majority_prize": 10,
    "favoured_per_card": 3,
    "rank_florins_weight": 1000
  },
  "attributes": {
    "player": [
      {"key": "florins", "type": "number", "visible": "ally", "initial": 40, "meaning": "Florins held. This is the score and is private to its owner.", "observable": true},
      {"key": "favoured_good", "type": "text", "visible": "ally", "initial": "", "meaning": "Secret favoured good (Grain, Cloth, Spice or Dye). It is different for every player and revealed at game end.", "observable": false},
      {"key": "bid", "type": "number", "visible": "ally", "initial": 0, "meaning": "This round's sealed bid. It is set to 0 if the bid is invalid.", "observable": false},
      {"key": "ship_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Cards loaded on the ship today.", "observable": false},
      {"key": "ship_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of card values on the ship today.", "observable": false},
      {"key": "ship_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards on the ship today (at most 5).", "observable": true},
      {"key": "grain_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Grain cards collected over the whole game.", "observable": false},
      {"key": "cloth_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Cloth cards collected over the whole game.", "observable": false},
      {"key": "spice_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Spice cards collected over the whole game.", "observable": false},
      {"key": "dye_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Dye cards collected over the whole game.", "observable": false},
      {"key": "total_cards", "type": "number", "visible": "public", "initial": 0, "meaning": "Total cards collected over the game. This is the tie-break.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "48 cards: Grain-0, Grain-1, Grain-1, Grain-2, Grain-2, Grain-3, Grain-3, Grain-3, Grain-4, Grain-4, Grain-5, Grain-5, and the same 12 values for Cloth, Spice and Dye", "meaning": "Today's shuffled deck. Drawing a card takes one at random.", "observable": false},
      {"key": "revealed", "type": "list", "visible": "public", "initial": [], "meaning": "Cards A, B and C revealed this round, in order.", "observable": false},
      {"key": "lot", "type": "list", "visible": "public", "initial": [], "meaning": "The cards on offer this round.", "observable": false},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "Unchosen revealed cards and unsold lots for today.", "observable": false},
      {"key": "lot_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in the lot (1 to 3).", "observable": false},
      {"key": "lot_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the card values in the lot.", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Round number, from 1 to 6N.", "observable": true},
      {"key": "day", "type": "number", "visible": "public", "initial": 1, "meaning": "Current day, from 1 to 3.", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Active player, equal to ((round-1) mod N)+1.", "observable": false},
      {"key": "winner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won this round's lot (0 if nobody did).", "observable": false},
      {"key": "price_paid", "type": "number", "visible": "public", "initial": 0, "meaning": "Winning bid paid this round.", "observable": false}
    ]
  },
  "setup": [
    "Every player gets 40 florins, kept private to that player.",
    "The four goods Grain, Cloth, Spice and Dye are shuffled, and each player is secretly dealt a different one as favoured_good, without replacement.",
    "Seats are numbered 1 to N. round=1, day=1 and active_seat=1.",
    "Ship cards, ship_value, ship_count, the four good counts and total_cards all start at 0 or empty."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "If round mod (2N) == 1 (first round of a day), the deck is rebuilt as all 48 cards, discard is emptied and every ship_cards, ship_value and ship_count is reset to empty or 0. Then active_seat = ((round-1) mod N)+1, and winner_seat and price_paid are set to 0."},
    {"action": "update", "who": "table", "answer": null, "effect": "Three cards are drawn at random from deck, in order, into revealed as cards A, B and C, and removed from deck."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Day {day}, round {round}: the active seat is {active_seat}. The revealed cards are A, B, C = {revealed}."},
    {"action": "ask", "who": "the active seat", "answer": "a choice: 1, 2 or 3", "effect": "lot_size is set to the choice. lot = the first lot_size cards of revealed, and lot_value is set to the sum of their values. The remaining revealed cards are appended to discard, and revealed is emptied."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "The lot is {lot} ({lot_size} cards, total value {lot_value})."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to your own florins (0 is a pass)", "effect": "Each player's bid is set to their answer. Bids stay hidden from the other players."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player: if ship_count + lot_size > 5, then bid is set to 0."},
    {"action": "update", "who": "table", "answer": null, "effect": "If every bid is 0, the lot is appended to discard and winner_seat stays 0. Otherwise, winner_seat is the seat with the highest bid. Ties are broken by priority = N - ((seat - active_seat + N) mod N), which makes the active seat highest, then the seats after it in order. price_paid is set to the winner's bid."},
    {"action": "update", "who": "the winner", "answer": null, "effect": "If winner_seat > 0, the winner loses price_paid florins. The lot is appended to their ship_cards, ship_value rises by lot_value, ship_count rises by lot_size, and total_cards rises by lot_size. grain_count, cloth_count, spice_count and dye_count each rise by the number of lot cards of that good. lot is then emptied."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Winner: seat {winner_seat} paid {price_paid} florins (seat 0 means the lot was discarded). The ship card counts of every seat are {ship_count}. Florins are not announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If round mod (2N) == 0 (end of a day), day scoring is applied. Let top = max ship_value. If top > 0 and exactly one player has top, that player gains 15. If k>1 players have top, each gains floor(22/k) and no second place is paid. If exactly one player has top, let second = the highest ship_value below top. If second > 0, the m players with second each gain floor(7/m). Then every ship_cards, ship_value and ship_count is reset to empty or 0, discard is emptied, and day rises by 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If round == 6N (after day 3 scoring), majorities are paid. For each of grain_count, cloth_count, spice_count and dye_count: let M = the max over players. If M > 0, the j players with M each gain floor(10/j). Then each player gains 3 × their count of their own favoured_good."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "If round == 6N, every player's favoured_good is revealed to everyone."},
    {"action": "update", "who": "table", "answer": null, "effect": "round rises by 1."},
    {"action": "check", "who": "table", "answer": null, "effect": "If round > 6N, the game ends. Otherwise the next round begins."}
  ],
  "ending": {
    "condition": "round > 6 * N",
    "rank_by": "you.florins * 1000 + you.total_cards",
    "decided_by": "The player with the most florins after end-of-game scoring wins. A tie on florins goes to the tied player with more total cards collected over the game. Players still tied share the win, which is the draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player has 40 florins, visible only to that player."},
    {"id": "R2", "text": "When the game starts, then each player holds a different favoured good drawn at random from Grain, Cloth, Spice and Dye, known only to that player."},
    {"id": "R3", "text": "When a day starts (round mod 2N == 1), then the deck is rebuilt as 48 cards: 12 per good, with values 0,1,1,2,2,3,3,3,4,4,5,5."},
    {"id": "R4", "text": "When it is round r, then the active seat is ((r-1) mod N)+1."},
    {"id": "R5", "text": "When the game has N players, then each day has 2N rounds and the game has 6N rounds: 18 with 3 players, 24 with 4."},
    {"id": "R6", "text": "When a round starts, then 3 cards are drawn from the deck and revealed in order as A, B and C."},
    {"id": "R7", "text": "When the active player chooses lot size 1, 2 or 3, then the lot is A, A+B or A+B+C, and the unchosen revealed cards are discarded."},
    {"id": "R8", "text": "When bidding happens, then all players, including the active player, bid at the same time a whole number from 0 to their own current florins, and 0 is a pass."},
    {"id": "R9", "text": "When a player's ship_count + lot_size > 5, then that player's bid is treated as 0."},
    {"id": "R10", "text": "When one valid bid above 0 is strictly highest, then that bidder wins the lot."},
    {"id": "R11", "text": "When the highest valid bids tie and the active player is among them, then the active player wins."},
    {"id": "R12", "text": "When the highest valid bids tie without the active player, then the tied player who comes first in seat order after the active seat wins."},
    {"id": "R13", "text": "When every bid is 0, then the lot is discarded and nobody pays."},
    {"id": "R14", "text": "When a player wins a lot with bid b, then their florins fall by b, ship_value rises by the sum of the lot's card values, ship_count and total_cards rise by the lot size, and each good count rises by that good's cards in the lot."},
    {"id": "R15", "text": "When a round ends, then the winner, the price paid and every player's ship_count are announced, and florins are not announced."},
    {"id": "R16", "text": "When a day ends and one player alone has the highest ship value (above 0), then that player gains 15 florins."},
    {"id": "R17", "text": "When a day ends and k>1 players tie for the highest ship value (above 0), then each gains floor(22/k) florins and no second place is paid."},
    {"id": "R18", "text": "When a day ends with a single leader, then the m players with the second-highest ship value (above 0) each gain floor(7/m) florins."},
    {"id": "R19", "text": "When a player's ship value is 0 at day end, then that player earns nothing from day scoring."},
    {"id": "R20", "text": "When day scoring is done, then all ships are emptied (value 0, count 0), and the game-long good counts are kept."},
    {"id": "R21", "text": "When the game ends, then for each good the j players with the most cards of it (more than 0) each gain floor(10/j) florins, and a good nobody collected pays nothing."},
    {"id": "R22", "text": "When the game ends, then each player gains 3 florins per card of their favoured good collected, and favoured goods are revealed."},
    {"id": "R23", "text": "When round 6N has been completed, then the game ends."},
    {"id": "R24", "text": "When the game ends, then the player with the most florins wins, a tie goes to more total_cards, and players still tied share the win."}
  ],
  "offers": [
    {"question": "Lot size", "who": "the active seat only", "options": "1, 2 or 3"},
    {"question": "Sealed bid", "who": "every seat, including the active seat", "options": "any whole number from 0 to that seat's current florins. A seat whose ship cannot hold the lot is still asked, but its bid counts as 0."}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 4", "why": "The designer chose 4. 3 is the least where a sealed auction has real rivals and both day prizes are contested. More than 4 would leave only 4 favoured goods to deal and make each majority too thin."},
    {"what": "No talk phase", "why": "The source says there is no talk. Bidding is sealed and simultaneous, so it is a poll."},
    {"what": "Tie-break order computed as priority = N - ((seat - active_seat + N) mod N)", "why": "This turns the rule 'active player first, then seats after the active player' into arithmetic."},
    {"what": "Cards encoded as text like 'Spice-3'", "why": "The good and the value are needed for counts and ship value."},
    {"what": "ship_value is public", "why": "Lots and winners are announced, so ship contents are public knowledge. Only florins, bids and favoured goods are secret."},
    {"what": "Second place is computed only among ship values above 0 and strictly below the top", "why": "The source says a value of 0 earns nothing and a tied first place cancels second place."},
    {"what": "Rank expression florins*1000 + total_cards", "why": "total_cards cannot reach 1000, so florins decide first and cards break ties. Remaining ties share the win as a draw."}
  ],
  "simplifications": [
    {"what": "The deck rebuild and ship emptying at a day boundary are done by a conditional update at the start of a day, alongside the end-of-day reset", "why": "The step list is flat, so day transitions use if-conditions on round."},
    {"what": "Favoured goods are revealed by a public tell at the end of the game", "why": "The attribute stays private to its owner. The reveal is an announcement."}
  ],
  "unsupported": []
}
```
````
