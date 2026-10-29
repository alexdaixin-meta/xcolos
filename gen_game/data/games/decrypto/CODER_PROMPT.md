# Task: write the XColos game file for "Decrypto Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. There are four players. Seats 1 and 2 form Team White; seats 3 and 4 form Team Black.

The word list is these 40 words: apple, anchor, bridge, candle, castle, cloud, crown, desert, diamond, dragon, drum, eagle, engine, feather, forest, ghost, glacier, hammer, island, jungle, key, ladder, lantern, mirror, moon, needle, ocean, piano, pirate, pyramid, rocket, saddle, shadow, ship, snake, spider, sword, tiger, volcano, whistle.

At the start, the engine shuffles the list and deals 8 different words: the first 4 to White as keywords 1, 2, 3, 4 and the next 4 to Black as keywords 1, 2, 3, 4. A team's keywords are shown only to its two members and never change.

The engine tracks for each team: Interceptions (start 0), Miscommunications (start 0) and Correct Decodes (start 0). It also keeps a public history listing, for every finished round, each team's three clues and true code. All counters are public.

ROLES. In odd rounds (1, 3, 5, 7), seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders. In even rounds (2, 4, 6, 8), seats 2 and 4 are Encryptors and seats 1 and 3 are Decoders.

CLUE RULES. A clue is one word or a short phrase. It must point to the matching keyword of the clue-giver's own team by its general meaning only. A clue may NOT:
(1) point to the keyword by spelling, letters, sound, rhyme, length or alphabetical position;
(2) contain the keyword, a part of it, or a word with the same root;
(3) repeat, word for word, a clue the same team used in an earlier round;
(4) refer to the game itself: seats, rounds, codes, digits or keyword numbers, earlier clues, or the other team's words;
(5) refer to private information, meaning anything not available from general knowledge, such as personal experiences, in-jokes or anything known only to the teammates.

EACH ROUND:
1. ANNOUNCE. The engine announces the round number and who is Encryptor and Decoder on each team.
2. ENCRYPT (simultaneous; Encryptors only). Each Encryptor privately submits a secret code and three clues. The code is three different digits from 1 to 4, in any order (for example 3-1-4). The three clues are given in code order: the first clue for the first digit's keyword, and so on.
3. CHECK. For each team, a referee rules the Encryptor's answer valid or invalid. It is valid only if the code is three different digits from 1 to 4 and all three clues obey the clue rules. If it is invalid, that team gains exactly 1 Miscommunication now. Its Decoder's guess this round will be ignored: step 6 does not score that team's decode at all, gives no further Miscommunication and adds no Correct Decode.
4. REVEAL. Both teams' clues are shown to all four players at once. Codes stay secret.
5. GUESS (simultaneous; all four players). Each Decoder submits a guess of their own team's code. Each Encryptor submits a guess of the opposing team's code. A guess must be three different digits from 1 to 4. Any other answer, or no answer, counts as a wrong guess. In round 1, Encryptors still answer, but their guesses are ignored.
6. SCORE.
   (a) DECODE, only for a team whose answer was valid in step 3. If the Decoder's guess equals the team's true code digit by digit in order, the team gains 1 Correct Decode. Otherwise it gains 1 Miscommunication.
   (b) INTERCEPT, from round 2 on, for both teams, whether or not the opposing answer was valid. If an Encryptor's guess equals the opposing team's true code digit by digit in order, the Encryptor's team gains 1 Interception. A code with repeated or out-of-range digits can never be matched.
7. HISTORY. Both true codes are shown to everyone and added to the public history beside that round's clues.
8. END CHECK. The game ends now if any team has 2 or more Interceptions or 2 or more Miscommunications, or if round 8 has just finished. Otherwise the next round begins.

There is no discussion phase. Teammates may communicate only through official clues.

How the winner is decided: When the game ends, apply these rules in order:
1. If exactly one team has 2 or more Interceptions together with fewer than 2 Miscommunications, that team wins.
2. Otherwise, if exactly one team has 2 or more Miscommunications, the other team wins.
3. Otherwise (both teams triggered an end condition in the same round, or round 8 ended):
   (a) the team with the higher net score (Interceptions minus Miscommunications) wins;
   (b) if tied, the team with more Interceptions wins;
   (c) if still tied, the team with more Correct Decodes wins;
   (d) if still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Decrypto Duel (4 to 4 players, best with 4)

