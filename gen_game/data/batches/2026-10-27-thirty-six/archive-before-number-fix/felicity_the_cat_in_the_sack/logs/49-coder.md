# 49 coder

- time: 2026-10-27T17:50:12+00:00 (124.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 c1d817c070f2f3a3, reply sha256 fb33666559823595

## Sent

````
# Task: write the XColos game file for "Cat in the Sack: Two Peeks"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

PARAMETERS (table attributes): starting_mice=15, stage1_pass_bonus=2, stage2_pass_bonus=3. The game lasts 9 rounds.

CARDS: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15 (each worth its number), rabbit (worth 0), large_dog, small_dog (worth 0; see the dog rule).

ATTRIBUTES.
- Per player: hand (private list), played_card (private until revealed), mice (public), cat_points (public), bid (public after each poll), in_auction (public).
- Table: set_aside (hidden list), start_seat, round_number, sack_owners, sack_cards (hidden), sack_revealed (public), standing_bid, leader_seat, bidder_count, sack_winner, sack_value.

R1 SETUP (normal initial setup only; do not replace any hands, mice or other state a scenario supplies): Each player's hand is the 10 cards above. One card is chosen at random from each hand and moved to set_aside, unseen by everyone, leaving 9 cards per hand.

R2 SETUP: Each player has mice=starting_mice and cat_points=0. round_number=0. start_seat is chosen at random once.

EACH ROUND:

R3 RESET AND PLAY: round_number increases by 1. Every player gets bid=0 and in_auction=true. Set standing_bid=0, leader_seat=0, bidder_count=0, sack_winner=0, sack_value=0, sack_revealed=[]. Then all players simultaneously choose one card from their own hand; it moves to played_card and the hand shrinks by 1.

R4 BUILD THE SACK: sack_owners lists every seat starting at start_seat, ascending and wrapping round (for example, start_seat 3 of 4 gives [3,4,1,2]). sack_cards holds each owner's played_card in that same order.

R5 FIRST PEEK: sack_cards[1] (the start seat's card) is appended to sack_revealed and shown to all.

R6 STAGE 1 POLL: Simultaneously, each player chooses a whole number from 0 up to their own current mice, inclusive. The choice is stored in bid. A bid of 0 is a pass.

R7 COUNT: bidder_count = the number of players with bid > 0. standing_bid = the highest bid. leader_seat = the player with the highest bid; ties go to whichever comes first in sack_owners. Every player with bid=0 gets in_auction=false. If bidder_count is at least 1, every player with bid=0 also gains stage1_pass_bonus mice.

R8 NO BIDDERS (only when bidder_count=0): Nobody gains anything. sack_cards is cleared, and start_seat advances to the next seat (after the last seat comes seat 1). Steps R9 to R14 are skipped this round.

R9 SOLE BIDDER (only when bidder_count=1): sack_winner=leader_seat, and the price is standing_bid (that player's bid). Stage 2 (R10 to R12) does not happen. Go to R13.

R10 SECOND PEEK (only when bidder_count is at least 2): sack_cards[2] is appended to sack_revealed and shown to all.

R11 STAGE 2 POLL (only when bidder_count is at least 2): Simultaneously, each player with in_auction=true chooses 0 or any whole number from standing_bid+1 up to their own current mice. A player with mice at or below standing_bid may only choose 0. The choice replaces bid.

R12 STAGE 2 RESOLUTION (only when bidder_count is at least 2):
- If any in-auction player bid more than 0, sack_winner is the one with the highest bid (ties go to whichever comes first in sack_owners), and standing_bid becomes that bid.
- Otherwise sack_winner=leader_seat, and the price stays at the stage-1 standing_bid.
- Every in-auction player who chose 0 in stage 2 and is not sack_winner gains stage2_pass_bonus mice.

R13 AWARD (whenever there is a sack_winner):
- The sack_winner pays standing_bid mice to the bank.
- Dog rule: if exactly one dog is among sack_cards, the large dog removes the cat with the highest value, or the small dog removes the cat with the lowest value. If there are no cats, nothing is removed. With 0 or 2 dogs, nothing is removed.
- sack_value = the sum of the values of the remaining cats (rabbit and dogs count 0), and is added to the winner's cat_points.
- All sack_cards are then shown and cleared.

R14 NEXT START: start_seat becomes sack_winner.

R15 END: After round 9, each player's score = cat_points + mice.

How the winner is decided: The highest score (cat_points + mice) wins. If tied, the higher cat_points wins. If still tied, it is a draw among the tied players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Cat in the Sack: Two Peeks (3 to 5 players, best with 4)

Each round every player secretly adds a card to a sack. Players bid mice in up to two sealed stages, seeing one card before each stage. The winner pays and scores the cats inside, and dogs may remove the best or worst cat. Most cat points plus mice after 9 rounds wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts ['cat_-8', 'cat_-5', 'cat_3', 'cat_5', 'cat_8', 'cat_11', 'cat_15', 'rabbit', 'large_dog', 'small_dog']); only its owner sees it. Cards the player may still play. It starts with all 10 cards, and setup removes 1 at random, leaving 9.
  - each player: played_card (text, starts ''); only its owner sees it. The card chosen this round. It stays private until the sack is revealed.
  - each player: mice (number, starts 15); everyone sees it. Currency used for bidding. It counts toward the score.
  - each player: cat_points (number, starts 0); everyone sees it. Total value of the cats won in sacks.
  - each player: bid (number, starts 0); everyone sees it. The latest sealed bid, made public after each poll. 0 is a pass.
  - each player: in_auction (bool, starts True); everyone sees it. Whether the player is still in this round's auction.
  - each player: score (number, starts 15); everyone sees it. cat_points + mice, recalculated at the end of each round.
  - the table: set_aside (list, starts []); hidden from all players. The cards removed unseen from each hand at setup.
  - the table: start_seat (number, starts 0); everyone sees it. The seat whose card is first in the sack. It is chosen at random once.
  - the table: round_number (number, starts 0); everyone sees it. The current round, from 1 to 9.
  - the table: sack_owners (list, starts []); everyone sees it. Seat order in the sack, starting at start_seat and wrapping round.
  - the table: sack_cards (list, starts []); hidden from all players. The played cards in sack_owners order.
  - the table: sack_revealed (list, starts []); everyone sees it. The sack cards peeked at so far this round.
  - the table: standing_bid (number, starts 0); everyone sees it. The current highest bid, which is the price.
  - the table: leader_seat (number, starts 0); everyone sees it. The stage-1 high bidder.
  - the table: bidder_count (number, starts 0); everyone sees it. The number of players with a stage-1 bid above 0.
  - the table: sack_winner (number, starts 0); everyone sees it. The seat that wins the sack. 0 means none.
  - the table: sack_value (number, starts 0); everyone sees it. The cat value awarded this round.
  - parameters, each kept as a table attribute: starting_mice = 15, stage1_pass_bonus = 2, stage2_pass_bonus = 3, rounds = 9, hand_size_dealt = 10, set_aside_per_player = 1, hand_size_after_setup = 9, cat_neg8_value = -8, cat_neg5_value = -5, cat_3_value = 3, cat_5_value = 5, cat_8_value = 8, cat_11_value = 11, cat_15_value = 15, rabbit_value = 0, large_dog_value = 0, small_dog_value = 0, first_peek_index = 1, second_peek_index = 2, min_bid_to_count = 1, rank_score_multiplier = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. This normal setup runs only when a scenario does not supply hands, mice or other state. Supplied state is never replaced.
  2. Each player's hand is set to the 10 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit, large_dog, small_dog.
  3. From each hand, one card is chosen at random, removed from hand and appended to set_aside, unseen by everyone. Each hand is left with 9 cards.
  4. Each player gets mice = starting_mice (15), cat_points = 0 and score = 15.
  5. round_number = 0.
  6. start_seat is chosen uniformly at random from the seats, once.
  7. Each player is synced with their own hand.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_number += 1. For every player: bid = 0, in_auction = true, played_card = ''. For the table: standing_bid = 0, leader_seat = 0, bidder_count = 0, sack_winner = 0, sack_value = 0, sack_revealed = [], sack_owners = [], sack_cards = [].
  2. [poll] all players answers: one card from your own hand. What happens: The chosen card is removed from hand and stored in played_card.
  3. [update] all players. What happens: sack_owners = the seats in ascending order starting at start_seat and wrapping after the last seat to seat 1 (for example, start_seat 3 of 4 gives [3,4,1,2]). sack_cards = each owner's played_card in the same order.
  4. [update] all players. What happens: First peek: sack_cards[1] (the start seat's card) is appended to sack_revealed and broadcast to all.
  5. [poll] all players answers: a whole number from 0 to your own mice (0 = pass). What happens: Stored in bid, then made public.
  6. [update] all players. What happens: bidder_count = the number of players with bid > 0. standing_bid = the maximum bid. leader_seat = the seat with the maximum bid; ties go to the seat earliest in sack_owners. Every player with bid = 0 gets in_auction = false. If bidder_count >= 1, every player with bid = 0 also gets mice += stage1_pass_bonus (2).
  7. [update] all players. What happens: This step runs when bidder_count = 0. sack_cards = []. start_seat = (start_seat mod player_count) + 1. Nobody gains anything, and no later step that needs bidders runs.
  8. [update] all players. What happens: This step runs when bidder_count = 1. sack_winner = leader_seat, and the price stays at standing_bid. There is no stage 2.
  9. [update] all players. What happens: This step runs when bidder_count >= 2. Second peek: sack_cards[2] is appended to sack_revealed and broadcast to all.
  10. [poll] every player with in_auction = true, when bidder_count >= 2 answers: 0, or a whole number from standing_bid+1 to your own mice. A player with mice <= standing_bid may only answer 0.. What happens: The answer replaces bid, which is then made public.
  11. [update] all players. What happens: This step runs when bidder_count >= 2. If any in-auction player has bid > 0: sack_winner = the in-auction seat with the highest bid (ties go to the seat earliest in sack_owners) and standing_bid = that bid. Otherwise sack_winner = leader_seat and standing_bid is unchanged. Then every in-auction player with bid = 0 who is not sack_winner gets mice += stage2_pass_bonus (3).
  12. [update] all players. What happens: This step runs when sack_winner > 0. The sack_winner's mice -= standing_bid. Dog rule: if exactly one of large_dog or small_dog is in sack_cards and at least one cat is there, then large_dog removes one cat with the highest value, or small_dog removes one cat with the lowest value. With 0 or 2 dogs, or no cats, nothing is removed. sack_value = the sum of the values of the remaining cat cards (rabbit and dogs count 0). The sack_winner's cat_points += sack_value. All sack_cards are broadcast to everyone, then sack_cards = [].
  13. [update] all players. What happens: This step runs when sack_winner > 0. start_seat = sack_winner.
  14. [update] all players. What happens: For every player: score = cat_points + mice. Mice, cat_points and score are announced.
  15. [check] all players. What happens: End the game if round_number >= 9. Otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At normal setup each player's hand holds the 10 cards, and 1 random card per hand is moved to set_aside, leaving 9 cards per hand. State supplied by a scenario is not replaced.
  R2. At setup each player has mice = 15 and cat_points = 0, round_number = 0, and start_seat is chosen at random once.
  R3. At the start of each round, round_number increases by 1. Every player has bid = 0 and in_auction = true. standing_bid, leader_seat, bidder_count, sack_winner and sack_value are 0, and sack_revealed is empty.
  R4. Each round every player simultaneously plays one card from their own hand to played_card, so the hand shrinks by 1.
  R5. sack_owners lists the seats from start_seat ascending and wrapping (start_seat 3 of 4 gives [3,4,1,2]), and sack_cards holds the played cards in that order.
  R6. Before stage 1, sack_cards[1] is appended to sack_revealed and shown to all.
  R7. In stage 1 each player simultaneously bids a whole number from 0 to their own mice, and 0 is a pass.
  R8. After stage 1, bidder_count is the number of bids above 0, standing_bid is the highest bid, and leader_seat is the highest bidder, with ties going to the seat earliest in sack_owners.
  R9. After stage 1, every player with bid 0 gets in_auction = false. If bidder_count >= 1, each of them also gains 2 mice.
  R10. When bidder_count = 0, nobody gains or pays, sack_cards is cleared, and start_seat advances by 1 (after the last seat comes seat 1).
  R11. When bidder_count = 1, sack_winner = leader_seat at a price of their stage-1 bid, and there is no second peek or stage 2.
  R12. When bidder_count >= 2, sack_cards[2] is appended to sack_revealed and shown to all.
  R13. In stage 2, each in-auction player simultaneously bids 0 or a number from standing_bid+1 to their mice. A player with mice <= standing_bid may only bid 0.
  R14. If any stage-2 bid is above 0, the highest stage-2 bidder wins (ties go to the seat earliest in sack_owners) and standing_bid becomes that bid. Otherwise leader_seat wins at the stage-1 standing_bid.
  R15. Every in-auction player who bid 0 in stage 2 and is not sack_winner gains 3 mice.
  R16. The sack_winner pays standing_bid mice to the bank.
  R17. If exactly one dog is in the sack, large_dog removes the highest-value cat or small_dog removes the lowest-value cat. With 0 or 2 dogs, or no cats, nothing is removed.
  R18. sack_value is the sum of the values of the remaining cats (rabbit and dogs are worth 0) and is added to the sack_winner's cat_points. All sack_cards are then shown and cleared.
  R19. When there is a sack_winner, start_seat becomes sack_winner.
  R20. The game ends after round 9, and each player's score = cat_points + mice.
  R21. The highest score wins, and ties are broken by higher cat_points. Players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Play a card | asked: all players | options: Every card currently in the player's own hand.
  - Stage 1 bid | asked: all players | options: A whole number from 0 to the player's own mice. A player with 0 mice may only choose 0.
  - Stage 2 bid | asked: players with in_auction = true, only when bidder_count >= 2 | options: A player with mice > standing_bid may choose 0 or a whole number from standing_bid+1 to their mice. A player with mice <= standing_bid may choose only 0. Players out of the auction are not asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number >= 9
  - each player's standing: (you.cat_points + you.mice) * 1000 + you.cat_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The highest cat_points + mice wins. Ties are broken by higher cat_points. Players still tied share the win, which is a draw among them.
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

- each player: `mice` (number, visible: public, starts 15): Currency used for bidding. It counts toward the score.
- each player: `cat_points` (number, visible: public, starts 0): Total value of the cats won in sacks.
- each player: `score` (number, visible: public, starts 15): cat_points + mice, recalculated at the end of each round.
- the table: `start_seat` (number, visible: public, starts 0): The seat whose card is first in the sack. It is chosen at random once.
- the table: `round_number` (number, visible: public, starts 0): The current round, from 1 to 9.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_mice = 15, stage1_pass_bonus = 2, stage2_pass_bonus = 3, rounds = 9, hand_size_dealt = 10, set_aside_per_player = 1, hand_size_after_setup = 9, cat_neg8_value = -8, cat_neg5_value = -5, cat_3_value = 3, cat_5_value = 5, cat_8_value = 8, cat_11_value = 11, cat_15_value = 15, rabbit_value = 0, large_dog_value = 0, small_dog_value = 0, first_peek_index = 1, second_peek_index = 2, min_bid_to_count = 1, rank_score_multiplier = 1000
- the game ends with ONE ending whose `rank_by` is `(you.cat_points + you.mice) * 1000 + you.cat_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

## Guidance from the last attempt

The previous attempt had problems:

1) Make the stage-1 poll a simultaneous numeric choice whose options are every whole number from 0 to that player's current `mice`, inclusive. Store the choice in `bid`. Make the stage-2 poll offer 0 plus standing_bid+1 up to `mice`, and offer it only to in_auction players. 2) Do not deal or replace hands, mice or other state that a scenario supplies. Run the 10-card deal and set-aside only during normal initial setup. Set start_seat at random once, not twice. 3) After stage 1, compute these from the stored bids: bidder_count (bids >= min_bid_to_count), standing_bid (the highest bid) and leader_seat (the highest bidder, ties broken by order in sack_owners). Order sack_owners from start_seat ascending with wrap, e.g. start_seat 3 of 4 gives [3,4,1,2]. Set in_auction=false for bid-0 players. Give those passers stage1_pass_bonus mice when bidder_count >= 1. 4) Implement the three branches with `when` conditions: 0 bidders (clear the sack, advance start_seat), 1 bidder (sole winner at their bid), 2+ bidders (second peek, stage-2 poll, resolution, stage2_pass_bonus for non-winning zero bidders). 5) In the award step, deduct standing_bid from the winner and apply the dog rule (exactly one dog: the large dog removes the highest cat, the small dog removes the lowest). Add sack_value to the winner's cat_points and set start_seat = sack_winner. Recompute score = cat_points + mice each round.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "cat_in_the_sack_two_peeks",
    "name": "Cat in the Sack: Two Peeks",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Each round everyone secretly drops a card in the sack; bid mice in up to two sealed stages after peeking at cards, and score the cats you win."
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
        "initial": [
          "cat_-8",
          "cat_-5",
          "cat_3",
          "cat_5",
          "cat_8",
          "cat_11",
          "cat_15",
          "rabbit",
          "large_dog",
          "small_dog"
        ]
      },
      {
        "key": "played_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "mice",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "cat_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "in_auction",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "stage2_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "starting_mice",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "stage1_pass_bonus",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stage2_pass_bonus",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "hand_size_dealt",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "set_aside_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_size_after_setup",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cat_neg8_value",
        "visible": "public",
        "type": "number",
        "initial": -8
      },
      {
        "key": "cat_neg5_value",
        "visible": "public",
        "type": "number",
        "initial": -5
      },
      {
        "key": "cat_3_value",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cat_5_value",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cat_8_value",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cat_11_value",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "cat_15_value",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "rabbit_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "large_dog_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "small_dog_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_peek_index",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "second_peek_index",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "min_bid_to_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_score_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1000
      },
      {
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "start_seat",
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
        "key": "sack_owners",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "sack_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "sack_revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "standing_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bidder_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sack_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sack_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cat_values",
        "visible": "none",
        "type": "list",
        "initial": []
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the deal and the set-aside",
      "when": {
        "calc": "all(len(p.hand) == hand_size_dealt for p in players) and len(set_aside) == 0"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": [
              "cat_-8",
              "cat_-5",
              "cat_3",
              "cat_5",
              "cat_8",
              "cat_11",
              "cat_15",
              "rabbit",
              "large_dog",
              "small_dog"
            ]
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": {
              "calc": "you.hand[min(len(you.hand) - 1, int(uniform(0, len(you.hand))))]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.played_card"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "[p.played_card for p in players]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "mice",
            "value": {
              "calc": "starting_mice"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cat_points",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_mice"
            }
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 0
          }
        }
      ],
      "text": "Each hand had one card set aside unseen. Every player holds {hand_size_after_setup} cards and {starting_mice} mice."
    },
    {
      "use": "update",
      "label": "the first start seat",
      "when": {
        "calc": "start_seat == 0"
      },
      "do": [
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "min(len(players), 1 + int(uniform(0, len(players))))"
            }
          }
        }
      ],
      "text": "Seat {start_seat} starts the first sack."
    },
    {
      "use": "sync",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "reset",
      "label": "a new round",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "in_auction",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stage2_answer",
            "value": ""
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bidder_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sack_revealed",
            "value": []
          }
        },
        {
          "set": {
            "key": "sack_owners",
            "value": []
          }
        },
        {
          "set": {
            "key": "sack_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "cat_values",
            "value": []
          }
        }
      ],
      "text": "Round {round_number} of {rounds} begins. Seat {start_seat} is first in the sack."
    },
    {
      "use": "sync",
      "phase": "play",
      "label": "your hand now",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "mice",
        "cat_points"
      ],
      "text": "Your hand and purse:"
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play a card",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "played_card",
      "text": "Put one card from your hand into the sack, face down. Nobody else sees it until the sack is opened."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "build the sack",
      "do": [
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.played_card"
            }
          }
        },
        {
          "set": {
            "key": "sack_owners",
            "value": {
              "calc": "[p.seat for p in players if p.seat >= start_seat] + [p.seat for p in players if p.seat < start_seat]"
            }
          }
        },
        {
          "set": {
            "key": "sack_cards",
            "value": {
              "calc": "[p.played_card for p in players if p.seat >= start_seat] + [p.played_card for p in players if p.seat < start_seat]"
            }
          }
        }
      ],
      "text": "The sack is filled in seat order {sack_owners}."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "first peek",
      "do": [
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[first_peek_index - 1]"
            }
          }
        }
      ],
      "text": "First peek: the start seat's card is {sack_revealed}."
    },
    {
      "use": "poll",
      "phase": "stage 1",
      "label": "stage 1 bid",
      "to": {
        "where": "you.mice > 0"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value} in stage 1."
      },
      "text": "Stage 1 sealed bid: a whole number from 0 to your mice. 0 is a pass: you leave this round's auction and, if anyone else bid, gain {stage1_pass_bonus} mice."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "count stage 1",
      "do": [
        {
          "set": {
            "key": "bidder_count",
            "value": {
              "calc": "count(p.bid >= min_bid_to_count for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "[s for s in sack_owners if players[s - 1].bid == standing_bid][0] if bidder_count >= 1 else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.bid == 0"
            },
            "key": "in_auction",
            "value": false
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.bid == 0"
            },
            "key": "mice",
            "value": {
              "calc": "stage1_pass_bonus"
            },
            "if": {
              "calc": "bidder_count >= 1"
            },
            "text": "Seat {player} passed and gains {stage1_pass_bonus} mice."
          }
        }
      ],
      "text": "Stage 1: {bidder_count} bidder(s), standing bid {standing_bid}, leader seat {leader_seat}."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "no bidders",
      "when": {
        "calc": "bidder_count == 0"
      },
      "do": [
        {
          "set": {
            "key": "sack_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "(start_seat % len(players)) + 1"
            }
          }
        }
      ],
      "text": "Nobody bid. The sack is discarded unopened and nobody gains anything. Seat {start_seat} starts next."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "sole bidder",
      "when": {
        "calc": "bidder_count == 1"
      },
      "do": [
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            }
          }
        }
      ],
      "text": "Only seat {sack_winner} bid. They take the sack for {standing_bid} mice; there is no stage 2."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "second peek",
      "when": {
        "calc": "bidder_count >= 2"
      },
      "do": [
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[second_peek_index - 1]"
            }
          }
        }
      ],
      "text": "Second peek: the sack shows {sack_revealed}."
    },
    {
      "use": "poll",
      "phase": "stage 2",
      "label": "stage 2 bid",
      "when": {
        "calc": "bidder_count >= 2"
      },
      "to": {
        "where": "you.in_auction and you.mice > standing_bid"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "standing_bid + 1"
        },
        "max": {
          "calc": "you.mice"
        },
        "or": [
          "pass"
        ]
      },
      "store": "stage2_answer",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers {value} in stage 2."
      },
      "text": "Stage 2 sealed bid: the standing bid is {standing_bid}. Bid a whole number above it, up to your mice, or answer pass (a bid of 0). If nobody bids above 0, the stage-1 leader wins at the standing bid. If you pass and do not win the sack, you gain {stage2_pass_bonus} mice."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "resolve stage 2",
      "when": {
        "calc": "bidder_count >= 2"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.in_auction"
            },
            "key": "bid",
            "value": {
              "calc": "0 if you.stage2_answer in ['', 'pass'] else int(you.stage2_answer)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "[s for s in sack_owners if players[s - 1].in_auction and players[s - 1].bid == max([p.bid for p in players if p.in_auction])][0] if max([p.bid for p in players if p.in_auction]) > 0 else leader_seat"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "players[sack_winner - 1].bid if players[sack_winner - 1].bid > 0 else standing_bid"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.bid == 0 and you.seat != sack_winner"
            },
            "key": "mice",
            "value": {
              "calc": "stage2_pass_bonus"
            },
            "text": "Seat {player} passed in stage 2 and gains {stage2_pass_bonus} mice."
          }
        }
      ],
      "text": "Stage 2 settled: seat {sack_winner} wins the sack at {standing_bid} mice."
    },
    {
      "use": "update",
      "phase": "award",
      "label": "award the sack",
      "when": {
        "calc": "sack_winner > 0"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "sack_winner"
            },
            "key": "mice",
            "value": {
              "calc": "-standing_bid"
            },
            "if": {
              "calc": "players[sack_winner - 1].mice >= standing_bid"
            }
          }
        },
        {
          "set": {
            "key": "cat_values",
            "value": {
              "calc": "[(cat_neg8_value if c == 'cat_-8' else cat_neg5_value if c == 'cat_-5' else cat_3_value if c == 'cat_3' else cat_5_value if c == 'cat_5' else cat_8_value if c == 'cat_8' else cat_11_value if c == 'cat_11' else cat_15_value) for c in sack_cards if c not in ['rabbit', 'large_dog', 'small_dog']]"
            }
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": {
              "calc": "sum(cat_values) + rabbit_value * count(c == 'rabbit' for c in sack_cards) + large_dog_value * count(c == 'large_dog' for c in sack_cards) + small_dog_value * count(c == 'small_dog' for c in sack_cards) - (((max(cat_values) if 'large_dog' in sack_cards else min(cat_values)) if (len(cat_values) > 0 and count(c in ['large_dog', 'small_dog'] for c in sack_cards) == 1) else 0))"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "sack_winner"
            },
            "key": "cat_points",
            "value": {
              "calc": "sack_value"
            }
          }
        }
      ],
      "text": "Seat {sack_winner} pays {standing_bid} mice and opens the sack: {sack_cards}. After the dog rule the cats are worth {sack_value}."
    },
    {
      "use": "update",
      "phase": "award",
      "label": "next start seat",
      "when": {
        "calc": "sack_winner > 0"
      },
      "do": [
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "sack_winner"
            }
          }
        },
        {
          "set": {
            "key": "sack_cards",
            "value": []
          }
        }
      ],
      "text": "Seat {start_seat} will start the next sack."
    },
    {
      "use": "update",
      "phase": "award",
      "label": "the scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.cat_points + you.mice"
            }
          }
        }
      ],
      "text": "After round {round_number} [seat, mice, cat points, score]: {[[p.seat, p.mice, p.cat_points, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "award",
      "label": "after the last round",
      "when": {
        "calc": "round_number >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number >= rounds"
      },
      "rank_by": "(you.cat_points + you.mice) * 1000 + you.cat_points",
      "text": "Winner: {result}. Final [seat, score, cat points]: {[[p.seat, p.cat_points + p.mice, p.cat_points] for p in players]}."
    }
  },
  "limits": {
    "rounds": 9,
    "rounds_max": 10,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Every player starts with the same {hand_size_dealt} cards: cats worth {cat_neg8_value}, {cat_neg5_value}, {cat_3_value}, {cat_5_value}, {cat_8_value}, {cat_11_value} and {cat_15_value}, a rabbit (worth {rabbit_value}), a large dog and a small dog (worth 0; see the dog rule). At setup one random card from each hand is set aside unseen, leaving {hand_size_after_setup} cards. Everyone starts with {starting_mice} mice and 0 cat points. A random seat is chosen once as the start seat. The game lasts {rounds} rounds.\n\nEach round: all players at once put one card from their hand into the sack, face down. The sack is ordered by seat, starting at the start seat and going up, wrapping after the last seat to seat 1 (start seat 3 of 4 gives 3,4,1,2).\n\nFirst peek: the start seat's card is shown to all.\n\nStage 1: all players at once bid a whole number from 0 to their own mice; 0 is a pass. The number of bids above 0 is the bidder count, the highest bid is the standing bid, and the highest bidder is the leader (ties go to the seat earliest in the sack order). Everyone who bid 0 is out of this round's auction; if at least one player bid, each of them gains {stage1_pass_bonus} mice, and if nobody bid they gain nothing.\n\nIf nobody bid: nobody gains or pays, the sack is discarded unopened, and the start seat moves to the next seat (after the last seat comes seat 1).\n\nIf exactly one player bid: that player wins the sack at their stage-1 bid. There is no second peek and no stage 2.\n\nIf two or more bid: the second card in the sack is shown to all. Stage 2: every player still in the auction at once bids 0 (pass) or a whole number from the standing bid + 1 up to their mice; a player whose mice are at or below the standing bid may only bid 0 and is not asked. If anyone bids above 0, the highest stage-2 bidder wins (ties go to the seat earliest in the sack order) and that bid becomes the price. If nobody bids above 0, the stage-1 leader wins at the stage-1 standing bid. Every in-auction player who bid 0 in stage 2 and did not win the sack gains {stage2_pass_bonus} mice.\n\nAward: the winner pays the price in mice to the bank. Dog rule: if exactly one dog is in the sack, the large dog removes the highest-value cat, or the small dog removes the lowest-value cat; with 0 or 2 or more dogs, or no cats, nothing is removed. The remaining cats' values are added up (rabbit and dogs count 0) and added to the winner's cat points, which can go down. All sack cards are then shown and cleared, and the winner becomes the next start seat.\n\nAfter round {rounds}, each player's score is cat points + mice. The highest score wins; a tie is broken by higher cat points; players still tied share the win."
}
```
````
