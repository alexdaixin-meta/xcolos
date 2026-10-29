# the_grimm_forest: ready for review

Built from the variation **Three Pigs: Secret Materials** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the whole Fable deck with one Wolf gather option: instead of gathering, a player sends the Wolf to a location. Nobody gathers there this round, and the pile stays and grows. (fixes: The Fable deck (many unique effects) and the Friend cards (individual powers, forced gifting) far exceed the platform's step, attribute and hidden-element limits.): This keeps the Monster idea of scaring pigs off a location as a single arithmetic rule. It also gives a way to block a leader or punish a predictable opponent, at the cost of your own gathering.
- Remove Friend cards and the draw-a-Fable build action. (fixes: Fable and Friend draws add large luck swings that can override good gather-reading.): This cuts complexity and removes card luck, so outcomes come from gather choices and build timing.
- All choices (gather, and both build actions) are simultaneous polls. Ties for the win are broken by leftover resources, not seat. (fixes: Building in turn order and resolving Fables in turn order give seat-dependent advantages.): This leaves no seat edge.
- Deal each player a secret Favoured Material, for which each section costs 1 instead of 2. Keep each player's stockpile private. Allow at most 2 completed houses of any one material, so every winner needs at least one house in a non-favoured material. (fixes: With any combination of houses allowed and all materials worth the same to everyone, players have no private agenda to hide or infer. The only inference is from public board state.): This gives every player a hidden agenda. Others must infer your type from where you gather and what you build, and stockpiles cannot be reconstructed without knowing your costs. The two-per-material cap forces everyone into a contested second material, so collisions and Wolf blocks are real decisions.
- Set a 15-round cap. If several players finish on the same round, the one with most leftover resources wins. At the cap, compare most houses, then most sections, else draw. (fixes: There is no turn cap or tiebreak for simultaneous finishes, which a fixed-length engine needs.): This guarantees an arithmetic end.
- Add one random bonus each round (+2 to one announced location) and a non-shared Market giving 1 of your favoured material. (fixes: Fable and Friend draws add large luck swings that can override good gather-reading.): The bonus plays the role of the original's Mega resources, a public lure that creates collisions. The Market preserves the 4-player location as a safe but slow option. Both are publicly known before players choose, so they shape decisions rather than decide outcomes.

Objective: The first player to complete 3 houses (at most 2 of any one material) wins. If several do so in the same round, the one with the most leftover resources wins, and a further tie is a draw. If nobody finishes in 15 rounds, the winner is the player with the most completed houses, then the most sections. Any remaining tie is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. COST TABLE. Each house is 3 sections. A section costs 1 in your Favoured Material and 2 otherwise. You may complete at most 2 houses of one material, so finishing needs at least 6 Favoured sections (6 units) plus 3 non-Favoured sections (6 units of one other material): 12 units and 9 sections. With 
- playable: pass. COMPLETENESS. The rules cover every case:
- refill, including the bonus;
- Wolf at a location, with any number of Wolves;
- equal split rounding down, with the remainder staying;
- an empty location;
- unlimited Market;
- builds that cannot be paid, or that would start a third house of one material,
- reasoning_over_luck: pass. CHANCE SOURCES. There are two:
(1) The bonus location (+2, each 1/3). It is announced BEFORE choices, so it is information to act on, and a crowd at the bonus pile can split it to nothing.
(2) The Favoured deal. It is symmetric in 3-player games. In 4-player games it is moderately asymmetric in 2/3 

## Complexity

- steps_per_round: designed 15, built 19, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 15, built 51, limit 20 (built: 80)
- hidden_elements: designed 2, built 11, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 15, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: 3 players: the 3-card favour deck is fully dealt, one card each
- pass: 4 players: 6-card favour deck, 4 dealt, 2 remain
- pass: At start every pile is 0 and nothing is built
- pass: Market gain changes a private stock that enables only the owner to build
- pass: Round begins: round becomes 1 and bonus is drawn from the locations list
- pass: Refill: each pile +3, bonus Forest gets +5
- pass: Talk step runs for all and the round completes
- pass: Gather choice offers all seven options and choices are public
- pass: Wolf at Fields: gatherer gets nothing and pile unchanged
- pass: 5 straw split by 2: each gets 2, 1 stays
- pass: Unchosen piles carry over
- pass: All choose Market: each gains 1 favoured and builds it at cost 1
- pass: Wolf chooser gains nothing and can build nothing
- pass: Lone gatherers empty their piles; choices and piles public (bonus-independent)
- pass: Favoured section costs 1, other costs 2
- pass: Build adds to the unfinished house, or starts a new one at the Floor
- pass: Roof completes the house: done +1, completed +1, progress back to 0
- pass: No third house of a material, and unaffordable builds are not offered
- pass: Building a section adds 1 to sections
- pass: Exactly 2 build actions per round even with stock for more
- pass: Third completed house sets finished and ends the game after the round
- pass: Single finisher wins over a non-finisher with more leftovers
- pass: Two finishers: most leftover materials wins
- pass: Two finishers with equal leftovers share the win
- pass: Round 15 ends with no finisher: most completed, then sections
- pass: Round 15 ends with a full tie at the top: shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 14, 'seat 1': 11, 'seat 2': 14, 'seats 1 and 3': 1}, 73-175 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 148.7 decisions, prompts of 135 characters on average (longest 224)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 22, 'seat 1': 17, 'seat 2': 20, 'seats 1 and 3': 1}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer suggests 3 and the deal is defined for 3 and 4. At 3, the favoured materials are a perfect split, so guessing the others' materials is clean deduction, and contesting a pile or sending the Wolf has a clear target. A fifth player has no deal defined, and splitting the piles that many ways would leave almost no gains.
- Talk kept as one simultaneous poll per round, broadcast to all: The source requires it. Players disagree: each wants a pile to themselves and wants to hide their favoured material. Bluffing about where you will go, or threatening a Wolf, gives everyone something to reason about. The talk is simultaneous because the source says messages are written at the same time.
- Build offers include only legal builds, plus Pass: A seat is never offered what it may not do. The 'counts as Pass' rule stays as a backstop. The filter uses only the seat's own private stockpile, so it leaks nothing.
- Ranking expression: finisher offset 100000, completed weight 100: A non-finisher's value is at most 2*100 + 12 sections, well below 100000, so finishers always rank above everyone. The weight of 100 makes completed houses outrank sections, since sections never reach 100.
- Sections tie-break counts every section ever built, including those in completed houses: The source says 'most built sections' without restricting it.
- Gather and wolf counts are announced after resolution: The source says the piles and the number of gatherers are public, so anyone can work out each gain.

## Simplifications

- Each house is tracked as a progress counter (0-2) plus a completed count per material, not as a list of named sections: Floor, Walls and Roof are always built in order, so a counter holds the same information.
- The 'one unfinished house per material' rule is enforced by the build always adding to the existing unfinished house: The engine has no separate choice to start a second unfinished house, so the limit holds automatically.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `locations` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
