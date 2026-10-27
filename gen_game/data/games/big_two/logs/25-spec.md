# 25 spec

- time: 2026-10-27T21:55:02+00:00 (56.4s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 40b1071ef3a423dc, reply sha256 c78fbcbada775df9

## Sent

````
Game: Little Two
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
CARDS. There are 30 cards, numbered 1 to 30. A card c has rank = floor((c+2)/3), from 1 to 10, and suit = c - 3*(rank-1), from 1 to 3. Rank 1 is lowest and rank 10 (cards 28, 29, 30) is highest and plays the role of the 2. Within a rank, a higher suit is a higher card, so a higher card number is always a higher card. Examples: card 13 has rank 5, suit 1; card 14 has rank 5, suit 2; card 16 has rank 6, suit 1.

PLAY KINDS. A play is 1 to 3 cards from your own hand, written as their numbers in ascending order separated by single spaces (for example '13 14').
- Single: 1 card.
- Pair: 2 cards of the same rank. '13 14' is a pair; '14 16' is not.
- Triple: 3 cards of the same rank.
- Run: 3 cards whose ranks are three consecutive numbers (for example ranks 4, 5, 6), in any suits. Ranks do not wrap around.
Any other set of cards is not a play. The value of a play is its highest card number.

SETUP. There are 3 players in seats 1, 2 and 3. Each player has a private hand, a public card_count, a public penalty (starting at 0), public deals_won (starting at 0) and a public last_action (starting as 'no play yet'). The table tracks deal_number (starting at 0), orbit (starting at 0), deal_active (starting false), leader_seat, first_orbit, pile_kind ('empty', 'single', 'pair', 'triple' or 'run'), pile_value and last_player (0 means nobody). The game lasts at most 40 orbits and at most 3 deals.

EACH ORBIT (one engine round):
1. Add 1 to orbit.
2. If deal_active is false and deal_number is less than 3, start a deal. Add 1 to deal_number. Shuffle all 30 cards. Deal 9 into each player's private hand and put the remaining 3 into a hidden aside list that nobody sees. Set every card_count to 9. Set leader_seat to deal_number, so seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3. Set deal_active to true, first_orbit to true, pile_kind to 'empty', pile_value to 0 and last_player to the leader. This is the only random event in an orbit.
3. Seats then take turns in the order seat 1, seat 2, seat 3. A seat skips its turn if deal_active is false, or if first_orbit is true and its seat number is lower than leader_seat. On each turn that is not skipped:
  a. Clearance. If last_player equals this seat, the other two have passed since this seat's last play (or the deal has just started). Set pile_kind to 'empty' and pile_value to 0. This seat now leads.
  b. Options. The seat is offered exactly the following, and nothing else:
     - If pile_kind is 'empty': every single, pair, triple and run that can be made from its hand. Passing is not allowed.
     - If pile_kind is 'single': 'pass', every single with value greater than pile_value, and every triple of any value (a bomb).
     - If pile_kind is 'pair': 'pass', every pair with value greater than pile_value, and every triple of any value (a bomb).
     - If pile_kind is 'triple': 'pass' and every triple with value greater than pile_value.
     - If pile_kind is 'run': 'pass' and every run with value greater than pile_value.
  c. The seat chooses one option. Everyone sees the choice.
  d. Apply the choice. If it is 'pass', set this seat's last_action to 'pass' and change nothing else. Otherwise:
     - Split the option on spaces into all of its card numbers.
     - Remove every one of those cards from the hand.
     - Lower card_count by the number of cards played (1, 2 or 3).
     - Set pile_kind: 1 card is 'single'; 2 cards are 'pair'; 3 cards of one rank are 'triple'; 3 cards of consecutive ranks are 'run'.
     - Set pile_value to the highest card number played.
     - Set last_player to this seat.
     - Set last_action to the full option string.
     A triple that bombs a single or a pair makes pile_kind 'triple', so only a higher triple can follow it.
  e. If this seat's card_count is now 0, it wins the deal. Add 1 to its deals_won. Every other seat with n cards left adds a penalty of n, doubled to 2n if n is 7 or more, plus 1 for each card numbered 28, 29 or 30 still in its hand. Set deal_active to false. The rest of this orbit's turns are skipped.
4. At the end of the orbit, set first_orbit to false.

END. The game ends when deal 3 has ended, or when orbit 40 is complete. If orbit 40 ends while a deal is still active, every seat is penalised for the cards it holds, by the same formula. Deals that never started are not played.

There is no talk phase. All plays and passes are public, and hands and the aside cards stay hidden.

How the winner is decided: The player with the lowest total penalty wins. If two or three players tie for lowest, the one among them with the most deals_won wins. If they are still tied, the game is a draw.
````

## Reply

````
```json
{
  "name": "Little Two",
  "summary": "A three-player climbing card game over up to 3 deals: shed your 9 cards by beating the pile with singles, pairs, triples or runs. Triples bomb singles and pairs. The lowest total penalty wins.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "deck_size": 30,
    "ranks": 10,
    "suits": 3,
    "hand_size": 9,
    "aside_size": 3,
    "max_deals": 3,
    "max_orbits": 40,
    "double_penalty_threshold": 7,
    "double_penalty_factor": 2,
    "top_rank_card_low": 28,
    "top_rank_card_high": 30,
    "top_card_penalty": 1,
    "min_play_cards": 1,
    "max_play_cards": 3,
    "run_length": 3,
    "initial_penalty": 0,
    "initial_deals_won": 0,
    "deals_won_tiebreak_multiplier": 10
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "card numbers (1-30) the player holds", "observable": false},
      {"key": "card_count", "type": "number", "visible": "public", "initial": 0, "meaning": "number of cards in hand", "observable": true},
      {"key": "penalty", "type": "number", "visible": "public", "initial": 0, "meaning": "total penalty points; lower is better", "observable": true},
      {"key": "deals_won", "type": "number", "visible": "public", "initial": 0, "meaning": "deals this player won by emptying their hand", "observable": true},
      {"key": "last_action", "type": "text", "visible": "public", "initial": "no play yet", "meaning": "'pass' or the last play string, e.g. '13 14'", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30], "meaning": "undealt cards during a deal", "observable": false},
      {"key": "aside", "type": "list", "visible": "none", "initial": [], "meaning": "the 3 undealt cards set aside each deal, seen by nobody", "observable": false},
      {"key": "deal_number", "type": "number", "visible": "public", "initial": 0, "meaning": "number of deals started", "observable": true},
      {"key": "orbit", "type": "number", "visible": "public", "initial": 0, "meaning": "number of orbits (engine rounds) begun", "observable": true},
      {"key": "deal_active", "type": "bool", "visible": "public", "initial": false, "meaning": "whether a deal is in progress", "observable": false},
      {"key": "leader_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "seat that leads the current deal (equals deal_number)", "observable": false},
      {"key": "first_orbit", "type": "bool", "visible": "public", "initial": false, "meaning": "true during the orbit in which a deal started", "observable": false},
      {"key": "pile_kind", "type": "text", "visible": "public", "initial": "empty", "meaning": "'empty', 'single', 'pair', 'triple' or 'run'", "observable": true},
      {"key": "pile_value", "type": "number", "visible": "public", "initial": 0, "meaning": "highest card number of the play on top of the pile", "observable": true},
      {"key": "last_player", "type": "number", "visible": "public", "initial": 0, "meaning": "seat of the last non-pass play (0 = nobody)", "observable": false}
    ]
  },
  "setup": [
    "Seat the 3 players in seats 1, 2 and 3.",
    "Every player starts with an empty hand, card_count 0, penalty 0, deals_won 0 and last_action 'no play yet'.",
    "The table starts with deal_number 0, orbit 0, deal_active false, pile_kind 'empty', pile_value 0 and last_player 0.",
    "No cards are dealt in setup. The first deal starts in step 2 of orbit 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "orbit += 1"},
    {"action": "update", "who": "all players", "answer": null, "when": "deal_active == false and deal_number < 3", "effect": "Start a deal: deal_number += 1; set deck to cards 1..30, every hand to [] and aside to []; draw 9 random cards from deck into each player's hand (remove from deck, append to hand); move the remaining 3 deck cards into aside; every card_count = 9; leader_seat = deal_number; deal_active = true; first_orbit = true; pile_kind = 'empty'; pile_value = 0; last_player = leader_seat. Announce that deal {deal_number} has started and seat {leader_seat} leads."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "each player privately sees their own hand and the public state"},

    {"action": "update", "who": "seat 1", "answer": null, "when": "deal_active == true and not (first_orbit == true and 1 < leader_seat) and last_player == 1", "effect": "Clearance: pile_kind = 'empty', pile_value = 0"},
    {"action": "ask", "who": "seat 1", "when": "deal_active == true and not (first_orbit == true and 1 < leader_seat)", "answer": "one option from the legal-play list built from seat 1's hand and the pile (see offers); the choice is shown to everyone", "effect": "the chosen option is recorded for the next step"},
    {"action": "update", "who": "seat 1", "answer": null, "when": "deal_active == true and not (first_orbit == true and 1 < leader_seat)", "effect": "If 'pass': seat1.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat1.hand; seat1.card_count -= number of cards; pile_kind = 'single' if 1 card, 'pair' if 2, 'triple' if 3 of one rank, 'run' if 3 of consecutive ranks; pile_value = highest card; last_player = 1; seat1.last_action = option."},
    {"action": "update", "who": "all players", "answer": null, "when": "deal_active == true and seat1.card_count == 0", "effect": "seat1.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"},

    {"action": "update", "who": "seat 2", "answer": null, "when": "deal_active == true and not (first_orbit == true and 2 < leader_seat) and last_player == 2", "effect": "Clearance: pile_kind = 'empty', pile_value = 0"},
    {"action": "ask", "who": "seat 2", "when": "deal_active == true and not (first_orbit == true and 2 < leader_seat)", "answer": "one option from the legal-play list built from seat 2's hand and the pile (see offers); the choice is shown to everyone", "effect": "the chosen option is recorded for the next step"},
    {"action": "update", "who": "seat 2", "answer": null, "when": "deal_active == true and not (first_orbit == true and 2 < leader_seat)", "effect": "If 'pass': seat2.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat2.hand; seat2.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 2; seat2.last_action = option."},
    {"action": "update", "who": "all players", "answer": null, "when": "deal_active == true and seat2.card_count == 0", "effect": "seat2.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"},

    {"action": "update", "who": "seat 3", "answer": null, "when": "deal_active == true and last_player == 3", "effect": "Clearance: pile_kind = 'empty', pile_value = 0"},
    {"action": "ask", "who": "seat 3", "when": "deal_active == true", "answer": "one option from the legal-play list built from seat 3's hand and the pile (see offers); the choice is shown to everyone", "effect": "the chosen option is recorded for the next step"},
    {"action": "update", "who": "seat 3", "answer": null, "when": "deal_active == true", "effect": "If 'pass': seat3.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat3.hand; seat3.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 3; seat3.last_action = option."},
    {"action": "update", "who": "all players", "answer": null, "when": "deal_active == true and seat3.card_count == 0", "effect": "seat3.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"},

    {"action": "update", "who": "all players", "answer": null, "effect": "first_orbit = false"},
    {"action": "update", "who": "all players", "answer": null, "when": "orbit == 40 and deal_active == true", "effect": "For every seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game if (deal_number == 3 and deal_active == false) or orbit >= 40; otherwise continue"}
  ],
  "ending": {
    "condition": "(deal_number == 3 and deal_active == false) or orbit >= 40",
    "rank_by": "you.deals_won - 10 * you.penalty",
    "decided_by": "The lowest total penalty wins. Among players tied for lowest penalty, the one with the most deals_won wins. Players still tied share the win, which is the draw."
  },
  "rules": [
    {"id": "R1", "text": "Card c has rank floor((c+2)/3), from 1 to 10, and suit c - 3*(rank-1), from 1 to 3; for example card 13 is rank 5 suit 1 and card 16 is rank 6 suit 1."},
    {"id": "R2", "text": "A higher card number is always a higher card, and the value of a play is its highest card number."},
    {"id": "R3", "text": "A single is 1 card, a pair is 2 cards of the same rank, a triple is 3 cards of the same rank, and a run is 3 cards of three consecutive ranks without wrap-around; any other set of cards is not a play."},
    {"id": "R4", "text": "When '13 14' is offered it is a pair; '14 16' is never offered as a pair."},
    {"id": "R5", "text": "Each orbit begins with orbit increased by 1."},
    {"id": "R6", "text": "When deal_active is false and deal_number < 3 at the start of an orbit, deal_number increases by 1, each player gets 9 random cards, 3 cards go to the hidden aside, every card_count becomes 9, leader_seat = deal_number, first_orbit = true, pile_kind = 'empty', pile_value = 0 and last_player = leader_seat."},
    {"id": "R7", "text": "Seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3."},
    {"id": "R8", "text": "Seats take turns in order 1, 2, 3; a seat is skipped when deal_active is false, or when first_orbit is true and its seat number is below leader_seat."},
    {"id": "R9", "text": "When a seat's turn starts and last_player equals that seat, pile_kind becomes 'empty' and pile_value becomes 0, and that seat leads."},
    {"id": "R10", "text": "When pile_kind is 'empty', the seat is offered every single, pair, triple and run from its hand, and 'pass' is not offered."},
    {"id": "R11", "text": "When pile_kind is 'single', the seat is offered 'pass', every single with value > pile_value and every triple of any value."},
    {"id": "R12", "text": "When pile_kind is 'pair', the seat is offered 'pass', every pair with value > pile_value and every triple of any value."},
    {"id": "R13", "text": "When pile_kind is 'triple', the seat is offered 'pass' and every triple with value > pile_value."},
    {"id": "R14", "text": "When pile_kind is 'run', the seat is offered 'pass' and every run with value > pile_value."},
    {"id": "R15", "text": "When a seat passes, its last_action becomes 'pass' and nothing else changes."},
    {"id": "R16", "text": "When a seat plays k cards, those cards leave its hand, card_count drops by k, pile_value becomes the highest card played, last_player becomes that seat and last_action becomes the option string."},
    {"id": "R17", "text": "After a play, pile_kind is 'single' for 1 card, 'pair' for 2, 'triple' for 3 of one rank and 'run' for 3 consecutive ranks; a triple bombing a single or pair sets pile_kind to 'triple'."},
    {"id": "R18", "text": "When a seat's card_count reaches 0, its deals_won increases by 1, deal_active becomes false and the rest of that orbit's turns are skipped."},
    {"id": "R19", "text": "When a deal is won, each other seat with n cards adds n to penalty, or 2n if n >= 7, plus 1 per card numbered 28, 29 or 30 it holds; for example 7 cards including card 30 adds 15."},
    {"id": "R20", "text": "At the end of every orbit first_orbit becomes false."},
    {"id": "R21", "text": "When orbit 40 ends with a deal still active, every seat adds the same penalty formula for the cards it holds."},
    {"id": "R22", "text": "The game ends when deal 3 has ended or when orbit 40 is complete, and deals that never started are not played."},
    {"id": "R23", "text": "The lowest penalty wins, ties are broken by the most deals_won, and players still tied share the win."},
    {"id": "R24", "text": "Hands and the aside cards are hidden; card_count, penalty, deals_won, last_action and the pile are public."}
  ],
  "offers": [
    {"question": "Turn choice when pile_kind is 'empty' (leading)", "who": "the seat whose turn it is", "options": "every single, pair, triple and run that can be made from its hand, each written as ascending card numbers separated by single spaces; no 'pass'"},
    {"question": "Turn choice when pile_kind is 'single'", "who": "the seat whose turn it is", "options": "'pass'; every single from its hand with card number > pile_value; every triple from its hand of any value"},
    {"question": "Turn choice when pile_kind is 'pair'", "who": "the seat whose turn it is", "options": "'pass'; every pair from its hand whose higher card > pile_value; every triple from its hand of any value"},
    {"question": "Turn choice when pile_kind is 'triple'", "who": "the seat whose turn it is", "options": "'pass'; every triple from its hand whose highest card > pile_value"},
    {"question": "Turn choice when pile_kind is 'run'", "who": "the seat whose turn it is", "options": "'pass'; every run from its hand whose highest card > pile_value"},
    {"question": "Any turn", "who": "seats skipped by rule R8 or after the deal ended", "options": "not asked"}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed the game at 3 seats. The clearance rule ('the other two have passed') and the leader rotation over 3 deals assume exactly three seats."},
    {"what": "No talk phase", "why": "The rules say there is no talk phase. All information comes from public plays, passes and card counts."},
    {"what": "Turns use ask, one seat at a time", "why": "The order of play matters, and each seat must see the earlier plays it has to beat."},
    {"what": "rank_by = deals_won - 10 * penalty", "why": "deals_won is at most 3, so a factor of 10 makes a lower penalty dominate and uses deals_won only as the tie-break. Players still tied share the win, which matches the source's draw."},
    {"what": "Strategy at the table", "why": "A thoughtful player keeps triples as bombs, holds high cards (28-30) to regain the lead, tracks which high cards are gone, and dumps cards before falling to 7 or more, where the penalty doubles."}
  ],
  "simplifications": [
    {"what": "The legal-play option list is computed by the engine from the seat's hand list and the pile each turn", "why": "The engine offers choices from a list. The rules define the options exactly, so they are generated by arithmetic on card numbers rather than typed freely."},
    {"what": "Each deal resets the deck to cards 1..30 and empties hands and aside before dealing", "why": "This is the 'shuffle all 30 cards' step expressed as list operations followed by random draws."},
    {"what": "The three seat turns are written out as three fixed blocks of steps, each with a when-condition", "why": "The step list is flat. Per-step conditions reproduce the skip rules and the end-of-deal cutoff."}
  ],
  "unsupported": []
}
```
````
