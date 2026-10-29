# Variation: Roach Bluff

This is a compact Cockroach Poker for 3–4 players. Players send face-down creature cards with claims that may be lies. Receivers call the claim or peek and pass it once. Wrong judges and exposed liars collect cards face-up. Three of one creature loses, and the cleanest survivor wins.

Players: 3 to 4, best with 4

## Review of the original

Cockroach Poker is a bluffing card game. Players slide face-down cards to each other with a claimed creature. The receiver either calls the claim true or false or, after peeking, passes the card on with a new claim. Whoever judges wrongly, or whose claim is caught out, takes the card face-up. Collecting four of one creature, or running out of cards to send, loses.

- **non_degenerate**: good. No simple policy is safe. If a receiver always says 'true', senders bluff every time and the receiver collects cards. If a sender always tells the truth, receivers always say 'true' and the sender collects them. If a player always passes, they give away information and still end up holding cards. Always picking the same target lets that target predict and exploit you. The only built-in edge is that the first sender has a forced move, which matters little.
- **skill_sensitive**: good. The deal decides only which cards you can send. The outcome comes from reading bluffs, choosing claims, and steering cards toward players who are close to losing. Card counting from the face-up piles also gives better players a real edge.
- **headroom**: good. Mixing truth and lies, reasoning about which creatures are still in hand, and targeting the player nearest a losing set all reward deeper play. A weak player still gets about half their calls right by chance.
- **reasoning_dependent**: good. Hands are hidden and the card in play is hidden. Every call means modelling the sender's incentive to lie and using the public face-up counts to judge how likely the claim is. Passing creates second-order bluffs.
- **verifiable**: good. Card identities are tracked, and whether a call was right is a direct comparison. The loss conditions are counts.
- **fits_platform**: weak. The game is turn-based and text-only. However, the open-ended pass chain (up to five passes with 6 players) needs a variable-length subsequence. 64 cards across 6 players is long. Only one loser is named, with no single winner. The 2-player mode with no passing loses the second-order bluffing.

## Problems

- The unbounded pass chain needs a variable number of choice steps per round. The engine cannot branch into repeating blocks.
- 64 cards with 8 creatures and four-of-a-kind to lose makes games too long, with too much state for the step and attribute budgets.
- The game names only one loser. The engine must declare a winner or a draw, so the outcome among the survivors is undefined.
- The 2-player variant removes passing and plays almost like a pure guessing game. Wide player counts (2–6) make balancing hard.

## Changes

- At most one pass per card. A receiver who passes peeks, then sends the card with a new claim to a player who is neither the original sender nor themselves. That final receiver must call true or false. (fixes: The unbounded pass chain needs a variable number of choice steps per round. The engine cannot branch into repeating blocks.): This keeps the peek-and-pass double bluff but fits into a flat list of 4 choice steps, using `when` conditions on the pass steps.
- Use 24 cards: 4 creatures (Roach, Rat, Fly, Toad), 6 copies each. Collecting three of one creature face-up loses. (fixes: 64 cards with 8 creatures and four-of-a-kind to lose makes games too long, with too much state for the step and attribute budgets.): Games last about 8–20 rounds and the state stays small. Card counting stays tractable but non-trivial.
- When a player loses, the game ends immediately. Among the other players, the one with the fewest face-up cards wins. If several tie for fewest, the game is a draw. (fixes: The game names only one loser. The engine must declare a winner or a draw, so the outcome among the survivors is undefined.): The winner is decided by arithmetic. Players must avoid cards all game, not just avoid the losing set, which rewards consistent good calls throughout.
- Restrict play to 3–4 players and drop the 2-player mode. (fixes: The 2-player variant removes passing and plays almost like a pure guessing game. Wide player counts (2–6) make balancing hard.): With at least 3 players, passing is always possible and targeting has meaning. Fewer counts are easier to balance.

## Kept from the original

- Sliding a face-down card with a declared creature that may be a lie.
- The receiver's choice to call true or false, or to peek and pass with a new claim.
- The loser of the judgement takes the card face-up and becomes the next sender.
- Losing by collecting a set of one creature or by having no card to send.

## The variation's rules

SETUP: The deck has 24 cards: 6 Roach, 6 Rat, 6 Fly and 6 Toad. Shuffle it once and deal it all face-down. With 4 players each gets 6 cards; with 3 players each gets 8. Each player's hand is private. Every player has a face-up pile, which starts empty; all face-up piles are public. Seat 1 is the first sender.

EACH ROUND:
1. The engine announces every player's face-up counts per creature and every player's hand size.
2. SEND: The sender privately picks one card from their hand. They declare a creature (Roach, Rat, Fly or Toad), which may be true or false. They also pick one other player as receiver. The card leaves the sender's hand and becomes the card in play. The claim and the receiver are announced to all; the card's identity is not.
3. RESPOND: The receiver chooses TRUE, FALSE or PASS.
   - TRUE or FALSE: Go to step 5.
   - PASS: Go to step 4.
4. PASS (only when the receiver chose PASS):
   - The receiver privately sees the card and becomes the passer.
   - The passer declares a creature, which may be true or false. They pick a new receiver who is neither the original sender nor the passer.
   - The new claim and new receiver are announced.
   - The final receiver must choose TRUE or FALSE; passing again is not allowed.
5. RESOLVE: The claim being judged is the latest one; the claimer is whoever made it (the sender, or the passer if there was a pass).
   - If the judge's call is correct (TRUE and the card matches the claim, or FALSE and it does not), the claimer takes the card face-up.
   - Otherwise the judge takes the card face-up.
   - The card's identity is revealed to everyone, and the player who took the card becomes the next sender.
6. CHECK:
   - If any player now has 3 face-up cards of one creature, that player loses and the game ends.
   - Otherwise, if the next sender has no cards in hand, that player loses and the game ends.

The game cannot last more than 24 rounds. There is no table talk: the claims are the only communication.

Objective: When the game ends, the player who triggered the end (three of one creature face-up, or no card to send) loses. Among all other players, the one with the fewest total face-up cards wins. If two or more of them tie for fewest, the game is a draw.

Expected effect: Players must mix truthful and false claims unpredictably. They count the public face-up piles and their own hand to judge how likely a claim is. They steer cards at whoever is nearest a losing set while watching their own total, because the winner is the cleanest survivor. The single pass adds a second layer: the passer knows the truth and can relay or twist it. A separate talk phase is left out because the claims already are the communication and adding messages would only lengthen rounds. Every simple policy loses to a player who exploits it: always-TRUE is bluffed, always-truthful is called, always-PASS hands opponents information and still has to make a claim that can be caught.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
