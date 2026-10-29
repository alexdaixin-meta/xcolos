# diamonds: ready for review

Built from the variation **Diamonds: Three-Hand Vault** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Clubs robs automatically: it takes 1 crystal from the opponent with the largest showroom. Ties go to the tied opponent who comes first clockwise from the actor. (fixes: Too many choice steps per round (8 against a limit of 4): the Clubs target choice and the multi-card pass each add choice steps.): This removes a choice step, and the tie-break depends only on the robbed player's position relative to the actor, not on fixed seats.
- The pass becomes exactly 1 card to the left, chosen by all players in one simultaneous poll, and only on the first trick of each hand. (fixes: Too many choice steps per round (8 against a limit of 4): the Clubs target choice and the multi-card pass each add choice steps.): It keeps the original's voiding and pass tactic while costing one choice step on one round in seven. The maximum per round is 3 plays plus 1 pass, which is 4.
- The game is fixed at 3 players, 3 hands and 7 tricks per hand (21 rounds), using a 32-card deck (4 suits, ranks 1-8). 21 cards are dealt and 11 stay unseen. (fixes: The game is too long for the platform (up to 60 tricks), which risks the 40-round limit and adds attribute and step load.): This keeps the game short and under 40 rounds. The unseen cards keep void-inference non-trivial.
- The dealer rotates clockwise each hand, so each seat deals exactly once and the player left of the dealer leads trick 1, giving each seat exactly one opening lead. All end-of-hand actions resolve starting from the player left of the dealer. (fixes: Seat imbalance: seat 3 won most often among random seats, from a fixed-seat Clubs tie-break and a dealer/lead rotation that did not give each seat equal leads.): Every seat gets identical structural treatment across the game.
- Vault totals are not displayed in the score summary, but every action is announced. Ties on score are broken by vault size. (fixes: Hidden vaults are not really hidden in a text engine, because every vault action is announced; this is not a flaw for play, but the hidden element is effectively the hands.): This honestly accepts that vault totals can be worked out from the announcements, and turns the hiddenness into a memory and tracking skill rather than a fake secret. The vault tie-break rewards Spades and Diamond play.

Objective: The player with the highest score after 3 hands wins. If two or more players tie for highest score, the tied player with more vault crystals wins. If they are still tied, the game is a draw between them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Action values in points (vault = 2, showroom = 1): Diamonds +2; Hearts +1; Spades +1 only if your showroom is non-empty, else 0; Clubs +1 to you and -1 to the opponent with the largest showroom (a swing of 2 against them, 1 against the third player). Average value of a led-suit trick action is about
- playable: pass. Deal arithmetic: 3 x 7 = 21 cards dealt, 11 set aside, total 32. A hand is 7 tricks, so 21 rounds; at most 40 allowed.

Choices per round: on trick 1, 1 simultaneous pass poll + 3 sequential plays = 4 (limit 4). Later tricks have 3.

Random draws: one shuffle per hand, on trick 1 only, so at most 1 
- reasoning_over_luck: pass. Chance: three random deals of 7 from 32, with high cards driving trick wins. Rough estimate: chance accounts for about 35-45% of the result.

Skill levers:
- The pass, which can create a void that enables +2 Diamond dumps, or shed a dangerous high card to keep the +4 zero-trick option alive.
- Count

## Complexity

- steps_per_round: designed 16, built 17, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 14, built 46, limit 20 (built: 80)
- hidden_elements: designed 2, built 14, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 21, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Showroom and vault start at 0 for every player
- pass: Deal: 7 cards each, 11 set aside (after one trick each hand holds 6, whatever the random deal)
- pass: Each player passes exactly one card left: hands stay 7 before trick 1, so 6 after it (independent of the deal)
- pass: A new hand starts cleanly from leftover per-hand counts (hand 2 trick 1; only deal-independent facts are asserted)
- pass: After trick 7 of hand 2 the game moves on to hand 3; the Hearts trick and the Hearts majority both go to seat 3
- pass: The winner of a trick leads the next one
- pass: After the lead, play goes clockwise: seat 3 plays its Heart before seat 1 plays its Club
- pass: A player holding the led suit must follow it
- pass: A void follower may play any card and its suit action resolves before the next player plays
- pass: The highest card of the led suit wins; a higher off-suit card does not
- pass: Won cards count by suit, every card in the trick included (seen through the end-of-hand majorities)
- pass: The trick winner takes the led suit's action exactly once
- pass: The Diamonds action (an off-suit Diamond) adds 1 to the vault
- pass: The Hearts action (an off-suit Heart) adds 1 to the showroom
- pass: Spades action with showroom >= 1 moves one crystal from the showroom to the vault
- pass: Spades action with an empty showroom does nothing
- pass: Clubs action takes 1 crystal from the opponent with the largest showroom
- pass: Clubs action does nothing when both opponents' showrooms are 0
- pass: Clubs action with tied opponents takes from the first one clockwise after the taker (taker seat 2, so seat 3)
- pass: Clubs action with tied opponents, taker seat 3, takes from seat 1
- pass: End-of-hand suit majorities: a strict leader takes the suit action, a tied suit gives nothing
- pass: A player who took no tricks in the hand gains 2 vault at the end of the hand
- pass: After the last trick of hand 3, score = 2*vault + showroom and the game ends
- pass: A tie on score is broken by the larger vault
- pass: Players level on both score and vault share the win
- pass: Suit action results show in the public showroom and vault counts

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `initialize` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 12, 'seat 2': 4, 'seat 1': 3, 'seats 2 and 3': 1}, 46-53 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 72.0 decisions, prompts of 142 characters on average (longest 190)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 18, 'seat 2': 22, 'seat 1': 19, 'seats 2 and 3': 1}
- always `first@seat1`: won 8, lost 51, drew 1
- always `first@seat2`: won 11, lost 48, drew 1
- always `last@seat1`: won 26, lost 33, drew 1
- always `last@seat2`: won 25, lost 33, drew 2

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3. Seat-based dealer rotation, passing left and the Clubs tie-break all assume 3 seats.
- Strategy at the table: A thoughtful player chooses when to void a suit so that off-suit plays trigger Diamonds or Clubs actions. They track opponents' showrooms to time Clubs and Spades, and weigh winning suit majorities against deliberately taking zero tricks for the +2 vault bonus.
- No talk step: The source rules include no table talk, and adding it would add a mechanic.
- Cards encoded as text 'D7', 'H3', and so on: The suit letter and rank can then be read arithmetically to find led_suit and the trick winner.
- Rank expression score * 1000 + vault: No score can reach 1000 in 21 tricks, so this ranks by score first and vault second. Equal values share the win, which matches the source's draw.
- Final scores computed in a step when hand 3's trick 7 ends: The source scores only at the end of hand 3.

## Simplifications

- Vault is declared public: The source leaves vaults out of summaries, but every vault change is announced to everyone, so vaults are fully trackable. Public visibility gives the same information.
- The trick is played as three separate ask steps addressed by seat expressions relative to leader_seat, each follower's ask followed by an update for an off-suit action: The engine's step list is flat. This keeps clockwise order from a variable leader and resolves each off-suit action before the next player plays.
- Start-of-hand dealing and passing run as steps guarded by trick_number == 1: One round is one trick, so the hand-start steps run only on the first trick of each hand.
- Won cards are tracked only as per-suit counts, not as a pile of cards: The rules use won cards only through their per-suit counts.
