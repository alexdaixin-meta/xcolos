# 05 spec

- time: 2026-10-28T01:40:06+00:00 (74.4s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 6a0f9c2f278956d5, reply sha256 489d79cbc9580ecd

## Sent

````
Game: Growl: Charmed Nights
Players in the source: 5 to 7
Suggested table size, chosen by the designer of these rules (keep it): 6

Rules, as filed in the inventory:
SETUP
- Players sit in a fixed order, numbered 1 to N, where N is 5, 6 or 7.
- Roles are dealt at random and told privately. There is 1 wolf with 5 or 6 players and 2 wolves with 7. Wolves are not told who the other wolf is. Everyone else is a human.
- Each player has four counters:
  - Bites: private; meaningful only for humans.
  - Charms: private.
  - Wounds: public.
  - Salves: public.
- All counters start at 0, except that each human starts with Charms 2 (Charms 3 at 7 players).
- The game lasts 2 x N rounds: 10, 12 or 14. Each round has a Day and a Night.

DAY
1. Active player. Living players take the active role in seat order, skipping dead players. Round 1 starts with player 1.
2. Draw. The engine draws one card at random and announces it to everyone:
   - Wound 30%
   - Charm 30%
   - Salve 25%
   - Bite 15%
3. Talk. Every living player writes one short message at the same moment, without seeing the others. Then all messages are shown to everyone.
4. Give. The active player gives the card to another living player (not themselves). Everyone sees who receives it.
   - Wound or Salve: add 1 to the recipient's counter, in public.
   - Charm: the recipient gains 1 Charm.
   - Bite: a human recipient gains 1 Bite. If the recipient is a wolf, the card is discarded with no effect, and only that wolf learns this.
5. Accusation. All living players vote at the same moment. Each names one other living player, or 'nobody'. If one player is named by strictly more than half of the living players, that player gains 1 Wound. The vote counts are announced.
6. Death check. A player whose Wounds minus Salves is 2 or more dies. Their role is revealed, and they take no further part. If no wolves are alive, the humans win immediately.

NIGHT (no messages)
7. Action. Each living player secretly chooses one action:
   - 'Bite X': wolves only. A human who chooses Bite is treated as choosing None.
   - 'Charm X': requires at least 1 Charm. The sender loses 1 Charm. If the sender has no Charm, this is treated as None.
   - 'None'.
   X must be another living player.
8. Calm. Every wolf targeted by at least one Charm is calmed: its Bite tonight is cancelled. Charms aimed at wolves are used up.
9. Bites land. Each uncancelled Bite on a human adds 1 to that human's Bites. A Bite aimed at a wolf has no effect.
10. Cures. Each Charm on a human removes 1 of that human's Bites, but never below 0.
11. Private reports. Each player is told privately how many Bites landed on them and how many Charms they received, never who sent them. A wolf that was calmed learns that it was calmed.
12. Public report. The engine announces two numbers: the Bites that landed on humans tonight, and the wolves calmed tonight.
13. Infection. Any living human with Bites of 3 or more becomes a wolf. They are told privately. Their Bites reset to 0 and they keep their Charms. From next night on, they may Bite. Wolves never change back.

END CHECKS (after every Night)
14. If every living player is a wolf, the wolves win.
15. If two or fewer players are alive, the game ends and is scored.
16. After the Night of the final round, the game ends and is scored.

SCORING
Count living wolves and living humans. If living wolves are at least as many as living humans, the wolf team wins. Otherwise the human team wins. Each player belongs to the team of their role when the game ends, so converted humans win with the wolves.

How the winner is decided: This is a team win decided by counting roles. The humans win at once if no wolf is alive after a Day death check. The wolves win at once if every living player is a wolf after a Night. Otherwise, when the game ends (final Night, or two or fewer players alive), the wolf team wins if living wolves are at least as many as living humans, and the human team wins otherwise. There are no draws. Each player wins or loses with the team of their role at game end.
````

## Reply

````
```json
{
  "name": "Growl: Charmed Nights",
  "summary": "A hidden-wolf game: wolves bite humans at night to turn them into wolves, humans charm and accuse to find the wolves, and the winning team is decided by counting living roles.",
  "players": {"min": 5, "max": 7, "suggested": 6},
  "parameters": {
    "min_players": 5,
    "max_players": 7,
    "wolves_at_5_or_6": 1,
    "wolves_at_7": 2,
    "human_start_charms_at_5_or_6": 2,
    "human_start_charms_at_7": 3,
    "rounds_per_player": 2,
    "card_weight_wound": 30,
    "card_weight_charm": 30,
    "card_weight_salve": 25,
    "card_weight_bite": 15,
    "card_pool_wound": 6,
    "card_pool_charm": 6,
    "card_pool_salve": 5,
    "card_pool_bite": 3,
    "accusation_wounds": 1,
    "death_threshold": 2,
    "infection_threshold": 3,
    "end_alive_at_most": 2,
    "charm_cost": 1
  },
  "attributes": {
    "player": [
      {"key": "role", "type": "text", "visible": "ally", "initial": "human", "meaning": "'human' or 'wolf'; a wolf is not told who the other wolf is", "observable": false},
      {"key": "is_wolf", "type": "number", "visible": "ally", "initial": 0, "meaning": "1 if role is wolf, else 0; kept equal to role, used in the ranking", "observable": false},
      {"key": "bites", "type": "number", "visible": "ally", "initial": 0, "meaning": "Bite counter; meaningful only for humans; at 3 or more a living human becomes a wolf at Infection", "observable": false},
      {"key": "charms", "type": "number", "visible": "ally", "initial": 0, "meaning": "Charm counter; spent 1 per Night Charm action", "observable": false},
      {"key": "wounds", "type": "number", "visible": "public", "initial": 0, "meaning": "Wound counter", "observable": true},
      {"key": "salves", "type": "number", "visible": "public", "initial": 0, "meaning": "Salve counter; offsets wounds in the death check", "observable": true},
      {"key": "alive", "type": "bool", "visible": "public", "initial": true, "meaning": "false once the player has died", "observable": true},
      {"key": "revealed_role", "type": "text", "visible": "public", "initial": "", "meaning": "the role, made public when the player dies", "observable": true},
      {"key": "votes_received", "type": "number", "visible": "public", "initial": 0, "meaning": "accusation votes naming this player this Day", "observable": true},
      {"key": "night_choice", "type": "text", "visible": "ally", "initial": "None", "meaning": "this Night's secret action: 'Bite seat k', 'Charm seat k' or 'None'", "observable": false},
      {"key": "bites_tonight", "type": "number", "visible": "ally", "initial": 0, "meaning": "uncancelled Bites that landed on this human tonight", "observable": false},
      {"key": "charms_tonight", "type": "number", "visible": "ally", "initial": 0, "meaning": "valid Charms aimed at this player tonight", "observable": false},
      {"key": "calmed", "type": "bool", "visible": "ally", "initial": false, "meaning": "true if this wolf was targeted by at least one valid Charm tonight", "observable": false},
      {"key": "won", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if this player's team won (set at game end)", "observable": true}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round number", "observable": true},
      {"key": "total_rounds", "type": "number", "visible": "public", "initial": 0, "meaning": "2 x N", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "seat of this Day's active player", "observable": true},
      {"key": "card_pool", "type": "list", "visible": "none", "initial": ["Wound","Wound","Wound","Wound","Wound","Wound","Charm","Charm","Charm","Charm","Charm","Charm","Salve","Salve","Salve","Salve","Salve","Bite","Bite","Bite"], "meaning": "the 20-entry pool that gives the card odds (30/30/25/15 percent); a card is picked from it at random and not removed", "observable": false},
      {"key": "card", "type": "text", "visible": "public", "initial": "", "meaning": "this Day's drawn card", "observable": true},
      {"key": "recipient_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "seat that received this Day's card", "observable": true},
      {"key": "living_count", "type": "number", "visible": "public", "initial": 0, "meaning": "number of living players", "observable": true},
      {"key": "living_wolves", "type": "number", "visible": "none", "initial": 0, "meaning": "number of living wolves", "observable": false},
      {"key": "living_humans", "type": "number", "visible": "none", "initial": 0, "meaning": "number of living humans", "observable": false},
      {"key": "bites_landed_tonight", "type": "number", "visible": "public", "initial": 0, "meaning": "public report: Bites that landed on humans tonight", "observable": true},
      {"key": "wolves_calmed_tonight", "type": "number", "visible": "public", "initial": 0, "meaning": "public report: wolves calmed tonight", "observable": true},
      {"key": "wolves_won", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if the wolf team won, 0 if the human team won", "observable": true},
      {"key": "game_over", "type": "number", "visible": "public", "initial": 0, "meaning": "1 once the game has ended", "observable": true}
    ]
  },
  "setup": [
    "Seats are numbered 1 to N in a fixed order, where N is 5, 6 or 7.",
    "total_rounds is set to 2 x N (10, 12 or 14). living_count is set to N.",
    "Roles are dealt at random: 1 wolf if N is 5 or 6, 2 wolves if N is 7, and every other seat is a human. Each wolf has role 'wolf' and is_wolf 1. Each player is told only their own role, and wolves are not told who the other wolf is.",
    "Each human gets charms 2, or charms 3 when N is 7. Wolves get charms 0. All other counters start at 0.",
    "living_wolves and living_humans are set from the deal."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; active_seat = the first living seat after active_seat in seat order, wrapping from N to 1 (round 1 gives seat 1, since active_seat starts at 0). Announce the round and the active seat."},
    {"action": "update", "who": "all players", "answer": null, "effect": "card = one entry picked at random from card_pool, which is not removed (30% Wound, 30% Charm, 25% Salve, 15% Bite). Announce card to everyone."},
    {"action": "poll", "who": "all living players", "answer": "a short text message", "effect": "No state changes. Once all messages are in, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."},
    {"action": "ask", "who": "the active player (seat active_seat)", "answer": "a choice of another living seat", "effect": "recipient_seat = the chosen seat. If card is Wound, the recipient's wounds += 1. If Salve, salves += 1. If Charm, charms += 1. If Bite and the recipient is human, bites += 1; if Bite and the recipient is a wolf, nothing changes and only that wolf is told privately that the Bite was discarded. Announce the recipient to everyone."},
    {"action": "poll", "who": "all living players", "answer": "a choice of another living seat, or 'nobody'", "effect": "Each living player's votes_received = the number of votes naming them. If some player has 2 x votes_received > living_count, that player's wounds += 1. Announce every vote count."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Each living player with wounds - salves >= 2: alive = false, revealed_role = role. Announce each death and the revealed role. Recompute living_count, living_wolves and living_humans. Reset votes_received to 0."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If living_wolves == 0: wolves_won = 0, game_over = 1, each human's won = 1, and the game ends with a human win. Otherwise continue."},
    {"action": "poll", "who": "all living players", "answer": "one of: 'Bite seat k' or 'Charm seat k' for each other living seat k, or 'None'", "effect": "Store each player's answer in their night_choice. No messages are allowed at Night."},
    {"action": "update", "who": "all players", "answer": null, "effect": "1. A Bite is valid only if the chooser's role is wolf; a human's Bite counts as None. 2. A Charm is valid only if the chooser has charms >= 1, and that chooser loses 1 charm; a Charm with no charms counts as None. 3. charms_tonight = the number of valid Charms aimed at the player. 4. Each wolf with charms_tonight >= 1 has calmed = true, and that wolf's Bite tonight is cancelled. 5. For each human, bites_tonight = the number of valid, uncancelled Bites aimed at them; Bites aimed at wolves have no effect. 6. Each human's bites = max(0, bites + bites_tonight - charms_tonight), so Bites land first and Charms then cure them, never below 0. 7. bites_landed_tonight = the sum of bites_tonight over humans; wolves_calmed_tonight = the number of wolves with calmed = true."},
    {"action": "tell", "who": "each living player privately", "answer": null, "effect": "Tell each player their bites_tonight (0 for a wolf) and charms_tonight, without naming any sender. Tell each calmed wolf that it was calmed."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Tonight {bites_landed_tonight} Bites landed on humans and {wolves_calmed_tonight} wolves were calmed.'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "Each living human with bites >= 3: role = 'wolf', is_wolf = 1, bites = 0, charms unchanged. They are told privately. Recompute living_wolves and living_humans. Reset night_choice, bites_tonight, charms_tonight and calmed."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If living_humans == 0: wolves_won = 1 and the game ends. Otherwise, if living_count <= 2 or round == total_rounds: wolves_won = 1 if living_wolves >= living_humans, else 0, and the game ends. When the game ends, set game_over = 1 and won = 1 for every player whose is_wolf equals wolves_won. Otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "game_over == 1, which is set when living_wolves == 0 after a Day death check, or after a Night when living_humans == 0, living_count <= 2 or round == total_rounds",
    "rank_by": "1 - abs(you.is_wolf - game.wolves_won)",
    "min_to_win": 1,
    "decided_by": "A team win. Every player whose current role is on the winning team (wolves if wolves_won is 1, humans otherwise) scores 1 and shares the win, including dead players and humans converted to wolves. Everyone else scores 0."
  },
  "rules": [
    {"id": "R1", "text": "When N is 5 or 6, exactly 1 seat is dealt the wolf role; when N is 7, exactly 2 are; every other seat is a human."},
    {"id": "R2", "text": "When the game starts, each human has charms 2 (3 when N is 7), each wolf has charms 0, and every bites, wounds and salves counter is 0."},
    {"id": "R3", "text": "When the game starts, total_rounds is 2 x N (10 at 5, 12 at 6, 14 at 7 players)."},
    {"id": "R4", "text": "When a round starts, the active player is the next living seat after the previous one in seat order, and round 1's active player is seat 1."},
    {"id": "R5", "text": "When a Day starts, one card is drawn from the 20-entry pool (6 Wound, 6 Charm, 5 Salve, 3 Bite) and announced to everyone."},
    {"id": "R6", "text": "When the Talk step runs, every living player submits one message at once and all messages are then shown to everyone."},
    {"id": "R7", "text": "When the active player gives the card, the recipient must be another living seat, never the active player."},
    {"id": "R8", "text": "When a Wound card is given, the recipient's wounds rise by 1; when a Salve card is given, the recipient's salves rise by 1."},
    {"id": "R9", "text": "When a Charm card is given, the recipient's charms rise by 1."},
    {"id": "R10", "text": "When a Bite card is given to a human, that human's bites rise by 1; when it is given to a wolf, nothing changes and only that wolf is told the card was discarded."},
    {"id": "R11", "text": "When the accusation vote is held, each living player names another living player or 'nobody', all at once."},
    {"id": "R12", "text": "When a player is named by more than half of the living players (for example 4 of 6 or 3 of 5), that player's wounds rise by 1; otherwise nobody gains a wound; the vote counts are announced either way."},
    {"id": "R13", "text": "When a living player's wounds minus salves is 2 or more at the Day death check, that player dies (alive = false) and their role is revealed."},
    {"id": "R14", "text": "When no wolf is alive after the Day death check, the humans win immediately."},
    {"id": "R15", "text": "When a human chooses 'Bite' at Night, it is treated as 'None'."},
    {"id": "R16", "text": "When a player with charms 0 chooses 'Charm', it is treated as 'None'; when a player with charms of 1 or more chooses 'Charm', they lose 1 charm."},
    {"id": "R17", "text": "When a wolf is targeted by at least one valid Charm, it is calmed and its Bite that Night is cancelled, and those Charms are used up."},
    {"id": "R18", "text": "When an uncancelled Bite targets a human, that human's bites rise by 1; when a Bite targets a wolf, it has no effect."},
    {"id": "R19", "text": "When valid Charms target a human, each removes 1 of that human's bites after the Bites land, never below 0."},
    {"id": "R20", "text": "When the Night resolves, each player is told privately how many Bites landed on them and how many Charms they received, never who sent them, and each calmed wolf is told it was calmed."},
    {"id": "R21", "text": "When the Night resolves, the total Bites landed on humans and the number of wolves calmed are announced to everyone."},
    {"id": "R22", "text": "When a living human has bites of 3 or more at Infection, they become a wolf, are told privately, reset bites to 0 and keep their charms."},
    {"id": "R23", "text": "When every living player is a wolf after a Night, the wolves win."},
    {"id": "R24", "text": "When 2 or fewer players are alive after a Night, or the Night of round 2 x N ends, the wolves win if living wolves are at least as many as living humans, and the humans win otherwise."},
    {"id": "R25", "text": "When the game ends, each player wins or loses with the team of their role at that moment, so converted humans win with the wolves, and dead players share their team's result."}
  ],
  "offers": [
    {"question": "Talk (Day)", "who": "every living seat", "options": "a short free-text message"},
    {"question": "Give the card", "who": "the active seat only", "options": "every living seat except the active seat"},
    {"question": "Accusation vote", "who": "every living seat", "options": "every living seat except the voter, plus 'nobody'"},
    {"question": "Night action", "who": "every living seat, wolf or human, whatever its charms", "options": "'Bite seat k' and 'Charm seat k' for every living seat k other than the chooser, plus 'None'; a human's Bite and a Charm with 0 charms are resolved as None"}
  ],
  "choices": [
    {"what": "5 to 7 players, suggested 6", "why": "The designer gives 5 to 7 and suggests 6. Below 5 a single wolf has too few humans to hide among. Above 7 the accusation majority and the night charms get too diffuse for one player's choice to matter."},
    {"what": "Keep the simultaneous Day talk as a poll with broadcast", "why": "The rules require it. Humans want to find the wolf while wolves want to misdirect, so the talk is real disagreement worth reasoning about."},
    {"what": "Card odds as a 20-entry pool drawn with replacement", "why": "6/6/5/3 out of 20 gives exactly 30/30/25/15 percent, and the rules state odds, not a depleting deck."},
    {"what": "Every seat is offered the same Night options, including Bite and Charm", "why": "The rules define a human's Bite and a chargeless Charm as None. Offering identical lists keeps the private offer itself from revealing a role or a charm count."},
    {"what": "Night action as one choice combining action and target", "why": "This fits the engine's single choice-from-a-list answer."},
    {"what": "A Bite card given to a human is never infection-checked during the Day", "why": "The source checks infection only at the Night Infection step."},
    {"what": "Team win encoded as is_wolf compared with wolves_won, with min_to_win 1", "why": "The engine ranks by one expression. This gives 1 to every member of the winning team and 0 to the rest."},
    {"what": "Ties and simultaneous end conditions are checked in this order: no living humans, then two or fewer alive or the final round", "why": "The outcome is the same either way: if no humans remain, wolves outnumber them."}
  ],
  "simplifications": [
    {"what": "Roles revealed on death are copied into a public revealed_role attribute", "why": "Visibility is fixed per attribute, so a public copy is how one player's secret becomes public."},
    {"what": "is_wolf kept as a number beside role", "why": "The ranking expression needs arithmetic on the role."}
  ],
  "unsupported": []
}
```
````
