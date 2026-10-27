# 09 coder

- time: 2026-10-27T17:59:22+00:00 (80.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 5b1a1ad0e587c401, reply sha256 40ff4c334c214831

## Sent

````
# Task: write the XColos game file for "Tides of Madness: Obsession"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK. 30 cards in 5 suits: Ruins, Idols, Deep, Stars, Shore. Each suit has 6 cards: 4 plain and 2 with a madness icon (written e.g. 'Deep*').

STRUCTURE. The game has 15 rounds in 3 tides of 5 rounds each: rounds 1-5 are tide 1, rounds 6-10 tide 2, rounds 11-15 tide 3. Each player has a score (starting at 0) and a madness total (starting at 0).

START OF EACH TIDE (rounds 1, 6, 11).
- All 30 cards are shuffled, minus any cards currently retained by players.
- Each player is dealt a private hand of 5. The rest are unused this tide.
- Each player sees only their own hand.
- At the same moment as their first pick, each player secretly chooses one suit as their Obsession for this tide. It is hidden from the opponent until the tide is scored.

EACH ROUND.
- Both players simultaneously choose one card from the hand they currently hold and place it face down in their tableau for this tide.
- Then the two players swap their remaining hands.
- Hands therefore go 5, 4, 3, 2, 1 cards, and the pick in the fifth round of a tide is forced.
- A player always knows the cards they themselves drafted and the hands they saw.

END OF EACH TIDE (rounds 5, 10, 15), in order:
1. Reveal. Both tableaus and both Obsessions are revealed. A player's tide tableau is the 5 cards drafted this tide plus all cards they have retained from earlier tides.
2. Madness. Each player counts madness icons in their tide tableau (retained cards count every tide they are in) and adds that number to their madness total.
3. Set points. For each suit, count the cards of that suit in the tableau: 0 cards = 0 points, 1 = 1, 2 = 3, 3 = 6, 4 or more = 10. Points for the player's Obsession suit are doubled.
4. Extra points. Add +1 point per madness card in the tableau. Add +4 points if the tableau contains at least 4 different suits.
5. Madness bonus. The player with strictly more madness icons in their tide tableau privately chooses one: gain 4 points, or reduce their madness total by 1. If the counts are equal, nobody gets the bonus.
6. Madness check. If a player's madness total is 9 or more, the game ends immediately and that player loses. If both are at 9 or more, the one with the higher madness total loses. If they are equal, the game is a draw.
7. Retain (tides 1 and 2 only). Each player simultaneously chooses one card drafted this tide to retain permanently. It stays face up beside them and is part of every later tide tableau. All other drafted cards return to the deck.

END OF GAME. After the tide 3 scoring, if no one has been eliminated, the winner is decided as stated in the objective.

How the winner is decided: A player loses immediately if their madness total reaches 9 or more at a tide's madness check. If both reach it, the higher madness total loses, and equal totals are a draw. Otherwise, after tide 3 the higher score wins. If scores are tied, the lower madness total wins. If that is also tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Tides of Madness: Obsession (2 to 2 players, best with 2)

A two-player card draft over 3 tides of 5 rounds: pick a card, swap hands, score suit sets doubled for a secret Obsession suit, and avoid reaching 9 madness.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Victory points so far.
  - each player: madness (number, starts 0); everyone sees it. Madness total. Reaching 9 or more at a madness check loses the game.
  - each player: hand (list, starts []); only its owner sees it. The cards the player currently holds to draft from. Only the owner sees it.
  - each player: tableau (list, starts []); only its owner sees it. Cards drafted face down this tide. Revealed by announcement at the end of the tide.
  - each player: obsession (text, starts ''); only its owner sees it. The secret Obsession suit for this tide. Revealed by announcement at the end of the tide.
  - each player: retained (list, starts []); everyone sees it. Cards kept face up from earlier tides. They are part of every later tide tableau.
  - each player: tide_icons (number, starts 0); everyone sees it. Madness icons in this tide's tableau plus retained cards. Computed at the end of the tide.
  - each player: tide_points (number, starts 0); everyone sees it. Points scored at this tide's scoring, before the madness bonus.
  - each player: lost (number, starts 0); everyone sees it. 1 if this player loses at a madness check, else 0.
  - the table: round (number, starts 0); everyone sees it. Current round, 1 to 15.
  - the table: tide (number, starts 0); everyone sees it. Current tide, 1 to 3. Equals ceil(round / 5).
  - the table: round_in_tide (number, starts 0); everyone sees it. Round within the tide, 1 to 5. Equals (round - 1) mod 5 + 1.
  - the table: full_deck (list, starts ['Ruins-1', 'Ruins-2', 'Ruins-3', 'Ruins-4', 'Ruins*-1', 'Ruins*-2', 'Idols-1', 'Idols-2', 'Idols-3', 'Idols-4', 'Idols*-1', 'Idols*-2', 'Deep-1', 'Deep-2', 'Deep-3', 'Deep-4', 'Deep*-1', 'Deep*-2', 'Stars-1', 'Stars-2', 'Stars-3', 'Stars-4', 'Stars*-1', 'Stars*-2', 'Shore-1', 'Shore-2', 'Shore-3', 'Shore-4', 'Shore*-1', 'Shore*-2']); everyone sees it. The full list of 30 cards, used to rebuild the deck each tide. A '*' marks a madness icon.
  - the table: deck (list, starts []); hidden from all players. This tide's shuffled deck: the full deck minus all retained cards. Undealt cards are unused this tide.
  - the table: bonus_seat (number, starts 0); everyone sees it. Seat with strictly more tide_icons this tide (1 or 2), or 0 if the counts are equal.
  - the table: madness_end (number, starts 0); everyone sees it. 1 if the game ended at a madness check, else 0.
  - parameters, each kept as a table attribute: deck_size = 30, suits = 5, cards_per_suit = 6, plain_cards_per_suit = 4, madness_cards_per_suit = 2, total_rounds = 15, tides = 3, rounds_per_tide = 5, hand_size = 5, set_points_0 = 0, set_points_1 = 1, set_points_2 = 3, set_points_3 = 6, set_points_4_or_more = 10, obsession_multiplier = 2, points_per_madness_card = 1, diversity_suits_needed = 4, diversity_bonus = 4, madness_bonus_points = 4, madness_bonus_reduction = 1, madness_loss_threshold = 9, cards_retained_per_tide = 1, retain_tides = 2, starting_score = 0, starting_madness = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 and seat 2 each start with score 0, madness 0, and empty hand, tableau, retained and obsession.
  2. The table's full_deck holds the 30 cards: in each of the 5 suits (Ruins, Idols, Deep, Stars, Shore), 4 plain cards and 2 madness cards marked '*'.
  3. round starts at 0. The deck is built and dealt at the start of each tide, inside the round steps.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; tide = ceil(round / 5); round_in_tide = (round - 1) mod 5 + 1. Announce the round and tide.
  2. [update] all players. What happens: When round_in_tide == 1: deck = full_deck minus every card in either player's retained list; each player's hand = [] and tableau = []; then deal 5 cards to each player's hand. Each card is a random draw removed from deck and appended to hand. The cards left in deck are unused this tide.
  3. [sync] all players. What happens: Each player privately sees their own hand, tableau, obsession and both retained lists.
  4. [poll] all players answers: one of: Ruins, Idols, Deep, Stars, Shore. What happens: When round_in_tide == 1: set you.obsession to the chosen suit. It stays hidden from the opponent (ally) until the tide's reveal.
  5. [poll] all players answers: one card from your own hand. What happens: Simultaneously, each player removes the chosen card from you.hand and appends it to you.tableau, face down. When round_in_tide == 5 the hand has 1 card, so the pick is forced.
  6. [update] all players. What happens: When round_in_tide < 5: swap hands, so seat 1's hand becomes seat 2's old hand and seat 2's hand becomes seat 1's old hand.
  7. [tell] all players. What happens: When round_in_tide == 5: reveal to everyone each player's tableau, retained cards and obsession.
  8. [update] all players. What happens: When round_in_tide == 5, for each player, with T = tableau + retained: tide_icons = number of cards in T with '*'; madness += tide_icons. For each suit, n = cards of that suit in T and set_pts = 0 if n=0, 1 if n=1, 3 if n=2, 6 if n=3, 10 if n>=4, doubled if the suit equals obsession. tide_points = sum of set_pts + tide_icons * 1 + (4 if the number of distinct suits in T >= 4 else 0). score += tide_points. Then bonus_seat = 1 if seat 1's tide_icons > seat 2's, 2 if seat 2's > seat 1's, else 0. Announce each player's tide_points, score and madness.
  9. [ask] the seat equal to bonus_seat (skipped if bonus_seat == 0) answers: one of: gain_4_points, reduce_madness_1. What happens: When round_in_tide == 5 and bonus_seat > 0: the bonus seat chooses privately. gain_4_points: you.score += 4. reduce_madness_1: you.madness -= 1.
  10. [update] all players. What happens: When round_in_tide == 5, madness check. If exactly one player has madness >= 9, that player's lost = 1 and madness_end = 1. If both have madness >= 9: the one with the higher madness gets lost = 1; if equal, both keep lost = 0 (a draw); madness_end = 1 either way. Announce the result.
  11. [check] all players. What happens: End the game if madness_end == 1 or (round == 15 and round_in_tide == 5); otherwise continue.
  12. [poll] all players answers: one card from your own tableau (the cards drafted this tide). What happens: When round_in_tide == 5 and tide < 3: simultaneously, each player picks one card to retain permanently.
  13. [update] all players. What happens: When round_in_tide == 5 and tide < 3: append each player's chosen card to you.retained, face up and public; set tableau = [] and obsession = ''. All other drafted cards go back to the pool used to rebuild the deck next tide. Announce the retained cards.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 30 cards: 5 suits (Ruins, Idols, Deep, Stars, Shore) of 6 cards each, 4 plain and 2 with a madness icon '*'.
  R2. The game has 15 rounds in 3 tides: rounds 1-5 are tide 1, rounds 6-10 tide 2, rounds 11-15 tide 3.
  R3. When a tide starts (rounds 1, 6, 11), then the deck is the 30 cards minus all retained cards, and each player is dealt a private hand of 5 drawn from it; the rest are unused that tide.
  R4. When a tide starts, then each player secretly chooses one of the 5 suits as their Obsession, hidden from the opponent until the tide is scored.
  R5. When a round is played, then both players simultaneously move one card from their own hand to their tableau, face down.
  R6. When the picks of rounds 1-4 of a tide are made, then the two players swap their remaining hands, so hands hold 5, 4, 3, 2, 1 cards.
  R7. When the fifth round of a tide is played, then each player's hand has exactly 1 card and that card is the forced pick.
  R8. When a tide ends (rounds 5, 10, 15), then both tableaus, retained cards and Obsessions are revealed to both players.
  R9. When a tide ends, then each player adds the number of '*' cards among their 5 drafted cards plus retained cards to their madness total.
  R10. When a tide ends, then each suit in a player's tide tableau scores 0/1/3/6/10 points for 0/1/2/3/4-or-more cards.
  R11. When a suit is the player's Obsession for that tide, then its set points are doubled (e.g., 3 cards score 12).
  R12. When a tide ends, then a player scores +1 point per madness card in their tide tableau.
  R13. When a player's tide tableau contains at least 4 different suits, then that player scores +4 points.
  R14. When one player has strictly more madness icons than the other in their tide tableau, then that player privately chooses +4 points or madness total -1.
  R15. When both players have equal madness icons in their tide tableaus, then nobody gets the madness bonus.
  R16. When, after the madness bonus, exactly one player has madness total 9 or more, then the game ends immediately and that player loses.
  R17. When both players have madness 9 or more at a madness check, then the game ends and the one with the higher madness total loses; equal totals are a draw.
  R18. When tide 1 or tide 2 ends without a madness loss, then each player simultaneously chooses 1 card drafted that tide to retain face up permanently, and the other drafted cards return to the deck.
  R19. When a card is retained, then it counts in every later tide tableau for set points, madness icons, the +1 per madness card and the 4-suit bonus.
  R20. When tide 3 ends, then no card is retained.
  R21. When tide 3 is scored and no one lost to madness, then the higher score wins; on tied scores the lower madness total wins; if both are tied, the game is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Obsession choice (round 1 of each tide) | asked: both seats | options: Ruins, Idols, Deep, Stars, Shore
  - Draft pick (every round) | asked: both seats | options: each card currently in the seat's own hand (5, 4, 3, 2 or 1 options; in round 5 of a tide only the single remaining card)
  - Madness bonus (end of each tide) | asked: only the seat with strictly more tide_icons; nobody if equal | options: gain_4_points, reduce_madness_1
  - Retain choice (end of tides 1 and 2 only, if the game continues) | asked: both seats | options: each of the 5 cards the seat drafted this tide (its tableau, not earlier retained cards)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: madness_end == 1 or (round == 15 and round_in_tide == 5)
  - each player's standing: madness_end * (1 - you.lost) * 1000000 + (1 - madness_end) * (you.score * 100 + (99 - you.madness)) (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: If the game ended at a madness check, the player who did not lose wins; if both reached 9 or more with equal madness totals, both rank level and the game is a draw. Otherwise, after tide 3 the higher score wins; on tied scores the lower madness total wins; if both are tied, the game is a draw (shared win).
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

- each player: `score` (number, visible: public, starts 0): Victory points so far.
- each player: `madness` (number, visible: public, starts 0): Madness total. Reaching 9 or more at a madness check loses the game.
- each player: `retained` (list, visible: public, starts []): Cards kept face up from earlier tides. They are part of every later tide tableau.
- the table: `round` (number, visible: public, starts 0): Current round, 1 to 15.
- the table: `madness_end` (number, visible: public, starts 0): 1 if the game ended at a madness check, else 0.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 30, suits = 5, cards_per_suit = 6, plain_cards_per_suit = 4, madness_cards_per_suit = 2, total_rounds = 15, tides = 3, rounds_per_tide = 5, hand_size = 5, set_points_0 = 0, set_points_1 = 1, set_points_2 = 3, set_points_3 = 6, set_points_4_or_more = 10, obsession_multiplier = 2, points_per_madness_card = 1, diversity_suits_needed = 4, diversity_bonus = 4, madness_bonus_points = 4, madness_bonus_reduction = 1, madness_loss_threshold = 9, cards_retained_per_tide = 1, retain_tides = 2, starting_score = 0, starting_madness = 0
- the game ends with ONE ending whose `rank_by` is `madness_end * (1 - you.lost) * 1000000 + (1 - madness_end) * (you.score * 100 + (99 - you.madness))`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "tides_of_madness_obsession",
    "name": "Tides of Madness: Obsession",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "A two-player card draft over 3 tides of 5 rounds: pick a card, swap hands, score suit sets doubled for a secret Obsession suit, and stay below 9 madness."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "madness",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "tableau",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "obsession",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "retained",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "tide_icons",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tide_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lost",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "drafted",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "keep",
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
        "initial": 0
      },
      {
        "key": "tide",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_in_tide",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "full_deck",
        "visible": "public",
        "type": "list",
        "initial": [
          "Ruins-1",
          "Ruins-2",
          "Ruins-3",
          "Ruins-4",
          "Ruins*-1",
          "Ruins*-2",
          "Idols-1",
          "Idols-2",
          "Idols-3",
          "Idols-4",
          "Idols*-1",
          "Idols*-2",
          "Deep-1",
          "Deep-2",
          "Deep-3",
          "Deep-4",
          "Deep*-1",
          "Deep*-2",
          "Stars-1",
          "Stars-2",
          "Stars-3",
          "Stars-4",
          "Stars*-1",
          "Stars*-2",
          "Shore-1",
          "Shore-2",
          "Shore-3",
          "Shore-4",
          "Shore*-1",
          "Shore*-2"
        ]
      },
      {
        "key": "suit_list",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ruins",
          "Idols",
          "Deep",
          "Stars",
          "Shore"
        ]
      },
      {
        "key": "deck",
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
        "key": "swap_tmp",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "bonus_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "madness_end",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reveal_tableau_1",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reveal_tableau_2",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reveal_obsession_1",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "reveal_obsession_2",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "plain_cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "madness_cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "tides",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_tide",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "set_points_0",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "set_points_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_points_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "set_points_3",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "set_points_4_or_more",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "obsession_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "points_per_madness_card",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "diversity_suits_needed",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "diversity_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "madness_bonus_points",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "madness_bonus_reduction",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "madness_loss_threshold",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_retained_per_tide",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "retain_tides",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_madness",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "madness",
            "value": {
              "calc": "starting_madness"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tableau",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "retained",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "obsession",
            "value": ""
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "madness_end",
            "value": 0
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
        "score",
        "madness"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "round",
      "label": "the next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "tide",
            "value": {
              "calc": "int((round - 1) / rounds_per_tide) + 1"
            }
          }
        },
        {
          "set": {
            "key": "round_in_tide",
            "value": {
              "calc": "round - rounds_per_tide * (tide - 1)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "drafted",
            "value": ""
          }
        }
      ],
      "text": "Round {round} of {total_rounds}: tide {tide}, round {round_in_tide} of {rounds_per_tide} in this tide."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "the tide deal",
      "when": {
        "calc": "round_in_tide == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in full_deck if not any(c in p.retained for p in players)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tableau",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        }
      ],
      "text": "Tide {tide} begins. The deck is shuffled without the retained cards and each player is dealt a private hand of {hand_size}."
    },
    {
      "use": "sync",
      "phase": "round",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "tableau",
        "retained",
        "score",
        "madness"
      ],
      "text": "Your hand, tableau and retained cards:"
    },
    {
      "use": "poll",
      "phase": "draft",
      "label": "the obsession",
      "when": {
        "calc": "round_in_tide == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Ruins",
          "Idols",
          "Deep",
          "Stars",
          "Shore"
        ]
      },
      "store": "obsession",
      "text": "Secretly choose one suit as your Obsession for tide {tide}. Its set points are doubled at the end of the tide. Your opponent will not see it until the tide is scored."
    },
    {
      "use": "poll",
      "phase": "draft",
      "label": "the draft pick",
      "when": {
        "calc": "round_in_tide < rounds_per_tide"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "drafted",
      "text": "Choose one card from your hand to place face down in your tableau. Afterwards the two of you swap your remaining hands."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "place the cards and swap",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "drafted",
            "value": {
              "calc": "you.hand[0]"
            },
            "if": {
              "calc": "round_in_tide == rounds_per_tide"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.drafted"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "tableau",
            "value": {
              "calc": "you.drafted"
            }
          }
        },
        {
          "set": {
            "key": "swap_tmp",
            "value": {
              "calc": "players[0].hand"
            },
            "if": {
              "calc": "round_in_tide < rounds_per_tide"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "players[1].hand"
            },
            "if": {
              "calc": "round_in_tide < rounds_per_tide"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "swap_tmp"
            },
            "if": {
              "calc": "round_in_tide < rounds_per_tide"
            }
          }
        }
      ],
      "text": "Both players place a card face down. Before round 5 of a tide the remaining hands are swapped; in round 5 the last card is placed automatically."
    },
    {
      "use": "update",
      "phase": "tide end",
      "label": "the reveal",
      "when": {
        "calc": "round_in_tide == rounds_per_tide"
      },
      "do": [
        {
          "set": {
            "key": "reveal_tableau_1",
            "value": {
              "calc": "players[0].tableau"
            }
          }
        },
        {
          "set": {
            "key": "reveal_tableau_2",
            "value": {
              "calc": "players[1].tableau"
            }
          }
        },
        {
          "set": {
            "key": "reveal_obsession_1",
            "value": {
              "calc": "players[0].obsession"
            }
          }
        },
        {
          "set": {
            "key": "reveal_obsession_2",
            "value": {
              "calc": "players[1].obsession"
            }
          }
        }
      ],
      "text": "Tide {tide} reveal. Seat 1 drafted {reveal_tableau_1}, Obsession {reveal_obsession_1}. Seat 2 drafted {reveal_tableau_2}, Obsession {reveal_obsession_2}. Retained cards also count: seat 1 {players[0].retained}, seat 2 {players[1].retained}."
    },
    {
      "use": "update",
      "phase": "tide end",
      "label": "the tide scoring",
      "when": {
        "calc": "round_in_tide == rounds_per_tide"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "tide_icons",
            "value": {
              "calc": "count('*' in c for c in you.tableau + you.retained)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "madness",
            "value": {
              "calc": "you.tide_icons"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tide_points",
            "value": {
              "calc": "sum([[set_points_0, set_points_1, set_points_2, set_points_3, set_points_4_or_more][min(count(s in c for c in you.tableau + you.retained), 4)] * (obsession_multiplier if s == you.obsession else 1) for s in suit_list]) + you.tide_icons * points_per_madness_card + (diversity_bonus if count(any(s in c for c in you.tableau + you.retained) for s in suit_list) >= diversity_suits_needed else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.tide_points"
            }
          }
        },
        {
          "set": {
            "key": "bonus_seat",
            "value": {
              "calc": "1 if players[0].tide_icons > players[1].tide_icons else (2 if players[1].tide_icons > players[0].tide_icons else 0)"
            }
          }
        }
      ],
      "text": "Tide {tide} scored. Seat 1: {players[0].tide_icons} madness icons, {players[0].tide_points} points, score {players[0].score}, madness {players[0].madness}. Seat 2: {players[1].tide_icons} madness icons, {players[1].tide_points} points, score {players[1].score}, madness {players[1].madness}. Madness bonus goes to seat {bonus_seat} (0 means nobody)."
    },
    {
      "use": "ask",
      "phase": "tide end",
      "label": "the madness bonus",
      "when": {
        "calc": "round_in_tide == rounds_per_tide and bonus_seat > 0"
      },
      "to": {
        "where": "you.seat == bonus_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "gain_4_points",
          "reduce_madness_1"
        ]
      },
      "verify": {
        "bind": "bonus"
      },
      "text": "You had strictly more madness icons this tide. Choose privately: gain_4_points (+{madness_bonus_points} score) or reduce_madness_1 (madness total -{madness_bonus_reduction})."
    },
    {
      "use": "update",
      "phase": "tide end",
      "label": "bonus and madness check",
      "when": {
        "calc": "round_in_tide == rounds_per_tide"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "bonus_seat"
            },
            "key": "score",
            "value": {
              "calc": "madness_bonus_points"
            },
            "if": {
              "calc": "bonus_seat > 0 and $bonus == 'gain_4_points'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "bonus_seat"
            },
            "key": "madness",
            "value": {
              "calc": "max(0, players[bonus_seat - 1].madness - madness_bonus_reduction)"
            },
            "if": {
              "calc": "bonus_seat > 0 and $bonus == 'reduce_madness_1'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "lost",
            "value": {
              "calc": "1 if you.madness >= madness_loss_threshold and all(p.madness < you.madness for p in players if p.seat != you.seat) else 0"
            }
          }
        },
        {
          "set": {
            "key": "madness_end",
            "value": {
              "calc": "1 if any(p.madness >= madness_loss_threshold for p in players) else 0"
            }
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.lost == 1"
            },
            "to": "out",
            "text": "Seat {player} has gone mad and loses."
          }
  
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `suit_list` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "tides_of_madness_obsession",
    "name": "Tides of Madness: Obsession",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "A two-player card draft over 3 tides of 5 rounds: pick a card, swap hands, score suit sets doubled for a secret Obsession suit, and stay below 9 madness."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "madness",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "tableau",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "obsession",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "retained",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "tide_icons",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tide_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lost",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "drafted",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "keep",
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
        "initial": 0
      },
      {
        "key": "tide",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_in_tide",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "full_deck",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "suit_list",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck",
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
        "key": "swap_tmp",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "bonus_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "madness_end",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reveal_tableau_1",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reveal_tableau_2",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reveal_obsession_1",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "reveal_obsession_2",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "plain_cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "madness_cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "tides",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_tide",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "set_points_0",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "set_points_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_points_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "set_points_3",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "set_points_4_or_more",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "obsession_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "points_per_madness_card",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "diversity_suits_needed",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "diversity_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "madness_bonus_points",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "madness_bonus_reduction",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "madness_loss_threshold",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_retained_per_tide",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "retain_tides",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_madness",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "madness",
            "value": {
              "calc": "starting_madness"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tableau",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "retained",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "obsession",
            "value": ""
          }
        },
        {
          "set": {
            "key": "suit_list",
            "value": [
              "Ruins",
              "Idols",
              "Deep",
              "Stars",
              "Shore"
            ]
          }
        },
        {
          "set": {
            "key": "full_deck",
            "value": [
              "Ruins-1",
              "Ruins-2",
              "Ruins-3",
              "Ruins-4",
              "Ruins*-1",
              "Ruins*-2",
              "Idols-1",
              "Idols-2",
              "Idols-3",
              "Idols-4",
              "Idols*-1",
              "Idols*-2",
              "Deep-1",
              "Deep-2",
              "Deep-3",
              "Deep-4",
              "Deep*-1",
              "Deep*-2",
              "Stars-1",
              "Stars-2",
              "Stars-3",
              "Stars-4",
              "Stars*-1",
              "Stars*-2",
              "Shore-1",
              "Shore-2",
              "Shore-3",
              "Shore-4",
              "Shore*-1",
              "Shore*-2"
            ]
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "madness_end",
            "value": 0
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
        "score",
        "madness"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "round",
      "label": "the next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "tide",
            "value": {
              "calc": "int((round - 1) / rounds_per_tide) + 1"
            }
          }
        },
        {
          "set": {
            "key": "round_in_tide",
            "value": {
              "calc": "round - rounds_per_tide * (tide - 1)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "drafted",
            "value": ""
          }
        }
      ],
      "text": "Round {round} of {total_rounds}: tide {tide}, round {round_in_tide} of {rounds_per_tide} in this tide."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "the tide deal",
      "when": {
        "calc": "round_in_tide == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in full_deck if not any(c in p.retained for p in players)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tableau",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        }
      ],
      "text": "Tide {tide} begins. The deck is shuffled without the retained cards and each player is dealt a private hand of {hand_size}."
    },
    {
      "use": "sync",
      "phase": "round",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "tableau",
        "obsession",
        "retained",
        "score",
        "madness"
      ],
      "text": "Your hand, tableau, Obsession and retained cards:"
    },
    {
      "use": "poll",
      "phase": "draft",
      "label": "the obsession",
      "when": {
        "calc": "round_in_tide == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Ruins",
          "Idols",
          "Deep",
          "Stars",
          "Shore"
        ]
      },
      "store": "obsession",
      "text": "Secretly choose one suit as your Obsession for tide {tide}. Its set points are doubled at the end of the tide. Your opponent will not see it until the tide is scored."
    },
    {
      "use": "poll",
      "phase": "draft",
      "label": "the draft pick",
      "when": {
        "calc": "round_in_tide < rounds_per_tide"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "drafted",
      "text": "Choose one card from your hand to place face down in your tableau. Afterwards the two of you swap your remaining hands."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "place the cards and swap",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "drafted",
            "value": {
              "calc": "you.hand[0]"
            },
            "if": {
              "calc": "round_in_tide == rounds_per_tide"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.drafted"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "tableau",
            "value": {
              "calc": "you.drafted"
            }
          }
        },
        {
          "set": {
            "key": "swap_tmp",
            "value": {
              "calc": "players[0].hand"
            },
            "if": {
              "calc": "round_in_tide < rounds_per_tide"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "players[1].hand"
            },
            "if": {
              "calc": "round_in_tide < rounds_per_tide"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "swap_tmp"
            },
            "if": {
              "calc": "round_in_tide < rounds_per_tide"
            }
          }
        }
      ],
      "text": "Both players place a card face down. Before round 5 of a tide the remaining hands are swapped; in round 5 the last card is placed automatically."
    },
    {
      "use": "update",
      "phase": "tide end",
      "label": "the reveal",
      "when": {
        "calc": "round_in_tide == rounds_per_tide"
      },
      "do": [
        {
          "set": {
            "key": "reveal_tableau_1",
            "value": {
              "calc": "players[0].tableau"
            }
          }
        },
        {
          "set": {
            "key": "reveal_tableau_2",
            "value": {
              "calc": "players[1].tableau"
            }
          }
        },
        {
          "set": {
            "key": "reveal_obsession_1",
            "value": {
              "calc": "players[0].obsession"
            }
          }
        },
        {
          "set": {
            "key": "reveal_obsession_2",
            "value": {
              "calc": "players[1].obsession"
            }
          }
        }
      ],
      "text": "Tide {tide} reveal. Seat 1 drafted {reveal_tableau_1}, Obsession {reveal_obsession_1}. Seat 2 drafted {reveal_tableau_2}, Obsession {reveal_obsession_2}. Retained cards also count: seat 1 {players[0].retained}, seat 2 {players[1].retained}."
    },
    {
      "use": "update",
      "phase": "tide end",
      "label": "the tide scoring",
      "when": {
        "calc": "round_in_tide == rounds_per_tide"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "tide_icons",
            "value": {
              "calc": "count('*' in c for c in you.tableau + you.retained)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "madness",
            "value": {
              "calc": "you.tide_icons"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tide_points",
            "value": {
              "calc": "sum([[set_points_0, set_points_1, set_points_2, set_points_3, set_points_4_or_more][min(count(s in c for c in you.tableau + you.retained), 4)] * (obsession_multiplier if s == you.obsession else 1) for s in suit_list]) + you.tide_icons * points_per_madness_card + (diversity_bonus if count(any(s in c for c in you.tableau + you.retained) for s in suit_list) >= diversity_suits_needed else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.tide_points"
            }
          }
        },
        {
          "set": {
            "key": "bonus_seat",
            "value": {
              "calc": "1 if players[0].tide_icons > players[1].tide_icons else (2 if players[1].tide_icons > players[0].tide_icons else 0)"
            }
          }
        }
      ],
      "text": "Tide {tide} scored. Seat 1: {players[0].tide_icons} madness icons, {players[0].tide_points} points, score {players[0].score}, madness {players[0].madness}. Seat 2: {players[1].tide_icons} madness icons, {players[1].tide_points} points, score {players[1].score}, madness {players[1].madness}. Madness bonus goes to seat {bonus_seat} (0 means nobody)."
    },
    {
      "use": "ask",
      "phase": "tide end",
      "label": "the madness bonus",
      "when": {
        "calc": "round_in_tide == rounds_per_tide and bonus_seat > 0"
      },
      "to": {
        "where": "you.seat == bonus_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "gain_4_points",
          "reduce_madness_1"
        ]
      },
      "verify": {
        "bind": "bonus"
      },
      "text": "You had strictly more madness icons this tide. Choose privately: gain_4_points (+{madness_bonus_points} score) or reduce_madness_1 (madness total -{madness_bonus_reduction})."
    },
    {
      "use": "update",
      "phase": "tide end",
      "label": "bonus and madness check",
      "when": {
        "calc": "round_in_tide == rounds_per_tide"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "bonus_seat"
            },
            "key": "score",
            "value": {
              "calc": "madness_bonus_points"
            },
            "if": {
              "calc": "bonus_seat > 0 and $bonus == 'gain_4_points'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "bonus_seat"
            },
            "key": "madness",
            "value": {
              "calc": "max(0, players[bonus_seat - 1].madness - madness_bonus_reduction)"
            },
            "if": {
              "calc": "bonus_seat > 0 and $bonus == 'reduce_madness_1'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "lost",
            "value": {
              "calc": "1 if you.madness >= madness_loss_threshold and all(p.madness < you.madness for p in players if p.seat != you.seat) else 0"
            }
          }
        },
        {
          "set": {
            "key": "madness_end",
            "value": {
              "calc": "1 if any(p.madness >= madness_loss_threshold for p in players) else 0"
            }
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.lost == 1"
            },
            "to": "out",
            "text": "Seat {player} has gone mad and loses."
          }
        }
      ],
      "text": "Madness check after tide {tide}: seat 1 score {players[0].score}, madness {players[0].madness}; seat 2 score {players[1].score}, madness {players[1].madness}."
    },
    {
      "use": "check",
      "phase": "tide end",
      "label": "is it over",
      "when": {
        "calc": "madness_end == 1 or (round == total_rounds and round_in_tide == rounds_per_tide)"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "poll",
      "phase": "tide end",
      "label": "the retain choice",
      "when": {
        "calc": "round_in_tide == rounds_per_tide and tide <= retain_tides"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "tableau"
        }
      },
      "store": "keep",
      "text": "Choose one card you drafted this tide to retain permanently. It stays face up beside you and counts in every later tide tableau; your other drafted cards return to the deck."
    },
    {
      "use": "update",
      "phase": "tide end",
      "label": "retain the cards",
      "when": {
        "calc": "round_in_tide == rounds_per_tide and tide <= retain_tides"
      },
      "do": [
        {
          "append": {
            "players": "all",
            "key": "retained",
            "value": {
              "calc": "you.keep"
            },
            "if": {
              "calc": "you.keep != ''"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tableau",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "obsession",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "keep",
            "value": ""
          }
        }
      ],
      "text": "Retained cards: seat 1 {players[0].retained}, seat 2 {players[1].retained}. All other drafted cards return to the deck."
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "madness_end == 1 or (round == total_rounds and round_in_tide == rounds_per_tide)"
      },
      "rank_by": "madness_end * (1 - you.lost) * 1000000 + (1 - madness_end) * (you.score * 100 + (99 - you.madness))",
      "text": "Winner: {result}. Final: Seat 1 score {players[0].score}, madness {players[0].madness}; Seat 2 score {players[1].score}, madness {players[1].madness}."
    }
  },
  "limits": {
    "rounds": 15,
    "rounds_max": 20,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "DECK. {deck_size} cards in {suits} suits: Ruins, Idols, Deep, Stars, Shore. Each suit has {cards_per_suit} cards: {plain_cards_per_suit} plain and {madness_cards_per_suit} with a madness icon (written e.g. 'Deep*').\n\nSTRUCTURE. The game has {total_rounds} rounds in {tides} tides of {rounds_per_tide} rounds each: rounds 1-5 are tide 1, rounds 6-10 tide 2, rounds 11-15 tide 3. Each player has a score (starting at {starting_score}) and a madness total (starting at {starting_madness}).\n\nSTART OF EACH TIDE (rounds 1, 6, 11). All 30 cards are shuffled, minus any cards currently retained by players. Each player is dealt a private hand of {hand_size}. The rest are unused this tide. Each player sees only their own hand. At the same moment as their first pick, each player secretly chooses one suit as their Obsession for this tide. It is hidden from the opponent until the tide is scored.\n\nEACH ROUND. Both players simultaneously choose one card from the hand they currently hold and place it face down in their tableau for this tide. Then the two players swap their remaining hands. Hands therefore go 5, 4, 3, 2, 1 cards, and the pick in the fifth round of a tide is forced (it is placed for you).\n\nEND OF EACH TIDE (rounds 5, 10, 15), in order:\n1. Reveal. Both tableaus and both Obsessions are revealed. A player's tide tableau is the 5 cards drafted this tide plus all cards they have retained from earlier tides.\n2. Madness. Each player counts madness icons in their tide tableau (retained cards count every tide they are in) and adds that number to their madness total.\n3. Set points. For each suit, count the cards of that suit in the tableau: 0 cards = {set_points_0} points, 1 = {set_points_1}, 2 = {set_points_2}, 3 = {set_points_3}, 4 or more = {set_points_4_or_more}. Points for the player's Obsession suit are multiplied by {obsession_multiplier}; other suits score normally.\n4. Extra points. Add +{points_per_madness_card} point per madness card in the tableau. Add +{diversity_bonus} points if the tableau contains at least {diversity_suits_needed} different suits; fewer suits give no bonus.\n5. Madness bonus. The player with strictly more madness icons in their tide tableau privately chooses one: gain {madness_bonus_points} points, or reduce their madness total by {madness_bonus_reduction}. If the counts are equal, nobody gets the bonus.\n6. Madness check. If a player's madness total is {madness_loss_threshold} or more, the game ends immediately and that player loses. If both are at {madness_loss_threshold} or more, the one with the higher madness total loses. If they are equal, the game is a draw. If nobody is at {madness_loss_threshold} or more, the game continues.\n7. Retain (tides 1 and 2 only). Each player simultaneously chooses {cards_retained_per_tide} card drafted this tide to retain permanently. It stays face up beside them and is part of every later tide tableau. All other drafted cards return to the deck. After tide 3 no card is retained.\n\nEND OF GAME. A player loses immediately if their madness total reaches {madness_loss_threshold} or more at a tide's madness check. If both reach it, the higher madness total loses, and equal totals are a draw. Otherwise, after tide 3 the higher score wins. If scores are tied, the lower madness total wins. If that is also tied, the game is a draw."
}
```
````
