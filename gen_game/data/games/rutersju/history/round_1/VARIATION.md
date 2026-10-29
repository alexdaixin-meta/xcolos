# Variation: Rutersju Twelve

3 or 4 players play 12 deals of three-card Rutersju. In each deal the highest bidder declares an exact trick count and plays alone against the rest, who try to push the declarer off the count. The highest total after 12 deals wins.

Players: 3 to 4, best with 4

## Review of the original

Rutersju is a Scandinavian trick-taking game for 3 to 12 players. Each player gets three cards from a 36-card pack and bids the exact number of tricks they will take. The highest bidder plays alone as declarer against everyone else, and the diamond 7 is a super-trump that wins any trick it is in. The declarer scores the bid if it is made exactly; otherwise every opponent scores one point per trick of miss.

- **non_degenerate**: weak. The policies are not trivially dominant. Always bidding 3 makes you declarer often but rarely exact, and each miss feeds every opponent. Always bidding 0 rarely makes you declarer. There are seat problems, though. Ties go to the last tied bidder, and no rotation is stated, so a fixed last seat wins every tie. A made 0-bid scores 0, so when everyone bids 0 the contract is worthless to the declarer. With 12 players only 36 cards exist, so the whole pack is dealt and the diamond 7 is always in play. At 3 players it is in play only a quarter of the time.
- **skill_sensitive**: weak. Three-card hands make a single deal close to a lottery: whoever holds the diamond 7 or a long suit of honours decides it. The rules state no number of deals, so luck is never averaged out. Over many deals, careful bidding and defending do matter.
- **headroom**: good. Exact bidding means a weak hand can still win a 0 or 1 contract. Defenders must cooperate silently to push the declarer off the exact count, either by feeding tricks or by stealing them. A strong player keeps finding better ways to read the bids and use the leads.
- **reasoning_dependent**: good. Hands are hidden. Bids, made in turn, signal hand strength. Card play reveals more information trick by trick. The defenders must infer one another's holdings without talking, and the declarer must plan three tricks ahead to land exactly on the count.
- **verifiable**: good. Trick winners follow from rank and suit. Scores are bid or bid difference, all arithmetic.
- **fits_platform**: weak. The game is turn-based text with hidden hands, which the platform supports. However, it has no fixed length or winner rule. The 12-player version makes rounds long. A trick's turn order changes with the trick winner, which needs explicit handling.

## Problems

- No number of deals and no winner rule: a single 3-card deal is mostly luck, and the game never ends by arithmetic.
- The tie rule (last tied bidder wins) hands a permanent edge to a fixed seat unless the bidding order rotates, and no rotation is stated.
- A declarer who makes a 0 bid scores 0, so a 0 contract is worthless. When everyone bids 0, the last bidder is forced into a pointless contract.
- Player counts up to 12 make rounds too long and exhaust the deck, which changes the game's character by player count.
- Talk among the defenders would let them announce their cards (for example 'I hold the diamond 7'), which would remove the hidden-hand inference that drives the defence.

## Changes

