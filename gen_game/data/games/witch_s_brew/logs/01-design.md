# 01 design

- time: 2026-10-27T22:07:18+00:00 (94.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 b5180c5434000a3a, reply sha256 27e966bcb85afe5b

## Sent

````
Original game: Witch's Brew
Players in the original: 3 to 5

Original rules:
Each player has 12 role cards and visible ingredients and gold. A set starts with each player secretly choosing 5 roles to hold. The start player plays a role face-up and claims it. Clockwise, each other player who holds that same role must reveal it and choose: contest by claiming the role for themselves, forcing the previous claimant to discard with nothing, or accept the weaker favor and then discard. Players without the role pass. The last unchallenged claimant must execute the full action. Winner starts next round. A role cannot be played twice in a set. When all 5 cards are spent, a new set starts with a fresh selection of 5. The game ends when collectively at least four raven potions have been taken; score is potion points plus vial tokens.
````

## Reply

````
```json
{
  "original_summary": "Witch's Brew is a 3-5 player role-claiming card game. Each set, players secretly keep 5 of 12 roles. When a role is led, every other holder must reveal it and either take over the claim, leaving the previous claimant with nothing, or accept a weaker favour. The last claimant performs the strong action, and potions and ingredients turn into points until a raven-count ending.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Always claiming loses when a later player holds the same role: the early claimant gets nothing instead of the favour. Always accepting never gets strong actions. Turn order matters, but it rotates through the start player, so no seat has a lasting edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Choosing which roles to keep, predicting who else kept them, and timing a contest or a concession are skilled decisions. The only randomness is in how ingredients and potions come out, and it is modest."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading opponents' hands from revealed and spent roles can be refined without limit. A weak player still collects favours."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must infer who holds which role from earlier reveals and from what each rival needs, and plan their hand across a set."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The score is potion points plus vial tokens, all countable."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "There are 12 distinct role actions on an ingredient, gold and potion economy, a variable raven-based ending, and a sequential clockwise chain of contests inside each lead. This far exceeds the step and attribute limits."
    }
  ],
  "problems": [
    "Twelve roles, each with a different action over ingredients, gold, potions and ravens, need far more steps and attributes than the platform allows.",
    "The ending depends on a raven count reached by an uncertain number of leads, so game length is unpredictable.",
    "The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer.",
    "The leader can run out of held roles to lead after spending cards in responses, which makes leading undefined unless the rules handle it.",
    "The resource economy hides the core decision (contest or concede) behind bookkeeping that adds no reasoning."
  ],
  "changes": [
    {
      "what": "Six roles, each with a fixed strong value and weak value paid directly in points. One role, the Thief, takes points from the leader in score instead.",
      "why": "This keeps the strong-versus-weak trade-off and one interactive role, without an economy.",
      "fixes": "Twelve roles, each with a different action over ingredients, gold, potions and ravens, need far more steps and attributes than the platform allows."
    },
    {
      "what": "Points are awarded immediately and the separate resource economy is removed.",
      "why": "The only decisions left are which roles to hold, what to lead and whether to contest, which is the heart of the game.",
      "fixes": "The resource economy hides the core decision (contest or concede) behind bookkeeping that adds no reasoning."
    },
    {
      "what": "Fixed length: 3 sets, each of exactly N leads (N = number of players). Every player leads once per set, and set k starts with player k.",
      "why": "Length is predictable and short (9-15 rounds), and leading positions are equal for every seat.",
      "fixes": "The ending depends on a raven count reached by an uncertain number of leads, so game length is unpredictable."
    },
    {
      "what": "All holders respond at the same moment (Contest or Yield). The claim is then resolved clockwise from the leader: the last contester in clockwise order takes the strong action.",
      "why": "This keeps the original's 'the later claimant takes over' rule in one simultaneous poll. Nobody sees the others' choices, so a contester must infer whether a later player holds the role and will contest.",
      "fixes": "The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer."
    },
    {
      "what": "The leader may name any role not yet led this set, held or not. A leader who does not hold the named role earns nothing even if uncontested, and only the engine knows whether they hold it.",
      "why": "This guarantees a legal lead. It also adds a bluff: a leader can name a role they think a rival holds, forcing that rival to spend the card on a weak result.",
      "fixes": "The leader can run out of held roles to lead after spending cards in responses, which makes leading undefined unless the rules handle it."
    },
    {
      "what": "Simultaneous one-message talk after the role is named and before responses.",
      "why": "Players can claim to hold the role ('I have it and will contest') to scare earlier holders into yielding, or hide their holding. The claims are unenforced, so they must be read for bluffs.",
      "fixes": "The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer."
    }
  ],
  "keeps": [
    "Secretly choosing a subset of roles to hold at the start of each set.",
    "Leading a role and claiming it; every other holder must reveal it and either contest (take over the claim, leaving the previous claimant with nothing) or concede for the weaker favour.",
    "The last unchallenged claimant gets the strong action; each role can be led only once per set; cards are spent when used.",
    "Witch, Raven, Alchemist, Druid, Herb Hag and Thief flavour, with the tension between greed and safety."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The contest-or-concede core over hidden hands is excellent reasoning material. Only the resource economy and the sequential chain need cutting, and both can be streamlined."
  },
  "variation": {
    "name": "Witch's Brew: Claims",
    "summary": "Players secretly hold 3 of 6 roles each set. A leader names a role, then all other holders simultaneously contest or yield. The last contester clockwise wins the strong reward, earlier claimants get nothing and yielders get a small favour. Highest total after 3 sets wins.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SETUP. N players (3-5) sit in a fixed clockwise order, numbered 1 to N. Everyone starts with 0 points. The game has 3 sets of N rounds each (3N rounds in total).\n\nROLES. There are six roles, each with a strong reward and a weak reward:\n- Witch: strong 5, weak 2.\n- Raven Keeper: strong 6, weak 0.\n- Alchemist: strong 4, weak 1.\n- Druid: strong 3, weak 2.\n- Herb Hag: strong 2, weak 1.\n- Thief: the strong reward is to take 3 points from the other player with the highest current total (ties go to the tied player first clockwise after the Thief). The Thief gains 3, that player loses 3, and a total may go below 0. Weak 1.\n\nSTART OF A SET. At the start of each set, every player secretly and simultaneously chooses exactly 3 different roles to hold for that set. Hands are private; the engine records them. The list of roles led this set is emptied.\n\nLEADER. In set k, the first round's leader is player k (set 3 with 3 players: player 3). Leadership then passes clockwise each round, so every player leads exactly once per set.\n\nEACH ROUND:\n1. The leader is announced.\n2. The leader names one role that has not yet been led in this set. They may name a role they do not hold. The named role is added to this set's led list.\n3. Talk: every player at the same time writes one short message without seeing the others. All messages are then shown to everyone. Messages bind no one.\n4. Responses: every player other than the leader who holds the named role must respond. All of them choose at the same moment, either CONTEST or YIELD. Players who do not hold it pass automatically.\n5. Reveal: all responses are shown, so everyone learns who held the role.\n6. Resolve: start from the leader and go clockwise. The leader is the first claimant, and each contester, in clockwise order, takes over the claim. The final claimant is the last contester in clockwise order after the leader, or the leader if nobody contested.\n   - The final claimant gets the role's strong reward. Exception: if the final claimant is the leader and the leader does not hold the named role, they get nothing.\n   - The leader, if overtaken, gets 0. Every contester overtaken by a later contester gets 0.\n   - Every player who yielded gets the role's weak reward.\n7. The named role is removed from the hand of the leader (if held) and of every responder. A role cannot be led again this set.\n8. Scores are announced and leadership passes clockwise.\n\nRoles held but never led or responded to during a set are simply lost when the set ends. After round 3N, the game ends.",
    "objective": "After the final round, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.",
    "expected_effect": "Each decision depends on inferring who holds what. A contester close after the leader risks being overtaken by a later holder and ending with 0 instead of the weak reward. A contester last in clockwise order is nearly safe, so position relative to the leader shapes every choice. As roles are revealed and spent, players can increasingly deduce hands, and later leads in a set become sharper. Hand selection is a guessing game: crowded high-value roles (Raven Keeper, Witch) get contested, while quieter roles pay strong rewards more often. The Thief punishes the score leader. Simple policies all lose: always contesting gives 0 too often from early positions, always yielding never collects strong rewards, and always leading your best role invites contests. Talk passes both tests. There is real conflict because only one player can win and claims cost nothing. An early holder who believes a later player's 'I hold it, I'll contest' and yields may have been bluffed out of a strong reward. An early holder who ignores a true warning and contests gets 0. Players disagree over who takes each strong reward, so following someone else's proposal usually hands them the points."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 4,
    "attributes": 9,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 15
  }
}
```
````
