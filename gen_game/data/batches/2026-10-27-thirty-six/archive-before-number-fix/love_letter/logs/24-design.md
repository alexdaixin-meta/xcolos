# 24 design

- time: 2026-10-27T18:59:58+00:00 (79.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 40021b83f4c7fdd1, reply sha256 f375f81eb1bcbf90

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
1) Remove every {hand} (and any other custom {name}) from prompts. The engine fills only {value} and {seat}. Keep each player's held cards in a player attribute visible only to its owner (private), so the card shows up in that player's state automatically, and write prompts like 'Your card(s) are shown in your state.' 2) Hide all scratch and bookkeeping attributes from the printed state: raise_said, resp_said, raise_choice, response, the drawn-card temporaries and similar. Use `none` visibility for table attributes and `ally` for player ones. This should leave only points, hands_won, turn, the stake, out-of-play cards, discards, the deck count and the owner's own hand. Do not re-expose them when fixing the prompts. 3) Make sure every attribute is changed by a step that actually runs. Build `full_deck` by the deck recipe from the rank and copies parameters, then shuffle and copy it at each hand start. Set `must_countess` after the draw, whenever the hand holds the Countess with the King or a Prince, and reset it after the play. Otherwise drop these attributes and apply the forced Countess discard directly in the play step with an `if`. 4) Before submitting, check all three things together (placeholders, visibility, every attribute updated) so one fix does not undo another.
the game file could not be built. What the checks found on the attempts:
- attempt 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: "You hold {hand}. Before drawing, choose 'raise' (stake becomes 2 if accepted; if your oppo"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: "Your opponent raised. You hold {hand}. 'accept': the stake becomes 2 and the turn goes on."); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'You hold {hand}. Choose the card to discard face up. If you hold the Countess (7) with the'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- attempt 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (raise_said, resp_said, raise_choice, response) in `your_card`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 3: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `must_countess` is never changed in 3 random matches, so nothing updates it. Steps that name it: start of turn, resolve the raise and draw. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- attempt 4: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (raise_choice, response) in `your_card`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 5: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'You hold {hand}. C

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player card game played with 16 ranked cards. Each turn a player draws to two cards and discards one, applying its effect: guessing, peeking, comparing, protecting, forcing a discard or swapping hands. A hand is won by being the last player standing or by holding the highest card when the deck runs out, and the first player to collect enough tokens wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy wins. Always discarding the lower card walks into Barons and loses the Princess to Princes. Always discarding the higher card throws away Handmaid protection and King swaps. Guard guesses must use the visible discards to beat random guessing. One seat-related asymmetry exists: the winner of a hand starts the next one, which mildly snowballs."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, Guard inference and Baron timing matter, but a single hand is short (often 3-6 turns), and opening draws, Guard hits and forced Princess or Countess situations swing hands heavily. A first-to-7 match helps, but variance stays high."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win hands through the draw. Strong players improve through card counting, reading what an opponent's kept card must be from their discards, and bluffing with play order. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, the burned card is hidden, and every discard leaks information about the card kept. Guard guesses and Baron plays are Bayesian inference about the opponent's hand."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "Hand results are arithmetic: elimination, highest card, then discard sum. However, the first player is chosen by 'who was most recently on a date', which is not arithmetic, and a tie on discard sums has no rule."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and has no board. But 2-4 players with targeted effects, eight distinct card effects and first-to-7 tokens push against the step, choice and length limits. The previous build also failed on implementation: literal {hand} placeholders, visible bookkeeping fields, and attributes (full_deck, must_countess) that no step ever changed."
    }
  ],
  "problems": [
    "P1 Luck dominates a single hand. Draw order and lucky Guard hits decide many hands, and a match of equal-value hands gives skill few levers.",
    "P2 The first player is chosen by a non-arithmetic rule, the winner starts the next hand (a snowball), and a tie on discard sums is undefined.",
    "P3 With 3-4 players the targeting choices plus eight effects exceed the step and choice limits, and a first-to-7 match can exceed the 40-round cap.",
    "P4 The previous build put a {hand} placeholder in prompts, which the engine cannot fill.",
    "P5 The previous build showed bookkeeping attributes (raise_choice, response and others) in the printed state.",
    "P6 The previous build declared full_deck and must_countess but no running step ever changed them.",
    "P7 The Prince's free target choice in 2-player play needs an extra choice step beyond the limit."
  ],
  "changes": [
    {
      "what": "Keep the previous variation's stake mechanic. Once per hand, before drawing, the active player may raise the stake from 1 to 2. The opponent accepts (the stake becomes 2) or folds (the raiser wins the hand for 1 point).",
      "why": "Players now win more on hands they read well and lose less on hands the draw spoiled. Bluffing and reading become central skills, and luck is diluted.",
      "fixes": "P1"
    },
    {
      "what": "Fix the game at 2 players. Seat 1 starts the first hand, the starting seat alternates every hand, and a tie on discard sums awards no points.",
      "why": "Removes the date rule and the winner-starts snowball, and closes the undefined tie.",
      "fixes": "P2"
    },
    {
      "what": "Set the goal at first to 5 points. A round is one player's turn, with a cap of 40 rounds; at the cap, more points wins, then more hands won, otherwise a draw.",
      "why": "Fits the round limit and the 2-player effect set while keeping a multi-hand match.",
      "fixes": "P3"
    },
    {
      "what": "Prompts use no custom placeholders. Each player's cards sit in a private player attribute `hand` that shows in the owner's state, and prompts say 'Your cards are shown in your state.' The only placeholders used are {seat} and {value}, for example the Priest's private message 'Your opponent holds {value}.'",
      "why": "The engine fills only {value} and {seat}.",
      "fixes": "P4"
    },
    {
      "what": "Give every scratch attribute hidden visibility: raise_choice, response and guess are `ally` on players; deck, full_deck, burned, hand_over, starter_seat and played_card are `none` on the table. The printed state holds only points, hands_won, protected, eliminated, discards, stake, out_of_play, deck_count, active_seat and the owner's own hand.",
      "why": "Clean state, with no empty internal fields shown to players.",
      "fixes": "P5"
    },
    {
      "what": "Build full_deck in the setup step from the rank and copies parameters by the deck recipe. At every hand start, copy it to deck and shuffle. Drop must_countess entirely and apply the forced Countess discard directly in the discard step with an `if`.",
      "why": "Every remaining attribute is now written by a step that runs, and must_countess no longer exists.",
      "fixes": "P6"
    },
    {
      "what": "The Prince always targets the opponent unless the opponent is protected, in which case it targets its player. The King and Guard do nothing against a protected opponent, and the Baron and Priest also have no effect against one.",
      "why": "Removes a fifth choice step while keeping the cards' character.",
      "fixes": "P7"
    }
  ],
  "keeps": [
    "The 16-card deck with ranks 1-8 and their classic effects (Guard, Priest, Baron, Handmaid, Prince, King, Countess, Princess).",
    "The 2-player setup: one burned card face down and three cards face up out of play.",
    "Draw one card, then discard one of two face up, applying its effect even when harmful.",
    "The forced Countess discard and Princess self-elimination.",
    "Hand end by elimination or an empty deck, with showdown by highest card and then by discard sum.",
    "A multi-hand match to a points target, like tokens of affection."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Love Letter is a compact hidden-information deduction game that fits inside the limits at 2 players. The stake raise adds reading and bluffing that counter its luck, and the build failures were implementation issues that the revised attribute and prompt plan fixes."
  },
  "variation": {
    "name": "Love Letter: Raised Stakes",
    "summary": "Two-player Love Letter played over several hands to 5 points. Before drawing, the active player may raise a hand's stake from 1 to 2, and the opponent must accept or fold, so reading and bluffing about hidden cards decide how much each hand is worth.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (16): 5 Guard (1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8). At game setup this list is built once as full_deck from the rank and copies parameters.\n\nSTATE: Each player has a private hand (only the owner sees it; it is shown in their state), public discards, points (start 0), hands_won (start 0), and public protected and eliminated flags (0/1). The table shows the stake, the out_of_play cards, deck_count and active_seat. Everything else is hidden bookkeeping.\n\nROUNDS: A round is one turn by the active player. The game lasts at most 40 rounds.\n\nHAND START (runs in round 1 and in any round after a hand ended):\n- Copy full_deck to deck and shuffle it.\n- Remove the top card face down as burned.\n- Remove the next 3 cards face up into out_of_play.\n- Deal 1 card to each player's hand.\n- Clear both players' discards, protected and eliminated. Set stake to 1 and deck_count to 10.\n- The starting seat is seat 1 in the first hand and alternates every hand after that. The starting seat becomes the active player.\n\nEACH TURN, in order:\n1. The active player's protected flag is cleared.\n2. RAISE (only if the stake is 1): the active player chooses 'raise' or 'pass'. The prompt reads: 'Your cards are shown in your state. Raise the stake to 2, or pass?'\n3. RESPONSE (only if the active player raised): the opponent chooses 'accept' or 'fold'. If they accept, the stake becomes 2 and the turn continues. If they fold, the raiser gains 1 point and 1 hand won, the hand ends, and the rest of this turn is skipped.\n4. DRAW: the top card of the deck goes into the active player's hand, and deck_count drops by 1.\n5. DISCARD: the active player chooses one of their two cards to discard face up. The prompt reads: 'Your cards are shown in your state. Choose the card to discard.' If the hand holds the Countess together with the King or a Prince, the Countess is discarded whatever was chosen. The discarded card is announced to both players ('Seat {seat} discards {value}') and its effect applies.\n6. EFFECTS:\n- Guard (1): if the opponent is not protected, the player names a rank from 2 to 8. If it matches the opponent's card, the opponent is eliminated.\n- Priest (2): if the opponent is not protected, the player alone receives the message 'Your opponent holds {value}.'\n- Baron (3): if the opponent is not protected, the two players secretly compare cards and the lower card's holder is eliminated; a tie does nothing. The eliminated card is announced.\n- Handmaid (4): the player becomes protected until the start of their next turn.\n- Prince (5): the target is the opponent, or the player if the opponent is protected. The target discards their card face up without its effect. If that card is the Princess, the target is eliminated. Otherwise the target draws the top card of the deck, or the burned card if the deck is empty.\n- King (6): if the opponent is not protected, the two players swap hands.\n- Countess (7): no effect.\n- Princess (8): the player is eliminated.\n7. HAND END CHECK:\n- If a player is eliminated, the other wins the hand.\n- Otherwise, if deck_count is 0, both players reveal their cards. The higher card wins; if the cards are equal, the higher sum of discards wins; if still tied, nobody wins the hand.\n- The winner gains points equal to the stake, plus 1 hand won. The hand ends, and the next round starts a new hand with the other seat starting.\n8. If the hand continues, the opponent becomes the active player.\n9. GAME END CHECK: if a player has 5 or more points, they win immediately. After round 40, the player with more points wins; if points are equal, more hands won wins; otherwise the game is a draw.",
    "objective": "The first player to reach 5 points wins immediately. If neither player has 5 points after 40 rounds, the player with more points wins; if points are equal, the player with more hands won wins; if that is also equal, the game is a draw.",
    "expected_effect": "Hands become unequal in value. A player who has read the opponent's card from their discards, a Priest peek or the out-of-play cards raises when strong, and can bluff a raise while holding a weak card. The opponent must infer whether to accept the risk of losing 2 or fold and concede 1. Simple policies lose: always raising is punished by an opponent who accepts only when strong, always folding concedes a point to every raise, always accepting pays double on bad hands, and always discarding the lower or the higher card loses to Barons, Princes and Guard inference. Alternating the starting seat removes the snowball, and the multi-hand target with variable stakes lets skill outweigh the draw over a match. Talk is omitted because it is a 2-player zero-sum game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 20,
    "choice_steps_per_round": 4,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