- Play exactly 12 deals. The highest total after 12 deals wins; a tie for the top is a draw. (fixes: No number of deals and no winner rule: a single 3-card deal is mostly luck, and the game never ends by arithmetic.): Gives the game an arithmetic end and averages hand luck over many deals, so bidding and defending skill decide the result.
- The first bidder rotates one seat clockwise each deal. 12 deals divides evenly by 3 and by 4, so every seat bids first, and last, equally often. (fixes: The tie rule (last tied bidder wins) hands a permanent edge to a fixed seat unless the bidding order rotates, and no rotation is stated.): The tie-goes-to-last advantage is shared equally among all seats.
- A declarer who takes exactly the bid scores the bid plus 1. Failure is unchanged: each opponent scores the number of tricks of difference. (fixes: A declarer who makes a 0 bid scores 0, so a 0 contract is worthless. When everyone bids 0, the last bidder is forced into a pointless contract.): A 0 contract is now worth 1 point, so every contract has value. Failure still feeds every opponent, so a reckless high bid is punished.
- Limit the game to 3 or 4 players. Keep the 36-card pack, so 9 or 12 cards are dealt and the rest stay unseen. (fixes: Player counts up to 12 make rounds too long and exhaust the deck, which changes the game's character by player count.): Keeps each round short and inside the step limits. Leaves undealt cards, so nobody knows whether the diamond 7 is in play, which keeps inference alive.
- No discussion phase. The only signals are bids and cards played. (fixes: Talk among the defenders would let them announce their cards (for example 'I hold the diamond 7'), which would remove the hidden-hand inference that drives the defence.): The defenders share an interest only against the declarer. Talk would let them reveal their hands outright, and the game's reasoning is inferring hands from bids and play.

## Kept from the original

- 36-card French pack, three-card hands, three tricks per deal
- The diamond 7 as the unbeatable card
- Bids from 0 to 3 for an exact number of tricks, made in turn, with ties going to the last tied bidder
- One declarer who leads first and plays alone against all the others
- Must follow suit; the highest card of the led suit wins
- Exact-or-fail scoring, with failure paying every opponent the size of the miss

## The variation's rules

CARDS. Use a 36-card pack with four suits (spades, hearts, diamonds, clubs). Each suit has the ranks A, K, Q, J, 10, 9, 8, 7, 6, from high to low. The diamond 7 is special: it wins any trick it is played to. Otherwise it is a diamond.

SEATS. Players sit in a fixed clockwise order, and every player starts at 0 points. The game lasts exactly 12 deals. In deal 1, seat 1 bids first. In each later deal, the first bidder is the next seat clockwise from the previous deal's first bidder.

EACH DEAL.
1. Deal. Shuffle all 36 cards and deal 3 cards face down to each player. Each player sees only their own hand. The remaining cards stay unseen for the whole deal.
2. Bid. Starting with the first bidder and going clockwise, each player in turn announces a bid of 0, 1, 2 or 3. All bids are public as soon as they are made. Every player must bid; there is no passing.
3. Declarer. The player with the highest bid becomes the declarer. If several players tie for the highest bid, the one of them who bid last becomes the declarer. The declarer's bid is the contract. All other players are opponents for this deal.
4. Play three tricks. The declarer leads the first trick. In each trick, the leader plays one card face up. Then each other player in clockwise order plays one card face up. A player who holds a card of the led suit must play a card of that suit. A player with none may play any card. If the diamond 7 is in the trick, its player wins the trick. Otherwise the highest card of the led suit wins. Each player's tricks are counted separately. The winner of a trick leads the next one. All played cards stay visible to everyone.
5. Score. Count the declarer's tricks.
   - If the declarer took exactly the contract, the declarer scores the contract plus 1 point. A contract of 0 made scores 1; a contract of 3 made scores 4.
   - If the declarer took more or fewer tricks than the contract, every opponent scores points equal to the difference between the contract and the declarer's tricks. The declarer scores nothing.
   - Opponents' own tricks are never scored.
6. Announce. Announce every player's total. Then start the next deal.

There is no discussion at any time. Players communicate only through their bids and the cards they play.

END. After the 12th deal is scored, the game ends.

Objective: After 12 deals, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

Expected effect: Bidding becomes a contest of reading hands. A high bid wins the declarer seat, but a miss pays every rival. A bid also reveals strength, which the defenders use against you. The defenders must silently coordinate to make the declarer miss, by feeding unwanted tricks or taking needed ones, while still competing among themselves for the top total. Rotating the first bidder removes the seat edge. Twelve deals average out the luck of the diamond 7. The bid-plus-1 reward makes even a weak hand worth declaring at 0 or 1. Simple policies lose: always bidding 3 hands every opponent points almost every deal, and always bidding 0 forfeits the declarer seat to whoever reads the table. There is no talk, because the defenders' shared interest would let them simply reveal their cards.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
