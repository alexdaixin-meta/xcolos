# 34 design

- time: 2026-10-27T18:26:54+00:00 (68.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 8e0145724bdff31d, reply sha256 67279fbf3ad3758c

## Sent

````
Original game: Skull King
Players in the original: 2 to 8

Original rules:
Play 10 hands. The deck has 4 colored suits 1-14, 5 Pirates, 5 Escapes, 2 Mermaids, 1 Scary Mary, 1 Skull King. In hand i each player is dealt i cards. Players simultaneously bid how many tricks they will win. Tricks are played clockwise; must follow lead suit if possible, but any special card may be played at any time. Highest card of lead suit wins unless trumped. Black is permanent trump over colors. Mermaid beats all colors and black. Pirate beats mermaid and all colors/black. Skull King beats all except Mermaid, which beats Skull King. Scary Mary is declared as Pirate or Escape when played. Escape is 0, loses unless all Escape, then first wins. If first card is special, first colored card defines lead suit. Score: if bid equals tricks taken, gain 20 per trick, plus zero-bid gives hand-number*10, plus bonuses: 30 per Pirate captured by Skull King, 50 for Skull King captured by Mermaid. If bid fails, lose 10 per difference, or minus hand*10 for failed zero bid. Highest total after 10 hands wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: The rules are complete and unambiguous:
- The tie-break is clear: SK + Mermaid → Mermaid wins, even if a Pirate is present.
- Only 2 Escapes share a power with 3+ players, so a winner always exists.
- The game is finite (8 rounds), and scoring is arithmetic.

No discussion is acceptable. Bids are announced publicly and give each player something to reason about, so players are not left to blind guessing.

The claimed complexity is wrong, though:
- Card play in R5 is sequential, one player at a time, inside each of 3 tricks.
- That is 3 tricks × 3–4 players = 9–12 player choices per round. With the bid poll, that makes 10–13 choice steps against a limit of 4. The stated 'choice_steps_per_round: 4' is false.
- The leader of tricks 2 and 3 is the previous winner, so the acting order changes at runtime. The step list is flat, so this needs one conditional copy of each seat's play step per possible leader position. For 4 players that is up to 4 orderings × 4 plays × 2 tricks.
- Each trick also needs its own resolution: find the maximum, the Mermaid/SK check, the Pirate bonus, the tricks_won increment, and card removal. Add deck reset, shuffle, deal ×players, bid poll, announce, and 4-case scoring.
- The honest total is well over 20 steps per round.
- reasoning_over_luck FAILED: Without suits, a hand's trick count is almost fixed by the cards dealt:
- SK is a near-certain trick.
- Pirate B is a certain trick unless SK shares its trick.
- Hands of ≤9 almost never win a trick.
Bidding reduces to counting top cards, and play reduces to 'highest when I need a trick, lowest when I don't'. Timing gives only a little real choice.

Inference is thin. 9 of 18 cards (3p) or 6 (4p) stay hidden and undealt, and nothing reveals them, so card counting is weak.

Scenario: all players play well.
- A weak hand earns at most +30 (zero bid).
- A strong hand earns +40/+60, plus SK/Pirate (+30 each) or Mermaid/SK (+50) bonuses that only the holders of those cards can collect.
- The ceiling per round depends on the deal: 30 vs 60–110.
- Over 8 short rounds with 4 key cards spread over 3–4 players, the player dealt SK/Pirates/Mermaid most often usually wins.

Estimated share of the result due to the deal: about 50–60%. A skilled player is not clearly favoured over an adequate one.
- change: Playable: replace sequential trick play with one simultaneous poll per trick (every player picks a card at once, then all are revealed). The round then has 4 choice steps: bid plus 3 tricks. Drop the 'winner leads next trick' rule. If sequential order is kept, cut to 1-2 tricks so choices stay at 4 or fewer.
- change: Playable: re-count every step and attribute against this design and show steps_per_round ≤ 20. Each trick's resolution (max, Mermaid/SK check, Pirate bonus, tricks_won, card removal) should take at most 3–4 steps, or the per-trick bonus checks should be simplified.
- change: Reasoning over luck: flatten exact-bid payoffs so deal strength matters less, e.g. exact bid of any value = +30 + 5×bid.
- change: Reasoning over luck: cut or cap the SK/Pirate/Mermaid bonuses, e.g. a single +20, so holding top cards is not a large automatic payoff.
- change: Reasoning over luck: publicly reveal 3 of the undealt cards each round so players can infer the remaining distribution and model opponents' bids.
- change: Reasoning over luck: optionally restore a following constraint, such as two colours with must-follow, so weak hands have meaningful sequencing choices.
- change: Balanced (recommended): set rounds to a multiple of the player count (9 for 3 players, 8 for 4) so every seat leads equally often.
The variation that was reviewed: Skull King: Short Seas: CARDS. Each card is a power number. The deck holds 18 cards:
- the numbers 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12;
- two Escapes, each power 0;
- one Mermaid, power 20;
- Pirate A, power 30;
- Pirate B, power 31;
- the Skull King, power 40.

TABLE CONSTANTS. rounds = 8, hand_size = 3, tricks_per_round = 3, bid_min = 0, bid_max = 3.

R1 SETUP. When the game starts, every player's score is 0 and the round counter is 0.

R2 ROUND START. When a round starts:
- round increases by 1;
- every player's tricks_won is set to 0, bonus is set to 0, and hand is set to empty.

R3 DECK AND DEAL. After R2:
- the deck is set to all 18 cards listed above, whatever it held before;
- the deck is shuffled (the round's one chance event);
- each player in seat order is dealt 3 cards from the deck into their private hand. 18 − 3 × players cards stay undealt (9 with 3 players, 6 with 4).
- Hands are hidden from other players.

R4 BID. All players bid at the same moment, without seeing other bids.
- Each player is asked exactly once per round, before any trick is played.
- The options are every whole number from bid_min to bid_max inclusive: exactly 0, 1, 2, 3.
- The chosen number is stored as a number in that player's bid (answering 3 gives bid = 3).
- After everyone has bid, all bids are announced.

R5 TRICKS. Three tricks are played.
- The leader of trick 1 in round r is seat ((r − 1) mod players) + 1.
- The leader of each later trick is the winner of the previous trick.
- In a trick, players act one at a time, starting with the leader and going up in seat order (wrapping from the last seat to seat 1).
- On their turn, each player chooses one card from their own hand. It is removed from the hand and shown to everyone. Any card may be played; there is no requirement to follow.

R6 TRICK WINNER.
- If the trick contains both the Mermaid and the Skull King, the Mermaid's player wins the trick, and that player's bonus increases by 50.
- Otherwise the card with the highest power wins the trick. Because only the Escapes share a power and there are 3 or more players, a winner always exists. If that card is the Skull King, its player's bonus increases by 30 for each Pirate (power 30 or 31) in the trick.
- The winner's tricks_won increases by 1.

R7 SCORING. After the third trick, each player's score changes by:
- bid 1, 2 or 3 and tricks_won equal to bid: +20 × bid + bonus;
- bid 0 and tricks_won 0: +30 + bonus;
- bid 1, 2 or 3 and tricks_won not equal to bid: −10 × |bid − tricks_won|;
- bid 0 and tricks_won above 0: −30.
Bonus counts only when the bid is exact.

R8 END. If round equals 8 after scoring, the game ends. Otherwise the next round starts at R2.

There is no discussion phase. Winner: After round 8, the player with the highest score wins. If two or more players tie for the highest score, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Skull King is a trick-taking game for 2 to 8 players over 10 hands of growing size. Players bid exactly how many tricks they will win, then play tricks with suits, black trump and special cards (Pirates, Mermaids, Escapes, the Skull King). Exact bids score big and capture bonuses, missed bids lose points, and the highest total wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Testing the previous Short Seas variation: no simple policy wins outright. Always bidding 3 misses most hands, and always bidding 0 fails on strong hands. But trick play reduced to 'highest card when I need a trick, lowest when I don't', so choices changed the outcome only a little. The rotating trick-1 leader gave a small seat edge over 8 rounds with 3 players, since 8 is not a multiple of 3."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "There were no suits and nothing to follow. The Skull King and Pirate B were near-certain tricks and cards of 9 or less almost never won, so the deal fixed each hand's trick count. Exact-bid pay rose with the bid (+20 per trick), and the +30 and +50 bonuses went only to holders of the top cards. The per-round ceiling was 30 for a weak hand and 60 to 110 for a strong one, and the deal decided an estimated 50 to 60% of results."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Bidding was little more than counting top cards and play was near-forced, so a competent player reached the ceiling quickly. Beyond that, results were noise from the deal."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Hands were hidden and bids were public, so some inference existed. But 6 to 9 undealt cards were never revealed, which made card counting thin. Sequential play with no follow rule left little to read about opponents."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners and scores follow by arithmetic from the cards played and the bids. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Sequential trick play meant 9 to 12 player choices per round plus the bid, against a limit of 4 choice steps. 'Winner leads the next trick' changes the acting order at runtime, which a flat step list cannot express without many conditional copies. The honest step count was well over 20."
    }
  ],
  "problems": [
    "P1: Sequential play inside each trick gives 10 to 13 choice steps per round, over the limit of 4.",
    "P2: 'The winner of a trick leads the next' changes the turn order at runtime, which needs conditional blocks of steps the engine cannot build.",
    "P3: Per-trick resolution (maximum, Mermaid/Skull King check, Pirate bonus, trick count, card removal) and four-case scoring push the round past 20 steps.",
    "P4: Exact-bid pay grows with the bid, so strong hands have a much higher ceiling than weak ones and the deal decides the winner.",
    "P5: The Skull King capture bonus (+30 per Pirate) and the Mermaid bonus (+50) are large automatic rewards for whoever was dealt those cards.",
    "P6: With sequential, unconstrained play the trick count is almost fixed by the deal, leaving little to plan or out-guess.",
    "P7: Undealt cards are never revealed, so there is little hidden-information inference beyond the bids.",
    "P8: The rotating trick-1 leader over 8 rounds gives seats unequal numbers of leads."
  ],
  "changes": [
    {
      "what": "Every trick is a simultaneous poll: all players pick a card from their hand at the same moment, then all cards are revealed together. The round has exactly 4 choice steps: the bid and three tricks.",
      "why": "This keeps choices within the limit. It also turns each trick into a guessing contest about when opponents will spend their high cards.",
      "fixes": "P1"
    },
    {
      "what": "Leaders and turn order are removed entirely.",
      "why": "Simultaneous tricks need no acting order, so there is no runtime reordering and no seat advantage from leading.",
      "fixes": "P2, P8"
    },
    {
      "what": "Trick resolution becomes a single winner rule with one small bonus, and scoring becomes a single formula. Played cards are removed by the poll itself.",
      "why": "Each trick then costs 3 steps (poll, reveal, resolve), giving 17 steps per round.",
      "fixes": "P3"
    },
    {
      "what": "Every exact bid, of any size including 0, scores a flat +30. A miss costs 10 points per trick of difference.",
      "why": "A weak hand that correctly bids 0 earns exactly as much as a strong hand that correctly bids 3. Points come from predicting your result accurately, not from being dealt power.",
      "fixes": "P4"
    },
    {
      "what": "The Pirate capture bonus is removed. Only one small bonus remains: +10 when the Mermaid captures the Skull King, paid only if the bid is exact.",
      "why": "This keeps the iconic Mermaid-beats-Skull-King moment but shrinks its payoff from 50 to 10. Landing it requires guessing which trick the Skull King will come out in.",
      "fixes": "P5"
    },
    {
      "what": "Simultaneous reveal combined with flat exact-bid scoring.",
      "why": "Middle-strength hands (a 10, 11, 12 or a lone Pirate) must guess when opponents will throw their big cards. They also read the public bids to infer who holds what. A player who needs exactly one trick must time it, and can deliberately waste a strong card where an opponent's card will beat it.",
      "fixes": "P6"
    },
    {
      "what": "After the deal, 3 of the undealt cards are turned face up for everyone to see.",
      "why": "Players can narrow down which top cards are in opponents' hands and cross-check that against the announced bids.",
      "fixes": "P7"
    },
    {
      "what": "The game lasts 10 rounds.",
      "why": "More rounds average out deal variance, and with no seat-based leading there is no rotation to balance. The step budget still fits.",
      "fixes": "P4, P8"
    }
  ],
  "keeps": [
    "Bid exactly how many tricks you will win, scored only on exactness.",
    "Highest card wins the trick, with the special-card hierarchy: Escape loses, Mermaid beats numbers, Pirates beat the Mermaid, the Skull King beats Pirates, and the Mermaid beats the Skull King.",
    "Zero bids as a real strategy.",
    "Hidden hands and public bids.",
    "Highest total after a fixed number of hands wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Simultaneous tricks and flat exact-bid scoring bring the game inside the limits. They also move the skill from holding big cards to predicting and out-timing opponents, which keeps the bid-exactly heart of Skull King."
  },
  "variation": {
    "name": "Skull King: Blind Broadsides",
    "summary": "A short Skull King for 3 to 4 players played over 10 rounds of 3 cards. Players bid their exact trick count after seeing 3 revealed spare cards. Each trick is played by everyone revealing a card at the same moment. Any exact bid scores the same 30 points, so the game is about predicting and timing, not about being dealt the Skull King.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "CARDS. Each card has a power number. The deck holds 18 cards:\n- the numbers 1 to 12 (power equal to the number);\n- two Escapes (power 0);\n- the Mermaid (power 20);\n- Pirate A (power 30);\n- Pirate B (power 31);\n- the Skull King (power 40).\n\nCONSTANTS. rounds = 10, hand_size = 3, tricks per round = 3, revealed cards = 3, bids from 0 to 3.\n\nR1 SETUP. When the game starts, every player's score is 0 and the round counter is 0.\n\nR2 ROUND START.\n- round increases by 1.\n- Every player's tricks_won is set to 0, bonus to 0 and hand to empty.\n- The public list 'revealed' is set to empty.\n\nR3 SHUFFLE. The deck is reset to all 18 cards and shuffled. This is the round's only chance event.\n\nR4 DEAL. Each player receives 3 cards from the top of the deck into a private hand that only they can see.\n\nR5 REVEAL. The next 3 cards of the deck are moved to 'revealed' and shown to everyone. These cards are out of play this round. The remaining undealt cards (3 with 4 players, 6 with 3 players) stay hidden.\n\nR6 BID. All players bid at the same moment, without seeing other bids. The options are exactly 0, 1, 2 or 3, and the choice is stored as the number bid.\n\nR7 ANNOUNCE. All bids are shown to everyone.\n\nR8 TRICKS. Three tricks are played. Each trick has three steps.\n\n(a) PLAY. All players at the same moment choose one card from their own hand. The chosen card is removed from the hand and becomes that player's 'played' card.\n\n(b) SHOW. All played cards are revealed together.\n\n(c) RESOLVE. The trick winner is decided as follows:\n- If the played cards include both the Mermaid and the Skull King, the Mermaid's player wins the trick, even if a Pirate was also played, and that player's bonus increases by 10.\n- Otherwise the card with the highest power wins.\n- Only the two Escapes share a power, and there are at least 3 players, so a unique winner always exists.\n- The winner's tricks_won increases by 1.\n\nR9 SCORING. After the third trick, each player's score changes as follows:\n- if tricks_won equals bid (including bid 0 with 0 tricks): +30 + bonus;\n- otherwise: −10 × |bid − tricks_won|, and the bonus is lost.\n\nR10 END. If round equals 10, the game ends. Otherwise the next round starts at R2.\n\nThere is no discussion phase.",
    "objective": "After round 10, the player with the highest score wins. If two or more players tie for the highest score, the game is a draw.",
    "expected_effect": "Every exact bid is worth the same 30, so a weak hand bidding 0 is as valuable as a Skull King hand bidding 3. The deal matters little, and the skill is in reading your hand against the revealed cards and the public bids. Middle hands must time their one good card for a trick where opponents are likely holding back, and must dump losers where someone who announced a high bid will win. The Mermaid holder tries to guess the Skull King's trick for +10, while the Skull King holder tries to dodge the Mermaid. Simple policies lose:\n- Always bid 0 and play lowest scores +30 on weak hands but misses whenever dealt the Skull King or Pirates. A player who bids accurately beats it.\n- Always bid 3 and play highest rarely hits.\n- Random play misses most bids.\nThere is no seat edge because nothing is sequential. Talk is left out because players' interests do conflict, but every claim would be cheap and unverifiable. The public bids already carry the real signal, a costly commitment about one's hand, while free talk would only add noise and steps."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 10,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
