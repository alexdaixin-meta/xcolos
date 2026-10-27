# wizard: ready for review

Built from the variation **Wizard Duel of Three** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- One engine round equals one trick. The game is 6 hands of 5 tricks each, so exactly 30 rounds. (fixes: Length: many rounds of growing hand sizes produce hundreds of play decisions, beyond the 40-round and 4-choice-steps-per-round limits.): Each round then has a constant structure with one bid poll and three plays. This fits 4 choice steps and stays within 40 rounds while keeping several hands so bidding skill averages out card luck.
- Fixed hand size of 5 cards in every hand instead of 1, 2, 3, and so on. (fixes: Variable hand size means a variable number of plays per round, which the flat step list cannot express.): The number of plays per hand is constant, so no block of steps has to switch on or off depending on hand size.
- Remove the obligation to follow suit. Any card in hand may be played. The led suit still matters, because off-suit non-trump cards can never win. (fixes: Follow-suit legality: the previous build repeatedly offered cards that were then refused ('Blue 5' in lead_a_card, 'Green 2' in second_card), because the legal list had to be rebuilt per seat from the trick state.): Each seat's options become exactly its own hand, so nothing is ever offered and then refused. Trick tactics (ducking, trumping, saving Wizards) and the inference about hidden cards remain.
- Bids become one sealed simultaneous poll on the first trick of each hand. The options are the fixed list 0, 1, 2, 3, 4, 5, written into the step. Bids are revealed after the poll. There is no forbidden dealer total. (fixes: Sequential bidding plus the dealer's forbidden-total rule costs three choice steps and a dynamic option list (the unused bid_options attribute) on top of three plays.): This uses one choice step instead of three and needs no dynamic option list. Players must infer from their own hand alone, then read opponents' revealed bids during play.
- Mark the player scratch attribute played_card as hidden and never store it inside hand. The playing step removes the card from hand directly, and played_card is cleared at the start of each trick. (fixes: Bookkeeping leaked into the displayed state: blank played_card copies appeared in your_hand.): Players see only their real hand, the public trick, and the scores.
- Drop the full_deck and bid_options attributes. The deal step rebuilds deck from the constant 32-card list written into the step, and the bid poll carries its fixed options. Every remaining attribute is changed by a step that runs. (fixes: Unused attributes (full_deck, bid_options) were never changed by any step.): No attribute stays untouched.
- Every broadcast uses only {seat} and {value}, with one value per message: a separate message for each bid, each trick winner, each trick count, and each score. (fixes: Broadcasts used unfillable placeholders ({bid}, {tricks}, {score}).): No literal placeholder ever reaches players.
- A turned Wizard or Jester both mean no trump for that hand. (fixes: The dealer choosing trump on a turned Wizard adds an extra choice step for little reasoning value.): This removes the dealer's extra trump choice step.
- Exactly 3 players and a 32-card deck: four suits of 1-7, 2 Wizards and 2 Jesters. 15 cards are dealt, 1 is turned for trump and 16 stay unseen. (fixes: A 60-card deck with up to 6 players and 13-card suits gives a large state for little added reasoning at 3 players.): The state is small enough to build, and enough cards stay unseen that card counting and inference still matter. With three players, one rival's broken bid is not automatically your gain.

Objective: After 6 hands (30 tricks), the player with the highest score wins. If two or three players tie for the highest score, those players share the win and the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SCORE TABLE per hand: exact bid k scores 20+10k (0→20, 1→30, 2→40, 3→50, 4→60, 5→70). A miss by d scores −10d. Average tricks per player = 5/3 ≈ 1.67, so a sensible exact bid is worth about 20+16.7 ≈ 37 per hand.

THOUGHTLESS POLICIES, judged by the winner rule:
(1) Always bid 0 and dump. With no fo
- playable: pass. COMPLETENESS: 32 cards = 3×5 dealt + 1 trump + 16 unused, which checks. Five cards each for five tricks, so hands empty exactly at trick 5. Lead order is defined: player after the dealer, then each trick winner.

TRICK RESOLUTION covers every case:
- Wizard anywhere: first Wizard wins.
- A Wizard le
- reasoning_over_luck: pass. CHANCE: the deal decides raw trick-taking strength (who holds the 2 Wizards and the top trumps). Because exact-bid value rises with tricks (20+10k), a strong hand is worth about 10–30 more points per hand than a weak one when both bid exactly. Over 6 hands this variance partly averages out. I estima

## Complexity

- steps_per_round: designed 18, built 18, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 15, built 38, limit 20 (built: 80)
- hidden_elements: designed 2, built 6, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 30, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Deck of 32: after the first deal and one trick, 16 stay in the deck and each hand holds 4 (cards are random, only counts asserted)
- pass: At the start every score is 0 and it stays 0 through the first trick
- pass: A new hand rebuilds the deck and deals exactly 5 cards to each player, replacing old hands (counts only)
- pass: One more card is turned as trump after the deal, leaving 16 in the deck (the card itself is random)
- pass: 16 cards stay unused in the deck after the deal (counts only)
- pass: Bids from a previous hand are reset and replaced by the new bids
- pass: All three may bid 5 at once; bids need not total 5
- pass: Each player's bid is recorded and revealed
- pass: After a hand ends a new hand starts with fresh bids (next leader is seat after new dealer; cards random)
- pass: Play order is leader, then leader%3+1, then the last seat: Jester lead, seat 3's Blue sets the led suit and wins
- pass: No need to follow suit: seat 2 holding Green may play Blue, which leaves its hand
- pass: A Jester lead does not set the suit; the first numbered card (Yellow 3) does and wins
- pass: A Wizard led wins over trump and a later Wizard
- pass: The first Wizard played wins even when not led
- pass: Without a Wizard the highest trump wins over a higher led card
- pass: Without Wizard or trump the highest led-suit card wins
- pass: Three Jesters in a trick: the first Jester played wins
- pass: Off-suit non-trump sevens never win; the led Green 1 wins
- pass: Trick winner gains a trick and leads the next: seat 3 wins with a Wizard, then leads Blue and wins again
- pass: Exact bids score 20 + 10 per trick (bid 2 took 2 = +40, bid 0 took 0 = +20)
- pass: Missed bids lose 10 per trick of difference
- pass: At hand end each trick count and new score is settled
- pass: After a hand ends the next hand is dealt and bid (dealer rotation itself not observable)
- pass: The game ends after the 30th trick and the highest score wins
- pass: Players tied at the top share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 3, 'seat 1': 7, 'seat 2': 10}, 90-90 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 108.0 decisions, prompts of 114 characters on average (longest 189)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 16, 'seat 1': 21, 'seat 2': 22, 'seats 2 and 3': 1}
- always `first@seat1`: won 12, lost 44, drew 4
- always `first@seat2`: won 17, lost 41, drew 2
- always `last@seat1`: won 3, lost 56, drew 1
- always `last@seat2`: won 3, lost 57, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: Each attempt failed in a different way, and each earlier failure was fixed by the next attempt: hidden bookkeeping fields, then illegal card offers, then unfilled placeholders, and now a constant `full_deck` attribute that nothing updates. These are coder mistakes that the platform can avoid, not a sign that the rules are unsound or need something the engine lacks.
- round 1: fix_game: Leading a trick has no restriction in the rules: the leader may play any card in hand. So refusing 'Red 6' or 'Green 2' in `lead_a_card` is a bug in the file, not a flaw in the rules or a missing platform capability. The identical failure across attempts 3–5 shows the faulty offer and check were never actually changed, so this needs a targeted fix rather than a redesign.
- round 1: fix_game: The failures differ from attempt to attempt and each one is a file mistake: empty bookkeeping fields shown to players, attributes nothing updates, unfilled placeholders, and a follow-suit filter that offers cards the game then refuses. Nothing points to a missing platform capability or a flaw in the rules, since per-seat legal options can be built from state.

## Choices the rules did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed the game at three. The deck arithmetic (15 dealt, 1 turned, 16 unused) and the seat rotation depend on exactly three seats, and a fourth would change the card counts.
- No talk step: The rules state there is no discussion phase.
- Cards coded as short text (R5, W1, J2) and the trick winner computed as a power value per card: This turns the trick-winning rules into pure arithmetic: the first Wizard beats everything, then the highest trump, then the highest led-suit card, and an all-Jester trick goes to the first Jester.
- Strategy at this table: A thoughtful player bids from hand strength and the trump suit, then plays to hit the bid exactly. They dump high cards or Jesters when they have enough tricks, and track played cards and others' bids to judge which cards are still out.

## Simplifications

- Start-of-hand and end-of-hand steps are ordinary round steps, each carrying a when-condition on trick_in_hand: The step list is flat. Each step is individually conditional on a counter rather than being a separately chosen block, so the game stays faithful.
- The order of play is addressed by seat expressions relative to leader: The engine asks named seats; leader, leader % 3 + 1 and (leader + 1) % 3 + 1 reproduce seat order starting from the trick winner.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (bid_said, played_card, played_card, played_card) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
