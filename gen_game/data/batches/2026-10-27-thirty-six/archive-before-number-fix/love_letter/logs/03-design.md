# 03 design

- time: 2026-10-27T18:11:02+00:00 (131.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 da893f535d9064da, reply sha256 283befc0da501d51

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: The rules text is mostly complete. Countess forcing, Prince on an empty deck (takes the burned card), deck-out at the end of the turn, tie-break by discard sum then shared win, and match-end draws are all specified. Talk is simultaneous. That suits a zero-sum game of hidden hands, where bluffing about your card and, in 3-4p, rallying against the token leader give real content.

The complexity figures are understated and break the limits.

Attributes:
- Each player needs: hand card, sum of discards (needed for the tie-break), in-hand flag, protected flag, tokens. That is 5 per player, or 20 at 4 players.
- The game itself needs: deck list, burned card, face-up removed cards, active seat, starting seat of the hand, drawn/second card, turn counter. That is 6-7 more.
- Total is about 26-27 at 4 players, against a limit of 20. The design claims 13.

Hidden elements: hands, the deck order and the burned card are three, plus private Priest/Baron knowledge. The design claims 2.

Steps per round, counted from the rules:
1. talk
2. protection reset
3. skip eliminated players / advance the active seat
4. draw
5. Countess forcing
6. play choice
7. target + guess choice
8. Guard
9. Priest
10. Baron compare
11. Baron eliminate
12. Handmaid
13. Prince discard
14. Prince Princess check
15. Prince redraw or burned card
16. King swap
17. Princess self-elimination
18. elimination reveal and discard-sum update
19. one-player-left check
20. deck-empty comparison with discard-sum tie-break
21. token award
22. match-end check
23. new-hand setup (shuffle, burn, 3 face-up in 2p, deal, reset flags)
24. turn-40 void check

That is about 24 or more, against a limit of 20. The design claims 17.

The variable player count (2-4) is what pushes the attributes over the limit.
- reasoning_over_luck FAILED: Single hand: much of the result comes from the shuffle.
- Who is dealt or draws the Princess or King.
- Whether a blind Guard (about 18-30%) hits.
- Who draws the Baron while holding a high card.
- In 2p, the 3 face-up removed cards and the burned card.

A reasonable estimate is that a skilled player beats a naive one in about 60% of hands, so roughly 60-70% of the variance in a single hand is chance.

The variation shortens the match drastically, from 7/5/4 tokens to 3/2/2.

**2p, first to 3 tokens:** with p = 0.6 per hand, the match win rate is about 0.68.
- A 2p hand runs up to 10 turns, about 7 on average.
- Five hands need about 35-50 turns, so the 40-turn cap often voids the decisive hand and leaves a draw.

**3-4p, first to 2 tokens:** in 4p with p ≈ 0.35 against 0.22 for the others, the skilled player wins the match well under half the time.

Under equal good play, both players infer identically from discards and Priests. The winner is then decided by deal order (Princess location, Guard luck) alone: a coin flip per hand over 3-5 hands.

There is something to infer (card counting from public discards, Priest and Baron knowledge, bluffing in talk), and a way to act on it (Guard naming, Baron timing, King swaps). But the match is too short for that edge to dominate.
- change: Restrict to exactly 2 players so the state fits the limits. Per player: hand, discard sum, in-hand flag, protected flag, tokens (10). Game: deck, burned card, active seat, starting seat, drawn card, turn (6). Total about 16. Restate the attributes truthfully, and set hidden_elements to 3 (hands, deck order, burned card).
- change: Cut steps to 20 or fewer:
- Merge the Prince sub-effects into one step with `if` operations (discard; if Princess, eliminate; else draw or take the burned card).
- Merge the Baron compare and eliminate into one step.
- Fold the protection reset into the draw step.
- Fold the match-end and turn-40 checks into the token step.
- Recount and state a real figure.
- change: Reduce luck with duplicate dealing. Each shuffle is used for a pair of hands: the second hand of the pair replays the same deck order (store the shuffled list) with the seats' starting roles swapped. Tokens are awarded per hand as now. This cancels Princess, King and Guard-hit luck across the pair, so the better reasoner wins the pair.
- change: Replace first-to-3 with a fixed number of hand pairs that fits 40 turns (e.g. 2 pairs = 4 hands; cap each hand at 10 turns). Score by tokens, with ties broken by total discard sum across all hands rather than a draw. This removes the frequent void-hand draws at turn 40.
- change: Alternatively, keep 2-4 players only if per-player state is cut, e.g. by dropping the stored discard sum and using the burned card as the tie-break. Even then, raise the token target and reduce luck as above, and show the attribute count is 20 or fewer at 4 players.
The variation that was reviewed: Love Letter: Sealed Court: CARDS (16): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess. Seats are numbered 1 to N in a fixed order.

STARTING A HAND: Shuffle all 16 cards. Remove the top card face down; this is the burned card, which nobody sees. In a 2-player game, also remove the next 3 cards face up so that all players see them. Deal one card face down to each player as their hand. All players are back in the hand, nobody is protected, and every player's discard pile is empty. Seat 1 starts the first hand. Each later hand starts with the seat after the previous hand's starting seat, wrapping from N back to 1.

TURNS: Each platform round is one turn by the active player. Play passes in seat order, skipping players eliminated from the current hand. A turn goes as follows.
(1) TALK: every player still in the hand writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages bind nobody and may be false.
(2) The active player loses any Handmaid protection from their own previous turn.
(3) The active player draws the top card of the deck and now holds two cards, which only they can see.
(4) PLAY: the active player chooses one of their two cards to discard face up onto their discard pile. If they hold the Countess together with the King or the Prince, they must discard the Countess; if they choose otherwise, the Countess is discarded instead. The Princess may be chosen, and doing so eliminates the player.
(5) TARGET: if the card needs a target, the active player names one other player who is still in the hand and not protected. For the Guard they also name a card number from 2 to 8. The Prince may instead target the active player. If no legal target exists, the card has no effect.
(6) EFFECT:
- Guard (1): if the target's card equals the named number, the target is eliminated.
- Priest (2): the target's card is shown privately to the active player.
- Baron (3): the active player and the target privately show each other their cards. The lower card's holder is eliminated; on a tie nothing happens.
- Handmaid (4): the active player cannot be targeted until the start of their next turn.
- Prince (5): the target discards their card face up without applying its effect. If that card is the Princess, they are eliminated. Otherwise they draw the top card of the deck, or take the burned card if the deck is empty.
- King (6): the active player and the target swap the cards in their hands.
- Countess (7): no effect.
- Princess (8): the active player is eliminated.
An eliminated player reveals their hand card face up onto their discard pile, with no effect, and takes no further part in this hand.
(7) ANNOUNCE: everyone is told the card discarded, the target and guess (if any), every elimination and the revealed cards, and how many cards remain in the deck.

END OF A HAND: A hand ends immediately when only one player remains in it, and that player wins the hand. It also ends at the end of a turn in which the deck becomes empty. In that case, the remaining players reveal their cards: the highest card wins. If several players tie for the highest card, the one with the largest sum of discarded card values wins. If they are still tied, every tied player wins. Each winner of the hand gains 1 token. A new hand then starts on the next turn.

MATCH END: The match ends as soon as a player reaches the token target at the end of a hand: 3 tokens with 2 players, 2 tokens with 3 or 4 players. It also ends after turn 40. A hand in progress at turn 40 is void and gives no tokens. Winner: A player who reaches the token target (3 tokens with 2 players, 2 tokens with 3-4 players) wins. If two or more players reach it at the end of the same hand, the match is a draw among them. If turn 40 ends first, the player with the most tokens wins, and a tie for the most tokens is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player card game played with 16 ranked cards (1 Guard to 8 Princess). On each turn a player draws a card and discards one of their two cards, applying its effect: guessing, peeking, comparing or swapping hands to knock rivals out. The last player standing, or the highest card when the deck runs out, wins a token, and the first to a token target wins the match.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Reviewed variation (Sealed Court): no simple policy wins. 'Always discard the higher card' throws away the Princess and is eliminated. 'Always discard the lower card' never uses the Baron or King well and guesses with the Guard blindly. Rotating the start removes most of the seat edge. With 3-4 players and a first-to-2 target, though, an early lucky token decides a lot."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "A skilled player wins about 60% of single 2-player hands. A first-to-3 match turns that into only about 68%. At 4 players a first-to-2 match leaves the strong player winning well under half the time. Who holds the Princess or King, and whether a blind Guard guess (18-30%) hits, dominate a 3-5 hand match. The 40-turn cap often voided the deciding hand and produced draws."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "There is real depth: counting cards from public discards, timing the Baron, naming the Guard from what the Priest saw, bluffing. Weak players still score, because luck hands them wins. But the match is too short for improvement to show up in results, so the headroom is mostly invisible."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands, deck order and the burned card are hidden. Good play means inferring the opponent's card from discards, from the 3 face-up removed cards, from Priest and Baron knowledge, and from their choices, then acting on it with Guard guesses, Baron challenges and King swaps."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every effect is an arithmetic comparison or an equality test, and tokens are counted. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The 2-4 player version needs about 26 attributes against a limit of 20. It needs about 24 steps per turn against 20. It has 3 or more hidden elements while claiming 2. Hands could still be in progress at turn 40 and be voided. The variation as written cannot be built correctly."
    }
  ],
  "problems": [
    "P1: Supporting 2-4 players pushes the state to about 26 attributes, over the limit of 20, and the reported figures were understated.",
    "P2: About 24 steps per turn, over the limit of 20, with Prince sub-effects, Baron compare/eliminate and the end checks all split into separate steps.",
    "P3: Luck dominates. Each hand is a near coin flip shaped by the deal (Princess or King location, blind Guard hits), and a first-to-3 or first-to-2 match is far too short for a roughly 60% per-hand edge to decide the winner.",
    "P4: The 40-turn cap can void a hand in progress, so many matches end in draws that no play caused.",
    "P5: The suggested fix, 'duplicate' replay of the same deck with seats swapped, fails with only two players. Both players remember the first hand, so in the replay each knows the other's starting card and much of the draw order, which turns the hand into near-perfect information.",
    "P6: Under equal good play, the only lever on the result is the one discard per turn, so nothing lets a better reasoner gain from judging their chances or losing less with bad cards.",
    "P7: The tie-break by sum of discards needs an extra stored attribute per player and rewards a mostly incidental quantity."
  ],
  "changes": [
    {
      "what": "Fix the game at exactly 2 players.",
      "why": "This cuts the per-player state to 4 attributes (hand, points, protected, in-hand), for 19 attributes in total. Every target becomes either 'the opponent' or 'yourself'.",
      "fixes": "P1"
    },
    {
      "what": "Merge steps. Each card effect is one step with `if` operations, including Prince discard / Princess check / redraw or burned card, Baron compare and eliminate, and the elimination reveal. Countess forcing is folded into the play resolution. The protection reset is folded into the draw. Advancing the seat and setting up a new hand are each one conditional step. The count is honestly 19 steps.",
      "why": "This brings the step count inside the limit.",
      "fixes": "P2"
    },
    {
      "what": "Add a doubling stake, like the doubling cube in backgammon. Each hand starts worth 1 point. At the start of their turn, before drawing, the active player may offer to double the stake (to at most 8). The opponent either accepts, which doubles the stake and gives only them the right to make the next double, or concedes, which hands the offerer the current stake and ends the hand.",
      "why": "Winning a hand stays partly luck, but how many points change hands becomes a skill decision. A player must judge their win chance from card counting and from what the opponent's actions reveal, double when ahead, concede bad hands cheaply, and decide whether an offer is a bluff. This is the tool that makes backgammon skill-dominant despite dice. Equal players still trade evenly, so the result is not a lottery.",
      "fixes": "P3, P6"
    },
    {
      "what": "Reject duplicate dealing, and use fresh shuffles with the starting seat alternating 1, 2, 1, 2.",
      "why": "With two players who remember everything, replaying the same deck leaks hidden cards. Alternating the start balances the first-mover edge without leaking anything.",
      "fixes": "P5"
    },
    {
      "what": "Play exactly 4 hands. The match is scored on total points, and equal points are a draw.",
      "why": "A 2-player hand has at most 10 draws, so 4 hands fit within 40 turns. No hand can ever be voided. Stakes give the 4 hands a range of 4 to 32 points, so the total reflects play.",
      "fixes": "P4, P3"
    },
    {
      "what": "Drop the discard-sum tie-break. A tie at deck-out, which can only happen with two equal low cards, scores nobody.",
      "why": "This saves an attribute per player and removes an incidental tie-break.",
      "fixes": "P7, P1"
    },
    {
      "what": "Drop the per-turn free-text talk.",
      "why": "Talk is optional with 2 players, and it cost a choice step that the doubling offer and response now need (4 choice steps at most). The double offer is a costly signal, where a bluff can be called, which carries more reasoning than cheap talk could.",
      "fixes": "P2, P6"
    }
  ],
  "keeps": [
    "The 16-card deck and all eight card effects, including Countess forcing and Princess self-elimination",
    "Draw one, play one, with effects applied even when harmful",
    "The burned card plus the 3 face-up removed cards in the 2-player game",
    "Hands won by being last standing or by holding the highest card at deck-out",
    "The core skills of card counting, Guard naming, Baron timing, King swaps and bluffing about your card"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Fixed at 2 players, Love Letter fits the limits. A doubling stake moves the decisive variance from the deal to judgement about win chances and bluffing, while keeping every card effect."
  },
  "variation": {
    "name": "Love Letter: Raised Stakes",
    "summary": "Two-player Love Letter over exactly 4 hands, with a backgammon-style doubling stake. Before drawing, a player may offer to double the hand's value. The opponent must accept, which raises the stake, or concede, which pays the current stake. Most points after 4 hands wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (16): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess. The two players are Seat 1 and Seat 2. Each starts the match with 0 points.\n\nTHE MATCH is exactly 4 hands. Seat 1 starts hands 1 and 3, and Seat 2 starts hands 2 and 4. Each platform round is one turn. A hand can last at most 10 turns, so the match never exceeds 40 turns.\n\nSTARTING A HAND: Shuffle all 16 cards. Remove the top card face down; this is the burned card, which nobody sees. Remove the next 3 cards face up and announce them to both players; they are out of play. Deal one card face down to each player. This leaves 10 cards in the deck. Both players are in the hand and unprotected. The hand's STAKE is 1, and the stake is CENTRED: either player may offer the next double.\n\nA TURN (active player = the player whose turn it is):\n(1) DOUBLE OFFER: if the stake is below 8 and the active player is allowed to double, they choose 'double' or 'no double'. A player may double when the stake is centred, or when they accepted the most recent double. They are holding only their one card at this point.\n(2) RESPONSE: if a double was offered, the opponent chooses 'accept' or 'concede'.\n(3) RESOLVE: on 'concede', the active player wins the hand and gains points equal to the current stake (before doubling); the hand ends and the rest of this turn is skipped. On 'accept', the stake doubles (1 to 2, 2 to 4, 4 to 8), and from now on only the player who accepted may offer the next double.\n(4) DRAW: the active player loses any Handmaid protection from their previous turn, then draws the top card of the deck. They now hold two cards, seen only by them.\n(5) PLAY: the active player chooses one of their two cards to discard face up. If they hold the Countess together with the King or the Prince, the Countess is discarded whatever they choose.\n(6) DETAIL: if the discarded card is the Guard, the active player names a number from 2 to 8. If it is the Prince, they choose to target themselves or the opponent; if the opponent is protected, they must target themselves.\n(7) EFFECT. The Guard, Priest, Baron and King target the opponent and do nothing if the opponent is protected.\n- Guard (1): if the opponent's card equals the named number, the opponent is eliminated.\n- Priest (2): the opponent's card is shown privately to the active player.\n- Baron (3): the two players privately show each other their cards. The holder of the lower card is eliminated; on a tie nothing happens.\n- Handmaid (4): the active player cannot be targeted until the start of their next turn.\n- Prince (5): the target discards their card face up without effect. If it is the Princess, they are eliminated. Otherwise they draw the top card of the deck, or the burned card if the deck is empty.\n- King (6): the players swap their hand cards.\n- Countess (7): no effect.\n- Princess (8): the active player is eliminated.\nAn eliminated player reveals their card face up.\n(8) ANNOUNCE to both players: the card discarded, the Guard number or Prince target, any elimination and revealed card, the stake, and the number of cards left in the deck.\n(9) HAND END: if a player was eliminated, the other player wins the hand and gains points equal to the stake. Otherwise, if the deck is now empty, both reveal their cards. The higher card wins the hand and gains the stake; if the cards are equal, nobody scores. When a hand ends and fewer than 4 hands have been played, the next hand starts on the next turn with the other seat as starting player. Otherwise, play passes to the other player.\n\nMATCH END: after the 4th hand ends, the match is over.",
    "objective": "After exactly 4 hands, the player with more points wins. Equal points is a draw.",
    "expected_effect": "Single hands remain swingy, but points now track judgement. A player who counts cards, reads the opponent's discards and Guard guesses, and infers the burned and remaining cards can double when their win chance is high. That player also concedes hopeless hands for 1 point rather than 4, and calls or folds against bluffed doubles correctly. Simple policies all lose. Always doubling is punished by accepting with good cards. Never conceding pays out doubled stakes on losing hands. Always conceding gives away every offered hand. Always discarding the higher card throws away the Princess, and always discarding the lower card is predictable to the Guard. Equal good players trade points roughly evenly, so the deal changes what each player knows and can do but does not decide the winner. There is no talk phase: in this zero-sum 2-player game the double offer is the bluffing channel, and unlike talk it is costly to fake."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 19,
    "choice_steps_per_round": 4,
    "attributes": 19,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
