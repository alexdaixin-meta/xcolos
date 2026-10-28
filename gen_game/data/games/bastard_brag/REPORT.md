# bastard_brag: ready for review

Built from the variation **Knock Brag (3-player)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Fix the game at exactly 3 players, each with 3 lives. (fixes: The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round.): This caps a round at 3 choices and 3 hand scores, which brings the round inside the step budget.
- Define a round as one pass in which every active player takes exactly one action, starting with that round's leader. The leader moves one active player clockwise every round. Only the leader may knock, and not in the first round of a deal. After a knock, the other players' turns in that same round are their final actions. (fixes: The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous.): A round now always holds one action per active player. Every non-knocker gets exactly one final action without the pass wrapping around. Because the leader rotates, every player gets knock chances.
- Same rule, applied to the knock: since the knocker always acts first in the round, every other player acts after the knock. (fixes: With knocks allowed from any seat mid-pass, players who acted earlier in the pass would get no final action, or the round would have to wrap around.): No player who acted earlier in the pass misses a final action.
- Force a showdown at the end of deal-round 4 when 3 players are active, or deal-round 3 when 2 are active. The deal-round counter counts the rounds of the current deal. (fixes: The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous.): This gives a clear, countable end to each deal. With the rotating leader it also gives each player exactly one chance to knock in a full deal.
- Add the rule: if all remaining players tie for the lowest score, nobody loses a life. Losing lives can then never eliminate everyone. Otherwise the knocker's double penalty applies as normal, and survivors continue. (fixes: The previous variation did not say who wins when every remaining player ties for the lowest score and would reach 0 lives, nor what happens when a knocker is eliminated alongside others.): This closes the empty-table case. A lowest-score tie is the only way every remaining player could reach 0.
- Score each hand with one arithmetic formula on its sorted cards. The showdown only sets a redeal flag. The shuffle and deal happen at the start of the next round. (fixes: The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round.): Scoring needs no lookup and takes 1 step. The shuffle never shares a round with the showdown, so each round has at most 1 random draw.
- State explicitly: runs do not wrap; a knock is the knocker's action for that round; each action is a single compound choice (action type, own card, slot, card to expose). (fixes: The previous variation did not say whether runs wrap, whether the shuffle shares a round with the showdown (only 1 random draw is allowed per round), or whether a knock counts as a turn.): This removes the remaining ambiguities.
- Keep the suitless 36-card deck (values 1 to 9, four of each) and the prial > run > pair > high card ranking. Drop the betting version. (fixes: Suits, flushes and suit tie-breaks in the original need lookup tables the engine lacks.): The suitless deck removes flushes and suit tie-breaks. The ranking order matches the real frequencies in this deck (prial 36, run 448, pair 1728 of the 7140 possible hands). The chip pot cannot be rewarded, so the lives game is the version to keep.
- Use only the lives version, and decide the winner by survival and lives. (fixes: The betting version's chip pot cannot be rewarded by a platform that only decides a winner.): The platform decides only a winner, so a chip pot has nothing to pay into.

Objective: If only one player remains, that player wins. If round 40 ends with two or three players still active, the player with the most lives wins. A tie on lives is broken by the higher last showdown score among the tied players. If they are still tied, or if no showdown has yet happened, the game is a draw between them.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SCORE LADDER. Prial 301-310 > run 204-210 > pair 112-198 > high card 6-23. The bands never overlap: the best pair, 9-9-8, scores 100+90+8=198, below the lowest run, 2-3-4=204. The lowest pair, 1-1-2, scores 112, above the best high card, 9+8+6=23. The exceptions 3-3-3=310 and 1-2-3=210 are explicit 
- playable: pass. COMPLETENESS.
- The deck, hand scoring (with tie behaviour) and the 4 actions are fully specified. Each action has its announcement text.
- Leader rotation is defined across deals and eliminations, including when the previous leader has just been eliminated (next active player clockwise from that se
- reasoning_over_luck: pass. CHANCE. The deal matters. Only 12 cards are in play per deal: 9 in hands and 3 on the table. Players can improve only through the 3 circulating table cards. A strong initial hand (pair or better, about 31%) is a real head start.

SKILL LEVERS.
- Tracking. Every take-up reveals the taken and left val

## Complexity

- steps_per_round: designed 17, built 13, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 14, built 47, limit 20 (built: 80)
- hidden_elements: designed 3, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with 3 lives each, seat 1 leading, deal_round 1
- pass: First deal gives 3 cards to each player and 3 to the table (random cards, only counts asserted)
- pass: Prials score 300+a and 3-3-3 scores 310
- pass: Runs score 200+c, 1-2-3 scores 210, 9-1-2 is not a run
- pass: 8-9-1 is not a run; 4-5-6 and unsorted 3-2-4 are runs
- pass: Pairs score 100 + 10*b + (a+c-b)
- pass: High-card hands score the sum of the cards
- pass: Take up giving card 2 leaves that card face up
- pass: Blind swap with D1 changes the hand but not the face-up card
- pass: Whole-hand swap takes the three table cards and exposes old card 1
- pass: Nobody may knock in deal_round 1
- pass: Only the leader is offered knock in deal_round 2
- pass: A knock forces a showdown at the end of the round; others still swap
- pass: With 2 active players a showdown happens at deal_round 3
- pass: With 3 active players there is no showdown at deal_round 3
- pass: Showdown records every active score, leader 2 acting first
- pass: All scores equal at showdown: nobody loses a life
- pass: A knocker with the lowest hand loses 2 lives
- pass: Two players tied on the lowest score each lose 1 life
- pass: A knocker on 1 life who is lowest drops to 0 and is eliminated
- pass: Leadership skips an eliminated seat and deal_round rises without a showdown
- pass: Last player with lives wins once the other survivor is eliminated
- pass: After round 40 the tie on lives is broken by the last showdown score
- pass: After round 40 players level on lives and score share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 5, 'seat 1': 8, 'seat 2': 7}, 34-90 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 67.0 decisions, prompts of 471 characters on average (longest 476)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 24, 'seat 1': 19, 'seat 2': 17}
- always `first@seat1`: won 22, lost 38, drew 0
- always `first@seat2`: won 23, lost 37, drew 0
- always `last@seat1`: won 13, lost 47, drew 0
- always `last@seat2`: won 14, lost 46, drew 0

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3, and the forced-showdown timing and leader rotation are written for it. A 3-seat table already gives rivals whose swaps and exposed cards can be read. The player's strategy is to infer opponents' hands from what they take and leave face up, to decide when to knock, and to avoid feeding a strong card into U.
- No free-talk step before actions: The source has no talk, and adding it would add a mechanic.
- Cards are named by hand position 1 to 3 in the choice options: Each action must be a single choice carrying every detail. The player sees their hand list, so a position identifies the card.
- Lives are floored at 0 when a loss would make them negative: The player is eliminated either way, and flooring keeps the ranking expression clean without changing who wins.
- Whole-hand swap puts the two unexposed old cards into D1 then D2 in their hand order: The source does not say which goes where. Nobody sees D1 or D2, so the order does not matter.
- rank_by = lives*1000 + last_showdown_score: Scores are at most 310, so lives always dominate and the showdown score breaks ties. Eliminated players have 0 lives and cannot tie with a survivor. A showdown happens at least every 4 rounds, so by round 40 one has always occurred.

## Simplifications

- The turn order is one ask step running clockwise from leader_seat and skipping eliminated seats, rather than fixed seat order: The engine asks in a flat sequence; the starting seat is taken from the table attribute leader_seat.
- Hand reveal at showdown is an announcement listing each active hand and score, not a change of the hand's visibility: The engine reveals through messages; hand_score is public.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Round 1, deal-round 1. You act first this round. Your hand (positions 1, 2, 3): {hand}. Fa'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Round 1, deal-round 1. Knocker this deal (0 = nobody): 0. Your hand (positions 1, 2, 3): {'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Round 1, deal-round 1. Knocker this deal (0 = nobody): 0. Your hand (positions 1, 2, 3): {'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `base_actions` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
