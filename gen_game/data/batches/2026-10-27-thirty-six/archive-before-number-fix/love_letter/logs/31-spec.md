# 31 spec

- time: 2026-10-27T19:07:38+00:00 (59.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 6df963ec052c7beb, reply sha256 df233e3cf3f092c0

## Sent

````
Game: Love Letter: Short Hands
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS (16, stored once as full_deck): 5 Guard (rank 1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8).

STATE
- Each player has: hand (private, seen only by its owner), discards (public list), points (start 0), protected (public, 0/1) and eliminated (public, 0/1).
- The table shows: out_of_play (public list), deck_count (public, always the number of cards in the deck), stake, active seat, starter seat (starts as seat 1) and round number.
- Hidden bookkeeping: deck order, new_hand (starts 1), folded, current_discard and guard_guess.
- The bottom card of the deck is the RESERVE. It is never drawn at the start of a turn.

ROUND: one round is one turn by the active player. The game lasts exactly 40 rounds. The steps run in order every round. A step marked 'when' runs only if its condition holds.

1. NEW HAND (when new_hand = 1):
- Empty both players' hands and discards, and clear out_of_play.
- Copy full_deck into the deck and shuffle it. This is the only random event in a round.
- Move the top 5 cards face up into out_of_play.
- Deal 1 card to each player's hand. The deck now holds 9 cards.
- Set protected = 0 and eliminated = 0 for both players, stake = 1 and folded = 0.
- The active seat becomes the starter seat. Set new_hand = 0.

2. START OF TURN: set the active player's protected to 0. The active player draws the top card of the deck, so they hold 2 cards.

3. DISCARD (choice, active player): 'Choose one of your two cards to discard.'

4. RESOLVE DISCARD: if the active player holds the Countess together with a King or a Prince, the Countess is discarded whatever was chosen. The card goes onto the player's discards and becomes current_discard. Everyone is told 'Seat X discards CARD'.

5. GUARD GUESS (choice, when current_discard is a Guard and the opponent is not protected): the active player names a rank from 2 to 8. The named rank is announced to both players.

6. GUARD CHECK (when step 5 ran): if the opponent's card has the named rank, the opponent is eliminated and everyone is told 'Hit: CARD'. Otherwise everyone is told 'Miss'.

7. PRIEST (when current_discard is a Priest and the opponent is not protected): only the active player is told the opponent's card.

8. BARON (when current_discard is a Baron and the opponent is not protected): the two hand cards are compared. The holder of the lower rank is eliminated and their card is announced. On equal ranks nothing happens and nothing is revealed.

9. HANDMAID (when current_discard is a Handmaid): the active player becomes protected (until their next turn starts).

10. PRINCE DISCARD (when current_discard is a Prince): the target is the opponent, or the active player if the opponent is protected. The target discards their hand card face up with no effect, and it is announced. If it is the Princess, the target is eliminated.

11. PRINCE REDRAW (when step 10 ran and the target is not eliminated): the target takes the top card of the deck. This may be the reserve if it is the only card left.

12. KING (when current_discard is a King and the opponent is not protected): the two players swap hand cards.

13. PRINCESS (when current_discard is the Princess): the active player is eliminated.

14. RAISE (choice, active player; only when stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least one card in their discards): 'Raise this hand's stake to 2, or pass?'

15. RESPONSE (choice, opponent; when a raise was just made): 'Accept (the stake becomes 2) or fold?' On accept, stake = 2. On fold, folded = 1.

16. HAND END. Apply the first of these that holds:
- (a) If folded = 1, the active player gains 1 point.
- (b) Otherwise, if a player is eliminated, the other player gains points equal to the stake.
- (c) Otherwise, if deck_count <= 1 or this is round 40, there is a showdown. Both hand cards are revealed and the higher rank gains points equal to the stake. On equal ranks nobody scores.
If (a), (b) or (c) applied, set new_hand = 1 and switch the starter seat to the other seat.

17. PASS TURN AND GAME END:
- If new_hand = 1, the active seat becomes the starter seat. Otherwise the opponent becomes the active player.
- After round 40 the game ends.

DECK CHECK: after the deal the deck holds 9 cards. A hand goes to showdown whenever 1 or 0 cards remain at the end of a turn. So every turn starts with at least 2 cards in the deck, the draw always leaves at least the reserve, and a Prince redraw always has a card to take.

How the winner is decided: After exactly 40 rounds (a hand still running in round 40 is settled by showdown in that round), the player with more points wins. Equal points is a draw.
````

## Reply

````
```json
{
  "name": "Love Letter: Short Hands",
  "summary": "Two-player Love Letter over exactly 40 turns: draw, discard a card to use its effect, knock out the rival or win the showdown, and optionally raise a hand's stake to 2.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 16,
    "guard_count": 5, "guard_rank": 1,
    "priest_count": 2, "priest_rank": 2,
    "baron_count": 2, "baron_rank": 3,
    "handmaid_count": 2, "handmaid_rank": 4,
    "prince_count": 2, "prince_rank": 5,
    "king_count": 1, "king_rank": 6,
    "countess_count": 1, "countess_rank": 7,
    "princess_count": 1, "princess_rank": 8,
    "total_rounds": 40,
    "cards_out_of_play": 5,
    "cards_dealt_each": 1,
    "deck_after_deal": 9,
    "base_stake": 1,
    "raised_stake": 2,
    "fold_points": 1,
    "guard_guess_min": 2,
    "guard_guess_max": 8,
    "showdown_deck_threshold": 1,
    "raise_min_deck": 2,
    "starting_points": 0,
    "starting_starter_seat": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Ranks of the cards held: 1 card between turns, 2 during own turn.", "observable": false},
      {"key": "discards", "type": "list", "visible": "public", "initial": [], "meaning": "Ranks this player discarded this hand, in order.", "observable": true},
      {"key": "points", "type": "number", "visible": "public", "initial": 0, "meaning": "Score.", "observable": true},
      {"key": "protected", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if protected by a Handmaid until this player's next turn starts.", "observable": true},
      {"key": "eliminated", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if knocked out of the current hand.", "observable": true}
    ],
    "game": [
      {"key": "full_deck", "type": "list", "visible": "none", "initial": [1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,8], "meaning": "The 16 card ranks, copied into the deck each new hand.", "observable": false},
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Drawable cards in shuffled order, top first, not counting the reserve.", "observable": false},
      {"key": "reserve", "type": "list", "visible": "none", "initial": [], "meaning": "The bottom card of the deck. It is never drawn at the start of a turn. A Prince redraw takes it only when the deck list is empty.", "observable": false},
      {"key": "deck_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Cards left in the deck: length of deck plus length of reserve.", "observable": true},
      {"key": "out_of_play", "type": "list", "visible": "public", "initial": [], "meaning": "The 5 cards set aside face up at the start of each hand.", "observable": true},
      {"key": "stake", "type": "number", "visible": "public", "initial": 1, "meaning": "Points the current hand is worth.", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat taking this turn.", "observable": false},
      {"key": "starter_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that starts the next or current hand.", "observable": false},
      {"key": "round_number", "type": "number", "visible": "public", "initial": 1, "meaning": "Current round (turn), 1 to 40.", "observable": true},
      {"key": "new_hand", "type": "number", "visible": "none", "initial": 1, "meaning": "1 if a new hand must be dealt at the start of this round.", "observable": false},
      {"key": "folded", "type": "number", "visible": "none", "initial": 0, "meaning": "1 if the opponent folded to a raise this turn.", "observable": false},
      {"key": "current_discard", "type": "number", "visible": "none", "initial": 0, "meaning": "Rank discarded this turn.", "observable": false},
      {"key": "guard_guess", "type": "number", "visible": "none", "initial": 0, "meaning": "Rank named with a Guard this turn (0 if none).", "observable": false},
      {"key": "raised", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch: 1 if the active player raised this turn.", "observable": false},
      {"key": "prince_target", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch: seat targeted by a Prince this turn (0 if none).", "observable": false}
    ]
  },
  "setup": [
    "Every player starts with points 0, empty hand and discards, protected 0 and eliminated 0.",
    "Set starter_seat = 1, active_seat = 1, round_number = 1, new_hand = 1 and stake = 1.",
    "No cards are dealt in setup. The first hand is dealt by the NEW HAND step of round 1."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "When new_hand = 1: empty both players' hand and discards. Clear out_of_play. Copy full_deck into deck and shuffle it. Move the top 5 cards of deck into out_of_play (public). Deal 1 card from the top of deck to each player's hand. Move the bottom card of deck into reserve, leaving deck with 8 cards and reserve with 1. Set deck_count = 9, protected = 0 and eliminated = 0 for both players, stake = 1, folded = 0, active_seat = starter_seat and new_hand = 0. Announce out_of_play to everyone."},
    {"action": "update", "who": "active seat", "answer": null, "effect": "Reset guard_guess = 0, raised = 0, prince_target = 0. Set the active player's protected = 0. Move the top card of deck into the active player's hand (never the reserve). Set deck_count = len(deck) + len(reserve)."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand and all public attributes."},
    {"action": "ask", "who": "active seat", "answer": "one rank from the active player's hand (see offers)", "effect": "The chosen rank is held for the next step. Prompt: 'Choose one of your two cards to discard.'"},
    {"action": "update", "who": "active seat", "answer": null, "effect": "If the active hand contains 7 together with 5 or 6, the discarded card is 7 whatever was chosen. Remove that card from the active hand, append it to the active player's discards and set current_discard to it. Announce 'Seat {active_seat} discards {card name}'."},
    {"action": "ask", "who": "active seat", "answer": "a whole number from 2 to 8", "effect": "When current_discard = 1 and the opponent's protected = 0: set guard_guess to the named rank and announce the named rank to both players."},
    {"action": "update", "who": "table", "answer": null, "effect": "When guard_guess >= 2: if the opponent's hand card equals guard_guess, set the opponent's eliminated = 1 and announce 'Hit: {card name}'. Otherwise announce 'Miss'."},
    {"action": "tell", "who": "active seat only", "answer": null, "effect": "When current_discard = 2 and the opponent's protected = 0: privately tell the active player the opponent's hand card."},
    {"action": "update", "who": "table", "answer": null, "effect": "When current_discard = 3 and the opponent's protected = 0: compare the active hand card with the opponent's hand card. The holder of the lower rank gets eliminated = 1 and their card is announced. On equal ranks nothing happens and nothing is revealed."},
    {"action": "update", "who": "active seat", "answer": null, "effect": "When current_discard = 4: set the active player's protected = 1."},
    {"action": "update", "who": "table", "answer": null, "effect": "When current_discard = 5: prince_target = the opponent if the opponent's protected = 0, otherwise the active seat. Move the target's hand card to the target's discards and announce it. If that card is 8, set the target's eliminated = 1."},
    {"action": "update", "who": "prince target", "answer": null, "effect": "When prince_target > 0 and the target's eliminated = 0: move the top card of deck into the target's hand, or the reserve card if deck is empty. Set deck_count = len(deck) + len(reserve)."},
    {"action": "update", "who": "both players", "answer": null, "effect": "When current_discard = 6 and the opponent's protected = 0: swap the active player's hand with the opponent's hand."},
    {"action": "update", "who": "active seat", "answer": null, "effect": "When current_discard = 8: set the active player's eliminated = 1."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own (possibly swapped or redrawn) hand and all public attributes."},
    {"action": "ask", "who": "active seat", "answer": "raise | pass", "effect": "When stake = 1, both players' eliminated = 0, deck_count >= 2 and the opponent's discards has at least 1 card: prompt 'Raise this hand's stake to 2, or pass?' On raise, set raised = 1 and announce the raise."},
    {"action": "ask", "who": "opponent of the active seat", "answer": "accept | fold", "effect": "When raised = 1: prompt 'Accept (the stake becomes 2) or fold?' On accept, set stake = 2. On fold, set folded = 1. Announce the answer."},
    {"action": "update", "who": "table", "answer": null, "effect": "HAND END, first that holds: (a) if folded = 1, the active player's points += 1; (b) else if a player has eliminated = 1, the other player's points += stake; (c) else if deck_count <= 1 or round_number = 40, reveal both hand cards and the higher rank's points += stake, with no score on equal ranks. If (a), (b) or (c) applied, set new_hand = 1 and starter_seat = 3 - starter_seat, and announce the result."},
    {"action": "update", "who": "table", "answer": null, "effect": "If new_hand = 1, set active_seat = starter_seat. Otherwise set active_seat = 3 - active_seat. Then round_number += 1."},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game if round_number > 40, otherwise continue."}
  ],
  "ending": {
    "condition": "round_number > 40",
    "rank_by": "you.points",
    "decided_by": "After exactly 40 rounds, the player with more points wins. Equal points share the win, which is the draw."
  },
  "rules": [
    {"id": "R1", "text": "When a new hand starts, the 16-card deck (5 Guard, 2 Priest, 2 Baron, 2 Handmaid, 2 Prince, 1 King, 1 Countess, 1 Princess) is shuffled, 5 cards go face up to out_of_play, each player gets 1 card, and deck_count = 9."},
    {"id": "R2", "text": "When a new hand starts, both players' discards are emptied, protected = 0, eliminated = 0, stake = 1, and the active seat becomes the starter seat."},
    {"id": "R3", "text": "When a turn starts, the active player's protected becomes 0 and they draw the top card, holding 2 cards, and deck_count falls by 1."},
    {"id": "R4", "text": "The bottom (reserve) card is never drawn at the start of a turn."},
    {"id": "R5", "text": "When the active player chooses a discard, that card moves from their hand to their discards and is announced as 'Seat X discards CARD'."},
    {"id": "R6", "text": "When the active player holds the Countess (7) with a King (6) or Prince (5), the Countess is discarded whatever was chosen."},
    {"id": "R7", "text": "When a Guard (1) is discarded and the opponent is not protected, the active player names a rank from 2 to 8, which is announced."},
    {"id": "R8", "text": "When the named Guard rank equals the opponent's card, the opponent is eliminated and 'Hit: CARD' is announced; otherwise 'Miss' is announced."},
    {"id": "R9", "text": "When a Priest (2) is discarded and the opponent is not protected, only the active player is told the opponent's card."},
    {"id": "R10", "text": "When a Baron (3) is discarded and the opponent is not protected, the lower hand card's holder is eliminated and their card announced; on equal ranks nothing happens and nothing is revealed."},
    {"id": "R11", "text": "When a Handmaid (4) is discarded, the active player's protected becomes 1 until their next turn starts."},
    {"id": "R12", "text": "When a Prince (5) is discarded, the opponent (or the active player if the opponent is protected) discards their hand card face up with no effect, and it is announced."},
    {"id": "R13", "text": "When a Prince makes a player discard the Princess (8), that player is eliminated."},
    {"id": "R14", "text": "When a Prince target is not eliminated, they draw the top card, taking the reserve only if it is the last card."},
    {"id": "R15", "text": "When a King (6) is discarded and the opponent is not protected, the two players swap hand cards."},
    {"id": "R16", "text": "When the Princess (8) is discarded, the active player is eliminated."},
    {"id": "R17", "text": "Cards targeting the opponent (Guard, Priest, Baron, King) have no effect when the opponent's protected = 1."},
    {"id": "R18", "text": "When stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least 1 discard, the active player may raise or pass."},
    {"id": "R19", "text": "When the active player raises, the opponent accepts (stake = 2) or folds (folded = 1)."},
    {"id": "R20", "text": "When the opponent folds, the active player gains 1 point and the hand ends."},
    {"id": "R21", "text": "When a player is eliminated and nobody folded, the other player gains points equal to the stake and the hand ends."},
    {"id": "R22", "text": "When nobody folded or was eliminated and deck_count <= 1 or it is round 40, both cards are revealed and the higher rank gains the stake; equal ranks score nothing."},
    {"id": "R23", "text": "When a hand ends, the starter seat switches and the new starter takes the next turn; otherwise the turn passes to the opponent."},
    {"id": "R24", "text": "After round 40 the game ends and the player with more points wins; equal points is a draw."}
  ],
  "offers": [
    {"question": "Choose one of your two cards to discard", "who": "active seat", "options": "Holding 7 together with 5 or 6: only 7. Otherwise: either of the two ranks in hand (one option if both are equal)."},
    {"question": "Guard guess", "who": "active seat, only when a Guard was discarded and the opponent is not protected", "options": "a whole number 2 to 8"},
    {"question": "Raise this hand's stake to 2, or pass?", "who": "active seat, only when stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least 1 discard", "options": "raise, pass"},
    {"question": "Accept (the stake becomes 2) or fold?", "who": "the opponent, only right after a raise", "options": "accept, fold"}
  ],
  "choices": [
    {"what": "2 players (min 2, max 2)", "why": "The designer fixed the table at 2. Every effect (Guard, Baron, King, the raise and fold) targets 'the opponent', so more seats would break the rules."},
    {"what": "No free talk step", "why": "The source has none. The raise and fold already carry the bluffing signal."},
    {"what": "Countess forcing is shown in the offer as well as enforced in the resolve step", "why": "A seat is never offered what it may not do. The outcome is the same as the source's override."},
    {"what": "Strategy at the table", "why": "Players track the out_of_play cards and both discard piles to make good Guard guesses, time Baron and King plays, and raise as a bluff or with a strong card."}
  ],
  "simplifications": [
    {"what": "Cards are stored as their ranks (1 to 8) and named in announcements", "why": "The Guard check, Baron comparison and showdown are then plain arithmetic."},
    {"what": "The reserve is kept in its own hidden list instead of at the bottom of the deck", "why": "The engine draws from a list, so separating it guarantees the turn-start draw never takes it. deck_count adds both lists."},
    {"what": "The Guard guess and Guard check are tracked with guard_guess > 0 instead of 'step 5 ran'; the Prince redraw uses prince_target", "why": "A step's 'when' must be an arithmetic condition on state."}
  ],
  "unsupported": []
}
```
````
