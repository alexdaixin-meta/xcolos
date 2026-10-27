# 20 spec

- time: 2026-10-27T21:47:41+00:00 (58.3s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 aec23274eb2904cf, reply sha256 e4fef4839c38f7f0

## Sent

````
Game: 11 Nimmt: Two Hot Piles
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
CARDS. The deck has N cards numbered 1 to N: N = 30 with 3 players, N = 40 with 4 players.

OX-HEADS. Cards 11, 22 and 33 carry 3 ox-heads. Every other multiple of 5 (5, 10, 15, 20, 25, 30, 35, 40) carries 2. All other cards carry 1.

SETUP.
- Shuffle once.
- Deal each player a private hand of H cards: H = 9 with 3 players, H = 8 with 4 players.
- Turn the next two cards face up. They start Pile A and Pile B, each of size 1.
- The rest (1 card with 3 players, 6 with 4) are set aside unseen and take no part in the game.
- Everyone starts with penalty 0 and bulls 0.

INFORMATION. You see only your own hand. Everyone sees both piles (their cards, top card, size and ox total), every card played and every take, and all penalties and bulls.

FITTING. A card c fits a pile with top card t if d = (c - t) mod N is between 1 and 10 inclusive. Example with N = 30: on a top of 25, the cards 26 to 30 and 1 to 5 fit.

ROOM. A pile has room if it has fewer than 5 cards.

PLACEMENT. A placement is a card from your hand that fits a pile with room.

ROUNDS. The game lasts exactly H rounds. In round r the seats act one after another, starting with seat ((r - 1) mod number of players) + 1 and continuing in seat order, wrapping round. Each seat starts 3 times (3 players) or 2 times (4 players).

TURN. On your turn you choose exactly one card from your hand and one pile (A or B).
- If you hold at least one placement, you must choose a placement: the card goes on top of that pile. The pile's size rises by 1 and its ox total rises by the card's ox.
- If you hold no placement at all, you must TAKE. You choose any card and either pile, and then:
  1. Add that pile's ox total to your penalty.
  2. If the pile had 3 or more cards, gain 1 bull.
  3. Discard that pile's cards out of the game.
  4. Your chosen card becomes that pile's only card (size 1, ox equal to that card's).
- The other pile is unchanged.
- Every turn removes exactly one card from your hand, so all hands empty at the end of round H.

BULLS. Each bull is worth -2 at the end. Bulls are unlimited and never move between players.

END. After round H, each player's final score = penalty - 2 x bulls. Cards left in the two piles count against nobody.

How the winner is decided: The lowest final score (penalty minus twice bulls) wins. If two or more players tie for lowest, the game is a draw among them.
````

## Reply

