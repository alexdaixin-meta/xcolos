# 39 design

- time: 2026-10-28T03:49:45+00:00 (90.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 7dab8ed8cc9b7822, reply sha256 f9df806afbda4c2a

## Sent

````
Original game: Mariáš
Players in the original: 3 to 3

Original rules:
Mariáš is played with 32 cards A-10-K-O-U-9-8-7 ranking A,10,K,O,U,9,8,7 except in Betl/Durch. Three players receive cards, eldest hand views 7 cards and chooses trump, then receives 5 more and discards 2. The other two form a defending partnership. Play is 10 tricks. Must follow suit, must head the trick if able, must trump if cannot follow. Highest trump or highest of led suit wins. Winner leads and keeps won tricks in order. Aces and Tens are 10 each, last trick is 10, total 90. King+Ober of same suit in one hand is a marriage, worth 40 if trump else 20, if its holder wins a trick. Defenders can double with Flek, declarer can redouble. Hearts trump doubles stakes. Special contracts: Betl win no tricks, Durch win all tricks, 7 win last trick with lowest trump, 100 score 100+ points.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: (1) RULE GAP WHEN TRUMP IS LED. The overtaking duty for the led suit applies only 'if no trump has been played in this trick'. When trump is led, a trump has by definition been played. Read literally, a player holding trumps never has to beat the highest trump in a trump-led trick, though they must head a non-trump lead. This contradicts the stated intent ('must head the trick') and the original game. Models and the referee will rule it differently.

(2) COMPLEXITY UNDERCOUNTED. The engine's step list is flat, so the round-1 steps and the trick steps must sit in one list, each gated by `when` conditions.
Round-1 steps (about 13):
- deal-1 shuffle and store
- deal-2 draw and rotation
- deal-3 assignment
- bid poll
- highest bid with tie-break by seat from the eldest (about 2-3 calc steps)
- all-pass check
- trump choice
- announcement
- Flek poll
- V calculation (base, Hearts, Flek)
- announcement
Trick-round steps (about 7-8):
- sequential play
- legality check
- trick winner
- point award
- last-trick bonus
- leader update
- scoring at round 9 (made/failed: 2-3 steps)
This comes to about 21-24 steps, above the cap of 20, not the 16 declared.
Attributes are also over 20 once fully listed: H1-H3 (3), current hands (3), scores (3), bids (3), declarer, trump, contract, V, two Flek choices, declarer points, defender points, current trick cards/leader, deal index and the draw result.
Choice steps reach exactly 4 (bid, trump, Flek, trick play) only if one sequential step covers all three card plays. The design does not say so.

(3) THE HIDDEN-INFORMATION CLAIMS ARE INACCURATE. After deal 1 is played, all 24 cards have been shown publicly with their players. In deal 2 every player knows all three hands; the 50/50 draw hides only which opponent holds which, and the first trick reveals it. Deal 3 is fully determined, since it is the other derangement, and is perfect information. 'Each player's hand is private' and hidden_elements=2 overstate what is hidden. The rules should state this explicitly, or the design should change.

WHAT IS ADEQUATE:
- The game is finite (27 rounds) and decided by arithmetic.
- One random draw per round is respected.
- There is no board, clock or trading.
- No talk is a sensible choice for a trick-taking game. Defenders signal through card play, and open talk would let them coordinate trivially.
- change: Fix the trump-led case. State: 'If you hold the suit led and your opponent's card is currently winning, you must beat it if you can with a card of that suit (this applies also when trump is led); if a non-trump suit was led and a trump has already been played, any card of the led suit is legal.'
- change: Recount and declare the full flat step list with `when` gates for round 1 and for rounds 2-9, keeping it at or below 20. For example: precompute the deal-2 and deal-3 hand assignments in deal 1 so each later deal needs one assignment step; compute V in one calc step; do the tie-break in one calc step.
- change: Give an explicit attribute list at or below 20. For example, use engine hidden_hands for the current hands instead of attributes, and drop the per-seat bid attributes by computing the winning bid directly from the poll.
- change: State that all three card plays in a trick use one sequential choice step, so choice_steps_per_round stays at 4.
- change: Remove or correct the claim that hands are private in deals 2-3. Either state openly that after deal 1 the hands are public knowledge (and declare hidden_elements accordingly), or keep information hidden: for example, leave 2 cards undealt as a hidden talon of 22 dealt cards (7/7/8, or 8/7/7 with the declarer taking the talon), so the rotated hands are not fully known.
The variation that was reviewed: Duplicate Mini Mariáš: DECK: 24 cards in four suits (Hearts, Bells, Leaves, Acorns). Each suit has A, 10, K, O (Ober), U (Unter) and 9, ranking high to low A, 10, K, O, U, 9. Card points: each Ace 10, each Ten 10, all others 0. The side that wins the 8th (last) trick of a deal gets 10 more. Card points in a deal always total 90.

SEATS AND MATCH: Seats 1, 2 and 3. Seat order runs 1, 2, 3, 1 and so on. There are three deals of 9 rounds each, 27 rounds in total. The eldest is Seat 1 in deal 1, Seat 2 in deal 2 and Seat 3 in deal 3; the eldest only breaks ties in bidding. Every match score starts at 0. Each player's hand is private. Hands are always shown sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low. There is no talk at any time.

ROUND 1 OF EACH DEAL (DEALING AND BIDDING):
(a) Hands.
- Deal 1: shuffle the 24 cards and deal 8 to each seat. Call Seat 1's hand H1, Seat 2's hand H2 and Seat 3's hand H3. The engine stores all three.
- Deal 2: one secret random draw, 50/50, picks LEFT or RIGHT. LEFT: Seat 1 gets H3, Seat 2 gets H1, Seat 3 gets H2. RIGHT: Seat 1 gets H2, Seat 2 gets H3, Seat 3 gets H1. The draw is never announced.
- Deal 3: each seat gets the one stored hand it has not yet held.
(b) All three players bid at the same time, without seeing the other bids. The options are PASS, 40, 50 and 60.
(c) If all three pass, the deal is not played. Nobody's score changes, and rounds 2-9 of this deal are skipped with no plays and no scoring. Otherwise the highest bid wins and that player is the declarer. A tie for the highest bid goes to the tied player who comes first in seat order starting from the eldest.
(d) The declarer chooses trump: Hearts, Bells, Leaves or Acorns.
(e) The contract value, the declarer and trump are announced. The other two players are defenders and share their card points for this deal.
(f) Flek: the two defenders each choose FLEK or NO at the same time. Both choices are announced.
(g) Stake V: start at 1 for a 40 contract, 2 for 50 and 4 for 60. Double V if trump is Hearts. Double V again if at least one defender chose FLEK. V is announced.

ROUNDS 2-9 OF EACH DEAL (ONE TRICK PER ROUND):
(a) The declarer leads in round 2. After that, the winner of the previous trick leads. The leader plays any card face up. The next player in seat order then plays, then the third player. Each card is shown to all as it is played.
(b) LEGAL CARDS. 'Currently winning card' means the card that would win the trick right now under rule (c). Your opponent is the declarer if you are a defender, and either defender if you are the declarer.
- If you hold the suit led, you must play that suit. If no trump has been played in this trick and your opponent's card is currently winning, you must also beat the highest card of the led suit if you can. Otherwise any card of the led suit is legal.
- If you hold no card of the led suit but hold a trump, and your opponent's card is currently winning, you must play a trump. If a trump is already in the trick, you must beat the highest trump if you can. If your partner's card is currently winning, you may play any card instead.
- If you hold neither the led suit nor a trump, you may play any card.
(c) The trick is won by the highest trump played. If no trump was played, it is won by the highest card of the led suit.
(d) The trick's card points go to the declarer if the declarer won it, or to the defenders' shared total if a defender won it. In round 9, the last-trick 10 also goes to the winning side. Running totals are public.
(e) The trick winner leads the next round.

SCORING AT THE END OF ROUND 9 (only if the deal was played): the contract is made if the declarer's card points are at least the contract value (40, 50 or 60).
- Made: the declarer gains 2V and each defender loses V.
- Failed: the declarer loses 2V and each defender gains V.
Match scores are announced.

END: after round 27, the game ends. Winner: After the third deal, the player with the highest match score wins. If two or three players tie for the highest score, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Mariáš is a Czech three-player trick-taking game with a 32-card deck. One declarer, who chooses trump and takes a talon, plays 10 tricks against two defenders in partnership. Players must follow suit, head the trick and trump when void. Aces and Tens count 10 each, the last trick counts 10, and a marriage (King and Ober of one suit) is worth 20 or 40. Flek doubling, Hearts doubling and special contracts set the stakes.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "In the original, no simple policy wins. Always passing never earns points as declarer and depends on others failing. Always declaring high loses badly with weak hands. The seat advantage of being eldest is offset because everyone holds that seat in turn. The previous variation kept this, but its duplicate rotation made deals 2 and 3 almost perfect information."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Card play, counting the Aces and Tens, choosing when to declare and Flek decisions all separate strong players from weak ones. The card deal adds variance over a single deal, but over several deals the bidding lets players avoid bad hands and punish overbids."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Inferring hidden cards from play, defenders signalling to each other, and judging contract levels against an unknown talon have a high skill ceiling. A weak player still scores by defending or by declaring a strong hand."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "In the original, hands and the talon are hidden, so play depends on inferring card locations and the declarer's intent. In the previous variation, after deal 1 every card was public, so deals 2 and 3 had little or nothing left to infer. That is the flaw this revision fixes."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners, card points, whether the contract is made and the stake are all arithmetic. Only the legality of a card needs a rule check, and with the original 'always head the trick' rule that check is mechanical."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The full original is too large for the limits: 32 cards, 10 tricks, talon exchange, marriages, four special contracts and redoubles. The previous variation went over 20 steps and 20 attributes. It also had a rule gap when trump is led."
    }
  ],
  "problems": [
    "Rule gap when trump is led: the previous duty to beat the trick applied only 'if no trump has been played', so it was unclear whether a player must overtake in a trump-led trick.",
    "Complexity was undercounted: the flat step list for the bidding round plus the trick rounds came to about 21-24 steps, attributes went over 20, and the single sequential play step was never stated.",
    "Hidden information was overstated: with duplicate rotation, after deal 1 all 24 cards were public, so deal 2 hid only a 50/50 rotation (revealed in the first trick) and deal 3 was perfect information.",
    "The full original (32 cards, talon exchange, marriages, special contracts, redouble) does not fit the step and choice limits.",
    "The previous variation's partner exception to the overtaking duty added a judgment call that is not in the original and invited conflicting rulings."
  ],
  "changes": [
    {
      "what": "Use the original Mariáš heading rule, worded so that it covers every lead. If the currently winning card is of the suit led (including when trump is led), a player who follows suit must play a higher card of that suit if able. A player void in the led suit must trump and must beat any trump already played if able. This duty applies whoever is winning, partner or not.",
      "why": "One unambiguous rule that a referee can check mechanically, and it matches the original game.",
      "fixes": "Rule gap when trump is led: the previous duty to beat the trick applied only 'if no trump has been played', so it was unclear whether a player must overtake in a trump-led trick."
    },
    {
      "what": "Drop the partner exception to the duty to overtake or trump.",
      "why": "It removes a judgment call and restores the original's 'must head' rule.",
      "fixes": "The previous variation's partner exception to the overtaking duty added a judgment call that is not in the original and invited conflicting rulings."
    },
    {
      "what": "Replace duplicate rotation with a fresh shuffle every deal. Deal 7 cards to each seat and leave a 3-card talon that is never seen and never played.",
      "why": "Every deal now has real hidden hands, and the hidden talon makes the points available uncertain. Bidding becomes a risk judgment and card counting becomes inference rather than bookkeeping.",
      "fixes": "Hidden information was overstated: with duplicate rotation, after deal 1 all 24 cards were public, so deal 2 hid only a 50/50 rotation (revealed in the first trick) and deal 3 was perfect information."
    },
    {
      "what": "Play 5 deals of 8 rounds (1 bidding round plus 7 tricks), 40 rounds in total. Bid ties go to the tied player with the lowest match score, then to seat order from the eldest.",
      "why": "More deals average out the luck that fresh shuffles bring back. Breaking ties by lowest score first neutralises the small advantage of being eldest twice in 5 deals.",
      "fixes": "Hidden information was overstated: with duplicate rotation, after deal 1 all 24 cards were public, so deal 2 hid only a 50/50 rotation (revealed in the first trick) and deal 3 was perfect information."
    },
    {
      "what": "Declare a flat step list of 19 steps with `when` gates. Use one sequential choice step for all three card plays in a trick. Keep the hands and talon in engine hidden hands, and take bids directly from the poll. This gives 16 attributes.",
      "why": "Stays inside the limits of 20 steps, 4 choice steps and 20 attributes.",
      "fixes": "Complexity was undercounted: the flat step list for the bidding round plus the trick rounds came to about 21-24 steps, attributes went over 20, and the single sequential play step was never stated."
    },
    {
      "what": "Keep the cut-down deck (24 cards, A to 9), leave out marriages, talon exchange and special contracts, and keep Flek (no redouble) and Hearts doubling.",
      "why": "Keeps the core of declarer against two defenders, contract levels and doubling while fitting the 4 choice steps.",
      "fixes": "The full original (32 cards, talon exchange, marriages, special contracts, redouble) does not fit the step and choice limits."
    }
  ],
  "keeps": [
    "Three players: one declarer against two defenders in a partnership.",
    "Mariáš card ranking A, 10, K, O, U, 9 and the Czech suits.",
    "Aces and Tens worth 10 points each, plus 10 for the last trick.",
    "The original duties to follow suit, head the trick and trump when void.",
    "The declarer chooses trump, and Hearts trump doubles the stakes.",
    "Flek: defenders can double the stake.",
    "A contract is made or failed against a card-point threshold; the declarer wins or loses double what each defender pays or receives."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Mariáš (bidding against hidden hands, declarer against a partnership, counting points) fits the limits once cut to 24 cards and 7 tricks, with a hidden talon keeping every deal a game of inference."
  },
  "variation": {
    "name": "Mini Mariáš with Hidden Talon",
    "summary": "A five-deal, three-player Mariáš. Each deal is freshly shuffled with a 3-card hidden talon. Players bid a contract of 40, 50 or 60 card points, the declarer picks trump, defenders may Flek, and 7 tricks are played under the original must-follow, must-head, must-trump rules.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "DECK: 24 cards in four suits (Hearts, Bells, Leaves, Acorns). Each suit has A, 10, K, O (Ober), U (Unter) and 9, ranking high to low A, 10, K, O, U, 9. Card points: each Ace 10, each Ten 10, all other cards 0. The side that wins the last (7th) trick of a deal also gets 10. At most 90 card points are available in a deal; fewer if Aces or Tens lie in the talon.\n\nSEATS AND MATCH: Seats 1, 2 and 3. Seat order runs 1, 2, 3, 1 and so on. The match has 5 deals of 8 rounds each, 40 rounds in total. The eldest is Seat 1 in deal 1, Seat 2 in deal 2, Seat 3 in deal 3, Seat 1 in deal 4 and Seat 2 in deal 5. Match scores start at 0 and are public. There is no talk at any time. Hands are shown to their owner sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low.\n\nROUND 1 OF EACH DEAL (DEAL AND BID):\n(a) Shuffle all 24 cards. Deal 7 cards privately to each seat. The remaining 3 cards are the talon. The talon is face down, is never played and is never shown to anyone, including at the end of the deal. Each player sees only their own hand.\n(b) All three players bid at the same time without seeing the other bids. The options are PASS, 40, 50 or 60.\n(c) If all three pass, the deal is not played. Rounds 2-8 of this deal are skipped with no plays and no scoring.\n(d) Otherwise the highest bid wins and that player is the declarer. If several players tie for the highest bid, it goes to the tied player with the lowest match score. If they are still tied, it goes to the tied player who comes first in seat order starting from the eldest.\n(e) The declarer chooses trump: Hearts, Bells, Leaves or Acorns.\n(f) The declarer, the contract (the winning bid) and trump are announced. The other two players are the defenders, and their card points this deal are pooled together.\n(g) Flek: the two defenders each choose FLEK or NO at the same time. Both choices are announced.\n(h) Stake V: start at 1 for a 40 contract, 2 for 50 and 4 for 60. Double V if trump is Hearts. Double V again if at least one defender chose FLEK. V is announced.\n\nROUNDS 2-8 OF EACH DEAL (ONE TRICK PER ROUND):\n(a) The declarer leads in round 2. In later rounds, the winner of the previous trick leads. The leader plays any card from their hand face up. Then the next player in seat order plays, then the third. Each card is shown to everyone as it is played.\n(b) LEGAL CARDS. The 'currently winning card' is the card that would win the trick right now under rule (c). The following rules apply to every player, whoever is currently winning.\n  1. If you hold a card of the suit led, you must play a card of that suit. If the currently winning card is of the suit led, you must play a higher card of that suit if you have one. This includes the case where trump was led. If the currently winning card is a trump and the suit led is not trump, any card of the suit led is legal.\n  2. If you hold no card of the suit led but hold a trump, you must play a trump. If a trump has already been played in this trick, you must play a higher trump than the highest one played if you have one; otherwise any trump.\n  3. If you hold neither the suit led nor a trump, you may play any card.\n(c) The trick is won by the highest trump in it. If it contains no trump, it is won by the highest card of the suit led.\n(d) The trick's card points go to the declarer if the declarer won it, or to the defenders' pooled total if either defender won it. In round 8 the last-trick 10 also goes to the side that won the trick. Running totals are announced.\n(e) The trick winner leads the next round.\n\nSCORING AT THE END OF ROUND 8 (only if the deal was played): the contract is made if the declarer's card points are at least the contract (40, 50 or 60).\n- Made: the declarer gains 2V and each defender loses V.\n- Failed: the declarer loses 2V and each defender gains V.\nMatch scores are announced.\n\nEND: the game ends after round 40.",
    "objective": "After round 40, the player with the highest match score wins. If two or three players tie for the highest score, the game is a draw among them.",
    "expected_effect": "Every deal is a fresh hidden-information problem. Bidders must judge their hand against two unseen hands and an unseen talon that may hold up to 30 card points. Defenders must infer the declarer's holdings from the bid and trump choice, and Flek only when they read the contract as shaky. Card play rewards counting the eight Aces and Tens and inferring where the missing ones are, including whether they are in the talon. The always-head rule removes rule ambiguity.\n\nSimple policies lose. Always passing never earns as declarer, and against competent declarers who make their contracts it bleeds V per deal. Always bidding 60 fails with weak hands at a stake of 4-16 and loses heavily. Always choosing FLEK doubles losses against strong declarers. Random play loses to counting.\n\nLuck from the deal is reduced by the bidding choice (a weak hand can pass and defend), by five deals, and by the lowest-score tie-break.\n\nTalk is omitted. The defenders share an interest and would coordinate trivially, and in-play signalling through cards is the intended channel. The game is zero-sum and has no endgame unravelling problem, because it is not a cooperation game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 19,
    "choice_steps_per_round": 4,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
