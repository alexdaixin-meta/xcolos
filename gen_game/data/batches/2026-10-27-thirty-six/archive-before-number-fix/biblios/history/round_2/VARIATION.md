# Variation: Biblios: Scriptorium Duel of Three

Three scribes take turns drawing two cards, secretly keeping one and auctioning the other to the two rivals in a sealed bid paid in gold. Before each bid all three speak once at the same moment, to fix prices, pitch the lot or propose blocking the leader. Church cards shift colour values. After 12 rounds each colour's value goes to its single strict leader, and the most VP wins.

Players: 3 to 3, best with 3

## Review of the original

Biblios is a 2-4 player card game. In a gift phase each player in turn splits drawn cards between a secret keep, a face-down auction pile and public picks for the others. In an auction phase Gold cards buy the remaining cards. Church cards shift the VP value of five colour categories, and the player with the most VP from winning categories wins.

- **non_degenerate**: good. No fixed policy dominates. Always passing in auctions leaves you with only gift-phase cards. Always bidding high drains the Gold needed later. Spreading across categories wins none. Category ties and the Church dice keep choices live. Seat order rotates, so no seat has a lasting edge.
- **skill_sensitive**: good. Splitting the gift cards (what to hide, what to give away, what to auction) and pricing auctions against the Gold you have left are real skills. The shuffle adds noise, but a strong player reliably beats a weak one over a game.
- **headroom**: good. Inferring rivals' hidden keeps from what they let go, timing Church moves and budgeting Gold across the auction leave deep room to improve. A novice still wins some categories.
- **reasoning_dependent**: good. Face-down keeps and face-down auction cards create hidden state. Players must infer rivals' colour totals and Gold from what was passed, bought and paid.
- **verifiable**: good. Scoring is arithmetic: colour sums, a letter tiebreak and VP totals.
- **fits_platform**: weak. It is turn-based and text-only, but there are 87 cards, two phases, multi-round ascending auctions, a random-steal penalty for failing to pay, letter tiebreaks and 5 dice. That is far more steps and state than the engine allows. The previous cut-down variation fit the limits but had no talk in a 3-player game full of side deals.

## Problems

- The original is too large for the engine: 87 cards, two separate phases, open ascending multi-bidder auctions, a random steal on failed payment, letter tiebreaks and five dice.
- In the previous variation the two bidders share an interest against the active seller: both bidding 0 starves the seller, but each is tempted to bid 1 and buy cheaply. With no talk this dilemma is a blind guess.
- In the previous variation the two trailing players share an interest in blocking the leader's colour, since a tied top total scores nobody. Without talk they cannot propose or test such an alliance.
- In the previous variation the active seller wants to talk up the lot and has no voice, so the seller seat is passive during its own auction.
- The previous variation sits at the attribute limit, so adding talk needs a saving elsewhere (the separate high_count attribute and a separate bid-reset step are redundant).

## Changes

