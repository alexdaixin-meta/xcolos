# Variation: Nyet! Contract Veto

Three players, six deals. Each deal one player is the Lone. The other two secretly veto colours, and the Lone picks trump, the first leader and a public exact-tricks contract. The Pair then tries to make the Lone miss while competing with each other for tricks.

Players: 3 to 3, best with 3

## Review of the original

Nyet! is a trick-taking game for 2 to 5 players. Each round, players take turns vetoing options on a five-line board (starting player, discard rule, trump, supertrump, points per trick) until one option per line remains. Shifting teams then play tricks, and the most points after 8 to 10 rounds wins. The previous variation cut it to three players: one Lone against a Pair, with a three-way colour veto and a 20-card deck.

- **non_degenerate**: weak. No simple policy wins outright, and the seats are rotated through the Lone role equally. However, Pair tricks pay both Pair members the same 1 point, so the 24 Pair tricks never separate those two players. The ranking reduces to Lone tricks, and the Lone's choices have little room to change those.
- **skill_sensitive**: bad. The winner is whoever took the most tricks across their two Lone deals: 12 tricks from two random 6-card hands. A Lone holding 0 or 1 trump and no high cards takes 0 or 1 tricks however well it plays. A Lone holding 3 or more trumps including the 5 takes 3 to 5. The estimated chance share of the result is 60 to 70%.
- **headroom**: weak. Card counting and lead choice exist, but with 6-card hands and forced follow-suit there are few real decisions per deal. Good play adds little beyond the deal.
- **reasoning_dependent**: weak. Hands are hidden, which is good. But trump is the first unbanned colour in a fixed order, and the Lone controls only one ban of three, so inferring the others' bans barely matters. With 18 of 20 cards seen by the end of a deal, inference is shallow.
- **verifiable**: good. Trick winners and scores follow from the cards by fixed rules. No judge is needed.
- **fits_platform**: good. It is text-only and turn-based, with 36 rounds, sequential plays, one simultaneous veto and one shuffle per deal. It is within the limits.

## Problems

- P1: Hand luck decides the game. Lone trick count from two random hands determines the winner, and well-played weak hands cannot recover.
- P2: Pair tricks pay both Pair members identically, so most of the game's tricks cannot separate two players.
- P3: The Lone has almost no control over the deal's conditions: one ban of three, and trump fixed by a priority order.
- P4: The suggested duplicate-dealing fix does not work here. The same three players would replay hands they have already watched being played, so the replays become perfect-information games.
- P5: With 6-card hands, 2 hidden cards and only trick count mattering, there is little to infer and few decisions that take thought.
- P6: The Nyet identity (vetoing options, then the chooser shaping the round) is thin. Only one line of the board survives, and it is decided mechanically.

## Changes

- The Lone makes a contract. After trump is set, the Lone publicly bids how many tricks (0 to 5) it will take. Exactly the bid scores 6 for the Lone. Missing by one scores 2 for the Lone and 1 for each Pair member. Missing by two or more scores 3 for each Pair member. Every trick won also scores 1 to its winner. (fixes: P1): A weak hand can bid low and succeed, and a strong hand can bid high. Success depends on judging the hand, controlling the play and reading the Pair, not on holding high cards. The main prize, 6, is the same for every hand. A Pair member's goal changes from 'win tricks' to 'make the Lone miss', which can mean pushing tricks onto a Lone that bid low.
- Each trick scores 1 point to the individual player who won it, including Pair members. (fixes: P2): Pair members are now rivals as well as allies. Each wants the Lone to miss, but each would rather take the tricks personally, so tricks separate them.
- Veto in the Nyet style. The two Pair members each secretly ban one colour. The Lone then chooses trump from the unbanned colours (2 or 3 remain), chooses who leads the first trick, and states the bid, all as one choice. (fixes: P3): The Lone can shape the deal to fit the hand: choose a void colour as trump to bid 0, or a long colour to bid high. Pair members must infer the Lone's likely strength from their own holdings before banning. The two choices restore two of Nyet's board lines, trump and first player.
- Drop duplicate dealing. Use fresh random deals, with the contract scoring and Lone control above absorbing hand luck instead. (fixes: P4): Replaying known hands between the same players removes the hidden information that the game depends on.
- Deal 5 cards to each player and leave 5 face down in the Widow (previously 6 cards each and a 2-card Widow). Each deal is one setup round plus 5 trick rounds, 6 deals in total, 36 rounds. (fixes: P5): A quarter of the deck stays unknown, so card counting becomes probabilistic and the Lone's bid is a real estimate. Separate setup rounds keep every round within 4 choice steps.
- Add one simultaneous public message per player in the setup round, before the bans. (fixes: P6): The Lone can bluff about its strong colour to steer the bans. Pair members can propose a split of bans, but they compete for tricks and for the win, so a proposal can be self-serving.

