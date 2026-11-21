# 11 coder

- time: 2026-11-21T01:28:13+00:00 (55.5s)  model: rl-muse-spark-1-3-sglang-playground
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 016d0aa7cb7c2bec, reply sha256 7194d0d93542cf71

## Sent (the whole conversation)

````
[
  {
    "role": "user",
    "content": "# Task: write the XColos game file for \"For Sale: Sealed Bids - Four Player\"\n\nWrite the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.\n\n## The game\n\nPlayers: 4 to 4; set `meta.players` to {\"min\": 4, \"max\": 4, \"suggested\": 4} (the suggested size is the one the game plays best at).\n\nSETUP. 4 players numbered 1, 2, 3, 4. Each starts with 18 coins (private) and 0 cheques (private cheque total) and empty property hand (public). Property deck: cards 1 to 30, one each. Cheque deck: values 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15, two of each, 30 cheques. Game lasts 14 rounds: rounds 1-7 BUYING, rounds 8-14 SELLING. No talk phase: every choice is sealed to preserve bluff; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW. BUYING ROUND (rounds 1-7): 1. In round 1 only, shuffle the property deck. Only the top 28 cards will ever be used; the bottom 2 stay unseen. 2. Reveal the next 4 cards from the property deck. Sort them and call them HIGH, SECOND, THIRD, LOW by value. 3. All players at the same moment secretly submit a bid: whole number 0 up to current coins. 4. Rank bids highest to lowest. Break ties by priority order: in round r priority goes first to player ((r-1) mod 4)+1, then next number wrapping 4 to 1. 5. First-ranked takes HIGH and pays full bid. Second-ranked takes SECOND and pays half bid rounded UP. Third-ranked takes THIRD and pays half bid rounded UP. Fourth-ranked takes LOW and pays half bid rounded UP. Example: bid 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. 6. Payments go to the bank from private coins. 7. Announce publicly which player took HIGH, SECOND, THIRD, LOW. Bid amounts and coin totals are NOT announced. After round 7 each holds 7 properties. SELLING ROUND (rounds 8-14): 1. In round 8 only, shuffle the cheque deck. Only the top 28 cheques will ever be used; bottom 2 unseen. 2. Reveal the next 4 cheques from the cheque deck, sorted highest to lowest. 3. All players at the same moment secretly choose one property from own hand. 4. Reveal chosen properties. All properties are different so no ties. 5. Highest property adds highest cheque to cheque total; second-highest adds second-highest cheque; third adds third; lowest adds lowest. 6. Played properties are discarded. 7. Announce publicly who played which property and who took which cheque. Running cheque totals stay private. END. After round 14 hands are empty. Reveal cheque totals, remaining coins, and final money = cheque total + remaining coins.\n\nHow the winner is decided: Player with most final money (cheques plus remaining coins) wins. If tied for most, tied player with more remaining coins wins. If still tied, game is a draw among them.\n\n## The game as a script\n\nThis is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the\nfile step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`\nthat really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check\nthat fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.\n\nGAME: For Sale: Sealed Bids - Four Player (4 to 4 players, best with 4)\n\nBid secretly for properties then sell them secretly for cheques; richest total wins.\n\nSTATE (every item below must exist in the file):\n  - each player: coins (number, starts 18); only its owner sees it. remaining private coins for bidding\n  - each player: cheque_total (number, starts 0); only its owner sees it. sum of cheques won kept private until end\n  - each player: properties (list, starts []); everyone sees it. property cards held in hand public\n  - each player: bid (number, starts 0); only its owner sees it. sealed bid submitted this buying round\n  - each player: selected_property (number, starts 0); only its owner sees it. property chosen to sell this selling round\n  - each player: final_money (number, starts 0); everyone sees it. cheque_total plus remaining coins revealed at end\n  - the table: property_deck (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]); hidden from all players. unseen property cards 1 to 30\n  - the table: cheque_deck (list, starts [0, 0, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15]); hidden from all players. unseen cheques 0 and 2 to 15 two each\n  - the table: current_offer (list, starts []); everyone sees it. 4 properties or cheques revealed this round sorted high to low\n  - the table: round_number (number, starts 1); everyone sees it. current round 1 to 14\n  - the table: priority_seat (number, starts 1); everyone sees it. first seat in tie break order this round\n  - the table: property_discard (list, starts []); everyone sees it. played properties discarded\n  - parameters, each kept as a table attribute: starting_coins = 18, property_low = 1, property_high = 30, property_deck_size = 30, property_deck_used = 28, cheque_low = 0, cheque_high = 15, cheque_copies = 2, cheque_deck_size = 30, cheque_deck_used = 28, total_rounds = 14, buying_rounds = 7, selling_rounds = 7, cards_per_round = 4\n\nINITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):\n  1. Give each of seats 1 to 4 exactly 18 coins, 0 cheque_total, 0 final_money and empty properties hand.\n  2. Build property_deck as cards 1 to 30 one each and cheque_deck as 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15 two each for 30 cheques.\n  3. Set round_number to 1 and current_offer to empty and property_discard to empty.\n  4. Only the top 28 properties and top 28 cheques will ever be used and the bottom 2 of each deck stay unseen.\n  5. There is no talk phase and all choices are sealed.\n\nEACH ROUND (steps in order; the round repeats until an ending):\n  1. [initialize] all players. What happens: set coins to 18 cheque_total to 0 properties to [] bid to 0 selected_property to 0 final_money to 0 property_deck to 1 to 30 cheque_deck to 0,0,2,2 to 15,15 round_number to 1 current_offer to []\n  2. [sync] all players. What happens: send each player their coins cheque_total and properties\n  3. [update] all players. What happens: when round_number is 1 remove 2 unseen cards from property_deck then move next 4 cards from property_deck to current_offer sorted HIGH SECOND THIRD LOW and set priority_seat to ((round_number-1) mod 4)+1\n  4. [poll] all players answers: {'type': 'number', 'min': 0, 'max': 'coins'}. What happens: set you.bid to sealed bid 0 up to you.coins\n  5. [update] all players. What happens: rank bids high to low breaking ties by priority_seat order wrapping 4 to 1 then first-ranked takes HIGH and pays full bid from coins second takes SECOND and pays (bid+1)//2 third takes THIRD and pays (bid+1)//2 fourth takes LOW and pays (bid+1)//2 and append taken property to you.properties\n  6. [tell] all players. What happens: broadcast which player took HIGH SECOND THIRD LOW without revealing bid amounts or coin totals\n  7. [update] all players. What happens: when round_number is 8 remove 2 unseen cheques from cheque_deck then move next 4 cheques from cheque_deck to current_offer sorted highest to lowest\n  8. [poll] all players answers: {'type': 'choice', 'from': 'you.properties'}. What happens: set you.selected_property to one property from you.properties\n  9. [update] all players. What happens: rank selected_property high to low with no ties then highest adds highest cheque in current_offer to cheque_total second-highest adds second-highest third adds third lowest adds lowest and remove selected_property from you.properties to property_discard\n  10. [tell] all players. What happens: broadcast who played which property and who took which cheque without revealing running cheque totals\n  11. [update] all players. What happens: set round_number to round_number+1 and if round_number>14 set you.final_money to you.cheque_total+you.coins\n  12. [check] all players. What happens: end the game when round_number>14 else continue\n\nRULES (each is tested by an independent scenario; the game must play every one exactly):\n  R1. When the game starts, then each of 4 players holds 18 coins, 0 cheque_total and empty properties hand.\n  R2. When built, then property_deck holds cards 1 to 30 one each for 30 cards.\n  R3. When built, then cheque_deck holds values 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15 two of each for 30 cheques.\n  R4. When the game runs, then rounds 1 to 7 are buying and rounds 8 to 14 are selling for 14 rounds total.\n  R5. When decks are prepared, then only the top 28 properties and top 28 cheques are ever used and the bottom 2 stay unseen.\n  R6. When a buying round starts, then reveal the next 4 property cards sorted HIGH SECOND THIRD LOW by value.\n  R7. When bidding, then all players at the same moment secretly submit a whole-number bid from 0 up to current coins.\n  R8. When bids are ranked, then rank highest to lowest and break ties by priority order starting at seat ((r-1) mod 4)+1 then next wrapping 4 to 1 in round r.\n  R9. When buying resolves, then first-ranked takes HIGH and pays full bid and second-ranked takes SECOND and pays half rounded up and third takes THIRD and pays half rounded up and fourth takes LOW and pays half rounded up where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2.\n  R10. When payments are made, then they go to the bank from private coins.\n  R11. When a buying round ends, then announce publicly which player took HIGH SECOND THIRD LOW and do not announce bid amounts or coin totals.\n  R12. When round 7 ends, then each player holds 7 properties.\n  R13. When a selling round starts, then reveal the next 4 cheques sorted highest to lowest.\n  R14. When selling, then all players at the same moment secretly choose one property from own hand.\n  R15. When chosen properties are revealed, then all properties are different so there are no ties.\n  R16. When cheques are awarded, then highest property adds highest cheque to cheque total and second-highest adds second-highest and third adds third and lowest adds lowest.\n  R17. When cheques are awarded, then played properties are discarded.\n  R18. When a selling round ends, then announce publicly who played which property and who took which cheque and keep running cheque totals private.\n  R19. When round 14 ends, then hands are empty and cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed.\n  R20. When the game ends, then the player with most final money wins.\n  R21. When players tie for most final money, then the tied player with more remaining coins wins and if still tied the game is a draw among them.\n  R22. When choices are made, then there is no talk phase and every choice is sealed.\n\nOFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):\n  - sealed bid | asked: all players | options: in buying rounds 1 to 7: any whole number 0 up to your current coins\n  - choose property to sell | asked: all players | options: in selling rounds 8 to 14: any one property from your own properties hand (7 options in round 8 down to 1 option in round 14)\n\nEVALUATION (how the game ends and who wins; decided by calculation):\n  - the game ends when: round_number > 14\n  - each player's standing: you.final_money * 1000 + you.coins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)\n  - how the result is decided: Standing is final_money equal to cheque_total plus remaining coins with remaining coins as tie-break; highest value wins and players level at the top share the win\n  - the end screen states the final scores or deciding figures, and a short model-written summary of how the game went\n\n## Recipe: a shared deck and hidden hands (tested on the engine)\n\nWhen the script has a deck and hands, both must exist as attributes, and setup must really deal. Declare the hand as a PLAYER attribute\n`{\"key\": \"hand\", \"visible\": \"ally\", \"type\": \"list\", \"initial\": []}` (only its owner sees it; a player attribute is never `none`) and the\ndeck as a TABLE attribute `{\"key\": \"deck\", \"visible\": \"none\", \"type\": \"list\", \"initial\": [every card, one entry per copy]}`, plus a table text\nattribute `pick` (visible `none`, initial `\"\"`) to hold the card just drawn. Then ONE draw, of a random card into seat N's hand, is three operations\nin an `update`'s `do` list, in this order:\n\n  {\"set\":    {\"key\": \"pick\", \"value\": {\"calc\": \"deck[int(uniform(0, len(deck)))]\"}}},\n  {\"append\": {\"player\": N, \"key\": \"hand\", \"value\": {\"calc\": \"pick\"}}},\n  {\"remove\": {\"key\": \"deck\", \"value\": {\"calc\": \"pick\"}}}\n\nDealing two cards to three seats is that block repeated twice for each seat (6 draws), never a fixed list written into `initial`: the deal\nis random and different each match, and every player's hand must differ. A card coming back is `{\"append\": {\"key\": \"deck\", ...}}` and\n`{\"remove\": {\"player\": N, \"key\": \"hand\", ...}}`. \"Has a card of role R\" is `\"R\" in you.hand`. Use `{\"if\": {\"calc\": ...}}` on an operation to make\nit conditional. Never declare `hand` or `deck` and then leave them unchanged: the rules would then claim cards that do not exist.\n\n## Pattern: offer each seat only what it may do (tested on the engine)\n\nA question's options may come from state, and the state can differ for every player. So make who may do what part of the OFFER, never a check\nafterwards. Declare a PLAYER list attribute (say `offer`, visible `ally`), and set it for everyone in one `update` just before the question,\nfrom each player's own attributes and the table's:\n\n  {\"set\": {\"players\": \"all\", \"key\": \"offer\",\n           \"value\": {\"calc\": \"['wait'] + (['buy'] if you.coins >= price else []) + (['block'] if you.seat == target else [])\"}}}\n\nthen ask with `\"answer\": {\"type\": \"choice\", \"options\": {\"attribute\": \"offer\"}}` and `to` naming who is asked. `you` is each player in turn, and a\nlist can be built with `+` and `(... if ... else [])`. Whatever a seat may not do is not in its list: a seat that cannot pay is not offered the\npaid action, only the target of an action is offered a block against it, a player already out is not asked. Do the same for a target: put the\nlegal seats in a list attribute.\n\nWhen only one option is left (the last unused action, the only legal card), still ask the question: the engine answers a choice with one\noption for the seat, with no model call, and records it as the seat's move. Do not skip the question with a `when` and set the answer\nyourself: that move is then missing from the match, and a test that scripts it fails.\n\nWhen a player is eliminated, set the PLATFORM status as well as your own counters: declare a status for it (`{\"id\": \"out\", \"acts\": false}`) next to `playing` and\nrun `{\"set_status\": {\"player\": N, \"to\": \"out\", \"text\": \"Seat {player} is out.\"}}`. Without it the platform and the console show the player as still in the game, and the\nprompts list them as playing, whatever your own `alive` attribute says. Name the cards it reveals in the same announcement.\n\nDo NOT offer a broad list and then refuse illegal answers and ask again (a `repeat` that asks, checks, and asks again, or an update that removes\nan option the player just picked). It costs a model call, it lets a model choose something illegal, and the pipeline reports it as a failure:\n\"an option is offered and then refused\". If you find yourself writing a step called \"refuse...\", \"check the answer is legal\" or \"not allowed\",\nyou are filling the wrong list: fix the offer.\n\n## Rounds and the safety cap\n\nIf the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed\nround count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of\nrounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap\nis reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.\n\n## The interface the file must use\n\nIndependent tests were written against these names and you cannot see them, so use them exactly.\n\n- each player: `properties` (list, visible: public, starts []): property cards held in hand public\n- each player: `final_money` (number, visible: public, starts 0): cheque_total plus remaining coins revealed at end\n- the table: `current_offer` (list, visible: public, starts []): 4 properties or cheques revealed this round sorted high to low\n- parameters (each must be an attribute holding this value, never a number buried in a step): starting_coins = 18, property_low = 1, property_high = 30, property_deck_size = 30, property_deck_used = 28, cheque_low = 0, cheque_high = 15, cheque_copies = 2, cheque_deck_size = 30, cheque_deck_used = 28, total_rounds = 14, buying_rounds = 7, selling_rounds = 7, cards_per_round = 4\n- the game ends with ONE ending whose `rank_by` is `you.final_money * 1000 + you.coins`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win\n- anything else the game needs to keep track of is yours to design: name it as you like.\n\n## How the platform works\n\nThe complete file format reference and two example games are in your system prompt. Follow them exactly: every key an\naction accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: write ONE\nending, whose `when` is a calc condition and whose `rank_by` is the ranking in the interface below; no `result`, no `winner`, no prose\nending, no `llm` in an ending. Use calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when` `{\"prose\": \"<the judged sentence, verbatim>\"}`: a referee answers it\ntrue or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no\nmodel answers. Choices made at the same moment are a `poll`. The end screen announces only the result: the ending's `text` says who won (`{result}`) and the final scores or deciding figures with\nplaceholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with `rank_by` as both examples do.\n\n- Mistakes the loader has refused before, so avoid them:\n  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table\n    attributes.) For something only its owner should see, use `ally`.\n  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.\n  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on\n    attributes, or with `set` operations in `setup`, instead.\n  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.\n  * TALK that everyone hears is a `poll` with a free-text answer and `\"broadcast\": {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}`\n    (or `\"broadcast\": \"all\"` with no `text`, which shows each message word for word). A broadcast may use ONLY `{value}` (what that\n    player answered), `{seat}` (who) and table attributes: a name bound by `verify` is not set yet, so `{talk_msg}` reaches players as\n    the literal braces, and the loader refuses it.\n  * WHO answered what (who challenged, who blocked, who raised a hand) is `\"store\": \"attr\"` on the `poll` or `ask`, naming a PLAYER\n    attribute declared under `attributes.player` (a `text` attribute for a choice). Each player's own answer is written to it and a calc reads\n    them all: `count(p.said == 'Challenge' for p in players)`, `min([p.seat for p in players if p.said == 'Challenge'])`. A `verify`\n    tally gives ONE winning value and loses who gave which: one \"Challenge\" against three \"Pass\" tallies to \"Pass\". Never write a seat\n    number into a calc by guessing (`2 if active_seat == 1 else 1`); read it from a stored answer. Reset the stored attribute with a `set`\n    to `\"\"` (`players: \"all\"`) before each poll, so last round's answers do not count.\n  * `meta.players` carries `min`, `max` and `suggested`, exactly as the task gives them: the console fills a table to the suggested size and the real-model tests play at it.\n  * THE RULES TEXT SAYS BOTH OUTCOMES. For every decision point (a challenge, a block, a claim, a cost), say what happens when it is true AND when it is false,\n    and whether the action still goes ahead; a player decides on this text and nothing else, and a check compares it with each numbered rule.\n  * THE RULES TEXT PLAYERS READ IS THE DESIGN'S. `meta.rules` (the brief) says each mechanic in the design's own words and in its order: how a challenge is resolved,\n    what a block costs, who counts when several answer. Do not paraphrase a mechanic: a reordered sentence is a different rule.\n  * BOOKKEEPING IS HIDDEN. An attribute that only the game's own steps read (a scratch value, a counter, a copy of an option list, who is blocking) is declared\n    hidden (`none` on the table, `ally` on a player), not `public`: every public attribute is printed into every player's prompt on every turn.\n  * THE DEAL REMOVES WHAT IT DEALS. Every card put into a hand is taken out of the deck in the same step (see the deck recipe); after setup, deck plus hands holds\n    exactly the cards the rules start with, and no card appears more often than the rules say.\n  * OFFER ONLY WHAT A SEAT MAY DO. Build each seat's option list from its own state (see the offer pattern) and never refuse an answer afterwards\n    and ask again: an option that is offered, taken and then taken back fails the pipeline's check.\n  * A QUESTION WITH ONE POSSIBLE ANSWER IS NEVER WORTH ASKING (\"pass\" and nothing else): the engine answers it itself, but write the step so\n    it is not asked at all, and never announce a seat's answer when the seat was not asked (eliminated players).\n  * ASK ONLY WHAT IS NEEDED. Put a `when` on a question that applies only sometimes: a target is asked only for the actions that take one\n    (`\"when\": {\"calc\": \"chosen_action in ['Steal', 'Assassinate', 'Coup']\"}`), a block only when something can be blocked.\n  * A counter must not go below what the rules allow. Guard every payment and loss with an `if` (`\"if\": {\"calc\": \"you.coins >= cost\"}`,\n    or check it before the action is allowed), and treat an action the player cannot afford as the cheapest legal one, as the rules say.\n  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {\"bind\": \"name\"}`; a later `update`\n    stores it with `\"value\": \"$name\"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the\n    answers away, and every score that depends on them stays at its starting value.\n  * An attribute declared `\"mutable\": false` is set once, by an `initialize` step, and any other step that sets it crashes the game\n    (\"declared static and has already been dealt\"). To set a hidden type or a starting value at setup, either use an `initialize`\n    step or leave the attribute mutable.\n  * Do not write steps that do nothing (for example an `if` of `{\"calc\": \"False\"}`), or two polls where one will do.\n  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,\n    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.\n- Keep a round to at most 20 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the\n  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.\n\n## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)\n\nFor \"each player chooses in private, then the choices decide the score\":\n1. One `ask` per seat, addressed with `{\"where\": \"you.seat == N\"}`, with `\"verify\": {\"bind\": \"aN\"}`. The answer exists only because it is bound.\n2. One `update` after both. It `set`s the bound answers into table attributes with `\"$aN\"`, and `adjust`s each player's score with a\n   `calc` that may use `$aN` and `if ... else`.\n3. A `check` with `when` and `against`, and ONE ending in `end` whose `rank_by` is `you.score`: the engine ranks the players by it.\nEvery attribute is set by a step that runs. Adapt this; do not invent another way to store answers.\n\n```json\n{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"match_or_miss\",\n    \"name\": \"Match or Miss\",\n    \"players\": {\n      \"min\": 2,\n      \"max\": 2\n    },\n    \"blurb\": \"Two players choose A or B in secret; seat 1 scores when they match, seat 2 when they differ.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"rounds_left\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"last_a1\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_a2\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      }\n    ]\n  },\n  \"rules\": \"Three rounds. Each round both players secretly choose A or B. If the choices match, seat 1 scores a point; if they differ, seat 2 does. The higher score wins.\",\n  \"setup\": [\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"ask\",\n      \"label\": \"seat 1 chooses\",\n      \"to\": {\n        \"where\": \"you.seat == 1\"\n      },\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": [\n          \"A\",\n          \"B\"\n        ]\n      },\n      \"verify\": {\n        \"bind\": \"a1\"\n      },\n      \"text\": \"Choose A or B. Your opponent will not see it.\"\n    },\n    {\n      \"use\": \"ask\",\n      \"label\": \"seat 2 chooses\",\n      \"to\": {\n        \"where\": \"you.seat == 2\"\n      },\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": [\n          \"A\",\n          \"B\"\n        ]\n      },\n      \"verify\": {\n        \"bind\": \"a2\"\n      },\n      \"text\": \"Choose A or B. Your opponent will not see it.\"\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"score the round\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"last_a1\",\n            \"value\": \"$a1\"\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_a2\",\n            \"value\": \"$a2\"\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"score\",\n            \"value\": {\n              \"calc\": \"1 if $a1 == $a2 else 0\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"score\",\n            \"value\": {\n              \"calc\": \"0 if $a1 == $a2 else 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"key\": \"rounds_left\",\n            \"value\": -1\n          }\n        }\n      ],\n      \"text\": \"Seat 1 chose {last_a1}, seat 2 chose {last_a2}.\"\n    },\n    {\n      \"use\": \"check\",\n      \"label\": \"is it over\",\n      \"when\": {\n        \"calc\": \"rounds_left <= 0\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"rounds_left <= 0\"\n      },\n      \"rank_by\": \"you.score\",\n      \"text\": \"{result} wins.\"\n    }\n  }\n}\n```\n\nYour file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every\nattribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and\nshown your file again; fix what is wrong and keep the rest.\n"
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"for-sale-sealed-bids-four-player\",\n    \"name\": \"For Sale: Sealed Bids - Four Player\",\n    \"players\": {\n      \"min\": 4,\n      \"max\": 4,\n      \"suggested\": 4\n    },\n    \"blurb\": \"Bid secretly for properties then sell them secretly for cheques; richest total wins.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"coins\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"cheque_total\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"properties\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"bid\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"selected_property\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"final_money\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"property_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          1,\n          2,\n          3,\n          4,\n          5,\n          6,\n          7,\n          8,\n          9,\n          10,\n          11,\n          12,\n          13,\n          14,\n          15,\n          16,\n          17,\n          18,\n          19,\n          20,\n          21,\n          22,\n          23,\n          24,\n          25,\n          26,\n          27,\n          28,\n          29,\n          30\n        ]\n      },\n      {\n        \"key\": \"cheque_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          0,\n          0,\n          2,\n          2,\n          3,\n          3,\n          4,\n          4,\n          5,\n          5,\n          6,\n          6,\n          7,\n          7,\n          8,\n          8,\n          9,\n          9,\n          10,\n          10,\n          11,\n          11,\n          12,\n          12,\n          13,\n          13,\n          14,\n          14,\n          15,\n          15\n        ]\n      },\n      {\n        \"key\": \"current_offer\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"priority_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_discard\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"pick\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"starting_coins\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"property_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"cheque_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"cheque_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 15\n      },\n      {\n        \"key\": \"cheque_copies\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"cheque_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"cheque_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"total_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 14\n      },\n      {\n        \"key\": \"buying_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"selling_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"cards_per_round\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 4\n      }\n    ]\n  },\n  \"rules\": \"Four players numbered 1 to 4. Each starts with {starting_coins} coins and 0 cheques and an empty property hand. Property deck holds cards {property_low} to {property_high} one each for {property_deck_size} cards. Cheque deck holds values {cheque_low} and 2 to {cheque_high} two of each for {cheque_deck_size} cheques. The game lasts {total_rounds} rounds: rounds 1 to {buying_rounds} are BUYING and rounds 8 to 14 are SELLING. There is no talk phase and every choice is sealed; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW.\\n\\nBUYING (rounds 1-7): In round 1 the property deck is shuffled. Only the top {property_deck_used} cards are ever used; the bottom 2 stay unseen. Each buying round reveal the next {cards_per_round} property cards, sorted HIGH, SECOND, THIRD, LOW by value. All players at the same moment secretly submit a whole-number bid from 0 up to current coins. Bids are ranked highest to lowest; ties are broken by priority order starting at seat ((r-1) mod 4)+1 in round r then next wrapping 4 to 1. First-ranked takes HIGH and pays full bid; second-ranked takes SECOND and pays half bid rounded UP; third takes THIRD and pays half rounded UP; fourth takes LOW and pays half rounded UP, where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. Payments go to the bank from private coins. Announce publicly which player took HIGH, SECOND, THIRD, LOW; bid amounts and coin totals are NOT announced. If you cannot afford a payment you cannot make that bid: a bid above your coins is never offered. After round 7 each holds 7 properties.\\n\\nSELLING (rounds 8-14): In round 8 the cheque deck is shuffled. Only the top {cheque_deck_used} cheques are ever used; the bottom 2 stay unseen. Each selling round reveal the next {cards_per_round} cheques sorted highest to lowest. All players at the same moment secretly choose one property from own hand. Chosen properties are revealed; all properties are different so there are no ties. Highest property adds highest cheque to cheque total; second-highest adds second-highest; third adds third; lowest adds lowest. Played properties are discarded. Announce publicly who played which property and who took which cheque; running cheque totals stay private.\\n\\nEND: After round 14 hands are empty. Cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed. The player with most final money wins. If tied for most, the tied player with more remaining coins wins; if still tied the game is a draw among them.\",\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"prepare the game\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"starting_coins\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"sync\",\n      \"phase\": \"start\",\n      \"label\": \"your standing\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"Your coins, cheques and properties:\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"reveal properties\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": {\n              \"calc\": \"(round_number - 1) % 4 + 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} buying: HIGH {current_offer} revealed with priority seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"buy\",\n      \"label\": \"sealed bids\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"number\",\n        \"min\": 0,\n        \"max\": {\n          \"calc\": \"you.coins\"\n        }\n      },\n      \"store\": \"bid\",\n      \"text\": \"Secretly submit a whole-number bid from 0 up to your current coins for properties HIGH to LOW. Highest bid takes HIGH and pays full bid; second takes SECOND and pays half rounded up; third takes THIRD and pays half rounded up; fourth takes LOW and pays half rounded up. Ties break by priority starting at seat {priority_seat} then wrapping 4 to 1. Bids and coins stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"resolve buying\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 1][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 2][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 3][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 4][0]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 1\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 2\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 3\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 4\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-you.bid\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 2\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 3\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 4\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Bids ranked highest to lowest with priority from seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"buy\",\n      \"label\": \"buying result\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} buying: seat {high_taker} took HIGH, seat {second_taker} took SECOND, seat {third_taker} took THIRD, seat {low_taker} took LOW. Bid amounts and coin totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"reveal cheques\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} selling: cheques {current_offer} revealed highest to lowest.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"sell\",\n      \"label\": \"choose property\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": {\n          \"attribute\": \"properties\"\n        }\n      },\n      \"store\": \"selected_property\",\n      \"text\": \"Secretly choose one property from your own hand to sell. Highest property takes highest cheque, second-highest takes second-highest, third takes third, lowest takes lowest. Your choice is sealed.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"resolve selling\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[3]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[2]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[1]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == high_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == second_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == third_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == low_play][0]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 2\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 3\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 4\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Properties ranked highest to lowest with no ties; cheques awarded in order.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"sell\",\n      \"label\": \"selling result\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} selling: seat {high_taker} played {high_play} and took {current_offer}, seat {second_taker} played {second_play}, seat {third_taker} played {third_play}, seat {low_taker} played {low_play}. Running cheque totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"end\",\n      \"label\": \"advance round\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": {\n              \"calc\": \"you.cheque_total + you.coins\"\n            },\n            \"if\": {\n              \"calc\": \"round_number > total_rounds\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"end\",\n      \"label\": \"game over\",\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"rank_by\": \"you.final_money * 1000 + you.coins\",\n      \"text\": \"Winner: {result}. Final money: Seat 1 {players[0].final_money}, Seat 2 {players[1].final_money}, Seat 3 {players[2].final_money}, Seat 4 {players[3].final_money}; coins Seat 1 {players[0].coins}, Seat 2 {players[1].coins}, Seat 3 {players[2].coins}, Seat 4 {players[3].coins}.\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 14,\n    \"rounds_max\": 14,\n    \"actions_max\": 1000,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: playing it with random seats failed: seed 1, 4 players: the match crashed: FlowError: '1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 1' reads `you` where there is no player\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"for-sale-sealed-bids-four-player\",\n    \"name\": \"For Sale: Sealed Bids - Four Player\",\n    \"players\": {\n      \"min\": 4,\n      \"max\": 4,\n      \"suggested\": 4\n    },\n    \"blurb\": \"Bid secretly for properties then sell them secretly for cheques; richest total wins.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"coins\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"cheque_total\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"properties\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"bid\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"selected_property\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"final_money\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"property_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          1,\n          2,\n          3,\n          4,\n          5,\n          6,\n          7,\n          8,\n          9,\n          10,\n          11,\n          12,\n          13,\n          14,\n          15,\n          16,\n          17,\n          18,\n          19,\n          20,\n          21,\n          22,\n          23,\n          24,\n          25,\n          26,\n          27,\n          28,\n          29,\n          30\n        ]\n      },\n      {\n        \"key\": \"cheque_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          0,\n          0,\n          2,\n          2,\n          3,\n          3,\n          4,\n          4,\n          5,\n          5,\n          6,\n          6,\n          7,\n          7,\n          8,\n          8,\n          9,\n          9,\n          10,\n          10,\n          11,\n          11,\n          12,\n          12,\n          13,\n          13,\n          14,\n          14,\n          15,\n          15\n        ]\n      },\n      {\n        \"key\": \"current_offer\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"priority_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_discard\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"pick\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"starting_coins\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"property_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"cheque_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"cheque_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 15\n      },\n      {\n        \"key\": \"cheque_copies\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"cheque_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"cheque_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"total_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 14\n      },\n      {\n        \"key\": \"buying_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"selling_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"cards_per_round\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 4\n      }\n    ]\n  },\n  \"rules\": \"Four players numbered 1 to 4. Each starts with {starting_coins} coins and 0 cheques and an empty property hand. Property deck holds cards {property_low} to {property_high} one each for {property_deck_size} cards. Cheque deck holds values {cheque_low} and 2 to {cheque_high} two of each for {cheque_deck_size} cheques. The game lasts {total_rounds} rounds: rounds 1 to {buying_rounds} are BUYING and rounds 8 to 14 are SELLING. There is no talk phase and every choice is sealed; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW.\\n\\nBUYING (rounds 1-7): In round 1 the property deck is shuffled. Only the top {property_deck_used} cards are ever used; the bottom 2 stay unseen. Each buying round reveal the next {cards_per_round} property cards, sorted HIGH, SECOND, THIRD, LOW by value. All players at the same moment secretly submit a whole-number bid from 0 up to current coins. Bids are ranked highest to lowest; ties are broken by priority order starting at seat ((r-1) mod 4)+1 in round r then next wrapping 4 to 1. First-ranked takes HIGH and pays full bid; second-ranked takes SECOND and pays half bid rounded UP; third takes THIRD and pays half rounded UP; fourth takes LOW and pays half rounded UP, where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. Payments go to the bank from private coins. Announce publicly which player took HIGH, SECOND, THIRD, LOW; bid amounts and coin totals are NOT announced. If you cannot afford a payment you cannot make that bid: a bid above your coins is never offered. After round 7 each holds 7 properties.\\n\\nSELLING (rounds 8-14): In round 8 the cheque deck is shuffled. Only the top {cheque_deck_used} cheques are ever used; the bottom 2 stay unseen. Each selling round reveal the next {cards_per_round} cheques sorted highest to lowest. All players at the same moment secretly choose one property from own hand. Chosen properties are revealed; all properties are different so there are no ties. Highest property adds highest cheque to cheque total; second-highest adds second-highest; third adds third; lowest adds lowest. Played properties are discarded. Announce publicly who played which property and who took which cheque; running cheque totals stay private.\\n\\nEND: After round 14 hands are empty. Cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed. The player with most final money wins. If tied for most, the tied player with more remaining coins wins; if still tied the game is a draw among them.\",\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"prepare the game\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"starting_coins\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"sync\",\n      \"phase\": \"start\",\n      \"label\": \"your standing\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"Your coins, cheques and properties:\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"reveal properties\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": {\n              \"calc\": \"(round_number - 1) % 4 + 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} buying: HIGH {current_offer} revealed with priority seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"buy\",\n      \"label\": \"sealed bids\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"number\",\n        \"min\": 0,\n        \"max\": {\n          \"calc\": \"you.coins\"\n        }\n      },\n      \"store\": \"bid\",\n      \"text\": \"Secretly submit a whole-number bid from 0 up to your current coins for properties HIGH to LOW. Highest bid takes HIGH and pays full bid; second takes SECOND and pays half rounded up; third takes THIRD and pays half rounded up; fourth takes LOW and pays half rounded up. Ties break by priority starting at seat {priority_seat} then wrapping 4 to 1. Bids and coins stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"resolve buying\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 1][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 2][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 3][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if 1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (p.bid * 4 + (3 - ((p.seat - priority_seat) % 4))) for q in players) == 4][0]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 1\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 2\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 3\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 4\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-you.bid\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 2\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 3\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 4\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Bids ranked highest to lowest with priority from seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"buy\",\n      \"label\": \"buying result\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} buying: seat {high_taker} took HIGH, seat {second_taker} took SECOND, seat {third_taker} took THIRD, seat {low_taker} took LOW. Bid amounts and coin totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"reveal cheques\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} selling: cheques {current_offer} revealed highest to lowest.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"sell\",\n      \"label\": \"choose property\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": {\n          \"attribute\": \"properties\"\n        }\n      },\n      \"store\": \"selected_property\",\n      \"text\": \"Secretly choose one property from your own hand to sell. Highest property takes highest cheque, second-highest takes second-highest, third takes third, lowest takes lowest. Your choice is sealed.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"resolve selling\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[3]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[2]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[1]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == high_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == second_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == third_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == low_play][0]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 2\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 3\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            },\n            \"if\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players) == 4\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Properties ranked highest to lowest with no ties; cheques awarded in order.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"sell\",\n      \"label\": \"selling result\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} selling: seat {high_taker} played {high_play} and took {current_offer}, seat {second_taker} played {second_play}, seat {third_taker} played {third_play}, seat {low_taker} played {low_play}. Running cheque totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"end\",\n      \"label\": \"advance round\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": {\n              \"calc\": \"you.cheque_total + you.coins\"\n            },\n            \"if\": {\n              \"calc\": \"round_number > total_rounds\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"end\",\n      \"label\": \"game over\",\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"rank_by\": \"you.final_money * 1000 + you.coins\",\n      \"text\": \"Winner: {result}. Final money: Seat 1 {players[0].final_money}, Seat 2 {players[1].final_money}, Seat 3 {players[2].final_money}, Seat 4 {players[3].final_money}; coins Seat 1 {players[0].coins}, Seat 2 {players[1].coins}, Seat 3 {players[2].coins}, Seat 4 {players[3].coins}.\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 14,\n    \"rounds_max\": 14,\n    \"actions_max\": 1000,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: playing it with random seats failed: seed 1, 4 players: the match crashed: FlowError: '1 + count((q.bid * 4 + (3 - ((q.seat - priority_seat) % 4))) > (you.bid * 4 + (3 - ((you.seat - priority_seat) % 4))) for q in players) == 1' reads `you` where there is no player\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"for-sale-sealed-bids-four-player\",\n    \"name\": \"For Sale: Sealed Bids - Four Player\",\n    \"players\": {\n      \"min\": 4,\n      \"max\": 4,\n      \"suggested\": 4\n    },\n    \"blurb\": \"Bid secretly for properties then sell them secretly for cheques; richest total wins.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"coins\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"cheque_total\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"properties\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"bid\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"selected_property\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"final_money\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"buy_rank\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"sell_rank\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"property_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          1,\n          2,\n          3,\n          4,\n          5,\n          6,\n          7,\n          8,\n          9,\n          10,\n          11,\n          12,\n          13,\n          14,\n          15,\n          16,\n          17,\n          18,\n          19,\n          20,\n          21,\n          22,\n          23,\n          24,\n          25,\n          26,\n          27,\n          28,\n          29,\n          30\n        ]\n      },\n      {\n        \"key\": \"cheque_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          0,\n          0,\n          2,\n          2,\n          3,\n          3,\n          4,\n          4,\n          5,\n          5,\n          6,\n          6,\n          7,\n          7,\n          8,\n          8,\n          9,\n          9,\n          10,\n          10,\n          11,\n          11,\n          12,\n          12,\n          13,\n          13,\n          14,\n          14,\n          15,\n          15\n        ]\n      },\n      {\n        \"key\": \"current_offer\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"priority_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_discard\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"pick\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"starting_coins\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"property_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"cheque_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"cheque_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 15\n      },\n      {\n        \"key\": \"cheque_copies\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"cheque_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"cheque_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"total_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 14\n      },\n      {\n        \"key\": \"buying_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"selling_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"cards_per_round\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 4\n      }\n    ]\n  },\n  \"rules\": \"Four players numbered 1 to 4. Each starts with {starting_coins} coins and 0 cheques and an empty property hand. Property deck holds cards {property_low} to {property_high} one each for {property_deck_size} cards. Cheque deck holds values {cheque_low} and 2 to {cheque_high} two of each for {cheque_deck_size} cheques. The game lasts {total_rounds} rounds: rounds 1 to {buying_rounds} are BUYING and rounds 8 to 14 are SELLING. There is no talk phase and every choice is sealed; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW.\\n\\nBUYING (rounds 1-7): In round 1 the property deck is shuffled. Only the top {property_deck_used} cards are ever used; the bottom 2 stay unseen. Each buying round reveal the next {cards_per_round} property cards, sorted HIGH, SECOND, THIRD, LOW by value. All players at the same moment secretly submit a whole-number bid from 0 up to current coins. Bids are ranked highest to lowest; ties are broken by priority order starting at seat ((r-1) mod 4)+1 in round r then next wrapping 4 to 1. First-ranked takes HIGH and pays full bid; second-ranked takes SECOND and pays half bid rounded UP; third takes THIRD and pays half rounded UP; fourth takes LOW and pays half rounded UP, where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. Payments go to the bank from private coins. Announce publicly which player took HIGH, SECOND, THIRD, LOW; bid amounts and coin totals are NOT announced. If you cannot afford a payment you cannot make that bid: a bid above your coins is never offered. After round 7 each holds 7 properties.\\n\\nSELLING (rounds 8-14): In round 8 the cheque deck is shuffled. Only the top {cheque_deck_used} cheques are ever used; the bottom 2 stay unseen. Each selling round reveal the next {cards_per_round} cheques sorted highest to lowest. All players at the same moment secretly choose one property from own hand. Chosen properties are revealed; all properties are different so there are no ties. Highest property adds highest cheque to cheque total; second-highest adds second-highest; third adds third; lowest adds lowest. Played properties are discarded. Announce publicly who played which property and who took which cheque; running cheque totals stay private.\\n\\nEND: After round 14 hands are empty. Cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed. The player with most final money wins. If tied for most, the tied player with more remaining coins wins; if still tied the game is a draw among them.\",\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"prepare the game\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"starting_coins\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"buy_rank\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"sell_rank\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"sync\",\n      \"phase\": \"start\",\n      \"label\": \"your standing\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"Your coins, cheques and properties:\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"reveal properties\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": {\n              \"calc\": \"(round_number - 1) % 4 + 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} buying: HIGH {current_offer} revealed with priority seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"buy\",\n      \"label\": \"sealed bids\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"number\",\n        \"min\": 0,\n        \"max\": {\n          \"calc\": \"you.coins\"\n        }\n      },\n      \"store\": \"bid\",\n      \"text\": \"Secretly submit a whole-number bid from 0 up to your current coins for properties HIGH to LOW. Highest bid takes HIGH and pays full bid; second takes SECOND and pays half rounded up; third takes THIRD and pays half rounded up; fourth takes LOW and pays half rounded up. Ties break by priority starting at seat {priority_seat} then wrapping 4 to 1. Bids and coins stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"rank bids\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"buy_rank\",\n            \"value\": {\n              \"calc\": \"1 + count(q.bid * 4 + (3 - ((q.seat - priority_seat) % 4)) > you.bid * 4 + (3 - ((you.seat - priority_seat) % 4)) for q in players)\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Bids ranked highest to lowest with priority from seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"resolve buying\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 1][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 2][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 3][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 4][0]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 1\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 2\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 3\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 4\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-you.bid\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 2\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 3\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            },\n            \"if\": {\n              \"calc\": \"you.buy_rank == 4\"\n            }\n          }\n        }\n      ],\n      \"text\": \"First takes HIGH and pays full bid; others pay half rounded up.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"buy\",\n      \"label\": \"buying result\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} buying: seat {high_taker} took HIGH, seat {second_taker} took SECOND, seat {third_taker} took THIRD, seat {low_taker} took LOW. Bid amounts and coin totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"reveal cheques\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} selling: cheques {current_offer} revealed highest to lowest.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"sell\",\n      \"label\": \"choose property\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": {\n          \"attribute\": \"properties\"\n        }\n      },\n      \"store\": \"selected_property\",\n      \"text\": \"Secretly choose one property from your own hand to sell. Highest property takes highest cheque, second-highest takes second-highest, third takes third, lowest takes lowest. Your choice is sealed.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"rank properties\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"sell_rank\",\n            \"value\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players)\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Properties ranked highest to lowest with no ties.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"resolve selling\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[3]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[2]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[1]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == high_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == second_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == third_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == low_play][0]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            },\n            \"if\": {\n              \"calc\": \"you.sell_rank == 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            },\n            \"if\": {\n              \"calc\": \"you.sell_rank == 2\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            },\n            \"if\": {\n              \"calc\": \"you.sell_rank == 3\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            },\n            \"if\": {\n              \"calc\": \"you.sell_rank == 4\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Cheques awarded in order; played properties discarded.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"sell\",\n      \"label\": \"selling result\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} selling: seat {high_taker} played {high_play} and took {current_offer}, seat {second_taker} played {second_play}, seat {third_taker} played {third_play}, seat {low_taker} played {low_play}. Running cheque totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"end\",\n      \"label\": \"advance round\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": {\n              \"calc\": \"you.cheque_total + you.coins\"\n            },\n            \"if\": {\n              \"calc\": \"round_number > total_rounds\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"end\",\n      \"label\": \"game over\",\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"rank_by\": \"you.final_money * 1000 + you.coins\",\n      \"text\": \"Winner: {result}. Final money: Seat 1 {players[0].final_money}, Seat 2 {players[1].final_money}, Seat 3 {players[2].final_money}, Seat 4 {players[3].final_money}; coins Seat 1 {players[0].coins}, Seat 2 {players[1].coins}, Seat 3 {players[2].coins}, Seat 4 {players[3].coins}.\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 14,\n    \"rounds_max\": 14,\n    \"actions_max\": 1000,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: playing it with random seats failed: seed 1, 4 players: the match crashed: FlowError: 'you.buy_rank == 1' reads `you` where there is no player\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"for-sale-sealed-bids-four-player\",\n    \"name\": \"For Sale: Sealed Bids - Four Player\",\n    \"players\": {\n      \"min\": 4,\n      \"max\": 4,\n      \"suggested\": 4\n    },\n    \"blurb\": \"Bid secretly for properties then sell them secretly for cheques; richest total wins.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"coins\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"cheque_total\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"properties\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"bid\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"selected_property\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"final_money\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"buy_rank\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"sell_rank\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"property_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          1,\n          2,\n          3,\n          4,\n          5,\n          6,\n          7,\n          8,\n          9,\n          10,\n          11,\n          12,\n          13,\n          14,\n          15,\n          16,\n          17,\n          18,\n          19,\n          20,\n          21,\n          22,\n          23,\n          24,\n          25,\n          26,\n          27,\n          28,\n          29,\n          30\n        ]\n      },\n      {\n        \"key\": \"cheque_deck\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": [\n          0,\n          0,\n          2,\n          2,\n          3,\n          3,\n          4,\n          4,\n          5,\n          5,\n          6,\n          6,\n          7,\n          7,\n          8,\n          8,\n          9,\n          9,\n          10,\n          10,\n          11,\n          11,\n          12,\n          12,\n          13,\n          13,\n          14,\n          14,\n          15,\n          15\n        ]\n      },\n      {\n        \"key\": \"current_offer\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"priority_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_discard\",\n        \"visible\": \"public\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"pick\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_taker\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"high_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"second_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"third_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"low_play\",\n        \"visible\": \"none\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"starting_coins\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 18\n      },\n      {\n        \"key\": \"property_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"property_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"property_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"cheque_low\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"cheque_high\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 15\n      },\n      {\n        \"key\": \"cheque_copies\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"cheque_deck_size\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 30\n      },\n      {\n        \"key\": \"cheque_deck_used\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 28\n      },\n      {\n        \"key\": \"total_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 14\n      },\n      {\n        \"key\": \"buying_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"selling_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 7\n      },\n      {\n        \"key\": \"cards_per_round\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 4\n      }\n    ]\n  },\n  \"rules\": \"Four players numbered 1 to 4. Each starts with {starting_coins} coins and 0 cheques and an empty property hand. Property deck holds cards {property_low} to {property_high} one each for {property_deck_size} cards. Cheque deck holds values {cheque_low} and 2 to {cheque_high} two of each for {cheque_deck_size} cheques. The game lasts {total_rounds} rounds: rounds 1 to {buying_rounds} are BUYING and rounds 8 to 14 are SELLING. There is no talk phase and every choice is sealed; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW.\\n\\nBUYING (rounds 1-7): In round 1 the property deck is shuffled. Only the top {property_deck_used} cards are ever used; the bottom 2 stay unseen. Each buying round reveal the next {cards_per_round} property cards, sorted HIGH, SECOND, THIRD, LOW by value. All players at the same moment secretly submit a whole-number bid from 0 up to current coins. Bids are ranked highest to lowest; ties are broken by priority order starting at seat ((r-1) mod 4)+1 in round r then next wrapping 4 to 1. First-ranked takes HIGH and pays full bid; second-ranked takes SECOND and pays half bid rounded UP; third takes THIRD and pays half rounded UP; fourth takes LOW and pays half rounded UP, where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. Payments go to the bank from private coins. Announce publicly which player took HIGH, SECOND, THIRD, LOW; bid amounts and coin totals are NOT announced. If you cannot afford a payment you cannot make that bid: a bid above your coins is never offered. After round 7 each holds 7 properties.\\n\\nSELLING (rounds 8-14): In round 8 the cheque deck is shuffled. Only the top {cheque_deck_used} cheques are ever used; the bottom 2 stay unseen. Each selling round reveal the next {cards_per_round} cheques sorted highest to lowest. All players at the same moment secretly choose one property from own hand. Chosen properties are revealed; all properties are different so there are no ties. Highest property adds highest cheque to cheque total; second-highest adds second-highest; third adds third; lowest adds lowest. Played properties are discarded. Announce publicly who played which property and who took which cheque; running cheque totals stay private.\\n\\nEND: After round 14 hands are empty. Cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed. The player with most final money wins. If tied for most, the tied player with more remaining coins wins; if still tied the game is a draw among them.\",\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"prepare the game\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"starting_coins\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"cheque_total\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"buy_rank\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"sell_rank\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"sync\",\n      \"phase\": \"start\",\n      \"label\": \"your standing\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"Your coins, cheques and properties:\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"reveal properties\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"property_deck[int(uniform(0, len(property_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"property_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"priority_seat\",\n            \"value\": {\n              \"calc\": \"(round_number - 1) % 4 + 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"bid\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} buying: HIGH {current_offer} revealed with priority seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"buy\",\n      \"label\": \"sealed bids\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"number\",\n        \"min\": 0,\n        \"max\": {\n          \"calc\": \"you.coins\"\n        }\n      },\n      \"store\": \"bid\",\n      \"text\": \"Secretly submit a whole-number bid from 0 up to your current coins for properties HIGH to LOW. Highest bid takes HIGH and pays full bid; second takes SECOND and pays half rounded up; third takes THIRD and pays half rounded up; fourth takes LOW and pays half rounded up. Ties break by priority starting at seat {priority_seat} then wrapping 4 to 1. Bids and coins stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"rank bids\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"buy_rank\",\n            \"value\": {\n              \"calc\": \"1 + count(q.bid * 4 + (3 - ((q.seat - priority_seat) % 4)) > you.bid * 4 + (3 - ((you.seat - priority_seat) % 4)) for q in players)\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Bids ranked highest to lowest with priority from seat {priority_seat}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"buy\",\n      \"label\": \"resolve buying\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 1][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 2][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 3][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.buy_rank == 4][0]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 1\"\n            },\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 2\"\n            },\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 3\"\n            },\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 4\"\n            },\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 1\"\n            },\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-you.bid\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 2\"\n            },\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 3\"\n            },\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.buy_rank == 4\"\n            },\n            \"key\": \"coins\",\n            \"value\": {\n              \"calc\": \"-((you.bid + 1) // 2)\"\n            }\n          }\n        }\n      ],\n      \"text\": \"First takes HIGH and pays full bid; others pay half rounded up.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"buy\",\n      \"label\": \"buying result\",\n      \"when\": {\n        \"calc\": \"round_number <= buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} buying: seat {high_taker} took HIGH, seat {second_taker} took SECOND, seat {third_taker} took THIRD, seat {low_taker} took LOW. Bid amounts and coin totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"reveal cheques\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"pick\",\n            \"value\": {\n              \"calc\": \"cheque_deck[int(uniform(0, len(cheque_deck)))]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"key\": \"cheque_deck\",\n            \"value\": {\n              \"calc\": \"pick\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"current_offer\",\n            \"value\": {\n              \"calc\": \"[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"selected_property\",\n            \"value\": 0\n          }\n        }\n      ],\n      \"text\": \"Round {round_number} selling: cheques {current_offer} revealed highest to lowest.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"sell\",\n      \"label\": \"choose property\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": {\n          \"attribute\": \"properties\"\n        }\n      },\n      \"store\": \"selected_property\",\n      \"text\": \"Secretly choose one property from your own hand to sell. Highest property takes highest cheque, second-highest takes second-highest, third takes third, lowest takes lowest. Your choice is sealed.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"rank properties\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"sell_rank\",\n            \"value\": {\n              \"calc\": \"1 + count(q.selected_property > you.selected_property for q in players)\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Properties ranked highest to lowest with no ties.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"sell\",\n      \"label\": \"resolve selling\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"high_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[3]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[2]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[1]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_play\",\n            \"value\": {\n              \"calc\": \"sorted([p.selected_property for p in players])[0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"high_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == high_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"second_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == second_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"third_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == third_play][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"low_taker\",\n            \"value\": {\n              \"calc\": \"[p.seat for p in players if p.selected_property == low_play][0]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.sell_rank == 1\"\n            },\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[0]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.sell_rank == 2\"\n            },\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[1]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.sell_rank == 3\"\n            },\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[2]\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.sell_rank == 4\"\n            },\n            \"key\": \"cheque_total\",\n            \"value\": {\n              \"calc\": \"current_offer[3]\"\n            }\n          }\n        },\n        {\n          \"append\": {\n            \"players\": \"all\",\n            \"key\": \"property_discard\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        },\n        {\n          \"remove\": {\n            \"players\": \"all\",\n            \"key\": \"properties\",\n            \"value\": {\n              \"calc\": \"you.selected_property\"\n            }\n          }\n        }\n      ],\n      \"text\": \"Cheques awarded in order; played properties discarded.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"sell\",\n      \"label\": \"selling result\",\n      \"when\": {\n        \"calc\": \"round_number > buying_rounds\"\n      },\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} selling: seat {high_taker} played {high_play} and took {current_offer}, seat {second_taker} played {second_play}, seat {third_taker} played {third_play}, seat {low_taker} played {low_play}. Running cheque totals stay secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"end\",\n      \"label\": \"advance round\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"final_money\",\n            \"value\": {\n              \"calc\": \"you.cheque_total + you.coins\"\n            },\n            \"if\": {\n              \"calc\": \"round_number > total_rounds\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"end\",\n      \"label\": \"game over\",\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"round_number > total_rounds\"\n      },\n      \"rank_by\": \"you.final_money * 1000 + you.coins\",\n      \"text\": \"Winner: {result}. Final money: Seat 1 {players[0].final_money}, Seat 2 {players[1].final_money}, Seat 3 {players[2].final_money}, Seat 4 {players[3].final_money}; coins Seat 1 {players[0].coins}, Seat 2 {players[1].coins}, Seat 3 {players[2].coins}, Seat 4 {players[3].coins}.\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 14,\n    \"rounds_max\": 14,\n    \"actions_max\": 1000,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: playing it with random seats failed: seed 1, 4 players: the match crashed: FlowError: 'property_discard' is not a declared player attribute\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  }
]
````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "for-sale-sealed-bids-four-player",
    "name": "For Sale: Sealed Bids - Four Player",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Bid secretly for properties then sell them secretly for cheques; richest total wins."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "coins",
        "visible": "ally",
        "type": "number",
        "initial": 18
      },
      {
        "key": "cheque_total",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "properties",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "selected_property",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_money",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "buy_rank",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sell_rank",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "property_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          29,
          30
        ]
      },
      {
        "key": "cheque_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          0,
          0,
          2,
          2,
          3,
          3,
          4,
          4,
          5,
          5,
          6,
          6,
          7,
          7,
          8,
          8,
          9,
          9,
          10,
          10,
          11,
          11,
          12,
          12,
          13,
          13,
          14,
          14,
          15,
          15
        ]
      },
      {
        "key": "current_offer",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "property_discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_taker",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_taker",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "third_taker",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "low_taker",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_play",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_play",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "third_play",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "low_play",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "property_low",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "property_high",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "property_deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "property_deck_used",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "cheque_low",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cheque_high",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "cheque_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "cheque_deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "cheque_deck_used",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "buying_rounds",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "selling_rounds",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "cards_per_round",
        "visible": "public",
        "type": "number",
        "initial": 4
      }
    ]
  },
  "rules": "Four players numbered 1 to 4. Each starts with {starting_coins} coins and 0 cheques and an empty property hand. Property deck holds cards {property_low} to {property_high} one each for {property_deck_size} cards. Cheque deck holds values {cheque_low} and 2 to {cheque_high} two of each for {cheque_deck_size} cheques. The game lasts {total_rounds} rounds: rounds 1 to {buying_rounds} are BUYING and rounds 8 to 14 are SELLING. There is no talk phase and every choice is sealed; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW.\n\nBUYING (rounds 1-7): In round 1 the property deck is shuffled. Only the top {property_deck_used} cards are ever used; the bottom 2 stay unseen. Each buying round reveal the next {cards_per_round} property cards, sorted HIGH, SECOND, THIRD, LOW by value. All players at the same moment secretly submit a whole-number bid from 0 up to current coins. Bids are ranked highest to lowest; ties are broken by priority order starting at seat ((r-1) mod 4)+1 in round r then next wrapping 4 to 1. First-ranked takes HIGH and pays full bid; second-ranked takes SECOND and pays half bid rounded UP; third takes THIRD and pays half rounded UP; fourth takes LOW and pays half rounded UP, where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. Payments go to the bank from private coins. Announce publicly which player took HIGH, SECOND, THIRD, LOW; bid amounts and coin totals are NOT announced. If you cannot afford a payment you cannot make that bid: a bid above your coins is never offered. After round 7 each holds 7 properties.\n\nSELLING (rounds 8-14): In round 8 the cheque deck is shuffled. Only the top {cheque_deck_used} cheques are ever used; the bottom 2 stay unseen. Each selling round reveal the next {cards_per_round} cheques sorted highest to lowest. All players at the same moment secretly choose one property from own hand. Chosen properties are revealed; all properties are different so there are no ties. Highest property adds highest cheque to cheque total; second-highest adds second-highest; third adds third; lowest adds lowest. Played properties are discarded. Announce publicly who played which property and who took which cheque; running cheque totals stay private.\n\nEND: After round 14 hands are empty. Cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed. The player with most final money wins. If tied for most, the tied player with more remaining coins wins; if still tied the game is a draw among them.",
  "setup": [
    {
      "use": "update",
      "label": "prepare the game",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "starting_coins"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cheque_total",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "properties",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "selected_property",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_money",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "buy_rank",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sell_rank",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "current_offer",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "property_discard",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "sync",
      "phase": "start",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "text": "Your coins, cheques and properties:"
    },
    {
      "use": "update",
      "phase": "buy",
      "label": "reveal properties",
      "when": {
        "calc": "round_number <= buying_rounds"
      },
      "do": [
        {
          "set": {
            "key": "current_offer",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "property_deck[int(uniform(0, len(property_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "property_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "property_deck[int(uniform(0, len(property_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "property_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "property_deck[int(uniform(0, len(property_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "property_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "property_deck[int(uniform(0, len(property_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "property_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "current_offer",
            "value": {
              "calc": "[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]"
            }
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": {
              "calc": "(round_number - 1) % 4 + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Round {round_number} buying: HIGH {current_offer} revealed with priority seat {priority_seat}."
    },
    {
      "use": "poll",
      "phase": "buy",
      "label": "sealed bids",
      "when": {
        "calc": "round_number <= buying_rounds"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.coins"
        }
      },
      "store": "bid",
      "text": "Secretly submit a whole-number bid from 0 up to your current coins for properties HIGH to LOW. Highest bid takes HIGH and pays full bid; second takes SECOND and pays half rounded up; third takes THIRD and pays half rounded up; fourth takes LOW and pays half rounded up. Ties break by priority starting at seat {priority_seat} then wrapping 4 to 1. Bids and coins stay secret."
    },
    {
      "use": "update",
      "phase": "buy",
      "label": "rank bids",
      "when": {
        "calc": "round_number <= buying_rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "buy_rank",
            "value": {
              "calc": "1 + count(q.bid * 4 + (3 - ((q.seat - priority_seat) % 4)) > you.bid * 4 + (3 - ((you.seat - priority_seat) % 4)) for q in players)"
            }
          }
        }
      ],
      "text": "Bids ranked highest to lowest with priority from seat {priority_seat}."
    },
    {
      "use": "update",
      "phase": "buy",
      "label": "resolve buying",
      "when": {
        "calc": "round_number <= buying_rounds"
      },
      "do": [
        {
          "set": {
            "key": "high_taker",
            "value": {
              "calc": "[p.seat for p in players if p.buy_rank == 1][0]"
            }
          }
        },
        {
          "set": {
            "key": "second_taker",
            "value": {
              "calc": "[p.seat for p in players if p.buy_rank == 2][0]"
            }
          }
        },
        {
          "set": {
            "key": "third_taker",
            "value": {
              "calc": "[p.seat for p in players if p.buy_rank == 3][0]"
            }
          }
        },
        {
          "set": {
            "key": "low_taker",
            "value": {
              "calc": "[p.seat for p in players if p.buy_rank == 4][0]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.buy_rank == 1"
            },
            "key": "properties",
            "value": {
              "calc": "current_offer[0]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.buy_rank == 2"
            },
            "key": "properties",
            "value": {
              "calc": "current_offer[1]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.buy_rank == 3"
            },
            "key": "properties",
            "value": {
              "calc": "current_offer[2]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.buy_rank == 4"
            },
            "key": "properties",
            "value": {
              "calc": "current_offer[3]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.buy_rank == 1"
            },
            "key": "coins",
            "value": {
              "calc": "-you.bid"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.buy_rank == 2"
            },
            "key": "coins",
            "value": {
              "calc": "-((you.bid + 1) // 2)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.buy_rank == 3"
            },
            "key": "coins",
            "value": {
              "calc": "-((you.bid + 1) // 2)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.buy_rank == 4"
            },
            "key": "coins",
            "value": {
              "calc": "-((you.bid + 1) // 2)"
            }
          }
        }
      ],
      "text": "First takes HIGH and pays full bid; others pay half rounded up."
    },
    {
      "use": "tell",
      "phase": "buy",
      "label": "buying result",
      "when": {
        "calc": "round_number <= buying_rounds"
      },
      "to": "all",
      "text": "Round {round_number} buying: seat {high_taker} took HIGH, seat {second_taker} took SECOND, seat {third_taker} took THIRD, seat {low_taker} took LOW. Bid amounts and coin totals stay secret."
    },
    {
      "use": "update",
      "phase": "sell",
      "label": "reveal cheques",
      "when": {
        "calc": "round_number > buying_rounds"
      },
      "do": [
        {
          "set": {
            "key": "current_offer",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "cheque_deck[int(uniform(0, len(cheque_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "cheque_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "cheque_deck[int(uniform(0, len(cheque_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "cheque_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "cheque_deck[int(uniform(0, len(cheque_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "cheque_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "cheque_deck[int(uniform(0, len(cheque_deck)))]"
            }
          }
        },
        {
          "append": {
            "key": "current_offer",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "cheque_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "current_offer",
            "value": {
              "calc": "[sorted(current_offer)[3], sorted(current_offer)[2], sorted(current_offer)[1], sorted(current_offer)[0]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "selected_property",
            "value": 0
          }
        }
      ],
      "text": "Round {round_number} selling: cheques {current_offer} revealed highest to lowest."
    },
    {
      "use": "poll",
      "phase": "sell",
      "label": "choose property",
      "when": {
        "calc": "round_number > buying_rounds"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "properties"
        }
      },
      "store": "selected_property",
      "text": "Secretly choose one property from your own hand to sell. Highest property takes highest cheque, second-highest takes second-highest, third takes third, lowest takes lowest. Your choice is sealed."
    },
    {
      "use": "update",
      "phase": "sell",
      "label": "rank properties",
      "when": {
        "calc": "round_number > buying_rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "sell_rank",
            "value": {
              "calc": "1 + count(q.selected_property > you.selected_property for q in players)"
            }
          }
        }
      ],
      "text": "Properties ranked highest to lowest with no ties."
    },
    {
      "use": "update",
      "phase": "sell",
      "label": "resolve selling",
      "when": {
        "calc": "round_number > buying_rounds"
      },
      "do": [
        {
          "set": {
            "key": "high_play",
            "value": {
              "calc": "sorted([p.selected_property for p in players])[3]"
            }
          }
        },
        {
          "set": {
            "key": "second_play",
            "value": {
              "calc": "sorted([p.selected_property for p in players])[2]"
            }
          }
        },
        {
          "set": {
            "key": "third_play",
            "value": {
              "calc": "sorted([p.selected_property for p in players])[1]"
            }
          }
        },
        {
          "set": {
            "key": "low_play",
            "value": {
              "calc": "sorted([p.selected_property for p in players])[0]"
            }
          }
        },
        {
          "set": {
            "key": "high_taker",
            "value": {
              "calc": "[p.seat for p in players if p.selected_property == high_play][0]"
            }
          }
        },
        {
          "set": {
            "key": "second_taker",
            "value": {
              "calc": "[p.seat for p in players if p.selected_property == second_play][0]"
            }
          }
        },
        {
          "set": {
            "key": "third_taker",
            "value": {
              "calc": "[p.seat for p in players if p.selected_property == third_play][0]"
            }
          }
        },
        {
          "set": {
            "key": "low_taker",
            "value": {
              "calc": "[p.seat for p in players if p.selected_property == low_play][0]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.sell_rank == 1"
            },
            "key": "cheque_total",
            "value": {
              "calc": "current_offer[0]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.sell_rank == 2"
            },
            "key": "cheque_total",
            "value": {
              "calc": "current_offer[1]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.sell_rank == 3"
            },
            "key": "cheque_total",
            "value": {
              "calc": "current_offer[2]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.sell_rank == 4"
            },
            "key": "cheque_total",
            "value": {
              "calc": "current_offer[3]"
            }
          }
        },
        {
          "append": {
            "key": "property_discard",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 1][0]"
            }
          }
        },
        {
          "append": {
            "key": "property_discard",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 2][0]"
            }
          }
        },
        {
          "append": {
            "key": "property_discard",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 3][0]"
            }
          }
        },
        {
          "append": {
            "key": "property_discard",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 4][0]"
            }
          }
        },
        {
          "remove": {
            "player": 1,
            "key": "properties",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 1][0]"
            }
          }
        },
        {
          "remove": {
            "player": 2,
            "key": "properties",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 2][0]"
            }
          }
        },
        {
          "remove": {
            "player": 3,
            "key": "properties",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 3][0]"
            }
          }
        },
        {
          "remove": {
            "player": 4,
            "key": "properties",
            "value": {
              "calc": "[p.selected_property for p in players if p.seat == 4][0]"
            }
          }
        }
      ],
      "text": "Cheques awarded in order; played properties discarded."
    },
    {
      "use": "tell",
      "phase": "sell",
      "label": "selling result",
      "when": {
        "calc": "round_number > buying_rounds"
      },
      "to": "all",
      "text": "Round {round_number} selling: seat {high_taker} played {high_play} and took {current_offer}, seat {second_taker} played {second_play}, seat {third_taker} played {third_play}, seat {low_taker} played {low_play}. Running cheque totals stay secret."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "advance round",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_money",
            "value": {
              "calc": "you.cheque_total + you.coins"
            },
            "if": {
              "calc": "round_number > total_rounds"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "game over",
      "when": {
        "calc": "round_number > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number > total_rounds"
      },
      "rank_by": "you.final_money * 1000 + you.coins",
      "text": "Winner: {result}. Final money: Seat 1 {players[0].final_money}, Seat 2 {players[1].final_money}, Seat 3 {players[2].final_money}, Seat 4 {players[3].final_money}; coins Seat 1 {players[0].coins}, Seat 2 {players[1].coins}, Seat 3 {players[2].coins}, Seat 4 {players[3].coins}."
    }
  },
  "limits": {
    "rounds": 14,
    "rounds_max": 14,
    "actions_max": 1000,
    "deadline_s": 120
  }
}
````
