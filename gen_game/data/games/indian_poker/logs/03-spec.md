# 03 spec

- time: 2026-10-28T01:33:50+00:00 (52.2s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 2b40e19bba98d563, reply sha256 530bb4656ab07db9

## Sent

````
Game: Forehead Poker Match
Players in the source: 4 to 6
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP: Each player starts with 40 chips. The pot starts at 0. The match lasts 16 hands.

CARD STRENGTH: A standard 52-card deck is used. Rank from high to low is A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2. Between equal ranks, suit decides, from high to low: Spades, Hearts, Diamonds, Clubs. No two cards are ever equal.

EACH HAND:
1. ELIGIBILITY: Any active player with fewer than 4 chips is eliminated. They take no further part, and their current chips are their final total.
2. DEAL: The full deck is shuffled and one card is dealt to each active player. Each player is privately told the card of every other active player, but never their own.
3. ANTE: Each active player pays 1 chip into the pot.
4. TALK: Every active player writes one short message (at most 40 words) at the same moment, without seeing the others. All messages are then shown to everyone. Messages may say anything, including claims about anyone's card, and none of them binds anyone.
5. FIRST BET: Every active player, at the same moment, chooses one option: Fold, Bet 1, Bet 2 or Bet 3. A player who bets pays that many chips into the pot immediately. A player who folds is out of this hand and has lost only the ante.
6. REVEAL BETS: Every player's choice from step 5 is shown to everyone. Let H be the highest bet made.
7. CALL OR FOLD: Every player who bet in step 5, at the same moment, chooses Call or Fold. Calling costs H minus that player's own step-5 bet, paid into the pot. A player whose bet was already H calls for free. Folding forfeits everything that player has put in this hand.
8. SHOWDOWN: Find the players who called.
   - Two or more callers: their cards are compared, and the caller with the strongest card wins the whole pot.
   - Exactly one caller: that player wins the whole pot without comparison.
   - No callers: the pot stays and carries over to the next hand.
   All cards are then revealed to everyone, so players can check what was said and bet.
9. Winnings are added to the winner's chips, the pot resets to 0 (unless it carried over), and the next hand begins.

END: The match ends after hand 16, or earlier if only one player is still active. Any pot remaining at that moment is discarded.

How the winner is decided: The player with the most chips at the end of the match wins. Eliminated players count with the chips they held when eliminated. If two or more players tie for the most chips, the game is a draw among them.
````

## Reply

````
```json
{
  "name": "Forehead Poker Match",
  "summary": "Over 16 hands, each player sees every other player's card but never their own, talks, bets and calls; the player with the most chips at the end wins.",
  "players": {"min": 4, "max": 6, "suggested": 4},
  "parameters": {
    "starting_chips": 40,
    "starting_pot": 0,
    "hands": 16,
    "elimination_below": 4,
    "ante": 1,
    "bet_min": 1,
    "bet_max": 3,
    "message_max_words": 40,
    "deck_size": 52,
    "cards_per_player": 1,
    "suits_per_rank": 4
  },
  "attributes": {
    "player": [
      {"key": "chips", "type": "number", "visible": "public", "initial": 40, "meaning": "The player's chip stack. This is the score. It freezes when the player is eliminated.", "observable": true},
      {"key": "active", "type": "bool", "visible": "public", "initial": true, "meaning": "Whether the player is still in the match. It becomes false when the player starts a hand with fewer than 4 chips.", "observable": true},
      {"key": "card", "type": "text", "visible": "others", "initial": "", "meaning": "The card dealt this hand, such as 'Q of Hearts'. Every other player sees it; the owner does not.", "observable": false},
      {"key": "card_value", "type": "number", "visible": "others", "initial": 0, "meaning": "The card's strength from 1 (2 of Clubs) to 52 (A of Spades), worked out as rank_index*4 + suit_index. rank_index runs 0 for 2 up to 12 for A. suit_index is Clubs 1, Diamonds 2, Hearts 3, Spades 4. It is 0 when no card is held.", "observable": false},
      {"key": "bet", "type": "number", "visible": "public", "initial": 0, "meaning": "The step-5 bet this hand: 0 for a fold, otherwise 1 to 3.", "observable": false},
      {"key": "folded", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the player folded in step 5 or step 7 of this hand.", "observable": false},
      {"key": "called", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the player called in step 7 of this hand.", "observable": false},
      {"key": "shown_card", "type": "text", "visible": "public", "initial": "", "meaning": "The player's card, revealed to everyone after the showdown. It is empty before then.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "the 52 standard cards", "meaning": "The shuffled deck that cards are dealt from. It is refilled to all 52 cards every hand.", "observable": false},
      {"key": "pot", "type": "number", "visible": "public", "initial": 0, "meaning": "The chips in the pot. It carries over when nobody calls.", "observable": true},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 0, "meaning": "The number of hands completed so far.", "observable": true},
      {"key": "high_bet", "type": "number", "visible": "public", "initial": 0, "meaning": "H, the highest step-5 bet this hand. It is 0 if everyone folded.", "observable": false},
      {"key": "caller_count", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players called in step 7.", "observable": false},
      {"key": "best_value", "type": "number", "visible": "none", "initial": 0, "meaning": "The highest card_value among this hand's callers. It is 0 if there are no callers.", "observable": false}
    ]
  },
  "setup": [
    "Each player gets 40 chips and is marked active.",
    "The pot is set to 0 and hand_number to 0.",
    "The deck list is filled with the 52 standard cards."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "ELIGIBILITY: every active player with chips < 4 gets active = false, and their chips stay as their final total. Then every player is reset for the hand: bet = 0, folded = false, called = false, card = '', card_value = 0, shown_card = ''. On the table, high_bet, caller_count and best_value are set to 0."},
    {"action": "check", "who": "all players", "answer": null, "effect": "The game ends if the number of players with active = true is 1 or fewer. Any pot is discarded."},
    {"action": "update", "who": "all players", "answer": null, "effect": "DEAL: deck is reset to all 52 cards. Each active player draws one card at random: it is removed from deck and its name is set as card, with its strength as card_value."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player is sent their state. They see the card and card_value of every other active player, but not their own."},
    {"action": "update", "who": "all players", "answer": null, "effect": "ANTE: each active player pays 1: chips -= 1 and pot += 1."},
    {"action": "poll", "who": "every active player", "answer": "short text, at most 40 words", "effect": "TALK: once every message is in, each one is broadcast to all as 'Seat {seat} says: {value}'. No message binds anyone."},
    {"action": "poll", "who": "every active player", "answer": "one of: Fold, Bet 1, Bet 2, Bet 3", "effect": "FIRST BET: answers are collected simultaneously and stored. Nothing is shown until all are in."},
    {"action": "update", "who": "every active player", "answer": null, "effect": "On Fold: bet = 0 and folded = true. On Bet k: bet = k, chips -= k and pot += k. Then high_bet = the largest bet among active players."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "REVEAL BETS: every player's step-5 choice (bet or fold) and H = high_bet are announced to everyone."},
    {"action": "poll", "who": "every active player with bet >= 1", "answer": "one of: Call, Fold", "effect": "CALL OR FOLD: answers are collected simultaneously. This step is skipped if nobody bet."},
    {"action": "update", "who": "every player asked in the previous step", "answer": null, "effect": "On Call: called = true, chips -= (high_bet - bet) and pot += (high_bet - bet); the cost is 0 if bet = high_bet. On Fold: folded = true, and nothing put in this hand is returned. Then caller_count = the number of players with called = true, and best_value = the highest card_value among players with called = true (0 if there are none)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "SHOWDOWN: if caller_count >= 1, the player with called = true and card_value = best_value gets chips += pot, and then pot = 0. If caller_count = 0, pot is unchanged and carries over. Every player who was dealt a card gets shown_card = card. Then hand_number += 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "All cards (shown_card), the callers, the winner of the pot (or that it carried over), the pot and everyone's chips are announced."},
    {"action": "check", "who": "all players", "answer": null, "effect": "The game ends if hand_number >= 16 or the number of players with active = true is 1 or fewer. Any remaining pot is discarded."}
  ],
  "ending": {
    "condition": "hand_number >= 16 or (count of players with active = true) <= 1",
    "rank_by": "you.chips",
    "decided_by": "Each player's standing is their chips at the end. Eliminated players count with the chips they held when eliminated. The most chips wins, and players tied for the most share a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the match starts, then each player has 40 chips, the pot is 0 and hand_number is 0."},
    {"id": "R2", "text": "When a hand begins and an active player has fewer than 4 chips, then that player becomes inactive, takes no further part, and keeps those chips as their final total."},
    {"id": "R3", "text": "When a hand begins and an active player has 4 or more chips, then that player stays active."},
    {"id": "R4", "text": "When a hand is dealt, then the deck is refilled to 52 cards and each active player receives exactly one card, removed from the deck."},
    {"id": "R5", "text": "When cards are dealt, then each player can see the card of every other active player but never their own."},
    {"id": "R6", "text": "When cards are compared, then rank decides first (A high, 2 low) and suit breaks ties (Spades > Hearts > Diamonds > Clubs), so the A of Spades is strongest and the 2 of Clubs weakest."},
    {"id": "R7", "text": "When the ante is taken, then each active player loses 1 chip and the pot grows by 1 per active player."},
    {"id": "R8", "text": "When talk happens, then every active player submits one message of at most 40 words simultaneously, and all messages are then shown to everyone."},
    {"id": "R9", "text": "When a player chooses Bet k (k = 1, 2 or 3) in the first bet, then their chips fall by k and the pot rises by k immediately."},
    {"id": "R10", "text": "When a player folds in the first bet, then they are out of the hand, have lost only the 1-chip ante, and are not asked to call."},
    {"id": "R11", "text": "When all first bets are in, then every choice is revealed to everyone and H is the highest bet made."},
    {"id": "R12", "text": "When a player who bet b calls, then they pay H - b chips into the pot, which is 0 if b = H."},
    {"id": "R13", "text": "When a player who bet folds at the call step, then they forfeit everything they put in this hand and nothing is returned."},
    {"id": "R14", "text": "When two or more players call, then the caller with the highest card strength wins the whole pot and the pot becomes 0."},
    {"id": "R15", "text": "When exactly one player calls, then that player wins the whole pot without comparison and the pot becomes 0."},
    {"id": "R16", "text": "When no player calls (including when everyone folded in the first bet), then the pot stays and carries over to the next hand."},
    {"id": "R17", "text": "When the showdown ends, then every dealt card is revealed to everyone."},
    {"id": "R18", "text": "When 16 hands have been completed, then the match ends and any remaining pot is discarded."},
    {"id": "R19", "text": "When only one or no player is active, then the match ends early and any remaining pot is discarded."},
    {"id": "R20", "text": "When the match ends, then the player with the most chips wins, eliminated players count with their chips at elimination, and players tied for the most share a draw."}
  ],
  "offers": [
    {"question": "TALK message", "who": "every active player", "options": "free text of at most 40 words. Eliminated players are not asked."},
    {"question": "FIRST BET", "who": "every active player", "options": "Fold, Bet 1, Bet 2, Bet 3 (every active player has at least 3 chips after the ante, so all four are always affordable). Eliminated players are not asked."},
    {"question": "CALL OR FOLD", "who": "every active player whose step-5 bet was 1, 2 or 3", "options": "Call, Fold. Players who folded in step 5 and eliminated players are not asked."}
  ],
  "choices": [
    {"what": "4 to 6 players, suggested 4", "why": "Kept from the source and the designer. Four is the smallest table where several opponents' cards give real information about your own and where there are rivals to bluff. Above 6, each player's card information and message get lost in a long conversation."},
    {"what": "Talk kept as a simultaneous poll broadcast to all", "why": "The rules require simultaneous messages. Talk earns its place: each player knows facts the others need (their cards) and has reason to lie about them, so following a claim can cost chips."},
    {"what": "Card strength encoded as a number from 1 to 52 (rank_index*4 + suit_index)", "why": "This lets the showdown winner be found by arithmetic (the highest card_value among callers) and exactly matches the rank-then-suit order in the rules."},
    {"what": "Eligibility check and early-end check placed at the start of each round, with a further end check after the showdown", "why": "Elimination happens at the start of a hand. Checking right after it stops a hand being played with a single active player."},
    {"what": "Strategy at the table", "why": "A thoughtful player infers their own card from the others' cards, their messages and their bets, and decides when to bluff, mislead others about their cards, or fold cheaply. A thoughtless player bets blindly."}
  ],
  "simplifications": [
    {"what": "Shuffling the full deck each hand is done by resetting the deck list to 52 cards and drawing at random", "why": "The engine has no shuffle; drawing at random from a full list is equivalent."},
    {"what": "The discarded leftover pot is simply ignored at the end", "why": "It does not affect anyone's chips or the ranking."}
  ],
  "unsupported": []
}
```
````
