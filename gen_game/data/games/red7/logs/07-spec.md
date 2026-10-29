# 07 spec

- time: 2026-10-27T17:38:21+00:00 (66.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0ffc3e25bf5e7276, reply sha256 b46b230404adf29a

## Sent

````
Game: Red3 Duel
Players in the source: 2 to 3
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. There are 21 cards: numbers 1 to 7 in each of three colours, Red, Green and Violet. Colour rank is Red 3, Green 2, Violet 1. A card's strength is number x 10 + colour rank (7 Red = 73, 4 Violet = 41). Higher strength beats lower. A card is EVEN if its number is 2, 4 or 6. A card is LOW if its number is 1, 2 or 3.

THE RULE. The Canvas shows one colour, which is the current rule. Each living player has a KEY under the current rule:
- Red: key = strength of the highest card in your palette.
- Green: key = 100 x (number of even cards in your palette) + strength of your highest even card, or 0 if you have no even card.
- Violet: key = 100 x (number of low cards in your palette) + strength of your highest low card, or 0 if you have no low card.
You are LEADING if your key is strictly higher than every other living player's key. If keys tie, including at 0, no tied player is leading.

SETUP OF A HAND. Shuffle all 21 cards. Deal each player 5 cards as a hidden hand, then 1 card face up as their palette. The remaining cards (9 with 2 players, 3 with 3 players) are set aside unseen for this hand. The Canvas starts as Red. Everyone is alive. The initial leader is the player whose palette card has the highest strength. The first turn of the hand goes to the next player in seat order after that leader.

A TURN. On your turn choose exactly one:
(a) play one card from your hand face up to your palette;
(b) discard one card from your hand to the Canvas, so the rule becomes that card's colour and the card leaves play;
(c) do (a), then (b), with two different cards;
(d) fold.
Then recompute keys under the current rule. If you are not leading, or you folded, or you named a card you do not hold, you are eliminated. Your palette stays visible but no longer counts. If you have no cards left in hand when your turn comes, you can only fold. Play passes to the next living player in seat order.

A ROUND is one pass of turns through all living players in seat order, starting with the player whose turn it is.

END OF A HAND. A hand ends the moment only one player is alive. That player is the hand winner.
- With 2 players: the hand winner scores 1 point; the other scores 0.
- With 3 players: the hand winner scores 2 points; the player whose elimination left one survivor scores 1; the first player eliminated scores 0.
The engine records the hand winner as the MOST RECENT HAND WINNER. If the match is not over, a new hand is set up at the start of the next round.

END OF THE MATCH.
- With 2 players, the match ends when a player reaches 3 points.
- With 3 players, the match ends after any hand in which a player reaches 6 or more points.
- In either case, it also ends when round 40 is complete; an unfinished hand then scores nothing.

INFORMATION. Palettes, the Canvas, eliminations, points and the most recent hand winner are public. Hands and set-aside cards are hidden. There is no table talk.

How the winner is decided: The player with the most points when the match ends wins. With 2 players this is the first to 3 points, and a tie cannot occur at that end. If two or more players share the most points, which can happen in 3 players or at the round-40 cap, the tied player who won the most recently completed hand wins. If no hand was completed at all, the match is a draw.
````

## Reply

````
```json
{
  "name": "Red3 Duel",
  "summary": "A Red7-style shedding duel: on your turn play a card to your palette and/or change the Canvas rule so that you lead under it, or you are out; the last player alive wins the hand, and points across hands win the match.",
  "players": {"min": 2, "max": 3, "suggested": 2},
  "parameters": {
    "card_numbers_min": 1,
    "card_numbers_max": 7,
    "colours": 3,
    "deck_size": 21,
    "rank_red": 3,
    "rank_green": 2,
    "rank_violet": 1,
    "strength_number_multiplier": 10,
    "key_count_multiplier": 100,
    "hand_size": 5,
    "palette_start_size": 1,
    "set_aside_2p": 9,
    "set_aside_3p": 3,
    "winner_points_2p": 1,
    "loser_points_2p": 0,
    "winner_points_3p": 2,
    "second_points_3p": 1,
    "first_out_points_3p": 0,
    "target_points_2p": 3,
    "target_points_3p": 6,
    "round_cap": 40,
    "even_numbers": [2, 4, 6],
    "low_number_max": 3
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards in the player's hidden hand, each stored as its strength (number*10 + colour rank, e.g. 73 = 7 Red).", "observable": false},
      {"key": "palette", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up cards in the player's palette, as strengths.", "observable": true},
      {"key": "alive", "type": "bool", "visible": "public", "initial": true, "meaning": "Whether the player is still in the current hand.", "observable": true},
      {"key": "key_value", "type": "number", "visible": "public", "initial": 0, "meaning": "The player's KEY under the current Canvas rule, recomputed after every turn.", "observable": false},
      {"key": "elim_order", "type": "number", "visible": "public", "initial": 0, "meaning": "0 while alive this hand; otherwise the order in which the player was eliminated this hand (1 = first out).", "observable": false},
      {"key": "acted_this_round", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the player has taken their turn in the current round.", "observable": false},
      {"key": "points", "type": "number", "visible": "public", "initial": 0, "meaning": "Match points (the score).", "observable": true},
      {"key": "is_recent_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if this player won the most recently completed hand, else 0.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [11,12,13,21,22,23,31,32,33,41,42,43,51,52,53,61,62,63,71,72,73], "meaning": "The undealt cards during dealing; rebuilt to all 21 at each new hand.", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "Cards set aside unseen for the current hand (9 with 2 players, 3 with 3 players).", "observable": false},
      {"key": "canvas", "type": "number", "visible": "public", "initial": 3, "meaning": "Current rule colour: 3 = Red, 2 = Green, 1 = Violet.", "observable": true},
      {"key": "turn_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat whose turn it is.", "observable": false},
      {"key": "eliminated_count", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players have been eliminated in the current hand.", "observable": false},
      {"key": "alive_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Living players in the current hand.", "observable": false},
      {"key": "hand_over", "type": "bool", "visible": "public", "initial": true, "meaning": "True when no hand is in progress, so that a new hand is set up at the start of the next round.", "observable": false},
      {"key": "most_recent_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the most recent hand winner (0 = none yet).", "observable": true},
      {"key": "round_no", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of completed rounds.", "observable": true}
    ]
  },
  "setup": [
    "Every player starts with 0 points and is_recent_winner 0; most_recent_winner is 0; round_no is 0.",
    "hand_over is set to true, so the first round begins by setting up a hand."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "when": "hand_over", "effect": "New hand: deck = all 21 strengths [11..73]; for every player: hand = [], palette = [], alive = true, elim_order = 0; eliminated_count = 0; alive_count = number of players; canvas = 3 (Red)."},
    {"action": "update", "who": "each player in turn", "answer": null, "when": "hand_over", "effect": "Deal: 5 times per player, move a random card from deck to that player's hand; then move 1 random card from deck to that player's palette."},
    {"action": "update", "who": "all players", "answer": null, "when": "hand_over", "effect": "Move all remaining deck cards to set_aside (9 with 2 players, 3 with 3 players). Compute key_value under Red (max of palette) for everyone. turn_seat = next seat in seat order after the player with the highest palette strength. hand_over = false. Announce palettes and the Canvas."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Start of round: acted_this_round = false for every player."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand plus all palettes, the canvas, alive flags, points and most_recent_winner."},
    {"action": "repeat", "who": "each living player in turn, starting at turn_seat", "answer": null, "effect": "Repeat the following three steps (turn, resolve, pass) until hand_over is true or every living player has acted_this_round = true."},
    {"action": "ask", "who": "the player at turn_seat", "answer": "one option: 'play X', 'discard X', 'play X then discard Y' (X != Y, both in hand), or 'fold'; only 'fold' if hand is empty", "effect": "Play X: move X from hand to palette. Discard X: remove X from hand (it leaves play) and set canvas = X mod 10. Play X then discard Y: both, in that order. Fold: nothing moves. Set acted_this_round = true."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Recompute key_value for every living player under canvas: Red(3): max strength in palette; Green(2): 100 * count of palette cards with floor(s/10) in {2,4,6} + max such strength, or 0 if none; Violet(1): 100 * count of palette cards with floor(s/10) <= 3 + max such strength, or 0 if none. If the acting player folded or their key_value is not strictly greater than every other living player's key_value: alive = false, eliminated_count += 1, elim_order = eliminated_count, alive_count -= 1. Announce the action, the canvas and any elimination."},
    {"action": "update", "who": "all players", "answer": null, "when": "alive_count == 1", "effect": "Hand ends. The survivor is the hand winner: with 2 players, winner points += 1 (the other gets 0); with 3 players, winner points += 2, the player with elim_order 2 points += 1, the player with elim_order 1 points += 0. Set is_recent_winner = 1 for the winner and 0 for everyone else; most_recent_winner = winner's seat; hand_over = true. Announce the points."},
    {"action": "update", "who": "all players", "answer": null, "when": "not hand_over", "effect": "turn_seat = the next living seat in seat order after the seat that just acted."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round_no += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the match if (number of players == 2 and any player's points >= 3) or (number of players == 3 and hand_over and any player's points >= 6) or round_no >= 40; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "(player_count == 2 and max(points) >= 3) or (player_count == 3 and hand_over and max(points) >= 6) or round_no >= 40",
    "rank_by": "you.points * 10 + you.is_recent_winner",
    "min_to_win": 1,
    "decided_by": "Most points wins. Among players tied on points, the one who won the most recently completed hand wins. If no hand was ever completed, nobody reaches the bar of 1 and the match is a draw with no winner."
  },
  "rules": [
    {"id": "R1", "text": "The deck has 21 cards, numbers 1 to 7 in Red (rank 3), Green (rank 2) and Violet (rank 1), and each card's strength is number*10 + rank (7 Red = 73, 4 Violet = 41)."},
    {"id": "R2", "text": "When a hand is set up, each player gets 5 hidden hand cards and 1 face-up palette card, and the rest (9 with 2 players, 3 with 3 players) go to set_aside unseen."},
    {"id": "R3", "text": "When a hand is set up, canvas is Red (3), every player is alive, and the first turn goes to the next seat after the player whose palette card has the highest strength."},
    {"id": "R4", "text": "When the canvas is Red, a player's key is the highest strength in their palette."},
    {"id": "R5", "text": "When the canvas is Green, a player's key is 100 * (number of palette cards numbered 2, 4 or 6) + the strength of the highest such card, or 0 if they have none."},
    {"id": "R6", "text": "When the canvas is Violet, a player's key is 100 * (number of palette cards numbered 1, 2 or 3) + the strength of the highest such card, or 0 if they have none."},
    {"id": "R7", "text": "A player is leading only if their key is strictly higher than every other living player's key; tied players, including ties at 0, are not leading."},
    {"id": "R8", "text": "When a player plays a card, it moves from their hand to their palette."},
    {"id": "R9", "text": "When a player discards a card, it leaves their hand and play entirely, and the canvas becomes that card's colour."},
    {"id": "R10", "text": "When a player plays then discards, the two cards must be different, and the play happens before the discard."},
    {"id": "R11", "text": "When, after their action, the acting player is not leading under the current canvas, they are eliminated (alive = false)."},
    {"id": "R12", "text": "When a player folds, they are eliminated."},
    {"id": "R13", "text": "When a player has no cards in hand on their turn, their only option is to fold."},
    {"id": "R14", "text": "When a player is eliminated, their palette stays visible but their key no longer counts against others."},
    {"id": "R15", "text": "After a turn, play passes to the next living player in seat order."},
    {"id": "R16", "text": "A round is one pass of turns through all living players in seat order, starting with the player whose turn it is."},
    {"id": "R17", "text": "When only one player is alive, the hand ends immediately and that player is the hand winner and the most recent hand winner."},
    {"id": "R18", "text": "With 2 players, the hand winner scores 1 point and the other scores 0."},
    {"id": "R19", "text": "With 3 players, the hand winner scores 2 points, the second player eliminated scores 1, and the first player eliminated scores 0."},
    {"id": "R20", "text": "When a hand ends and the match is not over, a new hand is set up at the start of the next round."},
    {"id": "R21", "text": "With 2 players, the match ends when a player reaches 3 points."},
    {"id": "R22", "text": "With 3 players, the match ends after a hand in which a player reaches 6 or more points."},
    {"id": "R23", "text": "When round 40 is complete, the match ends and an unfinished hand scores nothing."},
    {"id": "R24", "text": "The player with the most points wins; a tie on points goes to the tied player who won the most recently completed hand; if no hand was completed, the match is a draw."}
  ],
  "offers": [
    {"question": "Your turn: choose an action", "who": "the player at turn_seat (living)", "options": "With an empty hand: fold only. With exactly 1 card X in hand: play X, discard X, fold. With 2 or more cards: play X for each X in hand; discard X for each X in hand; play X then discard Y for each ordered pair of different cards X, Y in hand; fold."}
  ],
  "choices": [
    {"what": "2 to 3 players, suggested 2", "why": "The designer's suggested size is 2, which keeps it a pure duel of reading the rival's palette and timing rule changes. The minimum is 2 because a duel needs a rival, and the maximum is 3 because the deck and the scoring are only defined for 2 or 3 players."},
    {"what": "Cards are stored as their strength numbers (11 to 73)", "why": "Number = floor(s/10) and colour = s mod 10, so every key is plain arithmetic on the list."},
    {"what": "No talk step", "why": "The rules say there is no table talk."},
    {"what": "Turns use sequential ask", "why": "Turns are taken one at a time in seat order, and each player sees the result of the turns before."},
    {"what": "Draw when no hand was completed is made with min_to_win 1", "why": "With no completed hand everyone ranks at 0 and nobody qualifies, giving no winner. Any completed hand gives someone at least 1 point."},
    {"what": "A player's strategy", "why": "Hold back strong cards, switch the rule only when a discard both keeps you leading and leaves the rival needing cards they may not have, and read what a rival's palette implies about their hand."}
  ],
  "simplifications": [
    {"what": "Naming a card not held is never offered", "why": "Options are built from the player's hand, so the 'named a card you do not hold' elimination cannot arise."},
    {"what": "The turns within a round are a repeat loop over living players who have not yet acted", "why": "Turn order starts at turn_seat and must skip eliminated seats, and the loop must stop the moment a hand ends."},
    {"what": "The new-hand setup is a set of update steps each guarded by 'when hand_over'", "why": "The step list is flat, so the setup steps run only when a new hand is needed."}
  ],
  "unsupported": []
}
```
````
