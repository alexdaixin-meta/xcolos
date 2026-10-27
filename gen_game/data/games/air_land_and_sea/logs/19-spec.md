# 19 spec

- time: 2026-10-27T17:48:42+00:00 (42.5s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 ba9223bbf5ebfd41, reply sha256 16dc12ed6b9c6424

## Sent

````
Game: Air, Land and Sea: Four Battles
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. There are 18 cards: Air 1–6, Land 1–6 and Sea 1–6. A card's strength is its number.

MATCH. The match has 24 rounds, grouped into 4 battles of 6 rounds:
- Battle 1 is rounds 1–6.
- Battle 2 is rounds 7–12.
- Battle 3 is rounds 13–18.
- Battle 4 is rounds 19–24.

START OF EVERY ROUND (bookkeeping, no choices).
- Set battle = floor((round−1)/6)+1.
- Set round_in_battle = round − 6×(battle−1).
- Set first player = seat 1 if battle is 1 or 3, seat 2 if battle is 2 or 4.
- These values come only from the round number. Nothing else changes them.

BATTLE START (only when round_in_battle = 1).
- Set battle_over to false.
- Reset every player's Air, Land and Sea strength to 0 and clear all played cards.
- Shuffle all 18 cards.
- Deal 6 privately to each player's hand.
- Put the remaining 6 aside unseen. They are out of play for this battle.
- This is the only random event in a round.

ACTIONS. If battle_over is false, the first player takes one action. Then, if battle_over is still false, the second player takes one action. An action is exactly one of:
(a) DEPLOY: play a card from your hand face-up to the theater named on it. Add its number to your strength there.
(b) IMPROVISE: play a card from your hand face-down to any theater. Add 2 to your strength there. The opponent sees only the theater and the +2, not the card.
(c) WITHDRAW: concede the battle.

All theater strengths and face-up cards are public. Hands, the set-aside cards and the identity of face-down cards are hidden.

WITHDRAWAL.
- When a player withdraws, count the cards left in their hand.
- The opponent immediately gains VP as follows: 4 or more cards gives 2 VP; 2 or 3 cards gives 3 VP; 1 card gives 4 VP.
- battle_over becomes true at once.
- If the first player withdrew, the second player does not act that round.
- Every remaining round of the battle passes with no actions and no scoring.
- The next battle starts at its fixed round as usual.

BATTLE END (only when round_in_battle = 6 and battle_over is false, after both actions).
- Both hands are now empty.
- In each theater, the player with the higher strength controls it. A tie goes to that battle's first player.
- The player who controls 2 or more theaters wins the battle and gains 6 VP.
- Set battle_over to true.

END.
- After round 24 the game ends.

How the winner is decided: After round 24, the player with more VP wins. Equal VP is a draw.
````

## Reply

````
```json
{
  "name": "Air, Land and Sea: Four Battles",
  "summary": "Two commanders fight 4 battles of 6 rounds over three theaters, playing cards face-up for their strength or face-down for 2, and may withdraw early to limit the VP the opponent gains.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "total_cards": 18,
    "theaters": 3,
    "min_strength": 1,
    "max_strength": 6,
    "total_rounds": 24,
    "battles": 4,
    "rounds_per_battle": 6,
    "hand_size": 6,
    "set_aside_count": 6,
    "improvise_strength": 2,
    "withdraw_vp_4_plus_cards": 2,
    "withdraw_vp_2_or_3_cards": 3,
    "withdraw_vp_1_card": 4,
    "battle_win_vp": 6,
    "theaters_to_win_battle": 2
  },
  "attributes": {
    "player": [
      {"key": "vp", "type": "number", "visible": "public", "initial": 0, "meaning": "victory points earned so far", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "cards held this battle, such as 'Air 3'", "observable": false},
      {"key": "air", "type": "number", "visible": "public", "initial": 0, "meaning": "this player's strength in the Air theater this battle", "observable": true},
      {"key": "land", "type": "number", "visible": "public", "initial": 0, "meaning": "this player's strength in the Land theater this battle", "observable": true},
      {"key": "sea", "type": "number", "visible": "public", "initial": 0, "meaning": "this player's strength in the Sea theater this battle", "observable": true},
      {"key": "face_up", "type": "list", "visible": "public", "initial": [], "meaning": "cards this player deployed face-up this battle", "observable": false},
      {"key": "face_down", "type": "list", "visible": "ally", "initial": [], "meaning": "identities of cards this player improvised face-down this battle, with their theater; the opponent sees only the +2 in that theater's strength", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "current round, 1 to 24", "observable": true},
      {"key": "battle", "type": "number", "visible": "public", "initial": 1, "meaning": "current battle, floor((round-1)/6)+1", "observable": true},
      {"key": "round_in_battle", "type": "number", "visible": "public", "initial": 1, "meaning": "round - 6*(battle-1)", "observable": false},
      {"key": "first_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "first player: seat 1 in battles 1 and 3, seat 2 in battles 2 and 4", "observable": false},
      {"key": "battle_over", "type": "bool", "visible": "public", "initial": false, "meaning": "true once the current battle has been decided by withdrawal or by the battle end", "observable": false},
      {"key": "deck", "type": "list", "visible": "none", "initial": ["Air 1","Air 2","Air 3","Air 4","Air 5","Air 6","Land 1","Land 2","Land 3","Land 4","Land 5","Land 6","Sea 1","Sea 2","Sea 3","Sea 4","Sea 5","Sea 6"], "meaning": "the 18 cards to be shuffled and dealt at each battle start", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "the 6 undealt cards, out of play this battle", "observable": false}
    ]
  },
  "setup": [
    "Seat both players. Each player's vp is 0.",
    "round is set to 1 and battle_over to false.",
    "The deck holds all 18 cards: Air 1-6, Land 1-6 and Sea 1-6."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Set battle = floor((round-1)/6)+1. Set round_in_battle = round - 6*(battle-1). Set first_seat = 1 if battle is 1 or 3, and 2 if battle is 2 or 4. Announce the round, the battle and the first player."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Only when round_in_battle = 1 (battle start): set battle_over = false. Set every player's air, land and sea to 0. Return every card in each hand, face_up, face_down and set_aside to deck, so deck holds all 18 cards. Draw 6 cards at random from deck into each player's hand, removing each from deck. Move the remaining 6 deck cards to set_aside."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately sees their own hand and face_down, plus every public attribute: all air, land and sea strengths, all face_up cards, vp, round, battle, first_seat and battle_over."},
    {"action": "ask", "who": "the seat named by first_seat, only when battle_over is false", "answer": "one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand and any theater, or 'withdraw'", "effect": "Deploy: remove the card from hand, append it to face_up, and add its number to the player's strength in the theater named on the card. Improvise: remove the card from hand, append it with the chosen theater to face_down, and add 2 to the player's strength in the chosen theater; only the theater and the +2 are announced. Withdraw: let n = length of the player's hand; the opponent's vp += 4 if n = 1, 3 if n is 2 or 3, and 2 if n >= 4; set battle_over = true."},
    {"action": "ask", "who": "the seat that is not first_seat, only when battle_over is false", "answer": "one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand and any theater, or 'withdraw'", "effect": "Same effects as the first player's action, applied to this player."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Only when round_in_battle = 6 and battle_over is false (battle end): in each of air, land and sea, the player with the higher strength controls that theater, and a tie goes to the first_seat player. The player who controls 2 or more theaters gains vp += 6. Set battle_over = true. Announce the strengths and the battle winner."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round = 24, end the game. Otherwise continue."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1."}
  ],
  "ending": {
    "condition": "round = 24 after that round's steps have run",
    "rank_by": "you.vp",
    "decided_by": "Each player's standing is their total VP after round 24. The player with more VP wins. Equal VP is a draw, and both players share the win."
  },
  "rules": [
    {"id": "R1", "text": "The deck has 18 cards, Air 1-6, Land 1-6 and Sea 1-6, and a card's strength is its number."},
    {"id": "R2", "text": "The match has 24 rounds, and battle = floor((round-1)/6)+1, so rounds 1-6 are battle 1, rounds 7-12 battle 2, rounds 13-18 battle 3 and rounds 19-24 battle 4."},
    {"id": "R3", "text": "When the battle is 1 or 3, then seat 1 is the first player; when the battle is 2 or 4, then seat 2 is the first player."},
    {"id": "R4", "text": "When round_in_battle = 1, then battle_over becomes false, every air, land and sea strength becomes 0, and all played cards are cleared."},
    {"id": "R5", "text": "When round_in_battle = 1, then all 18 cards are shuffled, each player is dealt 6 cards privately into hand, and the remaining 6 go to set_aside, out of play and unseen."},
    {"id": "R6", "text": "When battle_over is false, then the first player takes exactly one action, and the second player then takes one action if battle_over is still false."},
    {"id": "R7", "text": "When a player deploys a card such as Land 5, then it leaves their hand face-up and their land strength rises by 5."},
    {"id": "R8", "text": "When a player improvises a card to a chosen theater, then it leaves their hand face-down and their strength in that theater rises by 2, whatever the card's number or suit."},
    {"id": "R9", "text": "When a card is improvised, then the opponent sees only the theater and the +2, never the card's identity."},
    {"id": "R10", "text": "When a player withdraws with 4 or more cards in hand, then the opponent gains 2 VP."},
    {"id": "R11", "text": "When a player withdraws with 2 or 3 cards in hand, then the opponent gains 3 VP."},
    {"id": "R12", "text": "When a player withdraws with 1 card in hand, then the opponent gains 4 VP."},
    {"id": "R13", "text": "When a player withdraws, then battle_over becomes true at once, and if the first player withdrew, then the second player does not act that round."},
    {"id": "R14", "text": "When battle_over is true, then the remaining rounds of that battle pass with no actions and no scoring, and the next battle starts at its fixed round."},
    {"id": "R15", "text": "When round_in_battle = 6 and battle_over is false after both actions, then in each theater the player with the higher strength controls it, and a tie goes to the battle's first player."},
    {"id": "R16", "text": "When a player controls 2 or more of the 3 theaters at a battle end, then they gain 6 VP and battle_over becomes true."},
    {"id": "R17", "text": "When round 24 ends, then the game ends, the player with more VP wins, and equal VP is a draw."}
  ],
  "offers": [
    {"question": "First player's action (when battle_over is false)", "who": "the seat named by first_seat", "options": "'deploy <card>' for each card in their hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in their hand; 'withdraw'."},
    {"question": "Second player's action (when battle_over is still false)", "who": "the seat that is not first_seat", "options": "'deploy <card>' for each card in their hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in their hand; 'withdraw'. Not asked at all if the first player withdrew this round."}
  ],
  "choices": [
    {"what": "Exactly 2 players", "why": "The designer fixed the table at 2. Theater control is a head-to-head comparison, the tie rule names the battle's first player, and withdrawal VP goes to 'the opponent', so the game is defined only for two."},
    {"what": "No talk step", "why": "The source has none. With two directly opposed players there is no coalition to form, so talk would only add words. The strategy lies in bluffing with face-down cards, reading the opponent's public strengths and judging when to withdraw cheaply."},
    {"what": "Actions use sequential ask", "why": "The rules order the first player before the second, and the second player reacts to the first player's public play."},
    {"what": "Withdrawal VP for 0 cards is not defined", "why": "A player always holds at least 1 card when acting, since 6 cards cover 6 actions, so the 0-card case never occurs."}
  ],
  "simplifications": [
    {"what": "Theater control compares two players' attributes", "why": "The engine has no player-attribute operand. The comparison of seat 1's and seat 2's air, land and sea is done with a table-attribute mirror beside the strengths, the listed workaround; the outcome is unchanged."},
    {"what": "Battle start is a single update with operations guarded by round_in_battle = 1", "why": "The step list is flat, so conditional operations replace a separate block. The behavior is identical."},
    {"what": "Shuffling is modeled as random draws from the deck list", "why": "Drawing at random is equivalent to shuffling and then dealing."}
  ],
  "unsupported": []
}
```
````
