# 29 coder

- time: 2026-10-27T17:23:09+00:00 (135.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 5e3d86df98a35c06, reply sha256 9d48ae2a5b5aa019

## Sent

````
# Task: write the XColos game file for "Cat in the Sack: Two-Stage Auction"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

CARDS. Every player starts with the same 10 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15 (cats, worth their number), rabbit (worth 0, not a cat), large_dog and small_dog (worth 0).

R1 SETUP. Remove one random card from each player's hand into the face-down set_aside pile, which nobody sees. Each hand now has 9 cards. Hands are private.

R2 SETUP. Each player has 15 mice and 0 cat_points; both are public. Choose start_seat at random. This is the only time start_seat is randomised. Play 9 rounds.

Each round:

R3 PLAY. At the start of the round, set every player's bid to 0 and in_auction to true, standing_bid to 0, leader_seat to 0, sack_done to false and sack_winner to 0. Every player then simultaneously chooses one card from their hand. It leaves their hand and becomes their played_card, which is private.

R4 SACK. sack_owners lists all seats in seat order, beginning with start_seat and continuing to the next higher seat, wrapping from the last seat to seat 1. sack_cards is the list of each owner's played_card in that same order: one card per seat, so 3 to 5 cards. Everyone knows which seat owns each position, but only the owner knows their own card. sack_cards is kept until the end of the round.

R5 TALK. Every player simultaneously writes one short message without seeing the others. Then all messages are shown with names. Talk is not binding; bluffing is allowed.

R6 STAGE 1. Sack card 1 (the start player's card) is revealed to all and added to sack_revealed. The standing_bid is 0. Every player simultaneously writes a whole number from 0 to their mice; every value in that range is an option. The number is stored as that player's bid. A bid of 0 is a pass, and so is any number above the player's mice.

R7 STAGE 1 RESOLUTION. All bids are announced by name. Each passer gains 2 mice and sets in_auction to false. If no one bid, nobody takes the sack: discard sack_cards, set start_seat to the next seat after start_seat, and the round ends. If exactly one player bid, that player wins the sack at once at their bid (go to R10). Otherwise, standing_bid becomes the highest bid. leader_seat is the player with that bid; ties go to the first tied seat in seat order starting from the seat after start_seat.

R8 STAGE 2. Sack card 2 is revealed to all and added to sack_revealed. Each player still in simultaneously writes a number. The options are 0 and every whole number from standing_bid+1 to their mice, where standing_bid is the value set in R7. The number is stored as that player's bid.
- For the leader, 0 means 'hold': their effective bid stays the standing_bid. A legal number above standing_bid is their new effective bid.
- For any other player, a legal number is their effective bid. 0, or any number at or below standing_bid or above their mice, means they drop out with no effective bid.

R9 STAGE 2 RESOLUTION. All stage-2 numbers are announced by name. The winner is the player with the highest effective bid. If tied, the leader wins if they are among the tied players; otherwise the first tied seat in seat order starting from the seat after start_seat wins. Every other player still in at stage 2 gains 3 mice.

R10 TAKING THE SACK. The winner pays their winning bid in mice to the bank. All sack cards are revealed. Dog rule: if exactly one dog is in the whole sack, it removes one cat.
- The large dog removes the highest positive cat. If there is no positive cat, it removes the most negative cat.
- The small dog removes the most negative cat. If there is no negative cat, it removes the lowest positive cat.
- If there is no cat at all, nothing happens.
- If there are zero or two dogs, nothing is removed.
sack_value is the sum of the remaining cat values; the rabbit and dogs count 0. The winner adds sack_value to cat_points (it may be negative). The winner becomes start_seat. All sack cards are then discarded.

R11 END. After round 9, each player's score is cat_points + mice.

How the winner is decided: The highest score (cat_points + mice) wins. If players tie, the one with more cat_points among them wins. If still tied, it is a draw between them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Cat in the Sack: Two-Stage Auction (3 to 5 players, best with 4)

Each round every player secretly adds one card to a shared sack, then everyone bids mice in two simultaneous sealed stages for a sack whose cards are only partly revealed. Final score is cat points plus mice.

STATE (every item below must exist in the file):
  - each player: hand (list, starts ['cat_-8', 'cat_-5', 'cat_3', 'cat_5', 'cat_8', 'cat_11', 'cat_15', 'rabbit', 'large_dog', 'small_dog']); only its owner sees it. The player's private cards. Setup moves one card out at random, leaving 9.
  - each player: played_card (text, starts ''); only its owner sees it. The card this player put into this round's sack.
  - each player: mice (number, starts 15); everyone sees it. The player's money for bidding. It is part of the final score.
  - each player: cat_points (number, starts 0); everyone sees it. The sum of the sack values this player has won. It can be negative.
  - each player: bid (number, starts 0); everyone sees it. The number this player wrote in the current stage. It is announced after each stage.
  - each player: effective_bid (number, starts 0); everyone sees it. The player's effective bid in stage 2. It is 0 if the player has none.
  - each player: in_auction (bool, starts True); everyone sees it. Whether the player is still bidding this round.
  - the table: set_aside (list, starts []); hidden from all players. The face-down pile holding the card removed from each hand at setup.
  - the table: start_seat (number, starts 0); everyone sees it. The start player. That player's card is sack card 1.
  - the table: round_number (number, starts 0); everyone sees it. The number of rounds completed.
  - the table: sack_owners (list, starts []); everyone sees it. The seats in sack order: start_seat first, then upward, wrapping to seat 1.
  - the table: sack_cards (list, starts []); hidden from all players. Each owner's played_card, in sack_owners order.
  - the table: sack_revealed (list, starts []); everyone sees it. The sack cards revealed so far this round.
  - the table: discard_pile (list, starts []); hidden from all players. Sack cards discarded after each round.
  - the table: standing_bid (number, starts 0); everyone sees it. The highest stage-1 bid when two or more players bid.
  - the table: leader_seat (number, starts 0); everyone sees it. The seat holding the standing_bid after stage 1. It is 0 if there is none.
  - the table: bidder_count (number, starts 0); everyone sees it. How many players bid more than 0 in stage 1.
  - the table: sack_done (bool, starts False); everyone sees it. True when the round's sack is settled: nobody bid, or it has been taken.
  - the table: sack_winner (number, starts 0); everyone sees it. The seat that wins the sack this round. It is 0 if there is none.
  - the table: winning_bid (number, starts 0); everyone sees it. The mice the sack winner pays.
  - the table: sack_value (number, starts 0); everyone sees it. The value of the sack won this round, after the dog rule.
  - parameters, each kept as a table attribute: starting_hand_size = 10, set_aside_per_player = 1, hand_size_after_setup = 9, starting_mice = 15, starting_cat_points = 0, rounds = 9, stage1_pass_bonus = 2, stage2_loser_bonus = 3, stage1_min_bid = 0, cat_minus8_value = -8, cat_minus5_value = -5, cat_3_value = 3, cat_5_value = 5, cat_8_value = 8, cat_11_value = 11, cat_15_value = 15, rabbit_value = 0, large_dog_value = 0, small_dog_value = 0, dogs_needed_for_dog_rule = 1, tiebreak_multiplier = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player receives the same 10 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit, large_dog and small_dog.
  2. One random card is removed from each player's hand and appended to the hidden table list set_aside, so each hand holds 9 private cards.
  3. Each player's mice is set to 15 and cat_points to 0. Both are public.
  4. start_seat is chosen at random from the seats. This is the only time it is randomised.
  5. round_number is set to 0. The game lasts 9 rounds.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: For every player, set bid=0, effective_bid=0 and in_auction=true. Set standing_bid=0, leader_seat=0, bidder_count=0, sack_done=false, sack_winner=0, winning_bid=0 and sack_value=0. Set sack_cards=[] and sack_revealed=[].
  2. [poll] all players answers: one card from the player's own hand. What happens: The chosen card is removed from that player's hand and stored as their played_card, which is private.
  3. [update] all players. What happens: Set sack_owners to all seats in order, starting at start_seat and counting upward, wrapping from the last seat to seat 1. Set sack_cards to each owner's played_card in that same order. Announce sack_owners to everyone.
  4. [poll] all players answers: a short free-text message. What happens: No state change. Broadcast to all: "Seat {seat} says: {value}". Talk is not binding.
  5. [update] all players. What happens: Stage 1: reveal sack_cards[1] (the start player's card) by appending it to sack_revealed, and announce it. standing_bid stays 0.
  6. [poll] all players answers: a whole number from 0 to the player's mice. What happens: Store the number as that player's bid.
  7. [update] all players. What happens: Announce every bid by seat. For each player with bid=0 or bid>mice: mice += 2 and in_auction=false. Set bidder_count = the number of players with in_auction=true. If bidder_count=0: sack_done=true and start_seat = (start_seat mod N) + 1. If bidder_count=1: sack_winner = that seat and winning_bid = that player's bid. If bidder_count>=2: standing_bid = the highest bid, and leader_seat = the seat with that bid; on a tie, the tied seat with the smallest (seat - start_seat - 1 + N) mod N.
  8. [update] all players. What happens: When bidder_count>=2 (stage 2): reveal sack_cards[2] by appending it to sack_revealed, and announce it.
  9. [poll] each player with in_auction=true, when bidder_count>=2 answers: 0, or a whole number from standing_bid+1 to the player's mice. What happens: Store the number as that player's bid.
  10. [update] all players. What happens: When bidder_count>=2: announce every stage-2 number by seat. For the leader, effective_bid = standing_bid if bid=0, else bid. For any other in_auction player, effective_bid = bid if standing_bid < bid <= mice, else 0. sack_winner = the seat with the highest effective_bid. On a tie, the leader wins if tied; otherwise the tied seat with the smallest (seat - start_seat - 1 + N) mod N wins. winning_bid = the winner's effective_bid. Every other player with in_auction=true gets mice += 3.
  11. [update] all players. What happens: When sack_winner != 0 (taking the sack): the winner pays mice -= winning_bid. Reveal all of sack_cards by setting sack_revealed = sack_cards. Dog rule, only when exactly one of large_dog and small_dog is in sack_cards. Large dog: remove the highest positive cat, or the most negative cat if there is no positive cat. Small dog: remove the most negative cat, or the lowest positive cat if there is no negative cat. No cat: nothing happens. sack_value = the sum of the remaining cat values (rabbit and dogs count 0). The winner gets cat_points += sack_value. Set start_seat = sack_winner and sack_done = true.
  12. [update] all players. What happens: Append all of sack_cards to discard_pile and set sack_cards=[]. round_number += 1. Announce mice and cat_points for every seat.
  13. [sync] all players. What happens: Each player is sent their own state (hand, mice, cat_points).
  14. [check] all players. What happens: If round_number >= 9 the game ends; otherwise the next round begins.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup each player holds the 10 cards cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit, large_dog and small_dog. One random card from each hand then moves to the hidden set_aside list, leaving 9 cards in each hand.
  R2. At setup each player has mice=15 and cat_points=0, both public. start_seat is chosen at random once, and the game lasts 9 rounds.
  R3. At the start of each round every player has bid=0 and in_auction=true, and standing_bid=0, leader_seat=0, sack_done=false and sack_winner=0. Each player then simultaneously moves one card from their hand to played_card, so the hand shrinks by 1.
  R4. sack_owners lists every seat starting at start_seat, ascending and wrapping, and sack_cards holds each owner's played_card in that order. With start_seat=3 of 4, sack_owners=[3,4,1,2].
  R5. Before stage 1, every player simultaneously sends one short message, and all messages are then shown with seat names.
  R6. In stage 1, sack_cards[1] is appended to sack_revealed, and each player simultaneously picks a bid from 0 to their mice. A bid of 0 is a pass.
  R7. When a player passes in stage 1 (bid 0, or bid above their mice), that player gains 2 mice and gets in_auction=false.
  R8. When nobody bids in stage 1, nobody takes the sack, the sack cards are discarded and start_seat becomes (start_seat mod N)+1. With N=4 and start_seat=4, start_seat becomes 1.
  R9. When exactly one player bids in stage 1, that player wins the sack at their bid, and stage 2 does not happen.
  R10. When two or more players bid in stage 1, standing_bid is the highest bid and leader_seat is its bidder. A tie goes to the first tied seat counting from the seat after start_seat.
  R11. In stage 2, sack_cards[2] is revealed, and each player with in_auction=true is offered 0 or any whole number from standing_bid+1 to their mice.
  R12. When the leader answers 0 in stage 2, their effective bid equals standing_bid. When the leader answers a number above standing_bid, that number is their effective bid.
  R13. When a non-leader answers 0, or a number not above standing_bid or above their mice, in stage 2, that player has no effective bid.
  R14. In stage 2 the highest effective bid wins. On a tie the leader wins if among the tied players; otherwise the first tied seat counting from the seat after start_seat wins.
  R15. When stage 2 resolves, every in_auction player other than the winner gains 3 mice.
  R16. The sack winner pays winning_bid mice, all sack cards are revealed, and the winner becomes start_seat.
  R17. When exactly one dog is in the sack and it is large_dog, it removes the highest positive cat, or the most negative cat if there is no positive cat. Example: a sack of cat_15, cat_3, large_dog has value 3.
  R18. When exactly one dog is in the sack and it is small_dog, it removes the most negative cat, or the lowest positive cat if there is no negative cat. Example: a sack of cat_-8, cat_5, small_dog has value 5.
  R19. When the sack holds zero or two dogs, no cat is removed. Example: a sack of cat_15, large_dog, small_dog has value 15.
  R20. sack_value is the sum of the remaining cat values, with rabbit and dogs worth 0, and it is added to the winner's cat_points even if negative. Example: cat_-8, rabbit, cat_-5 gives -13.
  R21. After round 9 the game ends, and the highest cat_points+mice wins. Ties go to more cat_points, and a remaining tie is a shared win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Play a card into the sack | asked: all players | options: Each card currently in that player's own hand (9 cards in round 1, falling by one each round).
  - Talk message | asked: all players | options: Any short free-text message.
  - Stage 1 bid | asked: all players | options: Every whole number from 0 to the player's current mice (0 = pass).
  - Stage 2 bid | asked: players with in_auction=true when two or more bid in stage 1 | options: The leader: 0 (hold at standing_bid) or every whole number from standing_bid+1 to their mice. Any other in_auction player: 0 (drop out) or every whole number from standing_bid+1 to their mice. If mice < standing_bid+1, only 0 is offered.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number >= 9
  - each player's standing: (you.cat_points + you.mice) * 1000 + you.cat_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's score is cat_points + mice, and the highest score wins. Among tied players, more cat_points wins. Players still tied share the win (a draw).
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

- each player: `mice` (number, visible: public, starts 15): The player's money for bidding. It is part of the final score.
- each player: `cat_points` (number, visible: public, starts 0): The sum of the sack values this player has won. It can be negative.
- the table: `start_seat` (number, visible: public, starts 0): The start player. That player's card is sack card 1.
- the table: `round_number` (number, visible: public, starts 0): The number of rounds completed.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_hand_size = 10, set_aside_per_player = 1, hand_size_after_setup = 9, starting_mice = 15, starting_cat_points = 0, rounds = 9, stage1_pass_bonus = 2, stage2_loser_bonus = 3, stage1_min_bid = 0, cat_minus8_value = -8, cat_minus5_value = -5, cat_3_value = 3, cat_5_value = 5, cat_8_value = 8, cat_11_value = 11, cat_15_value = 15, rabbit_value = 0, large_dog_value = 0, small_dog_value = 0, dogs_needed_for_dog_rule = 1, tiebreak_multiplier = 1000
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

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "cat_in_the_sack",
    "name": "Cat in the Sack: Two-Stage Auction",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Each round everyone secretly drops a card into a shared sack, then bids mice in two sealed stages for a sack only partly revealed."
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
        "key": "effective_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "in_auction",
        "visible": "public",
        "type": "bool",
        "initial": true
      }
    ],
    "game": [
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
        "key": "discard_pile",
        "visible": "none",
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
        "key": "sack_done",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "sack_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winning_bid",
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
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cat_values",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "dog_removed",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_hand_size",
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
        "key": "starting_mice",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "starting_cat_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "stage1_pass_bonus",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stage2_loser_bonus",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "stage1_min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cat_minus8_value",
        "visible": "public",
        "type": "number",
        "initial": -8
      },
      {
        "key": "cat_minus5_value",
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
        "key": "dogs_needed_for_dog_rule",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the hands",
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
        }
      ],
      "text": "Every player receives the same {starting_hand_size} cards."
    },
    {
      "use": "update",
      "label": "set cards aside",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[0].hand[min(len(players[0].hand) - 1, int(uniform(0, len(players[0].hand))))]"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "append": {
            "key": "set_aside",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "remove": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[1].hand[min(len(players[1].hand) - 1, int(uniform(0, len(players[1].hand))))]"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "append": {
            "key": "set_aside",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "remove": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[2].hand[min(len(players[2].hand) - 1, int(uniform(0, len(players[2].hand))))]"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "append": {
            "key": "set_aside",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "remove": {
            "player": 3,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "set_aside_per_player >= 1"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[3].hand[min(len(players[3].hand) - 1, int(uniform(0, len(players[3].hand))))]"
            },
            "if": {
              "calc": "len(players) >= 4 and set_aside_per_player >= 1"
            }
          }
        },
        {
          "append": {
            "key": "set_aside",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4 and set_aside_per_player >= 1"
            }
          }
        },
        {
          "remove": {
            "player": 4,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4 and set_aside_per_player >= 1"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[4].hand[min(len(players[4].hand) - 1, int(uniform(0, len(players[4].hand))))]"
            },
            "if": {
              "calc": "len(players) >= 5 and set_aside_per_player >= 1"
            }
          }
        },
        {
          "append": {
            "key": "set_aside",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 5 and set_aside_per_player >= 1"
            }
          }
        },
        {
          "remove": {
            "player": 5,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 5 and set_aside_per_player >= 1"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ],
      "text": "One random card from each hand is set aside face down. Each hand now holds {hand_size_after_setup} cards."
    },
    {
      "use": "update",
      "label": "mice and start player",
      "do": [
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
            "value": {
              "calc": "starting_cat_points"
            }
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "min(len(players), int(uniform(1, len(players) + 1)))"
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
      "text": "Everyone has {starting_mice} mice and {starting_cat_points} cat points. Seat {start_seat} is the start player. The game lasts {rounds} rounds."
    },
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
      "use": "update",
      "phase": "play",
      "label": "new round",
      "do": [
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
            "key": "effective_bid",
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
            "key": "sack_done",
            "value": false
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
            "key": "winning_bid",
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
            "key": "sack_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "sack_revealed",
            "value": []
          }
        }
      ],
      "text": "A new round begins. Rounds completed: {round_number} of {rounds}. Start player: seat {start_seat}."
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
      "text": "Choose one card from your hand to put face down into this round's sack. Only you will know which card it is until the sack is taken."
    },
    {
      "use": "update",
      "phase": "sack",
      "label": "the sack",
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
              "calc": "[(start_seat - 1 + p.seat - 1) % len(players) + 1 for p in players]"
            }
          }
        },
        {
          "set": {
            "key": "sack_cards",
            "value": {
              "calc": "[players[s - 1].played_card for s in sack_owners]"
            }
          }
        }
      ],
      "text": "The sack is filled. Sack positions belong to seats {sack_owners}, in that order."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Say one short thing to the table about the sack. Talk is not binding; bluffing is allowed."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "reveal card 1",
      "do": [
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[0]"
            }
          }
        }
      ],
      "text": "Stage 1: sack card 1 (seat {start_seat}'s card) is revealed. Revealed so far: {sack_revealed}. The standing bid is {standing_bid}."
    },
    {
      "use": "poll",
      "phase": "stage 1",
      "label": "stage 1 bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "stage1_min_bid"
        },
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "text": "Stage 1 sealed bid: write a whole number of mice from 0 to your mice. 0 is a pass: you gain {stage1_pass_bonus} mice and are out of this round's auction."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "stage 1 resolution",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.bid == 0 or you.bid > you.mice"
            },
            "key": "in_auction",
            "value": false
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.in_auction"
            },
            "key": "mice",
            "value": {
              "calc": "stage1_pass_bonus"
            },
            "text": "Seat {player} passes and gains {stage1_pass_bonus} mice."
          }
        },
        {
          "set": {
            "key": "bidder_count",
            "value": {
              "calc": "count(p.in_auction for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "bidder_count == 0"
            }
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "start_seat % len(players) + 1"
            },
            "if": {
              "calc": "bidder_count == 0"
            },
            "text": "Nobody bid. Nobody takes the sack; it is discarded and the start player moves to seat {value}."
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "min([p.seat for p in players if p.in_auction])"
            },
            "if": {
              "calc": "bidder_count == 1"
            },
            "text": "Only one player bid: seat {value} wins the sack at once."
          }
        },
        {
          "set": {
            "key": "winning_bid",
            "value": {
              "calc": "sum([p.bid for p in players if p.in_auction])"
            },
            "if": {
              "calc": "bidder_count == 1"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.in_auction])"
            },
            "if": {
              "calc": "bidder_count >= 2"
            },
            "text": "The standing bid is {value}."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "(min([(p.seat - start_seat - 1 + len(players)) % len(players) for p in players if p.in_auction and p.bid == standing_bid]) + start_seat) % len(players) + 1"
            },
            "if": {
              "calc": "bidder_count >= 2"
            },
            "text": "Seat {value} is the leader."
          }
        }
      ],
      "text": "Stage 1 bids [seat, bid]: {[[p.seat, p.bid] for p in players]}. Players who bid: {bidder_count}."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "reveal card 2",
      "when": {
        "calc": "bidder_count >= 2"
      },
      "do": [
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[1]"
            }
          }
        }
      ],
      "text": "Stage 2: sack card 2 is revealed. Revealed so far: {sack_revealed}. Standing bid {standing_bid}, held by seat {leader_seat}."
    },
    {
      "use": "poll",
      "phase": "stage 2",
      "label": "stage 2 bid",
      "when": {
        "calc": "bidder_count >= 2"
      },
      "to": {
        "where": "you.in_auction"
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
          "0"
        ]
      },
      "store": "bid",
      "text": "Stage 2 sealed bid. Standing bid {standing_bid}, leader seat {leader_seat}. Answer 0, or a whole number from {standing_bid}+1 to your mice. If you are the leader, 0 holds: your bid stays {standing_bid}. Anyone else who answers 0 drops out with no bid. Highest bid wins; a tie goes to the leader if tied, otherwise to the first tied seat after the start player. Everyone else still in gains {stage2_loser_bonus} mice."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "stage 2 resolution",
      "when": {
        "calc": "bidder_count >= 2"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.in_auction"
            },
            "key": "effective_bid",
            "value": {
              "calc": "(standing_bid if you.bid in [0, '0'] else you.bid) if you.seat == leader_seat else (0 if you.bid in [0, '0'] else (you.bid if you.bid > standing_bid and you.bid <= you.mice else 0))"
            }
          }
        },
        {
          "set": {
            "key": "winning_bid",
            "value": {
              "calc": "max([p.effective_bid for p in players if p.in_auction])"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat if players[leader_seat - 1].effective_bid == winning_bid else (min([(p.seat - start_seat - 1 + len(players)) % len(players) for p in players if p.in_auction and p.effective_bid == winning_bid]) + start_seat) % len(players) + 1"
            },
            "text": "Seat {value} wins the sack."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.seat != sack_winner"
            },
            "key": "mice",
            "value": {
              "calc": "stage2_loser_bonus"
            },
            "text": "Seat {player} loses stage 2 and gains {stage2_loser_bonus} mice."
          }
        }
      ],
      "text": "Stage 2 numbers [seat, number]: {[[p.seat, p.bid] for p in players if p.in_auction]}. Effective bids [seat, bid]: {[[p.seat, p.effective_bid] for p in players if p.in_auction]}."
    },
    {
      "use": "update",
      "phase": "take",
      "label": "taking the sack",
      "when": {
        "calc": "sack_winner != 0"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "sack_winner"
            },
            "key": "mice",
            "value": {
              "calc": "-winning_bid"
            },
            "if": {
              "calc": "players[sack_winner - 1].mice >= winning_bid"
            },
            "text": "Seat {player} pays {winning_bid} mice."
          }
        },
        {
          "set": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards"
            }
          }
        },
        {
          "set": {
            "key": "cat_values",
            "value": {
              "calc": "[cat_minus8_value if c == 'cat_-8' else (cat_minus5_value if c == 'cat_-5' else (cat_3_value if c == 'cat_3' else (cat_5_value if c == 'cat_5' else (cat_8_value if c == 'cat_8' else (cat_11_value if c == 'cat_11' else cat_15_value))))) for c in sack_cards if c in ['cat_-8', 'cat_-5', 'cat_3', 'cat_5', 'cat_8', 'cat_11', 'cat_15']]"
            }
          }
        },
        {
          "set": {
            "key": "dog_removed",
            "value": {
              "calc": "0 if count(c in ['large_dog', 'small_dog'] for c in sack_cards) != dogs_needed_for_dog_rule or len(cat_values) == 0 else ((max(cat_values) if max(cat_values) > 0 else min(cat_values)) if 'large_dog' in sack_cards else min(cat_values))"
            }
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": {
              "calc": "sum(cat_values) - dog_removed + sum([rabbit_value if c == 'rabbit' else (large_dog_value if c == 'large_dog' else small_dog_value) for c in sack_cards if c in ['rabbit', 'large_dog', 'small_dog']])"
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
            },
            "text": "Seat {player} adds {value} to their cat points."
          }
        },
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
            "key": "sack_done",
            "value": true
          }
        }
      ],
      "text": "Seat {sack_winner} takes the sack for {winning_bid} mice. The sack held {sack_revealed}. Sack value after the dog rule: {sack_value}. Seat {sack_winner} is the new start player."
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "clear the sack",
      "do": [
        {
          "set": {
            "key": "discard_pile",
            "value": {
              "calc": "discard_pile + sack_cards"
            }
          }
        },
        {
          "set": {
            "key": "sack_cards",
            "value": []
          }
        },
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        }
      ],
      "text": "Round {round_number} of {rounds} is over. Standings [seat, mice, cat_points]: {[[p.seat, p.mice, p.cat_points] for p in players]}."
    },
    {
      "use": "sync",
      "phase": "end of round",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "mice",
        "cat_points"
      ],
      "text": "Where you stand:"
    },
    {
      "use": "check",
      "phase": "end of round",
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
      "text": "Winner: {result}. Final [seat, score (cat_points + mice), cat_points]: {[[p.seat, p.cat_points + p.mice, p.cat_points] for p in players]}."
    }
  },
  "limits": {
    "rounds": 9,
    "rounds_max": 10,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "CARDS. Every player starts with the same {starting_hand_size} cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15 (cats, worth their number), rabbit (worth {rabbit_value}, not a cat), large_dog and small_dog (worth 0).\n\nSETUP. One random card is removed from each player's hand into a face-down set-aside pile, which nobody sees. Each hand then has {hand_size_after_setup} cards. Hands are private. Each player has {starting_mice} mice and {starting_cat_points} cat points; both are public. The start player is chosen at random; this is the only time it is randomised. The game lasts {rounds} rounds.\n\nEACH ROUND.\n1. PLAY. Every player's bid is reset to 0 and everyone is back in the auction; the standing bid is 0 and there is no leader. Every player simultaneously chooses one card from their hand; it leaves their hand and goes face down into the sack. Only you know your own card.\n2. SACK. The sack is ordered by seat: the start player's card is sack card 1, then the next higher seat, wrapping from the last seat to seat 1. Everyone knows which seat owns each position.\n3. TALK. Every player simultaneously writes one short message; all messages are then shown with seat names. Talk is not binding; bluffing is allowed.\n4. STAGE 1. Sack card 1 (the start player's card) is revealed. The standing bid is 0. Every player simultaneously writes a whole number from 0 to their mice. A bid of 0 is a pass, and so is any number above the player's mice.\n5. STAGE 1 RESOLUTION. All bids are announced by seat. Each passer gains {stage1_pass_bonus} mice and is out of the auction for this round. If no one bid, nobody takes the sack: the sack cards are discarded, the start player moves to the next seat, and the round ends. If exactly one player bid, that player wins the sack at once at their bid, and there is no stage 2. Otherwise the standing bid becomes the highest bid and the leader is the player with that bid; ties go to the first tied seat in seat order starting from the seat after the start player.\n6. STAGE 2. Sack card 2 is revealed. Each player still in simultaneously writes 0 or a whole number from the standing bid + 1 to their mice (if you cannot reach standing bid + 1, only 0 is possible). For the leader, 0 means hold: their bid stays the standing bid; a number above the standing bid is their new bid. For any other player, a number above the standing bid is their bid; 0 means they drop out with no bid.\n7. STAGE 2 RESOLUTION. All stage-2 numbers are announced by seat. The highest bid wins. If tied, the leader wins if among the tied players; otherwise the first tied seat in seat order starting from the seat after the start player wins. Every other player still in at stage 2 gains {stage2_loser_bonus} mice.\n8. TAKING THE SACK. The winner pays their winning bid in mice to the bank. All sack cards are revealed. Dog rule: if exactly one dog is in the whole sack, it removes one cat. The large dog removes the highest positive cat; if there is no positive cat, it removes the most negative cat. The small dog removes the most negative cat; if there is no negative cat, it removes the lowest positive cat. If there is no cat at all, nothing happens. If there are zero or two dogs, nothing is removed. The sack value is the sum of the remaining cat values; the rabbit and dogs count 0. The winner adds the sack value to their cat points, even if it is negative. The winner becomes the start player. All sack cards are then discarded.\n\nEND. After round {rounds}, each player's score is cat points + mice. The highest score wins. Among tied players, more cat points wins. Players still tied share the win."
}
```
````
