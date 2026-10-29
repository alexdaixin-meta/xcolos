# 03 spec

- time: 2026-10-28T02:19:38+00:00 (84.3s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 6fa1ba702159524a, reply sha256 987063f8cc7ff82b

## Sent

````
Game: Officers' Schafkopf: Bidding Match
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
DECK. There are 16 cards: Ace, Ten, Ober and Unter in each of four suits (Acorns, Leaves, Hearts, Bells). Card points are Ace 11, Ten 10, Ober 3 and Unter 2, which makes 104 in the deck.

MATCH. The match is 4 hands. Each hand is one bidding round followed by 8 trick rounds, which makes 36 rounds in total. Player 1 deals hands 1 and 3 and Player 2 deals hands 2 and 4. The non-dealer is called forehand.

DEAL (start of each hand's bidding round, the only random event of the round). Shuffle the 16 cards. Each player receives:
- 4 private hand cards, seen only by their owner;
- 2 stacks, each made of one face-down card under one face-up card.
The face-up cards (4 in total) are visible to both players. Face-down cards are unknown to both players, including their owner.

BIDDING ROUND.
(1) Both players secretly and simultaneously choose a bid: Pass, 53, 66 or 79. The bid is the number of card points the player promises to take as declarer.
(2) The higher bid becomes declarer at that bid. If the bids are equal and not Pass, forehand is declarer at that bid. If both pass, forehand is declarer at 53. Both bids are then announced.
(3) The declarer chooses a contract and it is announced:
- Acorns Solo, Leaves Solo, Hearts Solo or Bells Solo: trumps are, from highest to lowest, Ober of Acorns, Ober of Leaves, Ober of Hearts, Ober of Bells, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells, then the Ace and the Ten of the chosen suit. The three other suits each hold only Ace above Ten.
- Wenz: trumps are, from highest to lowest, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells. Each suit holds Ace above Ten above Ober.
(4) The defender chooses Stoß (double) or No Stoß, and the choice is announced. The multiplier is 2 with Stoß and 1 without.

TRICK ROUNDS (8 per hand).
Available cards: a player may play any of their private hand cards or any face-up card on top of one of their stacks.
Lead: in the first trick forehand leads; afterwards the winner of the previous trick leads. The leader plays one available card.
Follow: the other player then plays one available card. All trumps count as one suit, the trump suit, so in a Solo an Ober or Unter is never a card of its printed suit. If the follower has an available card of the led suit, they must play one. Otherwise they may play any available card.
Trick winner: if any trump was played, the higher trump wins. Otherwise the higher card of the led suit wins. The winner adds the card points of both cards to their card-point total for this hand.
Reveal: after the trick, any face-down card whose face-up card was played this trick is turned face up. It is available from the next trick on.

HAND SCORING (after trick 8).
- If the declarer's card points are at least their bid, the declarer scores the contract value in match points. Otherwise the defender scores it.
- Contract value = base, plus 1 if the player who scores took all 8 tricks, multiplied by the Stoß multiplier.
- The base is 2 for a bid of 53, 3 for a bid of 66 and 4 for a bid of 79.
Each player's card points for the hand are also added to their running card-point total for the match. Then all cards are collected for the next deal.

How the winner is decided: After 4 hands, the player with more match points wins. If match points are equal, the player with the higher total card points over all 4 hands wins. If both are equal, the match is a draw.
````

## Reply

````
```json
{
  "name": "Officers' Schafkopf: Bidding Match",
  "summary": "A two-player Schafkopf match of 4 hands with a 16-card deck, open and face-down stacks, sealed bids for the declarer's contract, an optional Stoß, and 8 tricks per hand. Match points decide the winner, total card points break ties.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 16,
    "points_ace": 11,
    "points_ten": 10,
    "points_ober": 3,
    "points_unter": 2,
    "deck_points": 104,
    "hands_in_match": 4,
    "tricks_per_hand": 8,
    "rounds_per_hand": 9,
    "total_rounds": 36,
    "private_cards_per_player": 4,
    "stacks_per_player": 2,
    "face_up_cards_on_table": 4,
    "bid_pass": 0,
    "bid_low": 53,
    "bid_mid": 66,
    "bid_high": 79,
    "default_bid_when_both_pass": 53,
    "base_for_53": 2,
    "base_for_66": 3,
    "base_for_79": 4,
    "all_tricks_bonus": 1,
    "multiplier_stoss": 2,
    "multiplier_no_stoss": 1,
    "trump_strength_ober_acorns": 20,
    "trump_strength_ober_leaves": 19,
    "trump_strength_ober_hearts": 18,
    "trump_strength_ober_bells": 17,
    "trump_strength_unter_acorns": 16,
    "trump_strength_unter_leaves": 15,
    "trump_strength_unter_hearts": 14,
    "trump_strength_unter_bells": 13,
    "trump_strength_solo_suit_ace": 12,
    "trump_strength_solo_suit_ten": 11,
    "plain_rank_ace": 3,
    "plain_rank_ten": 2,
    "plain_rank_ober": 1,
    "plain_rank_unter": 0,
    "rank_weight_match_points": 1000
  },
  "attributes": {
    "player": [
      {"key": "match_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Match points won so far.", "observable": true},
      {"key": "card_total", "type": "number", "visible": "public", "initial": 0, "meaning": "Running card-point total over all completed hands, used as the tie-break.", "observable": true},
      {"key": "hand_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Card points taken in tricks during the current hand.", "observable": false},
      {"key": "tricks_won", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won in the current hand.", "observable": false},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The 4 private hand cards, seen only by their owner.", "observable": false},
      {"key": "stack1_up", "type": "text", "visible": "public", "initial": "", "meaning": "Face-up card on top of stack 1 (empty when none).", "observable": false},
      {"key": "stack2_up", "type": "text", "visible": "public", "initial": "", "meaning": "Face-up card on top of stack 2 (empty when none).", "observable": false},
      {"key": "stack1_pending_reveal", "type": "bool", "visible": "public", "initial": false, "meaning": "True once stack 1's face-up card has been played this trick, so the card beneath it turns up after the trick.", "observable": false},
      {"key": "stack2_pending_reveal", "type": "bool", "visible": "public", "initial": false, "meaning": "The same for stack 2.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "This hand's bid (0 = Pass, or 53, 66, 79). It is collected by a sealed poll and announced after both bids are in.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["Ace of Acorns","Ten of Acorns","Ober of Acorns","Unter of Acorns","Ace of Leaves","Ten of Leaves","Ober of Leaves","Unter of Leaves","Ace of Hearts","Ten of Hearts","Ober of Hearts","Unter of Hearts","Ace of Bells","Ten of Bells","Ober of Bells","Unter of Bells"], "meaning": "The undealt cards.", "observable": false},
      {"key": "seat1_stack1_down", "type": "text", "visible": "none", "initial": "", "meaning": "Face-down card under seat 1's stack 1, unknown to both players.", "observable": false},
      {"key": "seat1_stack2_down", "type": "text", "visible": "none", "initial": "", "meaning": "Face-down card under seat 1's stack 2.", "observable": false},
      {"key": "seat2_stack1_down", "type": "text", "visible": "none", "initial": "", "meaning": "Face-down card under seat 2's stack 1.", "observable": false},
      {"key": "seat2_stack2_down", "type": "text", "visible": "none", "initial": "", "meaning": "Face-down card under seat 2's stack 2.", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current hand, from 1 to 4.", "observable": true},
      {"key": "round_in_hand", "type": "number", "visible": "public", "initial": 0, "meaning": "0 = bidding round; 1 to 8 = trick number.", "observable": false},
      {"key": "rounds_played", "type": "number", "visible": "public", "initial": 0, "meaning": "Rounds completed, out of 36.", "observable": false},
      {"key": "dealer", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat dealing this hand: seat 1 in hands 1 and 3, seat 2 in hands 2 and 4.", "observable": false},
      {"key": "forehand", "type": "number", "visible": "public", "initial": 2, "meaning": "The non-dealer.", "observable": false},
      {"key": "declarer", "type": "number", "visible": "public", "initial": 0, "meaning": "Declarer's seat this hand.", "observable": true},
      {"key": "defender", "type": "number", "visible": "public", "initial": 0, "meaning": "Defender's seat this hand.", "observable": false},
      {"key": "contract_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "The card points the declarer must reach (53, 66 or 79).", "observable": true},
      {"key": "contract", "type": "text", "visible": "public", "initial": "", "meaning": "Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo or Wenz.", "observable": true},
      {"key": "multiplier", "type": "number", "visible": "public", "initial": 1, "meaning": "2 with Stoß, 1 without.", "observable": true},
      {"key": "leader", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that leads the current trick.", "observable": false},
      {"key": "follower", "type": "number", "visible": "public", "initial": 0, "meaning": "The other seat.", "observable": false},
      {"key": "led_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card led to the current trick.", "observable": false},
      {"key": "followed_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card played second to the current trick.", "observable": false},
      {"key": "follow_options", "type": "list", "visible": "public", "initial": [], "meaning": "Legal cards for the follower, worked out by the follow-suit rule.", "observable": false}
    ]
  },
  "setup": [
    "Set hand_number to 1, round_in_hand to 0, rounds_played to 0, and each player's match_points and card_total to 0.",
    "Seat 1 is dealer for hand 1, so seat 2 is forehand."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand == 0 (the deal):\n- Set dealer = 1 if hand_number is odd, else 2, and set forehand to the other seat.\n- Refill deck with all 16 cards.\n- For each seat, draw 4 random cards from deck into hand, then 1 into stack1_up, 1 into the seat's stack1_down table attribute, 1 into stack2_up, and 1 into the seat's stack2_down table attribute.\n- Reset hand_points, tricks_won, bid and the pending_reveal flags.\n- Reset contract, multiplier = 1, declarer = 0 and defender = 0."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand, all four face-up stack cards, and the public table state."},
    {"action": "poll", "who": "all players", "answer": "one of: Pass, 53, 66, 79", "effect": "When round_in_hand == 0: each player's bid is set to their answer (Pass = 0). No one sees a bid until both are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand == 0, set declarer and contract_bid as follows:\n- If one bid is higher, that seat is declarer and contract_bid is that bid.\n- If the bids are equal and above 0, forehand is declarer at that bid.\n- If both bids are 0, forehand is declarer with contract_bid = 53.\nThen defender = the other seat. Both bids, the declarer and contract_bid are announced."},
    {"action": "ask", "who": "the seat in declarer", "answer": "one of: Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo, Wenz", "effect": "When round_in_hand == 0: contract is set to the answer and announced."},
    {"action": "ask", "who": "the seat in defender", "answer": "one of: Stoß, No Stoß", "effect": "When round_in_hand == 0: multiplier = 2 if Stoß, else 1. The choice is announced. Then leader = forehand and follower = dealer."},
    {"action": "ask", "who": "the seat in leader", "answer": "one card from that seat's hand plus its non-empty stack1_up and stack2_up", "effect": "When round_in_hand >= 1: led_card is set to the answer and announced. The card is removed from hand. If it was stack1_up or stack2_up, that attribute becomes empty and the matching pending_reveal flag is set to true."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand >= 1, build follow_options:\n- Take the follower's available cards (hand plus non-empty stack ups) whose effective suit under contract equals the effective suit of led_card.\n- If there are none, take all of the follower's available cards.\nEffective suit is 'Trump' if the card's trump_strength is above 0, otherwise its printed suit."},
    {"action": "ask", "who": "the seat in follower", "answer": "one card from follow_options", "effect": "When round_in_hand >= 1: followed_card is set to the answer and announced. The card is removed from hand or from its stack up, and the matching pending_reveal flag is set to true when it came from a stack."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand >= 1, decide the trick winner from trump_strength and plain_rank under contract:\n- If either card has trump_strength > 0, the card with the higher trump_strength wins.\n- Otherwise, if followed_card's printed suit equals led_card's suit, the higher plain_rank wins.\n- Otherwise the leader wins.\nThe winner adds the card points of both cards to hand_points and adds 1 to tricks_won. Set leader = winner and follower = the other seat. For every stack whose pending_reveal is true, move the matching face-down table card into that stack's up attribute and clear the flag. Announce the trick result."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand == 8 (hand scoring):\n- Let base = 2 if contract_bid == 53, 3 if 66, 4 if 79.\n- The scorer is the declarer if the declarer's hand_points >= contract_bid, otherwise the defender.\n- The scorer's match_points increase by (base + (1 if the scorer's tricks_won == 8 else 0)) * multiplier.\n- Each player's card_total increases by their hand_points.\nAnnounce the result."},
    {"action": "update", "who": "all players", "answer": null, "effect": "rounds_played += 1. If round_in_hand == 8, then round_in_hand = 0 and hand_number += 1; otherwise round_in_hand += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if rounds_played >= 36; otherwise continue."}
  ],
  "ending": {
    "condition": "game.rounds_played >= 36",
    "rank_by": "you.match_points * 1000 + you.card_total",
    "decided_by": "After 4 hands, the player with more match points wins. If match points are equal, the higher total card points over all 4 hands wins. If both are equal, the two players share the result, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "The deck has 16 cards: Ace, Ten, Ober and Unter of Acorns, Leaves, Hearts and Bells. Card points are Ace 11, Ten 10, Ober 3, Unter 2, totalling 104."},
    {"id": "R2", "text": "The match is 4 hands of 9 rounds each (1 bidding round, then 8 trick rounds), 36 rounds in all."},
    {"id": "R3", "text": "Seat 1 deals hands 1 and 3 and seat 2 deals hands 2 and 4. The non-dealer is forehand."},
    {"id": "R4", "text": "At the start of each hand all 16 cards are shuffled. Each player gets 4 private hand cards plus 2 stacks of one face-down card under one face-up card."},
    {"id": "R5", "text": "Hand cards are visible only to their owner, face-up stack cards to both players, and face-down cards to neither player."},
    {"id": "R6", "text": "Both players bid secretly and simultaneously: Pass, 53, 66 or 79."},
    {"id": "R7", "text": "When the bids differ, the higher bidder is declarer at their bid."},
    {"id": "R8", "text": "When both bid the same number (not Pass), forehand is declarer at that bid."},
    {"id": "R9", "text": "When both pass, forehand is declarer at 53."},
    {"id": "R10", "text": "Both bids are announced after the declarer is determined."},
    {"id": "R11", "text": "The declarer chooses Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo or Wenz, and the choice is announced."},
    {"id": "R12", "text": "In a Solo the trumps, from highest to lowest, are: Ober of Acorns, Leaves, Hearts, Bells; then Unter of Acorns, Leaves, Hearts, Bells; then the Ace and Ten of the chosen suit. Each other suit holds only Ace above Ten."},
    {"id": "R13", "text": "In Wenz the trumps, from highest to lowest, are Unter of Acorns, Leaves, Hearts, Bells. Each suit holds Ace above Ten above Ober."},
    {"id": "R14", "text": "The defender chooses Stoß (multiplier 2) or No Stoß (multiplier 1), and the choice is announced."},
    {"id": "R15", "text": "A player's available cards are their private hand cards plus the face-up card on top of each of their stacks."},
    {"id": "R16", "text": "In trick 1 forehand leads. In each later trick the previous trick's winner leads."},
    {"id": "R17", "text": "All trumps form one suit, so in a Solo an Ober or Unter never counts as its printed suit, and in Wenz an Unter never counts as its printed suit."},
    {"id": "R18", "text": "When the follower has an available card of the led suit, they must play one. Otherwise they may play any available card."},
    {"id": "R19", "text": "When any trump is played, the higher trump wins the trick. Otherwise the higher card of the led suit wins."},
    {"id": "R20", "text": "The trick winner adds the card points of both cards to their hand_points and 1 to tricks_won."},
    {"id": "R21", "text": "After a trick, the face-down card under any face-up card played in that trick turns face up and is available from the next trick on."},
    {"id": "R22", "text": "After trick 8, if the declarer's hand_points are at least contract_bid, the declarer scores the contract value in match points. Otherwise the defender scores it."},
    {"id": "R23", "text": "The contract value is (base + 1 if the scorer took all 8 tricks) times the multiplier, where the base is 2 for 53, 3 for 66 and 4 for 79. For example, a 66 bid made with Stoß and not every trick scores 6."},
    {"id": "R24", "text": "After each hand, each player's hand_points are added to their card_total."},
    {"id": "R25", "text": "After 36 rounds the game ends. More match points wins, card_total breaks ties, and if both are equal the match is a draw."}
  ],
  "offers": [
    {"question": "Bid (poll, bidding round)", "who": "both seats", "options": "Pass, 53, 66, 79"},
    {"question": "Contract", "who": "the declarer only", "options": "Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo, Wenz"},
    {"question": "Stoß", "who": "the defender only", "options": "Stoß, No Stoß"},
    {"question": "Lead a card", "who": "the leader only", "options": "every card in the leader's hand plus each non-empty face-up stack card of theirs"},
    {"question": "Follow a card", "who": "the follower only", "options": "if the follower has an available card of the led card's effective suit (trump counts as one suit), only those cards; otherwise every available card (hand plus non-empty face-up stack cards)"}
  ],
  "choices": [
    {"what": "2 players (min, max and suggested)", "why": "The designer set 2. The deal uses all 16 cards for exactly two players, so neither more nor fewer seats fit."},
    {"what": "Strategy check", "why": "A thoughtful player judges their hand plus the open stack cards before bidding high, picks the contract that fits their trumps, gives Stoß only when the declarer looks overstretched, and times the playing of stack cards to unlock the hidden cards beneath."},
    {"what": "No free-text talk step", "why": "Talk is not part of the rules, and with two opponents it only adds words."},
    {"what": "Pass is stored as bid 0", "why": "This makes 'higher bid' a numeric comparison."},
    {"what": "Trump ranks encoded as trump_strength 20 down to 11, and plain ranks as Ace 3, Ten 2, Ober 1", "why": "This lets the trick winner be decided by arithmetic while keeping exactly the source's order."},
    {"what": "rank_by = match_points * 1000 + card_total", "why": "Card totals can never reach 1000 (at most 416), so match points come first and card points only break ties. An exact tie is a shared result, which matches the source's draw."},
    {"what": "Trick card points and trick counts are public", "why": "Both players see every played card, so these totals are open information."}
  ],
  "simplifications": [
    {"what": "The bidding steps and the trick steps share one flat round list, each step gated by a 'when' condition on round_in_hand", "why": "The engine runs one round script. Per-step arithmetic conditions keep 36 rounds exactly as the source counts them."},
    {"what": "Hand scoring runs as an update at the end of trick round 8", "why": "This keeps the round count at 36 without adding a separate scoring round."},
    {"what": "Face-down stack cards are held as hidden table attributes rather than player attributes", "why": "Not even their owner may see them, and a player attribute cannot be hidden from its owner."}
  ],
  "unsupported": []
}
```
````
