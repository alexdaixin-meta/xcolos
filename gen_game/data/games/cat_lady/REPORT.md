# cat_lady: ready for review

Built from the variation **Cat Lady: Secret Favourites (Balanced)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- The 4-player game becomes 8 rounds of 5 lots of 2 cards (80 of the 96 cards are dealt; the bottom 16 are never used). The first picker still rotates by seat each round. (fixes: P1): Every seat now picks first twice, second twice, third twice and last twice, so the move-order edge disappears. The 3-player game stays at 12 rounds of 4 lots, already symmetric at 4 of each position.
- The Cats Favourite becomes +2 per fed cat, capped at +10. (fixes: P2): This removes the top end of the strongest Favourite: realistic value about +8-10.
- The Catnip Favourite becomes +2 per Catnip card owned (including any beyond 6), capped at +12. (fixes: P2): This raises the weakest Favourite. Catnip is heavily contested, and a holder typically gets 4-5 cards, so it is worth about +8-10.
- The Strays Favourite (4 players only) becomes +3 per Stray Cat. The Toys Favourite stays at +1 per Toy card. (fixes: P2, P3): With about 6-7 Strays dealt across 8 rounds, a holder gets about 3, worth about +9. Toys is already about +8-10. All four Favourites now sit near +8-10, so the deal changes what to draft, not who leads.
- No discussion phase is added. (fixes: P2): Picks are sequential and public, so Favourites are already inferred from behaviour. Talk would add only cheap claims that cannot be checked, and no plan players could share, because every player competes for one win. It also costs steps.

Objective: The highest final total wins. If players are tied, the tied player with the most fed cats wins. If they are still tied, those players draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Value per card for a 3-player game (24 cards each):

| Card or combo | Base value | With matching Favourite |
|---|---|---|
| Cat + Food-2 (2 cards) | 5 (2.5/card) | 7 (3.5/card), Cats Favourite capped at +10 (5 fed cats) |
| Cat + Food-1 + Food-1 (3 cards) | 5 (1.67/card) | 7 (2.33/card) |
| Unfed 
- playable: pass. Card counts are exact. With 3 players, 12 rounds × 4 lots × 2 cards = 96, the whole deck. With 4 players, 8 × 5 × 2 = 80, leaving the stated 16 unused.

The rules cover every situation:
- Each pick is from the remaining lots and is sequential and visible, so the order is the point and turns are corr
- reasoning_over_luck: pass. Chance comes from the market deal and the random Favourite assignment. All players draft from the same public market, and picking positions are equalised by rotation, so a bad deal hits everyone. Favourite strengths are roughly comparable (estimated specialist totals of about 33 to 50 before the res

## Complexity

- steps_per_round: designed 12, built 13, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 15, built 64, limit 20 (built: 80)
- hidden_elements: designed 1, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Deck holds 96 cards right after setup
- pass: 3 players: favourites never include strays, so all-zero tables with 2 strays each score 6 apiece
- pass: Favourite not revealed at setup
- pass: Favourite copied to favourite_revealed at final scoring
- pass: 4 players: round 8 is the last, so final scoring runs
- pass: 3 players: round 8 is not the last, so no scoring yet
- pass: Round 2 with 3 players: seat 2 picks first, then seat 3, then seat 1
- pass: 3 players: 4 lots of 2 are dealt, so 8 cards leave the deck
- pass: 4 players: 5 lots of 2 are dealt, so 10 cards leave the deck
- pass: First picker sees every lot before picking
- pass: A lot already taken is not offered again
- pass: Each food2 adds 2 food (all lots are food2)
- pass: Each food1 adds 1 food (all lots are food1)
- pass: Each cat adds 1 cat (all lots are cats)
- pass: Leftover lot goes to discard
- pass: 4 players: 16 cards remain unused after 8 rounds
- pass: 3 players: deck exactly used up after 12 rounds
- pass: 5 cats and 7 food give 3 fed cats
- pass: 5 cats with 3 fed score 13 (plus 6 for strays)
- pass: Leftover food is food minus 2 per fed cat: only the largest leftover is penalised
- pass: Each stray scores 3
- pass: 3 red, 2 blue, 1 green toys score 10
- pass: 4 catnip score 10, 8 catnip score 21
- pass: All players tied for the largest leftover lose 2
- pass: No food penalty when every leftover is 0
- pass: Cats favourite: 2 per fed cat (3 fed gives 6)
- pass: Cats favourite bonus capped at 10
- pass: Toys favourite: 1 per toy card
- pass: Catnip favourite: 2 per catnip, capped at 12
- pass: Catnip favourite: 5 catnip give 10 bonus
- pass: Strays favourite (4 players): 3 per stray
- pass: Score tie broken by fed cats
- pass: Players tied on score and fed cats share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 2': 11, 'seat 3': 10, 'seat 1': 12, 'seat 4': 7}, 32-36 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 34.0 decisions, prompts of 261 characters on average (longest 285)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 27, 'seat 3': 12, 'seat 1': 21}
- always `first@seat1`: won 18, lost 41, drew 1
- always `first@seat2`: won 23, lost 36, drew 1
- always `last@seat1`: won 18, lost 42, drew 0
- always `last@seat2`: won 26, lost 34, drew 0

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer chose 4. The minimum is 3 because with 2 players there is little contest over lots and almost nothing to hide a Favourite among. The maximum is 4 because the deck and the Favourite set (four Favourites) are built for at most 4.
- No talk step before picks: The source has no negotiation. Picks are public, and the interest lies in reading others' Favourites from their picks and hate-drafting, so talk would only add words.
- Strategy at the table: A thoughtful player balances food against cats to avoid unfed cats and the food penalty, chases toy sets and catnip, and infers rivals' secret Favourites from what they take so as to deny them key lots.
- Card codes food1, food2, cat, stray, toy_red, toy_blue, toy_green, catnip: The deck needs concrete list entries for drawing and counting.
- rank_by = score * 100 + fed_cats: fed_cats is at most 20 (below 100), so this ranks by score first and fed cats second, and remaining ties share the win as the source's draw.

## Simplifications

- Dealing the market from the top of the deck is done as random draws from the deck list: The deck is shuffled once, so drawing at random is equivalent.
- The Favourite is revealed by copying it to a public attribute favourite_revealed at final scoring: Visibility of an attribute is fixed, so revealing is done by copying the value.
- The food penalty uses a table attribute max_leftover: The engine has no direct player-to-player comparison; the maximum is kept on the table and each player is compared to it.
- Final scoring runs as conditional updates in the last round: The step list is flat, so the scoring steps carry a 'when round == num_rounds' condition.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (favourite_revealed, favourite_revealed, favourite_revealed); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `lot_e` is never changed in 3 random matches, so nothing updates it. Steps that name it: deal the market, discard the leftover lot. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
