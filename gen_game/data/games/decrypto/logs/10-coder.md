# 10 coder

- time: 2026-10-27T21:07:49+00:00 (85.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 21171b303431699e, reply sha256 56ee427bd5b8266d

## Sent

````
# Task: write the XColos game file for "Decrypto Duel (Paired Rounds)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
- There are 4 players: Team A (A1, A2) and Team B (B1, B2).
- The engine deals each team 4 different keywords from a fixed list of 120 common concrete nouns. No word is given to both teams.
- A team's keywords are numbered 1 to 4. They are shown privately to both members of that team and never to the other team.
- A public clue history shows, for each team, four columns (keywords 1-4) that start empty.
- Each team starts with 0 Interceptions and 0 Miscommunications. Token counts are always public.

PAIRS AND ROLES
- The game has up to 16 rounds, grouped into 8 pairs: pair 1 = rounds 1-2, pair 2 = rounds 3-4, ..., pair 8 = rounds 15-16.
- In each pair, each team encrypts exactly once.
- In odd pairs (1, 3, 5, 7), Team A encrypts in the first round of the pair and Team B in the second.
- In even pairs (2, 4, 6, 8), Team B encrypts first and Team A second.
- In each pair, each team has one Encryptor and one Guesser:
  - Odd pairs: A1 and B1 are Encryptors; A2 and B2 are Guessers.
  - Even pairs: A2 and B2 are Encryptors; A1 and B1 are Guessers.
- In a round where a team encrypts:
  - The Encryptor is that team's Encryptor for the pair.
  - The Decoder is that team's Guesser.
  - The Interceptor is the other team's Guesser.
  - The other team's Encryptor only watches.
- Full table (round: Encryptor / Decoder / Interceptor):
  - R1: A1 / A2 / none
  - R2: B1 / B2 / none
  - R3: B2 / B1 / A1
  - R4: A2 / A1 / B1
  - R5: A1 / A2 / B2
  - R6: B1 / B2 / A2
  - R7: B2 / B1 / A1
  - R8: A2 / A1 / B1
  - R9: A1 / A2 / B2
  - R10: B1 / B2 / A2
  - R11: B2 / B1 / A1
  - R12: A2 / A1 / B1
  - R13: A1 / A2 / B2
  - R14: B1 / B2 / A2
  - R15: B2 / B1 / A1
  - R16: A2 / A1 / B1

EACH ROUND
1. The engine announces the round number, the encrypting team, the Encryptor and the Decoder. In rounds 3-16 it also announces the Interceptor. In rounds 1 and 2 it announces that there is no interception.
2. The engine draws a code uniformly at random from the 24 ordered sequences of three different digits from 1 to 4 (for example 3-1-4). It shows the code privately to the Encryptor only.
3. The Encryptor writes three clues, one per digit, in code order. Each clue points to the keyword with that number and is at most 3 words.
4. Referee check. The clue set is valid only if all of these hold:
   - Every clue relates to its keyword by meaning or association.
   - No clue hints by spelling, letters, letter count, rhyme, or keyword number or position.
   - No clue contains its keyword or a form of it.
   - No clue repeats any clue this team has used before.
   If the set is invalid:
   - The code is revealed to everyone.
   - The encrypting team gains 1 Miscommunication.
   - The clues are not added to the history.
   - The round goes to step 8.
5. The valid clues are shown to all players.
6. At the same moment, the Decoder privately submits a guessed 3-digit code and the Interceptor (if any) privately submits a guessed 3-digit code.
7. The true code and the guesses are revealed, then scored:
   - If the Decoder's guess differs from the true code in any digit, the encrypting team gains 1 Miscommunication.
   - If the Interceptor's guess equals the true code exactly, the Interceptor's team gains 1 Interception.
   - Each clue is added to the encrypting team's public history column for the keyword it clued.
8. End check, only in even-numbered rounds (the end of a pair). In odd-numbered rounds, play continues.
   - A team TRIGGERS if it has 2 or more Interceptions, or if the other team has 2 or more Miscommunications.
   - If exactly one team triggers, it wins and the game ends.
   - If both teams trigger, apply the comparison rule and the game ends.
   - If neither team triggers and this was round 16, apply the comparison rule.
   - Otherwise play continues.

COMPARISON RULE
- Each team's value is its Interceptions minus its Miscommunications.
- The higher value wins. Equal values are a draw.

COMMUNICATION
- There is no talk phase. Players communicate only through clues. Teammates may not message each other.

How the winner is decided: The winner is decided only at the end of an even-numbered round. A team triggers if it holds 2 or more Interceptions or if the opponent holds 2 or more Miscommunications. If exactly one team triggers, it wins. If both trigger, or if neither has triggered by the end of round 16, each team's value is its Interceptions minus its Miscommunications: the higher value wins and equal values are a draw. Both members of a team share its result.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Decrypto Duel (Paired Rounds) (4 to 4 players, best with 4)

Two teams of two take turns sending a secret three-digit code through clues about their own four hidden keywords; the rival Guesser tries to intercept, and a team wins at the end of a pair with 2 Interceptions or when its rival has 2 Miscommunications, otherwise by Interceptions minus Miscommunications.

STATE (every item below must exist in the file):
  - each player: team (text, starts 'seats 1-2: A, seats 3-4: B'); everyone sees it. the player's team (seat 1 = A1, seat 2 = A2, seat 3 = B1, seat 4 = B2)
  - each player: keywords (list, starts []); only its owner sees it. the team's 4 keywords, numbered 1-4 by list position; both teammates hold the same copy
  - each player: my_code (text, starts ''); only its owner sees it. this round's secret code, set only for the Encryptor
  - each player: standing (number, starts 0); everyone sees it. (own team triggers - other team triggers) * 1000 + own team Interceptions - own team Miscommunications; recomputed at the end of each pair
  - the table: round_number (number, starts 0); everyone sees it. current round, 1 to 16
  - the table: word_list (list, starts '120 common concrete nouns'); hidden from all players. the deck that keywords are dealt from
  - the table: code_list (list, starts ['1-2-3', '1-2-4', '1-3-2', '1-3-4', '1-4-2', '1-4-3', '2-1-3', '2-1-4', '2-3-1', '2-3-4', '2-4-1', '2-4-3', '3-1-2', '3-1-4', '3-2-1', '3-2-4', '3-4-1', '3-4-2', '4-1-2', '4-1-3', '4-2-1', '4-2-3', '4-3-1', '4-3-2']); everyone sees it. the 24 possible codes, also the options for a guess
  - the table: enc_team (text, starts ''); everyone sees it. the team encrypting this round (A or B)
  - the table: encryptor_seat (number, starts 0); everyone sees it. seat of this round's Encryptor
  - the table: decoder_seat (number, starts 0); everyone sees it. seat of this round's Decoder
  - the table: interceptor_seat (number, starts 0); everyone sees it. seat of this round's Interceptor, 0 when there is none (rounds 1-2)
  - the table: current_code (text, starts ''); hidden from all players. this round's true code
  - the table: revealed_code (text, starts ''); everyone sees it. the true code once revealed this round
  - the table: current_clues (text, starts ''); hidden from all players. the Encryptor's three clues; shown to everyone only if valid
  - the table: clue_valid (bool, starts False); everyone sees it. the referee's ruling on this round's clue set
  - the table: decoder_guess (text, starts ''); everyone sees it. the Decoder's guess, revealed after both guesses are in
  - the table: interceptor_guess (text, starts ''); everyone sees it. the Interceptor's guess, revealed after both guesses are in
  - the table: clue_history_a (list, starts []); everyone sees it. Team A's valid past clues, each tagged with the keyword number it clued (columns 1-4)
  - the table: clue_history_b (list, starts []); everyone sees it. Team B's valid past clues, each tagged with the keyword number it clued (columns 1-4)
  - the table: a_interceptions (number, starts 0); everyone sees it. Team A's Interception tokens
  - the table: a_miscommunications (number, starts 0); everyone sees it. Team A's Miscommunication tokens
  - the table: b_interceptions (number, starts 0); everyone sees it. Team B's Interception tokens
  - the table: b_miscommunications (number, starts 0); everyone sees it. Team B's Miscommunication tokens
  - parameters, each kept as a table attribute: player_count = 4, team_size = 2, keywords_per_team = 4, word_list_size = 120, max_rounds = 16, pairs = 8, code_length = 3, code_digit_max = 4, code_count = 24, clue_max_words = 3, interception_trigger = 2, miscommunication_trigger = 2, first_interception_round = 3, trigger_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1 and 2 are Team A (A1, A2). Seats 3 and 4 are Team B (B1, B2).
  2. word_list is filled with 120 common concrete nouns.
  3. Four words are drawn at random from word_list, one at a time and removed as they are drawn, and are set in order as keywords 1-4 of seat 1 and seat 2.
  4. Four more words are drawn the same way from what remains and set as keywords 1-4 of seat 3 and seat 4, so no word goes to both teams.
  5. Each player is privately shown their own keywords.
  6. All token counts start at 0 and are public. clue_history_a and clue_history_b start empty, with four columns each.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] engine. What happens: round_number += 1; pair = (round_number + 1) div 2; enc_team = A if pair % 2 == round_number % 2, else B; in an odd pair encryptor_seat = 1 (A) or 3 (B) and decoder_seat = 2 (A) or 4 (B); in an even pair encryptor_seat = 2 (A) or 4 (B) and decoder_seat = 1 (A) or 3 (B); interceptor_seat = 0 if round_number < 3, otherwise the other team's Guesser (odd pair: 4 if enc_team = A, else 2; even pair: 3 if enc_team = A, else 1); clear my_code for every player; clear revealed_code, decoder_guess, interceptor_guess, current_clues; set clue_valid = false
  2. [tell] all players. What happens: announce round_number, enc_team, encryptor_seat and decoder_seat; if interceptor_seat > 0, announce the Interceptor; otherwise announce that there is no interception this round
  3. [update] engine. What happens: current_code = one entry of code_list drawn uniformly at random; set my_code of encryptor_seat = current_code
  4. [sync] all players. What happens: each player receives their own state; only the Encryptor sees my_code; each player sees their own keywords
  5. [ask] seat encryptor_seat answers: short text: three clues in code order, separated by ' / ', each at most 3 words. What happens: current_clues = the answer
  6. [update] engine. What happens: clue_valid = the referee's ruling JUDGED: a referee rules true or false on "Each of the three clues in current_clues relates by meaning or association to the keyword (from the encrypting team's keywords) numbered by its digit of current_code, no clue hints by spelling, letters, letter count, rhyme or keyword number or position, no clue contains its keyword or a form of it, and no clue repeats a clue already in the encrypting team's clue history."; write this step's `when` as {"prose": that sentence, verbatim}.
  7. [update] engine. What happens: when clue_valid is false: revealed_code = current_code; the encrypting team's miscommunications += 1 (a_miscommunications if enc_team = A, else b_miscommunications); the clues are not added to the history; the guess steps of this round are skipped
  8. [tell] all players. What happens: when clue_valid is true: show current_clues to everyone; when clue_valid is false: announce that the clue set was invalid, the code revealed_code, and the Miscommunication
  9. [poll] seat decoder_seat, and seat interceptor_seat when interceptor_seat > 0 answers: one code from code_list. What happens: when clue_valid is true: decoder_guess = the Decoder's answer; interceptor_guess = the Interceptor's answer (if any); neither sees the other's guess until both are in
  10. [update] engine. What happens: when clue_valid is true: revealed_code = current_code; if decoder_guess != current_code, the encrypting team's miscommunications += 1; if interceptor_seat > 0 and interceptor_guess == current_code, the Interceptor's team's interceptions += 1 (b_interceptions if enc_team = A, else a_interceptions); append each clue tagged with its digit to clue_history_a (enc_team = A) or clue_history_b (enc_team = B)
  11. [tell] all players. What happens: when clue_valid is true: announce revealed_code, decoder_guess, interceptor_guess (if any) and all four token counts
  12. [update] engine. What happens: when round_number % 2 == 0: trig_a = 1 if a_interceptions >= 2 or b_miscommunications >= 2, else 0; trig_b = 1 if b_interceptions >= 2 or a_miscommunications >= 2, else 0; for seats 1-2 standing = (trig_a - trig_b) * 1000 + a_interceptions - a_miscommunications; for seats 3-4 standing = (trig_b - trig_a) * 1000 + b_interceptions - b_miscommunications
  13. [check] engine. What happens: end the game if round_number % 2 == 0 and (a_interceptions >= 2 or b_miscommunications >= 2 or b_interceptions >= 2 or a_miscommunications >= 2 or round_number >= 16); otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each team is dealt 4 different keywords from a list of 120 nouns; no word goes to both teams, and a team's keywords are visible only to its two members.
  R2. All four token counts (a_interceptions, a_miscommunications, b_interceptions, b_miscommunications) start at 0 and are public.
  R3. When round_number is odd in an odd pair, or even in an even pair, Team A encrypts; otherwise Team B encrypts.
  R4. In odd pairs (rounds 1-2, 5-6, 9-10, 13-14), seats 1 and 3 are Encryptors and seats 2 and 4 are Guessers; in even pairs, seats 2 and 4 are Encryptors and seats 1 and 3 are Guessers.
  R5. The Decoder is the encrypting team's Guesser, and the Interceptor is the other team's Guesser, so round 3 is Encryptor seat 4, Decoder seat 3, Interceptor seat 1.
  R6. In rounds 1 and 2, interceptor_seat is 0, no interception guess is asked, and the engine announces that there is no interception.
  R7. Each round, the code is drawn uniformly from the 24 ordered sequences of three different digits from 1 to 4 and is shown only to the Encryptor.
  R8. The Encryptor submits three clues in code order, each at most 3 words.
  R9. When the referee rules the clue set invalid, the code is revealed to everyone, the encrypting team gains 1 Miscommunication, no clues are added to the history and no guesses are taken.
  R10. When the clue set is valid, the clues are shown to all players before the guesses.
  R11. The Decoder and the Interceptor submit their guesses at the same time, and neither sees the other's guess until both are in.
  R12. When the Decoder's guess differs from the true code in any digit, the encrypting team gains 1 Miscommunication.
  R13. When the Interceptor's guess equals the true code exactly, the Interceptor's team gains 1 Interception.
  R14. When the clues are valid, each clue is appended to the encrypting team's public history under the keyword number it clued.
  R15. The game can end only after an even-numbered round; after an odd-numbered round play always continues.
  R16. A team triggers when it has 2 or more Interceptions or the other team has 2 or more Miscommunications.
  R17. When exactly one team triggers at the end of an even round, that team wins and the game ends.
  R18. When both teams trigger at the end of an even round, the team with the higher Interceptions minus Miscommunications wins, and equal values are a draw.
  R19. When neither team has triggered by the end of round 16, the team with the higher Interceptions minus Miscommunications wins, and equal values are a draw.
  R20. Both members of a team share its result, and there is no talk phase.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Write three clues for your code | asked: seat encryptor_seat only | options: short text: three clues separated by ' / ', each at most 3 words; the other three seats are not asked
  - Guess the code | asked: seat decoder_seat, and seat interceptor_seat when interceptor_seat > 0 | options: Decoder: any of the 24 codes in code_list; Interceptor (rounds 3-16): any of the 24 codes in code_list; the watching Encryptor of the other team and the Encryptor are not asked; nobody is asked when the clue set was invalid

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number % 2 == 0 and (a_interceptions >= 2 or b_miscommunications >= 2 or b_interceptions >= 2 or a_miscommunications >= 2 or round_number >= 16)
  - each player's standing: you.standing (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their team's trigger edge times 1000 plus the team's Interceptions minus its Miscommunications. A team triggers with 2 or more Interceptions or when the other team has 2 or more Miscommunications. If exactly one team triggers, both its members rank highest and win. If both trigger, or neither has triggered by round 16, the team with the higher Interceptions minus Miscommunications wins. Equal values are a draw: all four players share the win.
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