Two teams of two take turns giving three meaning-only clues to a secret 3-digit code over their team's four hidden keywords. Teammates must decode their own code while the rival team tries to intercept it.

STATE (every item below must exist in the file):
  - each player: team (text, starts 'white for seats 1-2, black for seats 3-4'); everyone sees it. the player's team
  - each player: team_sign (number, starts '1 for seats 1-2, -1 for seats 3-4'); everyone sees it. +1 for White, -1 for Black, used to rank by the table result
  - each player: keywords (list, starts '[] (dealt in setup)'); only its owner sees it. the team's 4 keywords in order 1-4, the same list for both teammates, never changing
  - each player: role (text, starts ''); everyone sees it. encryptor or decoder this round
  - each player: guess (text, starts ''); only its owner sees it. this round's code guess, as one of the 24 permutations such as 3-1-4
  - the table: deck (list, starts 'the 40 words: apple, anchor, bridge, candle, castle, cloud, crown, desert, diamond, dragon, drum, eagle, engine, feather, forest, ghost, glacier, hammer, island, jungle, key, ladder, lantern, mirror, moon, needle, ocean, piano, pirate, pyramid, rocket, saddle, shadow, ship, snake, spider, sword, tiger, volcano, whistle'); hidden from all players. undealt words
  - the table: round (number, starts 0); everyone sees it. current round number
  - the table: white_code (text, starts ''); hidden from all players. White's secret code this round, until it is revealed in history
  - the table: black_code (text, starts ''); hidden from all players. Black's secret code this round, until it is revealed in history
  - the table: white_clues (text, starts ''); everyone sees it. White's three clues this round, in code order, separated by ' / '
  - the table: black_clues (text, starts ''); everyone sees it. Black's three clues this round, in code order, separated by ' / '
  - the table: white_valid (bool, starts True); everyone sees it. whether White's encryption was ruled valid this round
  - the table: black_valid (bool, starts True); everyone sees it. whether Black's encryption was ruled valid this round
  - the table: white_interceptions (number, starts 0); everyone sees it. White's Interceptions
  - the table: white_miscommunications (number, starts 0); everyone sees it. White's Miscommunications
  - the table: white_decodes (number, starts 0); everyone sees it. White's Correct Decodes
  - the table: black_interceptions (number, starts 0); everyone sees it. Black's Interceptions
  - the table: black_miscommunications (number, starts 0); everyone sees it. Black's Miscommunications
  - the table: black_decodes (number, starts 0); everyone sees it. Black's Correct Decodes
  - the table: history (list, starts []); everyone sees it. for each finished round: each team's three clues and true code
  - the table: result (number, starts 0); everyone sees it. +1 if White currently wins by the winner rules, -1 if Black does, 0 if it is a draw
  - parameters, each kept as a table attribute: player_count = 4, team_size = 2, word_list_size = 40, keywords_per_team = 4, code_length = 3, code_digit_min = 1, code_digit_max = 4, max_rounds = 8, interception_limit = 2, miscommunication_limit = 2, first_intercept_round = 2, correct_decode_gain = 1, miscommunication_gain = 1, interception_gain = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1 and 2 get team = white and team_sign = 1; seats 3 and 4 get team = black and team_sign = -1.
  2. The engine draws 4 different words at random from deck, removing each from deck, into seat 1's keywords as keywords 1-4, and copies that list into seat 2's keywords.
  3. The engine draws 4 more different words at random from deck, removing each from deck, into seat 3's keywords as keywords 1-4, and copies that list into seat 4's keywords.
  4. All six team counters start at 0, history starts empty and round starts at 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; if round is odd, seats 1 and 3 get role = encryptor and seats 2 and 4 get role = decoder; if round is even, seats 2 and 4 get role = encryptor and seats 1 and 3 get role = decoder; set white_valid = true and black_valid = true; announce the round number and each team's Encryptor and Decoder.
  2. [poll] the two players with role = encryptor answers: one of the 24 codes of three different digits from 1 to 4: 1-2-3, 1-2-4, 1-3-2, 1-3-4, 1-4-2, 1-4-3, 2-1-3, 2-1-4, 2-3-1, 2-3-4, 2-4-1, 2-4-3, 3-1-2, 3-1-4, 3-2-1, 3-2-4, 3-4-1, 3-4-2, 4-1-2, 4-1-3, 4-2-1, 4-2-3, 4-3-1, 4-3-2. What happens: the White Encryptor's answer is stored in white_code and the Black Encryptor's in black_code (both hidden).
  3. [poll] the two players with role = encryptor answers: short text: three clues in code order, separated by ' / '. What happens: the White Encryptor's text is stored in white_clues and the Black Encryptor's in black_clues.
  4. [update] the White Encryptor. What happens: if judged false: white_valid = false and white_miscommunications += 1. JUDGED: a referee rules true or false on "White's three clues in white_clues each point to the White keyword numbered by the matching digit of white_code by general meaning only, and none uses spelling, letters, sound, rhyme, length or alphabetical position, contains the keyword or part of it or a same-root word, repeats word for word a clue White used in an earlier round of history, refers to the game itself (seats, rounds, codes, digits, keyword numbers, earlier clues, the other team's words), or refers to private information."; write this step's `when` as {"prose": that sentence, verbatim}.
  5. [update] the Black Encryptor. What happens: if judged false: black_valid = false and black_miscommunications += 1. JUDGED: a referee rules true or false on "Black's three clues in black_clues each point to the Black keyword numbered by the matching digit of black_code by general meaning only, and none uses spelling, letters, sound, rhyme, length or alphabetical position, contains the keyword or part of it or a same-root word, repeats word for word a clue Black used in an earlier round of history, refers to the game itself (seats, rounds, codes, digits, keyword numbers, earlier clues, the other team's words), or refers to private information."; write this step's `when` as {"prose": that sentence, verbatim}.
  6. [tell] all players. What happens: show white_clues and black_clues to all four players at once; codes stay secret.
  7. [poll] all players answers: one of the 24 codes of three different digits from 1 to 4 (decoders guess their own team's code, encryptors guess the opposing team's code). What happens: each player's answer is stored in their guess; no answer leaves guess empty, which never matches.
  8. [update] the two decoders. What happens: when white_valid: if the White decoder's guess == white_code then white_decodes += 1, else white_miscommunications += 1. When black_valid: if the Black decoder's guess == black_code then black_decodes += 1, else black_miscommunications += 1. A team with valid = false is not scored here.
  9. [update] the two encryptors. What happens: when round >= 2: if the White encryptor's guess == black_code then white_interceptions += 1; if the Black encryptor's guess == white_code then black_interceptions += 1 (regardless of validity).
  10. [update] all players. What happens: append to history an entry {round, white_clues, white_code, black_clues, black_code} and announce both true codes to everyone.
  11. [update] all players. What happens: compute result: let WQ = (white_interceptions >= 2 and white_miscommunications < 2), BQ = (black_interceptions >= 2 and black_miscommunications < 2), WM = (white_miscommunications >= 2), BM = (black_miscommunications >= 2). If WQ and not BQ then result = 1; else if BQ and not WQ then result = -1; else if BM and not WM then result = 1; else if WM and not BM then result = -1; else let K = (white_interceptions - white_miscommunications - black_interceptions + black_miscommunications) * 10000 + (white_interceptions - black_interceptions) * 100 + (white_decodes - black_decodes), and result = 1 if K > 0, -1 if K < 0, 0 if K == 0.
  12. [check] all players. What happens: end the game if white_interceptions >= 2 or black_interceptions >= 2 or white_miscommunications >= 2 or black_miscommunications >= 2 or round >= 8; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When setup runs, then seats 1 and 2 are Team White, seats 3 and 4 are Team Black, and each team receives 4 different words from the 40-word list, so 8 distinct words are dealt in total.
  R2. When keywords are dealt, then both members of a team hold the same keyword list, it is visible only to them, and it never changes.
  R3. When a round is odd (1, 3, 5, 7), then seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders.
  R4. When a round is even (2, 4, 6, 8), then seats 2 and 4 are Encryptors and seats 1 and 3 are Decoders.
  R5. When the Encryptors submit, then only Encryptors are asked, simultaneously, for a code of three different digits from 1 to 4 and three clues in code order.
  R6. When the referee rules a team's clues invalid, then that team gains exactly 1 Miscommunication and its decode is not scored that round, with no further Miscommunication and no Correct Decode.
  R7. When clues are revealed, then both teams' clues are shown to all four players and both codes stay hidden until the history step.
  R8. When guesses are taken, then all four players answer simultaneously: decoders guess their own team's code and encryptors guess the opposing team's code.
  R9. When a valid team's Decoder guess equals its true code digit by digit, then that team gains 1 Correct Decode; otherwise it gains 1 Miscommunication.
  R10. When round >= 2 and an Encryptor's guess equals the opposing team's true code digit by digit, then the Encryptor's team gains 1 Interception, whether or not the opposing team's clues were valid.
  R11. When it is round 1, then Encryptors' guesses are ignored and no Interception can be scored.
  R12. When a player gives no answer to the guess, then it counts as a wrong guess.
  R13. When a round's scoring finishes, then both true codes are shown to everyone and appended to history beside that round's clues.
  R14. When, after a round, any team has 2 or more Interceptions or 2 or more Miscommunications, or round 8 has finished, then the game ends.
  R15. When the game ends and exactly one team has 2 or more Interceptions with fewer than 2 Miscommunications, then that team wins.
  R16. When rule R15 does not decide it and exactly one team has 2 or more Miscommunications, then the other team wins.
  R17. When neither R15 nor R16 decides, then the team with the higher Interceptions minus Miscommunications wins; if tied, the team with more Interceptions wins; if still tied, the team with more Correct Decodes wins; if still tied, it is a draw.
  R18. When the game is running, then there is no discussion phase, and teammates communicate only through official clues.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Encrypt: choose your secret code | asked: the two seats with role = encryptor (seats 1 and 3 in odd rounds, seats 2 and 4 in even rounds) | options: any of the 24 orderings of three different digits from 1 to 4; decoders are not asked
  - Encrypt: give three clues in code order | asked: the two encryptor seats | options: free short text with three clues separated by ' / '
  - Guess a code | asked: all four seats | options: any of the 24 orderings of three different digits from 1 to 4 (a decoder guesses their own team's code, an encryptor guesses the opposing team's code; in round 1 encryptors are still offered these, but their answers are ignored)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: white_interceptions >= 2 or black_interceptions >= 2 or white_miscommunications >= 2 or black_miscommunications >= 2 or round >= 8
  - each player's standing: you.team_sign * result (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: result is +1 if White wins by the ordered rules (sole team with 2+ Interceptions and fewer than 2 Miscommunications; else the sole team without 2+ Miscommunications; else higher Interceptions minus Miscommunications, then more Interceptions, then more Correct Decodes), -1 if Black wins, and 0 on a draw. Both members of the winning team score 1 and win together. On a draw all four score 0 and share the result.
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

