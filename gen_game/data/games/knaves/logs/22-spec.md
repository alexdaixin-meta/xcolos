# 22 spec

- time: 2026-10-27T18:28:49+00:00 (49.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 b3b55fb6b1d4278e, reply sha256 a0ce67670a189d8a

## Sent

````
Game: Knaves Short Deck with Bids
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
R1 Setup. There are exactly 3 players, seats 1, 2 and 3. The full deck is the 20 cards AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H. At the start every player's total is 0, their hand is empty, hand_number is 1, and the deck holds all 20 cards.

R2 Rank. Within a suit, cards rank A (high), K, Q, J, 10 (low).

R3 Length. The game has exactly 36 rounds. Each round is one trick. The game ends after round 36.

R4 Hands. Rounds 1-6 form hand 1, rounds 7-12 hand 2, and so on up to rounds 31-36, which form hand 6. trick_in_hand runs from 1 to 6 within each hand.

R5 Dealer. In hand h, the dealer is seat ((h-1) mod 3) + 1. So hand 1 is dealt by seat 1, hand 2 by seat 2, hand 3 by seat 3, hand 4 by seat 1, and so on.

R6 Eldest. When a hand begins, eldest is the seat to the dealer's left: (dealer mod 3) + 1. Eldest is the leader of that hand's first trick.

R7 Reset and deal. In the first round of every hand, before anything else happens:
(a) Set the deck to the full 20-card list from R1.
(b) Empty every player's hand and the discard pile.
(c) Set every player's bid, tricks_taken and hand_score to 0.
(d) Shuffle the deck once. This is the only random event in the round.
(e) Cards 1-6 of the shuffled deck go to seat 1, cards 7-12 to seat 2, and cards 13-18 to seat 3. Each hand is seen only by its owner.

R8 Turned card. Card 19 is turned face up into turned_card, seen by all, and trump_suit becomes its suit. That card is out of play for the hand.

R9 Hidden card. Card 20 goes face down into hidden_card. It is out of play and is never revealed during the hand. After the deal the deck holds 0 cards.

R10 Bid. In the first round of every hand, right after the deal, all three seats bid at the same moment in one simultaneous poll. Each seat is offered exactly the options 0, 1, 2, 3, 4, 5 and 6: the number of tricks it predicts it will take this hand. All bids are then shown to everyone.

R11 Play order. Every round, the leader plays one card from their hand first. Then seat (leader mod 3) + 1 plays, then the remaining seat. Players act one at a time and each sees the cards already played to the trick. The suit of the leader's card is led_suit. Each played card is removed from its owner's hand, recorded as that player's played_card, and added to the discard pile. It never returns to the deck.

R12 Follow suit. A player who holds any card of led_suit must play one of those cards. A player who holds none may play any card in their hand, including a trump. The leader may play any card.

R13 Trick winner. If any trump_suit cards were played, the highest-ranked trump wins. Otherwise the highest-ranked card of led_suit wins. The winner becomes trick_winner and leads the next trick of the same hand.

R14 Trick score. The trick winner adds 1 to tricks_taken and adds to hand_score: +2, minus the penalties for any Jacks among the three cards in the trick (JS 1, JC 2, JD 3, JH 4). A Jack is penalised even if it is the trump suit.

R15 End of hand. After the trick in round 6, 12, 18, 24, 30 or 36 is scored:
(a) Each player whose tricks_taken equals their bid adds 5 to hand_score.
(b) Each player adds hand_score to their total.
(c) The totals are announced to all.

R16 Winner. After round 36, the player with the highest total wins. If two or three players tie for the highest total, the game is a draw.

How the winner is decided: After the 36th trick and the final end-of-hand scoring, the single player with the highest total wins. A tie for the highest total is a draw.
````

## Reply

````
```json
{
  "name": "Knaves Short Deck with Bids",
  "summary": "Three players play 36 tricks with a 20-card deck, in six hands of six tricks. Each player bids how many tricks they will take each hand, Jacks in a won trick cost points, and an exact bid earns a bonus.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "num_players": 3,
    "deck_size": 20,
    "total_rounds": 36,
    "tricks_per_hand": 6,
    "num_hands": 6,
    "cards_per_player": 6,
    "turned_card_position": 19,
    "hidden_card_position": 20,
    "bid_min": 0,
    "bid_max": 6,
    "trick_base_points": 2,
    "penalty_JS": 1,
    "penalty_JC": 2,
    "penalty_JD": 3,
    "penalty_JH": 4,
    "exact_bid_bonus": 5,
    "rank_value_A": 5,
    "rank_value_K": 4,
    "rank_value_Q": 3,
    "rank_value_J": 2,
    "rank_value_10": 1,
    "trump_bonus": 10
  },
  "attributes": {
    "player": [
      {"key": "total", "type": "number", "visible": "public", "initial": 0, "meaning": "Running game score, added to at the end of each hand", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards the player holds in the current hand, seen only by the owner", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of tricks the player predicted for this hand, shown to all after the simultaneous bid", "observable": true},
      {"key": "tricks_taken", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won so far in this hand", "observable": true},
      {"key": "hand_score", "type": "number", "visible": "public", "initial": 0, "meaning": "Points scored in this hand so far", "observable": false},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "Card the player played to the current trick", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["AS","KS","QS","JS","10S","AC","KC","QC","JC","10C","AD","KD","QD","JD","10D","AH","KH","QH","JH","10H"], "meaning": "Undealt cards; empty after each deal", "observable": false},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "Cards played so far this hand", "observable": false},
      {"key": "turned_card", "type": "text", "visible": "public", "initial": "", "meaning": "Card 19 of the shuffled deck, face up and out of play", "observable": true},
      {"key": "trump_suit", "type": "text", "visible": "public", "initial": "", "meaning": "Suit of turned_card (S, C, D or H)", "observable": true},
      {"key": "hidden_card", "type": "text", "visible": "none", "initial": "", "meaning": "Card 20 of the shuffled deck, face down, out of play, never revealed", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Current round (trick) number, 1 to 36", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "Current hand, floor((round-1)/6)+1", "observable": true},
      {"key": "trick_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "Trick within the hand, ((round-1) mod 6)+1", "observable": false},
      {"key": "dealer", "type": "number", "visible": "public", "initial": 1, "meaning": "Dealer seat, ((hand_number-1) mod 3)+1", "observable": false},
      {"key": "leader", "type": "number", "visible": "public", "initial": 2, "meaning": "Seat that leads the current trick", "observable": false},
      {"key": "led_suit", "type": "text", "visible": "public", "initial": "", "meaning": "Suit of the leader's card in the current trick", "observable": false},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won the most recent trick", "observable": true}
    ]
  },
  "setup": [
    "Seat three players, seats 1, 2 and 3.",
    "Set every player's total to 0 and hand to empty.",
    "Set round to 1, hand_number to 1 and trick_in_hand to 1.",
    "Set deck to the full 20-card list: AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: set dealer = ((hand_number-1) mod 3)+1 and leader = (dealer mod 3)+1. Set deck to the full 20-card list, empty every hand and discard, and set every bid, tricks_taken and hand_score to 0. Shuffle the deck once. Deal cards 1-6 to seat 1's hand, 7-12 to seat 2's hand and 13-18 to seat 3's hand. Put card 19 in turned_card and set trump_suit to its suit. Put card 20 in hidden_card. The deck is now empty. Announce turned_card, trump_suit, dealer and leader."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: each player is sent their own hand, plus the public turned_card and trump_suit."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to 6", "effect": "When trick_in_hand == 1: set each player's bid to their answer. After all answers are in, broadcast every bid to all."},
    {"action": "ask", "who": "the seat equal to leader", "answer": "one card from own hand (any card)", "effect": "Remove the card from the leader's hand, set the leader's played_card to it, append it to discard, and set led_suit to its suit. Show the card to all."},
    {"action": "ask", "who": "seat (leader mod 3)+1", "answer": "one card from own hand: a led_suit card if any is held, otherwise any card", "effect": "Remove the card from the hand, set played_card to it, append it to discard, and show it to all."},
    {"action": "ask", "who": "seat ((leader+1) mod 3)+1", "answer": "one card from own hand: a led_suit card if any is held, otherwise any card", "effect": "Remove the card from the hand, set played_card to it, append it to discard, and show it to all."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Score each played_card as rank value (A 5, K 4, Q 3, J 2, 10 1), plus 10 if its suit is trump_suit, or 0 if its suit is neither trump_suit nor led_suit. Set trick_winner to the seat with the highest score. That seat adds 1 to tricks_taken and adds 2 - (1 if JS played) - (2 if JC played) - (3 if JD played) - (4 if JH played) to hand_score. Set leader = trick_winner. Announce the winner."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand == 6: each player with tricks_taken == bid adds 5 to hand_score. Every player then adds hand_score to total. Announce all totals."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Add 1 to round. Set trick_in_hand = ((round-1) mod 6)+1 and hand_number = floor((round-1)/6)+1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round > 36; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round > 36",
    "rank_by": "you.total",
    "decided_by": "Each player's standing is their total after the end-of-hand scoring of hand 6. The highest total wins. Players tied for the highest total share the result, which the source calls a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, every player's total is 0, hand_number is 1, and the deck holds the 20 cards AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H."},
    {"id": "R2", "text": "Within a suit, cards rank A > K > Q > J > 10."},
    {"id": "R3", "text": "When round 36's trick and end-of-hand scoring are done, the game ends; it never runs a 37th trick."},
    {"id": "R4", "text": "When round is r, hand_number is floor((r-1)/6)+1 and trick_in_hand is ((r-1) mod 6)+1, so rounds 31-36 are hand 6."},
    {"id": "R5", "text": "When hand h begins, dealer is ((h-1) mod 3)+1: hand 1 is seat 1, hand 2 seat 2, hand 3 seat 3, hand 4 seat 1."},
    {"id": "R6", "text": "When a hand begins, leader of its first trick is (dealer mod 3)+1, so hand 1 is led by seat 2."},
    {"id": "R7", "text": "When trick_in_hand is 1, the deck is reset to 20 cards, hands and discard are emptied, bid, tricks_taken and hand_score are set to 0, and seats 1, 2 and 3 each receive 6 cards, seen only by their owner."},
    {"id": "R8", "text": "When a hand is dealt, card 19 becomes turned_card, visible to all, trump_suit is its suit, and it is not in any hand."},
    {"id": "R9", "text": "When a hand is dealt, card 20 becomes hidden_card, is never shown, and the deck then holds 0 cards."},
    {"id": "R10", "text": "When trick_in_hand is 1, all three seats bid simultaneously from 0-6, and after all are in, every bid is shown to all."},
    {"id": "R11", "text": "When a trick is played, the leader plays first, then seat (leader mod 3)+1, then the remaining seat; each played card leaves the hand, becomes played_card and is appended to discard."},
    {"id": "R12", "text": "When a non-leader holds a card of led_suit, they are offered only led_suit cards; when they hold none, they are offered every card in their hand."},
    {"id": "R13", "text": "When any trump is played, the highest trump wins the trick; otherwise the highest led_suit card wins; the winner leads the next trick."},
    {"id": "R14", "text": "When a player wins a trick, tricks_taken rises by 1 and hand_score rises by 2 minus 1 for JS, 2 for JC, 3 for JD and 4 for JH among the trick's cards, including a trump Jack (e.g. a trick containing JH and JS scores 2-4-1 = -3)."},
    {"id": "R15", "text": "When trick_in_hand 6 is scored, each player with tricks_taken equal to bid gains 5 hand_score, every player adds hand_score to total, and totals are announced."},
    {"id": "R16", "text": "When the game ends, the player with the highest total wins; players tied for highest share it, which the source calls a draw."}
  ],
  "offers": [
    {"question": "Bid (first round of each hand)", "who": "all three seats, simultaneously", "options": "0, 1, 2, 3, 4, 5, 6 for every seat"},
    {"question": "Lead a card", "who": "the seat equal to leader", "options": "every card in the leader's hand"},
    {"question": "Play a card (second and third to the trick)", "who": "seat (leader mod 3)+1, then the remaining seat", "options": "a seat holding a led_suit card: only its led_suit cards; a seat holding no led_suit card: every card in its hand"}
  ],
  "choices": [
    {"what": "3 players, min = max = suggested = 3", "why": "The designer fixed the game at 3. The deal uses exactly 18 of 20 cards, the dealer rotation is mod 3, and the 6-card hand fits only three seats."},
    {"what": "No talk step before bids or plays", "why": "The rules include no table talk, and adding it would add a mechanic."},
    {"what": "Trick winner computed by an arithmetic card score (rank 1-5, +10 for trump, 0 for an off-suit non-trump)", "why": "This reproduces R13 exactly by calculation, with no referee needed."},
    {"what": "hand_score, played_card and discard are public", "why": "The source leaves their visibility open; all are derivable from cards played face up."},
    {"what": "Strategy at the table", "why": "Players read their hand against the trump suit to bid accurately, dodge winning tricks loaded with costly Jacks (especially JH and JD), and dump Jacks onto opponents' tricks while steering toward their exact bid."}
  ],
  "simplifications": [
    {"what": "A tie for the highest total is a shared win for the tied players rather than a separate draw result", "why": "The engine ranks by one expression and lets players level at the top share the win. This is equivalent to the source's draw."},
    {"what": "Per-hand reset, deal and bid run as single steps carrying the condition trick_in_hand == 1, and end-of-hand scoring carries trick_in_hand == 6", "why": "The step list is flat; each conditional step is a single step, not an alternative block."}
  ],
  "unsupported": []
}
```
````
