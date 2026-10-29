# 06 design

- time: 2026-10-28T06:18:14+00:00 (98.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 71138b01a1b2d0da, reply sha256 df8666388bcfee6f

## Sent

````
Original game: Put
Players in the original: 2 to 4

Original rules:
Use 52 cards ranking 3-2-A-K-Q-J-10-9-8-7-6-5-4, no trumps. Players ante to game score, 5 or 7 points to win match. Deal 3 cards each singly. Non-dealer leads. Any card may be played, no need to follow. Higher rank wins trick; equal ranks tie the trick and it belongs to none. Winner leads next, same leader after a tie. Winning 2 of 3 tricks scores 1 point, trick-and-tie scores none. Before a trick, holder may say "Put" to play for the whole game. If opponent folds, putter scores 1. If opponent says "I see it", the hand is played and winner of most tricks wins the whole game (5 or 7) not just 1. A player may also fold on seeing cards, conceding 1. Deal alternates.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: SKILL EDGE AGAINST ALWAYS-PUT. Every hand is raised at call 1, so the second call never happens. The sensible player's only levers are fold-or-see at call 1 and the simultaneous allocation of 3 cards.
- Best response: see when E>-1/3, which is roughly the top 70% of hands, and fold otherwise.
- Folding about 30% of hands costs 0.30 x 1 = -0.30.
- Seeing about 70% of hands, with an average margin of about +0.25 against a random hand, gains 0.70 x 3 x 0.25 = +0.52.
- Allocation skill in a 3-card simultaneous Blotto-like play adds perhaps +0.05.
- Net edge: about +0.25 points per hand, or about +6 over 24 hands.

VARIANCE. About 17 stake-3 hands are played out, each with a standard deviation of about 3 x 0.8 = 2.4. Over the match that is about 2.4 x sqrt(17) = 10 points. With an edge of +6 against a spread of 10, the thoughtless always-PUT player still wins about 25-30% of matches against correct play.

AGAINST A FELLOW REASONER the picture is worse. When both play the intended strategy (put strong, see medium, fold weak), most decisive hands are stake-3 showdowns between hands both players liked. Those are settled by the deal, because the stronger 3-card hand wins its tricks almost regardless of order. Bluffing and inference only shift the occasional 1- or 2-point fold.

THE DEAL DOMINATES. There are 3 random cards per player and swings of 3 points. Within a hand, the result is mostly the deal. Over 24 hands, chance decides a large share of matches, about 40-50% by this estimate.

INFERENCE IS THIN. There is something to infer: the opponent's call pattern, and the trick-1 card before call 2. But call 2 is reachable only when nobody put at call 1, and with a fully simultaneous first call there is no betting sequence to read. A good reasoner is favoured, but not clearly enough.
- change: Reduce the share of the result decided by the deal. Deal 5 cards to each player and have each secretly keep 3, so that hand construction is a skill. Alternatively, show one card of each player face up before the first call, so calls can be inferred from.
- change: Make the first call sequential, with a re-raise. For example, the hand's alternating first caller may PUT or PASS. The other then answers SEE, FOLD or RE-PUT (stake 5), and the first caller may then see or fold. This gives bluffing and reading a real betting sequence instead of a blind simultaneous guess.
- change: Lower the swing of showdowns relative to folds. Make a raised stake 2 rather than 3, and a fold at call 1 cost 1, so that well-timed folds and bluffs move the score as much as raw card strength does.
- change: Raise the match to 36-40 hands, within the 40-round limit, so that a per-hand skill edge of +0.25 or more outweighs the variance. The aim is for an always-PUT policy to win under 15% of matches against sensible play.
The variation that was reviewed: Put: Trick by Trick: CARDS. Use a standard 52-card deck; suits do not matter. Each card has a strength: 3 = 13, 2 = 12, A = 11, K = 10, Q = 9, J = 8, 10 = 7, 9 = 6, 8 = 5, 7 = 4, 6 = 3, 5 = 2, 4 = 1. Higher strength is better.

SETUP. There are two players. Each starts with 0 points and 0 hands won. The match lasts exactly 24 hands.

EACH HAND:
1. Deal. Shuffle all 52 cards and deal 3 cards to each player. Each player sees only their own cards. The hand's stake is 1 point, and the hand is not yet raised.

2. First call (simultaneous). Both players choose at the same moment, without seeing the other's choice, one of three answers: PUT, HOLD-AND-SEE, or HOLD-AND-FOLD. Both choices are then revealed.
- If both chose PUT, the hand is raised and the stake becomes 3.
- If exactly one chose PUT and the other chose HOLD-AND-SEE, the hand is raised and the stake becomes 3.
- If exactly one chose PUT and the other chose HOLD-AND-FOLD, the putter scores 1 point and wins the hand. The hand ends, with no cards shown; go to step 8.
- Otherwise neither player called PUT, and the stake stays 1.

3. Trick 1 (simultaneous). Each player secretly picks one card from their hand. Both cards are revealed and removed from the hands. The higher strength wins the trick. Equal strength ties the trick, which belongs to no one.

4. Second call (simultaneous). This step happens only if the hand is not already raised. Both players again choose PUT, HOLD-AND-SEE or HOLD-AND-FOLD at the same moment, and the choices are revealed.
- If both chose PUT, or one chose PUT and the other HOLD-AND-SEE, the hand is raised and the stake becomes 3.
- If one chose PUT and the other HOLD-AND-FOLD, the putter scores 2 points and wins the hand. The hand ends; go to step 8.
- Otherwise the stake stays 1.

5. Trick 2 (simultaneous). Each player secretly picks one of their two remaining cards. Both are revealed and compared as in trick 1.

6. Trick 3 (automatic). Each player's last card is played and revealed, and the two are compared as in trick 1.

7. Score the hand. If one player won more of the three tricks than the other, that player scores the stake (1, or 3 if raised) and wins the hand. If both won the same number of tricks, nobody scores and nobody wins the hand.

8. Announce. Announce the calls, every card that was played, the hand result, both players' points and both players' hands won.

END. After hand 24 the match ends. Winner: After 24 hands, the player with more points wins. If points are equal, the player with more hands won wins. A hand is won by scoring a hand on tricks or by the opponent folding to your Put. If both are equal, the match is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Put is an old two-to-four-player trick game with 3 cards each and the odd rank order 3-2-A-K-...-4. Players do not have to follow suit, and winning 2 of 3 tricks scores a point. At any moment a player may call 'Put' to stake the whole game, and the opponent must fold (conceding 1) or 'see it'. The previously tested two-player variation, 'Put: Trick by Trick', used a simultaneous PUT / HOLD-AND-SEE / HOLD-AND-FOLD call before trick 1 and again before trick 2, a raised stake of 3, and 24 hands.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Always-PUT forces every hand to stake 3 at the first call, so the second call never happens. The thoughtful player's only levers are a blind fold-or-see and a near-random 3-card allocation. Correct play gains only about +0.25 per hand, about +6 over 24 hands, against a match spread of about 10. Always-PUT therefore still wins roughly 25-30% of matches. No seat has an edge, but a thoughtless policy is far too competitive."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "When both players play sensibly, the decisive points come from stake-3 showdowns between two hands both players liked. These are settled by which 3 random cards are stronger. The test estimates that chance decides 40-50% of matches."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "There is little to improve on beyond a fold threshold of about the bottom 30% of hands. Allocation of 3 cards in simultaneous play adds about +0.05 per hand. A weak player can score, but a strong one has almost no further levers."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Cards are hidden, but the first call is simultaneous, so there is no betting sequence to read. The trick-1 card that could inform the second call is seen only when nobody put at call 1, which a PUT-heavy opponent prevents. Bluffing and opponent reading barely move the score."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Tricks, stakes, points and hands won are all arithmetic. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is two-player, turn-based and text-only, with one deal per hand. It uses 4 choice steps at most and stays within the step limits."
    }
  ],
  "problems": [
    "P1: Always-PUT is too strong. Because the first call is simultaneous, putting blind cannot be punished by a re-raise, and it wins about 25-30% of matches against correct play.",
    "P2: The deal dominates. Stake-3 showdowns between two strong hands decide most matches, and about 40-50% of results are chance.",
    "P3: Inference is thin. A simultaneous first call gives no betting sequence to read, no information is public before betting, and the second call is usually skipped.",
    "P4: Card play is nearly skill-free. With 3 cards and nothing to choose except the order, the stronger hand wins its tricks almost regardless.",
    "P5: The match is too short. 24 hands cannot let a per-hand skill edge outweigh the variance."
  ],
  "changes": [
    {
      "what": "The betting becomes a sequence with a re-raise. The caller, who alternates each hand, says PUT or PASS. The responder answers a PUT with SEE, FOLD or RE-PUT, and answers a PASS with PUT or PASS. The caller then answers a RE-PUT, or a PUT made after their PASS, with SEE or FOLD.",
      "why": "A blind putter can now be re-put by a strong hand and must then fold, costing 2, or see at stake 4. Calls are made in order, so they can be read and bluffed.",
      "fixes": "P1"
    },
    {
      "what": "The stakes are rescaled: 1 if nobody puts, 2 if a PUT is seen, 4 if a RE-PUT is seen. A fold to a PUT pays the putter 1, and a fold to a RE-PUT pays the re-putter 2.",
      "why": "The ladder rewards value-raising strong hands against a player who never folds, and makes well-timed bluffs and folds worth real points. Against always-PUT, folding the bottom ~37% of hands and re-putting the rest yields about +0.56 per hand.",
      "fixes": "P1"
    },
    {
      "what": "Each player is dealt 4 cards. The 4th is face up, visible to both, and the other 3 are private. A player plays only 3 of the 4 cards and chooses which to leave out.",
      "why": "The public card gives each player something to infer the opponent's strength and calls from. Choosing which card to drop, and in what order to play the others, against a known opponent card adds decisions to the card play. Every bet is judged against visible information.",
      "fixes": "P3, P4, P2"
    },
    {
      "what": "Card play becomes a single simultaneous secret submission of an ordered list of 3 cards. Trick 1 is the first card of each list, and so on.",
      "why": "This keeps the original's free play of any card while fitting the 4-choice limit next to three betting steps. Ordering against a known face-up card is a guessing game in which reading the opponent pays.",
      "fixes": "P4"
    },
    {
      "what": "The match lasts 40 hands instead of 24, with the caller alternating so each player calls 20 times.",
      "why": "Estimated edge against always-PUT is about +22 points against a spread of about 20 over 40 hands, which puts the thoughtless policy near or below a 13% win rate. The reasoner-vs-reasoner edges from reading and bluffing also accumulate.",
      "fixes": "P5, P2"
    },
    {
      "what": "The original rule is restored that a hand is scored only by a player who wins at least 2 of the 3 tricks. Trick-and-tie, or one trick each with a tie, scores nothing.",
      "why": "This is faithful to the original and makes the choice of order matter. A weaker hand that forces ties can neutralise a big stake.",
      "fixes": "P2, P4"
    }
  ],
  "keeps": [
    "The rank order 3-2-A-K-Q-J-10-9-8-7-6-5-4, with suits irrelevant.",
    "Any card may be played, with no need to follow suit.",
    "Equal ranks tie a trick, which belongs to no one.",
    "Winning 2 of 3 tricks scores the hand, and trick-and-tie scores nothing.",
    "The 'Put' call that raises the stake, answered by 'I see it' or by folding and conceding.",
    "Three-card hands in play and an alternating first player."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The Put/see/fold core is a compact bluffing game. A betting sequence with a re-raise, a public card, a choice of which card to drop, and a longer match fix the failures within the limits."
  },
  "variation": {
    "name": "Put: Show One, Keep Three",
    "summary": "A two-player bluffing card duel over 40 hands. Each player holds 4 cards, one of them face up. Players bet in sequence (PUT, SEE, FOLD, RE-PUT) on a best-of-3-tricks showdown played with 3 of their 4 cards in a secretly chosen order.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. Use a standard 52-card deck; suits do not matter. Strengths: 3 = 13, 2 = 12, A = 11, K = 10, Q = 9, J = 8, 10 = 7, 9 = 6, 8 = 5, 7 = 4, 6 = 3, 5 = 2, 4 = 1. Higher strength is better.\n\nSETUP. There are two players, A and B. Each starts with 0 points and 0 hands won. The match lasts exactly 40 hands. In odd-numbered hands A is the Caller and B the Responder. In even-numbered hands B is the Caller and A the Responder.\n\nEACH HAND:\n1. Deal. Shuffle all 52 cards and deal 4 cards to each player. Each player's 4th card is face up and announced to both players. The other 3 are private to their holder.\n\n2. Caller's call. The Caller says PUT or PASS.\n\n3. Responder's answer.\n- If the Caller said PUT, the Responder says SEE, FOLD or RE-PUT. On SEE, the stake is 2; go to step 5. On FOLD, the Caller scores 1 point and wins the hand; go to step 8. On RE-PUT, go to step 4.\n- If the Caller said PASS, the Responder says PUT or PASS. On PASS, the stake is 1; go to step 5. On PUT, go to step 4.\n\n4. Caller's answer. This step happens only if the Responder said RE-PUT or PUT in step 3. The Caller says SEE or FOLD.\n- After a RE-PUT: SEE makes the stake 4. FOLD gives the Responder 2 points and the hand.\n- After a PUT that followed the Caller's PASS: SEE makes the stake 2. FOLD gives the Responder 1 point and the hand.\n- A FOLD ends the hand; go to step 8.\n\n5. Play (simultaneous). Each player secretly writes an ordered list of 3 different cards chosen from their own 4 cards. The face-up card may be used or left out. The lists are then revealed.\n\n6. Tricks. Compare the 1st cards of the two lists, then the 2nd cards, then the 3rd cards. In each pair the higher strength wins that trick. Equal strength ties the trick, and it belongs to no one.\n\n7. Score. A player who won at least 2 of the 3 tricks scores the stake (1, 2 or 4) and wins the hand. Otherwise, for example one trick each with a tie, or one win and two ties, or three ties, nobody scores.\n\n8. Announce. Announce all calls, all 8 cards (including any card that was left out or never played), the hand result, and both players' points and hands won.\n\nEND. After hand 40 the match ends.",
    "objective": "After 40 hands, the player with more points wins. If points are equal, the player with more hands won wins. A hand is won by scoring it on tricks or by the opponent folding. If both are equal, the match is a draw.",
    "expected_effect": "Always-PUT is now punished. A reader re-puts the top ~60% of hands and folds the rest cheaply, for an estimated edge of about +0.56 per hand, about +22 over 40 hands against a spread of about 20. That leaves the blind policy winning roughly 10-13% of matches. Always-SEE loses to value raises, and always-PASS or always-FOLD lose outright. Between two reasoners, the visible card and the order of calls give something to read. A PASS from a Caller showing a 3 is suspicious, and a RE-PUT against a high face-up card signals strength or a bluff. Folds at 1 or 2 points and value raises to 4 now shift the score as much as raw card strength does. Choosing which card to leave out, and how to order the rest against a known enemy card, rewards anticipating the opponent's order. Equal-rank ties let a weaker hand void a big stake. This is a two-player zero-sum duel, so talk is omitted: it would add nothing beyond what the calls already signal."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 17,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
