# Scopa Duel

Two-player Scopa over 2 hands of 18 rounds. Players capture table cards by matching rank or summing to it, score Scopas for sweeping the table, then score cards, Coins, the Seven of Coins and sevens.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 40
- `suits` = 4
- `ranks_per_suit` = 10
- `ace_rank` = 1
- `jack_rank` = 8
- `knight_rank` = 9
- `king_rank` = 10
- `hands` = 2
- `rounds_per_hand` = 18
- `total_rounds` = 36
- `table_deal` = 4
- `cards_per_deal` = 3
- `deals_per_hand` = 6
- `shuffle_round_hand1` = 1
- `shuffle_round_hand2` = 19
- `redeal_interval` = 3
- `first_redeal_round_hand1` = 4
- `last_redeal_round_hand1` = 16
- `first_redeal_round_hand2` = 22
- `last_redeal_round_hand2` = 34
- `final_play_round_hand1` = 18
- `final_play_round_hand2` = 36
- `scopa_points` = 1
- `most_cards_points` = 1
- `cards_tie_count` = 20
- `most_coins_points` = 1
- `coins_tie_count` = 5
- `seven_of_coins_points` = 1
- `most_sevens_points` = 1
- `primary_rank` = 7
- `secondary_rank` = 6
- `no_capturer` = 0
- `score_weight` = 10000
- `cards_weight` = 100
- `coins_weight` = 1

## Round

1. **update** (all players): When round is 1 or 19: deck = full_deck; table_cards, every hand, every captures and every declared are emptied; scopa_points = 0 for each player; last_capturer = 0. Then 4 cards are drawn at random from deck into table_cards, and 3 cards are drawn at random from deck into each player's hand (each draw is removed from deck and appended to its destination).
2. **update** (all players): When round is in {4,7,10,13,16,22,25,28,31,34}: 3 cards are drawn at random from deck into each player's hand.
3. **sync** (all players): Each player sees their own hand plus the public table_cards, captures, scopa_points, score, total_cards, total_coins and round.
4. **ask** (the Leader: seat 1 when round <= 18, seat 2 when round >= 19): Leader.played_card = the chosen card; it is removed from Leader.hand.
5. **ask** (the Leader): Leader.declared = the listed table cards (empty if 'none').
6. **update** (the Leader): If legal and declared is non-empty: the played_card and the declared cards are appended to Leader.captures, the declared cards are removed from table_cards, and last_capturer = Leader's seat; then, if table_cards is empty, Leader.scopa_points += 1. Otherwise (declared is empty, or the declaration is illegal): played_card is appended to table_cards and nothing is captured. The table is told what was played and captured. (judged: "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank.")
7. **ask** (the Dealer: seat 2 when round <= 18, seat 1 when round >= 19): Dealer.played_card = the chosen card; it is removed from Dealer.hand.
8. **ask** (the Dealer): Dealer.declared = the listed table cards (empty if 'none').
9. **update** (the Dealer): If legal and declared is non-empty: the played_card and the declared cards are appended to Dealer.captures, the declared cards are removed from table_cards, and last_capturer = Dealer's seat; then, if table_cards is empty and round is not 18 or 36, Dealer.scopa_points += 1. Otherwise: played_card is appended to table_cards and nothing is captured. The table is told what was played and captured. (judged: "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank.")
10. **update** (all players): When round is 18 or 36: if last_capturer > 0, all table_cards are appended to that seat's captures; otherwise they are discarded. table_cards is emptied. Hand scoring, using this hand's captures: +1 score to the player with strictly more cards; +1 to the player with strictly more cards whose suit is Co; +1 to the holder of '7Co'; +1 to the player with more rank-7 cards, or, if those are tied, more rank-6 cards, and no point if both are tied; each player's score += scopa_points. Each player's total_cards += count(captures) and total_coins += count of Co cards in captures. The hand's results are announced.
11. **update** (all players): round += 1.
12. **check** (all players): End the game if round > 36; otherwise continue to the next round.

## Ending

- ends when: round > 36
- ranked by: `you.score * 10000 + you.total_cards * 100 + you.total_coins` (the highest wins; players level at the top share the win)
- decided by: Most total points across both hands wins. A tie goes to more total captured cards, then to more total captured Coins. If still tied, both players share the result (a draw).

## Choices the source did not make

- Exactly 2 players (suggested 2): The designer's rules are a duel: fixed Leader/Dealer roles and a 40-card count that assumes exactly two hands of play.
- No pre-play talk step: This is a zero-sum duel with no coordination; talk would only add words.
- Card codes such as '7Co', '10Sw': A compact text form of rank and suit, so suit and rank counts are simple arithmetic.
- Play is split into a card choice and a text declaration: Choosing from the hand list guarantees a real card; the capture set has too many possible subsets to list as options.
- Seat 1 is Player A, seat 2 is Player B: The source names players A and B but not seats.
- Leftover cards with no last capturer are not counted for either player: The source says they are discarded.
- Round lists are given as single-number parameters (first round, last round and an interval of 3 for redeals): Each parameter must be one number. The redeal rounds are first_redeal_round plus multiples of redeal_interval, up to last_redeal_round.

## Simplifications

- Capture legality is decided by a judged referee sentence: Checking for a same-rank card and an exact subset sum over parsed text is too complex for a single arithmetic check. The effects of the ruling are still arithmetic.
- The three-step tie-break is folded into one rank expression: score*10000 + total_cards*100 + total_coins: rank_by must be a single expression. total_cards and total_coins never reach 100, so the order of the tie-breaks is preserved.
- A complete tie is a shared win: The engine treats players level at the top as sharing the win, which is equivalent to a draw.

## Unsupported (needs engine work)

- none
