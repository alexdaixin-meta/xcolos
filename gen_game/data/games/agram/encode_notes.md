# Agram Match: encoding notes

## Status

- `python3 -m gen_game verify agram game`: **ok**
- `python3 -m gen_game verify agram rules`: **17 of 21 scenarios fail.** As far as I can tell from the failure text, every failure comes from chance, not from a broken rule (see below).

## One round is one trick, not one hand

The script makes a round one hand and plays the 6 tricks with a `repeat` inside it. I built it that way first. The scenarios count a round the same way (rounds = 1 means one whole hand). But `verify game` then fails with "an option is offered and then refused". That lint compares two questions from the same step to the same seat in the same round. If a seat leads twice in one hand, the second offer is its hand minus the card it already played. That is a strict subset of the first offer, so the lint reads it as a refusal. Step labels are fixed, so any design where a seat plays 6 cards in one round under one label trips it.

So the file plays **one trick per round** (36 rounds, `limits.rounds` 36, `rounds_max` 40). The hand-level steps are gated on state:

- **"A new hand"** (hand_number += 1, rotate the dealer, gather and reset) runs only when every hand is empty. The deal `repeat` is gated the same way.
- **The stub and the private hand message** run only while `trick_number == 0`.
- **Hand scoring and the standings** run only when `trick_number == tricks_per_hand`.
- **The check** fires when `hand_number >= num_hands` after trick 6.

The rules play the same either way, and the scenario results were the same 17/21 in both structures. One consequence: a scenario that sets 6-card hands and stops after `rounds: 1` sees one trick played, not six.

Because a hand is only redealt when all hands are empty, a state set from outside (hands already dealt, or a hand in progress at trick 5) continues from where it is. It is not overwritten. If `trick_winner_seat` is 0 mid-hand, the leader falls back to the seat left of the dealer.

## The failing scenarios

The 17 failures are mostly "Ada: the rule for 'HA' was never matched (the game never put that option to this seat)" and similar for DA, CA, H10 and S10. The R20 ones are point totals that depend on who wins trick 6. These scenarios set no hands, so whether Ada holds HA depends on the random deal. I checked the opposite case with my own scenarios: given hands are played exactly as given, followers are offered only led-suit cards, and the highest led-suit card wins. Dealing from the top of an unshuffled deck changed which of those rules matched but did not make them pass, so the scenarios do not stack the deck either. I did not read `scenarios.json`.

## Other choices

- **Cards** are suit + rank (`HA`, `S10`), as in the script's deck. The calculator has no slicing or `str()`. So each seat's card for the current trick is also kept in a hidden player attribute `played`. The winner is the first `lead_suit + rank`, going through `rank_order` (A,10,9,…,3, set in setup), that appears among the played cards. Spades has no A, so its order is 10 down to 3 automatically.
- **trick_plays** entries read `"seat N: CARD"`, so plays are recorded with the seat as the script asks. Each play is also broadcast to all as "Seat N plays CARD".
- **Shuffle** is the recipe's random draw from the deck, one card at a time, while dealing. Batches go clockwise from the dealer's left: three cards to each seat, then three more. Seat number + 1 counts as clockwise/left. The cards left over become `stub`, and `deck` is emptied. At the next hand, deck + stub + played cards are gathered and the deal starts again.
- **Clockwise follow order from any leader** uses three follower `ask` steps (follower k is seat `leader + k`). The third is skipped at 3 players. The leader's answer sets `lead_suit` and rebuilds every seat's `offer`: their led-suit cards if they hold any, otherwise their whole hand. Nothing is refused afterwards.
- **"Seat 1 to num_players" lists** in the private message, the standings and the endings use the engine's expressions in text. Seat 4 appears only through `{', seat 4 ' if len(players) > 3 else ''}{players[3].match_points if len(players) > 3 else ''}`. The draw ending prints the tied seats as a list ("Draw among seats [1, 2, 3]").
- **Private message at the start of a hand** is a `tell` using the given template only. A `sync` would add a state dump. The engine itself adds a "Living seats" line to every turn prompt. The game cannot remove it.
- **lead_suit and trick_winner_seat** are public as STATE says. They are reset to `""` / `0` when a trick starts, so the previous trick's winner is not shown as current. With public visibility the empty values may still appear in a state dump, which the platform controls.
- **Round step 1** (`hand_number == 0`: zero the match points, rebuild the deck) repeats what setup already did. It is kept because the script lists it.
- **Setup steps 4–5** (ranks, no discussion): step 4 really sets `rank_order`, which decides every trick. Step 5 is a `tell`, because "no discussion" has no state to change. The game has no talk step.
