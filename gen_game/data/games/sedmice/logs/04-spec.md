# 04 spec

- time: 2026-10-28T03:34:25+00:00 (48.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 a7d48c207cfa7847, reply sha256 254e6e8f4c2d8541

## Sent

````
Game: Sedmice Duel
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS: 32 cards, four each of the ranks 7, 8, 9, 10, J, Q, K, A. Suits do not matter. Aces and Tens are point cards worth 10 each. Sevens are wild.

MATCH: 4 deals. Each deal lasts up to 8 rounds, so the match has 32 rounds. Each round is one trick.

DEALING (first round of each deal): Shuffle the full deck. Each player receives exactly one Seven, one Ace and one Ten. Shuffle the remaining 26 cards and deal 5 more to each player, so each hand has 8 cards. Hands are private. The 16 undealt cards are set aside face down and are never revealed or used in that deal. Both players know the dealing rule.

FIRST LEAD: Player A leads first in deals 1 and 3. Player B leads first in deals 2 and 4. After that, the winner of each trick leads the next one.

A TRICK:
(1) The leader plays any card face up. Its rank is the 'led rank'.
(2) The follower plays any card face up. If it matches the led rank or is a Seven, the follower is currently winning. Otherwise the leader wins the trick and it ends.
(3) If the follower is currently winning, the leader may extend once by playing a second card that matches the led rank or is a Seven. The leader may also decline. If the leader declines or has no such card, the follower wins the trick.
(4) If the leader extended, the follower must play a second card (any card). If it matches the led rank or is a Seven, the follower wins the trick. Otherwise the leader wins.
A trick can never be extended more than once.

AFTER EACH TRICK: All cards played in the trick are announced. The winner scores 10 points for each Ace and each Ten among them. Both players always play the same number of cards, so both hands empty together. If the hands are now empty, the winner of this trick also scores 10 points for the last trick, and the deal ends. Any remaining rounds of that deal are skipped. A deal lasts 4 to 8 tricks.

INFORMATION: Each player sees their own hand and every card played. Neither sees the opponent's hand or the set-aside cards.

How the winner is decided: After 4 deals, the player with the higher total points across all deals wins. Equal totals are a draw.
````

## Reply

````
```json
{
  "name": "Sedmice Duel",
  "summary": "A two-player trick-taking duel over 4 deals of 8-card hands. Sevens are wild, Aces and Tens score 10 each, and the leader may extend a trick once to win it back.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 32,
    "copies_per_rank": 4,
    "point_card_value": 10,
    "deals": 4,
    "max_rounds_per_deal": 8,
    "total_rounds": 32,
    "guaranteed_cards_per_player": 3,
    "extra_cards_dealt_per_player": 5,
    "hand_size": 8,
    "set_aside_cards": 16,
    "last_trick_bonus": 10,
    "max_extensions_per_trick": 1,
    "min_tricks_per_deal": 4
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Ranks of the cards this player holds in the current deal ('7','8','9','10','J','Q','K','A').", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total points across all deals.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Cards not yet dealt during dealing: 4 copies of each of 7,8,9,10,J,Q,K,A.", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "The 16 undealt cards of the current deal. They are never revealed or used.", "observable": false},
      {"key": "deal_number", "type": "number", "visible": "public", "initial": 1, "meaning": "Current deal, from 1 to 4. It becomes 5 when the match is over.", "observable": true},
      {"key": "new_deal", "type": "bool", "visible": "public", "initial": true, "meaning": "True when the next trick is the first of a deal, so cards must be dealt.", "observable": false},
      {"key": "leader", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that leads the current trick (seat 1 = Player A, seat 2 = Player B).", "observable": false},
      {"key": "led_rank", "type": "text", "visible": "public", "initial": "", "meaning": "Rank of the card the leader played first in this trick.", "observable": false},
      {"key": "follower_winning", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the follower is currently winning the trick.", "observable": false},
      {"key": "extended", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the leader extended this trick.", "observable": false},
      {"key": "trick_cards", "type": "list", "visible": "public", "initial": [], "meaning": "All cards played face up in the current trick.", "observable": true},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won the latest trick.", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 is Player A and seat 2 is Player B.",
    "Both scores start at 0, deal_number is 1 and new_deal is true.",
    "Both players are told the dealing rule: each hand gets exactly one Seven, one Ace and one Ten, plus 5 random cards from the remaining 26."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "when": "game.new_deal == true",
     "effect": "Set deck to the full 32 cards (four each of 7,8,9,10,J,Q,K,A). Set each hand to empty. For each player, move one '7', one 'A' and one '10' from deck to hand. Then draw 5 cards at random from deck into each hand, so each hand has 8 cards. Move the 16 remaining deck cards to set_aside. Set leader = 1 if deal_number is 1 or 3, else 2. Set new_deal = false."},
    {"action": "sync", "who": "all players", "answer": null, "when": "trick_cards is empty",
     "effect": "Each player sees their own hand, both scores, deal_number and who leads."},
    {"action": "ask", "who": "the leader (seat game.leader)", "answer": "one card from your hand",
     "effect": "Remove the card from the leader's hand, append it to trick_cards and set led_rank to its rank."},
    {"action": "ask", "who": "the follower (the seat that is not game.leader)", "answer": "one card from your hand",
     "effect": "Remove the card from the follower's hand and append it to trick_cards. Set follower_winning = (card == led_rank or card == '7')."},
    {"action": "ask", "who": "the leader (seat game.leader)", "answer": "decline, or one card from your hand whose rank is led_rank or '7'",
     "when": "follower_winning == true and the leader's hand contains led_rank or '7'",
     "effect": "If a card is chosen: remove it from the leader's hand, append it to trick_cards and set extended = true. If declined: nothing changes."},
    {"action": "ask", "who": "the follower (the seat that is not game.leader)", "answer": "one card from your hand", "when": "extended == true",
     "effect": "Remove the card from the follower's hand and append it to trick_cards. Set follower_winning = (card == led_rank or card == '7')."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Set trick_winner = the follower if follower_winning is true, else leader. The trick winner's score += 10 × (count of 'A' in trick_cards + count of '10' in trick_cards). Announce trick_cards, the winner and the points scored."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "If both hands are empty: the trick winner's score += last_trick_bonus (10), clear set_aside, deal_number += 1 and new_deal = true. Otherwise leader = trick_winner. Announce the result."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Reset for the next trick: trick_cards = [], led_rank = '', follower_winning = false, extended = false."},
    {"action": "check", "who": "all players", "answer": null,
     "effect": "End the game if deal_number > 4; otherwise continue."}
  ],
  "ending": {
    "condition": "game.deal_number > 4",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total points across the 4 deals. The higher total wins, and equal totals share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "The deck has 32 cards, four each of 7, 8, 9, 10, J, Q, K and A, and suits do not matter."},
    {"id": "R2", "text": "When a deal starts, each player receives exactly one 7, one A and one 10, then 5 random cards from the remaining 26, for a hand of 8."},
    {"id": "R3", "text": "When a deal has been dealt, the 16 undealt cards go to set_aside and are never revealed or played that deal."},
    {"id": "R4", "text": "When deal 1 or deal 3 starts, seat 1 (Player A) leads the first trick. When deal 2 or deal 4 starts, seat 2 (Player B) leads."},
    {"id": "R5", "text": "When a trick ends without emptying the hands, the trick winner leads the next trick."},
    {"id": "R6", "text": "When the leader plays the first card, its rank becomes led_rank, and the leader may play any card in hand."},
    {"id": "R7", "text": "When the follower's first card is neither led_rank nor a 7, the leader wins the trick immediately with 2 cards played."},
    {"id": "R8", "text": "When the follower's first card is led_rank or a 7, the follower is currently winning."},
    {"id": "R9", "text": "When the follower is currently winning and the leader holds a led_rank card or a 7, the leader may extend by playing one such card, or may decline."},
    {"id": "R10", "text": "When the follower is currently winning and the leader declines or holds no led_rank card and no 7, the follower wins the trick."},
    {"id": "R11", "text": "When the leader extends, the follower must play a second card from hand (any card)."},
    {"id": "R12", "text": "When the follower's second card is led_rank or a 7, the follower wins the trick; otherwise the leader wins."},
    {"id": "R13", "text": "A trick is extended at most once, so each player plays at most 2 cards in a trick."},
    {"id": "R14", "text": "When a trick ends, all of its cards are announced and the winner scores 10 points for each A and each 10 among them."},
    {"id": "R15", "text": "When a trick empties both hands, its winner scores an extra 10 points for the last trick and the deal ends."},
    {"id": "R16", "text": "Both players play the same number of cards in every trick, so a deal lasts between 4 and 8 tricks and the remaining rounds of that deal are skipped."},
    {"id": "R17", "text": "When deal 4 ends (deal_number reaches 5), the game ends and the higher score wins; equal scores are a draw."},
    {"id": "R18", "text": "Each player sees only their own hand and the cards played, never the opponent's hand or the set-aside cards."}
  ],
  "offers": [
    {"question": "Leader's first card", "who": "seat game.leader", "options": "every card currently in the leader's hand"},
    {"question": "Follower's first card", "who": "the seat that is not game.leader", "options": "every card currently in the follower's hand"},
    {"question": "Leader's extension", "who": "seat game.leader, only when the follower is currently winning and the leader holds a led_rank card or a 7", "options": "decline, plus each card in the leader's hand whose rank is led_rank or '7'"},
    {"question": "Follower's second card", "who": "the seat that is not game.leader, only when the leader extended", "options": "every card currently in the follower's hand"}
  ],
  "choices": [
    {"what": "Exactly 2 players, suggested 2", "why": "The designer fixed it as a duel. Its trick mechanics (one leader, one follower, an extension answered by the follower) only work with two players."},
    {"what": "No talk step", "why": "With two directly opposed players, talk gives nothing to coordinate and only adds words."},
    {"what": "Seat 1 is Player A and seat 2 is Player B", "why": "This maps the source's named players to seats so the first-lead rule can be applied."},
    {"what": "Cards are stored as rank strings in lists", "why": "Suits do not matter, so a rank fully identifies a card."},
    {"what": "The match loop runs trick by trick instead of in 32 fixed round slots", "why": "Skipped rounds in a deal do nothing, so ending each deal when the hands empty and counting deals gives the same game."}
  ],
  "simplifications": [
    {"what": "The 8-round deal slot is not counted explicitly; a deal ends when both hands are empty", "why": "The rules say the remaining rounds of a deal are skipped, so counting slots adds steps without changing play."},
    {"what": "Dealing is a single conditional update at the start of a round when new_deal is true", "why": "The engine's step list is flat, and a step with a when condition expresses dealing on the first round of each deal."}
  ],
  "unsupported": []
}
```
````
