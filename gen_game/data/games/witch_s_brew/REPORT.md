# witch_s_brew: ready for review

Built from the variation **Witch's Brew: Claims** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Six roles, each with a fixed strong value and weak value paid directly in points. One role, the Thief, takes points from the leader in score instead. (fixes: Twelve roles, each with a different action over ingredients, gold, potions and ravens, need far more steps and attributes than the platform allows.): This keeps the strong-versus-weak trade-off and one interactive role, without an economy.
- Points are awarded immediately and the separate resource economy is removed. (fixes: The resource economy hides the core decision (contest or concede) behind bookkeeping that adds no reasoning.): The only decisions left are which roles to hold, what to lead and whether to contest, which is the heart of the game.
- Fixed length: 3 sets, each of exactly N leads (N = number of players). Every player leads once per set, and set k starts with player k. (fixes: The ending depends on a raven count reached by an uncertain number of leads, so game length is unpredictable.): Length is predictable and short (9-15 rounds), and leading positions are equal for every seat.
- All holders respond at the same moment (Contest or Yield). The claim is then resolved clockwise from the leader: the last contester in clockwise order takes the strong action. (fixes: The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer.): This keeps the original's 'the later claimant takes over' rule in one simultaneous poll. Nobody sees the others' choices, so a contester must infer whether a later player holds the role and will contest.
- The leader may name any role not yet led this set, held or not. A leader who does not hold the named role earns nothing even if uncontested, and only the engine knows whether they hold it. (fixes: The leader can run out of held roles to lead after spending cards in responses, which makes leading undefined unless the rules handle it.): This guarantees a legal lead. It also adds a bluff: a leader can name a role they think a rival holds, forcing that rival to spend the card on a weak result.
- Simultaneous one-message talk after the role is named and before responses. (fixes: The clockwise contest chain inside one lead is a variable-length sequence of decisions, which the flat step list cannot express. It also hands the last holder perfect information, so nothing is left to infer.): Players can claim to hold the role ('I have it and will contest') to scare earlier holders into yielding, or hide their holding. The claims are unenforced, so they must be read for bluffs.

Objective: After the final round, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Reward table (strong/weak, gain from contesting = strong - weak): Witch 5/2 (+3), Raven Keeper 6/0 (+6), Alchemist 4/1 (+3), Druid 3/2 (+1), Herb Hag 2/1 (+1), Thief 3 plus a 3-point swing against the leader / 1. A contester gets the strong reward only if no holder later in clockwise order also cont
- playable: pass. Rules cover hand selection (exactly 3 of 6, i.e. 20 options as a simultaneous poll), legal leads (any unled role, held or not), who responds, simultaneous CONTEST/YIELD, resolution order, the leader exception, Thief targeting with clockwise tie-break and negative totals, removal of roles, lost roles
- reasoning_over_luck: pass. There are zero random draws. Hands are chosen, not dealt, and no chance element exists apart from opponents' simultaneous choices. Chance share is about 0%.
When all players play well, the outcome comes from hand selection (avoiding crowded roles), the leader's choice of a role it holds that others 

## Complexity

- steps_per_round: designed 16, built 16, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 9, built 31, limit 20 (built: 80)
- hidden_elements: designed 1, built 4, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 15, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Every player starts with score 0 (a round where nobody holds the named role leaves every score at its starting value)
- pass: At the start of a set hands are chosen and the set's first round plays (role choice by chance, only the named role is asserted)
- pass: A new set empties led_list, so a role led in the previous set can be named again
- pass: Set 3 round 2 with 4 players is led by seat 4
- pass: A role already led cannot be named, and the leader may name a role they do not hold
- pass: After the role is named everyone talks, and the round still resolves normally
- pass: Only a non-leader holder is asked to contest or yield
- pass: Responses are revealed: one contester claims, one yielder gets the weak reward
- pass: With two contesters the one furthest clockwise from the leader claims
- pass: A non-leader contester claims Raven Keeper and gains 6
- pass: Leader names a role they do not hold and the only holder yields: no strong reward, the yielder gets the weak 2
- pass: Thief claimed by a contester robs the highest other score, the tie going to the first seat clockwise, and a score goes below 0
- pass: Thief claimed by the leader holding it: the tie between seats 1 and 3 goes to seat 3, first clockwise after seat 2
- pass: A leader holding Herb Hag overtaken by a contester gains 0, and the claimant gains 2
- pass: Two yielders of Druid each gain 2 while the leader holding it gains 3
- pass: Yielding Raven Keeper gives 0 points
- pass: The named role leaves the hands of the leader and the responder, and a non-holder's hand is unchanged
- pass: The last round ends the game and the highest score wins
- pass: Tied top scores at the end share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 9, 'seat 1': 6, 'seats 2 and 3': 2, 'seat 3': 9, 'seats 1 and 3': 2, 'seats 2 and 5': 1, 'seat 4': 7, 'seat 5': 4}, 50-140 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 94.3 decisions, prompts of 145 characters on average (longest 243)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 20, 'seat 1': 12, 'seats 2 and 3': 2, 'seat 3': 23, 'seats 1 and 3': 3}
- always `first@seat1`: won 44, lost 13, drew 3
- always `first@seat2`: won 41, lost 16, drew 3
- always `last@seat1`: won 15, lost 44, drew 1
- always `last@seat2`: won 13, lost 41, drew 6

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer chose 4 and the source range is 3 to 5. Three is the minimum so that claim order and contest bluffing matter; more than 5 would exceed the 6 roles, which could run out within a set.
- Hand choice offered as one pick from the 20 three-role combinations: This guarantees exactly 3 different roles in a single simultaneous answer.
- Talk kept as a simultaneous poll, broadcast to all: The rules specify simultaneous messages. Players disagree about who should claim, so bluffing about holdings is meaningful.
- Leader formula ((set_number-1)+(round_in_set-1)) mod N + 1: This matches 'set k starts with player k' and clockwise passing; with 3 players set 3 starts with player 3.
- Thief tie-break uses the first tied seat clockwise from the final claimant: The final claimant is the one using the Thief's reward.

## Simplifications

- A tie for the top score is a shared win rather than a declared draw: The engine has no separate draw; tied top players share the win.
- Roles left in a hand at the end of a set are discarded by emptying hands at the start of the next set: This has the same effect as losing them at the end of the set.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (set_pick, named_role); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `roles` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
