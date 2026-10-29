# sedmice: ready for review

Built from the variation **Sedmice Duel** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- The leader may extend a trick at most once: one extra card from each player. (fixes: Unlimited trick extension creates a loop of unbounded length that a flat step list cannot express, and it can exceed 4 choices per round.): This keeps the signature extension decision while bounding each trick to at most 4 card plays.
- Replace the talon refill with one deal of 8 cards per player at the start of each deal. The 16 undealt cards are set aside face down and never used. (fixes: Refilling every hand from the talon after every trick needs several random draws per round, above the limit of 1.): There is only one random event per deal, at its first round. Hidden information remains, because neither player can deduce the other's hand from their own cards.
- Use a guaranteed core deal: each player always receives exactly one Seven, one Ace and one Ten, plus 5 random cards. Play 4 deals, with the first lead alternating. (fixes: A single lucky deal (many Sevens, Aces and Tens) can decide the match, so luck can swamp skill.): This caps how lopsided a deal can be and averages luck over four deals. Both players also know the opponent started with at least one Seven, Ace and Ten, which gives a firm basis for inference.
- Restrict the game to 2 players. (fixes: The 4-player partnership version and variable player counts multiply the choice steps and the rules for turn order.): A strict head-to-head duel keeps the game within 4 choices per round with no partner roles.
- Fix the length at 4 deals of up to 8 tricks (32 rounds). The higher total of points over all deals wins, and equal totals are a draw. (fixes: The 'first to 120 across deals, 50+ to win a deal' scoring gives a match of variable length, which is awkward for a fixed number of rounds.): This gives a fixed, arithmetic winner rule. The game is purely competitive, so no cooperative option collapses under 'higher total wins'.

Objective: After 4 deals, the player with the higher total points across all deals wins. Equal totals are a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. DECK PER DEAL: each player gets one 7, one A and one 10 for certain. The other 26 cards are 2x7, 2xA, 2x10 and 4 each of 8, 9, J, Q, K. Each player draws 5 of them, so the expected extra Aces and Tens per hand are 5*4/26 = 0.77 and the expected extra Sevens are 5*2/26 = 0.38. Points in play per deal
- playable: pass. The rules cover all cases.
- A trick has at most 4 card plays: lead, follow, optional extension, second follow.
- When the led card is a Seven, only a Seven matches, because Sevens are wild and also the led rank.
- A leader with no legal second card cannot extend.
- An extension needs both hands to 
- reasoning_over_luck: pass. WHAT IS LEFT TO CHANCE: the 5 random cards per hand.
- They can give one player 1-2 extra Sevens, roughly a 1 in 3 chance per deal for any given player to receive one.
- They can give one player more of the 4 swing point cards.
- The guaranteed 7/A/10 for each player caps how much the deal can decid

## Complexity

- steps_per_round: designed 13, built 10, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 14, built 28, limit 20 (built: 80)
- hidden_elements: designed 2, built 6, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 32, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 deck is 32 cards: two 8-card hands plus 16 set aside, one trick played (counts only, chance-free)
- pass: R2 each hand holds a guaranteed A and 7: A led, 7 followed, leader declines, follower scores 10
- pass: R3 the 16 undealt cards go to set_aside after dealing
- pass: R4 deal 2 starts with seat 2 leading
- pass: R4 deal 3 starts with seat 1 leading
- pass: R5 trick winner leads the next trick
- pass: R6 leader may lead any card in hand
- pass: R7 non-matching follow: leader wins with 2 cards, no extension asked
- pass: R8 follower playing a 7 is winning; leader without A or 7 cannot extend
- pass: R9 leader extends with a matching card and wins
- pass: R10 leader declines the extension, follower wins
- pass: R11 after an extension the follower plays a second card of any rank
- pass: R12 follower's second card is a 7, so the follower wins the extended trick
- pass: R13 no second extension: follower wins after one extension even though leader still holds a 7
- pass: R14 trick winner scores 10 per A and per 10 in the trick
- pass: R15 last trick of a deal gives +10 and ends the deal
- pass: R16 an extended trick that empties both hands ends the deal
- pass: R17 game ends after deal 4 and the higher score wins
- pass: R17 equal final scores share the win
- pass: R18 a player is offered only cards from their own hand

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 11, 'seat 1': 9}, 52-59 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 66.3 decisions, prompts of 123 characters on average (longest 245)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 32, 'seat 1': 26, 'seats 1 and 2': 2}
- always `first@seat1`: won 22, lost 37, drew 1
- always `first@seat2`: won 23, lost 34, drew 3
- always `last@seat1`: won 38, lost 19, drew 3
- always `last@seat2`: won 37, lost 21, drew 2

## Choices the rules did not make

- Exactly 2 players, suggested 2: The designer fixed it as a duel. Its trick mechanics (one leader, one follower, an extension answered by the follower) only work with two players.
- No talk step: With two directly opposed players, talk gives nothing to coordinate and only adds words.
- Seat 1 is Player A and seat 2 is Player B: This maps the source's named players to seats so the first-lead rule can be applied.
- Cards are stored as rank strings in lists: Suits do not matter, so a rank fully identifies a card.
- The match loop runs trick by trick instead of in 32 fixed round slots: Skipped rounds in a deal do nothing, so ending each deal when the hands empty and counting deals gives the same game.

## Simplifications

- The 8-round deal slot is not counted explicitly; a deal ends when both hands are empty: The rules say the remaining rounds of a deal are skipped, so counting slots adds steps without changing play.
- Dealing is a single conditional update at the start of a round when new_deal is true: The engine's step list is flat, and a step with a when condition expresses dealing on the first round of each deal.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
