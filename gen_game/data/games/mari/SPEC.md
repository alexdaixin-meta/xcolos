# Mini Mariáš with Hidden Talon

Three players play 5 deals of a 24-card trick-taking game: each deal starts with a sealed bid for a point contract, then 7 tricks with strict follow, overtake and trump rules, and the stake scales with the contract, Hearts trump and flek.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 24
- `suits` = 4
- `cards_per_suit` = 6
- `hand_size` = 7
- `talon_size` = 3
- `ace_points` = 10
- `ten_points` = 10
- `other_card_points` = 0
- `last_trick_bonus` = 10
- `max_card_points` = 90
- `deals` = 5
- `rounds_per_deal` = 8
- `tricks_per_deal` = 7
- `total_rounds` = 40
- `bid_low` = 40
- `bid_mid` = 50
- `bid_high` = 60
- `stake_for_40` = 1
- `stake_for_50` = 2
- `stake_for_60` = 4
- `hearts_trump_multiplier` = 2
- `flek_multiplier` = 2
- `declarer_win_multiplier` = 2
- `defender_win_multiplier` = 1
- `starting_score` = 0

## Round

1. **update** (all players): round_number += 1; round_in_deal = ((round_number - 1) mod 8) + 1; deal_number = floor((round_number - 1) / 8) + 1; when round_in_deal == 1, eldest = ((deal_number - 1) mod 3) + 1.
2. **update** (all players): When round_in_deal == 1: deck = all 24 cards. Every hand is emptied; bid = 0, flek = '', is_declarer = false, played_card = ''. declarer = 0, contract = 0, trump = '', stake_v = 0, declarer_points = 0, defender_points = 0. Deal 7 cards to each hand, each a random draw removed from deck. The remaining 3 cards are moved from deck to talon.
3. **sync** (all players): When round_in_deal == 1, each player sees only their own hand, sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low.
4. **poll** (all players): When round_in_deal == 1: bid = 0 for PASS, otherwise the number. Nobody sees another bid.
5. **update** (all players): When round_in_deal == 1: deal_played = (max bid > 0). If deal_played: among the seats with the highest bid, the one with the lowest score; if still tied, the one first in seat order starting from eldest. That seat becomes declarer, contract = its bid, and its is_declarer = true.
6. **tell** (all players): When round_in_deal == 1 and not deal_played: 'All three passed; deal {deal_number} is not played.'
7. **ask** (the declarer): When round_in_deal == 1 and deal_played: trump = the answer.
8. **tell** (all players): When round_in_deal == 1 and deal_played: 'Declarer: Seat {declarer}, contract {contract}, trump {trump}. The other two seats are the defenders.'
9. **poll** (the two defenders): When round_in_deal == 1 and deal_played: flek = the answer, then both choices are announced.
10. **update** (all players): When round_in_deal == 1 and deal_played: stake_v = 1 if contract == 40, 2 if 50, 4 if 60; multiply by 2 if trump == Hearts; multiply by 2 again if at least one defender has flek == FLEK. Announce 'Flek: {flek choices}. V = {stake_v}.'
11. **update** (all players): When round_in_deal >= 2 and deal_played: trick = [], led_suit = '', played_card = '' for every seat, winning_seat = 0. leader = declarer if round_in_deal == 2, otherwise the previous trick's winner.
12. **ask** (the seat equal to leader): When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick; led_suit = its suit; winning_seat = leader. The card is shown to everyone.
13. **ask** (the next seat after leader in seat order): When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick. winning_seat is updated: a trump beats any non-trump, a higher trump beats a lower trump, and a higher card of led_suit beats the current winner when no trump is in the trick. The card is shown to everyone. (judged: "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card.")
14. **ask** (the third seat (the seat before leader in seat order)): When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick; winning_seat is updated as in the previous step. The card is shown to everyone. (judged: "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card.")
15. **update** (all players): When round_in_deal >= 2 and deal_played: pts = 10 x (number of Aces and Tens in trick), plus 10 if round_in_deal == 8. If winning_seat == declarer, declarer_points += pts, otherwise defender_points += pts. Announce 'Seat {winning_seat} wins the trick. Declarer {declarer_points}, defenders {defender_points}.'
16. **update** (all players): When round_in_deal == 8 and deal_played: if declarer_points >= contract, the declarer's score += 2 x stake_v and each defender's score -= stake_v; otherwise the declarer's score -= 2 x stake_v and each defender's score += stake_v. Announce the result and the match scores.
17. **check** (all players): End the game if round_number == 40; otherwise continue.

## Ending

- ends when: round_number == 40
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's match score after round 40. The highest score wins, and players tied at the top share the win (a draw among them).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3: one declarer against two pooled defenders is the whole structure of the game. The minimum cannot be lower and the maximum cannot be higher because the 24-card deal (3x7 + 3) and the 2V/V scoring only balance with three seats.
- No talk step: The source says there is no talk at any time. Strategy is in bid sizing against your own hand, the trump choice, when to flek, and card play that reads which cards the others are forced to play.
- Bids stay private to their owner: The source announces only the declarer, contract and trump, not the losing bids.
- Card encoding 'Suit Rank' with rank values A=6, 10=5, K=4, O=3, U=2, 9=1: This lets the trick winner and the card points be worked out by arithmetic.
- Card legality is enforced by offering only legal cards, with a judged sentence as a check: The follow, overtake and trump rules are long. The legal set is worked out from trick, led_suit and trump, and a referee confirms it.
- PASS is stored as bid 0: This makes the highest bid and the all-pass test simple arithmetic.

## Simplifications

- One engine round equals one source round; rounds 2-8 of an all-pass deal still run as engine rounds with every step skipped by its condition: This keeps the count at 40 rounds and matches the source's 'skipped with no plays and no scoring'.
- Each step carries a condition on round_in_deal and deal_played instead of separate bidding and trick blocks: The step list is flat; per-step conditions express the same flow.

## Unsupported (needs engine work)

- none
