# Offered-Trump Duel Durak

Two-player Durak over 4 deals of up to 10 bouts each. The first attacker offers two suits and the defender picks one as trump. The player left holding cards takes penalty points, and the lower total penalty wins.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 36
- `suits` = 4
- `ranks_per_suit` = 9
- `lowest_rank` = 6
- `highest_rank` = 14
- `hand_size_dealt` = 8
- `cards_set_aside` = 20
- `deals` = 4
- `max_bouts_per_deal` = 10
- `max_rounds_total` = 40
- `min_attack_cards` = 1
- `max_attack_cards` = 3
- `suits_offered` = 2
- `suit_code_clubs` = 1
- `suit_code_diamonds` = 2
- `suit_code_hearts` = 3
- `suit_code_spades` = 4

## Round

1. **update** (all players): Start of a deal (S1). Set deck to all 36 card codes, empty both hands and clear discard, offer and trump. Draw 8 cards at random from deck into each seat's hand, removing each from deck. The 20 cards left in deck are set aside, unused. Set hand_count = 8 for each seat. Set attacker_seat = 1 if deal_number is 1 or 3, and 2 if deal_number is 2 or 4.
2. **sync** (all players): Each seat privately sees its own hand.
3. **ask** (the seat in attacker_seat (first attacker)): Set offer to the two named suits (S2). If the answer is not two different suits, set offer = [Hearts, Spades]. Announce the offer to both seats.
4. **ask** (the seat not in attacker_seat (first defender)): Set trump to the chosen suit (S3). If the answer is not in offer, set trump to the first suit in offer. Announce trump.
5. **ask** (the seat in attacker_seat): Set attack_cards to the named cards and remove them from the attacker's hand. If any card is not in hand, the ranks differ, or there are more cards than 3 or than the defender's hand_count, use instead the single card with the minimum code in the attacker's hand. Announce attack_cards. (judged: "Every card the attacker named is in the attacker's hand, all named cards share one rank, and there are between 1 and 3 of them, no more than the defender's hand_count.")
6. **ask** (the seat not in attacker_seat (defender)): If judged true, set defence_ok = true, set defence_cards to the named defence cards and remove them from the defender's hand. Otherwise set defence_ok = false and defence_cards = [] (counts as TAKE). (judged: "The defender named exactly one different card from the defender's own hand for each card in attack_cards, and each named card beats its paired attack card: it is the same suit and of higher rank, or it is of the trump suit while the attack card is not.")
7. **update** (all players): RESOLVE. If defence_ok: append attack_cards and defence_cards to discard, and switch attacker_seat to the other seat. If not defence_ok: append attack_cards to the defender's hand, and attacker_seat stays the same. Recompute hand_count for both seats. Clear attack_cards and defence_cards. Add 1 to bout_counter and 1 to round_number. Announce the cards played, the result, and both hand_count values.
8. **update** (all players): END OF DEAL. If exactly one seat has hand_count 0, the other seat adds its hand_count to penalty. If both have 0, nobody scores. If both hold cards, the seat with the larger hand_count adds (larger hand_count - smaller hand_count) to penalty; equal hands score nothing. Then add 1 to deal_number and set bout_counter = 0. Announce both penalty totals.
9. **check** (all players): End the game if deal_number > 4 or round_number >= 40; otherwise continue.

## Ending

- ends when: deal_number > 4 or round_number >= 40
- ranked by: `0 - you.penalty` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total penalty, and the lower total wins. If the two totals are equal, both share the top spot, which is the draw.

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed the game as a duel: the offer-and-choose trump mechanic and the attacker/defender alternation are defined only between two seats.
- No talk step before choices: The rules have no talk, and in a zero-sum duel talk would only add words.
- Cards encoded as rank*10 + suit code (Clubs 1, Diamonds 2, Hearts 3, Spades 4): The minimum code in a hand is then exactly the lowest-ranked card with ties broken by suit order, so the illegal-attack fallback is pure arithmetic.
- The offer is asked as a choice among the six suit pairs: Every reply is then two different suits; the Hearts and Spades fallback is kept in the effect for completeness.
- The 20 set-aside cards stay in the hidden deck list: They are unused for the deal; keeping them in the deck is equivalent to setting them aside face down.
- Strategy at the table: The first attacker offers two suits they hold strength in, or that the opponent likely lacks. The chooser picks the one that helps their own hand. Attackers lead ranks the defender probably cannot beat, and defenders weigh taking against spending their trumps.

## Simplifications

- Attack legality and defence legality are judged by a referee from one sentence each: Parsing free-text card lists and matching each defence card to an attack card is too complex for plain arithmetic. The effects of each ruling (moving cards, scoring) are still calculated.
- Deal-start steps run inside the round, each carrying the condition bout_counter == 0: The engine repeats one flat round. Per-step conditions reproduce 'only in the first bout of a deal' without choosing between blocks of steps.
- A draw is shown as both players sharing the win: The engine ranks by one expression, and players level at the top share the win; this is equivalent to the source's draw.
- The 40-round cap and the 4-deal end are both checked: With at most 10 bouts per deal over 4 deals, round 40 can only fall at the end of deal 4, so the cap is kept as a safeguard.

## Unsupported (needs engine work)

- none
