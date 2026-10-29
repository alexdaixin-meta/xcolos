# Variation: Witch's Brew: Claims

Players secretly hold 3 of 6 roles each set. A leader names a role, then all other holders simultaneously contest or yield. The last contester clockwise wins the strong reward, earlier claimants get nothing and yielders get a small favour. Highest total after 3 sets wins.

Players: 3 to 5, best with 4

## Review of the original

Witch's Brew is a 3-5 player role-claiming card game. Each set, players secretly keep 5 of 12 roles. When a role is led, every other holder must reveal it and either take over the claim, leaving the previous claimant with nothing, or accept a weaker favour. The last claimant performs the strong action, and potions and ingredients turn into points until a raven-count ending.

- **non_degenerate**: good. Always claiming loses when a later player holds the same role: the early claimant gets nothing instead of the favour. Always accepting never gets strong actions. Turn order matters, but it rotates through the start player, so no seat has a lasting edge.
- **skill_sensitive**: good. Choosing which roles to keep, predicting who else kept them, and timing a contest or a concession are skilled decisions. The only randomness is in how ingredients and potions come out, and it is modest.
- **headroom**: good. Reading opponents' hands from revealed and spent roles can be refined without limit. A weak player still collects favours.
- **reasoning_dependent**: good. Hands are hidden. Players must infer who holds which role from earlier reveals and from what each rival needs, and plan their hand across a set.
- **verifiable**: good. The score is potion points plus vial tokens, all countable.
- **fits_platform**: bad. There are 12 distinct role actions on an ingredient, gold and potion economy, a variable raven-based ending, and a sequential clockwise chain of contests inside each lead. This far exceeds the step and attribute limits.

## Problems

- Twelve roles, each with a different action over ingredients, gold, potions and ravens, need far more steps and attributes than the platform allows.
- The ending depends on a raven count reached by an uncertain number of leads, so game length is unpredictable.
- The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer.
- The leader can run out of held roles to lead after spending cards in responses, which makes leading undefined unless the rules handle it.
- The resource economy hides the core decision (contest or concede) behind bookkeeping that adds no reasoning.

## Changes

- Six roles, each with a fixed strong value and weak value paid directly in points. One role, the Thief, takes points from the leader in score instead. (fixes: Twelve roles, each with a different action over ingredients, gold, potions and ravens, need far more steps and attributes than the platform allows.): This keeps the strong-versus-weak trade-off and one interactive role, without an economy.
- Points are awarded immediately and the separate resource economy is removed. (fixes: The resource economy hides the core decision (contest or concede) behind bookkeeping that adds no reasoning.): The only decisions left are which roles to hold, what to lead and whether to contest, which is the heart of the game.
- Fixed length: 3 sets, each of exactly N leads (N = number of players). Every player leads once per set, and set k starts with player k. (fixes: The ending depends on a raven count reached by an uncertain number of leads, so game length is unpredictable.): Length is predictable and short (9-15 rounds), and leading positions are equal for every seat.
- All holders respond at the same moment (Contest or Yield). The claim is then resolved clockwise from the leader: the last contester in clockwise order takes the strong action. (fixes: The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer.): This keeps the original's 'the later claimant takes over' rule in one simultaneous poll. Nobody sees the others' choices, so a contester must infer whether a later player holds the role and will contest.
- The leader may name any role not yet led this set, held or not. A leader who does not hold the named role earns nothing even if uncontested, and only the engine knows whether they hold it. (fixes: The leader can run out of held roles to lead after spending cards in responses, which makes leading undefined unless the rules handle it.): This guarantees a legal lead. It also adds a bluff: a leader can name a role they think a rival holds, forcing that rival to spend the card on a weak result.
- Simultaneous one-message talk after the role is named and before responses. (fixes: The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer.): Players can claim to hold the role ('I have it and will contest') to scare earlier holders into yielding, or hide their holding. The claims are unenforced, so they must be read for bluffs.

## Kept from the original

- Secretly choosing a subset of roles to hold at the start of each set.
- Leading a role and claiming it; every other holder must reveal it and either contest (take over the claim, leaving the previous claimant with nothing) or concede for the weaker favour.
- The last unchallenged claimant gets the strong action; each role can be led only once per set; cards are spent when used.
- Witch, Raven, Alchemist, Druid, Herb Hag and Thief flavour, with the tension between greed and safety.

## The variation's rules

SETUP. N players (3-5) sit in a fixed clockwise order, numbered 1 to N. Everyone starts with 0 points. The game has 3 sets of N rounds each (3N rounds in total).

ROLES. There are six roles, each with a strong reward and a weak reward:
- Witch: strong 5, weak 2.
- Raven Keeper: strong 6, weak 0.
- Alchemist: strong 4, weak 1.
- Druid: strong 3, weak 2.
- Herb Hag: strong 2, weak 1.
- Thief: the strong reward is to take 3 points from the other player with the highest current total (ties go to the tied player first clockwise after the Thief). The Thief gains 3, that player loses 3, and a total may go below 0. Weak 1.

START OF A SET. At the start of each set, every player secretly and simultaneously chooses exactly 3 different roles to hold for that set. Hands are private; the engine records them. The list of roles led this set is emptied.

LEADER. In set k, the first round's leader is player k (set 3 with 3 players: player 3). Leadership then passes clockwise each round, so every player leads exactly once per set.

EACH ROUND:
1. The leader is announced.
2. The leader names one role that has not yet been led in this set. They may name a role they do not hold. The named role is added to this set's led list.
3. Talk: every player at the same time writes one short message without seeing the others. All messages are then shown to everyone. Messages bind no one.
4. Responses: every player other than the leader who holds the named role must respond. All of them choose at the same moment, either CONTEST or YIELD. Players who do not hold it pass automatically.
5. Reveal: all responses are shown, so everyone learns who held the role.
6. Resolve: start from the leader and go clockwise. The leader is the first claimant, and each contester, in clockwise order, takes over the claim. The final claimant is the last contester in clockwise order after the leader, or the leader if nobody contested.
   - The final claimant gets the role's strong reward. Exception: if the final claimant is the leader and the leader does not hold the named role, they get nothing.
   - The leader, if overtaken, gets 0. Every contester overtaken by a later contester gets 0.
   - Every player who yielded gets the role's weak reward.
7. The named role is removed from the hand of the leader (if held) and of every responder. A role cannot be led again this set.
8. Scores are announced and leadership passes clockwise.

Roles held but never led or responded to during a set are simply lost when the set ends. After round 3N, the game ends.

Objective: After the final round, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

Expected effect: Each decision depends on inferring who holds what. A contester close after the leader risks being overtaken by a later holder and ending with 0 instead of the weak reward. A contester last in clockwise order is nearly safe, so position relative to the leader shapes every choice. As roles are revealed and spent, players can increasingly deduce hands, and later leads in a set become sharper. Hand selection is a guessing game: crowded high-value roles (Raven Keeper, Witch) get contested, while quieter roles pay strong rewards more often. The Thief punishes the score leader. Simple policies all lose: always contesting gives 0 too often from early positions, always yielding never collects strong rewards, and always leading your best role invites contests. Talk passes both tests. There is real conflict because only one player can win and claims cost nothing. An early holder who believes a later player's 'I hold it, I'll contest' and yields may have been bluffed out of a strong reward. An early holder who ignores a true warning and contests gets 0. Players disagree over who takes each strong reward, so following someone else's proposal usually hands them the points.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 9 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 15 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
