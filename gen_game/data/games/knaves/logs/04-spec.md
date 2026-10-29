# 04 spec

- time: 2026-10-27T18:06:39+00:00 (58.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 917476fa5d8aaf58, reply sha256 cbee63c6f3905e42

## Sent

````
Game: Knaves' Wager
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
PLAYERS AND DECK. 3 players sit in a fixed order. The deck has 20 cards: A, K, Q, J, 10 in each of spades, clubs, diamonds and hearts. Within a suit, cards rank A (high), K, Q, J, 10 (low).

HANDS AND ROUNDS. The game is 6 hands of 6 tricks each, 36 rounds in all. Each round is one trick. The dealer for hand 1 is player 1. The dealer moves one seat to the left each hand, so each player deals twice. The player to the dealer's left is eldest for that hand.

DEAL (first round of each hand). Shuffle all 20 cards. Deal 6 cards privately to each player; a hand is seen only by its owner. Turn the 19th card face up: its suit is trump for this hand, and the card itself is out of play. The 20th card stays face down and out of play, and is never revealed during the hand.

BID (first round of each hand, after the deal). All players at the same moment secretly choose a whole number from 0 to 6: the number of tricks they predict they will take this hand. All three bids are then revealed to everyone.

TRICK PLAY (every round). The leader plays any card from their hand face up. The eldest leads the first trick of a hand; afterwards, the winner of the previous trick leads. Then the next player to the left plays, then the third. Each must play a card of the led suit if they have one. If they have none, they may play any card, including a trump. The trick is won by the highest trump in it. If it holds no trump, the highest card of the led suit wins. All plays are visible to everyone as they are made.

TRICK SCORING. The trick winner adds 2 to their hand score. They also take penalties for any Jacks in the trick: Jack of spades -1, Jack of clubs -2, Jack of diamonds -3, Jack of hearts -4. The trick's cards, its winner and the running trick counts are announced.

END OF HAND (after the 6th trick). Any player whose tricks taken equal their bid adds 4 to their hand score. Each player's hand score (2 per trick, minus Jack penalties, plus any bid bonus) is added to their total and announced. Hand scores reset to 0, and the dealer rotates.

END OF GAME. After the 6th hand (round 36), the game ends.

How the winner is decided: After 6 hands, the player with the highest total wins. If two or three players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Knaves' Wager",
  "summary": "A 3-player trick-taking game over 6 hands of 6 tricks: bid your trick count secretly, take tricks for 2 points each, avoid winning Jacks, and score a 4-point bonus for an exact bid.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "player_count": 3,
    "deck_size": 20,
    "suits": 4,
    "ranks_per_suit": 5,
    "hands": 6,
    "tricks_per_hand": 6,
    "total_rounds": 36,
    "cards_dealt_per_player": 6,
    "trump_card_position": 19,
    "hidden_card_position": 20,
    "bid_min": 0,
    "bid_max": 6,
    "trick_points": 2,
    "jack_of_spades_penalty": 1,
    "jack_of_clubs_penalty": 2,
    "jack_of_diamonds_penalty": 3,
    "jack_of_hearts_penalty": 4,
    "exact_bid_bonus": 4,
    "deals_per_player": 2,
    "first_dealer_seat": 1,
    "rank_value_A": 14,
    "rank_value_K": 13,
    "rank_value_Q": 12,
    "rank_value_J": 11,
    "rank_value_10": 10
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The cards this player holds, as codes such as 'AS' or '10H'. Only the owner sees it.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "The tricks this player predicted for the current hand, from 0 to 6. Revealed after all players have bid.", "observable": true},
      {"key": "tricks_taken", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks this player has won in the current hand.", "observable": true},
      {"key": "hand_score", "type": "number", "visible": "public", "initial": 0, "meaning": "Points this player has earned in the current hand: 2 per trick, minus Jack penalties, plus any bid bonus.", "observable": true},
      {"key": "total", "type": "number", "visible": "public", "initial": 0, "meaning": "This player's running game total, which is the score.", "observable": true},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card this player played to the current trick.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["AS","KS","QS","JS","10S","AC","KC","QC","JC","10C","AD","KD","QD","JD","10D","AH","KH","QH","JH","10H"], "meaning": "The undealt cards. At the start of each hand all 20 cards are gathered here and shuffled.", "observable": false},
      {"key": "turned_card", "type": "text", "visible": "public", "initial": "", "meaning": "The 19th card, turned face up. It sets trump and is out of play.", "observable": true},
      {"key": "hidden_card", "type": "text", "visible": "none", "initial": "", "meaning": "The 20th card. It stays face down, is out of play, and is never revealed during the hand.", "observable": false},
      {"key": "trump_suit", "type": "text", "visible": "public", "initial": "", "meaning": "The suit of turned_card: S, C, D or H.", "observable": true},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current hand, from 1 to 6.", "observable": true},
      {"key": "trick_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "The current trick within the hand, from 1 to 6.", "observable": false},
      {"key": "round_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current round, from 1 to 36. One round is one trick.", "observable": false},
      {"key": "dealer", "type": "number", "visible": "public", "initial": 1, "meaning": "The dealer's seat for this hand.", "observable": false},
      {"key": "eldest", "type": "number", "visible": "public", "initial": 2, "meaning": "The seat to the dealer's left, which leads the first trick of the hand.", "observable": false},
      {"key": "leader", "type": "number", "visible": "public", "initial": 2, "meaning": "The seat that leads the current trick.", "observable": false},
      {"key": "led_suit", "type": "text", "visible": "public", "initial": "", "meaning": "The suit of the card led to the current trick.", "observable": false},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat that won the last trick.", "observable": true}
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 sit in a fixed order; the seat to a player's left is the next seat number, and seat 1 follows seat 3.",
    "Set every player's total to 0.",
    "Set hand_number to 1, round_number to 1 and trick_in_hand to 1.",
    "Set dealer to 1 and eldest to 2."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand = 1: gather all 20 cards into deck and empty every hand. Deal 6 cards to each player by drawing at random from deck into hand. Draw one more card at random into turned_card, and set trump_suit to its suit. Move the last card into hidden_card. Set leader = eldest. Set every player's tricks_taken, bid and hand_score to 0."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player is shown their own hand and the public state."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_hand = 1: announce hand_number, dealer, eldest, turned_card and trump_suit."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to 6", "effect": "When trick_in_hand = 1: each player's answer is stored in bid, and no bid is seen until all three are in."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_hand = 1: reveal all three bids to everyone."},
    {"action": "ask", "who": "the seat equal to leader", "answer": "one card from their hand", "effect": "Remove the card from the leader's hand and set the leader's played_card to it. Set led_suit to the card's suit. The play is shown to everyone."},
    {"action": "ask", "who": "the seat to the leader's left (leader mod 3 + 1)", "answer": "one card from their hand; it must be of led_suit if they hold any card of led_suit, otherwise any card", "effect": "Remove the card from that player's hand and set their played_card to it. The play is shown to everyone."},
    {"action": "ask", "who": "the third seat ((leader + 1) mod 3 + 1)", "answer": "one card from their hand; it must be of led_suit if they hold any card of led_suit, otherwise any card", "effect": "Remove the card from that player's hand and set their played_card to it. The play is shown to everyone."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Rank values are A=14, K=13, Q=12, J=11, 10=10. If any played_card has suit trump_suit, trick_winner is the seat whose trump has the highest rank value; otherwise it is the seat whose led_suit card has the highest rank value. The winner gets tricks_taken += 1 and hand_score += 2, then hand_score -= 1 for JS, 2 for JC, 3 for JD and 4 for JH among the three played cards. Set leader = trick_winner."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce the three played cards, trick_winner, and every player's tricks_taken and hand_score."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand = 6: each player with tricks_taken = bid gets hand_score += 4. Then each player's total += hand_score. Announce each hand_score and total. Then set every hand_score to 0, set dealer = dealer mod 3 + 1, set eldest = dealer mod 3 + 1, and set hand_number += 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set round_number += 1. Set trick_in_hand = trick_in_hand mod 6 + 1. Clear every played_card and led_suit."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round_number > 36, the game ends; otherwise the round repeats."}
  ],
  "ending": {
    "condition": "round_number > 36",
    "rank_by": "you.total",
    "decided_by": "Each player's standing is their total after 6 hands (36 tricks). The highest total wins; if two or three players tie for the highest total, they share the result, which is the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, there are exactly 3 players and a 20-card deck of A, K, Q, J and 10 in each of spades, clubs, diamonds and hearts."},
    {"id": "R2", "text": "When cards of one suit are compared, they rank A (high), K, Q, J, 10 (low)."},
    {"id": "R3", "text": "When the game runs, it consists of 6 hands of 6 tricks each, 36 rounds in all, one trick per round."},
    {"id": "R4", "text": "When hand 1 begins, seat 1 is dealer and seat 2 is eldest."},
    {"id": "R5", "text": "When a hand ends, the dealer moves one seat to the left (1 to 2, 2 to 3, 3 to 1), so each seat deals exactly 2 of the 6 hands."},
    {"id": "R6", "text": "When a hand begins, eldest is the seat to the dealer's left: dealer mod 3 + 1."},
    {"id": "R7", "text": "When a hand begins, all 20 cards are shuffled and each player is dealt 6 cards into their hand, which only the owner can see."},
    {"id": "R8", "text": "When a hand is dealt, the 19th card is turned face up into turned_card, trump_suit becomes its suit, and that card is out of play."},
    {"id": "R9", "text": "When a hand is dealt, the 20th card goes face down into hidden_card, is out of play, and is never revealed during the hand."},
    {"id": "R10", "text": "When a hand has been dealt, all players bid at the same moment a whole number from 0 to 6, and no bid is seen until all three are in."},
    {"id": "R11", "text": "When all three bids are in, all three are revealed to everyone."},
    {"id": "R12", "text": "When the first trick of a hand is played, eldest leads it."},
    {"id": "R13", "text": "When any trick after the first in a hand is played, the winner of the previous trick leads it."},
    {"id": "R14", "text": "When a trick is played, the leader plays first, then the seat to the leader's left, then the remaining seat."},
    {"id": "R15", "text": "When the leader plays, they may play any card from their hand."},
    {"id": "R16", "text": "When a following player holds a card of the led suit, they must play a card of the led suit."},
    {"id": "R17", "text": "When a following player holds no card of the led suit, they may play any card in their hand, including a trump."},
    {"id": "R18", "text": "When a trick contains at least one trump, the highest trump wins it."},
    {"id": "R19", "text": "When a trick contains no trump, the highest card of the led suit wins it, and off-suit cards cannot win."},
    {"id": "R20", "text": "When a player wins a trick, their tricks_taken rises by 1 and their hand_score rises by 2."},
    {"id": "R21", "text": "When a trick's winner takes Jacks, their hand_score falls by 1 for the Jack of spades, 2 for the Jack of clubs, 3 for the Jack of diamonds and 4 for the Jack of hearts in that trick."},
    {"id": "R22", "text": "When a trick ends, its three cards, its winner and every player's tricks taken are announced."},
    {"id": "R23", "text": "When the 6th trick of a hand ends, each player whose tricks_taken equals their bid adds 4 to their hand_score."},
    {"id": "R24", "text": "When the 6th trick of a hand ends, each player's hand_score is added to their total and announced, and then every hand_score resets to 0."},
    {"id": "R25", "text": "When all plays are made, every played card is visible to everyone as it is played."},
    {"id": "R26", "text": "When round 36 (the 6th trick of the 6th hand) is complete, the game ends."},
    {"id": "R27", "text": "When the game ends, the player with the highest total wins; if two or three players tie for the highest total, the game is a draw among them."}
  ],
  "offers": [
    {"question": "Bid (first round of each hand)", "who": "all three seats, simultaneously", "options": "any whole number from 0 to 6"},
    {"question": "Lead a card", "who": "the seat equal to leader (eldest on the first trick of a hand, otherwise the previous trick's winner)", "options": "every card in that seat's hand"},
    {"question": "Follow to the trick (second player)", "who": "the seat to the leader's left", "options": "if the seat holds any card of led_suit, only its cards of led_suit; otherwise every card in its hand"},
    {"question": "Follow to the trick (third player)", "who": "the remaining seat", "options": "if the seat holds any card of led_suit, only its cards of led_suit; otherwise every card in its hand"}
  ],
  "choices": [
    {"what": "Exactly 3 players (min, max and suggested 3)", "why": "The designer fixed 3. The 20-card deck is built for it: 3 x 6 dealt cards plus the turned trump card and the hidden card make 20, so no other count works without changing the deck."},
    {"what": "No talk phase", "why": "The source has no table talk, and adding one would add a mechanic. The strategy is already in the exact bid (balancing taking tricks against hitting the bid), in dumping or avoiding Jacks, and in reading the revealed bids."},
    {"what": "Cards are written as rank plus suit letter (AS, 10H, ...), with rank values A=14, K=13, Q=12, J=11, 10=10", "why": "This lets the trick winner be worked out by arithmetic comparison."},
    {"what": "Seat to the left means the next seat number, with seat 1 after seat 3", "why": "The source says 'left' but gives no numbering, and a direction is needed for dealer rotation, eldest and play order."},
    {"what": "The first-round-of-hand steps (deal, bid, reveal) and the end-of-hand step carry a when condition on trick_in_hand", "why": "This keeps the step list flat while running those steps only on tricks 1 and 6 of each hand."}
  ],
  "simplifications": [
    {"what": "A tie for the highest total is a shared win rather than a separately named draw", "why": "The engine has no separate draw outcome; players level at the top share the result, which matches the source's draw."},
    {"what": "Dealing is done by random draws from the deck list rather than by a physical shuffle and dealing in order", "why": "Drawing at random is equivalent to shuffling, so the 19th and 20th cards are simply the two left after the 18 dealt cards."},
    {"what": "The order of play within a trick is three ask steps addressed relative to leader", "why": "The engine has no seat-order rotation, so the leader, the next seat and the third seat are each named by arithmetic on leader."}
  ],
  "unsupported": []
}
```
````
