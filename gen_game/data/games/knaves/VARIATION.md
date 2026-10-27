# Variation: Knaves Short Deck with Bids

Three players play 6 hands of 6 tricks with a 20-card deck and a turned trump. Each trick is worth +2, minus penalties for Jacks in it. Each hand opens with a simultaneous bid, and taking exactly your bid earns +5. The highest total after 36 tricks wins.

Players: 3 to 3, best with 3

## Review of the original

Knaves is a 3-player trick-taking game with a 52-card deck, a turned trump card and 17 cards per player. Each trick scores +1 and each Jack taken costs points (J♠ -1, J♣ -2, J♦ -3, J♥ -4); the first player to reach 20 points wins.

- **non_degenerate**: good. No simple policy is safe. Always playing your highest card wins tricks but collects Jacks: the J♥ alone wipes out four tricks. Always playing low hands the lead to opponents. With three players, one rival's gain is not automatically another's loss. Eldest leads first, but eldest rotates each hand.
- **skill_sensitive**: weak. Card play is skilful: following suit, trumping, dumping Jacks onto a trick an opponent will win, and counting cards. But with no bidding, a hand full of trumps and aces simply wins, and one lucky deal can be most of the way to 20. Luck of the deal outweighs skill over a short match.
- **headroom**: good. Counting 52 cards, inferring voids and timing Jack dumps has a high ceiling. A weak player still takes some tricks.
- **reasoning_dependent**: good. Hands are hidden. Players must infer who is void in a suit, who holds trumps, and where the Jacks are.
- **verifiable**: good. Tricks and Jack penalties are plain arithmetic.
- **fits_platform**: weak. It is turn-based text play, but 17 tricks per hand and an open-ended race to 20 is far too long. 52 cards in hidden hands is heavy to build. First-to-20 also needs a tie rule for several players crossing 20 in the same hand.

## Problems

- P1: Too long. 17 tricks per hand and an open-ended race to 20 exceeds the platform's round limit.
- P2: Luck dominates. With no bid, whoever is dealt the trumps and aces wins, and a poor hand has nothing to play for except avoiding Jacks.
- P3: The previous build never reset the deck at the start of a new hand. The second hand drew from an empty list and crashed (rule R6/R7).
- P4: The previous build appended played cards back into the deck, so the deck held 3 cards after the first trick instead of 0 (rules R7, R8, R9).
- P5: The previous build's bid poll did not offer the full range 0 to 6, including 0, to every seat. Tests found the 0 option never offered to some seats.
- P6: The previous build stored many fixed numbers (deck_size, suits, ranks_per_suit, hands and so on) as attributes. This wasted the attribute budget and invited mismatches.
- P7: The previous build dealt by drawing one random card at a time, which is many random draws per round. The limit is 1.

## Changes

- Use a 20-card deck (A K Q J 10 in four suits), 6 cards each, 6 hands of 6 tricks: 36 rounds, one trick per round. (fixes: P1): Fits the round limit while keeping trumps, follow-suit and all four Jacks.
- Add a simultaneous bid of 0 to 6 tricks at the start of each hand, with a +5 bonus for taking exactly the bid. Bids are revealed together. (fixes: P2): A weak hand can score by bidding low and ducking. Bids reveal information that opponents can reason about and try to spoil.
- At the first round of every hand, explicitly reset the deck to the full 20-card list, clear every hand and the discard pile, and reset the per-hand counters. This happens before shuffling. (fixes: P3): Every hand starts from a full deck, so the deal can never draw from an empty list.
- Played cards move from the hand to a separate discard list and are never returned to the deck. After the deal the deck is empty. (fixes: P4): Keeps the card count consistent: 18 dealt, 1 turned, 1 hidden, 0 in the deck.
- The bid poll is one simultaneous choice put to all three seats, each offered exactly the options 0, 1, 2, 3, 4, 5, 6. It runs only in the first round of each hand. (fixes: P5): Removes the ambiguity about who is asked and which options are offered.
- All fixed numbers are written into the rules as constants, not stored as attributes. (fixes: P6): Saves attributes and removes the mismatch risk.
- Deal with one shuffle of the full deck (the single random event), then hand out cards in fixed order: cards 1-6 to seat 1, 7-12 to seat 2, 13-18 to seat 3, card 19 turned, card 20 hidden. (fixes: P7): One random draw per round, and a deterministic deal after it.

## Kept from the original

