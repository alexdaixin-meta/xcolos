# 04 spec

- time: 2026-10-27T22:06:48+00:00 (40.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0e50b78d97a938d7, reply sha256 0b75aef8831b4eb4

## Sent

````
Game: Libertalia: Shared Hand
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP: 3 players, each with a score of 0 doubloons. The game has 2 campaigns of 5 days (10 rounds). At the start of each campaign every player receives the same 7-card hand: ranks 1 to 7, one card of each rank. Cards played are removed from the owner's hand. The 2 cards left after day 5 are discarded unused, and a fresh full hand is dealt for campaign 2. Which cards each player has played is public once revealed.

CHARACTERS:
- Rank 1, Cabin Boy: takes no booty. Gains 3 doubloons.
- Rank 2, Gunner: takes booty normally. Every other non-clashed player who played rank 6 or 7 loses 3 doubloons.
- Rank 3, Quartermaster: takes booty normally. Gains 1 doubloon for each other non-clashed player who played a higher rank.
- Rank 4, Bosun: takes booty normally. If the token taken is negative, it counts as 0.
- Rank 5, Merchant: takes booty normally. Gains 2 extra doubloons if the token taken is worth 3 or more.
- Rank 6, Captain: takes booty normally. No ability.
- Rank 7, Admiral: takes booty normally. Pays a wage: loses 2 doubloons.

BOOTY ROWS: each day one row is drawn at random, each equally likely, with replacement, from: A [5,3,1], B [5,1,-3], C [3,3,1], D [5,3,-3], E [3,1,-3], F [5,5,-3]. The values are the tokens, listed best to worst.

EACH DAY (ROUND):
1. Draw the booty row and announce it to all players.
2. Talk: everyone writes one short message at the same time. All messages are then shown to everyone. Messages are not binding.
3. All players secretly and simultaneously choose one card from their hand.
4. Reveal all cards.
5. Clash: if two or three players played the same rank, all of those players are clashed. They take no booty, their abilities do not fire, and their cards are still spent.
6. Booty: non-clashed players other than the Cabin Boy are ordered by rank, highest first. The first takes the best token, the second the next, and so on. Tokens left over are discarded.
7. Abilities of non-clashed characters resolve at the same time, as listed above. Gunner and Quartermaster count only non-clashed players.
8. Each player adds their token value plus or minus their ability effects to their score.
9. After day 5, discard leftover cards and deal fresh hands. After day 10, the game ends.

The Cabin Boy's +3 still applies when other players take booty. Scores can go negative.

How the winner is decided: After 10 rounds, the player with the highest doubloon total wins. If two or more players share the highest total, they draw.
````

## Reply

````
```json
{
  "name": "Libertalia: Shared Hand",
  "summary": "Three pirates play identical 7-card hands over 2 campaigns of 5 days, revealing one character a day at the same time to share out booty tokens and trigger abilities, while avoiding clashes on the same rank.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "players": 3,
    "campaigns": 2,
    "days_per_campaign": 5,
    "total_rounds": 10,
    "starting_score": 0,
    "hand_size": 7,
    "lowest_rank": 1,
    "highest_rank": 7,
    "cards_discarded_per_campaign": 2,
    "cabin_boy_rank": 1,
    "cabin_boy_gain": 3,
    "gunner_rank": 2,
    "gunner_penalty": 3,
    "gunner_target_min_rank": 6,
    "quartermaster_rank": 3,
    "quartermaster_bonus_per_higher": 1,
    "bosun_rank": 4,
    "bosun_floor": 0,
    "merchant_rank": 5,
    "merchant_bonus": 2,
    "merchant_threshold": 3,
    "captain_rank": 6,
    "admiral_rank": 7,
    "admiral_wage": 2,
    "row_count": 6,
    "tokens_per_row": 3,
    "row_A_1": 5, "row_A_2": 3, "row_A_3": 1,
    "row_B_1": 5, "row_B_2": 1, "row_B_3": -3,
    "row_C_1": 3, "row_C_2": 3, "row_C_3": 1,
    "row_D_1": 5, "row_D_2": 3, "row_D_3": -3,
    "row_E_1": 3, "row_E_2": 1, "row_E_3": -3,
    "row_F_1": 5, "row_F_2": 5, "row_F_3": -3
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "doubloons; may go negative", "observable": true},
      {"key": "hand", "type": "list", "visible": "public", "initial": [1, 2, 3, 4, 5, 6, 7], "meaning": "ranks still in hand this campaign; public because every hand starts identical and played cards are revealed", "observable": false},
      {"key": "card", "type": "number", "visible": "public", "initial": 0, "meaning": "rank played today, chosen secretly and revealed once all have chosen", "observable": true},
      {"key": "clashed", "type": "bool", "visible": "public", "initial": false, "meaning": "true if another player played the same rank today", "observable": true},
      {"key": "token", "type": "number", "visible": "public", "initial": 0, "meaning": "booty token value taken today, after the Bosun floor", "observable": false},
      {"key": "ability", "type": "number", "visible": "public", "initial": 0, "meaning": "net ability effect on this player today, including the Gunner penalty received", "observable": false},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "today's talk message", "observable": false}
    ],
    "game": [
      {"key": "day", "type": "number", "visible": "public", "initial": 0, "meaning": "current day, 1 to 10", "observable": true},
      {"key": "booty_rows", "type": "list", "visible": "public", "initial": [[5, 3, 1], [5, 1, -3], [3, 3, 1], [5, 3, -3], [3, 1, -3], [5, 5, -3]], "meaning": "rows A to F; one is drawn each day with replacement", "observable": false},
      {"key": "booty_row", "type": "list", "visible": "public", "initial": [], "meaning": "today's three tokens, best to worst", "observable": true}
    ]
  },
  "setup": [
    "Seat 3 players, each with score 0.",
    "Set day to 0.",
    "Give every player hand = [1,2,3,4,5,6,7] for campaign 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "day += 1; if day == 6, every player's hand is set to [1,2,3,4,5,6,7], which discards the 2 leftover cards and deals campaign 2; every player's card = 0, clashed = false, token = 0, ability = 0"},
    {"action": "update", "who": "all players", "answer": null, "effect": "booty_row = one entry of booty_rows picked at random, each equally likely, without removing it (with replacement); announce booty_row to all"},
    {"action": "poll", "who": "all players", "answer": "short text", "effect": "message = the text; then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}"},
    {"action": "poll", "who": "all players", "answer": "one rank from own hand", "effect": "card = the chosen rank; no answer is seen until all are in"},
    {"action": "update", "who": "all players", "answer": null, "effect": "remove card from hand; reveal every player's card to all"},
    {"action": "update", "who": "all players", "answer": null, "effect": "clashed = (number of other players whose card == you.card) >= 1"},
    {"action": "update", "who": "all players", "answer": null, "effect": "if not clashed and card >= 2: pos = 1 + number of other players with not clashed and card >= 2 and card > you.card; token = booty_row[pos]; if card == 4, token = max(token, 0); otherwise token = 0"},
    {"action": "update", "who": "all players", "answer": null, "effect": "ability = 0; if not clashed and card == 1: ability += 3; if not clashed and card == 3: ability += 1 * (number of other non-clashed players with card > 3); if not clashed and card == 5 and token >= 3: ability += 2; if not clashed and card == 7: ability -= 2; if not clashed and card >= 6 and some other non-clashed player has card == 2: ability -= 3"},
    {"action": "update", "who": "all players", "answer": null, "effect": "score += token + ability; announce each player's card, clashed, token, ability and score"},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game if day == 10, otherwise continue"}
  ],
  "ending": {
    "condition": "day == 10",
    "rank_by": "you.score",
    "decided_by": "Highest doubloon total after 10 days wins; players tied at the top share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup, each of the 3 players has score 0 and hand [1,2,3,4,5,6,7]."},
    {"id": "R2", "text": "Each day, booty_row is one of A [5,3,1], B [5,1,-3], C [3,3,1], D [5,3,-3], E [3,1,-3], F [5,5,-3], drawn with equal chance and with replacement, and announced before any choice."},
    {"id": "R3", "text": "Each day, every player first sends one short message at the same time, and all messages are shown to everyone."},
    {"id": "R4", "text": "Each day, every player secretly and simultaneously plays one rank from their hand, and that rank is removed from their hand."},
    {"id": "R5", "text": "When two or three players play the same rank, then all of them are clashed: token 0, no ability, and the card is still removed."},
    {"id": "R6", "text": "When a non-clashed player plays rank 2 to 7, then they take booty_row[1 + number of other non-clashed players with rank 2 to 7 and a higher rank]; for example, the higher of two such players takes the best token and the other takes the second."},
    {"id": "R7", "text": "When a non-clashed player plays rank 1 (Cabin Boy), then they take no token and gain 3."},
    {"id": "R8", "text": "When a non-clashed player plays rank 2 (Gunner), then every other non-clashed player who played rank 6 or 7 loses 3."},
    {"id": "R9", "text": "When a non-clashed player plays rank 3 (Quartermaster), then they gain 1 for each other non-clashed player who played a rank above 3."},
    {"id": "R10", "text": "When a non-clashed player plays rank 4 (Bosun) and takes a negative token, then the token counts as 0."},
    {"id": "R11", "text": "When a non-clashed player plays rank 5 (Merchant) and takes a token worth 3 or more, then they gain 2 extra."},
    {"id": "R12", "text": "When a non-clashed player plays rank 6 (Captain), then they take booty normally and have no ability."},
    {"id": "R13", "text": "When a non-clashed player plays rank 7 (Admiral), then they lose 2."},
    {"id": "R14", "text": "Each day, each player's score changes by token + ability, and a score may go negative."},
    {"id": "R15", "text": "When day 6 begins, every player's 2 leftover cards are discarded and their hand is reset to [1,2,3,4,5,6,7]."},
    {"id": "R16", "text": "When day 10 ends, the game ends, and the highest score wins, with tied leaders sharing the win."}
  ],
  "offers": [
    {"question": "talk message", "who": "all players", "options": "any short text"},
    {"question": "which card to play", "who": "all players", "options": "each seat: exactly the ranks still in its own hand (7 options on days 1 and 6, down to 3 options on days 5 and 10)"}
  ],
  "choices": [
    {"what": "3 players (min = max = suggested = 3)", "why": "The designer fixed 3. With 3 seats, clashes are a real risk and the three tokens are enough for everyone. A different count would change the token count and how clashes play out."},
    {"what": "Keep the simultaneous talk poll before the card poll", "why": "The rules require it. Players disagree, since each wants the others to avoid their rank, so a bluff or proposal is worth weighing, and messages are not binding."},
    {"what": "Hands are public attributes", "why": "All hands start identical and played cards are revealed, so the remaining hand can be worked out by everyone. Only the day's choice is secret, and the simultaneous poll keeps it so."},
    {"what": "Gunner penalty is a flat 3", "why": "Only one non-clashed Gunner can exist on a day, because two Gunners clash each other."}
  ],
  "simplifications": [
    {"what": "Booty rows are stored as a list of token lists, and the row is picked at random without removal", "why": "Drawing with replacement needs no deck depletion."},
    {"what": "Leftover tokens and discarded cards are not tracked", "why": "The rules never refer to them again."}
  ],
  "unsupported": []
}
```
````