## Kept from the original

- Shifting teams: a different player stands alone each deal against a temporary Pair.
- Veto first, then the remaining options become the rules of the deal, with first player and trump decided this way.
- Four colours numbered 1 to 5, follow suit, and the highest trump wins the trick.
- Points per trick, and the highest total after a fixed number of deals wins.

## The variation's rules

SETUP. The deck has 20 cards in four colours (Red, Blue, Green, Yellow), each numbered 1 to 5. Seats are 1, 2 and 3. Clockwise means 1 to 2, 2 to 3, and 3 to 1. All scores start at 0. The game has 6 deals. Each deal is 6 rounds: one setup round, then 5 trick rounds. That makes 36 rounds in total.

SETUP ROUND (first round of each deal).
1. Shuffle the deck. Deal 5 cards to each player, each hand seen only by its owner. The remaining 5 cards form the Widow, face down, seen by nobody until the game ends.
2. The Lone is seat 1 in deals 1 and 4, seat 2 in deals 2 and 5, and seat 3 in deals 3 and 6. The other two players are the Pair. This is announced.
3. TALK. All three players write one short message at the same moment, without seeing the others. All messages are then shown to everyone. Messages bind nobody.
4. VETO. The two Pair members at the same moment each name one colour to ban. Both bans are then announced. If both ban the same colour, three colours remain unbanned. Otherwise two remain.
5. CONTRACT. The Lone chooses three things in one decision and announces them:
   (a) trump, which must be one of the unbanned colours;
   (b) the first leader, which may be any of the three seats;
   (c) the bid, a whole number from 0 to 5: the exact number of tricks the Lone promises to win this deal.

TRICK ROUNDS (rounds 2 to 6 of each deal, one trick each).
6. The leader plays one card face up. On the first trick, the leader is the player the Lone named. On later tricks, the leader is the winner of the previous trick. The led card's colour is the led colour.
7. The next player clockwise plays one card, then the remaining player plays one card. A player holding a card of the led colour must play one. A player holding none may play any card.
8. The trick winner is the player of the highest-numbered trump, if any trump was played. Otherwise, it is the player of the highest-numbered card of the led colour. There are no ties.
9. The trick winner gains 1 point, whether they are the Lone or a Pair member. The number of tricks the Lone has won this deal is tracked. The winner, the scores and the Lone's trick count are announced.
10. CONTRACT SCORING (after the 5th trick of the deal). Compare the Lone's tricks T with the bid B:
   - If T equals B, the Lone gains 6.
   - If T and B differ by exactly 1, the Lone gains 2 and each Pair member gains 1.
   - If T and B differ by 2 or more, each Pair member gains 3.
   The result is announced.
11. After deal 6 is scored, the game ends.

Objective: After 36 rounds (6 deals), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.

Expected effect: Hand strength no longer decides the game. Every hand can make some contract, and the 6-point prize is the same at any bid. Skill now lies in choosing a trump and first leader that make the hand predictable, bidding accurately with 5 unseen Widow cards, steering tricks toward or away from the Lone, and reading the Pair's bans for clues about their hands. Lone hand luck is estimated at about 30 to 40% of the result, down from 60 to 70%. The players disagree about several things. Pair members both want the Lone to miss, but each wants the other to give up tricks. The Lone wants the Pair to ban the wrong colours and may bluff in talk to cause that. A Pair member who just follows a partner's ban proposal can be left banning a colour that helps the partner's own hand, while losing tricks to that partner. Simple policies can all lose. Always bidding 0 can be broken by a Pair that pushes tricks onto the Lone. Always bidding high fails with weak hands. Always banning the same colour lets the Lone plan around it. Banning only blocks the Lone's trump choice, and always leading the highest card wastes control of the play.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
