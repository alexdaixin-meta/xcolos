# 01 design

- time: 2026-10-28T01:31:46+00:00 (93.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ff6b564c23d3b516, reply sha256 c477f4fbbb44532c

## Sent

````
Original game: One Night Revolution
Players in the original: 3 to 10

Original rules:
Each player gets a secret ID token (Rebel or Informant) plus a secret Specialist card giving a night power; three extra IDs go to the HQ. At night eyes closed, controller leads informants to recognize each other, then clockwise each player opens eyes alone to do their Specialist action which may look at or swap ID tokens. By day, players in order claim a Specialist token (may lie) then discuss freely for 5-10 minutes, without looking at cards, trying to deduce current alignments. Then all simultaneously point at someone to Terminate. Most-voted players reveal IDs. If any Informant is terminated, Rebels win. If none or only Rebels are terminated, Informants win. Rebels can also win by voting in a circle with zero eliminations if all Informant tokens are correctly believed to be on HQ.
````

## Reply

````
```json
{
  "original_summary": "One Night Revolution is a one-round hidden-team deduction game. Secret Rebels and Informants use night powers to peek at or swap ID tokens, argue by day, and then vote once at the same moment. The Rebels win if any Informant is terminated; otherwise the Informants win.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Choices do matter, since the vote decides everything. But balance shifts with player count and with the three HQ tokens. Seat order matters at night: later Specialists act on more information, and token swaps can undo earlier actions. A Rebel who always votes for the loudest claimant does about as well as a careful one in many games."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Everything rides on one vote in one round. The deal, the HQ contents and which swaps happened to hit you cause large swings. Over a single game, a strong player often loses through no fault of their own."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Lying about claims, building consistent stories and reading contradictions have no ceiling. A naive player still wins often with their team."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Alignments are hidden and partially revealed by night powers. Claims may be lies, so players must infer who is consistent and who benefits from each story."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The vote tally and the revealed IDs determine the winner mechanically."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The rules depend on an eyes-closed sequence and on Specialist powers that move tokens around. Many Specialist types, the HQ pool and the circle-vote exception make a long rule chain. The free-form timed discussion is real-time and has to become structured messages."
    }
  ],
  "problems": [
    "P1: A single round decides the game, so luck in the deal and the HQ swamps skill.",
    "P2: Many distinct Specialist powers, token swaps and the HQ pool exceed the engine's complexity limits and create order-dependent resolution.",
    "P3: Seat order at night gives later actors an information edge.",
    "P4: The team-only win rule cannot separate a sharp player from a passive teammate, so individual reasoning is not rewarded.",
    "P5: The real-time, timed free discussion does not fit a turn-based, text-only engine.",
    "P6: Randomly dealt roles over several rounds would create a lottery, because whoever is dealt the stronger side more often would end ahead."
  ],
  "changes": [
    {
      "what": "Play 5 rounds (nights) with 5 players instead of one night.",
      "why": "Many rounds average out the swings of a single vote and reward tracking information across nights.",
      "fixes": "P1"
    },
    {
      "what": "Replace all Specialist powers, swaps and the HQ with one night action whose meaning depends on role. A Rebel investigates a player and privately learns their ID. An Informant frames a player, so that any investigation of that player this round reports 'Informant'. Both roles simply name a target, so the night poll does not reveal role. All actions resolve at the same moment.",
      "why": "This keeps the core tension of the original: night information that may be tampered with. A 'Rebel' result is always true, while an 'Informant' result may be a frame. The game fits in one simultaneous step with no swaps.",
      "fixes": "P2"
    },
    {
      "what": "The night action is a simultaneous poll with no clockwise order.",
      "why": "No seat acts on more information than any other.",
      "fixes": "P3"
    },
    {
      "what": "Score individually. When the Rebels win a round, each Rebel gets +2, and each player who voted for a terminated Informant gets +1 more. When the Informants win, each Informant gets +3. The highest total after 5 rounds wins.",
      "why": "Team results still dominate, but the bonus rewards personally identifying an Informant rather than following the crowd. Roles change every round, so totals reflect individual play.",
      "fixes": "P4"
    },
    {
      "what": "Run talk as two simultaneous message rounds. In the first, each player writes a claim. In the second, each player responds after seeing all the claims.",
      "why": "This turns timed discussion into turn-based text without letting later speakers simply copy earlier ones.",
      "fixes": "P5"
    },
    {
      "what": "At the start, one secret shuffle sets a rotating schedule in which every player is an Informant in exactly 2 of the 5 rounds and a Rebel in 3.",
      "why": "Everyone gets the same mix of roles, so the deal changes only who you are each night, not your expected total. The public quota is also a cross-round clue: a player known to have been an Informant twice cannot be one again.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Secret Rebel and Informant teams, with the Informants knowing each other",
    "Night actions that gather or corrupt information about alignments",
    "Day claims that may be lies, followed by discussion",
    "A simultaneous vote to Terminate, in which every player tied for most votes is terminated",
    "Rebels win if any Informant is terminated, otherwise the Informants win",
    "No termination when nobody gets more than one vote (the circle-vote idea)"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core deduction loop of hidden teams, unreliable night information, lying claims and a simultaneous vote fits the engine once powers are reduced to one investigate/frame action and the game is spread over 5 balanced rounds."
  },
  "variation": {
    "name": "One Night Revolution: Five Nights",
    "summary": "Five players play 5 rounds of hidden-team deduction. Each night, Rebels investigate and Informants frame. By day, players exchange two simultaneous rounds of claims and then vote to Terminate. Individual points accumulate, and every player is an Informant in exactly 2 rounds.",
    "players": {
      "min": 5,
      "max": 5,
      "suggested": 5
    },
    "rules": "SETUP: There are 5 players, each starting with 0 points. Before round 1, the engine secretly shuffles the 5 players into a hidden order of positions 1 to 5. This is the only random event in the game. In round r (r = 1 to 5), the Informants are the players at positions r and r+1, with position 6 meaning position 1. The other 3 players are Rebels for that round. As a result, every player is an Informant in exactly 2 rounds and a Rebel in 3. All players are told this quota rule but not the hidden order.\n\nEACH ROUND:\n1. ROLES: Each player is privately told their role for this round. Each Informant is also privately told who the other Informant is.\n2. NIGHT (simultaneous): Every player privately names one other player as a target.\n   - A Rebel's target is investigated.\n   - An Informant's target is framed.\n3. NIGHT RESULTS: Each Rebel is privately told one result about their target.\n   - The result is 'Informant' if the target is an Informant this round, or if the target was framed by at least one Informant this round.\n   - Otherwise the result is 'Rebel'.\n   - A 'Rebel' result is always true. An 'Informant' result may be a frame.\n   - Informants receive no result.\n4. CLAIMS (simultaneous): Every player writes one short message, for example a claimed role, target or result. Lying is allowed. All messages are then shown to everyone.\n5. RESPONSES (simultaneous): Every player writes one more short message. All are shown to everyone.\n6. VOTE (simultaneous): Every player names one other player to Terminate.\n7. TERMINATION:\n   - If the highest number of votes any player received is 1 or less, nobody is terminated.\n   - Otherwise, every player tied for the most votes is terminated.\n   - The round roles of the terminated players are announced publicly.\n8. SCORING:\n   - If at least one terminated player is an Informant this round, the Rebels win the round. Each Rebel gains 2 points, and each Rebel who voted for a terminated Informant gains 1 additional point.\n   - Otherwise, the Informants win the round, and each Informant gains 3 points.\n   - Everyone's totals are announced.\n9. Termination does not remove anyone; all 5 players take part in every round. After round 5 the game ends.",
    "objective": "After 5 rounds, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.",
    "expected_effect": "Night information is asymmetric. A 'Rebel' result clears a player for certain, while an 'Informant' result might be a frame. Rebels must therefore weigh claimed results against each other, and Informants must invent consistent clear results and frame Rebels who would otherwise be trusted. Talk passes both tests. Rebels and Informants want opposite termination outcomes, so a player who just follows the first confident claim can be steered by an Informant into voting a Rebel, which costs their team the round and costs them the +1 bonus. Even among Rebels, the bonus rewards personally voting correctly rather than drifting. The equal role quota removes luck from the role deal. The public quota and the revealed IDs give a cross-round deduction layer, since players can work out who has already served their two Informant rounds. This rewards memory and multi-round planning, and Informants must also hide their history. No simple policy is safe. Always voting for a fixed seat terminates an Informant only by chance, and a Rebel who never investigates or reads claims loses bonus points to Rebels who do."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 19,
    "choice_steps_per_round": 4,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 5
  }
}
```
````
