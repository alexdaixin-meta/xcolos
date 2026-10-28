# 23 spec

- time: 2026-10-28T06:13:33+00:00 (63.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 5cb75c72d763c575, reply sha256 e0fba30f6363b38e

## Sent

````
Game: Simultaneous Yaniv
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
CARDS
- Card values: Joker = 0, Ace = 1, 2 to 10 = face value, J/Q/K = 10.
- Every random card is drawn from a 54-card shoe: two 0s, four each of 1 to 9, and sixteen 10s.
- The shoe is full for every draw, so it never runs out.
- A hand is a list of values. hand_sum is the sum of the hand. hand_size is the number of cards in it.

PARAMETERS
call_limit = 7; asaf_penalty = 30; end_total = 100; max_rounds = 30.

SETUP
- Every total is 0.
- In one deal operation, each player is dealt 5 random cards, seen only by that player.
- Each player's hand_sum is computed. Each hand_size (5) is public.

EACH ROUND (rounds 1 to 30)
1. Options. Each player's first-choice options are listed in this order:
   - 'CALL', only if their current hand_sum is 7 or less;
   - then 'discard V' for each distinct value V in their hand, V ascending.
   The current hand_sum is the one computed at the end of the previous round (step 10, or after a redeal in step 4), or at setup in round 1.
2. Talk. Everyone writes one short message at the same time without seeing the others; all messages are then shown to everyone.
3. First choice. Everyone answers at the same time with one of their options. An invalid answer counts as follows:
   - CALL if the player's hand is empty;
   - otherwise 'discard H', where H is the highest value in their hand.
4. Showdown, if at least one player chose CALL:
   a. All hands are revealed. L = the lowest hand_sum among all players.
   b. A caller scores 0 if every other player's hand_sum is strictly greater than theirs. Otherwise (Asaf) they score hand_sum + 30.
   c. A non-caller scores 0 if their hand_sum equals L, otherwise their hand_sum.
   d. Each score is added to that player's total. Discards chosen this round are ignored.
   e. If any total is now 100 or more, or this is round 30, the game ends now.
   f. Otherwise, in one deal operation (the round's only random draw), every player's hand is replaced by 5 new random cards, seen only by that player. hand_sums are recomputed, hand_sizes reset to 5 publicly, and the round ends (steps 5 to 11 are skipped).
5. Discard, if no one called:
   - Each player removes every card of their chosen value V from their hand; the hand may become empty. These cards leave play.
   - Each player's V and the number of cards they shed are announced publicly. Each player's offer is one card of value V.
6. Claim options. Each player's options are listed in this order:
   - 'BLIND';
   - then 'value V' for each distinct value offered this round by at least one OTHER player, V ascending.
7. Claim choice. Everyone answers at the same time. An invalid answer counts as BLIND.
8. Resolve claims.
   - A claim on V succeeds if exactly one player claimed V; that player adds one card of value V to their hand.
   - If two or more players claimed the same V, all of them fail.
9. Blind draw. One random card value B is drawn (the round's only random draw).
   - Every player who chose BLIND or whose claim failed adds one card of value B to their hand.
   - Each such player is told B privately.
10. Announce.
   - Every hand_sum is recomputed; this is the value step 1 of the next round uses.
   - Announced publicly for each player: discarded value, number shed, claimed value, success or failure, whether they took the blind card, and new hand_size.
   - B and hand contents stay private.
11. Final showdown, if this is round 30 and no one called this round:
   - All hands are revealed.
   - Each player scores 0 if their hand_sum equals the lowest hand_sum, otherwise their hand_sum. This is added to their total.
   - The game ends.

How the winner is decided: The game ends either after a showdown that leaves any total at 100 or more, or after a showdown in round 30 (from a call or the final showdown). The player with the lowest total wins. If two or more players share the lowest total, the game is a draw among them.
````

## Reply

````
```json
{
  "name": "Simultaneous Yaniv",
  "summary": "Each round, every player secretly chooses at the same time to discard a set of equal cards or to call. Claims on cards others discarded collide, and showdowns score hand sums. The lowest total after a showdown that pushes anyone to 100, or after round 30, wins.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "call_limit": 7,
    "asaf_penalty": 30,
    "end_total": 100,
    "max_rounds": 30,
    "hand_cards": 5,
    "shoe_size": 54,
    "shoe_zeros": 2,
    "shoe_each_1_to_9": 4,
    "shoe_tens": 16,
    "joker_value": 0,
    "ace_value": 1,
    "face_value": 10,
    "caller_safe_score": 0,
    "lowest_noncaller_score": 0
  },
  "attributes": {
    "player": [
      {"key": "total", "type": "number", "visible": "public", "initial": 0, "meaning": "running penalty total; lowest wins", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "card values held, seen only by the owner", "observable": false},
      {"key": "hand_sum", "type": "number", "visible": "ally", "initial": 0, "meaning": "sum of hand, recomputed at setup, at a redeal, and at step 10 (announce); this is what decides whether CALL is offered", "observable": false},
      {"key": "hand_size", "type": "number", "visible": "public", "initial": 5, "meaning": "number of cards in hand", "observable": true},
      {"key": "revealed_hand", "type": "list", "visible": "public", "initial": [], "meaning": "copy of the hand shown to all at a showdown; empty otherwise", "observable": true},
      {"key": "first_choice", "type": "text", "visible": "public", "initial": "", "meaning": "this round's first choice: CALL or 'discard V', revealed after the simultaneous answer", "observable": false},
      {"key": "called", "type": "bool", "visible": "public", "initial": false, "meaning": "player chose CALL this round", "observable": true},
      {"key": "discard_value", "type": "number", "visible": "public", "initial": -1, "meaning": "value V discarded this round (-1 if none); also the value of the one card this player offers", "observable": true},
      {"key": "shed_count", "type": "number", "visible": "public", "initial": 0, "meaning": "number of cards removed this round", "observable": true},
      {"key": "claim", "type": "text", "visible": "public", "initial": "", "meaning": "claim choice: BLIND or 'value V'", "observable": true},
      {"key": "claim_success", "type": "bool", "visible": "public", "initial": false, "meaning": "claim on an offered value succeeded", "observable": true},
      {"key": "took_blind", "type": "bool", "visible": "public", "initial": false, "meaning": "player received the blind card this round", "observable": true},
      {"key": "blind_seen", "type": "number", "visible": "ally", "initial": -1, "meaning": "the blind value B, told privately to those who took it", "observable": false},
      {"key": "round_score", "type": "number", "visible": "public", "initial": 0, "meaning": "score added at the last showdown", "observable": true}
    ],
    "game": [
      {"key": "shoe", "type": "list", "visible": "none", "initial": "[0,0, 1x4, 2x4, 3x4, 4x4, 5x4, 6x4, 7x4, 8x4, 9x4, 10x16] (54 values)", "meaning": "the shoe; draws pick a random element and never remove it, so it is always full", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round number, 1 to 30", "observable": true},
      {"key": "any_call", "type": "bool", "visible": "public", "initial": false, "meaning": "at least one player chose CALL this round", "observable": true},
      {"key": "lowest_sum", "type": "number", "visible": "public", "initial": 0, "meaning": "L, the lowest hand_sum at a showdown", "observable": true},
      {"key": "lowest_count", "type": "number", "visible": "public", "initial": 0, "meaning": "number of players whose hand_sum equals L", "observable": false},
      {"key": "blind_value", "type": "number", "visible": "none", "initial": -1, "meaning": "B, this round's blind card value", "observable": false},
      {"key": "game_over", "type": "bool", "visible": "public", "initial": false, "meaning": "set true when a showdown happens in round 30", "observable": true}
    ]
  },
  "setup": [
    "Every player's total is set to 0 and game.round to 0.",
    "game.shoe is filled with the 54 values: two 0s, four each of 1 to 9, and sixteen 10s.",
    "In one deal operation, each player's hand receives 5 values drawn at random from game.shoe, without removing them from the shoe; each hand is visible only to its owner.",
    "Each player's hand_sum is computed as the sum of their hand, and hand_size is set to 5 publicly."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "game.round += 1; game.any_call = false; for each player: called = false, first_choice = '', discard_value = -1, shed_count = 0, claim = '', claim_success = false, took_blind = false, blind_seen = -1, revealed_hand = []"},
    {"action": "poll", "who": "all players", "answer": "short text message", "effect": "messages are gathered simultaneously and then broadcast to all as 'Seat {seat} says: {value}'"},
    {"action": "poll", "who": "all players", "answer": "one of: 'CALL' (only if hand_sum <= 7), then 'discard V' for each distinct V in hand, V ascending", "effect": "set first_choice. An invalid answer becomes CALL if hand is empty, otherwise 'discard H' with H = max(hand). called = (first_choice == 'CALL'); game.any_call = (count of players with called) >= 1; all first choices revealed publicly"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when game.any_call: revealed_hand = hand for every player (public); game.lowest_sum = min over players of hand_sum; game.lowest_count = count of players with hand_sum == game.lowest_sum"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when game.any_call: for each player, round_score = if called then (if hand_sum == game.lowest_sum and game.lowest_count == 1 then 0 else hand_sum + 30) else (if hand_sum == game.lowest_sum then 0 else hand_sum); total += round_score; if game.round == 30 then game.game_over = true; announce each round_score and total publicly; discards chosen this round are ignored"},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game if game.any_call and (max over players of total >= 100 or game.game_over)"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when game.any_call: in one deal operation, each hand is replaced by 5 random values from game.shoe (shoe not depleted), visible only to the owner; hand_sum = sum(hand); hand_size = 5 (public); revealed_hand = []. Steps 8 to 13 are skipped because each carries the condition not game.any_call"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when not game.any_call: V = value in first_choice; discard_value = V; shed_count = count of V in hand; remove every V from hand (the cards leave play); announce publicly each player's discard_value and shed_count. Each player offers one card of value discard_value"},
    {"action": "poll", "who": "all players", "answer": "one of: 'BLIND', then 'value V' for each distinct V offered as discard_value by at least one OTHER player, V ascending", "effect": "when not game.any_call: set claim; an invalid answer becomes 'BLIND'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when not game.any_call: for each player with claim 'value V': claim_success = (count of players with claim == 'value V') == 1; if claim_success, append V to hand"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when not game.any_call: game.blind_value = one random value from game.shoe (not removed); for each player with claim == 'BLIND' or not claim_success: append game.blind_value to hand, took_blind = true, blind_seen = game.blind_value (told privately)"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when not game.any_call: hand_sum = sum(hand); hand_size = length(hand); announce publicly for each player: discard_value, shed_count, claim, claim_success, took_blind, hand_size. B and hand contents stay private"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when not game.any_call and game.round == 30: revealed_hand = hand for all; game.lowest_sum = min hand_sum; round_score = if hand_sum == game.lowest_sum then 0 else hand_sum; total += round_score; game.game_over = true; announce publicly"},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game if game.game_over or max over players of total >= 100"}
  ],
  "ending": {
    "condition": "game.game_over == true or max over players of total >= 100",
    "rank_by": "0 - you.total",
    "decided_by": "Each player's standing is their total, and lower is better. The player with the lowest total wins, and players tied at the lowest total share the win (a draw among them)."
  },
  "rules": [
    {"id": "R1", "text": "Card values are Joker = 0, Ace = 1, 2 to 10 at face value, and J/Q/K = 10. The shoe holds two 0s, four each of 1 to 9, and sixteen 10s (54 cards)."},
    {"id": "R2", "text": "Every random draw picks a value from the full 54-card shoe; the shoe never shrinks or runs out."},
    {"id": "R3", "text": "At setup, every total is 0, each player is dealt 5 private cards, hand_sum is their sum, and hand_size 5 is public."},
    {"id": "R4", "text": "When a player's current hand_sum is 7 or less, 'CALL' is offered first; otherwise it is not offered."},
    {"id": "R5", "text": "A player is offered 'discard V' for each distinct value V in their hand, in ascending order."},
    {"id": "R6", "text": "Before the first choice, every player writes one message simultaneously, and all messages are then shown to everyone."},
    {"id": "R7", "text": "First choices are made simultaneously. An invalid answer becomes CALL if the hand is empty, otherwise 'discard H' where H is the highest value in the hand."},
    {"id": "R8", "text": "When at least one player calls, all hands are revealed and L is the lowest hand_sum."},
    {"id": "R9", "text": "When a caller's hand_sum is strictly lower than every other player's, the caller scores 0."},
    {"id": "R10", "text": "When a caller's hand_sum is tied with or above another player's, the caller scores hand_sum + 30 (Asaf); for example, a caller with 5 tied by another 5 scores 35."},
    {"id": "R11", "text": "When a non-caller's hand_sum equals L, they score 0; otherwise they score their hand_sum."},
    {"id": "R12", "text": "When anyone calls, discards chosen that round are ignored."},
    {"id": "R13", "text": "When a showdown leaves any total at 100 or more, the game ends."},
    {"id": "R14", "text": "When a call happens in round 30, the game ends after that showdown."},
    {"id": "R15", "text": "When a showdown does not end the game, every hand is replaced by 5 new random cards, hand_size is reset to 5, and the round ends with no discard, claim or blind draw."},
    {"id": "R16", "text": "When no one calls, each player removes every card of their chosen value V; the hand may become empty."},
    {"id": "R17", "text": "When no one calls, each player's V and the number of cards shed are announced publicly."},
    {"id": "R18", "text": "Claim options are 'BLIND' followed by 'value V' for each distinct V offered by at least one other player, in ascending order; a player is never offered only their own offered value."},
    {"id": "R19", "text": "Claims are made simultaneously, and an invalid claim counts as BLIND."},
    {"id": "R20", "text": "When exactly one player claims value V, that player adds one card of value V to their hand."},
    {"id": "R21", "text": "When two or more players claim the same V, all of their claims fail."},
    {"id": "R22", "text": "One blind value B is drawn per no-call round; every player who chose BLIND or whose claim failed adds one card of value B and is told B privately."},
    {"id": "R23", "text": "After claims, hand_sum and hand_size are recomputed, and each player's discarded value, number shed, claim, success, whether they took the blind card, and hand_size are announced; B and hands stay private."},
    {"id": "R24", "text": "When round 30 ends with no call, all hands are revealed, each player scores 0 if their hand_sum equals the lowest hand_sum and otherwise their hand_sum, and the game ends."},
    {"id": "R25", "text": "When the game ends, the lowest total wins, and players tied at the lowest total share the win."}
  ],
  "offers": [
    {"question": "Talk message", "who": "all players", "options": "any short text"},
    {"question": "First choice", "who": "all players", "options": "a seat with hand_sum <= 7: 'CALL', then 'discard V' for each distinct value in its hand, ascending; a seat with hand_sum > 7: only the 'discard V' options; a seat with an empty hand: only 'CALL'"},
    {"question": "Claim choice", "who": "all players (only in rounds with no call)", "options": "'BLIND', then 'value V' for each distinct discard_value offered by at least one other seat, ascending; a value offered only by this seat is not listed"}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer suggested 4, which is kept. Claim collisions and Asaf ties need at least 3 rivals' worth of interaction, and above 5 the claim list and the announcements grow long while one player's choice matters little."},
    {"what": "Talk is a simultaneous poll broadcast to all", "why": "The rules say messages are written at the same time. Talk earns its place: players disagree over who claims which offered value, so announcing a claim can deter rivals or bait a collision."},
    {"what": "Ranking is 0 - total", "why": "The engine ranks highest first, and the lowest total wins."},
    {"what": "Asaf is tested as hand_sum == L and lowest_count == 1", "why": "This is an arithmetic form of 'every other hand_sum is strictly greater', using table attributes because players cannot be compared directly."},
    {"what": "game_over flag", "why": "This records the end that comes from a showdown in round 30, so a single check covers both endings."},
    {"what": "Strategy", "why": "A thoughtful player times a call against the public hand_sizes and the claims seen, avoids claiming values that others likely want, and uses talk to steer or bluff about claims."}
  ],
  "simplifications": [
    {"what": "Cards are stored as values only, with no suits or ranks", "why": "Only values matter in these rules; J, Q and K are all 10 and the Joker is 0."},
    {"what": "The skip of steps 5 to 11 after a call is done by putting the condition 'not game.any_call' on each later step", "why": "The step list is flat, but per-step conditions express the same skip exactly."},
    {"what": "Draws pick from game.shoe without removing the value", "why": "The source states the shoe is full for every draw."}
  ],
  "unsupported": []
}
```
````
