# Variation: Scriptorium Lots (Seller's Edition)

Three scribes take turns privately splitting a two-card lot: one card kept secretly, one auctioned to the other two for gold that the seller pockets. Colour majorities score the colours' shifting worths, and leftover gold scores too.

Players: 3 to 3, best with 3

## Review of the original

Biblios is a 2-4 player set-collection game. In a gift phase the active player splits drawn cards between themselves, the auction pile and the other players. In an auction phase cards are bid for with Gold cards, and Church cards shift what each colour is worth. Winning the majority in a colour scores that colour's current die value.

- **non_degenerate**: weak. In the original, choices matter: what to keep, give or auction, and how much to bid. The previous variation, though, let a thoughtless 'always keep the 4, auction the 1' policy be close to optimal. Gold paid simply vanished, so a cheap card left little reason to sell anything valuable. Ties discarded the card, so 'always bid 0' cost nothing when the other bidders also passed. Neither policy is a certain winner, but the trade-offs were thin.
- **skill_sensitive**: weak. The previous test estimated that 30-40% of results were set by the deal. Which lots a player was active on decided where their four high cards fell. The auction pool, mostly 1s and 2s, rarely overturned a 3-card cluster. Once auction ties and blocking cancel out among good players, the luck of the high cards decides most majorities.
- **headroom**: good. Gold budgeting over many auctions, reading which colour opponents are chasing, and timing changes to colour worth leave room to improve. A weak player still collects cards and scores some colours.
- **reasoning_dependent**: bad. The previous variation revealed the lot publicly, so every kept card could be deduced (auction card subtracted from the lot). The only hidden thing left was an ambiguous peek, and the game became open-information bidding. The original Biblios has real hidden cards, but at 87 cards that hidden state is far too large for the platform.
- **verifiable**: good. Majorities, worths and VP are all sums and comparisons. No judge is needed.
- **fits_platform**: weak. The original's 87-card deck, Church cards and re-auction on non-payment are too large. The previous variation was text-only and turn-based but broke the limits: it needed 24 attributes against a limit of 20, used exactly 20 steps with no slack, and left the peek undefined in round 12.

## Problems

- P1 Hidden-information contradiction: the lot was revealed publicly, so kept cards could be deduced and the claimed inference did not exist.
- P2 The 'next lot' peek was undefined in round 12 and confusing in every round.
- P3 Separate hidden and public holdings needed 24 attributes, more than the limit of 20.
- P4 The step budget sat exactly at 20, with no slack for the multi-operation resolve and the bounded worth shift.
- P5 Deal luck: which lots a player was active on decided their high kept cards. Nothing let a player convert a bad lot into value.
- P6 Thin trade-offs: gold paid simply vanished, so selling a valuable card never paid. Ties discarded the card, so passive zero bidding carried no risk.

## Changes

- The current lot is shown privately to the active player only. Everyone else sees just the auction card. The public lot list lets opponents work out that the kept card's value is 5 minus the auction value and that its colour is one of exactly two. They narrow it by tracking which lots are used up. (fixes: P1 Hidden-information contradiction: the lot was revealed publicly, so kept cards could be deduced and the claimed inference did not exist.): This creates real, bounded hidden state that rewards bookkeeping and inference.
- The 'next lot' peek is removed entirely. Each round's own lot is the only thing shown, and only to its active player. (fixes: P2 The 'next lot' peek was undefined in round 12 and confusing in every round.): Nothing is left unspecified in round 12, and there is one clear private view per round.
- There is a single hidden holding per player per colour (9 attributes). Cards gained in auctions are announced in the public log rather than stored separately. The total is 19 attributes. (fixes: P3 Separate hidden and public holdings needed 24 attributes, more than the limit of 20.): This stays under 20, and the public cards remain knowable from the log.
- Announcing bids is merged into resolve, and the active player is excluded from bidding. The round is 15 steps. (fixes: P4 The step budget sat exactly at 20, with no slack for the multi-operation resolve and the bounded worth shift.): This leaves 5 steps of slack.
- The active player is the seller: the winning bid is paid to the active player, not removed. Remaining gold counts at the end, at 1 VP per full 4 gold. (fixes: P5 Deal luck: which lots a player was active on decided their high kept cards. Nothing let a player convert a bad lot into value.): A lot in an unwanted colour can be sold dear for gold that becomes VP. Choosing whether to keep the 4 or sell it becomes a real decision, and bad deals can be overcome by play.
- Equal bids, including 0-0, give the auction card to the seller for free. (fixes: P6 Thin trade-offs: gold paid simply vanished, so selling a valuable card never paid. Ties discarded the card, so passive zero bidding carried no risk.): Passive bidding now hands the seller a full lot, so 'always bid 0' can lose. Bidders must actually contest.
- Only the two non-active players bid, and they bid simultaneously. (fixes: P6 Thin trade-offs: gold paid simply vanished, so selling a valuable card never paid. Ties discarded the card, so passive zero bidding carried no risk.): This creates a direct duel between two rivals, with the seller profiting from their competition.

