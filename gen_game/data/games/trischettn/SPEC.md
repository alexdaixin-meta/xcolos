# Trischettn Duel

A two-player, no-trump trick-taking duel over 2 deals of 16 tricks with a talon draw, where pips from won cards and the last trick decide the winner.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 32
- `suits` = 4
- `ranks_per_suit` = 8
- `hand_size` = 8
- `talon_size` = 16
- `tricks_per_deal` = 16
- `deals` = 2
- `total_rounds` = 32
- `drawing_tricks_per_deal` = 8
- `strength_ten` = 8
- `strength_nine` = 7
- `strength_ace` = 6
- `strength_king` = 5
- `strength_ober` = 4
- `strength_unter` = 3
- `strength_eight` = 2
- `strength_seven` = 1
- `pips_ace` = 3
- `pips_ten` = 1
- `pips_nine` = 1
- `pips_king` = 1
- `pips_ober` = 1
- `pips_unter` = 1
- `pips_eight` = 0
- `pips_seven` = 0
- `last_trick_bonus` = 3
- `pips_per_deal` = 35
- `pips_per_match` = 70
- `deal_1_first_leader_seat` = 1
- `deal_2_first_leader_seat` = 2

## Round

1. **update** (table): When trick_number = 1: rebuild deck with all 32 cards, empty every hand, then draw 8 cards at random from deck into each player's hand. Move the remaining 16 cards into talon in random order, then remove the first talon card and set it as talon_up. Set talon_count = 16, set each deal_pips = 0, and set leader_seat = 1 if deal_number = 1, else 2. Announce the deal number, talon_up and the leader.
2. **sync** (all players): Each player sees their own hand plus all public attributes: deal_number, trick_number, leader_seat, led_card, follow_card, talon_up, talon_count, every deal_pips and every match_total.
3. **ask** (the seat equal to leader_seat): Remove the chosen card from the leader's hand and set led_card to it. Announce led_card.
4. **ask** (the seat not equal to leader_seat): Remove the chosen card from the follower's hand and set follow_card to it. Announce follow_card.
5. **update** (table): If follow_card has the same suit as led_card and its strength is higher (Ten 8, Nine 7, Ace 6, King 5, Ober 4, Unter 3, Eight 2, Seven 1), set trick_winner_seat to the follower's seat; otherwise set it to leader_seat. Add the pips of led_card and follow_card (Ace 3; Ten, Nine, King, Ober, Unter 1; Eight, Seven 0) to the winner's deal_pips, plus 3 if trick_number = 16. Announce the winner and both deal_pips.
6. **update** (table): When talon_count > 0: append talon_up to the winner's hand and announce which card it was. Remove the first card of talon and append it to the loser's hand, without announcing it. Set talon_count = talon_count - 2. If talon_count > 0, remove the first card of talon and set talon_up to it; otherwise set talon_up = 'none'. Announce talon_up and talon_count.
7. **update** (table): Set leader_seat = trick_winner_seat, led_card = 'none' and follow_card = 'none'. If trick_number = 16, add each player's deal_pips to their match_total, announce both match_total values, set deal_number = deal_number + 1 and trick_number = 1. Otherwise set trick_number = trick_number + 1.
8. **check** (table): End the game if deal_number > 2; otherwise continue with the next round.

## Ending

- ends when: deal_number > 2
- ranked by: `you.match_total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their match total, the pips summed over both deals (70 available). The higher total wins. Equal totals (35 each) share the win, which is a draw.

## Choices the source did not make

- 2 players (min 2, max 2, suggested 2): The designer set 2. The game is a duel: one leader and one follower per trick, with a talon split between winner and loser. A third player would break the follow-and-draw structure.
- Card names written as text like 'Ace of Bells', with strength and pips taken from the parameter table: The engine has no card type. Strength and pip values are listed as parameters so the trick and scoring arithmetic is explicit.
- talon_count counts the talon-up card: The rules ask for 'the number of cards left in the talon' to be public. Counting the face-up card makes it 16 at the start and 0 after 8 tricks.
- No talk step: The rules have no table talk. In a two-player zero-sum duel, talk would add words without a real decision about whether to trust a proposal.
- Strategy at the table: A thoughtful player tracks played cards and openly drawn talon cards, decides when to win a trick for talon_up versus duck to save strong cards, keeps Aces (3 pips) safe, and plans the endgame for the 3-pip last trick.

## Simplifications

- The deal is run as conditional updates inside the round steps (when trick_number = 1) instead of as separate deal phases: The step list is flat. A single step with an arithmetic 'when' condition reproduces the start of deal 1 and deal 2.
- The talon-up card taken by the winner goes into their ally-visible hand, and is only announced publicly at the moment it is taken: The engine has no per-card visibility inside a list. The card was already public as talon_up, so players keep the same knowledge the rules give them.

## Unsupported (needs engine work)

- none
