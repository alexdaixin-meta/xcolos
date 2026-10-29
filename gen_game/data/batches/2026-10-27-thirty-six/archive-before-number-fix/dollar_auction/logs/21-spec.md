# 21 spec

- time: 2026-10-27T16:56:39+00:00 (45.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 c3fa337341150b48, reply sha256 58eb7c5165fa94c0

## Sent

````
Game: Escalation Auction
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
PARAMETERS (stored as table attributes): starting_coins = 100; auctions = 6; raise_stages = 3; min_winning_bid = 1; prize_deck = [10, 15, 20, 25, 30, 40].

R1 Setup: every player has coins = 100, prize_points = 0, committed = 0, final_score = 0. Table: auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none'.

R2 Private values: at setup each player is dealt their own values list, a random order of [10, 15, 20, 25, 30, 40] (total 140), visible only to its owner. Entry k is that player's value for auction k. Players' lists are dealt independently, so two players may hold the same value for the same auction.

Each round is one auction. There are 6 rounds.

R3 Round start: auction increases by 1 and every player's committed is set to 0. Each player is privately told their value for this auction (entry number 'auction' of their values list). Everyone is told the auction number and every player's current coins.

R4 Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and change no numbers.

R5 Raise stage (runs 3 times per auction): all players choose at the same time a raise, a whole number from 0 up to (their own coins − their own committed). The range is computed for each player at that moment from their current coins and committed attributes. For example, it is 0..100 at the start of an auction with 100 coins, and 0..55 for a player with 85 coins who committed 30 earlier in the same auction. Immediately after the poll, each player's committed increases by the raise they chose.

R6 Budget limit: a player can never commit more than their coins in one auction. With coins 40 and committed 30, the options are exactly 0 to 10.

R7 Announcement: after each of the 3 raise stages, every player's committed total is announced to all.

R8 Resolution, payment: after the third stage, top_bid = the highest committed, and top_count = the number of players whose committed equals top_bid. Every player's coins decrease by their committed, whether or not they won. For example, bids of 20, 15 and 0 leave coins of 80, 85 and 100 from 100 each.

R9 Resolution, prize: if top_count = 1 and top_bid ≥ 1, that player is the auction_winner and adds their own value for this auction to prize_points. Otherwise auction_winner = 'none' and nobody gets a prize. The winner and every player's coins are announced. Each player's committed is then reset to 0.

R10 End: after the 6th auction, each player's final_score = coins + prize_points.

How the winner is decided: After 6 auctions, the player with the highest final_score (coins remaining + prize_points) wins. If several players tie for the highest final_score, the game is a draw among them.
````

## Reply

````
```json
{
  "name": "Escalation Auction",
  "summary": "Six sealed all-pay auctions, each with three simultaneous raise stages. Every bidder pays what they committed, only a sole top bidder wins their private prize value, and the highest coins plus prize points wins.",
  "players": {"min": 3, "max": 5, "suggested": 3},
  "parameters": {
    "starting_coins": 100,
    "auctions": 6,
    "raise_stages": 3,
    "min_winning_bid": 1,
    "prize_value_1": 10,
    "prize_value_2": 15,
    "prize_value_3": 20,
    "prize_value_4": 25,
    "prize_value_5": 30,
    "prize_value_6": 40,
    "prize_values_total": 140,
    "initial_prize_points": 0,
    "initial_committed": 0,
    "initial_final_score": 0,
    "min_raise": 0,
    "winning_top_count": 1
  },
  "attributes": {
    "player": [
      {"key": "coins", "type": "number", "visible": "public", "initial": 100, "meaning": "Coins the player still holds. All committed coins are paid at the end of each auction.", "observable": true},
      {"key": "prize_points", "type": "number", "visible": "ally", "initial": 0, "meaning": "Sum of the player's own private values for the auctions they won.", "observable": false},
      {"key": "committed", "type": "number", "visible": "public", "initial": 0, "meaning": "Total the player has raised so far in the current auction. It is announced after each raise stage.", "observable": true},
      {"key": "final_score", "type": "number", "visible": "public", "initial": 0, "meaning": "coins + prize_points, computed after the 6th auction.", "observable": true},
      {"key": "values", "type": "list", "visible": "ally", "initial": "a random order of [10, 15, 20, 25, 30, 40], dealt independently to each player", "meaning": "Entry k is the player's private value for auction k.", "observable": false},
      {"key": "current_value", "type": "number", "visible": "ally", "initial": 0, "meaning": "The player's value for the current auction (entry number 'auction' of values).", "observable": false}
    ],
    "game": [
      {"key": "prize_deck", "type": "list", "visible": "public", "initial": [10, 15, 20, 25, 30, 40], "meaning": "The six prize values that each player's values list is a permutation of.", "observable": false},
      {"key": "auction", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of the current auction, from 1 to 6.", "observable": true},
      {"key": "top_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "The highest committed total at the resolution of the auction.", "observable": true},
      {"key": "top_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players whose committed equals top_bid.", "observable": true},
      {"key": "auction_winner", "type": "text", "visible": "public", "initial": "none", "meaning": "The seat that won the current auction, or 'none'.", "observable": true}
    ]
  },
  "setup": [
    "Every player gets coins = 100, prize_points = 0, committed = 0, final_score = 0 and current_value = 0.",
    "The table gets auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none' and prize_deck = [10, 15, 20, 25, 30, 40].",
    "Each player is dealt their own values list, a random order of prize_deck (total 140). The lists are dealt independently and seeded, and each is visible only to its owner.",
    "Each player is sent their own state (sync)."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "auction += 1. Every player's committed = 0. Every player's current_value = entry number 'auction' (1-based) of their values list."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player is privately sent their current_value for this auction."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Auction {auction} of 6.' plus every seat's coins."},
    {"action": "poll", "who": "all players", "answer": "short text message", "effect": "No state change. Broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all are in."},
    {"action": "poll", "who": "all players", "answer": "whole number from 0 to (you.coins - you.committed)", "effect": "Raise stage 1: each player's committed += their raise."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every seat's committed after stage 1."},
    {"action": "poll", "who": "all players", "answer": "whole number from 0 to (you.coins - you.committed)", "effect": "Raise stage 2: each player's committed += their raise."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every seat's committed after stage 2."},
    {"action": "poll", "who": "all players", "answer": "whole number from 0 to (you.coins - you.committed)", "effect": "Raise stage 3: each player's committed += their raise."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every seat's committed after stage 3."},
    {"action": "update", "who": "all players", "answer": null, "effect": "top_bid = max over players of committed. top_count = number of players with committed == top_bid. Every player's coins -= committed."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If top_count == 1 and top_bid >= 1: auction_winner = the seat with committed == top_bid, and that player's prize_points += their current_value. Otherwise auction_winner = 'none'."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Auction {auction} winner: {auction_winner}.' plus every seat's coins."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Every player's committed = 0. If auction == 6: every player's final_score = coins + prize_points."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if auction >= 6. Otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "auction >= 6",
    "rank_by": "you.final_score",
    "decided_by": "Each player's standing is final_score = coins remaining + prize_points. The highest final_score wins, and players tied at the top share the win (a draw among them)."
  },
  "rules": [
    {"id": "R1", "text": "At setup every player has coins = 100, prize_points = 0, committed = 0, final_score = 0, and the table has auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none'."},
    {"id": "R2", "text": "At setup each player is dealt a values list that is a random order of [10, 15, 20, 25, 30, 40] (sum 140), visible only to its owner. Lists are dealt independently, so two players may hold the same value for the same auction."},
    {"id": "R3", "text": "When a round starts, auction increases by 1, every player's committed becomes 0, and each player's current_value becomes entry number 'auction' of their values list."},
    {"id": "R4", "text": "At the start of each auction, each player is told only their own current_value, and everyone is told the auction number and every player's coins."},
    {"id": "R5", "text": "Each auction, every player sends one short message simultaneously, all messages are shown to everyone, and no number changes."},
    {"id": "R6", "text": "Each auction has exactly 3 simultaneous raise stages, and after each one every player's committed increases by the raise they chose."},
    {"id": "R7", "text": "In a raise stage a player's options are exactly the whole numbers 0 to (coins - committed): 0..100 with coins 100 and committed 0, 0..55 with coins 85 and committed 30, 0..10 with coins 40 and committed 30."},
    {"id": "R8", "text": "A player's committed can never exceed their coins within one auction."},
    {"id": "R9", "text": "After each of the 3 raise stages, every player's committed total is announced to all."},
    {"id": "R10", "text": "After the third stage, top_bid = the highest committed and top_count = the number of players whose committed equals top_bid."},
    {"id": "R11", "text": "After the third stage every player's coins decrease by their committed, win or lose: bids of 20, 15 and 0 from 100 coins each leave 80, 85 and 100."},
    {"id": "R12", "text": "When top_count = 1 and top_bid >= 1, the player with committed = top_bid becomes auction_winner and adds their current_value to prize_points."},
    {"id": "R13", "text": "When top_count >= 2 (a tie for the highest bid), auction_winner = 'none' and nobody's prize_points change, although all players still pay their committed."},
    {"id": "R14", "text": "When top_bid = 0 (everyone bid 0), auction_winner = 'none' and nobody's prize_points change."},
    {"id": "R15", "text": "After resolution the auction_winner and every player's coins are announced, and every player's committed is reset to 0."},
    {"id": "R16", "text": "After the 6th auction, each player's final_score = coins + prize_points, and the game ends."},
    {"id": "R17", "text": "The player with the highest final_score wins, and players tied for the highest final_score share the win as a draw."}
  ],
  "offers": [
    {"question": "Talk message each auction", "who": "every seat", "options": "one short free-text message"},
    {"question": "Raise in each of the 3 raise stages", "who": "every seat", "options": "every whole number from 0 to (own coins - own committed). A seat with coins equal to committed is offered only 0."}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 3", "why": "The designer chose 3, and an auction needs at least two rivals for ties and bid-reading to matter. Above 5, the talk and announcements grow long and each player wins too few of the 6 auctions for budgeting to matter."},
    {"what": "Keep the simultaneous talk poll", "why": "The rules require it, and players genuinely disagree: everyone wants rivals to back off. Bluffs and threats about which auctions they value give players something to reason about, and since talk is not binding, believing it can be costly."},
    {"what": "prize_points visible only to its owner", "why": "The rules announce only the winner and coins. Publishing prize_points would reveal the winner's private value for that auction."},
    {"what": "Values entries indexed from 1", "why": "The rules say entry k is the value for auction k, and auction runs from 1 to 6."},
    {"what": "Strategy at the table", "why": "This is an all-pay auction, so overbidding is costly and ties waste both bids. A thoughtful player rations 100 coins over 6 auctions, pushes on high-value auctions, watches rivals' committed totals between stages, and avoids matching a rival's total."}
  ],
  "simplifications": [
    {"what": "The 3 raise stages are written out as explicit poll and tell steps rather than as a repeat", "why": "This keeps the flat step list clear without a scratch stage counter, and the behaviour is identical."},
    {"what": "final_score is computed in the last update of the 6th round", "why": "It is the same arithmetic as R10, placed just before the ending check."}
  ],
  "unsupported": []
}
```
````