- each player: `team` (text, visible: public, starts 'white for seats 1-2, black for seats 3-4'): the player's team
- the table: `round` (number, visible: public, starts 0): current round number
- the table: `white_clues` (text, visible: public, starts ''): White's three clues this round, in code order, separated by ' / '
- the table: `black_clues` (text, visible: public, starts ''): Black's three clues this round, in code order, separated by ' / '
- the table: `white_interceptions` (number, visible: public, starts 0): White's Interceptions
- the table: `white_miscommunications` (number, visible: public, starts 0): White's Miscommunications
- the table: `white_decodes` (number, visible: public, starts 0): White's Correct Decodes
- the table: `black_interceptions` (number, visible: public, starts 0): Black's Interceptions
- the table: `black_miscommunications` (number, visible: public, starts 0): Black's Miscommunications
- the table: `black_decodes` (number, visible: public, starts 0): Black's Correct Decodes
- the table: `history` (list, visible: public, starts []): for each finished round: each team's three clues and true code
- the table: `result` (number, visible: public, starts 0): +1 if White currently wins by the winner rules, -1 if Black does, 0 if it is a draw
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 4, team_size = 2, word_list_size = 40, keywords_per_team = 4, code_length = 3, code_digit_min = 1, code_digit_max = 4, max_rounds = 8, interception_limit = 2, miscommunication_limit = 2, first_intercept_round = 2, correct_decode_gain = 1, miscommunication_gain = 1, interception_gain = 1
- the game ends with ONE ending whose `rank_by` is `you.team_sign * result`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
