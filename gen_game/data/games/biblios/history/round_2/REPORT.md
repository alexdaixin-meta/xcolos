# biblios: needs review

Built from the variation **Biblios: Sealed Scriptorium (revised)** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- The original is reduced to a 36-card deck, abstract gold, one sealed bid per round, and the active player's keep-one-of-two choice standing in for the gift split. This is retained from the previous variation. (fixes: The original's deck, payment-by-cards, theft and open-outcry auctions exceed platform complexity, and its many random steps let luck swamp skill.): It keeps the gift-and-auction identity within the step limits, with one shuffle at setup.
- A kept Church card no longer changes worths during play. Its owner records a secret colour and direction in their hidden collection, applied only at scoring. Worths shown during play exclude these secret adjustments. Nothing is announced when a kept Church card is used. (fixes: The previous variation contradicted itself. Step 4 hid whether the kept card was a Church card, but step 9 announced 'a hidden Church card was used', which reveals both the card type and the user, since only the active player keeps a card.): This keeps secrecy without contradiction, and makes reading which colour a rival secretly boosted part of the inference.
- Every round the active player always gives a secret mark (a colour and +1 or -1), whatever they kept. The mark counts only if the kept card was a Church card. (fixes: A hidden Church choice that only some players are asked to make would itself leak information: being asked reveals that the kept card is a Church card.): Being asked never reveals anything, because everyone sees the active player asked every round.
- A won Church card is used at once in public (the winner names a colour and a direction, applied immediately) and is then discarded face-up. It never enters any collection. (fixes: The previous variation never said where a won Church card goes after it is used.): It gives the card a stated destination.
- During play only the public adjustment from a won Church card changes a worth, so at most one public adjustment happens per round. At scoring, the secret marks that count are applied one at a time in round order, starting from the final public worths. Each mark is checked against the limit using the worth as already changed by earlier marks; a mark that would take a worth below 2 or above 8 has no effect. (fixes: The previous variation called two Church adjustments simultaneous yet ordered, without saying whether the 2-8 limit is checked before or after the first adjustment.): This gives an exact, ordered clamping rule. For example, worth 7 with two +1 marks becomes 8, then the second mark has no effect.

Objective: The player with the most VP after scoring wins. If two or more players tie for the most VP, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. ECONOMY. Each player has 8 gold plus 12 income, so 20 gold. Kept as gold, that is 4 VP, a rate of 0.2 VP per gold, paid only in full blocks of 5. Each colour holds value 1+1+2+2+3+4 = 13, and its worth starts at 4 (range 2 to 8). The colour pool is therefore about 20 VP of majorities, against about 
- playable: pass. The rules cover every case:
- the deck and its composition;
- the hidden and public collections;
- the private A/B view and choice;
- the public lot;
- simultaneous talk;
- sealed bids from 0 up to the gold held;
- an explicit tie rule (tied high bid: nobody pays, lot discarded) and an explicit 0-bi
- reasoning_over_luck: pass. SOURCES OF CHANCE:
- the deck order decides which 24 cards appear;
- the 12 unseen cards make the totals uncertain;
- the number of Churches drawn while active varies (about 4 of the 6 appear in expectation).

The active player always picks the better of 2 cards, which softens bad draws.

SOURCES OF

## Complexity

