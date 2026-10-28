# Variation: Mini Mariáš with Hidden Talon

A five-deal, three-player Mariáš. Each deal is freshly shuffled with a 3-card hidden talon. Players bid a contract of 40, 50 or 60 card points, the declarer picks trump, defenders may Flek, and 7 tricks are played under the original must-follow, must-head, must-trump rules.

Players: 3 to 3, best with 3

## Review of the original

Mariáš is a Czech three-player trick-taking game with a 32-card deck. One declarer, who chooses trump and takes a talon, plays 10 tricks against two defenders in partnership. Players must follow suit, head the trick and trump when void. Aces and Tens count 10 each, the last trick counts 10, and a marriage (King and Ober of one suit) is worth 20 or 40. Flek doubling, Hearts doubling and special contracts set the stakes.

- **non_degenerate**: good. In the original, no simple policy wins. Always passing never earns points as declarer and depends on others failing. Always declaring high loses badly with weak hands. The seat advantage of being eldest is offset because everyone holds that seat in turn. The previous variation kept this, but its duplicate rotation made deals 2 and 3 almost perfect information.
- **skill_sensitive**: good. Card play, counting the Aces and Tens, choosing when to declare and Flek decisions all separate strong players from weak ones. The card deal adds variance over a single deal, but over several deals the bidding lets players avoid bad hands and punish overbids.
- **headroom**: good. Inferring hidden cards from play, defenders signalling to each other, and judging contract levels against an unknown talon have a high skill ceiling. A weak player still scores by defending or by declaring a strong hand.
- **reasoning_dependent**: good. In the original, hands and the talon are hidden, so play depends on inferring card locations and the declarer's intent. In the previous variation, after deal 1 every card was public, so deals 2 and 3 had little or nothing left to infer. That is the flaw this revision fixes.
- **verifiable**: good. Trick winners, card points, whether the contract is made and the stake are all arithmetic. Only the legality of a card needs a rule check, and with the original 'always head the trick' rule that check is mechanical.
- **fits_platform**: weak. The full original is too large for the limits: 32 cards, 10 tricks, talon exchange, marriages, four special contracts and redoubles. The previous variation went over 20 steps and 20 attributes. It also had a rule gap when trump is led.

## Problems

- Rule gap when trump is led: the previous duty to beat the trick applied only 'if no trump has been played', so it was unclear whether a player must overtake in a trump-led trick.
- Complexity was undercounted: the flat step list for the bidding round plus the trick rounds came to about 21-24 steps, attributes went over 20, and the single sequential play step was never stated.
- Hidden information was overstated: with duplicate rotation, after deal 1 all 24 cards were public, so deal 2 hid only a 50/50 rotation (revealed in the first trick) and deal 3 was perfect information.
- The full original (32 cards, talon exchange, marriages, special contracts, redouble) does not fit the step and choice limits.
- The previous variation's partner exception to the overtaking duty added a judgment call that is not in the original and invited conflicting rulings.

## Changes

