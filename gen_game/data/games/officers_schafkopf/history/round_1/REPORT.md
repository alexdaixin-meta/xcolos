# officers_schafkopf: needs review

Built from the variation **Officers' Schafkopf: Bidding Match** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Shrink the deck to 16 cards (Ace, Ten, Ober, Unter in four suits, 104 card points). Each player gets 4 private hand cards and 2 stacks of one face-down card under one face-up card. A hand is 8 tricks and the declarer needs 53. (fixes: The state is too large: 32 cards in four stack positions per player plus a hand exceeds the platform's attribute and step limits.): Keeps the private hand, the face-up and face-down stacks, the revealing of the down card and the Solo/Wenz trump structures, while bringing the state and step count within the limits.
- Play a match of 4 hands with the dealer alternating, scored in match points. (fixes: One deal decides everything, so luck of the cards swamps skill.): Several deals average out card luck, and each player is forehand twice, so no seat has an edge over the match.
- Add a simultaneous sealed bid before the contract: Pass, 53, 66 or 79 card points. The higher bid declares, ties go to forehand, and if both pass, forehand must declare at 53. A higher bid is worth more match points if made and costs as much if failed. (fixes: The non-dealer is forced to declare whatever they hold, so a bad deal for the forced declarer is close to an automatic loss. This is a seat and deal edge with no decision to correct it.): A weak hand can now hand the declaration to the opponent. Bidding forces each player to judge their own strength from partial information and to guess the opponent's bid. Hand evaluation becomes a scored skill.
- Use graded match points: a bid of 53 is worth 2, 66 is worth 3 and 79 is worth 4, plus 1 for taking all 8 tricks, all doubled by Stoß. The winner is the player with more match points, then more total card points. (fixes: Winning is binary (61 or not). It gives no reward for judging how strong a hand is, so there is little to reason about before play beyond picking the trump suit.): This rewards accurate judgement of how much the hand can make rather than a single win/lose line. The Stoß becomes a risk decision with a real price either way.
- State every rule explicitly: the dealing layout, the trump orders for Solo and Wenz, the following rules, and when a down card is revealed and becomes playable. (fixes: The rules are underspecified for building: 'or deal as hands' is optional, the trump order is not stated, and the scoring of doubles is not stated.): So the game can be built and played without guessing.

Objective: After 4 hands, the player with more match points wins. If match points are equal, the player with the higher total card points over all 4 hands wins. If both are equal, the match is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. ARITHMETIC CHECKS. Each suit is 11+10+3+2 = 26 points, and 4 x 26 = 104. Each player gets 4 hand cards and 2 stacks of 2, so 8 cards each, 16 in all, which matches 8 tricks. The 53 threshold is one more than half (52), so 52-52 is a failed contract. That is a real threshold and not a free win.

Solo
- playable: pass. COMPLETENESS. The rules cover:
- the deal (who sees what; face-down cards are unknown even to their owner);
- the simultaneous bid, including the ties rule and the both-pass rule;
- the contract choice and the full trump order for Solo and for Wenz;
- the Stoß decision;
- available cards, which are 
- reasoning_over_luck: pass. WHAT THERE IS TO INFER:
- At the bid, each player knows 8 of 16 cards (4 own plus 4 up). The opponent's 4 hidden cards and the 4 face-down cards are unknown.
- The opponent's bid, announced after bidding, signals their strength.
- The contract choice reveals the declarer's trump holding to the defen

## Complexity

