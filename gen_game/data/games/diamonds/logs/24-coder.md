# 24 coder

- time: 2026-10-27T18:40:19+00:00 (194.0s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 17c0687f76ea45be, reply sha256 0f1ce6319c6d73c4

## Sent

````
# Task: write the XColos game file for "Diamonds: Three-Hand Vault"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

COMPONENTS: A deck of 32 cards with 4 suits (Diamonds, Hearts, Spades, Clubs) and ranks 1 to 8 in each suit. Each player has a showroom and a vault, each holding crystals and each starting at 0. The supply of crystals is unlimited. Seats are numbered 1, 2 and 3 clockwise; 'left' means the next seat clockwise.

STRUCTURE: The game is 3 hands of 7 tricks, which is 21 rounds; one round is one trick. In hand 1 the dealer is seat 1, in hand 2 seat 2, and in hand 3 seat 3.

START OF EACH HAND (on trick 1 of the hand): Shuffle all 32 cards and deal 7 to each player face down; the remaining 11 cards are set aside unseen for the hand. Each player privately sees only their own hand. Shown to each player, a hand is listed sorted by suit (Diamonds, Hearts, Spades, Clubs) and then by ascending rank. Then all players at the same moment secretly choose exactly 1 card from their hand to pass to the player on their left. All passes are exchanged at once, and passed cards are not revealed to the third player. Every player's per-hand count of won cards in each suit is reset to 0, and so is their tricks-won count.

PLAYING A TRICK: On trick 1 of a hand, the player left of the dealer leads; on later tricks, the winner of the previous trick leads. The leader plays any card from their hand, and its suit is the led suit. The other two players then play one card each, in clockwise order. A player who holds a card of the led suit must play one. A player who holds no card of the led suit may play any card, and immediately takes the action of the suit of the card they played (see SUIT ACTIONS), resolved before the next player plays. All played cards are shown to everyone.

WINNING A TRICK: The highest-ranked card of the led suit wins the trick, and off-suit cards never win. The winner takes all 3 cards face down, adds 1 to their tricks-won count, and adds the number of cards of each suit in the trick to their won-card count for that suit. The winner then takes the action of the led suit once, and leads the next trick.

SUIT ACTIONS:
- Diamonds: move 1 crystal from the supply to your vault.
- Hearts: move 1 crystal from the supply to your showroom.
- Spades: move 1 crystal from your own showroom to your own vault. If your showroom is empty, nothing happens.
- Clubs: move 1 crystal from the showroom of the opponent whose showroom is largest into your own showroom. If both opponents tie for largest, take it from the tied opponent who sits first clockwise after you. If both opponents' showrooms are empty, nothing happens.
Every action and its result is announced to all players.

END OF HAND (after trick 7): For each suit in the order Diamonds, Hearts, Spades, Clubs, the player with strictly the most won cards of that suit takes that suit's action once; if the top count is tied, no one takes it. Then every player whose tricks-won count for the hand is 0 takes the Diamonds action twice. The dealer passes to the left for the next hand. Resolve all end-of-hand actions in the order given.

VISIBILITY: Showroom counts are always displayed. Vault counts are not displayed in score summaries, but every action that changes a vault is announced, so they can be tracked. Hands, passed cards and the 11 set-aside cards are hidden.

SCORING: At the end of hand 3, each player's score is 2 times their vault crystals plus their showroom crystals.

How the winner is decided: The player with the highest score after 3 hands wins. If two or more players tie for highest score, the tied player with more vault crystals wins. If they are still tied, the game is a draw between them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Diamonds: Three-Hand Vault (3 to 3 players, best with 3)

A three-player trick-taking game over 3 hands of 7 tricks. Winning tricks, and playing off-suit, trigger suit actions that move crystals into your showroom (worth 1 each) and your vault (worth 2 each).

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards held, as text such as 'D7' (suit letter D/H/S/C, then rank 1-8). Shown to the owner sorted by suit D,H,S,C, then by ascending rank.
  - each player: pass_card (text, starts ''); only its owner sees it. The card this player chose to pass left at the start of the hand.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played to the current trick.
  - each player: showroom (number, starts 0); everyone sees it. Crystals in the showroom, always displayed.
  - each player: vault (number, starts 0); everyone sees it. Crystals in the vault. It is left out of score summaries, but every change to it is announced.
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won this hand. Reset to 0 at the start of each hand.
  - each player: won_diamonds (number, starts 0); only its owner sees it. Diamond cards won this hand. Reset each hand.
  - each player: won_hearts (number, starts 0); only its owner sees it. Heart cards won this hand. Reset each hand.
  - each player: won_spades (number, starts 0); only its owner sees it. Spade cards won this hand. Reset each hand.
  - each player: won_clubs (number, starts 0); only its owner sees it. Club cards won this hand. Reset each hand.
  - each player: score (number, starts 0); everyone sees it. Final score: 2 * vault + showroom, computed at the end of hand 3.
  - the table: deck (list, starts 'all 32 cards D1..D8, H1..H8, S1..S8, C1..C8'); hidden from all players. The undealt deck during dealing.
  - the table: set_aside (list, starts []); hidden from all players. The 11 cards left after the deal, unseen for the hand.
  - the table: hand_number (number, starts 1); everyone sees it. Current hand, from 1 to 3.
  - the table: trick_number (number, starts 1); everyone sees it. Current trick within the hand, from 1 to 7.
  - the table: rounds_played (number, starts 0); everyone sees it. Tricks completed in total, from 0 to 21.
  - the table: dealer_seat (number, starts 1); everyone sees it. Dealer this hand (equals hand_number).
  - the table: leader_seat (number, starts 2); everyone sees it. Seat that leads the current trick.
  - the table: led_suit (text, starts ''); everyone sees it. Suit letter of the led card.
  - the table: trick_cards (list, starts []); everyone sees it. Cards played to the current trick, in play order.
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the current trick.
  - parameters, each kept as a table attribute: deck_size = 32, suits = 4, ranks_per_suit = 8, lowest_rank = 1, highest_rank = 8, hands = 3, tricks_per_hand = 7, total_rounds = 21, cards_dealt_per_player = 7, cards_set_aside = 11, cards_passed_per_player = 1, cards_per_trick = 3, crystals_per_action = 1, zero_trick_diamond_actions = 2, vault_weight = 2, showroom_weight = 1, starting_showroom = 0, starting_vault = 0, rank_tiebreak_multiplier = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 sit clockwise; the left of seat s is seat (s mod 3) + 1.
  2. Every player's showroom and vault start at 0, and score at 0.
  3. Set hand_number = 1, trick_number = 1, rounds_played = 0, dealer_seat = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: When trick_number == 1: deck = all 32 cards; set_aside = []; every player's hand = []; dealer_seat = hand_number; leader_seat = (dealer_seat mod 3) + 1; reset each player's tricks_won, won_diamonds, won_hearts, won_spades and won_clubs to 0. Announce the new hand and its dealer.
  2. [initialize] all players. What happens: When trick_number == 1: deal 7 cards to each player, each one a random draw removed from deck and appended to that player's hand. Then move the remaining 11 deck cards to set_aside.
  3. [sync] all players. What happens: When trick_number == 1: each player privately sees their own hand, sorted by suit D,H,S,C and then by ascending rank.
  4. [poll] all players answers: one card from your own hand. What happens: When trick_number == 1: store the answer in pass_card. Nobody sees another player's choice.
  5. [update] all players. What happens: When trick_number == 1: at once, for each seat s, remove pass_card from s.hand and append it to the hand of seat (s mod 3) + 1. Each receiver is told privately which card they received; the third player is not told.
  6. [sync] all players. What happens: When trick_number == 1: each player sees their updated sorted hand.
  7. [update] table. What happens: trick_cards = []; every played_card = ''.
  8. [ask] seat leader_seat answers: any card from your hand. What happens: Remove the card from hand; played_card = the card; append it to trick_cards; led_suit = its suit letter. Announce the card to all.
  9. [ask] seat (leader_seat mod 3) + 1 answers: a card from your hand of led_suit if you hold one, otherwise any card from your hand. What happens: Remove the card from hand; played_card = the card; append it to trick_cards; announce it to all.
  10. [update] seat (leader_seat mod 3) + 1. What happens: If that seat's played_card suit != led_suit, the seat takes the action of the played card's suit (see rules R14-R17) at once. Announce the action and its result.
  11. [ask] seat ((leader_seat + 1) mod 3) + 1 answers: a card from your hand of led_suit if you hold one, otherwise any card from your hand. What happens: Remove the card from hand; played_card = the card; append it to trick_cards; announce it to all.
  12. [update] seat ((leader_seat + 1) mod 3) + 1. What happens: If that seat's played_card suit != led_suit, the seat takes the action of the played card's suit at once. Announce the action and its result.
  13. [update] table. What happens: trick_winner = the seat whose played_card has suit == led_suit and the highest rank. The winner gets tricks_won += 1, and for each suit, won_<suit> += the count of that suit in trick_cards. The winner then takes the action of led_suit once. Announce the winner, the action and its result.
  14. [update] table. What happens: When trick_number == 7, end of hand, resolved in order: for suit in Diamonds, Hearts, Spades, Clubs, if exactly one player has the strictly highest won_<suit>, that player takes that suit's action once. Then each player with tricks_won == 0 takes the Diamonds action twice (vault += 2). Announce every action.
  15. [update] all players. What happens: When trick_number == 7 and hand_number == 3: score = 2 * vault + showroom. Announce scores and vaults.
  16. [update] table. What happens: rounds_played += 1. If trick_number == 7, then hand_number += 1 and trick_number = 1; otherwise trick_number += 1 and leader_seat = trick_winner.
  17. [check] table. What happens: End the game if rounds_played >= 21; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player's showroom and vault are 0.
  R2. When a hand starts, all 32 cards are shuffled, each player receives 7 cards into their hand, and the other 11 go to set_aside, unseen.
  R3. When a hand starts, each player simultaneously passes exactly 1 card from their hand to the seat on their left, and the third player is not told which card was passed.
  R4. When a hand starts, every player's tricks_won and won_diamonds, won_hearts, won_spades and won_clubs are reset to 0.
  R5. In hand h, the dealer is seat h (hand 1: seat 1, hand 2: seat 2, hand 3: seat 3).
  R6. On trick 1 of a hand, the seat left of the dealer leads; on later tricks, the previous trick's winner leads.
  R7. When the leader plays a card, its suit becomes led_suit, and the other two players then play in clockwise order.
  R8. When a player holds a card of led_suit, they may only play a card of led_suit.
  R9. When a non-leader holds no card of led_suit, they may play any card, and they immediately take that card's suit action before the next player plays.
  R10. When all 3 cards are played, the highest-ranked card of led_suit wins the trick, and an off-suit card never wins.
  R11. When a player wins a trick, their tricks_won increases by 1, and each won_<suit> increases by the number of that suit among the 3 trick cards.
  R12. When a player wins a trick, they take the action of led_suit once and lead the next trick.
  R13. When the Diamonds action is taken, the taker's vault increases by 1 from the supply.
  R14. When the Hearts action is taken, the taker's showroom increases by 1 from the supply.
  R15. When the Spades action is taken and the taker's showroom >= 1, their showroom decreases by 1 and their vault increases by 1; when their showroom is 0, nothing happens.
  R16. When the Clubs action is taken, 1 crystal moves from the opponent with the largest showroom into the taker's showroom; if both opponents' showrooms are 0, nothing happens.
  R17. When the Clubs action is taken and both opponents tie for the largest showroom (above 0), the crystal is taken from the tied opponent seated first clockwise after the taker.
  R18. When trick 7 of a hand ends, for each suit in the order Diamonds, Hearts, Spades, Clubs, the single player with strictly the most won cards of that suit takes that suit's action once; if the top count is tied, nobody takes it.
  R19. When trick 7 of a hand ends, after the suit-majority actions, each player with tricks_won == 0 takes the Diamonds action twice (vault += 2).
  R20. When hand 3 ends (after 21 tricks), each player's score = 2 * vault + showroom, and the game ends.
  R21. When the game ends, the highest score wins; a tie is broken by the larger vault; players still tied share the win as a draw.
  R22. When a card is played or a suit action resolves, the card and the action's result are announced to all players, and showroom counts are always public.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Pass a card (start of each hand) | asked: all players simultaneously | options: every card currently in your own hand (7 cards)
  - Lead a card | asked: seat leader_seat | options: every card in your hand
  - Follow to the trick | asked: the second and third seats clockwise from the leader | options: if you hold at least one card of led_suit: only your cards of led_suit; otherwise: every card in your hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: rounds_played >= 21
  - each player's standing: you.score * 1000 + you.vault (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest score (2 * vault + showroom) after 3 hands wins. A tie on score is broken by more vault crystals. Players still tied share the win, which is the draw.
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

- each player: `showroom` (number, visible: public, starts 0): Crystals in the showroom, always displayed.
- each player: `vault` (number, visible: public, starts 0): Crystals in the vault. It is left out of score summaries, but every change to it is announced.
- each player: `score` (number, visible: public, starts 0): Final score: 2 * vault + showroom, computed at the end of hand 3.
- the table: `hand_number` (number, visible: public, starts 1): Current hand, from 1 to 3.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 32, suits = 4, ranks_per_suit = 8, lowest_rank = 1, highest_rank = 8, hands = 3, tricks_per_hand = 7, total_rounds = 21, cards_dealt_per_player = 7, cards_set_aside = 11, cards_passed_per_player = 1, cards_per_trick = 3, crystals_per_action = 1, zero_trick_diamond_actions = 2, vault_weight = 2, showroom_weight = 1, starting_showroom = 0, starting_vault = 0, rank_tiebreak_multiplier = 1000
- the game ends with ONE ending whose `rank_by` is `you.score * 1000 + you.vault`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
{
  "schema": 1,
  "meta": {
    "id": "diamonds_three_hand_vault",
    "name": "Diamonds: Three-Hand Vault",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three hands of seven tricks: win tricks and play off-suit to move crystals into your showroom (1 point each) and vault (2 points each)."
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
        "key": "pass_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "received_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "showroom",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "vault",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_diamonds",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_hearts",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_spades",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_clubs",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "card_order",
        "visible": "none",
        "type": "list",
        "initial": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
      },
      {
        "key": "set_aside",
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
        "key": "actor",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "act_suit",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "victim",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rounds_played",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dealer_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 32
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
        "initial": 8
      },
      {
        "key": "lowest_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "highest_rank",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "cards_set_aside",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "cards_passed_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cards_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "crystals_per_action",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "zero_trick_diamond_actions",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "vault_weight",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "showroom_weight",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_showroom",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_vault",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rank_tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the table is set",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "showroom",
            "value": {
              "calc": "starting_showroom"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "vault",
            "value": {
              "calc": "starting_vault"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "rounds_played",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dealer_seat",
            "value": {
              "calc": "hand_number"
            }
          }
        }
      ],
      "text": "Seats 1, 2 and 3 sit clockwise. Every showroom and vault starts empty."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "a new hand",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "card_order"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "dealer_seat",
            "value": {
              "calc": "hand_number"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "dealer_seat % 3 + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_diamonds",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_hearts",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_spades",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_clubs",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "received_card",
            "value": ""
          }
        }
      ],
      "text": "Hand {hand_number} of {hands} begins. Seat {dealer_seat} deals; seat {leader_seat} will lead the first trick."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[c for c in card_order if c in you.hand]"
            }
          }
        }
      ],
      "text": "Each player is dealt {cards_dealt_per_player} cards face down; the other {cards_set_aside} cards are set aside unseen for this hand."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "all",
      "mode": "self",
      "fields": [
        "hand"
      ],
      "text": "Your hand, sorted by suit (D, H, S, C) and rank:"
    },
    {
      "use": "poll",
      "phase": "pass",
      "label": "pass a card",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "pass_card",
      "text": "Choose exactly one card from your hand to pass face down to the player on your left (seat 1 passes to 2, 2 to 3, 3 to 1). All passes happen at once and the third player never sees your card."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "the passes are exchanged",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "received_card",
            "value": {
              "calc": "[p.pass_card for p in players if p.seat % 3 + 1 == you.seat][0]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pass_card"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.received_card"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[c for c in card_order if c in you.hand]"
            }
          }
        }
      ],
      "text": "Every player passes one card to the left at the same moment."
    },
    {
      "use": "sync",
      "phase": "pass",
      "label": "your hand after the pass",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "all",
      "mode": "self",
      "fields": [
        "hand",
        "received_card"
      ],
      "text": "The card you received from your right and your hand now:"
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "clear the trick",
      "do": [
        {
          "set": {
            "key": "trick_cards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        }
      ],
      "text": "Hand {hand_number}, trick {trick_number} of {tricks_per_hand}. Seat {leader_seat} leads."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "lead a card",
      "to": {
        "where": "you.seat == leader_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "players[leader_seat - 1].played_card[0]"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_suit] if any(c[0] == led_suit for c in you.hand) else you.hand"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "You lead this trick. Play any card from your hand; its suit becomes the led suit."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second seat follows",
      "to": {
        "where": "you.seat == leader_seat % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "The led suit is {led_suit}. You are offered only the cards you may play: your {led_suit} cards if you hold any, otherwise any card. Playing off-suit gives you that card's suit action at once."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second seat off-suit action",
      "when": {
        "calc": "players[leader_seat % 3].played_card[0] != led_suit"
      },
      "do": [
        {"set": {"key": "actor", "value": {"calc": "leader_seat % 3 + 1"}}},
        {"set": {"key": "act_suit", "value": {"calc": "players[actor - 1].played_card[0]"}}},
        {"set": {"key": "victim", "value": {"calc": "0 if act_suit != 'C' else (0 if max(players[actor % 3].showroom, players[(actor + 1) % 3].showroom) == 0 else (actor % 3 + 1 if players[actor % 3].showroom >= players[(actor + 1) % 3].showroom else (actor + 1) % 3 + 1))"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'D'"}, "text": "Diamonds action: seat {player} moves {crystals_per_action} crystal from the supply to their vault."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'H'"}, "text": "Hearts action: seat {player} moves {crystals_per_action} crystal from the supply to their showroom."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": 0, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom < crystals_per_action"}, "text": "Spades action: seat {player}'s showroom is empty, so nothing happens."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}, "text": "Spades action: seat {player} moves {crystals_per_action} crystal from their showroom to their vault."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}}},
        {"adjust": {"player": {"calc": "victim"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}, "text": "Clubs action: seat {actor} takes {crystals_per_action} crystal from seat {player}'s showroom into their own showroom."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": 0, "if": {"calc": "act_suit == 'C' and victim == 0"}, "text": "Clubs action: both opponents of seat {player} have empty showrooms, so nothing happens."}}
      ],
      "text": "Seat {actor} played off-suit and takes the {act_suit} action."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third seat follows",
      "to": {
        "where": "you.seat == (leader_seat + 1) % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "The led suit is {led_suit}; cards played so far: {trick_cards}. You are offered only the cards you may play: your {led_suit} cards if you hold any, otherwise any card. Playing off-suit gives you that card's suit action at once."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "third seat off-suit action",
      "when": {
        "calc": "players[(leader_seat + 1) % 3].played_card[0] != led_suit"
      },
      "do": [
        {"set": {"key": "actor", "value": {"calc": "(leader_seat + 1) % 3 + 1"}}},
        {"set": {"key": "act_suit", "value": {"calc": "players[actor - 1].played_card[0]"}}},
        {"set": {"key": "victim", "value": {"calc": "0 if act_suit != 'C' else (0 if max(players[actor % 3].showroom, players[(actor + 1) % 3].showroom) == 0 else (actor % 3 + 1 if players[actor % 3].showroom >= players[(actor + 1) % 3].showroom else (actor + 1) % 3 + 1))"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'D'"}, "text": "Diamonds action: seat {player} moves {crystals_per_action} crystal from the supply to their vault."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'H'"}, "text": "Hearts action: seat {player} moves {crystals_per_action} crystal from the supply to their showroom."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": 0, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom < crystals_per_action"}, "text": "Spades action: seat {player}'s showroom is empty, so nothing happens."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}, "text": "Spades action: seat {player} moves {crystals_per_action} crystal from their showroom to their vault."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}}},
        {"adjust": {"player": {"calc": "victim"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}, "text": "Clubs action: seat {actor} takes {crystals_per_action} crystal from seat {player}'s showroom into their own showroom."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": 0, "if": {"calc": "act_suit == 'C' and victim == 0"}, "text": "Clubs action: both opponents of seat {player} have empty showrooms, so nothing happens."}}
      ],
      "text": "Seat {actor} played off-suit and takes the {act_suit} action."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is won",
      "do": [
        {"set": {"key": "trick_winner", "value": {"calc": "[p.seat for p in players if p.played_card[0] == led_suit and int(p.played_card[1]) == max([int(q.played_card[1]) for q in players if q.played_card[0] == led_suit])][0]"}}},
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "tricks_won", "value": 1}},
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "won_diamonds", "value": {"calc": "count(c[0] == 'D' for c in trick_cards)"}}},
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "won_hearts", "value": {"calc": "count(c[0] == 'H' for c in trick_cards)"}}},
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "won_spades", "value": {"calc": "count(c[0] == 'S' for c in trick_cards)"}}},
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "won_clubs", "value": {"calc": "count(c[0] == 'C' for c in trick_cards)"}}},
        {"set": {"key": "actor", "value": {"calc": "trick_winner"}}},
        {"set": {"key": "act_suit", "value": {"calc": "led_suit"}}},
        {"set": {"key": "victim", "value": {"calc": "0 if act_suit != 'C' else (0 if max(players[actor % 3].showroom, players[(actor + 1) % 3].showroom) == 0 else (actor % 3 + 1 if players[actor % 3].showroom >= players[(actor + 1) % 3].showroom else (actor + 1) % 3 + 1))"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'D'"}, "text": "Diamonds action: seat {player} moves {crystals_per_action} crystal from the supply to their vault."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'H'"}, "text": "Hearts action: seat {player} moves {crystals_per_action} crystal from the supply to their showroom."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": 0, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom < crystals_per_action"}, "text": "Spades action: seat {player}'s showroom is empty, so nothing happens."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}, "text": "Spades action: seat {player} moves {crystals_per_action} crystal from their showroom to their vault."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}}},
        {"adjust": {"player": {"calc": "victim"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}, "text": "Clubs action: seat {actor} takes {crystals_per_action} crystal from seat {player}'s showroom into their own showroom."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": 0, "if": {"calc": "act_suit == 'C' and victim == 0"}, "text": "Clubs action: both opponents of seat {player} have empty showrooms, so nothing happens."}}
      ],
      "text": "Trick {trick_number}: {trick_cards}. Seat {trick_winner} wins with the highest {led_suit} card, takes the cards and the {led_suit} action, and leads next."
    },
    {
      "use": "update",
      "phase": "end of hand",
      "label": "suit majorities and empty-handed players",
      "when": {
        "calc": "trick_number == tricks_per_hand"
      },
      "do": [
        {"set": {"key": "actor", "value": {"calc": "[p.seat for p in players if p.won_diamonds == max([q.won_diamonds for q in players])][0] if count(p.won_diamonds == max([q.won_diamonds for q in players]) for p in players) == 1 else 0"}}},
        {"set": {"key": "act_suit", "value": {"calc": "'D' if actor > 0 else ''"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'D'"}, "text": "Most Diamonds won: seat {player} takes the Diamonds action and moves {crystals_per_action} crystal from the supply to their vault."}},

        {"set": {"key": "actor", "value": {"calc": "[p.seat for p in players if p.won_hearts == max([q.won_hearts for q in players])][0] if count(p.won_hearts == max([q.won_hearts for q in players]) for p in players) == 1 else 0"}}},
        {"set": {"key": "act_suit", "value": {"calc": "'H' if actor > 0 else ''"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'H'"}, "text": "Most Hearts won: seat {player} takes the Hearts action and moves {crystals_per_action} crystal from the supply to their showroom."}},

        {"set": {"key": "actor", "value": {"calc": "[p.seat for p in players if p.won_spades == max([q.won_spades for q in players])][0] if count(p.won_spades == max([q.won_spades for q in players]) for p in players) == 1 else 0"}}},
        {"set": {"key": "act_suit", "value": {"calc": "'S' if actor > 0 else ''"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": 0, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom < crystals_per_action"}, "text": "Most Spades won: seat {player} takes the Spades action, but their showroom is empty, so nothing happens."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "vault", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}, "text": "Most Spades won: seat {player} takes the Spades action and moves {crystals_per_action} crystal from their showroom to their vault."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'S' and players[actor - 1].showroom >= crystals_per_action"}}},

        {"set": {"key": "actor", "value": {"calc": "[p.seat for p in players if p.won_clubs == max([q.won_clubs for q in players])][0] if count(p.won_clubs == max([q.won_clubs for q in players]) for p in players) == 1 else 0"}}},
        {"set": {"key": "act_suit", "value": {"calc": "'C' if actor > 0 else ''"}}},
        {"set": {"key": "victim", "value": {"calc": "0 if act_suit != 'C' else (0 if max(players[actor % 3].showroom, players[(actor + 1) % 3].showroom) == 0 else (actor % 3 + 1 if players[actor % 3].showroom >= players[(actor + 1) % 3].showroom else (actor + 1) % 3 + 1))"}}},
        {"adjust": {"player": {"calc": "victim"}, "key": "showroom", "value": {"calc": "-crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}, "text": "Most Clubs won: seat {actor} takes the Clubs action and takes {crystals_per_action} crystal from seat {player}'s showroom into their own showroom."}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": {"calc": "crystals_per_action"}, "if": {"calc": "act_suit == 'C' and victim > 0"}}},
        {"adjust": {"player": {"calc": "actor"}, "key": "showroom", "value": 0, "if": {"calc": "act_suit == 'C' and victim == 0"}, "text": "Most Clubs won: seat {player} takes the Clubs action, but both opponents' showrooms are empty, so nothing happens."}},

        {"adjust": {"players": {"where": "you.tricks_won == 0"}, "key": "vault", "value": {"calc": "zero_trick_diamond_actions * crystals_per_action"}, "text": "Seat {player} won no tricks this hand and takes the Diamonds action {zero_trick_diamond_actions} times: their vault grows by {value}."}}
      ],
      "text": "Hand {hand_number} is over. Suit majorities (Diamonds, Hearts, Spades, Clubs; ties give nothing), then players who won no tricks, take their actions."
    },
    {
      "use": "update",
      "phase": "end of hand",
      "label": "final scores",
      "when": {
        "calc": "trick_number == tricks_per_hand and hand_number == hands"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "vault_weight * you.vault + showroom_weight * you.showroom"
            },
            "text": "Seat {player} finishes with a score of {value}."
          }
        }
      ],
      "text": "The last hand is over. Each score is {vault_weight} x vault plus showroom."
    },
    {
      "use": "update",
      "phase": "end of trick",
      "label": "advance",
      "do": [
        {
          "adjust": {
            "key": "rounds_played",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "trick_winner"
            }
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": 1,
            "if": {
              "calc": "trick_number == tricks_per_hand and hand_number < hands"
            }
          }
        },
        {
          "set": {
            "key": "trick_number",
            "value": {
              "calc": "1 if trick_number == tricks_per_hand else trick_number + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end of trick",
      "label": "after the last trick",
      "when": {
        "calc": "rounds_played >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "rounds_played >= total_rounds"
      },
      "rank_by": "you.score * 1000 + you.vault",
      "text": "Winner: {result}. Final scores (vault): Seat 1 {players[0].score} ({players[0].vault}), Seat 2 {players[1].score} ({players[1].vault}), Seat 3 {players[2].score} ({players[2].vault})."
    }
  },
  "limits": {
    "rounds": 21,
    "rounds_max": 25,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "Three players, seats 1, 2 and 3 clockwise; 'left' means the next seat clockwise. The deck has {deck_size} cards: {suits} suits (Diamonds D, Hearts H, Spades S, Clubs C), ranks {lowest_rank} to {highest_rank}, written like D7. Each player has a showroom and a vault of crystals, starting at {starting_showroom} and {starting_vault}; the supply is unlimited. The game is {hands} hands of {tricks_per_hand} tricks ({total_rounds} tricks in all). In hand 1 the dealer is seat 1, in hand 2 seat 2, in hand 3 seat 3.\n\nSTART OF EACH HAND: all {deck_size} cards are shuffled and {cards_dealt_per_player} are dealt face down to each player; the remaining {cards_set_aside} cards are set aside unseen for the hand. You see only your own hand, sorted by suit (D, H, S, C) then ascending rank. Then all players at the same moment secretly choose exactly {cards_passed_per_player} card from their hand to pass to the player on their left. All passes are exchanged at once, and passed cards are not revealed to the third player. Every player's won-card counts per suit and tricks-won count are reset to 0.\n\nPLAYING A TRICK: on trick 1 of a hand the player left of the dealer leads; on later tricks the winner of the previous trick leads. The leader plays any card, and its suit is the led suit. The other two players then play one card each, in clockwise order. A player who holds a card of the led suit must play one (you are only offered those cards). A player who holds no card of the led suit may play any card, and immediately takes the action of the suit of the card they played, resolved before the next player plays. All played cards are shown to everyone.\n\nWINNING A TRICK: the highest-ranked card of the led suit wins the trick; off-suit cards never win. The winner takes all {cards_per_trick} cards, adds 1 to their tricks-won count, and adds the number of cards of each suit in the trick to their won-card count for that suit. The winner then takes the action of the led suit once, and leads the next trick.\n\nSUIT ACTIONS:\n- Diamonds: move {crystals_per_action} crystal from the supply to your vault.\n- Hearts: move {crystals_per_action} crystal from the supply to your showroom.\n- Spades: move {crystals_per_action} crystal from your own showroom to your own vault. If your showroom is empty, nothing happens.\n- Clubs: move {crystals_per_action} crystal from the showroom of the opponent whose showroom is largest into your own showroom. If both opponents tie for largest, take it from the tied opponent who sits first clockwise after you. If both opponents' showrooms are empty, nothing happens.\nEvery action and its result is announced to all players.\n\nEND OF HAND (after trick {tricks_per_hand}): for each suit in the order Diamonds, Hearts, Spades, Clubs, the player with strictly the most won cards of that suit takes that suit's action once; if the top count is tied, no one takes it. Then every player who won 0 tricks in the hand takes the Diamonds action {zero_trick_diamond_actions} times. The dealer passes to the left for the next hand.\n\nVISIBILITY: showroom counts are always displayed; every change to a vault is announced. Hands, passed cards and the set-aside cards are hidden.\n\nSCORING: at the end of hand {hands}, each player's score is {vault_weight} times their vault crystals plus their showroom crystals. The highest score wins. If two or more players tie for highest score, the tied player with more vault crystals wins; if they are still tied, they share the win as a draw."
}
````
