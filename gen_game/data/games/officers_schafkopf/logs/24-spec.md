# 24 spec

- time: 2026-10-28T02:53:28+00:00 (68.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 95c64eceb301b5c1, reply sha256 741056e3b13508e2

## Sent

````
Game: Blind Officers' Schafkopf
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. There are 24 cards in four suits: Acorns, Leaves, Hearts, Bells. Each suit has Ace (11 card points), Ten (10), King (4), Ober (3), Unter (2) and Nine (0). The deck holds 120 card points.

MATCH. The match is four hands of 8 tricks each, one trick per round: 32 rounds. Both players start with 0 match points. Seat 1 has priority in hands 1 and 3. Seat 2 has priority in hands 2 and 4.

START OF EACH HAND (first round of the hand only).
1) Shuffle and deal 8 cards face down to each player. Each player sees only their own cards. The remaining 8 cards form the Blind. They are never seen by anyone, never played and never scored.
2) Sealed bid. Both players choose at the same moment exactly one of these eleven options:
- Pass;
- Wenz-Simple;
- Acorns-Simple;
- Leaves-Simple;
- Hearts-Simple;
- Bells-Simple;
- Wenz-Strong;
- Acorns-Strong;
- Leaves-Strong;
- Hearts-Strong;
- Bells-Strong.
3) Resolution. If both players pass, the hand is Ramsch. Otherwise Strong beats Simple, and any bid beats Pass. If both players bid at the same level (both Simple or both Strong), the priority player's bid wins whatever the contracts. The winning bidder is the declarer and the other player is the defender. The contract and level are those of the winning bid.
4) Both bids and the resulting contract (or Ramsch) are announced to both players.
5) Double. If the hand is not Ramsch, the defender chooses Double or No double. The choice is announced.

CONTRACTS.
- Wenz: the trumps are the four Unters only, ranked Acorns Unter > Leaves Unter > Hearts Unter > Bells Unter. In every suit the non-trump cards rank Ace > Ten > King > Ober > Nine. Unters belong to no plain suit.
- Suit Solo (Acorns, Leaves, Hearts or Bells, as named): there are 12 trumps, ranked from high to low:
  - the four Obers (Acorns > Leaves > Hearts > Bells);
  - then the four Unters (Acorns > Leaves > Hearts > Bells);
  - then the Ace, Ten, King and Nine of the named suit.
  Obers and Unters belong to no plain suit. In the other three suits the non-trump cards rank Ace > Ten > King > Nine.
- Ramsch: trumps and ranks exactly as in Wenz.

TRICKS (every round).
1) The leader plays any card from their hand. In the first trick of a hand the leader is the declarer, or the priority player in Ramsch. Afterwards the leader is the winner of the previous trick.
2) The other player then plays a card. If a trump was led, they must play a trump if they have one. If a plain suit was led, they must play a non-trump card of that suit if they have one. Otherwise they may play any card.
3) The trick is won by the highest trump in it. If it has no trump, it is won by the higher card of the led suit.
4) The trick winner adds the card points of both cards to their card-point total for the hand, and leads next.
5) The two cards, the trick winner and both players' card-point totals for the hand are announced.

END OF EACH HAND (after the 8th trick). Let D be the declarer's card points and F the defender's card points.
- A Simple contract is made if D >= F + 10.
- A Strong contract is made if D >= 2 x F and D >= 30.
- Stake: Simple is 2 match points and Strong is 4 match points. The stake is doubled if the defender chose Double (Simple 4, Strong 8).
- If the contract is made, the declarer gains the stake. Otherwise the defender gains the stake.
- Ramsch: the player with fewer card points gains 1 match point. If the card points are equal, nobody scores.
- Card-point totals reset to 0 and the next hand begins.

END. After the fourth hand the match ends.

How the winner is decided: After the fourth hand, the player with more match points wins. Equal match points is a draw.
````

## Reply

