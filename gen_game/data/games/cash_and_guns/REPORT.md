# cash_and_guns: ready for review

Built from the variation **Cash and Guns: Standoff** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the loot draft with an equal split of a single round pot among the players who are still standing and unwounded. The pot size is one random draw, announced before any choice. (fixes: The loot draft is a variable-length sequence of picks that can circle the table several times. The engine cannot build that, and it would need far more than 4 choice steps per round.): The split keeps the incentive that each rival removed raises your share. It needs only one step. Announcing the pot first gives planning content: save Bangs for big pots, stand when the pot is worth the risk.
- Remove the Godfather token and redirect. (fixes: The Godfather redirect adds an extra sequential choice phase and a seat-like advantage, and it is hard to fit beside aiming and standing.): This removes a sequential sub-phase and a positional edge, and keeps the round to three simultaneous choices.
- Drop loot card types and the diamond bonus. Loot is plain cash in thousands. (fixes: Card-level loot types (cash values, diamonds, special cards) and the separate diamond-majority bonus add hidden-state bookkeeping without adding much inference.): This keeps the single strong hidden element, which is the bullet hand.
- Limit play to 3-5 players, suggested 4. Keep exactly 8 rounds and 8 bullets (3 Bang, 5 Click), with one bullet spent every round. (fixes: With up to 8 players the shooting becomes chaotic and skill shows only noisily.): With fewer players, who shot whom matters and can be remembered and punished. Because every card is spent exactly once, Bang-counting is a precise inference problem.
- Turn pointing into a simultaneous text choice of a target and a bullet. Targets are then announced openly before the stand-or-lie decision. Add one simultaneous message per round before aiming. (fixes: Physical gun pointing has to become a text choice.): Players still see exactly who is aiming at them, as in the original. The message adds threats, bluffs and temporary alliances. Only one player can win, so following a proposal can cost you.

Objective: Only players still alive at the end can win. The living player with the highest cash wins. If living players are tied on cash, the one among them with the most wounds wins. If still tied, the game is a draw. If exactly one player is alive, that player wins. If no player is alive, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SINGLE STANDOFF, payoff to the target T, who is aimed at by one shooter S. Pot P averages 10k; s is T's share if T is unhurt.
- T Stands, S holds Bang and Stands: T gets 0 and 1 wound. S's Bang is spent and revealed.
- T Stands, S holds Click and Stands: T gets s.
- T Stands, S Ducks: T gets s. S's 
- playable: pass. The rules cover every case:
- Targets are restricted to living others.
- A bullet must be held, and 8 cards over 8 rounds means a card is always available. Round 8 is forced.
- Fired versus discarded is explicit, wounds are simultaneous, and elimination is at ≥3.
- Sharers are defined, the empty-pot
- reasoning_over_luck: pass. The only random draw is the pot (6-14k). It applies equally to all sharers in a round, so it shifts stakes, not who wins. Its effect is weighting: an elimination or duck in a 14k round matters more, which estimates chance at well under 15% of the result.
There is no random deal. All hands start iden

## Complexity

- steps_per_round: designed 16, built 13, limit 20
- choice_steps_per_round: designed 3, built 4, limit 4
- attributes: designed 12, built 33, limit 20 (built: 80)
- hidden_elements: designed 2, built 6, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 8, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: cash 0, wounds 0, alive, a hand holding both Bang and Click; all Duck so nothing else changes
- pass: Round counter increases by 1 (pot is random, not asserted)
- pass: Talk step changes nothing; the round still plays
- pass: Aim offers only other living seats and only bullet types in hand
- pass: Targets are shown publicly; bullets are not revealed
- pass: Stances are recorded and announced
- pass: Chosen bullet leaves the hand even when not fired
- pass: Shooter and target both Stand: bullet fired and revealed
- pass: A Duck by shooter or target discards the bullet unrevealed and harmless
- pass: Two fired Bangs on one target give 2 wounds
- pass: Simultaneous shots: a player eliminated this round still fires
- pass: Third wound eliminates; cash is kept and the player sits out later rounds
- pass: Two unwounded Standers split the pot equally; the Ducker gets nothing (wounds decide the equal cash)
- pass: Everyone Ducks: the pot is lost
- pass: A Ducker and a wounded Stander gain no cash
- pass: Last survivor wins
- pass: Both last players eliminate each other: no winner
- pass: After round 8 the richest living player wins
- pass: Cash tie broken by most wounds
- pass: Tied on cash and wounds: shared win
- pass: Eliminated rich player cannot win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 1': 10, 'seat 3': 13, 'seat 2': 7, 'seats 1 and 3': 1, 'seat 4': 4, 'seat 5': 5}, 56-154 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 125.3 decisions, prompts of 166 characters on average (longest 256)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 19, 'seat 3': 20, 'seat 2': 19, 'seats 1 and 3': 1, 'seats 2 and 3': 1}
- always `first@seat1`: won 47, lost 13, drew 0
- always `first@seat2`: won 46, lost 14, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The game file lets eliminated players keep acting: dead seat 3 was offered aims and stances, and its seat stayed in other players' target offers. It also stores `target` as a number, although the interface declares it as text. The extra wounds (4 instead of 3) are most likely shots from dead seats that should no longer fire.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer chose 4, so it is kept. The minimum is 3, because with 2 players aiming has no choice and splitting the pot is trivial. The maximum is 5, because beyond that a single gun matters little and the talk is long.
- Keep a simultaneous talk poll each round, broadcast to all: The source requires it. Players disagree about who should duck and who gets shot, so non-binding threats and bluffs about bullets give them something to reason about.
- Target and bullet are taken in two consecutive polls, with the target held in a hidden aim_target until GUNS SHOWN: A step takes one answer. Holding the target hidden keeps both choices simultaneous and secret, as the source requires.
- rank_by = alive*1000000 + cash*1000 + wounds, with min_to_win 1000000: Only living players can win, cash comes first and wounds break ties. Cash differences are multiples of 1/60, so the weight 1000 keeps them above the maximum wound gap of 2. The bar makes an all-eliminated game end with no winner.

## Simplifications

- A tie on both cash and wounds is a shared win: The engine has no separate draw: players level at the top share the win, which stands for the source's draw.
- Comparing a player's stance with their target's stance, and counting the Bangs aimed at a seat, uses the player-attribute-compare workaround: The engine has no direct operand for another player's attribute, so this costs extra steps.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: "you.bullet != ''" reads `you` where there is no player
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (aim_target, bullet, stance, target) in `your_starting_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: player attribute `alive` is never changed in 3 random matches, so nothing updates it. Steps that name it: the gang assembles, elimination. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
