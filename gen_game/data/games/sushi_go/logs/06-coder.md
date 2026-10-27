# 06 coder

- time: 2026-10-27T16:43:50+00:00 (131.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 d528e78fbd214525, reply sha256 648ee4e39a560231

## Sent

````
# Task: write the XColos game file for "Sushi Draft"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

DECK (104 cards): 14 Tempura, 14 Sashimi, 14 Dumpling, 6 Maki-1 (1 maki icon), 12 Maki-2 (2 icons), 8 Maki-3 (3 icons), 10 Salmon Nigiri, 5 Squid Nigiri, 5 Egg Nigiri, 10 Pudding, 6 Wasabi.

SETUP: Shuffle the deck once at the start of the game. Every player starts with a score of 0 and 0 puddings. The game has 3 hands. Each hand has 9 picks with 3 players or 8 picks with 4 players, so the game lasts 27 or 24 rounds. One round is one pick.

EACH ROUND:
1. Deal (first pick of a hand only): deal each player a hand from the top of the deck, 9 cards with 3 players or 8 cards with 4 players. Undealt cards stay hidden and are not reshuffled.
2. Announce: everyone is told every player's face-up cards for this hand, every player's pudding count and score, and how many cards each hand holds. Each player is shown privately the cards in their own current hand.
3. Pick: all players at the same moment secretly choose one card from their own hand. If a hand holds one card, that card is taken automatically.
4. Reveal: all chosen cards are revealed at once and placed face up in front of their owners.
5. Record the chosen card:
   - Tempura adds 1 to your tempura count.
   - Sashimi adds 1 to your sashimi count.
   - Dumpling adds 1 to your dumpling count.
   - Maki adds its icons (1, 2 or 3) to your maki total.
   - Pudding adds 1 to your puddings, which are kept across all hands.
   - Wasabi adds 1 to your unused wasabi.
   - Nigiri is worth 1 (Egg), 2 (Salmon) or 3 (Squid). If you have at least 1 unused wasabi, the nigiri is placed on it: its value is tripled (3, 6 or 9) and your unused wasabi drops by 1. Add the nigiri's value to your nigiri points for this hand.
6. Pass: everyone passes their remaining hand to the player on their left.
7. Hand scoring (last pick of a hand only). Each player adds the following to their score:
   - Tempura: 5 points per complete pair, so floor(tempura/2) x 5.
   - Sashimi: 10 points per complete set of three, so floor(sashimi/3) x 10.
   - Dumplings: 0 for 0, 1 for 1, 3 for 2, 6 for 3, 10 for 4, and 15 for 5 or more.
   - Nigiri: all nigiri points for the hand. Unused wasabi scores 0.
   - Maki: among players with a maki total of at least 1, those with the highest total split 6 points equally, rounded down. If exactly one player has the highest total, the players with the second-highest total (at least 1) split 3 points equally, rounded down. If two or more players tie for highest, no second-place points are awarded.
   Then every hand-only count (tempura, sashimi, dumplings, maki, unused wasabi, nigiri points) resets to 0. Puddings stay.
8. Pudding scoring (last pick of the third hand only):
   - Players with the most puddings split +6 equally, rounded down.
   - Players with the fewest puddings split -6 equally, rounded toward zero (for example, two tied players get -3 each).
   - Players with 0 puddings count for the fewest.
   - If all players have the same number of puddings, nobody scores for pudding.
9. End check: after the last pick of the third hand, the game ends.

There is no talk phase.

How the winner is decided: After pudding scoring, the player with the highest score wins. If two or more players tie for the highest score, the one among them with the most puddings wins. If they are still tied, the game is a draw among those players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Sushi Draft (3 to 4 players, best with 4)

A card-drafting game: each round every player secretly keeps one card from the hand they hold and passes the rest left. Sets of sushi score at the end of each of 3 hands, and puddings score at the end of the game.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points so far.
  - each player: puddings (number, starts 0); everyone sees it. Pudding cards collected. Kept across all hands.
  - each player: hand (list, starts []); only its owner sees it. Cards the player currently holds to pick from. Only the holder sees them.
  - each player: tableau (list, starts []); everyone sees it. Face-up cards the player has chosen this hand.
  - each player: pick (text, starts ''); only its owner sees it. The card secretly chosen this round, before the reveal.
  - each player: tempura (number, starts 0); everyone sees it. Tempura taken this hand.
  - each player: sashimi (number, starts 0); everyone sees it. Sashimi taken this hand.
  - each player: dumplings (number, starts 0); everyone sees it. Dumplings taken this hand.
  - each player: maki (number, starts 0); everyone sees it. Maki icons taken this hand.
  - each player: wasabi_unused (number, starts 0); everyone sees it. Wasabi taken this hand that no nigiri has been placed on yet.
  - each player: nigiri_points (number, starts 0); everyone sees it. Nigiri value earned this hand, with the wasabi tripling already applied.
  - the table: deck (list, starts 'the 104 cards listed in parameters, shuffled'); hidden from all players. Undealt cards. Hidden and never reshuffled.
  - the table: picks_per_hand (number, starts '9 if 3 players, 8 if 4 players'); everyone sees it. Cards dealt per hand, which is also the number of picks per hand.
  - the table: hand_number (number, starts 1); everyone sees it. The current hand (1 to 3). It becomes 4 when the game is over.
  - the table: pick_number (number, starts 1); everyone sees it. The current pick within the hand, from 1 to picks_per_hand.
  - parameters, each kept as a table attribute: deck_size = 104, count_tempura = 14, count_sashimi = 14, count_dumpling = 14, count_maki_1 = 6, count_maki_2 = 12, count_maki_3 = 8, count_salmon_nigiri = 10, count_squid_nigiri = 5, count_egg_nigiri = 5, count_pudding = 10, count_wasabi = 6, hands_per_game = 3, hand_size_3_players = 9, hand_size_4_players = 8, rounds_3_players = 27, rounds_4_players = 24, maki_icons_1 = 1, maki_icons_2 = 2, maki_icons_3 = 3, egg_value = 1, salmon_value = 2, squid_value = 3, wasabi_multiplier = 3, tempura_set_size = 2, tempura_set_points = 5, sashimi_set_size = 3, sashimi_set_points = 10, dumpling_points_0 = 0, dumpling_points_1 = 1, dumpling_points_2 = 3, dumpling_points_3 = 6, dumpling_points_4 = 10, dumpling_points_5_plus = 15, maki_first_points = 6, maki_second_points = 3, pudding_most_points = 6, pudding_fewest_points = -6, starting_score = 0, starting_puddings = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the deck list from the 104 cards (14 Tempura, 14 Sashimi, 14 Dumpling, 6 Maki-1, 12 Maki-2, 8 Maki-3, 10 Salmon Nigiri, 5 Squid Nigiri, 5 Egg Nigiri, 10 Pudding, 6 Wasabi) and shuffle it once.
  2. Set picks_per_hand to 9 with 3 players or 8 with 4 players.
  3. Every player starts with score 0, puddings 0, an empty hand, an empty tableau and all hand counts at 0.
  4. Set hand_number to 1 and pick_number to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When pick_number == 1: draw picks_per_hand cards at random from deck into each player's hand, removing each card from deck.
  2. [sync] all players. What happens: Announce to everyone each player's tableau, puddings and score, and the size of each hand. Show each player their own hand privately.
  3. [poll] all players answers: one card name from the player's own hand. What happens: When the size of hand > 1: set pick to the chosen card. No one sees another player's pick until all have answered.
  4. [update] all players. What happens: When the size of hand == 1: set pick to the single card in hand automatically.
  5. [update] all players. What happens: Reveal: remove pick from hand, append it to tableau, and announce every player's pick to all.
  6. [update] all players. What happens: Record pick. Tempura: tempura +1. Sashimi: sashimi +1. Dumpling: dumplings +1. Maki-1/2/3: maki +1/+2/+3. Pudding: puddings +1. Wasabi: wasabi_unused +1. Egg/Salmon/Squid Nigiri with base value v of 1, 2 or 3: if wasabi_unused >= 1, then nigiri_points += 3*v and wasabi_unused -= 1; otherwise nigiri_points += v.
  7. [update] all players. What happens: Pass: each player's remaining hand moves to the player on their left (seat s gives its hand to seat s+1, and the last seat gives to seat 1).
  8. [update] all players. What happens: When pick_number == picks_per_hand, add to score: floor(tempura/2)*5 + floor(sashimi/3)*10 + m*(m+1)/2 where m = min(dumplings,5) + nigiri_points. Maki: let M1 be the highest maki among players with maki >= 1, and k1 the number of players with maki == M1; each of them gains floor(6/k1). If k1 == 1, let M2 be the highest maki >= 1 below M1, and k2 the number of players with maki == M2; each of them gains floor(3/k2). Then set tempura, sashimi, dumplings, maki, wasabi_unused and nigiri_points to 0 and empty tableau. Puddings stay.
  9. [update] all players. What happens: When pick_number == picks_per_hand and hand_number == 3, and not all players have equal puddings: players with puddings == max split +6, each gaining floor(6/count). Players with puddings == min (0 counts as fewest) split -6, each gaining -floor(6/count).
  10. [update] all players. What happens: Advance: pick_number += 1. If pick_number > picks_per_hand, set pick_number to 1 and hand_number += 1.
  11. [check] all players. What happens: End the game if hand_number > 3; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, the 104-card deck is shuffled once, and every player has score 0 and puddings 0.
  R2. When pick_number is 1, each player is dealt 9 cards (3 players) or 8 cards (4 players) from the deck into their hand, and those cards leave the deck.
  R3. Undealt cards stay in the hidden deck and are never reshuffled.
  R4. When a pick is made, all players choose at the same time, and no player sees another's choice until all have chosen.
  R5. When a player's hand holds exactly 1 card, that card is picked automatically, without a question.
  R6. When picks are revealed, each picked card leaves its owner's hand and is added face up to their tableau.
  R7. When Tempura is picked, tempura +1. When Sashimi is picked, sashimi +1. When Dumpling is picked, dumplings +1.
  R8. When Maki-1, Maki-2 or Maki-3 is picked, maki increases by 1, 2 or 3.
  R9. When Pudding is picked, puddings +1, and puddings are never reset between hands.
  R10. When Wasabi is picked, wasabi_unused +1.
  R11. When a nigiri is picked with wasabi_unused 0, nigiri_points increases by 1 (Egg), 2 (Salmon) or 3 (Squid).
  R12. When a nigiri is picked with wasabi_unused >= 1, nigiri_points increases by 3 (Egg), 6 (Salmon) or 9 (Squid), and wasabi_unused decreases by 1.
  R13. When picks are recorded, each player's remaining hand passes to the player on their left.
  R14. When a hand ends, each player gains floor(tempura/2)*5 points (for example, 3 tempura gives 5).
  R15. When a hand ends, each player gains floor(sashimi/3)*10 points (for example, 5 sashimi gives 10).
  R16. When a hand ends, dumplings score 0/1/3/6/10/15 for 0/1/2/3/4/5-or-more dumplings.
  R17. When a hand ends, each player gains their nigiri_points, and unused wasabi scores 0.
  R18. When a hand ends, the players with the highest maki total (at least 1) split 6 points, each gaining floor(6/k).
  R19. When a hand ends and exactly one player has the highest maki, the players with the second-highest maki (at least 1) split 3 points, each gaining floor(3/k).
  R20. When two or more players tie for the highest maki, no second-place maki points are awarded.
  R21. When a player has maki 0, they score no maki points.
  R22. When a hand ends, tempura, sashimi, dumplings, maki, wasabi_unused, nigiri_points and tableau reset, while puddings stay.
  R23. When the third hand ends, the players with the most puddings split +6, each gaining floor(6/k).
  R24. When the third hand ends, the players with the fewest puddings (0 counts as fewest) split -6, rounded toward zero (two tied players get -3 each).
  R25. When the third hand ends and all players have equal puddings, nobody scores for pudding.
  R26. When the last pick of the third hand is done (pick 27 with 3 players, pick 24 with 4 players), the game ends.
  R27. When the game ends, the highest score wins, ties are broken by most puddings, and players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Pick: choose one card from your hand | asked: all players, when their hand holds 2 or more cards | options: each distinct card name currently in that player's own hand
  - Pick when the hand holds 1 card | asked: no one is asked | options: none: the single card is taken automatically

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number > 3
  - each player's standing: you.score * 100 + you.puddings (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest score wins. Among players tied on score, the one with the most puddings wins. Players still tied share the win, which is the source's draw.
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

- each player: `score` (number, visible: public, starts 0): Total points so far.
- each player: `puddings` (number, visible: public, starts 0): Pudding cards collected. Kept across all hands.
- the table: `hand_number` (number, visible: public, starts 1): The current hand (1 to 3). It becomes 4 when the game is over.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 104, count_tempura = 14, count_sashimi = 14, count_dumpling = 14, count_maki_1 = 6, count_maki_2 = 12, count_maki_3 = 8, count_salmon_nigiri = 10, count_squid_nigiri = 5, count_egg_nigiri = 5, count_pudding = 10, count_wasabi = 6, hands_per_game = 3, hand_size_3_players = 9, hand_size_4_players = 8, rounds_3_players = 27, rounds_4_players = 24, maki_icons_1 = 1, maki_icons_2 = 2, maki_icons_3 = 3, egg_value = 1, salmon_value = 2, squid_value = 3, wasabi_multiplier = 3, tempura_set_size = 2, tempura_set_points = 5, sashimi_set_size = 3, sashimi_set_points = 10, dumpling_points_0 = 0, dumpling_points_1 = 1, dumpling_points_2 = 3, dumpling_points_3 = 6, dumpling_points_4 = 10, dumpling_points_5_plus = 15, maki_first_points = 6, maki_second_points = 3, pudding_most_points = 6, pudding_fewest_points = -6, starting_score = 0, starting_puddings = 0
- the game ends with ONE ending whose `rank_by` is `you.score * 100 + you.puddings`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "sushi_draft",
    "name": "Sushi Draft",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Keep one card from your hand each round and pass the rest left; sushi sets score after each of 3 hands, puddings at the end."
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
      },
      {
        "key": "puddings",
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
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "tempura",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sashimi",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dumplings",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "maki",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wasabi_unused",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "nigiri_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "incoming",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "picks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pick_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "card_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Tempura",
          "Sashimi",
          "Dumpling",
          "Maki-1",
          "Maki-2",
          "Maki-3",
          "Salmon Nigiri",
          "Squid Nigiri",
          "Egg Nigiri",
          "Pudding",
          "Wasabi"
        ]
      },
      {
        "key": "positions",
        "visible": "none",
        "type": "list",
        "initial": [
          0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
          10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
          20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
          30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
          40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
          50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
          60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
          70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
          80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
          90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
          100, 101, 102, 103
        ]
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 104
      },
      {
        "key": "count_tempura",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "count_sashimi",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "count_dumpling",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "count_maki_1",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "count_maki_2",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "count_maki_3",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "count_salmon_nigiri",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "count_squid_nigiri",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "count_egg_nigiri",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "count_pudding",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "count_wasabi",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "hands_per_game",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hand_size_3_players",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "hand_size_4_players",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "rounds_3_players",
        "visible": "public",
        "type": "number",
        "initial": 27
      },
      {
        "key": "rounds_4_players",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "maki_icons_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "maki_icons_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "maki_icons_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "egg_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "salmon_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "squid_value",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "wasabi_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tempura_set_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "tempura_set_points",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "sashimi_set_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "sashimi_set_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "dumpling_points_0",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dumpling_points_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dumpling_points_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "dumpling_points_3",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "dumpling_points_4",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "dumpling_points_5_plus",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "maki_first_points",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "maki_second_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pudding_most_points",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "pudding_fewest_points",
        "visible": "public",
        "type": "number",
        "initial": -6
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_puddings",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build and shuffle the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "['Tempura' for i in positions if i < count_tempura] + ['Sashimi' for i in positions if i < count_sashimi] + ['Dumpling' for i in positions if i < count_dumpling] + ['Maki-1' for i in positions if i < count_maki_1] + ['Maki-2' for i in positions if i < count_maki_2] + ['Maki-3' for i in positions if i < count_maki_3] + ['Salmon Nigiri' for i in positions if i < count_salmon_nigiri] + ['Squid Nigiri' for i in positions if i < count_squid_nigiri] + ['Egg Nigiri' for i in positions if i < count_egg_nigiri] + ['Pudding' for i in positions if i < count_pudding] + ['Wasabi' for i in positions if i < count_wasabi]"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c[1] for c in sorted([[uniform(0, 1), d] for d in deck])]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "hand size",
      "do": [
        {
          "set": {
            "key": "picks_per_hand",
            "value": {
              "calc": "hand_size_3_players if len(players) == 3 else hand_size_4_players"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "players start",
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
            "key": "puddings",
            "value": {
              "calc": "starting_puddings"
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
            "key": "tempura",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sashimi",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "dumplings",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "maki",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wasabi_unused",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "nigiri_points",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first hand, first pick",
      "do": [
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "pick_number",
            "value": 1
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "deal the hands",
      "when": {
        "calc": "pick_number == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[deck[(you.seat - 1) * picks_per_hand + j] for j in positions if j < picks_per_hand]"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[deck[i] for i in positions if i >= len(players) * picks_per_hand and i < len(deck)]"
            }
          }
        }
      ],
      "text": "Hand {hand_number} of {hands_per_game}: each player is dealt {picks_per_hand} cards."
    },
    {
      "use": "sync",
      "phase": "announce",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "Hand {hand_number}, pick {pick_number} of {picks_per_hand}; every hand now holds the same number of cards. Every player's tableau, puddings and score are public. Your own state, with your private hand:"
    },
    {
      "use": "update",
      "phase": "pick",
      "label": "prepare the offer",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "pick",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in card_names if c in you.hand]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "pick",
      "label": "pick a card",
      "when": {
        "calc": "any(len(p.hand) > 1 for p in players)"
      },
      "to": {
        "where": "len(you.hand) > 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pick",
      "text": "Secretly choose one card from your hand to keep. Everyone chooses at the same moment; all choices are revealed together, and the rest of your hand passes to the player on your left."
    },
    {
      "use": "update",
      "phase": "pick",
      "label": "last card taken automatically",
      "do": [
        {
          "set": {
            "players": {
              "where": "len(you.hand) == 1"
            },
            "key": "pick",
            "value": {
              "calc": "you.hand[0]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "reveal",
      "do": [
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pick"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "tableau",
            "value": {
              "calc": "you.pick"
            },
            "text": "Seat {player} reveals {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "record the picks",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Tempura'"
            },
            "key": "tempura",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Sashimi'"
            },
            "key": "sashimi",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Dumpling'"
            },
            "key": "dumplings",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick in ['Maki-1', 'Maki-2', 'Maki-3']"
            },
            "key": "maki",
            "value": {
              "calc": "maki_icons_1 if you.pick == 'Maki-1' else (maki_icons_2 if you.pick == 'Maki-2' else maki_icons_3)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Pudding'"
            },
            "key": "puddings",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Wasabi'"
            },
            "key": "wasabi_unused",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick in ['Egg Nigiri', 'Salmon Nigiri', 'Squid Nigiri']"
            },
            "key": "nigiri_points",
            "value": {
              "calc": "(egg_value if you.pick == 'Egg Nigiri' else (salmon_value if you.pick == 'Salmon Nigiri' else squid_value)) * (wasabi_multiplier if you.wasabi_unused >= 1 else 1)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick in ['Egg Nigiri', 'Salmon Nigiri', 'Squid Nigiri'] and you.wasabi_unused >= 1"
            },
            "key": "wasabi_unused",
            "value": -1,
            "text": "Seat {player} places the nigiri on a wasabi: its value is tripled."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "pass left",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "incoming",
            "value": {
              "calc": "players[you.seat - 2].hand if you.seat > 1 else players[len(players) - 1].hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.incoming"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "incoming",
            "value": []
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "hand scoring",
      "when": {
        "calc": "pick_number == picks_per_hand"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "int(you.tempura / tempura_set_size) * tempura_set_points + int(you.sashimi / sashimi_set_size) * sashimi_set_points + [dumpling_points_0, dumpling_points_1, dumpling_points_2, dumpling_points_3, dumpling_points_4, dumpling_points_5_plus][min(you.dumplings, 5)] + you.nigiri_points"
            },
            "text": "Seat {player} scores {value} for tempura, sashimi, dumplings and nigiri."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.maki >= 1 and you.maki == max([p.maki for p in players])"
            },
            "key": "score",
            "value": {
              "calc": "int(maki_first_points / count(p.maki == you.maki for p in players))"
            },
            "text": "Seat {player} has the most maki and gains {value}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.maki >= 1 and count(p.maki == max([q.maki for q in players]) for p in players) == 1 and you.maki == max([0] + [p.maki for p in players if p.maki < max([q.maki for q in players])])"
            },
            "key": "score",
            "value": {
              "calc": "int(maki_second_points / count(p.maki == you.maki for p in players))"
            },
            "text": "Seat {player} has the second most maki and gains {value}."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tempura",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sashimi",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "dumplings",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "maki",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wasabi_unused",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "nigiri_points",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tableau",
            "value": []
          }
        }
      ],
      "text": "Hand {hand_number} is scored. Hand counts and tableaus reset; puddings stay."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "pudding scoring",
      "when": {
        "calc": "pick_number == picks_per_hand and hand_number == hands_per_game and max([p.puddings for p in players]) != min([p.puddings for p in players])"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.puddings == max([p.puddings for p in players])"
            },
            "key": "score",
            "value": {
              "calc": "int(pudding_most_points / count(p.puddings == you.puddings for p in players))"
            },
            "text": "Seat {player} has the most puddings: {value}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.puddings == min([p.puddings for p in players])"
            },
            "key": "score",
            "value": {
              "calc": "int(pudding_fewest_points / count(p.puddings == you.puddings for p in players))"
            },
            "text": "Seat {player} has the fewest puddings: {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "advance",
      "label": "advance",
      "do": [
        {
          "adjust": {
            "key": "hand_number",
            "value": 1,
            "if": {
              "calc": "pick_number == picks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "pick_number",
            "value": {
              "calc": "1 if pick_number == picks_per_hand else pick_number + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "advance",
      "label": "after the third hand",
      "when": {
        "calc": "hand_number > hands_per_game"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand_number > hands_per_game"
      },
      "rank_by": "you.score * 100 + you.puddings",
      "text": "Winner: {result}. Final [seat, score, puddings]: {[[p.seat, p.score, p.puddings] for p in players]}."
    }
  },
  "limits": {
    "rounds": 27,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Sushi Draft uses a {deck_size}-card deck: {count_tempura} Tempura, {count_sashimi} Sashimi, {count_dumpling} Dumpling, {count_maki_1} Maki-1 (1 maki icon), {count_maki_2} Maki-2 (2 icons), {count_maki_3} Maki-3 (3 icons), {count_salmon_nigiri} Salmon Nigiri, {count_squid_nigiri} Squid Nigiri, {count_egg_nigiri} Egg Nigiri, {count_pudding} Pudding and {count_wasabi} Wasabi. The deck is shuffled once at the start. Everyone starts with score {starting_score} and {starting_puddings} puddings.\n\nThe game has {hands_per_game} hands. Each hand has {hand_size_3_players} picks with 3 players or {hand_size_4_players} picks with 4 players ({rounds_3_players} or {rounds_4_players} rounds in all). One round is one pick.\n\nEach round:\n1. Deal (first pick of a hand only): each player is dealt a hand from the top of the deck, {hand_size_3_players} cards with 3 players or {hand_size_4_players} with 4. Undealt cards stay hidden and are never reshuffled.\n2. Everyone sees every player's face-up cards for this hand, pudding count and score, and how many cards each hand holds. You alone see the cards in your own hand.\n3. Pick: all players at the same moment secretly choose one card from their own hand. Nobody sees another's choice until all have chosen. If your hand holds one card, it is taken automatically and you are not asked.\n4. Reveal: all chosen cards are revealed at once, leave their owners' hands and go face up in front of them.\n5. Record: Tempura adds 1 to your tempura count; Sashimi adds 1 to your sashimi count; Dumpling adds 1 to your dumpling count; Maki adds its icons ({maki_icons_1}, {maki_icons_2} or {maki_icons_3}) to your maki total; Pudding adds 1 to your puddings, kept across all hands; Wasabi adds 1 to your unused wasabi. Nigiri is worth {egg_value} (Egg), {salmon_value} (Salmon) or {squid_value} (Squid). If you have at least 1 unused wasabi, the nigiri is placed on it: its value is multiplied by {wasabi_multiplier} (3, 6 or 9) and your unused wasabi drops by 1. If you have no unused wasabi, the nigiri scores its plain value. Add the nigiri's value to your nigiri points for this hand.\n6. Pass: everyone passes their remaining hand to the player on their left.\n7. Hand scoring (last pick of a hand only). Each player adds: Tempura: {tempura_set_points} points per complete pair of {tempura_set_size}. Sashimi: {sashimi_set_points} points per complete set of {sashimi_set_size}. Dumplings: {dumpling_points_0} for 0, {dumpling_points_1} for 1, {dumpling_points_2} for 2, {dumpling_points_3} for 3, {dumpling_points_4} for 4, {dumpling_points_5_plus} for 5 or more. Nigiri: all nigiri points for the hand; unused wasabi scores 0. Maki: among players with a maki total of at least 1, those with the highest total split {maki_first_points} points equally, rounded down. If exactly one player has the highest total, the players with the second-highest total (at least 1) split {maki_second_points} points equally, rounded down. If two or more players tie for highest, no second-place points are awarded. A player with maki 0 scores no maki points. Then tempura, sashimi, dumplings, maki, unused wasabi, nigiri points and the face-up cards reset; puddings stay.\n8. Pudding scoring (last pick of the third hand only): players with the most puddings split +{pudding_most_points} equally, rounded down. Players with the fewest puddings split {pudding_fewest_points} equally, rounded toward zero (two tied players get -3 each). Players with 0 puddings count for the fewest. If all players have the same number of puddings, nobody scores for pudding.\n9. After the last pick of the third hand, the game ends.\n\nThere is no talking. The highest score wins. If two or more players tie for the highest score, the one among them with the most puddings wins. Players still tied share the win."
}
```
````
