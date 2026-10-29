# nyet: needs review

Built from the variation **Nyet! Trio (Widow edition, compact)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Remove the separate Lone discard choice. The Lone keeps all 6 cards (5 dealt plus the Widow) and plays one per trick. The single card left unplayed after the 5th trick is the hidden discard and is never shown. (fixes: P1: Too many choice steps): This removes a whole choice step but keeps the decision: the Lone still chooses which card to keep back.
- Use three shared sequential choice slots for both veto tokens and card plays. Slot A is First in a veto round and the leader in a trick round. Slots B and C are the next players clockwise. Each slot's options are computed: legal empty boxes in veto rounds, legal cards in hand in trick rounds. Talk runs only in veto rounds. (fixes: P1: Too many choice steps): Talk plus 3 shared slots gives exactly 4 choice steps across the whole flat list.
- Store the Nyet board as one list attribute. Store the current trick as one list, so the led colour comes from its first card. Drop the 'tricks' stat and break ties on score, then lone_tricks, then last_win. Set-aside cards are one list. The Lone's unplayed card simply stays in their hand, so hidden elements fall to 2. (fixes: P2: Too many attributes): This brings attributes to 19 and states the count honestly. The tiebreak still almost always produces a unique winner.
- Allow at most one token on the LONE line per veto round. Rotate the order of the TRUMP line each deal, so the default trump changes. (fixes: P3: Weak trump veto): At least two of the three tokens must now go to the TRUMP line, so trump is genuinely contested. The single LONE token becomes a race that means something different by seat. First tokening 'First' declines to be Lone. Second tokening 'First' claims Lone. Third tokening 'First' forces Second to be Lone. Rotating the trump order stops one colour from being the standing default.
- Keep the reduced core: 3 players, a 24-card deck, a two-line Nyet board, 1 Lone against a Pair, a Widow, and trump-only trick rules. (fixes: P4: Full rule set cannot be built): This is the smallest version that keeps veto-to-set-the-rules, shifting teams and trick play, within the limits.

Objective: The highest score wins. If players tie, the tied player with the most lone_tricks wins. If still tied, the tied player with the highest last_win wins (the one who won a trick most recently; this is unique unless no tied player has won a trick). If still tied, the game is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Payoff per deal (5 tricks), with k = tricks the Lone wins. Lone gets 2k; each Pair member gets 5-k.

| k | Lone | each Pair member | result |
|---|---|---|---|
| 0 | 0 | 5 | Lone -5 |
| 1 | 2 | 4 | Lone -2 |
| 2 | 4 | 3 | Lone +1 |
| 3 | 6 | 2 | Lone +4 |
| 4 | 8 | 1 | Lone +7 |
| 5 | 10 | 0 | Lone 
- playable: pass. Rules are complete.

Deal: 5 cards each plus a public Widow; 8 cards stay hidden.

Veto mechanics:
- 3 tokens are placed sequentially; each placer sees earlier tokens.
- At most one LONE token is allowed, so the LONE line never reaches its last box.
- If all 3 tokens go on TRUMP, 1 of 4 boxes remain
- reasoning_over_luck: pass. The deal matters within a deal: 5-card hands from a 24-card deck. Over 6 deals and 30 tricks, though, decisions dominate. The skill levers are:
- Judging one's hand against the visible Widow to decide whether to seek or deny the Lone role. Being Lone is a +/- swing of several points per deal.
- Usin

## Complexity

