# 04 spec

- time: 2026-10-27T08:38:22+00:00 (79.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 deb647fc718a8b34, reply sha256 b86956caea77ddb3

## Sent

````
Game: Lost Cities: Four Expeditions
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. The deck has 44 cards in 4 colours: Red, Blue, Green and Yellow. Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9 and 10 (9 cards) and 2 wager cards.

STATE. Each player has a hidden hand.
- For each colour, each player has a public expedition record with three parts:
  - sum: the total of the number cards played in that colour (starts at 0);
  - top: the highest number played in that colour (starts at 0);
  - wagers: the number of wager cards played in that colour (starts at 0).
- There is a public 'discard tops' row. It holds at most one face-up card per colour.
- The number of cards left in the deck is public. The order of the deck is hidden.
- Each player has a match score that starts at 0.

MATCH. The match is two deals. Player A leads in deal 1 and Player B leads in deal 2. The leader takes the first turn of every round in that deal.

START OF A DEAL. All expedition records are reset to 0, and the discard tops row is cleared. All 44 cards are shuffled and each player is dealt 6 cards. The remaining 32 cards form the face-down deck.

ROUND. A round is one turn by the leader followed by one turn by the other player. A turn has two parts.

(1) PLAY OR DISCARD. Choose one card from your hand and say whether you PLAY it or DISCARD it.
- PLAY a number card of colour X: it is legal only if its number is greater than your top in X. Your sum in X increases by the number, and your top in X becomes the number.
- PLAY a wager card of colour X: it is legal only if your top in X is 0, meaning no number has been played there yet. Your wagers in X increase by 1.
- An illegal PLAY is treated as a DISCARD of that card.
- DISCARD a card of colour X: it becomes the face-up top card of colour X in the discard tops row. Any card that was there before is removed from the game.

(2) DRAW. Take one card into your hand, either the top card of the deck or the top discard card of any colour. You may not take the card you discarded this turn.
- If you name an unavailable source, you take the deck top.
- If the deck is empty, you take a discard top. If none is available apart from the card you just discarded, you draw nothing.

After each turn, the played or discarded card, the drawn source (but not the deck card's identity) and the deck size are announced to both players.

END OF A DEAL. A deal ends at the end of a round if the deck is empty, or at the end of the 20th round of that deal, whichever comes first.
- Each player then scores each colour separately. If their top in that colour is above 0 or their wagers in it are above 0, the colour scores (sum − 20) × (1 + wagers). Otherwise it scores 0.
- The four colour scores are added to the player's match score, which can go negative.
- Cards still in hand score nothing.

END OF MATCH. After deal 2 ends, the match is over. The match always ends within 40 rounds.

How the winner is decided: After both deals, the player with the higher match score wins. If the match scores are equal, the match is a draw.
````

## Reply

````
```json
{
  "name": "Lost Cities: Four Expeditions",
  "summary": "Two players spend two deals building four colour expeditions with rising number cards and optional up-front wagers, discarding and drawing from a shared deck and face-up discard tops; each colour scores (sum - 20) x (1 + wagers).",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 44,
    "colours": 4,
    "number_card_min": 2,
    "number_card_max": 10,
    "number_cards_per_colour": 9,
    "wager_cards_per_colour": 2,
    "hand_size": 6,
    "deck_after_deal": 32,
    "deals": 2,
    "max_rounds_per_deal": 20,
    "max_rounds_per_match": 40,
    "expedition_cost": 20,
    "wager_multiplier_base": 1,
    "initial_match_score": 0,
    "initial_record_value": 0
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards held. Each card is a text such as 'Red 7' or 'Red W1'.", "observable": false},
      {"key": "red_sum", "type": "number", "visible": "public", "initial": 0, "meaning": "Total of number cards played in Red this deal", "observable": true},
      {"key": "red_top", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest number played in Red this deal (0 = none)", "observable": true},
      {"key": "red_wagers", "type": "number", "visible": "public", "initial": 0, "meaning": "Wager cards played in Red this deal", "observable": true},
      {"key": "blue_sum", "type": "number", "visible": "public", "initial": 0, "meaning": "Total of number cards played in Blue this deal", "observable": true},
      {"key": "blue_top", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest number played in Blue this deal (0 = none)", "observable": true},
      {"key": "blue_wagers", "type": "number", "visible": "public", "initial": 0, "meaning": "Wager cards played in Blue this deal", "observable": true},
      {"key": "green_sum", "type": "number", "visible": "public", "initial": 0, "meaning": "Total of number cards played in Green this deal", "observable": true},
      {"key": "green_top", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest number played in Green this deal (0 = none)", "observable": true},
      {"key": "green_wagers", "type": "number", "visible": "public", "initial": 0, "meaning": "Wager cards played in Green this deal", "observable": true},
      {"key": "yellow_sum", "type": "number", "visible": "public", "initial": 0, "meaning": "Total of number cards played in Yellow this deal", "observable": true},
      {"key": "yellow_top", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest number played in Yellow this deal (0 = none)", "observable": true},
      {"key": "yellow_wagers", "type": "number", "visible": "public", "initial": 0, "meaning": "Wager cards played in Yellow this deal", "observable": true},
      {"key": "match_score", "type": "number", "visible": "public", "initial": 0, "meaning": "Running match score over both deals. It can go negative.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Face-down draw deck. Its order is hidden and a draw picks a card at random.", "observable": false},
      {"key": "deck_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Cards left in the deck", "observable": true},
      {"key": "discard_red", "type": "text", "visible": "public", "initial": "", "meaning": "Face-up top discard card of Red ('' = none)", "observable": true},
      {"key": "discard_blue", "type": "text", "visible": "public", "initial": "", "meaning": "Face-up top discard card of Blue ('' = none)", "observable": true},
      {"key": "discard_green", "type": "text", "visible": "public", "initial": "", "meaning": "Face-up top discard card of Green ('' = none)", "observable": true},
      {"key": "discard_yellow", "type": "text", "visible": "public", "initial": "", "meaning": "Face-up top discard card of Yellow ('' = none)", "observable": true},
      {"key": "removed_cards", "type": "list", "visible": "none", "initial": [], "meaning": "Discard tops that were covered by a newer discard and so removed from the game", "observable": false},
      {"key": "turn_discard", "type": "text", "visible": "public", "initial": "", "meaning": "The card discarded in the current turn ('' if the card was played). It may not be drawn back this turn.", "observable": false},
      {"key": "deal", "type": "number", "visible": "public", "initial": 1, "meaning": "Current deal (1 or 2). Seat 1 leads deal 1 and seat 2 leads deal 2.", "observable": true},
      {"key": "round_in_deal", "type": "number", "visible": "public", "initial": 0, "meaning": "Rounds started in the current deal (0 = a new deal must be dealt)", "observable": true},
      {"key": "match_over", "type": "bool", "visible": "public", "initial": false, "meaning": "True once deal 2 has been scored", "observable": true}
    ]
  },
  "setup": [
    "Seat 1 is Player A and seat 2 is Player B.",
    "Set deal = 1, round_in_deal = 0, match_over = false and each player's match_score = 0.",
    "The first round step deals deal 1 (it runs whenever round_in_deal = 0)."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "when": "round_in_deal == 0",
     "effect": "Start of a deal: set every player's red/blue/green/yellow _sum, _top and _wagers to 0. Set discard_red, discard_blue, discard_green and discard_yellow to ''. Set removed_cards = [] and every hand = []. Set deck to all 44 cards: for each colour Red, Blue, Green and Yellow, the cards '<Colour> 2' to '<Colour> 10' plus '<Colour> W1' and '<Colour> W2'. Deal 6 cards to each player, each one drawn at random from deck, appended to hand and removed from deck. Set deck_count = 32."},
    {"action": "sync", "who": "all players", "answer": null, "when": "round_in_deal == 0",
     "effect": "Each player sees their own hand and all public attributes."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "round_in_deal += 1."},

    {"action": "ask", "who": "seat 1", "when": "deal == 1",
     "answer": "One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand",
     "effect": "The answer is stored for the next step."},
    {"action": "update", "who": "seat 1", "answer": null, "when": "deal == 1",
     "effect": "Remove the chosen card from seat 1's hand. If it is a PLAY of number card n of colour X and n > X_top: X_sum += n and X_top = n, and turn_discard = ''. If it is a PLAY of a wager of colour X and X_top == 0: X_wagers += 1, and turn_discard = ''. Otherwise (a DISCARD, or an illegal PLAY): if discard_X != '', append discard_X to removed_cards; then discard_X = card and turn_discard = card."},
    {"action": "ask", "who": "seat 1", "when": "deal == 1 and (deck_count > 0 or any discard top other than turn_discard is non-empty)",
     "answer": "One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard",
     "effect": "The answer is stored for the next step."},
    {"action": "update", "who": "seat 1", "answer": null, "when": "deal == 1",
     "effect": "If a discard top of colour X was named, is non-empty and is not turn_discard: append discard_X to hand and set discard_X = ''. Else if deck_count > 0: draw a random card from deck into hand and deck_count -= 1. Else, if any discard top other than turn_discard is non-empty: take the first one in the order Red, Blue, Green, Yellow into hand and set it to ''. Otherwise draw nothing. Set turn_discard = ''."},
    {"action": "tell", "who": "all players", "answer": null, "when": "deal == 1",
     "effect": "Announce seat 1's played or discarded card, the draw source (deck, a discard colour, or nothing; a deck card's identity is not shown) and deck_count."},

    {"action": "ask", "who": "seat 2",
     "answer": "One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand",
     "effect": "The answer is stored for the next step."},
    {"action": "update", "who": "seat 2", "answer": null,
     "effect": "Resolved as in the seat 1 play/discard step, on seat 2's attributes."},
    {"action": "ask", "who": "seat 2", "when": "deck_count > 0 or any discard top other than turn_discard is non-empty",
     "answer": "One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard",
     "effect": "The answer is stored for the next step."},
    {"action": "update", "who": "seat 2", "answer": null,
     "effect": "Resolved as in the seat 1 draw step, into seat 2's hand. Set turn_discard = ''."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce seat 2's played or discarded card, the draw source (deck, a discard colour, or nothing; a deck card's identity is not shown) and deck_count."},

    {"action": "ask", "who": "seat 1", "when": "deal == 2",
     "answer": "One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand",
     "effect": "The answer is stored for the next step."},
    {"action": "update", "who": "seat 1", "answer": null, "when": "deal == 2",
     "effect": "Resolved as in the seat 1 play/discard step above."},
    {"action": "ask", "who": "seat 1", "when": "deal == 2 and (deck_count > 0 or any discard top other than turn_discard is non-empty)",
     "answer": "One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard",
     "effect": "The answer is stored for the next step."},
    {"action": "update", "who": "seat 1", "answer": null, "when": "deal == 2",
     "effect": "Resolved as in the seat 1 draw step above. Set turn_discard = ''."},
    {"action": "tell", "who": "all players", "answer": null, "when": "deal == 2",
     "effect": "Announce seat 1's played or discarded card, the draw source and deck_count."},

    {"action": "update", "who": "all players", "answer": null, "when": "deck_count == 0 or round_in_deal == 20",
     "effect": "End of deal: for each player and each colour X, if X_top > 0 or X_wagers > 0, then match_score += (X_sum - 20) * (1 + X_wagers); otherwise that colour adds 0. Cards in hand score nothing. Then, if deal == 2, set match_over = true; otherwise set deal = 2 and round_in_deal = 0."},
    {"action": "tell", "who": "all players", "answer": null, "when": "round_in_deal == 0 or match_over == true",
     "effect": "Announce each player's colour scores for the deal and their match_score."},
    {"action": "check", "who": "all players", "answer": null,
     "effect": "End the game if match_over == true; otherwise continue."}
  ],
  "ending": {
    "condition": "match_over == true",
    "rank_by": "you.match_score",
    "decided_by": "After both deals, the player with the higher match_score wins. Equal match scores share the win, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When a deal starts, the deck holds 44 cards: for each of Red, Blue, Green and Yellow, the numbers 2 to 10 and two wagers (W1, W2)."},
    {"id": "R2", "text": "When a deal starts, every sum, top and wagers record is 0, every discard top is empty, each player is dealt 6 random cards from the deck, and deck_count is 32."},
    {"id": "R3", "text": "When the match is in deal 1, seat 1 takes the first turn of every round and seat 2 the second; in deal 2, seat 2 goes first and seat 1 second."},
    {"id": "R4", "text": "When a player plays number card n of colour X and n > X_top, then X_sum increases by n and X_top becomes n (for example, playing Red 7 with red_top 5 and red_sum 5 gives red_sum 12 and red_top 7)."},
    {"id": "R5", "text": "When a player plays a wager of colour X while X_top == 0, then X_wagers increases by 1."},
    {"id": "R6", "text": "When a player plays a number card not greater than X_top, or a wager while X_top > 0, then the card is discarded instead."},
    {"id": "R7", "text": "When a card of colour X is discarded, it becomes discard_X, and the card previously in discard_X is moved to removed_cards."},
    {"id": "R8", "text": "When a player draws from the deck and deck_count > 0, then a random deck card goes to their hand and deck_count decreases by 1."},
    {"id": "R9", "text": "When a player draws a non-empty discard top other than the card they discarded this turn, then that card goes to their hand and that discard top becomes empty."},
    {"id": "R10", "text": "When a player names an unavailable draw source, then they take the deck top if deck_count > 0."},
    {"id": "R11", "text": "When the deck is empty, the player takes an available discard top; when none is available apart from the card they just discarded, they draw nothing."},
    {"id": "R12", "text": "When a turn ends, both players are told the card played or discarded, the draw source (not the identity of a deck card) and deck_count."},
    {"id": "R13", "text": "When a round ends with deck_count == 0 or round_in_deal == 20, then the deal ends."},
    {"id": "R14", "text": "When a deal ends, each colour with X_top > 0 or X_wagers > 0 adds (X_sum - 20) * (1 + X_wagers) to match_score (for example, sum 27 with 1 wager gives +14), and any other colour adds 0."},
    {"id": "R15", "text": "When a colour has only wagers played (top 0 and wagers w > 0), it scores -20 * (1 + w)."},
    {"id": "R16", "text": "When a deal ends, cards still in hand score nothing, and match_score may go negative."},
    {"id": "R17", "text": "When deal 2 ends, the match is over and the higher match_score wins; equal scores are a draw."},
    {"id": "R18", "text": "The match always ends within 40 rounds (at most 20 rounds in each of the 2 deals)."}
  ],
  "offers": [
    {"question": "Play or discard", "who": "the seat whose turn it is",
     "options": "For each card in hand: 'discard <card>'. Also 'play <card>' for each number card whose number is greater than that colour's top, and for each wager whose colour top is 0."},
    {"question": "Draw source", "who": "the seat whose turn it is",
     "options": "'deck' if deck_count > 0, plus 'discard <colour>' for each non-empty discard top that is not the card discarded this turn. If no option exists, the question is skipped and nothing is drawn."}
  ],
  "choices": [
    {"what": "Exactly 2 players (min 2, max 2, suggested 2)", "why": "The designer fixed 2. The match structure (alternating leaders over two deals, a shared discard row contested by one rival) is a head-to-head duel, and a third player would break the deal and turn structure."},
    {"what": "No talk step", "why": "With two opponents in a zero-sum duel, talk gives nothing to coordinate on and only adds words."},
    {"what": "Strategy check", "why": "A thoughtful player commits to colours early with wagers only when they hold strong cards, plays numbers in rising order without skipping too far, avoids discarding cards the opponent needs, reads the opponent's discard draws, and manages the 20-round and deck clock."},
    {"what": "Card names such as 'Red 7' and 'Red W1'/'Red W2'", "why": "The two wagers of a colour need distinct list entries."},
    {"what": "Only legal plays are offered", "why": "A seat is never offered what it may not do. The rule that an illegal play becomes a discard is kept as a fallback for invalid answers."},
    {"what": "With an empty deck and an unavailable source named, the discard top taken is the first available in the order Red, Blue, Green, Yellow", "why": "The source says 'you take a discard top' without saying which."},
    {"what": "Covered discards go to a hidden removed_cards list", "why": "The rules say they leave the game. They were already announced when discarded."}
  ],
  "simplifications": [
    {"what": "The two seat orders are written as one flat list: a seat 1 turn when deal == 1, then a seat 2 turn, then a seat 1 turn when deal == 2", "why": "The step list is flat. Per-step `when` conditions give the correct leader in each deal without a conditional block."},
    {"what": "The deck is an unordered hidden list and a deck draw picks a random card", "why": "Drawing at random from a list is equivalent to drawing the top of a shuffled deck."},
    {"what": "The start of each deal runs as round steps gated by round_in_deal == 0", "why": "This lets the same script reset and deal again for deal 2."}
  ],
  "unsupported": []
}
```
````
