# 06 spec

- time: 2026-10-27T08:41:21+00:00 (70.3s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 5af7ead81ddc4e05, reply sha256 c9665746a4656a15

## Sent

````
Game: Kobayakawa: Held Cards
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP: Each player starts with 4 kamons and sits in a numbered seat (1 to N). The centre holds 11 kamons and the pot starts at 0. Nobody holds a card. The start player for round 1 is seat 1. The game lasts 10 rounds, or ends sooner if only one player remains.

EACH ROUND:
1. DEAL (the round's only random event). Shuffle all cards numbered 1 to 15 except the hand cards currently held by players. Each active player without a hand card receives one, seen only by that player. Every active player then receives one RESERVE card, face down and unseen. Then deal the KOBAYAKAWA face up and the ALTERNATE face down.
2. ANNOUNCE. The engine announces:
   - the round number;
   - the Kobayakawa value and the current pot;
   - each player's kamons;
   - which players are holding a card kept from an earlier round, and for how many rounds;
   - the start player;
   - the minimum stake: 1 in rounds 1-9, 2 in round 10.
3. DRAW CHOICE (simultaneous). Each active player secretly chooses one option:
   - KEEP: keep your hand card.
   - DRAW: look at your reserve card.
   - SHIFT: vote to replace the Kobayakawa.
4. Each player who chose DRAW privately sees their reserve card.
5. KEEP CHOICE (simultaneous, drawers only). Each drawer keeps OLD (the hand card) or NEW (the reserve card) as their hand card. The other card is discarded face up. All undrawn reserve cards are discarded face down, unseen.
6. REVEAL. The engine announces each player's draw choice and all face-up discards.
7. SHIFT. If at least one player chose SHIFT, the Alternate replaces the Kobayakawa and its value is announced.
8. TALK (simultaneous). Every active player writes one short message without seeing the others; all messages are then shown. Talk is not binding and may be false.
9. FIGHT (sequential). Players act once each in seat order, beginning with the start player and wrapping around. Each player sees all earlier choices.
   - The REQUIRED STAKE is the minimum stake, or the minimum + 1 if any earlier player this round fought HIGH.
   - A player chooses PASS, FIGHT LOW (stake = minimum, allowed only while nobody has fought HIGH) or FIGHT HIGH (stake = minimum + 1).
   - A player must PASS if they have fewer kamons than every stake they are allowed to choose.
10. STAKE. Each fighter pays their stake into the pot. The engine moves centre kamons into the pot: 1 in rounds 1-9, and all remaining centre kamons in round 10.
11. SCORE.
   - Nobody fought: the pot carries to the next round.
   - Exactly one fighter: that player takes the whole pot, and their card is not revealed.
   - Two or more fighters: all fighters' cards are revealed. Each fighter's total is their card value. The fighter with the lowest card adds the Kobayakawa value to their total. The highest total takes the whole pot.
12. TIES. If fighters share the highest total, nobody takes the pot and it carries to the next round. In round 10, the pot is instead split equally among the tied fighters, rounding down, and any remainder is removed from the game.
13. CLEANUP.
   - Every fighter's hand card is discarded; that player will receive a fresh card next round.
   - Every player who passed keeps their hand card, still secret.
   - The next start player is the pot winner. If nobody won the pot, it is the next active seat after this round's start player.
14. ELIMINATION. Any player with 0 kamons is eliminated, and their card is discarded unseen.
15. END CHECK. The game ends after round 10, or as soon as only one active player remains.

How the winner is decided: When the game ends, the player with the most kamons wins. If two or more players tie for the most, the game is a draw. If only one active player remains before round 10, that player wins.
````

## Reply

````
```json
{
  "name": "Kobayakawa: Held Cards",
  "summary": "A bluffing and betting game over 10 rounds. Each player holds one secret card and may keep, swap or shift the bonus card, then decides in seat order whether to fight for the kamon pot. A passer may carry their card into later rounds.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "starting_kamons": 4,
    "centre_kamons": 11,
    "starting_pot": 0,
    "card_min": 1,
    "card_max": 15,
    "total_rounds": 10,
    "min_stake_rounds_1_to_9": 1,
    "min_stake_round_10": 2,
    "high_stake_extra": 1,
    "centre_feed_rounds_1_to_9": 1,
    "first_start_seat": 1
  },
  "attributes": {
    "player": [
      {"key": "kamons", "type": "number", "visible": "public", "initial": 4, "meaning": "the player's kamons; this is the score", "observable": true},
      {"key": "active", "type": "bool", "visible": "public", "initial": true, "meaning": "false once the player is eliminated at 0 kamons", "observable": true},
      {"key": "hand", "type": "number", "visible": "ally", "initial": 0, "meaning": "the player's secret hand card, 1-15, or 0 for no card", "observable": false},
      {"key": "held_rounds", "type": "number", "visible": "public", "initial": 0, "meaning": "how many earlier rounds the current hand card has been kept through by passing; 0 means a fresh card", "observable": true},
      {"key": "reserve_seen", "type": "number", "visible": "ally", "initial": 0, "meaning": "the reserve card's value, shown only to a player who chose DRAW, otherwise 0", "observable": false},
      {"key": "draw_choice", "type": "text", "visible": "public", "initial": "", "meaning": "this round's KEEP, DRAW or SHIFT; gathered by a simultaneous poll and revealed at step 6", "observable": true},
      {"key": "keep_choice", "type": "text", "visible": "ally", "initial": "", "meaning": "OLD or NEW, set for drawers only", "observable": false},
      {"key": "fight_choice", "type": "text", "visible": "public", "initial": "", "meaning": "this round's PASS, LOW or HIGH", "observable": true},
      {"key": "stake", "type": "number", "visible": "public", "initial": 0, "meaning": "kamons staked this round", "observable": false},
      {"key": "shown_card", "type": "number", "visible": "public", "initial": 0, "meaning": "the fighter's card once revealed in a showdown, otherwise 0", "observable": false},
      {"key": "total", "type": "number", "visible": "public", "initial": 0, "meaning": "the fighter's showdown total: the card, plus the Kobayakawa if it is the lowest fighter's card", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "the current round, 1-10", "observable": true},
      {"key": "pot", "type": "number", "visible": "public", "initial": 0, "meaning": "kamons in the pot", "observable": true},
      {"key": "centre", "type": "number", "visible": "public", "initial": 11, "meaning": "kamons left in the centre", "observable": true},
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "the shuffled cards 1-15, less the hand cards held by players, rebuilt each round", "observable": false},
      {"key": "reserves", "type": "list", "visible": "none", "initial": [], "meaning": "the face-down reserve cards, one per active seat in seat order, unseen by all", "observable": false},
      {"key": "kobayakawa", "type": "number", "visible": "public", "initial": 0, "meaning": "the face-up Kobayakawa value", "observable": true},
      {"key": "alternate", "type": "number", "visible": "none", "initial": 0, "meaning": "the face-down Alternate card", "observable": false},
      {"key": "face_up_discards", "type": "list", "visible": "public", "initial": [], "meaning": "cards discarded face up this round", "observable": false},
      {"key": "start_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "the seat that acts first in the fight", "observable": true},
      {"key": "min_stake", "type": "number", "visible": "public", "initial": 1, "meaning": "the minimum stake: 1 in rounds 1-9, 2 in round 10", "observable": false},
      {"key": "high_fought", "type": "bool", "visible": "public", "initial": false, "meaning": "true once anyone has fought HIGH this round", "observable": false},
      {"key": "winner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "the seat that took the pot this round, or 0 for none", "observable": false}
    ]
  },
  "setup": [
    "Seat players 1 to N.",
    "Set each player's kamons to 4, active to true, hand to 0 and held_rounds to 0.",
    "Set centre to 11, pot to 0, round to 1 and start_seat to 1."
  ],
  "round": [
    {"action": "update", "who": "engine", "answer": null, "effect": "Set min_stake = 1 if round <= 9, else 2. Set high_fought = false and winner_seat = 0. Clear face_up_discards, and clear each player's draw_choice, keep_choice, fight_choice, stake, shown_card, total and reserve_seen. Set deck = the cards 1..15 minus every active player's hand (where hand > 0), then shuffle it."},
    {"action": "update", "who": "each active player with hand = 0", "answer": null, "effect": "Draw one card at random from deck into hand (visible only to the owner) and remove it from deck."},
    {"action": "update", "who": "each active player", "answer": null, "effect": "Draw one card at random from deck and append it to reserves at that seat's position; remove it from deck. Nobody sees it."},
    {"action": "update", "who": "engine", "answer": null, "effect": "Draw one card from deck into kobayakawa (public) and one into alternate (hidden), removing each from deck."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce round, kobayakawa, pot, every player's kamons, every player with held_rounds > 0 and their held_rounds, start_seat, and min_stake."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player is sent their own state, including their hand."},
    {"action": "poll", "who": "all active players", "answer": "one of KEEP, DRAW, SHIFT", "effect": "Store the answer in draw_choice. It is not shown until step 6."},
    {"action": "update", "who": "each active player with draw_choice = DRAW", "answer": null, "effect": "Set reserve_seen = that seat's card in reserves; only the owner sees it."},
    {"action": "poll", "who": "active players with draw_choice = DRAW", "answer": "one of OLD, NEW", "effect": "Store the answer in keep_choice. If NEW: append hand to face_up_discards, then set hand = reserve_seen. If OLD: append reserve_seen to face_up_discards. Then clear reserves; undrawn reserves are discarded face down, unseen. If a player chose NEW, set held_rounds = 0."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every active player's draw_choice and the contents of face_up_discards."},
    {"action": "update", "who": "engine", "answer": null, "effect": "If the count of players with draw_choice = SHIFT is >= 1, set kobayakawa = alternate and announce the new kobayakawa."},
    {"action": "poll", "who": "all active players", "answer": "short text", "effect": "Broadcast every message to all as {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk is not binding."},
    {"action": "ask", "who": "each active player in turn, in seat order starting at start_seat and wrapping around", "answer": "one of the options allowed for this seat: PASS; LOW if high_fought = false and kamons >= min_stake; HIGH if kamons >= min_stake + 1", "effect": "Store the answer in fight_choice. If LOW, set stake = min_stake. If HIGH, set stake = min_stake + 1 and high_fought = true. If PASS, set stake = 0."},
    {"action": "update", "who": "engine", "answer": null, "effect": "For each player: kamons -= stake and pot += stake. Then the centre feeds the pot: if round <= 9, move min(1, centre) from centre to pot; if round = 10, move all of centre to pot."},
    {"action": "update", "who": "engine", "answer": null, "effect": "Let F = the number of players with fight_choice in {LOW, HIGH}. If F = 1, set winner_seat = that fighter and move the whole pot to their kamons; their card is not revealed. If F >= 2: for each fighter set shown_card = hand and total = hand, and add kobayakawa to the total of the fighter with the lowest hand. If exactly one fighter has the highest total, move the whole pot to them and set winner_seat to their seat. If F = 0, the pot carries."},
    {"action": "update", "who": "engine", "answer": null, "effect": "If F >= 2 and two or more fighters share the highest total: if round <= 9, the pot carries. If round = 10, each tied fighter gains floor(pot / number tied), and pot is set to 0 (the remainder leaves the game)."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every fight_choice, every shown_card and total, the pot result, and every player's kamons."},
    {"action": "update", "who": "engine", "answer": null, "effect": "Each fighter sets hand = 0 and held_rounds = 0. Each active passer keeps hand and adds 1 to held_rounds. For each active player with kamons = 0, set active = false and hand = 0 (their card is discarded unseen). Then set start_seat = winner_seat if winner_seat > 0; otherwise the next active seat after the old start_seat, wrapping. Then add 1 to round."},
    {"action": "check", "who": "engine", "answer": null, "effect": "End the game if round > 10 or the count of active players <= 1. Otherwise continue."}
  ],
  "ending": {
    "condition": "round > 10 or count(active players) <= 1",
    "rank_by": "you.kamons",
    "decided_by": "The player with the most kamons wins. Eliminated players have 0. If only one player remains active, that player has the most kamons and wins. Players tied for the most share the result, which stands for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "At setup, then each player has 4 kamons, the centre has 11, the pot is 0, the start seat is 1, and nobody holds a card."},
    {"id": "R2", "text": "When a round begins, then the deck is the cards 1-15 minus the hand cards held by active players."},
    {"id": "R3", "text": "When a round begins, then each active player with no hand card is dealt one hand card, seen only by them."},
    {"id": "R4", "text": "When a round begins, then each active player is dealt one face-down reserve card that nobody sees, then a face-up Kobayakawa and a face-down Alternate are dealt."},
    {"id": "R5", "text": "When the round is 1-9, then the minimum stake is 1; when the round is 10, then it is 2."},
    {"id": "R6", "text": "When the round is announced, then the announcement gives the round, the Kobayakawa, the pot, every player's kamons, the players holding a kept card with its held_rounds, the start seat and the minimum stake."},
    {"id": "R7", "text": "When the draw choice is made, then every active player chooses KEEP, DRAW or SHIFT at the same time, and no choice is seen until all are in."},
    {"id": "R8", "text": "When a player chose DRAW, then they alone see their reserve card."},
    {"id": "R9", "text": "When a drawer chooses NEW, then the reserve card becomes their hand and the old hand card is discarded face up; when they choose OLD, then the reserve card is discarded face up."},
    {"id": "R10", "text": "When drawers have chosen, then every undrawn reserve card is discarded face down and stays unseen."},
    {"id": "R11", "text": "When the draw choices are revealed, then every player's draw choice and every face-up discard is announced."},
    {"id": "R12", "text": "When at least 1 player chose SHIFT, then the Alternate replaces the Kobayakawa and the new value is announced; when no player chose SHIFT, then the Kobayakawa is unchanged."},
    {"id": "R13", "text": "When the talk step runs, then every active player writes one short message at the same time, and all messages are shown to everyone."},
    {"id": "R14", "text": "When the fight runs, then each active player acts once, in seat order starting at the start seat and wrapping around, and sees all earlier choices."},
    {"id": "R15", "text": "When nobody earlier this round has fought HIGH and the player has at least the minimum stake in kamons, then FIGHT LOW is offered at a stake equal to the minimum."},
    {"id": "R16", "text": "When the player has at least the minimum stake + 1 in kamons, then FIGHT HIGH is offered at a stake of the minimum + 1."},
    {"id": "R17", "text": "When any earlier player this round fought HIGH, then FIGHT LOW is not offered."},
    {"id": "R18", "text": "When a player has fewer kamons than every stake they are allowed, then only PASS is offered."},
    {"id": "R19", "text": "When the fight ends, then each fighter pays their stake into the pot."},
    {"id": "R20", "text": "When the fight ends in rounds 1-9, then 1 kamon moves from the centre to the pot if the centre has any."},
    {"id": "R21", "text": "When the fight ends in round 10, then all remaining centre kamons move to the pot."},
    {"id": "R22", "text": "When nobody fights, then the pot carries to the next round."},
    {"id": "R23", "text": "When exactly one player fights, then they take the whole pot and their card is not revealed."},
    {"id": "R24", "text": "When two or more players fight, then all fighters' cards are revealed, the fighter with the lowest card adds the Kobayakawa value to it, and the unique highest total takes the whole pot."},
    {"id": "R25", "text": "When fighters tie for the highest total in rounds 1-9, then nobody takes the pot and it carries."},
    {"id": "R26", "text": "When fighters tie for the highest total in round 10, then each tied fighter gets floor(pot / number tied), and the remainder leaves the game."},
    {"id": "R27", "text": "When a round is cleaned up, then each fighter's hand card is discarded and their held_rounds is set to 0, and each passer keeps their card and adds 1 to held_rounds."},
    {"id": "R28", "text": "When a player wins the pot, then they are the next start player; when nobody wins it, then the next start player is the next active seat after this round's start seat."},
    {"id": "R29", "text": "When a player has 0 kamons at the end of a round, then they are eliminated and their card is discarded unseen."},
    {"id": "R30", "text": "When round 10 ends, or when only 1 active player remains, then the game ends, and the most kamons wins."}
  ],
  "offers": [
    {"question": "Draw choice", "who": "every active seat", "options": "KEEP, DRAW, SHIFT"},
    {"question": "Keep choice", "who": "every active seat that chose DRAW", "options": "OLD, NEW"},
    {"question": "Talk", "who": "every active seat", "options": "a short free-text message"},
    {"question": "Fight", "who": "each active seat in turn from the start seat", "options": "no HIGH fought yet and kamons >= min+1: PASS, LOW, HIGH. No HIGH fought yet and kamons = min: PASS, LOW. HIGH already fought and kamons >= min+1: PASS, HIGH. Any other case: PASS only."}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer chose 4. Three is the smallest table where fight order, reads and pot competition work. Five fits the 15-card deck: up to 5 hands, 5 reserves and 2 table cards is 12 cards, and more players would stretch the fight sequence."},
    {"what": "Talk kept as one simultaneous poll", "why": "The source specifies it. Bluffing about hand strength gives players something to disagree about."},
    {"what": "A SHIFT voter keeps their hand card", "why": "SHIFT replaces neither the hand nor the reserve, so the hand stays."},
    {"what": "Next start seat chosen after eliminations, skipping eliminated seats", "why": "The source says 'next active seat'."},
    {"what": "Centre feed in rounds 1-9 is limited by what remains", "why": "The centre cannot go negative."},
    {"what": "A drawer who keeps NEW has held_rounds reset to 0", "why": "Their card is no longer one kept from an earlier round."}
  ],
  "simplifications": [
    {"what": "A tie for the most kamons is a shared win rather than a declared draw", "why": "The engine treats players level at the top as sharing the win, with no separate draw."},
    {"what": "Reserve cards are kept in a hidden table list, indexed by seat", "why": "A player attribute cannot be hidden from its own owner, and the rules say the reserve is unseen until drawn."}
  ],
  "unsupported": []
}
```
````
