# 12 spec

- time: 2026-10-28T06:12:08+00:00 (43.2s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 2d1e76edad1f10aa, reply sha256 918d6ded94f896a4

## Sent

````
Game: Cockroach Poker: Straight Calls
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP
- The deck has 24 cards: 4 creatures (Cockroach, Rat, Stinkbug, Toad), 6 copies of each.
- Shuffle. Deal 7 cards face-down to each of the 3 players as their private hand. Set the remaining 3 cards aside face-down, unseen by anyone, for the whole game.
- Each player starts with no face-up cards.
- Choose the first sender uniformly at random.

EACH ROUND (at most 24 rounds)
1. Announce the round number, the sender, and every player's face-up cards (counts per creature) and hand size.
2. The sender privately chooses one card from their own hand.
3. The sender chooses a claim: one of the 4 creatures. It may be true or false.
4. The sender chooses a receiver: either of the other two players.
5. The receiver, who sees the claim but not the card, calls TRUE (the card is the claimed creature) or FALSE (it is not).
6. Reveal the card to everyone.
   - The receiver is correct if they called TRUE and the card matches the claim, or called FALSE and it does not.
   - If the receiver is correct, the sender takes the card face-up.
   - If the receiver is wrong, the receiver takes it face-up.
   - Either way, the card has left the sender's hand.
7. The player who took the card face-up becomes the sender for the next round.
8. Loss check: if the player who took the card now has 3 face-up cards of the same creature, that player LOSES and the game ends.
9. Empty-hand check: if the next sender has no cards in hand, that player LOSES and the game ends.
10. If round 24 has finished without a loser, the game ends with no loser.

TALK
There is no separate talk phase. The claim is the only message.

ENDING
When the game ends, the losing player (if any) cannot win. The players who did not lose are ranked by these tests in order:
(a) fewest total face-up cards;
(b) if tied, the smaller count of their single most common face-up creature;
(c) if still tied, the most cards remaining in hand.
The player ranked first wins. If the top players are tied on all three tests, the game is a draw between them.

How the winner is decided: Avoid being the loser, who ends the game with 3 face-up cards of one creature or must send with an empty hand. Among the players who did not lose, the one with the fewest face-up cards wins. Ties are broken by the smaller count of their most common face-up creature, then by more cards left in hand. Players tied on all three draw.
````

## Reply

````
{
  "name": "Cockroach Poker: Straight Calls",
  "summary": "Three players pass cards face-down with a creature claim. The receiver calls the claim true or false, and whoever is wrong about the card takes it face-up. Three face-up cards of one creature, or having to send from an empty hand, loses.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "deck_size": 24,
    "creature_kinds": 4,
    "copies_per_creature": 6,
    "hand_size_start": 7,
    "aside_cards": 3,
    "max_rounds": 24,
    "loss_same_creature": 3,
    "receiver_options": 2
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The player's private hand of creature cards, one entry per card, such as 'Rat'.", "observable": false},
      {"key": "hand_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in the hand.", "observable": true},
      {"key": "face_cockroach", "type": "number", "visible": "public", "initial": 0, "meaning": "Face-up Cockroach cards.", "observable": true},
      {"key": "face_rat", "type": "number", "visible": "public", "initial": 0, "meaning": "Face-up Rat cards.", "observable": true},
      {"key": "face_stinkbug", "type": "number", "visible": "public", "initial": 0, "meaning": "Face-up Stinkbug cards.", "observable": true},
      {"key": "face_toad", "type": "number", "visible": "public", "initial": 0, "meaning": "Face-up Toad cards.", "observable": true},
      {"key": "face_total", "type": "number", "visible": "public", "initial": 0, "meaning": "Total face-up cards, the sum of the four face counts.", "observable": true},
      {"key": "max_face", "type": "number", "visible": "public", "initial": 0, "meaning": "Largest of the four face counts.", "observable": true},
      {"key": "lost", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if this player has lost, otherwise 0.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["Cockroach x6", "Rat x6", "Stinkbug x6", "Toad x6"], "meaning": "The 24-card deck before dealing: 6 entries of each creature.", "observable": false},
      {"key": "aside", "type": "list", "visible": "none", "initial": [], "meaning": "The 3 cards set aside face-down, unseen by anyone, for the whole game.", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Current round number.", "observable": true},
      {"key": "sender", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the current sender.", "observable": true},
      {"key": "receiver", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat chosen as receiver this round.", "observable": true},
      {"key": "card_in_play", "type": "text", "visible": "none", "initial": "", "meaning": "The creature on the card being passed. It stays hidden until the reveal.", "observable": false},
      {"key": "revealed_card", "type": "text", "visible": "public", "initial": "", "meaning": "The passed card's creature, made public at the reveal.", "observable": true},
      {"key": "claim", "type": "text", "visible": "public", "initial": "", "meaning": "The sender's claimed creature.", "observable": true},
      {"key": "call", "type": "text", "visible": "public", "initial": "", "meaning": "The receiver's call, TRUE or FALSE.", "observable": true},
      {"key": "taker", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that took the card face-up this round.", "observable": true},
      {"key": "game_over", "type": "number", "visible": "public", "initial": 0, "meaning": "1 once the game has ended.", "observable": true}
    ]
  },
  "setup": [
    "Fill deck with 24 cards: 6 each of Cockroach, Rat, Stinkbug and Toad.",
    "Deal 7 cards to each of the 3 players. Each card is a random draw removed from deck and appended to that player's hand. Set each hand_size to 7.",
    "Move the remaining 3 cards from deck to aside, unseen by anyone, for the whole game.",
    "Every player starts with all face counts, face_total, max_face and lost at 0.",
    "Set sender to a seat chosen uniformly at random, and set round to 1."
  ],
  "round": [
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce round, sender, and each player's face_cockroach, face_rat, face_stinkbug, face_toad and hand_size."},
    {"action": "ask", "who": "the sender (seat = sender)", "answer": "one creature present in the sender's hand", "effect": "Set card_in_play to the chosen creature. Remove one card of that creature from the sender's hand and decrease the sender's hand_size by 1."},
    {"action": "ask", "who": "the sender (seat = sender)", "answer": "one of Cockroach, Rat, Stinkbug, Toad", "effect": "Set claim to the answer, visible to all."},
    {"action": "ask", "who": "the sender (seat = sender)", "answer": "one of the two other seats", "effect": "Set receiver to the chosen seat."},
    {"action": "ask", "who": "the receiver (seat = receiver)", "answer": "TRUE or FALSE", "effect": "Set call to the answer."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set revealed_card = card_in_play and announce it. Let correct = (call == TRUE and card_in_play == claim) or (call == FALSE and card_in_play != claim). If correct, taker = sender, otherwise taker = receiver. Add 1 to the taker's face_<card_in_play> and to their face_total, and recompute the taker's max_face."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set sender = taker for the next round."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If the taker's face count for revealed_card >= 3, set the taker's lost = 1 and game_over = 1, and end the game."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If the new sender's hand_size == 0, set that player's lost = 1 and game_over = 1, and end the game."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round >= 24, set game_over = 1 and end the game with no loser. Otherwise add 1 to round."}
  ],
  "ending": {
    "condition": "game_over == 1, which happens when some player's lost == 1 or when round 24 has finished",
    "rank_by": "(1 - you.lost) * 1000000 - you.face_total * 10000 - you.max_face * 100 + you.hand_size",
    "decided_by": "A player who lost can never rank above a player who did not. Among the others, fewest face-up cards ranks first, then the smaller most-common face-up creature count, then more cards left in hand. The highest value wins, and players level on all three tests share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup, each of the 3 players holds 7 cards, 3 cards are set aside unseen, and the deck of 24 (6 of each of 4 creatures) is fully used."},
    {"id": "R2", "text": "At setup, every player has 0 face-up cards and lost = 0, and the first sender is a random seat."},
    {"id": "R3", "text": "Each round, the sender passes one card from their own hand, and the sender's hand_size falls by 1."},
    {"id": "R4", "text": "The sender's claim is one of Cockroach, Rat, Stinkbug or Toad, and it may differ from the card."},
    {"id": "R5", "text": "The receiver must be one of the two seats other than the sender."},
    {"id": "R6", "text": "When the receiver calls TRUE and the card matches the claim, the sender takes the card face-up."},
    {"id": "R7", "text": "When the receiver calls FALSE and the card does not match the claim, the sender takes the card face-up."},
    {"id": "R8", "text": "When the receiver calls TRUE and the card does not match, or calls FALSE and it matches, the receiver takes the card face-up."},
    {"id": "R9", "text": "The card is revealed to everyone after the call, and the taker's count for that creature and face_total rise by 1."},
    {"id": "R10", "text": "The player who took the card face-up is the sender of the next round."},
    {"id": "R11", "text": "When the taker reaches 3 face-up cards of one creature, the taker's lost becomes 1 and the game ends."},
    {"id": "R12", "text": "When the next sender has 0 cards in hand, that player's lost becomes 1 and the game ends."},
    {"id": "R13", "text": "When round 24 finishes without a loser, the game ends with no loser."},
    {"id": "R14", "text": "A player with lost = 1 cannot win."},
    {"id": "R15", "text": "Among the players who did not lose, the one with the fewest face_total wins."},
    {"id": "R16", "text": "If face_total is tied, the smaller max_face wins. If that is still tied, the larger hand_size wins. If all three are tied, the tied players draw."}
  ],
  "offers": [
    {"question": "Which card to pass", "who": "the sender only", "options": "each distinct creature currently in the sender's hand"},
    {"question": "Which creature to claim", "who": "the sender only", "options": "Cockroach, Rat, Stinkbug, Toad"},
    {"question": "Who receives the card", "who": "the sender only", "options": "the two seats other than the sender"},
    {"question": "Call the claim", "who": "the receiver only", "options": "TRUE, FALSE"}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed the game at 3. The deal of 7 + 7 + 7 + 3 aside uses the 24-card deck exactly, so another count would break the deal. Three seats also give the sender a real choice of whom to target."},
    {"what": "No talk phase", "why": "The rules say the claim is the only message."},
    {"what": "Single rank_by expression with weights 1000000 / 10000 / 100", "why": "This encodes not-lost first, then fewest face_total, then smaller max_face, then more hand_size. Each weight exceeds the largest possible value of the next term (face_total <= 24, max_face <= 6, hand_size <= 7)."},
    {"what": "Strategy at the table", "why": "The sender reads which creatures each player already shows and steers cards toward the player closest to 3 of a kind, bluffing or telling the truth unpredictably. The receiver weighs the sender's hand and the creatures already exposed when calling."}
  ],
  "simplifications": [
    {"what": "A card is chosen by naming its creature", "why": "Copies of a creature are identical, so naming the creature is equivalent to picking the card."},
    {"what": "The sender's three decisions are three sequential asks", "why": "Only the sender answers them and the receiver does not see the card, so splitting them changes nothing."}
  ],
  "unsupported": []
}
````
