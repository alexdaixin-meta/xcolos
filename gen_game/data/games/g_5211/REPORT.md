# g_5211: ready for review

Built from the variation **5211: Mirror Hands** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Every player gets an identical fixed 14-card hand: 4 colours each with values 1, 2 and 3, plus 2 Kododos. There is no deck and no refills. (fixes: Luck of the deal and of the per-turn refill draws strongly affects who can control a colour or hit the Kododo count. This is a lottery element.): This removes hand luck entirely. Because played cards are public, a player who tracks the plays knows what everyone has left, so the contest is about predicting intent and timing.
- Removed all in-game drawing. The only random event is a setup deal of distinct secret bonus colours. (fixes: Per-player refill draws every turn need several random draws per round, which the platform limits to one.): This fits the limit of at most one random draw per round.
- Each round is two simultaneous card plays: one face-down card, a reveal, then a second face-down card, then a reveal. This replaces the original three turns of 2+1+1 cards. (fixes: Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps.): It keeps the 'see part of the table, then commit more' tension in far fewer steps.
- Cut to 4 colours. Resolution is a single rule: the non-busted colour with the strictly highest count scores, and if the top is tied nothing scores. (fixes: Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps.): A single arithmetic comparison replaces the cascade. Ties still kill the colour, as in the original.
- The game is fixed at 7 rounds, so all 14 cards are played. (fixes: The game length (a 100-card deck run down) is too long for the platform.): This keeps it short. The forced endgame also rewards planning which cards to save.
- Each player gets a secret bonus colour, distinct from everyone else's, and earns +1 per scored card of that colour. (fixes: Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent.): It adds a symmetric hidden type. Each type has equal total value, but it changes which colours you want to win. Players must infer each other's bonus colours from their plays and talk.
- Added a simultaneous one-message talk phase before the first card each round. (fixes: Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent.): It allows bluffing and temporary alliances to swing a majority. Since only one player can win and players hold different bonus colours, proposals are self-interested and following one blindly can tie or bust a colour.

Objective: The player with the highest total score wins. If players are tied on total score, the one among them with the higher scored-card count wins. If they are still tied, the game is a draw among the tied players.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. There are no seats and no move order: every choice is a simultaneous poll, and all hands start identical. Each player holds 4 colours × (1+2+3) = 24 colour points plus 2 Kododos × 3 = 6, so 30 base points. A bonus colour adds at most +3 (one per card). Per-round payoffs for a two-card play: KK score
- playable: pass. The rules are complete. They specify the hands, the K = n-1 test, the bust threshold n+1, the unique-maximum rule among non-busted colours with count ≥ 1, the 'nothing scores' cases, the bonus +1 per card, the scored-card count, and the tie-break followed by a draw. The game is finite: exactly 14 ca
- reasoning_over_luck: pass. The only randomness is the setup deal of distinct bonus colours, worth at most +3 per player. It is symmetric: everyone gets one, and no colour is intrinsically better. With all players playing well, the result is decided by things players control. One is which colours each player steers into scorin

## Complexity

- steps_per_round: designed 17, built 14, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 14, built 31, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 7, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every hand holds 14 cards, so after one round of two plays each hand holds 12
- pass: Setup: 3 players take 3 distinct bonus colours, leaving 1 in the pool
- pass: Setup: 4 players take all 4 bonus colours
- pass: Setup: scores and scored cards start at 0 (still 0 after a round where nothing scores)
- pass: Talk poll happens and the round completes
- pass: First card leaves the hand
- pass: Second card comes from the remaining hand: a seat holding K and R1 that plays K first is left with only R1
- pass: 3 players, 2 Kododos played: Kododo scores 3 per K
- pass: 4 players, 3 Kododos with one seat playing two: that seat gains 6 points and 2 cards
- pass: 4 players, 2 Kododos: Kododos score nothing and Red scores
- pass: Red played 5 times with 4 players busts; Green scores
- pass: 3 players: single most-played colour Red scores its face values
- pass: Bonus colour Red with R3 and R2 while Red scores gives 7
- pass: Red and Blue tie for the highest count: nothing scores
- pass: All 8 Kododos played: no eligible colour and nothing scores
- pass: Round 7 plays the last two cards and the game ends
- pass: Tie on score broken by scored_cards
- pass: Players tied on score and scored_cards share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 14, 'seat 3': 11, 'seat 2': 12, 'seats 1 and 3': 1, 'seat 4': 2}, 59-80 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 73.5 decisions, prompts of 108 characters on average (longest 134)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 19, 'seat 3': 20, 'seat 2': 15, 'seats 1 and 3': 4, 'seats 1 and 2': 1, 'seats 1, 2 and 3': 1}
- always `first@seat1`: won 33, lost 26, drew 1
- always `first@seat2`: won 42, lost 17, drew 1
- always `last@seat1`: won 47, lost 11, drew 2
- always `last@seat2`: won 48, lost 11, drew 1

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer fixed 3-4 and suggested 4. Below 3 the n-1 Kododo threshold and the bust rule lose their tension, and there are only 4 bonus colours, so 4 is the maximum.
- Keep the simultaneous talk poll before the plays: The rules require it. Players disagree about which colour should score, because each has a secret bonus colour, and coordinating exactly n-1 Kododos invites bluffing. A simultaneous poll with broadcast matches 'at the same time, without seeing the others'.
- Card codes R1..Y3 and K: Each card needs a compact text form so hands can be lists and colour counts can be taken by first letter.
- Ranking expression score*100 + scored_cards: scored_cards can never exceed 14, so multiplying the score by 100 puts score first and scored cards second. Players still level share the win, which is the source's draw.

## Simplifications

- Hands are visible only to their owner, while played cards are public: This matches 'hands are private'. Tracking what others hold is left to the players, as the source intends.
- Reveal steps are tell steps over the public first_card and second_card: Cards placed in a poll stay unseen until all answers are in, which is the face-down placement; the tell then reveals them.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (first_card, second_card, first_card, first_card); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
