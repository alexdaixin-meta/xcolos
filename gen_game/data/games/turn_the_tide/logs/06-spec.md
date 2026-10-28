# 06 spec

- time: 2026-10-28T06:12:52+00:00 (29.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 e1730733c55731cf, reply sha256 c6de6b00f6f8a7f6

## Sent

````
Game: Turn The Tide: Short Seas (revised)
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP. Let P be the number of players (3 or 4). The Weather deck is the cards 1 to 12xP (1-36 for 3 players, 1-48 for 4), each number once. Shuffle it and deal 11 cards face down to each player as that player's hand. The remaining P cards are set aside face down and stay unseen for the whole game. Each player starts with a game score of 0. The game has P deals of 10 hands each, so 10xP hands in total. One round is one hand.

INFORMATION. You always see your own hand. Every Weather card becomes public the moment it is played and stays face up in front of whoever played it until the end of that deal. Unplayed cards and set-aside cards are never shown. So from deal 2 on, every player knows the cards of a passed hand that were played in earlier deals but not its unplayed card or cards, unless they held that hand themselves.

START OF EACH DEAL (before hand 1 of deals 1 to P):
- Shuffle a Tide deck of the cards 1 to 20.
- Set every player's Tide level to 15.
- Give every player 4 lifelines.
- Clear every player's Sunk status.
- From deal 2 on: each player takes all 10 Weather cards lying face up in front of them, plus the 1 card still in their hand, making 11 cards. They pass these 11 cards as a hand to the player on their left. The face-up rows are now empty. Over the P deals each player plays each of the P original hands exactly once.

EACH HAND (10 per deal):
1. Reveal the next two cards of the Tide deck to everyone. The smaller is Low Tide and the larger is High Tide.
2. Every player secretly chooses one Weather card from their hand. All choices are revealed at the same time and each card is placed face up in front of the player who played it.
3. The player who played the highest Weather card sets their Tide level to Low Tide. The player who played the second highest sets their Tide level to High Tide. All others keep their current Tide level. Weather numbers are unique, so there are no ties. Sunk players take part in this step like anyone else.
4. Among players who are NOT Sunk, find the highest Tide level. Every non-Sunk player at that level loses 1 lifeline. A player who must lose a lifeline while at 0 lifelines becomes Sunk instead. A Sunk player stays Sunk until the next deal, keeps playing cards and is ignored in this step. If every player is Sunk, nothing happens.
5. Announce all Weather cards played, all Tide levels, all lifelines and all Sunk statuses.

END OF EACH DEAL (after hand 10 of each deal), adjust each game score:
- Each player who is not Sunk adds their remaining lifelines (0 to 4).
- Each Sunk player subtracts 1.
- Among players who are not Sunk, the player or players with the lowest Tide level each add 1.
After each deal every player holds exactly 1 card, which is not shown to others.

There is no talk phase.

END. After deal P, the game ends and the winner is decided as in the objective.

How the winner is decided: After the last deal, the player with the highest game score wins. If several players tie for the highest score, the tied player with the lowest Tide level at the end of the last deal wins. If that is still tied, the game is a draw.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "Turn The Tide: Short Seas (revised)",
  "summary": "Over P deals of 10 hands, players play Weather cards at the same time to dodge high Tide levels and keep their lifelines. Each deal the hands pass to the left, and the highest total score wins.",
  "players": {"min": 3, "max": 4, "suggested": 4},
  "parameters": {
    "weather_cards_per_player": 12,
    "hand_size": 11,
    "hands_per_deal": 10,
    "tide_deck_size": 20,
    "tide_start_level": 15,
    "lifelines_per_deal": 4,
    "sunk_penalty": 1,
    "lowest_tide_bonus": 1,
    "deals": "P (number of players)",
    "set_aside_cards": "P (number of players)",
    "weather_deck_size": "12 * P"
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Game score summed over the deals.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Weather cards held and not yet played.", "observable": false},
      {"key": "played", "type": "list", "visible": "public", "initial": [], "meaning": "Weather cards this player has played face up in the current deal.", "observable": false},
      {"key": "card_played", "type": "number", "visible": "public", "initial": 0, "meaning": "Weather card played in the current hand.", "observable": false},
      {"key": "tide", "type": "number", "visible": "public", "initial": 15, "meaning": "Current Tide level.", "observable": true},
      {"key": "lifelines", "type": "number", "visible": "public", "initial": 4, "meaning": "Lifelines left in this deal.", "observable": true},
      {"key": "sunk", "type": "bool", "visible": "public", "initial": false, "meaning": "Sunk status for this deal.", "observable": true},
      {"key": "pass_buffer", "type": "list", "visible": "ally", "initial": [], "meaning": "The 11 cards gathered for passing to the left at the start of a deal.", "observable": false}
    ],
    "game": [
      {"key": "weather_deck", "type": "list", "visible": "none", "initial": "cards 1 to 12*P", "meaning": "Shuffled Weather deck used for dealing.", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "The P Weather cards set aside unseen for the whole game.", "observable": false},
      {"key": "tide_deck", "type": "list", "visible": "none", "initial": "cards 1 to 20", "meaning": "Tide deck, refilled at the start of each deal.", "observable": false},
      {"key": "low_tide", "type": "number", "visible": "public", "initial": 0, "meaning": "Smaller of the two Tide cards revealed this hand.", "observable": false},
      {"key": "high_tide", "type": "number", "visible": "public", "initial": 0, "meaning": "Larger of the two Tide cards revealed this hand.", "observable": false},
      {"key": "deal_no", "type": "number", "visible": "public", "initial": 1, "meaning": "Current deal, from 1 to P.", "observable": true},
      {"key": "hand_no", "type": "number", "visible": "public", "initial": 1, "meaning": "Current hand within the deal, from 1 to 10.", "observable": false},
      {"key": "max_tide", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch value: highest Tide level among non-Sunk players.", "observable": false},
      {"key": "min_tide", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch value: lowest Tide level among non-Sunk players at the end of a deal.", "observable": false}
    ]
  },
  "setup": [
    "Let P be the number of players (3 or 4).",
    "weather_deck is set to the cards 1 to 12*P, each number once.",
    "Each player draws 11 cards at random from weather_deck into hand, and each card is removed from weather_deck.",
    "The remaining P cards move from weather_deck to set_aside, which is never shown.",
    "Every score is 0, deal_no is 1 and hand_no is 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When hand_no == 1 and deal_no >= 2: each player's pass_buffer = played + hand; then each player's hand = pass_buffer of the player on their right (each player passes to the left); played = [] for everyone.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "When hand_no == 1: tide_deck = cards 1 to 20; every tide = 15; every lifelines = 4; every sunk = false.", "judged": null},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When hand_no == 1, each player is sent their hand, along with deal_no and all public attributes.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "Draw 2 cards at random from tide_deck and remove them from it; low_tide = the smaller, high_tide = the larger.", "judged": null},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Deal {deal_no}, hand {hand_no}: Low Tide {low_tide}, High Tide {high_tide}.'", "judged": null},
    {"action": "poll", "who": "all players", "answer": "one card from your hand", "effect": "Each player's card_played = the chosen card; it is removed from hand and appended to played. All are revealed together.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "The player with the highest card_played sets tide = low_tide. The player with the second-highest card_played sets tide = high_tide. Sunk players are included. Everyone else keeps their tide.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "max_tide = the highest tide among players with sunk == false. For each player with sunk == false and tide == max_tide: if lifelines == 0 then sunk = true, else lifelines -= 1. If every player is Sunk, nothing changes.", "judged": null},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every card_played, tide, lifelines and sunk.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "When hand_no == 10: each player with sunk == false adds lifelines to score; each player with sunk == true subtracts 1 from score; min_tide = the lowest tide among players with sunk == false; each player with sunk == false and tide == min_tide adds 1 to score.", "judged": null},
    {"action": "update", "who": "table", "answer": null, "effect": "hand_no += 1; if hand_no > 10 then hand_no = 1 and deal_no += 1.", "judged": null},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game when deal_no > P; otherwise continue.", "judged": null}
  ],
  "ending": {
    "condition": "deal_no > P (number of players)",
    "rank_by": "you.score * 100 - you.tide",
    "decided_by": "The highest game score wins. A tie is broken by the lowest Tide level at the end of the last deal. Players still level on both share the win, which stands in for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "At setup, the Weather deck is the cards 1 to 12*P, each player is dealt 11 cards into hand, and the remaining P cards go to set_aside and are never shown."},
    {"id": "R2", "text": "At setup, every score is 0."},
    {"id": "R3", "text": "At the start of every deal, tide_deck is reset to 1 to 20, every tide is 15, every lifelines is 4 and every sunk is false."},
    {"id": "R4", "text": "At the start of deals 2 to P, each player's played cards plus their 1 remaining card (11 cards) pass to the player on their left as that player's hand, and played becomes empty."},
    {"id": "R5", "text": "Each hand, two Tide cards are drawn from tide_deck; the smaller is low_tide and the larger is high_tide."},
    {"id": "R6", "text": "Each hand, every player chooses one card from hand at the same time; it is removed from hand, appended to played and revealed."},
    {"id": "R7", "text": "The player who played the highest Weather card sets tide = low_tide, and the player who played the second highest sets tide = high_tide; this includes Sunk players."},
    {"id": "R8", "text": "Every non-Sunk player whose tide equals the highest tide among non-Sunk players loses 1 lifeline; a player at 0 lifelines who must lose one becomes Sunk instead."},
    {"id": "R9", "text": "A Sunk player stays Sunk until the next deal, still plays cards and is ignored when lifelines are lost; if all players are Sunk, no lifelines are lost."},
    {"id": "R10", "text": "After hand 10 of a deal, each non-Sunk player adds their lifelines (0 to 4) to score."},
    {"id": "R11", "text": "After hand 10 of a deal, each Sunk player subtracts 1 from score."},
    {"id": "R12", "text": "After hand 10 of a deal, each non-Sunk player whose tide is the lowest among non-Sunk players adds 1 to score."},
    {"id": "R13", "text": "A deal has 10 hands and the game ends after deal P."},
    {"id": "R14", "text": "The highest score wins; a tie is broken by the lowest final tide; players still level share the win."}
  ],
  "offers": [
    {"question": "Choose a Weather card to play this hand", "who": "every seat", "options": "Exactly the cards currently in that seat's hand: 11 options on hand 1 of a deal, down to 2 on hand 10."}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 4", "why": "The designer suggests 4 and the deck size and deal count scale with P. Fewer than 3 makes the highest and second-highest cards decide everyone's Tide. More than 4 is outside the deck design."},
    {"what": "No talk phase", "why": "The rules state there is no talk phase."},
    {"what": "Tie-break encoded as score*100 - tide", "why": "Tide is between 1 and 20, so it never outweighs a point of score, and a lower tide ranks higher."},
    {"what": "Hand passing modelled with a pass_buffer list", "why": "All players pass at once, so each 11-card set is gathered first and then moved to the left-hand neighbour."}
  ],
  "simplifications": [
    {"what": "The source's draw becomes a shared win", "why": "The engine has no separate draw: players level at the top share the win."},
    {"what": "Start-of-deal and end-of-deal work is done by steps conditioned on hand_no", "why": "The step list is flat, so these steps run every round but act only on hand 1 or hand 10."}
  ],
  "unsupported": []
}
```

Why it was refused: parameters must map each name to a number
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "Turn The Tide: Short Seas (revised)",
  "summary": "Over P deals of 10 hands, players play Weather cards at the same time to dodge high Tide levels and keep their lifelines. Each deal the hands pass to the left, and the highest total score wins.",
  "players": {"min": 3, "max": 4, "suggested": 4},
  "parameters": {
    "weather_cards_per_player": 12,
    "hand_size": 11,
    "hands_per_deal": 10,
    "tide_deck_size": 20,
    "tide_start_level": 15,
    "lifelines_per_deal": 4,
    "sunk_penalty": 1,
    "lowest_tide_bonus": 1,
    "deals_per_player": 1,
    "set_aside_cards_per_player": 1,
    "tie_break_weight": 100
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Game score summed over the deals.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Weather cards held and not yet played.", "observable": false},
      {"key": "played", "type": "list", "visible": "public", "initial": [], "meaning": "Weather cards this player has played face up in the current deal.", "observable": false},
      {"key": "card_played", "type": "number", "visible": "public", "initial": 0, "meaning": "Weather card played in the current hand.", "observable": false},
      {"key": "tide", "type": "number", "visible": "public", "initial": 15, "meaning": "Current Tide level.", "observable": true},
      {"key": "lifelines", "type": "number", "visible": "public", "initial": 4, "meaning": "Lifelines left in this deal.", "observable": true},
      {"key": "sunk", "type": "bool", "visible": "public", "initial": false, "meaning": "Sunk status for this deal.", "observable": true},
      {"key": "pass_buffer", "type": "list", "visible": "ally", "initial": [], "meaning": "The 11 cards gathered for passing to the left at the start of a deal.", "observable": false}
    ],
    "game": [
      {"key": "weather_deck", "type": "list", "visible": "none", "initial": "cards 1 to 12*P", "meaning": "Shuffled Weather deck used for dealing.", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "The P Weather cards set aside unseen for the whole game.", "observable": false},
      {"key": "tide_deck", "type": "list", "visible": "none", "initial": "cards 1 to 20", "meaning": "Tide deck, refilled at the start of each deal.", "observable": false},
      {"key": "low_tide", "type": "number", "visible": "public", "initial": 0, "meaning": "Smaller of the two Tide cards revealed this hand.", "observable": false},
      {"key": "high_tide", "type": "number", "visible": "public", "initial": 0, "meaning": "Larger of the two Tide cards revealed this hand.", "observable": false},
      {"key": "deal_no", "type": "number", "visible": "public", "initial": 1, "meaning": "Current deal, from 1 to P.", "observable": true},
      {"key": "hand_no", "type": "number", "visible": "public", "initial": 1, "meaning": "Current hand within the deal, from 1 to 10.", "observable": false},
      {"key": "max_tide", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch value: highest Tide level among non-Sunk players.", "observable": false},
      {"key": "min_tide", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch value: lowest Tide level among non-Sunk players at the end of a deal.", "observable": false}
    ]
  },
  "setup": [
    "Let P be the number of players (3 or 4).",
    "weather_deck is set to the cards 1 to 12*P, each number once.",
    "Each player draws 11 cards at random from weather_deck into hand, and each card is removed from weather_deck.",
    "The remaining P cards move from weather_deck to set_aside, which is never shown.",
    "Every score is 0, deal_no is 1 and hand_no is 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When hand_no == 1 and deal_no >= 2: each player's pass_buffer = played + hand; then each player's hand = pass_buffer of the player on their right (each player passes to the left); played = [] for everyone.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "When hand_no == 1: tide_deck = cards 1 to 20; every tide = 15; every lifelines = 4; every sunk = false.", "judged": null},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When hand_no == 1, each player is sent their hand, along with deal_no and all public attributes.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "Draw 2 cards at random from tide_deck and remove them from it; low_tide = the smaller, high_tide = the larger.", "judged": null},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Deal {deal_no}, hand {hand_no}: Low Tide {low_tide}, High Tide {high_tide}.'", "judged": null},
    {"action": "poll", "who": "all players", "answer": "one card from your hand", "effect": "Each player's card_played = the chosen card; it is removed from hand and appended to played. All are revealed together.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "The player with the highest card_played sets tide = low_tide. The player with the second-highest card_played sets tide = high_tide. Sunk players are included. Everyone else keeps their tide.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "max_tide = the highest tide among players with sunk == false. For each player with sunk == false and tide == max_tide: if lifelines == 0 then sunk = true, else lifelines -= 1. If every player is Sunk, nothing changes.", "judged": null},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every card_played, tide, lifelines and sunk.", "judged": null},
    {"action": "update", "who": "all players", "answer": null, "effect": "When hand_no == 10: each player with sunk == false adds lifelines to score; each player with sunk == true subtracts 1 from score; min_tide = the lowest tide among players with sunk == false; each player with sunk == false and tide == min_tide adds 1 to score.", "judged": null},
    {"action": "update", "who": "table", "answer": null, "effect": "hand_no += 1; if hand_no > 10 then hand_no = 1 and deal_no += 1.", "judged": null},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game when deal_no > P; otherwise continue.", "judged": null}
  ],
  "ending": {
    "condition": "deal_no > P (number of players)",
    "rank_by": "you.score * 100 - you.tide",
    "decided_by": "The highest game score wins. A tie is broken by the lowest Tide level at the end of the last deal. Players still level on both share the win, which stands in for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "At setup, the Weather deck is the cards 1 to 12*P, each player is dealt 11 cards into hand, and the remaining P cards go to set_aside and are never shown."},
    {"id": "R2", "text": "At setup, every score is 0."},
    {"id": "R3", "text": "At the start of every deal, tide_deck is reset to 1 to 20, every tide is 15, every lifelines is 4 and every sunk is false."},
    {"id": "R4", "text": "At the start of deals 2 to P, each player's played cards plus their 1 remaining card (11 cards) pass to the player on their left as that player's hand, and played becomes empty."},
    {"id": "R5", "text": "Each hand, two Tide cards are drawn from tide_deck; the smaller is low_tide and the larger is high_tide."},
    {"id": "R6", "text": "Each hand, every player chooses one card from hand at the same time; it is removed from hand, appended to played and revealed."},
    {"id": "R7", "text": "The player who played the highest Weather card sets tide = low_tide, and the player who played the second highest sets tide = high_tide; this includes Sunk players."},
    {"id": "R8", "text": "Every non-Sunk player whose tide equals the highest tide among non-Sunk players loses 1 lifeline; a player at 0 lifelines who must lose one becomes Sunk instead."},
    {"id": "R9", "text": "A Sunk player stays Sunk until the next deal, still plays cards and is ignored when lifelines are lost; if all players are Sunk, no lifelines are lost."},
    {"id": "R10", "text": "After hand 10 of a deal, each non-Sunk player adds their lifelines (0 to 4) to score."},
    {"id": "R11", "text": "After hand 10 of a deal, each Sunk player subtracts 1 from score."},
    {"id": "R12", "text": "After hand 10 of a deal, each non-Sunk player whose tide is the lowest among non-Sunk players adds 1 to score."},
    {"id": "R13", "text": "A deal has 10 hands and the game ends after deal P."},
    {"id": "R14", "text": "The highest score wins; a tie is broken by the lowest final tide; players still level share the win."}
  ],
  "offers": [
    {"question": "Choose a Weather card to play this hand", "who": "every seat", "options": "Exactly the cards currently in that seat's hand: 11 options on hand 1 of a deal, down to 2 on hand 10."}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 4", "why": "The designer suggests 4, and the deck size and deal count scale with P. With fewer than 3 players, the highest and second-highest cards decide everyone's Tide. More than 4 is outside the deck design."},
    {"what": "No talk phase", "why": "The rules state there is no talk phase."},
    {"what": "Tie-break encoded as score*100 - tide", "why": "Tide is between 1 and 20, so it never outweighs a point of score, and a lower tide ranks higher."},
    {"what": "Hand passing modelled with a pass_buffer list", "why": "All players pass at once, so each 11-card set is gathered first and then moved to the left-hand neighbour."},
    {"what": "Count-dependent numbers written per player (weather_cards_per_player 12, deals_per_player 1, set_aside_cards_per_player 1)", "why": "Parameters must be plain numbers. The Weather deck is 12*P cards, there are 1*P deals and 1*P cards set aside, so each holds at 3 and at 4 players."}
  ],
  "simplifications": [
    {"what": "The source's draw becomes a shared win", "why": "The engine has no separate draw: players level at the top share the win."},
    {"what": "Start-of-deal and end-of-deal work is done by steps conditioned on hand_no", "why": "The step list is flat, so these steps run every round but act only on hand 1 or hand 10."}
  ],
  "unsupported": []
}
```
````