- steps_per_round: designed 12, built 21, limit 20
- choice_steps_per_round: designed 4, built 5, limit 4
- attributes: designed 18, built 65, limit 20 (built: 80)
- hidden_elements: designed 2, built 15, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: deck holds 36 cards
- pass: Setup: 8 gold each and all worths 4
- pass: Game ends after round 12
- pass: Round 7 active seat is 3
- pass: Round 9 active seat is 1
- pass: Round 1 starts with seat 1 active and public state as set up
- pass: Top two cards leave the deck; Keep A makes card B the lot
- pass: Keep B puts card B in hidden collection and card A up as lot
- pass: Kept card stays out of public collection
- pass: Talk step does not block the round
- pass: All bid up to own gold, active player too
- pass: Sole highest bid wins and pays
- pass: Tied top bid: nobody pays, lot discarded
- pass: All bid 0: nobody wins, lot discarded
- pass: Won colour lot joins winner's public collection
- pass: Active player makes a secret mark; others are not asked
- pass: Mark counts when Church was kept
- pass: Mark is void when a colour card was kept
- pass: Church winner raises a public worth
- pass: Worth cannot exceed 8
- pass: Worth cannot go below 2
- pass: Won Church card is discarded
- pass: Unwon Church lot changes no worth
- pass: Active player winning Church answers both mark and Church
- pass: Secret mark changes no public worth
- pass: Every player gains 1 gold per round
- pass: Counting mark beyond 8 has no effect at scoring
- pass: Totals add hidden and public cards; Church counts 0
- pass: Strict majority scores full final worth
- pass: Tied majority each scores half worth rounded down
- pass: Colours nobody holds score nothing
- pass: 1 VP per full 5 gold at scoring
- pass: Most VP after round 12 wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seats 1 and 2': 2, 'seat 3': 5, 'seat 1': 6, 'seat 2': 6, 'seats 1 and 3': 1}, 96-99 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 97.0 decisions, prompts of 197 characters on average (longest 263)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 1 and 2': 3, 'seat 3': 13, 'seat 1': 14, 'seat 2': 27, 'seats 1 and 3': 2, 'seats 2 and 3': 1}
- always `first@seat1`: won 12, lost 45, drew 3
- always `first@seat2`: won 8, lost 47, drew 5
- always `last@seat1`: won 16, lost 38, drew 6
- always `last@seat2`: won 20, lost 37, drew 3

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are buildable on this platform. The attempts fail on two file-level bookkeeping problems, and the coder keeps fixing one while bringing back the other: talk/auction_colour fields shown blank, and a static `lot_list` attribute that no step ever changes.
- round 1: fix_tests: The failing test checks the length of `lot_list`. That attribute is not in the interface: it is the coder's own scratch value, emptied while shuffling the lots into `lots`, which holds the 11 lots not yet used after round 1 was dealt. Everything the interface does define came out as the rules say: seat 1 kept B1, G4 went to auction, both bids were 0, the auction card went back to seat 1, all gold stayed at 12 and the worths stayed at 3.
- round 1: revise_rules: The game behaves as specified, yet a thoughtless policy dominates. Always taking the first option (keep the first card, bid 0) wins about 80-85% of matches, and always taking the last option (bid all your gold) almost always loses. Bidding is a losing proposition: the winner's gold goes straight to a rival, gold converts directly to VP, and tied or zero bids hand the card to the seller for free.
- round 2: revise_rules: The game was built correctly and behaves as specified, but the design itself breaks the evaluation limits: 21 steps and 5 choice steps per round, against limits of 20 and 4. It is also unbalanced, with seat 2 winning about twice as often as seat 1 or seat 3 against random play.

## Choices the rules did not make

- Exactly 3 players (min 3, max 3, suggested 3): The designer fixed the table at 3, and the active-seat schedule (1,2,3,1,2,3,3,2,1,3,2,1) is written for three seats. Three is also the smallest table where a sealed-bid tie can void a lot and a majority can be split. A thoughtful player bluffs about the kept card, reads the others' bids and Church choices, and spends gold only where a majority can still be won.
- Keep the simultaneous talk step as a poll broadcast to all: The source requires it. It earns its place because players disagree about which colours should rise, and they can bluff about kept cards or try to steer bids.
- Cards are named as text '<Colour> <value>' and 'Church'; the top of the deck is index 0 after the single setup shuffle: The source gives no card labels, and it needs a fixed hidden order with a top card.
- Card values per colour are given as counts per value in parameters (two 1s, two 2s, one 3, one 4): Every parameter must be a number.
- Marks are stored as 'round:colour:direction:counts', with counts fixed when the mark is made: This lets scoring apply only the counting marks, in round order, by arithmetic, without working out again which card was kept each round.
- Per-colour totals and final worths are explicit attributes computed at scoring: The majority rule needs these numbers stored as state so they can be compared across players.
- The active player's choice of A or B is an ask to that seat alone: Only one player answers, and the answer is private.

## Simplifications

- Scoring runs as conditional steps (when round == 12) at the end of round 12 rather than as a separate phase: The step list is flat, so final scoring is gated by an arithmetic condition.
- A tie for most VP is shown as a shared win rather than a 'draw': The engine has no separate draw; players level at the top share the win, which is the same outcome in effect.
- Parts (a) and (b) of step 9 are one poll addressed to the active seat and, when it applies, the Church winner: The source says they are answered at the same time; a seat that is both gets both questions in the same poll.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {offer_a} (in `prompt`: 'Card A is {offer_a}, Card B is {offer_b}. Keep one secretly in your hidden collection; the'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {offer_a} (in `prompt`: 'Card A is {offer_a}, Card B is {offer_b}. Keep one secretly in your hidden collection; the'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {offer_a} (in `prompt`: 'Card A is {offer_a}, Card B is {offer_b}. Keep one secretly in your hidden collection; the'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (kept_card, message, offer_a, offer_b) in `your_start`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `worth_blue` is never changed in 3 random matches, so nothing updates it. Steps that name it: the table, apply church. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `worth_yellow` is never changed in 3 random matches, so nothing updates it. Steps that name it: the table, apply church. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `final_worth_yellow` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and final worths, apply one mark. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
