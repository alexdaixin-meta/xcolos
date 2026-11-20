# 25 coder

- time: 2026-11-20T02:38:31+00:00 (57.8s)  model: rl-muse-spark-1-3-sglang-playground
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 96c360b70c2f4c9d, reply sha256 4346191150ec0303

## Sent (the whole conversation)

````
[
  {
    "role": "user",
    "content": "# Task: write the XColos game file for \"One Night Revolution: Ten Nights, Hidden Ledger\"\n\nWrite the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.\n\n## The game\n\nPlayers: 5 to 5; set `meta.players` to {\"min\": 5, \"max\": 5, \"suggested\": 5} (the suggested size is the one the game plays best at).\n\nSETUP: 5 players. Each starts with 0 total points, 0 Rebel points, 0 Informant points. Before round 1 the engine lists all 10 unordered pairs of players and shuffles the list secretly. This is the only random event. In round r (r=1 to 10) the pair in position r is the Informants; the other 3 are Rebels. Every player is Informant in exactly 4 rounds with each other player as partner exactly once, and Rebel in exactly 6 rounds. Players are told this rule but not the order. EACH ROUND, in order: 1. ROLES: Each player is privately told Rebel or Informant for this round. Each Informant is also privately told who the other Informant is. 2. NIGHT (simultaneous): Every player privately names one other player as target. A Rebel target is investigated. An Informant target is framed. An Informant may name any other player including the partner; framing a partner has no extra effect. 3. NIGHT RESULTS: Each Rebel is privately told one result about their target: 'Informant' if the target is an Informant this round OR at least one Informant framed that target this round, otherwise 'Rebel'. A 'Rebel' result is always true; an 'Informant' result may be true or a frame. Informants receive no result. 4. CLAIMS (simultaneous): Every player writes one short message, e.g. claimed role, target or result. Lying allowed. All messages then shown to everyone. 5. RESPONSES (simultaneous): Every player writes one more short message. All shown to everyone. 6. VOTE (simultaneous): Every player names one other player to Terminate. All votes showing who voted for whom are then announced publicly. 7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise every player tied for the most votes is terminated. The round roles of terminated players only are announced publicly; no other roles revealed. 8. SCORING (hidden): Each Rebel who voted for an Informant gains 2 points. If at least one terminated player is an Informant, each Rebel gains 1 more point. Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3). Each Informant who was not terminated this round gains 2 points. Points gained while Rebel are also added to Rebel points; points gained while Informant also added to Informant points. No totals of any kind are announced during the game. Only the votes and the terminated roles are announced each round. Termination removes no one; all 5 play every round. After round 10 the engine announces every player's final total, Rebel points and Informant points and the game ends.\n\nHow the winner is decided: After 10 rounds the player with the highest total points wins. Tie-break: among tied, most Rebel points wins; if still tied, most Informant points wins; if still tied, draw.\n\n## The game as a script\n\nThis is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the\nfile step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`\nthat really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check\nthat fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.\n\nGAME: One Night Revolution: Ten Nights, Hidden Ledger (5 to 5 players, best with 5)\n\n5 players play 10 rounds as rotating Rebels and Informants with framing, claims, and termination votes for hidden points.\n\nSTATE (every item below must exist in the file):\n  - each player: total_points (number, starts 0); only its owner sees it. total hidden points\n  - each player: rebel_points (number, starts 0); only its owner sees it. points earned while Rebel\n  - each player: informant_points (number, starts 0); only its owner sees it. points earned while Informant\n  - each player: current_role (text, starts ''); only its owner sees it. Rebel or Informant this round\n  - each player: partner (number, starts 0); only its owner sees it. other Informant seat this round, 0 if Rebel\n  - each player: target (number, starts 0); only its owner sees it. night target seat\n  - each player: investigation_result (text, starts ''); only its owner sees it. Rebel night result Rebel or Informant, empty for Informants\n  - each player: claim_msg (text, starts ''); everyone sees it. round claim message shown to all\n  - each player: response_msg (text, starts ''); everyone sees it. round response message shown to all\n  - each player: vote (number, starts 0); everyone sees it. seat voted to Terminate\n  - each player: is_terminated (bool, starts False); everyone sees it. terminated this round\n  - each player: revealed_role (text, starts ''); everyone sees it. round role announced if terminated else empty\n  - the table: round_number (number, starts 1); everyone sees it. current round 1 to 10\n  - the table: pair_order (list, starts []); hidden from all players. secret shuffled list of all 10 unordered pairs, position r is Informants in round r\n  - the table: terminated_informant_count (number, starts 0); everyone sees it. number of terminated players who were Informant this round\n  - parameters, each kept as a table attribute: num_players = 5, num_rounds = 10, num_pairs = 10, initial_points = 0, informant_rounds_per_player = 4, rebel_rounds_per_player = 6, rebel_correct_vote_gain = 2, rebel_team_bonus = 1, informant_per_misdirected_gain = 1, informant_survival_gain = 2, termination_min_votes = 2\n\nINITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):\n  1. Each of the 5 players starts with 0 total points, 0 Rebel points and 0 Informant points.\n  2. The engine lists all 10 unordered pairs of the 5 players and shuffles the list secretly as pair_order.\n  3. This shuffle is the only random event and players are told the schedule rule but not the order.\n  4. The engine sets game round_number to 1.\n\nEACH ROUND (steps in order; the round repeats until an ending):\n  1. [update] all players. What happens: sets each player current_role and partner from pair_order for game.round_number; clears is_terminated, revealed_role, target, vote, investigation_result\n  2. [sync] all players. What happens: privately sends each player current_role; Informants also receive partner\n  3. [poll] all players answers: {'type': 'choice', 'prompt': 'name one other player as night target'}. What happens: sets player.target; Rebel target is investigated and Informant target is framed\n  4. [update] all players. What happens: sets player.investigation_result to Informant if target current_role is Informant or target was framed by any Informant, else Rebel; Informants keep empty\n  5. [sync] all players. What happens: privately sends each Rebel investigation_result; Informants receive no result\n  6. [poll] all players answers: {'type': 'text', 'prompt': 'write one short claim message'}. What happens: sets player.claim_msg and broadcasts to all as Seat {seat} says: {value}\n  7. [poll] all players answers: {'type': 'text', 'prompt': 'write one short response message'}. What happens: sets player.response_msg and broadcasts to all as Seat {seat} says: {value}\n  8. [poll] all players answers: {'type': 'choice', 'prompt': 'name one other player to Terminate'}. What happens: sets player.vote\n  9. [tell] all players. What happens: announces all player.vote showing who voted for whom using vote\n  10. [update] all players. What happens: sets player.is_terminated: if no seat has 2 or more votes then false for all, else true for seats tied for most votes; sets player.revealed_role to current_role if is_terminated else empty; sets game.terminated_informant_count\n  11. [tell] all players. What happens: announces player.is_terminated and player.revealed_role for terminated players only\n  12. [update] all players. What happens: adds hidden points: Rebels who voted for an Informant gain 2 to total_points and rebel_points; if terminated_informant_count >=1 each Rebel gains 1 more to total_points and rebel_points; each Informant gains 1 per Rebel who voted for a Rebel to total_points and informant_points; each Informant with is_terminated false gains 2 to total_points and informant_points; increments game.round_number; nothing about points is announced\n  13. [check] all players. What happens: continues if game.round_number <= 10, otherwise ends and announces total_points, rebel_points and informant_points\n\nRULES (each is tested by an independent scenario; the game must play every one exactly):\n  R1. When the game starts, then each player has 0 total points, 0 Rebel points and 0 Informant points.\n  R2. When the game is played, then there are 10 rounds and in round r the pair in position r of the shuffled 10 pairs is the Informants.\n  R3. When the schedule is used, then each player is Informant in exactly 4 rounds with each other player as partner exactly once and Rebel in exactly 6 rounds.\n  R4. When a round starts, then each player is privately told Rebel or Informant and each Informant is told who the other Informant is.\n  R5. When night happens, then every player simultaneously names one other player as target.\n  R6. When night targets are set, then a Rebel target is investigated and an Informant target is framed, and an Informant may target anyone including the partner with no extra effect for framing a partner.\n  R7. When night results are given, then each Rebel is privately told Informant if the target is an Informant this round or at least one Informant framed that target, otherwise Rebel.\n  R8. When night results are given, then a Rebel result is always true and an Informant result may be true or a frame.\n  R9. When night results are given, then Informants receive no result.\n  R10. When claims happen, then every player simultaneously writes one short message with lying allowed and all messages are then shown to everyone.\n  R11. When responses happen, then every player simultaneously writes one more short message and all are then shown to everyone.\n  R12. When voting happens, then every player simultaneously names one other player to Terminate and all votes showing who voted for whom are announced publicly.\n  R13. When votes are counted, then if no player received 2 or more votes nobody is terminated.\n  R14. When at least one player received 2 or more votes, then every player tied for the most votes is terminated.\n  R15. When termination is announced, then only the round roles of terminated players are announced publicly and no other roles are revealed.\n  R16. When scoring happens, then each Rebel who voted for an Informant gains 2 points.\n  R17. When scoring happens, then if at least one terminated player is an Informant each Rebel gains 1 more point.\n  R18. When scoring happens, then each Informant gains 1 point for every Rebel who voted for a Rebel.\n  R19. When scoring happens, then each Informant who was not terminated this round gains 2 points.\n  R20. When points are gained while Rebel, then they are also added to Rebel points and when gained while Informant also added to Informant points.\n  R21. When the game is played, then no totals of any kind are announced during the game and only votes and terminated roles are announced each round.\n  R22. When termination happens, then it removes no one and all 5 play every round.\n  R23. When round 10 ends, then the engine announces every player's final total, Rebel points and Informant points and the game ends.\n  R24. When the game ends, then the player with the highest total points wins with tie-break most Rebel points then most Informant points then draw.\n\nOFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):\n  - night target | asked: all players | options: any other living seat except self: the 4 other seats\n  - claim message | asked: all players | options: any short text, lying allowed\n  - response message | asked: all players | options: any short text, lying allowed\n  - vote to Terminate | asked: all players | options: any other living seat except self: the 4 other seats\n\nEVALUATION (how the game ends and who wins; decided by calculation):\n  - the game ends when: game.round_number > 10\n  - each player's standing: you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)\n  - how the result is decided: standing is total_points, tie-break most rebel_points then most informant_points; highest wins and tied top share the win\n  - the end screen states the final scores or deciding figures, and a short model-written summary of how the game went\n\n## Recipe: a shared deck and hidden hands (tested on the engine)\n\nWhen the script has a deck and hands, both must exist as attributes, and setup must really deal. Declare the hand as a PLAYER attribute\n`{\"key\": \"hand\", \"visible\": \"ally\", \"type\": \"list\", \"initial\": []}` (only its owner sees it; a player attribute is never `none`) and the\ndeck as a TABLE attribute `{\"key\": \"deck\", \"visible\": \"none\", \"type\": \"list\", \"initial\": [every card, one entry per copy]}`, plus a table text\nattribute `pick` (visible `none`, initial `\"\"`) to hold the card just drawn. Then ONE draw, of a random card into seat N's hand, is three operations\nin an `update`'s `do` list, in this order:\n\n  {\"set\":    {\"key\": \"pick\", \"value\": {\"calc\": \"deck[int(uniform(0, len(deck)))]\"}}},\n  {\"append\": {\"player\": N, \"key\": \"hand\", \"value\": {\"calc\": \"pick\"}}},\n  {\"remove\": {\"key\": \"deck\", \"value\": {\"calc\": \"pick\"}}}\n\nDealing two cards to three seats is that block repeated twice for each seat (6 draws), never a fixed list written into `initial`: the deal\nis random and different each match, and every player's hand must differ. A card coming back is `{\"append\": {\"key\": \"deck\", ...}}` and\n`{\"remove\": {\"player\": N, \"key\": \"hand\", ...}}`. \"Has a card of role R\" is `\"R\" in you.hand`. Use `{\"if\": {\"calc\": ...}}` on an operation to make\nit conditional. Never declare `hand` or `deck` and then leave them unchanged: the rules would then claim cards that do not exist.\n\n## Pattern: offer each seat only what it may do (tested on the engine)\n\nA question's options may come from state, and the state can differ for every player. So make who may do what part of the OFFER, never a check\nafterwards. Declare a PLAYER list attribute (say `offer`, visible `ally`), and set it for everyone in one `update` just before the question,\nfrom each player's own attributes and the table's:\n\n  {\"set\": {\"players\": \"all\", \"key\": \"offer\",\n           \"value\": {\"calc\": \"['wait'] + (['buy'] if you.coins >= price else []) + (['block'] if you.seat == target else [])\"}}}\n\nthen ask with `\"answer\": {\"type\": \"choice\", \"options\": {\"attribute\": \"offer\"}}` and `to` naming who is asked. `you` is each player in turn, and a\nlist can be built with `+` and `(... if ... else [])`. Whatever a seat may not do is not in its list: a seat that cannot pay is not offered the\npaid action, only the target of an action is offered a block against it, a player already out is not asked. Do the same for a target: put the\nlegal seats in a list attribute.\n\nWhen only one option is left (the last unused action, the only legal card), still ask the question: the engine answers a choice with one\noption for the seat, with no model call, and records it as the seat's move. Do not skip the question with a `when` and set the answer\nyourself: that move is then missing from the match, and a test that scripts it fails.\n\nWhen a player is eliminated, set the PLATFORM status as well as your own counters: declare a status for it (`{\"id\": \"out\", \"acts\": false}`) next to `playing` and\nrun `{\"set_status\": {\"player\": N, \"to\": \"out\", \"text\": \"Seat {player} is out.\"}}`. Without it the platform and the console show the player as still in the game, and the\nprompts list them as playing, whatever your own `alive` attribute says. Name the cards it reveals in the same announcement.\n\nDo NOT offer a broad list and then refuse illegal answers and ask again (a `repeat` that asks, checks, and asks again, or an update that removes\nan option the player just picked). It costs a model call, it lets a model choose something illegal, and the pipeline reports it as a failure:\n\"an option is offered and then refused\". If you find yourself writing a step called \"refuse...\", \"check the answer is legal\" or \"not allowed\",\nyou are filling the wrong list: fix the offer.\n\n## Rounds and the safety cap\n\nIf the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed\nround count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of\nrounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap\nis reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.\n\n## The interface the file must use\n\nIndependent tests were written against these names and you cannot see them, so use them exactly.\n\n- each player: `total_points` (number, visible: ally, starts 0): total hidden points\n- each player: `rebel_points` (number, visible: ally, starts 0): points earned while Rebel\n- each player: `informant_points` (number, visible: ally, starts 0): points earned while Informant\n- each player: `vote` (number, visible: public, starts 0): seat voted to Terminate\n- each player: `is_terminated` (bool, visible: public, starts False): terminated this round\n- each player: `revealed_role` (text, visible: public, starts ''): round role announced if terminated else empty\n- the table: `terminated_informant_count` (number, visible: public, starts 0): number of terminated players who were Informant this round\n- parameters (each must be an attribute holding this value, never a number buried in a step): num_players = 5, num_rounds = 10, num_pairs = 10, initial_points = 0, informant_rounds_per_player = 4, rebel_rounds_per_player = 6, rebel_correct_vote_gain = 2, rebel_team_bonus = 1, informant_per_misdirected_gain = 1, informant_survival_gain = 2, termination_min_votes = 2\n- the game ends with ONE ending whose `rank_by` is `you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win\n- anything else the game needs to keep track of is yours to design: name it as you like.\n\n## How the platform works\n\nThe complete file format reference and two example games are in your system prompt. Follow them exactly: every key an\naction accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: write ONE\nending, whose `when` is a calc condition and whose `rank_by` is the ranking in the interface below; no `result`, no `winner`, no prose\nending, no `llm` in an ending. Use calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when` `{\"prose\": \"<the judged sentence, verbatim>\"}`: a referee answers it\ntrue or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no\nmodel answers. Choices made at the same moment are a `poll`. The end screen announces only the result: the ending's `text` says who won (`{result}`) and the final scores or deciding figures with\nplaceholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with `rank_by` as both examples do.\n\n- Mistakes the loader has refused before, so avoid them:\n  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table\n    attributes.) For something only its owner should see, use `ally`.\n  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.\n  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on\n    attributes, or with `set` operations in `setup`, instead.\n  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.\n  * TALK that everyone hears is a `poll` with a free-text answer and `\"broadcast\": {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}`\n    (or `\"broadcast\": \"all\"` with no `text`, which shows each message word for word). A broadcast may use ONLY `{value}` (what that\n    player answered), `{seat}` (who) and table attributes: a name bound by `verify` is not set yet, so `{talk_msg}` reaches players as\n    the literal braces, and the loader refuses it.\n  * WHO answered what (who challenged, who blocked, who raised a hand) is `\"store\": \"attr\"` on the `poll` or `ask`, naming a PLAYER\n    attribute declared under `attributes.player` (a `text` attribute for a choice). Each player's own answer is written to it and a calc reads\n    them all: `count(p.said == 'Challenge' for p in players)`, `min([p.seat for p in players if p.said == 'Challenge'])`. A `verify`\n    tally gives ONE winning value and loses who gave which: one \"Challenge\" against three \"Pass\" tallies to \"Pass\". Never write a seat\n    number into a calc by guessing (`2 if active_seat == 1 else 1`); read it from a stored answer. Reset the stored attribute with a `set`\n    to `\"\"` (`players: \"all\"`) before each poll, so last round's answers do not count.\n  * `meta.players` carries `min`, `max` and `suggested`, exactly as the task gives them: the console fills a table to the suggested size and the real-model tests play at it.\n  * THE RULES TEXT SAYS BOTH OUTCOMES. For every decision point (a challenge, a block, a claim, a cost), say what happens when it is true AND when it is false,\n    and whether the action still goes ahead; a player decides on this text and nothing else, and a check compares it with each numbered rule.\n  * THE RULES TEXT PLAYERS READ IS THE DESIGN'S. `meta.rules` (the brief) says each mechanic in the design's own words and in its order: how a challenge is resolved,\n    what a block costs, who counts when several answer. Do not paraphrase a mechanic: a reordered sentence is a different rule.\n  * BOOKKEEPING IS HIDDEN. An attribute that only the game's own steps read (a scratch value, a counter, a copy of an option list, who is blocking) is declared\n    hidden (`none` on the table, `ally` on a player), not `public`: every public attribute is printed into every player's prompt on every turn.\n  * THE DEAL REMOVES WHAT IT DEALS. Every card put into a hand is taken out of the deck in the same step (see the deck recipe); after setup, deck plus hands holds\n    exactly the cards the rules start with, and no card appears more often than the rules say.\n  * OFFER ONLY WHAT A SEAT MAY DO. Build each seat's option list from its own state (see the offer pattern) and never refuse an answer afterwards\n    and ask again: an option that is offered, taken and then taken back fails the pipeline's check.\n  * A QUESTION WITH ONE POSSIBLE ANSWER IS NEVER WORTH ASKING (\"pass\" and nothing else): the engine answers it itself, but write the step so\n    it is not asked at all, and never announce a seat's answer when the seat was not asked (eliminated players).\n  * ASK ONLY WHAT IS NEEDED. Put a `when` on a question that applies only sometimes: a target is asked only for the actions that take one\n    (`\"when\": {\"calc\": \"chosen_action in ['Steal', 'Assassinate', 'Coup']\"}`), a block only when something can be blocked.\n  * A counter must not go below what the rules allow. Guard every payment and loss with an `if` (`\"if\": {\"calc\": \"you.coins >= cost\"}`,\n    or check it before the action is allowed), and treat an action the player cannot afford as the cheapest legal one, as the rules say.\n  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {\"bind\": \"name\"}`; a later `update`\n    stores it with `\"value\": \"$name\"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the\n    answers away, and every score that depends on them stays at its starting value.\n  * An attribute declared `\"mutable\": false` is set once, by an `initialize` step, and any other step that sets it crashes the game\n    (\"declared static and has already been dealt\"). To set a hidden type or a starting value at setup, either use an `initialize`\n    step or leave the attribute mutable.\n  * Do not write steps that do nothing (for example an `if` of `{\"calc\": \"False\"}`), or two polls where one will do.\n  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,\n    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.\n- Keep a round to at most 20 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the\n  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.\n\n## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)\n\nFor \"each player chooses in private, then the choices decide the score\":\n1. One `ask` per seat, addressed with `{\"where\": \"you.seat == N\"}`, with `\"verify\": {\"bind\": \"aN\"}`. The answer exists only because it is bound.\n2. One `update` after both. It `set`s the bound answers into table attributes with `\"$aN\"`, and `adjust`s each player's score with a\n   `calc` that may use `$aN` and `if ... else`.\n3. A `check` with `when` and `against`, and ONE ending in `end` whose `rank_by` is `you.score`: the engine ranks the players by it.\nEvery attribute is set by a step that runs. Adapt this; do not invent another way to store answers.\n\n```json\n{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"match_or_miss\",\n    \"name\": \"Match or Miss\",\n    \"players\": {\n      \"min\": 2,\n      \"max\": 2\n    },\n    \"blurb\": \"Two players choose A or B in secret; seat 1 scores when they match, seat 2 when they differ.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"rounds_left\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"last_a1\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_a2\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      }\n    ]\n  },\n  \"rules\": \"Three rounds. Each round both players secretly choose A or B. If the choices match, seat 1 scores a point; if they differ, seat 2 does. The higher score wins.\",\n  \"setup\": [\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"ask\",\n      \"label\": \"seat 1 chooses\",\n      \"to\": {\n        \"where\": \"you.seat == 1\"\n      },\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": [\n          \"A\",\n          \"B\"\n        ]\n      },\n      \"verify\": {\n        \"bind\": \"a1\"\n      },\n      \"text\": \"Choose A or B. Your opponent will not see it.\"\n    },\n    {\n      \"use\": \"ask\",\n      \"label\": \"seat 2 chooses\",\n      \"to\": {\n        \"where\": \"you.seat == 2\"\n      },\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": [\n          \"A\",\n          \"B\"\n        ]\n      },\n      \"verify\": {\n        \"bind\": \"a2\"\n      },\n      \"text\": \"Choose A or B. Your opponent will not see it.\"\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"score the round\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"last_a1\",\n            \"value\": \"$a1\"\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_a2\",\n            \"value\": \"$a2\"\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"score\",\n            \"value\": {\n              \"calc\": \"1 if $a1 == $a2 else 0\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"score\",\n            \"value\": {\n              \"calc\": \"0 if $a1 == $a2 else 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"key\": \"rounds_left\",\n            \"value\": -1\n          }\n        }\n      ],\n      \"text\": \"Seat 1 chose {last_a1}, seat 2 chose {last_a2}.\"\n    },\n    {\n      \"use\": \"check\",\n      \"label\": \"is it over\",\n      \"when\": {\n        \"calc\": \"rounds_left <= 0\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"rounds_left <= 0\"\n      },\n      \"rank_by\": \"you.score\",\n      \"text\": \"{result} wins.\"\n    }\n  }\n}\n```\n\nYour file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every\nattribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and\nshown your file again; fix what is wrong and keep the rest.\n\n## Guidance from the last attempt\n\nThe previous attempt had problems:\n\nReset per-round state every round: at round start set all players is_terminated=False and revealed_role='' and set table terminated_informant_count=0, then compute termination fresh as all players with max votes if max>=termination_min_votes and count only this round's terminated Informants. Do not use elimination; ensure all 5 players get target/claim/response/vote options every round.\n"
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"one-night-revolution-ten-nights\",\n    \"name\": \"One Night Revolution: Ten Nights, Hidden Ledger\",\n    \"players\": {\n      \"min\": 5,\n      \"max\": 5,\n      \"suggested\": 5\n    },\n    \"blurb\": \"5 players play 10 rounds as rotating Rebels and Informants with framing, claims, and termination votes for hidden points.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"total_points\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"rebel_points\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"informant_points\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"current_role\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Rebel\",\n          \"Informant\",\n          \"\"\n        ]\n      },\n      {\n        \"key\": \"partner\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"target\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"investigation_result\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Rebel\",\n          \"Informant\",\n          \"\"\n        ]\n      },\n      {\n        \"key\": \"claim_msg\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"response_msg\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"vote\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"is_terminated\",\n        \"visible\": \"public\",\n        \"type\": \"bool\",\n        \"initial\": false\n      },\n      {\n        \"key\": \"revealed_role\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Rebel\",\n          \"Informant\",\n          \"\"\n        ]\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"pair_order\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"terminated_informant_count\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"num_players\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 5\n      },\n      {\n        \"key\": \"num_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 10\n      },\n      {\n        \"key\": \"num_pairs\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 10\n      },\n      {\n        \"key\": \"initial_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"informant_rounds_per_player\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 4\n      },\n      {\n        \"key\": \"rebel_rounds_per_player\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 6\n      },\n      {\n        \"key\": \"rebel_correct_vote_gain\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"rebel_team_bonus\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"informant_per_misdirected_gain\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"informant_survival_gain\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"termination_min_votes\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      }\n    ]\n  },\n  \"rules\": \"{num_players} players play {num_rounds} rounds. Each player starts with {initial_points} total points, {initial_points} Rebel points and {initial_points} Informant points. Before round 1 the engine lists all {num_pairs} unordered pairs of players and shuffles the list secretly; this shuffle is the only random event. In round r the pair in position r is the Informants and the other 3 are Rebels, so each player is Informant in exactly {informant_rounds_per_player} rounds with each other player as partner exactly once and Rebel in exactly {rebel_rounds_per_player} rounds. You are told this schedule rule but not the order.\\n\\nEach round: 1. ROLES: each player is privately told Rebel or Informant for this round, and each Informant is also privately told who the other Informant is; Rebels are told no partner. 2. NIGHT: every player simultaneously names one other player as target; a Rebel target is investigated and an Informant target is framed, and an Informant may name anyone including the partner with no extra effect for framing a partner. 3. NIGHT RESULTS: each Rebel is privately told Informant if the target is an Informant this round or at least one Informant framed that target this round, otherwise Rebel; a Rebel result is always true and an Informant result may be true or a frame; Informants receive no result. 4. CLAIMS: every player simultaneously writes one short message, lying allowed, then all messages are shown to everyone. 5. RESPONSES: every player simultaneously writes one more short message, then all are shown to everyone. 6. VOTE: every player simultaneously names one other player to Terminate, then all votes showing who voted for whom are announced publicly. 7. TERMINATION: if no player received {termination_min_votes} or more votes nobody is terminated; otherwise every player tied for the most votes is terminated, and only the round roles of terminated players are announced publicly while no other roles are revealed; termination removes no one and all {num_players} play every round. 8. SCORING (hidden): a Rebel who voted for an Informant gains {rebel_correct_vote_gain} points and a Rebel who voted for a Rebel gains nothing for that vote; if at least one terminated player is an Informant each Rebel gains {rebel_team_bonus} more point, and if none is an Informant there is no bonus; each Informant gains {informant_per_misdirected_gain} point for every Rebel who voted for a Rebel; each Informant who was not terminated gains {informant_survival_gain} points and a terminated Informant gains no survival points; points gained while Rebel are also added to Rebel points and points gained while Informant also added to Informant points; no totals of any kind are announced during the game and only votes and terminated roles are announced each round.\\n\\nAfter round {num_rounds} the engine announces every player's final total, Rebel points and Informant points and the game ends. The highest total points wins; tie-break most Rebel points, then most Informant points, then tied top share the win.\",\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"starting points and parameters\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"initial_points\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"initial_points\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"initial_points\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"num_players\",\n            \"value\": {\n              \"calc\": \"num_players\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"num_rounds\",\n            \"value\": {\n              \"calc\": \"num_rounds\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"num_pairs\",\n            \"value\": {\n              \"calc\": \"num_pairs\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"terminated_informant_count\",\n            \"value\": 0\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"shuffle the pairs\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"pair_order\",\n            \"value\": {\n              \"calc\": \"[pair[1] for pair in sorted([[uniform(0, 1), [1, 2]], [uniform(0, 1), [1, 3]], [uniform(0, 1), [1, 4]], [uniform(0, 1), [1, 5]], [uniform(0, 1), [2, 3]], [uniform(0, 1), [2, 4]], [uniform(0, 1), [2, 5]], [uniform(0, 1), [3, 4]], [uniform(0, 1), [3, 5]], [uniform(0, 1), [4, 5]]])]\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"tell\",\n      \"label\": \"the schedule rule\",\n      \"to\": \"all\",\n      \"text\": \"There are {num_rounds} rounds. The {num_pairs} unordered pairs were shuffled secretly; in round r that pair are the Informants. Each player is Informant in exactly {informant_rounds_per_player} rounds with each other player once, and Rebel in {rebel_rounds_per_player} rounds. The order is secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"round 1 begins\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"update\",\n      \"phase\": \"roles\",\n      \"label\": \"assign roles\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"target\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"vote\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"investigation_result\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"is_terminated\",\n            \"value\": false\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"revealed_role\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"claim_msg\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"response_msg\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"terminated_informant_count\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1]\"\n            },\n            \"key\": \"current_role\",\n            \"value\": \"Informant\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"not (you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1])\"\n            },\n            \"key\": \"current_role\",\n            \"value\": \"Rebel\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"you.seat == pair_order[round_number - 1][0]\"\n            },\n            \"key\": \"partner\",\n            \"value\": {\n              \"calc\": \"pair_order[round_number - 1][1]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"you.seat == pair_order[round_number - 1][1]\"\n            },\n            \"key\": \"partner\",\n            \"value\": {\n              \"calc\": \"pair_order[round_number - 1][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"not (you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1])\"\n            },\n            \"key\": \"partner\",\n            \"value\": 0\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"phase\": \"roles\",\n      \"label\": \"private roles\",\n      \"mode\": \"self\",\n      \"to\": \"acting\",\n      \"text\": \"Round {round_number}: your private role and partner if Informant.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"night\",\n      \"label\": \"night targets\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"player\",\n        \"exclude_self\": true\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"night_common\"\n      },\n      \"store\": \"target\",\n      \"text\": \"Name one other player as night target. A Rebel target is investigated and an Informant target is framed.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"night\",\n      \"label\": \"night results\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"you.current_role == 'Rebel'\"\n            },\n            \"key\": \"investigation_result\",\n            \"value\": {\n              \"calc\": \"'Informant' if (any(p.seat == you.target and p.current_role == 'Informant' for p in players) or any(p.current_role == 'Informant' and p.target == you.target for p in players)) else 'Rebel'\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"phase\": \"night\",\n      \"label\": \"private results\",\n      \"mode\": \"self\",\n      \"to\": {\n        \"where\": \"you.current_role == 'Rebel'\"\n      },\n      \"text\": \"Your private night result for round {round_number}.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"claims\",\n      \"label\": \"claims\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"text\",\n        \"max_words\": 30\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"claim_common\"\n      },\n      \"store\": \"claim_msg\",\n      \"broadcast\": {\n        \"to\": \"all\",\n        \"text\": \"Seat {seat} says: {value}\"\n      },\n      \"text\": \"Write one short claim message, e.g. claimed role, target or result. Lying allowed.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"claims\",\n      \"label\": \"responses\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"text\",\n        \"max_words\": 30\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"response_common\"\n      },\n      \"store\": \"response_msg\",\n      \"broadcast\": {\n        \"to\": \"all\",\n        \"text\": \"Seat {seat} says: {value}\"\n      },\n      \"text\": \"Write one more short response message.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"vote\",\n      \"label\": \"termination vote\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"player\",\n        \"exclude_self\": true\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"vote_common\"\n      },\n      \"store\": \"vote\",\n      \"text\": \"Name one other player to Terminate.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"vote\",\n      \"label\": \"votes announced\",\n      \"to\": \"all\",\n      \"text\": \"Votes round {round_number}: seat 1 voted {players[0].vote}, seat 2 voted {players[1].vote}, seat 3 voted {players[2].vote}, seat 4 voted {players[3].vote}, seat 5 voted {players[4].vote}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"termination\",\n      \"label\": \"termination\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"is_terminated\",\n            \"value\": {\n              \"calc\": \"count(p.vote == you.seat for p in players) == max([count(p.vote == s for p in players) for s in [1, 2, 3, 4, 5]]) and max([count(p.vote == s for p in players) for s in [1, 2, 3, 4, 5]]) >= termination_min_votes\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"revealed_role\",\n            \"value\": {\n              \"calc\": \"you.current_role if you.is_terminated else ''\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"terminated_informant_count\",\n            \"value\": {\n              \"calc\": \"count(p.is_terminated and p.current_role == 'Informant' for p in players)\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"termination\",\n      \"label\": \"termination announced\",\n      \"to\": \"all\",\n      \"text\": \"Terminated round {round_number}: seat 1 {players[0].is_terminated} {players[0].revealed_role}, seat 2 {players[1].is_terminated} {players[1].revealed_role}, seat 3 {players[2].is_terminated} {players[2].revealed_role}, seat 4 {players[3].is_terminated} {players[3].revealed_role}, seat 5 {players[4].is_terminated} {players[4].revealed_role}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"scoring\",\n      \"label\": \"hidden scoring\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"you.current_role == 'Rebel' and any(p.seat == you.vote and p.current_role == 'Informant' for p in players)\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"you.current_role == 'Rebel' and any(p.seat == you.vote and p.current_role == 'Informant' for p in players)\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"you.current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": \"all\",\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"you.current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.current_role == 'Informant'\"\n            },\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and any(q.seat == p.vote and q.current_role == 'Rebel' for q in players) for p in players) * informant_per_misdirected_gain\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.current_role == 'Informant'\"\n            },\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and any(q.seat == p.vote and q.current_role == 'Rebel' for q in players) for p in players) * informant_per_misdirected_gain\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.current_role == 'Informant' and not you.is_terminated\"\n            },\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"players\": {\n              \"where\": \"you.current_role == 'Informant' and not you.is_terminated\"\n            },\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"scoring\",\n      \"label\": \"after round 10\",\n      \"when\": {\n        \"calc\": \"round_number > num_rounds\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds\"\n      },\n      \"rank_by\": \"you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points\",\n      \"text\": \"Winner: {result}. Final totals: seat 1 {players[0].total_points} (Rebel {players[0].rebel_points}, Informant {players[0].informant_points}), seat 2 {players[1].total_points} (Rebel {players[1].rebel_points}, Informant {players[1].informant_points}), seat 3 {players[2].total_points} (Rebel {players[2].rebel_points}, Informant {players[2].informant_points}), seat 4 {players[3].total_points} (Rebel {players[3].rebel_points}, Informant {players[3].informant_points}), seat 5 {players[4].total_points} (Rebel {players[4].rebel_points}, Informant {players[4].informant_points}).\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 10,\n    \"rounds_max\": 10,\n    \"actions_max\": 500,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: playing it with random seats failed: seed 1, 5 players: the match crashed: FlowError: \"you.current_role == 'Rebel' and any(p.seat == you.vote and p.current_role == 'Informant' for p in players)\" reads `you` where there is no player\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"one-night-revolution-ten-nights\",\n    \"name\": \"One Night Revolution: Ten Nights, Hidden Ledger\",\n    \"players\": {\n      \"min\": 5,\n      \"max\": 5,\n      \"suggested\": 5\n    },\n    \"blurb\": \"5 players play 10 rounds as rotating Rebels and Informants with framing, claims, and termination votes for hidden points.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"total_points\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"rebel_points\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"informant_points\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"current_role\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Rebel\",\n          \"Informant\",\n          \"\"\n        ]\n      },\n      {\n        \"key\": \"partner\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"target\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"investigation_result\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Rebel\",\n          \"Informant\",\n          \"\"\n        ]\n      },\n      {\n        \"key\": \"claim_msg\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"response_msg\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"vote\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"is_terminated\",\n        \"visible\": \"public\",\n        \"type\": \"bool\",\n        \"initial\": false\n      },\n      {\n        \"key\": \"revealed_role\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Rebel\",\n          \"Informant\",\n          \"\"\n        ]\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"pair_order\",\n        \"visible\": \"none\",\n        \"type\": \"list\",\n        \"initial\": []\n      },\n      {\n        \"key\": \"terminated_informant_count\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"num_players\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 5\n      },\n      {\n        \"key\": \"num_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 10\n      },\n      {\n        \"key\": \"num_pairs\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 10\n      },\n      {\n        \"key\": \"initial_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"informant_rounds_per_player\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 4\n      },\n      {\n        \"key\": \"rebel_rounds_per_player\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 6\n      },\n      {\n        \"key\": \"rebel_correct_vote_gain\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"rebel_team_bonus\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"informant_per_misdirected_gain\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"informant_survival_gain\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"termination_min_votes\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      }\n    ]\n  },\n  \"rules\": \"{num_players} players play {num_rounds} rounds. Each player starts with {initial_points} total points, {initial_points} Rebel points and {initial_points} Informant points. Before round 1 the engine lists all {num_pairs} unordered pairs of players and shuffles the list secretly; this shuffle is the only random event. In round r the pair in position r is the Informants and the other 3 are Rebels, so each player is Informant in exactly {informant_rounds_per_player} rounds with each other player as partner exactly once and Rebel in exactly {rebel_rounds_per_player} rounds. You are told this schedule rule but not the order.\\n\\nEach round: 1. ROLES: each player is privately told Rebel or Informant for this round, and each Informant is also privately told who the other Informant is; Rebels are told no partner. 2. NIGHT: every player simultaneously names one other player as target; a Rebel target is investigated and an Informant target is framed, and an Informant may name anyone including the partner with no extra effect for framing a partner. 3. NIGHT RESULTS: each Rebel is privately told Informant if the target is an Informant this round or at least one Informant framed that target this round, otherwise Rebel; a Rebel result is always true and an Informant result may be true or a frame; Informants receive no result. 4. CLAIMS: every player simultaneously writes one short message, lying allowed, then all messages are shown to everyone. 5. RESPONSES: every player simultaneously writes one more short message, then all are shown to everyone. 6. VOTE: every player simultaneously names one other player to Terminate, then all votes showing who voted for whom are announced publicly. 7. TERMINATION: if no player received {termination_min_votes} or more votes nobody is terminated; otherwise every player tied for the most votes is terminated, and only the round roles of terminated players are announced publicly while no other roles are revealed; termination removes no one and all {num_players} play every round. 8. SCORING (hidden): a Rebel who voted for an Informant gains {rebel_correct_vote_gain} points and a Rebel who voted for a Rebel gains nothing for that vote; if at least one terminated player is an Informant each Rebel gains {rebel_team_bonus} more point, and if none is an Informant there is no bonus; each Informant gains {informant_per_misdirected_gain} point for every Rebel who voted for a Rebel; each Informant who was not terminated gains {informant_survival_gain} points and a terminated Informant gains no survival points; points gained while Rebel are also added to Rebel points and points gained while Informant also added to Informant points; no totals of any kind are announced during the game and only votes and terminated roles are announced each round.\\n\\nAfter round {num_rounds} the engine announces every player's final total, Rebel points and Informant points and the game ends. The highest total points wins; tie-break most Rebel points, then most Informant points, then tied top share the win.\",\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"starting points and parameters\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"initial_points\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"initial_points\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"initial_points\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"terminated_informant_count\",\n            \"value\": 0\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"shuffle the pairs\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"pair_order\",\n            \"value\": {\n              \"calc\": \"[pair[1] for pair in sorted([[uniform(0, 1), [1, 2]], [uniform(0, 1), [1, 3]], [uniform(0, 1), [1, 4]], [uniform(0, 1), [1, 5]], [uniform(0, 1), [2, 3]], [uniform(0, 1), [2, 4]], [uniform(0, 1), [2, 5]], [uniform(0, 1), [3, 4]], [uniform(0, 1), [3, 5]], [uniform(0, 1), [4, 5]]])]\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"tell\",\n      \"label\": \"the schedule rule\",\n      \"to\": \"all\",\n      \"text\": \"There are {num_rounds} rounds. The {num_pairs} unordered pairs were shuffled secretly; in round r that pair are the Informants. Each player is Informant in exactly {informant_rounds_per_player} rounds with each other player once, and Rebel in {rebel_rounds_per_player} rounds. The order is secret.\"\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"round 1 begins\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"update\",\n      \"phase\": \"roles\",\n      \"label\": \"assign roles\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"target\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"vote\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"investigation_result\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"is_terminated\",\n            \"value\": false\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"revealed_role\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"claim_msg\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"response_msg\",\n            \"value\": \"\"\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"terminated_informant_count\",\n            \"value\": 0\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1]\"\n            },\n            \"key\": \"current_role\",\n            \"value\": \"Informant\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"not (you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1])\"\n            },\n            \"key\": \"current_role\",\n            \"value\": \"Rebel\"\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"you.seat == pair_order[round_number - 1][0]\"\n            },\n            \"key\": \"partner\",\n            \"value\": {\n              \"calc\": \"pair_order[round_number - 1][1]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"you.seat == pair_order[round_number - 1][1]\"\n            },\n            \"key\": \"partner\",\n            \"value\": {\n              \"calc\": \"pair_order[round_number - 1][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": {\n              \"where\": \"not (you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1])\"\n            },\n            \"key\": \"partner\",\n            \"value\": 0\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"phase\": \"roles\",\n      \"label\": \"private roles\",\n      \"mode\": \"self\",\n      \"to\": \"acting\",\n      \"text\": \"Round {round_number}: your private role and partner if Informant.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"night\",\n      \"label\": \"night targets\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"player\",\n        \"exclude_self\": true\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"night_common\"\n      },\n      \"store\": \"target\",\n      \"text\": \"Name one other player as night target. A Rebel target is investigated and an Informant target is framed.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"night\",\n      \"label\": \"night results\",\n      \"do\": [\n        {\n          \"set\": {\n            \"player\": 1,\n            \"key\": \"investigation_result\",\n            \"value\": {\n              \"calc\": \"'Informant' if (players[0].target == pair_order[round_number - 1][0] or players[0].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[0].target or players[pair_order[round_number - 1][1] - 1].target == players[0].target) else 'Rebel'\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Rebel'\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 2,\n            \"key\": \"investigation_result\",\n            \"value\": {\n              \"calc\": \"'Informant' if (players[1].target == pair_order[round_number - 1][0] or players[1].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[1].target or players[pair_order[round_number - 1][1] - 1].target == players[1].target) else 'Rebel'\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Rebel'\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 3,\n            \"key\": \"investigation_result\",\n            \"value\": {\n              \"calc\": \"'Informant' if (players[2].target == pair_order[round_number - 1][0] or players[2].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[2].target or players[pair_order[round_number - 1][1] - 1].target == players[2].target) else 'Rebel'\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Rebel'\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 4,\n            \"key\": \"investigation_result\",\n            \"value\": {\n              \"calc\": \"'Informant' if (players[3].target == pair_order[round_number - 1][0] or players[3].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[3].target or players[pair_order[round_number - 1][1] - 1].target == players[3].target) else 'Rebel'\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Rebel'\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 5,\n            \"key\": \"investigation_result\",\n            \"value\": {\n              \"calc\": \"'Informant' if (players[4].target == pair_order[round_number - 1][0] or players[4].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[4].target or players[pair_order[round_number - 1][1] - 1].target == players[4].target) else 'Rebel'\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Rebel'\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"phase\": \"night\",\n      \"label\": \"private results\",\n      \"mode\": \"self\",\n      \"to\": {\n        \"where\": \"you.current_role == 'Rebel'\"\n      },\n      \"text\": \"Your private night result for round {round_number}.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"claims\",\n      \"label\": \"claims\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"text\",\n        \"max_words\": 30\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"claim_common\"\n      },\n      \"store\": \"claim_msg\",\n      \"broadcast\": {\n        \"to\": \"all\",\n        \"text\": \"Seat {seat} says: {value}\"\n      },\n      \"text\": \"Write one short claim message, e.g. claimed role, target or result. Lying allowed.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"claims\",\n      \"label\": \"responses\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"text\",\n        \"max_words\": 30\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"response_common\"\n      },\n      \"store\": \"response_msg\",\n      \"broadcast\": {\n        \"to\": \"all\",\n        \"text\": \"Seat {seat} says: {value}\"\n      },\n      \"text\": \"Write one more short response message.\"\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"vote\",\n      \"label\": \"termination vote\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"player\",\n        \"exclude_self\": true\n      },\n      \"verify\": {\n        \"tally\": \"plurality\",\n        \"on_tie\": \"random\",\n        \"bind\": \"vote_common\"\n      },\n      \"store\": \"vote\",\n      \"text\": \"Name one other player to Terminate.\"\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"vote\",\n      \"label\": \"votes announced\",\n      \"to\": \"all\",\n      \"text\": \"Votes round {round_number}: seat 1 voted {players[0].vote}, seat 2 voted {players[1].vote}, seat 3 voted {players[2].vote}, seat 4 voted {players[3].vote}, seat 5 voted {players[4].vote}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"termination\",\n      \"label\": \"termination\",\n      \"do\": [\n        {\n          \"set\": {\n            \"player\": 1,\n            \"key\": \"is_terminated\",\n            \"value\": {\n              \"calc\": \"count(p.vote == 1 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 2,\n            \"key\": \"is_terminated\",\n            \"value\": {\n              \"calc\": \"count(p.vote == 2 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 3,\n            \"key\": \"is_terminated\",\n            \"value\": {\n              \"calc\": \"count(p.vote == 3 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 4,\n            \"key\": \"is_terminated\",\n            \"value\": {\n              \"calc\": \"count(p.vote == 4 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 5,\n            \"key\": \"is_terminated\",\n            \"value\": {\n              \"calc\": \"count(p.vote == 5 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 1,\n            \"key\": \"revealed_role\",\n            \"value\": {\n              \"calc\": \"players[0].current_role if players[0].is_terminated else ''\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 2,\n            \"key\": \"revealed_role\",\n            \"value\": {\n              \"calc\": \"players[1].current_role if players[1].is_terminated else ''\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 3,\n            \"key\": \"revealed_role\",\n            \"value\": {\n              \"calc\": \"players[2].current_role if players[2].is_terminated else ''\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 4,\n            \"key\": \"revealed_role\",\n            \"value\": {\n              \"calc\": \"players[3].current_role if players[3].is_terminated else ''\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"player\": 5,\n            \"key\": \"revealed_role\",\n            \"value\": {\n              \"calc\": \"players[4].current_role if players[4].is_terminated else ''\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"terminated_informant_count\",\n            \"value\": {\n              \"calc\": \"count(p.is_terminated and p.current_role == 'Informant' for p in players)\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"termination\",\n      \"label\": \"termination announced\",\n      \"to\": \"all\",\n      \"text\": \"Terminated round {round_number}: seat 1 {players[0].is_terminated} {players[0].revealed_role}, seat 2 {players[1].is_terminated} {players[1].revealed_role}, seat 3 {players[2].is_terminated} {players[2].revealed_role}, seat 4 {players[3].is_terminated} {players[3].revealed_role}, seat 5 {players[4].is_terminated} {players[4].revealed_role}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"scoring\",\n      \"label\": \"hidden scoring\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Rebel' and (players[0].vote == pair_order[round_number - 1][0] or players[0].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Rebel' and (players[0].vote == pair_order[round_number - 1][0] or players[0].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Rebel' and (players[1].vote == pair_order[round_number - 1][0] or players[1].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Rebel' and (players[1].vote == pair_order[round_number - 1][0] or players[1].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Rebel' and (players[2].vote == pair_order[round_number - 1][0] or players[2].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Rebel' and (players[2].vote == pair_order[round_number - 1][0] or players[2].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Rebel' and (players[3].vote == pair_order[round_number - 1][0] or players[3].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Rebel' and (players[3].vote == pair_order[round_number - 1][0] or players[3].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Rebel' and (players[4].vote == pair_order[round_number - 1][0] or players[4].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_correct_vote_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Rebel' and (players[4].vote == pair_order[round_number - 1][0] or players[4].vote == pair_order[round_number - 1][1])\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"rebel_points\",\n            \"value\": {\n              \"calc\": \"rebel_team_bonus\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Rebel' and terminated_informant_count >= 1\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Informant'\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Informant' and not players[0].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 1,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[0].current_role == 'Informant' and not players[0].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Informant' and not players[1].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 2,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[1].current_role == 'Informant' and not players[1].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Informant' and not players[2].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 3,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[2].current_role == 'Informant' and not players[2].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Informant' and not players[3].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 4,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[3].current_role == 'Informant' and not players[3].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"total_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Informant' and not players[4].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": 5,\n            \"key\": \"informant_points\",\n            \"value\": {\n              \"calc\": \"informant_survival_gain\"\n            },\n            \"if\": {\n              \"calc\": \"players[4].current_role == 'Informant' and not players[4].is_terminated\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"scoring\",\n      \"label\": \"after round 10\",\n      \"when\": {\n        \"calc\": \"round_number > num_rounds\"\n      },\n      \"against\": [\n        \"over\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"over\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds\"\n      },\n      \"rank_by\": \"you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points\",\n      \"text\": \"Winner: {result}. Final totals: seat 1 {players[0].total_points} (Rebel {players[0].rebel_points}, Informant {players[0].informant_points}), seat 2 {players[1].total_points} (Rebel {players[1].rebel_points}, Informant {players[1].informant_points}), seat 3 {players[2].total_points} (Rebel {players[2].rebel_points}, Informant {players[2].informant_points}), seat 4 {players[3].total_points} (Rebel {players[3].rebel_points}, Informant {players[3].informant_points}), seat 5 {players[4].total_points} (Rebel {players[4].rebel_points}, Informant {players[4].informant_points}).\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 10,\n    \"rounds_max\": 10,\n    \"actions_max\": 500,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (claim_msg, investigation_result, response_msg, revealed_role) in `private_roles`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  }
]
````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "one-night-revolution-ten-nights",
    "name": "One Night Revolution: Ten Nights, Hidden Ledger",
    "players": {
      "min": 5,
      "max": 5,
      "suggested": 5
    },
    "blurb": "5 players play 10 rounds as rotating Rebels and Informants with framing, claims, and termination votes for hidden points."
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
        "key": "total_points",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rebel_points",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "informant_points",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_role",
        "visible": "ally",
        "type": "text",
        "initial": "",
        "values": [
          "Rebel",
          "Informant",
          ""
        ]
      },
      {
        "key": "partner",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "target",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "investigation_result",
        "visible": "ally",
        "type": "text",
        "initial": "",
        "values": [
          "Rebel",
          "Informant",
          ""
        ]
      },
      {
        "key": "claim_msg",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "response_msg",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "vote",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "is_terminated",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "revealed_role",
        "visible": "public",
        "type": "text",
        "initial": "",
        "values": [
          "Rebel",
          "Informant",
          ""
        ]
      }
    ],
    "game": [
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pair_order",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "terminated_informant_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "num_players",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "num_rounds",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "num_pairs",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "initial_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "informant_rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rebel_rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rebel_correct_vote_gain",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rebel_team_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "informant_per_misdirected_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "informant_survival_gain",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "termination_min_votes",
        "visible": "public",
        "type": "number",
        "initial": 2
      }
    ]
  },
  "rules": "{num_players} players play {num_rounds} rounds. Each player starts with {initial_points} total points, {initial_points} Rebel points and {initial_points} Informant points. Before round 1 the engine lists all {num_pairs} unordered pairs of players and shuffles the list secretly; this shuffle is the only random event. In round r the pair in position r is the Informants and the other 3 are Rebels, so each player is Informant in exactly {informant_rounds_per_player} rounds with each other player as partner exactly once and Rebel in exactly {rebel_rounds_per_player} rounds. You are told this schedule rule but not the order.\n\nEach round: 1. ROLES: each player is privately told Rebel or Informant for this round, and each Informant is also privately told who the other Informant is; Rebels are told no partner. 2. NIGHT: every player simultaneously names one other player as target; a Rebel target is investigated and an Informant target is framed, and an Informant may name anyone including the partner with no extra effect for framing a partner. 3. NIGHT RESULTS: each Rebel is privately told Informant if the target is an Informant this round or at least one Informant framed that target this round, otherwise Rebel; a Rebel result is always true and an Informant result may be true or a frame; Informants receive no result. 4. CLAIMS: every player simultaneously writes one short message, lying allowed, then all messages are shown to everyone. 5. RESPONSES: every player simultaneously writes one more short message, then all are shown to everyone. 6. VOTE: every player simultaneously names one other player to Terminate, then all votes showing who voted for whom are announced publicly. 7. TERMINATION: if no player received {termination_min_votes} or more votes nobody is terminated; otherwise every player tied for the most votes is terminated, and only the round roles of terminated players are announced publicly while no other roles are revealed; termination removes no one and all {num_players} play every round. 8. SCORING (hidden): a Rebel who voted for an Informant gains {rebel_correct_vote_gain} points and a Rebel who voted for a Rebel gains nothing for that vote; if at least one terminated player is an Informant each Rebel gains {rebel_team_bonus} more point, and if none is an Informant there is no bonus; each Informant gains {informant_per_misdirected_gain} point for every Rebel who voted for a Rebel; each Informant who was not terminated gains {informant_survival_gain} points and a terminated Informant gains no survival points; points gained while Rebel are also added to Rebel points and points gained while Informant also added to Informant points; no totals of any kind are announced during the game and only votes and terminated roles are announced each round.\n\nAfter round {num_rounds} the engine announces every player's final total, Rebel points and Informant points and the game ends. The highest total points wins; tie-break most Rebel points, then most Informant points, then tied top share the win.",
  "setup": [
    {
      "use": "update",
      "label": "starting points and parameters",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total_points",
            "value": {
              "calc": "initial_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "rebel_points",
            "value": {
              "calc": "initial_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "informant_points",
            "value": {
              "calc": "initial_points"
            }
          }
        },
        {
          "set": {
            "key": "terminated_informant_count",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle the pairs",
      "do": [
        {
          "set": {
            "key": "pair_order",
            "value": {
              "calc": "[pair[1] for pair in sorted([[uniform(0, 1), [1, 2]], [uniform(0, 1), [1, 3]], [uniform(0, 1), [1, 4]], [uniform(0, 1), [1, 5]], [uniform(0, 1), [2, 3]], [uniform(0, 1), [2, 4]], [uniform(0, 1), [2, 5]], [uniform(0, 1), [3, 4]], [uniform(0, 1), [3, 5]], [uniform(0, 1), [4, 5]]])]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the schedule rule",
      "to": "all",
      "text": "There are {num_rounds} rounds. The {num_pairs} unordered pairs were shuffled secretly; in round r that pair are the Informants. Each player is Informant in exactly {informant_rounds_per_player} rounds with each other player once, and Rebel in {rebel_rounds_per_player} rounds. The order is secret."
    },
    {
      "use": "update",
      "label": "round 1 begins",
      "do": [
        {
          "set": {
            "key": "round_number",
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
      "fields": [
        "total_points",
        "rebel_points",
        "informant_points"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roles",
      "label": "assign roles",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "target",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "vote",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "investigation_result",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_terminated",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_role",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_msg",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "response_msg",
            "value": ""
          }
        },
        {
          "set": {
            "key": "terminated_informant_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1]"
            },
            "key": "current_role",
            "value": "Informant"
          }
        },
        {
          "set": {
            "players": {
              "where": "not (you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1])"
            },
            "key": "current_role",
            "value": "Rebel"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == pair_order[round_number - 1][0]"
            },
            "key": "partner",
            "value": {
              "calc": "pair_order[round_number - 1][1]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == pair_order[round_number - 1][1]"
            },
            "key": "partner",
            "value": {
              "calc": "pair_order[round_number - 1][0]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not (you.seat == pair_order[round_number - 1][0] or you.seat == pair_order[round_number - 1][1])"
            },
            "key": "partner",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "roles",
      "label": "private roles",
      "mode": "self",
      "to": "acting",
      "fields": [
        "current_role",
        "partner"
      ],
      "text": "Round {round_number}: your private role and partner if Informant."
    },
    {
      "use": "poll",
      "phase": "night",
      "label": "night targets",
      "to": "acting",
      "answer": {
        "type": "player",
        "exclude_self": true
      },
      "verify": {
        "tally": "plurality",
        "on_tie": "random",
        "bind": "night_common"
      },
      "store": "target",
      "text": "Name one other player as night target. A Rebel target is investigated and an Informant target is framed."
    },
    {
      "use": "update",
      "phase": "night",
      "label": "night results",
      "do": [
        {
          "set": {
            "player": 1,
            "key": "investigation_result",
            "value": {
              "calc": "'Informant' if (players[0].target == pair_order[round_number - 1][0] or players[0].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[0].target or players[pair_order[round_number - 1][1] - 1].target == players[0].target) else 'Rebel'"
            },
            "if": {
              "calc": "players[0].current_role == 'Rebel'"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "investigation_result",
            "value": {
              "calc": "'Informant' if (players[1].target == pair_order[round_number - 1][0] or players[1].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[1].target or players[pair_order[round_number - 1][1] - 1].target == players[1].target) else 'Rebel'"
            },
            "if": {
              "calc": "players[1].current_role == 'Rebel'"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "investigation_result",
            "value": {
              "calc": "'Informant' if (players[2].target == pair_order[round_number - 1][0] or players[2].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[2].target or players[pair_order[round_number - 1][1] - 1].target == players[2].target) else 'Rebel'"
            },
            "if": {
              "calc": "players[2].current_role == 'Rebel'"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "investigation_result",
            "value": {
              "calc": "'Informant' if (players[3].target == pair_order[round_number - 1][0] or players[3].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[3].target or players[pair_order[round_number - 1][1] - 1].target == players[3].target) else 'Rebel'"
            },
            "if": {
              "calc": "players[3].current_role == 'Rebel'"
            }
          }
        },
        {
          "set": {
            "player": 5,
            "key": "investigation_result",
            "value": {
              "calc": "'Informant' if (players[4].target == pair_order[round_number - 1][0] or players[4].target == pair_order[round_number - 1][1] or players[pair_order[round_number - 1][0] - 1].target == players[4].target or players[pair_order[round_number - 1][1] - 1].target == players[4].target) else 'Rebel'"
            },
            "if": {
              "calc": "players[4].current_role == 'Rebel'"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "night",
      "label": "private results",
      "mode": "self",
      "to": {
        "where": "you.current_role == 'Rebel'"
      },
      "fields": [
        "investigation_result",
        "target"
      ],
      "text": "Your private night result for round {round_number}."
    },
    {
      "use": "poll",
      "phase": "claims",
      "label": "claims",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "verify": {
        "tally": "plurality",
        "on_tie": "random",
        "bind": "claim_common"
      },
      "store": "claim_msg",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short claim message, e.g. claimed role, target or result. Lying allowed."
    },
    {
      "use": "poll",
      "phase": "claims",
      "label": "responses",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "verify": {
        "tally": "plurality",
        "on_tie": "random",
        "bind": "response_common"
      },
      "store": "response_msg",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one more short response message."
    },
    {
      "use": "poll",
      "phase": "vote",
      "label": "termination vote",
      "to": "acting",
      "answer": {
        "type": "player",
        "exclude_self": true
      },
      "verify": {
        "tally": "plurality",
        "on_tie": "random",
        "bind": "vote_common"
      },
      "store": "vote",
      "text": "Name one other player to Terminate."
    },
    {
      "use": "tell",
      "phase": "vote",
      "label": "votes announced",
      "to": "all",
      "text": "Votes round {round_number}: seat 1 voted {players[0].vote}, seat 2 voted {players[1].vote}, seat 3 voted {players[2].vote}, seat 4 voted {players[3].vote}, seat 5 voted {players[4].vote}."
    },
    {
      "use": "update",
      "phase": "termination",
      "label": "termination",
      "do": [
        {
          "set": {
            "player": 1,
            "key": "is_terminated",
            "value": {
              "calc": "count(p.vote == 1 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "is_terminated",
            "value": {
              "calc": "count(p.vote == 2 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "is_terminated",
            "value": {
              "calc": "count(p.vote == 3 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "is_terminated",
            "value": {
              "calc": "count(p.vote == 4 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes"
            }
          }
        },
        {
          "set": {
            "player": 5,
            "key": "is_terminated",
            "value": {
              "calc": "count(p.vote == 5 for p in players) == max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) and max([count(p.vote == 1 for p in players), count(p.vote == 2 for p in players), count(p.vote == 3 for p in players), count(p.vote == 4 for p in players), count(p.vote == 5 for p in players)]) >= termination_min_votes"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "revealed_role",
            "value": {
              "calc": "players[0].current_role if players[0].is_terminated else ''"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "revealed_role",
            "value": {
              "calc": "players[1].current_role if players[1].is_terminated else ''"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "revealed_role",
            "value": {
              "calc": "players[2].current_role if players[2].is_terminated else ''"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "revealed_role",
            "value": {
              "calc": "players[3].current_role if players[3].is_terminated else ''"
            }
          }
        },
        {
          "set": {
            "player": 5,
            "key": "revealed_role",
            "value": {
              "calc": "players[4].current_role if players[4].is_terminated else ''"
            }
          }
        },
        {
          "set": {
            "key": "terminated_informant_count",
            "value": {
              "calc": "count(p.is_terminated and p.current_role == 'Informant' for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "termination",
      "label": "termination announced",
      "to": "all",
      "text": "Terminated round {round_number}: seat 1 {players[0].is_terminated} {players[0].revealed_role}, seat 2 {players[1].is_terminated} {players[1].revealed_role}, seat 3 {players[2].is_terminated} {players[2].revealed_role}, seat 4 {players[3].is_terminated} {players[3].revealed_role}, seat 5 {players[4].is_terminated} {players[4].revealed_role}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "hidden scoring",
      "do": [
        {
          "adjust": {
            "player": 1,
            "key": "total_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[0].current_role == 'Rebel' and (players[0].vote == pair_order[round_number - 1][0] or players[0].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[0].current_role == 'Rebel' and (players[0].vote == pair_order[round_number - 1][0] or players[0].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "total_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[1].current_role == 'Rebel' and (players[1].vote == pair_order[round_number - 1][0] or players[1].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[1].current_role == 'Rebel' and (players[1].vote == pair_order[round_number - 1][0] or players[1].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "total_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[2].current_role == 'Rebel' and (players[2].vote == pair_order[round_number - 1][0] or players[2].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[2].current_role == 'Rebel' and (players[2].vote == pair_order[round_number - 1][0] or players[2].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "total_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[3].current_role == 'Rebel' and (players[3].vote == pair_order[round_number - 1][0] or players[3].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[3].current_role == 'Rebel' and (players[3].vote == pair_order[round_number - 1][0] or players[3].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "total_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[4].current_role == 'Rebel' and (players[4].vote == pair_order[round_number - 1][0] or players[4].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_correct_vote_gain"
            },
            "if": {
              "calc": "players[4].current_role == 'Rebel' and (players[4].vote == pair_order[round_number - 1][0] or players[4].vote == pair_order[round_number - 1][1])"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "total_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[0].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[0].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "total_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[1].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[1].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "total_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[2].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[2].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "total_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[3].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[3].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "total_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[4].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "rebel_points",
            "value": {
              "calc": "rebel_team_bonus"
            },
            "if": {
              "calc": "players[4].current_role == 'Rebel' and terminated_informant_count >= 1"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "total_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[0].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "informant_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[0].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "total_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[1].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "informant_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[1].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "total_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[2].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "informant_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[2].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "total_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[3].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "informant_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[3].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "total_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[4].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "informant_points",
            "value": {
              "calc": "count(p.current_role == 'Rebel' and not (p.vote == pair_order[round_number - 1][0] or p.vote == pair_order[round_number - 1][1]) for p in players) * informant_per_misdirected_gain"
            },
            "if": {
              "calc": "players[4].current_role == 'Informant'"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "total_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[0].current_role == 'Informant' and not players[0].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "informant_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[0].current_role == 'Informant' and not players[0].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "total_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[1].current_role == 'Informant' and not players[1].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "informant_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[1].current_role == 'Informant' and not players[1].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "total_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[2].current_role == 'Informant' and not players[2].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "informant_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[2].current_role == 'Informant' and not players[2].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "total_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[3].current_role == 'Informant' and not players[3].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 4,
            "key": "informant_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[3].current_role == 'Informant' and not players[3].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "total_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[4].current_role == 'Informant' and not players[4].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "player": 5,
            "key": "informant_points",
            "value": {
              "calc": "informant_survival_gain"
            },
            "if": {
              "calc": "players[4].current_role == 'Informant' and not players[4].is_terminated"
            }
          }
        },
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after round 10",
      "when": {
        "calc": "round_number > num_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number > num_rounds"
      },
      "rank_by": "you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points",
      "text": "Winner: {result}. Final totals: seat 1 {players[0].total_points} (Rebel {players[0].rebel_points}, Informant {players[0].informant_points}), seat 2 {players[1].total_points} (Rebel {players[1].rebel_points}, Informant {players[1].informant_points}), seat 3 {players[2].total_points} (Rebel {players[2].rebel_points}, Informant {players[2].informant_points}), seat 4 {players[3].total_points} (Rebel {players[3].rebel_points}, Informant {players[3].informant_points}), seat 5 {players[4].total_points} (Rebel {players[4].rebel_points}, Informant {players[4].informant_points})."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 500,
    "deadline_s": 120
  }
}
````
