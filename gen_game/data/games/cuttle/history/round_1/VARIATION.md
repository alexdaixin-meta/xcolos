# Variation: Blind Scuttle

A two-player Cuttle race. Point cards are laid face down showing only a rough band, so scuttles and Jack steals are reads. A 10 can knock out a King, and a crossing player must survive one reply from the opponent before winning.

Players: 2 to 2, best with 2

## Review of the original

Cuttle is a two-player card race. Players lay point cards toward 21, or fewer if they control Kings. They can scuttle an opponent's point card with a higher card, use one-off and permanent effects such as Jacks that steal, and draw. The previous variation, Scuttle Race, cut it down to point cards, Jacks and Kings, with a 30-round cap and a shortfall tiebreak.

- **non_degenerate**: bad. In Scuttle Race, the greedy policy 'King at once, else highest point card' is near-optimal, not a weak simple policy. Kings could not be answered, so playing one immediately is dominant. Jacks only steal rank 7 or less, so leading with 8 to 10 is safe. The seat moving first makes its third play before the second seat and was estimated to win 60-65% of greedy-vs-greedy games.
- **skill_sensitive**: bad. Games ended in rounds 3-6, so the deal decided about 70% or more of results. That deal mainly meant who held Kings (0.36 / 0.43 chance of at least one) and who held 10s (the only answer to a 10). Both seats had little choice beyond greedy play plus 'scuttle if you can'.
- **headroom**: weak. Weak players could score with greedy play. Strong players had almost no further lever: holding back only gave away tempo, and scrap counting changed few decisions.
- **reasoning_dependent**: bad. All point cards were face up. The only hidden things were the hands and the deck. There was no bluff, no read of the opponent, and multi-round planning hardly mattered in a 3-6 round race.
- **verifiable**: good. Totals, thresholds, legality of scuttles and steals, and the shortfall tiebreak are all arithmetic on tracked numbers.
- **fits_platform**: good. It is turn-based and text-only with no board. Card draws are remove/append operations, and the length is short. One problem: with two draws per round it can exceed one random draw per round unless each turn is counted as an engine round.

## Problems

- P1 Seat edge: the first mover's tempo advantage gives about 60-65% wins between equal greedy players.
- P2 Kings cannot be answered, so 'play a King at once' is dominant and the King deal decides games.
- P3 Jacks only steal rank 7 or less, so leading with the highest card is automatically safe and card order is not a decision.
- P4 The race is too short (3-6 rounds), so the deal swamps skill.
- P5 Perfect information about laid points: nothing to infer, no bluff, scuttling is automatic.
- P6 Two random draws per round would exceed the platform limit of one.

## Changes

