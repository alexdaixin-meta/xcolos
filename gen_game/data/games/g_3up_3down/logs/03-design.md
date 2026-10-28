# 03 design

- time: 2026-10-28T03:54:19+00:00 (70.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 d7ec628785ce83a5, reply sha256 64f44763ca5b0a9c

## Sent

````
Original game: 3Up 3Down
Players in the original: 2 to 6

Original rules:
Each player gets 3 face-down blind cards (3DOWN) they cannot look at, then 6 cards to look at; they choose 3 to place face-up on their blind cards as their 3UP pile. Remaining 3 cards form their starting hand. Remaining deck is draw pile. On your turn clockwise you must play a card >= top of discard pile; you may play multiple copies of same rank together. If you can play, you must; after playing you refill hand to 3 from draw pile if possible. If you cannot play, you take the entire discard pile into your hand. Clear, Clear+1, Clear+2 beat any number and remove the discard pile from game; Clear ends turn, Clear+1 requires one extra play (may draw first), Clear+2 requires two extra plays. Three consecutive same numbers by any players also clears. When draw pile empty and hand empty, play from 3UP, then blindly flip one 3DOWN per turn if legal. First to empty all piles wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: DEAL: the deal is stratified, so every player gets 3 Low, 3 Mid, 3 High and 1 Clear. The only built-in asymmetries are seat order and First's extra '1'.

TURNS NEEDED TO SHED: each PLAY sheds one rank group from one source. For a 3-card band dealt from {x,x,x,y,y,y,z,z,z} there are C(9,3)=84 hands:
| band shape | hands | distinct ranks |
|---|---|---|
| all same | 3 | 1 |
| pair + single | 54 | 2 |
| all different | 27 | 3 |
Expected distinct ranks per band = (3*1 + 54*2 + 27*3)/84 = 2.29. A player therefore needs about 2.29*3 + 1 (Clear) = 7.9 plays with no pickups.

THE HANDICAP IS MOSTLY FREE: the extra '1' costs First a play only when First holds no other 1. P(no 1 among 3 Low cards) = C(6,3)/C(9,3) = 20/84 = 24%. In 76% of deals it joins an existing group of 1s at zero extra turns. With two 1s it becomes three 1s, which reaches a run of 3 and clears the Pile. Expected cost is about 0.24 plays.

THE TEMPO EDGE IS LARGER: First moves first in every round, so in any race where players need the same number of plays, First empties first and wins under the END CHECK. First also opens on an empty Pile and can dump its least sheddable low group. With required plays clustered around 7–9, ties in play count are common, and First wins all of them. The labelled 'handicap' does not offset move order, so First has a systematic seat edge. Random seat assignment does not fix this: it only moves the edge to whoever draws First.

THOUGHTLESS POLICIES, under the winner rule:
- Always PICK UP: never sheds, never wins, never draws. It loses to everything.
- Always play the highest legal card: it strands low cards, which are playable only on an empty or low Pile, so it loses to sensible play.
- Always play the lowest legal rank (max copies), Clear when blocked, pick up otherwise: this is a competent shedding heuristic. It still loses to a player who plays a 9 or a triple to force the next seat into a pickup at the right moment, and to one who saves Clear.
No policy found that never loses, and no option is strictly dominant. All three players can realistically win.

The failure is the seat imbalance from a near-costless compensation.
- change: Balanced: make First's compensation actually cost a turn. For example, make the handicap a distinct 'Lone 1' that must be played alone from Hand, never joins a group or a run, and is legal only on an empty Pile or a top of 1. This costs First about one extra play in every deal instead of 24% of deals.
- change: Balanced (alternative or extra): give the last seat a compensating benefit, such as winning fewest-card ties against First at the round cap or receiving a second Clear in place of a High card. Then show by worked race counts or simulation that the three seats win at roughly equal rates.
- change: Playable (safeguard): document per-turn step use, aiming for at most 4 steps per turn using per-operation `if` conditions, so the 15-steps-per-round claim is verifiable within the 20-step limit.
The variation that was reviewed: Three Up: CARDS. There are 31 cards:
- three copies each of ranks 1 to 9 (27 cards);
- three Clear cards;
- one extra '1' (the handicap card).

SETUP.
1. Choose one of the three players at random to be First. Turn order is First, then the next seat, then the last seat, and it stays the same in every round.
2. Make three separate shuffled stacks: Low (all 1s, 2s, 3s except the handicap card; 9 cards), Mid (all 4s, 5s, 6s; 9 cards) and High (all 7s, 8s, 9s; 9 cards).
3. Deal each player 3 cards from Low, 3 from Mid, 3 from High, and 1 Clear, for 10 cards each. First also receives the handicap '1', for 11 cards.
4. Each player privately looks at their cards.
5. At the same moment, each player chooses exactly 3 of their cards to form their Up pile. These 3 cards are revealed to everyone.
6. The other cards are the player's Hand, which only that player sees.
7. The discard Pile starts empty.

WHAT EVERYONE CAN SEE AT ALL TIMES. Everyone can see:
- every card on the Pile;
- the top rank of the Pile;
- the run count (how many cards of the top rank are on top of the Pile in a row);
- every player's Up pile;
- every player's card counts;
- the full history of plays and pickups.

EACH ROUND.
(a) TALK. Every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages bind no one.
(b) TURNS. Each player in turn order takes one turn, as described below.
(c) END CHECK. After every turn, if the player who just acted has no cards left in Hand and Up pile, that player wins and the game ends immediately.
(d) ROUND CAP. After the last turn of round 40, the game ends.

A TURN. The player chooses one action.
- PLAY: choose one rank and play one or more copies of that rank together, all from the same source. The source must be your Hand if your Hand has any cards; you may play from your Up pile only when your Hand is empty.
  - A numbered play is legal only if the Pile is empty or the rank is greater than or equal to the Pile's top rank.
  - A Clear is always legal and is played alone.
- PICK UP: take every card on the Pile into your Hand; the Pile becomes empty. You may pick up at any time, even if you have a legal play. If the Pile is already empty, a pick up does nothing.
- An illegal or unreadable choice counts as PICK UP.

RESOLVING A PLAY.
- Played numbered cards go on top of the Pile. If the top rank is the same as before, the run count rises by the number of cards played; otherwise the run count equals the number of cards played.
- If the run count reaches 3 or more, the Pile is cleared: removed from the game, now empty, run count 0.
- If a Clear is played, the Clear and the whole Pile are removed from the game and the Pile is empty.
- In every case the turn then ends, and the next player acts on whatever Pile remains (an empty Pile accepts any card). Winner: The first player to have no cards in Hand and Up pile wins immediately. If nobody has done so after round 40, the player with the fewest cards (Hand plus Up pile) wins. If two or three players tie for fewest, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "3Up 3Down is a shedding card game for 2 to 6 players. Each player has hidden blind cards, face-up cards and a hand, and on each turn plays a card equal to or higher than the top of the discard pile, or else picks the whole pile up. Clear cards and runs of three wipe the pile, and the first player to get rid of every card wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the original, the blind 3DOWN flips and the random refills from the draw pile are pure chance. In the previous variation, no simple policy dominated. Always picking up never sheds a card. Always playing the highest card strands low cards. Playing the lowest legal rank is competent but loses to timed forcing plays. However, First wins every race in which the players need the same number of plays, because the END CHECK ends the game immediately and First moves first. The '1' handicap costs First an extra play in only about 24% of deals (expected cost about 0.24 plays). That is a built-in seat edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The original is dominated by the draws: blind flips and refills. The previous variation removed the draw pile and stratified the deal, which made skill matter: choosing the Up pile, saving the Clear, and forcing a pickup with a 9 or a triple at the right moment. But the seat edge decides close races regardless of skill."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A player needs about 7.9 plays with no pickups. The quality of play shows in when you dump low groups, when you block the next seat, and when you spend the Clear, so strong players keep finding improvements. Weak but legal play still sheds cards and can win when an opponent is forced into a big pickup."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each hand is private, but the history of plays and the known 30-card deck let players infer what an opponent can still play. Up piles are public commitments. Timing a block or a Clear needs a plan over several turns and a prediction of the next seat's reply."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Legality, run counts, clears, card counts and the winner all follow by arithmetic from the recorded plays."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original has 2 to 6 players, a draw pile, blind flips and multi-play Clear+1 and Clear+2 cards. These are heavy, but the previous variation trimmed them to fit. That variation's claim of 15 steps per round was not broken down, and its immediate mid-round win check costs a check after every turn."
    }
  ],
  "problems": [
    "Seat edge: the game ends the instant a player empties, so First wins every race in which players need equal numbers of plays, and with 7 to 9 plays needed such ties are common.",
    "The compensation for First (an extra '1') is nearly free: it costs a play in only about 24% of deals, and it can even complete a run of three 1s and clear the Pile, so it does not offset the tempo edge.",
    "When several players finish level, nothing decided by skill separates them; the result falls to seat order alone.",
    "The step budget was asserted rather than shown, and an end check after every individual turn inflates the step count."
  ],
  "changes": [
    {
      "what": "Every player always gets the same number of turns. The win check happens once, at the end of each round, after all three players have acted. A player who empties mid-round simply passes on their remaining turns that round, and the others still take their turns.",
      "why": "Moving first no longer lets a player finish a turn ahead of an equally fast opponent. A player who needs the same number of plays as First now finishes in the same round.",
      "fixes": "Seat edge: the game ends the instant a player empties, so First wins every race in which players need equal numbers of plays, and with 7 to 9 plays needed such ties are common."
    },
    {
      "what": "Remove the extra '1' handicap card. Each player gets exactly 3 Low, 3 Mid, 3 High and 1 Clear, which uses all 30 cards.",
      "why": "Once turns are equalised, no compensation is needed, and the handicap only created a new asymmetry of its own.",
      "fixes": "The compensation for First (an extra '1') is nearly free: it costs a play in only about 24% of deals, and it can even complete a run of three 1s and clear the Pile, so it does not offset the tempo edge."
    },
    {
      "what": "If two or three players empty in the same round, the one who picked up the fewest cards over the whole game wins. If they are still tied, the game is a draw. The engine keeps a public 'cards picked up' count for each player.",
      "why": "Ties in the race are settled by play quality, since avoiding pickups and forcing them on others is the core skill, not by seat.",
      "fixes": "When several players finish level, nothing decided by skill separates them; the result falls to seat order alone."
    },
    {
      "what": "The step budget is laid out explicitly. Per round: 1 talk poll and 1 reveal. Per player: 1 choice, 1 apply step (play or pickup, using if-conditions) and 1 run/clear step. Then 1 end check and 1 cap check. That is 13 steps and 4 choice steps per round.",
      "why": "This makes the build verifiable within the 20-step and 4-choice limits.",
      "fixes": "The step budget was asserted rather than shown, and an end check after every individual turn inflates the step count."
    }
  ],
  "keeps": [
    "Shedding by playing a rank equal to or higher than the top of the Pile, or else taking the whole Pile.",
    "Playing several copies of one rank together, and runs of three of the same rank clearing the Pile.",
    "Clear cards that wipe the Pile whatever is on it.",
    "A chosen face-up Up pile, played only after the Hand is empty.",
    "The goal: be the first to get rid of all your cards."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The shedding core already rewards inference and timing. The only failing was the tempo edge, which equal turns per round and a skill-based tiebreak remove without changing the game's identity."
  },
  "variation": {
    "name": "Three Up: Even Rounds",
    "summary": "A three-player shedding game in which every player plays a card equal to or higher than the top of a shared Pile or else takes the Pile. Clears and runs of three wipe the Pile. All three players get equal turns, the win is checked at the end of each round, and players who finish together are separated by who picked up fewer cards.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "CARDS. There are 30 cards: three copies each of ranks 1 to 9 (27 cards) and three Clear cards.\n\nSETUP.\n1. Seat the three players in a random order called First, Second and Third. Turn order is First, Second, Third in every round.\n2. Make three separately shuffled stacks: Low (all 1s, 2s and 3s; 9 cards), Mid (all 4s, 5s and 6s; 9 cards) and High (all 7s, 8s and 9s; 9 cards).\n3. Deal each player 3 cards from Low, 3 from Mid, 3 from High and 1 Clear, so each player has 10 cards. Every card is dealt.\n4. Each player privately looks at their cards.\n5. At the same moment, each player chooses exactly 3 of their cards to be their Up pile. All Up piles are then revealed.\n6. A player's remaining 7 cards are their Hand, which only that player sees.\n7. The discard Pile starts empty, with a run count of 0. Each player's 'picked up' count starts at 0.\n\nPUBLIC INFORMATION. At all times everyone can see:\n- every card on the Pile, its top rank and its run count (how many cards of the top rank lie on top of the Pile in a row);\n- every Up pile;\n- each player's number of Hand cards;\n- each player's picked-up count;\n- the full history of plays and pickups.\n\nEACH ROUND (at most 40 rounds).\n(a) TALK. Every player writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Messages bind no one.\n(b) TURNS. First, then Second, then Third each take one turn as described below. A player who already has no cards in Hand or Up pile skips their turn.\n(c) END CHECK. After Third's turn, look at every player who now has no cards in Hand or Up pile.\n- If exactly one player is out of cards, that player wins.\n- If two or three players are out of cards, the one among them with the lowest picked-up count wins. If they are tied on that count, the game is a draw.\n- If nobody is out of cards, play continues.\n(d) ROUND CAP. If round 40 ends with nobody out of cards, the player with the fewest cards (Hand plus Up pile) wins. A tie for fewest cards is broken by the lowest picked-up count. If players are still tied, the game is a draw.\n\nA TURN. The player chooses one of two actions.\n- PLAY: choose one rank and play one or more cards of that rank together, all from the same source.\n  - The source must be your Hand while your Hand has any cards. You play from your Up pile only once your Hand is empty.\n  - A numbered play is legal only if the Pile is empty or the rank is equal to or higher than the Pile's top rank.\n  - A Clear is always legal and is played on its own.\n- PICK UP: take every card on the Pile into your Hand, and add the number of cards taken to your picked-up count. The Pile becomes empty with a run count of 0. You may pick up even when you have a legal play. Picking up an empty Pile does nothing.\n- An illegal or unreadable choice counts as PICK UP.\n\nRESOLVING A PLAY.\n- Numbered cards go on top of the Pile. If their rank equals the previous top rank, the run count rises by the number of cards played; otherwise the run count becomes the number of cards played.\n- If the run count reaches 3 or more, the Pile is cleared: its cards are removed from the game, it becomes empty, and the run count is 0.\n- A played Clear and the whole Pile are removed from the game, leaving the Pile empty.\n- The turn then ends, and the next player acts on whatever Pile remains. An empty Pile accepts any card.",
    "objective": "At the end of each round, if exactly one player has no cards left in Hand or Up pile, that player wins. If several players emptied by the end of the same round, the one with the lowest total of cards picked up during the game wins; if they are tied on that total, the game is a draw. If round 40 ends with nobody out of cards, the player with the fewest remaining cards wins, ties are broken by the lowest picked-up total, and a remaining tie is a draw.",
    "expected_effect": "Equal turns per round remove First's tempo win: two players who need 8 plays each now finish in the same round, and the one who absorbed fewer pickups wins. This makes forcing pickups on others, and avoiding them yourself, decisive in close races, instead of seat order. Always picking up loses to everything. Always playing the highest card strands low cards. The lowest-legal-rank heuristic loses to timed blocks with a 9 or a triple and to a well-saved Clear. Talk earns its place because only one player can win. The two trailing players can propose to gang up on the leader (for example, 'both play high so the leader must pick up'), but each also wants the other to absorb the cost of blocking. A player who follows a proposal can therefore spend their own high cards or their Clear while the proposer sheds freely, and lose. Players must judge which proposals serve the speaker. Remaining asymmetries, such as First's opening on an empty Pile and Third seeing the round's earlier plays, recur cyclically and are small. Seat win rates should still be confirmed by simulation."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 4,
    "attributes": 11,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 40
  }
}
```
````
