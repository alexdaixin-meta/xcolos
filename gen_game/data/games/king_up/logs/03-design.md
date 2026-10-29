# 03 design

- time: 2026-10-28T05:57:37+00:00 (55.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c3c74245a4584eeb, reply sha256 bd6243727dd32cd0

## Sent

````
Original game: King Up
Players in the original: 3 to 6

Original rules:
Each game has three rounds. At start of a round, deal each player a secret goal showing six favored characters. Players in turn order place characters onto floors 0 to 4 of the castle, at most four per floor. Leftovers go to floor 0. Then players take turns moving any character up one floor if destination has fewer than four. Moving from floor 5 to the throne triggers an election. All players simultaneously vote Yes or No: Yes cards are unlimited, No cards are limited and discarded when used, and hand sizes are secret. If all Yes, that character is king and round ends. If any No, the character is eliminated from the round and play continues left of the crown holder. At round end, players reveal goals and score by final heights: throne 10, floor 5 is 5, 4 is 4, 3 is 3, 2 is 2, 1 is 1, 0 is 0, eliminated 0. In round three, a zero becomes 33. Highest total after three rounds wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: The three-player case is sound. All 9 characters are dealt, so each is favoured by exactly one player. On any candidate the owner gains +5 if it is crowned (10 vs 5) and loses 5 if it is eliminated (0 vs 5). Every non-owner is unaffected by its score but loses the chance to keep playing if it is crowned. So a non-owner vetoes unless they lead and want the game to end.

Thoughtless policies (3 players):
- Always Yes: every rival candidate is crowned. That player wins only when their own characters already lead. They lose most games against sensible play and roughly 2 in 3 against random play.
- Always No (until cards run out): this burns both cards, possibly on their own characters (owner -5 each time). It also leaves them unable to veto once the 6 No cards (2 x 3) are gone, after which the next candidate is forced through. They often lose.
- Always raise the same character, or the first legal character: this exposes their goal, and that character gets vetoed. Raising the first character only helps them a third of the time. They lose against sensible play.
- Never raise to 5: not possible in the long run. At most 36 raises can be absorbed at height 4 or below (9 x 4), while 15 rounds x 3 = 45 raises occur, so a 4-to-5 raise is eventually the only legal move.

No option is strictly dominant for 3 players. Seats 1 to 3 are each first raiser 5 times out of 15.

The 4 and 5 player cases are structurally unfair by seat. Goals are dealt in seat order from a 9-card shuffle, then a fresh shuffle for the rest:
- With 4 players, seats 1 to 3 hold disjoint triples covering all 9 characters. Seat 4 draws 3 of 9 from a new shuffle, so every one of seat 4's characters is co-owned by someone in seats 1 to 3, and everyone knows this from the rules.
- Seat 4 therefore always has a built-in Yes ally on every candidate it favours and never has a character only it benefits from. Seats 1 to 3 do have such characters.
- With probability 3/84 (about 3.6%), seat 4's triple is identical to one other player's. Seat 4 can then never win outright; the best it can do is a draw.
- With 5 players, seats 4 and 5 both draw from the second shuffle (3 + 3 of its 9 cards). Again only the later seats overlap.
- First-raiser counts over 15 rounds are unequal with 4 players (4, 4, 4, 3).

The seat number therefore determines goal structure and voting alliances. That is a seat edge, not a skill edge.
- change: Make goal dealing seat-symmetric for 4 and 5 players. Either give each player an independent random 3 of the 9 characters (every seat has the same overlap distribution), or use more characters, e.g. 12 for 4 players and 15 for 5, so that all goals are disjoint like the 3-player case. State the exact draw procedure, including how duplicates are handled.
- change: Set the round limit to a multiple of the player count (e.g. 12 rounds for 4 players, 15 for 3 or 5), or otherwise equalise how often each seat is first raiser.
- change: Clarify the rotation direction to match the seat order used in the Raise step, and store elimination as height -1 so the attribute count stays under 20.
The variation that was reviewed: King Up: Numbered Throne: SETUP. There are 9 characters, labelled A to I, each with a public height starting at 0. Shuffle the 9 labels and deal each player 3 different characters as their secret goal. With 3 players the leftover 0 characters are favoured by no one; with 4 or 5 players, deal a fresh shuffle once the 9 run out, so goals can overlap. No player gets the same character twice. Each player receives secret No cards: 2 each with 3 or 4 players, 1 each with 5 players. Yes votes are unlimited. Seat 1 is the first raiser in round 1.

EACH ROUND (at most 15 rounds):
1. Announce. All heights, eliminated characters and the round number are shown to everyone.
2. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.
3. Raise. Starting with this round's first raiser and going in seat order, each player chooses one active (not eliminated) character and raises its height by 1. A character may be raised from 4 to 5 only if no character is currently at height 5. No character may go above 5. A player with no legal raise passes.
4. Election. If a character is at height 5, it is the candidate. Every player simultaneously votes Yes or No. A player with no No cards left must vote Yes.
5. Resolve. If all votes are Yes, the candidate is crowned king and the game ends after scoring. If one or more votes are No, each No voter discards one No card, the candidate is eliminated (removed for the rest of the game, worth 0), and only the NUMBER of No votes is announced, not who cast them.
6. Rotate. The first raiser for the next round is the next seat to the left.
7. End check. The game ends if a king was crowned, or if round 15 has finished.

SCORING. Each player reveals their goal. For each of their 3 favoured characters they score: 10 if it is king; its height (0 to 5) if it is active and not king; 0 if it is eliminated. Winner: The player with the highest total wins. If several players tie for the highest total, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "King Up is a 3-6 player game of hidden goals. Players secretly favour certain characters, take turns raising characters up castle floors, and vote on each character that reaches the throne. One secret No vote eliminates a candidate. Players score by how high their favoured characters finish.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "With 3 players nothing degenerate survives. Always Yes crowns rivals' characters and loses about 2 games in 3 even against random play. Always No burns cards, sometimes on the player's own characters, and leaves them unable to veto later. Always raising the same character reveals the goal and gets that character vetoed. The previous variation still gave seats an edge with 4-5 players. Seats 1-3 held disjoint triples, while seats 4-5 drew from a second shuffle. So the later seats' characters were always co-owned, which handed them built-in Yes allies, and about 3.6% of the time a late seat's triple duplicated another player's and could not win outright. First-raiser counts were also unequal (4,4,4,3 over 15 rounds with 4 players)."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The only randomness is the goal deal, and it changes what each player knows, not who is ahead. The result comes from raising decoys to hide one's goal, guessing rivals' goals from their raises, choosing when to spend a scarce No, and deciding when ending the game helps."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still scores the heights of their own characters. A strong player can keep improving at bluffing with raises, reading the anonymous No counts, tracking how many No cards may remain, and timing the throne push. There is no simple solved line."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Three things are hidden: goals, No-card counts and who voted No. Every raise and vote has to be read as evidence about rivals' goals. Players must plan over rounds because raises to height 5 are eventually forced."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Scores are sums of fixed values per height. The winner is the highest total, a plain arithmetic comparison."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original's floors are only numbers, so no spatial board is needed. But its free movement between floors, its three-round structure and the round-3 rule turning zero into 33 make it long and branchy. The earlier variation flattened this into one game of up to 15 rounds of numeric heights, which fits. Storing eliminated and crowned characters as separate state wasted attributes."
    }
  ],
  "problems": [
    "P1: Goals are not seat-symmetric with 4-5 players. Later seats draw from a second shuffle, so their characters are always co-owned (built-in voting allies), and they can be dealt a triple identical to another player's.",
    "P2: First-raiser turns are unequal when the round limit is not a multiple of the player count (15 rounds with 4 players gives 4,4,4,3).",
    "P3: The rotation direction and the raise order were not stated in the same terms, so seat order could be built inconsistently.",
    "P4: Eliminated and crowned status took extra attributes, pushing the attribute count toward the limit of 20 with more characters.",
    "P5: The No-card count differed by player count (1 each with 5 players), which would make vetoes too scarce once 15 characters are in play."
  ],
  "changes": [
    {
      "what": "Use 3 characters per player (9 for 3 players, 12 for 4, 15 for 5) and deal each player a disjoint triple from one shuffle. Every character is favoured by exactly one player.",
      "why": "Every seat gets the same goal structure. No seat has built-in allies or can be dealt a duplicate goal, and the sound 3-player logic (owner gains +5 if crowned, loses 5 if eliminated, non-owners only care about game length) carries over to every player count.",
      "fixes": "P1"
    },
    {
      "what": "Set the round limit by player count: 15 rounds for 3 players, 16 for 4 and 15 for 5.",
      "why": "Each limit is a multiple of the player count, so every seat is first raiser equally often (5, 4 and 3 times). Raises still outnumber what heights 0-4 can absorb (45>36, 64>48, 75>60), so pushes to the throne are eventually forced.",
      "fixes": "P2"
    },
    {
      "what": "Define seat order once: ascending seat number, wrapping from the highest seat to seat 1. Both the raise sequence and the first-raiser rotation follow it.",
      "why": "Removes the ambiguity between 'left' and seat order.",
      "fixes": "P3"
    },
    {
      "what": "Store status inside each character's height: -1 means eliminated, 6 means king, 0 to 5 means active.",
      "why": "One attribute per character. That gives 15 heights plus goal, No cards, round number and first raiser = 19 attributes at 5 players.",
      "fixes": "P4"
    },
    {
      "what": "Give every player 2 secret No cards at every player count.",
      "why": "With 3n characters and 2n No cards, vetoes stay scarce and strategic but meaningful at 5 players. The game still ends by a king or the round limit.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "Secret goals of favoured characters",
    "Characters climbing numbered levels toward a throne",
    "Unanimous election: one anonymous No eliminates the candidate",
    "Unlimited Yes and scarce, secret No cards",
    "Scoring by final height, with the king worth 10 and an eliminated character worth 0",
    "Bluffing through which characters you raise"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game's core of hidden goals, bluff raises and scarce anonymous vetoes is strong reasoning material. It only needed seat-symmetric dealing and equalised turn order to be balanced at every player count."
  },
  "variation": {
    "name": "King Up: Fair Throne",
    "summary": "Each player secretly favours 3 characters that no one else favours. Players take turns raising characters toward height 5. Every character reaching height 5 faces a unanimous vote, and a single anonymous No eliminates it. Players score by the final heights of their favoured characters.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SEAT ORDER. Seats are numbered 1 to N (N = 3, 4 or 5). 'Seat order' always means ascending seat number, wrapping from seat N back to seat 1.\n\nSETUP.\n- Use 3N characters, labelled with letters: A-I for 3 players, A-L for 4, A-O for 5.\n- Each character has a public height, starting at 0. Height also records status: -1 means eliminated, 6 means king, and 0 to 5 means active.\n- Shuffle all labels once. Deal 3 to seat 1, the next 3 to seat 2, and so on. Every character is favoured by exactly one player, and no two players share a character.\n- Each player's 3 characters are their secret goal.\n- Each player receives 2 secret No cards. Yes votes are unlimited. The number of No cards a player holds is secret.\n- The round limit is 15 rounds with 3 players, 16 with 4 and 15 with 5.\n- Seat 1 is the first raiser in round 1.\n\nEACH ROUND:\n1. Announce. Show everyone all heights and the round number.\n2. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.\n3. Raise. Starting with this round's first raiser and going in seat order, each player in turn raises one active character's height by 1. A character may go from 4 to 5 only if no character is currently at height 5. No height may exceed 5. A player with no legal raise passes.\n4. Election. If a character is at height 5, it is the candidate, and every player votes Yes or No at the same time. A player with no No cards left must vote Yes. If no character is at height 5, skip steps 4 and 5.\n5. Resolve.\n   - If all votes are Yes, the candidate's height becomes 6 (king) and the game ends after this round.\n   - If any vote is No, each No voter loses one No card and the candidate's height becomes -1 (eliminated for the rest of the game). Only the number of No votes is announced, not who cast them.\n6. Rotate. The first raiser for the next round is the next seat in seat order.\n7. End check. The game ends if a king was crowned or the round limit has been played.\n\nSCORING. Each player reveals their goal. For each of their 3 characters they score:\n- 10 if its height is 6 (king);\n- 0 if its height is -1 (eliminated);\n- otherwise its height (0 to 5).\nA player's score is the sum of these three values.",
    "objective": "The player with the highest score wins. If two or more players tie for the highest score, the game is a draw among them.",
    "expected_effect": "Every seat now has the same goal structure and the same number of first-raiser turns, so the seat edge is gone.\n\nPlay centres on four things:\n- raising decoys to hide one's goal;\n- inferring rivals' goals from their raises and from anonymous No counts;\n- spending the two No cards on threatening candidates rather than wasting them;\n- choosing whether to let a candidate through to end the game while ahead.\n\nTalk passes both tests.\n- What players disagree about: each candidate has exactly one owner who wants it crowned. The others want it vetoed unless they lead and want the game over.\n- Why reasoning is needed: players propose vetoes, claim false goals and try to bait rivals into spending No cards.\n- How a follower loses: a player who obeys the call 'everyone veto C' may be spending a scarce No for the caller's benefit, or may be fooled into crowning the caller's own character.\n\nThe thoughtless policies all lose. Always Yes crowns rivals' characters. Always No exhausts both cards and may hit the player's own characters. Always raising one character exposes it to a veto. When everyone plays well, the deal only fixes who owns what. Every goal is equally placed, so reading and timing decide the winner."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 3,
    "attributes": 19,
    "hidden_elements": 3,
    "random_draws_per_round": 0,
    "rounds": 16
  }
}
```
````
