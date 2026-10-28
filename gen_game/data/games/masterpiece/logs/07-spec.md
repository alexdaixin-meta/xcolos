# 07 spec

- time: 2026-10-28T05:06:34+00:00 (57.5s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 7310b9aa8bf68c86, reply sha256 66dc67328138053a

## Sent

````
Game: Masterpiece: Secret Collectors
Players in the source: 4 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
MONEY: All amounts are in thousands of dollars. Bids and reserves are whole multiples of 50.

SETUP:
1. Seat the players 1 to 4 in a fixed circle. The player 'to the left' of player p is player p+1, and player 4's left is player 1.
2. Each player starts with 1500 cash. Cash is always public.
3. There are 4 public styles: Red, Blue, Gold and Green.
4. Each player receives 4 paintings, one of each style, with public names (for example 'P2-Gold'). Who owns which painting, and each painting's style, are always public.
5. Secret themes: the engine randomly gives each player a different style as their collector theme. Each player is told only their own theme. Everyone knows that the four themes are all different.
6. Painting values are dealt as follows.
   - Start from the pattern value(player p, style s) = [0, 300, 600, 1200][(p + s) mod 4], with players and styles indexed 0 to 3.
   - Then randomly shuffle which player is which row, which style is which column, and which value is which number.
   - The result: every player holds exactly one painting each worth 0, 300, 600 and 1200, and every style has exactly one painting of each of those values.
7. Each player is told privately the values of their own four paintings. A painting's value is known only to players who have owned it.

ROUNDS: The game has 12 rounds. The seller in round r is player ((r-1) mod 4) + 1, so each player sells 3 times. Each round:
1. ANNOUNCE: The engine names the seller. If the seller owns no paintings, skip to step 9.
2. LOT CHOICE: The player to the seller's left chooses one painting from the seller's current collection. The engine announces it, with its style, as the lot.
3. TALK: Every player, seller included, writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.
4. SEALED BIDS AND RESERVE: At the same moment, each non-seller submits a bid from 0 up to their current cash, and the seller submits a secret reserve from 0 to 2000.
5. HIGH BID: Let B be the highest bid. A tie goes to the tied bidder nearest the seller going clockwise (seller's left first).
6. RESOLVE:
   - If B > reserve, the high bidder pays B to the seller, takes the painting, and is told its value privately.
   - Otherwise the seller keeps the painting. If B is at least 50, the seller pays a fee of 50 to the bank, or all their cash if they have less than 50. Fee money leaves the game.
7. ANNOUNCE: The engine publishes all bids, whether the lot was sold or kept, the money moved and the new cash totals. The reserve and the painting's value are NOT published.
8. A painting that was bought can be chosen as a lot again later, when its new owner is the seller.
9. END CHECK: After round 12, go to scoring.

SCORING:
1. All values and themes are revealed.
2. Each player's score = cash + the total value of the paintings they own + 400 for each painting they own whose style is their own theme.

How the winner is decided: The highest score wins. If several players tie for the highest score, the one among them with the most cash wins. If they are still tied, the game is a draw.
````

## Reply

````
```json
{
  "name": "Masterpiece: Secret Collectors",
  "summary": "Four collectors take turns selling paintings in sealed-bid auctions against secret reserves, each guarding private knowledge of painting values and a secret theme style worth a 400 bonus per matching painting.",
  "players": {"min": 4, "max": 4, "suggested": 4},
  "parameters": {
    "starting_cash": 1500,
    "num_styles": 4,
    "paintings_per_player": 4,
    "value_low": 0,
    "value_mid_low": 300,
    "value_mid_high": 600,
    "value_high": 1200,
    "rounds": 12,
    "sales_per_player": 3,
    "bid_step": 50,
    "reserve_max": 2000,
    "bid_min": 0,
    "reserve_min": 0,
    "unsold_fee": 50,
    "fee_trigger_min_bid": 50,
    "theme_bonus": 400
  },
  "attributes": {
    "player": [
      {"key": "cash", "type": "number", "visible": "public", "initial": 1500, "meaning": "Cash in thousands of dollars. Always public.", "observable": true},
      {"key": "paintings", "type": "list", "visible": "public", "initial": "four painting names, one of each style, e.g. ['P2-Red','P2-Blue','P2-Gold','P2-Green']", "meaning": "Names of the paintings this player currently owns. Ownership and style are public; a name encodes its style.", "observable": true},
      {"key": "theme", "type": "text", "visible": "ally", "initial": "a random style, different for every player", "meaning": "Secret collector theme style. Each owned painting of this style is worth +400 at scoring. Revealed at the end.", "observable": false},
      {"key": "known_values", "type": "list", "visible": "ally", "initial": "'name=value' entries for the player's own four paintings", "meaning": "Painting values this player has learned: the values of every painting they have ever owned.", "observable": false},
      {"key": "bid", "type": "number", "visible": "ally", "initial": 0, "meaning": "Sealed bid this round (non-sellers). Published after resolution.", "observable": false},
      {"key": "reserve", "type": "number", "visible": "ally", "initial": 0, "meaning": "Secret reserve this round (seller only). Never published.", "observable": false},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "This round's talk message, shown to all after everyone has written.", "observable": false},
      {"key": "tie_priority", "type": "number", "visible": "public", "initial": 0, "meaning": "Scratch tie-break key this round: 3 for the seller's left, 2 for the next seat, 1 for the seat after that, 0 for the seller.", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Final score = cash + total value of owned paintings + 400 for each owned painting of the player's theme. Computed at game end.", "observable": true}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Current round number, 1 to 12.", "observable": true},
      {"key": "seller", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of this round's seller: ((round-1) mod 4) + 1.", "observable": true},
      {"key": "lot", "type": "text", "visible": "public", "initial": "", "meaning": "Name of the painting being auctioned this round.", "observable": true},
      {"key": "lot_style", "type": "text", "visible": "public", "initial": "", "meaning": "Style of the current lot.", "observable": false},
      {"key": "painting_values", "type": "list", "visible": "none", "initial": "16 'name=value' entries dealt from a shuffled Latin square of {0,300,600,1200}", "meaning": "True value of every painting. Hidden from all; each player learns only the values of paintings they have owned. Revealed at the end.", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest bid B this round.", "observable": true},
      {"key": "high_bidder", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the winning bidder after the tie-break.", "observable": true},
      {"key": "sold", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this round's lot was sold.", "observable": true}
    ]
  },
  "setup": [
    "Seat players 1 to 4 in a fixed circle; the left of seat p is seat p+1, and the left of seat 4 is seat 1.",
    "Every player's cash is set to 1500.",
    "Each player p receives four paintings named 'Pp-Red', 'Pp-Blue', 'Pp-Gold' and 'Pp-Green' in their paintings list.",
    "The four styles Red, Blue, Gold and Green are dealt at random as secret themes, one different style per player, each stored in that player's theme (ally).",
    "Painting values are built from the pattern value(p, s) = [0,300,600,1200][(p+s) mod 4], with players and styles indexed 0 to 3. Rows (players), columns (styles) and the value labels are then shuffled at random, so each player holds one painting each worth 0, 300, 600 and 1200, and each style has one painting of each value. The result is stored in painting_values (hidden).",
    "Each player's known_values is set to the values of their own four paintings, and the engine tells each player those values privately.",
    "Everyone is told that the four themes are all different."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; seller = ((round-1) mod 4) + 1; sold = false; high_bid = 0; high_bidder = 0; lot = ''; each player's bid = 0 and reserve = 0; tie_priority = 3 for seat ((seller) mod 4)+1, 2 for seat ((seller+1) mod 4)+1, 1 for seat ((seller+2) mod 4)+1, 0 for the seller. Announces the seller."},
    {"action": "ask", "who": "the seat to the seller's left: ((seller) mod 4) + 1", "answer": "one painting name from the seller's current paintings list", "effect": "when the seller's paintings list is not empty: lot = chosen name; lot_style = its style. The lot and its style are announced to all."},
    {"action": "poll", "who": "all players", "answer": "short text message", "effect": "when the seller's paintings list is not empty: each player's message = their text; afterwards broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk is not binding."},
    {"action": "poll", "who": "all players", "answer": "non-sellers: a whole number from 0 to their cash (bid); seller: a whole number from 0 to 2000 (reserve)", "effect": "when the seller's paintings list is not empty: each value is rounded down to a multiple of 50. Each non-seller's bid is set to their number; the seller's reserve is set to theirs. Nobody sees any answer until all are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when the seller's paintings list is not empty: high_bid = max over non-sellers of bid; high_bidder = the non-seller with the largest (bid * 10 + tie_priority)."},
    {"action": "update", "who": "seller and high bidder", "answer": null, "effect": "when the seller's paintings list is not empty: if high_bid > seller.reserve then sold = true; high_bidder.cash -= high_bid; seller.cash += high_bid; remove lot from seller.paintings; append lot to high_bidder.paintings; append the lot's 'name=value' entry from painting_values to high_bidder.known_values and tell the high bidder privately. Otherwise sold = false, and if high_bid >= 50 then seller.cash -= min(50, seller.cash), and that money leaves the game."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "when the seller's paintings list is not empty: publish every non-seller's bid, whether the lot was sold or kept, the money moved (price or fee) and every player's new cash. The reserve and the painting's value are not published."},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round == 12: reveal painting_values and every theme to all; each player's score = cash + sum of values of the paintings in their paintings list + 400 * (number of paintings in their list whose style equals their theme)."},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game if round == 12, otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.score * 100000 + you.cash",
    "decided_by": "Each player's standing is their score (cash + value of owned paintings + 400 per owned painting of their theme), with cash breaking ties. The highest wins; players still level on both score and cash share the win, which stands for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player has cash 1500 and owns exactly 4 paintings, one each of Red, Blue, Gold and Green."},
    {"id": "R2", "text": "When themes are dealt, then each of the 4 players has a different theme style, and each is told only their own."},
    {"id": "R3", "text": "When values are dealt, then each player holds one painting each worth 0, 300, 600 and 1200, and each style has exactly one painting of each of those values."},
    {"id": "R4", "text": "When values are dealt, then each player learns privately the values of their own 4 paintings and no other values."},
    {"id": "R5", "text": "When round r begins, then the seller is seat ((r-1) mod 4)+1, so seats 1, 2, 3, 4 sell in rounds 1, 2, 3, 4 and again in rounds 5 to 8 and 9 to 12."},
    {"id": "R6", "text": "When the seller owns no paintings, then the lot choice, talk, bids and resolution are skipped that round."},
    {"id": "R7", "text": "When a lot is chosen, then the chooser is the seat to the seller's left (seat seller mod 4 + 1), the lot is one of the seller's current paintings, and it is announced with its style."},
    {"id": "R8", "text": "When talk happens, then every player, seller included, submits one message at the same time, and all messages are shown to everyone afterwards."},
    {"id": "R9", "text": "When bids are made, then each non-seller bids a multiple of 50 from 0 to their current cash, and the seller sets a secret reserve that is a multiple of 50 from 0 to 2000, all at the same time."},
    {"id": "R10", "text": "When two or more bidders tie for the highest bid B, then the winner is the tied bidder nearest the seller going clockwise, the seller's left first."},
    {"id": "R11", "text": "When B > reserve, then the high bidder pays B to the seller, the lot moves to the high bidder's paintings, and the high bidder privately learns its value."},
    {"id": "R12", "text": "When B <= reserve and B >= 50, then the seller keeps the lot and pays a fee of 50 (or all their cash if under 50), which leaves the game."},
    {"id": "R13", "text": "When B <= reserve and B is 0, then the seller keeps the lot and pays no fee."},
    {"id": "R14", "text": "When an auction resolves, then all bids, sold or kept, the money moved and every new cash total are published, but not the reserve or the painting's value."},
    {"id": "R15", "text": "When a bought painting's new owner is the seller in a later round, then that painting may be chosen as the lot."},
    {"id": "R16", "text": "When round 12 ends, then the game ends, and all values and themes are revealed."},
    {"id": "R17", "text": "When scoring, then score = cash + the total value of owned paintings + 400 for each owned painting whose style equals the owner's theme."},
    {"id": "R18", "text": "When scores tie at the top, then the tied player with more cash wins, and players tied on both share the win (the draw)."}
  ],
  "offers": [
    {"question": "Lot choice", "who": "the seat to the seller's left", "options": "each painting name currently in the seller's paintings list; the step is not asked if that list is empty"},
    {"question": "Talk", "who": "all four seats", "options": "one short free-text message"},
    {"question": "Sealed bid", "who": "each non-seller", "options": "a whole number from 0 to their current cash, rounded down to a multiple of 50"},
    {"question": "Secret reserve", "who": "the seller", "options": "a whole number from 0 to 2000, rounded down to a multiple of 50"}
  ],
  "choices": [
    {"what": "Exactly 4 players (min 4, max 4, suggested 4)", "why": "The designer chose 4. The structure needs it: 4 styles, 4 distinct themes, a 4x4 Latin square of values and 3 sales per seat over 12 rounds. Fewer seats break the value deal, and more have no theme or values to receive."},
    {"what": "Talk kept as a simultaneous poll broadcast to all", "why": "The source requires simultaneous unbinding talk. It earns its place because interests conflict: sellers want to talk up lots, and bidders want to bluff their themes and known values."},
    {"what": "Tie-break encoded as bid*10 + tie_priority", "why": "Bids are multiples of 50, so adding a priority from 0 to 3 never changes the order of different bids. It ranks the seller's left first, as the rules say."},
    {"what": "Ranking expression score*100000 + cash", "why": "Scores stay well under 100000, so cash only breaks ties in score. Players tied on both share the win, which stands for the source's draw."},
    {"what": "Strategy at the table", "why": "A thoughtful player infers others' themes from their bids and talk, uses known values to bid on undervalued lots, sets reserves to protect theme paintings, and bluffs in talk. A thoughtless one bids on face value."}
  ],
  "simplifications": [
    {"what": "Bids and reserves are entered as whole numbers and rounded down to a multiple of 50", "why": "The engine takes a whole number in a range; rounding enforces the multiple-of-50 rule."},
    {"what": "The skip when the seller has no paintings is done with a 'when' condition on each step", "why": "The step list is flat; per-step conditions give the same effect without choosing a block of steps."},
    {"what": "Painting values are stored as 'name=value' text entries in lists", "why": "The engine has lists, not maps; each player's known_values plays the role of 'values known to past owners'."},
    {"what": "Bids and the reserve are gathered in one simultaneous poll with different ranges per seat", "why": "The source makes them simultaneous; one poll keeps every answer hidden until all are in."}
  ],
  "unsupported": []
}
```
````
