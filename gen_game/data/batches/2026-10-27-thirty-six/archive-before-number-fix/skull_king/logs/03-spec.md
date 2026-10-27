# 03 spec

- time: 2026-10-27T17:56:26+00:00 (42.0s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 a43bb82209312aba, reply sha256 4a48a4cf83590831

## Sent

````
Game: Skull King: Three-Card Raids
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
DECK (18 cards, each with a power value): number cards 1 through 12 (power equals the number); Escape x2 (power 0); Mermaid x1 (power 20); Pirate A (power 30); Pirate B (power 31); Skull King x1 (power 40).

SETUP: Every player starts at 0 points. The game lasts exactly 8 rounds.

EACH ROUND:
1. DEAL (the round's only random event): Shuffle all 18 cards and deal 3 to each player, privately. The remaining cards stay face down and unseen for the whole round.
2. BID: All players at the same time secretly choose a bid of 0, 1, 2 or 3 (how many tricks they will win this round).
3. REVEAL BIDS: All bids are announced to everyone.
4. TRICK 1: All players at the same time choose one card from their hand to play. All played cards are revealed together and removed from hands.
5. RESOLVE TRICK 1: If the Mermaid and the Skull King were both played, the Mermaid's player wins the trick. Otherwise the card with the highest power wins the trick. If every card played has power 0 (all Escapes), nobody wins the trick. Add 1 to the winner's tricks-won count. Capture bonuses are recorded for the winner: if the Skull King won, count the Pirates in the trick (each is worth a +20 bonus); if the Mermaid won and the Skull King is in the trick, record a +40 bonus. Announce the winner.
6. TRICK 2 and RESOLVE TRICK 2: same as steps 4 and 5.
7. TRICK 3 and RESOLVE TRICK 3: same as steps 4 and 5 (each player plays their last card).
8. SCORING, for each player:
   - Bid 0 and won 0 tricks: +30.
   - Bid 0 and won 1 or more tricks: -30.
   - Bid k of 1 or more and won exactly k tricks: +20 times k, plus all capture bonuses that player recorded this round.
   - Bid k of 1 or more and won a different number: -10 times the absolute difference between bid and tricks won. No bonuses.
   - Capture bonuses are paid only on an exact bid (zero bids cannot have bonuses, since bonuses require winning a trick).
9. ANNOUNCE: Each player's tricks won, points this round and running total are announced. Reset tricks won and bonuses to 0.
10. END CHECK: After round 8 the game ends.

INFORMATION: Your own hand is private. Bids, every played card, trick winners and scores are public. There is no talk phase.

How the winner is decided: After 8 rounds, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Skull King: Three-Card Raids",
  "summary": "Eight rounds of three simultaneous tricks: secretly bid how many tricks you will win, then play cards from a private 3-card hand. Exact bids score and pay capture bonuses.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "deck_size": 18,
    "hand_size": 3,
    "tricks_per_round": 3,
    "rounds": 8,
    "bid_min": 0,
    "bid_max": 3,
    "number_card_min": 1,
    "number_card_max": 12,
    "escape_count": 2,
    "escape_power": 0,
    "mermaid_count": 1,
    "mermaid_power": 20,
    "pirate_a_power": 30,
    "pirate_b_power": 31,
    "skull_king_count": 1,
    "skull_king_power": 40,
    "zero_bid_success_points": 30,
    "zero_bid_fail_points": -30,
    "exact_bid_points_per_trick": 20,
    "missed_bid_points_per_trick_off": -10,
    "pirate_capture_bonus": 20,
    "skull_king_capture_bonus": 40,
    "starting_score": 0,
    "tricks_won_per_trick": 1
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "running total of points", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "the player's private cards, each written as its power value (Escape 0, numbers 1-12, Mermaid 20, Pirate A 30, Pirate B 31, Skull King 40)", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "tricks the player bid this round, 0-3; it stays secret until all bids are revealed together", "observable": true},
      {"key": "tricks_won", "type": "number", "visible": "public", "initial": 0, "meaning": "tricks won so far this round", "observable": true},
      {"key": "bonus", "type": "number", "visible": "public", "initial": 0, "meaning": "capture bonus points recorded this round", "observable": false},
      {"key": "played", "type": "number", "visible": "public", "initial": -1, "meaning": "power of the card played in the current trick; it is revealed when all cards are in", "observable": true},
      {"key": "round_points", "type": "number", "visible": "public", "initial": 0, "meaning": "points scored this round", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40], "meaning": "the 18 cards as power values; the undealt cards stay face down and unseen", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round number, 1-8", "observable": true},
      {"key": "trick_number", "type": "number", "visible": "public", "initial": 0, "meaning": "current trick within the round, 1-3", "observable": false},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "seat that won the last trick, or 0 if nobody won", "observable": true}
    ]
  },
  "setup": [
    "Every player's score is set to 0.",
    "round is set to 0.",
    "The game will last exactly 8 rounds."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; trick_number = 0; deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]; every hand = []; every tricks_won = 0; every bonus = 0; every round_points = 0"},
    {"action": "update", "who": "all players", "answer": null, "effect": "Deal: 3 times for each player, pick a random card from deck, append it to that player's hand and remove it from deck. This is the round's only random event."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "each player privately sees their own hand"},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to 3", "effect": "bid = answer; no bid is shown until all are in"},
    {"action": "tell", "who": "all players", "answer": null, "effect": "announce every player's bid"},
    {"action": "update", "who": "all players", "answer": null, "effect": "trick_number += 1; every played = -1; trick_winner = 0"},
    {"action": "poll", "who": "all players", "answer": "one card from own hand (a power value in hand)", "effect": "played = answer; remove one copy of answer from hand; nobody sees a card until all are in"},
    {"action": "tell", "who": "all players", "answer": null, "effect": "reveal every player's played card"},
    {"action": "update", "who": "all players", "answer": null, "effect": "if some player played 20 and some player played 40: trick_winner = seat with played == 20; else if max(played) > 0: trick_winner = seat with played == max(played) (unique, since only the Escapes share a power); else trick_winner = 0. If trick_winner != 0: that player's tricks_won += 1. If the winner played 40: winner's bonus += 20 * (count of players with played == 30 or played == 31). If the winner played 20 and some player played 40: winner's bonus += 40."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "announce trick_winner (or that nobody won) and any bonus recorded"},
    {"action": "repeat", "who": "all players", "answer": null, "effect": "run the trick steps again (from 'trick_number += 1' through the trick announcement) until trick_number == 3"},
    {"action": "update", "who": "all players", "answer": null, "effect": "for each player: if bid == 0 and tricks_won == 0: round_points = 30; if bid == 0 and tricks_won >= 1: round_points = -30; if bid >= 1 and tricks_won == bid: round_points = 20 * bid + bonus; if bid >= 1 and tricks_won != bid: round_points = -10 * abs(bid - tricks_won). Then score += round_points."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "announce each player's tricks_won, round_points and score"},
    {"action": "update", "who": "all players", "answer": null, "effect": "every tricks_won = 0; every bonus = 0"},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game if round == 8, otherwise continue"}
  ],
  "ending": {
    "condition": "round == 8 after the round's scoring",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 8 rounds. The highest total wins; players tied for the highest total share the result, which is the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player's score is 0."},
    {"id": "R2", "text": "When a round starts, then the full 18-card deck (numbers 1-12, two Escapes of power 0, Mermaid 20, Pirate A 30, Pirate B 31, Skull King 40) is shuffled and each player receives exactly 3 cards in their private hand."},
    {"id": "R3", "text": "When cards are dealt, then the undealt cards stay in deck and are never revealed that round."},
    {"id": "R4", "text": "When players bid, then each chooses simultaneously a whole number from 0 to 3, and all bids are revealed only after all are in."},
    {"id": "R5", "text": "When a trick is played, then each player simultaneously plays one card from their own hand, and that card is removed from the hand and revealed to all."},
    {"id": "R6", "text": "When both the Mermaid (20) and the Skull King (40) are played in a trick, then the Mermaid's player wins the trick."},
    {"id": "R7", "text": "When the Mermaid and the Skull King are not both in a trick and some card has power above 0, then the player of the highest-power card wins the trick."},
    {"id": "R8", "text": "When every card played in a trick has power 0, then nobody wins the trick and no tricks_won changes."},
    {"id": "R9", "text": "When a player wins a trick, then their tricks_won increases by 1."},
    {"id": "R10", "text": "When the Skull King wins a trick, then its player records a bonus of +20 for each Pirate (30 or 31) in that trick."},
    {"id": "R11", "text": "When the Mermaid wins a trick containing the Skull King, then its player records a +40 bonus."},
    {"id": "R12", "text": "When a player bid 0 and won 0 tricks, then they score +30 for the round."},
    {"id": "R13", "text": "When a player bid 0 and won 1 or more tricks, then they score -30 for the round."},
    {"id": "R14", "text": "When a player bid k >= 1 and won exactly k tricks, then they score 20*k plus all bonuses recorded that round."},
    {"id": "R15", "text": "When a player bid k >= 1 and won a different number of tricks t, then they score -10*|k - t| and no bonuses."},
    {"id": "R16", "text": "When a round's scoring ends, then each player's tricks_won, round points and score are announced, and tricks_won and bonus reset to 0."},
    {"id": "R17", "text": "When round 8 has been scored, then the game ends and the highest score wins; players tied for the highest score share the result (a draw)."},
    {"id": "R18", "text": "When any phase of the game runs, then there is no talk phase."}
  ],
  "offers": [
    {"question": "Bid", "who": "all players, simultaneously", "options": "any whole number 0, 1, 2 or 3"},
    {"question": "Trick 1 card", "who": "all players, simultaneously", "options": "any of the 3 cards in the player's own hand"},
    {"question": "Trick 2 card", "who": "all players, simultaneously", "options": "any of the 2 cards remaining in the player's own hand"},
    {"question": "Trick 3 card", "who": "all players, simultaneously", "options": "the 1 card remaining in the player's own hand"}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer chose 4. Three is the smallest table where tricks are contested enough for bidding to be hard. Five is the cap because 15 of the 18 cards are dealt, and more seats would exhaust the deck."},
    {"what": "Cards are stored as their power values", "why": "Every card except the two Escapes has a unique power, so the value identifies the card, and resolving a trick is plain arithmetic on played."},
    {"what": "Trick steps are written once and run again with repeat until trick_number == 3", "why": "The three tricks are identical in the source."},
    {"what": "No talk step", "why": "The source states there is no talk phase."},
    {"what": "Strategy at the table", "why": "A thoughtful player bids from hand strength and from what others' bids imply. During tricks they dump Escapes or low cards to hit a bid exactly, or hold the Mermaid back to catch the Skull King."}
  ],
  "simplifications": [
    {"what": "A tie for the highest total is a shared win rather than a separate 'draw' outcome", "why": "The engine has no separate draw; players level at the top share the win, which is equivalent."}
  ],
  "unsupported": []
}
```
````
