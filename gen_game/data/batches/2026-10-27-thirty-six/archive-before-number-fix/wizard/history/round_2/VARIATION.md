# Variation: Three-Card Wizard

A compact Wizard for 3 players: 12 hands of 3 cards from a 28-card deck, simultaneous exact bids, and one trick per round.

Players: 3 to 3, best with 3

## Review of the original

Wizard is a trick-taking game for 3-6 players with a 60-card deck (four suits of 1-13, plus 4 Wizards and 4 Jesters). Hands grow from 1 card to 60/players cards, a turned card sets trump, and each player bids the exact number of tricks they will take. An exact bid scores 20 plus 10 per trick, and a missed bid loses 10 per trick off.

- **non_degenerate**: good. Every fixed bid loses. Always bidding 0 fails whenever the hand is strong, and always bidding high fails on weak hands. Missing by k costs 10k, so no fixed policy can match a player who reads their hand. One seat edge exists: bidding in turn order gives the last bidder information. A second, much smaller one comes from leading.
- **skill_sensitive**: weak. Skill shows in hand evaluation, card counting and dumping or ducking tricks. Single hands are very card-driven, though, and the many tiny early hands are close to lotteries. Skill wins out only over many hands.
- **headroom**: good. A weak player can still score exact bids of 0 or 1. A strong player keeps improving by inferring others' hands from their bids and play, steering tricks to the right player, and playing to make others miss.
- **reasoning_dependent**: good. Hands are hidden. Bids reveal partial information. Each trick requires inferring what the remaining players hold and planning across the rest of the hand.
- **verifiable**: good. Trick winners and scores follow mechanically from the cards played and the bids.
- **fits_platform**: bad. The original runs up to 20 hands of up to 20 cards, which means hundreds of sequential choices. It also needs a 60-card deck, a dealer trump choice, a variable hand size and a sequential bidding order. This exceeds the step and round limits.

## Problems

- P1: Length and size. Variable hands up to 20 cards and up to 60 hands far exceed 40 rounds and 4 choices per round.
- P2: Sequential bidding gives the last bidder a built-in information edge, and the dealer's trump choice on a Wizard adds an extra sub-procedure.
- P3: The previous build did not offer the bid options 0-3 to seats. It derived them from parameter attributes (bid_min..bid_max) that did not produce a valid option list. Every bid then fell to the default 1, which overwrote valid answers including 0. This broke the deal/bid scenario (R1), the recorded-bids scenario (R3) and the new-hand scenario (R4).
- P4: The illegal-choice fallback (lowest led-suit card, else Jester, else lowest suited card with colour tie-breaks, and so on) was a long priority chain. It was built incorrectly (R9) and is error-prone to build.
- P5: Tiny one-card hands are nearly pure luck, so card luck swamps skill in early hands.

## Changes

- Three players, a 28-card deck (Red, Blue, Green 1-8, plus 2 Wizards and 2 Jesters), 12 hands of exactly 3 cards. Each round is one trick, so there are 36 rounds. (fixes: P1): This keeps trick-taking, trump and exact bidding within 40 rounds and at most 4 choices per round. Every hand is large enough to plan over.
- Every hand has 3 cards instead of 1 to 20. (fixes: P5): Removes the near-random one-card hands. Every hand now offers a real bid decision and in-hand planning.
- Bids are a single simultaneous poll. The literal fixed options 0, 1, 2 and 3 are written directly into the step, not computed from attributes. The answer is stored exactly as given. The default of 1 applies only if the answer is missing or not one of 0-3. The bid is not touched again until end-of-hand scoring. (fixes: P3): Simultaneous bidding removes the last-bidder edge. Hard-coding the option list fixes the build failure where no options were offered and every bid became 1.
- A turned Wizard or Jester simply means no trump. (fixes: P2): Removes the dealer-choice sub-procedure and the dealer's advantage.
- The first leader of hand h is seat ((h - 1) mod 3) + 1. After that, the trick winner leads. (fixes: P2): Balances the leading advantage over 12 hands (4 each).
- The illegal-choice fallback is one rule: play the first card of the player's legal-card list, which keeps the order the cards sit in their hand. (fixes: P4): This is a one-operation fallback that is deterministic and easy to build and test, replacing the broken priority chain.
- Trick resolution uses one numeric strength per card, and the best card is replaced only by a strictly greater strength. A Wizard is 100, a trump is 20 + rank, a led-suit card is its rank, and anything else is 0. (fixes: P1): Implements 'first Wizard wins, else highest trump, else highest led suit, all Jesters means the first Jester wins' as plain arithmetic, with no lookup table.

## Kept from the original

- Wizards always win, with the first one played taking the trick. Jesters always lose, and the first one wins only if every card is a Jester.
- A turned card sets trump each hand.
- Players must follow the led suit if able, but Wizards and Jesters may always be played.
- When a Jester is led, the next suited card sets the led suit. When a Wizard is led, there is no led suit.
- Exact-bid scoring: 20 + 10 per trick when exact, otherwise -10 per trick off.
- Bids need not sum to the number of tricks.
- The highest total after the last hand wins.

