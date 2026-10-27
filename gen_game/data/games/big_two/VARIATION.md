# Variation: Big Two: Balanced Climb

Three players play three hands of a suitless climbing game. Everyone holds one card of each value plus two random extras, which form their two pairs. Tricks are one pass of three turns and each trick won is worth a point. Players infer the hidden extras to decide when to spend their high cards.

Players: 3 to 3, best with 3

## Review of the original

Big Two is a shedding card game. Players play singles, pairs, triples or poker hands that must top the last play, and the first to empty their hand wins. The previous XColos variation cut it to a 3-player, 40-card, suitless climbing game over three 12-round hands, with one circuit per trick and lowest total penalty winning.

- **non_degenerate**: weak. Thoughtless policies do lose: always-pass keeps 12 cards and always-highest wastes 10s. But one near-mechanical policy does about as well as anything: lead the lowest pair, beat with the lowest legal card, keep 10s to top on turn 4 as leader, never bomb. The leader acts first and last in each trick, so the trick winner tends to keep the lead.
- **skill_sensitive**: bad. Testing put chance at about 50-60% of the result. The number of pairs in 12 random cards ranges from about 2 to 6, and holding two or more 10s swings 6-10 penalty per hand. The gap between a skilled and a greedy player with equal cards is only 2-4.
- **headroom**: weak. A weak player still scores. A strong one has little to improve, because each card shed is worth exactly 1 at any time and responses are nearly forced, so holding back rarely pays.
- **reasoning_dependent**: weak. Opponents' hands are hidden, but card counting gives little to act on. An opponent's best move hardly depends on yours, so opponent modelling barely matters.
- **verifiable**: good. Penalties are pure arithmetic on cards left, bomb costs and going-out bonuses.
- **fits_platform**: good. Text-only and turn-based, with 16 steps, 3 choices per round and 36 rounds, all inside the limits.

## Problems

- P1 Deal luck dominates: a fully random 12-card deal gives anywhere from about 2 to 6 pairs and 0 to 3 10s, which decides about a third of games.
- P2 No hold-versus-shed tension: every card is worth exactly -1 whenever it is shed, so play is near-mechanical.
- P3 Leader snowball: the leader acts first AND last in each trick and keeps the lead cheaply by topping on turn 4.
- P4 Little to infer: hidden holdings are wide but uninformative, and nothing makes a good guess about an opponent's cards change the best move.
- P5 Duplicate dealing, as suggested, would leak information: in hand 2 you remember your hand-1 holding, now sitting with the next seat, so you would know nearly every card. So the luck fix has to come from somewhere else.

## Changes

- Balanced deal: every player always receives one card of each value 1-10. Only the 10 'extra' cards (one of each value) are shuffled: 2 go to each player and 4 are set aside. Every hand therefore has exactly two pairs (at the two extra values) and eight unpaired cards, and at least one 10. (fixes: P1 Deal luck dominates): Hand strength now differs only in WHICH two values are paired, not in how many pairs or 10s a player has, so deal luck shrinks sharply without repeating deals.
- Reject duplicate dealing; reshuffle only the extras each hand. (fixes: P5 Duplicate dealing would leak information): Duplicate dealing would turn hands 2 and 3 into near-perfect information. The balanced deal cuts luck without that leak.
- The trick winner subtracts 1 from their penalty. (fixes: P2 No hold-versus-shed tension): High cards now have two uses that compete. You can spend them to win tricks (worth 1 point plus the lead) or keep them for later contests, while a 10 still held at the end costs 2.
- Each trick is a single pass of three turns (leader, next seat, third seat). The leader no longer acts again at the end. (fixes: P3 Leader snowball): Leading now guarantees one card shed but means acting first, while the last responder has the edge in the contest. This removes the cheap lead retention.
- At each deal, seats 1, 2 and 3 each privately see one different aside card. The fourth aside card is seen by nobody. (fixes: P4 Little to infer): Every player knows 3 of the 10 extras and must infer where the other 7 are (4 with opponents, 3 aside). Whether a pair can be topped, or whether an opponent still holds a second 10, becomes a real deduction from plays and passes.
- Remove triples and bombs. They are impossible anyway, because no value appears more than twice in a hand. (fixes: P2 No hold-versus-shed tension): Simplifies the rules and frees steps; the pair is now the rare, strong shape.
- Use 13 rounds per hand and 39 rounds in total. (fixes: P2 No hold-versus-shed tension): Gives room to shed all 12 cards, so going out remains possible but only for a player who wins the lead often enough to dump unpaired low cards.

## Kept from the original