- steps_per_round: designed 17, built 13, limit 20
- choice_steps_per_round: designed 3, built 5, limit 4
- attributes: designed 19, built 87, limit 20 (built: 80)
- hidden_elements: designed 2, built 18, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Before any deal the deck holds all 16 cards
- pass: After 18 rounds (two hands of 9 rounds) the match is in hand 3
- pass: Seat 1 is forehand in hand 2, so it declares when both pass
- pass: After the deal each seat holds 4 hand cards and the deck is empty
- pass: Each seat's private hand holds exactly 4 cards after the deal
- pass: Both seats are offered every bid and the bids are recorded
- pass: Higher bidder (seat 1, 79 over 53) is declarer at 79
- pass: Equal bids of 66: forehand seat 2 declares at 66
- pass: Both pass: forehand seat 2 declares at 53
- pass: Both bids are announced along with the declarer
- pass: Declarer seat 2 picks Wenz; the defender is not asked for a contract
- pass: A Hearts Solo hand plays all 8 tricks for any deal: every hand card is used and hand 2 begins
- pass: A Wenz hand plays all 8 tricks for any deal
- pass: Defender seat 1 gives Stoss: multiplier 2; the declarer is not asked
- pass: Defender seat 1 gives No Stoss: multiplier 1
- pass: Hand cards and stack cards together supply all 8 tricks: no hand card is left after the hand
- pass: Lead passes correctly through the 8 tricks for any deal, and the hand completes
- pass: A Bells Solo hand with trumps as one suit completes all tricks for any deal
- pass: Following under the follow-suit rule always leaves a legal card: the hand completes
- pass: Trick winners are decided in a Leaves Solo for any deal and the hand completes
- pass: Trick points accrue over a full hand for any deal (hand completes)
- pass: Face-down cards turn up so all 8 tricks can be played
- pass: Without Stoss at bid 53 a seat gains at most 3 per hand, so a 13-point lead holds for any deal
- pass: With Stoss at bid 53 a seat gains at most 6 per hand, so a 25-point lead holds for any deal
- pass: Hand scoring runs after trick 8 and the next hand begins
- pass: After 36 rounds more match points wins: a 100-point head start cannot be caught

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 8, 'seat 1': 12}, 56-68 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 80.0 decisions, prompts of 177 characters on average (longest 245)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 27, 'seat 1': 33}
- always `first@seat1`: won 40, lost 20, drew 0
- always `first@seat2`: won 44, lost 16, drew 0
- always `last@seat1`: won 11, lost 49, drew 0
- always `last@seat2`: won 10, lost 50, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The R1 test is correct. In Acorns Solo, Ober of Bells (trump strength 17) beats Unter of Hearts (14), so seat 2 should take the 5 points (49+5=54) and seat 1 stays at 50, below the 53 bid. The game gave the trick to seat 1, and the R12 failures show the same fault: trick resolution ignores the trump strengths.
- round 1: fix_tests: The full-play tests (R2, R3) start from a real deal and ran without error, so trick play itself works. Only the four scenarios that inject a mid-hand state crashed. Those scenarios use internal names the test writer guessed (round_in_hand, leader, follower, hand, stack1_up, hand_points, a 'led card'), so the game's own bookkeeping, such as its led_card, did not match a card in its card table.
- round 1: revise_rules: The game was built faithfully, but the design exceeds the platform's budgets: 5 choice steps per round against a limit of 4, and 87 attributes against a limit of 80. It also has a degenerate strategy: always picking the first option wins about 70% of games for either seat, and always picking the last option loses over 80%.

## Choices the rules did not make

- 2 players (min, max and suggested): The designer set 2. The deal uses all 16 cards for exactly two players, so neither more nor fewer seats fit.
- Strategy check: A thoughtful player judges their hand plus the open stack cards before bidding high, picks the contract that fits their trumps, gives Stoß only when the declarer looks overstretched, and times the playing of stack cards to unlock the hidden cards beneath.
- No free-text talk step: Talk is not part of the rules, and with two opponents it only adds words.
- Pass is stored as bid 0: This makes 'higher bid' a numeric comparison.
- Trump ranks encoded as trump_strength 20 down to 11, and plain ranks as Ace 3, Ten 2, Ober 1: This lets the trick winner be decided by arithmetic while keeping exactly the source's order.
- rank_by = match_points * 1000 + card_total: Card totals can never reach 1000 (at most 416), so match points come first and card points only break ties. An exact tie is a shared result, which matches the source's draw.
- Trick card points and trick counts are public: Both players see every played card, so these totals are open information.

## Simplifications

- The bidding steps and the trick steps share one flat round list, each step gated by a 'when' condition on round_in_hand: The engine runs one round script. Per-step arithmetic conditions keep 36 rounds exactly as the source counts them.
- Hand scoring runs as an update at the end of trick round 8: This keeps the round count at 36 without adding a separate scoring round.
- Face-down stack cards are held as hidden table attributes rather than player attributes: Not even their owner may see them, and a player attribute cannot be hidden from its owner.
