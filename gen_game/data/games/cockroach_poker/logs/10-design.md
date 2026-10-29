# 10 design

- time: 2026-10-28T06:09:52+00:00 (53.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 3744b8cc60dad909, reply sha256 e290ad6612f914da

## Sent

````
Original game: Cockroach Poker
Players in the original: 2 to 6

Original rules:
Shuffle 64 cards (8 types x 8 copies) and deal face-down evenly. On your turn, slide one card from your hand face-down to another player and declare its creature (truthfully or falsely). The receiver may: 1) Accept - say 'true' or 'false' about your claim. If correct, you must take the card face-up in front of you; if wrong, receiver takes it. 2) Pass - peek secretly at the card, then slide it to a different player who hasn't seen it, either repeating or changing the claim. A card may be passed until all players have seen it; the last player must accept. Whoever ends up with the card starts the next round. In 2 players, remove 10 unseen cards and no passing. Lose if you collect four of the same creature in front of you or you must start a round with no cards in hand.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Cut the per-round choices to at most 4. The simplest change is to drop the PASS mechanic entirely. The sender picks a card, declares a creature and picks a receiver, and the receiver calls TRUE or FALSE, which is exactly 4 choices. Resolve, reveal, check for three of one creature and check for an empty hand exactly as now. If you want to keep some passing, make the receiver fixed instead, for example always the next seat clockwise who still has cards. That frees one choice, so a single pass with a forced claim is possible, though dropping PASS is cleaner. Keep the 24-round cap, the face-up counters and the ending that ranks fewest face-up cards with a penalty for the loser. Also check that the change reduces the shared wins among non-losers; the random-play results show many split outcomes. A tie-break such as fewest face-up cards of the single most common creature would make outright winners more common.
the game was built and behaves as specified, but evaluation found design flaws:
- the built game has 7 choice steps per round, over the limit of 4
- against random seats the results were {'seats 1 and 2': 15, 'seat 3': 11, 'seat 1': 11, 'seat 2': 20, 'seats 1 and 3': 2, 'seats 2 and 3': 1}
- a thoughtless policy `first@seat1`: won 4, lost 53, drew 3
- a thoughtless policy `first@seat2`: won 2, lost 55, drew 3
- a thoughtless policy `last@seat1`: won 20, lost 31, drew 9
- a thoughtless policy `last@seat2`: won 21, lost 36, drew 3

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
"original_summary": "Cockroach Poker is a bluffing card game. Players slide a face-down card to another player and name its creature, truthfully or not. The receiver either calls the claim true or false, or peeks and passes the card on. Whoever is wrong takes the card face-up, and a player loses on collecting four of one creature or on having to start a turn with an empty hand.",
"review": [
{"criterion": "non_degenerate", "verdict": "good", "evidence": "The previous build showed simple policies losing heavily. first@seat1 went 4-53-3, first@seat2 2-55-3, last@seat1 20-31-9 and last@seat2 21-36-3. Always calling FALSE, always telling the truth and always targeting one player can all be read and punished, because the sender adapts the true-claim rate to the receiver's habit. One weakness: seat 2 won 20 of 60 against random seats and seat 3 won 11, a seat skew probably caused by the fixed first sender."},
{"criterion": "skill_sensitive", "verdict": "good", "evidence": "Results come from reading lies, tracking which creatures are already face-up and choosing whom to target. The deal changes what each player can claim believably, but card-counting and opponent modelling decide most rounds."},
{"criterion": "headroom", "verdict": "good", "evidence": "Weak players still win some rounds on calls that are right by chance. Strong players improve by modelling each opponent's lying frequency, using face-up information and steering cards toward the player closest to three of a kind."},
{"criterion": "reasoning_dependent", "verdict": "good", "evidence": "Each player's hand and the removed cards are hidden. Every call is an inference about the sender's honesty. Every send is a plan about the receiver's likely call and about the elimination race."},
{"criterion": "verifiable", "verdict": "good", "evidence": "A call is checked by revealing the card, and losses are counts of face-up cards or an empty hand. The only weak point is the previous non-loser ranking, which produced many shared wins: 18 of 60 games against random play ended with two seats sharing the win."},
{"criterion": "fits_platform", "verdict": "bad", "evidence": "The previous build had 7 choice steps per round against a limit of 4, because passing adds a peek, a pass-or-call decision, a new receiver and a new claim. Variable-length pass chains are also a conditional block the flat step list cannot express."}
],
"problems": [
"The PASS mechanic pushes choice steps per round to 7, over the limit of 4, and needs a conditional sub-sequence the engine lacks.",
"Seat imbalance against random play (seat 2 won 20, seat 3 won 11, seat 1 won 11 outright), most likely from a fixed first sender and fixed seat order.",
"Many shared wins between the two non-losers (18 of 60 random games), so the ending often fails to separate players.",
"A 64-card, 8-creature deck makes hands large and card-counting too diffuse for a short text game. With few creatures face-up, the inference is weak until very late."
],
"changes": [
{"what": "Drop PASS entirely. Each round the sender chooses a card, chooses a claimed creature and chooses a receiver, and the receiver calls TRUE or FALSE. That is exactly 4 choice steps.", "why": "This keeps the core bluff-and-call duel inside the limit, and the step list becomes flat.", "fixes": "The PASS mechanic pushes choice steps per round to 7, over the limit of 4, and needs a conditional sub-sequence the engine lacks."},
{"what": "Choose the first sender at random during setup instead of always seat 1. After that, whoever takes a card sends next, as in the original.", "why": "This removes the built-in seat advantage while keeping the original's rule that the loser of a card starts the next round.", "fixes": "Seat imbalance against random play (seat 2 won 20, seat 3 won 11, seat 1 won 11 outright), most likely from a fixed first sender and fixed seat order."},
{"what": "Shrink the deck to 4 creatures x 6 copies (24 cards). Deal 7 to each of 3 players and set 3 aside unseen. A player loses on 3 face-up cards of one creature.", "why": "Fewer creatures make face-up information and card-counting meaningful and the game short. The 3 hidden cards keep counting from becoming certain.", "fixes": "A 64-card, 8-creature deck makes hands large and card-counting too diffuse for a short text game. With few creatures face-up, the inference is weak until very late."},
{"what": "Use a chain of arithmetic tie-breaks among non-losers. First, fewest face-up cards. Then fewest cards of their single most common face-up creature. Then most cards still in hand. Only after that is it a draw.", "why": "Outright winners become far more common, and every tie-break is a count the engine tracks.", "fixes": "Many shared wins between the two non-losers (18 of 60 random games), so the ending often fails to separate players."}
],
"keeps": [
"Face-down card handed over with a claim that may be a lie.",
"The receiver calls TRUE or FALSE, and whoever is wrong takes the card face-up.",
"Losing by collecting too many of one creature, or by having to send with an empty hand.",
"The loser of a card sends next, so being caught creates pressure to act.",
"The sender chooses whom to target, which creates ganging-up and elimination-race dynamics."
],
"recommendation": {"decision": "adapt", "kind": "none", "reason": "The bluff-and-call core fits in exactly 4 choices once passing is removed. Hidden hands and lie detection give real inference, and the earlier tests showed thoughtless policies lose."},
"variation": {
"name": "Cockroach Poker: Straight Calls",
"summary": "This is a three-player game. A sender hands one face-down card to a chosen rival and claims its creature. The rival calls TRUE or FALSE, and whoever is wrong takes the card face-up. The game ends as soon as one player loses, and the other two are ranked by fewest face-up cards.",
"players": {"min": 3, "max": 3, "suggested": 3},
"rules": "SETUP\n- The deck has 24 cards: 4 creatures (Cockroach, Rat, Stinkbug, Toad), 6 copies of each.\n- Shuffle. Deal 7 cards face-down to each of the 3 players as their private hand. Set the remaining 3 cards aside face-down, unseen by anyone, for the whole game.\n- Each player starts with no face-up cards.\n- Choose the first sender uniformly at random.\n\nEACH ROUND (at most 24 rounds)\n1. Announce the round number, the sender, and every player's face-up cards (counts per creature) and hand size.\n2. The sender privately chooses one card from their own hand.\n3. The sender chooses a claim: one of the 4 creatures. It may be true or false.\n4. The sender chooses a receiver: either of the other two players.\n5. The receiver, who sees the claim but not the card, calls TRUE (the card is the claimed creature) or FALSE (it is not).\n6. Reveal the card to everyone.\n   - The receiver is correct if they called TRUE and the card matches the claim, or called FALSE and it does not.\n   - If the receiver is correct, the sender takes the card face-up.\n   - If the receiver is wrong, the receiver takes it face-up.\n   - Either way, the card has left the sender's hand.\n7. The player who took the card face-up becomes the sender for the next round.\n8. Loss check: if the player who took the card now has 3 face-up cards of the same creature, that player LOSES and the game ends.\n9. Empty-hand check: if the next sender has no cards in hand, that player LOSES and the game ends.\n10. If round 24 has finished without a loser, the game ends with no loser.\n\nTALK\nThere is no separate talk phase. The claim is the only message.\n\nENDING\nWhen the game ends, the losing player (if any) cannot win. The players who did not lose are ranked by these tests in order:\n(a) fewest total face-up cards;\n(b) if tied, the smaller count of their single most common face-up creature;\n(c) if still tied, the most cards remaining in hand.\nThe player ranked first wins. If the top players are tied on all three tests, the game is a draw between them.",
"objective": "Avoid being the loser, who ends the game with 3 face-up cards of one creature or must send with an empty hand. Among the players who did not lose, the one with the fewest face-up cards wins. Ties are broken by the smaller count of their most common face-up creature, then by more cards left in hand. Players tied on all three draw.",
"expected_effect": "Every round is a two-player lie-detection duel with a third player watching and keeping score. Senders must vary their truth rate per receiver, because a receiver who always calls FALSE is beaten by honest claims and one who always calls TRUE is beaten by lies. Face-up counts and the shrinking 24-card deck let players reason about what a sender can still hold, and claiming a creature the receiver already has two of becomes a pointed threat. A random first sender removes the seat skew, and the three-step tie-break should turn most shared non-loser wins into outright wins.\n\nTalk is left out deliberately. The claim already is the communication, and a free chat would mostly repeat claims or let two players openly coordinate against the third. That second effect already arises tacitly through the choice of receiver, which keeps it a matter of reading rather than of announcing.\n\nBecause the winner is the non-loser with the fewest face-up cards, nobody can safely coast. Pushing cards onto the leader matters as much as sinking the weakest player, so a player who blindly piles onto whoever is nearly eliminated can end the game while holding more face-up cards than the other survivor, and lose."
},
"model": null,
"complexity": {"steps_per_round": 12, "choice_steps_per_round": 4, "attributes": 14, "hidden_elements": 2, "random_draws_per_round": 0, "rounds": 24}
}
```
````
