# 21 design

- time: 2026-10-28T03:14:08+00:00 (102.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 8d44105b551ff464, reply sha256 1dc166df6743a232

## Sent

````
Original game: Mariáš
Players in the original: 3 to 3

Original rules:
Mariáš is played with 32 cards A-10-K-O-U-9-8-7 ranking A,10,K,O,U,9,8,7 except in Betl/Durch. Three players receive cards, eldest hand views 7 cards and chooses trump, then receives 5 more and discards 2. The other two form a defending partnership. Play is 10 tricks. Must follow suit, must head the trick if able, must trump if cannot follow. Highest trump or highest of led suit wins. Winner leads and keeps won tricks in order. Aces and Tens are 10 each, last trick is 10, total 90. King+Ober of same suit in one hand is a marriage, worth 40 if trump else 20, if its holder wins a trick. Defenders can double with Flek, declarer can redouble. Hearts trump doubles stakes. Special contracts: Betl win no tricks, Durch win all tricks, 7 win last trick with lowest trump, 100 score 100+ points.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Simplify the trick mechanics so each play step is easy to validate and record.

1. Drop the 'must beat' duty in (a) and (b). Keep plain follow-suit: follow the led suit if able, otherwise trump if able, otherwise any card.
2. Replace the illegal-card fallback with a simple rule, such as 'the first legal card in your hand in code order', so the played card always exists and always lands in the trick list.
3. State that the trick winner is the card with the highest key (rank + 10 if trump + 5 if led suit), and the seat that played it. Record the winning seat directly while the cards are played: keep a running best key and best seat updated after each card, rather than searching the trick list afterwards.
4. Say explicitly that the full 20-card deck is rebuilt and reshuffled at the start of every deal.
5. Simplify the invalid-suit default for bidding to a fixed suit (for example the suit of the player's first card, or Acorns), rather than the suit with the most cards.
6. Consider dropping marriages, or limiting them to the trump suit only, to cut announcement and tally steps.

Keep the scoring formula, which is sound and zero-sum.
the game file could not be built. What the checks found on the attempts:
- attempt 1: playing it with random seats failed: seed 1, 3 players: the match crashed: CalcError: 'deck[min(int(uniform(0, len(deck))), len(deck) - 1)]': list index out of range
- attempt 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (deal_result, last_card, trump) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 3: playing it with random seats failed: seed 1, 3 players: the match crashed: CalcError: '[((leader - 1 + i) % 3) + 1 for i in [0, 1, 2] if (trick_cards[i] % ranks_per_suit) + (trump_key_bonus if int(trick_cards[i] / suit_code_multiplier) == trump_idx else 0) + (led_suit_key_bonus if int(trick_cards[i] / suit_code_multiplier) == led_suit else 0) == win_key][0]': list index out of range
- attempt 4: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {held} (in `prompt`: "Your hand: {held}. Bid in secret: choose one 'BID SUIT', where BID is PASS or 50 to 150 in"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {held} (in `prompt`: "Your hand: {held}. Bid in secret: choose one 'BID SUIT', where BID is PASS or 50 to 150 in"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {held} (in `prompt`: "Your hand: {held}. Bid in secret: choose one 'BID SUIT', where BID is PASS or 50 to 150 in"); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- attempt 5: playing it with random seats failed: seed 1, 3 players: the match crashed: CalcError: '[(leader - 1 + i) % len(players) + 1 for i in positions if trick_cards[i] == win_card][0]': list index out of range

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Mariáš is a Czech three-player trick-taking game with a 32-card deck. A declarer picks trump and a contract and plays against two defenders who are partners. Players must follow suit, head the trick and trump when void. Aces and Tens are worth 10 each, the last trick is worth 10, and marriages add points. Flek and re double the stakes, and there are special contracts (Betl, Durch, Seven, Hundred).",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always declaring loses against weak hands, and always passing gives up every strong hand. Flek every time pays double whenever the declarer makes the contract. The forehand advantage is balanced over a full rotation. Choices of trump, contract and card play decide most deals."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Over many deals strong players beat weak ones reliably, through card counting, partnership defence and judging when to bid or flek. Any single deal is heavily card-driven."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "The game is deep and unsolved: inferring hands from play, defensive signalling, bid judgment and doubling psychology. A beginner who follows suit and bids only strong hands still scores."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must infer cards from the bidding and from voids shown in play, and plan over 10 tricks. Defenders must also cooperate without seeing each other's cards."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card points, marriages and contract success are all arithmetic, and the stakes follow from the multipliers."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Ten tricks with must-head rules, a talon exchange, marriages, four special contracts and sequential flek/re chains exceed the step and choice limits. The previous built version crashed five times: drawing from an emptied deck, empty list searches for the trick winner, and unfilled {held} placeholders. It also showed empty bookkeeping fields to players."
    }
  ],
  "problems": [
    "P1: The full rules (32 cards, 10 tricks, talon exchange, marriages, Betl/Durch/Seven/Hundred) need far more steps and choices per round than the engine allows.",
    "P2: Dealing by repeated random index draws from a shrinking deck crashed with 'list index out of range' when the deck ran short or was not rebuilt.",
    "P3: Finding the trick winner by searching the trick list afterwards crashed with empty list comprehensions.",
    "P4: The 'must head the trick' duty and the illegal-card fallback made each play step hard to validate, and could produce a card that never landed in the trick.",
    "P5: Prompts embedded a {held} placeholder that the engine cannot fill, so players saw literal braces.",
    "P6: Internal bookkeeping fields (deal_result, last_card, trump before it was set) were printed empty to players.",
    "P7: The forehand who must name trump has a built-in edge or burden within a deal, so balance needs even rotation.",
    "P8: A sequential flek, then re, then further doubling chain costs several choice steps."
  ],
  "changes": [
    {
      "what": "Shrink the deck to 12 cards: four suits (Hearts, Bells, Leaves, Acorns) times three ranks (A, 10, K). Deal 4 cards each with no talon, for 4 tricks per deal. Drop marriages and the special contracts. Card values stay A=10 and 10=10, and the last trick stays 10, so the total is still 90.",
      "why": "This keeps the 90-point economy, the trump choice and follow/trump play, while one trick fits in one round with at most 4 choice steps.",
      "fixes": "P1"
    },
    {
      "what": "At the start of each deal, build a fresh list of the 12 card codes 0 to 11 and shuffle it once. Seat 1 takes positions 1-4, seat 2 positions 5-8, seat 3 positions 9-12. There are no index draws from a shrinking deck.",
      "why": "A fixed-size permutation sliced at fixed positions cannot run out, and it is the round's only random draw.",
      "fixes": "P2"
    },
    {
      "what": "Track the trick winner with a running best_key and best_seat. The leader's card sets them. Each later card replaces them only if its key is strictly greater. The key is rank (K=0, 10=1, A=2), plus 10 if trump, plus 5 if of the led suit.",
      "why": "No list search is needed, so nothing can come back empty.",
      "fixes": "P3"
    },
    {
      "what": "Use plain follow-suit: follow the led suit if able, otherwise trump if able, otherwise any card. An illegal or unheld card is replaced by the lowest-code legal card. A hand always has a card when its owner plays.",
      "why": "Each play is one validated step, and the played card always exists and always enters the trick.",
      "fixes": "P4"
    },
    {
      "what": "Prompts contain no placeholders except {seat} and {value}. Each player's own hand is shown through their private hand attribute in their state view.",
      "why": "Players never see unfilled braces.",
      "fixes": "P5"
    },
    {
      "what": "Hide the bookkeeping attributes (best_key, led_suit, deck, the bid's raw fields). Show only hand, score, trump, declarer, contract, multiplier, cards in the current trick, trick number and the points taken so far.",
      "why": "The state view holds only usable information.",
      "fixes": "P6"
    },
    {
      "what": "Play 9 deals, with the eldest hand rotating 1, 2, 3, 1, ... so each seat is eldest exactly 3 times. The eldest cannot pass: an invalid entry or PASS from the eldest counts as '50 A'. Bid ties go to the player nearest the eldest in seat order.",
      "why": "This preserves Mariáš's forced forehand while spreading that burden and privilege evenly.",
      "fixes": "P7"
    },
    {
      "what": "Make flek and re one simultaneous poll after trick 1. Each defender says FLEK or NO, and the declarer says RE or NO at the same moment. Any flek doubles the stake. RE doubles it again only if at least one flek was given.",
      "why": "One choice step replaces a sequential chain, and the declarer must predict whether the defenders will flek.",
      "fixes": "P8"
    }
  ],
  "keeps": [
    "Three players: one declarer against two defenders in a temporary partnership",
    "The declarer names trump; must follow suit, else must trump",
    "Aces and Tens are 10 each and the last trick is 10, for a total of 90 card points",
    "Bidding a contract level with a forced forehand",
    "Flek and re doubling",
    "Hearts as trump doubles the stakes",
    "Zero-sum settlement: the declarer is paid by or pays each defender"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "A reduced 12-card, 4-trick Mariáš keeps the hidden hands, the bidding judgment and the partnership defence. With running-key trick resolution and a fixed-slice deal it fits the step limits and removes every crash source found."
  },
  "variation": {
    "name": "Malý Mariáš (Little Mariáš)",
    "summary": "A 12-card, 4-trick Mariáš for three players over 9 deals. Each deal, players bid in secret for the right to declare a trump suit and a card-point target out of 90. The two others defend together. Flek and re double the stakes, Hearts doubles them again, and the highest running total after 9 deals wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "CARDS. There are 12 cards: four suits, Hearts (H), Bells (B), Leaves (L) and Acorns (A), each with three ranks, Ace (A), Ten (10) and King (K). A card is written rank then suit, for example AH, 10L, KB. Internally, card code = 3 x suit index + rank index, with suits H=0, B=1, L=2, A=3 and ranks K=0, 10=1, A=2. Rank order within a suit is A > 10 > K. Card points: each Ace 10, each Ten 10, each King 0. Whoever wins the 4th (last) trick of a deal gets 10 more. The total per deal is 90.\n\nSTRUCTURE. The match is 9 deals of 4 tricks each, which is 36 rounds. Each round is one trick. The eldest hand of deal d is seat ((d-1) mod 3)+1, so seats 1, 2, 3, 1, 2, 3, 1, 2, 3. Every player starts with score 0.\n\nWHAT PLAYERS SEE. Each player sees their own hand (private), all scores, the current deal and trick number, the declarer, contract and trump once set, the stake multiplier, the cards played so far in the current trick with who played them, the card points taken so far by the declarer and by the defenders, and every public announcement. Internal working values are not shown.\n\nROUND STEPS (steps marked [trick 1] or [trick 2] happen only in that trick of a deal):\n1. [trick 1] Deal. Build the list of the 12 codes 0-11, shuffle it once, and give positions 1-4 to seat 1, positions 5-8 to seat 2 and positions 9-12 to seat 3. Reset the declarer points, defender points and multiplier to 1.\n2. [trick 1] Bid (simultaneous, secret). Each player answers 'PASS' or 'N S', where N is 50, 60, 70, 80 or 90 and S is H, B, L or A. The eldest may not pass: PASS or any invalid answer from the eldest counts as '50 A'. An invalid answer from anyone else counts as PASS.\n3. [trick 1] Resolve the bid. The highest N becomes the declarer, with contract N and trump S. On a tie, the tied player first in seat order starting from the eldest wins. The other two are defenders. Set base stake = N/10 - 4 (so 50→1, 60→2, 70→3, 80→4, 90→5). The declarer leads trick 1. Announce all bids, the declarer, the contract and the trump.\n4. [trick 2] Flek poll (simultaneous). Each defender answers FLEK or NO, and the declarer answers RE or NO. Invalid answers count as NO.\n5. [trick 2] Resolve. If at least one defender said FLEK, the multiplier is doubled. If, in addition, the declarer said RE, it is doubled again. Announce all answers and the multiplier.\n6. First card. The leader names a card from their hand.\n7. Resolve the first card. If the card is not in the leader's hand, the lowest-code card in their hand is played instead. Remove it from the hand and add it to the trick. Set led suit to its suit. Set best_key = rank index + (10 if its suit is trump) + 5, and set best_seat = the leader. Announce the card.\n8. Second card. The next seat clockwise, (leader mod 3)+1, names a card.\n9. Resolve the second card. The card is legal if: it is of the led suit; or the hand has no led-suit card and the card is trump; or the hand has neither led-suit cards nor trumps. If the named card is not held or not legal, play instead the lowest-code held card of the led suit, else the lowest-code held trump, else the lowest-code held card. Remove the card from the hand and add it to the trick. Its key = rank index + (10 if trump) + (5 if of the led suit). If its key is greater than best_key, set best_key to it and best_seat to this seat. Announce the card.\n10. Third card. The next seat names a card.\n11. Resolve the third card exactly as in step 9.\n12. Award the trick. Add the trick's card points, plus 10 if this is trick 4, to the declarer's points if best_seat is the declarer, otherwise to the defenders' points. Set leader = best_seat. Announce the winner and the running points.\n13. [trick 4] Settle the deal. Stake = base stake x multiplier x (2 if trump is Hearts, else 1). If the declarer's points are at least the contract N, the declarer gains 2 x stake and each defender loses stake. Otherwise the declarer loses 2 x stake and each defender gains stake. Announce the result and the scores.\n14. Advance. Add 1 to the trick number. After trick 4, reset it to 1, add 1 to the deal number and rotate the eldest. After deal 9, the match ends.\n\nThere is no discussion phase. Hands are always non-empty when their owner must play, because each player plays exactly one card per trick and holds 4 cards for 4 tricks.",
    "objective": "After 9 deals, the player with the highest score wins. If two or three players tie for highest, those players draw. Scores are the sum of the zero-sum deal settlements in step 13.",
    "expected_effect": "Bidding becomes a real judgment: hand strength, choice of trump, the risk of a Hearts contract and the stake level. The forced eldest must handle weak hands, which is spread evenly by rotation. The simultaneous flek/re poll rewards reading hand strength from the bids. Defenders must cooperate within a deal through card play alone (they read each other's discards and voids), while remaining rivals for the overall win, since both gain or lose equally in a deal but only one can finish first. Card counting over 4 tricks with 12 known cards rewards inference: by trick 3 a careful player can often deduce the remaining hands exactly. Simple policies all lose. Always passing leaves the eldest stuck with forced 50s and gives up strong hands. Always bidding 90 fails most deals at the maximum stake. Always flekking pays double whenever the declarer bid soundly. Always re-ing costs the declarer double whenever a flekked contract fails. Deal luck stays, but 9 deals and the freedom to bid low or pass let good players limit its effect. Talk is left out: the only conflict within a deal is declarer against defenders, and public talk between the defenders would reveal their hands to the declarer as well."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