## The variation's rules

CARDS. The deck has 28 cards:
- Red R1-R8, Blue B1-B8 and Green G1-G8 (the suit is the letter, the rank is the number);
- two Wizards, W1 and W2;
- two Jesters, J1 and J2.

SEATS. Players sit in seats 1, 2 and 3. Everyone starts with a score of 0.

STRUCTURE. The game has 12 hands of 3 tricks each. Each round is one trick, so there are 36 rounds.
- The table tracks hand_number (starting at 0) and trick_in_hand (starting at 1).
- Each player has: hand (a list, private to them), bid, tricks_taken, played_card, offer (a list) and score.

RULE 1 (new hand: deal). Only when trick_in_hand = 1:
- add 1 to hand_number;
- shuffle all 28 cards into the deck (this is the round's only random event);
- empty every hand and set every tricks_taken to 0;
- deal the top 3 cards of the deck to seat 1, the next 3 to seat 2 and the next 3 to seat 3, each seen only by its owner;
- remove the 10th card from the deck and place it face up as trump_card, announced to all. After this, 18 cards remain in the deck.

RULE 2 (trump). If trump_card is suited, trump_suit is its suit letter. If it is a Wizard or a Jester, trump_suit is 'none' for the whole hand.

RULE 3 (first leader). Only when trick_in_hand = 1, leader = ((hand_number - 1) mod 3) + 1:
- seat 1 leads in hands 1, 4, 7 and 10;
- seat 2 leads in hands 2, 5, 8 and 11;
- seat 3 leads in hands 3, 6, 9 and 12.

RULE 4 (bidding). Only when trick_in_hand = 1, all three players answer one simultaneous poll.
- The options are exactly the fixed list 0, 1, 2, 3, offered to every seat.
- Each player's answer is stored in their bid exactly as given, and a 0 stays 0.
- Only if an answer is missing or not one of 0, 1, 2, 3 does that bid become 1.
- All bids are then announced. They need not sum to 3.
- Bids are not changed again until Rule 10.

RULE 5 (trick setup). Every round, set:
- led_suit = 'none';
- wizard_played = false;
- best_value = -1;
- best_seat = 0;
- played_cards empty.

RULE 6 (play order). Three players play one card each, one after another:
- first the seat in leader;
- then the seat (leader mod 3) + 1;
- then the seat ((leader + 1) mod 3) + 1.
Each player sees the cards already played to the trick.

RULE 7 (legal cards). Before a player chooses, build their offer list, keeping the order the cards sit in their hand:
- if led_suit is not 'none' and they hold at least one card of led_suit, the offer is their cards of led_suit plus any Wizards and Jesters they hold;
- otherwise, the offer is every card in their hand.
The player picks one card from the offer.

RULE 8 (fallback). If the answer is missing or not in the offer, the engine plays the first card of the offer list.

RULE 9 (resolving each played card). As each card is played, remove it from the hand, record it as played_card and append it to played_cards. Then work out the led suit and the card's strength.

Led suit:
- If the card is suited, led_suit is 'none' and wizard_played is false, then led_suit becomes that card's suit.
- If the card is a Wizard, set wizard_played = true.
- A Wizard or Jester never sets led_suit. Once any Wizard is played, later cards do not set led_suit.

Strength:
- Wizard: 100.
- Suited card whose suit equals trump_suit: 20 + rank.
- Other suited card whose suit equals led_suit: its rank.
- Anything else: 0. This includes Jesters and off-suit non-trump cards.

If strength > best_value (strictly), set best_value = strength and best_seat = this seat. As a result:
- the first Wizard wins the trick;
- otherwise the highest trump wins;
- otherwise the highest card of the led suit wins;
- if all three cards are Jesters, the first Jester wins.

RULE 10 (end of trick). Add 1 to tricks_taken of best_seat, announce the winner, and set leader = best_seat.
- If trick_in_hand = 3, score the hand. A player whose tricks_taken equals their bid gains 20 + 10 × tricks_taken. Otherwise they lose 10 × |tricks_taken - bid|. Announce all scores, then set every bid to 0 and trick_in_hand = 1.
- Otherwise add 1 to trick_in_hand.

RULE 11 (end). The game ends after round 36, which is the end of hand 12.

Objective: After hand 12, the player with the highest score wins. If two or three players tie for the highest score, the game is a draw.

Expected effect: Simultaneous bids remove the last-bidder edge, and rotating the first lead balances the seats. Three-card hands make every bid a real estimate: count Wizards and trumps, and judge how the off-suit cards will play. Mid-hand play rewards inference from the announced bids and the cards seen, such as ducking a trick to stay exact or forcing a trick onto an opponent who bid 0. Simple policies lose: always bidding 0 is beaten by reading the hand, and always bidding 3 misses most hands at -10 to -30. Over 12 hands, skill outweighs the deal. Talk is left out: with only 3 players and public bids, messages would add little beyond the bids and could enable two-player collusion against the third.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
