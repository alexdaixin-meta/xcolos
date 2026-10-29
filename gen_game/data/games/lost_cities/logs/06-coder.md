# 06 coder

- time: 2026-10-27T08:41:44+00:00 (166.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 42bbe57c365fc35d, reply sha256 51aa7b66fd551d8d

## Sent

````
# Task: write the XColos game file for "Lost Cities: Four Expeditions"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. The deck has 44 cards in 4 colours: Red, Blue, Green and Yellow. Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9 and 10 (9 cards) and 2 wager cards.

STATE. Each player has a hidden hand.
- For each colour, each player has a public expedition record with three parts:
  - sum: the total of the number cards played in that colour (starts at 0);
  - top: the highest number played in that colour (starts at 0);
  - wagers: the number of wager cards played in that colour (starts at 0).
- There is a public 'discard tops' row. It holds at most one face-up card per colour.
- The number of cards left in the deck is public. The order of the deck is hidden.
- Each player has a match score that starts at 0.

MATCH. The match is two deals. Player A leads in deal 1 and Player B leads in deal 2. The leader takes the first turn of every round in that deal.

START OF A DEAL. All expedition records are reset to 0, and the discard tops row is cleared. All 44 cards are shuffled and each player is dealt 6 cards. The remaining 32 cards form the face-down deck.

ROUND. A round is one turn by the leader followed by one turn by the other player. A turn has two parts.

(1) PLAY OR DISCARD. Choose one card from your hand and say whether you PLAY it or DISCARD it.
- PLAY a number card of colour X: it is legal only if its number is greater than your top in X. Your sum in X increases by the number, and your top in X becomes the number.
- PLAY a wager card of colour X: it is legal only if your top in X is 0, meaning no number has been played there yet. Your wagers in X increase by 1.
- An illegal PLAY is treated as a DISCARD of that card.
- DISCARD a card of colour X: it becomes the face-up top card of colour X in the discard tops row. Any card that was there before is removed from the game.

(2) DRAW. Take one card into your hand, either the top card of the deck or the top discard card of any colour. You may not take the card you discarded this turn.
- If you name an unavailable source, you take the deck top.
- If the deck is empty, you take a discard top. If none is available apart from the card you just discarded, you draw nothing.

After each turn, the played or discarded card, the drawn source (but not the deck card's identity) and the deck size are announced to both players.

END OF A DEAL. A deal ends at the end of a round if the deck is empty, or at the end of the 20th round of that deal, whichever comes first.
- Each player then scores each colour separately. If their top in that colour is above 0 or their wagers in it are above 0, the colour scores (sum − 20) × (1 + wagers). Otherwise it scores 0.
- The four colour scores are added to the player's match score, which can go negative.
- Cards still in hand score nothing.

END OF MATCH. After deal 2 ends, the match is over. The match always ends within 40 rounds.

How the winner is decided: After both deals, the player with the higher match score wins. If the match scores are equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Lost Cities: Four Expeditions (2 to 2 players, best with 2)

Two players spend two deals building four colour expeditions with rising number cards and optional up-front wagers, discarding and drawing from a shared deck and face-up discard tops; each colour scores (sum - 20) x (1 + wagers).

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards held. Each card is a text such as 'Red 7' or 'Red W1'.
  - each player: red_sum (number, starts 0); everyone sees it. Total of number cards played in Red this deal
  - each player: red_top (number, starts 0); everyone sees it. Highest number played in Red this deal (0 = none)
  - each player: red_wagers (number, starts 0); everyone sees it. Wager cards played in Red this deal
  - each player: blue_sum (number, starts 0); everyone sees it. Total of number cards played in Blue this deal
  - each player: blue_top (number, starts 0); everyone sees it. Highest number played in Blue this deal (0 = none)
  - each player: blue_wagers (number, starts 0); everyone sees it. Wager cards played in Blue this deal
  - each player: green_sum (number, starts 0); everyone sees it. Total of number cards played in Green this deal
  - each player: green_top (number, starts 0); everyone sees it. Highest number played in Green this deal (0 = none)
  - each player: green_wagers (number, starts 0); everyone sees it. Wager cards played in Green this deal
  - each player: yellow_sum (number, starts 0); everyone sees it. Total of number cards played in Yellow this deal
  - each player: yellow_top (number, starts 0); everyone sees it. Highest number played in Yellow this deal (0 = none)
  - each player: yellow_wagers (number, starts 0); everyone sees it. Wager cards played in Yellow this deal
  - each player: match_score (number, starts 0); everyone sees it. Running match score over both deals. It can go negative.
  - the table: deck (list, starts []); hidden from all players. Face-down draw deck. Its order is hidden and a draw picks a card at random.
  - the table: deck_count (number, starts 0); everyone sees it. Cards left in the deck
  - the table: discard_red (text, starts ''); everyone sees it. Face-up top discard card of Red ('' = none)
  - the table: discard_blue (text, starts ''); everyone sees it. Face-up top discard card of Blue ('' = none)
  - the table: discard_green (text, starts ''); everyone sees it. Face-up top discard card of Green ('' = none)
  - the table: discard_yellow (text, starts ''); everyone sees it. Face-up top discard card of Yellow ('' = none)
  - the table: removed_cards (list, starts []); hidden from all players. Discard tops that were covered by a newer discard and so removed from the game
  - the table: turn_discard (text, starts ''); everyone sees it. The card discarded in the current turn ('' if the card was played). It may not be drawn back this turn.
  - the table: deal (number, starts 1); everyone sees it. Current deal (1 or 2). Seat 1 leads deal 1 and seat 2 leads deal 2.
  - the table: round_in_deal (number, starts 0); everyone sees it. Rounds started in the current deal (0 = a new deal must be dealt)
  - the table: match_over (bool, starts False); everyone sees it. True once deal 2 has been scored
  - parameters, each kept as a table attribute: deck_size = 44, colours = 4, number_card_min = 2, number_card_max = 10, number_cards_per_colour = 9, wager_cards_per_colour = 2, hand_size = 6, deck_after_deal = 32, deals = 2, max_rounds_per_deal = 20, max_rounds_per_match = 40, expedition_cost = 20, wager_multiplier_base = 1, initial_match_score = 0, initial_record_value = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player A and seat 2 is Player B.
  2. Set deal = 1, round_in_deal = 0, match_over = false and each player's match_score = 0.
  3. The first round step deals deal 1 (it runs whenever round_in_deal = 0).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Start of a deal: set every player's red/blue/green/yellow _sum, _top and _wagers to 0. Set discard_red, discard_blue, discard_green and discard_yellow to ''. Set removed_cards = [] and every hand = []. Set deck to all 44 cards: for each colour Red, Blue, Green and Yellow, the cards '<Colour> 2' to '<Colour> 10' plus '<Colour> W1' and '<Colour> W2'. Deal 6 cards to each player, each one drawn at random from deck, appended to hand and removed from deck. Set deck_count = 32.
  2. [sync] all players. What happens: Each player sees their own hand and all public attributes.
  3. [update] all players. What happens: round_in_deal += 1.
  4. [ask] seat 1 answers: One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand. What happens: The answer is stored for the next step.
  5. [update] seat 1. What happens: Remove the chosen card from seat 1's hand. If it is a PLAY of number card n of colour X and n > X_top: X_sum += n and X_top = n, and turn_discard = ''. If it is a PLAY of a wager of colour X and X_top == 0: X_wagers += 1, and turn_discard = ''. Otherwise (a DISCARD, or an illegal PLAY): if discard_X != '', append discard_X to removed_cards; then discard_X = card and turn_discard = card.
  6. [ask] seat 1 answers: One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard. What happens: The answer is stored for the next step.
  7. [update] seat 1. What happens: If a discard top of colour X was named, is non-empty and is not turn_discard: append discard_X to hand and set discard_X = ''. Else if deck_count > 0: draw a random card from deck into hand and deck_count -= 1. Else, if any discard top other than turn_discard is non-empty: take the first one in the order Red, Blue, Green, Yellow into hand and set it to ''. Otherwise draw nothing. Set turn_discard = ''.
  8. [tell] all players. What happens: Announce seat 1's played or discarded card, the draw source (deck, a discard colour, or nothing; a deck card's identity is not shown) and deck_count.
  9. [ask] seat 2 answers: One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand. What happens: The answer is stored for the next step.
  10. [update] seat 2. What happens: Resolved as in the seat 1 play/discard step, on seat 2's attributes.
  11. [ask] seat 2 answers: One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard. What happens: The answer is stored for the next step.
  12. [update] seat 2. What happens: Resolved as in the seat 1 draw step, into seat 2's hand. Set turn_discard = ''.
  13. [tell] all players. What happens: Announce seat 2's played or discarded card, the draw source (deck, a discard colour, or nothing; a deck card's identity is not shown) and deck_count.
  14. [ask] seat 1 answers: One choice: 'play <card>' for each card in hand that is a legal play, or 'discard <card>' for each card in hand. What happens: The answer is stored for the next step.
  15. [update] seat 1. What happens: Resolved as in the seat 1 play/discard step above.
  16. [ask] seat 1 answers: One choice: 'deck' (if deck_count > 0), or 'discard <colour>' for each non-empty discard top whose card is not turn_discard. What happens: The answer is stored for the next step.
  17. [update] seat 1. What happens: Resolved as in the seat 1 draw step above. Set turn_discard = ''.
  18. [tell] all players. What happens: Announce seat 1's played or discarded card, the draw source and deck_count.
  19. [update] all players. What happens: End of deal: for each player and each colour X, if X_top > 0 or X_wagers > 0, then match_score += (X_sum - 20) * (1 + X_wagers); otherwise that colour adds 0. Cards in hand score nothing. Then, if deal == 2, set match_over = true; otherwise set deal = 2 and round_in_deal = 0.
  20. [tell] all players. What happens: Announce each player's colour scores for the deal and their match_score.
  21. [check] all players. What happens: End the game if match_over == true; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a deal starts, the deck holds 44 cards: for each of Red, Blue, Green and Yellow, the numbers 2 to 10 and two wagers (W1, W2).
  R2. When a deal starts, every sum, top and wagers record is 0, every discard top is empty, each player is dealt 6 random cards from the deck, and deck_count is 32.
  R3. When the match is in deal 1, seat 1 takes the first turn of every round and seat 2 the second; in deal 2, seat 2 goes first and seat 1 second.
  R4. When a player plays number card n of colour X and n > X_top, then X_sum increases by n and X_top becomes n (for example, playing Red 7 with red_top 5 and red_sum 5 gives red_sum 12 and red_top 7).
  R5. When a player plays a wager of colour X while X_top == 0, then X_wagers increases by 1.
  R6. When a player plays a number card not greater than X_top, or a wager while X_top > 0, then the card is discarded instead.
  R7. When a card of colour X is discarded, it becomes discard_X, and the card previously in discard_X is moved to removed_cards.
  R8. When a player draws from the deck and deck_count > 0, then a random deck card goes to their hand and deck_count decreases by 1.
  R9. When a player draws a non-empty discard top other than the card they discarded this turn, then that card goes to their hand and that discard top becomes empty.
  R10. When a player names an unavailable draw source, then they take the deck top if deck_count > 0.
  R11. When the deck is empty, the player takes an available discard top; when none is available apart from the card they just discarded, they draw nothing.
  R12. When a turn ends, both players are told the card played or discarded, the draw source (not the identity of a deck card) and deck_count.
  R13. When a round ends with deck_count == 0 or round_in_deal == 20, then the deal ends.
  R14. When a deal ends, each colour with X_top > 0 or X_wagers > 0 adds (X_sum - 20) * (1 + X_wagers) to match_score (for example, sum 27 with 1 wager gives +14), and any other colour adds 0.
  R15. When a colour has only wagers played (top 0 and wagers w > 0), it scores -20 * (1 + w).
  R16. When a deal ends, cards still in hand score nothing, and match_score may go negative.
  R17. When deal 2 ends, the match is over and the higher match_score wins; equal scores are a draw.
  R18. The match always ends within 40 rounds (at most 20 rounds in each of the 2 deals).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Play or discard | asked: the seat whose turn it is | options: For each card in hand: 'discard <card>'. Also 'play <card>' for each number card whose number is greater than that colour's top, and for each wager whose colour top is 0.
  - Draw source | asked: the seat whose turn it is | options: 'deck' if deck_count > 0, plus 'discard <colour>' for each non-empty discard top that is not the card discarded this turn. If no option exists, the question is skipped and nothing is drawn.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: match_over == true
  - each player's standing: you.match_score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After both deals, the player with the higher match_score wins. Equal match scores share the win, which is a draw.
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