- each player: `standing` (number, visible: public, starts 0): (own team triggers - other team triggers) * 1000 + own team Interceptions - own team Miscommunications; recomputed at the end of each pair
- the table: `round_number` (number, visible: public, starts 0): current round, 1 to 16
- the table: `revealed_code` (text, visible: public, starts ''): the true code once revealed this round
- the table: `a_interceptions` (number, visible: public, starts 0): Team A's Interception tokens
- the table: `a_miscommunications` (number, visible: public, starts 0): Team A's Miscommunication tokens
- the table: `b_interceptions` (number, visible: public, starts 0): Team B's Interception tokens
- the table: `b_miscommunications` (number, visible: public, starts 0): Team B's Miscommunication tokens
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 4, team_size = 2, keywords_per_team = 4, word_list_size = 120, max_rounds = 16, pairs = 8, code_length = 3, code_digit_max = 4, code_count = 24, clue_max_words = 3, interception_trigger = 2, miscommunication_trigger = 2, first_interception_round = 3, trigger_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.standing`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "decrypto_duel_paired",
    "name": "Decrypto Duel (Paired Rounds)",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Two teams of two send secret three-digit codes through clues about hidden keywords while the rival Guesser tries to intercept."
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
        "initial": "",
        "values": [
          "",
          "A",
          "B"
        ]
      },
      {
        "key": "keywords",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "my_code",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "standing",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guess",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pair_number",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "word_list",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "code_list",
        "visible": "public",
        "type": "list",
        "initial": [
          "1-2-3",
          "1-2-4",
          "1-3-2",
          "1-3-4",
          "1-4-2",
          "1-4-3",
          "2-1-3",
          "2-1-4",
          "2-3-1",
          "2-3-4",
          "2-4-1",
          "2-4-3",
          "3-1-2",
          "3-1-4",
          "3-2-1",
          "3-2-4",
          "3-4-1",
          "3-4-2",
          "4-1-2",
          "4-1-3",
          "4-2-1",
          "4-2-3",
          "4-3-1",
          "4-3-2"
        ]
      },
      {
        "key": "enc_team",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "encryptor_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "decoder_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "interceptor_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_code",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed_code",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "current_clues",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "shown_clues",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clue_valid",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "decoder_guess",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "interceptor_guess",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clue_history_a",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_history_b",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "a_interceptions",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "a_miscommunications",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "b_interceptions",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "b_miscommunications",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
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
        "key": "keywords_per_team",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "word_list_size",
        "visible": "public",
        "type": "number",
        "initial": 120
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "pairs",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "code_length",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "key": "clue_max_words",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "interception_trigger",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "miscommunication_trigger",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_interception_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "trigger_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "teams and tokens",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat <= team_size"
            },
            "key": "team",
            "value": "A"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat > team_size"
            },
            "key": "team",
            "value": "B"
          }
        },
        {
          "set": {
            "key": "a_interceptions",
            "value": 0
          }
        },
        {
          "set": {
            "key": "a_miscommunications",
            "value": 0
          }
        },
        {
          "set": {
            "key": "b_interceptions",
            "value": 0
          }
        },
        {
          "set": {
            "key": "b_miscommunications",
            "value": 0
          }
        },
        {
          "set": {
            "key": "clue_history_a",
            "value": []
          }
        },
        {
          "set": {
            "key": "clue_history_b",
            "value": []
          }
        }
      ],
      "text": "Seats 1 and 2 are Team A (A1, A2). Seats 3 and 4 are Team B (B1, B2). All tokens start at 0."
    },
    {
      "use": "update",
      "label": "the word list",
      "do": [
        {
          "set": {
            "key": "word_list",
            "value": [
              "apple", "anchor", "arrow", "axe", "balloon", "banana", "barrel", "basket", "bell", "bicycle",
              "blanket", "boat", "book", "bottle", "bowl", "bread", "brick", "bridge", "broom", "bucket",
              "butterfly", "cactus", "camera", "candle", "car", "carrot", "castle", "chair", "cheese", "clock",
              "cloud", "coin", "comb", "compass", "crown", "cup", "curtain", "desk", "diamond", "dog",
              "door", "drum", "eagle", "egg", "envelope", "feather", "fence", "flag", "flower", "fork",
              "fountain", "frog", "glove", "guitar", "hammer", "hat", "helmet", "honey", "horse", "island",
              "jacket", "kettle", "key", "kite", "ladder", "lamp", "leaf", "lemon", "lighthouse", "lion",
              "lock", "map", "mirror", "moon", "mountain", "mushroom", "nail", "needle", "nest", "ocean",
              "onion", "orange", "owl", "paint", "pencil", "piano", "pillow", "pipe", "pizza", "planet",
              "pumpkin", "rabbit", "river", "robot", "rocket", "rope", "saddle", "sandwich", "scissors", "shark",
              "sheep", "shell", "shield", "ship", "shoe", "snake", "sock", "spoon", "star", "sword",
              "table", "tent", "tiger", "tomato", "tower", "train", "tree", "trumpet", "umbrella", "volcano"
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal Team A keywords",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
        }
      ]
    },
    {
      "use": "update",
      "label": "deal Team B keywords",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
      "use": "sync",
      "label": "your keywords",
      "mode": "self",
      "to": "all",
      "fields": [
        "team",
        "keywords"
      ],
      "text": "Your team and your keywords (numbered 1-4 in list order):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roles",
      "label": "the round's roles",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "pair_number",
            "value": {
              "calc": "int((round_number + 1) / 2)"
            }
          }
        },
        {
          "set": {
            "key": "enc_team",
            "value": {
              "calc": "'A' if pair_number % 2 == round_number % 2 else 'B'"
            }
          }
        },
        {
          "set": {
            "key": "encryptor_seat",
            "value": {
              "calc": "((1 if enc_team == 'A' else 3) if pair_number % 2 == 1 else (2 if enc_team == 'A' else 4))"
            }
          }
        },
        {
          "set": {
            "key": "decoder_seat",
            "value": {
              "calc": "((2 if enc_team == 'A' else 4) if pair_number % 2 == 1 else (1 if enc_team == 'A' else 3))"
            }
          }
        },
        {
          "set": {
            "key": "interceptor_seat",
            "value": {
              "calc": "0 if round_number < first_interception_round else ((4 if enc_team == 'A' else 2) if pair_number % 2 == 1 else (3 if enc_team == 'A' else 1))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "my_code",
            "value": ""
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
            "key": "revealed_code",
            "value": ""
          }
        },
        {
          "set": {
            "key": "decoder_guess",
            "value": ""
          }
        },
        {
          "set": {
            "key": "interceptor_guess",
            "value": ""
          }
        },
        {
          "set": {
            "key": "current_clues",
            "value": ""
          }
        },
        {
          "set": {
            "key": "shown_clues",
            "value": ""
          }
        },
        {
          "set": {
            "key": "clue_valid",
            "value": false
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "roles",
      "label": "announce roles with interception",
      "when": {
        "calc": "interceptor_seat > 0"
      },
      "to": "all",
      "text": "Round {round_number}: Team {enc_team} encrypts. Encryptor: seat {encryptor_seat}. Decoder: seat {decoder_seat}. Interceptor: seat {interceptor_seat}."
    },
    {
      "use": "tell",
      "phase": "roles",
      "label": "announce roles without interception",
      "when": {
        "calc": "interceptor_seat == 0"
      },
      "to": "all",
      "text": "Round {round_number}: Team {enc_team} encrypts. Encryptor: seat {encryptor_seat}. Decoder: seat {decoder_seat}. There is no interception this round."
    },
    {
      "use": "update",
      "phase": "code",
      "label": "draw the code",
      "do": [
        {
          "set": {
            "key": "current_code",
            "value": {
              "calc": "code_list[min(code_count - 1, int(uniform(0, code_count)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == encryptor_seat"
            },
            "key": "my_code",
            "value": {
              "calc": "current_code"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "code",
      "label": "your keywords",
      "mode": "self",
      "to": "acting",
      "fields": [
        "keywords"
      ],
      "text": "Your keywords (numbered 1-4 in list order):"
    },
    {
      "use": "sync",
      "phase": "code",
      "label": "the secret code",
      "mode": "self",
      "to": {
        "where": "you.seat == encryptor_seat"
      },
      "fields": [
        "my_code"
      ],
      "text": "You are the Encryptor. Your secret code this round:"
    },
    {
      "use": "ask",
      "phase": "clues",
      "label": "write three clues",
      "to": {
        "where": "you.seat == encryptor_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 11
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_clues",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You are the Encryptor. Your secret code is {my_code} (digits refer to your keywords numbered 1-4 in list order). Write three clues in code order, separated by ' / ', each at most {clue_max_words} words. Each clue must relate to its keyword by meaning or association; no hints by spelling, letters, letter count, rhyme, or keyword number or position; never use the keyword or a form of it; never repeat a clue your team has used before. An invalid set reveals the code and costs your team 1 Miscommunication."
    },
    {
      "use": "update",
      "phase": "clues",
      "label": "referee check",
      "when": {
        "prose": "Each of the three clues in current_clues relates by meaning or association to the keyword (from the encrypting team's keywords) numbered by its digit of current_code, no clue hints by spelling, letters, letter count, rhyme or keyword number or position, no clue contains its keyword or a form of it, and no clue repeats a clue already in the encrypting team's clue history."
      },
      "do": [
        {
          "set": {
            "key": "clue_valid",
            "value": true
          }
        },
        {
          "set": {
            "key": "shown_clues",
            "value": {
              "calc": "current_clues"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "clues",
      "label": "invalid clue set",
      "when": {
        "calc": "not clue_valid"
      },
      "do": [
        {
          "set": {
            "key": "revealed_code",
            "value": {
              "calc": "current_code"
            }
          }
        },
        {
          "adjust": {
            "key": "a_miscommunications",
            "value": 1,
            "if": {
              "calc": "enc_team == 'A'"
            }
          }
        },
        {
          "adjust": {
            "key": "b_miscommunications",
            "value": 1,
            "if": {
              "calc": "enc_team == 'B'"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "clues",
      "label": "show the clues",
      "when": {
        "calc": "clue_valid"
      },
      "to": "all",
      "text": "Team {enc_team}'s clues, in code order: {shown_clues}"
    },
    {
      "use": "tell",
      "phase": "clues",
      "label": "clues ruled invalid",
      "when": {
        "calc": "not clue_valid"
      },
      "to": "all",
      "text": "The referee ruled Team {enc_team}'s clue set invalid. The code was {revealed_code}. Team {enc_team} gains 1 Miscommunication; no clues are added and no guesses are taken. Tokens - Team A: {a_interceptions} Interceptions, {a_miscommunications} Miscommunications; Team B: {b_interceptions} Interceptions, {b_miscommunications} Miscommunications."
    },
    {
      "use": "poll",
      "phase": "guess",
      "label": "guess the code",
      "when": {
        "calc": "clue_valid"
      },
      "to": {
        "where": "you.seat == decoder_seat or (interceptor_seat > 0 and you.seat == interceptor_seat)"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "code_list"
        }
      },
      "store": "guess",
      "text": "Clues from Team {enc_team}: {shown_clues}. Guess the 3-digit code (Decoder: your own team's code; Interceptor: the rival team's code, using their public clue history). Guesses are secret until both are in."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the guesses",
      "when": {
        "calc": "clue_valid"
      },
      "do": [
        {
          "set": {
            "key": "revealed_code",
            "value": {
              "calc": "current_code"
            }
          }
        },
        {
          "set": {
            "key": "decoder_guess",
            "value": {
              "calc": "([p.guess for p in players if p.seat == decoder_seat] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "interceptor_guess",
            "value": {
              "calc": "([p.guess for p in players if p.seat == interceptor_seat] + [''])[0]"
            }
          }
        },
        {
          "adjust": {
            "key": "a_miscommunications",
            "value": 1,
            "if": {
              "calc": "enc_team == 'A' and decoder_gues
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {my_code} (in `prompt`: 'You are the Encryptor. Your secret code is {my_code} (digits refer to your keywords number'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {my_code} (in `prompt`: 'You are the Encryptor. Your secret code is {my_code} (digits refer to your keywords number'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {my_code} (in `prompt`: 'You are the Encryptor. Your secret code is {my_code} (digits refer to your keywords number'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "decrypto_duel_paired",
    "name": "Decrypto Duel (Paired Rounds)",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Two teams of two send secret three-digit codes through clues about hidden keywords while the rival Guesser tries to intercept."
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
        "initial": "",
        "values": [
          "",
          "A",
          "B"
        ]
      },
      {
        "key": "keywords",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "my_code",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "standing",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guess",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pair_number",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "word_list",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "code_list",
        "visible": "public",
        "type": "list",
        "initial": [
          "1-2-3",
          "1-2-4",
          "1-3-2",
          "1-3-4",
          "1-4-2",
          "1-4-3",
          "2-1-3",
          "2-1-4",
          "2-3-1",
          "2-3-4",
          "2-4-1",
          "2-4-3",
          "3-1-2",
          "3-1-4",
          "3-2-1",
          "3-2-4",
          "3-4-1",
          "3-4-2",
          "4-1-2",
          "4-1-3",
          "4-2-1",
          "4-2-3",
          "4-3-1",
          "4-3-2"
        ]
      },
      {
        "key": "enc_team",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "encryptor_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "decoder_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "interceptor_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_code",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed_code",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "current_clues",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "shown_clues",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clue_valid",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "decoder_guess",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "interceptor_guess",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clue_history_a",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_history_b",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "a_interceptions",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "a_miscommunications",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "b_interceptions",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "b_miscommunications",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
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
        "key": "keywords_per_team",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "word_list_size",
        "visible": "public",
        "type": "number",
        "initial": 120
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "pairs",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "code_length",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "key": "clue_max_words",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "interception_trigger",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "miscommunication_trigger",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_interception_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "trigger_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "teams and tokens",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat <= team_size"
            },
            "key": "team",
            "value": "A"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat > team_size"
            },
            "key": "team",
            "value": "B"
          }
        },
        {
          "set": {
            "key": "a_interceptions",
            "value": 0
          }
        },
        {
          "set": {
            "key": "a_miscommunications",
            "value": 0
          }
        },
        {
          "set": {
            "key": "b_interceptions",
            "value": 0
          }
        },
        {
          "set": {
            "key": "b_miscommunications",
            "value": 0
          }
        },
        {
          "set": {
            "key": "clue_history_a",
            "value": []
          }
        },
        {
          "set": {
            "key": "clue_history_b",
            "value": []
          }
        }
      ],
      "text": "Seats 1 and 2 are Team A (A1, A2). Seats 3 and 4 are Team B (B1, B2). All tokens start at 0."
    },
    {
      "use": "update",
      "label": "the word list",
      "do": [
        {
          "set": {
            "key": "word_list",
            "value": [
              "apple", "anchor", "arrow", "axe", "balloon", "banana", "barrel", "basket", "bell", "bicycle",
              "blanket", "boat", "book", "bottle", "bowl", "bread", "brick", "bridge", "broom", "bucket",
              "butterfly", "cactus", "camera", "candle", "car", "carrot", "castle", "chair", "cheese", "clock",
              "cloud", "coin", "comb", "compass", "crown", "cup", "curtain", "desk", "diamond", "dog",
              "door", "drum", "eagle", "egg", "envelope", "feather", "fence", "flag", "flower", "fork",
              "fountain", "frog", "glove", "guitar", "hammer", "hat", "helmet", "honey", "horse", "island",
              "jacket", "kettle", "key", "kite", "ladder", "lamp", "leaf", "lemon", "lighthouse", "lion",
              "lock", "map", "mirror", "moon", "mountain", "mushroom", "nail", "needle", "nest", "ocean",
              "onion", "orange", "owl", "paint", "pencil", "piano", "pillow", "pipe", "pizza", "planet",
              "pumpkin", "rabbit", "river", "robot", "rocket", "rope", "saddle", "sandwich", "scissors", "shark",
              "sheep", "shell", "shield", "ship", "shoe", "snake", "sock", "spoon", "star", "sword",
              "table", "tent", "tiger", "tomato", "tower", "train", "tree", "trumpet", "umbrella", "volcano"
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal Team A keywords",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
        }
      ]
    },
    {
      "use": "update",
      "label": "deal Team B keywords",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
              "calc": "word_list[min(len(word_list) - 1, int(uniform(0, len(word_list))))]"
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
      "use": "sync",
      "label": "your keywords",
      "mode": "self",
      "to": "all",
      "fields": [
        "team",
        "keywords"
      ],
      "text": "Your team and your keywords (numbered 1-4 in list order):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roles",
      "label": "the round's roles",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "pair_number",
            "value": {
              "calc": "int((round_number + 1) / 2)"
            }
          }
        },
        {
          "set": {
            "key": "enc_team",
            "value": {
              "calc": "'A' if pair_number % 2 == round_number % 2 else 'B'"
            }
          }
        },
        {
          "set": {
            "key": "encryptor_seat",
            "value": {
              "calc": "((1 if enc_team == 'A' else 3) if pair_number % 2 == 1 else (2 if enc_team == 'A' else 4))"
            }
          }
        },
        {
          "set": {
            "key": "decoder_seat",
            "value": {
              "calc": "((2 if enc_team == 'A' else 4) if pair_number % 2 == 1 else (1 if enc_team == 'A' else 3))"
            }
          }
        },
        {
          "set": {
            "key": "interceptor_seat",
            "value": {
              "calc": "0 if round_number < first_interception_round else ((4 if enc_team == 'A' else 2) if pair_number % 2 == 1 else (3 if enc_team == 'A' else 1))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "my_code",
            "value": ""
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
            "key": "revealed_code",
            "value": ""
          }
        },
        {
          "set": {
            "key": "decoder_guess",
            "value": ""
          }
        },
        {
          "set": {
            "key": "interceptor_guess",
            "value": ""
          }
        },
        {
          "set": {
            "key": "current_clues",
            "value": ""
          }
        },
        {
          "set": {
            "key": "shown_clues",
            "value": ""
          }
        },
        {
          "set": {
            "key": "clue_valid",
            "value": false
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "roles",
      "label": "announce roles with interception",
      "when": {
        "calc": "interceptor_seat > 0"
      },
      "to": "all",
      "text": "Round {round_number}: Team {enc_team} encrypts. Encryptor: seat {encryptor_seat}. Decoder: seat {decoder_seat}. Interceptor: seat {interceptor_seat}."
    },
    {
      "use": "tell",
      "phase": "roles",
      "label": "announce roles without interception",
      "when": {
        "calc": "interceptor_seat == 0"
      },
      "to": "all",
      "text": "Round {round_number}: Team {enc_team} encrypts. Encryptor: seat {encryptor_seat}. Decoder: seat {decoder_seat}. There is no interception this round."
    },
    {
      "use": "update",
      "phase": "code",
      "label": "draw the code",
      "do": [
        {
          "set": {
            "key": "current_code",
            "value": {
              "calc": "code_list[min(code_count - 1, int(uniform(0, code_count)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == encryptor_seat"
            },
            "key": "my_code",
            "value": {
              "calc": "current_code"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "code",
      "label": "your keywords",
      "mode": "self",
      "to": "acting",
      "fields": [
        "keywords"
      ],
      "text": "Your keywords (numbered 1-4 in list order):"
    },
    {
      "use": "sync",
      "phase": "code",
      "label": "the secret code",
      "mode": "self",
      "to": {
        "where": "you.seat == encryptor_seat"
      },
      "fields": [
        "my_code"
      ],
      "text": "You are the Encryptor. Your secret code this round:"
    },
    {
      "use": "ask",
      "phase": "clues",
      "label": "write three clues",
      "to": {
        "where": "you.seat == encryptor_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 11
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_clues",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You are the Encryptor. Your secret code was just sent to you privately as my_code (its digits refer to your keywords numbered 1-4 in list order). Write three clues in code order, separated by ' / ', each at most {clue_max_words} words. Each clue must relate to its keyword by meaning or association; no hints by spelling, letters, letter count, rhyme, or keyword number or position; never use the keyword or a form of it; never repeat a clue your team has used before. An invalid set reveals the code and costs your team 1 Miscommunication."
    },
    {
      "use": "update",
      "phase": "clues",
      "label": "referee check",
      "when": {
        "prose": "Each of the three clues in current_clues relates by meaning or association to the keyword (from the encrypting team's keywords) numbered by its digit of current_code, no clue hints by spelling, letters, letter count, rhyme or keyword number or position, no clue contains its keyword or a form of it, and no clue repeats a clue already in the encrypting team's clue history."
      },
      "do": [
        {
          "set": {
            "key": "clue_valid",
            "value": true
          }
        },
        {
          "set": {
            "key": "shown_clues",
            "value": {
              "calc": "current_clues"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "clues",
      "label": "invalid clue set",
      "when": {
        "calc": "not clue_valid"
      },
      "do": [
        {
          "set": {
            "key": "revealed_code",
            "value": {
              "calc": "current_code"
            }
          }
        },
        {
          "adjust": {
            "key": "a_miscommunications",
            "value": 1,
            "if": {
              "calc": "enc_team == 'A'"
            }
          }
        },
        {
          "adjust": {
            "key": "b_miscommunications",
            "value": 1,
            "if": {
              "calc": "enc_team == 'B'"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "clues",
      "label": "show the clues",
      "when": {
        "calc": "clue_valid"
      },
      "to": "all",
      "text": "Team {enc_team}'s clues, in code order: {shown_clues}"
    },
    {
      "use": "tell",
      "phase": "clues",
      "label": "clues ruled invalid",
      "when": {
        "calc": "not clue_valid"
      },
      "to": "all",
      "text": "The referee ruled Team {enc_team}'s clue set invalid. The code was {revealed_code}. Team {enc_team} gains 1 Miscommunication; no clues are added and no guesses are taken. Tokens - Team A: {a_interceptions} Interceptions, {a_miscommunications} Miscommunications; Team B: {b_interceptions} Interceptions, {b_miscommunications} Miscommunications."
    },
    {
      "use": "poll",
      "phase": "guess",
      "label": "guess the code",
      "when": {
        "calc": "clue_valid"
      },
      "to": {
        "where": "you.seat == decoder_seat or (interceptor_seat > 0 and you.seat == interceptor_seat)"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "code_list"
        }
      },
      "store": "guess",
      "text": "Clues from Team {enc_team}: {shown_clues}. Guess the 3-digit code (Decoder: your own team's code; Interceptor: the rival team's code, using their public clue history). Guesses are secret until both are in."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the guesses",
      "when": {
        "calc": "clue_valid"
      },
      "do": [
        {
          "set": {
            "key": "revealed_code",
            "value": {
              "calc": "current_code"
            }
          }
        },
        {
          "set": {
            "key": "decoder_guess",
            "value": {
              "calc": "([p.guess for p in players if p.seat == decoder_seat] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "interceptor_guess",
            "value": {
              "calc": "([p.guess for p in players if p.seat == interceptor_seat] + [''])[0]"
            }
          }
        },
        {
          "adjust": {
            "key": "a_miscommunications",
            "value": 1,
            "if": {
              "calc": "enc_team == 'A' and decoder_guess != current_code"
            }
          }
        },
        {
          "adjust": {
            "key": "b_miscommunications",
            "value": 1,
            "if": {
              "calc": "enc_team == 'B' and decoder_guess != current_code"
            }
          }
        },
        {
          "adjust": {
            "key": "b_interceptions",
            "value": 1,
            "if": {
              "calc": "enc_team == 'A' and interceptor_seat > 0 and interceptor_guess == current_code"
            }
          }
        },
        {
          "adjust": {
            "key": "a_interceptions",
            "value": 1,
            "if": {
              "calc": "enc_team == 'B' and interceptor_seat > 0 and interceptor_guess == current_code"
            }
          }
        },
        {
          "append": {
            "key": "clue_history_a",
            "value": {
              "calc": "current_code + ' -> ' + current_clues"
            },
            "if": {
              "calc": "enc_team == 'A'"
            }
          }
        },
        {
          "append": {
            "key": "clue_history_b",
            "value": {
              "calc": "current_code + ' -> ' + current_clues"
            },
            "if": {
              "calc": "enc_team == 'B'"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "the reveal",
      "when": {
        "calc": "clue_valid"
      },
      "to": "all",
      "text": "The code was {revealed_code}. Decoder guessed {decoder_guess}; Interceptor guessed {interceptor_guess} (blank when there was no Interceptor). Tokens - Team A: {a_interceptions} Interceptions, {a_miscommunications} Miscommunications; Team B: {b_interceptions} Interceptions, {b_miscommunications} Miscommunications."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "standings at the end of the pair",
      "when": {
        "calc": "round_number % 2 == 0"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.team == 'A'"
            },
            "key": "standing",
            "value": {
              "calc": "((1 if a_interceptions >= interception_trigger or b_miscommunications >= miscommunication_trigger else 0) - (1 if b_interceptions >= interception_trigger or a_miscommunications >= miscommunication_trigger else 0)) * trigger_weight + a_interceptions - a_miscommunications"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.team == 'B'"
            },
            "key": "standing",
            "value": {
              "calc": "((1 if b_interceptions >= interception_trigger or a_miscommunications >= miscommunication_trigger else 0) - (1 if a_interceptions >= interception_trigger or b_miscommunications >= miscommunication_trigger else 0)) * trigger_weight + b_interceptions - b_miscommunications"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "end of the pair",
      "when": {
        "calc": "round_number % 2 == 0"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number % 2 == 0 and (a_interceptions >= interception_trigger or b_miscommunications >= miscommunication_trigger or b_interceptions >= interception_trigger or a_miscommunications >= miscommunication_trigger or round_number >= max_rounds)"
      },
      "rank_by": "you.standing",
      "text": "Winner: {result}. Team A: {a_interceptions} Interceptions, {a_miscommunications} Miscommunications; Team B: {b_interceptions} Interceptions, {b_miscommunications} Miscommunications (standings: seat 1 {players[0].standing}, seat 2 {players[1].standing}, seat 3 {players[2].standing}, seat 4 {players[3].standing})."
    }
  },
  "limits": {
    "rounds": 16,
    "rounds_max": 16,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "SETUP. {player_count} players: seats 1 and 2 are Team A (A1, A2); seats 3 and 4 are Team B (B1, B2). Each team is dealt {keywords_per_team} different keywords from a fixed list of {word_list_size} common concrete nouns; no word is given to both teams. A team's keywords are numbered 1 to 4 and are shown privately to both its members, never to the other team. A public clue history shows each team's past clues, tagged with the code they clued (columns 1-4). Each team starts with 0 Interceptions and 0 Miscommunications; token counts are always public.\n\nPAIRS AND ROLES. Up to {max_rounds} rounds, grouped into {pairs} pairs (pair 1 = rounds 1-2, pair 2 = rounds 3-4, ...). In each pair each team encrypts exactly once. In odd pairs Team A encrypts first and Team B second; in even pairs Team B first and Team A second. In odd pairs A1 and B1 are Encryptors and A2 and B2 are Guessers; in even pairs A2 and B2 are Encryptors and A1 and B1 are Guessers. In a round, the Encryptor is the encrypting team's Encryptor, the Decoder is that team's Guesser, the Interceptor is the other team's Guesser, and the other team's Encryptor only watches. There is no Interceptor in rounds 1 and 2; interception starts in round {first_interception_round}.\n\nEACH ROUND. 1) The round, encrypting team, Encryptor and Decoder are announced, and the Interceptor (or that there is no interception). 2) A code is drawn uniformly at random from the {code_count} ordered sequences of {code_length} different digits from 1 to {code_digit_max} (for example 3-1-4) and shown privately to the Encryptor only. 3) The Encryptor writes three clues, one per digit, in code order, separated by ' / ', each at most {clue_max_words} words; each clue points to the keyword with that number. 4) A referee checks the set. It is valid only if every clue relates to its keyword by meaning or association; no clue hints by spelling, letters, letter count, rhyme, or keyword number or position; no clue contains its keyword or a form of it; and no clue repeats any clue this team has used before. If the set is INVALID: the code is revealed to everyone, the encrypting team gains 1 Miscommunication, the clues are not added to the history, no guesses are taken, and the round goes to the end check. If the set is VALID: 5) the clues are shown to all players; 6) at the same moment the Decoder and the Interceptor (if any) each privately submit a guessed code from the 24 codes, and neither sees the other's guess until both are in; 7) the true code and the guesses are revealed. If the Decoder's guess differs from the true code in any digit, the encrypting team gains 1 Miscommunication; if it matches, nothing is gained or lost. If the Interceptor's guess equals the true code exactly, the Interceptor's team gains 1 Interception; otherwise nothing happens. The clues are added to the encrypting team's public history.\n\nEND CHECK, only after even-numbered rounds (the end of a pair); after odd rounds play always continues. A team TRIGGERS if it has {interception_trigger} or more Interceptions, or if the other team has {miscommunication_trigger} or more Miscommunications. If exactly one team triggers, it wins and the game ends. If both teams trigger, apply the comparison rule and the game ends. If neither triggers and this was round {max_rounds}, apply the comparison rule. Otherwise play continues.\n\nCOMPARISON RULE. Each team's value is its Interceptions minus its Miscommunications. The higher value wins; equal values are a draw and all four players share the win. Both members of a team share its result.\n\nCOMMUNICATION. There is no talk phase. Players communicate only through clues; teammates may not message each other."
}
```
````
