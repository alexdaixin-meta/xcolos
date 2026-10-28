# 08 spec

- time: 2026-10-28T06:20:37+00:00 (59.2s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 fbd4ed8d1c3ead70, reply sha256 b456c8c1f738308f

## Sent

````
Game: Put: Show One, Keep Three
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. Use a standard 52-card deck; suits do not matter. Strengths: 3 = 13, 2 = 12, A = 11, K = 10, Q = 9, J = 8, 10 = 7, 9 = 6, 8 = 5, 7 = 4, 6 = 3, 5 = 2, 4 = 1. Higher strength is better.

SETUP. There are two players, A and B. Each starts with 0 points and 0 hands won. The match lasts exactly 40 hands. In odd-numbered hands A is the Caller and B the Responder. In even-numbered hands B is the Caller and A the Responder.

EACH HAND:
1. Deal. Shuffle all 52 cards and deal 4 cards to each player. Each player's 4th card is face up and announced to both players. The other 3 are private to their holder.

2. Caller's call. The Caller says PUT or PASS.

3. Responder's answer.
- If the Caller said PUT, the Responder says SEE, FOLD or RE-PUT. On SEE, the stake is 2; go to step 5. On FOLD, the Caller scores 1 point and wins the hand; go to step 8. On RE-PUT, go to step 4.
- If the Caller said PASS, the Responder says PUT or PASS. On PASS, the stake is 1; go to step 5. On PUT, go to step 4.

4. Caller's answer. This step happens only if the Responder said RE-PUT or PUT in step 3. The Caller says SEE or FOLD.
- After a RE-PUT: SEE makes the stake 4. FOLD gives the Responder 2 points and the hand.
- After a PUT that followed the Caller's PASS: SEE makes the stake 2. FOLD gives the Responder 1 point and the hand.
- A FOLD ends the hand; go to step 8.

5. Play (simultaneous). Each player secretly writes an ordered list of 3 different cards chosen from their own 4 cards. The face-up card may be used or left out. The lists are then revealed.

6. Tricks. Compare the 1st cards of the two lists, then the 2nd cards, then the 3rd cards. In each pair the higher strength wins that trick. Equal strength ties the trick, and it belongs to no one.

7. Score. A player who won at least 2 of the 3 tricks scores the stake (1, 2 or 4) and wins the hand. Otherwise, for example one trick each with a tie, or one win and two ties, or three ties, nobody scores.

8. Announce. Announce all calls, all 8 cards (including any card that was left out or never played), the hand result, and both players' points and hands won.

END. After hand 40 the match ends.

How the winner is decided: After 40 hands, the player with more points wins. If points are equal, the player with more hands won wins. A hand is won by scoring it on tricks or by the opponent folding. If both are equal, the match is a draw.
````

## Reply

````
```json
{
  "name": "Put: Show One, Keep Three",
  "summary": "A two-player betting card duel over 40 hands. Each player holds 3 hidden cards and 1 face-up card, calls are made to raise the stake, and then each secretly orders 3 of their 4 cards to fight 3 tricks.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "hands_total": 40,
    "deck_size": 52,
    "cards_dealt_per_player": 4,
    "private_cards_per_player": 3,
    "face_up_cards_per_player": 1,
    "cards_played": 3,
    "tricks_per_hand": 3,
    "tricks_to_win_hand": 2,
    "starting_points": 0,
    "starting_hands_won": 0,
    "stake_pass_pass": 1,
    "stake_put_see": 2,
    "stake_pass_put_see": 2,
    "stake_reput_see": 4,
    "fold_to_put_points": 1,
    "fold_to_reput_points": 2,
    "fold_to_put_after_pass_points": 1,
    "strength_3": 13,
    "strength_2": 12,
    "strength_A": 11,
    "strength_K": 10,
    "strength_Q": 9,
    "strength_J": 8,
    "strength_10": 7,
    "strength_9": 6,
    "strength_8": 5,
    "strength_7": 4,
    "strength_6": 3,
    "strength_5": 2,
    "strength_4": 1,
    "suits": 4,
    "rank_points_weight": 1000
  },
  "attributes": {
    "player": [
      {"key": "points", "type": "number", "visible": "public", "initial": 0, "meaning": "Match points scored so far.", "observable": true},
      {"key": "hands_won", "type": "number", "visible": "public", "initial": 0, "meaning": "Hands won, either on tricks or because the opponent folded. Used as the tie-break.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The player's 3 private cards this hand. Each card is coded as strength*10+suit, e.g. 134 is a 3 (strength 13) of suit 4.", "observable": false},
      {"key": "face_up", "type": "number", "visible": "public", "initial": 0, "meaning": "The player's 4th card, dealt face up and announced to both players (same coding).", "observable": true},
      {"key": "play", "type": "list", "visible": "ally", "initial": [], "meaning": "The ordered list of 3 different cards the player secretly chose from hand plus face_up. It is revealed in the announcement.", "observable": false},
      {"key": "tricks_won", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won in the current hand (0 to 3).", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "all 52 codes s*10+u for strength s in 1..13 and suit u in 1..4", "meaning": "The shuffled deck that cards are dealt from. It is refilled every hand.", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "Current hand, from 1 to 40. When odd, seat 1 (A) is the Caller; when even, seat 2 (B) is the Caller.", "observable": true},
      {"key": "caller_call", "type": "text", "visible": "public", "initial": "", "meaning": "The Caller's call: PUT or PASS.", "observable": false},
      {"key": "responder_answer", "type": "text", "visible": "public", "initial": "", "meaning": "The Responder's answer: SEE, FOLD, RE-PUT, PUT or PASS.", "observable": false},
      {"key": "caller_answer", "type": "text", "visible": "public", "initial": "", "meaning": "The Caller's second answer: SEE or FOLD, or empty if step 4 did not happen.", "observable": false},
      {"key": "stake", "type": "number", "visible": "public", "initial": 0, "meaning": "The stake played for on tricks: 1, 2 or 4.", "observable": false},
      {"key": "folded", "type": "bool", "visible": "public", "initial": false, "meaning": "True when a FOLD ended the hand before play.", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 is player A and seat 2 is player B.",
    "Both players start with points = 0 and hands_won = 0.",
    "hand_number is set to 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Refill deck with all 52 cards. Clear each player's hand and play, set tricks_won = 0 and face_up = 0. Set stake = 0, folded = false, and caller_call, responder_answer and caller_answer to empty."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Deal: for each player, draw 3 cards at random from deck into hand, then draw 1 card at random from deck into face_up. Each drawn card is removed from deck."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce hand_number, who is Caller and who is Responder, and both players' face_up cards."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand and face_up, the opponent's face_up, and both players' points and hands_won."},
    {"action": "ask", "who": "the Caller (seat 1 if hand_number is odd, seat 2 if even)", "answer": "PUT or PASS", "effect": "Set caller_call to the answer."},
    {"action": "ask", "who": "the Responder (seat 2 if hand_number is odd, seat 1 if even)", "answer": "If caller_call = PUT: SEE, FOLD or RE-PUT. If caller_call = PASS: PUT or PASS.", "effect": "Set responder_answer to the answer."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If caller_call = PUT and responder_answer = SEE, set stake = 2. If caller_call = PUT and responder_answer = FOLD, the Caller gets points += 1 and hands_won += 1, and folded = true. If caller_call = PASS and responder_answer = PASS, set stake = 1."},
    {"action": "ask", "who": "the Caller, only when responder_answer is RE-PUT or PUT", "answer": "SEE or FOLD", "effect": "Set caller_answer to the answer."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If responder_answer = RE-PUT and caller_answer = SEE, set stake = 4. If responder_answer = RE-PUT and caller_answer = FOLD, the Responder gets points += 2 and hands_won += 1, and folded = true. If responder_answer = PUT and caller_answer = SEE, set stake = 2. If responder_answer = PUT and caller_answer = FOLD, the Responder gets points += 1 and hands_won += 1, and folded = true."},
    {"action": "poll", "who": "all players, only when folded = false", "answer": "One of the 24 ordered lists of 3 different cards drawn from the player's 4 cards (hand plus face_up).", "effect": "Set each player's play to the chosen ordered list. Neither player sees the other's choice until both are in."},
    {"action": "update", "who": "all players, only when folded = false", "answer": null, "effect": "For each position i = 1, 2, 3, compare floor(play[i]/10) between the two players. The higher strength gets tricks_won += 1. Equal strength gives the trick to no one."},
    {"action": "update", "who": "all players, only when folded = false", "answer": null, "effect": "A player with tricks_won >= 2 gets points += stake and hands_won += 1. Otherwise nobody scores."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce caller_call, responder_answer, caller_answer, all 8 cards (both hands and face_up cards, including cards left out or never played), both play lists, tricks_won, the hand result, and both players' points and hands_won."},
    {"action": "update", "who": "all players", "answer": null, "effect": "hand_number += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if hand_number > 40. Otherwise run the round again."}
  ],
  "ending": {
    "condition": "hand_number > 40",
    "rank_by": "you.points * 1000 + you.hands_won",
    "decided_by": "After 40 hands the player with more points wins. If points are equal, the player with more hands won wins. If both are equal, the players share the result, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "Card strengths are 3=13, 2=12, A=11, K=10, Q=9, J=8, 10=7, 9=6, 8=5, 7=4, 6=3, 5=2, 4=1, and suits do not matter."},
    {"id": "R2", "text": "Both players start with 0 points and 0 hands won, and the match lasts exactly 40 hands."},
    {"id": "R3", "text": "When hand_number is odd, seat 1 (A) is the Caller and seat 2 (B) is the Responder; when it is even, seat 2 is the Caller and seat 1 is the Responder."},
    {"id": "R4", "text": "Each hand, all 52 cards are shuffled and each player gets 3 private cards in hand and 1 face_up card that is announced to both players."},
    {"id": "R5", "text": "The Caller first says PUT or PASS."},
    {"id": "R6", "text": "When the Caller said PUT and the Responder says SEE, the stake is 2 and play follows."},
    {"id": "R7", "text": "When the Caller said PUT and the Responder says FOLD, the Caller scores 1 point and 1 hand won, and the hand ends without play."},
    {"id": "R8", "text": "When the Caller said PUT and the Responder says RE-PUT, the Caller must answer SEE or FOLD."},
    {"id": "R9", "text": "When the Caller said PASS and the Responder says PASS, the stake is 1 and play follows."},
    {"id": "R10", "text": "When the Caller said PASS and the Responder says PUT, the Caller must answer SEE or FOLD."},
    {"id": "R11", "text": "When the Caller answers SEE after a RE-PUT, the stake is 4 and play follows."},
    {"id": "R12", "text": "When the Caller answers FOLD after a RE-PUT, the Responder scores 2 points and 1 hand won, and the hand ends without play."},
    {"id": "R13", "text": "When the Caller answers SEE after PASS then PUT, the stake is 2 and play follows."},
    {"id": "R14", "text": "When the Caller answers FOLD after PASS then PUT, the Responder scores 1 point and 1 hand won, and the hand ends without play."},
    {"id": "R15", "text": "When play happens, both players simultaneously choose an ordered list of 3 different cards from their 4 cards, and the face-up card may be used or left out."},
    {"id": "R16", "text": "Trick i compares the i-th cards of the two lists; the higher strength wins the trick, and equal strength ties it so no one gets it."},
    {"id": "R17", "text": "When a player wins at least 2 of the 3 tricks, that player scores the stake (1, 2 or 4) and 1 hand won."},
    {"id": "R18", "text": "When no player wins at least 2 tricks (e.g. 1-1 with a tie, 1 win and 2 ties, or 3 ties), nobody scores that hand."},
    {"id": "R19", "text": "After every hand, all calls, all 8 cards, the result, and both players' points and hands won are announced."},
    {"id": "R20", "text": "After hand 40 the match ends; more points wins, then more hands won breaks a tie, and if both are equal it is a draw."}
  ],
  "offers": [
    {"question": "Caller's call", "who": "the Caller", "options": "PUT, PASS"},
    {"question": "Responder's answer", "who": "the Responder", "options": "If caller_call = PUT: SEE, FOLD, RE-PUT. If caller_call = PASS: PUT, PASS."},
    {"question": "Caller's answer", "who": "the Caller, only when responder_answer is RE-PUT or PUT", "options": "SEE, FOLD"},
    {"question": "Play", "who": "both seats, only when folded = false", "options": "Each of the 24 ordered lists of 3 different cards from that seat's own 3 hand cards plus its face_up card."}
  ],
  "choices": [
    {"what": "Exactly 2 players (suggested 2)", "why": "The designer fixed the game at 2. The call structure (Caller/Responder alternating by hand) and the head-to-head tricks only work with two seats."},
    {"what": "Card coding as strength*10+suit", "why": "Strength is then floor(card/10), which makes trick comparison pure arithmetic while keeping 52 distinct cards."},
    {"what": "Play offered as one choice among 24 ordered triples", "why": "This makes the simultaneous secret ordered list a single poll with only legal options (3 different cards from own 4)."},
    {"what": "No free-text talk step", "why": "The rules contain no talk. With two players the calls themselves are the signalling and bluffing channel."},
    {"what": "Strategy check", "why": "A thoughtful player weighs the opponent's visible face-up card against their own, bluffs PUT or RE-PUT with weak hands, folds cheaply when outmatched, and orders cards to dodge the opponent's likely ordering (e.g. sacrificing a weak card against a strong one)."},
    {"what": "rank_by weight 1000", "why": "Hands won is at most 40, so points*1000 + hands_won ranks by points first, then by hands won."}
  ],
  "simplifications": [
    {"what": "The Caller and Responder are worked out from hand_number parity in each step's 'who'", "why": "The engine has no role-swap action; parity gives the same alternation."},
    {"what": "Conditional steps 4 and 5–7 are written as individual steps with when-conditions on caller_call, responder_answer and folded", "why": "The step list is flat, and per-step conditions reproduce the branching of the hand faithfully."},
    {"what": "Trick comparison between the two players' play lists uses a table-side comparison", "why": "Comparing one player's attribute with another's needs the documented workaround of copying values to the table."}
  ],
  "unsupported": []
}
```
````
