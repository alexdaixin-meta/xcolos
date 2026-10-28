# loot: ready for review

Built from the variation **Loot: Sealed Raids** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the open-ended multi-ship board with one contest per round. A rotating owner sails one merchant, and every player commits strength to it at the same moment. (fixes: Too many concurrent contests, each with per-color strength tracking and turn-relative claim timing: it cannot be built inside the step and attribute limits.): One contest per round fits about 12 steps and keeps the core attack-versus-defend fight for a merchant.
- Replace the pirate cards with a private budget of 30 crew points per player. Crew committed is spent whether the contest is won or lost, as attacking cards were discarded. (fixes: Several random draws per turn from a large deck: this exceeds the one-draw-per-round limit and lets the luck of the draw (captains, Admiral, high merchants) swamp skill.): This keeps the cost of fighting and the choice to fight or let go, without a deck or any draws.
- Give every player the identical merchant set (3, 5 and 7 gold), one Captain (+6 strength once as an attacker) and one Admiral (an automatic defense once as the owner). (fixes: Endowments are unequal: one player can be dealt captains and 8-gold merchants while another gets 2s and weak pirates, so the draw alone can decide the winner.): Equal endowments mean the result comes from play, not the deal. The trump cards remain as one-shot timing decisions.
- The owner secretly chooses which unsailed merchant to sail. Commitments stay secret, and only the winner, the ship's value and any trump used are announced, so remaining crew stays hidden. (fixes: Card counting by color is an important skill, but it rests on a large hidden state that the platform cannot track.): This replaces card counting with one manageable piece of hidden state: rivals must infer how much crew each player has left from which contests they won, and guess the ship's value from the owner's remaining set and behavior.
- Add one simultaneous message per player before commitments. (fixes: Card counting by color is an important skill, but it rests on a large hidden state that the platform cannot track.): With only one winner, players disagree. Bluffing about a ship's value or one's remaining crew, and proposals to gang up on the leader, are worth reasoning about.

Objective: After the final round, the player with the most gold wins. If two or more players tie for the most gold, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. One contest, owner defense d, attacker commits a (crew), strength a+6 with Captain. Crew is spent whatever the result. Admiral always keeps the ship.

Table for a single unprotected ship with one attacker:
- d=0, a=1: attacker takes the ship.
- d=10, a=10 with Captain (16): attacker takes it.
- d=15
- playable: pass. The rules cover every case:
- Invalid crew amounts are set to 0, and invalid trump declarations are ignored.
- If all bids are 0, the highest is 0, which is not greater than 0, so the owner keeps the ship.
- An attacker tie and a failure to beat the defense both mean the owner keeps the ship.
- With
- reasoning_over_luck: pass. There are no random draws (0 per round), so chance comes only from opponents' simultaneous mixed choices, about 0% from the engine.

Players have several things to infer:
- The value of the sailed ship. It is one of 3, 5 or 7, narrowed by elimination as ships are revealed, and the third sail is know

## Complexity

- steps_per_round: designed 12, built 13, limit 20
- choice_steps_per_round: designed 3, built 4, limit 4
- attributes: designed 14, built 33, limit 20 (built: 80)
- hidden_elements: designed 3, built 10, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 30 crew, 0 gold, ships [3,5,7], Captain and Admiral unused
- pass: With 4 players round 5 is owned by seat 1
- pass: Game with 4 players ends after round 12; owner seat 4 keeps its last ship and wins
- pass: Round 1 begins with seat 1 as owner, offered its unsailed ships
- pass: Owner with several ships chooses the 7 to sail
- pass: Owner with one ship left sails it automatically
- pass: Sailed ship value is revealed at the end of the round
- pass: Talk step runs and the round completes
- pass: Seat with 10 crew may commit up to 10 but not 11, and wins the ship alone
- pass: Committed crew is spent: seat 2 spends all 10, then can commit only 0 as owner and loses its 7
- pass: Captain adds 6: commit 2 + Captain beats defense 7
- pass: Admiral keeps the ship against a 20-crew attack
- pass: Wrong-role and used trumps are not offered
- pass: Attack 8 beats defense 7 and the other attacker's 5
- pass: Attack 7 against defense 7: owner keeps the ship
- pass: Two attackers tied at 10 against defense 0: owner keeps the ship
- pass: Taker adds the ship value to gold: 4 + 3 = 7
- pass: Sailed ship removed and declared trumps marked used
- pass: End of round reveals ship value and taker
- pass: Final round ties seats 2 and 3 at 13 gold: shared win, unspent crew worth 0

## Does the file follow the spec's shape? (flags for a person)

- rule R10 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 3': 13, 'seat 1': 8, 'seat 2': 6, 'seats 1, 2 and 3': 2, 'seat 5': 6, 'seat 4': 5}, 66-187 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 161.0 decisions, prompts of 173 characters on average (longest 245)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 26, 'seat 1': 13, 'seat 2': 17, 'seats 1, 2 and 3': 4}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 1, lost 51, drew 8
- always `last@seat2`: won 12, lost 40, drew 8

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer suggests 4, and the minimum of 3 keeps it from being a plain duel. Two or more raiders are needed for ties between attackers and for a raider to free-ride while others overbid. Beyond 5 players each seat is owner rarely and the ties between attackers dominate.
- Keep the simultaneous talk poll: The source requires it. Players have opposing interests over who raids which ship, so a non-binding message can bluff, threaten or deter, and following someone else's proposal can cost a player.
- The unsailed-ships list is public and a value is removed only at bookkeeping: The source announces the owner's unsailed ships each round. Removing the value at sail time would leak the hidden value before the announcement.
- Strategy at the table: A thoughtful player rations 30 crew over 3 x N rounds. They infer which ship sailed from the remaining list, time the one-shot Admiral and Captain, and use talk to bluff or provoke ties between rival raiders.

## Simplifications

- A tie for the most gold is a shared win instead of a draw: The engine ranks by an arithmetic expression and players level at the top share the win. This is the closest equivalent to 'the game is a draw'.
- The commit poll offers only valid amounts and valid trumps: The engine constrains answers to the offered range, so the source's 'invalid amounts are set to 0' and 'invalid trumps are ignored' rarely trigger. Both are kept as rules anyway.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'you.committed <= you.crew' reads `you` where there is no player
- 2: passed