````
```json
{
  "name": "Blind Officers' Schafkopf",
  "summary": "Two-player Schafkopf variant: sealed contract bids, an optional double, 8 tricks per hand from a 24-card deck with an unseen Blind, over 4 hands (32 rounds), scored in match points.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 24,
    "suits": 4,
    "cards_per_suit": 6,
    "deck_card_points": 120,
    "points_ace": 11,
    "points_ten": 10,
    "points_king": 4,
    "points_ober": 3,
    "points_unter": 2,
    "points_nine": 0,
    "hands": 4,
    "tricks_per_hand": 8,
    "total_rounds": 32,
    "cards_dealt_per_player": 8,
    "blind_size": 8,
    "bid_options": 11,
    "wenz_trumps": 4,
    "suit_solo_trumps": 12,
    "simple_margin": 10,
    "strong_multiplier": 2,
    "strong_minimum_points": 30,
    "simple_stake": 2,
    "strong_stake": 4,
    "double_factor": 2,
    "ramsch_award": 1,
    "starting_match_points": 0,
    "level_pass": 0,
    "level_simple": 1,
    "level_strong": 2,
    "trump_strength_base": 100,
    "plain_rank_ace": 6,
    "plain_rank_ten": 5,
    "plain_rank_king": 4,
    "plain_rank_ober": 3,
    "plain_rank_nine": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The cards this player holds, named like 'Acorns Ace', 'Bells Unter'.", "observable": false},
      {"key": "bid", "type": "text", "visible": "public", "initial": "", "meaning": "This hand's sealed bid (one of the 11 options). It is revealed only after both players have bid.", "observable": false},
      {"key": "bid_level", "type": "number", "visible": "public", "initial": 0, "meaning": "Bid level: Pass 0, Simple 1, Strong 2.", "observable": false},
      {"key": "card_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Card points won in tricks this hand. Reset to 0 at the end of each hand.", "observable": true},
      {"key": "match_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Match points across the match (the score).", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Undealt cards during the deal (24 at the start of each hand).", "observable": false},
      {"key": "blind", "type": "list", "visible": "none", "initial": [], "meaning": "The 8 undealt cards of the hand. Never seen, played or scored.", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current hand, 1 to 4 (5 means the match is over).", "observable": true},
      {"key": "trick_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The trick within the current hand, 1 to 8.", "observable": false},
      {"key": "priority_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat with priority: 1 in hands 1 and 3, 2 in hands 2 and 4.", "observable": false},
      {"key": "contract", "type": "text", "visible": "public", "initial": "", "meaning": "Wenz, Acorns, Leaves, Hearts, Bells, or Ramsch.", "observable": true},
      {"key": "level", "type": "text", "visible": "public", "initial": "", "meaning": "Simple or Strong (empty in Ramsch).", "observable": false},
      {"key": "declarer_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The declarer's seat (0 in Ramsch).", "observable": true},
      {"key": "defender_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The defender's seat (0 in Ramsch).", "observable": false},
      {"key": "doubled", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the defender chose Double this hand.", "observable": false},
      {"key": "trump_list", "type": "list", "visible": "public", "initial": [], "meaning": "This hand's trumps, ordered from highest to lowest.", "observable": false},
      {"key": "leader_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat that leads the current trick.", "observable": false},
      {"key": "led_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card led in the current trick.", "observable": false},
      {"key": "follow_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card played second in the current trick.", "observable": false},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat that won the last trick.", "observable": false}
    ]
  },
  "setup": [
    "Both players start with 0 match points.",
    "hand_number is set to 1 and trick_number to 1.",
    "The full 24-card deck consists of Acorns, Leaves, Hearts and Bells, each with Ace, Ten, King, Ober, Unter and Nine. It is rebuilt at the start of every hand."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_number == 1: set game.deck to all 24 cards. Draw 8 cards at random from deck into each player's hand. Move the remaining 8 cards to game.blind, leaving deck empty. Set every card_points to 0, doubled to false, contract and level to empty, and declarer_seat and defender_seat to 0. Set priority_seat to 1 if hand_number is odd, else 2."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When trick_number == 1: each player is sent their own hand."},
    {"action": "poll", "who": "all players", "answer": "one of: Pass, Wenz-Simple, Acorns-Simple, Leaves-Simple, Hearts-Simple, Bells-Simple, Wenz-Strong, Acorns-Strong, Leaves-Strong, Hearts-Strong, Bells-Strong", "effect": "When trick_number == 1: store each answer in that player's bid. Set bid_level to 0 for Pass, 1 for any -Simple bid, 2 for any -Strong bid. No one sees a bid until both are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_number == 1, resolve the bids. If both bid_level == 0: contract = Ramsch, declarer_seat = 0, defender_seat = 0, leader_seat = priority_seat, trump_list = [Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter]. Otherwise the declarer is the seat with the higher bid_level; if the levels are equal, the declarer is priority_seat. Set declarer_seat to that seat and defender_seat to the other. Take contract (the word before the dash) and level (Simple or Strong) from the declarer's bid. Set leader_seat = declarer_seat. If contract == Wenz, trump_list = [Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter]. If contract is a suit X, trump_list = [Acorns Ober, Leaves Ober, Hearts Ober, Bells Ober, Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter, X Ace, X Ten, X King, X Nine]."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_number == 1: announce both bids, the contract and level (or Ramsch), and the declarer."},
    {"action": "ask", "who": "the seat in game.defender_seat", "answer": "one of: Double, No double", "effect": "When trick_number == 1 and contract != Ramsch: set doubled = true if the answer is Double, else false."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_number == 1 and contract != Ramsch: announce whether the defender doubled."},
    {"action": "ask", "who": "the seat in game.leader_seat", "answer": "any one card from their own hand", "effect": "Set led_card to the chosen card and remove it from the leader's hand."},
    {"action": "ask", "who": "the seat that is not game.leader_seat", "answer": "one legal card from their own hand (see offers)", "effect": "Set follow_card to the chosen card and remove it from the follower's hand."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Compute each card's strength. A card in trump_list scores 100 + (length of trump_list - its position, where the first position is 0). A card not in trump_list whose suit matches led_card's suit (led_card itself not being a trump) scores its plain rank: Ace 6, Ten 5, King 4, Ober 3, Nine 1. Any other card scores 0. trick_winner = leader_seat if strength(led_card) > strength(follow_card), else the other seat. Add the card points of both cards (Ace 11, Ten 10, King 4, Ober 3, Unter 2, Nine 0) to the trick winner's card_points. Set leader_seat = trick_winner."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce led_card, follow_card, the trick_winner, and both players' card_points."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_number == 8, score the hand. Let D = the declarer's card_points and F = the defender's card_points. Stake = 2 if level is Simple, 4 if level is Strong; doubled if doubled == true. Simple is made if D >= F + 10. Strong is made if D >= 2*F and D >= 30. If made, the declarer's match_points += stake; otherwise the defender's match_points += stake. If contract == Ramsch, the player with fewer card_points gets match_points += 1, and nobody scores if the totals are equal. Then set both card_points to 0, hand_number += 1, trick_number = 1. Otherwise (trick_number < 8): trick_number += 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When a hand has just been scored (trick_number == 1 and hand_number > 1): announce whether the contract was made (or the Ramsch result), the stake awarded, and both match_points."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if hand_number > 4; otherwise continue."}
  ],
  "ending": {
    "condition": "game.hand_number > 4",
    "rank_by": "you.match_points",
    "decided_by": "After four hands (32 tricks), the player with more match points wins. Equal match points share the win, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When a hand starts, then each player receives 8 cards from the 24-card deck into hand, and the other 8 go to blind, which is never played or scored."},
    {"id": "R2", "text": "When it is hand 1 or 3, then priority_seat is 1; when it is hand 2 or 4, then priority_seat is 2."},
    {"id": "R3", "text": "When a hand starts, then both players bid simultaneously, choosing one of 11 options: Pass, or one of Wenz/Acorns/Leaves/Hearts/Bells at the Simple or Strong level."},
    {"id": "R4", "text": "When both players pass, then contract is Ramsch and nobody is declarer."},
    {"id": "R5", "text": "When one player bids Strong and the other bids Simple or Pass, then the Strong bidder is declarer."},
    {"id": "R6", "text": "When one player bids Simple and the other passes, then the Simple bidder is declarer."},
    {"id": "R7", "text": "When both players bid at the same level, then the priority player's bid wins, whatever the contracts."},
    {"id": "R8", "text": "When the bids are resolved, then both bids and the resulting contract are announced to both players."},
    {"id": "R9", "text": "When the hand is not Ramsch, then the defender chooses Double or No double, and the choice is announced."},
    {"id": "R10", "text": "When the contract is Wenz or Ramsch, then the only trumps are the 4 Unters, ranked Acorns > Leaves > Hearts > Bells, and plain suits rank Ace > Ten > King > Ober > Nine."},
    {"id": "R11", "text": "When the contract is a suit solo, then there are 12 trumps ranked: the 4 Obers (Acorns > Leaves > Hearts > Bells), then the 4 Unters in the same order, then Ace, Ten, King, Nine of the named suit; the other suits rank Ace > Ten > King > Nine."},
    {"id": "R12", "text": "When it is the first trick of a hand, then the declarer leads, or the priority player leads in Ramsch."},
    {"id": "R13", "text": "When a trick after the first starts, then the previous trick's winner leads."},
    {"id": "R14", "text": "When a trump is led and the follower holds a trump, then the follower must play a trump."},
    {"id": "R15", "text": "When a plain suit is led and the follower holds a non-trump card of that suit, then the follower must play one."},
    {"id": "R16", "text": "When the follower cannot follow as required, then the follower may play any card."},
    {"id": "R17", "text": "When a trick contains a trump, then the highest trump wins it; otherwise the higher card of the led suit wins it."},
    {"id": "R18", "text": "When a trick is won, then the winner's card_points increase by the card points of both cards (Ace 11, Ten 10, King 4, Ober 3, Unter 2, Nine 0)."},
    {"id": "R19", "text": "When a trick ends, then both cards, the winner and both card_points totals are announced."},
    {"id": "R20", "text": "When a Simple contract ends, then it is made if the declarer's card points D >= the defender's card points F + 10."},
    {"id": "R21", "text": "When a Strong contract ends, then it is made if D >= 2 x F and D >= 30."},
    {"id": "R22", "text": "When a contract is made, then the declarer gains the stake (Simple 2, Strong 4); when it is not made, then the defender gains it."},
    {"id": "R23", "text": "When the defender chose Double, then the stake is doubled (Simple 4, Strong 8)."},
    {"id": "R24", "text": "When a Ramsch hand ends, then the player with fewer card points gains 1 match point, and nobody scores if the card points are equal."},
    {"id": "R25", "text": "When a hand ends, then both card_points reset to 0."},
    {"id": "R26", "text": "When the fourth hand (round 32) ends, then the match ends, the player with more match_points wins, and equal match_points is a draw."}
  ],
  "offers": [
    {"question": "Sealed bid (first round of each hand)", "who": "both seats", "options": "Pass, Wenz-Simple, Acorns-Simple, Leaves-Simple, Hearts-Simple, Bells-Simple, Wenz-Strong, Acorns-Strong, Leaves-Strong, Hearts-Strong, Bells-Strong"},
    {"question": "Double (first round of a non-Ramsch hand)", "who": "the defender only; the declarer is not asked", "options": "Double, No double"},
    {"question": "Lead a card", "who": "the seat in leader_seat", "options": "every card in their hand"},
    {"question": "Follow a card", "who": "the seat that did not lead", "options": "If led_card is in trump_list and the follower holds any card in trump_list: only those trumps. If led_card is not a trump and the follower holds non-trump cards of led_card's suit: only those. Otherwise: every card in their hand."}
  ],
  "choices": [
    {"what": "2 players, as the designer set", "why": "The source is written for exactly 2 players (priority, declarer against defender). Its core is reading the opponent's sealed bid and hand strength, which works at 2. More seats would break the declarer/defender structure."},
    {"what": "No table talk step", "why": "The rules have none, and with 2 opposed players talk would only add words."},
    {"what": "Card naming as '<Suit> <Rank>'", "why": "Lets the suit and rank be read from the card's name for the follow rule, strength and points."},
    {"what": "Trick winner decided by a numeric strength", "why": "Trump strength is 100 plus a position score from the ordered trump_list, plain led-suit cards score their rank, and others score 0. This is an arithmetic version of the stated ranking rules."},
    {"what": "Hand bookkeeping driven by trick_number and hand_number with per-step 'when' conditions", "why": "The start-of-hand and end-of-hand steps run only on the first and eighth trick of each hand, without needing alternative blocks."}
  ],
  "simplifications": [
    {"what": "Follow-suit legality is enforced by restricting the offered options rather than by a penalty", "why": "The engine offers a seat only what it may do, so illegal plays cannot occur."},
    {"what": "Card point values and plain ranks are applied by rank name instead of a lookup table", "why": "The engine has no lookup operation; a small conditional on the rank word is equivalent."}
  ],
  "unsupported": []
}
```
````