- A 10 may scuttle a King: both go to scrap and the owner's King count drops by 1. Kings also lower the threshold less (by 8/6/4/3 instead of 7/4/3/2). (fixes: P2 Kings cannot be answered, so 'play a King at once' is dominant and the King deal decides games.): Playing a King becomes a timing decision: wait until the opponent's 10s are spent or scrapped. Holding a 10 in reserve becomes a plan.
- A Jack may steal any point card, of any rank. (fixes: P3 Jacks only steal rank 7 or less, so leading with the highest card is automatically safe and card order is not a decision.): High cards become the best targets, so leading greedily with 10s feeds the opponent's Jacks. Card order becomes a real trade-off.
- Base threshold raised to 30 (32 for the First player). Both players are dealt 6 cards, and the cap becomes 40 turns. (fixes: P4 The race is too short (3-6 rounds), so the deal swamps skill.): About 5+ net plays are needed, and scuttles and steals undo progress. Typical games should last 8+ rounds, so draws and decisions accumulate and the opening deal matters less.
- Point cards are laid face down showing only a band: Low 1-4, Mid 5-7, High 8-10. A scuttle names a target and succeeds only if the attacking rank is at least the hidden rank. A failed scuttle scraps the attacker's card and turns the target face up. (fixes: P5 Perfect information about laid points: nothing to infer, no bluff, scuttling is automatic.): Scuttling becomes a risky read that uses band information and public scrap counting. A player can weigh a safer Mid against a Jack-bait High. A player can also stack Mids, whose exact total the opponent must estimate.
- You win only if you are at or above your threshold at the START of your own turn, so the opponent always gets one turn to answer. The First player's base threshold is 32 against the Second's 30. (fixes: P1 Seat edge: the first mover's tempo advantage gives about 60-65% wins between equal greedy players.): Each crossing gets exactly one reply, whichever seat makes it. The 2-point handicap offsets the First player's half-turn of tempo, worth about half a typical 5-6 point play. The split should be checked by greedy-vs-greedy simulation and the handicap tuned to between 1 and 3 if needed.
- Each single turn is one engine round (40 turns = 20 per player). (fixes: P6 Two random draws per round would exceed the platform limit of one.): At most one card is drawn per engine round.

## Kept from the original

- The point race to a threshold that Kings lower
- Scuttling an opponent's point card with an equal or higher card
- Jacks stealing point cards
- The choice each turn between drawing and playing, a private hand and a public scrap pile
- Two players

## The variation's rules

DECK: 48 cards.
- 40 point cards: ranks 1 to 10, four copies of each, no suits.
- 4 Jacks and 4 Kings.
Shuffle the deck.

BANDS: Every point card has a band. Low is ranks 1-4, Mid is ranks 5-7, High is ranks 8-10.

SETUP:
- Randomly pick the First player.
- Deal 6 cards to each player. Hands are private.
- The other 36 cards are the face-down draw pile.
- The scrap pile is face up and fully public.
- Each player has a point pile (starting empty) and a King count (starting 0).

THRESHOLD:
- First player: 32 with 0 Kings, 24 with 1, 18 with 2, 14 with 3, 11 with 4.
- Second player: 30 with 0 Kings, 22 with 1, 16 with 2, 12 with 3, 9 with 4.
- Points are the sum of the ranks in your point pile.
- Shortfall is threshold minus points, with a minimum of 0.

TURNS: Players alternate single turns, First player first. There are at most 40 turns in total (20 each), numbered 1 to 40.

START OF TURN:
1. If the acting player's points are at or above their threshold right now, they win immediately.
2. Otherwise the engine shows everyone the public state:
   - each point pile as a list of cards, each shown as its band if face down or its rank if face up;
   - both King counts and thresholds;
   - the scrap pile;
   - the draw pile size;
   - both hand sizes;
   - the turn number.
3. The acting player also sees their own hand and the exact ranks of their own face-down cards.

ACTION: The acting player chooses exactly one of the following.
(a) DRAW: Take the top card of the draw pile. Not allowed if you hold 8 cards or the pile is empty.
(b) POINTS: Place one point card from your hand face down in your point pile. Its band is visible to the opponent.
(c) SCUTTLE: Choose one point card from your hand and one card in the opponent's point pile. Reveal both.
   - If your rank is equal to or higher than the target's rank, both go to scrap.
   - Otherwise your card goes to scrap and the target stays in place, now face up.
(d) KING-SCUTTLE: Play a 10 from your hand against an opponent's King. Both go to scrap and the opponent's King count falls by 1.
(e) JACK: Play a Jack from your hand and choose any card in the opponent's point pile. It moves to your point pile face up, and the Jack goes to scrap.
(f) KING: Place a King from your hand. Your King count rises by 1.
(g) PASS: Allowed only if you cannot draw.
An illegal or unparseable choice counts as PASS.

END: After turn 40, the player with the smaller shortfall wins. Equal shortfalls are a draw.

Objective: You win at the start of any of your own turns if your point total is at or above your threshold. If no one has won after turn 40, the smaller shortfall (threshold minus points, minimum 0) wins, and equal shortfalls are a draw.

Expected effect: Greedy 'highest card first' now loses to an opponent who Jacks its Highs: each steal is a swing of up to 20 points. Greedy 'King at once' loses its King to a saved 10.

Good players will:
- mix Mid cards to stay below Jack value;
- count scrapped 8s-10s to judge whether a High is a 10 before scuttling it;
- hold a 10 for King defence;
- time a threshold crossing for when the opponent has no answer left, which can be inferred from their hand size and the scrap pile.

Games should run about 8-15 rounds, so the deal matters less. The one-reply win rule plus the 2-point First-player handicap should bring the seat split close to 50%; confirm by simulation.

Talk is not included: the game has two players, so the talk test does not apply.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