- Climbing and shedding: each play must strictly beat the last play of the same shape, or you pass.
- The trick winner leads next, with a free choice of shape.
- Penalty for cards left in hand, doubled for holding the top rank (the analogue of holding 2s in Big Two).
- A bonus for going out first.
- Singles and pairs as the core shapes, and high cards as the scarce resource.

## The variation's rules

DECK: 40 cards, four copies of each value 1 to 10. There are no suits. 10 is highest and 1 is lowest.

SEATS: Seats 1, 2 and 3. Turn order is 1, then 2, then 3, then back to 1.

STRUCTURE: Exactly 39 rounds in three hands of 13 rounds: hand 1 is rounds 1-13, hand 2 is rounds 14-26 and hand 3 is rounds 27-39. If a hand ends early, its remaining rounds are void: nobody is asked anything and nothing changes. The next hand still starts exactly at round 14 or 27. Penalties carry over between hands; everyone starts at 0.

DEAL (rounds 1, 14 and 27): Collect all 40 cards. Give each player one card of every value 1 to 10 (30 cards in all). The remaining 10 cards, one of each value, are the EXTRAS. Shuffle the extras. Deal 2 to each player privately and place the other 4 face down as aside cards A1, A2, A3 and A4. Seat 1 privately sees A1, seat 2 privately sees A2 and seat 3 privately sees A3. Nobody sees A4. Each player now holds 12 cards: their two extra values form pairs and the other eight values are held once. The first leader is seat 1 in hand 1, seat 2 in hand 2 and seat 3 in hand 3.

INFORMATION: Each player sees their own hand and their one aside card. Everyone sees every play and pass, the discard pile, each player's card count and all penalties.

PLAYS: A play is a single (one card) or a pair (two cards of the same value), valued at the card's value. A player holding a pair may play just one card of it as a single. A single is beaten only by a strictly higher single, and a pair only by a strictly higher pair.

TRICK (one per round while the hand is active): The current play starts empty.
- Turn 1: the leader must play any single or pair.
- Turn 2: the next seat in turn order either plays something that beats the current play, or passes.
- Turn 3: the third seat either beats the current play or passes.
A player with no cards passes automatically. Played cards go face up to the discard pile. The owner of the current play after turn 3 wins the trick: they subtract 1 from their penalty and lead the next round.

OPTION ORDER: When leading, the options are all legal leads in ascending value, with the single listed before the pair at the same value. When responding, the options are all legal beats in ascending value, then Pass last.

END OF HAND: A hand ends at the end of the first round in which any player holds no cards, or at the end of round 13, 26 or 39, whichever comes first. Each player then adds 1 to their penalty for each card left in hand, plus 1 more for each 10 left. Each player holding no cards subtracts 3. Penalties may go below zero.

ROUND STEPS:
1. On a deal round, shuffle the extras.
2. On a deal round, deal base cards, extras and aside cards.
3. On a deal round, privately show A1, A2 and A3 to seats 1, 2 and 3.
4. On a deal round, mark the hand active and set the leader.
5. If the hand is active, clear the current play.
6. The leader chooses a lead.
7. Remove the led cards and set the current play's value, shape and owner.
8. The second seat chooses to beat or pass.
9. If they beat, resolve the play as in step 7.
10. The third seat chooses to beat or pass.
11. If they beat, resolve the play as in step 7.
12. The owner subtracts 1 from their penalty and becomes the leader.
13. If any player has 0 cards, or this is round 13, 26 or 39, mark the hand ending.
14. If the hand is ending, score seat 1.
15. If the hand is ending, score seat 2.
16. If the hand is ending, score seat 3 and mark the hand inactive.

The engine stores each score as the negative of the penalty.

Objective: After round 39, the player with the lowest total penalty (highest score) wins. Total penalty is the sum of cards-left penalties, minus 1 per trick won, minus 3 for each hand in which the player went out. If two or three players tie for lowest, the game is a draw.

Expected effect: Every hand holds the same eight unpaired values plus two pairs, so results turn on timing and inference rather than the deal. Key decisions:
- When to spend your 10 (or second 10) to take a trick worth 1 point plus the lead.
- When to lead a pair, which can only be topped by a higher pair that may sit in an opponent's hand or among the aside cards.
- Whether to break a pair.
- How to dump unpaired low cards, which only shed when you lead.
The aside peeks and the record of plays and passes let a strong player locate the 7 unknown extras. Leading means acting first, so lead retention is no longer automatic. Some luck remains in which values are paired; a pair of 10s is worth roughly 1-3 points per hand, and three hands average this out. Talk is left out. All three compete for a single win, so promises could not bind, and talk would mostly be cheap claims about holdings that replace the card-counting inference the game is built on.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 39 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
