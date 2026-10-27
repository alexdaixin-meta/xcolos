# 29 design

- time: 2026-10-27T19:05:38+00:00 (63.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 2f1dd836e567a6e3, reply sha256 d582cac97edf9405

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: LIMITS. 19 steps (max 20), 4 choice steps (discard, Guard guess, raise, response; max 4), 19 attributes (about 20 with full_deck, at the limit), hidden elements = hands + deck order + burned card = 3 (max 3; the design says 2), 1 random draw per round, 40 rounds. Inside the limits, with no board, judge or clock needed. Two players, so no talk is needed, and private Priest info uses the private channel.

DECK-EMPTY CLAIM, checked. After the deal the deck holds 16 - 1 - 3 - 2 = 10 cards. Whenever a draw at step 3, or a Prince redraw at step 12, empties the deck, step 17(c) forces a showdown in that same round. A Prince on an empty deck uses the burned card. So step 3 never meets an empty deck. This holds.

BLOCKING BUG. Step 2 copies all 16 cards of full_deck into the deck and deals 1 card to each player. It clears discards, protected and eliminated, but it never clears the players' HANDS. At every hand end (fold, elimination or showdown) each player still holds a card; step 17 only reveals or announces it. The next hand therefore starts with 2 cards per player, plus a third at the draw, and with 18 physical cards in play. That contradicts the 16-card count and the two-card choice prompt in step 4. A model with only these words cannot play the second hand.

Minor ambiguity: the Guard guess is listed as hidden bookkeeping, so it is unclear whether the opponent hears the named rank. That changes what can be inferred.
- reasoning_over_luck FAILED: HAND COUNT. A 2-player Love Letter hand lasts at most 10 turns and typically about 5 to 7, because Guards (5 of 16 cards) and Barons end hands early. Forty rounds therefore give only about 6 to 8 hands. The original plays to 7 tokens, roughly 10 to 13 hands, precisely to wash out luck.

VARIANCE. The raise triples the stake of some hands, so the match result is often decided by one or two stake-3 hands.

ESTIMATE. A skilled player wins perhaps 55-60% of individual hands. Many results are driven purely by the deal: a turn-1 Guard hits about 1 time in 7 blind, Baron outcomes are set by the deal, and some hands are dealt the Princess. Over about 7 hands with weights of 1 or 3, the skilled player wins the match only about 60-65% of the time, so chance alone often decides it.

GOOD PLAY BOTH SIDES. When both follow card-counting and raise-when-p-is-high, the winner is decided almost entirely by which hands are dealt strong cards, especially those dealt strong cards in raised hands.

INFERENCE AVAILABLE. Inference exists (card counting from out_of_play and discards, Priest info, reading raises) and can be acted on through Guard guesses and the raise/fold decision. But too few hands are played for it to show reliably.
- change: Step 2: before dealing, clear both players' hands (and treat any card still held as returned to the pool), so every hand starts with exactly 16 cards and one card per player.
- change: Increase the number of hands that fit in 40 rounds, for example by moving 5 cards (not 3) face up into out_of_play. This leaves an 8-card deck, which shortens hands to about 4-5 turns, gives about 9-10 hands, and adds public information for card counting.
- change: Reduce single-hand variance: cap the raised stake at 2 instead of 3, or alternatively score only hands won (stake as a tiebreak), so one lucky raised hand cannot decide the match.
- change: State explicitly that the Guard's named rank is announced to both players, as in the original, so the guess and its miss are usable public information.
The variation that was reviewed: Love Letter: Informed Stakes: CARDS (16 in total): 5 Guard (rank 1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8). This list is stored once as full_deck.

STATE
- Each player has: a hand (private; only the owner sees it), discards (a public list), points (start 0), hands_won (start 0), protected (public, 0/1) and eliminated (public, 0/1).
- The table shows: stake, out_of_play (3 face-up cards), deck_count (always equal to the number of cards in the deck), active seat, the round number, and raised_this_hand (0/1).
- Hidden bookkeeping: the deck order, the burned card, new_hand (starts at 1), starter seat (starts as seat 1), raiser, folded and the Guard guess.

ROUNDS: one round is one turn by the active player. The game lasts exactly 40 rounds. The steps below run in this order every round. A step marked 'when' runs only if its condition holds. No step is ever skipped by an earlier step.

1. NEW HAND, SHUFFLE (when new_hand = 1): copy full_deck into the deck and shuffle it. This is the only random event in the round.
2. NEW HAND, DEAL (when new_hand = 1):
- Remove the top card face down as the burned card.
- Move the next 3 cards face up into out_of_play.
- Deal 1 card to each player's hand.
- Clear both players' discards. Set protected = 0 and eliminated = 0 for both players.
- Set stake = 1, raised_this_hand = 0 and folded = 0.
- The active seat becomes the starter seat. Set new_hand = 0.
3. START OF TURN: the active player's protected flag is set to 0, and the active player draws the top card of the deck into their hand. (If the deck were ever empty here, the hand would go straight to showdown at step 17. The rules below prevent this from happening.)
4. DISCARD (choice, active player): 'Your two cards are shown in your state. Choose one to discard.'
5. RESOLVE DISCARD: if the active player's hand holds the Countess together with a King or a Prince, the Countess is discarded whatever was chosen. The discarded card goes face up onto the player's discards, and everyone is told 'Seat X discards CARD'. The effect below applies.
6. GUARD GUESS (choice, when the discard is a Guard and the opponent is not protected): the active player names a rank from 2 to 8.
7. GUARD CHECK (when step 6 ran): if the named rank equals the opponent's card, the opponent is eliminated and the card is announced.
8. PRIEST (when the discard is a Priest and the opponent is not protected): the active player alone is told 'Your opponent holds CARD'.
9. BARON (when the discard is a Baron and the opponent is not protected): the two remaining cards are compared. The holder of the lower card is eliminated, and their card is announced. On a tie nothing happens, and nothing is revealed.
10. HANDMAID (when the discard is a Handmaid): the active player becomes protected until the start of their next turn.
11. PRINCE, DISCARD (when the discard is a Prince): the target is the opponent, or the active player if the opponent is protected. The target discards their hand card face up with no effect, and it is announced. If that card is the Princess, the target is eliminated.
12. PRINCE, REDRAW (when step 11 ran and the target was not eliminated): the target takes the top card of the deck. If the deck is empty, the target takes the burned card instead.
13. KING (when the discard is a King and the opponent is not protected): the two players swap their remaining hand cards.
14. PRINCESS (when the discard is the Princess, by choice): the active player is eliminated.
15. RAISE (choice, active player). This step runs only when all of the following hold:
- stake = 1;
- raised_this_hand = 0;
- nobody is eliminated;
- the deck is not empty;
- the opponent has at least one card in their discards.
Prompt: 'Raise this hand's stake to 3, or pass?' If the player raises, set raised_this_hand = 1 and record them as the raiser.
16. RESPONSE (choice, opponent; when a raise was just made): 'Accept (the stake becomes 3) or fold (the raiser gains 1 point and the hand ends)?' On accept, stake = 3. On fold, folded = 1.
17. HAND END. Exactly one of the following applies, checked in this order:
- (a) If folded = 1, the raiser gains 1 point and 1 hand won.
- (b) Otherwise, if a player is eliminated, the other player gains points equal to the stake and 1 hand won.
- (c) Otherwise, if the deck is empty, or if this is round 40, there is a showdown. Both hand cards are revealed, and the higher rank gains points equal to the stake and 1 hand won. On equal ranks nobody scores.
If (a), (b) or (c) applied, the hand is over: set new_hand = 1, and the starter seat switches to the other seat.
18. PASS TURN: if the hand is over, the active seat becomes the new starter seat. Otherwise, the opponent becomes the active player.
19. GAME END (every round): after round 40 the game ends. More points wins. If points are equal, more hands won wins. If that is also equal, the game is a draw. Winner: After exactly 40 rounds (a hand still in progress at the end of round 40 is settled by showdown at step 17), the player with more points wins. If points are equal, the player with more hands won wins. If both are equal, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player card game with a 16-card deck ranked 1 (Guard) to 8 (Princess). Each turn you draw to two cards and discard one, applying its effect (guess, peek, compare, protect, force a discard, swap). A hand ends when one player remains or the deck runs out, and the highest card wins. Winning a hand earns a token, and the first player to a set number of tokens wins the game.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy dominates. Always discarding the higher card throws away strong showdown cards. Always discarding the lower card walks into Barons and Guards. Always guessing the same rank with a Guard hits about 1 time in 7. In the earlier variation, always raising is punished by an opponent who accepts with strong cards, and always folding gives away every raised hand. Seat order is balanced because the starter alternates."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, Priest information and reading discards improve Guard and Baron play. Many hands are still settled by the deal: being dealt the Princess, a lucky turn-1 Guard, or a Baron comparison fixed at the deal. The earlier variation fit only about 6-8 hands into 40 rounds and could triple the stake, so a skilled player won the match only about 60-65% of the time."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Exact counting, inferring a hand from what an opponent chose to keep, Guard guessing that uses the guesses already announced, and well-timed bluff raises all leave room to improve. A novice still wins hands through the deal."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. The deck and out-of-play cards allow counting. Discards and kept cards reveal likely holdings. A raise is a signal that can be read or bluffed."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every effect and the showdown are rank comparisons, and the winner comes from adding up points. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based text with no board, but the earlier variation sat at every limit (19 steps, 4 choices, about 20 attributes, 3 hidden elements). It also had a blocking bug: hands were never cleared between hands, so the second hand started with 2 cards per player."
    }
  ],
  "problems": [
    "P1 Blocking bug: players' hands are not cleared when a new hand is dealt, so the second hand starts with too many cards and contradicts the 16-card count.",
    "P2 Too few hands fit in 40 rounds (about 6-8), so the deal decides the match far more than skill does.",
    "P3 The raise triples the stake, so one or two lucky stake-3 hands decide the match.",
    "P4 It is ambiguous whether the Guard's named rank is public, which changes what can be inferred.",
    "P5 The design sits at or over the platform limits: 19 steps, about 20 attributes, and 3 hidden elements (hands, deck order, burned card).",
    "P6 Bookkeeping attributes the rules do not need (raised_this_hand, raiser, hands_won) push the attribute count to the limit."
  ],
  "changes": [
    {
      "what": "The new-hand setup step first empties both hands (any card still held returns to the pool), then rebuilds the 16-card deck and deals 1 card to each player.",
      "why": "Every hand starts from exactly 16 cards with one card per player.",
      "fixes": "P1 Blocking bug"
    },
    {
      "what": "Five cards (not 3) go face up out of play. This leaves 9 cards in the deck after the deal, of which 8 can be drawn.",
      "why": "Hands become shorter (about 3-5 turns), so roughly 9-11 hands fit in 40 rounds. There is also more public information for counting.",
      "fixes": "P2 Too few hands"
    },
    {
      "what": "The raise lifts the stake from 1 to 2 only. A fold gives the raiser 1 point.",
      "why": "A raised hand is worth at most double, so no single hand can swing the match. Bluffing and calling remain worthwhile.",
      "fixes": "P3 Raise variance"
    },
    {
      "what": "The Guard's named rank is announced to both players, along with whether it hit.",
      "why": "A missed guess becomes public information, as in the original game.",
      "fixes": "P4 Guard ambiguity"
    },
    {
      "what": "The burned card is replaced by a reserve card: the bottom card of the deck, which is never drawn normally. The hand goes to showdown once only the reserve (or nothing) is left. A Prince redraw may take the reserve.",
      "why": "The burn's role (one unknown card, and a card for a late Prince) is kept, but it becomes part of the deck order. Hidden elements drop from 3 to 2.",
      "fixes": "P5 Limits"
    },
    {
      "what": "Steps are merged (shuffle and deal in one step, pass turn and game end in one step).",
      "why": "This brings the count down to 17 steps.",
      "fixes": "P5 Limits"
    },
    {
      "what": "raised_this_hand, raiser and hands_won are removed. A raise is allowed only while the stake is 1, and a fold always pays the active player, because the response happens in the raiser's own round. Equal points is a draw.",
      "why": "Attributes drop to 17 without changing any decision.",
      "fixes": "P6 Bookkeeping attributes"
    }
  ],
  "keeps": [
    "The 16-card Love Letter deck with its original ranks, counts and effects (Guard through Princess, Countess rule, Princess self-elimination).",
    "Draw one, discard one, and apply the effect even if it hurts you.",
    "Hands end by elimination or by the deck running out, with the highest rank winning the showdown.",
    "Hidden one-card hands, face-up discards and public out-of-play cards for card counting (from the 2-player original).",
    "A short repeated series of hands where hand wins accumulate."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game's inference (counting, reading discards, Guard guessing, raise bluffs) is real. Its faults were a bug, too few hands, too much variance, and sitting at the limits, and all of these are fixable within the limits."
  },
  "variation": {
    "name": "Love Letter: Short Hands",
    "summary": "Two-player Love Letter on a thinner deck: 5 cards face up out of play and one hidden reserve card. Hands are short, so about 10 are played in 40 turns. Each hand offers one chance to raise the stake to 2, which the opponent may accept or answer by folding. The player with more points wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (16, stored once as full_deck): 5 Guard (rank 1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8).\n\nSTATE\n- Each player has: hand (private, seen only by its owner), discards (public list), points (start 0), protected (public, 0/1) and eliminated (public, 0/1).\n- The table shows: out_of_play (public list), deck_count (public, always the number of cards in the deck), stake, active seat, starter seat (starts as seat 1) and round number.\n- Hidden bookkeeping: deck order, new_hand (starts 1), folded, current_discard and guard_guess.\n- The bottom card of the deck is the RESERVE. It is never drawn at the start of a turn.\n\nROUND: one round is one turn by the active player. The game lasts exactly 40 rounds. The steps run in order every round. A step marked 'when' runs only if its condition holds.\n\n1. NEW HAND (when new_hand = 1):\n- Empty both players' hands and discards, and clear out_of_play.\n- Copy full_deck into the deck and shuffle it. This is the only random event in a round.\n- Move the top 5 cards face up into out_of_play.\n- Deal 1 card to each player's hand. The deck now holds 9 cards.\n- Set protected = 0 and eliminated = 0 for both players, stake = 1 and folded = 0.\n- The active seat becomes the starter seat. Set new_hand = 0.\n\n2. START OF TURN: set the active player's protected to 0. The active player draws the top card of the deck, so they hold 2 cards.\n\n3. DISCARD (choice, active player): 'Choose one of your two cards to discard.'\n\n4. RESOLVE DISCARD: if the active player holds the Countess together with a King or a Prince, the Countess is discarded whatever was chosen. The card goes onto the player's discards and becomes current_discard. Everyone is told 'Seat X discards CARD'.\n\n5. GUARD GUESS (choice, when current_discard is a Guard and the opponent is not protected): the active player names a rank from 2 to 8. The named rank is announced to both players.\n\n6. GUARD CHECK (when step 5 ran): if the opponent's card has the named rank, the opponent is eliminated and everyone is told 'Hit: CARD'. Otherwise everyone is told 'Miss'.\n\n7. PRIEST (when current_discard is a Priest and the opponent is not protected): only the active player is told the opponent's card.\n\n8. BARON (when current_discard is a Baron and the opponent is not protected): the two hand cards are compared. The holder of the lower rank is eliminated and their card is announced. On equal ranks nothing happens and nothing is revealed.\n\n9. HANDMAID (when current_discard is a Handmaid): the active player becomes protected (until their next turn starts).\n\n10. PRINCE DISCARD (when current_discard is a Prince): the target is the opponent, or the active player if the opponent is protected. The target discards their hand card face up with no effect, and it is announced. If it is the Princess, the target is eliminated.\n\n11. PRINCE REDRAW (when step 10 ran and the target is not eliminated): the target takes the top card of the deck. This may be the reserve if it is the only card left.\n\n12. KING (when current_discard is a King and the opponent is not protected): the two players swap hand cards.\n\n13. PRINCESS (when current_discard is the Princess): the active player is eliminated.\n\n14. RAISE (choice, active player; only when stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least one card in their discards): 'Raise this hand's stake to 2, or pass?'\n\n15. RESPONSE (choice, opponent; when a raise was just made): 'Accept (the stake becomes 2) or fold?' On accept, stake = 2. On fold, folded = 1.\n\n16. HAND END. Apply the first of these that holds:\n- (a) If folded = 1, the active player gains 1 point.\n- (b) Otherwise, if a player is eliminated, the other player gains points equal to the stake.\n- (c) Otherwise, if deck_count <= 1 or this is round 40, there is a showdown. Both hand cards are revealed and the higher rank gains points equal to the stake. On equal ranks nobody scores.\nIf (a), (b) or (c) applied, set new_hand = 1 and switch the starter seat to the other seat.\n\n17. PASS TURN AND GAME END:\n- If new_hand = 1, the active seat becomes the starter seat. Otherwise the opponent becomes the active player.\n- After round 40 the game ends.\n\nDECK CHECK: after the deal the deck holds 9 cards. A hand goes to showdown whenever 1 or 0 cards remain at the end of a turn. So every turn starts with at least 2 cards in the deck, the draw always leaves at least the reserve, and a Prince redraw always has a card to take.",
    "objective": "After exactly 40 rounds (a hand still running in round 40 is settled by showdown in that round), the player with more points wins. Equal points is a draw.",
    "expected_effect": "With 8 drawable cards and 5 known out of play, hands last about 3-5 turns, so about 9-11 hands are played instead of 6-8. More hands and a stake capped at 2 should let a counting, discard-reading player win noticeably more often, an estimated 65-72% of matches against a naive player. Fewer unknown cards make counting and Guard guessing sharper. The raise stays as a bluff-and-call decision. Showdown luck within a hand remains, but no single hand decides the match. No talk phase: this is a two-player game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 17,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
