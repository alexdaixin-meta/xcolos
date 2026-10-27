# 35 coder

- time: 2026-10-27T21:45:48+00:00 (116.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 3c735df4958386d9, reply sha256 1a051fdd26f980f7

## Sent

````
# Task: write the XColos game file for "Decrypto: Points Race"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. Four players: seats 1 and 2 form team Red, seats 3 and 4 form team Blue. Eight distinct keywords are drawn at random from a fixed list of 40 common nouns. The first four go to Red, numbered 1-4; the next four go to Blue, numbered 1-4. Each team's keywords are shown only to that team's two players. Each team starts with 0 points, 0 exact interceptions and 0 exact decodes. A public history lists, for each team and each past round, its three clues and its revealed true code.

CODES. A code is three different digits from 1-4 in order. There are 24 codes, offered in this order: 123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432.

ROLES. In odd rounds, seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders. In even rounds, the roles swap.

EACH ROUND (8 rounds):
1. Roles for the round are announced.
2. Code choice (simultaneous, secret): each Encryptor chooses one of the 24 codes for their team. No one else sees it.
3. Clues (simultaneous): each Encryptor writes three clues, one per digit of the code in order. Clue 1 should point to the team keyword numbered by the first digit, and so on.
4. Clue check. A clue is valid only if all of these hold: it is a single word with no spaces; it is 2-20 letters long; ignoring case, it does not contain any of the team's own four keywords and is not contained in any of them; it is not identical, ignoring case, to any clue either team has given in an earlier round. A team with any invalid clue this round is marked invalid.
5. All six clues are shown to everyone.
6. Guesses (simultaneous): each Decoder chooses one of the 24 codes as a decode of their own team's clues. Each Encryptor chooses one of the 24 codes as an interception of the opposing team's clues.
7. Decode scoring, for each team that is not invalid: the team gains 1 point for each position (first, second, third) where the Decoder's guess matches the team's true code. If all three match, the team gains 1 more point and 1 exact decode. A team marked invalid gains 0 decode points this round.
8. Interception scoring, rounds 2-8 only: each team gains 1 point for each position where its Encryptor's interception matches the opposing team's true code. If all three match, the team gains 2 more points and 1 exact interception. In round 1 interceptions score nothing.
9. Invalid penalty: if a team is marked invalid, the opposing team gains 3 points.
10. Both true codes, all guesses and all points gained are announced, and the clues and codes are added to the public history.

No other talk is allowed. The clues are the only communication.

END. After round 8 the game ends.

How the winner is decided: The team with more points after round 8 wins, and both of its players win. If points are tied, the team with more exact interceptions wins. If still tied, the team with more exact decodes wins. If still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Decrypto: Points Race (4 to 4 players, best with 4)

Two teams of two take turns encrypting three-digit codes as word clues for a partner who knows the team's secret keywords, while the rival team tries to intercept; points over 8 rounds decide the winning team.

STATE (every item below must exist in the file):
  - each player: team (text, starts 'seats 1,2: Red; seats 3,4: Blue'); everyone sees it. the player's team
  - each player: keywords (list, starts []); only its owner sees it. the team's four keywords in order (position 1-4 is keyword number 1-4); both teammates hold the same list
  - each player: role (text, starts ''); everyone sees it. Encryptor or Decoder for the current round
  - each player: guess (text, starts ''); only its owner sees it. this round's guessed code: a decode of the own team's clues for a Decoder, an interception of the opposing clues for an Encryptor
  - each player: score (number, starts 0); everyone sees it. the team's points (kept equal for both teammates)
  - each player: exact_interceptions (number, starts 0); everyone sees it. the team's exact interceptions (kept equal for both teammates)
  - each player: exact_decodes (number, starts 0); everyone sees it. the team's exact decodes (kept equal for both teammates)
  - the table: round (number, starts 1); everyone sees it. current round number, 1-8
  - the table: word_list (list, starts ['apple', 'river', 'castle', 'dragon', 'piano', 'rocket', 'garden', 'window', 'mirror', 'candle', 'forest', 'bridge', 'anchor', 'pencil', 'tiger', 'cloud', 'engine', 'island', 'ladder', 'moon', 'needle', 'orange', 'pirate', 'queen', 'robot', 'shadow', 'tower', 'umbrella', 'violin', 'whale', 'bottle', 'camera', 'desert', 'feather', 'glove', 'hammer', 'jungle', 'kettle', 'lemon', 'mountain']); hidden from all players. the fixed list of 40 nouns that keywords are drawn from
  - the table: codes (list, starts ['123', '124', '132', '134', '142', '143', '213', '214', '231', '234', '241', '243', '312', '314', '321', '324', '341', '342', '412', '413', '421', '423', '431', '432']); everyone sees it. the 24 legal codes in offer order
  - the table: red_code (text, starts ''); hidden from all players. Red's true code this round; revealed at step 10
  - the table: blue_code (text, starts ''); hidden from all players. Blue's true code this round; revealed at step 10
  - the table: red_clues (list, starts []); hidden from all players. Red's three clues this round, in code order; revealed at step 5
  - the table: blue_clues (list, starts []); hidden from all players. Blue's three clues this round, in code order; revealed at step 5
  - the table: red_invalid (bool, starts False); everyone sees it. Red gave an invalid clue this round
  - the table: blue_invalid (bool, starts False); everyone sees it. Blue gave an invalid clue this round
  - the table: red_points (number, starts 0); everyone sees it. Red's points (mirrors seats 1-2 score)
  - the table: blue_points (number, starts 0); everyone sees it. Blue's points (mirrors seats 3-4 score)
  - the table: red_gain (number, starts 0); everyone sees it. points Red gained this round (announced at step 10)
  - the table: blue_gain (number, starts 0); everyone sees it. points Blue gained this round (announced at step 10)
  - the table: history (list, starts []); everyone sees it. public record: for each past round and team, its three clues and its true code
  - parameters, each kept as a table attribute: rounds = 8, seats = 4, team_size = 2, keyword_list_size = 40, keywords_per_team = 4, code_length = 3, code_digit_min = 1, code_digit_max = 4, code_count = 24, clues_per_team_per_round = 3, clue_min_letters = 2, clue_max_letters = 20, decode_points_per_position = 1, exact_decode_bonus_points = 1, exact_decode_count_gain = 1, intercept_points_per_position = 1, exact_intercept_bonus_points = 2, exact_intercept_count_gain = 1, first_scoring_interception_round = 2, invalid_penalty_points = 3, starting_points = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1 and 2 are team Red; seats 3 and 4 are team Blue.
  2. Draw 8 distinct nouns at random from word_list, removing each from word_list as it is drawn.
  3. The first four drawn, in draw order, become keywords 1-4 of seats 1 and 2 (Red); the next four become keywords 1-4 of seats 3 and 4 (Blue). keywords is ally, so each team sees only its own.
  4. Every player's score, exact_interceptions and exact_decodes start at 0; red_points and blue_points start at 0; history starts empty; round is 1.
  5. Sync: each player is sent their own state, including their team's keywords.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: If round is odd: role = Encryptor for seats 1 and 3, Decoder for seats 2 and 4. If round is even: role = Encryptor for seats 2 and 4, Decoder for seats 1 and 3. Reset red_invalid, blue_invalid to false, red_gain, blue_gain to 0, and every guess to empty.
  2. [tell] all players. What happens: Announce: 'Round {round}: the Encryptors are seats {red encryptor} (Red) and {blue encryptor} (Blue); the Decoders are seats {red decoder} (Red) and {blue decoder} (Blue).'
  3. [poll] the two Encryptors answers: one of the 24 codes, from codes. What happens: Red Encryptor's answer is set into red_code; Blue Encryptor's answer is set into blue_code (both hidden from all players, including the Decoder teammate).
  4. [poll] the two Encryptors answers: short text: three clues separated by commas, clue 1 for the keyword numbered by the code's first digit, clue 2 for the second, clue 3 for the third. What happens: Red Encryptor's three clues are set into red_clues and Blue Encryptor's into blue_clues, in order.
  5. [update] Red. What happens: red_invalid = true if the referee rules the sentence false; otherwise it stays false. JUDGED: a referee rules true or false on "Each of Red's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Red's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."; write this step's `when` as {"prose": that sentence, verbatim}.
  6. [update] Blue. What happens: blue_invalid = true if the referee rules the sentence false; otherwise it stays false. JUDGED: a referee rules true or false on "Each of Blue's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Blue's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."; write this step's `when` as {"prose": that sentence, verbatim}.
  7. [tell] all players. What happens: Announce all six clues: 'Red clues: {red_clues}. Blue clues: {blue_clues}.'
  8. [poll] all players answers: one of the 24 codes, from codes. What happens: Each Decoder's answer (a decode of their own team's clues) and each Encryptor's answer (an interception of the opposing team's clues) is stored in that player's guess.
  9. [update] both teams. What happens: Decode scoring. For Red, if red_invalid is false: matches = the number of positions 1-3 where the Red Decoder's guess digit equals red_code's digit; red_gain += matches; if matches == 3, red_gain += 1 and exact_decodes += 1 for seats 1 and 2. For Blue, the same with blue_invalid, the Blue Decoder's guess and blue_code, with exact_decodes added for seats 3 and 4. An invalid team gains 0 here.
  10. [update] both teams. What happens: Interception scoring, only when round >= 2. Red: matches = the number of positions where the Red Encryptor's guess equals blue_code; red_gain += matches; if matches == 3, red_gain += 2 and exact_interceptions += 1 for seats 1 and 2. Blue: the same with the Blue Encryptor's guess against red_code, adding to blue_gain and to seats 3 and 4. When round == 1, nothing changes.
  11. [update] both teams. What happens: Invalid penalty: if red_invalid, blue_gain += 3; if blue_invalid, red_gain += 3. Then red_points += red_gain and blue_points += blue_gain; score of seats 1,2 = red_points; score of seats 3,4 = blue_points.
  12. [update] all players. What happens: Append to history: 'Round {round} Red clues {red_clues}, code {red_code}; Blue clues {blue_clues}, code {blue_code}'.
  13. [tell] all players. What happens: Announce: 'Red's code was {red_code}, Blue's was {blue_code}. Guesses: seat 1 {guess}, seat 2 {guess}, seat 3 {guess}, seat 4 {guess}. Red invalid: {red_invalid}; Blue invalid: {blue_invalid}. Red gained {red_gain} (total {red_points}); Blue gained {blue_gain} (total {blue_points}).'
  14. [update] all players. What happens: round += 1
  15. [check] all players. What happens: End the game if round > 8; otherwise repeat the round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, seats 1 and 2 are team Red and seats 3 and 4 are team Blue.
  R2. At setup, 8 distinct keywords are drawn at random from the 40-noun word_list: the first 4 become Red's keywords 1-4 and the next 4 become Blue's keywords 1-4.
  R3. A team's keywords are visible to its own two players only, never to the opposing team.
  R4. At setup, each team has 0 points, 0 exact interceptions and 0 exact decodes.
  R5. When the round is odd, seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders.
  R6. When the round is even, seats 2 and 4 are Encryptors and seats 1 and 3 are Decoders.
  R7. Each round, each Encryptor secretly chooses one of the 24 codes (three different digits from 1-4), and no other player, including the teammate, sees it before step 10.
  R8. Each round, each Encryptor writes exactly three clues, one per digit of their code, in order.
  R9. When any of a team's clues has a space, has fewer than 2 or more than 20 letters, contains or is contained in one of the team's own keywords (ignoring case), or repeats a clue from an earlier round (ignoring case), that team is marked invalid for the round.
  R10. All six clues are shown to all four players before guesses are made.
  R11. Guesses are simultaneous: each Decoder picks one of the 24 codes as a decode of their own team's clues, and each Encryptor picks one of the 24 codes as an interception of the opposing team's clues.
  R12. When a team is not invalid, it gains 1 point for each position where its Decoder's guess matches its true code (e.g. guess 123 against code 132 gains 1).
  R13. When a team's Decoder's guess matches all three positions and the team is not invalid, the team gains 3 + 1 = 4 points and 1 exact decode.
  R14. When a team is marked invalid, it gains 0 decode points that round even if its Decoder's guess is correct.
  R15. In rounds 2-8, a team gains 1 point for each position where its Encryptor's interception matches the opposing team's true code.
  R16. In rounds 2-8, when a team's interception matches all three positions, the team gains 3 + 2 = 5 points and 1 exact interception.
  R17. In round 1, interceptions score 0 points and add no exact interceptions.
  R18. When a team is marked invalid, the opposing team gains 3 points.
  R19. At the end of each round, both true codes, all four guesses and each team's points gained are announced, and both teams' clues and codes are appended to the public history.
  R20. Both players on a team always have the same score, exact_interceptions and exact_decodes.
  R21. The game ends after round 8.
  R22. When the game ends, the team with more points wins; if points are tied, the team with more exact interceptions wins; if still tied, the team with more exact decodes wins; if still tied, it is a draw and all four players share the result.
  R23. Players have no talk step: the clues are the only communication.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Code choice | asked: the two Encryptors of the round (seats 1 and 3 in odd rounds, seats 2 and 4 in even rounds) | options: each Encryptor: the 24 codes 123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432; Decoders are not asked
  - Clues | asked: the two Encryptors of the round | options: each Encryptor: short free text with three clues separated by commas; Decoders are not asked
  - Guesses | asked: all four seats | options: a Decoder: the 24 codes, as a decode of their own team's clues; an Encryptor: the 24 codes, as an interception of the opposing team's clues (asked in round 1 too, though it scores nothing)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 8
  - each player's standing: you.score * 10000 + you.exact_interceptions * 100 + you.exact_decodes (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player stands on their team's points, then its exact interceptions, then its exact decodes. The team that is higher wins and both its players win. If both teams are level on all three, all four players share the result as a draw.
  - the end screen states the final scores or deciding figures, and a short model-written summary of how the game went