- Add a simultaneous talk step after the lot is announced and before bidding. All three players, including the active player, each write one short free-text message at the same moment. All three are then shown to everyone, and nothing said is binding. (fixes: In the previous variation the two bidders share an interest against the active seller: both bidding 0 starves the seller, but each is tempted to bid 1 and buy cheaply. With no talk this dilemma is a blind guess.): This gives the bidders' price-fixing dilemma, the trailing players' blocking alliance and the seller's sales pitch something to reason about. Promises can be made, tested against the public bid record and broken. Writing at the same moment stops later speakers from copying the first.
- Bids, results and Church choices stay fully public, and the bought list stays public, so every talk promise can be checked against what each player actually did. (fixes: In the previous variation the two trailing players share an interest in blocking the leader's colour, since a tied top total scores nobody. Without talk they cannot propose or test such an alliance.): Reading who can be trusted needs a visible record. Cheating on a 'both bid 0' pact or on a blocking promise is visible next round, so reputation matters.
- The active player speaks in the talk step even though they do not bid. (fixes: In the previous variation the active seller wants to talk up the lot and has no voice, so the seller seat is passive during its own auction.): The seller can talk up the lot, hint at which colour they kept, or offer future Church support to one bidder to break the other bidders' pact. This turns the seller seat into an active one.
- Remove the high_count attribute (the winner is simply the bidder whose bid is strictly greater than the other's and at least 1). Merge the bid reset into the announcement step (bids are reset to 0 right after being announced). (fixes: The previous variation sits at the attribute limit, so adding talk needs a saving elsewhere (the separate high_count attribute and a separate bid-reset step are redundant).): This frees one attribute and one step, so the per-player message attribute and the talk step fit: 18 steps, 4 choice steps, 20 attributes.
- Keep the cut-down core from the previous variation: a 24-card deck in three colours, a 2-card gift (keep one secretly, auction the other), a sealed two-bidder auction capped at gold, Church moves clamped once to 1-5, and a strict-majority colour scoring with no letters. (fixes: The original is too large for the engine: 87 cards, two separate phases, open ascending multi-bidder auctions, a random steal on failed payment, letter tiebreaks and five dice.): It already fits the limits and removes the impossible-to-build parts while keeping hidden keeps, Gold-funded auctions and Church manipulation.

## Kept from the original

- The gift dilemma: the active player secretly keeps one card and is forced to offer another.
- Auctions paid in Gold, with Gold also available as cards to keep or buy.
- Church cards that move colour VP values up or down.
- Majority scoring per colour: the single highest total takes that colour's current VP value.
- Hidden hands, so rivals' colour totals must be inferred from what they kept, passed and bought.
- Gold has no value at the end beyond breaking ties, so it must be spent wisely before then.

## The variation's rules

VISIBILITY.
V1. Hidden: each player's private hand, colour totals (red, blue, green) and gold are known only to that player. The order of the deck is known to nobody.
V2. Public: the deck composition (R1), every lot, every talk message and who wrote it, every bid, every auction result and price, every player's bought list, every Church choice and who made it, and the table VP values.
V3. Opponents can work out part of a rival's gold from sales and purchases, but kept Gold cards are never revealed. All gold is revealed at scoring.

SETUP.
R1. The deck holds 24 cards:
- Red, Blue and Green, each with values 1,1,2,2,3,4 (written like 'red-1'), 18 cards;
- Gold cards with values 2,2,3,3 (written like 'gold-2'), 4 cards;
- 2 Church cards ('church').
The deck is shuffled once at the start and never again.
R2. Each player starts with:
- gold 4;
- an empty private hand and an empty public bought list;
- red=0, blue=0, green=0;
- bid=0, church_pending=false, church_choice='none', message empty, vp=0.
R3. The table starts with vp_red=3, vp_blue=3, vp_green=3, round=0, lot='none' and drawn empty.

EACH ROUND (12 rounds).
R4. Round r begins (round becomes r). The active seat is ((r-1) mod 3)+1, so seats go 1,2,3,1,2,3,... and each seat is active exactly 4 times.
R5. The first two cards of the deck are moved, in order, into 'drawn'. Only the active player sees them.
R6. Keep. The active player alone chooses one of the two drawn cards to keep.
R7. The kept card goes into the active player's private hand:
- a colour card adds its value to their matching colour total;
- a Gold card adds its value to their gold;
- a Church card sets their church_pending to true.
The kept card is never announced.
R8. The other drawn card becomes the lot and is announced to everyone. 'drawn' is emptied.

TALK.
R9. All three players, including the active player, each write one short message at the same moment, without seeing the others' messages. All three messages are then shown to everyone with who wrote them. Nothing said is binding. Players may propose prices, alliances or Church moves, bluff about their hands, or say nothing useful.

AUCTION.
R10. The two non-active players at the same moment each secretly bid a whole number from 0 up to their own current gold. The active player does not bid.
R11. If one bid is strictly greater than the other and is at least 1, that bidder wins the lot:
- they pay their bid from their gold to the active player's gold;
- the lot is added to their public bought list;
- a colour lot adds its value to their matching total, a Gold lot adds its value to their gold, and a Church lot sets their church_pending to true.
If the two bids are equal (including both 0), nobody pays and the lot is discarded.
R12. Both bids and the result (the winner and the price, or 'discarded') are announced to everyone. Then both bids are reset to 0 and lot becomes 'none'.

CHURCH.
R13. Every player whose church_pending is true chooses, at the same moment, one of: 'red up', 'red down', 'blue up', 'blue down', 'green up', 'green down'. The choice is stored as church_choice. At most two players can choose in a round: the active player through a kept Church, and the lot winner through a bought Church.
R14. For each colour, the net change is (number of '<colour> up' choices) minus (number of '<colour> down' choices) made this round. This net change is added to that colour's VP value, and the result is clamped once to between 1 and 5. All choices are announced with who made them. Then church_pending becomes false and church_choice becomes 'none' for everyone.
R15. If round is 12, go to END. Otherwise start the next round.

END.
R16. After round 12 the deck is empty. All hands, colour totals and gold are revealed.
R17. For each colour, if one player's total is strictly higher than both others, that player adds that colour's current VP value to their vp. If the highest total is tied between two or more players, nobody scores that colour.
R18. The highest vp wins. A tie on vp is broken by more remaining gold. If that is also tied, the game is a draw.

Objective: After 12 rounds, each colour's VP value (1 to 5) goes to the single player with the strictly highest total in that colour. A tied top total scores no one. The player with the highest vp wins. A tie on vp is broken by more remaining gold, and a further tie is a draw.

Expected effect: Each auction becomes a short non-binding negotiation among three players with clearly opposed interests.

What the players disagree about:
- The two bidders jointly prefer a 'both bid 0' pact that starves the seller of gold. Each can instead bid 1 and take the lot almost free. A player who follows the pact and bids 0 while the other defects loses the card, and the seller gains gold.
- The two trailing players can agree to block the leader's colour by buying cards in it, or by pushing its value down with a Church card. The leader, or the second-placed player, can quietly defect to take that colour themselves. A follower who spends gold blocking can end up handing the game to their 'ally'.
- The seller talks up the lot, hints at a kept colour, or offers future Church support to one bidder to break the bidders' pact. A bidder who believes a bluff overpays.

Why talk takes thought:
- Bids and Church choices are public, so promises are tested and reputations form across the 4 times each seat is active.
- Hidden hands mean claims about colour totals cannot be verified until scoring.
- Gold is worthless at the end except as a tiebreaker, so late rounds bring aggressive spending and sharper betrayals of earlier pacts.

Simple policies all lose against reasoned play:
- Always bidding 0 forfeits every lot.
- Always bidding all your gold enriches sellers and leaves you broke when key colours appear.
- Always keeping the higher-value card ignores what the lot tells rivals.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 20 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
