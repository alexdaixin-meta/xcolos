# Variation: Gracias: The Counted Gift

Four players draft triplets from a finite 48-card deck. Each keeps one face-up card, hides the face-down card and must gift the other face-up card to a rival. Card counting reveals what rivals are hiding, and gifts are aimed to spoil their stacks or push them into the losing majority.

Players: 4 to 4, best with 4

## Review of the original

Gracias is a 3-6 player set-collection game over three sessions of four rounds. Each round players draft triplets of cards (two face-up, one face-down), keep one face-up card, hide the face-down card and must gift the other face-up card to an opponent. At each session end, cards in a colour are bundled into 5-stacks, the majority holder of each colour's face-up excess discards it, and players score surviving face-up cards plus stacks.

- **non_degenerate**: good. The forced gift and the majority discard mean no fixed rule wins. 'Always keep the first card and gift to the left' hands the left neighbour cards blindly and can push yourself into majorities. Seats rotate the start player. The previous variation kept this, so no simple policy dominates.
- **skill_sensitive**: weak. The previous variation dealt every card as an independent random draw, and scores turned on totals mod 3. The deal alone gave a session-score standard deviation of about 2 points, while skilled choices were worth about 1 to 2 points per session. Its testers estimated 60-70% of the result was chance, with a skilled player winning only 35-40% against a 25% baseline. The original's finite 108-card deck and draft give somewhat more control, but it is still noisy.
- **headroom**: good. Choosing which card to keep, whom to burden and which majorities to risk gives a weak player a score. Card counting, reading rivals' hidden cards and timing gifts against the leader leave room to improve.
- **reasoning_dependent**: weak. The original has hidden face-down cards and an inferable deck. The previous variation dropped the finite deck, so the 4 hidden cards per opponent per session were uniformly unknown. Targeted gifts became guesses and there was no card counting.
- **verifiable**: good. Stacks, discards and scores are pure arithmetic on card counts, and the winner is the highest total.
- **fits_platform**: bad. The previous variation needed 12 independent random draws per round against a limit of 1, and the engine has no multi-card random deal. The original's 6 colours, 108 cards and up to 6 players also inflate attributes.

## Problems

