# 15 coder

- time: 2026-10-27T17:01:34+00:00 (114.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 881f8f2efe667a42, reply sha256 787089a4e1b75c69

## Sent

````
# Task: write the XColos game file for "Cat in the Sack: Sealed Stages (Revised)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
- Each player gets an identical hand of 10 cards: cats worth -8, -5, 3, 5, 8, 11 and 15; a rabbit worth 0; a large dog; and a small dog.
- One random card is removed from each hand and set aside unseen by everyone. Each player keeps 9 cards in a private hand.
- Each player starts with 15 mice and 0 cat points. Both numbers are public throughout.
- Seats are in a fixed order. A random player is the first start player.

EACH ROUND (9 rounds; every player plays exactly one card per round, so every hand is empty after round 9)

1. Fill the sack and talk.
   - All players, at the same moment, choose one card from their hand and place it face down. The card leaves their hand.
   - In the same moment, each player writes one short message (at most 30 words). Messages are free text, may claim anything and are not enforced.

2. Lay out the sack.
   - The sack is laid out in seat order beginning with the start player. Sack card 1 is the start player's card, card 2 belongs to the next player in seat order, and so on.
   - Everyone knows whose card is in each position. Only the owner knows its face.
   - All messages are now shown to everyone, labelled with each writer's name.

3. Stage 1.
   - Sack card 1 is revealed to all. The standing bid is 0 and there is no leader.
   - All players, at the same moment, write a whole number. 0 means pass; anything else is a bid.
   - A bid must be at least the standing bid + 1 and at most the player's current mice. An illegal number counts as a pass.

4. Resolve the stage. Apply these rules after every stage, in this order:
   a. Announce: every bidder's number (bid, or 0 for a pass) is shown to all by name.
   b. All passed at stage 1: if every player passed, every player gains 2 mice, nobody takes the sack, and it is discarded without being opened. Go to step 9.
   c. All passed at stage 2 or 3: if every player still in passed, the leader from the previous stage takes the sack at the standing bid and gains no reward. Every other player who passed at this stage gains the reward for this stage. Go to step 7.
   d. Otherwise:
      - Each player who passed at this stage leaves the auction for the round and gains mice from the bank: 2 at stage 1, 3 at stage 2, 4 at stage 3.
      - The standing bid becomes the highest bid made at this stage, and the player who made it is the leader.
      - If several players made the highest bid, the leader is the first of them in seat order, counting from the player after the start player, with the start player counted last.
      - The new standing bid, the leader and every player's mice are announced.
   e. Immediate win: if exactly one player is still in, that player wins the sack at the standing bid just set. Skip the remaining stages and go to step 7.

5. Stage 2.
   - Played only if two or more players are still in.
   - Sack card 2 is revealed.
   - The players still in, at the same moment, pass (0) or bid between the standing bid + 1 and their current mice. An illegal number is a pass.
   - Resolve as in step 4.

6. Stage 3.
   - Played only if two or more players are still in.
   - Sack card 3 is revealed.
   - The players still in, at the same moment, pass or bid under the same rules.
   - Resolve as in step 4.
   - Then, if two or more players are still in, the leader wins the sack at the standing bid, and each player who bid at stage 3 but is not the leader gains 5 mice.

7. Open the sack.
   - All sack cards are revealed. With 4 or 5 players, cards 4 and 5 are seen for the first time.
   - Dog rule: if exactly one dog is in the sack, it removes one cat. The large dog removes the highest-valued cat; the small dog removes the lowest-valued cat. If no cat is present, nothing is removed. If both dogs are present, neither has any effect.
   - All dogs and any removed cat are discarded.

8. Pay and score.
   - The sack winner pays their winning bid in mice to the bank.
   - The sack winner adds the total value of the cats remaining in the sack to their cat points. Cat points may go negative. The rabbit is worth 0.
   - The sack cards are discarded face up, so everyone can see which cards each player has used.

9. Next start player.
   - The sack winner becomes the start player.
   - If nobody took the sack, the start player passes to the next seat.

END
After round 9, each player's score is cat points + mice.

How the winner is decided: The player with the highest score (cat points + mice) wins. If several players tie, the tied player with the most cat points wins. If they are still tied, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Cat in the Sack: Sealed Stages (Revised) (3 to 5 players, best with 4)

Each round every player secretly adds one card to a shared sack and writes a message. The sack is then auctioned over up to three sealed-bid stages, with one more card revealed at each stage. After 9 rounds the highest cat points + mice wins.

STATE (every item below must exist in the file):
  - each player: seat (number, starts '1..N in fixed seat order'); everyone sees it. the player's fixed seat number
  - each player: hand (list, starts 'the 10 identical cards minus one random card set aside (9 cards)'); only its owner sees it. cards the player can still put in the sack; card codes are cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit, large_dog, small_dog
  - each player: mice (number, starts 15); everyone sees it. the player's mice, used for bidding; counts toward the score
  - each player: cat_points (number, starts 0); everyone sees it. total value of the cats won in sacks; may be negative
  - each player: played_card (text, starts ''); only its owner sees it. the card the player put face down in the sack this round
  - each player: message (text, starts ''); everyone sees it. the player's message this round (at most 30 words), shown after all are written
  - each player: bid (number, starts 0); everyone sees it. the number written at the current stage; 0 is a pass, and an illegal number is treated as 0
  - each player: in_auction (bool, starts True); everyone sees it. whether the player is still in the auction this round
  - the table: round_number (number, starts 0); everyone sees it. rounds started so far
  - the table: start_seat (number, starts 'a random seat'); everyone sees it. seat of the current start player
  - the table: set_aside (list, starts "the one random card removed from each player's 10"); hidden from all players. the cards set aside unseen at setup
  - the table: sack_owners (list, starts []); everyone sees it. seat owning each sack position, in seat order starting with the start player
  - the table: sack_cards (list, starts []); hidden from all players. card faces in sack position order (each owner knows their own card through played_card)
  - the table: sack_revealed (list, starts []); everyone sees it. sack cards revealed so far, in position order
  - the table: stage (number, starts 0); everyone sees it. current auction stage, 1 to 3
  - the table: standing_bid (number, starts 0); everyone sees it. the current standing bid
  - the table: leader_seat (number, starts 0); everyone sees it. seat of the current leader; 0 means no leader
  - the table: sack_done (bool, starts False); everyone sees it. whether this round's auction is settled
  - the table: sack_winner (number, starts 0); everyone sees it. seat that took the sack this round; 0 means nobody
  - the table: sack_value (number, starts 0); everyone sees it. total value of the cats left in the opened sack after the dog rule
  - the table: discard_pile (list, starts []); everyone sees it. opened sack cards, discarded face up with their owners
  - the table: unopened_pile (list, starts []); hidden from all players. unrevealed cards of sacks discarded without being opened
  - parameters, each kept as a table attribute: cat_value_1 = -8, cat_value_2 = -5, cat_value_3 = 3, cat_value_4 = 5, cat_value_5 = 8, cat_value_6 = 11, cat_value_7 = 15, cats_per_hand = 7, rabbit_value = 0, dogs_per_hand = 2, hand_size_dealt = 10, cards_set_aside_per_player = 1, hand_size_kept = 9, starting_mice = 15, starting_cat_points = 0, rounds = 9, message_max_words = 30, max_stages = 3, pass_reward_stage_1 = 2, pass_reward_stage_2 = 3, pass_reward_stage_3 = 4, all_pass_stage_1_reward = 2, stage_3_outbid_bonus = 5, initial_standing_bid = 0, rank_tiebreak_multiplier = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Each player is given the same 10 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit, large_dog, small_dog.
  2. One random card is removed from each player's hand and appended to set_aside, unseen by everyone; each hand keeps 9 cards.
  3. Each player's mice is set to 15 and cat_points to 0; both are public.
  4. Seats are numbered 1..N in a fixed order, and start_seat is set to a random seat.
  5. Each player is sent their own state.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [poll] all players answers: short text, at most 30 words. What happens: message := the text; nobody sees any message until the messages are shown in step 4
  2. [poll] all players answers: one card from own hand. What happens: played_card := the chosen card; the card is removed from hand; nobody sees another player's choice
  3. [update] all players. What happens: round_number += 1; sack_owners := seats in seat order beginning with start_seat; sack_cards := each owner's played_card in that order; sack_revealed := []; standing_bid := 0; leader_seat := 0; stage := 1; sack_done := false; sack_winner := 0; sack_value := 0; every in_auction := true; every bid := 0. Announce whose card is in each position.
  4. [tell] all players. What happens: broadcast every message labelled by seat: 'Seat {seat} says: {message}'
  5. [update] all players. What happens: append sack_cards[1] to sack_revealed and announce it; stage := 1
  6. [poll] all players answers: a whole number from 0 to own mice. What happens: bid := the number; if bid < standing_bid + 1 or bid > mice, then bid := 0 (pass)
  7. [update] all players. What happens: Announce every bid by seat. If every bid = 0: every player's mice += 2, sack_cards are appended to unopened_pile, sack_winner := 0, sack_done := true. Otherwise: every player with bid = 0 sets in_auction := false and mice += 2; standing_bid := highest bid; leader_seat := the first seat with that bid, in seat order from the seat after start_seat with start_seat last; announce standing_bid, leader_seat and everyone's mice; if exactly one player has in_auction = true, then sack_winner := leader_seat and sack_done := true.
  8. [update] all players. What happens: when sack_done = false and count(in_auction) >= 2: stage := 2; append sack_cards[2] to sack_revealed and announce it; bid := 0 for all
  9. [poll] players with in_auction = true, when sack_done = false and stage = 2 answers: a whole number from 0 to own mice. What happens: bid := the number; if bid < standing_bid + 1 or bid > mice, then bid := 0
  10. [update] all players. What happens: when sack_done = false and stage = 2: announce bids. If every in_auction player bid 0: sack_winner := leader_seat (the previous leader, at the current standing_bid, with no reward); every in_auction player other than leader_seat gains mice += 3; sack_done := true. Otherwise: each in_auction player with bid 0 sets in_auction := false and mice += 3; standing_bid := highest bid; leader_seat := the first seat with that bid in the tie order; announce standing_bid, leader_seat and mice; if exactly one in_auction remains, then sack_winner := leader_seat and sack_done := true.
  11. [update] all players. What happens: when sack_done = false and count(in_auction) >= 2: stage := 3; append sack_cards[3] to sack_revealed and announce it; bid := 0 for all
  12. [poll] players with in_auction = true, when sack_done = false and stage = 3 answers: a whole number from 0 to own mice. What happens: bid := the number; if bid < standing_bid + 1 or bid > mice, then bid := 0
  13. [update] all players. What happens: when sack_done = false and stage = 3: announce bids. If every in_auction player bid 0: sack_winner := leader_seat; every in_auction player other than leader_seat gains mice += 4; sack_done := true. Otherwise: each in_auction player with bid 0 sets in_auction := false and mice += 4; standing_bid := highest bid; leader_seat := the first seat with that bid in the tie order; announce standing_bid, leader_seat and mice; if exactly one in_auction remains, then sack_winner := leader_seat and sack_done := true.
  14. [update] all players. What happens: when sack_done = false: sack_winner := leader_seat; every player with bid >= 1 at stage 3 and seat != leader_seat gains mice += 5; sack_done := true
  15. [update] all players. What happens: when sack_winner != 0: reveal all sack_cards (sack_revealed := sack_cards). Dog rule: if large_dog is in the sack and small_dog is not, remove the highest-valued cat; if small_dog is in the sack and large_dog is not, remove the lowest-valued cat; if no cat is present, nothing is removed; if both dogs are present, neither has any effect. sack_value := sum of the values of the cats remaining (rabbit 0; dogs and removed cats count nothing). The sack_winner pays mice -= standing_bid and gains cat_points += sack_value. All sack cards are appended face up to discard_pile with their owners. Announce the result.
  16. [update] all players. What happens: if sack_winner != 0, then start_seat := sack_winner; otherwise start_seat := the next seat after start_seat (wrapping from N to 1)
  17. [check] all players. What happens: end the game if round_number >= 9; otherwise continue to the next round

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each player has the same 10 cards (cats -8, -5, 3, 5, 8, 11, 15; rabbit 0; large dog; small dog), and one random card from each hand goes to set_aside unseen, leaving 9 cards per hand.
  R2. At setup, each player has 15 mice and 0 cat_points, both public, and start_seat is a random seat.
  R3. Each round, every player simultaneously chooses one card from their hand; it leaves the hand and becomes their played_card.
  R4. Each round, every player writes one message of at most 30 words; all messages are shown to everyone, labelled by seat, only after all are written.
  R5. The sack is ordered in seat order beginning with the start player, so sack position 1 is the start player's card; everyone knows the owner of each position.
  R6. At stage 1, sack card 1 is revealed to all, the standing bid is 0 and there is no leader.
  R7. At each stage, the players still in simultaneously write a number; 0 is a pass, and a bid must be at least standing_bid + 1 and at most the bidder's mice, or it counts as a pass.
  R8. After each stage, every player's bid (0 for a pass) is announced by name.
  R9. When every player passes at stage 1, then every player gains 2 mice, nobody takes the sack, it is discarded unopened, and play goes to choosing the next start player.
  R10. When every player still in passes at stage 2, then the previous leader takes the sack at the standing bid with no reward, and every other passer gains 3 mice.
  R11. When every player still in passes at stage 3, then the previous leader takes the sack at the standing bid with no reward, and every other passer gains 4 mice.
  R12. When not everyone passed, then each passer leaves the auction for the round and gains 2 mice at stage 1, 3 at stage 2 or 4 at stage 3.
  R13. When not everyone passed, then the standing bid becomes the highest bid at that stage, and its bidder becomes the leader.
  R14. When several players make the highest bid, then the leader is the first of them in seat order, counting from the player after the start player, with the start player last.
  R15. After a stage is resolved, the new standing bid, the leader and every player's mice are announced.
  R16. When exactly one player remains in after a stage, then that player wins the sack at the standing bid just set and the remaining stages are skipped.
  R17. Stage 2 reveals sack card 2 and stage 3 reveals sack card 3, and each is played only if two or more players are still in.
  R18. When two or more players are still in after stage 3 is resolved, then the leader wins the sack at the standing bid, and each other player who bid at stage 3 gains 5 mice.
  R19. When the sack is opened, all its cards are revealed.
  R20. When exactly one dog is in the sack, then the large dog removes the highest-valued cat or the small dog removes the lowest-valued cat; when no cat is present nothing is removed, and when both dogs are present neither has any effect.
  R21. The sack winner pays their winning bid in mice and adds the total value of the remaining cats to cat_points, which may go negative; the rabbit is worth 0.
  R22. Opened sack cards are discarded face up, so everyone can see which cards each player has used.
  R23. When someone took the sack, then the sack winner becomes the start player; otherwise the start player passes to the next seat.
  R24. The game ends after round 9, when every hand is empty.
  R25. At the end, the highest cat_points + mice wins; a tie goes to the most cat_points, and players still tied draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Message for this round | asked: every seat | options: free text of at most 30 words
  - Card to put in the sack | asked: every seat | options: any card currently in that seat's hand
  - Stage 1 bid | asked: every seat | options: a whole number from 0 to that seat's mice; 0 is a pass
  - Stage 2 bid | asked: seats with in_auction = true, only if two or more are still in | options: a whole number from 0 to that seat's mice; 0 or any number at or below the standing bid is a pass; a seat that has left the auction is not asked
  - Stage 3 bid | asked: seats with in_auction = true, only if two or more are still in | options: a whole number from 0 to that seat's mice; 0 or any number at or below the standing bid is a pass; a seat that has left the auction is not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number >= 9
  - each player's standing: (you.cat_points + you.mice) * 1000 + you.cat_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's score is cat points + mice, and the highest score wins. Among tied players, the one with more cat points wins. Players still tied share the win (a draw among them).
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

- each player: `mice` (number, visible: public, starts 15): the player's mice, used for bidding; counts toward the score
- each player: `cat_points` (number, visible: public, starts 0): total value of the cats won in sacks; may be negative
- the table: `start_seat` (number, visible: public, starts 'a random seat'): seat of the current start player
- parameters (each must be an attribute holding this value, never a number buried in a step): cat_value_1 = -8, cat_value_2 = -5, cat_value_3 = 3, cat_value_4 = 5, cat_value_5 = 8, cat_value_6 = 11, cat_value_7 = 15, cats_per_hand = 7, rabbit_value = 0, dogs_per_hand = 2, hand_size_dealt = 10, cards_set_aside_per_player = 1, hand_size_kept = 9, starting_mice = 15, starting_cat_points = 0, rounds = 9, message_max_words = 30, max_stages = 3, pass_reward_stage_1 = 2, pass_reward_stage_2 = 3, pass_reward_stage_3 = 4, all_pass_stage_1_reward = 2, stage_3_outbid_bonus = 5, initial_standing_bid = 0, rank_tiebreak_multiplier = 1000
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

Rebuild the bid choice for each stage as a simultaneous numeric poll among the players still in. Its options must be 0 (pass) plus every whole number from standing_bid + 1 up to that player's current mice. At stage 1 with 15 mice that is 0 and 1..15; check this against the stage-1 standing bid of initial_standing_bid = 0. Any number outside that range must be treated as a pass. Then confirm resolution from these bids works:
- A sole bidder becomes leader and wins immediately at their bid.
- They pay mice, gain the cat value after the dog rule, and become start_seat.
- Passers gain the stage reward.
- A stage-2 bid at or below the standing bid counts as a pass.
For the stage-1 all-pass case, the whole sack is discarded unopened, so all sack cards, including card 1, go to the unopened pile. Card 1 being face up while players bid does not count as opening the sack. Every player gains all_pass_stage_1_reward, and start_seat moves to the next seat, wrapping from the last seat back to 1.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
{
  "schema": 1,
  "meta": {
    "id": "cat_in_the_sack_sealed_stages_revised",
    "name": "Cat in the Sack: Sealed Stages (Revised)",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Everyone slips a card into a shared sack. The sack is then auctioned in up to three sealed stages, with one card shown per stage. Highest cat points plus mice after 9 rounds wins."
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
        "key": "played_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "draft",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "aside_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "start_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
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
        "key": "stage",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "sack_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "discard_pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "unopened_pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "cat_pairs",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "cat_value_1",
        "visible": "public",
        "type": "number",
        "initial": -8
      },
      {
        "key": "cat_value_2",
        "visible": "public",
        "type": "number",
        "initial": -5
      },
      {
        "key": "cat_value_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cat_value_4",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cat_value_5",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cat_value_6",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "cat_value_7",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "cats_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "rabbit_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dogs_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_size_dealt",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "cards_set_aside_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_size_kept",
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
        "key": "message_max_words",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "max_stages",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pass_reward_stage_1",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "pass_reward_stage_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pass_reward_stage_3",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "all_pass_stage_1_reward",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stage_3_outbid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "initial_standing_bid",
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
        },
        {
          "set": {
            "key": "cat_pairs",
            "value": {
              "calc": "[['cat_-8', cat_value_1], ['cat_-5', cat_value_2], ['cat_3', cat_value_3], ['cat_5', cat_value_4], ['cat_8', cat_value_5], ['cat_11', cat_value_6], ['cat_15', cat_value_7]]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set one card aside",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "aside_card",
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
              "calc": "you.aside_card"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "[p.aside_card for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "mice, points and the start player",
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
              "calc": "min(len(players), 1 + int(uniform(0, len(players))))"
            }
          }
        }
      ],
      "text": "Everyone starts with {starting_mice} mice and {starting_cat_points} cat points. Seat {start_seat} is the first start player."
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
      "use": "poll",
      "phase": "sack",
      "label": "write a message",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "draft",
      "text": "Write one short message (at most {message_max_words} words) for the table. It may claim anything and is not binding. Nobody sees it until all messages are written and the sack is laid out."
    },
    {
      "use": "poll",
      "phase": "sack",
      "label": "fill the sack",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "played_card",
      "text": "Choose one card from your hand to put face down in the sack. It leaves your hand. Nobody else sees your choice."
    },
    {
      "use": "update",
      "phase": "sack",
      "label": "lay out the sack",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
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
            "players": "all",
            "key": "message",
            "value": {
              "calc": "you.draft"
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
        },
        {
          "set": {
            "key": "sack_revealed",
            "value": []
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "initial_standing_bid"
            }
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
            "key": "stage",
            "value": 1
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
            "key": "sack_value",
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
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Round {round_number} of {rounds}. The sack is laid out. Its positions, in order, hold the cards of seats {sack_owners}."
    },
    {
      "use": "tell",
      "phase": "sack",
      "label": "the messages",
      "to": "all",
      "text": "This round's messages, as [seat, message]: {[[p.seat, p.message] for p in players]}"
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "reveal sack card 1",
      "do": [
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[0]"
            }
          }
        },
        {
          "set": {
            "key": "stage",
            "value": 1
          }
        }
      ],
      "text": "Stage 1: sack card 1 (seat {start_seat}'s card) is revealed. Revealed so far: {sack_revealed}. The standing bid is {standing_bid} and there is no leader."
    },
    {
      "use": "poll",
      "phase": "stage 1",
      "label": "stage 1 bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "text": "Stage 1. Standing bid {standing_bid}. Write 0 to pass, or bid a whole number from standing bid + 1 up to your mice ({mice}). Passing takes you out of this round's auction and earns {pass_reward_stage_1} mice, unless everyone passes."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "resolve stage 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "you.bid if (you.in_auction and you.bid >= standing_bid + 1 and you.bid <= you.mice) else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "mice",
            "value": {
              "calc": "all_pass_stage_1_reward"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "unopened_pile",
            "value": {
              "calc": "unopened_pile + sack_cards"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": 0,
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            },
            "text": "Everyone passed at stage 1: every player gains {all_pass_stage_1_reward} mice, nobody takes the sack and it is discarded unopened."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "([p.seat for p in players if p.seat > start_seat and p.bid == max([q.bid for q in players])] + [p.seat for p in players if p.seat <= start_seat and p.bid == max([q.bid for q in players])])[0]"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([q.bid for q in players])"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_1"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "in_auction",
            "value": false,
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            },
            "text": "Only seat {leader_seat} is still in: they win the sack at {standing_bid}."
          }
        }
      ],
      "text": "Stage 1 bids, as [seat, bid] (0 is a pass): {[[p.seat, p.bid] for p in players]}. Standing bid {standing_bid}, leader seat {leader_seat} (0 = none). Mice, as [seat, mice]: {[[p.seat, p.mice] for p in players]}."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "reveal sack card 2",
      "when": {
        "calc": "not sack_done and count(p.in_auction for p in players) >= 2"
      },
      "do": [
        {
          "set": {
            "key": "stage",
            "value": 2
          }
        },
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[1]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Stage 2: sack card 2 (seat {sack_owners[1]}'s card) is revealed. Revealed so far: {sack_revealed}. Standing bid {standing_bid}, leader seat {leader_seat}."
    },
    {
      "use": "poll",
      "phase": "stage 2",
      "label": "stage 2 bid",
      "when": {
        "calc": "not sack_done and stage == 2"
      },
      "to": {
        "where": "you.in_auction"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "text": "Stage 2. Standing bid {standing_bid}, leader seat {leader_seat}. Write 0 to pass, or bid a whole number from standing bid + 1 up to your mice ({mice}); a number at or below the standing bid is a pass. Passing earns {pass_reward_stage_2} mice, but if everyone still in passes, the leader takes the sack at the standing bid and gains nothing."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "resolve stage 2",
      "when": {
        "calc": "not sack_done and stage == 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "you.bid if (you.in_auction and you.bid >= standing_bid + 1 and you.bid <= you.mice) else 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.seat != leader_seat"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_2"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            },
            "text": "Everyone still in passed at stage 2: seat {leader_seat} takes the sack at {standing_bid}; the other passers gain {pass_reward_stage_2} mice."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "([p.seat for p in players if p.seat > start_seat and p.bid == max([q.bid for q in players])] + [p.seat for p in players if p.seat <= start_seat and p.bid == max([q.bid for q in players])])[0]"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([q.bid for q in players])"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_2"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "in_auction",
            "value": false,
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            },
            "text": "Only seat {leader_seat} is still in: they win the sack at {standing_bid}."
          }
        }
      ],
      "text": "Stage 2 bids, as [seat, bid] (0 is a pass or not in): {[[p.seat, p.bid] for p in players]}. Standing bid {standing_bid}, leader seat {leader_seat}. Mice, as [seat, mice]: {[[p.seat, p.mice] for p in players]}."
    },
    {
      "use": "update",
      "phase": "stage 3",
      "label": "reveal sack card 3",
      "when": {
        "calc": "not sack_done and count(p.in_auction for p in players) >= 2"
      },
      "do": [
        {
          "set": {
            "key": "stage",
            "value": 3
          }
        },
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[2]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Stage 3: sack card 3 (seat {sack_owners[2]}'s card) is revealed. Revealed so far: {sack_revealed}. Standing bid {standing_bid}, leader seat {leader_seat}."
    },
    {
      "use": "poll",
      "phase": "stage 3",
      "label": "stage 3 bid",
      "when": {
        "calc": "not sack_done and stage == 3"
      },
      "to": {
        "where": "you.in_auction"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "text": "Stage 3, the last. Standing bid {standing_bid}, leader seat {leader_seat}. Write 0 to pass, or bid a whole number from standing bid + 1 up to your mice ({mice}); a number at or below the standing bid is a pass. Passing earns {pass_reward_stage_3} mice; if two or more stay in, the leader takes the sack and every other stage-3 bidder gains {stage_3_outbid_bonus} mice."
    },
    {
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {mice} (in `prompt`: 'Stage 1. Standing bid 0. Write 0 to pass, or bid a whole number from standing bid + 1 up t'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {mice} (in `prompt`: 'Stage 1. Standing bid 0. Write 0 to pass, or bid a whole number from standing bid + 1 up t'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {mice} (in `prompt`: 'Stage 1. Standing bid 0. Write 0 to pass, or bid a whole number from standing bid + 1 up t'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "cat_in_the_sack_sealed_stages_revised",
    "name": "Cat in the Sack: Sealed Stages (Revised)",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Everyone slips a card into a shared sack, which is auctioned in up to three sealed stages with one card shown per stage. Highest cat points plus mice after 9 rounds wins."
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
        "key": "played_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "draft",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "aside_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "start_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
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
        "key": "stage",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "sack_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "discard_pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "unopened_pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "sack_cats",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "cat_value_1",
        "visible": "public",
        "type": "number",
        "initial": -8
      },
      {
        "key": "cat_value_2",
        "visible": "public",
        "type": "number",
        "initial": -5
      },
      {
        "key": "cat_value_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cat_value_4",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cat_value_5",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cat_value_6",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "cat_value_7",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "cats_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "rabbit_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dogs_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_size_dealt",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "cards_set_aside_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_size_kept",
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
        "key": "message_max_words",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "max_stages",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pass_reward_stage_1",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "pass_reward_stage_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pass_reward_stage_3",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "all_pass_stage_1_reward",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stage_3_outbid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "initial_standing_bid",
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
      ]
    },
    {
      "use": "update",
      "label": "set one card aside",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "aside_card",
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
              "calc": "you.aside_card"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "[p.aside_card for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "mice, points and the start player",
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
              "calc": "min(len(players), 1 + int(uniform(0, len(players))))"
            }
          }
        }
      ],
      "text": "Everyone starts with {starting_mice} mice and {starting_cat_points} cat points. Seat {start_seat} is the first start player."
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
      "use": "poll",
      "phase": "sack",
      "label": "write a message",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "draft",
      "text": "Write one short message (at most {message_max_words} words) for the table. It may claim anything and is not binding. Nobody sees it until all messages are written and the sack is laid out."
    },
    {
      "use": "poll",
      "phase": "sack",
      "label": "fill the sack",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "played_card",
      "text": "Choose one card from your hand to put face down in the sack. It leaves your hand. Nobody else sees your choice."
    },
    {
      "use": "update",
      "phase": "sack",
      "label": "lay out the sack",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
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
            "players": "all",
            "key": "message",
            "value": {
              "calc": "you.draft"
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
        },
        {
          "set": {
            "key": "sack_revealed",
            "value": []
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "initial_standing_bid"
            }
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
            "key": "stage",
            "value": 1
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
            "key": "sack_value",
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
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Round {round_number} of {rounds}. The sack is laid out. Its positions, in order, hold the cards of seats {sack_owners}."
    },
    {
      "use": "tell",
      "phase": "sack",
      "label": "the messages",
      "to": "all",
      "text": "This round's messages, as [seat, message]: {[[p.seat, p.message] for p in players]}"
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "reveal sack card 1",
      "do": [
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[0]"
            }
          }
        },
        {
          "set": {
            "key": "stage",
            "value": 1
          }
        }
      ],
      "text": "Stage 1: sack card 1 (seat {start_seat}'s card) is revealed. Revealed so far: {sack_revealed}. The standing bid is {standing_bid} and there is no leader."
    },
    {
      "use": "poll",
      "phase": "stage 1",
      "label": "stage 1 bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "text": "Stage 1. Standing bid {standing_bid}. Write 0 to pass, or bid a whole number from the standing bid + 1 up to your current mice. Passing takes you out of this round's auction and earns {pass_reward_stage_1} mice; if everyone passes, everyone gains {all_pass_stage_1_reward} mice instead and the sack is discarded unopened."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "resolve stage 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "you.bid if (you.in_auction and you.bid >= standing_bid + 1 and you.bid <= you.mice) else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "mice",
            "value": {
              "calc": "all_pass_stage_1_reward"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "unopened_pile",
            "value": {
              "calc": "unopened_pile + sack_cards"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": 0,
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            },
            "text": "Everyone passed at stage 1: every player gains {all_pass_stage_1_reward} mice, nobody takes the sack and it is discarded unopened."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "([p.seat for p in players if p.seat > start_seat and p.bid == max([q.bid for q in players])] + [p.seat for p in players if p.seat <= start_seat and p.bid == max([q.bid for q in players])])[0]"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([q.bid for q in players])"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_1"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "in_auction",
            "value": false,
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            },
            "text": "Only seat {leader_seat} is still in: they win the sack at {standing_bid}."
          }
        }
      ],
      "text": "Stage 1 bids, as [seat, bid] (0 is a pass): {[[p.seat, p.bid] for p in players]}. Standing bid {standing_bid}, leader seat {leader_seat} (0 = none). Mice, as [seat, mice]: {[[p.seat, p.mice] for p in players]}."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "reveal sack card 2",
      "when": {
        "calc": "not sack_done and count(p.in_auction for p in players) >= 2"
      },
      "do": [
        {
          "set": {
            "key": "stage",
            "value": 2
          }
        },
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[1]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Stage 2: sack card 2 is revealed. Sack owners in position order: {sack_owners}. Revealed so far: {sack_revealed}. Standing bid {standing_bid}, leader seat {leader_seat}."
    },
    {
      "use": "poll",
      "phase": "stage 2",
      "label": "stage 2 bid",
      "when": {
        "calc": "not sack_done and stage == 2"
      },
      "to": {
        "where": "you.in_auction"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "text": "Stage 2. Standing bid {standing_bid}, leader seat {leader_seat}. Write 0 to pass, or bid a whole number from the standing bid + 1 up to your current mice; a number at or below the standing bid is a pass. If someone bids, each passer leaves the auction and earns {pass_reward_stage_2} mice. If everyone still in passes, the leader takes the sack at the standing bid with no reward and every other passer earns {pass_reward_stage_2} mice."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "resolve stage 2",
      "when": {
        "calc": "not sack_done and stage == 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "you.bid if (you.in_auction and you.bid >= standing_bid + 1 and you.bid <= you.mice) else 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.seat != leader_seat"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_2"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            },
            "text": "Everyone still in passed at stage 2: seat {leader_seat} takes the sack at {standing_bid}; the other passers gain {pass_reward_stage_2} mice."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "([p.seat for p in players if p.seat > start_seat and p.bid == max([q.bid for q in players])] + [p.seat for p in players if p.seat <= start_seat and p.bid == max([q.bid for q in players])])[0]"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([q.bid for q in players])"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_2"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "in_auction",
            "value": false,
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            },
            "text": "Only seat {leader_seat} is still in: they win the sack at {standing_bid}."
          }
        }
      ],
      "text": "Stage 2 bids, as [seat, bid] (0 is a pass or not in): {[[p.seat, p.bid] for p in players]}. Standing bid {standing_bid}, leader seat {leader_seat}. Mice, as [seat, mice]: {[[p.seat, p.mice] for p in players]}."
    },
    {
      "use": "update",
      "phase": "stage 3",
      "label": "reveal sack card 3",
      "when": {
        "calc": "not sack_done and count(p.in_auction for p in players) >= 2"
      },
      "do": [
        {
          "set": {
            "key": "stage",
            "value": 3
          }
        },
        {
          "append": {
            "key": "sack_revealed",
            "value": {
              "calc": "sack_cards[2]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Stage 3: sack card 3 is revealed. Sack owners in position order: {sack_owners}. Revealed so far: {sack_revealed}. Standing bid {standing_bid}, leader seat {leader_seat}."
    },
    {
      "use": "poll",
      "phase": "stage 3",
      "label": "stage 3 bid",
      "when": {
        "calc": "not sack_done and stage == 3"
      },
      "to": {
        "where": "you.in_auction"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "text": "Stage 3, the last. Standing bid {standing_bid}, leader seat {leader_seat}. Write 0 to pass, or bid a whole number from the standing bid + 1 up to your current mice; a number at or below the standing bid is a pass. If someone bids, each passer leaves and earns {pass_reward_stage_3} mice; if two or more stay in, the leader takes the sack and every other stage-3 bidder gains {stage_3_outbid_bonus} mice. If everyone still in passes, the leader takes the sack at the standing bid with no reward and every other passer earns {pass_reward_stage_3} mice."
    },
    {
      "use": "update",
      "phase": "stage 3",
      "label": "resolve stage 3",
      "when": {
        "calc": "not sack_done and stage == 3"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "you.bid if (you.in_auction and you.bid >= standing_bid + 1 and you.bid <= you.mice) else 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.seat != leader_seat"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_3"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "not any(p.bid > 0 for p in players)"
            },
            "text": "Everyone still in passed at stage 3: seat {leader_seat} takes the sack at {standing_bid}; the other passers gain {pass_reward_stage_3} mice."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "([p.seat for p in players if p.seat > start_seat and p.bid == max([q.bid for q in players])] + [p.seat for p in players if p.seat <= start_seat and p.bid == max([q.bid for q in players])])[0]"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([q.bid for q in players])"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "mice",
            "value": {
              "calc": "pass_reward_stage_3"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.in_auction and you.bid == 0"
            },
            "key": "in_auction",
            "value": false,
            "if": {
              "calc": "any(p.bid > 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            },
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            }
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true,
            "if": {
              "calc": "any(p.bid > 0 for p in players) and count(p.in_auction for p in players) == 1"
            },
            "text": "Only seat {leader_seat} is still in: they win the sack at {standing_bid}."
          }
        }
      ],
      "text": "Stage 3 bids, as [seat, bid] (0 is a pass or not in): {[[p.seat, p.bid] for p in players]}. Standing bid {standing_bid}, leader seat {leader_seat}. Mice, as [seat, mice]: {[[p.seat, p.mice] for p in players]}."
    },
    {
      "use": "update",
      "phase": "stage 3",
      "label": "stage 3 leader takes the sack",
      "when": {
        "calc": "not sack_done"
      },
      "do": [
        {
          "set": {
            "key": "sack_winner",
            "value": {
              "calc": "leader_seat"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.bid >= 1 and you.seat != leader_seat"
            },
            "key": "mice",
            "value": {
              "calc": "stage_3_outbid_bonus"
            },
            "text": "Seat {player} was outbid at stage 3 and gains {stage_3_outbid_bonus} mice."
          }
        },
        {
          "set": {
            "key": "sack_done",
            "value": true
          }
        }
      ],
      "text": "Two or more players stayed in through stage 3: seat {leader_seat} wins the sack at {standing_bid}."
    },
    {
      "use": "update",
      "phase": "open",
      "label": "open the sack",
      "when": {
        "calc": "sack_winner != 0"
      },
      "do": [
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
            "key": "sack_cats",
            "value": {
              "calc": "[(cat_value_1 if c == 'cat_-8' else cat_value_2 if c == 'cat_-5' else cat_value_3 if c == 'cat_3' else cat_value_4 if c == 'cat_5' else cat_value_5 if c == 'cat_8' else cat_value_6 if c == 'cat_11' else cat_value_7) for c in sack_cards if c not in ['rabbit', 'large_dog', 'small_dog']]"
            }
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": {
              "calc": "sum(sack_cats) - (max(sack_cats + [-1000]) if ('large_dog' in sack_cards and 'small_dog' not in sack_cards and len(sack_cats) > 0) else 0) - (min(sack_cats + [1000]) if ('small_dog' in sack_cards and 'large_dog' not in sack_cards and len(sack_cats) > 0) else 0) + rabbit_value * count(c == 'rabbit' for c in sack_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "sack_winner"
            },
            "key": "mice",
            "value": {
              "calc": "-min(standing_bid, players[sack_winner - 1].mice)"
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
        },
        {
          "set": {
            "key": "discard_pile",
            "value": {
              "calc": "discard_pile + [[p.seat, p.played_card] for p in players]"
            }
          }
        }
      ],
      "text": "The sack is opened: {sack_revealed} (owners in order {sack_owners}). After the dog rule the cats are worth {sack_value}. Seat {sack_winner} pays {standing_bid} mice and adds {sack_value} cat points."
    },
    {
      "use": "update",
      "phase": "open",
      "label": "next start player",
      "do": [
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "sack_winner if sack_winner != 0 else (start_seat + 1 if start_seat < len(players) else 1)"
            }
          }
        }
      ],
      "text": "Seat {start_seat} is the start player. Standings as [seat, mice, cat points]: {[[p.seat, p.mice, p.cat_points] for p in players]}."
    },
    {
      "use": "check",
      "phase": "open",
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
    "rounds_max": 9,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "SETUP. Each player gets an identical hand of {hand_size_dealt} cards: cats worth {cat_value_1}, {cat_value_2}, {cat_value_3}, {cat_value_4}, {cat_value_5}, {cat_value_6} and {cat_value_7}; a rabbit worth {rabbit_value}; a large dog; and a small dog. One random card is removed from each hand and set aside unseen by everyone, so each player keeps {hand_size_kept} cards in a private hand. Each player starts with {starting_mice} mice and {starting_cat_points} cat points; both numbers are public throughout. Seats are in a fixed order and a random player is the first start player.\n\nEACH ROUND ({rounds} rounds; every player plays exactly one card per round).\n1. Fill the sack and talk. All players, at the same moment, choose one card from their hand and place it face down; the card leaves their hand. Each player also writes one short message (at most {message_max_words} words); messages may claim anything and are not enforced.\n2. Lay out the sack in seat order beginning with the start player: sack card 1 is the start player's card, card 2 belongs to the next player in seat order, and so on. Everyone knows whose card is in each position; only the owner knows its face. All messages are now shown to everyone, labelled by seat.\n3. Stage 1. Sack card 1 is revealed to all. The standing bid is {initial_standing_bid} and there is no leader. All players, at the same moment, write a whole number: 0 means pass, anything else is a bid. A bid must be at least the standing bid + 1 and at most the player's current mice; an illegal number counts as a pass.\n4. Resolve the stage, after every stage, in this order: (a) every player's number (bid, or 0 for a pass) is shown to all by seat. (b) If every player passed at stage 1, every player gains {all_pass_stage_1_reward} mice, nobody takes the sack, and it is discarded without being opened; go to step 9. (c) If every player still in passed at stage 2 or 3, the leader from the previous stage takes the sack at the standing bid and gains no reward, and every other player who passed at this stage gains the reward for this stage; go to step 7. (d) Otherwise, each player who passed at this stage leaves the auction for the round and gains mice: {pass_reward_stage_1} at stage 1, {pass_reward_stage_2} at stage 2, {pass_reward_stage_3} at stage 3. The standing bid becomes the highest bid made at this stage and the player who made it is the leader. If several players made the highest bid, the leader is the first of them in seat order, counting from the player after the start player, with the start player counted last. The new standing bid, the leader and every player's mice are announced. (e) If exactly one player is still in, that player wins the sack at the standing bid just set; skip the remaining stages and go to step 7.\n5. Stage 2, played only if two or more players are still in: sack card 2 is revealed; the players still in, at the same moment, pass (0) or bid between the standing bid + 1 and their current mice; an illegal number is a pass. Resolve as in step 4.\n6. Stage 3, played only if two or more players are still in: sack card 3 is revealed; the players still in pass or bid under the same rules. Resolve as in step 4. Then, if two or more players are still in, the leader wins the sack at the standing bid, and each player who bid at stage 3 but is not the leader gains {stage_3_outbid_bonus} mice.\n7. Open the sack: all sack cards are revealed. Dog rule: if exactly one dog is in the sack, it removes one cat; the large dog removes the highest-valued cat and the small dog removes the lowest-valued cat. If no cat is present, nothing is removed. If both dogs are present, neither has any effect. All dogs and any removed cat are discarded.\n8. Pay and score: the sack winner pays their winning bid in mice to the bank and adds the total value of the cats remaining in the sack to their cat points. Cat points may go negative; the rabbit is worth {rabbit_value}. The sack cards are discarded face up with their owners, so everyone can see which cards each player has used.\n9. Next start player: the sack winner becomes the start player. If nobody took the sack, the start player passes to the next seat (from the last seat back to seat 1).\n\nEND. After round {rounds}, each player's score is cat points + mice. The highest score wins. If several players tie, the tied player with the most cat points wins; if they are still tied, they share the win."
}
```
````
