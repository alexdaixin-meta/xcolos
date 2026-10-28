# Task: write the XColos game file for "Knock Brag (3-player)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

PLAYERS AND LIVES: Exactly 3 players, in seats 1, 2 and 3 clockwise. Each starts with 3 lives. A player at 0 lives is eliminated and takes no further part. The others are 'active'.

DECK: 36 cards, four copies each of the values 1, 2, 3, 4, 5, 6, 7, 8 and 9. There are no suits.

HAND SCORE (used at the showdown): Sort a hand's three values so that a <= b <= c.
- Prial (a = c): 300 + a. Exception: 3-3-3 scores 310.
- Run (b = a+1 and c = b+1): 200 + c. Exception: 1-2-3 scores 210. Runs do not wrap: 8-9-1 and 9-1-2 are not runs.
- Pair (a = b or b = c, but not a prial): 100 + 10 x b + (a + c - b). That is 100 + 10 x the pair value + the odd card.
- High card (anything else): a + b + c.
Higher is better.

ROUNDS, LEADER AND DEALS: The game is played in rounds, at most 40. In each round every active player takes exactly one action, in clockwise order starting with that round's leader. Seat 1 leads round 1. In each later round the leader is the next active player clockwise from the previous round's leader. This rotation continues across deals and skips eliminated players. A 'deal' is the series of rounds from one dealing of the cards to its showdown. The deal-round counter is 1 in the first round of a deal, 2 in the second, and so on.

