# 20 design

- time: 2026-10-27T04:43:53+00:00 (100.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 a9488e26982ed4c0, reply sha256 6e1e9b361386101e

## Sent

````
Original game: Hanabi
Players in the original: 2 to 5

Original rules:
Cooperative 2-5 players. Deck has 5 colors with three 1s, two 2s-4s, one 5 each. Players hold cards facing out, unseen to owner. Setup 8 hint tokens and 3 fuse tokens. On your turn do one: give a hint, discard, or play. To give a hint spend a hint token, choose one other player and name a color or rank; you must point to all their cards matching it. To discard, choose one of your unknown cards, discard face up, regain one hint token and draw a replacement unseen. To play, place a card to the table; if it is the next number in its color (1 starts a pile) it stays, and completing a pile to 5 regains a hint if available, otherwise it fails and a fuse token is spent. Three fuse tokens lost ends game in failure. When deck empties, each player gets one final turn. Score is sum of top card of each color pile.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Keep a single source of truth for card faces. Treat hand_ids and hand_faces (and deck_ids and deck_faces) as parallel lists that always move together. When a seat discards or plays an ID, find that ID's index in hand_ids and take the face from the same index in hand_faces. Remove both entries together. Write the result as '#ID=face' into discard_pile, or judge the play against the colour's pile using that face. When drawing, move the top entry of deck_ids and deck_faces together onto the end of the hand's two lists. Remove the id_faces lookup, or rebuild it from these lists so it can never disagree with them. Then recheck the following:
- deck_count equals the length of deck_ids after every draw.
- legal_options for the active seat are built from that seat's current hand_ids. Seat 2 was offered PLAY/DISCARD #21 while its hand held #22, #23, #24 and #16.
- A successful play raises the pile and team_score, and every total follows team_score.
- A failed play costs exactly one fuse.
- Discard gains one token, capped at hint_tokens_max.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `R9: seat 1 then seat 2 act; seat 3 is not yet asked after two turns` failed: rule R9 is broken: When turns pass, seats act in order 1, 2, ..., num_players, then seat 1 again, starting with seat 1.; game discard_pile: expected ['#11=R1', '#21=G2'], got ['#11=R4', '#21=R3']; Cleo: the rule for 'DISCARD #25' was never matched (the game never put that option to this seat)
- scenario `R13: a discard reveals the card to discard_pile, gains a token and draws a replacement` failed: rule R13 is broken: When a seat discards an ID from its own hand, the card's face is revealed, it goes to discard_pile, and hint_tokens rises by 1, to at most 8.; game discard_pile: expected ['#12=G1'], got ['#12=B2']
- scenario `R14: discarding at 8 hint tokens keeps 8` failed: rule R14 is broken: When a seat discards with hint_tokens = 8, hint_tokens stays at 8.; game discard_pile: expected ['#12=G1'], got ['#12=R4']
- scenario `R15: playing R1 on an empty red pile raises it to 1` failed: rule R15 is broken: When a seat plays a card whose rank is exactly 1 more than its colour's pile, that pile becomes the card's rank.; seat 1 total: expected 1, got 0; seat 2 total: expected 1, got 0; seat 3 total: expected 1, got 0; game pile_red: expected 1, got 0; game fuses: expected 3, got 2; ga
- what the game did on `R9: seat 1 then seat 2 act; seat 3 is not yet asked after two turns`: moves played: r1 seat 1: 'DISCARD #11'; r2 seat 2: 'DISCARD #21'. First attribute changes: table num_players: 0 -> 3; table target: 0 -> 10; table rank_pool: [] -> ['1', '1', '1', '2', '2', '3', '3', '4', '4', '5']; table deck_faces: [] -> ['R1', 'R1', 'R1', 'R2', 'R2', 'R3', 'R3', 'R4', 'R4', 'R5', 'G1', 'G1', 'G1', 'G2', 'G2', 'G3', 'G3', 'G4', 'G4', 'G5', 'B1', 'B1', 'B1', 'B2', 'B2', 'B3', 'B3', 'B4', 'B4', 'B5']; table id_labels: [] -> ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25', '#26', '#27', '#28', '#29', '#30']; table seat_labels: [] -> ['1', '2', '3', '4']; table hint_values: [] -> ['R', 'G', 'B', '1', '2', '3', '4', '5']; table shuffle_keys: [] -> [[0.7343671530089991, 'R1'], [0.13097277147873954, 'R1'], [0.8417750378811617, 'R1'], [0.8562980243755834, 'R2'], [0.9489545175731703, 'R2'], [0.7873762309262483, 'R3'], [0.7846283011562719, 'R3'], [0.9732059377493494, 'R4'], [0.2931833375134907, 'R4'], [0.2410546760294846, 'R5'], [0.2886262879060659, 'G1'], [0.0015408255802468185, 'G1'], [0.8996227893546725, 'G1'], [0.04170423088910691, 'G2'], [0.29266739407576914, 'G2'], [0.22292047488214473, 'G3'], [0.9192024574483013, 'G3'], [0.13216582981639902, 'G4'], [0.2945236313160716, 'G4'], [0.7850829778452646, 'G5'], [0.5817093302434544, 'B1'], [0.9637872730517733, 'B1'], [0.8638817226735788, 'B1'], [0.9230152601502023, 'B2'], [0.4116506947342514, 'B2'], [0.469935223885966, 'B3'], [0.13405974169398205, 'B3'], [0.09880164945802361, 'B4'], [0.6037157269506478, 'B4'], [0.4259300579889771, 'B5']]; table id_faces: [] -> [['#1', 'G1', 0], ['#2', 'G2', 1], ['#3', 'B4', 2], ['#4', 'R1', 3], ['#5', 'G4', 4], ['#6', 'B3', 5], ['#7', 'G3', 6], ['#8', 'R5', 7], ['#9', 'G1', 8], ['#10', 'G2', 9], ['#11', 'R4', 10], ['#12', 'G4', 11], ['#13', 'B2', 12], ['#14', 'B5', 13], ['#15', 'B3', 14], ['#16', 'B1', 15], ['#17', 'B4', 16], ['#18', 'R1', 17], ['#19', 'R3', 18], ['#20', 'G5', 19], ['#21', 'R3', 20], ['#22', 'R1', 21], ['#23', 'R2', 22], ['#24', 'B1', 23], ['#25', 'G1', 24], ['#26', 'G3', 25], ['#27', 'B2', 26], ['#28', 'R2', 27], ['#29', 'B1', 28], ['#30', 'R4', 29]]; table deck_ids: [] -> ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25', '#26', '#27', '#28', '#29', '#30']; table deck_faces: ['R1', 'R1', 'R1', 'R2', 'R2', 'R3', 'R3', 'R4', 'R4', 'R5', 'G1', 'G1', 'G1', 'G2', 'G2', 'G3', 'G3', 'G4', 'G4', 'G5', 'B1', 'B1', 'B1', 'B2', 'B2', 'B3', 'B3', 'B4', 'B4', 'B5'] -> ['G1', 'G2', 'B4', 'R1', 'G4', 'B3', 'G3', 'R5', 'G1', 'G2', 'R4', 'G4', 'B2', 'B5', 'B3', 'B1', 'B4', 'R1', 'R3', 'G5', 'R3', 'R1', 'R2', 'B1', 'G1', 'G3', 'B2', 'R2', 'B1', 'R4']; table hand_size: 0 -> 4; seat 1 hand_ids: [] -> ['#1', '#4', '#7', '#10']; seat 2 hand_ids: [] -> ['#2', '#5', '#8', '#11'] .... Final: players {"seat 1": {"hand_ids": ["#12", "#13", "#14", "#15"], "hand_faces": ["G4", "B2", "B5", "R1"], "legal_options": [], "total": 0}, "seat 2": {"hand_ids": ["#22", "#23", "#24", "#16"], "hand_faces": ["R1", "R2", "B1", "G1"], "legal_options": ["PLAY #21", "PLAY #22", "PLAY #23", "PLAY #24", "DISCARD #21", "DISCARD #22", "DISCARD #23", "DISCARD #24", "HINT 1 R", "HINT 1 G", "HINT 1 B", "HINT 1 1", "HINT 1 2", "HINT 1 4", "; table {"num_players": 3, "deck_ids": ["#17", "#18", "#19", "#20", "#29", "#30"], "deck_faces": ["B1", "R2", "G2", "B2", "R3", "G3"], "deck_count": 6, "pile_red": 0, "pile_green": 0, "pile_blue": 0, "hint_tokens": 7, "fuses": 3, "discard_pile": ["#11=R4", "#21=R3"], "hint_log": [], "turns_played": 2, "final_round_counter": -1, "counter_set_this_turn": false, "target": 10, "team_score": 0, "active_seat": 3, "last_move": "DIS
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "R1: setup builds 30 cards, 4 per hand with 3 players and 18 in the deck (chance-free counts only)",
  "rule": "R1",
  "players": 3,
  "seed": 1,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": "HINT",
    "times": "all"
   }
  ],
  "expect": {
   "game": {
    "deck_count": 18
   },
   "lens": {
    "game": {
     "deck_faces": 18,
     "deck_ids": 18,
     "discard_pile": 0
    },
    "players": {
     "1": {
      "hand_faces": 4
     },
     "2": {
      "hand_faces": 4
     },
     "3": {
      "hand_faces": 4
     }
    }
   }
  },
  "rule_text": "When the game is set up, the deck has 30 cards: for each of Red, Green and Blue, three 1s, two 2s, two 3s, two 4s and one 5."
 },
 {
  "name": "R2: every card gets an ID, so the deck and hands hold 30 IDs in total (chance-free counts only)",
  "rule": "R2",
  "players": 3,
  "seed": 2,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": "HINT",
    "times": "all"
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "deck_ids": 18
    },
    "players": {
     "1": {
      "hand_ids": 4
     },
     "2": {
      "hand_ids": 4
     },
     "3": {
      "hand_ids": 4
     }
    }
   }
  },
  "rule_text": "When the deck is shuffled at setup, the cards get the IDs #1 to #30 in shuffled order, and an ID never reveals a face."
 },
 {
  "name": "R3: 2 players get 5 cards each and deck_count starts at 20",
  "rule": "R3",
  "players": 2,
  "seed": 3,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": "HINT",
    "times": "all"
   }
  ],
  "expect": {
   "game": {
    "deck_count": 20
   },
   "lens": {
    "game": {
     "deck_ids": 20
    },
    "players": {
     "1": {
      "hand_ids": 5
     },
     "2": {
      "hand_ids": 5
     }
    }
   }
  },
  "rule_text": "When there are 2 players, each hand starts with 5 cards and deck_count starts at 20."
 },
 {
  "name": "R4: 3 players get 4 cards each and deck_count starts at 18",
  "rule": "R4",
  "players": 3,
  "seed": 4,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": "HINT",
    "times": "all"
   }
  ],
  "expect": {
   "game": {
    "deck_count": 18
   },
   "lens": {
    "game": {
     "deck_ids": 18
    },
    "players": {
     "1": {
      "hand_ids": 4
     },
     "2": {
      "hand_ids": 4
     },
     "3": {
      "hand_ids": 4
     }
    }
   }
  },
  "rule_text": "When there are 3 players, each hand starts with 4 cards and deck_count starts at 18; when there are 4 players, each hand starts with 4 cards and deck_count starts at 14."
 },
 {
  "name": "

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Hanabi is a cooperative card game for 2 to 5 players. Each player holds a hand they cannot see but everyone else can, and the team builds five colour piles from 1 to 5 using limited hint tokens, discards and risky plays. The team's score is the sum of the pile tops.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Every simple policy fails. Always discarding scores 0. Always playing blind burns the 3 fuses within a few turns and usually ends below 5. Always hinting runs out of tokens and then has to fall back on another action. No seat has an edge because all share one score. Which card to hint, play or discard decides the outcome."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Good teams that make sound inferences reach 20+ of 25. Careless teams lose fuses and discard 5s, and score under 10. The shuffle matters at the margin: a 5 buried at the bottom of the deck, or both copies of a 2 discarded early, can cap the score. Skill dominates over many games."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak team still lands some 1s and 2s. Strong play keeps improving through hint efficiency, finesse-style inference and token economy. Even expert human groups do not always reach the maximum score."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Your own hand is hidden, so every play rests on inference. You use the hints you received, the cards you can see and what a hint implies about why it was given. Doing this well requires modelling your partners' intentions and planning tokens over many turns."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Pile heights, fuses and the score are pure arithmetic on recorded plays."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only, and its hidden hands are supported. However, 50 cards in 5 colours and 60+ turns exceed the 40-round limit. The result is a team score rather than a winner. The previous build also kept card faces in a lookup table separate from the hands, which drifted out of sync."
    }
  ],
  "problems": [
    "P1 Length: 50 cards and 5 colours give games of 60+ turns, beyond the 40-round limit and too much state for the builder.",
    "P2 No winner: the original produces a cooperative score, but the platform decides only who wins.",
    "P3 Card-face bookkeeping in the previous build: a separate id_faces lookup, built in a different order from the shuffled deck, disagreed with the hands. Discards revealed wrong faces (#12 shown as B2 or R4), and a correct R1 play was judged as a failure, cost a fuse and did not raise the pile.",
    "P4 Legal options in the previous build were not rebuilt from the active seat's current hand. Seat 2 was offered PLAY/DISCARD #21 while holding #22, #23, #24 and #16. Seat 1 was allowed to discard #11, which it did not hold.",
    "P5 Turn order and the end-of-deck final round were under-specified, so the build used extra flags such as counter_set_this_turn and was hard to test.",
    "P6 Attribute budget: the previous design carried redundant state (id_faces, shuffle_keys, id_labels, rank_pool, hint_values, seat_labels, last_move, hand_size), pushing it past 20 attributes."
  ],
  "changes": [
    {
      "what": "Use 3 colours (Red, Green, Blue) with the original rank mix: three 1s, two each of 2/3/4 and one 5, giving 30 cards. Allow 2 to 4 players with fixed hand sizes. Cap the game at 40 turns.",
      "why": "Keeps every game within 40 turns while preserving the rank scarcity that makes discards dangerous.",
      "fixes": "P1 Length"
    },
    {
      "what": "Every seat's total always equals team_score. Every seat whose total reaches 10 (of a maximum 15) wins, so the whole team wins together or all lose together.",
      "why": "Turns the cooperative score into an arithmetic win condition. 10 is out of reach of thoughtless play but reachable by careful inference.",
      "fixes": "P2 No winner"
    },
    {
      "what": "Use a single source of truth for card faces. deck_ids and deck_faces are parallel lists, and each seat's hand_ids and hand_faces are parallel lists. Every move takes entries from the same index of both lists and moves them together. There is no separate lookup table.",
      "why": "A face can then never disagree with its card. Discard reveals and play judgements always use the true face.",
      "fixes": "P3 Card-face bookkeeping in the previous build"
    },
    {
      "what": "At the start of every turn, rebuild legal_options for the active seat only, from that seat's current hand_ids. Clear every other seat's options.",
      "why": "A seat can only play or discard cards it actually holds.",
      "fixes": "P4 Legal options in the previous build"
    },
    {
      "what": "Fix turn order explicitly: seat 1 first, then 2, …, num_players, then seat 1 again. Use a single final_turns_left counter, set to num_players + 1 on the turn the last card is drawn and reduced by 1 at the end of every turn, including that one.",
      "why": "Gives an unambiguous, testable turn order and end of game with no extra flag.",
      "fixes": "P5 Turn order and the end-of-deck final round"
    },
    {
      "what": "Remove id_faces, shuffle_keys, id_labels, rank_pool, hint_values, seat_labels, hand_size and last_move. Merge hint and move logging into one action_log. Hand size follows from num_players. The target 10 is a constant in the rules.",
      "why": "Brings the state to 19 attributes and removes the stale copies that caused the bugs.",
      "fixes": "P6 Attribute budget"
    }
  ],
  "keeps": [
    "Players hold hands they cannot see but everyone else can.",
    "There are three action types: give a hint (spend a token and point to every matching card), discard (regain a token) or play (extend a pile or lose a fuse).",
    "8 hint tokens and 3 fuses, with a token regained for completing a pile.",
    "The original rank distribution per colour: three 1s, two 2s, two 3s, two 4s and one 5.",
    "When the deck runs out, each player gets one final turn.",
    "The game is fully cooperative and the score is the sum of the pile tops.",
    "No free talk: information passes only through hints and through what moves imply."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Hanabi is a strong test of inference from hidden information and partner modelling. A 3-colour, 30-card version fits the limits once card faces have a single source of truth."
  },
  "variation": {
    "name": "Hanabi Trio",
    "summary": "A 3-colour, 30-card cooperative Hanabi for 2 to 4 players. Each player sees everyone's cards except their own and the team must build Red, Green and Blue piles from 1 to 5 using hints, discards and plays. The team wins if it scores at least 10 of 15 before running out of fuses, cards or turns.",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "rules": "R1 Cards. The deck has 30 cards. For each colour Red (R), Green (G) and Blue (B) there are three 1s, two 2s, two 3s, two 4s and one 5. A face is written as colour letter plus rank, e.g. R1, G4, B5.\n\nR2 Shuffle and IDs. At setup the 30 faces are shuffled once into the list deck_faces. The list deck_ids is #1, #2, …, #30 in order, so deck_ids position k and deck_faces position k always belong to the same card. An ID never reveals a face. The front of both lists is the top of the deck. deck_faces is hidden from every player.\n\nR3 Single source of truth. A card's face exists in exactly one place: the faces list paired with the IDs list that currently holds it. That is deck_ids/deck_faces, or a seat's hand_ids/hand_faces, or the discard_pile entry once revealed. Whenever a card moves, its ID and its face are removed from the same index of their two lists and moved together. There is no other record of faces.\n\nR4 Hand sizes. With 2 players each hand has 5 cards and deck_count starts at 20. With 3 players each hand has 4 cards and deck_count starts at 18. With 4 players each hand has 4 cards and deck_count starts at 14.\n\nR5 Dealing. Seat 1 takes the top hand-size cards (ID and face together, in order), then seat 2 takes the next hand-size cards, and so on up to the last seat. Example: with 3 players, seat 1 holds #1-#4, seat 2 #5-#8 and seat 3 #9-#12, and the deck holds #13-#30. deck_count always equals the number of entries in deck_ids.\n\nR6 Visibility. Every player sees every seat's hand_ids. Every player sees every other seat's hand_faces, but never their own. The piles, hint_tokens, fuses, deck_count, discard_pile, action_log, team_score and turns_played are public.\n\nR7 Starting state. pile_red, pile_green and pile_blue start at 0. hint_tokens starts at 8 (maximum 8). fuses starts at 3. team_score starts at 0. discard_pile and action_log start empty. turns_played starts at 0. final_turns_left starts at -1. active_seat starts at 1.\n\nR8 Turn order. One round is one turn by the active seat. Seats act in order 1, 2, …, num_players, then seat 1 again, starting with seat 1. Only the active seat is asked to choose.\n\nR9 Legal options. At the start of each turn, legal_options for the active seat is built from that seat's current hand_ids only. The options are:\n- \"PLAY #id\" for each ID in its hand.\n- \"DISCARD #id\" for each ID in its hand.\n- If hint_tokens is at least 1, \"HINT s v\" for each other seat s and each value v in R, G, B, 1, 2, 3, 4, 5 that matches at least one card in seat s's hand.\nEvery other seat's legal_options is empty. The active seat chooses exactly one option.\n\nR10 Hint. hint_tokens falls by 1. A line is added to action_log naming the giver, the receiver, the value and every ID in the receiver's hand that matches it, e.g. \"turn 4: seat 1 hints seat 2 R = #5, #7\". Hints are public and are not otherwise stored. No card moves.\n\nR11 Finding the card. For PLAY or DISCARD of an ID, find that ID's index i in the active seat's hand_ids. The card's face is hand_faces[i]. Remove index i from both hand_ids and hand_faces.\n\nR12 Play succeeds. The play succeeds if the card's rank is exactly 1 more than its colour's pile. That pile becomes the card's rank and team_score rises by 1. If the rank is 5 and hint_tokens is below 8, hint_tokens rises by 1. action_log records \"turn t: seat a plays #id = face, success\".\n\nR13 Play fails. If the play does not succeed, fuses falls by exactly 1. \"#id=face\" is added to the end of discard_pile, and action_log records the failure with the face.\n\nR14 Discard. The face is revealed and \"#id=face\" is added to the end of discard_pile. hint_tokens rises by 1, to at most 8: discarding with 8 tokens leaves 8. action_log records \"turn t: seat a discards #id = face\".\n\nR15 Drawing. After a PLAY or DISCARD, if deck_ids is not empty, the front entry of deck_ids and the front entry of deck_faces are removed together and added to the end of the active seat's hand_ids and hand_faces. deck_count is set to the length of deck_ids. If this draw made deck_count 0 and final_turns_left is -1, set final_turns_left to num_players + 1. After a HINT, nobody draws.\n\nR16 End of turn. Every seat's total is set to team_score. turns_played rises by 1. If final_turns_left is above 0, it falls by 1. active_seat passes to the next seat (after the last seat, seat 1).\n\nR17 Game end. The game ends at the end of a turn if any of these holds:\n- fuses is 0;\n- team_score is 15;\n- final_turns_left is 0, meaning every player, including the one who drew the last card, has had one more turn after the deck emptied;\n- turns_played is 40.\n\nR18 No talk. There is no message phase. Players may communicate only through the moves above.\n\nR19 Result. Every seat whose total is at least 10 wins. Since all totals equal team_score, the team either wins together (team_score 10 or more) or loses together (below 10). Pile progress counts even if the game ended on the third fuse.",
    "objective": "Cooperative target. When the game ends, every seat's total equals team_score, which is pile_red + pile_green + pile_blue (maximum 15). Every seat whose total reaches 10 wins, so all seats win together if team_score ≥ 10. Otherwise no seat wins and the game counts as a loss for the whole team. Pile progress is counted even when the game ended because fuses reached 0.",
    "expected_effect": "Each player must infer the face of their own cards from hints, from visible cards, from the discard pile and from why a partner chose that hint over the alternatives. This rewards modelling partners' intentions. Token economy matters: with 8 tokens, single 5s and scarce 2s-4s, careless discards or blind plays cap the score below 10, while careful teams reach 11-15. Simple policies lose. Always discard scores 0. Always play burns 3 fuses fast and typically scores 2-5. Always hint stalls once tokens run out. The target of 10 leaves headroom without being hopeless for a reasonable team. Talk is left out because all players want the same outcome (no conflict) and open talk would simply reveal hands, removing the inference. The fixed card bookkeeping means discards reveal true faces, correct plays raise piles, and only held cards can be played."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 1,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 40
  }
}
```
````
