# da_bai_fen: ready for review

Built from the variation **Da Bai Fen Duplicate** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Each round is exactly one trick: four sequential card plays and nothing else. The trump suit is fixed by hand number (Spades in hands 1 and 3, Hearts in hands 2 and 4), with both jokers as the top trumps. There is no trump-naming or exposure decision. (fixes: P1): This brings choice steps to exactly 4 per round and removes the extra declaration step.
- Hands 1 and 2 are fresh random shuffles. Hands 3 and 4 are duplicate replays of hands 1 and 2: the identical cards and kitty, with every hand rotated one seat, so the other partnership holds each set of cards and the same cards lead first. (fixes: P2, P3): The deal is genuinely random each match, yet each partnership plays both sides of every deal. Card luck cancels out and only the quality of play differs.
- First leads by hand are seat 1, seat 2, seat 2 and seat 3. Each partnership leads first in exactly two hands, and the replay makes each team lead with the same cards the other team led with. (fixes: P2): This removes any structural first-lead edge for seats 1 and 3.
- The deck is cut to 26 cards: four suits of A, K, Q, J, 10, 5 plus two jokers. Each player gets 6 cards and 2 go face down to the kitty. Only single cards are led. There is no kitty exchange and no redeal. Instead the kitty's points, doubled, go to the team that wins the last trick of the hand. (fixes: P4): The game becomes buildable while keeping the point cards (still 100 points in the deck), the jokers, the trump suit, the kitty and an end-of-hand fight. Doubled kitty points reward saving control for the final trick.
- The level ladder is replaced by total captured points over the four hands. The higher partnership total wins, and equal totals are a draw. (fixes: P5): This gives a short match decided by arithmetic. Under duplicate dealing the point total measures play directly.
- The engine offers each player only legal cards. You must play a card of the led suit if you hold one, with trump-suit cards and jokers counting as the trump suit; otherwise you may play any card. (fixes: P6): This makes legality mechanical, so no judge and no illegal plays are involved.
- There is no talk phase. (fixes: P3): Partners would simply announce their hands, deleting the inference that makes the game worth playing. The conflict is between teams, and inside a team there is nothing to bargain. Signalling happens through card play, as in the original.

Objective: After hand 4, the team with the higher match total (captured card points plus doubled kitty points) wins. If the totals are equal, the match is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SEAT/ROTATION CHECK. Hand 1: Spades trump, seat 1 (A) leads, holdings X1..X4. Hand 3: seat s+1 receives Xs, Spades trump again, and seat 2 leads holding X1. The play order from the leader is therefore 2(X1),3(X2),4(X3),1(X4), the same as 1(X1),2(X2),3(X3),4(X4) in hand 1. The trump suit and kitty ar
- playable: pass. COMPLETENESS. The rules fix the deck (26 unique cards), point values, trump order (BJ > SJ > A K Q J 10 5 of trump), that jokers follow as trump, the plain-suit order, the follow rules (trump lead requires trump; otherwise follow suit if able; otherwise any card), and the trick winner. Cards are uni
- reasoning_over_luck: pass. CHANCE. The random deals of hands 1 and 2 are each replayed with the teams swapped, from the same relative seat and leader, with the same trump suit and kitty. A strong or weak deal therefore benefits both teams equally. When both teams follow the same good strategy, the result is a draw, not a deal

## Complexity

- steps_per_round: designed 15, built 16, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 17, built 56, limit 20 (built: 80)
- hidden_elements: designed 2, built 14, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Seats 1 and 3 are team A, seats 2 and 4 are team B; scores start at 0
- pass: The deck holds 26 cards before the first deal
- pass: 5, 10 and K are worth 5, 10 and 10, A is worth 0: a trick of C5 C10 CK CA gives team B 25
- pass: Hand 2 has Hearts as trump (deal is random, only the trump suit is asserted)
- pass: Hand 1 starts with Spades as trump
- pass: Big Joker beats Small Joker beats trump Ace; jokers must follow a trump lead
- pass: In a non-trump suit K beats Q, J and 10
- pass: Hand 1 deal: 6 cards each, 2 in the kitty, deck emptied (random cards, only counts asserted)
- pass: Hand 3 gives each seat the hand-1 cards of the previous seat
- pass: Hand 4 gives each seat the hand-2 cards of the previous seat
- pass: Hand 3 is played as a replay of hand 1's cards
- pass: Seat 2 leads the first trick of hand 3 (only seat 2 holds clubs and no trump is out)
- pass: Seat 3 leads the first trick of hand 4 (only seat 3 holds clubs and no trump is out)
- pass: The leader is offered every card in hand
- pass: On a trump lead, a seat holding trumps is offered only trumps
- pass: On a non-trump lead, a seat holding that suit is offered only that suit
- pass: A seat void in the led suit is offered every card
- pass: The highest trump wins over the led suit's Ace
- pass: With no trump played, off-suit Aces lose to the led suit's 10
- pass: Trick points add to the winning team's existing total
- pass: Seat 4 wins a trick and leads the next one with its lone heart
- pass: After trick 6 the kitty is revealed and doubled for the trick winner's team
- pass: The kitty is not revealed before the end of the hand
- pass: Match ends after hand 4; team A with the higher total wins
- pass: Equal match totals: all four seats share the win
- pass: A trick plays through with no talk step and scores still at 0 for a pointless trick

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seats 1 and 3': 14, 'seats 2 and 4': 6}, 49-67 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 96.0 decisions, prompts of 87 characters on average (longest 111)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 1 and 3': 33, 'seats 2 and 4': 24, 'seats 1, 2, 3 and 4': 3}
- always `first@seat1`: won 0, lost 31, drew 29
- always `first@seat2`: won 0, lost 29, drew 31
- always `last@seat1`: won 0, lost 29, drew 31
- always `last@seat2`: won 0, lost 28, drew 32

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built as specified, and evaluation found design flaws. Because the step list is flat, the declarer's trump-naming choice sits beside the four card plays and gives 5 choice steps per round, over the limit of 4. Every random match also ended as a win for seats 1 and 3, so the players' choices do not change the result.

## Choices the rules did not make

- 4 players, suggested 4: The designer fixed two partnerships of two. The duplicate replay structure depends on exactly 4 seats rotating, so neither fewer nor more seats work.
- No talk step: The source forbids table talk. Partnership play here rests on inferring a partner's cards from what they play.
- Rank numbers 1 to 8 and strength bases of 100 (led suit) and 200 (trump): These let the trick winner be found by arithmetic as the seat with the highest card_strength.
- The play order starts at the leader: The source says the leader plays first and the others follow anticlockwise. The ask step runs from the seat in leader.
- Saved hand1_cards and hand2_cards are visible to their owner (ally): A player attribute cannot be hidden from its owner, and the owner already saw those cards when they were dealt.
- Strategy at the table: A thoughtful player counts the trumps and points already played, keeps high trumps to capture the 6th trick (worth the doubled kitty), and feeds point cards to tricks the partner is winning.

## Simplifications

- Each team's match total is mirrored onto both partners as score: The ranking is a per-player expression, so both partners carry their team's total.
- A draw is represented as all four seats sharing the top rank: The engine has no separate draw outcome. Tied totals give every seat the same rank_by value.

## Encoding attempts

- 1: the game file was refused by the loader: da_bai_fen: steps[6].each.do[5].value.calc: "led_card in ['JOKER_BIG', 'JOKER_SMALL'] or led_card[0:1] == trump_suit": Slice is not allowed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (played_card, played_card, played_card, played_card) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
