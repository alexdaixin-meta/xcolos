# diamonds: needs review

Built from the variation **Diamonds: Three-Hand Vault** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Fix the game at exactly 3 players. (fixes: With more than 4 players, one trick needs more than 4 sequential choice steps, which exceeds the platform limit.): Each trick then needs 3 sequential plays, plus one simultaneous pass poll on deal rounds, which makes exactly 4 choice steps. Three players also avoid the two-player 'only the difference matters' trap: helping or robbing one rival is not automatically good against the other.
- Play exactly 3 hands of 10 tricks (30 rounds, one trick per round). The deal rotates so that each player leads the first trick of exactly one hand. (fixes: 4 to 6 deals of 10 tricks is up to 60 tricks, over the 40-round limit.): This stays within 40 rounds and gives every seat the same number of first leads.
- Use the same rotation guarantee as above: across the 3 hands, each seat leads the first trick once. (fixes: The first-trick lead rotates unevenly when the number of deals does not divide by the player count, which gives some seats an edge.): This removes the uneven-rotation seat edge.
- Use a 36-card deck (4 suits of ranks 1 to 9). Deal 10 cards to each player and set 6 aside face down and unseen. (fixes: Few deals of a large, fully dealt deck let the card draw swamp skill, especially at high player counts.): A smaller deck makes card counting tractable, which rewards reasoning. The 6 unseen cards keep real uncertainty about which cards are live. Three hands, each followed by a pass, let skill average out the draw.
- Every hand, each player simultaneously passes exactly 2 cards to the player on their left. (fixes: The dealer's choice of passing 1 to 3 cards adds a choice step and a rule that is hard to resolve in the engine, for little strategic value.): This keeps the passing decision (voiding suits, feeding or starving the next player) in a single fixed simultaneous poll.
- Each card play also names a 'Clubs target' (one opponent), which is used if that player gets a Clubs action that trick. An end-of-hand Clubs majority robs the opponent with the largest showroom, with a tie broken toward the opponent on the receiver's left. Stealing from an empty showroom does nothing, and so does Spades with an empty showroom. (fixes: Clubs steals do not say who chooses the victim or when, and end-of-hand Clubs majorities do not say whom they rob.): This makes targeting an explicit opponent-modelling decision (rob the leader, or punish a threat) without adding extra choice steps, and it defines every edge case.
- Make vaults public, and define a tie-break: on equal score, more vault crystals wins; if still tied, the game is a draw. (fixes: The hidden vault is reconstructible from public actions, so it adds bookkeeping rather than inference while using up a hidden element.): This keeps the 2-point versus 1-point tension (vault crystals are also safe from Clubs) and drops bookkeeping that cannot really be hidden. The hidden information goes where inference is genuine: hands and the unseen cards.
- Write out the edge-case rules (empty showroom, Spades with nothing to move, score ties) as part of the rules. (fixes: Edge cases are undefined: stealing from an empty showroom, Spades with an empty showroom, ties on final score.): This leaves nothing for a judge to decide.

Objective: The player with the highest score (2 x vault + 1 x showroom) wins. If players tie on score, the tied player with more vault crystals wins. If they are still tied, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. VALUE OF EACH ACTION (points to the actor; swing against a chosen rival in brackets): Diamonds +2 (+2). Hearts +1 (+1). Spades +1 if showroom > 0, else 0 (+1). Clubs +1 to you and -1 to the target if the target's showroom > 0 (+2 against that target, 0 against the third player). End-of-hand majority
- playable: pass. COMPLETENESS: deal, pass, follow-suit, off-suit timing, trick winner, led-suit action, Clubs target and its empty-showroom case, end-of-hand order (D, H, S, C), Clubs tie rule, zero-trick bonus and tiebreaks (score, then vault, then draw) are all specified. Every player always holds a card, since 10
- reasoning_over_luck: pass. CHANCE: three random deals of 10 from 36, with 6 unseen. Hand quality, especially holding high Diamonds, varies a lot. Over only 3 hands that leaves about 35 to 45% of outcomes driven by the deal. SKILL LEVERS: (a) Choosing 2 cards to pass, to create a void for off-suit Diamond discards (2 points ea

## Complexity

- steps_per_round: designed 18, built 20, limit 20
- choice_steps_per_round: designed 4, built 8, limit 4
- attributes: designed 14, built 48, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 30, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with every showroom, vault and score at 0 and round 1
- pass: Hand 1 deal: 6 cards set aside and the deck emptied, after one trick each hand holds 9 (counts only, the deal is random)
- pass: Hand 3 start (round 21) deals again and the first trick is played (counts only, the deal is random)
- pass: The pass gives 2 and takes 2, so every hand is 9 after the first trick (counts only, the deal is random)
- pass: Hand 2 start (round 11) re-deals and play goes on (counts only, the deal is random)
- pass: Leader may play any card; its suit becomes the led suit and the highest card of that suit wins
- pass: A player holding the led suit must follow it; a player without it may play any card
- pass: Each player names one of the two other seats as Clubs target, and the trick winner's Clubs action robs that seat
- pass: An off-suit action happens at once: seat 2's Hearts crystal is stolen by seat 3's off-suit Clubs
- pass: Winning a Diamonds trick adds 1 to the vault
- pass: Winning a Hearts trick adds 1 to the showroom
- pass: Spades action with a showroom moves 1 crystal from showroom to vault
- pass: Spades action with an empty showroom does nothing
- pass: Off-suit Clubs takes 1 crystal from the named target's showroom
- pass: Off-suit Clubs against an empty showroom does nothing
- pass: The highest card of the led suit wins; a higher off-suit card does not
- pass: The trick winner takes the led-suit action and leads the next trick
- pass: End of hand: a tie on Diamonds gives nothing, the strict Hearts leader gets a crystal and then banks it with Spades
- pass: End-of-hand Clubs with tied opponents robs the receiver's left
- pass: End-of-hand Clubs robs the opponent with the larger showroom
- pass: End of hand: a player who won no tricks gets vault +2
- pass: End of hand reveals the set-aside cards; the 6 cards stay set aside and play moves to round 11
- pass: Score is recomputed as 2 x vault + showroom
- pass: The game ends after round 30's end-of-hand step and the highest score wins
- pass: Game end: a 4-4 score tie is broken by the larger vault
- pass: Game end: seats level on score and vault share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 8, 'seat 3': 9, 'seat 2': 3}, 169-177 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 198.0 decisions, prompts of 123 characters on average (longest 195)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 19, 'seat 3': 26, 'seat 2': 14, 'seats 2 and 3': 1}
- always `first@seat1`: won 13, lost 46, drew 1
- always `first@seat2`: won 19, lost 41, drew 0
- always `last@seat1`: won 20, lost 39, drew 1
- always `last@seat2`: won 24, lost 33, drew 3

