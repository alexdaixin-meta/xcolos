# 27 design

- time: 2026-10-27T19:02:39+00:00 (113.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c6a18150cc6db617, reply sha256 1a319174ded8bb1e

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: 1. DECK BOOKKEEPING BUG. deck_count starts at 10 and drops only at step 4 (DRAW). A Prince makes its target draw the top card of the deck, but deck_count is not decremented. After any Prince, deck_count is larger than the real deck size. The real deck can then empty while deck_count > 0. The next DRAW step takes from an empty deck, which the rules do not define. The end-of-hand reveal also triggers late or not at all. The burned-card fallback covers the Prince only, not the DRAW step.
2. FOLD SKIPS THE GAME-END CHECK. A fold ends the hand and 'the rest of this turn is skipped'. Step 9 is part of the rest of the turn. A player who reaches 5 points through a fold therefore does not 'win immediately'. If the fold happens in round 40, the after-round-40 comparison is skipped as well.
3. STEP BUDGET. The designer claims exactly 20 steps. HAND START alone needs about 6-7 steps: copy, shuffle, burn, reveal 3, deal 2, clear flags, set stake, set seat. The turn then needs: clear protection, raise, response, fold scoring, draw, discard, Countess override, announce, Guard (guess plus check), Priest message, Baron compare and eliminate, Handmaid, Prince (target selection, discard, Princess check, draw or burned card), King swap, Princess, the deck-empty reveal with its tie-break on discard sums, scoring, active switch and game end. This is clearly more than 20 steps, so the limit of 20 is exceeded.
4. Choice steps (raise, response, discard, Guard guess) total 4, which is at the limit and acceptable. Hidden elements (hands, deck) total 2, which is acceptable. Attributes 19 is acceptable if accurate.
5. Talk: this is a two-player game, so talk is not required. The raise acts as an implicit signal.
- reasoning_over_luck FAILED: Love Letter has real inference: counting cards against the 3 face-up cards and the discards, using Guard guesses, acting on Priest information, and timing the Baron. The raise and fold adds a bluffing layer. However, the variation sharply increases the effect of chance.
- If sensible players accept almost every raise (p > 0.25 is almost always true), most hands are played at stake 2. Reaching 5 points then takes only 3 hand wins, compared with 7 tokens in the original two-player game.
- Suppose a skilled player wins 60% of individual hands, which is generous for two-player Love Letter, where the burn card, the initial deal and early Baron or Guard hits are largely luck. Their chance of winning a race to 3 hand wins is 0.6^3*(1 + 3*0.4 + 6*0.16) = 0.216*3.16 ≈ 0.68.
- So the weaker player wins about a third of games. At 55% per hand the figure is about 0.59, close to a coin flip.
- The raise decision itself is made before the draw, holding one card, with only the 3 out-of-play cards as information. p' is therefore close to 0.5 in most situations, and the stake mainly doubles variance rather than rewarding inference.
- With both players following the intended good strategy (raise on strong cards, accept almost always), the winner is largely decided by who is dealt the high card or the early Guard or Baron hit in about 3 short hands.
Chance alone decides the winner too often.
- change: Playable: make every card leaving the deck decrement deck_count, including the Prince's replacement draw. Alternatively, compute deck_count as the length of the deck list. Define DRAW so that, if the deck is empty, the hand ends immediately with a showdown.
- change: Playable: state that the GAME END CHECK (step 9) runs even when a fold skips the rest of the turn. A fold that brings a player to 5 points, or that happens in round 40, must then be scored as a game end.
- change: Playable: re-count the steps honestly and bring them to 20 or fewer. For example, fold the out_of_play reveal and burn into one list operation, merge the protection checks into the conditions of each effect step, and drop the discard-sum tie-break in favour of 'tie = nobody wins'. Otherwise simplify the card effects.
- change: Reasoning over luck: lengthen the race so skill can accumulate. Use first to 9 points, or make the stake raise to 2 only after the DRAW, so the raiser decides with two cards and has seen a discard.
- change: Reasoning over luck: make the fold option meaningful so the raise is a real bluffing decision. For example, the folder concedes 1 point while an accepted raise is worth 3. Alternatively, allow a raise only once per hand per player and after at least one discard by each player, so that the raise and response decisions use inferred information about the opponent's hand rather than a single blind card.
The variation that was reviewed: Love Letter: Raised Stakes: CARDS (16): 5 Guard (1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8). At game setup this list is built once as full_deck from the rank and copies parameters.

STATE: Each player has a private hand (only the owner sees it; it is shown in their state), public discards, points (start 0), hands_won (start 0), and public protected and eliminated flags (0/1). The table shows the stake, the out_of_play cards, deck_count and active_seat. Everything else is hidden bookkeeping.

ROUNDS: A round is one turn by the active player. The game lasts at most 40 rounds.

HAND START (runs in round 1 and in any round after a hand ended):
- Copy full_deck to deck and shuffle it.
- Remove the top card face down as burned.
- Remove the next 3 cards face up into out_of_play.
- Deal 1 card to each player's hand.
- Clear both players' discards, protected and eliminated. Set stake to 1 and deck_count to 10.
- The starting seat is seat 1 in the first hand and alternates every hand after that. The starting seat becomes the active player.

EACH TURN, in order:
1. The active player's protected flag is cleared.
2. RAISE (only if the stake is 1): the active player chooses 'raise' or 'pass'. The prompt reads: 'Your cards are shown in your state. Raise the stake to 2, or pass?'
3. RESPONSE (only if the active player raised): the opponent chooses 'accept' or 'fold'. If they accept, the stake becomes 2 and the turn continues. If they fold, the raiser gains 1 point and 1 hand won, the hand ends, and the rest of this turn is skipped.
4. DRAW: the top card of the deck goes into the active player's hand, and deck_count drops by 1.
5. DISCARD: the active player chooses one of their two cards to discard face up. The prompt reads: 'Your cards are shown in your state. Choose the card to discard.' If the hand holds the Countess together with the King or a Prince, the Countess is discarded whatever was chosen. The discarded card is announced to both players ('Seat {seat} discards {value}') and its effect applies.
6. EFFECTS:
- Guard (1): if the opponent is not protected, the player names a rank from 2 to 8. If it matches the opponent's card, the opponent is eliminated.
- Priest (2): if the opponent is not protected, the player alone receives the message 'Your opponent holds {value}.'
- Baron (3): if the opponent is not protected, the two players secretly compare cards and the lower card's holder is eliminated; a tie does nothing. The eliminated card is announced.
- Handmaid (4): the player becomes protected until the start of their next turn.
- Prince (5): the target is the opponent, or the player if the opponent is protected. The target discards their card face up without its effect. If that card is the Princess, the target is eliminated. Otherwise the target draws the top card of the deck, or the burned card if the deck is empty.
- King (6): if the opponent is not protected, the two players swap hands.
- Countess (7): no effect.
- Princess (8): the player is eliminated.
7. HAND END CHECK:
- If a player is eliminated, the other wins the hand.
- Otherwise, if deck_count is 0, both players reveal their cards. The higher card wins; if the cards are equal, the higher sum of discards wins; if still tied, nobody wins the hand.
- The winner gains points equal to the stake, plus 1 hand won. The hand ends, and the next round starts a new hand with the other seat starting.
8. If the hand continues, the opponent becomes the active player.
9. GAME END CHECK: if a player has 5 or more points, they win immediately. After round 40, the player with more points wins; if points are equal, more hands won wins; otherwise the game is a draw. Winner: The first player to reach 5 points wins immediately. If neither player has 5 points after 40 rounds, the player with more points wins; if points are equal, the player with more hands won wins; if that is also equal, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player card game with a 16-card deck ranked 1 (Guard) to 8 (Princess). Each turn a player draws to two cards and discards one, applying its effect, trying to be the last player standing or to hold the highest card when the deck runs out. Hand wins earn tokens, and the first player to a set number of tokens wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy dominates. 'Always discard the higher card' throws away the Princess and is eliminated. 'Always keep the higher card' is beaten by Barons and Guard guesses aimed at the obvious high card. 'Always guess Princess with the Guard' hits rarely. The starting player rotates to the previous hand's winner, which gives a small edge to whoever is ahead, and the alternation in the variation removes this."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In two-player play the burn card, the first deal and early Guard or Baron hits decide many hands outright. The previous variation made this worse: a blind stake-2 raise taken holding one card, and a race to 5 points, meant about 3 hand wins settled the game. A 60% per-hand edge became only about a 68% match win."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Card counting against the 3 face-up cards and the discards, Bayesian Guard guesses, timing the Baron, bluffing about the Countess and using Priest information all reward deeper play. A beginner still wins hands through good draws."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden and the deck order is hidden. Every Guard guess and Baron play is an inference about the opponent's card from public discards, out-of-play cards and the opponent's choices. The Countess rule creates readable tells and bluffs."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Eliminations, the showdown comparison and the token counts are all arithmetic on tracked state. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and has no board. However, the previous adaptation broke the engine limits and had bugs. Its deck_count drifted after a Prince, which made a draw from an empty deck possible. A fold skipped the game-end check. An honest count came to about 25 steps per round against a limit of 20."
    }
  ],
  "problems": [
    "P1 Deck bookkeeping: deck_count fell only on the normal draw, so a Prince's replacement draw made it wrong. An empty-deck draw could then happen, and the deck-out showdown could fire late or never.",
    "P2 A fold skipped 'the rest of the turn', including the game-end check, so a winning fold or a fold in round 40 was never scored as a game end.",
    "P3 Step budget exceeded: the hand set-up, the raise and response, every card effect, the discard-sum tie-break and the end checks needed well over 20 steps.",
    "P4 Luck dominated. The raise was taken blind (one card, before drawing, nothing seen), so it only doubled variance. Accepting was almost always right, so the fold decision was empty.",
    "P5 The race was too short: first to 5 points at stake 2 meant about 3 hand wins decided the game, too few hands for skill to accumulate.",
    "P6 The original's rotation (the hand winner starts next) gives a snowball seat edge to the leader."
  ],
  "changes": [
    {
      "what": "deck_count is defined as the current length of the deck list, so every card leaving the deck (the normal draw or a Prince's replacement draw) lowers it automatically. Every hand-ending condition is checked in one step at the end of the turn, so a turn never starts with an empty deck. As a safeguard, if the draw ever finds the deck empty, the hand goes straight to showdown.",
      "why": "The displayed count and the real deck can no longer disagree, and an empty-deck draw is defined.",
      "fixes": "P1 Deck bookkeeping"
    },
    {
      "what": "A fold no longer skips anything. It sets a flag, and the single HAND END step scores it. The PASS TURN and GAME END steps then run every round without exception.",
      "why": "Game-end evaluation can never be bypassed.",
      "fixes": "P2 A fold skipped the game-end check"
    },
    {
      "what": "Set-up is compressed into 2 steps. Clearing protection is merged into the draw step, and the Countess override and the announcement are merged into one resolve step. The discard-sum tie-break is dropped: a tied showdown means nobody wins the hand. The early 'first to N' win is removed in favour of a single fixed-length ending. The honest total is 19 steps.",
      "why": "This brings the game inside the 20-step limit while keeping all 8 card effects.",
      "fixes": "P3 Step budget exceeded"
    },
    {
      "what": "The raise moves to the END of the active player's turn, after their draw, discard and effect. It is allowed only once per hand, only while the stake is 1, and only once the opponent has discarded at least one card. An accepted raise sets the stake to 3. A fold concedes just 1 point to the raiser.",
      "why": "The raiser now acts on public discards, the out-of-play cards, any Priest peek and the opponent's earlier choices. The responder faces a real threshold: accepting is right only above roughly a 1-in-3 chance of winning the hand. Bluff raises and cheap folds both become skilful plays.",
      "fixes": "P4 Luck dominated"
    },
    {
      "what": "The game always runs the full 40 rounds (one turn per round, about 6-8 hands). Points accumulate over all hands, and a hand still running at the end of round 40 is decided by an immediate showdown. More points wins, then more hands won, otherwise a draw.",
      "why": "Every hand counts toward one total, so a skill edge accumulates over all of them, not just the first 3 wins. The known cut-off also adds a planning element: whether to raise or hold a high card as round 40 approaches.",
      "fixes": "P5 The race was too short"
    },
    {
      "what": "The starting seat strictly alternates each hand (seat 1, then seat 2, and so on), whoever won.",
      "why": "This removes the leader's snowball and any built-in seat edge.",
      "fixes": "P6 Snowball seat edge"
    }
  ],
  "keeps": [
    "The full 16-card deck and all 8 card effects (Guard, Priest, Baron, Handmaid, Prince, King, Countess with its forced-discard rule, Princess).",
    "Draw-one, discard-one turns with effects applied even when harmful.",
    "The two-player set-up: burn 1 card unseen and reveal 3 cards face up as out of play.",
    "Hands end by elimination or by the deck running out, followed by a highest-card showdown.",
    "Hidden hands and inference from discards as the core skill.",
    "The raise/fold bluffing layer from the previous variation, now informed instead of blind."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Love Letter's hidden-hand inference is exactly the kind of reasoning XColos wants. Its problems (bookkeeping bugs, the step count, blind high-variance stakes, a short race) can all be fixed inside the limits without losing the game's identity."
  },
  "variation": {
    "name": "Love Letter: Informed Stakes",
    "summary": "Two-player Love Letter played over a fixed 40 turns. After acting, a player may raise the current hand's stake from 1 to 3 once the opponent has shown a discard, and the opponent must accept or concede 1 point. Most points after 40 rounds wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (16 in total): 5 Guard (rank 1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8). This list is stored once as full_deck.\n\nSTATE\n- Each player has: a hand (private; only the owner sees it), discards (a public list), points (start 0), hands_won (start 0), protected (public, 0/1) and eliminated (public, 0/1).\n- The table shows: stake, out_of_play (3 face-up cards), deck_count (always equal to the number of cards in the deck), active seat, the round number, and raised_this_hand (0/1).\n- Hidden bookkeeping: the deck order, the burned card, new_hand (starts at 1), starter seat (starts as seat 1), raiser, folded and the Guard guess.\n\nROUNDS: one round is one turn by the active player. The game lasts exactly 40 rounds. The steps below run in this order every round. A step marked 'when' runs only if its condition holds. No step is ever skipped by an earlier step.\n\n1. NEW HAND, SHUFFLE (when new_hand = 1): copy full_deck into the deck and shuffle it. This is the only random event in the round.\n2. NEW HAND, DEAL (when new_hand = 1):\n- Remove the top card face down as the burned card.\n- Move the next 3 cards face up into out_of_play.\n- Deal 1 card to each player's hand.\n- Clear both players' discards. Set protected = 0 and eliminated = 0 for both players.\n- Set stake = 1, raised_this_hand = 0 and folded = 0.\n- The active seat becomes the starter seat. Set new_hand = 0.\n3. START OF TURN: the active player's protected flag is set to 0, and the active player draws the top card of the deck into their hand. (If the deck were ever empty here, the hand would go straight to showdown at step 17. The rules below prevent this from happening.)\n4. DISCARD (choice, active player): 'Your two cards are shown in your state. Choose one to discard.'\n5. RESOLVE DISCARD: if the active player's hand holds the Countess together with a King or a Prince, the Countess is discarded whatever was chosen. The discarded card goes face up onto the player's discards, and everyone is told 'Seat X discards CARD'. The effect below applies.\n6. GUARD GUESS (choice, when the discard is a Guard and the opponent is not protected): the active player names a rank from 2 to 8.\n7. GUARD CHECK (when step 6 ran): if the named rank equals the opponent's card, the opponent is eliminated and the card is announced.\n8. PRIEST (when the discard is a Priest and the opponent is not protected): the active player alone is told 'Your opponent holds CARD'.\n9. BARON (when the discard is a Baron and the opponent is not protected): the two remaining cards are compared. The holder of the lower card is eliminated, and their card is announced. On a tie nothing happens, and nothing is revealed.\n10. HANDMAID (when the discard is a Handmaid): the active player becomes protected until the start of their next turn.\n11. PRINCE, DISCARD (when the discard is a Prince): the target is the opponent, or the active player if the opponent is protected. The target discards their hand card face up with no effect, and it is announced. If that card is the Princess, the target is eliminated.\n12. PRINCE, REDRAW (when step 11 ran and the target was not eliminated): the target takes the top card of the deck. If the deck is empty, the target takes the burned card instead.\n13. KING (when the discard is a King and the opponent is not protected): the two players swap their remaining hand cards.\n14. PRINCESS (when the discard is the Princess, by choice): the active player is eliminated.\n15. RAISE (choice, active player). This step runs only when all of the following hold:\n- stake = 1;\n- raised_this_hand = 0;\n- nobody is eliminated;\n- the deck is not empty;\n- the opponent has at least one card in their discards.\nPrompt: 'Raise this hand's stake to 3, or pass?' If the player raises, set raised_this_hand = 1 and record them as the raiser.\n16. RESPONSE (choice, opponent; when a raise was just made): 'Accept (the stake becomes 3) or fold (the raiser gains 1 point and the hand ends)?' On accept, stake = 3. On fold, folded = 1.\n17. HAND END. Exactly one of the following applies, checked in this order:\n- (a) If folded = 1, the raiser gains 1 point and 1 hand won.\n- (b) Otherwise, if a player is eliminated, the other player gains points equal to the stake and 1 hand won.\n- (c) Otherwise, if the deck is empty, or if this is round 40, there is a showdown. Both hand cards are revealed, and the higher rank gains points equal to the stake and 1 hand won. On equal ranks nobody scores.\nIf (a), (b) or (c) applied, the hand is over: set new_hand = 1, and the starter seat switches to the other seat.\n18. PASS TURN: if the hand is over, the active seat becomes the new starter seat. Otherwise, the opponent becomes the active player.\n19. GAME END (every round): after round 40 the game ends. More points wins. If points are equal, more hands won wins. If that is also equal, the game is a draw.",
    "objective": "After exactly 40 rounds (a hand still in progress at the end of round 40 is settled by showdown at step 17), the player with more points wins. If points are equal, the player with more hands won wins. If both are equal, the game is a draw.",
    "expected_effect": "Card play stays classic Love Letter inference: counting against the out-of-play cards and the discards, Guard guesses, Baron timing and Countess bluffs. The raise is now an informed bet made after seeing at least one discard from each side, with an asymmetric price. Accepting risks 3 points to win 3, while folding costs only 1, so accepting pays off only above roughly a 1-in-3 chance of winning the hand. That makes bluff raises, value raises and disciplined folds real, readable decisions, and a skilled player can limit losses on hands the deal has doomed. Points accumulate over all 6-8 hands, not a race to 3 wins, so skill compounds. The fixed round-40 showdown adds endgame planning. Simple policies all lose to a sensible opponent: always raising is punished by informed accepts, always accepting by value raises, always folding by bluff raises, and fixed discard rules by Baron and Guard play. This is a two-player game, so there is no talk phase; the raise itself is the signalling channel."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 19,
    "choice_steps_per_round": 4,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
