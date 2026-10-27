# Variation: Biblios: The Scriptorium (revised)

Three scribes take turns drawing 3 cards, secretly keeping one, auctioning one by sealed bid and giving one away. They collect Red, Green and Blue manuscripts, Gold and Church cards that shift what each colour is worth. The majority in each colour scores its die.

Players: 3 to 3, best with 3

## Review of the original

Biblios is a 2-4 player card game. Players take turns as active player, drawing cards and splitting them between a secret keep, a blind auction pile and public picks for the others. In a second phase the auction pile is sold for Gold cards, Church cards shift the victory-point dice on five colours, and the majority holder in each colour scores that colour's die.

- **non_degenerate**: good. In the previous Scriptorium variation no simple policy is safe. Always bidding 0 leaves you with only leftover gifts while rivals win lots. Always bidding all your Gold wins one early lot and then leaves you broke against later, better lots. Always keeping the highest card telegraphs your colour, and rivals bid against you or push its die down. Seats are symmetric: each player is active 4 times in 12 rounds, and the lot-tie rule favours the active player, which rotates. Majority ties score nothing, so mirroring a rival gains nothing.
- **skill_sensitive**: good. The deal order is random, but every card passes through a deliberate split, a sealed-bid auction or a die vote. Card counting matters: each colour totals 16 and the composition is public. So do reading which colour an opponent is building from their bids and Church votes, and budgeting Gold. These decide the result more than the draw does.
- **headroom**: good. A weak player still collects gifts and can take one colour cheaply. A strong player keeps improving: splitting so the gift tempts nobody and the lot draws overbids, shading bids to just above rivals' likely values, and timing Church votes to devalue a colour already lost.
- **reasoning_dependent**: good. Kept cards, Gold totals and the deck order are hidden. A player must infer rivals' colour sums and budgets from public lots, gifts, revealed bids and die votes, and plan Gold over 12 rounds.
- **verifiable**: good. Majorities, die values, VP and the Gold tiebreak are all arithmetic on tracked numbers.
- **fits_platform**: weak. The previous variation broke the limits and was ambiguous. Its attributes reached 21 (more than 20) once the dice were counted. A player holding two Church cards needed a second choice that the single pending flag could not represent. 'Clockwise' was never defined, yet the tie rules depended on it. A lot and a gift could also both reach the same non-active player when the two non-actives tied on the highest bid.

## Problems

- (a) Attributes exceed 20. Stored red/green/blue sums per player plus the dice and table state push the count to 21 or more.
- (b) Double Church. A player can receive two Church cards in one round (active keeps one and wins a Church lot, or a non-active wins the lot and also gets the gift). That needs a second choice the flag cannot hold, and the rule text contradicts itself.
- (c) 'Clockwise' is undefined relative to P1, P2, P3, so the lot and gift tie rules are ambiguous.
- (d) The gift rule can hand both the lot and the gift to the same non-active player when the two non-actives tie on the highest bid. This contradicts the gift's role as a consolation and creates the double-Church case.

## Changes

- Delete the stored Red/Green/Blue sums. Colour sums are computed from hands once, at scoring. (fixes: (a) Attributes exceed 20.): Saves 9 attributes. The sums are only needed at the end.
- Replace the church-pending flag with a per-player church_count (0-2). Each player with church_count of 1 or more makes ONE simultaneous Church choice, which moves the chosen die by church_count steps. (fixes: (b) Double Church.): A single choice step handles any number of Church cards with plain arithmetic, so no fifth choice step is needed.
- Define clockwise as P1 -> P2 -> P3 -> P1. 'Next clockwise from the active player' is stated for each seat. (fixes: (c) 'Clockwise' is undefined.): Makes the tie rules unambiguous.
- The gift goes to the non-active player who did NOT win the lot. Only if the active player won the lot does it go to the lower-bidding non-active player (tie: the player next clockwise after the active player). (fixes: (d) The gift rule can hand both cards to one player.): No player ever receives both the lot and the gift. A non-active player now gains at most 1 card per round (lot or gift) and the active player at most 2 (keep and lot), so church_count never exceeds 2.

## Kept from the original

- The active player's split of drawn cards into a secret keep, an auctioned lot and a gift to others
- Gold cards as currency gained from cards, and paying Gold to win auctions
- Church cards that move the colour dice up or down
- Majority scoring per colour worth the current die value, with ties scoring nothing
- Hidden hands and hidden Gold, read through bids and votes

## The variation's rules