## Kept from the original

- The active player privately splits a draw between a secret card for themselves and a card that goes to auction, as in Biblios's gift phase.
- Gold-based auctions for cards.
- Colour majorities score the colour's current worth.
- Worth of colours shifts during play, like the Church cards and dice.
- Hidden holdings, with majorities known only at the end.

## The variation's rules

SETUP
- 3 players, seated 1, 2, 3.
- Each player starts with 12 gold. Gold is public.
- Each player has a holding of 0 in each of three colours: Red, Blue, Green.
- A player always knows their own holdings. Other players' holdings are never shown during the game.
- Each colour has a public worth, starting at 3.

THE LOT LIST
- The lot list is public and contains exactly these 12 lots of two cards each: R1+B4, R2+B3, B1+R4, B2+R3, R1+G4, R2+G3, G1+R4, G2+R3, B1+G4, B2+G3, G1+B4, G2+B3.
- R1 means a Red card of value 1, B4 a Blue card of value 4, and so on.
- Every lot sums to 5. Every individual card appears in exactly two lots.
- Before round 1, the 12 lots are put in a random hidden order. Round k uses the k-th lot, so all 12 lots are used, one per round.

ROUNDS
- There are 12 rounds.
- The active player is seat 1 in round 1, seat 2 in round 2, seat 3 in round 3, seat 1 in round 4, and so on. Each seat is active 4 times.
- The two other players are the bidders.

EACH ROUND
1. Private view. This round's lot is shown to the active player only. No other player ever sees it.
2. Keep. The active player chooses one of the two cards to keep. Its value is added secretly to that player's holding in its colour.
3. Announce. The other card (the auction card) is announced to everyone: its colour and value. Others can deduce the kept card's value (5 minus the auction value), but its colour is one of the two lots containing the auction card. Lots already used narrow this down.
4. Talk. All three players each write one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.
5. Bid. The two bidders, at the same time, each submit a whole-number bid from 0 up to the gold they hold.
6. Resolve. Both bids are announced.
   - If one bid is strictly higher, that bidder wins. The winner pays the bid to the active player (gold moves from winner to active player). The winner adds the auction card's value to their holding in its colour.
   - If the bids are equal (including both 0), nobody pays. The active player adds the auction card's value to their own holding in its colour.
   - The log records who received the auction card.
7. Shift worth. If a bidder won, that winner may choose one colour and raise its worth by 1 or lower it by 1, or change nothing. Worth stays between 1 and 5: a change past these limits has no effect. If nobody won, no shift happens. The worths are announced.

END OF GAME (after round 12)
- For each colour, compare the three players' holdings.
- The single highest holder scores VP equal to that colour's final worth.
- If two or three players tie for highest, each tied player scores half the worth, rounded down.
- If everyone holds 0 in a colour, nobody scores that colour.
- Each player also scores 1 VP for every full 4 gold they hold (gold divided by 4, rounded down).
- A player's VP is the colour VP plus the gold VP.

Objective: The player with the most VP wins. If players tie on VP, the tied player with more remaining gold wins. If still tied, the game is a draw.

Expected effect: Kept-card colours become the hidden state. Players track the lot list to work out whether a rival's secret 4 went to Red or Blue, and bid and shift worths accordingly. Because sellers pocket the gold, a lot in an unwanted colour can be sold dear, which offsets deal luck and makes keeping versus selling the 4 a real choice. Equal bids hand the card to the seller, so passive bidding is punished, while overbidding enriches a rival. Talk earns its place because interests conflict. The seller wants the bidders to escalate. Each bidder wants the card cheaply and wants the other to overpay. Everyone disagrees about which colour's worth should move. A player who believes a seller's claim, such as 'I kept Blue, I won't contest Red', or a bidder's bluff, such as 'I'm all-in on this one', can overpay, push up a rival's colour, or concede a majority that the claim's maker was secretly building. Following a proposal can lose.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
