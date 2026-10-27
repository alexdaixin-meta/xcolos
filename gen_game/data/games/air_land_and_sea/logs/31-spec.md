# 31 spec

- time: 2026-10-27T18:01:21+00:00 (47.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 8005c03a20e9085b, reply sha256 ccacaf1189cab4f4

## Sent

````
Game: Air, Land and Sea: Three Fronts
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
DECK. There are 18 cards. Each has a theater (Air, Land or Sea) and a strength from 1 to 6, giving exactly one card of each strength per theater (Air 1-6, Land 1-6, Sea 1-6). Both players know the full deck list.

MATCH STRUCTURE. The match lasts at most 36 rounds. It is a sequence of battles, and each battle lasts up to 6 battle rounds. Battle round 1 of the first battle is match round 1. When a battle ends, the next battle begins in the next match round, but only if at least 6 match rounds remain (the next round is 31 or earlier). Otherwise the match ends.

START OF A BATTLE (battle round 1 only). Shuffle all 18 cards. Deal 6 privately to each player; this is the round's one random draw. The remaining 6 stay unseen for this battle. Each player's hand is shown to them in the order dealt. Both players' strength in each theater is set to 0.

EACH BATTLE ROUND, in order:
1. WITHDRAW DECISION (simultaneous). Each player secretly chooses 'Fight' or 'Withdraw'.
   - If exactly one player withdraws in battle round k, the other player gains 2 + floor((k-1)/2) VP. That is 2 VP in rounds 1-2, 3 VP in rounds 3-4 and 4 VP in rounds 5-6. The battle ends immediately.
   - If both withdraw, nobody scores and the battle ends.
2. CARD CHOICE (simultaneous). Each player secretly picks one card from their hand.
3. THEATER CHOICE (simultaneous). Each player secretly names Air, Land or Sea.
4. PLACEMENT. Each chosen card leaves its owner's hand and is placed on its owner's side in the named theater.
   - If the named theater matches the card's own theater, the card is face-up and adds its printed strength.
   - Otherwise it is face-down and adds exactly 3 strength.
5. REVEAL. Both players are told every new placement. Face-up cards show their identity. A face-down card is shown only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced.
6. If this was battle round 6 (both hands empty), the battle is resolved.

RESOLVING A BATTLE.
- In each theater, the player with the higher strength controls it. A tie means nobody controls it.
- The player controlling more theaters wins the battle. If both control the same number, the player with the higher total strength across all three theaters wins.
- If that is also equal, the battle is drawn and nobody scores.
- The winner gains 4 VP, or 6 VP if they control all three theaters.
- All face-down identities are then revealed to both players.

AFTER EACH ROUND, the match ends if either player has 12 or more VP.

How the winner is decided: The first player to reach 12 VP at the end of a round wins. Only one player can score in any battle, so both can never reach 12 together. If the match ends because the round limit allows no further full battle, the player with more VP wins. Equal VP is a draw.
````

## Reply

````
```json
{
  "name": "Air, Land and Sea: Three Fronts",
  "summary": "Two commanders fight a series of 6-round battles over three theaters, placing cards face-up or face-down and deciding each round whether to withdraw; the first to 12 VP wins.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 18,
    "theaters": 3,
    "min_strength": 1,
    "max_strength": 6,
    "hand_size": 6,
    "max_match_rounds": 36,
    "battle_rounds": 6,
    "last_battle_start_round": 31,
    "withdraw_base_vp": 2,
    "facedown_strength": 3,
    "battle_win_vp": 4,
    "sweep_vp": 6,
    "target_vp": 12
  },
  "attributes": {
    "player": [
      {"key": "vp", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory points; the score", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards in hand, e.g. 'Air 4', in the order dealt", "observable": false},
      {"key": "air", "type": "number", "visible": "public", "initial": 0, "meaning": "This player's total strength in Air this battle", "observable": true},
      {"key": "land", "type": "number", "visible": "public", "initial": 0, "meaning": "This player's total strength in Land this battle", "observable": true},
      {"key": "sea", "type": "number", "visible": "public", "initial": 0, "meaning": "This player's total strength in Sea this battle", "observable": true},
      {"key": "faceup_played", "type": "list", "visible": "public", "initial": [], "meaning": "Cards this player has placed face-up this battle, with their theater", "observable": false},
      {"key": "facedown_played", "type": "list", "visible": "ally", "initial": [], "meaning": "Identities of cards this player has placed face-down this battle, with the theater each was placed in; the opponent sees only 'face-down card (strength 3) in [theater]'", "observable": false},
      {"key": "withdraw_choice", "type": "text", "visible": "ally", "initial": "", "meaning": "This round's secret Fight/Withdraw choice", "observable": false},
      {"key": "card_choice", "type": "text", "visible": "ally", "initial": "", "meaning": "This round's secret card choice", "observable": false},
      {"key": "theater_choice", "type": "text", "visible": "ally", "initial": "", "meaning": "This round's secret theater choice", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Undealt cards of the current battle; the 6 left after dealing stay unseen", "observable": false},
      {"key": "match_round", "type": "number", "visible": "public", "initial": 1, "meaning": "Current match round, 1 to 36", "observable": true},
      {"key": "battle_round", "type": "number", "visible": "public", "initial": 1, "meaning": "Current round within the battle, 1 to 6", "observable": true},
      {"key": "battle_over", "type": "bool", "visible": "public", "initial": false, "meaning": "True once the current battle has ended by withdrawal or resolution", "observable": false},
      {"key": "match_over", "type": "bool", "visible": "public", "initial": false, "meaning": "True when not enough match rounds remain for another full battle", "observable": false}
    ]
  },
  "setup": [
    "Both players start with 0 vp.",
    "The table sets match_round to 1, battle_round to 1, battle_over to false and match_over to false.",
    "Both players are told the full 18-card deck list: Air 1-6, Land 1-6 and Sea 1-6."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When battle_round == 1: deck is set to all 18 cards; each player's hand, faceup_played and facedown_played are emptied and air, land and sea are set to 0; then 6 random cards are moved from deck to each player's hand (6 draws each). The 6 cards left in deck stay unseen."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand in the order dealt, their facedown_played, and all public state."},
    {"action": "poll", "who": "all players", "answer": "Fight or Withdraw", "effect": "Sets withdraw_choice for each player; nobody sees the other's answer until both are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If exactly one player's withdraw_choice is Withdraw, the other player's vp += 2 + floor((battle_round - 1) / 2). If at least one player withdrew, battle_over = true. Both choices are announced."},
    {"action": "poll", "who": "all players", "answer": "one card from own hand", "effect": "When battle_over is false: sets card_choice for each player; it stays secret until placement."},
    {"action": "poll", "who": "all players", "answer": "Air, Land or Sea", "effect": "When battle_over is false: sets theater_choice for each player; it stays secret until placement."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When battle_over is false: card_choice is removed from each player's hand. If its theater equals theater_choice, it is appended to faceup_played and its printed strength is added to that player's attribute for theater_choice (air, land or sea). Otherwise it is appended to facedown_played and 3 is added to that attribute."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When battle_over is false: both new placements are announced. A face-up card shows its identity and theater. A face-down card shows only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced (each player's air, land and sea)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When battle_round == 6 and battle_over is false: in each theater the player with the higher strength controls it, and a tie means nobody does. The player controlling more theaters wins. If both control the same number, the player with the higher air+land+sea wins. If that is also equal, the battle is drawn and nobody scores. The winner's vp += 6 if they control all 3 theaters, otherwise += 4. battle_over = true."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When the battle was just resolved at battle_round 6: the battle result is announced and every card in both players' facedown_played is revealed to both players."},
    {"action": "update", "who": "all players", "answer": null, "effect": "match_round += 1. If battle_over is true: battle_round = 1 and battle_over = false, and if match_round > 31 then match_over = true. Otherwise battle_round += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if any player's vp >= 12, or match_over is true, or match_round > 36. Otherwise continue with the next round."}
  ],
  "ending": {
    "condition": "any player's vp >= 12 OR match_over == true OR match_round > 36",
    "rank_by": "you.vp",
    "decided_by": "A player's standing is their VP. The first player to reach 12 VP wins; only one player can score in a battle, so both cannot reach 12 together. If the match ends on the round limit, the player with more VP wins, and equal VP is a draw (both share the result)."
  },
  "rules": [
    {"id": "R1", "text": "When a battle starts (battle_round 1), then all 18 cards are shuffled, 6 are dealt into each player's hand, the remaining 6 stay unseen in the deck, and every theater strength is set to 0."},
    {"id": "R2", "text": "When each battle round starts, then both players choose Fight or Withdraw simultaneously, and neither sees the other's choice before both are in."},
    {"id": "R3", "text": "When exactly one player withdraws in battle round 1 or 2, then the other player gains 2 VP and the battle ends immediately."},
    {"id": "R4", "text": "When exactly one player withdraws in battle round 3 or 4, then the other player gains 3 VP and the battle ends immediately."},
    {"id": "R5", "text": "When exactly one player withdraws in battle round 5 or 6, then the other player gains 4 VP and the battle ends immediately."},
    {"id": "R6", "text": "When both players withdraw, then nobody scores and the battle ends immediately."},
    {"id": "R7", "text": "When a battle ends by withdrawal, then no card or theater choice is made that round."},
    {"id": "R8", "text": "When both players fight, then each secretly picks one card from their own hand and then secretly names Air, Land or Sea."},
    {"id": "R9", "text": "When a card is placed in its own theater, then it is face-up and adds its printed strength (1 to 6) to its owner's strength in that theater."},
    {"id": "R10", "text": "When a card is placed in a theater other than its own, then it is face-down and adds exactly 3 strength to its owner's strength in that theater."},
    {"id": "R11", "text": "When cards are placed, then each card leaves its owner's hand and both players are told every placement: face-up cards by identity, face-down cards only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced."},
    {"id": "R12", "text": "When battle round 6 is completed without a withdrawal, then in each theater the player with the higher strength controls it, and a tie means nobody controls it."},
    {"id": "R13", "text": "When a battle is resolved, then the player controlling more theaters wins the battle."},
    {"id": "R14", "text": "When both players control the same number of theaters, then the player with the higher total strength across all three theaters wins the battle."},
    {"id": "R15", "text": "When both players also have equal total strength, then the battle is drawn and nobody scores."},
    {"id": "R16", "text": "When a player wins a battle controlling fewer than 3 theaters, then they gain 4 VP."},
    {"id": "R17", "text": "When a player wins a battle controlling all 3 theaters, then they gain 6 VP."},
    {"id": "R18", "text": "When a battle is resolved, then all face-down card identities are revealed to both players."},
    {"id": "R19", "text": "When a battle ends and the next match round is 31 or earlier, then a new battle begins in the next match round."},
    {"id": "R20", "text": "When a battle ends and the next match round would be 32 or later, then the match ends."},
    {"id": "R21", "text": "When any player has 12 or more VP at the end of a round, then the match ends and that player wins."},
    {"id": "R22", "text": "When the match ends on the round limit, then the player with more VP wins, and equal VP is a draw."}
  ],
  "offers": [
    {"question": "Withdraw decision", "who": "both seats, every battle round", "options": "Fight, Withdraw"},
    {"question": "Card choice", "who": "both seats, only when neither player withdrew this round", "options": "each card currently in that seat's own hand, and nothing else"},
    {"question": "Theater choice", "who": "both seats, only when neither player withdrew this round", "options": "Air, Land, Sea"}
  ],
  "choices": [
    {"what": "2 players (min 2, max 2, suggested 2)", "why": "The designer fixed the game at 2. It is a head-to-head duel of bluffing and tempo: theater control is a two-sided comparison, and withdrawal VP go to 'the other player'. More seats would break both."},
    {"what": "No talk step", "why": "The source has no communication. With two opponents in a zero-sum duel, talk would only add bluffing words that the rules do not call for."},
    {"what": "Card choice and theater choice are two separate simultaneous polls", "why": "The source lists them as separate simultaneous steps. Neither answer is revealed until placement."},
    {"what": "Steps after the withdrawal are skipped with a `when battle_over is false` condition", "why": "This ends the battle immediately within a flat step list."},
    {"what": "The round limit is enforced through match_over, set when the next match round after a battle ends would be greater than 31", "why": "This states the rule that only a full battle may start."},
    {"what": "Card names are written as text like 'Air 4'", "why": "Each card is identified by its theater and strength."}
  ],
  "simplifications": [
    {"what": "A drawn match (equal VP at the round limit) is shown as both players sharing the top rank", "why": "The engine has no separate draw; players level at the top share the result."},
    {"what": "The battle resolution (controls, tie-break by total strength, 4 or 6 VP) is computed in one update step with conditional operations", "why": "It is all arithmetic on air, land and sea, so it needs no referee."}
  ],
  "unsupported": []
}
```
````
