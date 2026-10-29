# 21 spec

- time: 2026-10-27T09:02:49+00:00 (48.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 4b88a15b9e725a13, reply sha256 90d884b9f278af1c

## Sent

````
Game: Kobayakawa Duel Rounds with Table Talk
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP: Each player starts with 5 kamons. The centre starts with 10 kamons. The game lasts exactly 10 rounds.

EACH ROUND:
1. Deal. Shuffle a fresh deck of 15 cards numbered 1 to 15. Deal each player one face-down hand card, which only that player sees. Deal each player one face-down reserve card, which nobody sees. Turn one more card face up: this is the Kobayakawa card, value K. Announce K.
2. Draw choice. All players choose KEEP or SWAP at the same moment. A SWAP player discards their hand card face up, takes their reserve card as their new hand card, and looks at it. Reserve cards of KEEP players are not used. Announce every discarded card and who discarded it.
3. Talk. Every player writes one short public message at the same moment, without seeing the others' messages. Then all messages are shown to everyone. Messages may say anything, including false claims about one's card or intentions. Nothing said is binding.
4. Fight choice. All players choose FIGHT or PASS at the same moment. A player with 0 kamons must PASS. Each FIGHT player puts 1 kamon into the pot.
5. Resolve.
   - No fighters: nothing happens.
   - Exactly one fighter: that player takes their own kamon back. Their card is not revealed, and the centre pays nothing.
   - Two or more fighters: all fighters reveal their cards. Each fighter's total equals their card, except that the fighter with the lowest card adds K to it. The fighter with the highest total wins. If totals tie, the tied fighter with the lower card wins. The winner takes the whole pot. If the centre has at least 1 kamon, the winner also takes 1 kamon from the centre. Losing fighters lose their stakes.
6. Announce all fighters, revealed cards, totals, the winner, and every player's kamon count.
7. After round 10 the game ends.

How the winner is decided: After round 10, the player with the most kamons wins. If two or more players tie for most, the game is a draw.
````

## Reply

````
```json
{
  "name": "Kobayakawa Duel Rounds with Table Talk",
  "summary": "Over 10 rounds, players hold one secret card, may swap it blind, talk, then fight for a pot. The lowest fighter's card adds the face-up Kobayakawa value, and the highest total takes the pot plus 1 kamon from the centre.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "starting_kamons": 5,
    "centre_starting_kamons": 10,
    "rounds": 10,
    "deck_size": 15,
    "card_min": 1,
    "card_max": 15,
    "fight_stake": 1,
    "centre_bonus": 1,
    "hand_cards_per_player": 1,
    "reserve_cards_per_player": 1,
    "minimum_fighters_for_showdown": 2
  },
  "attributes": {
    "player": [
      {"key": "kamons", "type": "number", "visible": "public", "initial": 5, "meaning": "the player's kamons; this is the score", "observable": true},
      {"key": "hand", "type": "number", "visible": "ally", "initial": 0, "meaning": "the player's current face-down hand card (1-15), seen only by its owner", "observable": false},
      {"key": "draw_choice", "type": "text", "visible": "public", "initial": "", "meaning": "KEEP or SWAP this round", "observable": false},
      {"key": "discarded", "type": "number", "visible": "public", "initial": 0, "meaning": "the card discarded face up by a SWAP this round (0 if the player kept)", "observable": true},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "this round's public table-talk message", "observable": false},
      {"key": "fight_choice", "type": "text", "visible": "public", "initial": "", "meaning": "FIGHT or PASS this round", "observable": false},
      {"key": "fought", "type": "bool", "visible": "public", "initial": false, "meaning": "whether the player fights this round", "observable": false},
      {"key": "revealed_card", "type": "number", "visible": "public", "initial": 0, "meaning": "the card revealed in a showdown of 2 or more fighters (0 if not revealed)", "observable": true},
      {"key": "total", "type": "number", "visible": "public", "initial": 0, "meaning": "the fight total in a showdown: the card, plus K for the lowest card (0 if not in a showdown)", "observable": true}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "the current round number", "observable": true},
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "this round's fresh shuffled deck of cards 1-15", "observable": false},
      {"key": "reserve_cards", "type": "list", "visible": "none", "initial": [], "meaning": "each seat's face-down reserve card, in seat order; nobody sees it", "observable": false},
      {"key": "kobayakawa", "type": "number", "visible": "public", "initial": 0, "meaning": "K, the face-up Kobayakawa card this round", "observable": true},
      {"key": "centre", "type": "number", "visible": "public", "initial": 10, "meaning": "kamons left in the centre", "observable": true},
      {"key": "pot", "type": "number", "visible": "public", "initial": 0, "meaning": "kamons staked this round", "observable": false},
      {"key": "fighter_count", "type": "number", "visible": "public", "initial": 0, "meaning": "the number of FIGHT players this round", "observable": false},
      {"key": "lowest_card", "type": "number", "visible": "public", "initial": 0, "meaning": "the lowest card among the fighters in a showdown", "observable": false},
      {"key": "winner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "the seat that won this round's showdown (0 if there was none)", "observable": true}
    ]
  },
  "setup": [
    "Every player's kamons is set to 5.",
    "The centre is set to 10 kamons.",
    "The round is set to 0."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; deck = [1..15] (a fresh deck); reserve_cards = []; pot = 0; fighter_count = 0; lowest_card = 0; winner_seat = 0; for every player: draw_choice = '', discarded = 0, message = '', fight_choice = '', fought = false, revealed_card = 0, total = 0"},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player: draw one random card from deck into hand and remove it from deck. Then, for each seat in order: draw one random card from deck, append it to reserve_cards and remove it from deck. Then draw one random card from deck into kobayakawa and remove it from deck. Announce: 'Round {round}: the Kobayakawa card K is {kobayakawa}.'"},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand, every player's kamons, the centre and kobayakawa."},
    {"action": "poll", "who": "all players", "answer": "choice: KEEP | SWAP", "effect": "draw_choice = the answer"},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player with draw_choice == 'SWAP': discarded = hand; hand = reserve_cards[seat-1]. Announce each discard: 'Seat {seat} swapped and discarded {discarded}.'"},
    {"action": "sync", "who": "each player with draw_choice SWAP", "answer": null, "effect": "Each swapping player sees their new hand."},
    {"action": "poll", "who": "all players", "answer": "short text", "effect": "message = the answer; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all messages are in"},
    {"action": "poll", "who": "all players", "answer": "choice: FIGHT | PASS (only PASS when kamons == 0)", "effect": "fight_choice = the answer; fought = (fight_choice == 'FIGHT')"},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player with fought: kamons -= 1; pot += 1. fighter_count = the number of players with fought."},
    {"action": "update", "who": "the single fighter", "answer": null, "effect": "when fighter_count == 1: that player's kamons += pot; pot = 0. The card is not revealed and the centre is unchanged."},
    {"action": "update", "who": "all fighters", "answer": null, "effect": "when fighter_count >= 2: lowest_card = min(hand) over players with fought; for each player with fought: revealed_card = hand; total = hand + (hand == lowest_card ? kobayakawa : 0)"},
    {"action": "update", "who": "the showdown winner", "answer": null, "effect": "when fighter_count >= 2: winner_seat = the fighter with the largest (total * 100 - hand), so the highest total wins and a tie goes to the lower card; that player's kamons += pot + min(1, centre); centre -= min(1, centre); pot = 0"},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce the fighters, each revealed_card and total, winner_seat, and every player's kamons and the centre."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round >= 10; otherwise continue."}
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.kamons",
    "decided_by": "After round 10, each player's standing is their kamons. The most kamons wins, and players tied for most share the result (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then each player has 5 kamons, the centre has 10 kamons and the round is 0."},
    {"id": "R2", "text": "When a round starts, then the deck is a fresh set of the 15 cards 1 to 15, and each player gets 1 hand card and 1 reserve card from it, all distinct."},
    {"id": "R3", "text": "When the deal is done, then one more card from the deck is set as kobayakawa (K) and announced publicly."},
    {"id": "R4", "text": "When a player's hand is dealt, then only that player can see it, and no player can see any reserve card."},
    {"id": "R5", "text": "When a player chooses SWAP, then discarded becomes their old hand card (publicly announced with their seat) and hand becomes their reserve card."},
    {"id": "R6", "text": "When a player chooses KEEP, then hand is unchanged, discarded stays 0 and their reserve card is not used."},
    {"id": "R7", "text": "When the KEEP/SWAP choice is asked, then all players answer at once, without seeing the others' choices."},
    {"id": "R8", "text": "When the talk step runs, then every player submits one short message at once, and all messages are shown to everyone only after all are in."},
    {"id": "R9", "text": "When a player has 0 kamons at the fight choice, then their only option is PASS."},
    {"id": "R10", "text": "When a player chooses FIGHT, then their kamons drop by 1 and the pot rises by 1."},
    {"id": "R11", "text": "When no player fights, then no kamons change that round."},
    {"id": "R12", "text": "When exactly one player fights, then that player gets their 1 kamon back, their card is not revealed and the centre is unchanged."},
    {"id": "R13", "text": "When two or more players fight, then each fighter's revealed_card equals their hand and their total equals their hand, plus K for the fighter with the lowest card."},
    {"id": "R14", "text": "When two or more players fight, then the fighter with the highest total wins, and if totals tie the tied fighter with the lower card wins (e.g. K=5: cards 3 and 8 give totals 8 and 8, so card 3 wins)."},
    {"id": "R15", "text": "When a showdown winner is decided and the centre has at least 1 kamon, then the winner gains the whole pot plus 1 kamon and the centre loses 1."},
    {"id": "R16", "text": "When a showdown winner is decided and the centre has 0 kamons, then the winner gains only the pot."},
    {"id": "R17", "text": "When a showdown is decided, then each losing fighter loses the 1 kamon they staked."},
    {"id": "R18", "text": "When round 10 ends, then the game ends and the player with the most kamons wins, with players tied for most sharing the result."}
  ],
  "offers": [
    {"question": "Draw choice", "who": "every seat", "options": "KEEP, SWAP"},
    {"question": "Talk message", "who": "every seat", "options": "any short text"},
    {"question": "Fight choice", "who": "every seat", "options": "a seat with kamons >= 1: FIGHT, PASS; a seat with kamons == 0: PASS only"}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer suggests 4, so it is kept. Below 3 a showdown is just a duel with no one to bluff off the table. Above 5 the 15-card deck cannot cover a hand and a reserve for every player plus K (6 players would need 13 of the 15 cards, leaving swaps and discards nearly fully informative), and one player's choice matters less."},
    {"what": "Table talk kept as a simultaneous poll broadcast to all", "why": "The source requires simultaneous messages. Talk earns its place because interests conflict: a player can claim a high card to scare others into passing, or a low card to bait fighters when K is large."},
    {"what": "Reserve cards stored as a hidden table list in seat order", "why": "Nobody may see a reserve card, and a player attribute cannot be hidden from its owner, so the reserves live on the table with visibility none."},
    {"what": "The tie-break is coded as the largest (total * 100 - card)", "why": "Totals are at most 30, so this ranks by total first and by the lower card second. Cards are distinct, so the result is unique."},
    {"what": "Strategy at the table", "why": "A thoughtful player weighs K against their card (a low card plus a big K can win), reads public discards and messages, bluffs about strength, and saves kamons near 0, because staying out also keeps them alive."}
  ],
  "simplifications": [
    {"what": "A tie for most kamons at the end is a shared win rather than a declared draw", "why": "The engine ranks by one expression and players level at the top share the win, which is how it expresses the source's draw."}
  ],
  "unsupported": []
}
```
````
