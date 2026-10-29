# 37 design

- time: 2026-10-28T03:45:19+00:00 (165.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 7839f71f1891eaf9, reply sha256 5879777587b1d807

## Sent

````
Original game: Mariáš
Players in the original: 3 to 3

Original rules:
Mariáš is played with 32 cards A-10-K-O-U-9-8-7 ranking A,10,K,O,U,9,8,7 except in Betl/Durch. Three players receive cards, eldest hand views 7 cards and chooses trump, then receives 5 more and discards 2. The other two form a defending partnership. Play is 10 tricks. Must follow suit, must head the trick if able, must trump if cannot follow. Highest trump or highest of led suit wins. Winner leads and keeps won tricks in order. Aces and Tens are 10 each, last trick is 10, total 90. King+Ober of same suit in one hand is a marriage, worth 40 if trump else 20, if its holder wins a trick. Defenders can double with Flek, declarer can redouble. Hearts trump doubles stakes. Special contracts: Betl win no tricks, Durch win all tricks, 7 win last trick with lowest trump, 100 score 100+ points.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: Chance dominates.

There are only 3 deals, so a match has only 3 bidding decisions and 3 trump choices. The result of each deal turns mostly on hand strength.

Card play offers less choice than it seems. The must-follow, must-beat, must-trump and must-over-trump rules often leave 1-2 legal cards. Defenders must even overtake their own partner's winning card. Real choice is mostly limited to leads and to picking among the cards that beat the trick.

When every player plays well, each bids only on strong hands. With 8 random cards and no talon, roughly one player in a deal holds a biddable hand, or none does and the eldest is forced to 40. The player dealt the strongest hand(s) collects +2V to +8V; the others mostly pass and score ±V by the declarer's luck. If all three bid and play perfectly, the match winner is essentially whoever received the best hands in 3 deals.

Rough estimate: deal luck decides well over half of match outcomes, probably 60-70%. A skilled player cannot reliably beat a weaker one over a single 3-deal sample. There is something to infer: the bids, and inference from forced plays. But too few independent decisions exist to overcome the deal.
- change: Use duplicate dealing to remove hand luck. Shuffle once at the start, store the three 8-card hands, and in deals 2 and 3 rotate the same hands so every player holds each hand exactly once, with eldest rotating as now. This still uses at most 1 random draw per round, and 27 rounds.
- change: Alternatively, or as well, raise the number of independent deals to 4 (36 rounds ≤ 40) so skill has more decisions to show itself.
- change: Give card play more real choice. Drop the requirement to beat a card already played by your own partner (or the must-beat rule for defenders entirely), so defenders choose between overtaking and discarding a low card. This makes play and inference matter more than forced sequences.
- change: Optionally add a 2-card talon dealt face down, which the declarer picks up and then discards 2. Contracts then reward hand evaluation in bidding rather than raw deal strength; this is within hidden_elements ≤ 3.
The variation that was reviewed: Mini Mariáš: DECK: 24 cards in four suits (Hearts, Bells, Leaves, Acorns), each suit containing A, 10, K, O (Ober), U (Unter), 9. In each suit, cards rank high to low as A, 10, K, O, U, 9. Card points: each Ace is 10, each Ten is 10, all other cards are 0. The side that wins the last (8th) trick gets 10 more. The total is always 90.

MATCH: Three deals, 9 rounds each, 27 rounds in total. The eldest is Seat 1 in deal 1, Seat 2 in deal 2 and Seat 3 in deal 3. Seat order runs 1, 2, 3, 1, and so on. Every player's match score starts at 0.

ROUND 1 OF EACH DEAL (BIDDING):
(a) Shuffle the 24 cards and deal 8 face down to each player. Each player sees only their own hand. Each hand is stored in the order dealt, and this order is never sorted.
(b) All three players bid at the same time, without seeing the other bids. The options, always in this order, are: PASS, 40, 50, 60.
(c) The highest bid wins and that player is the declarer. If two or more players tie for the highest bid, the tied player who comes first in seat order starting from the eldest wins. If all three pass, the eldest is the declarer with a contract of 40.
(d) The declarer chooses trump. The options, always in this order, are: Hearts, Bells, Leaves, Acorns.
(e) The contract, the declarer and trump are announced to everyone. The other two players are defenders and share their card points for this deal.
(f) The contract's stake V is 1 for 40, 2 for 50 and 4 for 60.

ROUNDS 2-9 OF EACH DEAL (ONE TRICK EACH):
(a) The leader plays one card face up. The declarer leads round 2; after that, the winner of the previous trick leads.
(b) The next player in seat order plays, then the third. Each player may choose only among their legal cards, offered in their hand's dealt order.
(c) LEGAL CARDS:
- If you hold a card of the suit led, you must play that suit. You must also beat the highest card of that suit played so far, if you can, unless the trick has already been trumped. Then you may play any card of the suit led.
- If you hold no card of the suit led but hold a trump, you must play a trump. You must beat the highest trump played so far in this trick, if you can.
- If you hold neither, you may play any card.
(d) The trick goes to whoever played the highest trump. If no trump was played, it goes to whoever played the highest card of the suit led.
(e) The card points in the trick are added to the declarer's total if the declarer won it, or to the defenders' shared total if a defender won it. In round 9, the 10 points for the last trick are added to the winner's side.
(f) The trick winner leads the next round.

SCORING AT THE END OF ROUND 9 OF EACH DEAL: The contract is made if the declarer's card points are at least the contract value.
- If made: the declarer's match score goes up by 2V and each defender's goes down by V.
- If failed: the declarer's goes down by 2V and each defender's goes up by V.
The cards are then gathered for the next deal.

There is no talk between players at any time. Winner: After the third deal, the player with the highest match score wins. If two or three players tie for the highest score, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Mariáš is a Czech three-player trick-taking game with a 32-card deck. A declarer names trump and a contract, then plays alone against a two-player defending partnership over 10 tricks. Aces and Tens count 10 each and the last trick counts 10, so card points total 90. Marriages, doubling (Flek) and special contracts change the stakes. The reviewed variation was a 24-card, 3-deal version with simultaneous bidding and the strict must-follow, must-beat and must-trump rules.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. Always bidding 60 fails most contracts and pays -8 each time. Always passing leaves you exposed to ±V as a defender, and in the reviewed variation it forced the eldest into a 40 contract. The scoring is zero-sum and seats rotate. The only built-in edge was the eldest's tie-break and the forced contract, which were minor."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "A match was only 3 independent deals, and the deals were freshly shuffled. The testers estimated that deal luck decided 60-70% of matches. The player dealt the strongest hand collects +2V to +8V while the others mostly pass, so a strong player cannot reliably beat a weak one."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Several skills can keep improving: judging a hand for a contract level, choosing trump, planning leads, and defending as a partnership with no signals. A weak player still scores as a defender when the declarer fails."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Each player knows the 16 cards held by the two opponents together, but not how they are split, so there is something to infer from bids and plays. However, the must-beat and must-trump rules, including having to overtake your own partner, often left only 1-2 legal cards. Most of the play was therefore forced and the inference had little to act on."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card points, contract success and match scores are pure arithmetic on cards the engine tracks."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is turn-based text with no board. It runs 27 rounds, uses one shuffle per deal and needs at most 3 choices per round."
    }
  ],
  "problems": [
    "P1: Deal luck dominates. Three fresh deals mean the player dealt the best hands usually wins, whatever the skill.",
    "P2: Card play is mostly forced. A defender must beat or over-trump even a partner's winning card, which leaves 1-2 legal cards and removes partnership choice and inference.",
    "P3: When all three players pass, the eldest is forced into a 40 contract. This adds pure luck and a seat penalty.",
    "P4: There are few decisions per deal that test opponent modelling. The defenders can never challenge a contract, and the declarer's trump choice carries no stake trade-off.",
    "P5: Duplicate dealing naively leaks information. If the rotation of stored hands is public, a player in deal 2 knows exactly which opponent holds which hand, and the hidden split vanishes."
  ],
  "changes": [
    {
      "what": "Duplicate dealing. Shuffle once at the start of deal 1 and store the three 8-card hands. In deals 2 and 3 the same three hands are redealt so that every player holds each hand exactly once over the match.",
      "why": "Everyone plays the same cards over the match, so the score difference measures how well each player bid and played those hands, not who was dealt them.",
      "fixes": "P1: Deal luck dominates."
    },
    {
      "what": "Secret rotation in deal 2. One hidden coin decides whether the hands shift one seat 'left' or 'right'. It is never announced. Deal 3 gives each player the remaining hand.",
      "why": "In deal 2 each player knows the two hands the opponents hold, but not which opponent has which. Bids, Flek decisions and early plays become evidence to read. Deal 3 is open-handed and becomes a planning test.",
      "fixes": "P5: Duplicate dealing naively leaks information."
    },
    {
      "what": "Relaxed must-beat and must-trump rules. You must beat the trick, or trump or over-trump it, only when the card currently winning was played by your opponent. A defender whose partner is winning may play any card of the led suit, or discard instead of trumping.",
      "why": "Defenders get real choices: overtake or duck, trump or keep a trump, and which point card to give to a partner's trick. Play becomes partnership planning and inference about the partner's cards.",
      "fixes": "P2: Card play is mostly forced."
    },
    {
      "what": "If all three pass, the deal is not played and scores nothing.",
      "why": "This removes the forced contract and its luck and seat penalty. Passing becomes a real judgement, because passing a playable hand gives up the chance to score with it.",
      "fixes": "P3: When all three pass, the eldest is forced into a 40 contract."
    },
    {
      "what": "Restore Flek and Hearts trump from the original. After trump is announced, the defenders secretly choose Flek or No; any Flek doubles the stake. Hearts as trump also doubles the stake.",
      "why": "Defenders must judge whether the declarer can make the contract, and a Flek is a signal and a risk shared with the partner. The declarer weighs the best-fitting trump against the Hearts multiplier and the risk of a Flek.",
      "fixes": "P4: There are few decisions per deal that test opponent modelling."
    },
    {
      "what": "Hands are shown sorted by suit (Hearts, Bells, Leaves, Acorns) and by rank, instead of in dealt order.",
      "why": "Players can read their hand and the legal options clearly, so errors come from strategy, not presentation.",
      "fixes": "P2: Card play is mostly forced."
    }
  ],
  "keeps": [
    "A declarer plays alone against a two-player defending partnership.",
    "Bidding for the right to declare, then the declarer choosing trump.",
    "The Mariáš rank order A, 10, K, O, U, 9.",
    "Aces and Tens worth 10 each, the last trick worth 10, 90 points in total.",
    "Must follow suit and must trump when void, with must-beat kept against the opponent.",
    "Flek, which doubles the stake, and Hearts trump doubling the stake.",
    "Zero-sum settlement: the declarer wins or loses 2V and each defender loses or wins V."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Duplicate dealing with a secret rotation removes most hand luck within 27 rounds and one random draw per round. Relaxed beat rules and Flek give the bidding, defence and inference room to decide the match."
  },
  "variation": {
    "name": "Duplicate Mini Mariáš",
    "summary": "Three players play three deals of 24-card Mariáš with the same three hands, so each player holds each hand once. The rotation in deal 2 is secret. Defenders may duck under a partner's winning card and may Flek a contract. The highest match score wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "DECK: 24 cards in four suits (Hearts, Bells, Leaves, Acorns). Each suit has A, 10, K, O (Ober), U (Unter) and 9, ranking high to low A, 10, K, O, U, 9. Card points: each Ace 10, each Ten 10, all others 0. The side that wins the 8th (last) trick of a deal gets 10 more. Card points in a deal always total 90.\n\nSEATS AND MATCH: Seats 1, 2 and 3. Seat order runs 1, 2, 3, 1 and so on. There are three deals of 9 rounds each, 27 rounds in total. The eldest is Seat 1 in deal 1, Seat 2 in deal 2 and Seat 3 in deal 3; the eldest only breaks ties in bidding. Every match score starts at 0. Each player's hand is private. Hands are always shown sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low. There is no talk at any time.\n\nROUND 1 OF EACH DEAL (DEALING AND BIDDING):\n(a) Hands.\n- Deal 1: shuffle the 24 cards and deal 8 to each seat. Call Seat 1's hand H1, Seat 2's hand H2 and Seat 3's hand H3. The engine stores all three.\n- Deal 2: one secret random draw, 50/50, picks LEFT or RIGHT. LEFT: Seat 1 gets H3, Seat 2 gets H1, Seat 3 gets H2. RIGHT: Seat 1 gets H2, Seat 2 gets H3, Seat 3 gets H1. The draw is never announced.\n- Deal 3: each seat gets the one stored hand it has not yet held.\n(b) All three players bid at the same time, without seeing the other bids. The options are PASS, 40, 50 and 60.\n(c) If all three pass, the deal is not played. Nobody's score changes, and rounds 2-9 of this deal are skipped with no plays and no scoring. Otherwise the highest bid wins and that player is the declarer. A tie for the highest bid goes to the tied player who comes first in seat order starting from the eldest.\n(d) The declarer chooses trump: Hearts, Bells, Leaves or Acorns.\n(e) The contract value, the declarer and trump are announced. The other two players are defenders and share their card points for this deal.\n(f) Flek: the two defenders each choose FLEK or NO at the same time. Both choices are announced.\n(g) Stake V: start at 1 for a 40 contract, 2 for 50 and 4 for 60. Double V if trump is Hearts. Double V again if at least one defender chose FLEK. V is announced.\n\nROUNDS 2-9 OF EACH DEAL (ONE TRICK PER ROUND):\n(a) The declarer leads in round 2. After that, the winner of the previous trick leads. The leader plays any card face up. The next player in seat order then plays, then the third player. Each card is shown to all as it is played.\n(b) LEGAL CARDS. 'Currently winning card' means the card that would win the trick right now under rule (c). Your opponent is the declarer if you are a defender, and either defender if you are the declarer.\n- If you hold the suit led, you must play that suit. If no trump has been played in this trick and your opponent's card is currently winning, you must also beat the highest card of the led suit if you can. Otherwise any card of the led suit is legal.\n- If you hold no card of the led suit but hold a trump, and your opponent's card is currently winning, you must play a trump. If a trump is already in the trick, you must beat the highest trump if you can. If your partner's card is currently winning, you may play any card instead.\n- If you hold neither the led suit nor a trump, you may play any card.\n(c) The trick is won by the highest trump played. If no trump was played, it is won by the highest card of the led suit.\n(d) The trick's card points go to the declarer if the declarer won it, or to the defenders' shared total if a defender won it. In round 9, the last-trick 10 also goes to the winning side. Running totals are public.\n(e) The trick winner leads the next round.\n\nSCORING AT THE END OF ROUND 9 (only if the deal was played): the contract is made if the declarer's card points are at least the contract value (40, 50 or 60).\n- Made: the declarer gains 2V and each defender loses V.\n- Failed: the declarer loses 2V and each defender gains V.\nMatch scores are announced.\n\nEND: after round 27, the game ends.",
    "objective": "After the third deal, the player with the highest match score wins. If two or three players tie for the highest score, the game is a draw among them.",
    "expected_effect": "Because every player holds every hand once, a strong hand no longer decides the match. What decides it is: (1) who has the nerve and judgement to bid each hand at the right level, possibly outbidding a rival on the same cards they will later hold; (2) Flek decisions that read whether a declarer is overreaching; and (3) defence that now has real choices about ducking, discarding or trumping. In deal 2, players know the two opposing hands but not who holds which, so early bids and plays must be read to resolve this. Deal 3 is open-handed and rewards exact planning. Simple policies all lose to sensible play: always 60 fails heavily, always pass gives up declarer gains, and always Flek pays double on made contracts. Talk is left out, as in real Mariáš. In each deal one side's interests are opposed to the other's, but the two defenders want the same thing, so any public talk would either be partnership signalling the declarer also hears, or pointless. Inferring a partner's hand from their plays is the intended skill. A small residual edge remains in the eldest's bid tie-break."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 3,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 27
  }
}
```
````
