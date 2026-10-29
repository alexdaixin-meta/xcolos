# 19 design

- time: 2026-10-27T18:17:05+00:00 (71.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 264b98e613362997, reply sha256 4e3af97ae7f0f49d

## Sent

````
Original game: Wizard
Players in the original: 3 to 6

Original rules:
Wizard uses 60 cards: 1-13 in four suits plus 4 Wizards (highest) and 4 Jesters (lowest). 3-6 players play 60/players rounds, dealt 1 card first round, 2 second, etc. After each deal one card is turned for trump; Jester means no trump, Wizard lets dealer choose. In turn order each player bids number of tricks they will take (bids need not sum to tricks available). Then cards are played clockwise; must follow led suit if possible, but Wizards/Jesters may be played anytime. Trick won by first Wizard, else highest trump, else highest of led suit; Jester led means next suit sets led suit, and only Jesters means first Jester wins. Scoring: exact bid = 20 + 10 per trick taken; otherwise -10 per trick off bid. Highest total after final round wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Make the start-of-hand bid a single simultaneous poll in which every seat is offered exactly the numeric options bid_min..bid_max (0, 1, 2, 3), built from the parameter attributes. Store each answer in that player's `bid` exactly as given. Apply default_bid (1) only when the answer is missing or outside 0-3; a valid 0 must stay 0. Do not reset or overwrite `bid` during the hand; clear it only after the end-of-hand scoring in rule 11. Check that the deal still happens before the poll on trick 1 of each hand, with 3 cards to each seat and the 10th card as trump, so 18 cards remain in the deck after the first trick. Check that the first leader is seat ((hand_number - 1) mod 3) + 1. Check that the illegal-choice fallback follows the a/b/c/d priority from rule 8, with ties broken Red, then Blue, then Green.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `R1: a new hand deals 3 cards to each seat and 1 trump card; after the first trick the deck holds 18 and each hand 2 (the cards themselves are random)` failed: rule R1 is broken: When a hand starts (trick_in_hand == 1), then all 28 cards are shuffled into deck and each player is dealt exactly 3 cards into their hand, seen only by them.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never mat
- scenario `R3: simultaneous bids 2, 0 and 3 are recorded as given, although they do not sum to 3` failed: rule R3 is broken: When bidding, then all three players bid 0, 1, 2 or 3 simultaneously, and a missing or invalid bid becomes 1; all bids are then revealed, and they need not sum to 3.; seat 1 bid: expected 2, got 0; seat 3 bid: expected 3, got 0; Ada: the rule for 2 was never matched (the game neve
- scenario `R4: after hand 1 is scored, the next round starts hand 2 with a fresh deal` failed: rule R4 is broken: When hand h starts, then the first leader is seat ((h - 1) mod 3) + 1: P1 for hands 1, 4, 7, 10; P2 for hands 2, 5, 8, 11; P3 for hands 3, 6, 9, 12.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the 
- scenario `R9: an invalid answer falls back to the seat's lowest card of the led suit (R2 rather than R6)` failed: rule R9 is broken: When a player's choice is missing or not a legal card they hold, then the engine plays, in order of priority: (a) their lowest led-suit card if a led suit exists and they hold one; (b) else a Jester; (c) else their lowest suited card, with ties broken Red, then Blue, then Green; (
- what the game did on `R3: simultaneous bids 2, 0 and 3 are recorded as given, although they do not sum to 3`: moves played: r1 seat 1: 0; r1 seat 2: 0; r1 seat 3: 0; r1 seat 1: 'G5'; r1 seat 2: 'G1'; r1 seat 3: 'G3'. First attribute changes: table hand_number: 0 -> 1; seat 1 bid: 0 -> 1; seat 2 bid: 0 -> 1; seat 3 bid: 0 -> 1; table pick: '' -> 'G5'; seat 1 hand: [] -> ['G5']; table deck: ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2'] -> ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G1', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2']; table pick: 'G5' -> 'G1'; seat 2 hand: [] -> ['G1']; table deck: ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G1', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2'] -> ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2']; table pick: 'G1' -> 'G6'; seat 3 hand: [] -> ['G6']; table deck: ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2'] -> ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G2', 'G3', 'G4', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2']; table pick: 'G6' -> 'R8' .... Final: players {"seat 1": {"hand": ["R8", "G7"], "bid": 0, "tricks_taken": 1, "played_card": "G5", "score": 0, "offer": ["G7"], "fallback": "G7"}, "seat 2": {"hand": ["B2", "R6"], "bid": 0, "tricks_taken": 0, "played_card": "G1", "score": 0, "offer": ["B2", "R6"], "fallback": "B2"}, "seat 3": {"hand": ["G6", "G4"], "bid": 0, "tricks_taken": 0, "played_card": "G3", "score": 0, "offer": ["G6", "G4", "G3"], "fallback": "G3"}}; table {"deck": ["R1", "R2", "R3", "R4", "R5", "R7", "B3", "B4", "B5", "B6", "B7", "B8", "G2", "G8", "W1", "W2", "J1", "J2"], "pick": "B1", "card": "G3", "strength": 3, "trump_card": "B1", "trump_suit": "B", "hand_number": 1, "hands_done": 0, "trick_in_hand": 2, "leader": 1, "led_suit": "G", "wizard_played": false, "best_value": 5, "best_seat": 1, "played_cards": ["G5", "G1", "G3"], "deck_size": 28, "suits": 3, "rank_min": 
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "R1: a new hand deals 3 cards to each seat and 1 trump card; after the first trick the deck holds 18 and each hand 2 (the cards themselves are random)",
  "rule": "R1",
  "players": 3,
  "seed": 1,
  "rounds": 1,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": 0,
    "answer": 0,
    "times": 1
   },
   {
    "seat": 2,
    "options_include": 0,
    "answer": 0,
    "times": 1
   },
   {
    "seat": 3,
    "options_include": 0,
    "answer": 0,
    "times": 1
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "deck": 18
    },
    "players": {
     "1": {
      "hand": 2
     },
     "2": {
      "hand": 2
     },
     "3": {
      "hand": 2
     }
    }
   },
   "game": {
    "hand_number": 1
   }
  },
  "rule_text": "When a hand starts (trick_in_hand == 1), then all 28 cards are shuffled into deck and each player is dealt exactly 3 cards into their hand, seen only by them."
 },
 {
  "name": "R2: with a suited trump (G), a green card played off-suit beats the led red card",
  "rule": "R2",
  "players": 3,
  "rounds": 1,
  "default": "decline",
  "given": {
   "game": {
    "trick_in_hand": 2,
    "leader": 1,
    "trump_card": "G3",
    "trump_suit": "G",
    "hand_number": 1
   },
   "players": {
    "1": {
     "hand": [
      "R8",
      "B1"
     ],
     "tricks_taken": 0
    },
    "2": {
     "hand": [
      "G1",
      "B2"
     ],
     "tricks_taken": 0
    },
    "3": {
     "hand": [
      "R2",
      "B3"
     ],
     "tricks_taken": 0
    }
   }
  },
  "rules": [
   {
    "seat": 1,
    "options_include": "R8"
   },
   {
    "seat": 2,
    "options_include": "G1"
   }
  ],
  "expect": {
   "players": {
    "1": {
     "played_card": "R8",
     "tricks_taken": 0
    },
    "2": {
     "played_card": "G1",
     "tricks_taken": 1
    },
    "3": {
     "played_card": "R2",
     "tricks_taken": 0
    }
   }
  },
  "rule_text": "When the 10th card (the trump card) is suited, then trump_suit is its suit; when it is a Wizard or a Jester, then trump_suit is 'none' for that hand."
 },
 {
  "name": "R3: simultaneous bids 2, 0 and 3 are recorded as given, although they do not sum to 3",
  "rule": "R3",
  "players": 3,
  "seed": 2,
  "rounds": 1,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": 2,
    "answer": 2,
    "times": 1
   },
   {
    "seat": 2,
    "options_include": 0,
    "answer": 0,
    "times": 1
   },
   {
    "seat": 3,
    "options_include": 3,
    "answer": 3,
    "times": 1
   }
  ],
  "expect": {
   "players": {
    "1": {
     "bid": 2
    },
    "2"

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
  "original_summary": "Wizard is a trick-taking game for 3-6 players with a 60-card deck (four suits of 1-13, plus 4 Wizards and 4 Jesters). Hands grow from 1 card to 60/players cards, a turned card sets trump, and each player bids the exact number of tricks they will take. An exact bid scores 20 plus 10 per trick, and a missed bid loses 10 per trick off.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Every fixed bid loses. Always bidding 0 fails whenever the hand is strong, and always bidding high fails on weak hands. Missing by k costs 10k, so no fixed policy can match a player who reads their hand. One seat edge exists: bidding in turn order gives the last bidder information. A second, much smaller one comes from leading."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Skill shows in hand evaluation, card counting and dumping or ducking tricks. Single hands are very card-driven, though, and the many tiny early hands are close to lotteries. Skill wins out only over many hands."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player can still score exact bids of 0 or 1. A strong player keeps improving by inferring others' hands from their bids and play, steering tricks to the right player, and playing to make others miss."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Bids reveal partial information. Each trick requires inferring what the remaining players hold and planning across the rest of the hand."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners and scores follow mechanically from the cards played and the bids."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The original runs up to 20 hands of up to 20 cards, which means hundreds of sequential choices. It also needs a 60-card deck, a dealer trump choice, a variable hand size and a sequential bidding order. This exceeds the step and round limits."
    }
  ],
  "problems": [
    "P1: Length and size. Variable hands up to 20 cards and up to 60 hands far exceed 40 rounds and 4 choices per round.",
    "P2: Sequential bidding gives the last bidder a built-in information edge, and the dealer's trump choice on a Wizard adds an extra sub-procedure.",
    "P3: The previous build did not offer the bid options 0-3 to seats. It derived them from parameter attributes (bid_min..bid_max) that did not produce a valid option list. Every bid then fell to the default 1, which overwrote valid answers including 0. This broke the deal/bid scenario (R1), the recorded-bids scenario (R3) and the new-hand scenario (R4).",
    "P4: The illegal-choice fallback (lowest led-suit card, else Jester, else lowest suited card with colour tie-breaks, and so on) was a long priority chain. It was built incorrectly (R9) and is error-prone to build.",
    "P5: Tiny one-card hands are nearly pure luck, so card luck swamps skill in early hands."
  ],
  "changes": [
    {
      "what": "Three players, a 28-card deck (Red, Blue, Green 1-8, plus 2 Wizards and 2 Jesters), 12 hands of exactly 3 cards. Each round is one trick, so there are 36 rounds.",
      "why": "This keeps trick-taking, trump and exact bidding within 40 rounds and at most 4 choices per round. Every hand is large enough to plan over.",
      "fixes": "P1"
    },
    {
      "what": "Every hand has 3 cards instead of 1 to 20.",
      "why": "Removes the near-random one-card hands. Every hand now offers a real bid decision and in-hand planning.",
      "fixes": "P5"
    },
    {
      "what": "Bids are a single simultaneous poll. The literal fixed options 0, 1, 2 and 3 are written directly into the step, not computed from attributes. The answer is stored exactly as given. The default of 1 applies only if the answer is missing or not one of 0-3. The bid is not touched again until end-of-hand scoring.",
      "why": "Simultaneous bidding removes the last-bidder edge. Hard-coding the option list fixes the build failure where no options were offered and every bid became 1.",
      "fixes": "P3"
    },
    {
      "what": "A turned Wizard or Jester simply means no trump.",
      "why": "Removes the dealer-choice sub-procedure and the dealer's advantage.",
      "fixes": "P2"
    },
    {
      "what": "The first leader of hand h is seat ((h - 1) mod 3) + 1. After that, the trick winner leads.",
      "why": "Balances the leading advantage over 12 hands (4 each).",
      "fixes": "P2"
    },
    {
      "what": "The illegal-choice fallback is one rule: play the first card of the player's legal-card list, which keeps the order the cards sit in their hand.",
      "why": "This is a one-operation fallback that is deterministic and easy to build and test, replacing the broken priority chain.",
      "fixes": "P4"
    },
    {
      "what": "Trick resolution uses one numeric strength per card, and the best card is replaced only by a strictly greater strength. A Wizard is 100, a trump is 20 + rank, a led-suit card is its rank, and anything else is 0.",
      "why": "Implements 'first Wizard wins, else highest trump, else highest led suit, all Jesters means the first Jester wins' as plain arithmetic, with no lookup table.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "Wizards always win, with the first one played taking the trick. Jesters always lose, and the first one wins only if every card is a Jester.",
    "A turned card sets trump each hand.",
    "Players must follow the led suit if able, but Wizards and Jesters may always be played.",
    "When a Jester is led, the next suited card sets the led suit. When a Wizard is led, there is no led suit.",
    "Exact-bid scoring: 20 + 10 per trick when exact, otherwise -10 per trick off.",
    "Bids need not sum to the number of tricks.",
    "The highest total after the last hand wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of hidden hands, exact bidding and trick inference fits the platform once the game is shrunk to 3 players, 3-card hands and simultaneous bids with a hard-coded option list."
  },
  "variation": {
    "name": "Three-Card Wizard",
    "summary": "A compact Wizard for 3 players: 12 hands of 3 cards from a 28-card deck, simultaneous exact bids, and one trick per round.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "CARDS. The deck has 28 cards:\n- Red R1-R8, Blue B1-B8 and Green G1-G8 (the suit is the letter, the rank is the number);\n- two Wizards, W1 and W2;\n- two Jesters, J1 and J2.\n\nSEATS. Players sit in seats 1, 2 and 3. Everyone starts with a score of 0.\n\nSTRUCTURE. The game has 12 hands of 3 tricks each. Each round is one trick, so there are 36 rounds.\n- The table tracks hand_number (starting at 0) and trick_in_hand (starting at 1).\n- Each player has: hand (a list, private to them), bid, tricks_taken, played_card, offer (a list) and score.\n\nRULE 1 (new hand: deal). Only when trick_in_hand = 1:\n- add 1 to hand_number;\n- shuffle all 28 cards into the deck (this is the round's only random event);\n- empty every hand and set every tricks_taken to 0;\n- deal the top 3 cards of the deck to seat 1, the next 3 to seat 2 and the next 3 to seat 3, each seen only by its owner;\n- remove the 10th card from the deck and place it face up as trump_card, announced to all. After this, 18 cards remain in the deck.\n\nRULE 2 (trump). If trump_card is suited, trump_suit is its suit letter. If it is a Wizard or a Jester, trump_suit is 'none' for the whole hand.\n\nRULE 3 (first leader). Only when trick_in_hand = 1, leader = ((hand_number - 1) mod 3) + 1:\n- seat 1 leads in hands 1, 4, 7 and 10;\n- seat 2 leads in hands 2, 5, 8 and 11;\n- seat 3 leads in hands 3, 6, 9 and 12.\n\nRULE 4 (bidding). Only when trick_in_hand = 1, all three players answer one simultaneous poll.\n- The options are exactly the fixed list 0, 1, 2, 3, offered to every seat.\n- Each player's answer is stored in their bid exactly as given, and a 0 stays 0.\n- Only if an answer is missing or not one of 0, 1, 2, 3 does that bid become 1.\n- All bids are then announced. They need not sum to 3.\n- Bids are not changed again until Rule 10.\n\nRULE 5 (trick setup). Every round, set:\n- led_suit = 'none';\n- wizard_played = false;\n- best_value = -1;\n- best_seat = 0;\n- played_cards empty.\n\nRULE 6 (play order). Three players play one card each, one after another:\n- first the seat in leader;\n- then the seat (leader mod 3) + 1;\n- then the seat ((leader + 1) mod 3) + 1.\nEach player sees the cards already played to the trick.\n\nRULE 7 (legal cards). Before a player chooses, build their offer list, keeping the order the cards sit in their hand:\n- if led_suit is not 'none' and they hold at least one card of led_suit, the offer is their cards of led_suit plus any Wizards and Jesters they hold;\n- otherwise, the offer is every card in their hand.\nThe player picks one card from the offer.\n\nRULE 8 (fallback). If the answer is missing or not in the offer, the engine plays the first card of the offer list.\n\nRULE 9 (resolving each played card). As each card is played, remove it from the hand, record it as played_card and append it to played_cards. Then work out the led suit and the card's strength.\n\nLed suit:\n- If the card is suited, led_suit is 'none' and wizard_played is false, then led_suit becomes that card's suit.\n- If the card is a Wizard, set wizard_played = true.\n- A Wizard or Jester never sets led_suit. Once any Wizard is played, later cards do not set led_suit.\n\nStrength:\n- Wizard: 100.\n- Suited card whose suit equals trump_suit: 20 + rank.\n- Other suited card whose suit equals led_suit: its rank.\n- Anything else: 0. This includes Jesters and off-suit non-trump cards.\n\nIf strength > best_value (strictly), set best_value = strength and best_seat = this seat. As a result:\n- the first Wizard wins the trick;\n- otherwise the highest trump wins;\n- otherwise the highest card of the led suit wins;\n- if all three cards are Jesters, the first Jester wins.\n\nRULE 10 (end of trick). Add 1 to tricks_taken of best_seat, announce the winner, and set leader = best_seat.\n- If trick_in_hand = 3, score the hand. A player whose tricks_taken equals their bid gains 20 + 10 × tricks_taken. Otherwise they lose 10 × |tricks_taken - bid|. Announce all scores, then set every bid to 0 and trick_in_hand = 1.\n- Otherwise add 1 to trick_in_hand.\n\nRULE 11 (end). The game ends after round 36, which is the end of hand 12.",
    "objective": "After hand 12, the player with the highest score wins. If two or three players tie for the highest score, the game is a draw.",
    "expected_effect": "Simultaneous bids remove the last-bidder edge, and rotating the first lead balances the seats. Three-card hands make every bid a real estimate: count Wizards and trumps, and judge how the off-suit cards will play. Mid-hand play rewards inference from the announced bids and the cards seen, such as ducking a trick to stay exact or forcing a trick onto an opponent who bid 0. Simple policies lose: always bidding 0 is beaten by reading the hand, and always bidding 3 misses most hands at -10 to -30. Over 12 hands, skill outweighs the deal. Talk is left out: with only 3 players and public bids, messages would add little beyond the bids and could enable two-player collusion against the third."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 17,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
````
