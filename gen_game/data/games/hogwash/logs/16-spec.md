# 16 spec

- time: 2026-10-28T04:02:03+00:00 (51.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 b91824918b244112, reply sha256 9fd12253bc85c632

## Sent

````
Game: Hogwash: Six Ranks
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP. The deck has 24 cards: ranks 1 to 6, four copies of each. Shuffle and deal 8 cards to each of seats 1, 2 and 3. Hands are private. Everyone always knows every hand size and the pile size. The central pile starts empty; its cards are face down. Each player has two public counters starting at 0: CATCHES (correct challenges) and CAUGHT (times caught bluffing).

ROUNDS. The game lasts exactly 24 rounds. In round r the active player is seat ((r-1) mod 3)+1 and the required rank is ((r-1) mod 6)+1. As a result, seat 1 always faces ranks 1 and 4, seat 2 faces ranks 2 and 5, and seat 3 faces ranks 3 and 6. Each seat is active 8 times.

EACH ROUND:
1. Announce the round, the active player and the required rank.
2. If the active player holds 0 cards, they skip; go to step 8. Otherwise the active player privately chooses k from 1 to 4. If k exceeds their hand size, k becomes their hand size. They may add one short public statement, which may be untrue.
3. The engine moves k cards from the active player's hand onto the top of the pile. It takes cards of the required rank first, up to k. If more are needed, it takes cards of the next rank up, then the next, counting 6 as followed by 1. The play is TRUE if all k cards are the required rank; otherwise it is a BLUFF. This is recorded privately.
4. Announce: 'Seat X claims k cards of rank R', plus the statement.
5. Simultaneous poll: each of the two other players secretly chooses Trust or Challenge. The choices are revealed together.
6. If anyone challenged, reveal the k played cards to all.
   (a) If the play was a BLUFF: the active player takes the entire pile into their hand, and the pile becomes empty. The active player's CAUGHT increases by 1. Each challenger's CATCHES increases by 1.
   (b) If the play was TRUE and there was one challenger: that challenger takes the entire pile into their hand.
   (c) If the play was TRUE and there were two challengers: shuffle the pile. Each challenger takes half of it, rounded down. If one card remains, it is removed from the game face down. The pile becomes empty.
7. If both players chose Trust, nothing happens. The cards stay face down in the pile, true or not.
8. Announce every player's hand size, the pile size and all CATCHES and CAUGHT counters.
9. If round 24 has been played, the game ends.

A player holding 0 cards still answers every poll. Trusting can never give them cards.

How the winner is decided: After round 24, the player holding the fewest cards wins. If several players tie for fewest, the one with the most CATCHES wins. If still tied, the one with the fewest CAUGHT wins. If still tied, the game is a draw among those players.
````

## Reply

````
```json
{
  "name": "Hogwash: Six Ranks",
  "summary": "Three players take turns face-down dumping 1 to 4 cards that they claim are the required rank. The others secretly trust or challenge, and whoever holds the fewest cards after 24 rounds wins.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "deck_size": 24,
    "num_ranks": 6,
    "copies_per_rank": 4,
    "hand_size_initial": 8,
    "num_seats": 3,
    "total_rounds": 24,
    "k_min": 1,
    "k_max": 4,
    "turns_per_seat": 8,
    "catches_initial": 0,
    "caught_initial": 0,
    "pile_initial_size": 0,
    "rank_weight_hand": 10000,
    "rank_weight_catches": 100,
    "rank_weight_caught": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": "8 cards dealt from deck", "meaning": "the ranks of the cards this player holds", "observable": false},
      {"key": "hand_size", "type": "number", "visible": "public", "initial": 8, "meaning": "number of cards in hand, kept equal to the length of hand", "observable": true},
      {"key": "catches", "type": "number", "visible": "public", "initial": 0, "meaning": "CATCHES: challenges this player made against a bluff", "observable": true},
      {"key": "caught", "type": "number", "visible": "public", "initial": 0, "meaning": "CAUGHT: times this player was caught bluffing", "observable": true},
      {"key": "response", "type": "text", "visible": "ally", "initial": "", "meaning": "this round's Trust or Challenge answer, revealed to all after the poll", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "24 cards: ranks 1-6, four of each", "meaning": "undealt cards, empty after the deal", "observable": false},
      {"key": "pile", "type": "list", "visible": "none", "initial": [], "meaning": "the face-down central pile", "observable": false},
      {"key": "pile_size", "type": "number", "visible": "public", "initial": 0, "meaning": "number of cards in the pile", "observable": true},
      {"key": "removed", "type": "list", "visible": "none", "initial": [], "meaning": "cards removed from the game face down", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round number r", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "((round-1) mod 3)+1", "observable": false},
      {"key": "required_rank", "type": "number", "visible": "public", "initial": 0, "meaning": "((round-1) mod 6)+1", "observable": false},
      {"key": "skipped", "type": "bool", "visible": "public", "initial": false, "meaning": "true when the active player held 0 cards this round", "observable": false},
      {"key": "k", "type": "number", "visible": "public", "initial": 0, "meaning": "number of cards played this round, after clamping to hand size", "observable": false},
      {"key": "statement", "type": "text", "visible": "public", "initial": "", "meaning": "the active player's optional public statement", "observable": false},
      {"key": "played", "type": "list", "visible": "none", "initial": [], "meaning": "the k cards played this round, revealed to all if challenged", "observable": false},
      {"key": "play_true", "type": "bool", "visible": "none", "initial": false, "meaning": "true if all k played cards equal required_rank, otherwise a bluff", "observable": false},
      {"key": "challengers", "type": "number", "visible": "public", "initial": 0, "meaning": "count of non-active players who answered Challenge this round", "observable": false}
    ]
  },
  "setup": [
    "Build the deck list with 24 cards: ranks 1 to 6, four copies of each.",
    "Deal 8 cards at random from deck into the hand of each of seats 1, 2 and 3, removing each card from deck; set each hand_size to 8.",
    "Set pile to empty, pile_size to 0, and every player's catches and caught to 0.",
    "Sync each player's own hand to them; hand sizes, pile size and counters are public."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1; active_seat = ((round-1) mod 3)+1; required_rank = ((round-1) mod 6)+1; skipped = (hand_size of active_seat == 0); k = 0; statement = ''; played = []; challengers = 0; every response = ''"},
    {"action": "tell", "who": "all players", "answer": null, "effect": "announce 'Round {round}: Seat {active_seat} must play rank {required_rank}' (plus 'and skips, holding 0 cards' when skipped)"},
    {"action": "sync", "who": "all players", "answer": null, "effect": "each player sees their own hand"},
    {"action": "ask", "who": "seat active_seat, when skipped is false", "answer": "a whole number from 1 to 4", "effect": "k = min(answer, hand_size of active seat)"},
    {"action": "ask", "who": "seat active_seat, when skipped is false", "answer": "short text, may be empty, may be untrue", "effect": "statement = answer"},
    {"action": "update", "who": "table, when skipped is false", "answer": null, "effect": "move k cards from the active player's hand to played and onto the top of pile: first cards equal to required_rank, then rank required_rank+1, and so on, wrapping 6 to 1, until k are taken; hand_size -= k; pile_size += k; play_true = (count of cards in played equal to required_rank == k)"},
    {"action": "tell", "who": "all players, when skipped is false", "answer": null, "effect": "announce 'Seat {active_seat} claims {k} cards of rank {required_rank}. Statement: {statement}'"},
    {"action": "poll", "who": "every seat except active_seat, simultaneously, when skipped is false (including players holding 0 cards)", "answer": "one of: Trust, Challenge", "effect": "response = answer for each polled player; then reveal all responses together; challengers = count of polled players with response == Challenge"},
    {"action": "tell", "who": "all players, when skipped is false and challengers > 0", "answer": null, "effect": "reveal the contents of played to everyone"},
    {"action": "update", "who": "table, when skipped is false and challengers > 0 and play_true is false", "answer": null, "effect": "append all of pile to the active player's hand; pile = []; pile_size = 0; active player's caught += 1; each player with response == Challenge: catches += 1; refresh hand_size"},
    {"action": "update", "who": "table, when skipped is false and challengers == 1 and play_true is true", "answer": null, "effect": "append all of pile to the hand of the player with response == Challenge; pile = []; pile_size = 0; refresh hand_size"},
    {"action": "update", "who": "table, when skipped is false and challengers == 2 and play_true is true", "answer": null, "effect": "shuffle pile; each challenger draws floor(pile_size/2) cards at random from pile into hand; if 1 card remains, move it to removed; pile = []; pile_size = 0; refresh hand_size"},
    {"action": "tell", "who": "all players", "answer": null, "effect": "announce every player's hand_size, pile_size, and every player's catches and caught"},
    {"action": "check", "who": "table", "answer": null, "effect": "if round >= 24, end the game; otherwise continue"}
  ],
  "ending": {
    "condition": "round >= 24",
    "rank_by": "0 - you.hand_size * 10000 + you.catches * 100 - you.caught",
    "decided_by": "Fewest cards in hand wins. Ties go to the most CATCHES, then to the fewest CAUGHT. Players still level share the win, which is the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, the deck holds 24 cards (ranks 1-6, four of each) and each of seats 1, 2 and 3 is dealt 8 cards into hand, leaving deck empty."},
    {"id": "R2", "text": "When the game starts, pile_size is 0 and every player's catches and caught are 0."},
    {"id": "R3", "text": "When round r begins, then active_seat = ((r-1) mod 3)+1 and required_rank = ((r-1) mod 6)+1; e.g. round 4 has seat 1 and rank 4, round 6 has seat 3 and rank 6."},
    {"id": "R4", "text": "When the active player holds 0 cards, then they are not asked for k, no cards move, no poll is held, and the round goes straight to the announcement."},
    {"id": "R5", "text": "When the active player chooses k greater than their hand size, then k becomes their hand size (e.g. choosing 4 with 2 cards plays 2)."},
    {"id": "R6", "text": "When k cards are played, then cards of the required rank are taken first, then the next rank up, wrapping 6 to 1; e.g. required rank 5, k=3, hand {5,6,1,2} plays 5,6,1."},
    {"id": "R7", "text": "When all k played cards equal the required rank, then the play is TRUE; otherwise it is a BLUFF."},
    {"id": "R8", "text": "When cards are played, then the active player's hand_size falls by k and pile_size rises by k."},
    {"id": "R9", "text": "When the claim is announced, then it reads 'Seat X claims k cards of rank R' plus the active player's statement."},
    {"id": "R10", "text": "When the claim is made, then exactly the two non-active seats are polled simultaneously with options Trust and Challenge, including a player holding 0 cards."},
    {"id": "R11", "text": "When at least one player challenges, then the k played cards are revealed to all players."},
    {"id": "R12", "text": "When a BLUFF is challenged, then the active player adds the whole pile to their hand, pile_size becomes 0, the active player's caught rises by 1, and each challenger's catches rises by 1."},
    {"id": "R13", "text": "When a TRUE play is challenged by exactly one player, then that challenger adds the whole pile to their hand and pile_size becomes 0; no catches or caught change."},
    {"id": "R14", "text": "When a TRUE play is challenged by both players, then each challenger gets floor(pile_size/2) random pile cards, any 1 leftover card is removed from the game, and pile_size becomes 0 (e.g. pile 7: each gets 3 and 1 is removed)."},
    {"id": "R15", "text": "When both players choose Trust, then no hand changes and the played cards stay in the pile face down."},
    {"id": "R16", "text": "When a player chooses Trust, then that choice never adds cards to their hand."},
    {"id": "R17", "text": "When a round ends, then every hand_size, pile_size, and all catches and caught are announced."},
    {"id": "R18", "text": "When round 24 has been played, then the game ends."},
    {"id": "R19", "text": "When the game ends, then the player with the fewest cards wins; ties go to most catches, then fewest caught, and players still tied share the win."}
  ],
  "offers": [
    {"question": "How many cards (k) do you play?", "who": "the active seat, only when it holds at least 1 card", "options": "a whole number 1 to 4 (clamped to hand size afterwards); seats that are not active are not asked"},
    {"question": "Optional public statement", "who": "the active seat, only when it holds at least 1 card", "options": "short free text, may be empty or untrue"},
    {"question": "Trust or Challenge the claim", "who": "the two seats other than the active seat, whatever their hand size", "options": "Trust, Challenge; the active seat is not asked"}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed the table at 3. The rank schedule (each seat facing two fixed ranks, 8 turns each) and the split rule for two challengers depend on exactly 3 seats, so neither the minimum nor the maximum can move."},
    {"what": "No all-players talk poll before the Trust/Challenge poll", "why": "The source gives only the active player one public statement. Adding free talk would add a mechanic; the bluffing lives in the claim and the statement."},
    {"what": "The statement is a separate ask after k", "why": "Each question takes one answer type, so the number and the text are asked in two steps by the same seat."},
    {"what": "Ranking expression -hand_size*10000 + catches*100 - caught", "why": "Catches are at most 24 (times 100 is under 10000) and caught is at most 8 (under 100), so the weights reproduce the strict tie-break order: fewest cards, then most catches, then fewest caught."},
    {"what": "Strategy at the table", "why": "A thoughtful player tracks how many of each rank have been revealed, picked up or must still be out, judges whether a claim of k is plausible, and weighs taking the pile against letting a rival shed cards. They also choose when an honest play invites a costly challenge, and use the statement to mislead."}
  ],
  "simplifications": [
    {"what": "The k cards are chosen by a fixed engine rule rather than by the player", "why": "The source already specifies this; it is carried out as remove/append operations on hand, played and pile."},
    {"what": "Shuffling and splitting the pile are random draws from the pile list", "why": "The engine shuffles by drawing at random, which gives the same result."},
    {"what": "The draw among tied players is a shared win", "why": "The engine has no separate draw; players level at the top share the win."}
  ],
  "unsupported": []
}
```
````
