# 05 spec

- time: 2026-10-28T03:56:21+00:00 (64.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 3b66ce2b42c7cab5, reply sha256 5a21aa412f0d555b

## Sent

````
Game: Three Up: Even Rounds
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
CARDS. There are 30 cards: three copies each of ranks 1 to 9 (27 cards) and three Clear cards.

SETUP.
1. Seat the three players in a random order called First, Second and Third. Turn order is First, Second, Third in every round.
2. Make three separately shuffled stacks: Low (all 1s, 2s and 3s; 9 cards), Mid (all 4s, 5s and 6s; 9 cards) and High (all 7s, 8s and 9s; 9 cards).
3. Deal each player 3 cards from Low, 3 from Mid, 3 from High and 1 Clear, so each player has 10 cards. Every card is dealt.
4. Each player privately looks at their cards.
5. At the same moment, each player chooses exactly 3 of their cards to be their Up pile. All Up piles are then revealed.
6. A player's remaining 7 cards are their Hand, which only that player sees.
7. The discard Pile starts empty, with a run count of 0. Each player's 'picked up' count starts at 0.

PUBLIC INFORMATION. At all times everyone can see:
- every card on the Pile, its top rank and its run count (how many cards of the top rank lie on top of the Pile in a row);
- every Up pile;
- each player's number of Hand cards;
- each player's picked-up count;
- the full history of plays and pickups.

EACH ROUND (at most 40 rounds).
(a) TALK. Every player writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Messages bind no one.
(b) TURNS. First, then Second, then Third each take one turn as described below. A player who already has no cards in Hand or Up pile skips their turn.
(c) END CHECK. After Third's turn, look at every player who now has no cards in Hand or Up pile.
- If exactly one player is out of cards, that player wins.
- If two or three players are out of cards, the one among them with the lowest picked-up count wins. If they are tied on that count, the game is a draw.
- If nobody is out of cards, play continues.
(d) ROUND CAP. If round 40 ends with nobody out of cards, the player with the fewest cards (Hand plus Up pile) wins. A tie for fewest cards is broken by the lowest picked-up count. If players are still tied, the game is a draw.

A TURN. The player chooses one of two actions.
- PLAY: choose one rank and play one or more cards of that rank together, all from the same source.
  - The source must be your Hand while your Hand has any cards. You play from your Up pile only once your Hand is empty.
  - A numbered play is legal only if the Pile is empty or the rank is equal to or higher than the Pile's top rank.
  - A Clear is always legal and is played on its own.
- PICK UP: take every card on the Pile into your Hand, and add the number of cards taken to your picked-up count. The Pile becomes empty with a run count of 0. You may pick up even when you have a legal play. Picking up an empty Pile does nothing.
- An illegal or unreadable choice counts as PICK UP.

RESOLVING A PLAY.
- Numbered cards go on top of the Pile. If their rank equals the previous top rank, the run count rises by the number of cards played; otherwise the run count becomes the number of cards played.
- If the run count reaches 3 or more, the Pile is cleared: its cards are removed from the game, it becomes empty, and the run count is 0.
- A played Clear and the whole Pile are removed from the game, leaving the Pile empty.
- The turn then ends, and the next player acts on whatever Pile remains. An empty Pile accepts any card.

How the winner is decided: At the end of each round, if exactly one player has no cards left in Hand or Up pile, that player wins. If several players emptied by the end of the same round, the one with the lowest total of cards picked up during the game wins; if they are tied on that total, the game is a draw. If round 40 ends with nobody out of cards, the player with the fewest remaining cards wins, ties are broken by the lowest picked-up total, and a remaining tie is a draw.
````

## Reply

````
```json
{
  "name": "Three Up: Even Rounds",
  "summary": "A three-player shedding game: each round everyone talks at the same time, then First, Second and Third each play cards of one rank at or above the Pile's top rank, play a Clear, or pick up the Pile; the first to empty Hand and Up pile wins, and the lowest picked-up total breaks ties.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "total_cards": 30,
    "lowest_rank": 1,
    "highest_rank": 9,
    "copies_per_rank": 3,
    "clear_cards": 3,
    "stack_size": 9,
    "low_ranks_max": 3,
    "mid_ranks_max": 6,
    "high_ranks_max": 9,
    "deal_per_stack": 3,
    "clear_per_player": 1,
    "cards_per_player": 10,
    "up_pile_size": 3,
    "hand_after_up": 7,
    "run_to_clear": 3,
    "max_rounds": 40,
    "rank_out_weight": 1000000,
    "rank_cards_weight": 10000
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The player's Hand cards, each written as '1'..'9' or 'C' for a Clear. Only the owner sees them.", "observable": false},
      {"key": "up_choice", "type": "list", "visible": "ally", "initial": [], "meaning": "The cards picked for the Up pile during the simultaneous setup choice, held privately until every player has chosen.", "observable": false},
      {"key": "up_pile", "type": "list", "visible": "public", "initial": [], "meaning": "The player's revealed Up pile of 3 cards.", "observable": true},
      {"key": "hand_count", "type": "number", "visible": "public", "initial": 0, "meaning": "The number of cards in Hand.", "observable": true},
      {"key": "up_count", "type": "number", "visible": "public", "initial": 0, "meaning": "The number of cards in the Up pile.", "observable": true},
      {"key": "cards_left", "type": "number", "visible": "public", "initial": 0, "meaning": "hand_count + up_count.", "observable": true},
      {"key": "picked_up", "type": "number", "visible": "public", "initial": 0, "meaning": "The total number of cards this player has taken from the Pile during the game.", "observable": true},
      {"key": "out", "type": "bool", "visible": "public", "initial": false, "meaning": "True when cards_left is 0. An out player skips their turns.", "observable": true}
    ],
    "game": [
      {"key": "low_stack", "type": "list", "visible": "none", "initial": ["1","1","1","2","2","2","3","3","3"], "meaning": "The shuffled Low stack.", "observable": false},
      {"key": "mid_stack", "type": "list", "visible": "none", "initial": ["4","4","4","5","5","5","6","6","6"], "meaning": "The shuffled Mid stack.", "observable": false},
      {"key": "high_stack", "type": "list", "visible": "none", "initial": ["7","7","7","8","8","8","9","9","9"], "meaning": "The shuffled High stack.", "observable": false},
      {"key": "clear_stack", "type": "list", "visible": "none", "initial": ["C","C","C"], "meaning": "The three Clear cards before the deal.", "observable": false},
      {"key": "pile", "type": "list", "visible": "public", "initial": [], "meaning": "The discard Pile, bottom to top.", "observable": true},
      {"key": "top_rank", "type": "number", "visible": "public", "initial": 0, "meaning": "The rank of the Pile's top card, or 0 when the Pile is empty.", "observable": true},
      {"key": "run_count", "type": "number", "visible": "public", "initial": 0, "meaning": "How many cards of the top rank lie in a row on top of the Pile.", "observable": true},
      {"key": "removed", "type": "list", "visible": "public", "initial": [], "meaning": "Cards removed from the game by run clears and Clears.", "observable": false},
      {"key": "history", "type": "list", "visible": "public", "initial": [], "meaning": "The full public log of plays and pickups.", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "The current round number.", "observable": true},
      {"key": "players_out", "type": "number", "visible": "public", "initial": 0, "meaning": "The number of players with out = true.", "observable": true}
    ]
  },
  "setup": [
    "Seats are assigned in random (seeded) order. Seat 1 is First, seat 2 is Second and seat 3 is Third, and turn order is seat 1, 2, 3 in every round.",
    "low_stack, mid_stack and high_stack are each shuffled separately. Drawing at random from a stack is the shuffle.",
    "Each player draws 3 cards at random from low_stack, 3 from mid_stack and 3 from high_stack, and takes 1 card from clear_stack. Each card is appended to that player's hand and removed from its stack. Every stack ends empty and each hand holds 10 cards.",
    "Each player privately sees their own hand.",
    "Up pile selection, done simultaneously by poll: three successive polls ask every player at once to choose one card from their own hand. Each chosen card moves from hand to up_choice (visible only to the owner), so nobody sees another player's choice until all three picks are made.",
    "When every player has 3 cards in up_choice, each up_choice is copied to up_pile (public) and emptied. All Up piles are announced to everyone.",
    "Every player gets hand_count = 7, up_count = 3, cards_left = 10, picked_up = 0 and out = false.",
    "The table starts with pile = [], top_rank = 0, run_count = 0, removed = [], round = 0 and players_out = 0."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; announce the round number, pile, top_rank, run_count, every up_pile, hand_count and picked_up."},
    {"action": "poll", "who": "all players", "answer": "short text (one message)", "effect": "Every message is shown to everyone at once: broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. No state changes and nothing binds."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player receives their own hand, plus the public pile, top_rank, run_count, up_piles, hand_counts and picked_up counts."},
    {"action": "ask", "who": "seat 1 (First), when out = false", "answer": "one choice from the offered list: 'pick up', 'play Clear' (only if the source holds a C), or 'play K x rank R' for each rank R held in the source with R >= top_rank (any rank if the pile is empty) and each K from 1 to the number of R cards held. The source is hand if hand_count > 0, otherwise up_pile.", "effect": "Records the chosen action. An illegal or unreadable answer counts as 'pick up'."},
    {"action": "update", "who": "seat 1 (First), when out = false", "answer": null, "effect": "PICK UP: append every pile card to hand; picked_up += len(pile); pile = []; top_rank = 0; run_count = 0. PLAY K x R: remove K R cards from the source and append them to pile; if R == top_rank then run_count += K, else run_count = K; top_rank = R; if run_count >= 3, move all pile cards to removed, set pile = [], top_rank = 0, run_count = 0. PLAY Clear: move the C and all pile cards to removed; pile = []; top_rank = 0; run_count = 0. Then recompute hand_count, up_count and cards_left = hand_count + up_count; out = (cards_left == 0); append the action to history; announce it."},
    {"action": "ask", "who": "seat 2 (Second), when out = false", "answer": "as for seat 1, against the current pile", "effect": "Records the chosen action. An illegal or unreadable answer counts as 'pick up'."},
    {"action": "update", "who": "seat 2 (Second), when out = false", "answer": null, "effect": "Resolved exactly as for seat 1."},
    {"action": "ask", "who": "seat 3 (Third), when out = false", "answer": "as for seat 1, against the current pile", "effect": "Records the chosen action. An illegal or unreadable answer counts as 'pick up'."},
    {"action": "update", "who": "seat 3 (Third), when out = false", "answer": null, "effect": "Resolved exactly as for seat 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "players_out = the number of players with out = true."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if players_out >= 1 or round >= 40; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "players_out >= 1 or round >= 40 (checked only after seat 3's turn)",
    "rank_by": "you.out * 1000000 - you.cards_left * 10000 - you.picked_up",
    "decided_by": "If any player is out at the end of the round, only the out players can win, and among them the lowest picked_up wins; out players tied on picked_up share the result (a draw). If round 40 ends with nobody out, the fewest cards_left wins, then the lowest picked_up, and players still tied share the result (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When the game is set up, there are 30 cards: three each of ranks 1 to 9 and three Clears."},
    {"id": "R2", "text": "When cards are dealt, each player gets 3 cards from Low (ranks 1-3), 3 from Mid (4-6), 3 from High (7-9) and 1 Clear, 10 cards in all, and every stack ends empty."},
    {"id": "R3", "text": "When Up piles are chosen, every player chooses exactly 3 of their own cards simultaneously; all Up piles are then made public and each hand holds 7 cards."},
    {"id": "R4", "text": "When setup ends, pile is empty, top_rank = 0, run_count = 0 and every picked_up = 0."},
    {"id": "R5", "text": "When a round starts, every player writes one message at the same time, and all messages are shown to everyone only after all are in."},
    {"id": "R6", "text": "When it is a player's turn, seats act in order 1 (First), 2 (Second), 3 (Third), and a player with cards_left = 0 skips the turn."},
    {"id": "R7", "text": "When a player has hand_count > 0, they may play only from hand; when hand_count = 0, they play from up_pile."},
    {"id": "R8", "text": "When a player plays numbered cards, all cards are of one rank and from one source, and the play is legal only if the pile is empty or the rank >= top_rank (e.g., on top_rank 5, a 5 or 9 is legal and a 4 is not)."},
    {"id": "R9", "text": "When a player plays K cards of rank R equal to top_rank, run_count increases by K; when R differs from top_rank, run_count becomes K and top_rank becomes R."},
    {"id": "R10", "text": "When run_count reaches 3 or more, all pile cards go to removed, the pile empties, and top_rank and run_count become 0."},
    {"id": "R11", "text": "When a player plays a Clear, it is played alone and is always legal; the Clear and the whole pile go to removed, and top_rank and run_count become 0."},
    {"id": "R12", "text": "When a player picks up, every pile card moves to their hand, picked_up increases by the number of cards taken, and pile, top_rank and run_count reset to empty/0; picking up an empty pile changes nothing."},
    {"id": "R13", "text": "When a player may legally play, they may still choose to pick up."},
    {"id": "R14", "text": "When a player's answer is illegal or unreadable, it is resolved as a pick up."},
    {"id": "R15", "text": "When seat 3's turn ends and exactly one player has cards_left = 0, that player wins."},
    {"id": "R16", "text": "When seat 3's turn ends and two or three players have cards_left = 0, the one among them with the lowest picked_up wins, and a tie on picked_up is a draw between them."},
    {"id": "R17", "text": "When a player empties mid-round, the round still continues to seat 3 before any end check."},
    {"id": "R18", "text": "When round 40 ends with nobody out, the fewest cards_left wins, ties are broken by the lowest picked_up, and a remaining tie is a draw."}
  ],
  "offers": [
    {"question": "Talk message each round", "who": "all players (including out players)", "options": "One short free-text message."},
    {"question": "Up pile pick (setup, three simultaneous polls)", "who": "every seat", "options": "Any one card still in their own hand."},
    {"question": "Turn action", "who": "the seat whose turn it is, if out = false; an out seat is not asked", "options": "Always 'pick up'. 'play Clear' if the source (hand if non-empty, else up_pile) holds a C. 'play K x rank R' for each rank R in the source with R >= top_rank (any rank when the pile is empty), with K from 1 to the count of R cards in that source. Cards from the other source are never offered."}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed the table at three: three ranked seats in a turn order, and an end check written for one, two or three emptied players."},
    {"what": "The talk round is a simultaneous poll with broadcast", "why": "The rules say messages are written at the same moment. Talk earns its place because players want opposite things (each wants the others to pick up) and can try to coax a rival into taking the Pile."},
    {"what": "Random seating maps to seat numbers 1, 2, 3 as First, Second, Third", "why": "The engine's seeded random seating gives the random order the rules ask for."},
    {"what": "Up pile chosen by three successive simultaneous polls into a private up_choice list, revealed afterwards", "why": "A single answer is one choice; three picks kept hidden until all are done keep the choice simultaneous."},
    {"what": "rank_by = out*1000000 - cards_left*10000 - picked_up", "why": "Out players rank above all others, then fewer cards, then fewer picked up. picked_up cannot reach 10000 in 40 rounds (at most 40 pickups of 27 cards), so the weights never overlap."},
    {"what": "Cards are written as text '1'..'9' and 'C'; top_rank is 0 for an empty pile", "why": "Gives the legality check a simple arithmetic comparison."}
  ],
  "simplifications": [
    {"what": "A draw is represented as all tied top players sharing the win", "why": "The engine has no separate draw; players level at the top share the result, and the other players still lose."},
    {"what": "Each seat's turn is written as its own ask plus update steps, in fixed seat order", "why": "Each play must resolve before the next seat chooses, against the current pile."}
  ],
  "unsupported": []
}
```
````