- Three players, trick-taking with a trump suit set by a turned card.
- Must follow suit if able; otherwise any card, including trump.
- Highest trump wins, otherwise the highest card of the led suit; the trick winner leads next.
- Jack penalties in the original ratio: J♠ -1, J♣ -2, J♦ -3, J♥ -4.
- Points for tricks taken, accumulated over hands.
- Eldest, the seat left of the dealer, leads the first trick.

## The variation's rules

R1 Setup. There are exactly 3 players, seats 1, 2 and 3. The full deck is the 20 cards AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H. At the start every player's total is 0, their hand is empty, hand_number is 1, and the deck holds all 20 cards.

R2 Rank. Within a suit, cards rank A (high), K, Q, J, 10 (low).

R3 Length. The game has exactly 36 rounds. Each round is one trick. The game ends after round 36.

R4 Hands. Rounds 1-6 form hand 1, rounds 7-12 hand 2, and so on up to rounds 31-36, which form hand 6. trick_in_hand runs from 1 to 6 within each hand.

R5 Dealer. In hand h, the dealer is seat ((h-1) mod 3) + 1. So hand 1 is dealt by seat 1, hand 2 by seat 2, hand 3 by seat 3, hand 4 by seat 1, and so on.

R6 Eldest. When a hand begins, eldest is the seat to the dealer's left: (dealer mod 3) + 1. Eldest is the leader of that hand's first trick.

R7 Reset and deal. In the first round of every hand, before anything else happens:
(a) Set the deck to the full 20-card list from R1.
(b) Empty every player's hand and the discard pile.
(c) Set every player's bid, tricks_taken and hand_score to 0.
(d) Shuffle the deck once. This is the only random event in the round.
(e) Cards 1-6 of the shuffled deck go to seat 1, cards 7-12 to seat 2, and cards 13-18 to seat 3. Each hand is seen only by its owner.

R8 Turned card. Card 19 is turned face up into turned_card, seen by all, and trump_suit becomes its suit. That card is out of play for the hand.

R9 Hidden card. Card 20 goes face down into hidden_card. It is out of play and is never revealed during the hand. After the deal the deck holds 0 cards.

R10 Bid. In the first round of every hand, right after the deal, all three seats bid at the same moment in one simultaneous poll. Each seat is offered exactly the options 0, 1, 2, 3, 4, 5 and 6: the number of tricks it predicts it will take this hand. All bids are then shown to everyone.

R11 Play order. Every round, the leader plays one card from their hand first. Then seat (leader mod 3) + 1 plays, then the remaining seat. Players act one at a time and each sees the cards already played to the trick. The suit of the leader's card is led_suit. Each played card is removed from its owner's hand, recorded as that player's played_card, and added to the discard pile. It never returns to the deck.

R12 Follow suit. A player who holds any card of led_suit must play one of those cards. A player who holds none may play any card in their hand, including a trump. The leader may play any card.

R13 Trick winner. If any trump_suit cards were played, the highest-ranked trump wins. Otherwise the highest-ranked card of led_suit wins. The winner becomes trick_winner and leads the next trick of the same hand.

R14 Trick score. The trick winner adds 1 to tricks_taken and adds to hand_score: +2, minus the penalties for any Jacks among the three cards in the trick (JS 1, JC 2, JD 3, JH 4). A Jack is penalised even if it is the trump suit.

R15 End of hand. After the trick in round 6, 12, 18, 24, 30 or 36 is scored:
(a) Each player whose tricks_taken equals their bid adds 5 to hand_score.
(b) Each player adds hand_score to their total.
(c) The totals are announced to all.

R16 Winner. After round 36, the player with the highest total wins. If two or three players tie for the highest total, the game is a draw.

Objective: After the 36th trick and the final end-of-hand scoring, the single player with the highest total wins. A tie for the highest total is a draw.

Expected effect: Bidding turns each deal into a forecasting problem. Strong hands bid high and must win exactly that many tricks. Weak hands bid 0 or 1 and try to duck. Because bids are public, opponents can spoil an exact bid: they can force a trick onto a player who bid 0, or dump a Jack onto a trick the leader must win. Inferring voids and the location of the hidden card and the Jacks drives card play. The exact-bid bonus lets a poor deal still score, which reduces luck, and six hands with a rotating eldest average out seat effects. Simple policies can all lose. Always bidding 0 scores only when you take no tricks. Always bidding 6 almost never hits. Always playing high collects Jacks. Always playing low gives up both tricks and bonuses. Talk is left out. Bids already signal intentions, and free talk in a single-winner trick game would mostly be bluffing that adds steps without adding a decision the bids do not already create.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
