# 03 spec

- time: 2026-10-28T02:59:28+00:00 (55.5s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 6c02c67df61fe5f6, reply sha256 60db74f459358cfe

## Sent

````
Game: Da Bai Fen Lite
Players in the source: 4 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SEATS AND TEAMS. Seats 1, 2, 3 and 4 sit in anticlockwise order. Seats 1 and 3 are Team North-South (NS). Seats 2 and 4 are Team East-West (EW). Partners cannot see each other's cards. There is no talk; the only communication is the cards played.

DECK. The deck has 30 cards. Each of four suits (Spades, Hearts, Clubs, Diamonds) has seven cards: 5, 8, 10, J, Q, K, A, with rank values 5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7. There are also two jokers: the Big Joker and the Small Joker. Point cards: each K is worth 10 points, each 10 is worth 10 points, each 5 is worth 5 points. All other cards and both jokers are worth 0. The deck holds 100 points in total.

MATCH STRUCTURE. The match has 4 hands of 8 rounds each, 32 rounds in total. The declarer is seat 1 in hand 1, seat 2 in hand 2, seat 3 in hand 3 and seat 4 in hand 4. The declarer's team is the Declaring Team for that hand; the other team is the Defending Team.

ROUND 1 OF EACH HAND (DEAL AND TRUMPS). The 30 cards are shuffled (the only random draw of the round). Each player privately receives 7 cards. The remaining 2 cards form the face-down kitty, which no one sees. The declarer then names one suit as the trump suit, and it is announced to all. Trumps are the Big Joker, the Small Joker and the 7 cards of the trump suit, 9 cards in all. For following purposes all trumps form one suit, the Trump suit. The declarer will lead the first trick.

ROUNDS 2 TO 8 OF EACH HAND (ONE TRICK EACH).
(a) The leader plays any one card face up. The suit of that card is the led suit; if the card is a trump, the led suit is Trump.
(b) The other three players then each play one card face up, one after another, in anticlockwise order from the leader. Each sees the cards already played. A player holding a card of the led suit must play one. A player holding none may play any card. An illegal play is rejected and the player must choose again.
(c) Strength of each played card. Big Joker = 40. Small Joker = 39. A trump-suit card = 20 + its rank value. A non-trump card of the led suit = 10 + its rank value. Any other card = its rank value.
(d) The card with the highest strength wins the trick. Ties cannot occur. The winner's team adds the point values of the four cards to its hand points, and the winner leads the next trick.
(e) In round 8 (the 7th and last trick), the kitty is also revealed after the trick, and its points are added to the hand points of the team that won that trick.

END OF HAND SCORING. Let P be the Defending Team's hand points, always a multiple of 5 from 0 to 100.
- P from 0 to 15: Declaring Team +3 match points.
- P from 20 to 35: Declaring Team +2.
- P from 40 to 55: Defending Team +1.
- P from 60 to 75: Defending Team +2.
- P from 80 to 100: Defending Team +3.
In addition, each team adds its hand points to its running card-point total. Hand points then reset to 0 for the next hand.

How the winner is decided: After hand 4, the team with more match points wins, and both its players win. If match points are equal, the team with the higher card-point total over all four hands wins. If that is also equal, the match is a draw.
````

## Reply

````
```json
{
  "name": "Da Bai Fen Lite",
  "summary": "A four-player partnership trick-taking game (NS v EW) over 4 hands of 7 tricks with a 30-card deck and jokers. Teams win match points by how many card points the defenders capture.",
  "players": {"min": 4, "max": 4, "suggested": 4},
  "parameters": {
    "seats": 4,
    "deck_size": 30,
    "suits": 4,
    "cards_per_suit": 7,
    "jokers": 2,
    "rank_5": 1, "rank_8": 2, "rank_10": 3, "rank_j": 4, "rank_q": 5, "rank_k": 6, "rank_a": 7,
    "points_k": 10, "points_10": 10, "points_5": 5, "points_other": 0,
    "total_points": 100,
    "hands": 4,
    "rounds_per_hand": 8,
    "total_rounds": 32,
    "tricks_per_hand": 7,
    "cards_dealt_each": 7,
    "kitty_size": 2,
    "trump_count": 9,
    "big_joker_strength": 40,
    "small_joker_strength": 39,
    "trump_base": 20,
    "led_suit_base": 10,
    "off_suit_base": 0,
    "band_declarer_3_max": 15,
    "band_declarer_2_min": 20, "band_declarer_2_max": 35,
    "band_defender_1_min": 40, "band_defender_1_max": 55,
    "band_defender_2_min": 60, "band_defender_2_max": 75,
    "band_defender_3_min": 80,
    "award_3": 3, "award_2": 2, "award_1": 1,
    "rank_weight_match_points": 1000
  },
  "attributes": {
    "player": [
      {"key": "team", "type": "text", "visible": "public", "initial": "NS for seats 1 and 3, EW for seats 2 and 4", "meaning": "the player's team", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "the cards the player holds, as codes such as 'S-K', 'H-10', 'BJ' (Big Joker), 'SJ' (Small Joker)", "observable": false},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "the card the player played to the current trick, face up", "observable": false},
      {"key": "card_strength", "type": "number", "visible": "public", "initial": 0, "meaning": "the strength of played_card in the current trick", "observable": false},
      {"key": "match_points", "type": "number", "visible": "public", "initial": 0, "meaning": "the team's match points, mirrored on both partners", "observable": true},
      {"key": "card_points", "type": "number", "visible": "public", "initial": 0, "meaning": "the team's running card-point total over completed hands, mirrored on both partners", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "all 30 cards", "meaning": "the undealt cards: 4 suits x {5,8,10,J,Q,K,A} plus BJ and SJ", "observable": false},
      {"key": "kitty", "type": "list", "visible": "none", "initial": [], "meaning": "the 2 face-down cards left after the deal", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "the current hand, 1 to 4", "observable": true},
      {"key": "round_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "the round within the hand, 1 to 8 (1 = deal and trumps, 2 to 8 = tricks)", "observable": false},
      {"key": "declarer", "type": "number", "visible": "public", "initial": 1, "meaning": "the declarer's seat, equal to hand_number", "observable": true},
      {"key": "declaring_team", "type": "text", "visible": "public", "initial": "NS", "meaning": "the declarer's team: NS when declarer is 1 or 3, EW when declarer is 2 or 4", "observable": false},
      {"key": "trump_suit", "type": "text", "visible": "public", "initial": "", "meaning": "the trump suit named by the declarer", "observable": true},
      {"key": "leader", "type": "number", "visible": "public", "initial": 1, "meaning": "the seat that leads the current trick", "observable": false},
      {"key": "led_suit", "type": "text", "visible": "public", "initial": "", "meaning": "the suit of the led card, or 'Trump' if the led card is a trump", "observable": false},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "the seat whose card has the highest card_strength in the trick", "observable": false},
      {"key": "trick_points", "type": "number", "visible": "public", "initial": 0, "meaning": "the sum of point values of the 4 cards in the trick", "observable": false},
      {"key": "ns_hand_points", "type": "number", "visible": "public", "initial": 0, "meaning": "card points NS has won this hand", "observable": true},
      {"key": "ew_hand_points", "type": "number", "visible": "public", "initial": 0, "meaning": "card points EW has won this hand", "observable": true},
      {"key": "defender_points", "type": "number", "visible": "public", "initial": 0, "meaning": "P, the Defending Team's hand points at the end of the hand", "observable": false},
      {"key": "ns_match_points", "type": "number", "visible": "public", "initial": 0, "meaning": "NS match points", "observable": true},
      {"key": "ew_match_points", "type": "number", "visible": "public", "initial": 0, "meaning": "EW match points", "observable": true},
      {"key": "ns_card_points", "type": "number", "visible": "public", "initial": 0, "meaning": "NS running card-point total", "observable": true},
      {"key": "ew_card_points", "type": "number", "visible": "public", "initial": 0, "meaning": "EW running card-point total", "observable": true}
    ]
  },
  "setup": [
    "Seats 1 and 3 get team NS; seats 2 and 4 get team EW.",
    "All match_points, card_points and team totals start at 0.",
    "Set hand_number = 1, round_in_hand = 1, declarer = 1, declaring_team = NS."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "when round_in_hand == 1: deck is reset to all 30 cards; every hand, kitty and trump_suit are cleared; ns_hand_points = ew_hand_points = 0; declarer = hand_number; declaring_team = NS if declarer is odd, else EW; leader = declarer"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round_in_hand == 1: draw 7 random cards from deck into each player's hand (removed from deck), then move the 2 remaining cards of deck into kitty"},
    {"action": "sync", "who": "all players", "answer": null, "effect": "when round_in_hand == 1: each player sees their own hand only"},
    {"action": "ask", "who": "the declarer (seat = declarer)", "answer": "one of: Spades, Hearts, Clubs, Diamonds", "effect": "when round_in_hand == 1: trump_suit = the answer; announce to all 'Trump suit is {trump_suit}; seat {declarer} leads.'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round_in_hand >= 2: every played_card = '' and card_strength = 0; led_suit = ''"},
    {"action": "ask", "who": "each player in turn, starting from seat = leader and going anticlockwise (leader, leader+1, leader+2, leader+3, wrapping 4 to 1)", "answer": "one card from own hand: the leader may choose any card; a follower must choose a card of led_suit if holding one (jokers and trump_suit cards count as suit 'Trump'), otherwise any card", "effect": "when round_in_hand >= 2: the card moves from hand to played_card, face up to all; if the player is the leader, led_suit = 'Trump' when the card is a joker or of trump_suit, else the card's suit; card_strength = 40 for BJ, 39 for SJ, 20 + rank for a trump_suit card, 10 + rank for a non-trump card of led_suit, otherwise rank (5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7)", "judged": "The card this player chose is legal: either the player is the leader, or the card is of the led suit (jokers and trump-suit cards counting as Trump), or the player held no card of the led suit."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round_in_hand >= 2: trick_winner = the seat with the highest card_strength; trick_points = sum over the 4 played cards of (10 for K, 10 for 10, 5 for 5, 0 otherwise); if trick_winner's team is NS then ns_hand_points += trick_points, else ew_hand_points += trick_points; leader = trick_winner; announce 'Seat {trick_winner} wins the trick for {trick_points} points.'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round_in_hand == 8: reveal kitty to all; add the kitty's point values to the hand points of trick_winner's team"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round_in_hand == 8: defender_points = ew_hand_points if declaring_team is NS, else ns_hand_points; if defender_points <= 15, the declaring team's match points += 3; if 20..35, the declaring team += 2; if 40..55, the defending team += 1; if 60..75, the defending team += 2; if >= 80, the defending team += 3; ns_card_points += ns_hand_points; ew_card_points += ew_hand_points; copy the team match points and card points onto each player's match_points and card_points; announce the hand result"},
    {"action": "update", "who": "all players", "answer": null, "effect": "if round_in_hand == 8 then hand_number += 1 and round_in_hand = 1, else round_in_hand += 1"},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game when hand_number > 4; otherwise continue"}
  ],
  "ending": {
    "condition": "hand_number > 4 (after 32 rounds)",
    "rank_by": "you.match_points * 1000 + you.card_points",
    "decided_by": "The team with more match points wins, and both its partners win. If match points are equal, the team with the higher card-point total wins. If both are equal, all four players share the top value, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "Seats 1 and 3 are team NS and seats 2 and 4 are team EW, and no talk step exists."},
    {"id": "R2", "text": "When round_in_hand is 1, each player is dealt 7 cards from the 30-card deck and the other 2 cards go to the hidden kitty."},
    {"id": "R3", "text": "The declarer is seat 1 in hand 1, seat 2 in hand 2, seat 3 in hand 3 and seat 4 in hand 4."},
    {"id": "R4", "text": "When round_in_hand is 1, the declarer names one of Spades, Hearts, Clubs or Diamonds as trump_suit, it is announced to all, and the declarer leads the first trick."},
    {"id": "R5", "text": "Trumps are BJ, SJ and the 7 cards of trump_suit, 9 cards in all, and they count as the single suit 'Trump' for following."},
    {"id": "R6", "text": "When the leader plays a card, led_suit becomes that card's suit, or 'Trump' if the card is a joker or of trump_suit."},
    {"id": "R7", "text": "When a follower holds a card of led_suit, then only led_suit cards are offered; when they hold none, then every card in their hand is offered."},
    {"id": "R8", "text": "Players play to a trick in anticlockwise order starting from the leader, and each sees the cards already played."},
    {"id": "R9", "text": "Card strength is 40 for BJ, 39 for SJ, 20 + rank for a trump_suit card, 10 + rank for a non-trump led_suit card, and rank otherwise, with 5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7."},
    {"id": "R10", "text": "The highest-strength card wins the trick; its team adds the trick's points (K=10, 10=10, 5=5, others 0) to its hand points, and its player leads next."},
    {"id": "R11", "text": "When round_in_hand is 8, after the trick the kitty is revealed and its points go to the team that won that trick."},
    {"id": "R12", "text": "At the end of a hand, if defender_points is 0 to 15, the Declaring Team gains 3 match points."},
    {"id": "R13", "text": "At the end of a hand, if defender_points is 20 to 35, the Declaring Team gains 2 match points."},
    {"id": "R14", "text": "At the end of a hand, if defender_points is 40 to 55, the Defending Team gains 1 match point."},
    {"id": "R15", "text": "At the end of a hand, if defender_points is 60 to 75, the Defending Team gains 2 match points."},
    {"id": "R16", "text": "At the end of a hand, if defender_points is 80 to 100, the Defending Team gains 3 match points."},
    {"id": "R17", "text": "At the end of each hand, each team adds its hand points to its card-point total, and hand points reset to 0 for the next hand."},
    {"id": "R18", "text": "After 4 hands (32 rounds), the team with more match points wins; if level, the team with more card points wins; if both are level, the match is a draw."}
  ],
  "offers": [
    {"question": "Name the trump suit (round 1 of each hand)", "who": "the declarer only", "options": "Spades, Hearts, Clubs, Diamonds"},
    {"question": "Play a card to the trick (rounds 2 to 8)", "who": "each seat in turn from the leader", "options": "the leader: every card in own hand; a follower holding at least one card of led_suit (for led_suit Trump: jokers and trump_suit cards; for any other suit: cards of that suit that are not trumps): only those cards; a follower holding no led_suit card: every card in own hand"}
  ],
  "choices": [
    {"what": "4 players (min = max = suggested = 4)", "why": "The designer fixed two partnerships of two. Fewer seats break the teams, and more seats do not fit the 30-card deal of 7 each plus a 2-card kitty."},
    {"what": "No talk step", "why": "The rules forbid talk; signalling through card play is the skill. A thoughtful player tracks played trumps and points, smears points onto a partner's winning trick, and holds trumps back to capture kings and tens."},
    {"what": "Team scores are mirrored onto each player's match_points and card_points", "why": "The ranking expression works per player, so both partners carry the team's totals."},
    {"what": "Ranking expression match_points * 1000 + card_points", "why": "Card points can total at most 400, so match points always come first and card points break ties. A full tie makes all four seats share the win, which is the draw."},
    {"what": "Card codes such as 'S-K', 'H-10', 'BJ', 'SJ'", "why": "The rules do not say how cards are labelled; codes let suit, rank and points be read arithmetically."}
  ],
  "simplifications": [
    {"what": "The 32 rounds run as one repeated step list, with `when` conditions on round_in_hand choosing the deal steps (round 1) or the trick steps (rounds 2 to 8)", "why": "The step list is flat; a condition on each single step gives the same order."},
    {"what": "Legality of following suit is enforced by offering only legal cards, with a judged check as a backstop", "why": "The source rejects illegal plays and asks again; offering only legal cards has the same effect."},
    {"what": "A draw is shown as all four seats sharing the win", "why": "The engine has no separate draw outcome."}
  ],
  "unsupported": []
}
```
````
