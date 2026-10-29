# 21 design

- time: 2026-10-27T17:56:50+00:00 (67.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 632b60470310d703, reply sha256 e93bffb00b98639a

## Sent

````
Original game: Cuttle
Players in the original: 2 to 2

Original rules:
Two players share a standard 52-card deck. Deal 6 cards to dealer and 5 to opponent, rest is draw pile; scrap pile is face-up discard showing top only. On your turn do exactly one: draw one card, or play one card from hand. Number cards A,2-10 can be point cards worth their value (A=1) placed on your side; first to 21+ points wins, but kings reduce requirement to 14/10/7/5 for 1-4 kings you control. A point card can also scuttle: play a higher rank, or equal rank with higher suit C<D<H<S, to discard both cards. Cards  A,2-7,9 can be one-offs discarded after use for effects like wipe points, destroy permanents, recover from scrap, force opponent discard 2, draw 2, play top of deck immediately, bounce a permanent. 8,J,Q,K are permanents staying on table: 8 forces opponent to reveal hand, J stacked on a point card steals it, Q protects your other points/permanents from single-target effects, K lowers win threshold. 2 can be played on opponent's turn to counter a one-off. If draw pile empty you may pass; three passes ends game with no winner.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
1) The `won` flag must only be set by the start-of-turn check. Give that step a `when` condition `points >= threshold` for the acting player. Do not set `won` anywhere else: not at turn 41, not in a final step, not for the player who would have acted next. After turn 40, end the game with `won` left at 0 for both players, so `rank_by` (`won*1000 - shortfall`) decides by the smaller shortfall and equal shortfalls tie. Make sure the turn counter reaching `max_turns` + 1 stops play before any further win check or action runs. 2) The fallback for an illegal or unparseable reply must be PASS, not DRAW. Map a missing or unrecognised action to 'pass' so nothing changes: no draw, no hand or pile changes. Check that `draw` is not the default option and that no draw step runs unconditionally. 3) While there, recompute `threshold` from `is_first` and `king_count` using the parameter attributes, and recompute `shortfall` as max(threshold - points, `shortfall_min`), after every action. Also check that setup sets `is_first` consistently: the trace flips seat 2 to True, but the final state shows seat 1 as First.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `The game stops after turn 40 and the smaller shortfall wins` failed: rule R3 is broken: When the players alternate single turns, the game has at most 40 turns, numbered 1 to 40.; seat 2 standing: expected -30, got 970; seat 2 won: expected 0, got 1
- scenario `An unparseable reply counts as pass and nothing changes` failed: rule R15 is broken: When a reply is illegal or unparseable, then it counts as PASS and nothing changes.; seat 1 hand: expected 1 items, got 2; game draw_pile: expected 36 items, got 35
- scenario `After turn 40 the smaller shortfall wins` failed: rule R16 is broken: When turn 40 ends with no winner, then the player with the smaller max(threshold - points, 0) wins, and equal shortfalls are a draw.; seat 2 standing: expected -5, got 995; seat 2 won: expected 0, got 1
- scenario `After turn 40 equal shortfalls share the result` failed: rule R16 is broken: When turn 40 ends with no winner, then the player with the smaller max(threshold - points, 0) wins, and equal shortfalls are a draw.; seat 1 standing: expected -5, got 995; seat 2 standing: expected -5, got 995
- what the game did on `The game stops after turn 40 and the smaller shortfall wins`: moves played: r1 seat 1: 'draw'. First attribute changes: table draw_pile: [] -> ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'K', 'K', 'K', 'K']; table positions: [] -> ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40']; table slots: [] -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]; table acting_seat: 1 -> 2; seat 2 is_first: False -> True; table pick: '' -> '3'; seat 1 hand: [] -> ['3']; table draw_pile: ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'K', 'K', 'K', 'K'] -> ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'K', 'K', 'K', 'K']; table pick: '3' -> '6'; seat 2 hand: [] -> ['6']; table draw_pile: ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'K', 'K', 'K', 'K'] -> ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'K', 'K', 'K', 'K']; table pick: '6' -> '9'; seat 1 hand: ['3'] -> ['3', '9']; table draw_pile: ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'K', 'K', 'K', 'K'] -> ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'K', 'K', 'K', 'K'] .... Final: players {"seat 1": {"is_first": true, "hand": ["1", "4"], "hand_count": 2, "point_pile": [], "point_pile_view": [], "points": 0, "king_count": 0, "threshold": 32, "shortfall": 32, "won": 0}, "seat 2": {"is_first": false, "hand": ["6", "J", "3", "1", "10", "J"], "hand_count": 6, "point_pile": [], "point_pile_view": [], "points": 0, "king_count": 0, "threshold": 30, "shortfall": 30, "won": 1}}; table {"draw_pile": ["1", "2", "2", "2", "2", "3", "3", "4", "4", "4", "5", "5", "5", "5", "6", "6", "6", "7", "7", "7", "7", "8", "8", "8", "8", "9", "9", "9", "10", "10", "J", "J", "K", "K", "K"], "scrap": [], "turn": 41, "acting_seat": 2, "action": "draw", "chosen_card": "", "target_index": 0, "draw_count": 35, "opp_seat": 2, "act_hand": ["1"], "opp_view": [], "opp_pile": [], "action_opts": ["pass", "draw", "points"], "
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "Setup deals 6 cards to each seat and leaves 36 in the draw pile",
  "rule": "R1",
  "players": 2,
  "seed": 1,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": "draw"
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "draw_pile": 36,
     "scrap": 0
    },
    "players": {
     "1": {
      "hand": 6,
      "point_pile": 0,
      "point_pile_view": 0
     },
     "2": {
      "hand": 6,
      "point_pile": 0,
      "point_pile_view": 0
     }
    }
   },
   "players": {
    "1": {
     "points": 0,
     "king_count": 0,
     "won": 0
    },
    "2": {
     "points": 0,
     "king_count": 0,
     "won": 0
    }
   },
   "game": {
    "turn": 1
   }
  },
  "rule_text": "When setup is done, each player has 6 cards in hand, draw_pile has 36 cards, and the deck had 40 point cards (ranks 1-10, four each), 4 Jacks and 4 Kings."
 },
 {
  "name": "The First player acts on turn 1",
  "rule": "R2",
  "players": 2,
  "seed": 1,
  "rounds": 1,
  "given": {
   "players": {
    "1": {
     "is_first": true,
     "hand": [
      "5"
     ],
     "hand_count": 1
    },
    "2": {
     "is_first": false
    }
   },
   "game": {
    "acting_seat": 1,
    "turn": 1
   }
  },
  "rules": [
   {
    "seat": 1,
    "options_include": "points"
   }
  ],
  "expect": {
   "players": {
    "1": {
     "points": 5,
     "point_pile_view": [
      "Mid"
     ],
     "threshold": 32,
     "shortfall": 27
    },
    "2": {
     "points": 0,
     "threshold": 30,
     "shortfall": 30
    }
   },
   "game": {
    "turn": 2
   }
  },
  "rule_text": "When the game starts, a random seat is First, and the First player takes turn 1."
 },
 {
  "name": "The game stops after turn 40 and the smaller shortfall wins",
  "rule": "R3",
  "players": 2,
  "seed": 1,
  "given": {
   "players": {
    "1": {
     "is_first": true,
     "hand": [
      "1"
     ],
     "hand_count": 1
    },
    "2": {
     "is_first": false
    }
   },
   "game": {
    "turn": 40,
    "acting_seat": 1
   }
  },
  "rules": [
   {
    "seat": 1,
    "options_include": "draw",
    "times": "all"
   },
   {
    "seat": 2,
    "options_include": "draw",
    "times": "all"
   }
  ],
  "expect": {
   "winner": 2,
   "standings": {
    "1": -32,
    "2": -30
   },
   "players": {
    "1": {
     "won": 0,
     "shortfall": 32
    },
    "2": {
     "won": 0,
     "shortfall": 30
    }
   },
   "game": {
    "turn": 41
   }
  },
  "rule_text": "When the players alternate single turns, the game has at most 40 turns, numbered 1 to 40."
 },
 {
  "name": "First player with 1 King has thresho

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Cuttle is a two-player combat card game played with a standard deck. Each turn a player draws or plays one card: a number card for points, a number card to scuttle (destroy) an opposing point card, a one-off effect, or a permanent such as an 8, Jack, Queen or King. The first player to reach 21 points wins, and each King held lowers that target.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "No single simple policy wins. Always-draw never scores, and always-play-points gets scuttled. But the dealer starts with 6 cards against 5 and also moves first, so one seat has a built-in edge. The empty-deck rule (three passes ends the game with no winner) lets a player who is behind stall into a no-result."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Choosing when to scuttle, when to bank points, when to hold a 2 as a counter and when to commit Kings separates players clearly, although lucky draws of Kings and Jacks can swing a single game."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Hand reading, tempo and counter-play leave a lot of room to improve. A weak player still scores by laying point cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, so a player must infer whether the opponent holds a counter, a Jack or a scuttler. Planning the race toward a threshold that the opponent can lower takes several turns of foresight."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Points, King count and threshold are all arithmetic. The only gap is that the three-passes ending gives no winner."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The game has more than ten distinct one-off effects, out-of-turn counters (a 2 played on the opponent's turn, which needs interrupt windows), suit ordering, and stacked Jacks. That is far beyond the step and choice limits. Out-of-turn play is a conditional subsequence that the engine cannot do."
    }
  ],
  "problems": [
    "P1: The full card-effect list (one-offs, out-of-turn 2-counters, 8s, Queens, stacked Jacks, suits) is far too complex to build inside the limits.",
    "P2: Seat asymmetry: the dealer gets an extra card and the first move.",
    "P3: Stalling on an empty deck ends with no winner, so a losing player can force a non-result.",
    "P4: Once the opponent's point cards are fully visible, scuttling is a pure perfect-information calculation, with nothing to infer about the board.",
    "P5 (previous build): `won` was set to 1 for the player who would have acted on turn 41. The turn limit leaked into a win, when after turn 40 the result should be decided by shortfall alone.",
    "P6 (previous build): an unparseable reply defaulted to DRAW, changing the hand and the draw pile, when it should have been PASS.",
    "P7 (previous build): `threshold` and `shortfall` were not reliably recomputed, and `is_first` was set inconsistently at setup (both seats were flipped during the trace)."
  ],
  "changes": [
    {
      "what": "Use a 48-card deck: 40 number cards (ranks 1-10, four of each), 4 Jacks and 4 Kings. There are no suits, no one-offs, no Queens, no 8s and no out-of-turn play. Each turn has exactly one action: PASS, DRAW, POINTS, SCUTTLE, JACK or KING.",
      "why": "This keeps Cuttle's core of racing for points, destroying opposing points, stealing points and lowering the threshold with Kings, inside about 14 steps and 3 choices.",
      "fixes": "P1"
    },
    {
      "what": "Both players get 6 cards. The First seat is chosen at random and needs a base of 32 points; the second seat needs 30.",
      "why": "The 2-point handicap offsets the tempo of moving first, and equal hands remove the extra-card edge.",
      "fixes": "P2"
    },
    {
      "what": "Use a fixed limit of 40 turns. If nobody has won, the smaller shortfall wins; equal shortfalls are a draw.",
      "why": "Every game reaches an arithmetic result, so stalling cannot force a non-result. The shortfall comparison makes the final turns a real race.",
      "fixes": "P3"
    },
    {
      "what": "Point cards show the opponent only a band (Low 1-3, Mid 4-7, High 8-10). Exact points and shortfall are private. A scuttle aimed at a card whose exact rank is unknown fails if the scuttling card is not strictly higher; the scuttling card is lost and the target's rank is announced.",
      "why": "This creates real hidden state. Players must infer the opponent's exact total, how close they are to winning, and whether a scuttle will land.",
      "fixes": "P4"
    },
    {
      "what": "`won` is set in exactly one place: the start-of-turn check, which runs only when turn ≤ 40 and the acting player's points ≥ threshold. After turn 40's action the game ends immediately. No turn 41 exists, no further check runs, and both `won` flags stay 0, so standing = won×1000 − shortfall decides.",
      "why": "This matches rules R3 and R16 and the failed tests that expected standings of −32/−30 and −5/−5 with won = 0.",
      "fixes": "P5"
    },
    {
      "what": "PASS is the default option. Any missing, illegal or unparseable reply resolves as PASS and changes nothing. The DRAW step runs only when the action is exactly DRAW and is legal.",
      "why": "This matches rule R15: hand and draw pile stay unchanged on a bad reply.",
      "fixes": "P6"
    },
    {
      "what": "After every action, both players get points = sum of point-pile ranks, threshold = base − 5×king_count, and shortfall = max(threshold − points, 0). Setup sets is_first exactly once: one random seat True, the other False, never changed afterwards.",
      "why": "This guarantees consistent state for the win check and the tiebreak.",
      "fixes": "P7"
    }
  ],
  "keeps": [
    "A two-player race to a point threshold, played by laying number cards as points.",
    "Scuttling: spend a higher number card to destroy an opposing point card.",
    "Jacks steal an opposing point card.",
    "Kings lower your own winning threshold.",
    "One action per turn: draw or play, from a hidden hand."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The race, scuttle, steal and King core fits the limits once one-offs and out-of-turn play are cut. Hidden point values restore inference. The previous build's bugs are fixed by explicit rules."
  },
  "variation": {
    "name": "Cuttle Lite: Blind Scuttle",
    "summary": "A two-player race to a private point threshold using number cards, Jacks and Kings. Opponents see only the band of each point card, so scuttles and steals are made on inference. The game ends after 40 turns at most, and if nobody has won, the smaller shortfall wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 48 cards: number cards of rank 1 to 10 (four of each, 40 cards), 4 Jacks (J) and 4 Kings (K). There are no suits.\n\nSETUP: Shuffle the deck. Deal 6 cards to each player's hidden hand. The remaining 36 cards form the face-down draw pile. The scrap pile starts empty. Choose one seat at random and mark it First (is_first = true); the other seat gets is_first = false. These marks never change. Each player starts with an empty point pile, points 0, king_count 0 and won 0. Set turn = 1. The First player acts on turn 1, and turns then alternate.\n\nTHRESHOLD: base = 32 for the First player and 30 for the other. threshold = base − 5 × king_count. shortfall = max(threshold − points, 0).\n\nVISIBILITY: Your hand, your exact point cards, your points and your shortfall are known only to you. Both players see:\n- each player's hand_count;\n- each player's king_count and is_first;\n- the size of the draw pile and the scrap pile's contents;\n- each player's point_pile_view, which is the band of every point card in order: Low = rank 1-3, Mid = 4-7, High = 8-10.\n\nEACH TURN (turn 1 to 40):\n1. WIN CHECK: if the acting player's points ≥ threshold, set that player's won = 1 and end the game immediately. This is the only place won is ever set.\n2. The acting player chooses one action. If the reply is missing, illegal or unparseable, the action is PASS.\n   - PASS: nothing happens. Always legal; this is the default.\n   - DRAW: legal only if the draw pile is not empty and your hand has fewer than 8 cards. Take the top card of the draw pile into your hand.\n   - POINTS: choose a number card from your hand and place it in your point pile.\n   - SCUTTLE: choose a number card from your hand and a target position in the opponent's point pile.\n     • If your card's rank is strictly higher than the target's rank, both cards go to the scrap pile.\n     • Otherwise, only your card goes to the scrap pile, the target stays, and the target's exact rank is announced to both players.\n   - JACK: play a Jack from your hand and choose a target position in the opponent's point pile. Move that point card to the end of your own point pile; the Jack goes to the scrap pile.\n   - KING: play a King from your hand. It stays on your side permanently, and your king_count increases by 1.\n   An action that names a card you do not hold, or a target that does not exist, is illegal and counts as PASS.\n3. RECOMPUTE for both players: points = sum of ranks in their point pile; threshold = base − 5 × king_count; shortfall = max(threshold − points, 0); point_pile_view from the bands.\n4. Increase turn by 1. If turn is now 41, the game ends at once: no win check and no action takes place, and won stays 0 for both players. Otherwise the other player acts next.\n\nNote: a player who reaches the threshold during their own turn wins only at the start of their next turn. The opponent therefore gets one turn to scuttle or steal them back below it.",
    "objective": "If a start-of-turn win check sets won = 1, that player wins. If the game ends after turn 40, both won flags are 0 and the player with the smaller shortfall wins; equal shortfalls are a draw. Standing = won × 1000 − shortfall, and the higher standing wins.",
    "expected_effect": "Players race and harass under uncertainty. Each player must estimate the opponent's exact total from the bands, from failed-scuttle reveals and from cards seen in the scrap pile, in order to decide when a scuttle or Jack is needed to stop a win next turn. Low-rank scuttles aimed at Mid cards are gambles. Kings trade a tempo now for a lower bar later. The one-turn grace before a win makes timing and keeping a Jack in reserve matter. Simple policies all lose: always-pass and always-draw score 0, and always-points gets scuttled and stolen by a thinking opponent. The 2-point handicap balances the seats. Talk is omitted because this is a two-player zero-sum game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 3,
    "attributes": 20,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