- each player: `red_sum` (number, visible: public, starts 0): Total of number cards played in Red this deal
- each player: `red_top` (number, visible: public, starts 0): Highest number played in Red this deal (0 = none)
- each player: `red_wagers` (number, visible: public, starts 0): Wager cards played in Red this deal
- each player: `blue_sum` (number, visible: public, starts 0): Total of number cards played in Blue this deal
- each player: `blue_top` (number, visible: public, starts 0): Highest number played in Blue this deal (0 = none)
- each player: `blue_wagers` (number, visible: public, starts 0): Wager cards played in Blue this deal
- each player: `green_sum` (number, visible: public, starts 0): Total of number cards played in Green this deal
- each player: `green_top` (number, visible: public, starts 0): Highest number played in Green this deal (0 = none)
- each player: `green_wagers` (number, visible: public, starts 0): Wager cards played in Green this deal
- each player: `yellow_sum` (number, visible: public, starts 0): Total of number cards played in Yellow this deal
- each player: `yellow_top` (number, visible: public, starts 0): Highest number played in Yellow this deal (0 = none)
- each player: `yellow_wagers` (number, visible: public, starts 0): Wager cards played in Yellow this deal
- each player: `match_score` (number, visible: public, starts 0): Running match score over both deals. It can go negative.
- the table: `deck_count` (number, visible: public, starts 0): Cards left in the deck
- the table: `discard_red` (text, visible: public, starts ''): Face-up top discard card of Red ('' = none)
- the table: `discard_blue` (text, visible: public, starts ''): Face-up top discard card of Blue ('' = none)
- the table: `discard_green` (text, visible: public, starts ''): Face-up top discard card of Green ('' = none)
- the table: `discard_yellow` (text, visible: public, starts ''): Face-up top discard card of Yellow ('' = none)
- the table: `deal` (number, visible: public, starts 1): Current deal (1 or 2). Seat 1 leads deal 1 and seat 2 leads deal 2.
- the table: `round_in_deal` (number, visible: public, starts 0): Rounds started in the current deal (0 = a new deal must be dealt)
- the table: `match_over` (bool, visible: public, starts False): True once deal 2 has been scored
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 44, colours = 4, number_card_min = 2, number_card_max = 10, number_cards_per_colour = 9, wager_cards_per_colour = 2, hand_size = 6, deck_after_deal = 32, deals = 2, max_rounds_per_deal = 20, max_rounds_per_match = 40, expedition_cost = 20, wager_multiplier_base = 1, initial_match_score = 0, initial_record_value = 0
- the game ends with ONE ending whose `rank_by` is `you.match_score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "lost_cities_four_expeditions",
    "name": "Lost Cities: Four Expeditions",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two deals of building four colour expeditions with rising cards and up-front wagers; each colour scores (sum - 20) x (1 + wagers)."
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
        "key": "red_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_wagers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_wagers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_wagers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "yellow_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "yellow_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "yellow_wagers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "match_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_scores",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "offer",
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
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "discard_red",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "discard_blue",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "discard_green",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "discard_yellow",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "removed_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "turn_discard",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_deal",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "match_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "number_card_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "number_card_max",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "number_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "wager_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_rounds_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "max_rounds_per_match",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "expedition_cost",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "wager_multiplier_base",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "initial_match_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_record_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_info",
        "visible": "none",
        "type": "list",
        "initial": [
          ["Red 2", "Red", 2],
          ["Red 3", "Red", 3],
          ["Red 4", "Red", 4],
          ["Red 5", "Red", 5],
          ["Red 6", "Red", 6],
          ["Red 7", "Red", 7],
          ["Red 8", "Red", 8],
          ["Red 9", "Red", 9],
          ["Red 10", "Red", 10],
          ["Red W1", "Red", 0],
          ["Red W2", "Red", 0],
          ["Blue 2", "Blue", 2],
          ["Blue 3", "Blue", 3],
          ["Blue 4", "Blue", 4],
          ["Blue 5", "Blue", 5],
          ["Blue 6", "Blue", 6],
          ["Blue 7", "Blue", 7],
          ["Blue 8", "Blue", 8],
          ["Blue 9", "Blue", 9],
          ["Blue 10", "Blue", 10],
          ["Blue W1", "Blue", 0],
          ["Blue W2", "Blue", 0],
          ["Green 2", "Green", 2],
          ["Green 3", "Green", 3],
          ["Green 4", "Green", 4],
          ["Green 5", "Green", 5],
          ["Green 6", "Green", 6],
          ["Green 7", "Green", 7],
          ["Green 8", "Green", 8],
          ["Green 9", "Green", 9],
          ["Green 10", "Green", 10],
          ["Green W1", "Green", 0],
          ["Green W2", "Green", 0],
          ["Yellow 2", "Yellow", 2],
          ["Yellow 3", "Yellow", 3],
          ["Yellow 4", "Yellow", 4],
          ["Yellow 5", "Yellow", 5],
          ["Yellow 6", "Yellow", 6],
          ["Yellow 7", "Yellow", 7],
          ["Yellow 8", "Yellow", 8],
          ["Yellow 9", "Yellow", 9],
          ["Yellow 10", "Yellow", 10],
          ["Yellow W1", "Yellow", 0],
          ["Yellow W2", "Yellow", 0]
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "active",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn_no",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "t_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "t_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "t_top",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "t_play",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_draw",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "start the match",
      "do": [
        {
          "set": {
            "key": "deal",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_deal",
            "value": 0
          }
        },
        {
          "set": {
            "key": "match_over",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "match_score",
            "value": {
              "calc": "initial_match_score"
            }
          }
        }
      ],
      "text": "Seat 1 is Player A and leads deal 1. Seat 2 is Player B and leads deal 2."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "start of a deal",
      "when": {
        "calc": "round_in_deal == 0"
      },
      "do": [
        {"set": {"players": "all", "key": "red_sum", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "red_top", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "red_wagers", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "blue_sum", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "blue_top", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "blue_wagers", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "green_sum", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "green_top", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "green_wagers", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "yellow_sum", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "yellow_top", "value": {"calc": "initial_record_value"}}},
        {"set": {"players": "all", "key": "yellow_wagers", "value": {"calc": "initial_record_value"}}},
        {"set": {"key": "discard_red", "value": ""}},
        {"set": {"key": "discard_blue", "value": ""}},
        {"set": {"key": "discard_green", "value": ""}},
        {"set": {"key": "discard_yellow", "value": ""}},
        {"set": {"key": "turn_discard", "value": ""}},
        {"set": {"key": "removed_cards", "value": {"calc": "[]"}}},
        {"set": {"players": "all", "key": "hand", "value": {"calc": "[]"}}},
        {"set": {"key": "deck", "value": {"calc": "[i[0] for i in card_info]"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "deck_count", "value": {"calc": "len(deck)"}}}
      ],
      "text": "Deal {deal} begins. All 44 cards are shuffled and each player is dealt 6. Cards left in the deck: {deck_count}."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
    },
    {
      "use": "update",
      "phase": "round",
      "label": "the round begins",
      "do": [
        {"adjust": {"key": "round_in_deal", "value": 1}},
        {"set": {"key": "turn_no", "value": 0}}
      ],
      "text": "Deal {deal}, round {round_in_deal}."
    },
    {
      "use": "repeat",
      "label": "the two turns",
      "until": {
        "calc": "turn_no >= 2"
      },
      "max": 3,
      "steps": [
        {
          "use": "update",
          "phase": "turn",
          "label": "whose turn",
          "do": [
            {
              "set": {
                "key": "active",
                "value": {
                  "calc": "deal if turn_no == 0 else (2 if deal == 1 else 1)"
                }
              }
            },
            {
              "set": {
                "players": {"where": "you.seat == active"},
                "key": "offer",
                "value": {
                  "calc": "['discard ' + c for c in you.hand] + ['play ' + i[0] for i in card_info if i[0] in you.hand and ((i[2] > (you.red_top if i[1] == 'Red' else you.blue_top if i[1] == 'Blue' else you.green_top if i[1] == 'Green' else you.yellow_top)) if i[2] > 0 else ((you.red_top if i[1] == 'Red' else you.blue_top if i[1] == 'Blue' else you.green_top if i[1] == 'Green' else you.yellow_top) == 0))]"
                }
              }
            }
          ]
        },
        {
          "use": "ask",
          "phase": "turn",
          "label": "play or discard",
          "to": {
            "where": "you.seat == active"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "verify": {
            "bind": "choice"
          },
          "text": "Your turn. Choose one card from your hand to PLAY onto your expedition or to DISCARD face up. Only legal plays are offered: a number card higher than your top in that colour, or a wager while that colour's top is 0."
        },
        {
          "use": "update",
          "phase": "turn",
          "label": "resolve the card",
          "do": [
            {"set": {"key": "last_card", "value": {"calc": "[i[0] for i in card_info if $choice == 'play ' + i[0] or $choice == 'discard ' + i[0]][0]"}}},
            {"set": {"key": "t_colour", "value": {"calc": "[i[1] for i in card_info if i[0] == last_card][0]"}}},
            {"set": {"key": "t_value", "value": {"calc": "[i[2] for i in card_info if i[0] == last_card][0]"}}},
            {"set": {"key": "t_top", "value": {"calc": "sum([(p.red_top if t_colour == 'Red' else p.blue_top if t_colour == 'Blue' else p.green_top if t_colour == 'Green' else p.yellow_top) for p in players if p.seat == active])"}}},
            {"set": {"key": "t_play", "value": {"calc": "$choice == 'play ' + last_card and (t_value > t_top if t_value > 0 else t_top == 0)"}}},
            {"set": {"key": "last_action", "value": {"calc": "'played' if t_play else 'discarded'"}}},
            {"remove": {"players": {"where": "you.seat == active"}, "key": "hand", "value": {"calc": "last_card"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "red_sum", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Red' and t_value > 0"}}},
            {"set": {"players": {"where": "you.seat == active"}, "key": "red_top", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Red' and t_value > 0"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "red_wagers", "value": 1, "if": {"calc": "t_play and t_colour == 'Red' and t_value == 0"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "blue_sum", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Blue' and t_value > 0"}}},
            {"set": {"players": {"where": "you.seat == active"}, "key": "blue_top", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Blue' and t_value > 0"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "blue_wagers", "value": 1, "if": {"calc": "t_play and t_colour == 'Blue' and t_value == 0"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "green_sum", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Green' and t_value > 0"}}},
            {"set": {"players": {"where": "you.seat == active"}, "key": "green_top", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Green' and t_value > 0"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "green_wagers", "value": 1, "if": {"calc": "t_play and t_colour == 'Green' and t_value == 0"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "yellow_sum", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Yellow' and t_value > 0"}}},
            {"set": {"players": {"where": "you.seat == active"}, "key": "yellow_top", "value": {"calc": "t_value"}, "if": {"calc": "t_play and t_colour == 'Yellow' and t_value > 0"}}},
            {"adjust": {"players": {"where": "you.seat == active"}, "key": "yellow_wagers", "value": 1, "if": {"calc": "t_play and t_colour == 'Yellow' and t_value == 0"}}},
            {"append": {"key": "removed_cards", "value": {"calc": "discard_red"}, "if": {"calc": "not t_play and t_colour == 'Red' and discard_red != ''"}}},
            {"set": {"key": "discard_red", "value": {"calc": "last_card"}, "if": {"calc": "not t_play and t_colour == 'Red'"}}},
            {"append": {"key": "removed_cards", "value": {"calc": "discard_blue"}, "if": {"calc": "not t_play and t_colour == 'Blue' and discard_blue != ''"}}},
            {"set": {"key": "discard_blue", "value": {"calc": "last_card"}, "if": {"calc": "not t_play and t_colour == 'Blue'"}}},
            {"append": {"key": "removed_cards", "value": {"calc": "discard_green"}, "if": {"calc": "not t_play and t_colour == 'Green' and discard_green != ''"}}},
            {"set": {"key": "discard_green", "value": {"calc": "last_card"}, "if": {"calc": "not t_play and t_colour == 'Green'"}}},
            {"append": {"key": "removed_cards", "value": {"calc": "discard_yellow"}, "if": {"calc": "not t_play and t_colour == 'Yellow' and discard_yellow != ''"}}},
            {"set": {"key": "discard_yellow", "value": {"calc": "last_card"}, "if": {"calc": "not t_play and t_colour == 'Yellow'"}}},
            {"set": {"key": "turn_discard", "value": {"calc": "'' if t_play else last_card"}}},
            {
              "set": {
                "players": {"where": "you.seat == active"},
                "key": "offer",
                "value": {
                  "calc": "(['deck'] if deck_count > 0 else []) + (['discard Red'] if discard_red != '' and discard_red != turn_discard else []) + (['discard Blue'] if discard_blue != '' and discard_blue != turn_discard else []) + (['discard Green'] if discard_green != '' and discard_green != turn_discard else []) + (['discard Yellow'] if discard_yellow != '' and discard_yellow != turn_discard else [])"
                }
              }
            }
          ]
        },
        {
          "use": "ask",
          "phase": "turn",
          "label": "draw",
          "to": {
            "where": "you.seat == active"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "verify": {
            "bind": "src"
          },
          "text": "Draw one card: the top card of the face-down deck, or the face-up top discard of a colour. You may not take back the card you discarded this turn."
        },
        {
          "use": "update",
          "phase": "turn",
          "label": "resolve the draw",
          "do": [
            {
              "set": {
                "key": "last_draw",
                "value": {
                  "calc": "'the Red discard' if ($src == 'discard Red' and discard_red != '' and discard_red != turn_discard) else 'the Blue discard' if ($src == 'discard Blue' and discard_blue != '' and discard_blue != turn_discard) else 'the Green discard' if ($src == 'discard Green' and discard_green != '' and discard_green != turn_discard) else 'the Yellow discard' if ($src == 'discard Yellow' and discard_yellow != '' and discard_yellow != turn_discard) else 'the deck' if deck_count > 0 else 'the Red discard' if (discard_red != '' and discard_red != turn_discard) else 'the Blue discard' if (discard_blue != '' and discard_blue != turn_discard) else 'the Green discard' if (discard_green != '' and discard_green != turn_discard) else 'the Yellow discard' if (discard_yellow != '' and discard_yellow != turn_discard) else 'nothing'"
                }
              }
            },
            {"append": {"players": {"where": "you.seat == active"}, "key": "hand", "value": {"calc": "discard_red"}, "if": {"calc": "last_draw == 'the Red discard'"}}},
            {"set": {"key": "discard_red", "value": "", "if": {"calc": "last_draw == 'the Red discard'"}}},
            {"append": {"players": {"where": "you.seat == active"}, "key": "hand", "value": {"calc": "discard_blue"}, "if": {"calc": "last_draw == 'the Blue discard'"}}},
            {"set": {"key": "discard_blue", "value": "", "if": {"calc": "last_draw == 'the Blue discard'"}}},
            {"append": {"players": {"where": "you.seat == active"}, "key": "hand", "value": {"calc": "discard_green"}, "if": {"calc": "last_draw == 'the Green discard'"}}},
            {"set": {"key": "discard_green", "value": "", "if": {"calc": "last_draw == 'the Green discard'"}}},
            {"append": {"players": {"where": "you.seat == active"}, "key": "hand", "value": {"calc": "discard_yellow"}, "if": {"calc": "last_draw == 'the Yellow discard'"}}},
            {"set": {"key": "discard_yellow", "value": "", "if": {"calc": "last_draw == 'the Yellow discard'"}}},
            {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "last_draw == 'the deck'"}}},
            {"append": {"players": {"where": "you.seat == active"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "last_draw == 'the deck'"}}},
            {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "last_draw == 'the deck'"}}},
            {"adjust": {"key": "deck_count", "value": -1, "if": {"calc": "last_draw == 'the deck'"}}},
            {"set": {"key": "turn_discard", "value": ""}},
            {"adjust": {"key": "turn_no", "value": 1}}
          ]
        },
        {
          "use": "tell",
          "phase": "turn",
          "label": "the turn is announced",
          "to": "all",
          "text": "Seat {active} {last_action} {last_card} and drew from {last_draw}. Cards left in the deck: {deck_count}."
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "end of deal",
      "when": {
        "calc": "deck_count == 0 or round_in_deal >= max_rounds_per_deal"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "deal_scores",
            "value": {
              "calc": "[((you.red_sum - expedition_cost) * (wager_multiplier_base + you.red_wagers) if you.red_top > 0 or you.red_wagers > 0 else 0), ((you.blue_sum - expedition_cost) * (wager_multiplier_base + you.blue_wagers) if you.blue_top > 0 or you.blue_wagers > 0 else 0), ((you.green_sum - expedition_cost) * (wager_multiplier_base + you.green_wagers) if you.green_top > 0 or you.green_wagers > 0 else 0), ((you.yellow_sum - expedition_cost) * (wager_multiplier_base + you.yellow_wagers) if you.yellow_top > 0 or you.yellow_wagers > 0 else 0)]"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "match_score",
            "value": {
              "calc": "sum(you.deal_scores)"
            }
          }
        },
        {
          "set": {
            "key": "match_over",
            "value": true,
            "if": {
              "calc": "deal >= deals"
            }
          }
        },
        {
          "set": {
            "key": "round_in_deal",
            "value": 0,
            "if": {
              "calc": "deal < deals"
            }
          }
        },
        {
          "adjust": {
            "key": "deal",
            "value": 1,
            "if": {
              "calc": "deal < deals"
            }
          }
        }
      ],
      "text": "The deal is over and is scored."
    },
    {
      "use": "tell",
      "phase": "scoring",
      "label": "deal scores",
      "when": {
        "calc": "round_in_deal == 0 or match_over"
      },
      "to": "all",
      "text": "Deal scores [Red, Blue, Green, Yellow]: Seat 1 {players[0].deal_scores}, match score {players[0].match_score}; Seat 2 {players[1].deal_scores}, match score {players[1].match_score}."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after deal 2",
      "when": {
        "calc": "match_over"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "match_over"
      },
      "rank_by": "you.match_score",
      "text": "Winner: {result}. Final match scores: Seat 1 {players[0].match_score}, Seat 2 {players[1].match_score}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS. The deck has {deck_size} cards in {colours} colours: Red, Blue, Green and Yellow. Each colour has number cards {number_card_min} to {number_card_max} ({number_cards_per_colour} cards) and {wager_cards_per_colour} wager cards (W1, W2).\n\nSTATE. Your hand is hidden. For each colour each player has a public expedition record: sum (total of number cards played there), top (highest number played there, 0 = none) and wagers (wager cards played there). There is a public discard tops row holding at most one face-up card per colour. The number of cards left in the deck is public; its order is hidden. Each player has a match score starting at {initial_match_score}.\n\nMATCH. The match is {deals} deals. Seat 1 (Player A) leads deal 1 and seat 2 (Player B) leads deal 2; the leader takes the first turn of every round in that deal.\n\nSTART OF A DEAL. All expedition records are reset to {initial_record_value} and the discard tops row is cleared. All {deck_size} cards are shuffled and each player is dealt {hand_size} cards. The remaining {deck_after_deal} cards form the face-down deck.\n\nROUND. A round is one turn by the leader followed by one turn by the other player. A turn has two parts.\n(1) PLAY OR DISCARD. Choose one card from your hand and say whether you PLAY it or DISCARD it. PLAY a number card of colour X: legal only if its number is greater than your top in X; your sum in X increases by the number and your top in X becomes the number. PLAY a wager of colour X: legal only if your top in X is 0; your wagers in X increase by 1. An illegal PLAY is treated as a DISCARD of that card (only legal plays are offered to you). DISCARD a card of colour X: it becomes the face-up top card of colour X in the discard tops row; any card that was there before is removed from the game.\n(2) DRAW. Take one card into your hand: the top card of the deck, or the top discard card of any colour. You may not take the card you discarded this turn. If you name an unavailable source, you take the deck top. If the deck is empty, you take a discard top; if none is available apart from the card you just discarded, you draw nothing.\nAfter each turn, the played or discarded card, the draw source (but not the deck card's identity) and the deck size are announced to both players.\n\nEND OF A DEAL. A deal ends at the end of a round if the deck is empty, or at the end of round {max_rounds_per_deal} of that deal, whichever comes first. Each player scores each colour separately: if their top there is above 0 or their wagers there are above 0, the colour scores (sum - {expedition_cost}) x ({wager_multiplier_base} + wagers); otherwise it scores 0. A colour with only wagers scores -{expedition_cost} x (1 + wagers). The four colour scores are added to the match score, which can go negative. Cards still in hand score nothing.\n\nEND OF MATCH. After deal 2 ends, the match is over (always within {max_rounds_per_match} rounds). The player with the higher match score wins; equal match scores share the win, which is a draw."
}
```
````
