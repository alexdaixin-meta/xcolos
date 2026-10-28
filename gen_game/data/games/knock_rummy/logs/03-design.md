# 03 design

- time: 2026-10-28T04:04:21+00:00 (55.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c969fb4d8fe229c0, reply sha256 c038bb0310a52c1c

## Sent

````
Original game: Knock Rummy
Players in the original: 2 to 6

Original rules:
Deal 10 cards each for 2 players, 7 for 3-4 players, 6 for 5-6 players. Place remainder as stock, flip top as upcard discard pile. On turn draw the upcard or stock top, then you may knock before discarding to end the hand. Discard one. After knock, knocker lays melds (3-4 of a kind or 3+ sequence same suit) and announces unmatched count (face =10, ace=1, others pip value, though variations exist). Others do same. Lowest unmatched wins difference from each opponent. Knocker going rummy (zero unmatched) gets +25 bonus per opponent. If knocker ties, tying player wins. If knocker is not lowest, knocker pays 10 penalty plus difference to the lowest player. If stock empties, next player may take discard top or flip discard without shuffling to new stock.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Thoughtless policies, using the WINNER RULE with deadwood estimates. A random 5-card hand averages 27.5 points; the chance of holding a meld is roughly 30%; under steady play deadwood falls to about 8-15 within a few turns. (1) 'Always knock at once': knocker deadwood k is about 27 and defender deadwood d is about 25 (the defender drew nothing yet but may hold a meld), so k>=d about half the time. When that happens the knocker pays (k-d)+10, about 15; when k<d the knocker gains d-k, about 8. Net is about -4 per hand, and the policy loses against sensible and random play. It fails as a policy. (2) 'Never knock': every hand runs to exhaustion. A sensible opponent knocks only when its estimate is well below the defender's, and scores d-k each time. This policy loses to sensible play and draws or wins against random play, so it is not a never-lose policy. (3) 'Always draw stock, discard highest': this ignores low upcards that the sensible player takes, so it loses on average. (4) 'Always take upcard': it often takes high discards, so it loses. Dominance: no option is strictly better whatever the opponent does. Knocking early wins only against a slow opponent; a low upcard is good unless it reveals your hand. The payoff ordering is stated correctly: a failed knock costs 10 more than a successful knock earns at the same margin, which deters reckless knocks. Rummy needs a 5-card run in a 5-card hand. That is rare but valid, and the +20 is not dominant. SEAT EDGE (the failure): the starter of a hand sees 6 cards first and gets the first chance to knock. A starts hands 1, 3, 5 and so on, so at match end A has started either the same number of hands as B or one more, never fewer. The edge always runs toward A. It is made worse by the turn-40 'final showdown'. If a hand is dealt on turn 38-40, its starter alone gets one or two draws or discards before a forced no-knocker showdown. That is almost pure deal luck tilted to the starter, and with alternation the starter is A whenever the hand count is odd. Expected size is a few points per match against a typical margin of 10-20, which is enough to be a systematic bias for one seat. Both players can realistically win, but the seats are not symmetric.
- change: Remove the seat bias in hand starts. Make the starter of each new hand the player who has started fewer hands so far, with ties going to the player with the LOWER total score instead of always to A. Alternatively, offer the non-starter the first chance at the initial upcard in each hand, as in classic gin.
- change: Neutralise the truncated final hand. Deal no new hand if fewer than 6 turns remain; the remaining turns pass with no action and the match is scored as it stands. Or score a turn-40 final showdown only if the current hand has lasted at least 4 turns, and void it otherwise.
The variation that was reviewed: Knock Rummy Duel: DECK: 30 cards: values 1 to 10, three copies of each value, no suits. A card is worth its value.

DEALING A HAND:
- Shuffle all 30 cards.
- Deal 5 cards face down to each player.
- Turn the next card face up to start the discard pile; its top card is the 'upcard'.
- The other 19 cards form the face-down stock.
- In the first hand, Player A starts. In each later hand, the player who did not start the previous hand starts.

MELDS:
- A meld is 3 or more cards of equal value (at most 3, since there are only 3 copies), or 3 or more cards of consecutive values, such as 4-5-6 or 6-7-8-9. Values do not wrap: 10 is not next to 1.
- A 5-card hand can contain at most one meld.
- Deadwood is the total value of the hand's cards that are not in the declared meld.

A TURN: The match lasts exactly 40 turns, and players alternate turns.
1. DRAW: The active player chooses either the upcard or the top card of the stock. Both players are told which source was used and, if it was the upcard, which card was taken. A stock card stays secret.
2. DISCARD (and optional KNOCK): The active player discards one of their 6 cards face up onto the discard pile. That card becomes the new upcard. At the same time, they may announce a knock.
3. A showdown happens immediately if any of these is true:
   - the active player knocked;
   - the stock now holds 2 or fewer cards (an 'exhausted hand', no knocker);
   - this was turn 40 (a 'final showdown', no knocker).
   Otherwise play passes to the other player.

SHOWDOWN:
- Both players simultaneously declare which cards in their 5-card hand form their meld, or 'none'.
- Each declaration is checked. An invalid declaration counts as 'none'.
- Each player's deadwood = sum of hand values minus the sum of their valid declared meld.
- Hands are revealed.

SCORING:
- If there was a knocker, let k be the knocker's deadwood and d the defender's deadwood.
  - If k < d: the knocker scores d - k. If k = 0, the knocker also scores a rummy bonus of 20.
  - If k >= d: the defender scores (k - d) + 10.
- If there was no knocker (exhausted hand or final showdown): the player with the lower deadwood scores the difference. On a tie, nobody scores.

AFTER A SHOWDOWN: If fewer than 40 turns have been played, deal a new hand, which starts on the next turn. Turns keep counting across hands.

INFORMATION:
- Each player knows their own hand, the whole discard pile, every pickup from the discard pile, and both scores.
- The stock order and the opponent's hand are hidden. Winner: After turn 40 and its showdown, the player with the higher total score wins. Equal totals are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Knock Rummy is a draw-and-discard card game. Players build melds (sets or runs) to cut their unmatched 'deadwood'. Any player may knock to end the hand: the lowest deadwood wins the difference, and a knocker who is not lowest pays a penalty. The reviewed variation, Knock Rummy Duel, is a two-player version with a 30-card suitless deck, 5-card hands and a 40-turn match, but its seats are biased toward Player A.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "No thoughtless policy dominates. 'Always knock at once' nets about -4 per hand. 'Never knock' loses to a sensible knocker. 'Always stock' and 'always upcard' both lose on average. But the seats are not symmetric. A starts hands 1, 3, 5 and so on, so A has started as many hands as B or one more, never fewer. A hand dealt on turns 38-40 gives its starter one or two actions and then a forced showdown that is almost pure deal luck, and that starter is A whenever the hand count is odd. Expected bias is a few points per match against typical margins of 10-20."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Choosing which card to keep, when to take a revealed upcard and when to knock all reward skill over several hands. Two things add noise that skill cannot touch: the truncated final hand, and the variable number of hands each player starts."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still melds and scores some hands. A strong player can improve without limit at tracking the discard pile, reading the opponent's pickups and judging the knock threshold against the defender's likely deadwood."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The opponent's hand and the stock order are hidden. Upcard pickups and discards are signals to infer from. Knocking is a risk judgement about the opponent's likely deadwood, and an undercut costs a penalty of 10."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Deadwood and scores are plain sums. The winner is the higher total."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and has no board. Its weaknesses are the variable hand count, the stock-exhaustion rule, which rarely triggers, and the 40-turn cutoff that slices through a hand. These make the flow uneven and the end of the match arbitrary."
    }
  ],
  "problems": [
    "Seat bias in hand starts: with strict alternation and a 40-turn cutoff, A always starts as many hands as B or one more.",
    "The truncated final hand: a hand dealt near turn 40 ends in a forced showdown after one or two actions, which is deal luck tilted to its starter.",
    "The starter of each hand acts first and gets the first knock chance, with no compensation for the non-starter.",
    "The match length in hands varies, so luck from a short last hand can decide a close match.",
    "Each showdown needs players to declare melds, which adds a choice step and room for invalid declarations without testing any strategy."
  ],
  "changes": [
    {
      "what": "Replace the 40-turn match with exactly 4 hands. A starts hands 1 and 3; B starts hands 2 and 4.",
      "why": "Each player starts exactly the same number of hands, so neither seat gets an extra start.",
      "fixes": "Seat bias in hand starts: with strict alternation and a 40-turn cutoff, A always starts as many hands as B or one more."
    },
    {
      "what": "Cap each hand at 10 turns, 5 per player. If nobody has knocked, the hand ends in a no-knocker showdown after turn 10. Remove the stock-exhaustion rule: at most 10 of the 19 stock cards can be drawn, so it can never trigger.",
      "why": "Every hand has the same full length and both players get equal turns in it. No hand is cut short by a global turn limit, and the match is at most 40 turns.",
      "fixes": "The truncated final hand: a hand dealt near turn 40 ends in a forced showdown after one or two actions, which is deal luck tilted to its starter."
    },
    {
      "what": "Give the non-starter first refusal on the initial upcard, as in classic gin. Before the starter's first turn, the non-starter may take the upcard and discard one card, without knocking.",
      "why": "This offsets the starter's first-move and first-knock advantage within each hand. It also adds an early signal: taking or refusing the upcard reveals something about the non-starter's hand.",
      "fixes": "The starter of each hand acts first and gets the first knock chance, with no compensation for the non-starter."
    },
    {
      "what": "Fix the match at 4 equal-length hands instead of a variable number.",
      "why": "Every match has the same structure, so the result reflects four full hands of play rather than a short leftover hand.",
      "fixes": "The match length in hands varies, so luck from a short last hand can decide a close match."
    },
    {
      "what": "Compute each player's deadwood automatically at showdown as the lowest achievable: the hand total minus its best single meld.",
      "why": "Meld declaration is bookkeeping, not strategy. Removing it saves a choice step and rules out accidental invalid declarations.",
      "fixes": "Each showdown needs players to declare melds, which adds a choice step and room for invalid declarations without testing any strategy."
    }
  ],
  "keeps": [
    "Draw from the upcard or the stock, then discard face up.",
    "An optional knock, which ends the hand immediately.",
    "Melds of three of a kind or runs of 3 or more consecutive values, with deadwood scored by card value.",
    "The knocker scores the difference; a rummy (zero deadwood) earns a +20 bonus.",
    "The undercut penalty: a knocker who is not strictly lower pays the difference plus 10 to the defender.",
    "Hidden hands and stock, a public discard pile and public upcard pickups.",
    "The 30-card suitless deck (values 1-10, three copies each) and 5-card hands."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core knock decision is a genuine inference-and-risk problem. Only the seat structure and the match ending needed fixing, and both fit inside the platform's limits."
  },
  "variation": {
    "name": "Knock Rummy Duel: Even Hands",
    "summary": "A two-player knock rummy match of exactly 4 hands, each capped at 10 turns. Starts alternate evenly and the non-starter gets first refusal on the opening upcard. Players draw, discard and decide when to knock against an opponent whose hand they must infer.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 30 cards, values 1 to 10, three copies of each value, no suits. A card is worth its value.\n\nMATCH: The match is exactly 4 hands. Player A starts hands 1 and 3. Player B starts hands 2 and 4. Scores carry across hands. Both start at 0.\n\nDEALING A HAND:\n1. Shuffle all 30 cards.\n2. Deal 5 cards face down to each player.\n3. Turn the next card face up to start the discard pile. The top card of the discard pile is the 'upcard'.\n4. The remaining 19 cards form the face-down stock.\n\nOPENING OFFER: Before the starter's first turn, the non-starter may take the upcard. If they do, they discard one of their 6 cards face up, and that card becomes the new upcard. If they decline, nothing changes. Both players are told which happened and which cards were taken and discarded. This offer is not a turn, and no knock is allowed with it.\n\nTURNS: Within a hand, players alternate turns, beginning with the starter. A hand has at most 10 turns, 5 per player. Each turn:\n1. DRAW: The active player takes either the upcard or the top card of the stock. Both players are told which source was used and, if it was the upcard, which card. A stock card stays secret.\n2. DISCARD AND OPTIONAL KNOCK: The active player discards one of their 6 cards face up, and it becomes the new upcard. At the same time, they may announce a knock.\n3. If the active player knocked, a showdown happens with them as knocker. If this was the 10th turn of the hand and nobody knocked, a showdown happens with no knocker. Otherwise play passes to the other player.\n\nMELDS AND DEADWOOD:\n- A meld is 3 cards of equal value, or 3 or more cards of consecutive values, such as 4-5-6 or 6-7-8-9. Values do not wrap: 10 is not next to 1.\n- A 5-card hand contains at most one meld.\n- At showdown, each player's deadwood is computed automatically as the lowest possible: the sum of their 5 cards minus the sum of the meld that gives the smallest remainder. With no meld, it is the sum of all 5 cards.\n- Both hands are then revealed.\n\nSCORING A SHOWDOWN:\n- With a knocker, let k be the knocker's deadwood and d the defender's deadwood.\n  - If k < d, the knocker scores d - k. If k = 0, the knocker also scores a rummy bonus of 20.\n  - If k >= d, the defender scores (k - d) + 10.\n- With no knocker (10-turn cap reached), the player with the lower deadwood scores the difference. On a tie, nobody scores.\n\nAFTER A SHOWDOWN: If fewer than 4 hands have been played, deal the next hand. After the 4th hand's showdown, the match ends.\n\nINFORMATION: Each player knows their own hand, the whole discard pile, every upcard pickup, which hand and turn it is, and both scores. The stock order and the opponent's hand are hidden until showdown.",
    "objective": "After the 4th hand's showdown, the player with the higher total score wins. Equal totals are a draw.",
    "expected_effect": "Each player starts exactly 2 hands, and every hand has the same 10-turn length with 5 turns each, so neither seat has a structural edge and no truncated end-hand exists. First refusal on the opening upcard offsets the starter's first knock chance and adds an early read on the non-starter's hand. Simple policies still lose. Knocking at once gets undercut about half the time and nets about -4 per hand. Never knocking concedes d - k to a sensible knocker in every hand it trails, with no chance to strike first. Always taking from the stock gives up low upcards, and always taking the upcard picks up high cards and reveals the hand. The 10-turn cap adds a timing question: knock now while slightly ahead, or wait for the guaranteed no-penalty showdown, judging what the opponent's pickups and discards imply about their deadwood. There is no talk phase: this is a two-player zero-sum game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
