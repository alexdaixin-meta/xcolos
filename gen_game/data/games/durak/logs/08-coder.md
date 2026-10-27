# 08 coder

- time: 2026-10-27T21:17:47+00:00 (104.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 833f7fb0cd8994ac, reply sha256 7a7a9acf73c11a6a

## Sent

````
# Task: write the XColos game file for "Offered-Trump Duel Durak"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. There are 36 cards: four suits (Clubs, Diamonds, Hearts, Spades), each with ranks 6, 7, 8, 9, 10, J (11), Q (12), K (13), A (14). Suit order, used only to break ties, is Clubs, Diamonds, Hearts, Spades.

BEATING. Once a trump suit is set, card X beats card Y if (a) X is the same suit as Y and of higher rank, or (b) X is a trump and Y is not. Nothing else beats.

STRUCTURE. The game has 4 deals. Each round is one bout. There are at most 10 bouts per deal and at most 40 rounds in total. Player 1 is the first attacker (the proposer) in deals 1 and 3. Player 2 is the first attacker in deals 2 and 4. The other player is the first defender (the chooser).

STARTING A DEAL (these steps happen only in the first bout of a deal, when the deal's bout counter is 0):
S1. DEAL. Shuffle all 36 cards once. Deal 8 cards face down to each player; only the owner sees their hand. The remaining 20 cards are set aside face down, unseen by both and unused this deal. This shuffle is the only random event.
S2. OFFER. The first attacker names two different suits. If the answer is not two different suits, the offer is Hearts and Spades. The offer is announced to both players.
S3. CHOICE. The first defender picks one of the two offered suits. That suit is the trump for the whole deal and is announced. If the answer is not one of the offered suits, the first suit offered becomes trump.

A BOUT (every round), in order:
1. ATTACK. The attacker places 1, 2 or 3 cards from their hand face up. All of them must be the same rank, and their number may not exceed the number of cards in the defender's hand. An illegal attack (a card not in hand, mixed ranks, or too many cards) is replaced by the attacker's single lowest-ranked card; ties go to the earliest suit in suit order. The attack is announced.
2. DEFENCE. The defender either says TAKE, or names one different card from their hand for each attack card, saying which attack card each one beats. Every pairing must be a legal beat. Any illegal or incomplete defence counts as TAKE.
3. RESOLVE. If the defence succeeded, all attack and defence cards are discarded face up, out of play, and the defender becomes the attacker for the next bout. If the defender took, the attack cards go into the defender's hand and the same player attacks again next bout. All cards played, the result, and both hand sizes are announced. Add 1 to the bout counter.

ENDING A DEAL. After RESOLVE, the deal ends if either player has no cards or the bout counter has reached 10. Penalties:
- If exactly one player has no cards, the other player (the durak) adds the number of cards in their hand to their penalty total.
- If both have no cards, nobody scores.
- If the deal ended at 10 bouts with both holding cards, the player with more cards adds the difference in hand sizes to their penalty total. Equal hands score nothing.

The next deal then starts with its bout counter at 0 and the first attacker set by the schedule above.

ENDING THE GAME. The game ends when deal 4 has ended. If round 40 finishes during a deal, that deal is scored as if it had reached its 10-bout cap.

How the winner is decided: When the game ends, the player with the lower total penalty wins. If the two totals are equal, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Offered-Trump Duel Durak (2 to 2 players, best with 2)

Two-player Durak over 4 deals of up to 10 bouts each. The first attacker offers two suits and the defender picks one as trump. The player left holding cards takes penalty points, and the lower total penalty wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Card codes in the player's hand. A code is rank*10+suit code, e.g. 61 = 6 of Clubs, 144 = Ace of Spades.
  - each player: hand_count (number, starts 0); everyone sees it. Number of cards in hand, announced after each bout
  - each player: penalty (number, starts 0); everyone sees it. Total penalty points (lower is better)
  - the table: deck (list, starts []); hidden from all players. The 36 card codes, refilled and shuffled at the start of each deal; the 20 cards left after dealing stay here, set aside and unused
  - the table: deal_number (number, starts 1); everyone sees it. Current deal, 1 to 4; becomes 5 when deal 4 has ended
  - the table: bout_counter (number, starts 0); everyone sees it. Bouts played in the current deal
  - the table: round_number (number, starts 0); everyone sees it. Total bouts played in the game
  - the table: attacker_seat (number, starts 1); everyone sees it. Seat that attacks this bout; the other seat defends
  - the table: offer (list, starts []); everyone sees it. The two suits offered as trump this deal
  - the table: trump (text, starts ''); everyone sees it. Trump suit for the current deal
  - the table: attack_cards (list, starts []); everyone sees it. Cards placed in the current attack
  - the table: defence_cards (list, starts []); everyone sees it. Cards played in defence, each paired with an attack card
  - the table: defence_ok (bool, starts False); everyone sees it. Whether this bout's defence succeeded
  - the table: discard (list, starts []); everyone sees it. Face-up discarded cards, out of play for the deal
  - parameters, each kept as a table attribute: deck_size = 36, suits = 4, ranks_per_suit = 9, lowest_rank = 6, highest_rank = 14, hand_size_dealt = 8, cards_set_aside = 20, deals = 4, max_bouts_per_deal = 10, max_rounds_total = 40, min_attack_cards = 1, max_attack_cards = 3, suits_offered = 2, suit_code_clubs = 1, suit_code_diamonds = 2, suit_code_hearts = 3, suit_code_spades = 4

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Each seat's penalty is set to 0.
  2. deal_number is set to 1, bout_counter to 0, round_number to 0 and attacker_seat to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Start of a deal (S1). Set deck to all 36 card codes, empty both hands and clear discard, offer and trump. Draw 8 cards at random from deck into each seat's hand, removing each from deck. The 20 cards left in deck are set aside, unused. Set hand_count = 8 for each seat. Set attacker_seat = 1 if deal_number is 1 or 3, and 2 if deal_number is 2 or 4.
  2. [sync] all players. What happens: Each seat privately sees its own hand.
  3. [ask] the seat in attacker_seat (first attacker) answers: one pair of two different suits: Clubs+Diamonds, Clubs+Hearts, Clubs+Spades, Diamonds+Hearts, Diamonds+Spades, Hearts+Spades. What happens: Set offer to the two named suits (S2). If the answer is not two different suits, set offer = [Hearts, Spades]. Announce the offer to both seats.
  4. [ask] the seat not in attacker_seat (first defender) answers: one of the two suits in offer. What happens: Set trump to the chosen suit (S3). If the answer is not in offer, set trump to the first suit in offer. Announce trump.
  5. [ask] the seat in attacker_seat answers: short text: 1 to 3 card codes from your hand, all of the same rank. What happens: Set attack_cards to the named cards and remove them from the attacker's hand. If any card is not in hand, the ranks differ, or there are more cards than 3 or than the defender's hand_count, use instead the single card with the minimum code in the attacker's hand. Announce attack_cards. JUDGED: a referee rules true or false on "Every card the attacker named is in the attacker's hand, all named cards share one rank, and there are between 1 and 3 of them, no more than the defender's hand_count."; write this step's `when` as {"prose": that sentence, verbatim}.
  6. [ask] the seat not in attacker_seat (defender) answers: short text: TAKE, or one pairing per attack card in the form 'defence card beats attack card'. What happens: If judged true, set defence_ok = true, set defence_cards to the named defence cards and remove them from the defender's hand. Otherwise set defence_ok = false and defence_cards = [] (counts as TAKE). JUDGED: a referee rules true or false on "The defender named exactly one different card from the defender's own hand for each card in attack_cards, and each named card beats its paired attack card: it is the same suit and of higher rank, or it is of the trump suit while the attack card is not."; write this step's `when` as {"prose": that sentence, verbatim}.
  7. [update] all players. What happens: RESOLVE. If defence_ok: append attack_cards and defence_cards to discard, and switch attacker_seat to the other seat. If not defence_ok: append attack_cards to the defender's hand, and attacker_seat stays the same. Recompute hand_count for both seats. Clear attack_cards and defence_cards. Add 1 to bout_counter and 1 to round_number. Announce the cards played, the result, and both hand_count values.
  8. [update] all players. What happens: END OF DEAL. If exactly one seat has hand_count 0, the other seat adds its hand_count to penalty. If both have 0, nobody scores. If both hold cards, the seat with the larger hand_count adds (larger hand_count - smaller hand_count) to penalty; equal hands score nothing. Then add 1 to deal_number and set bout_counter = 0. Announce both penalty totals.
  9. [check] all players. What happens: End the game if deal_number > 4 or round_number >= 40; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 36 cards: suits Clubs, Diamonds, Hearts, Spades, each with ranks 6, 7, 8, 9, 10, 11 (J), 12 (Q), 13 (K) and 14 (A).
  R2. When a deal starts (bout_counter is 0), all 36 cards are shuffled, each player receives 8 cards in hand, and the remaining 20 stay set aside, unused.
  R3. When deal 1 or 3 starts, seat 1 is the first attacker; when deal 2 or 4 starts, seat 2 is the first attacker.
  R4. When a deal starts, the first attacker names two different suits as the offer; if the answer is not two different suits, the offer is Hearts and Spades.
  R5. When the offer is made, the first defender picks one offered suit as trump for the whole deal; if the answer is not an offered suit, the first offered suit becomes trump.
  R6. Card X beats card Y only when X is the same suit as Y and of higher rank, or when X is trump and Y is not.
  R7. When attacking, the attacker places 1 to 3 cards of the same rank from hand, and never more cards than the defender holds.
  R8. When an attack is illegal (a card not in hand, mixed ranks, or too many cards), it is replaced by the attacker's single lowest-ranked card, with ties going to the earliest suit in the order Clubs, Diamonds, Hearts, Spades.
  R9. When defending, the defender says TAKE or names one different card from hand for each attack card that legally beats it; any illegal or incomplete defence counts as TAKE.
  R10. When the defence succeeds, all attack and defence cards are discarded, and the defender becomes the attacker for the next bout.
  R11. When the defender takes, the attack cards go into the defender's hand, and the same player attacks again next bout.
  R12. When a bout resolves, the cards played, the result and both hand sizes are announced, and bout_counter rises by 1.
  R13. When a bout resolves with either player at 0 cards or bout_counter at 10, the deal ends.
  R14. When a deal ends with exactly one player at 0 cards, the other player adds their hand size to their penalty (e.g. holding 5 cards adds 5).
  R15. When a deal ends with both players at 0 cards, nobody's penalty changes.
  R16. When a deal ends at 10 bouts with both holding cards, the player with more cards adds the difference to their penalty (e.g. 7 vs 3 adds 4); equal hands add nothing.
  R17. When round 40 finishes during a deal, that deal is scored as if it had reached its 10-bout cap.
  R18. When deal 4 has ended, the game ends: the player with the lower total penalty wins, and equal totals are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - OFFER (first bout of a deal) | asked: the first attacker | options: one of the six pairs of two different suits: Clubs+Diamonds, Clubs+Hearts, Clubs+Spades, Diamonds+Hearts, Diamonds+Spades, Hearts+Spades
  - CHOICE (first bout of a deal) | asked: the first defender | options: either of the two suits in the offer, and no other
  - ATTACK | asked: the attacker | options: free text naming 1 to 3 cards of one rank from their own hand, no more than the defender's hand_count
  - DEFENCE | asked: the defender | options: TAKE, or free text pairing one different card from their own hand with each attack card

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deal_number > 4 or round_number >= 40
  - each player's standing: 0 - you.penalty (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total penalty, and the lower total wins. If the two totals are equal, both share the top spot, which is the draw.
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

- each player: `hand_count` (number, visible: public, starts 0): Number of cards in hand, announced after each bout
- each player: `penalty` (number, visible: public, starts 0): Total penalty points (lower is better)
- the table: `deal_number` (number, visible: public, starts 1): Current deal, 1 to 4; becomes 5 when deal 4 has ended
- the table: `bout_counter` (number, visible: public, starts 0): Bouts played in the current deal
- the table: `trump` (text, visible: public, starts ''): Trump suit for the current deal
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, suits = 4, ranks_per_suit = 9, lowest_rank = 6, highest_rank = 14, hand_size_dealt = 8, cards_set_aside = 20, deals = 4, max_bouts_per_deal = 10, max_rounds_total = 40, min_attack_cards = 1, max_attack_cards = 3, suits_offered = 2, suit_code_clubs = 1, suit_code_diamonds = 2, suit_code_hearts = 3, suit_code_spades = 4
- the game ends with ONE ending whose `rank_by` is `0 - you.penalty`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "offered_trump_duel_durak",
    "name": "Offered-Trump Duel Durak",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Durak over 4 deals: the attacker offers two suits, the defender picks trump, and whoever is left holding cards takes penalty points."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [61, 62, 63, 64, 71, 72, 73, 74, 81, 82, 83, 84, 91, 92, 93, 94, 101, 102, 103, 104, 111, 112, 113, 114, 121, 122, 123, 124, 131, 132, 133, 134, 141, 142, 143, 144]
      },
      {
        "key": "card_text",
        "visible": "none",
        "type": "list",
        "initial": ["61", "62", "63", "64", "71", "72", "73", "74", "81", "82", "83", "84", "91", "92", "93", "94", "101", "102", "103", "104", "111", "112", "113", "114", "121", "122", "123", "124", "131", "132", "133", "134", "141", "142", "143", "144"]
      },
      {
        "key": "card_idx",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "attack_ok",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deal_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "bout_counter",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attacker_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "offer",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "attack_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "defence_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "defence_ok",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "lowest_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "highest_rank",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "hand_size_dealt",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cards_set_aside",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "max_bouts_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "max_rounds_total",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "min_attack_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_attack_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "suits_offered",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "suit_code_clubs",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "suit_code_diamonds",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "suit_code_hearts",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "suit_code_spades",
        "visible": "public",
        "type": "number",
        "initial": 4
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "reset penalties",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "penalty",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "reset counters",
      "do": [
        {
          "set": {
            "key": "deal_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "bout_counter",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "attacker_seat",
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
      "label": "start of deal",
      "when": {
        "calc": "bout_counter == 0"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
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
            "key": "discard",
            "value": []
          }
        },
        {
          "set": {
            "key": "offer",
            "value": []
          }
        },
        {
          "set": {
            "key": "trump",
            "value": ""
          }
        },
        {
          "set": {
            "key": "attack_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "defence_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "attack_ok",
            "value": false
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
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "hand_size_dealt"
            }
          }
        },
        {
          "set": {
            "key": "attacker_seat",
            "value": {
              "calc": "1 if deal_number in [1, 3] else 2"
            }
          }
        }
      ],
      "text": "Deal {deal_number} of {deals} begins. Each player is dealt {hand_size_dealt} cards; {cards_set_aside} cards are set aside unused. Seat {attacker_seat} is the first attacker."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Your current state:"
    },
    {
      "use": "ask",
      "phase": "deal",
      "label": "the offer",
      "when": {
        "calc": "bout_counter == 0"
      },
      "to": {
        "where": "you.seat == attacker_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Clubs+Diamonds",
          "Clubs+Hearts",
          "Clubs+Spades",
          "Diamonds+Hearts",
          "Diamonds+Spades",
          "Hearts+Spades"
        ]
      },
      "verify": {
        "bind": "offer_pick"
      },
      "text": "You are the first attacker of deal {deal_number}. Offer two different suits; your opponent will pick one of them as trump for the whole deal."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "set the offer",
      "when": {
        "calc": "bout_counter == 0"
      },
      "do": [
        {
          "set": {
            "key": "offer",
            "value": {
              "calc": "['Clubs', 'Diamonds'] if $offer_pick == 'Clubs+Diamonds' else (['Clubs', 'Hearts'] if $offer_pick == 'Clubs+Hearts' else (['Clubs', 'Spades'] if $offer_pick == 'Clubs+Spades' else (['Diamonds', 'Hearts'] if $offer_pick == 'Diamonds+Hearts' else (['Diamonds', 'Spades'] if $offer_pick == 'Diamonds+Spades' else ['Hearts', 'Spades']))))"
            }
          }
        }
      ],
      "text": "Seat {attacker_seat} offers {offer} as trump."
    },
    {
      "use": "ask",
      "phase": "deal",
      "label": "the trump choice",
      "when": {
        "calc": "bout_counter == 0"
      },
      "to": {
        "where": "you.seat != attacker_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "offer"
        }
      },
      "verify": {
        "bind": "trump_pick"
      },
      "text": "You are the first defender. Pick one of the offered suits {offer} as trump for the whole deal."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "set the trump",
      "when": {
        "calc": "bout_counter == 0"
      },
      "do": [
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "$trump_pick if $trump_pick in offer else offer[0]"
            }
          }
        }
      ],
      "text": "Trump for deal {deal_number} is {trump}."
    },
    {
      "use": "ask",
      "phase": "bout",
      "label": "attack",
      "to": {
        "where": "you.seat == attacker_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 10
      },
      "verify": {
        "bind": "att"
      },
      "text": "You attack. Trump is {trump}. Name {min_attack_cards} to {max_attack_cards} card codes from your hand, all of the same rank, separated by spaces (e.g. '91 93'), and no more cards than the defender holds. A code is rank*10+suit (1 Clubs, 2 Diamonds, 3 Hearts, 4 Spades). An illegal attack is replaced by your single lowest card."
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "legal attack",
      "when": {
        "prose": "Every card the attacker named is in the attacker's hand, all named cards share one rank, and there are between 1 and 3 of them, no more than the defender's hand_count."
      },
      "do": [
        {
          "set": {
            "key": "attack_cards",
            "value": {
              "calc": "[full_deck[i] for i in card_idx if card_text[i] in $att and full_deck[i] in players[attacker_seat - 1].hand]"
            }
          }
        },
        {
          "set": {
            "key": "attack_ok",
            "value": {
              "calc": "len(attack_cards) >= min_attack_cards and len(attack_cards) <= max_attack_cards and len(attack_cards) <= players[2 - attacker_seat].hand_count and all(int(c / 10) == int(attack_cards[0] / 10) for c in attack_cards)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "the attack is laid",
      "do": [
        {
          "set": {
            "key": "attack_cards",
            "value": {
              "calc": "[min(players[attacker_seat - 1].hand)]"
            },
            "if": {
              "calc": "not attack_ok and len(players[attacker_seat - 1].hand) > 0"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "attacker_seat"
            },
            "key": "hand",
            "value": {
              "calc": "[c for c in players[attacker_seat - 1].hand if c not in attack_cards]"
            }
          }
        },
        {
          "set": {
            "key": "defence_ok",
            "value": false
          }
        }
      ],
      "text": "Seat {attacker_seat} attacks with {attack_cards}."
    },
    {
      "use": "ask",
      "phase": "bout",
      "label": "defence",
      "to": {
        "where": "you.seat != attacker_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 20
      },
      "verify": {
        "bind": "dfn"
      },
      "text": "You defend against {attack_cards}. Trump is {trump}. Say TAKE, or for each attack card name one different card from your hand that beats it, as 'defence card beats attack card' (e.g. '94 beats 91, 133 beats 101'). A card beats another of the same suit and lower rank, or any non-trump if it is trump. An illegal or incomplete defence counts as TAKE."
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "legal defence",
      "when": {
        "prose": "The defender named exactly one different card from the defender's own hand for each card in attack_cards, and each named card beats its paired attack card: it is the same suit and of higher rank, or it is of the trump suit while the attack card is not."
      },
      "do": [
        {
          "set": {
            "key": "defence_cards",
            "value": {
              "calc": "[full_deck[i] for i in card_idx if card_text[i] in $dfn and full_deck[i] in players[2 - attacker_seat].hand]"
            }
          }
        },
        {
          "set": {
            "key": "defence_ok",
            "value": {
              "calc": "len(defence_cards) == len(attack_cards)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "resolve",
      "do": [
        {
          "set": {
            "key": "defence_cards",
            "value": [],
            "if": {
              "calc": "not defence_ok"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - attacker_seat"
            },
            "key": "hand",
            "value": {
              "calc": "[c for c in players[2 - attacker_seat].hand if c not in defence_cards]"
            },
            "if": {
              "calc": "defence_ok"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + attack_cards + defence_cards"
            },
            "if": {
              "calc": "defence_ok"
            },
            "text": "Defence succeeds: attack {attack_cards} beaten by {defence_cards}. All are discarded."
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - attacker_seat"
            },
            "key": "hand",
            "value": {
              "calc": "players[2 - attacker_seat].hand + attack_cards"
            },
            "if": {
              "calc": "not defence_ok"
            },
            "text": "Seat {player} takes {attack_cards}."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "attacker_seat",
            "value": {
              "calc": "3 - attacker_seat"
            },
            "if": {
              "calc":
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_text` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_idx` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `attack_ok` is never changed in 3 random matches, so nothing updates it. Steps that name it: start of deal, legal attack, resolve. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "offered_trump_duel_durak",
    "name": "Offered-Trump Duel Durak",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Durak over 4 deals: the attacker offers two suits, the defender picks trump, and whoever is left holding cards takes penalty points."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_text",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_idx",
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
        "key": "deal_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "bout_counter",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attacker_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "offer",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "attack_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "defence_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "defence_ok",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "lowest_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "highest_rank",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "hand_size_dealt",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cards_set_aside",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "max_bouts_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "max_rounds_total",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "min_attack_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_attack_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "suits_offered",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "suit_code_clubs",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "suit_code_diamonds",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "suit_code_hearts",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "suit_code_spades",
        "visible": "public",
        "type": "number",
        "initial": 4
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "reset penalties",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "penalty",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "reset counters",
      "do": [
        {
          "set": {
            "key": "deal_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "bout_counter",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "attacker_seat",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "build the card list",
      "do": [
        {
          "set": {
            "key": "card_idx",
            "value": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
          }
        },
        {
          "set": {
            "key": "full_deck",
            "value": {
              "calc": "[(lowest_rank + int(i / suits)) * 10 + i - int(i / suits) * suits + 1 for i in card_idx]"
            }
          }
        },
        {
          "set": {
            "key": "card_text",
            "value": ["61", "62", "63", "64", "71", "72", "73", "74", "81", "82", "83", "84", "91", "92", "93", "94", "101", "102", "103", "104", "111", "112", "113", "114", "121", "122", "123", "124", "131", "132", "133", "134", "141", "142", "143", "144"]
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "start of deal",
      "when": {
        "calc": "bout_counter == 0"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
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
            "key": "discard",
            "value": []
          }
        },
        {
          "set": {
            "key": "offer",
            "value": []
          }
        },
        {
          "set": {
            "key": "trump",
            "value": ""
          }
        },
        {
          "set": {
            "key": "attack_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "defence_cards",
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
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "attacker_seat",
            "value": {
              "calc": "1 if deal_number in [1, 3] else 2"
            }
          }
        }
      ],
      "text": "Deal {deal_number} of {deals} begins. Each player is dealt {hand_size_dealt} cards; {cards_set_aside} cards are set aside unused. Seat {attacker_seat} is the first attacker."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Your current state:"
    },
    {
      "use": "ask",
      "phase": "deal",
      "label": "the offer",
      "when": {
        "calc": "bout_counter == 0"
      },
      "to": {
        "where": "you.seat == attacker_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Clubs+Diamonds",
          "Clubs+Hearts",
          "Clubs+Spades",
          "Diamonds+Hearts",
          "Diamonds+Spades",
          "Hearts+Spades"
        ]
      },
      "verify": {
        "bind": "offer_pick"
      },
      "text": "You are the first attacker of deal {deal_number}. Offer two different suits; your opponent will pick one of them as trump for the whole deal."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "set the offer",
      "when": {
        "calc": "bout_counter == 0"
      },
      "do": [
        {
          "set": {
            "key": "offer",
            "value": {
              "calc": "['Clubs', 'Diamonds'] if $offer_pick == 'Clubs+Diamonds' else (['Clubs', 'Hearts'] if $offer_pick == 'Clubs+Hearts' else (['Clubs', 'Spades'] if $offer_pick == 'Clubs+Spades' else (['Diamonds', 'Hearts'] if $offer_pick == 'Diamonds+Hearts' else (['Diamonds', 'Spades'] if $offer_pick == 'Diamonds+Spades' else ['Hearts', 'Spades']))))"
            }
          }
        }
      ],
      "text": "Seat {attacker_seat} offers {offer} as trump."
    },
    {
      "use": "ask",
      "phase": "deal",
      "label": "the trump choice",
      "when": {
        "calc": "bout_counter == 0"
      },
      "to": {
        "where": "you.seat != attacker_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "offer"
        }
      },
      "verify": {
        "bind": "trump_pick"
      },
      "text": "You are the first defender. Pick one of the offered suits {offer} as trump for the whole deal."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "set the trump",
      "when": {
        "calc": "bout_counter == 0"
      },
      "do": [
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "$trump_pick if $trump_pick in offer else offer[0]"
            }
          }
        }
      ],
      "text": "Trump for deal {deal_number} is {trump}."
    },
    {
      "use": "ask",
      "phase": "bout",
      "label": "attack",
      "to": {
        "where": "you.seat == attacker_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 10
      },
      "verify": {
        "bind": "att"
      },
      "text": "You attack. Trump is {trump}. Name {min_attack_cards} to {max_attack_cards} card codes from your hand, all of the same rank, separated by spaces (e.g. '91 93'), and no more cards than the defender holds. A code is rank*10+suit (1 Clubs, 2 Diamonds, 3 Hearts, 4 Spades). An illegal attack is replaced by your single lowest card."
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "legal attack",
      "when": {
        "prose": "Every card the attacker named is in the attacker's hand, all named cards share one rank, and there are between 1 and 3 of them, no more than the defender's hand_count."
      },
      "do": [
        {
          "set": {
            "key": "attack_cards",
            "value": {
              "calc": "[full_deck[i] for i in card_idx if card_text[i] in $att and full_deck[i] in players[attacker_seat - 1].hand]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "the attack is laid",
      "do": [
        {
          "set": {
            "key": "attack_cards",
            "value": {
              "calc": "[min(players[attacker_seat - 1].hand)]"
            },
            "if": {
              "calc": "len(players[attacker_seat - 1].hand) > 0 and (len(attack_cards) < min_attack_cards or len(attack_cards) > max_attack_cards or len(attack_cards) > players[2 - attacker_seat].hand_count or any(int(c / 10) != int(attack_cards[0] / 10) for c in attack_cards))"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "attacker_seat"
            },
            "key": "hand",
            "value": {
              "calc": "[c for c in players[attacker_seat - 1].hand if c not in attack_cards]"
            }
          }
        },
        {
          "set": {
            "key": "defence_ok",
            "value": false
          }
        }
      ],
      "text": "Seat {attacker_seat} attacks with {attack_cards}."
    },
    {
      "use": "ask",
      "phase": "bout",
      "label": "defence",
      "to": {
        "where": "you.seat != attacker_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 20
      },
      "verify": {
        "bind": "dfn"
      },
      "text": "You defend against {attack_cards}. Trump is {trump}. Say TAKE, or for each attack card name one different card from your hand that beats it, as 'defence card beats attack card' (e.g. '94 beats 91, 133 beats 101'). A card beats another of the same suit and lower rank, or any non-trump if it is trump. An illegal or incomplete defence counts as TAKE."
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "legal defence",
      "when": {
        "prose": "The defender named exactly one different card from the defender's own hand for each card in attack_cards, and each named card beats its paired attack card: it is the same suit and of higher rank, or it is of the trump suit while the attack card is not."
      },
      "do": [
        {
          "set": {
            "key": "defence_cards",
            "value": {
              "calc": "[full_deck[i] for i in card_idx if card_text[i] in $dfn and full_deck[i] in players[2 - attacker_seat].hand]"
            }
          }
        },
        {
          "set": {
            "key": "defence_ok",
            "value": {
              "calc": "len(defence_cards) == len(attack_cards)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "resolve",
      "do": [
        {
          "set": {
            "key": "defence_cards",
            "value": [],
            "if": {
              "calc": "not defence_ok"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - attacker_seat"
            },
            "key": "hand",
            "value": {
              "calc": "[c for c in players[2 - attacker_seat].hand if c not in defence_cards]"
            },
            "if": {
              "calc": "defence_ok"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + attack_cards + defence_cards"
            },
            "if": {
              "calc": "defence_ok"
            },
            "text": "Defence succeeds: attack {attack_cards} beaten by {defence_cards}. All are discarded."
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - attacker_seat"
            },
            "key": "hand",
            "value": {
              "calc": "players[2 - attacker_seat].hand + attack_cards"
            },
            "if": {
              "calc": "not defence_ok"
            },
            "text": "Seat {player} takes {attack_cards}."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "attacker_seat",
            "value": {
              "calc": "3 - attacker_seat"
            },
            "if": {
              "calc": "defence_ok"
            }
          }
        },
        {
          "set": {
            "key": "attack_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "defence_cards",
            "value": []
          }
        },
        {
          "adjust": {
            "key": "bout_counter",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        }
      ],
      "text": "Bout resolved (defence succeeded: {defence_ok}). Hand sizes: seat 1 {players[0].hand_count}, seat 2 {players[1].hand_count}. Bouts this deal: {bout_counter}. Next attacker: seat {attacker_seat}."
    },
    {
      "use": "update",
      "phase": "bout",
      "label": "end of deal",
      "when": {
        "calc": "bout_counter >= max_bouts_per_deal or round_number >= max_rounds_total or min(p.hand_count for p in players) == 0"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "penalty",
            "value": {
              "calc": "you.hand_count if min(p.hand_count for p in players) == 0 else you.hand_count - min(p.hand_count for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "deal_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "bout_counter",
            "value": 0
          }
        }
      ],
      "text": "The deal is over. Penalty totals: seat 1 {players[0].penalty}, seat 2 {players[1].penalty}."
    },
    {
      "use": "check",
      "phase": "bout",
      "label": "is the game over",
      "when": {
        "calc": "deal_number > deals or round_number >= max_rounds_total"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "deal_number > deals or round_number >= max_rounds_total"
      },
      "rank_by": "0 - you.penalty",
      "text": "Winner: {result}. Final penalties: Seat 1 {players[0].penalty}, Seat 2 {players[1].penalty} (lower is better)."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {deck_size} cards: four suits (Clubs, Diamonds, Hearts, Spades), each with ranks 6, 7, 8, 9, 10, J (11), Q (12), K (13), A (14). A card is written as a code, rank*10+suit code, with suit codes Clubs {suit_code_clubs}, Diamonds {suit_code_diamonds}, Hearts {suit_code_hearts}, Spades {suit_code_spades}: 61 is the 6 of Clubs, 144 the Ace of Spades. Suit order, used only to break ties, is Clubs, Diamonds, Hearts, Spades.\n\nBEATING. Once a trump suit is set, card X beats card Y if (a) X is the same suit as Y and of higher rank, or (b) X is a trump and Y is not. Nothing else beats.\n\nSTRUCTURE. The game has {deals} deals. Each round is one bout. There are at most {max_bouts_per_deal} bouts per deal and at most {max_rounds_total} rounds in total. Seat 1 is the first attacker in deals 1 and 3; seat 2 is the first attacker in deals 2 and 4. The other player is the first defender.\n\nSTARTING A DEAL. S1: all {deck_size} cards are shuffled and each player is dealt {hand_size_dealt} cards face down; only the owner sees their hand. The remaining {cards_set_aside} cards are set aside, unseen and unused this deal. S2: the first attacker names {suits_offered} different suits; if the answer is not two different suits, the offer is Hearts and Spades. The offer is announced. S3: the first defender picks one of the two offered suits; it is trump for the whole deal and is announced. If the answer is not an offered suit, the first suit offered becomes trump.\n\nA BOUT. 1. ATTACK: the attacker places {min_attack_cards} to {max_attack_cards} cards from their hand face up, all of the same rank, and never more cards than the defender holds. A legal attack is played as named. An illegal attack (a card not in hand, mixed ranks, or too many cards) is replaced by the attacker's single lowest-ranked card, ties going to the earliest suit in suit order. The attack is announced. 2. DEFENCE: the defender either says TAKE, or names one different card from their hand for each attack card, saying which attack card each one beats. Every pairing must be a legal beat. If it is, the defence succeeds; any illegal or incomplete defence counts as TAKE. 3. RESOLVE: if the defence succeeded, all attack and defence cards are discarded face up, out of play, and the defender becomes the attacker for the next bout. If the defender took, the attack cards go into the defender's hand and the same player attacks again next bout. The cards played, the result and both hand sizes are announced, and the bout counter rises by 1.\n\nENDING A DEAL. After a bout resolves, the deal ends if either player has no cards or the bout counter has reached {max_bouts_per_deal}. If exactly one player has no cards, the other player (the durak) adds the number of cards in their hand to their penalty total. If both have no cards, nobody scores. If the deal ended at {max_bouts_per_deal} bouts with both holding cards, the player with more cards adds the difference in hand sizes to their penalty; equal hands score nothing. The next deal then starts with its bout counter at 0.\n\nENDING THE GAME. The game ends when deal {deals} has ended. If round {max_rounds_total} finishes during a deal, that deal is scored as if it had reached its bout cap. The player with the lower total penalty wins; equal totals are a draw (a shared win)."
}
```
````