SETUP. The deck has 36 cards:
- Colour cards (21): for each of Red, Green and Blue, values 1, 1, 2, 2, 3, 3, 4. Each colour totals 16.
- Gold cards (9): values 1, 1, 1, 2, 2, 2, 3, 3, 3. These total 18 Gold.
- Church cards (6): each simply named 'Church'.
The deck composition is public. The deck is shuffled once at setup and kept face-down, its order hidden from everyone.
Each player starts with:
- 4 Gold, private (only that player sees it);
- an empty hand, private;
- church_count 0.
Three public dice, vp_red, vp_green and vp_blue, each start at 3 and always stay between 1 and 5.
Players sit P1, P2, P3. Clockwise order is P1 -> P2 -> P3 -> P1. The player next clockwise after P1 is P2, after P2 is P3, and after P3 is P1.
The game lasts 12 rounds. 12 rounds x 3 cards uses the whole deck exactly.

EACH ROUND (r = 1 to 12):
1. Active player. P1 is active in rounds 1, 4, 7 and 10; P2 in rounds 2, 5, 8 and 11; P3 in rounds 3, 6, 9 and 12. This is announced to everyone.
2. Deal. The top 3 cards of the deck are removed and shown privately to the active player as positions 1, 2 and 3.
3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone with their authors. Talk is not binding and may be a bluff.
4. Split. The active player chooses one of: 'keep 1 sell 2', 'keep 1 sell 3', 'keep 2 sell 1', 'keep 2 sell 3', 'keep 3 sell 1', 'keep 3 sell 2'. The keep card goes face-down into the active player's hand. The sell card becomes the lot. The remaining card becomes the gift.
5. Reveal. The lot and the gift are shown face-up to everyone. The kept card stays secret.
6. Bid. All three players, including the active player, privately bid a whole number of Gold from 0 upward, all at the same moment. A bid above a player's current Gold counts as exactly that player's whole Gold.
7. Sale. The highest bid wins the lot.
- On a tie for highest: the active player wins if among the tied; otherwise the tied player who comes first clockwise after the active player wins. (If all bid 0, the active player wins.)
- The winner loses Gold equal to their bid (paid to the bank) and takes the lot into their hand.
- All three bids are then revealed to everyone.
8. Gift.
- If a non-active player won the lot, the gift goes to the other non-active player.
- If the active player won the lot, the gift goes to whichever non-active player bid lower. On a tie it goes to the player next clockwise after the active player.
9. Gold cards. Every Gold card that entered a hand this round is removed from that hand, and its value is added to that player's Gold.
10. Church cards. For each player, church_count is set to the number of Church cards that entered their hand this round (0, 1 or 2; only the active player can reach 2). Those Church cards are removed from the hand. Each player's church_count is announced.
11. Church choice. Every player with church_count of 1 or more privately makes exactly ONE choice at the same moment, from: 'red up', 'red down', 'green up', 'green down', 'blue up', 'blue down'. Players with church_count 0 do not choose.
12. Red die. net = (sum of church_count over players who chose 'red up') minus (sum of church_count over players who chose 'red down'). Set vp_red = min(5, max(1, vp_red + net)).
13. Green die. Same calculation with 'green up' and 'green down': vp_green = min(5, max(1, vp_green + net)).
14. Blue die. Same calculation with 'blue up' and 'blue down': vp_blue = min(5, max(1, vp_blue + net)). The three die values and each player's Church choice are announced.
15. Reset. Every church_count is set to 0, and bids are cleared.
16. End check. After round 12, go to scoring; otherwise start the next round.

SCORING. For each colour, each player's sum is the total value of that colour's cards in their hand. The player with the strictly highest sum in a colour scores VP equal to that colour's die value. If two or more players tie for highest, nobody scores that colour. A player's VP is the total over the three colours.

Objective: The player with the most VP wins. If players tie on VP, the tied player with the most remaining Gold wins. If they are still tied, the game is a draw among them.

Expected effect: Play matches the tested variation, now buildable and unambiguous.

What the players disagree about:
- Every lot is contested between three rivals with hidden budgets.
- The active player wants the lot to fetch high bids and the gift to tempt no one.
- Each Church card is a fight over which die rises or falls: you want your colour up and your rivals' colours down.

Talk lets players bluff interest in a colour, propose a joint push against the leader's die, or feign poverty. A player who simply follows a proposal can lose: an ally who promised 'blue down' may vote 'blue up' because they secretly lead Blue, and a player who believes a rival's 'I'm out of Gold' bluff underbids and loses the lot.

Only one player can win and majority ties score nothing, so cooperation is always temporary and every message must be weighed. Simple policies fail:
- Always bidding 0 cedes every lot.
- Always bidding everything bankrupts you early.
- A blind fixed split leaks your colour.

The double-Church multiplier makes keeping a Church card while also winning a Church lot a real but readable swing.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
