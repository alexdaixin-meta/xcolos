# turn_the_tide: ready for review

Built from the variation **Turn The Tide: Short Seas (revised)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Played Weather cards stay face up in front of the player who played them. At the end of each deal each player gathers their played cards plus their one unplayed card (11 cards) into one hand and passes it to the player on their left. (fixes: Fatal contradiction: played Weather cards were discarded, so after 10 hands every hand was empty and the 'pass your 10 cards left' rule passed nothing. Deal 2 could not be played.): Hands now exist at every deal, and each player plays each original hand exactly once over P deals.
- Deal 11 Weather cards per player for 10 hands per deal, so one card per hand per deal goes unplayed. (fixes: The last hand of each deal was forced, because only one card remained, which wastes a round.): The 10th hand becomes a real choice between two cards.
- The unplayed card stays face down when the hand is passed, and the set-aside cards stay unseen. A card becomes public only when played. The rules state exactly who knows what. (fixes: Hidden information after deal 1 was thin, because every card ended up public.): Some hidden state survives every deal: rivals know 10 of a hand's 11 cards at most, and they must infer the rest from the unseen pool and the holder's past choices.
- State in the rules that every played card is public and that, from deal 2 on, most of each hand is known. (fixes: The rules implied hands stay hidden, when in fact every card becomes public once played, so from deal 2 on hands were fully known.): Players reason from the correct information.
- Everyone starts each deal at Tide level 15 instead of 11. (fixes: The starting Tide level of 11 sat at the median of the Tide deck, so in 4-player games a passive 'always play lowest' policy rarely ended up highest and was hard to punish.): 15 is above the average High Tide (about 14) and well above the average Low Tide (about 7). A player who never takes a Tide is usually the highest and bleeds lifelines, so dropping requires spending a high card at the right moment.
- Sunk players still play cards and can still take Tide levels, but their level is ignored when finding the highest level. (fixes: Sunk players' Tide levels still counted when finding the highest level while they lost nothing, so a Sunk player at a high level shielded everyone else and removed pressure.): Pressure falls on the players still at risk. Sunk players keep the hand-passing cycle intact and can still affect who takes which Tide.
- Define deal start and end by deal number (deals 1 to P) instead of listing round numbers. (fixes: The rules said 'rounds 1, 11, 21, 31' even for 3 players, who only have 3 deals.): The rules are correct for both 3 and 4 players.

Objective: After the last deal, the player with the highest game score wins. If several players tie for the highest score, the tied player with the lowest Tide level at the end of the last deal wins. If that is still tied, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. The game is symmetric. All choices are simultaneous, and over P deals each player plays each of the P original hands exactly once, so seat order and deal quality even out. The key decision: winning a hand gives you Low Tide, finishing second forces High Tide on you, and anyone else KEEPS their level
- playable: pass. The rules are complete and deterministic:
- Ties for highest Weather card are impossible, because the numbers are unique.
- Ties for highest Tide are handled: all players at that level lose a lifeline.
- Sunk at 0 lifelines is defined, and every-player-Sunk is handled.
- The card count works. Each p
- reasoning_over_luck: pass. There is real inference.
- Tide counting: the deck composition 1-20 is known, and each reveal narrows what remains. This tells you when to spend high cards.
- Hand tracking: from deal 2 on, you know all played cards of the hand you receive, and of the hands opponents hold, except 1 to 3 hidden cards

## Complexity

- steps_per_round: designed 13, built 12, limit 20
- choice_steps_per_round: designed 1, built 1, limit 4
- attributes: designed 12, built 33, limit 20 (built: 80)
- hidden_elements: designed 3, built 12, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 4 cards set aside and the weather deck is empty (still true after one hand)
- pass: Setup: every score is 0 and still 0 after the first hand of deal 1
- pass: Start of deal resets sunk and lifelines (highest card never loses a lifeline whatever the random tide)
- pass: Start of deal 2: hands pass to the left, so each seat plays a card from its right-hand neighbour's old set
- pass: Two tide cards 3 and 18 drawn: low 3 to the highest card, high 18 to the second
- pass: The chosen card leaves the hand and joins played; only cards in hand are offered
- pass: A sunk player with the highest card still takes low tide
- pass: Highest-tide player at 0 lifelines becomes sunk
- pass: All players level at the highest tide each lose a lifeline
- pass: A sunk player with the highest tide is ignored; the non-sunk maximum loses lifelines
- pass: When every player is sunk, no lifelines change
- pass: After hand 10, a non-sunk player adds remaining lifelines to score
- pass: After hand 10, a sunk player loses 1 point
- pass: After hand 10, the lowest non-sunk tide gains a bonus point
- pass: Hand 10 ends the deal and deal_no moves to 2
- pass: Game ends after hand 10 of deal P (3 players) and the highest score wins
- pass: Tied score broken by lower final tide
- pass: Players level on score and tide share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 11, 'seat 1': 12, 'seat 2': 12, 'seat 4': 5}, 90-160 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 125.0 decisions, prompts of 201 characters on average (longest 203)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 26, 'seat 1': 19, 'seat 2': 15}
- always `first@seat1`: won 11, lost 49, drew 0
- always `first@seat2`: won 10, lost 50, drew 0
- always `last@seat1`: won 17, lost 43, drew 0
- always `last@seat2`: won 17, lost 43, drew 0

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer suggests 4, and the deck size and deal count scale with P. With fewer than 3 players, the highest and second-highest cards decide everyone's Tide. More than 4 is outside the deck design.
- No talk phase: The rules state there is no talk phase.
- Tie-break encoded as score*100 - tide: Tide is between 1 and 20, so it never outweighs a point of score, and a lower tide ranks higher.
- Hand passing modelled with a pass_buffer list: All players pass at once, so each 11-card set is gathered first and then moved to the left-hand neighbour.
- Count-dependent numbers written per player (weather_cards_per_player 12, deals_per_player 1, set_aside_cards_per_player 1): Parameters must be plain numbers. The Weather deck is 12*P cards, there are 1*P deals and 1*P cards set aside, so each holds at 3 and at 4 players.

## Simplifications

- The source's draw becomes a shared win: The engine has no separate draw: players level at the top share the win.
- Start-of-deal and end-of-deal work is done by steps conditioned on hand_no: The step list is flat, so these steps run every round but act only on hand 1 or hand 10.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Deal 1, hand 1: Low Tide 5, High Tide 6. Choose one Weather card from your hand {hand} to '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Deal 1, hand 1: Low Tide 5, High Tide 6. Choose one Weather card from your hand {hand} to '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Deal 1, hand 1: Low Tide 5, High Tide 6. Choose one Weather card from your hand {hand} to '); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: it plays, but part of it does nothing: game attribute `card_numbers` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
