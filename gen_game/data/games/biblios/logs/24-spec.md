# 24 spec

- time: 2026-10-27T21:09:33+00:00 (52.2s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0b989f7e495dbca8, reply sha256 fce28debf00479ef

## Sent

````
Game: Biblios: Sealed Scriptorium (revised)
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP.
The deck has 36 cards.
- There are 30 colour cards: for each of the five colours (Red, Blue, Green, Yellow, Purple), one card each of values 1, 1, 2, 2, 3 and 4.
- There are 6 Church cards.
Shuffle the deck once. Its order is hidden from everyone.

Each player starts with 8 gold. Each colour has a public die worth, starting at 4. A public worth can never go below 2 or above 8.

Every player has two collections:
- A hidden collection, seen only by its owner. It holds the colour cards and Church cards they kept, and their secret marks.
- A public collection, seen by all. It holds the colour cards they won.
Gold totals and public die worths are public. The worths shown during play never include secret marks.

ROUNDS.
There are 12 rounds. The active player is seat 1, 2, 3, 1, 2, 3 in rounds 1-6, and seat 3, 2, 1, 3, 2, 1 in rounds 7-12. Each round has these steps:

1. Announce the round number, the active player, all public die worths, all gold totals and all public collections.
2. Remove the top two cards of the deck. Show them privately to the active player only, as Card A (the top card) and Card B (the next card).
3. The active player privately chooses Keep A or Keep B.
4. The kept card goes into the active player's hidden collection. Nothing about it is announced. The other card is announced publicly as this round's lot.
5. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
6. Sealed bid: all three players, including the active player, at the same time bid a whole number of gold from 0 up to the gold they hold.
7. Reveal all bids. If the highest bid is at least 1 and no other player bid the same amount, that player wins the lot and pays their bid to the bank (the gold leaves the game). Otherwise nobody pays and the lot is discarded face-up.
8. A won colour card goes into the winner's public collection.
9. Church and secret mark, answered at the same time:
   (a) The active player always privately names one colour and a direction (+1 or -1). This is recorded secretly in their hidden collection as this round's mark. It counts at scoring only if the card they kept this round is a Church card. Otherwise it is void. This question is asked every round, so being asked reveals nothing.
   (b) If the lot was a Church card and someone won it, the winner publicly names one colour and a direction (+1 or -1).
   If the active player is also the winner, they answer both parts.
10. If part (b) was answered, change that colour's public worth by the named direction. If this would take it below 2 or above 8, it has no effect. The won Church card is then discarded face-up. Secret marks change nothing now.
11. Every player gains 1 gold.
12. If this was round 12, go to scoring. Otherwise begin the next round.

SCORING.
1. Final worths. Start from each colour's public worth. Reveal all hidden collections. Take every mark that counts (made in a round where that player kept a Church card) and apply them one at a time in round order, earliest round first. Each mark changes its colour's worth by 1 in its direction, checked against the worth as already changed by earlier marks. A mark that would take a worth below 2 or above 8 has no effect.
2. Majorities. For each colour, add up the values of each player's cards of that colour, hidden and public together.
   - If one player has the strictly highest total and it is at least 1, they score VP equal to that colour's final worth.
   - If two or more players tie for the highest total (at least 1), each of them scores half the final worth, rounded down.
   - If no one has a card of that colour, nobody scores it.
   Church cards have no value at scoring.
3. Gold. Each player scores 1 VP for every full 5 gold they hold.

How the winner is decided: The player with the most VP after scoring wins. If two or more players tie for the most VP, the game is a draw.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "Biblios: Sealed Scriptorium (revised)",
  "summary": "Three scribes each round secretly keep one of two cards, then sealed-bid for the other, while public Church cards and secret marks shift the worth of five colours that score by majority.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "deck_size": 36,
    "colour_cards": 30,
    "church_cards": 6,
    "colours": 5,
    "colour_card_values_per_colour": "1,1,2,2,3,4",
    "cards_per_colour": 6,
    "starting_gold": 8,
    "starting_worth": 4,
    "worth_min": 2,
    "worth_max": 8,
    "rounds": 12,
    "cards_revealed_to_active": 2,
    "bid_min": 0,
    "min_winning_bid": 1,
    "gold_income_per_round": 1,
    "mark_step": 1,
    "church_step": 1,
    "tie_share_divisor": 2,
    "gold_per_vp": 5,
    "min_majority_total": 1
  },
  "attributes": {
    "player": [
      {"key": "gold", "type": "number", "visible": "public", "initial": 8, "meaning": "Gold held. Bids are paid from it, it gains 1 each round, and 1 VP is scored for every full 5 at the end.", "observable": true},
      {"key": "hidden_cards", "type": "list", "visible": "ally", "initial": [], "meaning": "Hidden collection: the cards this player kept as active player (colour cards such as 'Red 3', or 'Church'). It is revealed to all at scoring.", "observable": false},
      {"key": "public_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Public collection: the colour cards won at auction.", "observable": true},
      {"key": "marks", "type": "list", "visible": "ally", "initial": [], "meaning": "Secret marks, part of the hidden collection. There is one entry per round in which this player was active, recorded as 'round:colour:direction:counts', where counts is yes if the card kept that round was Church.", "observable": false},
      {"key": "offer_a", "type": "text", "visible": "ally", "initial": "", "meaning": "Card A (the top card) shown privately to this player while active.", "observable": false},
      {"key": "offer_b", "type": "text", "visible": "ally", "initial": "", "meaning": "Card B (the next card) shown privately to this player while active.", "observable": false},
      {"key": "kept_card", "type": "text", "visible": "ally", "initial": "", "meaning": "The card this player kept in the current round as active player.", "observable": false},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "This round's non-binding talk message.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "This round's sealed bid. It is revealed only after all bids are in.", "observable": false},
      {"key": "total_red", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Red card values in the hidden and public collections, computed at scoring.", "observable": false},
      {"key": "total_blue", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Blue card values, computed at scoring.", "observable": false},
      {"key": "total_green", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Green card values, computed at scoring.", "observable": false},
      {"key": "total_yellow", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Yellow card values, computed at scoring.", "observable": false},
      {"key": "total_purple", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Purple card values, computed at scoring.", "observable": false},
      {"key": "vp", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory points, computed at scoring.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "Red 1, Red 1, Red 2, Red 2, Red 3, Red 4, and the same six values for Blue, Green, Yellow and Purple, plus Church x6 (36 cards)", "meaning": "The draw pile, shuffled once at setup. Index 0 is the top card.", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "The current round number, from 1 to 12.", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat of this round's active player.", "observable": true},
      {"key": "worth_red", "type": "number", "visible": "public", "initial": 4, "meaning": "Red public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_blue", "type": "number", "visible": "public", "initial": 4, "meaning": "Blue public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_green", "type": "number", "visible": "public", "initial": 4, "meaning": "Green public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_yellow", "type": "number", "visible": "public", "initial": 4, "meaning": "Yellow public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_purple", "type": "number", "visible": "public", "initial": 4, "meaning": "Purple public die worth, from 2 to 8.", "observable": true},
      {"key": "lot", "type": "text", "visible": "public", "initial": "", "meaning": "The card put up for auction this round.", "observable": true},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up discards: unwon lots and won Church cards.", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "The highest bid this round.", "observable": false},
      {"key": "high_count", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players bid the highest amount this round.", "observable": false},
      {"key": "winner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat that won this round's lot, or 0 if nobody won it.", "observable": true},
      {"key": "final_worth_red", "type": "number", "visible": "public", "initial": 4, "meaning": "Red worth after counting marks are applied at scoring.", "observable": false},
      {"key": "final_worth_blue", "type": "number", "visible": "public", "initial": 4, "meaning": "Blue final worth.", "observable": false},
      {"key": "final_worth_green", "type": "number", "visible": "public", "initial": 4, "meaning": "Green final worth.", "observable": false},
      {"key": "final_worth_yellow", "type": "number", "visible": "public", "initial": 4, "meaning": "Yellow final worth.", "observable": false},
      {"key": "final_worth_purple", "type": "number", "visible": "public", "initial": 4, "meaning": "Purple final worth.", "observable": false}
    ]
  },
  "setup": [
    "Build the deck list of 36 cards: for each of Red, Blue, Green, Yellow and Purple, the cards '<Colour> 1', '<Colour> 1', '<Colour> 2', '<Colour> 2', '<Colour> 3' and '<Colour> 4', plus six 'Church' cards.",
    "Shuffle the deck once by random order. Its order is hidden from everyone (visibility none).",
    "Set every player's gold to 8, hidden_cards, public_cards and marks to empty, and vp to 0.",
    "Set worth_red, worth_blue, worth_green, worth_yellow and worth_purple to 4, round to 0 and discard to empty."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1. If round <= 6, active_seat = ((round - 1) mod 3) + 1; otherwise active_seat = 3 - ((round - 7) mod 3). This gives seats 1,2,3,1,2,3,3,2,1,3,2,1. Reset winner_seat = 0, high_bid = 0, high_count = 0 and every bid = 0."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce round, active_seat, worth_red, worth_blue, worth_green, worth_yellow, worth_purple, every player's gold and every player's public_cards."},
    {"action": "update", "who": "seat {active_seat}", "answer": null, "effect": "Active player's offer_a = deck[0] and offer_b = deck[1]. Remove both from deck. Nothing is announced."},
    {"action": "sync", "who": "seat {active_seat}", "answer": null, "effect": "The active player privately sees offer_a as Card A and offer_b as Card B."},
    {"action": "ask", "who": "seat {active_seat}", "answer": "choice: Keep A | Keep B", "effect": "Private answer. If Keep A, kept_card = offer_a and lot = offer_b; if Keep B, kept_card = offer_b and lot = offer_a. Append kept_card to the active player's hidden_cards."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce publicly: 'This round's lot is {lot}.' Nothing about the kept card is announced."},
    {"action": "poll", "who": "all players", "answer": "short text", "effect": "message = the answer. Once all are in, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Messages are not binding."},
    {"action": "poll", "who": "all players", "answer": "whole number from 0 to you.gold", "effect": "bid = the answer. No bid is seen until all three are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Reveal every bid publicly. high_bid = max of bid over players; high_count = number of players with bid == high_bid. If high_bid >= 1 and high_count == 1, then winner_seat = the seat with that bid and that player's gold -= high_bid (paid to the bank and removed from the game). Otherwise winner_seat = 0, nobody pays, and lot is appended to discard (face-up)."},
    {"action": "update", "who": "seat {winner_seat}", "answer": null, "effect": "when winner_seat != 0 and lot != 'Church': append lot to the winner's public_cards."},
    {"action": "poll", "who": "seat {active_seat}; also seat {winner_seat} when winner_seat != 0 and lot == 'Church'", "answer": "(a) for the active seat, privately: choice of a colour and direction from Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1; (b) for the Church winner, publicly: the same ten options. A seat that is both answers both questions.", "effect": "(a) Append 'round:colour:direction:counts' to the active player's marks, where counts = yes if kept_card == 'Church', otherwise no. This changes no worth now. (b) The answer is recorded for the next step and announced publicly."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when winner_seat != 0 and lot == 'Church': for the named colour, if worth + direction is between 2 and 8 inclusive, then worth_<colour> += direction; otherwise no change. Append the Church card to discard (face-up). Announce the new worth."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Every player's gold += 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round == 12: reveal every player's hidden_cards and marks to all. Set each final_worth_<colour> = worth_<colour>. Then take every mark with counts = yes, from all players, sorted by round ascending, and apply them one at a time: if final_worth_<colour> + direction is between 2 and 8 inclusive, final_worth_<colour> += direction; otherwise no effect. Each mark is checked against the worth already changed by earlier marks."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round == 12: for each player and each colour, total_<colour> = sum of the numeric values of that colour's cards in hidden_cards and public_cards together. Church cards count 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round == 12: for each colour, M = max of total_<colour> over players and K = number of players with total_<colour> == M. If M >= 1 and K == 1, that player's vp += final_worth_<colour>. If M >= 1 and K >= 2, each tied player's vp += floor(final_worth_<colour> / 2). If M == 0, nobody scores the colour. Then every player's vp += floor(gold / 5). Announce every player's final worths, totals and vp."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round == 12, end the game; otherwise begin the next round."}
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.vp",
    "decided_by": "Each player's standing is their VP after scoring: colour majorities at final worths plus 1 VP per full 5 gold. The highest VP wins; players tied at the top share the result (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup the deck holds 36 cards: for each of 5 colours, values 1,1,2,2,3,4 (30 colour cards), plus 6 Church cards. It is shuffled once and hidden from everyone."},
    {"id": "R2", "text": "At setup every player has 8 gold and every colour's public worth is 4."},
    {"id": "R3", "text": "The game lasts exactly 12 rounds."},
    {"id": "R4", "text": "The active seat in rounds 1 to 12 is 1, 2, 3, 1, 2, 3, 3, 2, 1, 3, 2, 1."},
    {"id": "R5", "text": "At the start of each round, the round number, active seat, all five public worths, all gold totals and all public collections are announced."},
    {"id": "R6", "text": "Each round the top two deck cards are removed from the deck and shown only to the active player, as Card A (top) and Card B (next)."},
    {"id": "R7", "text": "When the active player chooses Keep A, Card A goes to their hidden collection and Card B becomes the publicly announced lot; Keep B does the reverse."},
    {"id": "R8", "text": "The identity of the kept card is never announced during play."},
    {"id": "R9", "text": "Each round every player writes one short message simultaneously, and all messages are then shown to everyone; they bind no one."},
    {"id": "R10", "text": "Each round all three players, including the active player, bid simultaneously a whole number from 0 to their current gold."},
    {"id": "R11", "text": "When the highest bid is at least 1 and no other player bid that amount, that player wins the lot and loses gold equal to their bid, which leaves the game."},
    {"id": "R12", "text": "When the highest bid is 0, or two or more players tie for the highest bid, nobody pays and the lot is discarded face-up."},
    {"id": "R13", "text": "When the won lot is a colour card, it goes into the winner's public collection."},
    {"id": "R14", "text": "Every round the active player privately names one colour and a direction (+1 or -1), which is recorded secretly in their marks."},
    {"id": "R15", "text": "A mark counts at scoring only if the card the active player kept that round is a Church card; otherwise it is void."},
    {"id": "R16", "text": "When a Church lot is won, the winner publicly names a colour and a direction (+1 or -1), and that colour's public worth changes by 1 in that direction."},
    {"id": "R17", "text": "When a public worth change would take a worth below 2 or above 8, it has no effect."},
    {"id": "R18", "text": "A won Church card is discarded face-up after its effect, and an unwon Church lot changes no worth."},
    {"id": "R19", "text": "When the active player also wins a Church lot, they answer both the secret mark and the public Church question."},
    {"id": "R20", "text": "Secret marks change no public worth during play."},
    {"id": "R21", "text": "At the end of every round each player gains 1 gold."},
    {"id": "R22", "text": "At scoring, all hidden collections are revealed, and counting marks are applied to the public worths one at a time in round order, earliest first, each by 1 in its direction, with any mark that would go below 2 or above 8 having no effect."},
    {"id": "R23", "text": "At scoring, each player's colour total is the sum of that colour's card values in their hidden and public collections; Church cards count 0."},
    {"id": "R24", "text": "When one player has the strictly highest total of a colour and it is at least 1, they score VP equal to that colour's final worth."},
    {"id": "R25", "text": "When two or more players tie for the highest total of a colour (at least 1), each scores floor(final worth / 2) VP."},
    {"id": "R26", "text": "When no player has a card of a colour, nobody scores that colour."},
    {"id": "R27", "text": "At scoring each player gains floor(gold / 5) VP."},
    {"id": "R28", "text": "After scoring in round 12 the game ends, and the player with the most VP wins; players tied for most VP share the result."}
  ],
  "offers": [
    {"question": "Keep a card", "who": "the active seat only", "options": "Keep A, Keep B"},
    {"question": "Talk message", "who": "every seat", "options": "a short free-text message"},
    {"question": "Sealed bid", "who": "every seat", "options": "a whole number from 0 to that seat's current gold"},
    {"question": "Secret mark (part a)", "who": "the active seat, every round", "options": "Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1"},
    {"question": "Church effect (part b)", "who": "the seat that won a Church lot, only in a round where a Church lot was won", "options": "Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1; any other seat is not asked"}
  ],
  "choices": [
    {"what": "Exactly 3 players (min 3, max 3, suggested 3)", "why": "The designer fixed the table at 3, and the active-seat schedule (1,2,3,1,2,3,3,2,1,3,2,1) is written for three seats. Three is also the smallest table where a sealed-bid tie can void a lot and a majority can be split. A thoughtful player bluffs about the kept card, reads others' bids and Church choices, and spends gold only where a majority is contestable."},
    {"what": "Keep the simultaneous talk step as a poll broadcast to all", "why": "The source requires it. It earns its place because players disagree about which colours should rise, and they can bluff about kept cards or try to steer bids."},
    {"what": "Cards named as text '<Colour> <value>' and 'Church'; the deck top is index 0 after the single setup shuffle", "why": "The source gives no card labels, and it needs a fixed hidden order with a top card."},
    {"what": "Marks stored as 'round:colour:direction:counts', with counts fixed when the mark is made", "why": "This lets scoring apply only counting marks, in round order, by arithmetic, without re-deriving which card was kept each round."},
    {"what": "Per-colour totals and final worths are explicit attributes computed at scoring", "why": "The majority rule needs these numbers stored as state to compare across players."},
    {"what": "The active player's choice of A or B is an ask to that seat alone", "why": "Only one player answers, and the answer is private."}
  ],
  "simplifications": [
    {"what": "Scoring runs as conditional steps (when round == 12) at the end of round 12 rather than as a separate phase", "why": "The step list is flat, so final scoring is gated by an arithmetic condition."},
    {"what": "A tie for most VP is shown as a shared win rather than a 'draw'", "why": "The engine has no separate draw; players level at the top share the win, which is the same outcome in effect."},
    {"what": "Parts (a) and (b) of step 9 are one poll addressed to the active seat and, when applicable, the Church winner", "why": "The source says they are answered at the same time; a seat that is both gets both questions in the same poll."}
  ],
  "unsupported": []
}
```

Why it was refused: parameters must map each name to a number
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "Biblios: Sealed Scriptorium (revised)",
  "summary": "Three scribes each round secretly keep one of two cards, then sealed-bid for the other, while public Church cards and secret marks shift the worth of five colours that score by majority.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "deck_size": 36,
    "colour_cards": 30,
    "church_cards": 6,
    "colours": 5,
    "cards_per_colour": 6,
    "value_1_cards_per_colour": 2,
    "value_2_cards_per_colour": 2,
    "value_3_cards_per_colour": 1,
    "value_4_cards_per_colour": 1,
    "starting_gold": 8,
    "starting_worth": 4,
    "worth_min": 2,
    "worth_max": 8,
    "rounds": 12,
    "cards_revealed_to_active": 2,
    "bid_min": 0,
    "min_winning_bid": 1,
    "gold_income_per_round": 1,
    "mark_step": 1,
    "church_step": 1,
    "tie_share_divisor": 2,
    "gold_per_vp": 5,
    "min_majority_total": 1
  },
  "attributes": {
    "player": [
      {"key": "gold", "type": "number", "visible": "public", "initial": 8, "meaning": "Gold held. Bids are paid from it, it gains 1 each round, and 1 VP is scored for every full 5 at the end.", "observable": true},
      {"key": "hidden_cards", "type": "list", "visible": "ally", "initial": [], "meaning": "Hidden collection: the cards this player kept as active player (colour cards such as 'Red 3', or 'Church'). It is revealed to all at scoring.", "observable": false},
      {"key": "public_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Public collection: the colour cards won at auction.", "observable": true},
      {"key": "marks", "type": "list", "visible": "ally", "initial": [], "meaning": "Secret marks, part of the hidden collection. There is one entry per round in which this player was active, recorded as 'round:colour:direction:counts', where counts is yes if the card kept that round was Church.", "observable": false},
      {"key": "offer_a", "type": "text", "visible": "ally", "initial": "", "meaning": "Card A (the top card) shown privately to this player while active.", "observable": false},
      {"key": "offer_b", "type": "text", "visible": "ally", "initial": "", "meaning": "Card B (the next card) shown privately to this player while active.", "observable": false},
      {"key": "kept_card", "type": "text", "visible": "ally", "initial": "", "meaning": "The card this player kept in the current round as active player.", "observable": false},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "This round's non-binding talk message.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "This round's sealed bid. It is revealed only after all bids are in.", "observable": false},
      {"key": "total_red", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Red card values in the hidden and public collections, computed at scoring.", "observable": false},
      {"key": "total_blue", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Blue card values, computed at scoring.", "observable": false},
      {"key": "total_green", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Green card values, computed at scoring.", "observable": false},
      {"key": "total_yellow", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Yellow card values, computed at scoring.", "observable": false},
      {"key": "total_purple", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Purple card values, computed at scoring.", "observable": false},
      {"key": "vp", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory points, computed at scoring.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["Red 1", "Red 1", "Red 2", "Red 2", "Red 3", "Red 4", "Blue 1", "Blue 1", "Blue 2", "Blue 2", "Blue 3", "Blue 4", "Green 1", "Green 1", "Green 2", "Green 2", "Green 3", "Green 4", "Yellow 1", "Yellow 1", "Yellow 2", "Yellow 2", "Yellow 3", "Yellow 4", "Purple 1", "Purple 1", "Purple 2", "Purple 2", "Purple 3", "Purple 4", "Church", "Church", "Church", "Church", "Church", "Church"], "meaning": "The draw pile, shuffled once at setup. Index 0 is the top card.", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "The current round number, from 1 to 12.", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat of this round's active player.", "observable": true},
      {"key": "worth_red", "type": "number", "visible": "public", "initial": 4, "meaning": "Red public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_blue", "type": "number", "visible": "public", "initial": 4, "meaning": "Blue public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_green", "type": "number", "visible": "public", "initial": 4, "meaning": "Green public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_yellow", "type": "number", "visible": "public", "initial": 4, "meaning": "Yellow public die worth, from 2 to 8.", "observable": true},
      {"key": "worth_purple", "type": "number", "visible": "public", "initial": 4, "meaning": "Purple public die worth, from 2 to 8.", "observable": true},
      {"key": "lot", "type": "text", "visible": "public", "initial": "", "meaning": "The card put up for auction this round.", "observable": true},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up discards: unwon lots and won Church cards.", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "The highest bid this round.", "observable": false},
      {"key": "high_count", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players bid the highest amount this round.", "observable": false},
      {"key": "winner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat that won this round's lot, or 0 if nobody won it.", "observable": true},
      {"key": "final_worth_red", "type": "number", "visible": "public", "initial": 4, "meaning": "Red worth after the counting marks are applied at scoring.", "observable": false},
      {"key": "final_worth_blue", "type": "number", "visible": "public", "initial": 4, "meaning": "Blue final worth.", "observable": false},
      {"key": "final_worth_green", "type": "number", "visible": "public", "initial": 4, "meaning": "Green final worth.", "observable": false},
      {"key": "final_worth_yellow", "type": "number", "visible": "public", "initial": 4, "meaning": "Yellow final worth.", "observable": false},
      {"key": "final_worth_purple", "type": "number", "visible": "public", "initial": 4, "meaning": "Purple final worth.", "observable": false}
    ]
  },
  "setup": [
    "Build the deck list of 36 cards: for each of Red, Blue, Green, Yellow and Purple, the cards '<Colour> 1', '<Colour> 1', '<Colour> 2', '<Colour> 2', '<Colour> 3' and '<Colour> 4', plus six 'Church' cards.",
    "Shuffle the deck once into a random order. Its order is hidden from everyone (visibility none).",
    "Set every player's gold to 8, set hidden_cards, public_cards and marks to empty, and set vp to 0.",
    "Set worth_red, worth_blue, worth_green, worth_yellow and worth_purple to 4, round to 0 and discard to empty."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1. If round <= 6, active_seat = ((round - 1) mod 3) + 1; otherwise active_seat = 3 - ((round - 7) mod 3). This gives seats 1,2,3,1,2,3,3,2,1,3,2,1. Reset winner_seat = 0, high_bid = 0, high_count = 0 and every bid = 0."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce round, active_seat, worth_red, worth_blue, worth_green, worth_yellow, worth_purple, every player's gold and every player's public_cards."},
    {"action": "update", "who": "seat {active_seat}", "answer": null, "effect": "Set the active player's offer_a = deck[0] and offer_b = deck[1]. Remove both from deck. Nothing is announced."},
    {"action": "sync", "who": "seat {active_seat}", "answer": null, "effect": "The active player privately sees offer_a as Card A and offer_b as Card B."},
    {"action": "ask", "who": "seat {active_seat}", "answer": "choice: Keep A | Keep B", "effect": "The answer is private. If Keep A, kept_card = offer_a and lot = offer_b; if Keep B, kept_card = offer_b and lot = offer_a. Append kept_card to the active player's hidden_cards."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce publicly: 'This round's lot is {lot}.' Nothing about the kept card is announced."},
    {"action": "poll", "who": "all players", "answer": "short text", "effect": "message = the answer. Once all are in, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Messages are not binding."},
    {"action": "poll", "who": "all players", "answer": "whole number from 0 to you.gold", "effect": "bid = the answer. No bid is seen until all three are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Reveal every bid publicly. high_bid = max of bid over players; high_count = number of players with bid == high_bid. If high_bid >= 1 and high_count == 1, then winner_seat = the seat with that bid, and that player's gold -= high_bid (paid to the bank and removed from the game). Otherwise winner_seat = 0, nobody pays, and lot is appended to discard (face-up)."},
    {"action": "update", "who": "seat {winner_seat}", "answer": null, "effect": "when winner_seat != 0 and lot != 'Church': append lot to the winner's public_cards."},
    {"action": "poll", "who": "seat {active_seat}; also seat {winner_seat} when winner_seat != 0 and lot == 'Church'", "answer": "(a) for the active seat, privately: a choice of colour and direction from Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1; (b) for the Church winner, publicly: the same ten options. A seat that is both answers both questions.", "effect": "(a) Append 'round:colour:direction:counts' to the active player's marks, where counts = yes if kept_card == 'Church', otherwise no. This changes no worth now. (b) The answer is recorded for the next step and announced publicly."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when winner_seat != 0 and lot == 'Church': for the named colour, if worth + direction is between 2 and 8 inclusive, then worth_<colour> += direction; otherwise no change. Append the Church card to discard (face-up). Announce the new worth."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Every player's gold += 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round == 12: reveal every player's hidden_cards and marks to all. Set each final_worth_<colour> = worth_<colour>. Then take every mark with counts = yes, from all players, sorted by round ascending, and apply them one at a time: if final_worth_<colour> + direction is between 2 and 8 inclusive, final_worth_<colour> += direction; otherwise the mark has no effect. Each mark is checked against the worth as already changed by earlier marks."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round == 12: for each player and each colour, total_<colour> = sum of the numeric values of that colour's cards in hidden_cards and public_cards together. Church cards count 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round == 12: for each colour, M = max of total_<colour> over players and K = number of players with total_<colour> == M. If M >= 1 and K == 1, that player's vp += final_worth_<colour>. If M >= 1 and K >= 2, each tied player's vp += floor(final_worth_<colour> / 2). If M == 0, nobody scores the colour. Then every player's vp += floor(gold / 5). Announce every player's final worths, totals and vp."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round == 12, end the game; otherwise begin the next round."}
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.vp",
    "decided_by": "Each player's standing is their VP after scoring: colour majorities at final worths plus 1 VP per full 5 gold. The highest VP wins; players tied at the top share the result (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup the deck holds 36 cards: for each of 5 colours, values 1,1,2,2,3,4 (30 colour cards), plus 6 Church cards. It is shuffled once and hidden from everyone."},
    {"id": "R2", "text": "At setup every player has 8 gold and every colour's public worth is 4."},
    {"id": "R3", "text": "The game lasts exactly 12 rounds."},
    {"id": "R4", "text": "The active seat in rounds 1 to 12 is 1, 2, 3, 1, 2, 3, 3, 2, 1, 3, 2, 1."},
    {"id": "R5", "text": "At the start of each round, the round number, active seat, all five public worths, all gold totals and all public collections are announced."},
    {"id": "R6", "text": "Each round the top two deck cards are removed from the deck and shown only to the active player, as Card A (top) and Card B (next)."},
    {"id": "R7", "text": "When the active player chooses Keep A, Card A goes to their hidden collection and Card B becomes the publicly announced lot; Keep B does the reverse."},
    {"id": "R8", "text": "The identity of the kept card is never announced during play."},
    {"id": "R9", "text": "Each round every player writes one short message simultaneously, and all messages are then shown to everyone; they bind no one."},
    {"id": "R10", "text": "Each round all three players, including the active player, bid simultaneously a whole number from 0 to their current gold."},
    {"id": "R11", "text": "When the highest bid is at least 1 and no other player bid that amount, that player wins the lot and loses gold equal to their bid, which leaves the game."},
    {"id": "R12", "text": "When the highest bid is 0, or two or more players tie for the highest bid, nobody pays and the lot is discarded face-up."},
    {"id": "R13", "text": "When the won lot is a colour card, it goes into the winner's public collection."},
    {"id": "R14", "text": "Every round the active player privately names one colour and a direction (+1 or -1), which is recorded secretly in their marks."},
    {"id": "R15", "text": "A mark counts at scoring only if the card the active player kept that round is a Church card; otherwise it is void."},
    {"id": "R16", "text": "When a Church lot is won, the winner publicly names a colour and a direction (+1 or -1), and that colour's public worth changes by 1 in that direction."},
    {"id": "R17", "text": "When a public worth change would take a worth below 2 or above 8, it has no effect."},
    {"id": "R18", "text": "A won Church card is discarded face-up after its effect, and an unwon Church lot changes no worth."},
    {"id": "R19", "text": "When the active player also wins a Church lot, they answer both the secret mark and the public Church question."},
    {"id": "R20", "text": "Secret marks change no public worth during play."},
    {"id": "R21", "text": "At the end of every round each player gains 1 gold."},
    {"id": "R22", "text": "At scoring, all hidden collections are revealed, and counting marks are applied to the public worths one at a time in round order, earliest first, each by 1 in its direction; any mark that would go below 2 or above 8 has no effect."},
    {"id": "R23", "text": "At scoring, each player's colour total is the sum of that colour's card values in their hidden and public collections; Church cards count 0."},
    {"id": "R24", "text": "When one player has the strictly highest total of a colour and it is at least 1, they score VP equal to that colour's final worth."},
    {"id": "R25", "text": "When two or more players tie for the highest total of a colour (at least 1), each scores floor(final worth / 2) VP."},
    {"id": "R26", "text": "When no player has a card of a colour, nobody scores that colour."},
    {"id": "R27", "text": "At scoring each player gains floor(gold / 5) VP."},
    {"id": "R28", "text": "After scoring in round 12 the game ends, and the player with the most VP wins; players tied for most VP share the result."}
  ],
  "offers": [
    {"question": "Keep a card", "who": "the active seat only", "options": "Keep A, Keep B"},
    {"question": "Talk message", "who": "every seat", "options": "a short free-text message"},
    {"question": "Sealed bid", "who": "every seat", "options": "a whole number from 0 to that seat's current gold"},
    {"question": "Secret mark (part a)", "who": "the active seat, every round", "options": "Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1"},
    {"question": "Church effect (part b)", "who": "the seat that won a Church lot, only in a round where a Church lot was won", "options": "Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1; any other seat is not asked"}
  ],
  "choices": [
    {"what": "Exactly 3 players (min 3, max 3, suggested 3)", "why": "The designer fixed the table at 3, and the active-seat schedule (1,2,3,1,2,3,3,2,1,3,2,1) is written for three seats. Three is also the smallest table where a sealed-bid tie can void a lot and a majority can be split. A thoughtful player bluffs about the kept card, reads the others' bids and Church choices, and spends gold only where a majority can still be won."},
    {"what": "Keep the simultaneous talk step as a poll broadcast to all", "why": "The source requires it. It earns its place because players disagree about which colours should rise, and they can bluff about kept cards or try to steer bids."},
    {"what": "Cards are named as text '<Colour> <value>' and 'Church'; the top of the deck is index 0 after the single setup shuffle", "why": "The source gives no card labels, and it needs a fixed hidden order with a top card."},
    {"what": "Card values per colour are given as counts per value in parameters (two 1s, two 2s, one 3, one 4)", "why": "Every parameter must be a number."},
    {"what": "Marks are stored as 'round:colour:direction:counts', with counts fixed when the mark is made", "why": "This lets scoring apply only the counting marks, in round order, by arithmetic, without working out again which card was kept each round."},
    {"what": "Per-colour totals and final worths are explicit attributes computed at scoring", "why": "The majority rule needs these numbers stored as state so they can be compared across players."},
    {"what": "The active player's choice of A or B is an ask to that seat alone", "why": "Only one player answers, and the answer is private."}
  ],
  "simplifications": [
    {"what": "Scoring runs as conditional steps (when round == 12) at the end of round 12 rather than as a separate phase", "why": "The step list is flat, so final scoring is gated by an arithmetic condition."},
    {"what": "A tie for most VP is shown as a shared win rather than a 'draw'", "why": "The engine has no separate draw; players level at the top share the win, which is the same outcome in effect."},
    {"what": "Parts (a) and (b) of step 9 are one poll addressed to the active seat and, when it applies, the Church winner", "why": "The source says they are answered at the same time; a seat that is both gets both questions in the same poll."}
  ],
  "unsupported": []
}
```
````