## Triage (whose problem each failure was)

- round 1: fix_game: Every failing scenario fails on `round_number`, which the interface requires to track the current round from 1 to 30. The game never advances it: it stays at 1 after a played round while the file's own `rounds_played` reaches 1. With `round_number` set to 11 or 21 it still ends at 1, so the file overwrites or ignores it. The dealing, passing and trick counts themselves look correct.
- round 1: fix_tests: The game advanced round_number after the final trick exactly as it does after every round. The other tests themselves expect round_number 2 after round 1 and 12 after round 11, so 31 after round 30 is consistent behaviour. The ending scenario's assertion of round_number 30 is a check on a turn counter, not on the rule.
- round 1: revise_rules: The game was built and behaves as specified, but the design needs 8 choice steps per round, over the limit of 4. The pass is a 2-card selection, and each trick has three sequential plays that each carry a card choice and a Clubs target, so the rules themselves are too complex. Seat results are also somewhat uneven (seat 3: 26 wins, seat 2: 14), which a simpler design should address.

## Choices the rules did not make

- 3 players exactly (suggested 3): The designer fixed 3 seats. The dealer rotation, 'left', the 36-card deal (3 x 10 + 6) and the end-of-hand Clubs tie rule all assume 3 players.
- No talk step: The source has no table talk, and adding it would add a mechanic. Strategy lives in passing, suit play, off-suit timing and Clubs targeting: hold Hearts to build a showroom, use Spades to bank it, and point Clubs at the leader.
- Card codes such as D7 and seat numbers A=1, B=2, C=3: Gives arithmetic a concrete suit letter and rank to compare.
- The pass is two simultaneous polls of one card each: A question returns one choice; two polls keep the pass secret and simultaneous.
- Every player names a Clubs target with every card, even when Clubs cannot apply: The source says every player names one; it is used only if a Clubs action fires.
- Ranking expression score*100 + vault: Vault stays well below 100, so this ranks by score first and vault second, and remaining ties share the win (the draw).
- End-of-hand suit actions are applied one after another, each seeing the previous result: The source says 'for each suit in turn', so a Hearts crystal can be banked by a following Spades action.

## Simplifications

- The crystal supply is not tracked: The source says it is unlimited.
- Each player's turn is split into two asks: card, then Clubs target: A question returns a single choice.
- Follow-suit is enforced by restricting the offered cards: Options are filtered from the hand list by led_suit instead of checking after the play.
