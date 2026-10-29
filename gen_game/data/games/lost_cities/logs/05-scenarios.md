# 05 scenarios

- time: 2026-10-27T08:39:41+00:00 (122.5s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 0796add7613be73c, reply sha256 1fa35e13678f7935

## Sent

````
SPEC:
{
  "name": "Lost Cities: Four Expeditions",
  "summary": "Two players spend two deals building four colour expeditions with rising number cards and optional up-front wagers, discarding and drawing from a shared deck and face-up discard tops; each colour scores (sum - 20) x (1 + wagers).",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
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
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards held. Each card is a text such as 'Red 7' or 'Red W1'.",
        "observable": false
      },
      {
        "key": "red_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of number cards played in Red this deal",
        "observable": true
      },
      {
        "key": "red_top",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest number played in Red this deal (0 = none)",
        "observable": true
      },
      {
        "key": "red_wagers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wager cards played in Red this deal",
        "observable": true
      },
      {
        "key": "blue_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of number cards played in Blue this deal",
        "observable": true
      },
      {
        "key": "blue_top",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest number played in Blue this deal (0 = none)",
        "observable": true
      },
      {
        "key": "blue_wagers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wager cards played in Blue this deal",
        "observable": true
      },
      {
        "key": "green_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of number cards played in Green this deal",
        "observable": true
      },
      {
        "key": "green_top",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest number played in Green this deal (0 = none)",
        "observable": true
      },
      {
        "key": "green_wagers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wager cards played in Green this deal",
        "observable": true
      },
      {
        "key": "yellow_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of number cards played in Yellow this deal",
        "observable": true
      },
      {
        "key": "yellow_top",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest number played in Yellow this deal (0 = none)",
        "observable": true
      },
      {
        "key": "yellow_wagers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wager cards played in Yellow this deal",
        "observable": true
      },
      {
        "key": "match_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running match score over both deals. It can go negative.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Face-down draw deck. Its order is hidden and a draw picks a card at random.",
        "observable": false
      },
      {
        "key": "deck_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cards left in the deck",
        "observable": true
      },
      {
        "key": "discard_red",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Face-up top discard card of Red ('' = none)",
        "observable": true
      },
      {
        "key": "discard_blue",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Face-up top discard card of Blue ('' = none)",
        "observable": true
      },
      {
        "key": "discard_green",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Face-up top discard card of Green ('' = none)",
        "observable": true
      },
      {
        "key": "discard_yellow",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Face-up top discard card of Yellow ('' = none)",
        "observable": true
      },
      {
        "key": "removed_cards",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Discard tops that were covered by a newer discard and so removed from the game",
        "observable": false
      },
      {
        "key": "turn_discard",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card discarded in the current turn ('' if the card was played). It may not be drawn back this turn.",
        "observable": false
      },
      {
        "key": "deal",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current deal (1 or 2). Seat 1 leads deal 1 and seat 2 leads deal 2.",
        "observable": true
      },
      {
        "key": "round_in_deal",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rounds started in the current deal (0 = a new deal must be dealt)",
        "observable": true
      },
      {
        "key": "match_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once deal 2 has been scored",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat 1 is Player A and seat 2 is Player B.",
    "Set deal = 1, round_in_deal = 0, match_over = false and each player's match_score = 0.",
    "The first round step deals deal 1 (it runs whenever round_in_deal = 0)."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "round_in_deal == 0",
      "effect": "Start of a deal: set every player's red/blue/green/yellow _sum, _top and _wagers to 0. Set discard_red, discard_blue, discard_green and discard_yellow to ''. Set removed_cards = [] and every hand = []. Set deck to all 44 cards: for each colour Red, Blue, Green and Yellow, the cards '<Colour> 2' to '<Colour> 10' plus '<Colour> W1' and '<Colour> W2'. Deal 6 cards to each player, each one drawn at random from deck, appended to hand and removed from deck. Set deck_count = 32."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "when": "round_in_deal == 0",
      "effect": "Each player sees their own hand and all public attributes."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_in_deal += 1."
    },
    {
      "action": "ask",
      "who": "seat 1",
      "when": "deal == 1",
      "answer": "One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand",
      "effect": "The answer is stored for the next step."
    },
    {
      "action": "update",
      "who": "seat 1",
      "answer": null,
      "when": "deal == 1",
      "effect": "Remove the chosen card from seat 1's hand. If it is a PLAY of number card n of colour X and n > X_top: X_sum += n and X_top = n, and turn_discard = ''. If it is a PLAY of a wager of colour X and X_top == 0: X_wagers += 1, and turn_discard = ''. Otherwise (a DISCARD, or an illegal PLAY): if discard_X != '', append discard_X to removed_cards; then discard_X = card and turn_discard = card."
    },
    {
      "action": "ask",
      "who": "seat 1",
      "when": "deal == 1 and (deck_count > 0 or any discard top other than turn_discard is non-empty)",
      "answer": "One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard",
      "effect": "The answer is stored for the next step."
    },
    {
      "action": "update",
      "who": "seat 1",
      "answer": null,
      "when": "deal == 1",
      "effect": "If a discard top of colour X was named, is non-empty and is not turn_discard: append discard_X to hand and set discard_X = ''. Else if deck_count > 0: draw a random card from deck into hand and deck_count -= 1. Else, if any discard top other than turn_discard is non-empty: take the first one in the order Red, Blue, Green, Yellow into hand and set it to ''. Otherwise draw nothing. Set turn_discard = ''."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "deal == 1",
      "effect": "Announce seat 1's played or discarded card, the draw source (deck, a discard colour, or nothing; a deck card's identity is not shown) and deck_count."
    },
    {
      "action": "ask",
      "who": "seat 2",
      "answer": "One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand",
      "effect": "The answer is stored for the next step."
    },
    {
      "action": "update",
      "who": "seat 2",
      "answer": null,
      "effect": "Resolved as in the seat 1 play/discard step, on seat 2's attributes."
    },
    {
      "action": "ask",
      "who": "seat 2",
      "when": "deck_count > 0 or any discard top other than turn_discard is non-empty",
      "answer": "One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard",
      "effect": "The answer is stored for the next step."
    },
    {
      "action": "update",
      "who": "seat 2",
      "answer": null,
      "effect": "Resolved as in the seat 1 draw step, into seat 2's hand. Set turn_discard = ''."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce seat 2's played or discarded card, the draw source (deck, a discard colour, or nothing; a deck card's identity is not shown) and deck_count."
    },
    {
      "action": "ask",
      "who": "seat 1",
      "when": "deal == 2",
      "answer": "One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand",
      "effect": "The answer is stored for the next step."
    },
    {
      "action": "update",
      "who": "seat 1",
      "answer": null,
      "when": "deal == 2",
      "effect": "Resolved as in the seat 1 play/discard step above."
    },
    {
      "action": "ask",
      "who": "seat 1",
      "when": "deal == 2 and (deck_count > 0 or any discard top other than turn_discard is non-empty)",
      "answer": "One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard",
      "effect": "The answer is stored for the next step."
    },
    {
      "action": "update",
      "who": "seat 1",
      "answer": null,
      "when": "deal == 2",
      "effect": "Resolved as in the seat 1 draw step above. Set turn_discard = ''."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "deal == 2",
      "effect": "Announce seat 1's played or discarded card, the draw source and deck_count."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "deck_count == 0 or round_in_deal == 20",
      "effect": "End of deal: for each player and each colour X, if X_top > 0 or X_wagers > 0, then match_score += (X_sum - 20) * (1 + X_wagers); otherwise that colour adds 0. Cards in hand score nothing. Then, if deal == 2, set match_over = true; otherwise set deal = 2 and round_in_deal = 0."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "round_in_deal == 0 or match_over == true",
      "effect": "Announce each player's colour scores for the deal and their match_score."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if match_over == true; otherwise continue."
    }
  ],
  "ending": {
    "condition": "match_over == true",
    "rank_by": "you.match_score",
    "decided_by": "After both deals, the player with the higher match_score wins. Equal match scores share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a deal starts, the deck holds 44 cards: for each of Red, Blue, Green and Yellow, the numbers 2 to 10 and two wagers (W1, W2)."
    },
    {
      "id": "R2",
      "text": "When a deal starts, every sum, top and wagers record is 0, every discard top is empty, each player is dealt 6 random cards from the deck, and deck_count is 32."
    },
    {
      "id": "R3",
      "text": "When the match is in deal 1, seat 1 takes the first turn of every round and seat 2 the second; in deal 2, seat 2 goes first and seat 1 second."
    },
    {
      "id": "R4",
      "text": "When a player plays number card n of colour X and n > X_top, then X_sum increases by n and X_top becomes n (for example, playing Red 7 with red_top 5 and red_sum 5 gives red_sum 12 and red_top 7)."
    },
    {
      "id": "R5",
      "text": "When a player plays a wager of colour X while X_top == 0, then X_wagers increases by 1."
    },
    {
      "id": "R6",
      "text": "When a player plays a number card not greater than X_top, or a wager while X_top > 0, then the card is discarded instead."
    },
    {
      "id": "R7",
      "text": "When a card of colour X is discarded, it becomes discard_X, and the card previously in discard_X is moved to removed_cards."
    },
    {
      "id": "R8",
      "text": "When a player draws from the deck and deck_count > 0, then a random deck card goes to their hand and deck_count decreases by 1."
    },
    {
      "id": "R9",
      "text": "When a player draws a non-empty discard top other than the card they discarded this turn, then that card goes to their hand and that discard top becomes empty."
    },
    {
      "id": "R10",
      "text": "When a player names an unavailable draw source, then they take the deck top if deck_count > 0."
    },
    {
      "id": "R11",
      "text": "When the deck is empty, the player takes an available discard top; when none is available apart from the card they just discarded, they draw nothing."
    },
    {
      "id": "R12",
      "text": "When a turn ends, both players are told the card played or discarded, the draw source (not the identity of a deck card) and deck_count."
    },
    {
      "id": "R13",
      "text": "When a round ends with deck_count == 0 or round_in_deal == 20, then the deal ends."
    },
    {
      "id": "R14",
      "text": "When a deal ends, each colour with X_top > 0 or X_wagers > 0 adds (X_sum - 20) * (1 + X_wagers) to match_score (for example, sum 27 with 1 wager gives +14), and any other colour adds 0."
    },
    {
      "id": "R15",
      "text": "When a colour has only wagers played (top 0 and wagers w > 0), it scores -20 * (1 + w)."
    },
    {
      "id": "R16",
      "text": "When a deal ends, cards still in hand score nothing, and match_score may go negative."
    },
    {
      "id": "R17",
      "text": "When deal 2 ends, the match is over and the higher match_score wins; equal scores are a draw."
    },
    {
      "id": "R18",
      "text": "The match always ends within 40 rounds (at most 20 rounds in each of the 2 deals)."
    }
  ],
  "offers": [
    {
      "question": "Play or discard",
      "who": "the seat whose turn it is",
      "options": "For each card in hand: 'discard <card>'. Also 'play <card>' for each number card whose number is greater than that colour's top, and for each wager whose colour top is 0."
    },
    {
      "question": "Draw source",
      "who": "the seat whose turn it is",
      "options": "'deck' if deck_count > 0, plus 'discard <colour>' for each non-empty discard top that is not the card discarded this turn. If no option exists, the question is skipped and nothing is drawn."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (min 2, max 2, suggested 2)",
      "why": "The designer fixed 2. The match structure (alternating leaders over two deals, a shared discard row contested by one rival) is a head-to-head duel, and a third player would break the deal and turn structure."
    },
    {
      "what": "No talk step",
      "why": "With two opponents in a zero-sum duel, talk gives nothing to coordinate on and only adds words."
    },
    {
      "what": "Strategy check",
      "why": "A thoughtful player commits to colours early with wagers only when they hold strong cards, plays numbers in rising order without skipping too far, avoids discarding cards the opponent needs, reads the opponent's discard draws, and manages the 20-round and deck clock."
    },
    {
      "what": "Card names such as 'Red 7' and 'Red W1'/'Red W2'",
      "why": "The two wagers of a colour need distinct list entries."
    },
    {
      "what": "Only legal plays are offered",
      "why": "A seat is never offered what it may not do. The rule that an illegal play becomes a discard is kept as a fallback for invalid answers."
    },
    {
      "what": "With an empty deck and an unavailable source named, the discard top taken is the first available in the order Red, Blue, Green, Yellow",
      "why": "The source says 'you take a discard top' without saying which."
    },
    {
      "what": "Covered discards go to a hidden removed_cards list",
      "why": "The rules say they leave the game. They were already announced when discarded."
    }
  ],
  "simplifications": [
    {
      "what": "The two seat orders are written as one flat list: a seat 1 turn when deal == 1, then a seat 2 turn, then a seat 1 turn when deal == 2",
      "why": "The step list is flat. Per-step `when` conditions give the correct leader in each deal without a conditional block."
    },
    {
      "what": "The deck is an unordered hidden list and a deck draw picks a random card",
      "why": "Drawing at random from a list is equivalent to drawing the top of a shuffled deck."
    },
    {
      "what": "The start of each deal runs as round steps gated by round_in_deal == 0",
      "why": "This lets the same script reset and deal again for deal 2."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: red_sum, red_top, red_wagers, blue_sum, blue_top, blue_wagers, green_sum, green_top, green_wagers, yellow_sum, yellow_top, yellow_wagers, match_score; table: deck_count, discard_red, discard_blue, discard_green, discard_yellow, deal, round_in_deal, match_over.
````

## Reply

````
[
  {"name": "Deck holds 44 cards: after the deal and one deck draw each, 30 remain", "rule": "R1", "players": 2, "rounds": 1, "seed": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": "deck", "times": "all"},
             {"seat": 2, "options_include": "deck", "times": "all"},
             {"seat": 1, "options_include": "discard ", "times": "all"},
             {"seat": 2, "options_include": "discard ", "times": "all"}],
   "expect": {"game": {"deck_count": 30, "deal": 1, "round_in_deal": 1},
              "lens": {"game": {"deck": 30}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}}}},
  {"name": "Deal start: records zero, 6 cards each, deck_count 32 (only discards played, both draw deck)", "rule": "R2", "players": 2, "rounds": 1, "seed": 2, "default": "first",
   "rules": [{"seat": 1, "options_include": "deck", "times": "all"},
             {"seat": 2, "options_include": "deck", "times": "all"},
             {"seat": 1, "options_include": "discard ", "times": "all"},
             {"seat": 2, "options_include": "discard ", "times": "all"}],
   "expect": {"game": {"deck_count": 30},
              "players": {"1": {"red_sum": 0, "red_top": 0, "red_wagers": 0, "blue_sum": 0, "blue_top": 0, "blue_wagers": 0, "green_sum": 0, "green_top": 0, "green_wagers": 0, "yellow_sum": 0, "yellow_top": 0, "yellow_wagers": 0, "match_score": 0},
                          "2": {"red_sum": 0, "red_top": 0, "red_wagers": 0, "blue_sum": 0, "blue_top": 0, "blue_wagers": 0, "green_sum": 0, "green_top": 0, "green_wagers": 0, "yellow_sum": 0, "yellow_top": 0, "yellow_wagers": 0, "match_score": 0}},
              "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}}}}},
  {"name": "Deal 1: seat 1 discards first, so seat 2's red discard ends on top", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Red 7"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Red 5"}],
   "expect": {"game": {"discard_red": "Red 5", "deck_count": 8}}},
  {"name": "Deal 2: seat 2 discards first, so seat 1's red discard ends on top", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 2, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Red 7"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Red 5"}],
   "expect": {"game": {"discard_red": "Red 7", "deck_count": 8}}},
  {"name": "Playing Red 7 on red_top 5 / red_sum 5 gives sum 12 top 7", "rule": "R4", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"], "red_sum": 5, "red_top": 5},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "play Red 7"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"players": {"1": {"red_sum": 12, "red_top": 7, "red_wagers": 0}},
              "game": {"discard_red": "", "deck_count": 8},
              "offered": [{"seat": 1, "option": "play Red 7"}]}},
  {"name": "Wager on an empty colour adds 1 wager; wager on a started colour is not offered", "rule": "R5", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red W1", "Blue W1", "Green 4", "Yellow 5", "Blue 9", "Green 9"], "blue_sum": 5, "blue_top": 5},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "play Red W1"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Green 5"}],
   "expect": {"players": {"1": {"red_wagers": 1, "red_sum": 0, "red_top": 0, "blue_wagers": 0, "blue_sum": 5}},
              "offered": [{"seat": 1, "option": "play Red W1"}],
              "not_offered": [{"seat": 1, "option": "play Blue W1"}]}},
  {"name": "Cards not above the top and late wagers are not playable; discarding Red 7 leaves red unchanged", "rule": "R6", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Red 8", "Red W2", "Blue 3", "Green 4", "Yellow 5"], "red_sum": 8, "red_top": 8},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Red 7"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"players": {"1": {"red_sum": 8, "red_top": 8, "red_wagers": 0}},
              "game": {"discard_red": "Red 7"},
              "offered": [{"seat": 1, "option": "play Blue 3"}],
              "not_offered": [{"seat": 1, "option": "play Red 7"}, {"seat": 1, "option": "play Red 8"}, {"seat": 1, "option": "play Red W2"}]}},
  {"name": "Discard covers the previous top, which leaves the game", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10, "discard_red": "Red 3", "removed_cards": [],
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 6", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Red 7"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Green 5"}],
   "expect": {"game": {"discard_red": "Red 7", "discard_green": "Green 5", "deck_count": 8},
              "lens": {"game": {"removed_cards": 1}}}},
  {"name": "Each deck draw moves one card to hand and lowers deck_count by 1", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Blue 3"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"game": {"deck_count": 8},
              "lens": {"game": {"deck": 8}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}}}},
  {"name": "Drawing a discard top takes it into hand and empties that top", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Yellow 5", "Blue 9", "Red 9", "Yellow 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10, "discard_green": "Green 6", "removed_cards": [],
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "discard Blue 3"}, {"seat": 1, "options_include": "discard Green"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"game": {"discard_green": "", "discard_blue": "Blue 4", "deck_count": 9},
              "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}}, "game": {"removed_cards": 1}}}},
  {"name": "Naming an empty discard pile draws from the deck instead", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "discard Blue 3"}, {"seat": 1, "options_include": "deck", "answer": "discard Yellow"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Green 5"}],
   "expect": {"game": {"deck_count": 8, "discard_yellow": "", "discard_blue": "Blue 3"},
              "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}}}}},
  {"name": "Empty deck: take an available discard top; if only your own discard remains, draw nothing", "rule": "R11", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9", "Yellow 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 5, "deck_count": 0, "deck": [], "discard_red": "Red 3"}},
   "rules": [{"seat": 1, "options_include": "discard Blue 3"},
             {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"game": {"discard_red": "", "discard_blue": "Blue 4", "deck_count": 0},
              "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 5}}}}},
  {"name": "After both turns the public deck_count reflects the two deck draws", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"]},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"]}},
             "game": {"deal": 1, "round_in_deal": 3, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Yellow 5"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Yellow 6"}],
   "expect": {"game": {"deck_count": 8, "discard_yellow": "Yellow 6"}}},
  {"name": "Round 20 of deal 1 ends the deal: red sum 25 scores +5, deal 2 begins", "rule": "R13", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"], "red_sum": 25, "red_top": 10, "match_score": 0},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"], "match_score": 0}},
             "game": {"deal": 1, "round_in_deal": 19, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Blue 3"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"game": {"deal": 2, "round_in_deal": 0, "match_over": false},
              "players": {"1": {"match_score": 5}, "2": {"match_score": 0}}}},
  {"name": "Deal 2 scoring: sum 27 with 1 wager gives +14, beating sum 30 with no wager (+10)", "rule": "R14", "players": 2,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"], "red_sum": 27, "red_top": 10, "red_wagers": 1, "match_score": 0},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"], "blue_sum": 30, "blue_top": 10, "match_score": 0}},
             "game": {"deal": 2, "round_in_deal": 19, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Green 4"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Green 5"}],
   "expect": {"winner": 1, "standings": {"1": 14, "2": 10},
              "game": {"match_over": true},
              "players": {"1": {"match_score": 14}, "2": {"match_score": 10}}}},
  {"name": "Yellow with only 2 wagers scores -60", "rule": "R15", "players": 2,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"], "yellow_wagers": 2, "yellow_top": 0, "yellow_sum": 0, "match_score": 0},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"], "match_score": 0}},
             "game": {"deal": 2, "round_in_deal": 19, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Blue 3"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"winner": 2, "standings": {"1": -60, "2": 0},
              "players": {"1": {"match_score": -60}, "2": {"match_score": 0}}}},
  {"name": "Hand cards score nothing and match_score goes negative (5 + (4-20) = -11)", "rule": "R16", "players": 2,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"], "green_sum": 4, "green_top": 4, "match_score": 5},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"], "match_score": -3}},
             "game": {"deal": 2, "round_in_deal": 19, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Blue 3"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"winner": 2, "standings": {"1": -11, "2": -3},
              "players": {"1": {"match_score": -11, "green_sum": 4}, "2": {"match_score": -3}}}},
  {"name": "Equal match scores after deal 2 share the win", "rule": "R17", "players": 2,
   "given": {"players": {"1": {"hand": ["Red 7", "Blue 3", "Green 4", "Yellow 5", "Blue 9", "Green 9"], "match_score": 10},
                         "2": {"hand": ["Red 5", "Blue 4", "Green 5", "Yellow 6", "Blue 10", "Green 10"], "match_score": 10}},
             "game": {"deal": 2, "round_in_deal": 19, "deck_count": 10,
                      "deck": ["Yellow 2", "Yellow 3", "Yellow 4", "Red 2", "Red 3", "Red 4", "Blue 2", "Green 2", "Green 3", "Yellow 7"]}},
   "rules": [{"seat": 1, "options_include": "deck"}, {"seat": 1, "options_include": "discard Blue 3"},
             {"seat": 2, "options_include": "deck"}, {"seat": 2, "options_include": "discard Blue 4"}],
   "expect": {"winner": [1, 2], "standings": {"1": 10, "2": 10},
              "game": {"match_over": true}}},
  {"name": "A full random match is over within 40 rounds (only match_over and deal asserted)", "rule": "R18", "players": 2, "rounds": 40, "seed": 7, "default": "first",
   "rules": [{"seat": 1, "options_include": "deck", "times": "all"},
             {"seat": 2, "options_include": "deck", "times": "all"}],
   "expect": {"game": {"match_over": true, "deal": 2}}}
]
````