DEALING: At the very start of round 1, and at the start of every round that follows a showdown, the deck of 36 is shuffled (the round's one random event). Each active player receives 3 cards face down that only they see. Three cards go to the table: slot U face up, seen by everyone, and slots D1 and D2 face down, seen by nobody. The value of U is announced. The rest of the deck is not used in this deal.

ACTIONS: On your turn choose exactly one action. Give it as a single choice that includes every detail needed (which action, which of your cards, which slot, which card to expose).
(a) TAKE UP: swap one of your cards for the face-up card U. The card you give becomes the new face-up U. Announced: 'X took the face-up [value] and left a face-up [value]'.
(b) BLIND: swap one of your cards for D1 or D2 (your choice of slot) without seeing it first. Your card goes face down into that slot. You now see the card you received. Announced: 'X made a blind swap with D1' (or D2).
(c) WHOLE HAND: take all three table cards into your hand; you now see them. Your old three cards become the table hand. You choose which of them goes face up as U; the other two go face down into D1 and D2. Announced: 'X swapped the whole hand and exposed a [value]'.
(d) KNOCK: keep your hand and make no exchange. Only the round's leader may knock, and only when the deal-round counter is 2 or more. A knock is the knocker's action for that round. Announced: 'X knocks'.

AFTER A KNOCK: The remaining active players in that same round (everyone after the knocker in clockwise order) each take their action as normal, but must choose (a), (b) or (c). These are their final actions. The showdown then happens at the end of that round.

FORCED SHOWDOWN: If nobody has knocked, the showdown happens at the end of the round whose deal-round counter equals the number of active players plus 1. That is the end of deal-round 4 when 3 players are active, or deal-round 3 when 2 are active. There is no knocker.

SHOWDOWN (at the end of the round): All active hands are revealed and scored, and every player's score is announced and recorded as their 'last showdown score'. If every active player has the same score, nobody loses a life. Otherwise every player with the lowest score loses 1 life, except a knocker with the lowest score, who loses 2 lives. Players at 0 lives or fewer are eliminated. The next round then begins with a new deal and the deal-round counter at 1. If no showdown happened, the deal-round counter rises by 1 for the next round.

END: The game ends at once when only one active player remains, or at the end of round 40.

How the winner is decided: If only one player remains, that player wins. If round 40 ends with two or three players still active, the player with the most lives wins. A tie on lives is broken by the higher last showdown score among the tied players. If they are still tied, or if no showdown has yet happened, the game is a draw between them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Knock Brag (3-player) (3 to 3 players, best with 3)

Three players swap cards with a shared three-card table hand to build the best Brag hand; the leader may knock to force a showdown, the lowest hand at each showdown loses lives, and the last player with lives wins.

STATE (every item below must exist in the file):
  - each player: lives (number, starts 3); everyone sees it. Lives remaining. The player is eliminated at 0. It is never set below 0.
  - each player: eliminated (bool, starts False); everyone sees it. True once lives reach 0. An eliminated player takes no further part.
  - each player: hand (list, starts []); only its owner sees it. The player's 3 card values, as positions 1 to 3, seen only by the owner until the showdown.
  - each player: hand_score (number, starts 0); everyone sees it. The hand's Brag score, computed and shown at each showdown.
  - each player: last_showdown_score (number, starts 0); everyone sees it. The player's score at the most recent showdown. Used as the tie-break on lives.
  - the table: deck (list, starts [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9]); hidden from all players. The 36-card deck. It is rebuilt and dealt from at the start of each deal. Undealt cards are unused.
  - the table: table_up (number, starts 0); everyone sees it. The face-up table card in slot U.
  - the table: table_d1 (number, starts 0); hidden from all players. The face-down table card in slot D1, seen by nobody.
  - the table: table_d2 (number, starts 0); hidden from all players. The face-down table card in slot D2, seen by nobody.
  - the table: round_number (number, starts 1); everyone sees it. The current round, from 1 to 40.
  - the table: deal_round (number, starts 1); everyone sees it. The round number within the current deal.
  - the table: leader_seat (number, starts 1); everyone sees it. The seat that leads this round.
  - the table: knocker_seat (number, starts 0); everyone sees it. The seat that knocked in this deal, or 0 if nobody has knocked.
  - the table: active_count (number, starts 3); everyone sees it. The number of players not eliminated.
  - the table: showdown_now (bool, starts False); everyone sees it. True when this round ends in a showdown.
  - the table: lowest_score (number, starts 0); everyone sees it. The lowest hand_score among active players at the showdown.
  - the table: highest_score (number, starts 0); everyone sees it. The highest hand_score among active players at the showdown.
  - parameters, each kept as a table attribute: player_count = 3, starting_lives = 3, deck_size = 36, copies_per_value = 4, lowest_card_value = 1, highest_card_value = 9, hand_size = 3, table_cards = 3, max_rounds = 40, prial_base = 300, prial_333_score = 310, run_base = 200, run_123_score = 210, pair_base = 100, pair_multiplier = 10, knock_min_deal_round = 2, life_loss_lowest = 1, life_loss_knocker_lowest = 2, forced_showdown_offset = 1, rank_lives_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 sit clockwise. Each player starts with 3 lives and is active.
  2. round_number = 1, deal_round = 1, leader_seat = 1, knocker_seat = 0, active_count = 3.
  3. Every player's last_showdown_score is 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When deal_round == 1 (a new deal): rebuild deck as the 36 cards (four each of 1 to 9). Empty every hand. For each active player, draw 3 cards at random from deck into their hand. Then draw 1 card each into table_up, table_d1 and table_d2. Set knocker_seat = 0. The rest of deck is unused this deal.
  2. [tell] all players. What happens: When deal_round == 1: announce 'New deal. The face-up card U is {table_up}.'
  3. [sync] all players. What happens: Each player sees their own hand, table_up, lives, deal_round, leader_seat and knocker_seat.
  4. [ask] each active player in turn, clockwise starting at leader_seat and skipping eliminated seats answers: One choice from: take_up_give_1, take_up_give_2, take_up_give_3, blind_D1_give_1, blind_D1_give_2, blind_D1_give_3, blind_D2_give_1, blind_D2_give_2, blind_D2_give_3, whole_hand_expose_1, whole_hand_expose_2, whole_hand_expose_3, knock. Knock is offered only to the leader when deal_round >= 2.. What happens: take_up_give_k: swap hand[k] with table_up, then announce 'Seat X took the face-up [old U] and left a face-up [new U]'. blind_Dj_give_k: swap hand[k] with table_dj; the player now sees the received card in their hand; announce 'Seat X made a blind swap with Dj'. whole_hand_expose_k: the old hand [h1,h2,h3] becomes the table and the hand becomes [table_up, table_d1, table_d2]; table_up = old hk, and the other two old cards go to table_d1 and table_d2 in order; announce 'Seat X swapped the whole hand and exposed a [table_up]'. knock: no exchange, set knocker_seat = the leader's seat, announce 'Seat X knocks'. Each effect applies before the next player is asked.
  5. [update] all players. What happens: showdown_now = (knocker_seat > 0) or (deal_round == active_count + 1).
  6. [update] all players. What happens: When showdown_now: for each active player, let a = min(hand), c = max(hand), b = sum(hand) - a - c. Then hand_score = 310 if a == 3 and c == 3; else 300 + a if a == c; else 210 if a == 1 and b == 2 and c == 3; else 200 + c if b == a + 1 and c == b + 1; else 100 + 10*b + (a + c - b) if a == b or b == c; else a + b + c. Set last_showdown_score = hand_score. Set lowest_score = min and highest_score = max of hand_score over active players.
  7. [tell] all players. What happens: When showdown_now: reveal every active player's hand and announce 'Seat X shows [hand] scoring {hand_score}' for each.
  8. [update] all players. What happens: When showdown_now and lowest_score < highest_score: each active player with hand_score == lowest_score loses 2 lives if their seat == knocker_seat, otherwise 1 life. Lives are floored at 0. Any player with lives == 0 gets eliminated = true. Recompute active_count as the number of players not eliminated. Announce each life lost and each elimination.
  9. [update] all players. What happens: If showdown_now, deal_round = 1; otherwise deal_round = deal_round + 1. Then round_number = round_number + 1, and leader_seat = the next seat clockwise after leader_seat that is not eliminated.
  10. [check] all players. What happens: End the game if active_count <= 1 or round_number > 40; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, each of the 3 players has 3 lives, seat 1 leads round 1, and deal_round is 1.
  R2. When a deal starts (round 1, or the round after a showdown), the 36-card deck (four each of 1 to 9) is shuffled, each active player gets 3 private cards, and table_up, table_d1 and table_d2 get 1 card each, with table_up announced.
  R3. When a hand sorted a<=b<=c has a == c, then it scores 300 + a, except 3-3-3, which scores 310.
  R4. When a hand has b == a+1 and c == b+1, then it scores 200 + c, except 1-2-3, which scores 210; 8-9-1 and 9-1-2 are not runs.
  R5. When a hand has a == b or b == c but is not a prial, then it scores 100 + 10*b + (a + c - b); for example, 5-5-2 scores 152.
  R6. When a hand is no prial, run or pair, then it scores a + b + c; for example, 2-5-9 scores 16.
  R7. When a player takes up giving card k, then hand[k] and table_up are swapped and the new table_up is announced.
  R8. When a player makes a blind swap with Dj giving card k, then hand[k] and table_dj are swapped, only that player sees the received card, and only the slot is announced.
  R9. When a player swaps the whole hand exposing old card k, then the hand becomes the three table cards, old card k becomes table_up, the other two old cards go face down to D1 and D2, and the exposed value is announced.
  R10. When the leader acts and deal_round >= 2, then knock is offered; no other player, and no leader in deal_round 1, may knock.
  R11. When the leader knocks, then the players after them that round must take up, blind swap or whole-hand swap, and the showdown happens at the end of that round.
  R12. When nobody has knocked and deal_round == active_count + 1 (4 with 3 active, 3 with 2 active), then a showdown happens at the end of the round.
  R13. When there is a showdown, then every active hand is revealed and scored, and each score is recorded as that player's last_showdown_score.
  R14. When all active scores at a showdown are equal, then nobody loses a life.
  R15. When scores at a showdown differ, then every player on the lowest score loses 1 life, except a knocker on the lowest score, who loses 2.
  R16. When a player's lives reach 0 or fewer, then lives is set to 0 and the player is eliminated and takes no further part.
  R17. When a round ends, then the next leader is the next non-eliminated seat clockwise from the current leader, and deal_round resets to 1 after a showdown or rises by 1 otherwise.
  R18. When only one active player remains, then the game ends and that player wins.
  R19. When round 40 ends with 2 or 3 active players, then the player with the most lives wins, a tie is broken by the higher last_showdown_score, and a remaining tie is a shared draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Your action this round | asked: the leader (leader_seat) when deal_round >= 2 | options: take_up_give_1, take_up_give_2, take_up_give_3, blind_D1_give_1, blind_D1_give_2, blind_D1_give_3, blind_D2_give_1, blind_D2_give_2, blind_D2_give_3, whole_hand_expose_1, whole_hand_expose_2, whole_hand_expose_3, knock
  - Your action this round | asked: the leader when deal_round == 1, and every other active seat (including after a knock) | options: take_up_give_1, take_up_give_2, take_up_give_3, blind_D1_give_1, blind_D1_give_2, blind_D1_give_3, blind_D2_give_1, blind_D2_give_2, blind_D2_give_3, whole_hand_expose_1, whole_hand_expose_2, whole_hand_expose_3
  - Your action this round | asked: eliminated seats | options: not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: active_count <= 1 or round_number > 40
  - each player's standing: you.lives * 1000 + you.last_showdown_score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Most lives wins. A lone survivor is the only player with lives above 0. A tie on lives is broken by the higher last showdown score, and players still level share the win (a draw).
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

- each player: `lives` (number, visible: public, starts 3): Lives remaining. The player is eliminated at 0. It is never set below 0.
- each player: `eliminated` (bool, visible: public, starts False): True once lives reach 0. An eliminated player takes no further part.
- each player: `last_showdown_score` (number, visible: public, starts 0): The player's score at the most recent showdown. Used as the tie-break on lives.
- the table: `table_up` (number, visible: public, starts 0): The face-up table card in slot U.
- the table: `round_number` (number, visible: public, starts 1): The current round, from 1 to 40.
- the table: `deal_round` (number, visible: public, starts 1): The round number within the current deal.
- the table: `leader_seat` (number, visible: public, starts 1): The seat that leads this round.
- the table: `knocker_seat` (number, visible: public, starts 0): The seat that knocked in this deal, or 0 if nobody has knocked.
- the table: `active_count` (number, visible: public, starts 3): The number of players not eliminated.
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, starting_lives = 3, deck_size = 36, copies_per_value = 4, lowest_card_value = 1, highest_card_value = 9, hand_size = 3, table_cards = 3, max_rounds = 40, prial_base = 300, prial_333_score = 310, run_base = 200, run_123_score = 210, pair_base = 100, pair_multiplier = 10, knock_min_deal_round = 2, life_loss_lowest = 1, life_loss_knocker_lowest = 2, forced_showdown_offset = 1, rank_lives_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.lives * 1000 + you.last_showdown_score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