## Recipe: a shared deck and hidden hands (tested on the engine)

When the script has a deck and hands, both must exist as attributes, and setup must really deal. Declare the hand as a PLAYER attribute
`{"key": "hand", "visible": "ally", "type": "list", "initial": []}` (only its owner sees it; a player attribute is never `none`) and the
deck as a TABLE attribute `{"key": "deck", "visible": "none", "type": "list", "initial": [every card, one entry per copy]}`, plus a table text
attribute `pick` (visible `none`, initial `""`) to hold the card just drawn. Then ONE draw, of a random card into seat N's hand, is three operations
in an `update`'s `do` list, in this order:

  {"set":    {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
  {"append": {"player": N, "key": "hand", "value": {"calc": "pick"}}},
  {"remove": {"key": "deck", "value": {"calc": "pick"}}}

Dealing two cards to three seats is that block repeated twice for each seat (6 draws), never a fixed list written into `initial`: the deal
is random and different each match, and every player's hand must differ. A card coming back is `{"append": {"key": "deck", ...}}` and
`{"remove": {"player": N, "key": "hand", ...}}`. "Has a card of role R" is `"R" in you.hand`. Use `{"if": {"calc": ...}}` on an operation to make
it conditional. Never declare `hand` or `deck` and then leave them unchanged: the rules would then claim cards that do not exist.

## Pattern: offer each seat only what it may do (tested on the engine)

A question's options may come from state, and the state can differ for every player. So make who may do what part of the OFFER, never a check
afterwards. Declare a PLAYER list attribute (say `offer`, visible `ally`), and set it for everyone in one `update` just before the question,
from each player's own attributes and the table's:

  {"set": {"players": "all", "key": "offer",
           "value": {"calc": "['wait'] + (['buy'] if you.coins >= price else []) + (['block'] if you.seat == target else [])"}}}

then ask with `"answer": {"type": "choice", "options": {"attribute": "offer"}}` and `to` naming who is asked. `you` is each player in turn, and a
list can be built with `+` and `(... if ... else [])`. Whatever a seat may not do is not in its list: a seat that cannot pay is not offered the
paid action, only the target of an action is offered a block against it, a player already out is not asked. Do the same for a target: put the
legal seats in a list attribute.

When only one option is left (the last unused action, the only legal card), still ask the question: the engine answers a choice with one
option for the seat, with no model call, and records it as the seat's move. Do not skip the question with a `when` and set the answer
yourself: that move is then missing from the match, and a test that scripts it fails.

When a player is eliminated, set the PLATFORM status as well as your own counters: declare a status for it (`{"id": "out", "acts": false}`) next to `playing` and
run `{"set_status": {"player": N, "to": "out", "text": "Seat {player} is out."}}`. Without it the platform and the console show the player as still in the game, and the
prompts list them as playing, whatever your own `alive` attribute says. Name the cards it reveals in the same announcement.

Do NOT offer a broad list and then refuse illegal answers and ask again (a `repeat` that asks, checks, and asks again, or an update that removes
an option the player just picked). It costs a model call, it lets a model choose something illegal, and the pipeline reports it as a failure:
"an option is offered and then refused". If you find yourself writing a step called "refuse...", "check the answer is legal" or "not allowed",
you are filling the wrong list: fix the offer.

## Rounds and the safety cap

If the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed
round count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap
is reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `team` (text, visible: public, starts 'seats 1,2: Red; seats 3,4: Blue'): the player's team
- each player: `role` (text, visible: public, starts ''): Encryptor or Decoder for the current round
- each player: `score` (number, visible: public, starts 0): the team's points (kept equal for both teammates)
- each player: `exact_interceptions` (number, visible: public, starts 0): the team's exact interceptions (kept equal for both teammates)
- each player: `exact_decodes` (number, visible: public, starts 0): the team's exact decodes (kept equal for both teammates)
- the table: `round` (number, visible: public, starts 1): current round number, 1-8
- the table: `red_invalid` (bool, visible: public, starts False): Red gave an invalid clue this round
- the table: `blue_invalid` (bool, visible: public, starts False): Blue gave an invalid clue this round
- the table: `red_points` (number, visible: public, starts 0): Red's points (mirrors seats 1-2 score)
- the table: `blue_points` (number, visible: public, starts 0): Blue's points (mirrors seats 3-4 score)
- the table: `history` (list, visible: public, starts []): public record: for each past round and team, its three clues and its true code
- parameters (each must be an attribute holding this value, never a number buried in a step): rounds = 8, seats = 4, team_size = 2, keyword_list_size = 40, keywords_per_team = 4, code_length = 3, code_digit_min = 1, code_digit_max = 4, code_count = 24, clues_per_team_per_round = 3, clue_min_letters = 2, clue_max_letters = 20, decode_points_per_position = 1, exact_decode_bonus_points = 1, exact_decode_count_gain = 1, intercept_points_per_position = 1, exact_intercept_bonus_points = 2, exact_intercept_count_gain = 1, first_scoring_interception_round = 2, invalid_penalty_points = 3, starting_points = 0
- the game ends with ONE ending whose `rank_by` is `you.score * 10000 + you.exact_interceptions * 100 + you.exact_decodes`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: write ONE
ending, whose `when` is a calc condition and whose `rank_by` is the ranking in the interface below; no `result`, no `winner`, no prose
ending, no `llm` in an ending. Use calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when` `{"prose": "<the judged sentence, verbatim>"}`: a referee answers it
true or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no
model answers. Choices made at the same moment are a `poll`. The end screen announces only the result: the ending's `text` says who won (`{result}`) and the final scores or deciding figures with
placeholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with `rank_by` as both examples do.

- Mistakes the loader has refused before, so avoid them:
  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table
    attributes.) For something only its owner should see, use `ally`.
  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.
  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on
    attributes, or with `set` operations in `setup`, instead.
  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.
  * TALK that everyone hears is a `poll` with a free-text answer and `"broadcast": {"to": "all", "text": "Seat {seat} says: {value}"}`
    (or `"broadcast": "all"` with no `text`, which shows each message word for word). A broadcast may use ONLY `{value}` (what that
    player answered), `{seat}` (who) and table attributes: a name bound by `verify` is not set yet, so `{talk_msg}` reaches players as
    the literal braces, and the loader refuses it.
  * WHO answered what (who challenged, who blocked, who raised a hand) is `"store": "attr"` on the `poll` or `ask`, naming a PLAYER
    attribute declared under `attributes.player` (a `text` attribute for a choice). Each player's own answer is written to it and a calc reads
    them all: `count(p.said == 'Challenge' for p in players)`, `min([p.seat for p in players if p.said == 'Challenge'])`. A `verify`
    tally gives ONE winning value and loses who gave which: one "Challenge" against three "Pass" tallies to "Pass". Never write a seat
    number into a calc by guessing (`2 if active_seat == 1 else 1`); read it from a stored answer. Reset the stored attribute with a `set`
    to `""` (`players: "all"`) before each poll, so last round's answers do not count.
  * `meta.players` carries `min`, `max` and `suggested`, exactly as the task gives them: the console fills a table to the suggested size and the real-model tests play at it.
  * THE RULES TEXT SAYS BOTH OUTCOMES. For every decision point (a challenge, a block, a claim, a cost), say what happens when it is true AND when it is false,
    and whether the action still goes ahead; a player decides on this text and nothing else, and a check compares it with each numbered rule.
  * THE RULES TEXT PLAYERS READ IS THE DESIGN'S. `meta.rules` (the brief) says each mechanic in the design's own words and in its order: how a challenge is resolved,
    what a block costs, who counts when several answer. Do not paraphrase a mechanic: a reordered sentence is a different rule.
  * BOOKKEEPING IS HIDDEN. An attribute that only the game's own steps read (a scratch value, a counter, a copy of an option list, who is blocking) is declared
    hidden (`none` on the table, `ally` on a player), not `public`: every public attribute is printed into every player's prompt on every turn.
  * THE DEAL REMOVES WHAT IT DEALS. Every card put into a hand is taken out of the deck in the same step (see the deck recipe); after setup, deck plus hands holds
    exactly the cards the rules start with, and no card appears more often than the rules say.
  * OFFER ONLY WHAT A SEAT MAY DO. Build each seat's option list from its own state (see the offer pattern) and never refuse an answer afterwards
    and ask again: an option that is offered, taken and then taken back fails the pipeline's check.
  * A QUESTION WITH ONE POSSIBLE ANSWER IS NEVER WORTH ASKING ("pass" and nothing else): the engine answers it itself, but write the step so
    it is not asked at all, and never announce a seat's answer when the seat was not asked (eliminated players).
  * ASK ONLY WHAT IS NEEDED. Put a `when` on a question that applies only sometimes: a target is asked only for the actions that take one
    (`"when": {"calc": "chosen_action in ['Steal', 'Assassinate', 'Coup']"}`), a block only when something can be blocked.
  * A counter must not go below what the rules allow. Guard every payment and loss with an `if` (`"if": {"calc": "you.coins >= cost"}`,
    or check it before the action is allowed), and treat an action the player cannot afford as the cheapest legal one, as the rules say.
  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {"bind": "name"}`; a later `update`
    stores it with `"value": "$name"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the
    answers away, and every score that depends on them stays at its starting value.
  * An attribute declared `"mutable": false` is set once, by an `initialize` step, and any other step that sets it crashes the game
    ("declared static and has already been dealt"). To set a hidden type or a starting value at setup, either use an `initialize`
    step or leave the attribute mutable.
  * Do not write steps that do nothing (for example an `if` of `{"calc": "False"}`), or two polls where one will do.
  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,
    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.
- Keep a round to at most 20 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the
  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.

## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)

For "each player chooses in private, then the choices decide the score":
1. One `ask` per seat, addressed with `{"where": "you.seat == N"}`, with `"verify": {"bind": "aN"}`. The answer exists only because it is bound.
2. One `update` after both. It `set`s the bound answers into table attributes with `"$aN"`, and `adjust`s each player's score with a
   `calc` that may use `$aN` and `if ... else`.
3. A `check` with `when` and `against`, and ONE ending in `end` whose `rank_by` is `you.score`: the engine ranks the players by it.
Every attribute is set by a step that runs. Adapt this; do not invent another way to store answers.

```json
{
  "schema": 1,
  "meta": {
    "id": "match_or_miss",
    "name": "Match or Miss",
    "players": {
      "min": 2,
      "max": 2
    },
    "blurb": "Two players choose A or B in secret; seat 1 scores when they match, seat 2 when they differ."
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
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "rounds_left",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "last_a1",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_a2",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ]
  },
  "rules": "Three rounds. Each round both players secretly choose A or B. If the choices match, seat 1 scores a point; if they differ, seat 2 does. The higher score wins.",
  "setup": [
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
      "use": "ask",
      "label": "seat 1 chooses",
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a1"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "ask",
      "label": "seat 2 chooses",
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a2"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "update",
      "label": "score the round",
      "do": [
        {
          "set": {
            "key": "last_a1",
            "value": "$a1"
          }
        },
        {
          "set": {
            "key": "last_a2",
            "value": "$a2"
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": {
              "calc": "1 if $a1 == $a2 else 0"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": {
              "calc": "0 if $a1 == $a2 else 1"
            }
          }
        },
        {
          "adjust": {
            "key": "rounds_left",
            "value": -1
          }
        }
      ],
      "text": "Seat 1 chose {last_a1}, seat 2 chose {last_a2}."
    },
    {
      "use": "check",
      "label": "is it over",
      "when": {
        "calc": "rounds_left <= 0"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "rounds_left <= 0"
      },
      "rank_by": "you.score",
      "text": "{result} wins."
    }
  }
}
```

Your file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every
attribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and
shown your file again; fix what is wrong and keep the rest.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "decrypto_points_race",
    "name": "Decrypto: Points Race",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Two teams of two encrypt three-digit codes as word clues over secret keywords while the rivals try to intercept; most points after 8 rounds wins."
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
        "key": "team",
        "visible": "public",
        "type": "text",
        "initial": "seats 1,2: Red; seats 3,4: Blue"
      },
      {
        "key": "keywords",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "role",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "guess",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "exact_interceptions",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "exact_decodes",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clue_text",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "word_list",
        "visible": "none",
        "type": "list",
        "initial": [
          "apple",
          "river",
          "castle",
          "dragon",
          "piano",
          "rocket",
          "garden",
          "window",
          "mirror",
          "candle",
          "forest",
          "bridge",
          "anchor",
          "pencil",
          "tiger",
          "cloud",
          "engine",
          "island",
          "ladder",
          "moon",
          "needle",
          "orange",
          "pirate",
          "queen",
          "robot",
          "shadow",
          "tower",
          "umbrella",
          "violin",
          "whale",
          "bottle",
          "camera",
          "desert",
          "feather",
          "glove",
          "hammer",
          "jungle",
          "kettle",
          "lemon",
          "mountain"
        ]
      },
      {
        "key": "codes",
        "visible": "public",
        "type": "list",
        "initial": [
          "123",
          "124",
          "132",
          "134",
          "142",
          "143",
          "213",
          "214",
          "231",
          "234",
          "241",
          "243",
          "312",
          "314",
          "321",
          "324",
          "341",
          "342",
          "412",
          "413",
          "421",
          "423",
          "431",
          "432"
        ]
      },
      {
        "key": "red_code",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "blue_code",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "red_clues",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "blue_clues",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "red_invalid",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "blue_invalid",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "red_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "history",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_guesses",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "red_enc",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_enc",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_dec",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_dec",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "red_valid",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "blue_valid",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "red_g",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "blue_g",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "red_match",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_match",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "seats",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "team_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "keyword_list_size",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "keywords_per_team",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "code_length",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "code_digit_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "code_digit_max",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "code_count",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "clues_per_team_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clue_min_letters",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "clue_max_letters",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "decode_points_per_position",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_decode_bonus_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_decode_count_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "intercept_points_per_position",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_intercept_bonus_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "exact_intercept_count_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_scoring_interception_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "invalid_penalty_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the teams",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat in [1, 2]"
            },
            "key": "team",
            "value": "Red"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat in [3, 4]"
            },
            "key": "team",
            "value": "Blue"
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "draw the keywords",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting totals",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "exact_interceptions",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "exact_decodes",
            "value": 0
          }
        },
        {
          "set": {
            "key": "red_points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "key": "blue_points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "key": "history",
            "value": []
          }
        },
        {
          "set": {
            "key": "round",
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
      "text": "You start with (your team's keywords are numbered 1-4 in order):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roles",
      "label": "roles and resets",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat in [1, 3]"
            },
            "key": "role",
            "value": {
              "calc": "'Encryptor' if round % 2 == 1 else 'Decoder'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat in [2, 4]"
            },
            "key": "role",
            "value": {
              "calc": "'Decoder' if round % 2 == 1 else 'Encryptor'"
            }
          }
        },
        {
          "set": {
            "key": "red_enc",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Red' and p.role == 'Encryptor'])"
            }
          }
        },
        {
          "set": {
            "key": "blue_enc",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Blue' and p.role == 'Encryptor'])"
            }
          }
        },
        {
          "set": {
            "key": "red_dec",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Red' and p.role == 'Decoder'])"
            }
          }
        },
        {
          "set": {
            "key": "blue_dec",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Blue' and p.role == 'Decoder'])"
            }
          }
        },
        {
          "set": {
            "key": "red_invalid",
            "value": false
          }
        },
        {
          "set": {
            "key": "blue_invalid",
            "value": false
          }
        },
        {
          "set": {
            "key": "red_valid",
            "value": false
          }
        },
        {
          "set": {
            "key": "blue_valid",
            "value": false
          }
        },
        {
          "set": {
            "key": "red_gain",
            "value": 0
          }
        },
        {
          "set": {
            "key": "blue_gain",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guess",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "code_pick",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "clue_text",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "roles",
      "label": "roles announced",
      "to": "all",
      "text": "Round {round}: the Encryptors are seats {red_enc} (Red) and {blue_enc} (Blue); the Decoders are seats {red_dec} (Red) and {blue_dec} (Blue)."
    },
    {
      "use": "poll",
      "phase": "encrypt",
      "label": "code choice",
      "to": {
        "where": "you.role == 'Encryptor'"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "codes"
        }
      },
      "store": "code_pick",
      "text": "You are your team's Encryptor this round. Secretly choose your team's code: three different digits from 1-4, in order. Nobody else sees it, not even your teammate."
    },
    {
      "use": "poll",
      "phase": "encrypt",
      "label": "clues",
      "to": {
        "where": "you.role == 'Encryptor'"
      },
      "answer": {
        "type": "text",
        "max_words": 12
      },
      "store": "clue_text",
      "text": "Use the code you just chose (shown in your own state as code_pick). Write three clues separated by commas: clue 1 for your keyword numbered by the code's first digit, clue 2 for the second digit, clue 3 for the third. Each clue must be a single word with no spaces, 2-20 letters, must not contain or be contained in any of your team's keywords (ignoring case), and must not repeat any clue from an earlier round (see history). Any invalid clue marks your team invalid."
    },
    {
      "use": "update",
      "phase": "encrypt",
      "label": "record codes and clues",
      "do": [
        {
          "set": {
            "key": "red_code",
            "value": {
              "calc": "([p.code_pick for p in players if p.team == 'Red' and p.role == 'Encryptor'] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "blue_code",
            "value": {
              "calc": "([p.code_pick for p in players if p.team == 'Blue' and p.role == 'Encryptor'] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "red_clues",
            "value": {
              "calc": "[p.clue_text for p in players if p.team == 'Red' and p.role == 'Encryptor']"
            }
          }
        },
        {
          "set": {
            "key": "blue_clues",
            "value": {
              "calc": "[p.clue_text for p in players if p.team == 'Blue' and p.role == 'Encryptor']"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "check",
      "label": "red clue check",
      "when": {
        "prose": "Each of Red's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Red's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."
      },
      "do": [
        {
          "set": {
            "key": "red_valid",
            "value": true
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "check",
      "label": "blue clue check",
      "when": {
        "prose": "Each of Blue's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Blue's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."
      },
      "do": [
        {
          "set": {
            "key": "blue_valid",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "clues",
      "label": "clues shown",
      "to": "all",
      "text": "Red clues: {red_clues}. Blue clues: {blue_clues}."
    },
    {
      "use": "poll",
      "phase": "guess",
      "label": "guesses",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "game": "codes"
        }
      },
      "store": "guess",
      "text": "Choose one code. If you are a Decoder, it is your decode of your own team's clues. If you are an Encryptor, it is your interception of the opposing team's clues (interceptions score nothing in round 1)."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "decode scoring",
      "do": [
        {
          "set": {
            "key": "red_invalid",
            "value": {
              "calc": "not red_valid"
            }
          }
        },
        {
          "set": {
            "key": "blue_invalid",
            "value": {
              "calc": "not blue_valid"
            }
          }
        },
        {
          "set": {
            "key": "red_g",
            "value": {
              "calc": "([p.guess for p in players if p.team == 'Red' and p.role == 'Decoder'] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "blue_g",
            "value": {
              "calc": "([p.guess for p in players if p.team == 'Blue' and p.role == 'Decoder'] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "red_match",
            "value": {
              "calc": "count([red_g[i] == red_code[i] for i in [0, 1, 2]]) if len(red_
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (clue_text, code_pick, guess, role); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "decrypto_points_race",
    "name": "Decrypto: Points Race",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Two teams of two encrypt three-digit codes as word clues over secret keywords while the rivals try to intercept; most points after 8 rounds wins."
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
        "key": "team",
        "visible": "public",
        "type": "text",
        "initial": "seats 1,2: Red; seats 3,4: Blue"
      },
      {
        "key": "keywords",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "role",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "guess",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "exact_interceptions",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "exact_decodes",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "word_list",
        "visible": "none",
        "type": "list",
        "initial": [
          "apple",
          "river",
          "castle",
          "dragon",
          "piano",
          "rocket",
          "garden",
          "window",
          "mirror",
          "candle",
          "forest",
          "bridge",
          "anchor",
          "pencil",
          "tiger",
          "cloud",
          "engine",
          "island",
          "ladder",
          "moon",
          "needle",
          "orange",
          "pirate",
          "queen",
          "robot",
          "shadow",
          "tower",
          "umbrella",
          "violin",
          "whale",
          "bottle",
          "camera",
          "desert",
          "feather",
          "glove",
          "hammer",
          "jungle",
          "kettle",
          "lemon",
          "mountain"
        ]
      },
      {
        "key": "codes",
        "visible": "public",
        "type": "list",
        "initial": [
          "123",
          "124",
          "132",
          "134",
          "142",
          "143",
          "213",
          "214",
          "231",
          "234",
          "241",
          "243",
          "312",
          "314",
          "321",
          "324",
          "341",
          "342",
          "412",
          "413",
          "421",
          "423",
          "431",
          "432"
        ]
      },
      {
        "key": "red_code",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "blue_code",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "red_clues",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "blue_clues",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "red_invalid",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "blue_invalid",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "red_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "history",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_guesses",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "red_enc",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_enc",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_dec",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_dec",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "red_valid",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "blue_valid",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "red_g",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "blue_g",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "red_match",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_match",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "seats",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "team_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "keyword_list_size",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "keywords_per_team",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "code_length",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "code_digit_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "code_digit_max",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "code_count",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "clues_per_team_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clue_min_letters",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "clue_max_letters",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "decode_points_per_position",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_decode_bonus_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_decode_count_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "intercept_points_per_position",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_intercept_bonus_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "exact_intercept_count_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_scoring_interception_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "invalid_penalty_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the teams",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat in [1, 2]"
            },
            "key": "team",
            "value": "Red"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat in [3, 4]"
            },
            "key": "team",
            "value": "Blue"
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "draw the keywords",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[int(uniform(0, len(word_list)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "keywords",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "word_list",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting totals",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "exact_interceptions",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "exact_decodes",
            "value": 0
          }
        },
        {
          "set": {
            "key": "red_points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "key": "blue_points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "key": "history",
            "value": []
          }
        },
        {
          "set": {
            "key": "round",
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
        "team",
        "keywords",
        "score",
        "exact_interceptions",
        "exact_decodes"
      ],
      "text": "You start with (your team's keywords are numbered 1-4 in order):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roles",
      "label": "roles and resets",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat in [1, 3]"
            },
            "key": "role",
            "value": {
              "calc": "'Encryptor' if round % 2 == 1 else 'Decoder'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat in [2, 4]"
            },
            "key": "role",
            "value": {
              "calc": "'Decoder' if round % 2 == 1 else 'Encryptor'"
            }
          }
        },
        {
          "set": {
            "key": "red_enc",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Red' and p.role == 'Encryptor'])"
            }
          }
        },
        {
          "set": {
            "key": "blue_enc",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Blue' and p.role == 'Encryptor'])"
            }
          }
        },
        {
          "set": {
            "key": "red_dec",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Red' and p.role == 'Decoder'])"
            }
          }
        },
        {
          "set": {
            "key": "blue_dec",
            "value": {
              "calc": "min([p.seat for p in players if p.team == 'Blue' and p.role == 'Decoder'])"
            }
          }
        },
        {
          "set": {
            "key": "red_invalid",
            "value": false
          }
        },
        {
          "set": {
            "key": "blue_invalid",
            "value": false
          }
        },
        {
          "set": {
            "key": "red_valid",
            "value": false
          }
        },
        {
          "set": {
            "key": "blue_valid",
            "value": false
          }
        },
        {
          "set": {
            "key": "red_gain",
            "value": 0
          }
        },
        {
          "set": {
            "key": "blue_gain",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guess",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "roles",
      "label": "roles announced",
      "to": "all",
      "text": "Round {round}: the Encryptors are seats {red_enc} (Red) and {blue_enc} (Blue); the Decoders are seats {red_dec} (Red) and {blue_dec} (Blue)."
    },
    {
      "use": "poll",
      "phase": "encrypt",
      "label": "red code choice",
      "to": {
        "where": "you.seat == red_enc"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "codes"
        }
      },
      "verify": {
        "bind": "red_code_ans"
      },
      "text": "You are Red's Encryptor this round. Secretly choose Red's code: three different digits from 1-4, in order. Nobody else sees it, not even your teammate."
    },
    {
      "use": "poll",
      "phase": "encrypt",
      "label": "blue code choice",
      "to": {
        "where": "you.seat == blue_enc"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "codes"
        }
      },
      "verify": {
        "bind": "blue_code_ans"
      },
      "text": "You are Blue's Encryptor this round. Secretly choose Blue's code: three different digits from 1-4, in order. Nobody else sees it, not even your teammate."
    },
    {
      "use": "poll",
      "phase": "encrypt",
      "label": "red clues",
      "to": {
        "where": "you.seat == red_enc"
      },
      "answer": {
        "type": "text",
        "max_words": 12
      },
      "verify": {
        "bind": "red_clue_ans"
      },
      "text": "Your code is {red_code_ans}. Write three clues separated by commas: clue 1 for your keyword numbered by the code's first digit, clue 2 for the second digit, clue 3 for the third. Each clue must be a single word with no spaces, {clue_min_letters}-{clue_max_letters} letters, must not contain or be contained in any of your team's keywords (ignoring case), and must not repeat any clue from an earlier round (see history). Any invalid clue marks your team invalid: you score no decode points and Blue gains {invalid_penalty_points}."
    },
    {
      "use": "poll",
      "phase": "encrypt",
      "label": "blue clues",
      "to": {
        "where": "you.seat == blue_enc"
      },
      "answer": {
        "type": "text",
        "max_words": 12
      },
      "verify": {
        "bind": "blue_clue_ans"
      },
      "text": "Your code is {blue_code_ans}. Write three clues separated by commas: clue 1 for your keyword numbered by the code's first digit, clue 2 for the second digit, clue 3 for the third. Each clue must be a single word with no spaces, {clue_min_letters}-{clue_max_letters} letters, must not contain or be contained in any of your team's keywords (ignoring case), and must not repeat any clue from an earlier round (see history). Any invalid clue marks your team invalid: you score no decode points and Red gains {invalid_penalty_points}."
    },
    {
      "use": "update",
      "phase": "encrypt",
      "label": "record codes and clues",
      "do": [
        {
          "set": {
            "key": "red_code",
            "value": "$red_code_ans"
          }
        },
        {
          "set": {
            "key": "blue_code",
            "value": "$blue_code_ans"
          }
        },
        {
          "set": {
            "key": "red_clues",
            "value": {
              "calc": "[$red_clue_ans]"
            }
          }
        },
        {
          "set": {
            "key": "blue_clues",
            "value": {
              "calc": "[$blue_clue_ans]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "check",
      "label": "red clue check",
      "when": {
        "prose": "Each of Red's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Red's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."
      },
      "do": [
        {
          "set": {
            "key": "red_valid",
            "value": true
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "check",
      "label": "blue clue check",
      "when": {
        "prose": "Each of Blue's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Blue's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."
      },
      "do": [
        {
          "set": {
            "key": "blue_valid",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "clues",
      "label": "clues shown",
      "to": "all",
      "text": "Red clues: {red_clues}. Blue clues: {blue_clues}."
    },
    {
      "use": "poll",
      "phase": "guess",
      "label": "guesses",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "game": "codes"
        }
      },
      "store": "guess",
      "text": "Choose one code. If you are a Decoder, it is your decode of your own team's clues. If you are an Encryptor, it is your interception of the opposing team's clues (interceptions score nothing in round 1)."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "decode scoring",
      "do": [
        {
          "set": {
            "key": "red_invalid",
            "value": {
              "calc": "not red_valid"
            }
          }
        },
        {
          "set": {
            "key": "blue_invalid",
            "value": {
              "calc": "not blue_valid"
            }
          }
        },
        {
          "set": {
            "key": "last_guesses",
            "value": {
              "calc": "[p.guess for p in players]"
            }
          }
        },
        {
          "set": {
            "key": "red_g",
            "value": {
              "calc": "([p.guess for p in players if p.seat == red_dec] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "blue_g",
            "value": {
              "calc": "([p.guess for p in players if p.seat == blue_dec] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "red_match",
            "value": {
              "calc": "count(red_g[i] == red_code[i] for i in [0, 1, 2]) if len(red_g) == code_length and len(red_code) == code_length else 0"
            }
          }
        },
        {
          "set": {
            "key": "blue_match",
            "value": {
              "calc": "count(blue_g[i] == blue_code[i] for i in [0, 1, 2]) if len(blue_g) == code_length and len(blue_code) == code_length else 0"
            }
          }
        },
        {
          "adjust": {
            "key": "red_gain",
            "value": {
              "calc": "red_match * decode_points_per_position"
            },
            "if": {
              "calc": "not red_invalid"
            }
          }
        },
        {
          "adjust": {
            "key": "red_gain",
            "value": {
              "calc": "exact_decode_bonus_points"
            },
            "if": {
              "calc": "not red_invalid and red_match == code_length"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.team == 'Red'"
            },
            "key": "exact_decodes",
            "value": {
              "calc": "exact_decode_count_gain"
            },
            "if": {
              "calc": "not red_invalid and red_match == code_length"
            }
          }
        },
        {
          "adjust": {
            "key": "blue_gain",
            "value": {
              "calc": "blue_match * decode_points_per_position"
            },
            "if": {
              "calc": "not blue_invalid"
            }
          }
        },
        {
          "adjust": {
            "key": "blue_gain",
            "value": {
              "calc": "exact_decode_bonus_points"
            },
            "if": {
              "calc": "not blue_invalid and blue_match == code_length"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.team == 'Blue'"
            },
            "key": "exact_decodes",
            "value": {
              "calc": "exact_decode_count_gain"
            },
            "if": {
              "calc": "not blue_invalid and blue_match == code_length"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "interception scoring",
      "when": {
        "calc": "round >= first_scoring_interception_round"
      },
      "do": [
        {
          "set": {
            "key": "red_g",
            "value": {
              "calc": "([p.guess for p in players if p.seat == red_enc] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "blue_g",
            "value": {
              "calc": "([p.guess for p in players if p.seat == blue_enc] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "red_match",
            "value": {
              "calc": "count(red_g[i] == blue_code[i] for i in [0, 1, 2]) if len(red_g) == code_length and len(blue_code) == code_length else 0"
            }
          }
        },
        {
          "set": {
            "key": "blue_match",
            "value": {
              "calc": "count(blue_g[i] == red_code[i] for i in [0, 1, 2]) if len(blue_g) == code_length and len(red_code) == code_length else 0"
            }
          }
        },
        {
          "adjust": {
            "key": "red_gain",
            "value": {
              "calc": "red_match * intercept_points_per_position + (exact_intercept_bonus_points if red_match == code_length else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.team == 'Red'"
            },
            "key": "exact_interceptions",
            "value": {
              "calc": "exact_intercept_count_gain"
            },
            "if": {
              "calc": "red_match == code_length"
            }
          }
        },
        {
          "adjust": {
            "key": "blue_gain",
            "value": {
              "calc": "blue_match * intercept_points_per_position + (exact_intercept_bonus_points if blue_match == code_length else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.team == 'Blue'"
            },
            "key": "exact_interceptions",
            "value": {
              "calc": "exact_intercept_count_gain"
            },
            "if": {
              "calc": "blue_match == code_length"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "penalty and totals",
      "do": [
        {
          "adjust": {
            "key": "blue_gain",
            "value": {
              "calc": "invalid_penalty_points"
            },
            "if": {
              "calc": "red_invalid"
            }
          }
        },
        {
          "adjust": {
            "key": "red_gain",
            "value": {
              "calc": "invalid_penalty_points"
            },
            "if": {
              "calc": "blue_invalid"
            }
          }
        },
        {
          "adjust": {
            "key": "red_points",
            "value": {
              "calc": "red_gain"
            }
          }
        },
        {
          "adjust": {
            "key": "blue_points",
            "value": {
              "calc": "blue_gain"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.team == 'Red'"
            },
            "key": "score",
            "value": {
              "calc": "red_points"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.team == 'Blue'"
            },
            "key": "score",
            "value": {
              "calc": "blue_points"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "history",
      "do": [
        {
          "append": {
            "key": "history",
            "value": {
              "calc": "[round, 'Red clues', red_clues, 'Red code', red_code, 'Blue clues', blue_clues, 'Blue code', blue_code]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "the reveal",
      "to": "all",
      "text": "Red's code was {red_code}, Blue's was {blue_code}. Guesses (seats 1, 2, 3, 4): {last_guesses}. Red invalid: {red_invalid}; Blue invalid: {blue_invalid}. Red gained {red_gain} (total {red_points}); Blue gained {blue_gain} (total {blue_points})."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last round",
      "when": {
        "calc": "round > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > rounds"
      },
      "rank_by": "you.score * 10000 + you.exact_interceptions * 100 + you.exact_decodes",
      "text": "Winner: {result}. Red {red_points} points ({players[0].exact_interceptions} exact interceptions, {players[0].exact_decodes} exact decodes); Blue {blue_points} points ({players[2].exact_interceptions} exact interceptions, {players[2].exact_decodes} exact decodes)."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Four players: seats 1 and 2 form team Red, seats 3 and 4 form team Blue. Eight distinct keywords are drawn at random from a fixed list of {keyword_list_size} common nouns. The first four go to Red, numbered 1-4; the next four go to Blue, numbered 1-4. Each team's keywords are shown only to that team's two players. Each team starts with {starting_points} points, 0 exact interceptions and 0 exact decodes. A public history lists, for each team and each past round, its three clues and its revealed true code.\n\nCODES. A code is three different digits from 1-4 in order. There are {code_count} codes, offered in this order: 123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432.\n\nROLES. In odd rounds, seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders. In even rounds, the roles swap.\n\nEACH ROUND ({rounds} rounds):\n1. Roles for the round are announced.\n2. Code choice (simultaneous, secret): each Encryptor chooses one of the {code_count} codes for their team. No one else sees it, not even the teammate.\n3. Clues (simultaneous): each Encryptor writes three clues, separated by commas, one per digit of the code in order. Clue 1 should point to the team keyword numbered by the first digit, and so on.\n4. Clue check. A clue is valid only if all of these hold: it is a single word with no spaces; it is {clue_min_letters}-{clue_max_letters} letters long; ignoring case, it does not contain any of the team's own four keywords and is not contained in any of them; it is not identical, ignoring case, to any clue either team has given in an earlier round. A team with any invalid clue this round is marked invalid; a team whose clues are all valid is not. Play continues either way.\n5. All six clues are shown to everyone.\n6. Guesses (simultaneous): each Decoder chooses one of the {code_count} codes as a decode of their own team's clues. Each Encryptor chooses one of the {code_count} codes as an interception of the opposing team's clues.\n7. Decode scoring, for each team that is not invalid: the team gains {decode_points_per_position} point for each position (first, second, third) where the Decoder's guess matches the team's true code. If all three match, the team gains {exact_decode_bonus_points} more point and 1 exact decode. A team marked invalid gains 0 decode points this round, even if its Decoder's guess is correct.\n8. Interception scoring, rounds {first_scoring_interception_round}-{rounds} only: each team gains {intercept_points_per_position} point for each position where its Encryptor's interception matches the opposing team's true code. If all three match, the team gains {exact_intercept_bonus_points} more points and 1 exact interception. In round 1 interceptions score nothing.\n9. Invalid penalty: if a team is marked invalid, the opposing team gains {invalid_penalty_points} points; if it is not invalid, nobody gains penalty points.\n10. Both true codes, all guesses and all points gained are announced, and the clues and codes are added to the public history.\n\nNo other talk is allowed. The clues are the only communication. Both players on a team always share the same points, exact interceptions and exact decodes.\n\nEND. After round {rounds} the game ends. The team with more points wins, and both of its players win. If points are tied, the team with more exact interceptions wins. If still tied, the team with more exact decodes wins. If still tied, the game is a draw and all four players share the result."
}
```
````