- Use the original Mariáš heading rule, worded so that it covers every lead. If the currently winning card is of the suit led (including when trump is led), a player who follows suit must play a higher card of that suit if able. A player void in the led suit must trump and must beat any trump already played if able. This duty applies whoever is winning, partner or not. (fixes: Rule gap when trump is led: the previous duty to beat the trick applied only 'if no trump has been played', so it was unclear whether a player must overtake in a trump-led trick.): One unambiguous rule that a referee can check mechanically, and it matches the original game.
- Drop the partner exception to the duty to overtake or trump. (fixes: The previous variation's partner exception to the overtaking duty added a judgment call that is not in the original and invited conflicting rulings.): It removes a judgment call and restores the original's 'must head' rule.
- Replace duplicate rotation with a fresh shuffle every deal. Deal 7 cards to each seat and leave a 3-card talon that is never seen and never played. (fixes: Hidden information was overstated: with duplicate rotation, after deal 1 all 24 cards were public, so deal 2 hid only a 50/50 rotation (revealed in the first trick) and deal 3 was perfect information.): Every deal now has real hidden hands, and the hidden talon makes the points available uncertain. Bidding becomes a risk judgment and card counting becomes inference rather than bookkeeping.
- Play 5 deals of 8 rounds (1 bidding round plus 7 tricks), 40 rounds in total. Bid ties go to the tied player with the lowest match score, then to seat order from the eldest. (fixes: Hidden information was overstated: with duplicate rotation, after deal 1 all 24 cards were public, so deal 2 hid only a 50/50 rotation (revealed in the first trick) and deal 3 was perfect information.): More deals average out the luck that fresh shuffles bring back. Breaking ties by lowest score first neutralises the small advantage of being eldest twice in 5 deals.
- Declare a flat step list of 19 steps with `when` gates. Use one sequential choice step for all three card plays in a trick. Keep the hands and talon in engine hidden hands, and take bids directly from the poll. This gives 16 attributes. (fixes: Complexity was undercounted: the flat step list for the bidding round plus the trick rounds came to about 21-24 steps, attributes went over 20, and the single sequential play step was never stated.): Stays inside the limits of 20 steps, 4 choice steps and 20 attributes.
- Keep the cut-down deck (24 cards, A to 9), leave out marriages, talon exchange and special contracts, and keep Flek (no redouble) and Hearts doubling. (fixes: The full original (32 cards, talon exchange, marriages, special contracts, redouble) does not fit the step and choice limits.): Keeps the core of declarer against two defenders, contract levels and doubling while fitting the 4 choice steps.

## Kept from the original

- Three players: one declarer against two defenders in a partnership.
- Mariáš card ranking A, 10, K, O, U, 9 and the Czech suits.
- Aces and Tens worth 10 points each, plus 10 for the last trick.
- The original duties to follow suit, head the trick and trump when void.
- The declarer chooses trump, and Hearts trump doubles the stakes.
- Flek: defenders can double the stake.
- A contract is made or failed against a card-point threshold; the declarer wins or loses double what each defender pays or receives.

## The variation's rules

DECK: 24 cards in four suits (Hearts, Bells, Leaves, Acorns). Each suit has A, 10, K, O (Ober), U (Unter) and 9, ranking high to low A, 10, K, O, U, 9. Card points: each Ace 10, each Ten 10, all other cards 0. The side that wins the last (7th) trick of a deal also gets 10. At most 90 card points are available in a deal; fewer if Aces or Tens lie in the talon.

SEATS AND MATCH: Seats 1, 2 and 3. Seat order runs 1, 2, 3, 1 and so on. The match has 5 deals of 8 rounds each, 40 rounds in total. The eldest is Seat 1 in deal 1, Seat 2 in deal 2, Seat 3 in deal 3, Seat 1 in deal 4 and Seat 2 in deal 5. Match scores start at 0 and are public. There is no talk at any time. Hands are shown to their owner sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low.

ROUND 1 OF EACH DEAL (DEAL AND BID):
(a) Shuffle all 24 cards. Deal 7 cards privately to each seat. The remaining 3 cards are the talon. The talon is face down, is never played and is never shown to anyone, including at the end of the deal. Each player sees only their own hand.
(b) All three players bid at the same time without seeing the other bids. The options are PASS, 40, 50 or 60.
(c) If all three pass, the deal is not played. Rounds 2-8 of this deal are skipped with no plays and no scoring.
(d) Otherwise the highest bid wins and that player is the declarer. If several players tie for the highest bid, it goes to the tied player with the lowest match score. If they are still tied, it goes to the tied player who comes first in seat order starting from the eldest.
(e) The declarer chooses trump: Hearts, Bells, Leaves or Acorns.
(f) The declarer, the contract (the winning bid) and trump are announced. The other two players are the defenders, and their card points this deal are pooled together.
(g) Flek: the two defenders each choose FLEK or NO at the same time. Both choices are announced.
(h) Stake V: start at 1 for a 40 contract, 2 for 50 and 4 for 60. Double V if trump is Hearts. Double V again if at least one defender chose FLEK. V is announced.

ROUNDS 2-8 OF EACH DEAL (ONE TRICK PER ROUND):
(a) The declarer leads in round 2. In later rounds, the winner of the previous trick leads. The leader plays any card from their hand face up. Then the next player in seat order plays, then the third. Each card is shown to everyone as it is played.
(b) LEGAL CARDS. The 'currently winning card' is the card that would win the trick right now under rule (c). The following rules apply to every player, whoever is currently winning.
  1. If you hold a card of the suit led, you must play a card of that suit. If the currently winning card is of the suit led, you must play a higher card of that suit if you have one. This includes the case where trump was led. If the currently winning card is a trump and the suit led is not trump, any card of the suit led is legal.
  2. If you hold no card of the suit led but hold a trump, you must play a trump. If a trump has already been played in this trick, you must play a higher trump than the highest one played if you have one; otherwise any trump.
  3. If you hold neither the suit led nor a trump, you may play any card.
(c) The trick is won by the highest trump in it. If it contains no trump, it is won by the highest card of the suit led.
(d) The trick's card points go to the declarer if the declarer won it, or to the defenders' pooled total if either defender won it. In round 8 the last-trick 10 also goes to the side that won the trick. Running totals are announced.
(e) The trick winner leads the next round.

SCORING AT THE END OF ROUND 8 (only if the deal was played): the contract is made if the declarer's card points are at least the contract (40, 50 or 60).
- Made: the declarer gains 2V and each defender loses V.
- Failed: the declarer loses 2V and each defender gains V.
Match scores are announced.

END: the game ends after round 40.

Objective: After round 40, the player with the highest match score wins. If two or three players tie for the highest score, the game is a draw among them.

Expected effect: Every deal is a fresh hidden-information problem. Bidders must judge their hand against two unseen hands and an unseen talon that may hold up to 30 card points. Defenders must infer the declarer's holdings from the bid and trump choice, and Flek only when they read the contract as shaky. Card play rewards counting the eight Aces and Tens and inferring where the missing ones are, including whether they are in the talon. The always-head rule removes rule ambiguity.

Simple policies lose. Always passing never earns as declarer, and against competent declarers who make their contracts it bleeds V per deal. Always bidding 60 fails with weak hands at a stake of 4-16 and loses heavily. Always choosing FLEK doubles losses against strong declarers. Random play loses to counting.

Luck from the deal is reduced by the bidding choice (a weak hand can pass and defend), by five deals, and by the lowest-score tie-break.

Talk is omitted. The defenders share an interest and would coordinate trivially, and in-play signalling through cards is the intended channel. The game is zero-sum and has no endgame unravelling problem, because it is not a cooperation game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 19 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