````
```json
{
  "name": "11 Nimmt: Two Hot Piles",
  "summary": "Each turn, place one card from a hidden hand on one of two shared piles where it fits; a player with no legal placement must take a pile's ox-heads as penalty, though taking a pile of 3 or more cards earns a bull worth -2. The lowest penalty minus twice bulls wins.",
  "players": {"min": 3, "max": 4, "suggested": 3},
  "parameters": {
    "deck_size_3p": 30,
    "deck_size_4p": 40,
    "hand_size_3p": 9,
    "hand_size_4p": 8,
    "set_aside_3p": 1,
    "set_aside_4p": 6,
    "start_turns_per_seat_3p": 3,
    "start_turns_per_seat_4p": 2,
    "starting_piles": 2,
    "starting_pile_size": 1,
    "fit_min_distance": 1,
    "fit_max_distance": 10,
    "pile_room_limit": 5,
    "bull_pile_threshold": 3,
    "bull_value": 2,
    "ox_special_cards": 3,
    "ox_multiple_of_5": 2,
    "ox_other": 1,
    "special_card_1": 11,
    "special_card_2": 22,
    "special_card_3": 33,
    "starting_penalty": 0,
    "starting_bulls": 0
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The cards (numbers) in this player's private hand", "observable": false},
      {"key": "penalty", "type": "number", "visible": "public", "initial": 0, "meaning": "Total ox-heads taken from piles", "observable": true},
      {"key": "bulls", "type": "number", "visible": "public", "initial": 0, "meaning": "Bulls earned by taking piles of 3 or more cards; each is worth -2 at the end", "observable": true},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Final score so far: penalty - 2 * bulls (lower is better)", "observable": true}
    ],
    "game": [
      {"key": "deck_size", "type": "number", "visible": "public", "initial": 30, "meaning": "N: 30 with 3 players, 40 with 4 players", "observable": false},
      {"key": "hand_size", "type": "number", "visible": "public", "initial": 9, "meaning": "H, which is also the number of rounds: 9 with 3 players, 8 with 4 players", "observable": false},
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "The shuffled undealt cards, used only during setup", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "Cards set aside unseen that take no part in the game", "observable": false},
      {"key": "pile_a", "type": "list", "visible": "public", "initial": [], "meaning": "The cards in Pile A, in play order; the last card is the top", "observable": true},
      {"key": "pile_b", "type": "list", "visible": "public", "initial": [], "meaning": "The cards in Pile B, in play order; the last card is the top", "observable": true},
      {"key": "top_a", "type": "number", "visible": "public", "initial": 0, "meaning": "Top card of Pile A", "observable": false},
      {"key": "top_b", "type": "number", "visible": "public", "initial": 0, "meaning": "Top card of Pile B", "observable": false},
      {"key": "size_a", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in Pile A", "observable": false},
      {"key": "size_b", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in Pile B", "observable": false},
      {"key": "ox_a", "type": "number", "visible": "public", "initial": 0, "meaning": "Ox-head total of Pile A", "observable": false},
      {"key": "ox_b", "type": "number", "visible": "public", "initial": 0, "meaning": "Ox-head total of Pile B", "observable": false},
      {"key": "discarded", "type": "list", "visible": "public", "initial": [], "meaning": "Cards from taken piles, now out of the game", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Current round, from 1 to H", "observable": false},
      {"key": "current_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "The seat whose turn it is", "observable": false},
      {"key": "turns_in_round", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch counter of turns taken this round", "observable": false},
      {"key": "last_play", "type": "text", "visible": "public", "initial": "", "meaning": "Description of the latest turn: who played, which card, which pile, and whether it was a take", "observable": false}
    ]
  },
  "setup": [
    "Set deck_size N = 30 and hand_size H = 9 with 3 players, or N = 40 and H = 8 with 4 players.",
    "Fill deck with the cards 1 to N.",
    "Each card's ox value is 3 if it is 11, 22 or 33; otherwise 2 if it is a multiple of 5; otherwise 1.",
    "Deal each player H cards into hand, each one drawn at random from deck and removed from it.",
    "Draw one random card from deck into pile_a (top_a = that card, size_a = 1, ox_a = its ox), and one into pile_b (top_b, size_b = 1, ox_b = its ox). Both piles are public.",
    "Move every remaining deck card into set_aside (1 card with 3 players, 6 with 4). They are never seen and never used.",
    "Every player starts with penalty 0, bulls 0 and score 0, and round = 1.",
    "Sync each player's hand to that player only."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "current_seat = ((round - 1) mod number_of_players) + 1; turns_in_round = 0"},
    {"action": "ask", "who": "seat current_seat", "answer": "One option naming a card from own hand and a pile, e.g. '17 on A'. If the seat holds at least one placement (card c fits pile X, meaning (c - top_X) mod N is between 1 and 10, and size_X < 5), only placements are offered. Otherwise every card in hand on A and on B is offered, each marked as a take.", "effect": "Records the chosen card c and pile X"},
    {"action": "update", "who": "seat current_seat", "answer": null, "effect": "Remove c from hand. If c fits X ((c - top_X) mod N in 1..10) and size_X < 5 (a placement): append c to pile_X, top_X = c, size_X += 1, ox_X += ox(c). Otherwise (a take): penalty += ox_X; if size_X >= 3 then bulls += 1; move all of pile_X into discarded; pile_X = [c], top_X = c, size_X = 1, ox_X = ox(c). The other pile is unchanged. Then score = penalty - 2 * bulls, and last_play describes the move."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce last_play, both piles (cards, top, size, ox total) and every player's penalty, bulls and score."},
    {"action": "update", "who": "table", "answer": null, "effect": "current_seat = (current_seat mod number_of_players) + 1; turns_in_round += 1"},
    {"action": "repeat", "who": "table", "answer": null, "effect": "Repeat steps 2 to 5 until turns_in_round = number_of_players."},
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1"},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player is sent their own hand and the public state."},
    {"action": "check", "who": "table", "answer": null, "effect": "If round > hand_size, end the game; otherwise continue."}
  ],
  "ending": {
    "condition": "round > hand_size",
    "rank_by": "2 * you.bulls - you.penalty",
    "decided_by": "Each player's final score is penalty - 2 * bulls. The lowest final score wins, so ranking is by its negative. Players tied for lowest share the win, which is a draw among them."
  },
  "rules": [
    {"id": "R1", "text": "With 3 players the deck is cards 1 to 30 and each hand is 9 cards; with 4 players the deck is cards 1 to 40 and each hand is 8 cards."},
    {"id": "R2", "text": "Cards 11, 22 and 33 carry 3 ox-heads, every other multiple of 5 carries 2, and all other cards carry 1 (e.g. 11 -> 3, 25 -> 2, 7 -> 1)."},
    {"id": "R3", "text": "At setup two face-up cards start pile_a and pile_b, each of size 1 with ox equal to its card; the remaining 1 (3 players) or 6 (4 players) cards go to set_aside and are never used."},
    {"id": "R4", "text": "All players start with penalty 0 and bulls 0."},
    {"id": "R5", "text": "A card c fits a pile with top t when (c - t) mod N is between 1 and 10 inclusive; with N = 30 and top 25, cards 26 to 30 and 1 to 5 fit, and 6 and 25 do not."},
    {"id": "R6", "text": "A pile has room when it holds fewer than 5 cards; a pile of 5 cards accepts no placement."},
    {"id": "R7", "text": "When a player holds at least one placement (a card that fits a pile with room), only placements are offered to them."},
    {"id": "R8", "text": "When a player places card c on pile X, c leaves the hand, becomes top_X, size_X rises by 1 and ox_X rises by ox(c); the other pile is unchanged."},
    {"id": "R9", "text": "When a player holds no placement, they must take: they may choose any card from hand and either pile."},
    {"id": "R10", "text": "When a player takes pile X, their penalty rises by ox_X, the pile's cards go to discarded, and the chosen card becomes the pile's only card (size 1, ox equal to its ox)."},
    {"id": "R11", "text": "When the taken pile had 3 or more cards the taker gains 1 bull; when it had 1 or 2 cards they gain none."},
    {"id": "R12", "text": "In round r, seats act one after another starting with seat ((r - 1) mod number_of_players) + 1 and wrapping round in seat order."},
    {"id": "R13", "text": "Every turn removes exactly one card from the acting player's hand, so all hands are empty after round H."},
    {"id": "R14", "text": "The game ends after exactly H rounds (9 with 3 players, 8 with 4)."},
    {"id": "R15", "text": "A player's final score is penalty - 2 * bulls; e.g. penalty 7 with 2 bulls scores 3."},
    {"id": "R16", "text": "Cards left in the two piles at the end count against nobody."},
    {"id": "R17", "text": "The player with the lowest final score wins; players tied for lowest share a draw."}
  ],
  "offers": [
    {"question": "Your turn: choose a card and a pile", "who": "seat current_seat", "options": "If the seat holds any placement: exactly the pairs 'c on A' where c is in hand, (c - top_a) mod N is in 1..10 and size_a < 5, plus the pairs 'c on B' meeting the same test against top_b and size_b. If the seat holds no placement: every card in hand paired with A and with B, each labelled as a take (e.g. 'take A with 17')."}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 3", "why": "The source defines the deck and hand only for 3 and 4 players, and the designer suggests 3. With fewer, there is too little contention over the two piles; the rules define no larger deck."},
    {"what": "No talk step before each turn", "why": "The source has no communication phase, and adding one would be adding a mechanic. Play is about hand management: keeping low-risk cards, timing takes while piles are small, and taking a pile of 3 or more cards when the bull's -2 outweighs its ox-heads."},
    {"what": "Card and pile are chosen as one combined option", "why": "The rules ask for both together, and a single choice lets the offers enforce the placement-first rule exactly."},
    {"what": "Rank by 2 * bulls - penalty", "why": "The engine ranks the highest value first, and the rules want the lowest penalty - 2 * bulls."},
    {"what": "A running score attribute updated every turn", "why": "It makes the standing observable and testable during play."}
  ],
  "simplifications": [
    {"what": "The rotating start seat and sequential turns are built as a repeat loop over current_seat with a per-turn update", "why": "Each turn changes the piles before the next seat chooses, so each turn's update must run before the next ask."},
    {"what": "Whether a move is a take is worked out at update time by testing if the chosen card fits the chosen pile with room", "why": "The offers allow non-placements only when no placement exists, so this test is equivalent to the rule."}
  ],
  "unsupported": []
}
```
````
