# 03 design

- time: 2026-10-28T01:44:50+00:00 (79.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 deb690e636e50cc7, reply sha256 c8a6cb28a261f958

## Sent

````
Original game: Bastard Brag
Players in the original: 3 to 10

Original rules:
Deal 3 cards face down to each player and an extra 3-card hand to the table, two face down one face up. Ranking: prial (3-3-3 highest), running flush, run, flush, pair, high card, with 3-2-A high and suit tie-break spades>hearts>diamonds>clubs for lives game. Lives version: each player has 3 lives. Clockwise, on turn exchange one card with table (if you take face-up you must leave face-up, if face-down exchange is hidden) or swap whole hand for table hand turning one of yours face up. After first round you may knock to keep hand. After knock each other gets one final exchange. All show, worst hand loses a life, zero lives eliminated, last remains wins. Betting version: ante, two exchange rounds (first must exchange, second may pass), then Brag betting with raises until one remains or two-player pay-double-to-see.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: (1) MISSING END CASE. Showdown rule: 'Every player with the lowest score (all tied players if several) loses 1 life.' With 2 remaining players at 1 life each who tie for lowest, or 3 players all at 1 life tying, every remaining player reaches 0 and is eliminated. The END rule only covers 'only one player remains' or round 40. The design does not say who wins when zero players remain. A knocker on 2 lives in the 4-player game can also be eliminated alongside others. (2) CONTRADICTORY ROUND DEFINITION. 'Each round is one turn of the active player', yet 'AFTER A KNOCK: In the same round, each other active player ... makes one final action'. A knock round therefore contains up to 4 player actions, and the 40-round cap and forced-showdown count ('every active player has taken 2 turns ... at the end of that round') are ambiguous about what a round is. (3) STEP BUDGET IMPLAUSIBLE. A knock round with 4 players needs: knocker choice, 3 final-action choices (each with action type, own card, slot and exposed card, applied through table/hand updates), a reveal, scoring of 4 hands (each needing prial, run and pair tests, sorting and calc, with no lookup operation, roughly 4-6 steps per hand), finding the minimum, life loss with the knocker doubling, elimination, then shuffling and dealing 15 cards to hands and slots and advancing the starter. That is far over 19 steps. The choice limit of 4 is only met if each action is one compound choice. (4) MINOR AMBIGUITIES. It does not say whether runs wrap (9-1-2). It does not say whether the new deal's shuffle happens in the same round as the showdown (the random-draw budget allows only 1 per round). It does not say whether a KNOCK counts as one of the '2 turns'. (5) TALK. There is no talk phase. This is acceptable here, because inference comes from mandatory announcements and everyone's interests conflict. No board, clock or judge is needed.
- change: Add a simultaneous-elimination rule, e.g. 'If every remaining player would reach 0 lives, those players instead stay at 1 life and the deal is replayed' or 'the player with the higher score at that showdown wins; if equal, draw'.
- change: Redefine a round consistently, e.g. 'a round is one full clockwise pass in which every active player takes one action'. A knock then ends the round, and the knock's final actions are that round's remaining turns. Restate the forced showdown and the 40-round cap in these terms.
- change: Bring the step budget within 20. Precompute hand score with a single calc formula per hand, or reduce to 3 players fixed. Move the redeal (shuffle plus dealing) into the next round's opening so showdown scoring and dealing do not share one round. Show the step list to prove it fits.
- change: State that runs do not wrap (9-1-2 is not a run), that a KNOCK counts as a turn for the 2-turn limit, and that each action (type, own card, slot, exposed card) is made as one compound choice.
The variation that was reviewed: Knock Brag: DECK: 36 cards, four copies each of the values 1, 2, 3, 4, 5, 6, 7, 8, 9. There are no suits.

LIVES: With 3 players each starts with 3 lives. With 4 players each starts with 2 lives. A player at 0 lives is eliminated and takes no further part.

HAND SCORE (computed for every hand at showdown):
- Prial (three equal values): 300 + value, except 3-3-3 scores 310.
- Run (three consecutive values, such as 4-5-6): 200 + highest value, except 1-2-3 scores 210.
- Pair (exactly two equal): 100 + 10 × the pair value + the odd card.
- High card (anything else): the sum of the three cards.
Higher score is better.

DEALING: At the start of each deal the deck is shuffled (one random draw). Each active player gets 3 cards face down; only they see their own cards. Three cards go to the table: table slot U face up (everyone sees it) and table slots D1 and D2 face down (nobody sees them). The first deal starts with seat 1. Each later deal starts with the next active player clockwise from the previous deal's starter.

TURNS: Each round is one turn of the active player. Turns go clockwise among active players. On your turn choose exactly one action:
(a) TAKE UP: swap one of your cards for the face-up card U. The card you give becomes the new face-up U. Announce: 'X took the face-up [value] and left a face-up [value]'.
(b) BLIND: swap one of your cards for D1 or D2 (you choose which) without seeing it first. Your card goes face down into that slot. You now see the card you received. Announce: 'X made a blind swap'.
(c) WHOLE HAND: take all three table cards into your hand; you now see all three. Your old three cards become the table hand. You choose which of them goes face up as U; the other two go face down as D1 and D2. Announce: 'X swapped the whole hand and exposed a [value]'.
(d) KNOCK: keep your hand and make no exchange. You may knock only when every active player has had at least one turn in the current deal. Announce: 'X knocks'.

AFTER A KNOCK: In the same round, each other active player in clockwise order from the knocker makes one final action of type (a), (b) or (c). They may not knock or pass. Each final action is announced as above. Then the showdown happens.

FORCED SHOWDOWN: If nobody has knocked and every active player has taken 2 turns in the current deal, the showdown happens at once at the end of that round, with no further exchanges and no knocker.

SHOWDOWN: All hands are revealed and scored. Every player with the lowest score (all tied players if several) loses 1 life. If the knocker is among them, the knocker loses 2 lives instead. Players reaching 0 lives are eliminated. If more than one player remains, a new deal begins with the next starter.

END: The game ends when only one player remains, or at the end of round 40, whichever comes first. Winner: If only one player remains, that player wins. If round 40 ends with more than one player remaining, the player with the most lives wins. Ties on lives go to the higher hand score at the most recent showdown among the tied players. If still tied, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Bastard Brag is a 3-card Brag variant. Players take turns swapping cards with a three-card table hand (one card face up, two face down) or swapping their whole hand for it, until someone knocks. In the lives version the worst hand at showdown loses a life, and the last player with lives wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Only the single worst hand is punished, so no fixed policy is safe. Always knocking at once locks in a random hand and risks the penalty. Never knocking leaves the timing to others. Always taking the face-up card tells everyone what you hold. Seat order rotates, so no seat keeps an edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Any one deal is noisy. Over several lives, though, the better player wins more often: they track what others take and leave, choose between blind and open swaps, and time the knock. The betting version adds bluffing, but it relies on chips and pot sizes the platform cannot reward."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still survives deals, because only the worst hand loses. A strong player improves through card counting, reading the exposed cards, knock timing and judging when a mediocre hand is good enough."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the face-down table cards are hidden. The announcements (what was taken, what was left, what was exposed) let a player infer what opponents hold. Knocking is a bet on where you rank among the hidden hands."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Hand ranking and life loss are mechanical. Suit tie-breaks and flushes add bookkeeping but need no judge."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Turn-based and text-only. However, 3 to 10 players, a 52-card deck with suits and flushes, open-ended knocking and the betting version push past the step limits and need a lookup the engine lacks. The previous variation also left several cases undefined and was over its step budget."
    }
  ],
  "problems": [
    "The previous variation did not say who wins when every remaining player ties for the lowest score and would reach 0 lives, nor what happens when a knocker is eliminated alongside others.",
    "The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous.",
    "The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round.",
    "The previous variation did not say whether runs wrap, whether the shuffle shares a round with the showdown (only 1 random draw is allowed per round), or whether a knock counts as a turn.",
    "With knocks allowed from any seat mid-pass, players who acted earlier in the pass would get no final action, or the round would have to wrap around.",
    "Suits, flushes and suit tie-breaks in the original need lookup tables the engine lacks.",
    "The betting version's chip pot cannot be rewarded by a platform that only decides a winner."
  ],
  "changes": [
    {
      "what": "Fix the game at exactly 3 players, each with 3 lives.",
      "why": "This caps a round at 3 choices and 3 hand scores, which brings the round inside the step budget.",
      "fixes": "The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round."
    },
    {
      "what": "Define a round as one pass in which every active player takes exactly one action, starting with that round's leader. The leader moves one active player clockwise every round. Only the leader may knock, and not in the first round of a deal. After a knock, the other players' turns in that same round are their final actions.",
      "why": "A round now always holds one action per active player. Every non-knocker gets exactly one final action without the pass wrapping around. Because the leader rotates, every player gets knock chances.",
      "fixes": "The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous."
    },
    {
      "what": "Same rule, applied to the knock: since the knocker always acts first in the round, every other player acts after the knock.",
      "why": "No player who acted earlier in the pass misses a final action.",
      "fixes": "With knocks allowed from any seat mid-pass, players who acted earlier in the pass would get no final action, or the round would have to wrap around."
    },
    {
      "what": "Force a showdown at the end of deal-round 4 when 3 players are active, or deal-round 3 when 2 are active. The deal-round counter counts the rounds of the current deal.",
      "why": "This gives a clear, countable end to each deal. With the rotating leader it also gives each player exactly one chance to knock in a full deal.",
      "fixes": "The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous."
    },
    {
      "what": "Add the rule: if all remaining players tie for the lowest score, nobody loses a life. Losing lives can then never eliminate everyone. Otherwise the knocker's double penalty applies as normal, and survivors continue.",
      "why": "This closes the empty-table case. A lowest-score tie is the only way every remaining player could reach 0.",
      "fixes": "The previous variation did not say who wins when every remaining player ties for the lowest score and would reach 0 lives, nor what happens when a knocker is eliminated alongside others."
    },
    {
      "what": "Score each hand with one arithmetic formula on its sorted cards. The showdown only sets a redeal flag. The shuffle and deal happen at the start of the next round.",
      "why": "Scoring needs no lookup and takes 1 step. The shuffle never shares a round with the showdown, so each round has at most 1 random draw.",
      "fixes": "The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round."
    },
    {
      "what": "State explicitly: runs do not wrap; a knock is the knocker's action for that round; each action is a single compound choice (action type, own card, slot, card to expose).",
      "why": "This removes the remaining ambiguities.",
      "fixes": "The previous variation did not say whether runs wrap, whether the shuffle shares a round with the showdown (only 1 random draw is allowed per round), or whether a knock counts as a turn."
    },
    {
      "what": "Keep the suitless 36-card deck (values 1 to 9, four of each) and the prial > run > pair > high card ranking. Drop the betting version.",
      "why": "The suitless deck removes flushes and suit tie-breaks. The ranking order matches the real frequencies in this deck (prial 36, run 448, pair 1728 of the 7140 possible hands). The chip pot cannot be rewarded, so the lives game is the version to keep.",
      "fixes": "Suits, flushes and suit tie-breaks in the original need lookup tables the engine lacks."
    },
    {
      "what": "Use only the lives version, and decide the winner by survival and lives.",
      "why": "The platform decides only a winner, so a chip pot has nothing to pay into.",
      "fixes": "The betting version's chip pot cannot be rewarded by a platform that only decides a winner."
    }
  ],
  "keeps": [
    "A three-card table hand with one card face up and two face down",
    "The three exchange options: take the face-up card, make a blind swap, or swap the whole hand and expose one card",
    "Knocking to freeze your hand, followed by one final exchange for every other player",
    "Lives: the worst hand loses one, players are eliminated at 0, and the last survivor wins",
    "Prial is the top hand, 3-3-3 is the best prial, and 1-2-3 (A-2-3) is the best run",
    "Knocking is risky: a knocker who ends with the worst hand is punished harder"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (hidden hands, informative announcements, knock timing, worst-hand elimination) is strong reasoning material. The revision fixes the undefined end case, the round definition and the step budget."
  },
  "variation": {
    "name": "Knock Brag (3-player)",
    "summary": "Three players each hold three hidden cards and trade with a three-card table hand (one card face up) while every exchange is announced. The round's leader may knock to freeze their hand, after which the others get one final action. The worst hand at the showdown loses a life, a knocker who ends worst loses two, and the last player standing wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "PLAYERS AND LIVES: Exactly 3 players, in seats 1, 2 and 3 clockwise. Each starts with 3 lives. A player at 0 lives is eliminated and takes no further part. The others are 'active'.\n\nDECK: 36 cards, four copies each of the values 1, 2, 3, 4, 5, 6, 7, 8 and 9. There are no suits.\n\nHAND SCORE (used at the showdown): Sort a hand's three values so that a <= b <= c.\n- Prial (a = c): 300 + a. Exception: 3-3-3 scores 310.\n- Run (b = a+1 and c = b+1): 200 + c. Exception: 1-2-3 scores 210. Runs do not wrap: 8-9-1 and 9-1-2 are not runs.\n- Pair (a = b or b = c, but not a prial): 100 + 10 x b + (a + c - b). That is 100 + 10 x the pair value + the odd card.\n- High card (anything else): a + b + c.\nHigher is better.\n\nROUNDS, LEADER AND DEALS: The game is played in rounds, at most 40. In each round every active player takes exactly one action, in clockwise order starting with that round's leader. Seat 1 leads round 1. In each later round the leader is the next active player clockwise from the previous round's leader. This rotation continues across deals and skips eliminated players. A 'deal' is the series of rounds from one dealing of the cards to its showdown. The deal-round counter is 1 in the first round of a deal, 2 in the second, and so on.\n\nDEALING: At the very start of round 1, and at the start of every round that follows a showdown, the deck of 36 is shuffled (the round's one random event). Each active player receives 3 cards face down that only they see. Three cards go to the table: slot U face up, seen by everyone, and slots D1 and D2 face down, seen by nobody. The value of U is announced. The rest of the deck is not used in this deal.\n\nACTIONS: On your turn choose exactly one action. Give it as a single choice that includes every detail needed (which action, which of your cards, which slot, which card to expose).\n(a) TAKE UP: swap one of your cards for the face-up card U. The card you give becomes the new face-up U. Announced: 'X took the face-up [value] and left a face-up [value]'.\n(b) BLIND: swap one of your cards for D1 or D2 (your choice of slot) without seeing it first. Your card goes face down into that slot. You now see the card you received. Announced: 'X made a blind swap with D1' (or D2).\n(c) WHOLE HAND: take all three table cards into your hand; you now see them. Your old three cards become the table hand. You choose which of them goes face up as U; the other two go face down into D1 and D2. Announced: 'X swapped the whole hand and exposed a [value]'.\n(d) KNOCK: keep your hand and make no exchange. Only the round's leader may knock, and only when the deal-round counter is 2 or more. A knock is the knocker's action for that round. Announced: 'X knocks'.\n\nAFTER A KNOCK: The remaining active players in that same round (everyone after the knocker in clockwise order) each take their action as normal, but must choose (a), (b) or (c). These are their final actions. The showdown then happens at the end of that round.\n\nFORCED SHOWDOWN: If nobody has knocked, the showdown happens at the end of the round whose deal-round counter equals the number of active players plus 1. That is the end of deal-round 4 when 3 players are active, or deal-round 3 when 2 are active. There is no knocker.\n\nSHOWDOWN (at the end of the round): All active hands are revealed and scored, and every player's score is announced and recorded as their 'last showdown score'. If every active player has the same score, nobody loses a life. Otherwise every player with the lowest score loses 1 life, except a knocker with the lowest score, who loses 2 lives. Players at 0 lives or fewer are eliminated. The next round then begins with a new deal and the deal-round counter at 1. If no showdown happened, the deal-round counter rises by 1 for the next round.\n\nEND: The game ends at once when only one active player remains, or at the end of round 40.",
    "objective": "If only one player remains, that player wins. If round 40 ends with two or three players still active, the player with the most lives wins. A tie on lives is broken by the higher last showdown score among the tied players. If they are still tied, or if no showdown has yet happened, the game is a draw between them.",
    "expected_effect": "Each deal becomes a short inference contest. Take-up and whole-hand actions reveal values while blind swaps hide them, so players must track exposed cards to estimate opponents' hands and the face-down slots. Choosing the action is also a choice about how much to reveal. The rotating leader gives every player knock chances. Knocking early on a decent hand denies the others time to improve, but the double penalty makes a knock on a weak hand costly, so knocking is a calculated bet on one's rank. Only the single worst hand is punished, so a merely average hand often survives; the skill is judging 'good enough' from the signals. The all-tied rule and the fixed round structure make every case defined. Talk is left out: all three players want the others to lose, and talk would add bluffing words without changing the information, which comes from the forced announcements."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
