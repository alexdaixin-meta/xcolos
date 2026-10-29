# Blind Officers' Schafkopf

Two-player Schafkopf variant: sealed contract bids, an optional double, 8 tricks per hand from a 24-card deck with an unseen Blind, over 4 hands (32 rounds), scored in match points.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 24
- `suits` = 4
- `cards_per_suit` = 6
- `deck_card_points` = 120
- `points_ace` = 11
- `points_ten` = 10
- `points_king` = 4
- `points_ober` = 3
- `points_unter` = 2
- `points_nine` = 0
- `hands` = 4
- `tricks_per_hand` = 8
- `total_rounds` = 32
- `cards_dealt_per_player` = 8
- `blind_size` = 8
- `bid_options` = 11
- `wenz_trumps` = 4
- `suit_solo_trumps` = 12
- `simple_margin` = 10
- `strong_multiplier` = 2
- `strong_minimum_points` = 30
- `simple_stake` = 2
- `strong_stake` = 4
- `double_factor` = 2
- `ramsch_award` = 1
- `starting_match_points` = 0
- `level_pass` = 0
- `level_simple` = 1
- `level_strong` = 2
- `trump_strength_base` = 100
- `plain_rank_ace` = 6
- `plain_rank_ten` = 5
- `plain_rank_king` = 4
- `plain_rank_ober` = 3
- `plain_rank_nine` = 1

## Round

1. **update** (all players): When trick_number == 1: set game.deck to all 24 cards. Draw 8 cards at random from deck into each player's hand. Move the remaining 8 cards to game.blind, leaving deck empty. Set every card_points to 0, doubled to false, contract and level to empty, and declarer_seat and defender_seat to 0. Set priority_seat to 1 if hand_number is odd, else 2.
2. **sync** (all players): When trick_number == 1: each player is sent their own hand.
3. **poll** (all players): When trick_number == 1: store each answer in that player's bid. Set bid_level to 0 for Pass, 1 for any -Simple bid, 2 for any -Strong bid. No one sees a bid until both are in.
4. **update** (all players): When trick_number == 1, resolve the bids. If both bid_level == 0: contract = Ramsch, declarer_seat = 0, defender_seat = 0, leader_seat = priority_seat, trump_list = [Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter]. Otherwise the declarer is the seat with the higher bid_level; if the levels are equal, the declarer is priority_seat. Set declarer_seat to that seat and defender_seat to the other. Take contract (the word before the dash) and level (Simple or Strong) from the declarer's bid. Set leader_seat = declarer_seat. If contract == Wenz, trump_list = [Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter]. If contract is a suit X, trump_list = [Acorns Ober, Leaves Ober, Hearts Ober, Bells Ober, Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter, X Ace, X Ten, X King, X Nine].
5. **tell** (all players): When trick_number == 1: announce both bids, the contract and level (or Ramsch), and the declarer.
6. **ask** (the seat in game.defender_seat): When trick_number == 1 and contract != Ramsch: set doubled = true if the answer is Double, else false.
7. **tell** (all players): When trick_number == 1 and contract != Ramsch: announce whether the defender doubled.
8. **ask** (the seat in game.leader_seat): Set led_card to the chosen card and remove it from the leader's hand.
9. **ask** (the seat that is not game.leader_seat): Set follow_card to the chosen card and remove it from the follower's hand.
10. **update** (all players): Compute each card's strength. A card in trump_list scores 100 + (length of trump_list - its position, where the first position is 0). A card not in trump_list whose suit matches led_card's suit (led_card itself not being a trump) scores its plain rank: Ace 6, Ten 5, King 4, Ober 3, Nine 1. Any other card scores 0. trick_winner = leader_seat if strength(led_card) > strength(follow_card), else the other seat. Add the card points of both cards (Ace 11, Ten 10, King 4, Ober 3, Unter 2, Nine 0) to the trick winner's card_points. Set leader_seat = trick_winner.
11. **tell** (all players): Announce led_card, follow_card, the trick_winner, and both players' card_points.
12. **update** (all players): When trick_number == 8, score the hand. Let D = the declarer's card_points and F = the defender's card_points. Stake = 2 if level is Simple, 4 if level is Strong; doubled if doubled == true. Simple is made if D >= F + 10. Strong is made if D >= 2*F and D >= 30. If made, the declarer's match_points += stake; otherwise the defender's match_points += stake. If contract == Ramsch, the player with fewer card_points gets match_points += 1, and nobody scores if the totals are equal. Then set both card_points to 0, hand_number += 1, trick_number = 1. Otherwise (trick_number < 8): trick_number += 1.
13. **tell** (all players): When a hand has just been scored (trick_number == 1 and hand_number > 1): announce whether the contract was made (or the Ramsch result), the stake awarded, and both match_points.
14. **check** (all players): End the game if hand_number > 4; otherwise continue.

## Ending

- ends when: game.hand_number > 4
- ranked by: `you.match_points` (the highest wins; players level at the top share the win)
- decided by: After four hands (32 tricks), the player with more match points wins. Equal match points share the win, which is a draw.

## Choices the source did not make

- 2 players, as the designer set: The source is written for exactly 2 players (priority, declarer against defender). Its core is reading the opponent's sealed bid and hand strength, which works at 2. More seats would break the declarer/defender structure.
- No table talk step: The rules have none, and with 2 opposed players talk would only add words.
- Card naming as '<Suit> <Rank>': Lets the suit and rank be read from the card's name for the follow rule, strength and points.
- Trick winner decided by a numeric strength: Trump strength is 100 plus a position score from the ordered trump_list, plain led-suit cards score their rank, and others score 0. This is an arithmetic version of the stated ranking rules.
- Hand bookkeeping driven by trick_number and hand_number with per-step 'when' conditions: The start-of-hand and end-of-hand steps run only on the first and eighth trick of each hand, without needing alternative blocks.

## Simplifications

- Follow-suit legality is enforced by restricting the offered options rather than by a penalty: The engine offers a seat only what it may do, so illegal plays cannot occur.
- Card point values and plain ranks are applied by rank name instead of a lookup table: The engine has no lookup operation; a small conditional on the rank word is equivalent.

## Unsupported (needs engine work)

- none
