# hats: ready for review

Built from the variation **Ripening Hats** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the random positional order with a public VALUE for each colour. All colours start at 2. A colour gains +1 each round it is not successfully collected (capped at 7) and drops back to 1 when someone collects it. (fixes: P1): Every colour starts identical, so no favourite is dealt an advantage. The table is shaped entirely by what players do, like the original board, where taking a card changes what sits there.
- Replace pushing with the growth/reset rule above. Leaving a colour alone is now the way to 'push' it up, and taking it resets it. (fixes: P3): Value changes now fire every round from players' own choices. The question becomes timing: let your favourite ripen, or cash it now before someone else takes it?
- Keep choices and scores private. Each round announce only, per colour, whether it was collected, contested or untouched, plus how many players took Black. Never announce who took what. Each player sees only their own score until the end. (fixes: P2): Favourites stay genuinely hidden. Players must infer from aggregate patterns which colours someone is protecting and which are free to take, and whether a contest was a block or an accident.
- Make the favourite bonus position-independent (+3 per favourite hat, added privately). Let colour values grow so that ripe colours, including other players' favourites, are worth taking at up to 7. (fixes: P4): Your favourite is worth value+3 to you but only its value to rivals. If you let it ripen, an opportunist may take it at 7. If you take it every round, you earn only 1+3=4 per round while others harvest the ripening colours. 'Always favourite' becomes beatable and every pick is a timing and prediction decision.
- Contests give nothing and do not reset the colour, which keeps growing. The game uses 3-4 players, so 4 or 5 colours compete for a handful of pickers. (fixes: P4): This creates a chicken game over the ripest colours. Grabbing the top value collides with anyone else who reads the table the same way, so players must predict rivals rather than follow a fixed rule.
- Black is always available for a guaranteed 1 point. The cookie and per-kind tracking are dropped. (fixes: P5): Black becomes a real safe fallback when a collision is likely, especially in contested rounds, instead of a cookie token. Removing per-kind flags cuts about 24 attributes.
- Track only 5 colour values, 5 per-round chooser counts, and per player a private score and a private favourite. Step count is recounted honestly. (fixes: P6): This totals 19 attributes for 4 players and about 10 steps, inside the limits.
- Keep simultaneous one-message talk before each choice. (fixes: P7): Players now disagree about who gets the ripe colours. Claims such as 'I'm taking Blue' are cheap bluffs meant to scare others off. Promises to leave someone's favourite alone can be broken, and the aggregate outcome partly reveals who broke them.

Objective: The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Each round is an anti-coordination game. If you are the only player on a colour you get its value v (1 to 7), plus 3 if it is your favourite. If two or more players pick the same colour, all of them get 0. Black always pays 1.

Payoffs for me, given the others' choices:
| My choice | Nobody else on 
- playable: pass. The rules are complete.
- Values start at 2 and are capped at 7.
- Collection (step 4) uses the current value before the update (step 6).
- Contested colours give 0. Untouched and contested colours gain 1; collected colours reset to 1.
- The announcement is anonymous. Each player still knows their o
- reasoning_over_luck: pass. Chance is limited to the setup favourite deal. Its effect is +3 on each collection of that colour, worth about 6-15 points over the game. The deal does not decide the game, because colour values are public and change every round.

There is plenty to reason about:
- Which colours rivals will target, 

## Complexity

- steps_per_round: designed 10, built 12, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 19, built 33, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with all colour values at 2, scores at 0, round 1
- pass: Dealing favourites to 4 players removes 4 colours from the pool (which colours is random)
- pass: Dealing favourites to 3 players leaves 2 colours in the pool
- pass: After round 1 the round number advances and untouched values ripen to 3
- pass: Talk binds no one: after talk every seat still makes its own choice
- pass: Every seat is offered all five colours and Black
- pass: Choosing Black gives 1 point
- pass: Sole chooser of a non-favourite colour gains its value
- pass: Sole chooser of their favourite gains value plus 3
- pass: Two players on the same colour gain nothing, even if it is a favourite
- pass: Statuses are COLLECTED, CONTESTED or UNTOUCHED, with the Black count
- pass: A collected colour resets to value 1
- pass: Contested and untouched colours rise by 1, capped at 7
- pass: Scores accumulate privately across a round without affecting public values
- pass: Game ends after round 12 is resolved; highest score wins
- pass: Tie for highest score is shared

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 9, 'seat 3': 15, 'seat 2': 9, 'seat 4': 6, 'seats 1 and 2': 1}, 72-96 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 84.0 decisions, prompts of 187 characters on average (longest 223)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 16, 'seat 3': 25, 'seat 2': 17, 'seats 2 and 3': 2}
- always `first@seat1`: won 10, lost 49, drew 1
- always `first@seat2`: won 12, lost 48, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer's suggested size is 4, so it is kept. The minimum is 3 because with 2 players the competition over colours is too thin to be interesting. The maximum is 4 because with 5 colours, 4 players still leave room to spread out, while a fifth player would let every favourite be in play and make collisions near-constant.
- Talk is kept as a simultaneous poll with a broadcast: The rules say messages are written at the same time without seeing the others, so a poll fits rather than ask. Talk earns its place because players have conflicting interests. Each wants a ripe colour to themselves, so claiming, warning or bluffing about a favourite gives others something to weigh. Following a claim can cost a player a collision.
- Strategy at the table: A thoughtful player tracks which colours are ripening, reads the COLLECTED and CONTESTED history to infer others' favourites, and uses talk to steer rivals away from their own targets. They also judge when the safe 1 point from Black beats a likely collision.
- Favourites are dealt from a hidden colour_pool list: This makes 'all different' a matter of draw-and-remove, which the engine supports.
- Score is marked observable: The source reveals scores at the end, and tests need the score. It stays ally-visible during play.
- Each player is synced their own score after collection: The source says each player can see their own private score. The source does not say when updates are delivered, so the sync timing is my choice.

## Simplifications

- A tie for the highest score is represented as a shared win: The engine has no separate draw outcome: players level at the top share the win, which corresponds to the source's draw.
- Per-colour counts and statuses are kept as separate table attributes (count_red, status_red and so on): The engine has no lookup by colour, so each colour gets its own counter and status.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (status_blue, status_green, status_purple, status_red) in `your_favourite`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
