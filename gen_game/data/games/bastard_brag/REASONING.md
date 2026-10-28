# Reasoning and planning: Knock Brag (3-player)

**Verdict: adequate.** Winning rewards real inference, chiefly tracking which cards sit in which slots and counting outs, along with short-horizon planning around knock timing and card parking. Deal luck still swings many showdowns. More cards exposed through announcements, or longer deals, would deepen opponent modelling and multi-turn plans.

From 3 play(s): 148 choices, 148 with a reason given (about 69.6 words each); results {'seat 3': 1, 'seat 1': 1, 'seat 2': 1}.

## Reasoning: 3 of 3

Most decisions rest on concrete tracking of which face-down slot holds which discarded card, exact out-counts against the unseen cards, and some inference about opponents from their take-ups and repeated swaps. There are a few misreadings of opponent signals, but the bulk of the reasoning is specific and correct, matching the designer's inference contest.

- match 3, turn 38, seat 1: "From the earlier swaps, both face-down slots hold a 3. Slot D1 kept a 3 when I swapped with it, and I later put a 3 into D2." (Correctly reconstructs the hidden table from a chain of blind swaps and takes a 139 pair via whole hand, which proved decisive.)
- match 1, turn 7, seat 3: "Seat 1 took the 3 I discarded, so they likely now hold a pair of 3s." (Infers an opponent's holding from a public take-up and uses it to avoid a risky knock.)
- match 3, turn 49, seat 1: "only one 5 is unseen, so seat 2 cannot hold a pair of 5s. Any 5-5-x beats seat 2's pairs of 4s or lower" (Card-counting shows the kicker is irrelevant, so it picks the slot with prial upside.)
- match 1, turn 1, seat 1: "a 3 makes the run 2-3-4, and a 2 or 4 makes a pair. That is 10 good cards out of the 32 I cannot see." (Accurate out-counting to choose which card to discard.)

## Planning: 2 of 3

Players often park a card in a slot to recover it next turn, time their exchanges around when they will lead and can knock, and knock specifically to cut opponents' remaining actions. Plans rarely reach beyond two turns, though several depend on predicting that others will leave a slot untouched, and these were carried out.

- match 1, turn 46, seat 3: "If seat 2 doesn't disturb D1, I can swap the 9 back next turn. That includes the case where seat 2 knocks" (Hides a card for later retrieval, anticipating the opponent's knock; it executed this at turn 49.)
- match 1, turn 35, seat 2: "So I can look at the three table cards (9 plus two unknowns) and keep them if they are good, or take my run back next round." (Two-turn plan using whole-hand as a free look, relying on seat 3 not acting in between; carried out at turn 36.)
- match 1, turn 2, seat 2: "I also lead round 2, so I can knock then if this goes well." (Sets up a future knock opportunity.)
- match 2, turn 40, seat 2: "Knocking now gives them the fewest chances to beat my pair." (Times the knock to limit opponents' future improvement, weighing it against a known retrievable 7.)

## Luck: 2 of 3

Initial deals and single blind draws decided several showdowns, such as a last-action blind draw completing a run, or a 209 run losing to a dealt 1-2-3. Choices still mattered: slot tracking and knock timing repeatedly turned outcomes.

- match 2, turn 24, seat 1: "A 4 or 7 makes a run, and a 5 or 6 makes a pair." (A last-action blind draw of a 4 turned a likely loss (14) into the top hand (206).)
- match 3, turn 49, seat 1: "With 5-5-5 I must still exchange a card" (A lucky blind draw produced a prial in the deciding deal.)
- match 1, turn 12, seat 3: "turning 7-7-1 (171) into a guaranteed 7-7-4 (174)." (A solid pair still lost because both opponents happened to hold runs.)

## Weak spots

- match 1, turn 12, seat 3: Read seat 2's two D1 swaps as weakness ('Seat 2 looks weak, having swapped D1 twice') when seat 2 was retrieving its own parked card, and discounted seat 1's knock as a strength signal. No better move existed, but it misjudged that 174 was 'good enough'.
- match 2, turn 4, seat 2: Knocked with a pair of 3s (137) while on 3 lives, based on a random-hand base rate. Both opponents had just acted with hidden blind swaps and get another action, so the true risk was higher. Not knocking would have risked only 1 life, and the knock cost 2.
- match 1, turn 22, seat 2: Inferred weakness from opponents' blind swaps, but blind swaps are also how strong hands hide. It worked out, but the signal reading was shaky.