- steps_per_round: designed 16, built 18, limit 20
- choice_steps_per_round: designed 4, built 7, limit 4
- attributes: designed 19, built 56, limit 20 (built: 80)
- hidden_elements: designed 2, built 15, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: At game start every seat has score 0, lone_tricks 0 and last_win 0
- pass: Round 1 is a veto round: tokens choose trump and Lone, no trick and no score
- pass: Round 7 is a veto round: old hands are emptied, 5 cards are dealt to each seat, the Lone gets 6 and the deck keeps 8
- pass: Tokens left over from a previous deal are cleared at the start of a veto round
- pass: Deal 3 veto order is 3, 1, 2 (seat 3 places first and is the First Lone box)
- pass: Deal 5 veto order is 2, 3, 1: a token on First makes seat 3 (Second) the Lone
- pass: Deal 4 trump order is Blue, Red, Yellow, Green: vetoing Blue and Red gives Yellow
- pass: Veto talk is collected and the veto round still completes
- pass: A box that already holds a token is not offered again
- pass: Once the LONE line holds a token, no other LONE box is offered
- pass: With two trump boxes still empty, neither is withheld as a last box
- pass: Trump is the first colour of the line without a token (Yellow and Blue vetoed in deal 1 gives Red)
- pass: The Lone is the seat at the first LONE box without a token (Third vetoed gives seat 1)
- pass: The Lone takes the widow and holds 6 cards; the Pair hold 5
- pass: The leader plays first and sets the led colour; seat 3 leads Blue and seat 1's Blue 5 wins
- pass: A seat holding the led colour must follow it
- pass: A low trump beats the highest card of the led colour
- pass: An off-colour non-trump card cannot win; the highest card of the led colour wins
- pass: The Lone wins a trick: +2 score and +1 lone_tricks
- pass: A Pair member wins a trick: both Pair members gain 1, the Lone gains nothing
- pass: The trick winner's last_win is the round and that seat leads the next trick
- pass: After the 5th trick the Lone still holds 1 unplayed card
- pass: The game ends after round 36 and the highest score wins
- pass: Tie on score and lone_tricks is broken by the most recent trick win
- pass: Tie on score is broken by lone_tricks

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 7, 'seat 3': 6, 'seat 1': 7}, 84-97 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 126.0 decisions, prompts of 135 characters on average (longest 204)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 17, 'seat 3': 20, 'seat 1': 23}
- always `first@seat1`: won 27, lost 33, drew 0
- always `first@seat2`: won 22, lost 38, drew 0
- always `last@seat1`: won 15, lost 45, drew 0
- always `last@seat2`: won 21, lost 39, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are sound and the platform can express them. Every failure is a file mistake: calc expressions where `players` resolves to the engine's player list instead of the numeric parameter, and internal or not-yet-set text fields shown blank in announcements.
- round 1: revise_rules: The game was built faithfully, but the design needs 7 choice steps per round against a limit of 4. Because the step list is flat, the veto round (one talk poll plus three sequential token placements) and the trick round (three sequential card plays) all count toward the same per-round total, so the coder cannot fix this; the rules must change.

## Choices the rules did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed 3 seats. The game is one Lone against a Pair of two, and both the veto order and the LONE line have exactly 3 positions, so no other count works. The strategy is to veto colours and Lone positions to steer trump toward your own hand, and to judge whether to go Lone or force someone else into it.
- Talk is kept as a simultaneous poll with broadcast: The rules say all three write at once without seeing each other. The players disagree about trump and about who should be Lone, so talk gives them something to bluff and bargain over.
- Cards are text such as 'Red 3', handled through played_colour and played_rank: This lets the trick winner be found by arithmetic: strength = trump bonus 200 + led bonus 100 + rank.
- strength is a public scratch attribute: It is computed only from cards already played face up, so making it public reveals nothing; a player attribute may not be hidden from all.
- The 8 set-aside cards stay in the hidden deck list: They are never revealed or used, so the hidden deck can hold them.
- Tie-break encoded as score*10000 + lone_tricks*100 + last_win: lone_tricks is at most 30 and last_win at most 36, both under 100, so the order is strictly lexicographic. A full tie shares the win, which is the source's draw.

## Simplifications

- Veto-round and trick-round steps are one flat list, each step gated by a 'when' condition on round_in_deal: The engine has no branching blocks. Per-step conditions reproduce the alternation exactly.
- The 'Lone leads first' and 'winner leads next' rules are kept as a leader table attribute, and play order is addressed relative to the leader: The engine addresses seats by attribute rather than by a fixed rotation.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `colour_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `lone_line` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `trump_lines` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