- P1: Randomness exceeds the platform: dealing 12 independent cards per round is 12 random draws, the limit is 1, and there is no multi-card random operation.
- P2: Luck swamps skill: independent per-card randomness plus mod-3 scoring makes the deal decide about 60-70% of results.
- P3: No inference: with an infinite deck, opponents' hidden cards cannot be counted, so gifts aimed at rivals are guesses.
- P4: The majority discard was nearly meaningless: with loose values of 0-2, a loose 2 was almost always discarded and the majority comparison only mattered for loose 1.
- P5: The previous variation removed the draft (the original's triplet choice), the main decision that reduces deal variance.
- P6: The stack value (2 points for 3 cards) made completing versus spoiling a rival's stack a small, hard-to-read swing.

## Changes

- Use a finite 48-card deck (12 per colour), shuffled once at the start of each session (rounds 1, 5 and 9 only). Each round, deal by removing the top 12 cards of the shuffled list into 4 triplets. (fixes: P1: Randomness exceeds the platform): One shuffle per session is a single random draw, and dealing becomes list removal, the supported workaround. No round has more than one draw.
- All 48 cards are used every session. Face-up cards, keeps and gifts are public, so each colour's hidden total among opponents equals 12 minus all public cards of that colour minus your own hidden cards of it. (fixes: P3: No inference): Card counting lets players infer what rivals are hiding, so gifts that push a rival into a majority or away from a stack are planned rather than guessed.
- Restore the triplet draft. Each round, the 4 triplets are laid out with their two face-up cards shown. Players pick in turn, the start seat rotating each round. Each pick names the triplet, which face-up card to keep and which opponent receives the other. (fixes: P5: The previous variation removed the draft (also reduces P2)): Players choose among offers instead of receiving a private random deal, so decisions outweigh the deal. Rotation gives each seat first pick 3 times and last pick 3 times. Picking in turn lets later players react to earlier gifts.
- Use stacks of 4 worth 3 points each. Loose cards are worth 1 each, with loose = total mod 4 (0-3). Majority discard applies to the highest loose value per colour (ties all discard). (fixes: P4: The majority discard was nearly meaningless; P6: The stack value made the swing small (also reduces P2)): Loose values now range 0-3 and genuinely differ between players. Completing a rival's stack (+3 to them) versus pushing them into the majority is a large, readable swing.
- Drop the talk phase. (fixes: P1: Randomness exceeds the platform (keeps the build within limits)): Four turn-based picks already use the full 4 choice steps per round. The conflict over who gets burdened is expressed directly through public gifts in turn order.

## Kept from the original

- Three sessions of four rounds, with scores summed across sessions.
- Triplets of two face-up cards and one face-down card, drafted in turn order with a rotating start player.
- Keep one face-up card, hide the face-down card, and a forced gift of the other face-up card to an opponent.
- Stacks protect cards, and the majority holder of loose cards in a colour discards them, ties included.
- Highest total wins, with the best single session as tie-break.

## The variation's rules

SETUP
- 4 players in seats 1-4. 4 colours: Red, Blue, Green, Yellow.
- The deck has 48 cards: 12 of each colour.
- Each player has, for each colour, a public count and a hidden count, all starting at 0, plus a game total (0) and a best session score (0).
- The game has 3 sessions of 4 rounds each, 12 rounds in all.

EACH ROUND
1. Shuffle (rounds 1, 5 and 9 only). All 48 cards are shuffled into a random order. This is the only random event in the game. No other round shuffles.
2. Lay out. The next 12 cards are removed from the top of the deck and form 4 triplets, T1 to T4. Each triplet has face-up cards A and B and a face-down card H. The A and B cards of all four triplets are announced to everyone. The H cards stay secret.
3. Draft. Players pick one at a time. In round r, seat ((r-1) mod 4) + 1 picks first, then the others in increasing seat order, wrapping from 4 to 1. On their turn a player chooses one remaining triplet, which of its two face-up cards to keep, and which opponent receives the other face-up card. They may not gift to themselves and must gift. The choice is resolved and announced at once:
   - the kept card adds 1 to the picker's public count of its colour;
   - the gifted card adds 1 to the receiver's public count of its colour;
   - the H card is told only to the picker and adds 1 to the picker's hidden count of its colour;
   - the triplet is removed. The last picker takes the one remaining triplet but still chooses which card to keep and whom to gift.
4. Announce. All public counts of every player are announced.

SESSION END (after rounds 4, 8 and 12)
5. Reveal. All hidden counts are revealed. For each player and colour, total = public count + hidden count. Across the four players, each colour's totals sum to 12.
6. Stacks. For each player and colour: stacks = floor(total / 4), and loose = total - 4 × stacks, so loose is 0, 1, 2 or 3.
7. Majority discard. For each colour, find the highest loose value among the 4 players. If it is at least 1, every player whose loose equals it scores none of those loose cards (ties all discard).
8. Session score. Each player scores 3 points per stack plus 1 point per loose card not discarded, summed over the 4 colours. This is added to their game total. If it exceeds their best session score, it becomes their best session score.
9. Reset. All public and hidden counts return to 0. The next session begins with a fresh shuffle in its first round.

COUNTING NOTE (public information): during a session, the cards not yet seen by a player are their opponents' hidden cards plus the undealt deck, and the colour make-up of these is exactly 12 per colour minus every public card minus that player's own hidden cards.

Objective: After session 3, the player with the highest game total wins. If several players tie, the one among them with the highest best session score wins. If they are still tied, the game is a draw among them.

Expected effect: With the deck fixed and fully used each session, a player who tracks public cards can bound what each rival hides, especially in rounds 3-4 when only 16 hidden cards are unknown. A gift then becomes a calculated strike: giving a rival a third loose card in a colour where they likely lead the majority, or avoiding handing a fourth card that completes their 3-point stack. The draft with a rotating first pick lets players choose which risks to absorb, and seats are balanced. Simple policies lose: always taking the first triplet and gifting to the next seat feeds stacks and creates majorities blindly, and random play is exploited by counters. Hidden H cards still add chance, but the choice among offers, the 3-point stacks and the countable deck should shift results clearly toward skilled play. Talk is omitted: the 4 turn-based picks fill the choice budget, and the conflict over who gets burdened is expressed through public gifts.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
