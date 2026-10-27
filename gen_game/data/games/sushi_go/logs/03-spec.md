# 03 spec

- time: 2026-10-27T16:40:09+00:00 (50.5s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 254ee52d991b607f, reply sha256 d9da6877ba85af6d

## Sent

````
Game: Sushi Draft
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
DECK (104 cards): 14 Tempura, 14 Sashimi, 14 Dumpling, 6 Maki-1 (1 maki icon), 12 Maki-2 (2 icons), 8 Maki-3 (3 icons), 10 Salmon Nigiri, 5 Squid Nigiri, 5 Egg Nigiri, 10 Pudding, 6 Wasabi.

SETUP: Shuffle the deck once at the start of the game. Every player starts with a score of 0 and 0 puddings. The game has 3 hands. Each hand has 9 picks with 3 players or 8 picks with 4 players, so the game lasts 27 or 24 rounds. One round is one pick.

EACH ROUND:
1. Deal (first pick of a hand only): deal each player a hand from the top of the deck, 9 cards with 3 players or 8 cards with 4 players. Undealt cards stay hidden and are not reshuffled.
2. Announce: everyone is told every player's face-up cards for this hand, every player's pudding count and score, and how many cards each hand holds. Each player is shown privately the cards in their own current hand.
3. Pick: all players at the same moment secretly choose one card from their own hand. If a hand holds one card, that card is taken automatically.
4. Reveal: all chosen cards are revealed at once and placed face up in front of their owners.
5. Record the chosen card:
   - Tempura adds 1 to your tempura count.
   - Sashimi adds 1 to your sashimi count.
   - Dumpling adds 1 to your dumpling count.
   - Maki adds its icons (1, 2 or 3) to your maki total.
   - Pudding adds 1 to your puddings, which are kept across all hands.
   - Wasabi adds 1 to your unused wasabi.
   - Nigiri is worth 1 (Egg), 2 (Salmon) or 3 (Squid). If you have at least 1 unused wasabi, the nigiri is placed on it: its value is tripled (3, 6 or 9) and your unused wasabi drops by 1. Add the nigiri's value to your nigiri points for this hand.
6. Pass: everyone passes their remaining hand to the player on their left.
7. Hand scoring (last pick of a hand only). Each player adds the following to their score:
   - Tempura: 5 points per complete pair, so floor(tempura/2) x 5.
   - Sashimi: 10 points per complete set of three, so floor(sashimi/3) x 10.
   - Dumplings: 0 for 0, 1 for 1, 3 for 2, 6 for 3, 10 for 4, and 15 for 5 or more.
   - Nigiri: all nigiri points for the hand. Unused wasabi scores 0.
   - Maki: among players with a maki total of at least 1, those with the highest total split 6 points equally, rounded down. If exactly one player has the highest total, the players with the second-highest total (at least 1) split 3 points equally, rounded down. If two or more players tie for highest, no second-place points are awarded.
   Then every hand-only count (tempura, sashimi, dumplings, maki, unused wasabi, nigiri points) resets to 0. Puddings stay.
8. Pudding scoring (last pick of the third hand only):
   - Players with the most puddings split +6 equally, rounded down.
   - Players with the fewest puddings split -6 equally, rounded toward zero (for example, two tied players get -3 each).
   - Players with 0 puddings count for the fewest.
   - If all players have the same number of puddings, nobody scores for pudding.
9. End check: after the last pick of the third hand, the game ends.

There is no talk phase.

How the winner is decided: After pudding scoring, the player with the highest score wins. If two or more players tie for the highest score, the one among them with the most puddings wins. If they are still tied, the game is a draw among those players.
````

## Reply

````
```json
{
  "name": "Sushi Draft",
  "summary": "A card-drafting game: each round every player secretly keeps one card from the hand they hold and passes the rest left. Sets of sushi score at the end of each of 3 hands, and puddings score at the end of the game.",
  "players": {"min": 3, "max": 4, "suggested": 4},
  "parameters": {
    "deck_size": 104,
    "count_tempura": 14,
    "count_sashimi": 14,
    "count_dumpling": 14,
    "count_maki_1": 6,
    "count_maki_2": 12,
    "count_maki_3": 8,
    "count_salmon_nigiri": 10,
    "count_squid_nigiri": 5,
    "count_egg_nigiri": 5,
    "count_pudding": 10,
    "count_wasabi": 6,
    "hands_per_game": 3,
    "hand_size_3_players": 9,
    "hand_size_4_players": 8,
    "rounds_3_players": 27,
    "rounds_4_players": 24,
    "maki_icons_1": 1,
    "maki_icons_2": 2,
    "maki_icons_3": 3,
    "egg_value": 1,
    "salmon_value": 2,
    "squid_value": 3,
    "wasabi_multiplier": 3,
    "tempura_set_size": 2,
    "tempura_set_points": 5,
    "sashimi_set_size": 3,
    "sashimi_set_points": 10,
    "dumpling_points_0": 0,
    "dumpling_points_1": 1,
    "dumpling_points_2": 3,
    "dumpling_points_3": 6,
    "dumpling_points_4": 10,
    "dumpling_points_5_plus": 15,
    "maki_first_points": 6,
    "maki_second_points": 3,
    "pudding_most_points": 6,
    "pudding_fewest_points": -6,
    "starting_score": 0,
    "starting_puddings": 0
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total points so far.", "observable": true},
      {"key": "puddings", "type": "number", "visible": "public", "initial": 0, "meaning": "Pudding cards collected. Kept across all hands.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards the player currently holds to pick from. Only the holder sees them.", "observable": false},
      {"key": "tableau", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up cards the player has chosen this hand.", "observable": false},
      {"key": "pick", "type": "text", "visible": "ally", "initial": "", "meaning": "The card secretly chosen this round, before the reveal.", "observable": false},
      {"key": "tempura", "type": "number", "visible": "public", "initial": 0, "meaning": "Tempura taken this hand.", "observable": false},
      {"key": "sashimi", "type": "number", "visible": "public", "initial": 0, "meaning": "Sashimi taken this hand.", "observable": false},
      {"key": "dumplings", "type": "number", "visible": "public", "initial": 0, "meaning": "Dumplings taken this hand.", "observable": false},
      {"key": "maki", "type": "number", "visible": "public", "initial": 0, "meaning": "Maki icons taken this hand.", "observable": false},
      {"key": "wasabi_unused", "type": "number", "visible": "public", "initial": 0, "meaning": "Wasabi taken this hand that no nigiri has been placed on yet.", "observable": false},
      {"key": "nigiri_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Nigiri value earned this hand, with the wasabi tripling already applied.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "the 104 cards listed in parameters, shuffled", "meaning": "Undealt cards. Hidden and never reshuffled.", "observable": false},
      {"key": "picks_per_hand", "type": "number", "visible": "public", "initial": "9 if 3 players, 8 if 4 players", "meaning": "Cards dealt per hand, which is also the number of picks per hand.", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current hand (1 to 3). It becomes 4 when the game is over.", "observable": true},
      {"key": "pick_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current pick within the hand, from 1 to picks_per_hand.", "observable": false}
    ]
  },
  "setup": [
    "Build the deck list from the 104 cards (14 Tempura, 14 Sashimi, 14 Dumpling, 6 Maki-1, 12 Maki-2, 8 Maki-3, 10 Salmon Nigiri, 5 Squid Nigiri, 5 Egg Nigiri, 10 Pudding, 6 Wasabi) and shuffle it once.",
    "Set picks_per_hand to 9 with 3 players or 8 with 4 players.",
    "Every player starts with score 0, puddings 0, an empty hand, an empty tableau and all hand counts at 0.",
    "Set hand_number to 1 and pick_number to 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When pick_number == 1: draw picks_per_hand cards at random from deck into each player's hand, removing each card from deck."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Announce to everyone each player's tableau, puddings and score, and the size of each hand. Show each player their own hand privately."},
    {"action": "poll", "who": "all players", "answer": "one card name from the player's own hand", "effect": "When the size of hand > 1: set pick to the chosen card. No one sees another player's pick until all have answered."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When the size of hand == 1: set pick to the single card in hand automatically."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Reveal: remove pick from hand, append it to tableau, and announce every player's pick to all."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Record pick. Tempura: tempura +1. Sashimi: sashimi +1. Dumpling: dumplings +1. Maki-1/2/3: maki +1/+2/+3. Pudding: puddings +1. Wasabi: wasabi_unused +1. Egg/Salmon/Squid Nigiri with base value v of 1, 2 or 3: if wasabi_unused >= 1, then nigiri_points += 3*v and wasabi_unused -= 1; otherwise nigiri_points += v."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Pass: each player's remaining hand moves to the player on their left (seat s gives its hand to seat s+1, and the last seat gives to seat 1)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When pick_number == picks_per_hand, add to score: floor(tempura/2)*5 + floor(sashimi/3)*10 + m*(m+1)/2 where m = min(dumplings,5) + nigiri_points. Maki: let M1 be the highest maki among players with maki >= 1, and k1 the number of players with maki == M1; each of them gains floor(6/k1). If k1 == 1, let M2 be the highest maki >= 1 below M1, and k2 the number of players with maki == M2; each of them gains floor(3/k2). Then set tempura, sashimi, dumplings, maki, wasabi_unused and nigiri_points to 0 and empty tableau. Puddings stay."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When pick_number == picks_per_hand and hand_number == 3, and not all players have equal puddings: players with puddings == max split +6, each gaining floor(6/count). Players with puddings == min (0 counts as fewest) split -6, each gaining -floor(6/count)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Advance: pick_number += 1. If pick_number > picks_per_hand, set pick_number to 1 and hand_number += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if hand_number > 3; otherwise continue with the next round."}
  ],
  "ending": {
    "condition": "hand_number > 3",
    "rank_by": "you.score * 100 + you.puddings",
    "decided_by": "Highest score wins. Among players tied on score, the one with the most puddings wins. Players still tied share the win, which is the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, the 104-card deck is shuffled once, and every player has score 0 and puddings 0."},
    {"id": "R2", "text": "When pick_number is 1, each player is dealt 9 cards (3 players) or 8 cards (4 players) from the deck into their hand, and those cards leave the deck."},
    {"id": "R3", "text": "Undealt cards stay in the hidden deck and are never reshuffled."},
    {"id": "R4", "text": "When a pick is made, all players choose at the same time, and no player sees another's choice until all have chosen."},
    {"id": "R5", "text": "When a player's hand holds exactly 1 card, that card is picked automatically, without a question."},
    {"id": "R6", "text": "When picks are revealed, each picked card leaves its owner's hand and is added face up to their tableau."},
    {"id": "R7", "text": "When Tempura is picked, tempura +1. When Sashimi is picked, sashimi +1. When Dumpling is picked, dumplings +1."},
    {"id": "R8", "text": "When Maki-1, Maki-2 or Maki-3 is picked, maki increases by 1, 2 or 3."},
    {"id": "R9", "text": "When Pudding is picked, puddings +1, and puddings are never reset between hands."},
    {"id": "R10", "text": "When Wasabi is picked, wasabi_unused +1."},
    {"id": "R11", "text": "When a nigiri is picked with wasabi_unused 0, nigiri_points increases by 1 (Egg), 2 (Salmon) or 3 (Squid)."},
    {"id": "R12", "text": "When a nigiri is picked with wasabi_unused >= 1, nigiri_points increases by 3 (Egg), 6 (Salmon) or 9 (Squid), and wasabi_unused decreases by 1."},
    {"id": "R13", "text": "When picks are recorded, each player's remaining hand passes to the player on their left."},
    {"id": "R14", "text": "When a hand ends, each player gains floor(tempura/2)*5 points (for example, 3 tempura gives 5)."},
    {"id": "R15", "text": "When a hand ends, each player gains floor(sashimi/3)*10 points (for example, 5 sashimi gives 10)."},
    {"id": "R16", "text": "When a hand ends, dumplings score 0/1/3/6/10/15 for 0/1/2/3/4/5-or-more dumplings."},
    {"id": "R17", "text": "When a hand ends, each player gains their nigiri_points, and unused wasabi scores 0."},
    {"id": "R18", "text": "When a hand ends, the players with the highest maki total (at least 1) split 6 points, each gaining floor(6/k)."},
    {"id": "R19", "text": "When a hand ends and exactly one player has the highest maki, the players with the second-highest maki (at least 1) split 3 points, each gaining floor(3/k)."},
    {"id": "R20", "text": "When two or more players tie for the highest maki, no second-place maki points are awarded."},
    {"id": "R21", "text": "When a player has maki 0, they score no maki points."},
    {"id": "R22", "text": "When a hand ends, tempura, sashimi, dumplings, maki, wasabi_unused, nigiri_points and tableau reset, while puddings stay."},
    {"id": "R23", "text": "When the third hand ends, the players with the most puddings split +6, each gaining floor(6/k)."},
    {"id": "R24", "text": "When the third hand ends, the players with the fewest puddings (0 counts as fewest) split -6, rounded toward zero (two tied players get -3 each)."},
    {"id": "R25", "text": "When the third hand ends and all players have equal puddings, nobody scores for pudding."},
    {"id": "R26", "text": "When the last pick of the third hand is done (pick 27 with 3 players, pick 24 with 4 players), the game ends."},
    {"id": "R27", "text": "When the game ends, the highest score wins, ties are broken by most puddings, and players still tied share the win."}
  ],
  "offers": [
    {"question": "Pick: choose one card from your hand", "who": "all players, when their hand holds 2 or more cards", "options": "each distinct card name currently in that player's own hand"},
    {"question": "Pick when the hand holds 1 card", "who": "no one is asked", "options": "none: the single card is taken automatically"}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 4", "why": "The designer suggests 4, and hand sizes are defined only for 3 and 4. At 3, passing still creates drafting tension. Above 4 the rules give no hand size."},
    {"what": "No talk phase", "why": "The source says there is no talk phase. Drafting is decided by reading the visible tableaus and passed hands."},
    {"what": "Strategy at the table", "why": "A thoughtful player tracks what others are collecting and what will come back around, denies key cards to rivals, times wasabi before high nigiri, and weighs the pudding race against points in each hand."},
    {"what": "Tie-break encoded as score*100 + puddings", "why": "There are at most 10 puddings, so puddings can never outweigh one point of score. Players still tied share the win, matching the source's draw."},
    {"what": "Dumpling table written as m*(m+1)/2 with m = min(dumplings,5)", "why": "This gives exactly 0, 1, 3, 6, 10, 15 and is pure arithmetic."}
  ],
  "simplifications": [
    {"what": "The left neighbour is the next seat number, wrapping to seat 1", "why": "The engine has no physical seating."},
    {"what": "Passing is done by rotating the hand lists between players in one update", "why": "The engine moves cards only through list operations."},
    {"what": "The automatic last pick is done as an update instead of a question", "why": "The rules take the single card without a choice."}
  ],
  "unsupported": []
}
```
````
