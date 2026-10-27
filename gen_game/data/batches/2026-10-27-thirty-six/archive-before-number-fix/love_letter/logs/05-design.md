# 05 design

- time: 2026-10-27T18:14:23+00:00 (94.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 568b7269e9f7ea45, reply sha256 a535c0a79899876b

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: The cube lets a leader lock the match. A player who concedes every double never lets the opponent win more than 1 point per hand. The stake only rises above 1 if the receiver accepts. A concede pays only the pre-double stake (1). A hand played out at stake 1 pays at most 1. Leader policy P = 'concede every double, never double, play normally' gives this table for hand 4, with L = leader's margin entering it:

- Opponent doubles: leader concedes, opponent +1, final margin L-1.
- Opponent never doubles and wins the hand: opponent +1, margin L-1.
- Opponent never doubles and loses the hand: leader +1, margin L+1.
- Tie at deck end: margin L.

So L>=2 means P never loses (WIN in every row). L=1 means P never loses (DRAW or WIN in every row). Generalised: with k hands left, a lead greater than k is a guaranteed win and a lead equal to k is a guaranteed non-loss, with zero thinking.

Leads like this come early. One hand played at stake 4 in hand 1 (after a double and a redouble are accepted) gives a 4-point lead with 3 hands left, which is locked. One stake-2 hand in hand 3 locks the match. So typical matches are decided by one accepted double followed by up to three dead hands. That is the 'safe option wins every late round' failure.

Thoughtless policies:
- 'Always double, never concede': not dominant. It loses when the opponent holds the better card at a high stake.
- 'Never double, always concede': loses about 0-4 to an opponent who doubles every turn, since each concede gives them 1.
- 'Never double, always accept': lets the opponent choose high stakes on Princess or Countess holdings and loses on average.

No option is strictly better unconditionally, and the alternating starts (S1 starts hands 1 and 3, S2 starts 2 and 4) leave no big seat edge. But the conditional lock above is a policy that never loses from a reachable and common position.
- playable FAILED: The rules are mostly complete and finite. There are at most 10 draws per hand, including Prince draws. The burned card covers a Prince on the last deck card, and only one such draw can happen because the hand ends at an empty deck. There are 4 hands and at most 40 turns. Countess forcing, protection with Prince, and conceding are all specified. A 2-player game needs no talk.

The stated complexity does not hold:

- Hidden elements: the design needs Seat 1's hand, Seat 2's hand, the burned card and the hidden deck order. That is 4, over the limit of 3, and Priest and Baron add private reveals on top.
- Steps: realistic count against the claimed 19:
  - hand setup when a hand starts (shuffle, burn, reveal 3, deal 2, reset stake, cube and protection): about 4-5
  - double, respond, resolve concede, resolve accept: 4
  - drop protection and draw: 1-2
  - play, plus forced Countess: 2
  - detail: 1
  - effects (Guard, Priest, Baron, Handmaid, the 3 Prince parts, King, Princess): about 9
  - announce: 1
  - hand end (elimination payout, deck-empty compare, next starter): 2-3
  That totals about 24-27, over the limit of 20.
- Attributes: 19 is barely plausible. It needs points x2, protection x2, eliminated x2, hand cards x2, burned card, deck count, stake, cube owner, hand number, starter, active, Guard guess, Prince target, last discard and priest knowledge, with no spare.
- reasoning_over_luck FAILED: Two-player Love Letter hands are heavily luck-driven:

- A turn-1 Guard guess eliminates the opponent with probability about 1/6 to 1/7 even with good play.
- Being dealt the Princess or Countess versus a Guard sets the deck-out comparison.
- A skilled player wins perhaps 55-60% of hands against a weak one.

The match has only 4 hands, and the stake can reach 8, so one hand often decides everything. The locking effect above makes the first high-stake hand decisive. With two good players, both accept doubles on strong cards, and the hand that gets cubed is resolved by the draw order and Guard luck. The winner is then largely decided by that one deal.

The cube does add inference: reading the 3 face-up cards, the discards and the opponent's doubling behaviour. But a single-card holding before the draw is weak evidence, because cards change every turn. I estimate chance decides about 60-70% of match outcomes between unequal players, plus many 0-0 or 2-2 draws. A good reasoner is not clearly favoured.
- change: Remove the late-match lock. Replace 'exactly 4 hands' with a race: the first player to reach 7 points wins. At the 40-turn cap, the higher score wins, and equal scores are broken by most hands won. Conceded points then still advance the opponent toward the target, so conceding is no longer a free lock. Alternatively, keep a fixed length but make a concede pay the doubled stake.
- change: Lengthen the match, or cap the stake at 4, so one deal cannot decide it. Match length at the 40-turn limit is roughly 6-7 hands.
- change: Cut hidden elements to 3. One way: make the deck order public-random (each draw is a fresh random pick from the list of remaining cards) and fold the burned card into that list as the last card, so the hidden elements are the two hands plus one deck element.
- change: Restate the complexity with an honest step count. Merge steps to reach 20 or fewer: one step with operation-level ifs for all eight card effects, one combined hand-setup step, and one combined hand-end and scoring step. Or drop the Prince's burned-card draw by ending the hand when a Prince is played with the deck empty.
- change: Restore a tie-break on equal cards at deck-out (higher sum of discards) to cut zero-score hands and draws.
The variation that was reviewed: Love Letter: Raised Stakes: CARDS (16): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess. The two players are Seat 1 and Seat 2. Each starts the match with 0 points.

THE MATCH is exactly 4 hands. Seat 1 starts hands 1 and 3, and Seat 2 starts hands 2 and 4. Each platform round is one turn. A hand can last at most 10 turns, so the match never exceeds 40 turns.

STARTING A HAND: Shuffle all 16 cards. Remove the top card face down; this is the burned card, which nobody sees. Remove the next 3 cards face up and announce them to both players; they are out of play. Deal one card face down to each player. This leaves 10 cards in the deck. Both players are in the hand and unprotected. The hand's STAKE is 1, and the stake is CENTRED: either player may offer the next double.

A TURN (active player = the player whose turn it is):
(1) DOUBLE OFFER: if the stake is below 8 and the active player is allowed to double, they choose 'double' or 'no double'. A player may double when the stake is centred, or when they accepted the most recent double. They are holding only their one card at this point.
(2) RESPONSE: if a double was offered, the opponent chooses 'accept' or 'concede'.
(3) RESOLVE: on 'concede', the active player wins the hand and gains points equal to the current stake (before doubling); the hand ends and the rest of this turn is skipped. On 'accept', the stake doubles (1 to 2, 2 to 4, 4 to 8), and from now on only the player who accepted may offer the next double.
(4) DRAW: the active player loses any Handmaid protection from their previous turn, then draws the top card of the deck. They now hold two cards, seen only by them.
(5) PLAY: the active player chooses one of their two cards to discard face up. If they hold the Countess together with the King or the Prince, the Countess is discarded whatever they choose.
(6) DETAIL: if the discarded card is the Guard, the active player names a number from 2 to 8. If it is the Prince, they choose to target themselves or the opponent; if the opponent is protected, they must target themselves.
(7) EFFECT. The Guard, Priest, Baron and King target the opponent and do nothing if the opponent is protected.
- Guard (1): if the opponent's card equals the named number, the opponent is eliminated.
- Priest (2): the opponent's card is shown privately to the active player.
- Baron (3): the two players privately show each other their cards. The holder of the lower card is eliminated; on a tie nothing happens.
- Handmaid (4): the active player cannot be targeted until the start of their next turn.
- Prince (5): the target discards their card face up without effect. If it is the Princess, they are eliminated. Otherwise they draw the top card of the deck, or the burned card if the deck is empty.
- King (6): the players swap their hand cards.
- Countess (7): no effect.
- Princess (8): the active player is eliminated.
An eliminated player reveals their card face up.
(8) ANNOUNCE to both players: the card discarded, the Guard number or Prince target, any elimination and revealed card, the stake, and the number of cards left in the deck.
(9) HAND END: if a player was eliminated, the other player wins the hand and gains points equal to the stake. Otherwise, if the deck is now empty, both reveal their cards. The higher card wins the hand and gains the stake; if the cards are equal, nobody scores. When a hand ends and fewer than 4 hands have been played, the next hand starts on the next turn with the other seat as starting player. Otherwise, play passes to the other player.

MATCH END: after the 4th hand ends, the match is over. Winner: After exactly 4 hands, the player with more points wins. Equal points is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player elimination card game with a 16-card deck ranked 1 (Guard) to 8 (Princess). On each turn a player holds one card, draws a second and discards one, applying its effect. A hand is won by being the last player standing or by holding the highest card when the deck runs out, and the match is a race to a number of tokens.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy dominates. 'Always discard the higher card' throws away the Princess and eliminates you. 'Always discard the lower card' keeps you predictable to Guards and Barons. 'Always guess 2 with the Guard' ignores the face-up cards and the discards. The original's winner-starts rule gives a mild snowball, but no seat has a structural edge. In the previous variation, the fixed 4-hand match with a doubling cube created a policy that cannot lose: once the lead exceeds the number of hands left, conceding every double and never doubling locks the match."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, Guard guesses informed by the three face-up cards and the discards, and Priest/Baron timing all matter. A single hand is still very random. A turn-1 Guard hits about 1 time in 6 or 7, and being dealt the Princess against a Guard decides the deck-out comparison. A skilled player wins perhaps 55-60% of hands. Only a long race (7 tokens in 2-player) lets skill show. The previous 4-hand version with stakes up to 8 made one deal decisive."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win hands because of luck. Strong players improve by tracking the remaining cards, reading what the opponent's discards say about the card they kept, and bluffing through their own discard order. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The whole game is inference about one hidden card. The evidence is which cards are gone, what the opponent chose to keep, Priest knowledge, and what a King swap transfers. A betting layer adds opponent modelling of confidence."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Eliminations, the deck-out comparison and token counts are all arithmetic. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only with no board. As previously adapted it needed 4 hidden elements (two hands, the burned card, the deck order) and about 24-27 steps per round, over the limits of 3 and 20. A Prince-forced draw on top of the normal draw would also need two random draws in one turn unless the deck is shuffled once and then read from the top."
    }
  ],
  "problems": [
    "P1 Lock: the previous variation's fixed 4-hand length lets a leader concede every double and never lose. Any lead greater than the hands remaining is a guaranteed win, so late hands are dead.",
    "P2 Variance: stakes up to 8 in a 4-hand match let one lucky deal decide everything. Love Letter hands are already luck-heavy.",
    "P3 Hidden elements: two hands plus a separate burned card plus the hidden deck order make 4, over the limit of 3.",
    "P4 Step count: realistic steps per round were 24-27, over 20, and the attribute budget was exhausted.",
    "P5 Random draws: a Prince on yourself plus the normal draw could mean two random draws in one turn.",
    "P6 Dead hands: equal cards at deck-out scored nothing, adding zero-score hands and match draws.",
    "P7 Snowball and seat edge: who starts each hand gives a mild tempo edge that compounds over a short match."
  ],
  "changes": [
    {
      "what": "Replace the fixed 4 hands with a race: the first player to reach 5 points wins immediately. Only if the 40-turn cap is reached first does the higher score win, with ties broken by hands won.",
      "why": "A conceded double now pays the opponent 1 point toward the target and immediately restarts a hand they may double again. Conceding is a real cost, not a free lock. A lead can only become safe when it exceeds what can be scored in the turns left, which is a genuine endgame.",
      "fixes": "P1 Lock"
    },
    {
      "what": "Allow at most one double per hand: the stake is 1 or 2 and cannot be redoubled. A concede pays 1.",
      "why": "This caps the swing of any single deal at 2 points out of a 5-point race, so several hands decide the match. It keeps the bluff-and-read decision of the cube.",
      "fixes": "P2 Variance"
    },
    {
      "what": "Shuffle the deck once at hand start, then draw only from the top. The burned card becomes the bottom card of the deck. The hand ends when only that bottom card remains, and that card serves only a late Prince.",
      "why": "The hidden elements are now exactly Seat 1's card, Seat 2's card and the deck order. The only random event is the hand-start shuffle, so a turn has at most one random draw.",
      "fixes": "P3 Hidden elements; P5 Random draws"
    },
    {
      "what": "Merge setup into one step. Fold the forced Countess, Handmaid and Princess into a single post-play bookkeeping step using operation-level ifs. Merge elimination payout and deck-out comparison into one scoring step. Replace per-player eliminated flags with a single 'hand winner' attribute.",
      "why": "This brings the honest count to 18 steps, 4 choice steps and 19 attributes.",
      "fixes": "P4 Step count"
    },
    {
      "what": "At deck-out with equal cards, the higher sum of that hand's own discards wins. If that is also equal, nobody scores.",
      "why": "It restores Love Letter's own tie-break and removes most dead hands.",
      "fixes": "P6 Dead hands"
    },
    {
      "what": "Seat 1 starts hand 1. After that, the player who did not win the previous hand starts the next one; if nobody scored, the seat that did not start last time starts.",
      "why": "It gives a small catch-up instead of a winner-keeps-tempo snowball and offsets Seat 1's hand-1 start.",
      "fixes": "P7 Snowball and seat edge"
    }
  ],
  "keeps": [
    "The 16-card deck with eight ranks and all eight original effects",
    "Holding one hidden card, drawing to two, and discarding one with its effect applied even if harmful",
    "The 2-player setup of three face-up out-of-play cards and one unseen burned card",
    "Winning a hand by elimination or by the highest card at deck-out, with the discard-sum tie-break",
    "A race to a points target across several hands",
    "The confidence-reading double from the earlier variation, now bounded"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core is excellent hidden-information inference. The previous variation's failures came from the fixed-length winner rule, the uncapped stakes and an over-budget build. A race with a single bounded double and a top-of-deck draw fixes all three inside the limits."
  },
  "variation": {
    "name": "Love Letter: One Raise",
    "summary": "Two-player Love Letter played as a race to 5 points. In each hand, the player whose turn it is may raise the stake from 1 to 2 once before drawing; the opponent accepts or concedes 1 point.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (16): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess.\n\nPLAYERS: Seat 1 and Seat 2. Each starts with 0 points and 0 hands won.\n\nROUNDS: Each round is one turn by one player, the active player. The match lasts at most 40 turns.\n\nSTARTING A HAND (done at the start of a turn whenever a new hand is due, including turn 1):\n- Shuffle all 16 cards into a deck. This is the only random event of the turn.\n- Remove the top 3 cards face up as out of play and announce them to both players.\n- Deal the next card face down to the starting player and the next to the other player. Each player sees only their own card.\n- The remaining 11 cards stay as the deck in shuffled order, unseen. The bottom card of the deck is the burned card: it is never drawn normally.\n- Stake = 1, no raise has been made, nobody is protected, and every player's discard sum for the hand = 0.\n- Seat 1 starts hand 1. Afterwards, the player who did not win the previous hand starts. If nobody scored in the previous hand, the seat that did not start it starts.\n- The starting player takes the first turn of the hand, which is this turn.\n\nA TURN:\n(1) RAISE: if no raise has been made in this hand, the active player, holding their one card, chooses 'raise' or 'no raise'.\n(2) RESPONSE: if they raised, the opponent chooses 'accept' or 'concede'.\n(3) RESOLVE:\n- On 'concede', the active player wins the hand and gains 1 point. The hand ends and the rest of the turn is skipped; go to step 11.\n- On 'accept', the stake becomes 2. No further raise is possible this hand.\n(4) DRAW: the active player loses any Handmaid protection and takes the top card of the deck. They now hold two cards, seen only by them.\n(5) PLAY: the active player chooses one of their two cards to discard face up.\n(6) BOOKKEEPING:\n- If they hold the Countess together with the King or a Prince, the Countess is discarded instead, whatever they chose.\n- Add the discarded card's rank to their discard sum.\n- If the discard is the Handmaid, they are protected until the start of their next turn.\n- If the discard is the Princess, they are eliminated.\n(7) DETAIL:\n- If the discard is a Guard, the active player names a number from 2 to 8.\n- If it is a Prince, they choose a target, themselves or the opponent. If the opponent is protected, they must target themselves.\n(8) EFFECTS. The Guard, Priest, Baron and King do nothing if the opponent is protected.\n- Guard: if the opponent's card equals the named number, the opponent is eliminated.\n- Priest: the opponent's card is shown privately to the active player.\n- Baron: both players privately see each other's cards. The lower card's holder is eliminated; on equal cards nothing happens.\n- Prince: the target discards their card face up without effect and adds its rank to their discard sum. If it was the Princess, they are eliminated. Otherwise they take the top card of the deck; this may be the burned card if it is the only card left.\n- King: the two players swap their cards.\n- Countess, Handmaid, Princess: no further effect.\n(9) ANNOUNCE to both players: the card discarded, any Guard number or Prince target, any card discarded by a Prince, any elimination together with the eliminated player's revealed card, the stake, both scores, and the number of cards left in the deck.\n(10) HAND END CHECK:\n- If a player is eliminated, the other player wins the hand and gains points equal to the stake.\n- Otherwise, if the deck now holds 1 card or fewer, both players reveal their cards. The higher card wins the hand and gains the stake. On equal cards, the higher discard sum for this hand wins and gains the stake. If both are equal, nobody scores.\n- The winner of a hand adds 1 to their hands won.\n(11) MATCH CHECK AND NEXT TURN:\n- If a player has 5 or more points, they win the match immediately.\n- Otherwise, if this was turn 40, the match ends (see objective).\n- Otherwise, if the hand ended, the next turn starts a new hand. If it did not, the other player becomes active.",
    "objective": "The first player to reach 5 points wins; only one player can score per hand, so two players never reach 5 at once. If 40 turns pass with neither at 5, the player with more points wins. If points are equal, the player with more hands won wins. If those are also equal, the match is a draw.",
    "expected_effect": "Each hand is still classic Love Letter inference: counting cards against the three face-up cards and the discards, guessing with the Guard, timing the Priest and Baron, and bluffing through discard order. The raise adds a recurring read of the opponent's confidence while they hold a single card. Raising on a weak card can make the opponent concede for 1, but an accepted raise doubles the loss. Conceding is never a free lock, because every concede gives the opponent 1 point of the 5 needed and the next hand can be raised again. With swings capped at 2 and roughly 6-8 hands per match, no single deal decides the result. Simple policies fail. 'Always raise' loses 2-point hands whenever the opponent accepts on strength. 'Always concede' hands the opponent about a point per hand. 'Always accept' gets raised on every Princess and Countess. Luck within a hand remains real, so skill shows through over the series of hands. Talk is omitted: in a 2-player zero-sum race any message is pure cheap talk with nothing to bargain over."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 4,
    "attributes": 19,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
