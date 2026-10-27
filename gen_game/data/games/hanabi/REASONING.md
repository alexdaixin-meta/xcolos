# Reasoning and planning: Hanabi Trio

**Verdict: adequate.** Winning took real inference (copy counting, reading hints from what was and wasn't touched, modelling why a partner chose a hint) and multi-seat endgame planning around token flow. Each match was still won by one or two points after a blind discard or misplay removed a last copy, so requiring 14, or penalising lost fuses, would make careful protection of critical cards matter more than luck.

From 3 play(s): 103 choices, 103 with a reason given (about 62.0 words each); results {'all seats win': 3}.

## Reasoning: 3 of 3

Most decisions rest on specific, correct inference: players combine two hints to pin a face, count copies across visible hands and the discard pile to rule out colours, and read a partner's choice of hint as a play signal. The main lapses are a few risk assessments that missed which cards were critical, not a failure to reason.

- match 1, turn 23, seat 2: "Both red 3s are already accounted for: I played one, and seat 1 holds the other (#3). So my 3s must be green or blue." (Card counting turns an ambiguous rank hint into a certain play.)
- match 3, turn 20, seat 2: "the red hint on turn 6 touched only #6 and #14, so #8 is not red. ... both green 2s are accounted for. #1 was played and #11 is in seat 3's hand." (Uses negative information from an old hint plus visible cards to deduce B2 without a new hint.)
- match 1, turn 15, seat 3: "Seat 1 would hardly spend their last token marking a dead Red 1, so it is very likely Green 1" (Combines copy odds with a model of the partner's intent.)
- match 2, turn 23, seat 2: "If #6 is B4, then #21 fails 1 time in 3. ... So #21 fails only about 2/9 of the time, which makes it the safer play." (Uses conditional probability to choose between two hinted cards.)

## Planning: 3 of 3

Players repeatedly set up chains across seats: early 5-saves, hints that complete a colour run, and discards made so that a teammate can give a specific hint next turn. In the endgames these multi-turn plans, which depend on partners acting as expected, were stated and then carried out.

- match 3, turn 28, seat 1: "Hinting 4 tells them it is G4 and safe to play. After that, seat 3 will need a G hint on #9 ... One more discard will give us the token for that hint" (A plan over several turns and seats to reach 13 via G4 then G5.)
- match 1, turn 31, seat 1: "Discarding gives us a hint token, so seat 2 can tell seat 3 which card is green and seat 3 can then safely play G4." (A discard made for a partner's next hint; seat 2 hinted G and seat 3 played G4 for the win.)
- match 3, turn 1, seat 1: "The most useful move is to protect the 5s, since each colour has only one 5 ... one hint saves both" (Spends a token early to keep critical cards for later.)
- match 2, turn 24, seat 3: "The only useful cards left are R5, B5 and G4, and seat 1 holds all three. ... it gives back a token so seat 1 can be hinted." (Plans token flow so the endgame scorer can be told about the cards; carried out on turns 26 to 31.)

## Luck: 2 of 3

Blind discards and blind plays destroyed last copies in every match: G5 in matches 1 and 2, and both B4s in match 3. Each loss capped the reachable score, and two matches finished exactly at the target of 13, so chance clearly decided how much slack each team had, though reasoning still carried all three to the win.

- match 2, turn 18, seat 3: "with a 1-in-12 chance of G5" (A low-risk blind discard happened to hit the only G5, capping the score at 14.)
- match 3, turn 30, seat 3: "It is a 50/50 guess which card is G5." (The winning point came from a coin flip, though a miss could have been recovered next turn.)
- match 1, turn 27, seat 3: "Three of those five (G4, B4, B4) play right now." (A 3/5 gamble failed on G5, leaving only one point of margin.)

## Weak spots

- match 1, turn 27, seat 3: Blind-played #10 at 3/5 odds while listing G5 among its possible faces. A miss would destroy the last G5, and it did, leaving the team needing every remaining point. Discarding #25, a fresh unknown card, to regain a token was safer, since seat 1 could then hint a known playable card.
- match 3, turn 27, seat 3: Listed the unseen cards as including B4 but called the discard one that 'rarely costs anything useful'. After the turn-24 B4 discard, that B4 was the last copy and blue's only route to B5, so this was a 1-in-6 risk on a critical card. It hit and capped blue at 3.
- match 3, turn 24, seat 3: Discarded unknown #12 on the grounds that 'There are two copies of B4, so losing one is fine'. This gave up a safety margin on blue while holding B5, without noting that a second B4 loss would kill the colour.
- match 1, turn 7, seat 1: Doubted a single-card 3 hint given just as red reached 2, though the team was using exactly this play-signal convention. It spent a token re-signalling seat 2's R3 instead of trusting the convention, which left its own R3 unused until it became dead.
