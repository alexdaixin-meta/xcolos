# 37 design

- time: 2026-10-28T06:51:52+00:00 (29.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 fe663c06a97a62ac, reply sha256 e57f2ffd5bd53ac5

## Sent

````
Original game: Put
Players in the original: 2 to 4

Original rules:
Use 52 cards ranking 3-2-A-K-Q-J-10-9-8-7-6-5-4, no trumps. Players ante to game score, 5 or 7 points to win match. Deal 3 cards each singly. Non-dealer leads. Any card may be played, no need to follow. Higher rank wins trick; equal ranks tie the trick and it belongs to none. Winner leads next, same leader after a tie. Winning 2 of 3 tricks scores 1 point, trick-and-tie scores none. Before a trick, holder may say "Put" to play for the whole game. If opponent folds, putter scores 1. If opponent says "I see it", the hand is played and winner of most tricks wins the whole game (5 or 7) not just 1. A player may also fold on seeing cards, conceding 1. Deal alternates.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
At the start of each hand, reset the text attributes `leader_call`, `responder_action` and `leader_reply` to the empty string '', not 'none'. Only write `leader_reply` when the leader actually replies, which happens only after the leader checked and the responder put. In every other hand leave it as ''. Likewise reset `putter` to 0 and `folded` to false each hand, and set them only when a Put or a Fold actually happens.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `Leader puts, responder is offered See and Fold and sees` failed: rule R7 is broken: When the leader puts, the responder chooses See or Fold.; game leader_reply: expected '', got 'none'
- scenario `Both check: an unput hand with no fold (point winner is chance, not asserted)` failed: rule R14 is broken: When both players checked, the player with more tricks scores 1 point, and equal tricks score nothing.; game leader_reply: expected '', got 'none'
- what the game did on `Leader puts, responder is offered See and Fold and sees`: moves played: r1 seat 1: 'Put'; r1 seat 2: 'See'; r1 seat 1: '1-2-3'; r1 seat 2: '1-2-3'. First attribute changes: table leader_call: '' -> 'none'; table responder_action: '' -> 'none'; table leader_reply: '' -> 'none'; table hand_number: 0 -> 1; table leader: 0 -> 1; table pick: 0 -> 8; seat 1 hand: [] -> [8]; table deck: [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13] -> [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13]; table pick: 8 -> 10; seat 2 hand: [] -> [10]; table deck: [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13] -> [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13]; table pick: 10 -> 7; seat 1 hand: [8] -> [8, 7]; table deck: [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13] -> [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13] .... Final: players {"seat 1": {"score": 0, "hand": [8, 7, 5], "up_card": 8, "order": [8, 7, 5], "tricks": 1, "order_choice": "1-2-3", "offer": ["See", "Fold"], "hand_points": 0}, "seat 2": {"score": 3, "hand": [10, 1, 13], "up_card": 10, "order": [10, 1, 13], "tricks": 2, "order_choice": "1-2-3", "offer": ["See", "Fold"], "hand_points": 3}}; table {"deck": [1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13], "pick": 13, "hand_number": 1, "leader": 1, "leader_call": "Put", "responder_action": "See", "leader_reply": "none", "putter": 1, "folded": false, "hands_shown": [[8, 7, 5], [10, 1, 13]], "orders_shown": [[8, 7, 5], [10, 1, 13]], "trick_results": [2, 1, 2], 
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "Setup: both scores start at 0 and no hand has been played",
  "rule": "R2",
  "players": 2,
  "seed": 1,
  "rounds": 0,
  "default": "decline",
  "rules": [],
  "expect": {
   "players": {
    "1": {
     "score": 0
    },
    "2": {
     "score": 0
    }
   },
   "game": {
    "hand_number": 0
   }
  },
  "rule_text": "The match is exactly 12 hands, and both players start at 0 points."
 },
 {
  "name": "Match lasts exactly 12 hands: every hand the leader puts and the responder folds, 6-6 draw",
  "rule": "R2",
  "players": 2,
  "seed": 2,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": "Put",
    "times": "all"
   },
   {
    "seat": 1,
    "options_include": "Fold",
    "times": "all"
   },
   {
    "seat": 2,
    "options_include": "Put",
    "times": "all"
   },
   {
    "seat": 2,
    "options_include": "Fold",
    "times": "all"
   }
  ],
  "expect": {
   "winner": [
    1,
    2
   ],
   "standings": {
    "1": 6,
    "2": 6
   },
   "players": {
    "1": {
     "score": 6
    },
    "2": {
     "score": 6
    }
   },
   "game": {
    "hand_number": 12
   }
  },
  "rule_text": "The match is exactly 12 hands, and both players start at 0 points."
 },
 {
  "name": "Hand 1 is odd so seat 1 leads",
  "rule": "R3",
  "players": 2,
  "seed": 3,
  "rounds": 1,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": "Put"
   },
   {
    "seat": 2,
    "options_include": "Fold"
   }
  ],
  "expect": {
   "game": {
    "hand_number": 1,
    "leader": 1,
    "leader_call": "Put",
    "responder_action": "Fold",
    "putter": 1,
    "folded": true
   },
   "players": {
    "1": {
     "score": 1
    },
    "2": {
     "score": 0
    }
   },
   "offered": [
    {
     "seat": 1,
     "option": "Check"
    },
    {
     "seat": 1,
     "option": "Put"
    }
   ],
   "not_offered": [
    {
     "seat": 2,
     "option": "Check"
    }
   ]
  },
  "rule_text": "When hand_number is odd, seat 1 leads; when it is even, seat 2 leads."
 },
 {
  "name": "Hand 2 is even so seat 2 leads",
  "rule": "R3",
  "players": 2,
  "seed": 4,
  "rounds": 1,
  "default": "decline",
  "given": {
   "game": {
    "hand_number": 1
   }
  },
  "rules": [
   {
    "seat": 2,
    "options_include": "Put"
   },
   {
    "seat": 1,
    "options_include": "Fold"
   }
  ],
  "expect": {
   "game": {
    "hand_number": 2,
    "leader": 2,
    "leader_call": "Put",
    "responder_action": "Fold",
    "putter": 2,
    "folded": true
   },
   "players": {
    "1": {
     "score": 0
    },
    "2": {
     "score": 1
    }
   },

Revise the variation to fix these. Keep what works. Review it again against the criteria.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "original_summary": "Put is an old English tavern card game, a forerunner of poker. Each player holds 3 cards with an odd ranking (3 high, then 2, A, K down to 4) and plays tricks without having to follow suit. A player may call 'Put' to raise the stake from 1 point to the whole game, and the opponent must then fold, conceding 1, or 'see' and play for everything.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Betting stops any single policy from dominating: always folding loses, and always putting is punished by an opponent who sees only with strong hands. But the original winner rule ends the match in one seen Put worth 5 or 7. Seat order also matters through who leads, because the leader can react to the tied trick."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "A match can be decided by a single seen Put on a 3-card deal, so luck dominates any short sample. Skill (bluffing, reading a Put, ordering cards) only shows over many hands."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Bluff frequencies, calling thresholds, and card ordering against an opponent's likely order give a strong player room to improve. A weak player still wins hands on good cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. A Put is a signal that may be a bluff, and the opponent must infer hand strength from it and from play."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick outcomes and points follow by comparing card ranks and adding."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Turn-based and text-only. However, the open-ended match length, the mid-trick Put timing, the 'fold on seeing cards' option and trick-by-trick leading make many sequential steps, and the 2–4 player version is loosely specified."
    },
    {
      "criterion": "__previous_build__",
      "verdict": "bad",
      "evidence": "The built variation wrote 'none' into leader_call, responder_action and leader_reply each hand. It also always wrote leader_reply, so tests expecting '' in hands with no leader reply failed (R7, R14)."
    }
  ],
  "problems": [
    "Match-ending stakes (one seen Put wins 5 or 7 points, i.e. the match) let a single lucky deal decide everything.",
    "Open-ended match length to 5 or 7 points is not a fixed number of rounds.",
    "A Put may be called before any trick, and leaders depend on trick results. This is a long chain of sequential steps that is costly to build.",
    "Fully hidden hands with no public information give little to reason from beyond the betting itself.",
    "Previous build bug: at the start of each hand, leader_call, responder_action and leader_reply were set to 'none' instead of the empty string ''.",
    "Previous build bug: leader_reply was written in every hand, even when the leader never replied.",
    "Previous build bug risk: putter and folded must be reset each hand and set only when a Put or Fold actually happens."
  ],
  "changes": [
    {
      "what": "Fixed match of 12 hands. A seen Put is worth 3 points, a fold concedes 1, and an unput hand is worth 1. The higher total after 12 hands wins; equal totals draw.",
      "why": "Spreads the result over many hands so betting skill accumulates, while keeping the Put as a raise of the stake.",
      "fixes": "Match-ending stakes (one seen Put wins 5 or 7 points, i.e. the match) let a single lucky deal decide everything."
    },
    {
      "what": "The leader alternates by hand number: odd hands seat 1, even hands seat 2.",
      "why": "Gives a fixed length and an even split of the leading seat (6 hands each).",
      "fixes": "Open-ended match length to 5 or 7 points is not a fixed number of rounds."
    },
    {
      "what": "Betting happens once, before play. It goes: leader Check/Put, then responder (See/Fold after a Put, Check/Put after a Check), then the leader's See/Fold only if the responder put. After betting, both players secretly choose an order for their 3 cards at the same moment, and the tricks are resolved from those orders.",
      "why": "Keeps the bluff-and-call heart of Put and the 'no need to follow' trick play in at most 4 choice steps. Choosing the order becomes a guessing duel.",
      "fixes": "A Put may be called before any trick, and leaders depend on trick results. This is a long chain of sequential steps that is costly to build."
    },
    {
      "what": "Each player's first dealt card is shown face up to both players.",
      "why": "Gives a partial public signal to reason about when reading a Put and choosing an order.",
      "fixes": "Fully hidden hands with no public information give little to reason from beyond the betting itself."
    },
    {
      "what": "At the start of every hand, leader_call, responder_action and leader_reply are set to the empty string '' (never 'none').",
      "why": "Matches what the rules and tests require.",
      "fixes": "Previous build bug: at the start of each hand, leader_call, responder_action and leader_reply were set to 'none' instead of the empty string ''."
    },
    {
      "what": "leader_reply is written only in the leader-reply step. That step runs only when the leader checked and the responder put. In every other hand it stays ''.",
      "why": "Matches what the rules and tests require.",
      "fixes": "Previous build bug: leader_reply was written in every hand, even when the leader never replied."
    },
    {
      "what": "At the start of every hand, putter is set to 0 and folded to false. putter is set to a seat only when that seat says Put. folded is set to true only when someone folds.",
      "why": "Matches what the rules and tests require.",
      "fixes": "Previous build bug risk: putter and folded must be reset each hand and set only when a Put or Fold actually happens."
    }
  ],
  "keeps": [
    "52-card deck with Put's ranking (3 highest, then 2, A, K, Q, J, 10, 9, 8, 7, 6, 5, 4 lowest), no trumps, suits irrelevant.",
    "3 cards each, three tricks, any card may be played (no following).",
    "Equal ranks tie a trick and it belongs to no one.",
    "Winning more tricks than the opponent scores 1 in an unput hand.",
    "The Put call raises the stake; the opponent must fold (conceding 1) or see and play for the bigger stake.",
    "Bluffing and calling as the core skill."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Put is a compact bluffing game that fits the engine once betting is done once per hand and trick play is done by simultaneous card orders. The previous build only needs its attribute resets corrected."
  },
  "variation": {
    "name": "Put: Twelve Hands",
    "summary": "Two players play 12 hands of 3-card Put. One card of each hand is face up. Each hand there is one round of Put/See/Fold betting, then both secretly order their cards to resolve three tricks. Unput hands score 1, a fold concedes 1, a seen Put scores 3, and the higher total after 12 hands wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. A deck of 52 cards: four copies each of the values 1 to 13. Value 13 is a Three (highest), 12 a Two, 11 an Ace, 10 a King, 9 a Queen, 8 a Jack, 7 a Ten, 6 a Nine, 5 an Eight, 4 a Seven, 3 a Six, 2 a Five, 1 a Four (lowest). A higher value beats a lower value; suits do not exist.\n\nSETUP. Both players start with score 0. hand_number starts at 0. The match is exactly 12 hands.\n\nEACH HAND, in this order:\n1. Start of hand.\n   - Add 1 to hand_number.\n   - Restore the deck to all 52 cards.\n   - Set the text attributes leader_call, responder_action and leader_reply to the empty string ''.\n   - Set putter to 0 and folded to false.\n   - Empty each player's hand, order, order_choice, tricks (0) and hand_points (0).\n   - The leader is seat 1 if hand_number is odd and seat 2 if it is even. The other seat is the responder.\n2. Deal. Deal 3 cards to each player, one at a time from the shuffled deck, alternating leader then responder. Each player's first dealt card is their up_card.\n3. Show. Both up_cards are announced to both players. Each player privately sees their own full hand.\n4. Leader call. The leader chooses Check or Put. Record the choice in leader_call. If Put, set putter to the leader.\n5. Responder action.\n   - If leader_call is Put, the responder chooses See or Fold.\n   - If leader_call is Check, the responder chooses Check or Put.\n   - Record the choice in responder_action. If the responder chose Put, set putter to the responder. If the responder chose Fold, set folded to true.\n6. Leader reply. Only when leader_call is Check and responder_action is Put: the leader chooses See or Fold. Record the choice in leader_reply, and if it is Fold, set folded to true. In every other case this step is skipped and leader_reply stays ''.\n7. Fold scoring. If folded is true, the putter scores 1 point (hand_points 1) and the hand ends; go to step 11.\n8. Card order. Both players at the same moment, without seeing the other's choice, choose one of the six orders for their 3 cards: 1-2-3, 1-3-2, 2-1-3, 2-3-1, 3-1-2 or 3-2-1. The numbers are positions in the hand as dealt; position 1 is the up_card.\n9. Tricks. The cards are revealed. For trick 1, 2 and 3, each player plays the card in that place of their order.\n   - The higher value wins the trick.\n   - Equal values tie the trick and it belongs to no one.\n   - Count each player's tricks won.\n10. Hand scoring.\n   - If putter is not 0 (a Put was seen), the player with more tricks scores 3 points.\n   - If putter is 0 (both checked), the player with more tricks scores 1 point.\n   - If both have the same number of tricks, no one scores.\n11. End check. If hand_number is 12, the match ends; otherwise start the next hand.",
    "objective": "After 12 hands, the player with the higher score wins. Equal scores are a draw.",
    "expected_effect": "Every hand, players must judge whether a Put is strength or bluff, using the visible up_cards and the opponent's betting history over the match. Then they guess the opponent's card order (lead high, sandbag, or match their visible card). No simple policy wins:\n- Always folding gives every Put away.\n- Always putting is beaten by seeing with strong hands, which wins 3.\n- Always seeing is beaten by value Puts.\n- Always checking lets the opponent put on strength and fold nothing.\nThe leading seat alternates 6–6, so neither seat has an edge. Spreading the stakes over 12 hands lets betting skill outweigh any single deal. Two players, no talk phase."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 4,
    "attributes": 20,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```

Why it was refused: review needs exactly one entry per criterion, in this order: non_degenerate, skill_sensitive, headroom, reasoning_dependent, verifiable, fits_platform
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "original_summary": "Put is an old English tavern card game and a forerunner of poker. Each player holds 3 cards with an odd ranking (3 high, then 2, A, K down to 4) and plays tricks without having to follow suit. A player may call 'Put' to raise the stake from 1 point to the whole game, and the opponent must then fold, conceding 1, or 'see' and play for everything.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Betting stops any single policy from dominating. Always folding loses, and always putting is punished by an opponent who sees only with strong hands. But the original winner rule ends the match in one seen Put worth 5 or 7. Seat order also matters through who leads, because the leader can react to the tied trick."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "A single seen Put on a 3-card deal can decide the match, so luck dominates any short sample. Skill (bluffing, reading a Put, ordering cards) only shows over many hands."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Bluff frequencies, calling thresholds and card ordering against an opponent's likely order give a strong player room to improve. A weak player still wins hands on good cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. A Put is a signal that may be a bluff, and the opponent must infer hand strength from it and from play."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick outcomes and points follow by comparing card ranks and adding."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. The open-ended match length, the mid-trick Put timing, the 'fold on seeing cards' option and trick-by-trick leading make many sequential steps. The 2–4 player version is loosely specified. The previous adaptation built, but it wrote 'none' into leader_call, responder_action and leader_reply at the start of each hand and always wrote leader_reply. Tests expecting '' in hands with no leader reply therefore failed (rules R7 and R14)."
    }
  ],
  "problems": [
    "Match-ending stakes (one seen Put wins 5 or 7 points, i.e. the match) let a single lucky deal decide everything.",
    "Open-ended match length to 5 or 7 points is not a fixed number of rounds.",
    "A Put may be called before any trick, and leaders depend on trick results: a long chain of sequential steps that is costly to build.",
    "Fully hidden hands with no public information give little to reason from beyond the betting itself.",
    "Previous build bug: at the start of each hand, leader_call, responder_action and leader_reply were set to 'none' instead of the empty string ''.",
    "Previous build bug: leader_reply was written in every hand, even when the leader never replied.",
    "Previous build bug risk: putter and folded must be reset each hand and set only when a Put or Fold actually happens."
  ],
  "changes": [
    {
      "what": "The match is a fixed 12 hands. A seen Put is worth 3 points, a fold concedes 1, and an unput hand is worth 1. The higher total after 12 hands wins; equal totals draw.",
      "why": "Spreads the result over many hands so betting skill accumulates, while keeping the Put as a raise of the stake.",
      "fixes": "Match-ending stakes (one seen Put wins 5 or 7 points, i.e. the match) let a single lucky deal decide everything."
    },
    {
      "what": "The leader alternates by hand number: seat 1 leads odd hands and seat 2 leads even hands.",
      "why": "Gives a fixed length and an even 6–6 split of the leading seat.",
      "fixes": "Open-ended match length to 5 or 7 points is not a fixed number of rounds."
    },
    {
      "what": "Betting happens once, before play. The leader checks or puts. The responder then sees or folds after a Put, or checks or puts after a Check. The leader replies with See or Fold only if the responder put. After betting, both players secretly choose an order for their 3 cards at the same moment, and the tricks are resolved from those orders.",
      "why": "Keeps the bluff-and-call heart of Put and the 'no need to follow' trick play in at most 4 choice steps. Choosing the order becomes a guessing duel.",
      "fixes": "A Put may be called before any trick, and leaders depend on trick results: a long chain of sequential steps that is costly to build."
    },
    {
      "what": "Each player's first dealt card is shown face up to both players.",
      "why": "Gives a partial public signal to reason about when reading a Put and choosing an order.",
      "fixes": "Fully hidden hands with no public information give little to reason from beyond the betting itself."
    },
    {
      "what": "At the start of every hand, leader_call, responder_action and leader_reply are set to the empty string '' (never 'none').",
      "why": "Matches what the rules and tests require.",
      "fixes": "Previous build bug: at the start of each hand, leader_call, responder_action and leader_reply were set to 'none' instead of the empty string ''."
    },
    {
      "what": "leader_reply is written only in the leader-reply step. That step runs only when the leader checked and the responder put; in every other hand leader_reply stays ''.",
      "why": "Matches what the rules and tests require.",
      "fixes": "Previous build bug: leader_reply was written in every hand, even when the leader never replied."
    },
    {
      "what": "At the start of every hand, putter is set to 0 and folded to false. putter is set to a seat only when that seat says Put, and folded is set to true only when someone folds.",
      "why": "Matches what the rules and tests require.",
      "fixes": "Previous build bug risk: putter and folded must be reset each hand and set only when a Put or Fold actually happens."
    }
  ],
  "keeps": [
    "A 52-card deck with Put's ranking (3 highest, then 2, A, K, Q, J, 10, 9, 8, 7, 6, 5, 4 lowest), no trumps, suits irrelevant.",
    "3 cards each, three tricks, and any card may be played (no following).",
    "Equal ranks tie a trick and it belongs to no one.",
    "Winning more tricks than the opponent scores 1 in an unput hand.",
    "The Put call raises the stake; the opponent must fold (conceding 1) or see and play for the bigger stake.",
    "Bluffing and calling as the core skill."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Put is a compact bluffing game that fits the engine once betting is done once per hand and trick play is done by simultaneous card orders. The previous build only needs its attribute resets corrected."
  },
  "variation": {
    "name": "Put: Twelve Hands",
    "summary": "Two players play 12 hands of 3-card Put, with one card of each hand face up. Each hand has one round of Put/See/Fold betting, then both players secretly order their cards to resolve three tricks. Unput hands score 1, a fold concedes 1, a seen Put scores 3, and the higher total after 12 hands wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. A deck of 52 cards: four copies each of the values 1 to 13. Value 13 is a Three (highest), 12 a Two, 11 an Ace, 10 a King, 9 a Queen, 8 a Jack, 7 a Ten, 6 a Nine, 5 an Eight, 4 a Seven, 3 a Six, 2 a Five, 1 a Four (lowest). A higher value beats a lower value; suits do not exist.\n\nSETUP. Both players start with score 0. hand_number starts at 0. The match is exactly 12 hands.\n\nEACH HAND, in this order:\n1. Start of hand.\n   - Add 1 to hand_number.\n   - Restore the deck to all 52 cards.\n   - Set the text attributes leader_call, responder_action and leader_reply to the empty string ''.\n   - Set putter to 0 and folded to false.\n   - Empty each player's hand, order and order_choice, and set tricks to 0 and hand_points to 0.\n   - The leader is seat 1 if hand_number is odd and seat 2 if it is even. The other seat is the responder.\n2. Deal. Deal 3 cards to each player, one at a time from the shuffled deck, alternating leader then responder. Each player's first dealt card is their up_card.\n3. Show. Both up_cards are announced to both players. Each player privately sees their own full hand.\n4. Leader call. The leader chooses Check or Put. Record the choice in leader_call. If Put, set putter to the leader.\n5. Responder action.\n   - If leader_call is Put, the responder chooses See or Fold.\n   - If leader_call is Check, the responder chooses Check or Put.\n   - Record the choice in responder_action. If the responder chose Put, set putter to the responder. If the responder chose Fold, set folded to true.\n6. Leader reply. This step happens only when leader_call is Check and responder_action is Put. The leader chooses See or Fold. Record the choice in leader_reply, and if it is Fold, set folded to true. In every other case this step is skipped and leader_reply stays ''.\n7. Fold scoring. If folded is true, the putter scores 1 point (hand_points 1) and the hand ends; go to step 11.\n8. Card order. Both players choose at the same moment, without seeing the other's choice, one of the six orders for their 3 cards: 1-2-3, 1-3-2, 2-1-3, 2-3-1, 3-1-2 or 3-2-1. The numbers are positions in the hand as dealt; position 1 is the up_card.\n9. Tricks. The cards are revealed. For tricks 1, 2 and 3, each player plays the card in that place of their order.\n   - The higher value wins the trick.\n   - Equal values tie the trick, and it belongs to no one.\n   - Count each player's tricks won.\n10. Hand scoring.\n   - If putter is not 0 (a Put was seen), the player with more tricks scores 3 points.\n   - If putter is 0 (both checked), the player with more tricks scores 1 point.\n   - If both have the same number of tricks, no one scores.\n11. End check. If hand_number is 12, the match ends; otherwise start the next hand.",
    "objective": "After 12 hands, the player with the higher score wins. Equal scores are a draw.",
    "expected_effect": "Every hand, players must judge whether a Put is strength or bluff, using the visible up_cards and the opponent's betting history over the match. They then guess the opponent's card order: lead high, sandbag, or match their visible card. No simple policy wins:\n- Always folding gives every Put away.\n- Always putting is beaten by seeing with strong hands, which wins 3.\n- Always seeing is beaten by value Puts.\n- Always checking lets the opponent put on strength and never fold.\nThe leading seat alternates 6–6, so neither seat has an edge. Spreading the stakes over 12 hands lets betting skill outweigh any single deal. The game has two players and no talk phase."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 4,
    "attributes": 20,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
