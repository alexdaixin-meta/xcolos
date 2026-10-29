# 13 scenarios

- time: 2026-10-28T03:16:05+00:00 (37.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 40a04fd2fd624b00, reply sha256 9e0db56405e7f58f

## Sent

````
SPEC:
{
  "name": "Short Reversis",
  "summary": "A 4-player trick-avoidance card game over 4 hands with a 24-card deck. Players pass cards, then try not to take points; whoever takes all 6 tricks in a hand (a reversis) scores 0 and every other player scores 15. The lowest total after 4 hands wins.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "num_players": 4,
    "deck_size": 24,
    "num_hands": 4,
    "cards_dealt_per_player": 6,
    "pass_count": 2,
    "last_passing_hand": 3,
    "tricks_per_hand": 6,
    "rounds_per_hand": 7,
    "total_rounds": 28,
    "points_ace": 4,
    "points_king": 3,
    "points_queen": 2,
    "points_jack": 1,
    "points_quinola_jack_of_hearts": 5,
    "points_nine": 0,
    "points_eight": 0,
    "points_total_per_hand": 44,
    "reversis_tricks": 6,
    "reversis_taker_score": 0,
    "reversis_other_score": 15,
    "rank_value_ace": 6,
    "rank_value_king": 5,
    "rank_value_queen": 4,
    "rank_value_jack": 3,
    "rank_value_nine": 2,
    "rank_value_eight": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards the player holds, coded rank+suit, e.g. 'AS', 'JH', '9D', '8C'",
        "observable": false
      },
      {
        "key": "pass_1",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "First card chosen to pass this hand",
        "observable": false
      },
      {
        "key": "pass_2",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "Second card chosen to pass this hand",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Card played face up to the current trick",
        "observable": false
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won in the current hand",
        "observable": true
      },
      {
        "key": "hand_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card points taken in the current hand",
        "observable": true
      },
      {
        "key": "hand_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Score for the hand just finished, after the reversis rule",
        "observable": false
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running total of hand scores; lower is better",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "AS",
          "KS",
          "QS",
          "JS",
          "9S",
          "8S",
          "AH",
          "KH",
          "QH",
          "JH",
          "9H",
          "8H",
          "AD",
          "KD",
          "QD",
          "JD",
          "9D",
          "8D",
          "AC",
          "KC",
          "QC",
          "JC",
          "9C",
          "8C"
        ],
        "meaning": "Undealt cards of the 24-card deck",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current hand, 1 to 4",
        "observable": true
      },
      {
        "key": "trick_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks completed in the current hand, 0 to 6",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that leads the current trick",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Suit of the card led to the current trick (S, H, D or C)",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the last trick",
        "observable": false
      },
      {
        "key": "played_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "All cards played face up so far in this hand",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1 to 4 sit in a circle; play order is 1, 2, 3, 4, then back to 1.",
    "Every player's total starts at 0 and hand_number starts at 0.",
    "No cards are dealt yet; the deal happens at the start of each hand."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "One round of the script is one hand. hand_number += 1. deck is reset to all 24 cards. Every hand, played_cards, pass_1, pass_2 and played_card is cleared. Each player draws 6 cards at random from deck into their hand (24 draws in all, emptying the deck). trick_number = 0. leader = hand_number."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hand of 6 cards."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from your own hand",
      "effect": "when hand_number <= 3: pass_1 = the chosen card. Nobody sees any choice until all are in."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from your own hand other than pass_1",
      "effect": "when hand_number <= 3: pass_2 = the chosen card."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when hand_number <= 3: each player's pass_1 and pass_2 are removed from their hand and appended to the receiver's hand. The receiver is seat (seat mod 4)+1 (left) in hand 1, seat ((seat+2) mod 4)+1 (right) in hand 2, and seat ((seat+1) mod 4)+1 (across) in hand 3. Each passer and receiver is told privately which two cards moved. Every hand again holds 6 cards."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Passing is complete.' In hand 4 the announcement says there was no pass."
    },
    {
      "action": "repeat",
      "who": "all players",
      "answer": null,
      "effect": "Run the next 6 steps (one trick) until trick_number = 6."
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "any card from your hand",
      "effect": "played_card = the chosen card; led_suit = its suit; the card is removed from hand and appended to played_cards; the play is announced to everyone."
    },
    {
      "action": "ask",
      "who": "seat (leader mod 4)+1",
      "answer": "a card of led_suit from your hand if you hold one, otherwise any card from your hand",
      "effect": "played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone."
    },
    {
      "action": "ask",
      "who": "seat ((leader+1) mod 4)+1",
      "answer": "a card of led_suit from your hand if you hold one, otherwise any card from your hand",
      "effect": "played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone."
    },
    {
      "action": "ask",
      "who": "seat ((leader+2) mod 4)+1",
      "answer": "a card of led_suit from your hand if you hold one, otherwise any card from your hand",
      "effect": "played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_winner = the seat whose played_card has suit led_suit and the highest rank value (A=6, K=5, Q=4, J=3, 9=2, 8=1). That seat's hand_points += the sum of the points of the 4 played cards (A=4, K=3, Q=2, J=1 except JH=5, 9=0, 8=0). That seat's tricks_won += 1. leader = trick_winner. trick_number += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {trick_winner} wins trick {trick_number} and takes {points} points.' with each player's hand_points and tricks_won."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "End of hand. If some player has tricks_won = 6, that player's hand_score = 0 and every other player's hand_score = 15. Otherwise each player's hand_score = hand_points. Each player's total += hand_score. Then hand_points = 0 and tricks_won = 0 for every player."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce each player's hand_score and running total, and whether a reversis happened."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If hand_number = 4, end the game; otherwise start the next hand."
    }
  ],
  "ending": {
    "condition": "hand_number = 4 after the end-of-hand scoring",
    "rank_by": "0 - you.total",
    "decided_by": "Each player's standing is their running total after 4 hands, and lower is better. The player with the lowest total wins; players tied for the lowest total share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a hand starts, then the deck holds 24 cards (A, K, Q, J, 9, 8 of spades, hearts, diamonds and clubs) and each player is dealt 6 cards at random into their hand, seen only by that player."
    },
    {
      "id": "R2",
      "text": "When it is hand 1, 2 or 3, then all players simultaneously choose 2 different cards from their hand to pass, and no one sees another's choice before all have chosen."
    },
    {
      "id": "R3",
      "text": "When it is hand 1, then each seat s passes its 2 cards to seat (s mod 4)+1 (left), so seat 4 passes to seat 1."
    },
    {
      "id": "R4",
      "text": "When it is hand 2, then each seat s passes its 2 cards to the previous seat (right), so seat 1 passes to seat 4."
    },
    {
      "id": "R5",
      "text": "When it is hand 3, then each seat s passes its 2 cards to the seat two away (across): 1 with 3, and 2 with 4."
    },
    {
      "id": "R6",
      "text": "When cards are passed, then they leave the passer's hand and join the receiver's hand only after everyone has chosen, every hand still holds 6 cards, and only the passer and the receiver learn which cards moved."
    },
    {
      "id": "R7",
      "text": "When it is hand 4, then no cards are passed."
    },
    {
      "id": "R8",
      "text": "When passing is over, then the game announces that passing is complete."
    },
    {
      "id": "R9",
      "text": "When the first trick of hand h starts, then seat h leads (seat 1 in hand 1, seat 4 in hand 4)."
    },
    {
      "id": "R10",
      "text": "When any later trick starts, then the winner of the previous trick leads."
    },
    {
      "id": "R11",
      "text": "When a trick is played, then the leader plays first and the other 3 players follow one at a time in seat order, each playing one card face up."
    },
    {
      "id": "R12",
      "text": "When the leader plays, then they may play any card in their hand."
    },
    {
      "id": "R13",
      "text": "When a non-leader holds a card of the led suit, then they must play a card of that suit."
    },
    {
      "id": "R14",
      "text": "When a non-leader holds no card of the led suit, then they may play any card in their hand."
    },
    {
      "id": "R15",
      "text": "When all 4 cards are played, then the highest card of the led suit wins the trick (A > K > Q > J > 9 > 8), there are no trumps, and a card of another suit never wins."
    },
    {
      "id": "R16",
      "text": "When a player wins a trick, then their hand points rise by the trick's card points (A=4, K=3, Q=2, J=1, Jack of Hearts=5, 9=0, 8=0) and their trick count for the hand rises by 1."
    },
    {
      "id": "R17",
      "text": "When a hand ends with no player winning all 6 tricks, then each player's hand score equals the card points they took, and the four scores total 44."
    },
    {
      "id": "R18",
      "text": "When a hand ends with one player winning all 6 tricks (a reversis), then that player scores 0 for the hand and each other player scores 15."
    },
    {
      "id": "R19",
      "text": "When a hand ends, then each hand score is added to that player's public running total, and hand points and trick counts reset to 0."
    },
    {
      "id": "R20",
      "text": "When the 4th hand has been scored, then the game ends."
    },
    {
      "id": "R21",
      "text": "When the game ends, then the player with the lowest running total wins, and players tied for the lowest total share the result (a draw)."
    }
  ],
  "offers": [
    {
      "question": "First card to pass (hands 1 to 3)",
      "who": "all players at once",
      "options": "every card in the player's own hand"
    },
    {
      "question": "Second card to pass (hands 1 to 3)",
      "who": "all players at once",
      "options": "every card in the player's own hand except the one already chosen as pass_1"
    },
    {
      "question": "Lead a card",
      "who": "seat leader",
      "options": "every card in the leader's hand"
    },
    {
      "question": "Follow to the trick",
      "who": "each of the 3 seats after the leader, in seat order",
      "options": "a seat holding at least one card of led_suit: only its cards of led_suit; a seat holding no card of led_suit: every card in its hand"
    }
  ],
  "choices": [
    {
      "what": "4 players, minimum 4 and maximum 4",
      "why": "The designer fixed 4 seats. The deck of 24 cards deals exactly 6 to each of 4 players, the left/right/across passing needs exactly 4 seats, and the 15-point reversis payment is set for 3 opponents."
    },
    {
      "what": "No talk step before plays",
      "why": "The source has no table talk. Adding it would add a mechanic, and in a trick game it would leak hidden hands."
    },
    {
      "what": "One script round equals one hand (deal, pass, then 6 tricks run by a repeat)",
      "why": "The source's 7 rounds per hand (1 pass + 6 tricks) map onto one script round, and the game ends after 4 such rounds, giving 28 source rounds in all."
    },
    {
      "what": "Cards coded as rank+suit text (e.g. 'JH'), with rank values A=6, K=5, Q=4, J=3, 9=2, 8=1 for comparing",
      "why": "Finding the trick winner needs a number to compare; these values keep the source order A > K > Q > J > 9 > 8."
    },
    {
      "what": "Strategy at the table",
      "why": "Players pass away dangerous high cards and the Quinola, then duck under the led card and discard point cards when void. A player with a very strong hand may instead aim to win all 6 tricks for a reversis, so opponents must watch for it and take one trick to stop it."
    }
  ],
  "simplifications": [
    {
      "what": "Passing 2 cards is two simultaneous polls of one card each",
      "why": "A question takes a single choice from a list. The second poll excludes the first card, and no card moves until both polls are done, so passing stays simultaneous and secret."
    },
    {
      "what": "The winner is computed as the highest of 0 - total, and a tie at the lowest total is a shared result",
      "why": "The engine ranks by highest value and shares ties at the top. This matches 'lowest total wins, a tie for lowest is a draw'."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: tricks_won, hand_points, total; table: hand_number.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Keep to the round structure: round 1 of a hand is deal plus pass, and rounds 2 to 7 are the 6 tricks.
- After 1 round, expect the deck lens at 0 and each player's hand lens at 6. That is chance-independent, because passing 2 and receiving 2 keeps 6.
- To check that all cards are played out, run 7 rounds (a full hand). Then expect every hand lens at 0 and hand_number 1. Also expect the trick results to fit the scoring: the sum of hand scores added to totals is 44, or it is the reversis pattern 0/15/15/15.
- Do not assert on internal bookkeeping such as stage, pick, offer or trick_number.
- Do not predict which cards are dealt or passed, since chance decides them.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Before any hand starts, nobody holds cards and hand_number is 0",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "default": "first",
    "rounds": 0,
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 0},
      "players": {
        "1": {"total": 0, "tricks_won": 0, "hand_points": 0},
        "2": {"total": 0, "tricks_won": 0, "hand_points": 0},
        "3": {"total": 0, "tricks_won": 0, "hand_points": 0},
        "4": {"total": 0, "tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Hand 1 deal empties the 24-card deck and each player holds 6 (chance-independent)",
    "rule": "R1",
    "players": 4,
    "seed": 2,
    "default": "first",
    "rounds": 1,
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Hand 1 passing: every seat chooses two cards and still holds 6 afterwards",
    "rule": "R2",
    "players": 4,
    "seed": 3,
    "default": "first",
    "rounds": 1,
    "expect": {
      "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Hand 1 pass to the left keeps every hand at 6 cards",
    "rule": "R3",
    "players": 4,
    "seed": 4,
    "default": "last",
    "rounds": 1,
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Hand 2 pass to the right keeps every hand at 6 cards",
    "rule": "R4",
    "players": 4,
    "seed": 5,
    "default": "first",
    "rounds": 1,
    "given": {"game": {"hand_number": 1}},
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "Hand 3 pass across keeps every hand at 6 cards",
    "rule": "R5",
    "players": 4,
    "seed": 6,
    "default": "first",
    "rounds": 1,
    "given": {"game": {"hand_number": 2}},
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 3}
    }
  },
  {
    "name": "After passing, every hand still holds 6 cards and the deck is empty",
    "rule": "R6",
    "players": 4,
    "seed": 7,
    "default": "last",
    "rounds": 1,
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}}
    }
  },
  {
    "name": "Hand 4 has no pass and every hand holds 6 cards",
    "rule": "R7",
    "players": 4,
    "seed": 8,
    "default": "first",
    "rounds": 1,
    "given": {"game": {"hand_number": 3}},
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 4}
    }
  },
  {
    "name": "Passing completes and play continues with full hands",
    "rule": "R8",
    "players": 4,
    "seed": 9,
    "default": "first",
    "rounds": 1,
    "expect": {
      "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "First trick of hand 1: each seat plays one card, leaving 5 each",
    "rule": "R9",
    "players": 4,
    "seed": 10,
    "default": "first",
    "rounds": 2,
    "expect": {
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Later tricks are led and played: after 3 tricks each seat holds 3 cards",
    "rule": "R10",
    "players": 4,
    "seed": 11,
    "default": "first",
    "rounds": 4,
    "expect": {
      "lens": {"players": {"1": {"hand": 3}, "2": {"hand": 3}, "3": {"hand": 3}, "4": {"hand": 3}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "In a trick every player plays exactly one card face up",
    "rule": "R11",
    "players": 4,
    "seed": 12,
    "default": "last",
    "rounds": 2,
    "expect": {
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}}
    }
  },
  {
    "name": "Leader may play any card: the trick completes with 5 cards left each",
    "rule": "R12",
    "players": 4,
    "seed": 13,
    "default": "last",
    "rounds": 2,
    "expect": {
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}}
    }
  },
  {
    "name": "Following suit when able: all 6 tricks are played out legally",
    "rule": "R13",
    "players": 4,
    "seed": 14,
    "default": "first",
    "rounds": 7,
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "A void player may play any card: the hand plays out to empty hands",
    "rule": "R14",
    "players": 4,
    "seed": 15,
    "default": "last",
    "rounds": 7,
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Each trick is decided and a full hand of 6 tricks is played",
    "rule": "R15",
    "players": 4,
    "seed": 16,
    "default": "first",
    "rounds": 7,
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Trick points and counts are reset to 0 after the hand is scored",
    "rule": "R16",
    "players": 4,
    "seed": 17,
    "default": "first",
    "rounds": 7,
    "expect": {
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      },
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}}
    }
  },
  {
    "name": "Normal scoring: the hand is scored and its counters reset (chance decides the scores)",
    "rule": "R17",
    "players": 4,
    "seed": 18,
    "default": "first",
    "rounds": 7,
    "expect": {
      "game": {"hand_number": 1},
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Reversis scoring: the hand is scored and its counters reset (chance decides whether a reversis happens)",
    "rule": "R18",
    "players": 4,
    "seed": 19,
    "default": "last",
    "rounds": 7,
    "expect": {
      "game": {"hand_number": 1},
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "End of hand resets hand points and trick counts to 0",
    "rule": "R19",
    "players": 4,
    "seed": 20,
    "default": "first",
    "rounds": 7,
    "expect": {
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Game ends after hand 4 is scored; seat 1, far ahead, wins whatever the deal",
    "rule": "R20",
    "players": 4,
    "seed": 21,
    "default": "first",
    "given": {
      "game": {"hand_number": 3},
      "players": {"1": {"total": 0}, "2": {"total": 100}, "3": {"total": 100}, "4": {"total": 100}}
    },
    "expect": {
      "winner": 1,
      "game": {"hand_number": 4},
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Lowest total wins: seat 3 at 0 against 100s cannot be caught in the last hand",
    "rule": "R21",
    "players": 4,
    "seed": 22,
    "default": "last",
    "given": {
      "game": {"hand_number": 3},
      "players": {"1": {"total": 100}, "2": {"total": 100}, "3": {"total": 0}, "4": {"total": 100}}
    },
    "expect": {
      "winner": 3,
      "game": {"hand_number": 4}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Before any hand starts, nobody holds cards and hand_number is 0",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "default": "first",
    "rounds": 0,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 0},
      "players": {
        "1": {"total": 0, "tricks_won": 0, "hand_points": 0},
        "2": {"total": 0, "tricks_won": 0, "hand_points": 0},
        "3": {"total": 0, "tricks_won": 0, "hand_points": 0},
        "4": {"total": 0, "tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Hand 1 deal empties the 24-card deck and each player holds 6 (chance-independent)",
    "rule": "R1",
    "players": 4,
    "seed": 2,
    "default": "first",
    "rounds": 1,
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Hand 1 passing: every seat chooses two cards and still holds 6 afterwards",
    "rule": "R2",
    "players": 4,
    "seed": 3,
    "default": "first",
    "rounds": 1,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Hand 1 pass to the left keeps every hand at 6 cards",
    "rule": "R3",
    "players": 4,
    "seed": 4,
    "default": "last",
    "rounds": 1,
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Hand 2 pass to the right keeps every hand at 6 cards",
    "rule": "R4",
    "players": 4,
    "seed": 5,
    "default": "first",
    "rounds": 1,
    "rules": [],
    "given": {"game": {"hand_number": 1}},
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "Hand 3 pass across keeps every hand at 6 cards",
    "rule": "R5",
    "players": 4,
    "seed": 6,
    "default": "first",
    "rounds": 1,
    "rules": [],
    "given": {"game": {"hand_number": 2}},
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 3}
    }
  },
  {
    "name": "After passing, every hand still holds 6 cards and the deck is empty",
    "rule": "R6",
    "players": 4,
    "seed": 7,
    "default": "last",
    "rounds": 1,
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}}
    }
  },
  {
    "name": "Hand 4 has no pass and every hand holds 6 cards",
    "rule": "R7",
    "players": 4,
    "seed": 8,
    "default": "first",
    "rounds": 1,
    "rules": [],
    "given": {"game": {"hand_number": 3}},
    "expect": {
      "lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 4}
    }
  },
  {
    "name": "Passing completes and play continues with full hands",
    "rule": "R8",
    "players": 4,
    "seed": 9,
    "default": "first",
    "rounds": 1,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "First trick of hand 1: each seat plays one card, leaving 5 each",
    "rule": "R9",
    "players": 4,
    "seed": 10,
    "default": "first",
    "rounds": 2,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Later tricks are led and played: after 3 tricks each seat holds 3 cards",
    "rule": "R10",
    "players": 4,
    "seed": 11,
    "default": "first",
    "rounds": 4,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 3}, "2": {"hand": 3}, "3": {"hand": 3}, "4": {"hand": 3}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "In a trick every player plays exactly one card face up",
    "rule": "R11",
    "players": 4,
    "seed": 12,
    "default": "last",
    "rounds": 2,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}}
    }
  },
  {
    "name": "Leader may play any card: the trick completes with 5 cards left each",
    "rule": "R12",
    "players": 4,
    "seed": 13,
    "default": "last",
    "rounds": 2,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}}
    }
  },
  {
    "name": "Following suit when able: all 6 tricks are played out legally",
    "rule": "R13",
    "players": 4,
    "seed": 14,
    "default": "first",
    "rounds": 7,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "A void player may play any card: the hand plays out to empty hands",
    "rule": "R14",
    "players": 4,
    "seed": 15,
    "default": "last",
    "rounds": 7,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Each trick is decided and a full hand of 6 tricks is played",
    "rule": "R15",
    "players": 4,
    "seed": 16,
    "default": "first",
    "rounds": 7,
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Trick points and counts are reset to 0 after the hand is scored",
    "rule": "R16",
    "players": 4,
    "seed": 17,
    "default": "first",
    "rounds": 7,
    "rules": [],
    "expect": {
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      },
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}}
    }
  },
  {
    "name": "Normal scoring: the hand is scored and its counters reset (chance decides the scores)",
    "rule": "R17",
    "players": 4,
    "seed": 18,
    "default": "first",
    "rounds": 7,
    "rules": [],
    "expect": {
      "game": {"hand_number": 1},
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Reversis scoring: the hand is scored and its counters reset (chance decides whether a reversis happens)",
    "rule": "R18",
    "players": 4,
    "seed": 19,
    "default": "last",
    "rounds": 7,
    "rules": [],
    "expect": {
      "game": {"hand_number": 1},
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "End of hand resets hand points and trick counts to 0",
    "rule": "R19",
    "players": 4,
    "seed": 20,
    "default": "first",
    "rounds": 7,
    "rules": [],
    "expect": {
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Game ends after hand 4 is scored; seat 1, far ahead, wins whatever the deal",
    "rule": "R20",
    "players": 4,
    "seed": 21,
    "default": "first",
    "rules": [],
    "given": {
      "game": {"hand_number": 3},
      "players": {"1": {"total": 0}, "2": {"total": 100}, "3": {"total": 100}, "4": {"total": 100}}
    },
    "expect": {
      "winner": 1,
      "game": {"hand_number": 4},
      "players": {
        "1": {"tricks_won": 0, "hand_points": 0},
        "2": {"tricks_won": 0, "hand_points": 0},
        "3": {"tricks_won": 0, "hand_points": 0},
        "4": {"tricks_won": 0, "hand_points": 0}
      }
    }
  },
  {
    "name": "Lowest total wins: seat 3 at 0 against 100s cannot be caught in the last hand",
    "rule": "R21",
    "players": 4,
    "seed": 22,
    "default": "last",
    "rules": [],
    "given": {
      "game": {"hand_number": 3},
      "players": {"1": {"total": 100}, "2": {"total": 100}, "3": {"total": 0}, "4": {"total": 100}}
    },
    "expect": {
      "winner": 3,
      "game": {"hand_number": 4}
    }
  }
]
```
````
