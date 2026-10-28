# 10 coder

- time: 2026-10-28T02:35:05+00:00 (125.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 a39ea82c46d32876, reply sha256 90aeae74425c9323

## Sent

````
# Task: write the XColos game file for "Officers' Schafkopf: Bidding Match"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK. There are 16 cards: Ace, Ten, Ober and Unter in each of four suits (Acorns, Leaves, Hearts, Bells). Card points are Ace 11, Ten 10, Ober 3 and Unter 2, which makes 104 in the deck.

MATCH. The match is 4 hands. Each hand is one bidding round followed by 8 trick rounds, which makes 36 rounds in total. Player 1 deals hands 1 and 3 and Player 2 deals hands 2 and 4. The non-dealer is called forehand.

DEAL (start of each hand's bidding round, the only random event of the round). Shuffle the 16 cards. Each player receives:
- 4 private hand cards, seen only by their owner;
- 2 stacks, each made of one face-down card under one face-up card.
The face-up cards (4 in total) are visible to both players. Face-down cards are unknown to both players, including their owner.

BIDDING ROUND.
(1) Both players secretly and simultaneously choose a bid: Pass, 53, 66 or 79. The bid is the number of card points the player promises to take as declarer.
(2) The higher bid becomes declarer at that bid. If the bids are equal and not Pass, forehand is declarer at that bid. If both pass, forehand is declarer at 53. Both bids are then announced.
(3) The declarer chooses a contract and it is announced:
- Acorns Solo, Leaves Solo, Hearts Solo or Bells Solo: trumps are, from highest to lowest, Ober of Acorns, Ober of Leaves, Ober of Hearts, Ober of Bells, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells, then the Ace and the Ten of the chosen suit. The three other suits each hold only Ace above Ten.
- Wenz: trumps are, from highest to lowest, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells. Each suit holds Ace above Ten above Ober.
(4) The defender chooses Stoß (double) or No Stoß, and the choice is announced. The multiplier is 2 with Stoß and 1 without.

TRICK ROUNDS (8 per hand).
Available cards: a player may play any of their private hand cards or any face-up card on top of one of their stacks.
Lead: in the first trick forehand leads; afterwards the winner of the previous trick leads. The leader plays one available card.
Follow: the other player then plays one available card. All trumps count as one suit, the trump suit, so in a Solo an Ober or Unter is never a card of its printed suit. If the follower has an available card of the led suit, they must play one. Otherwise they may play any available card.
Trick winner: if any trump was played, the higher trump wins. Otherwise the higher card of the led suit wins. The winner adds the card points of both cards to their card-point total for this hand.
Reveal: after the trick, any face-down card whose face-up card was played this trick is turned face up. It is available from the next trick on.

HAND SCORING (after trick 8).
- If the declarer's card points are at least their bid, the declarer scores the contract value in match points. Otherwise the defender scores it.
- Contract value = base, plus 1 if the player who scores took all 8 tricks, multiplied by the Stoß multiplier.
- The base is 2 for a bid of 53, 3 for a bid of 66 and 4 for a bid of 79.
Each player's card points for the hand are also added to their running card-point total for the match. Then all cards are collected for the next deal.

How the winner is decided: After 4 hands, the player with more match points wins. If match points are equal, the player with the higher total card points over all 4 hands wins. If both are equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Officers' Schafkopf: Bidding Match (2 to 2 players, best with 2)

A two-player Schafkopf match of 4 hands with a 16-card deck, open and face-down stacks, sealed bids for the declarer's contract, an optional Stoß, and 8 tricks per hand. Match points decide the winner, total card points break ties.

STATE (every item below must exist in the file):
  - each player: match_points (number, starts 0); everyone sees it. Match points won so far.
  - each player: card_total (number, starts 0); everyone sees it. Running card-point total over all completed hands, used as the tie-break.
  - each player: hand_points (number, starts 0); everyone sees it. Card points taken in tricks during the current hand.
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won in the current hand.
  - each player: hand (list, starts []); only its owner sees it. The 4 private hand cards, seen only by their owner.
  - each player: stack1_up (text, starts ''); everyone sees it. Face-up card on top of stack 1 (empty when none).
  - each player: stack2_up (text, starts ''); everyone sees it. Face-up card on top of stack 2 (empty when none).
  - each player: stack1_pending_reveal (bool, starts False); everyone sees it. True once stack 1's face-up card has been played this trick, so the card beneath it turns up after the trick.
  - each player: stack2_pending_reveal (bool, starts False); everyone sees it. The same for stack 2.
  - each player: bid (number, starts 0); everyone sees it. This hand's bid (0 = Pass, or 53, 66, 79). It is collected by a sealed poll and announced after both bids are in.
  - the table: deck (list, starts ['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns', 'Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves', 'Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts', 'Ace of Bells', 'Ten of Bells', 'Ober of Bells', 'Unter of Bells']); hidden from all players. The undealt cards.
  - the table: seat1_stack1_down (text, starts ''); hidden from all players. Face-down card under seat 1's stack 1, unknown to both players.
  - the table: seat1_stack2_down (text, starts ''); hidden from all players. Face-down card under seat 1's stack 2.
  - the table: seat2_stack1_down (text, starts ''); hidden from all players. Face-down card under seat 2's stack 1.
  - the table: seat2_stack2_down (text, starts ''); hidden from all players. Face-down card under seat 2's stack 2.
  - the table: hand_number (number, starts 1); everyone sees it. The current hand, from 1 to 4.
  - the table: round_in_hand (number, starts 0); everyone sees it. 0 = bidding round; 1 to 8 = trick number.
  - the table: rounds_played (number, starts 0); everyone sees it. Rounds completed, out of 36.
  - the table: dealer (number, starts 1); everyone sees it. Seat dealing this hand: seat 1 in hands 1 and 3, seat 2 in hands 2 and 4.
  - the table: forehand (number, starts 2); everyone sees it. The non-dealer.
  - the table: declarer (number, starts 0); everyone sees it. Declarer's seat this hand.
  - the table: defender (number, starts 0); everyone sees it. Defender's seat this hand.
  - the table: contract_bid (number, starts 0); everyone sees it. The card points the declarer must reach (53, 66 or 79).
  - the table: contract (text, starts ''); everyone sees it. Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo or Wenz.
  - the table: multiplier (number, starts 1); everyone sees it. 2 with Stoß, 1 without.
  - the table: leader (number, starts 0); everyone sees it. Seat that leads the current trick.
  - the table: follower (number, starts 0); everyone sees it. The other seat.
  - the table: led_card (text, starts ''); everyone sees it. The card led to the current trick.
  - the table: followed_card (text, starts ''); everyone sees it. The card played second to the current trick.
  - the table: follow_options (list, starts []); everyone sees it. Legal cards for the follower, worked out by the follow-suit rule.
  - parameters, each kept as a table attribute: deck_size = 16, points_ace = 11, points_ten = 10, points_ober = 3, points_unter = 2, deck_points = 104, hands_in_match = 4, tricks_per_hand = 8, rounds_per_hand = 9, total_rounds = 36, private_cards_per_player = 4, stacks_per_player = 2, face_up_cards_on_table = 4, bid_pass = 0, bid_low = 53, bid_mid = 66, bid_high = 79, default_bid_when_both_pass = 53, base_for_53 = 2, base_for_66 = 3, base_for_79 = 4, all_tricks_bonus = 1, multiplier_stoss = 2, multiplier_no_stoss = 1, trump_strength_ober_acorns = 20, trump_strength_ober_leaves = 19, trump_strength_ober_hearts = 18, trump_strength_ober_bells = 17, trump_strength_unter_acorns = 16, trump_strength_unter_leaves = 15, trump_strength_unter_hearts = 14, trump_strength_unter_bells = 13, trump_strength_solo_suit_ace = 12, trump_strength_solo_suit_ten = 11, plain_rank_ace = 3, plain_rank_ten = 2, plain_rank_ober = 1, plain_rank_unter = 0, rank_weight_match_points = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set hand_number to 1, round_in_hand to 0, rounds_played to 0, and each player's match_points and card_total to 0.
  2. Seat 1 is dealer for hand 1, so seat 2 is forehand.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round_in_hand == 0 (the deal):
- Set dealer = 1 if hand_number is odd, else 2, and set forehand to the other seat.
- Refill deck with all 16 cards.
- For each seat, draw 4 random cards from deck into hand, then 1 into stack1_up, 1 into the seat's stack1_down table attribute, 1 into stack2_up, and 1 into the seat's stack2_down table attribute.
- Reset hand_points, tricks_won, bid and the pending_reveal flags.
- Reset contract, multiplier = 1, declarer = 0 and defender = 0.
  2. [sync] all players. What happens: Each player sees their own hand, all four face-up stack cards, and the public table state.
  3. [poll] all players answers: one of: Pass, 53, 66, 79. What happens: When round_in_hand == 0: each player's bid is set to their answer (Pass = 0). No one sees a bid until both are in.
  4. [update] all players. What happens: When round_in_hand == 0, set declarer and contract_bid as follows:
- If one bid is higher, that seat is declarer and contract_bid is that bid.
- If the bids are equal and above 0, forehand is declarer at that bid.
- If both bids are 0, forehand is declarer with contract_bid = 53.
Then defender = the other seat. Both bids, the declarer and contract_bid are announced.
  5. [ask] the seat in declarer answers: one of: Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo, Wenz. What happens: When round_in_hand == 0: contract is set to the answer and announced.
  6. [ask] the seat in defender answers: one of: Stoß, No Stoß. What happens: When round_in_hand == 0: multiplier = 2 if Stoß, else 1. The choice is announced. Then leader = forehand and follower = dealer.
  7. [ask] the seat in leader answers: one card from that seat's hand plus its non-empty stack1_up and stack2_up. What happens: When round_in_hand >= 1: led_card is set to the answer and announced. The card is removed from hand. If it was stack1_up or stack2_up, that attribute becomes empty and the matching pending_reveal flag is set to true.
  8. [update] all players. What happens: When round_in_hand >= 1, build follow_options:
- Take the follower's available cards (hand plus non-empty stack ups) whose effective suit under contract equals the effective suit of led_card.
- If there are none, take all of the follower's available cards.
Effective suit is 'Trump' if the card's trump_strength is above 0, otherwise its printed suit.
  9. [ask] the seat in follower answers: one card from follow_options. What happens: When round_in_hand >= 1: followed_card is set to the answer and announced. The card is removed from hand or from its stack up, and the matching pending_reveal flag is set to true when it came from a stack.
  10. [update] all players. What happens: When round_in_hand >= 1, decide the trick winner from trump_strength and plain_rank under contract:
- If either card has trump_strength > 0, the card with the higher trump_strength wins.
- Otherwise, if followed_card's printed suit equals led_card's suit, the higher plain_rank wins.
- Otherwise the leader wins.
The winner adds the card points of both cards to hand_points and adds 1 to tricks_won. Set leader = winner and follower = the other seat. For every stack whose pending_reveal is true, move the matching face-down table card into that stack's up attribute and clear the flag. Announce the trick result.
  11. [update] all players. What happens: When round_in_hand == 8 (hand scoring):
- Let base = 2 if contract_bid == 53, 3 if 66, 4 if 79.
- The scorer is the declarer if the declarer's hand_points >= contract_bid, otherwise the defender.
- The scorer's match_points increase by (base + (1 if the scorer's tricks_won == 8 else 0)) * multiplier.
- Each player's card_total increases by their hand_points.
Announce the result.
  12. [update] all players. What happens: rounds_played += 1. If round_in_hand == 8, then round_in_hand = 0 and hand_number += 1; otherwise round_in_hand += 1.
  13. [check] all players. What happens: End the game if rounds_played >= 36; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 16 cards: Ace, Ten, Ober and Unter of Acorns, Leaves, Hearts and Bells. Card points are Ace 11, Ten 10, Ober 3, Unter 2, totalling 104.
  R2. The match is 4 hands of 9 rounds each (1 bidding round, then 8 trick rounds), 36 rounds in all.
  R3. Seat 1 deals hands 1 and 3 and seat 2 deals hands 2 and 4. The non-dealer is forehand.
  R4. At the start of each hand all 16 cards are shuffled. Each player gets 4 private hand cards plus 2 stacks of one face-down card under one face-up card.
  R5. Hand cards are visible only to their owner, face-up stack cards to both players, and face-down cards to neither player.
  R6. Both players bid secretly and simultaneously: Pass, 53, 66 or 79.
  R7. When the bids differ, the higher bidder is declarer at their bid.
  R8. When both bid the same number (not Pass), forehand is declarer at that bid.
  R9. When both pass, forehand is declarer at 53.
  R10. Both bids are announced after the declarer is determined.
  R11. The declarer chooses Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo or Wenz, and the choice is announced.
  R12. In a Solo the trumps, from highest to lowest, are: Ober of Acorns, Leaves, Hearts, Bells; then Unter of Acorns, Leaves, Hearts, Bells; then the Ace and Ten of the chosen suit. Each other suit holds only Ace above Ten.
  R13. In Wenz the trumps, from highest to lowest, are Unter of Acorns, Leaves, Hearts, Bells. Each suit holds Ace above Ten above Ober.
  R14. The defender chooses Stoß (multiplier 2) or No Stoß (multiplier 1), and the choice is announced.
  R15. A player's available cards are their private hand cards plus the face-up card on top of each of their stacks.
  R16. In trick 1 forehand leads. In each later trick the previous trick's winner leads.
  R17. All trumps form one suit, so in a Solo an Ober or Unter never counts as its printed suit, and in Wenz an Unter never counts as its printed suit.
  R18. When the follower has an available card of the led suit, they must play one. Otherwise they may play any available card.
  R19. When any trump is played, the higher trump wins the trick. Otherwise the higher card of the led suit wins.
  R20. The trick winner adds the card points of both cards to their hand_points and 1 to tricks_won.
  R21. After a trick, the face-down card under any face-up card played in that trick turns face up and is available from the next trick on.
  R22. After trick 8, if the declarer's hand_points are at least contract_bid, the declarer scores the contract value in match points. Otherwise the defender scores it.
  R23. The contract value is (base + 1 if the scorer took all 8 tricks) times the multiplier, where the base is 2 for 53, 3 for 66 and 4 for 79. For example, a 66 bid made with Stoß and not every trick scores 6.
  R24. After each hand, each player's hand_points are added to their card_total.
  R25. After 36 rounds the game ends. More match points wins, card_total breaks ties, and if both are equal the match is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid (poll, bidding round) | asked: both seats | options: Pass, 53, 66, 79
  - Contract | asked: the declarer only | options: Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo, Wenz
  - Stoß | asked: the defender only | options: Stoß, No Stoß
  - Lead a card | asked: the leader only | options: every card in the leader's hand plus each non-empty face-up stack card of theirs
  - Follow a card | asked: the follower only | options: if the follower has an available card of the led card's effective suit (trump counts as one suit), only those cards; otherwise every available card (hand plus non-empty face-up stack cards)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.rounds_played >= 36
  - each player's standing: you.match_points * 1000 + you.card_total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 4 hands, the player with more match points wins. If match points are equal, the higher total card points over all 4 hands wins. If both are equal, the two players share the result, which is a draw.
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

- each player: `match_points` (number, visible: public, starts 0): Match points won so far.
- each player: `card_total` (number, visible: public, starts 0): Running card-point total over all completed hands, used as the tie-break.
- each player: `bid` (number, visible: public, starts 0): This hand's bid (0 = Pass, or 53, 66, 79). It is collected by a sealed poll and announced after both bids are in.
- the table: `hand_number` (number, visible: public, starts 1): The current hand, from 1 to 4.
- the table: `declarer` (number, visible: public, starts 0): Declarer's seat this hand.
- the table: `contract_bid` (number, visible: public, starts 0): The card points the declarer must reach (53, 66 or 79).
- the table: `contract` (text, visible: public, starts ''): Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo or Wenz.
- the table: `multiplier` (number, visible: public, starts 1): 2 with Stoß, 1 without.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 16, points_ace = 11, points_ten = 10, points_ober = 3, points_unter = 2, deck_points = 104, hands_in_match = 4, tricks_per_hand = 8, rounds_per_hand = 9, total_rounds = 36, private_cards_per_player = 4, stacks_per_player = 2, face_up_cards_on_table = 4, bid_pass = 0, bid_low = 53, bid_mid = 66, bid_high = 79, default_bid_when_both_pass = 53, base_for_53 = 2, base_for_66 = 3, base_for_79 = 4, all_tricks_bonus = 1, multiplier_stoss = 2, multiplier_no_stoss = 1, trump_strength_ober_acorns = 20, trump_strength_ober_leaves = 19, trump_strength_ober_hearts = 18, trump_strength_ober_bells = 17, trump_strength_unter_acorns = 16, trump_strength_unter_leaves = 15, trump_strength_unter_hearts = 14, trump_strength_unter_bells = 13, trump_strength_solo_suit_ace = 12, trump_strength_solo_suit_ten = 11, plain_rank_ace = 3, plain_rank_ten = 2, plain_rank_ober = 1, plain_rank_unter = 0, rank_weight_match_points = 1000
- the game ends with ONE ending whose `rank_by` is `you.match_points * 1000 + you.card_total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "officers_schafkopf_bidding_match",
    "name": "Officers' Schafkopf: Bidding Match",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Schafkopf over 4 hands: sealed bids, Solo or Wenz, an optional Stoß, open and hidden stacks, 8 tricks a hand."
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
      {"key": "match_points", "visible": "public", "type": "number", "initial": 0},
      {"key": "card_total", "visible": "public", "type": "number", "initial": 0},
      {"key": "hand_points", "visible": "public", "type": "number", "initial": 0},
      {"key": "tricks_won", "visible": "public", "type": "number", "initial": 0},
      {"key": "hand", "visible": "ally", "type": "list", "initial": []},
      {"key": "stack1_up", "visible": "public", "type": "text", "initial": ""},
      {"key": "stack2_up", "visible": "public", "type": "text", "initial": ""},
      {"key": "stack1_pending_reveal", "visible": "public", "type": "bool", "initial": false},
      {"key": "stack2_pending_reveal", "visible": "public", "type": "bool", "initial": false},
      {"key": "bid", "visible": "public", "type": "number", "initial": 0},
      {"key": "bid_choice", "visible": "ally", "type": "text", "initial": ""}
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["Ace of Acorns", "Ten of Acorns", "Ober of Acorns", "Unter of Acorns", "Ace of Leaves", "Ten of Leaves", "Ober of Leaves", "Unter of Leaves", "Ace of Hearts", "Ten of Hearts", "Ober of Hearts", "Unter of Hearts", "Ace of Bells", "Ten of Bells", "Ober of Bells", "Unter of Bells"]
      },
      {"key": "trumps", "visible": "none", "type": "list", "initial": []},
      {"key": "pick", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat1_stack1_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat1_stack2_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat2_stack1_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat2_stack2_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "hand_number", "visible": "public", "type": "number", "initial": 1},
      {"key": "round_in_hand", "visible": "public", "type": "number", "initial": 0},
      {"key": "rounds_played", "visible": "public", "type": "number", "initial": 0},
      {"key": "dealer", "visible": "public", "type": "number", "initial": 1},
      {"key": "forehand", "visible": "public", "type": "number", "initial": 2},
      {"key": "declarer", "visible": "public", "type": "number", "initial": 0},
      {"key": "defender", "visible": "public", "type": "number", "initial": 0},
      {"key": "contract_bid", "visible": "public", "type": "number", "initial": 0},
      {"key": "contract", "visible": "public", "type": "text", "initial": ""},
      {"key": "multiplier", "visible": "public", "type": "number", "initial": 1},
      {"key": "leader", "visible": "public", "type": "number", "initial": 0},
      {"key": "follower", "visible": "public", "type": "number", "initial": 0},
      {"key": "led_card", "visible": "public", "type": "text", "initial": ""},
      {"key": "followed_card", "visible": "public", "type": "text", "initial": ""},
      {"key": "follow_options", "visible": "public", "type": "list", "initial": []},
      {"key": "lead_options", "visible": "none", "type": "list", "initial": []},
      {"key": "led_suit", "visible": "none", "type": "text", "initial": ""},
      {"key": "followed_suit", "visible": "none", "type": "text", "initial": ""},
      {"key": "led_strength", "visible": "none", "type": "number", "initial": 0},
      {"key": "followed_strength", "visible": "none", "type": "number", "initial": 0},
      {"key": "led_rank", "visible": "none", "type": "number", "initial": 0},
      {"key": "followed_rank", "visible": "none", "type": "number", "initial": 0},
      {"key": "trick_winner", "visible": "none", "type": "number", "initial": 0},
      {"key": "trick_points", "visible": "none", "type": "number", "initial": 0},
      {"key": "scorer", "visible": "none", "type": "number", "initial": 0},
      {"key": "score_gain", "visible": "none", "type": "number", "initial": 0},
      {"key": "seat1_bid", "visible": "none", "type": "number", "initial": 0},
      {"key": "seat2_bid", "visible": "none", "type": "number", "initial": 0},
      {"key": "deck_size", "visible": "public", "type": "number", "initial": 16},
      {"key": "points_ace", "visible": "public", "type": "number", "initial": 11},
      {"key": "points_ten", "visible": "public", "type": "number", "initial": 10},
      {"key": "points_ober", "visible": "public", "type": "number", "initial": 3},
      {"key": "points_unter", "visible": "public", "type": "number", "initial": 2},
      {"key": "deck_points", "visible": "public", "type": "number", "initial": 104},
      {"key": "hands_in_match", "visible": "public", "type": "number", "initial": 4},
      {"key": "tricks_per_hand", "visible": "public", "type": "number", "initial": 8},
      {"key": "rounds_per_hand", "visible": "public", "type": "number", "initial": 9},
      {"key": "total_rounds", "visible": "public", "type": "number", "initial": 36},
      {"key": "private_cards_per_player", "visible": "public", "type": "number", "initial": 4},
      {"key": "stacks_per_player", "visible": "public", "type": "number", "initial": 2},
      {"key": "face_up_cards_on_table", "visible": "public", "type": "number", "initial": 4},
      {"key": "bid_pass", "visible": "public", "type": "number", "initial": 0},
      {"key": "bid_low", "visible": "public", "type": "number", "initial": 53},
      {"key": "bid_mid", "visible": "public", "type": "number", "initial": 66},
      {"key": "bid_high", "visible": "public", "type": "number", "initial": 79},
      {"key": "default_bid_when_both_pass", "visible": "public", "type": "number", "initial": 53},
      {"key": "base_for_53", "visible": "public", "type": "number", "initial": 2},
      {"key": "base_for_66", "visible": "public", "type": "number", "initial": 3},
      {"key": "base_for_79", "visible": "public", "type": "number", "initial": 4},
      {"key": "all_tricks_bonus", "visible": "public", "type": "number", "initial": 1},
      {"key": "multiplier_stoss", "visible": "public", "type": "number", "initial": 2},
      {"key": "multiplier_no_stoss", "visible": "public", "type": "number", "initial": 1},
      {"key": "trump_strength_ober_acorns", "visible": "public", "type": "number", "initial": 20},
      {"key": "trump_strength_ober_leaves", "visible": "public", "type": "number", "initial": 19},
      {"key": "trump_strength_ober_hearts", "visible": "public", "type": "number", "initial": 18},
      {"key": "trump_strength_ober_bells", "visible": "public", "type": "number", "initial": 17},
      {"key": "trump_strength_unter_acorns", "visible": "public", "type": "number", "initial": 16},
      {"key": "trump_strength_unter_leaves", "visible": "public", "type": "number", "initial": 15},
      {"key": "trump_strength_unter_hearts", "visible": "public", "type": "number", "initial": 14},
      {"key": "trump_strength_unter_bells", "visible": "public", "type": "number", "initial": 13},
      {"key": "trump_strength_solo_suit_ace", "visible": "public", "type": "number", "initial": 12},
      {"key": "trump_strength_solo_suit_ten", "visible": "public", "type": "number", "initial": 11},
      {"key": "plain_rank_ace", "visible": "public", "type": "number", "initial": 3},
      {"key": "plain_rank_ten", "visible": "public", "type": "number", "initial": 2},
      {"key": "plain_rank_ober", "visible": "public", "type": "number", "initial": 1},
      {"key": "plain_rank_unter", "visible": "public", "type": "number", "initial": 0},
      {"key": "rank_weight_match_points", "visible": "public", "type": "number", "initial": 1000}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "start the match",
      "do": [
        {"set": {"key": "hand_number", "value": 1}},
        {"set": {"key": "round_in_hand", "value": 0}},
        {"set": {"key": "rounds_played", "value": 0}},
        {"set": {"players": "all", "key": "match_points", "value": 0}},
        {"set": {"players": "all", "key": "card_total", "value": 0}},
        {"set": {"key": "dealer", "value": 1}},
        {"set": {"key": "forehand", "value": 2}}
      ],
      "text": "The match begins. Seat {dealer} deals hand 1, so seat {forehand} is forehand."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "when": {"calc": "round_in_hand == 0"},
      "do": [
        {"set": {"key": "dealer", "value": {"calc": "1 if hand_number % 2 == 1 else 2"}}},
        {"set": {"key": "forehand", "value": {"calc": "2 if dealer == 1 else 1"}}},
        {"set": {"key": "deck", "value": {"calc": "['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns', 'Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves', 'Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts', 'Ace of Bells', 'Ten of Bells', 'Ober of Bells', 'Unter of Bells']"}}},
        {"set": {"players": "all", "key": "hand", "value": []}},
        {"set": {"players": "all", "key": "hand_points", "value": 0}},
        {"set": {"players": "all", "key": "tricks_won", "value": 0}},
        {"set": {"players": "all", "key": "bid", "value": 0}},
        {"set": {"players": "all", "key": "bid_choice", "value": ""}},
        {"set": {"players": "all", "key": "stack1_pending_reveal", "value": false}},
        {"set": {"players": "all", "key": "stack2_pending_reveal", "value": false}},
        {"set": {"key": "contract", "value": ""}},
        {"set": {"key": "trumps", "value": []}},
        {"set": {"key": "multiplier", "value": {"calc": "multiplier_no_stoss"}}},
        {"set": {"key": "declarer", "value": 0}},
        {"set": {"key": "defender", "value": 0}},
        {"set": {"key": "led_card", "value": ""}},
        {"set": {"key": "followed_card", "value": ""}},
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
        {"set": {"player": 1, "key": "stack1_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat1_stack1_down", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"player": 1, "key": "stack2_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat1_stack2_down", "value": {"calc": "pick"}}},
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
        {"set": {"player": 2, "key": "stack1_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat2_stack1_down", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"player": 2, "key": "stack2_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat2_stack2_down", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ],
      "text": "Hand {hand_number} of {hands_in_match} is dealt. Seat {dealer} deals; seat {forehand} is forehand."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your view",
      "mode": "self",
      "to": "all",
      "fields": ["hand", "stack1_up", "stack2_up", "match_points", "card_total", "hand_points", "tricks_won"],
      "text": "Your hand, your face-up stack cards and your standing:"
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "the bids",
      "when": {"calc": "round_in_hand == 0"},
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": ["Pass", "53", "66", "79"]
      },
      "store": "bid_choice",
      "text": "Bid in secret: Pass, 53, 66 or 79. Your bid is the number of card points you promise to take as declarer. Your opponent sees your bid only after both bids are in."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "the declarer",
      "when": {"calc": "round_in_hand == 0"},
      "do": [
        {"set": {"players": "all", "key": "bid", "value": {"calc": "bid_low if you.bid_choice == '53' else bid_mid if you.bid_choice == '66' else bid_high if you.bid_choice == '79' else bid_pass"}}},
        {"set": {"key": "seat1_bid", "value": {"calc": "players[0].bid"}}},
        {"set": {"key": "seat2_bid", "value": {"calc": "players[1].bid"}}},
        {"set": {"key": "declarer", "value": {"calc": "forehand if seat1_bid == seat2_bid else (1 if seat1_bid > seat2_bid else 2)"}}},
        {"set": {"key": "contract_bid", "value": {"calc": "default_bid_when_both_pass if max(seat1_bid, seat2_bid) == bid_pass else max(seat1_bid, seat2_bid)"}}},
        {"set": {"key": "defender", "value": {"calc": "2 if declarer == 1 else 1"}}}
      ],
      "text": "Bids: seat 1 bid {seat1_bid}, seat 2 bid {seat2_bid} (0 means Pass). Seat {declarer} is declarer at {contract_bid}; seat {defender} defends."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "the contract",
      "when": {"calc": "round_in_hand == 0"},
      "to": {"where": "you.seat == declarer"},
      "answer": {
        "type": "choice",
        "options": ["Acorns Solo", "Leaves Solo", "Hearts Solo", "Bells Solo", "Wenz"]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} declares {value}."},
      "each": {
        "do": [
          {"set": {"key": "contract", "value": "$answer"}},
          {"set": {"key": "trumps", "value": {"calc": "['Unter of Acorns', 'Unter of Leaves', 'Unter of Hearts', 'Unter of Bells'] if contract == 'Wenz' else ['Ober of Acorns', 'Ober of Leaves', 'Ober of Hearts', 'Ober of Bells', 'Unter of Acorns', 'Unter of Leaves', 'Unter of Hearts', 'Unter of Bells'] + (['Ace of Acorns', 'Ten of Acorns'] if contract == 'Acorns Solo' else ['Ace of Leaves', 'Ten of Leaves'] if contract == 'Leaves Solo' else ['Ace of Hearts', 'Ten of Hearts'] if contract == 'Hearts Solo' else ['Ace of Bells', 'Ten of Bells'])"}}}
        ]
      },
      "text": "You are declarer at {contract_bid}. Choose the contract: Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo or Wenz."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "the Stoß",
      "when": {"calc": "round_in_hand == 0"},
      "to": {"where": "you.seat == defender"},
      "answer": {
        "type": "choice",
        "options": ["Stoß", "No Stoß"]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} chooses {value}."},
      "each": {
        "do": [
          {"set": {"key": "multiplier", "value": {"calc": "multiplier_stoss if $answer == 'Stoß' else multiplier_no_stoss"}}},
          {"set": {"key": "leader", "value": {"calc": "forehand"}}},
          {"set": {"key": "follower", "value": {"calc": "dealer"}}},
          {"set": {"key": "lead_options", "value": {"calc": "players[leader - 1].hand + ([players[leader - 1].stack1_up] if players[leader - 1].stack1_up != '' else []) + ([players[leader - 1].stack2_up] if players[leader - 1].stack2_up != '' else [])"}}}
        ]
      },
      "text": "Seat {declarer} plays {contract} at {contract_bid}. Choose Stoß (multiplier {multiplier_stoss}) or No Stoß (multiplier {multiplier_no_stoss})."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the lead",
      "when": {"calc": "round_in_hand >= 1"},
      "to": {"where": "you.seat == leader"},
      "answer": {
        "type": "choice",
        "options": {"game": "lead_options"}
      },
      "broadcast": {"to": "all", "text": "Seat {seat} leads {value}."},
      "each": {
        "do": [
          {"set": {"key": "led_card", "value": "$answer"}},
          {"set": {"key": "led_suit", "value": {"calc": "'Trump' if led_card in trumps else 'Acorns' if led_card in ['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns'] else 'Leaves' if led_card in ['Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves'] else 'Hearts' if led_card in ['Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts'] else 'Bells'"}}},
          {"set": {"player": "$seat", "key": "stack1_pending_reveal", "value": true, "if": {"calc": "led_card == players[leader - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack1_up", "value": "", "if": {"calc": "led_card == players[leader - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack2_pending_reveal", "value": true, "if": {"calc": "led_card == players[leader - 1].stack2_up"}}},
          {"set": {"player": "$seat", "key": "stack2_up", "value": "", "if": {"calc": "led_card == players[leader - 1].stack2_up"}}},
          {"remove": {"player": "$seat", "key": "hand", "value": {"calc": "led_card"}, "if": {"calc": "led_card in players[leader - 1].hand"}}}
        ]
      },
      "text": "Trick {round_in_hand} of {tricks_per_hand} under {contract}. Lead one available card: a card from your hand or a face-up card on top of one of your stacks."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the follow options",
      "when": {"calc": "round_in_hand >= 1"},
      "do": [
        {"set": {"key": "follow_options", "value": {"calc": "[c for c in players[follower - 1].hand + ([players[follower - 1].stack1_up] if players[follower - 1].stack1_up != '' else []) + ([players[follower - 1].stack2_up] if players[follower - 1].stack2_up != '' else []) if ('Trump' if c in trumps else 'Acorns' if c in ['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns'] else 'Leaves' if c in ['Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves'] else 'Hearts' if c in ['Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts'] else 'Bells') == led_suit]"}}},
        {"set": {"key": "follow_options", "value": {"calc": "follow_options if len(follow_options) > 0 else players[follower - 1].hand + ([players[follower - 1].stack1_up] if players[follower - 1].stack1_up != '' else []) + ([players[follower - 1].stack2_up] if players[follower - 1].stack2_up != '' else [])"}}}
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the follow",
      "when": {"calc": "round_in_hand >= 1"},
      "to": {"where": "you.seat == follower"},
      "answer": {
        "type": "choice",
        "options": {"game": "follow_options"}
      },
      "broadcast": {"to": "all", "text": "Seat {seat} plays {value}."},
      "each": {
        "do": [
          {"set": {"key": "followed_card", "value": "$answer"}},
          {"set": {"key": "followed_suit", "value": {"calc": "'Trump' if followed_card in trumps else 'Acorns' if followed_card in ['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns'] else 'Leaves' if followed_card in ['Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves'] else 'Hearts' if followed_card in ['Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts'] else 'Bells'"}}},
          {"set": {"player": "$seat", "key": "stack1_pending_reveal", "value": true, "if": {"calc": "followed_card == players[follower - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack1_up", "value": "", "if": {"calc": "followed_card == players[follower - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack2_pending_reveal", "value": true, "if": {"calc": "followed_card == players[follower - 1].stack2_up"}}},
          {"set": {"player": "$seat", "key": "stack2_up", "value": "", "if": {"calc": "followed_card == players[follower - 1].stack2_up"}}},
          {"remove": {"player": "$seat", "key": "hand", "value": {"calc": "followed_card"}, "if": {"calc": "followed_card in players[follower - 1].hand"}}}
        ]
      },
      "text": "Trick {round_in_hand} under {contract}: seat {leader} led {led_card}. Play one of the cards offered: you must follow the led suit (all trumps are one suit) if you can, otherwise any available card."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick",
      "when": {"calc": "round_in_hand >= 1"},
      "do": [
        {"set": {"key": "led_strength", "value": {"calc": "0 if led_card not in trumps else (trump_strength_ober_acorns if led_card == 'Ober of Acorns' else trump_strength_ober_leaves if led_card == 'Ober of Leaves' else trump_strength_ober_hearts if led_card == 'Ober of Hearts' else trump_strength_ober_bells if led_card == 'Ober of Bells' else trump_strength_unter_acorns if led_card == 'Unter of Acorns' else trump_strength_unter_leaves if led_card == 'Unter of Leaves' else trump_strength_unter_hearts if led_card == 'Unter of Hearts' else trump_strength_unter_bells if led_card == 'Unter of Bells' else trump_strength_solo_suit_ace if led_card in ['Ace of Acorns', 'Ace of Leaves', 'Ace of Hearts', 'Ace of Bells'] else trump_strength_solo_suit_ten)"}}},
        {"set": {"key": "followed_strength", "value": {"calc": "0 if followed_card not in trumps else (trump_strength_ober_acorns if followed_card == 'Ober of Acorns' else trump_strength_ober_leaves if followed_card == 'Ober of Leaves' else trump_strength
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (contract, followed_card, led_card) in `your_view`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "officers_schafkopf_bidding_match",
    "name": "Officers' Schafkopf: Bidding Match",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Schafkopf over 4 hands: sealed bids, Solo or Wenz, an optional Stoß, open and hidden stacks, 8 tricks a hand."
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
      {"key": "match_points", "visible": "public", "type": "number", "initial": 0},
      {"key": "card_total", "visible": "public", "type": "number", "initial": 0},
      {"key": "hand_points", "visible": "public", "type": "number", "initial": 0},
      {"key": "tricks_won", "visible": "public", "type": "number", "initial": 0},
      {"key": "hand", "visible": "ally", "type": "list", "initial": []},
      {"key": "stack1_up", "visible": "public", "type": "text", "initial": ""},
      {"key": "stack2_up", "visible": "public", "type": "text", "initial": ""},
      {"key": "stack1_pending_reveal", "visible": "public", "type": "bool", "initial": false},
      {"key": "stack2_pending_reveal", "visible": "public", "type": "bool", "initial": false},
      {"key": "bid", "visible": "public", "type": "number", "initial": 0},
      {"key": "bid_choice", "visible": "ally", "type": "text", "initial": ""}
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["Ace of Acorns", "Ten of Acorns", "Ober of Acorns", "Unter of Acorns", "Ace of Leaves", "Ten of Leaves", "Ober of Leaves", "Unter of Leaves", "Ace of Hearts", "Ten of Hearts", "Ober of Hearts", "Unter of Hearts", "Ace of Bells", "Ten of Bells", "Ober of Bells", "Unter of Bells"]
      },
      {"key": "trumps", "visible": "none", "type": "list", "initial": []},
      {"key": "pick", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat1_stack1_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat1_stack2_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat2_stack1_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "seat2_stack2_down", "visible": "none", "type": "text", "initial": ""},
      {"key": "hand_number", "visible": "public", "type": "number", "initial": 1},
      {"key": "round_in_hand", "visible": "public", "type": "number", "initial": 0},
      {"key": "rounds_played", "visible": "public", "type": "number", "initial": 0},
      {"key": "dealer", "visible": "public", "type": "number", "initial": 1},
      {"key": "forehand", "visible": "public", "type": "number", "initial": 2},
      {"key": "declarer", "visible": "public", "type": "number", "initial": 0},
      {"key": "defender", "visible": "public", "type": "number", "initial": 0},
      {"key": "contract_bid", "visible": "public", "type": "number", "initial": 0},
      {"key": "contract", "visible": "public", "type": "text", "initial": ""},
      {"key": "multiplier", "visible": "public", "type": "number", "initial": 1},
      {"key": "leader", "visible": "public", "type": "number", "initial": 0},
      {"key": "follower", "visible": "public", "type": "number", "initial": 0},
      {"key": "led_card", "visible": "public", "type": "text", "initial": ""},
      {"key": "followed_card", "visible": "public", "type": "text", "initial": ""},
      {"key": "follow_options", "visible": "none", "type": "list", "initial": []},
      {"key": "lead_options", "visible": "none", "type": "list", "initial": []},
      {"key": "led_suit", "visible": "none", "type": "text", "initial": ""},
      {"key": "followed_suit", "visible": "none", "type": "text", "initial": ""},
      {"key": "led_strength", "visible": "none", "type": "number", "initial": 0},
      {"key": "followed_strength", "visible": "none", "type": "number", "initial": 0},
      {"key": "led_rank", "visible": "none", "type": "number", "initial": 0},
      {"key": "followed_rank", "visible": "none", "type": "number", "initial": 0},
      {"key": "trick_winner", "visible": "none", "type": "number", "initial": 0},
      {"key": "trick_points", "visible": "none", "type": "number", "initial": 0},
      {"key": "scorer", "visible": "none", "type": "number", "initial": 0},
      {"key": "score_gain", "visible": "none", "type": "number", "initial": 0},
      {"key": "seat1_bid", "visible": "none", "type": "number", "initial": 0},
      {"key": "seat2_bid", "visible": "none", "type": "number", "initial": 0},
      {"key": "deck_size", "visible": "public", "type": "number", "initial": 16},
      {"key": "points_ace", "visible": "public", "type": "number", "initial": 11},
      {"key": "points_ten", "visible": "public", "type": "number", "initial": 10},
      {"key": "points_ober", "visible": "public", "type": "number", "initial": 3},
      {"key": "points_unter", "visible": "public", "type": "number", "initial": 2},
      {"key": "deck_points", "visible": "public", "type": "number", "initial": 104},
      {"key": "hands_in_match", "visible": "public", "type": "number", "initial": 4},
      {"key": "tricks_per_hand", "visible": "public", "type": "number", "initial": 8},
      {"key": "rounds_per_hand", "visible": "public", "type": "number", "initial": 9},
      {"key": "total_rounds", "visible": "public", "type": "number", "initial": 36},
      {"key": "private_cards_per_player", "visible": "public", "type": "number", "initial": 4},
      {"key": "stacks_per_player", "visible": "public", "type": "number", "initial": 2},
      {"key": "face_up_cards_on_table", "visible": "public", "type": "number", "initial": 4},
      {"key": "bid_pass", "visible": "public", "type": "number", "initial": 0},
      {"key": "bid_low", "visible": "public", "type": "number", "initial": 53},
      {"key": "bid_mid", "visible": "public", "type": "number", "initial": 66},
      {"key": "bid_high", "visible": "public", "type": "number", "initial": 79},
      {"key": "default_bid_when_both_pass", "visible": "public", "type": "number", "initial": 53},
      {"key": "base_for_53", "visible": "public", "type": "number", "initial": 2},
      {"key": "base_for_66", "visible": "public", "type": "number", "initial": 3},
      {"key": "base_for_79", "visible": "public", "type": "number", "initial": 4},
      {"key": "all_tricks_bonus", "visible": "public", "type": "number", "initial": 1},
      {"key": "multiplier_stoss", "visible": "public", "type": "number", "initial": 2},
      {"key": "multiplier_no_stoss", "visible": "public", "type": "number", "initial": 1},
      {"key": "trump_strength_ober_acorns", "visible": "public", "type": "number", "initial": 20},
      {"key": "trump_strength_ober_leaves", "visible": "public", "type": "number", "initial": 19},
      {"key": "trump_strength_ober_hearts", "visible": "public", "type": "number", "initial": 18},
      {"key": "trump_strength_ober_bells", "visible": "public", "type": "number", "initial": 17},
      {"key": "trump_strength_unter_acorns", "visible": "public", "type": "number", "initial": 16},
      {"key": "trump_strength_unter_leaves", "visible": "public", "type": "number", "initial": 15},
      {"key": "trump_strength_unter_hearts", "visible": "public", "type": "number", "initial": 14},
      {"key": "trump_strength_unter_bells", "visible": "public", "type": "number", "initial": 13},
      {"key": "trump_strength_solo_suit_ace", "visible": "public", "type": "number", "initial": 12},
      {"key": "trump_strength_solo_suit_ten", "visible": "public", "type": "number", "initial": 11},
      {"key": "plain_rank_ace", "visible": "public", "type": "number", "initial": 3},
      {"key": "plain_rank_ten", "visible": "public", "type": "number", "initial": 2},
      {"key": "plain_rank_ober", "visible": "public", "type": "number", "initial": 1},
      {"key": "plain_rank_unter", "visible": "public", "type": "number", "initial": 0},
      {"key": "rank_weight_match_points", "visible": "public", "type": "number", "initial": 1000}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "start the match",
      "do": [
        {"set": {"key": "hand_number", "value": 1}},
        {"set": {"key": "round_in_hand", "value": 0}},
        {"set": {"key": "rounds_played", "value": 0}},
        {"set": {"players": "all", "key": "match_points", "value": 0}},
        {"set": {"players": "all", "key": "card_total", "value": 0}},
        {"set": {"key": "dealer", "value": 1}},
        {"set": {"key": "forehand", "value": 2}}
      ],
      "text": "The match begins. Seat {dealer} deals hand 1, so seat {forehand} is forehand."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "when": {"calc": "round_in_hand == 0"},
      "do": [
        {"set": {"key": "dealer", "value": {"calc": "1 if hand_number % 2 == 1 else 2"}}},
        {"set": {"key": "forehand", "value": {"calc": "2 if dealer == 1 else 1"}}},
        {"set": {"key": "deck", "value": {"calc": "['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns', 'Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves', 'Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts', 'Ace of Bells', 'Ten of Bells', 'Ober of Bells', 'Unter of Bells']"}}},
        {"set": {"players": "all", "key": "hand", "value": []}},
        {"set": {"players": "all", "key": "hand_points", "value": 0}},
        {"set": {"players": "all", "key": "tricks_won", "value": 0}},
        {"set": {"players": "all", "key": "bid", "value": 0}},
        {"set": {"players": "all", "key": "bid_choice", "value": ""}},
        {"set": {"players": "all", "key": "stack1_pending_reveal", "value": false}},
        {"set": {"players": "all", "key": "stack2_pending_reveal", "value": false}},
        {"set": {"key": "contract", "value": "not chosen yet"}},
        {"set": {"key": "trumps", "value": []}},
        {"set": {"key": "multiplier", "value": {"calc": "multiplier_no_stoss"}}},
        {"set": {"key": "declarer", "value": 0}},
        {"set": {"key": "defender", "value": 0}},
        {"set": {"key": "led_card", "value": "none yet"}},
        {"set": {"key": "followed_card", "value": "none yet"}},
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
        {"set": {"player": 1, "key": "stack1_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat1_stack1_down", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"player": 1, "key": "stack2_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat1_stack2_down", "value": {"calc": "pick"}}},
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
        {"set": {"player": 2, "key": "stack1_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat2_stack1_down", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"player": 2, "key": "stack2_up", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"set": {"key": "seat2_stack2_down", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ],
      "text": "Hand {hand_number} of {hands_in_match} is dealt. Seat {dealer} deals; seat {forehand} is forehand."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your view",
      "mode": "self",
      "to": "all",
      "fields": ["hand", "stack1_up", "stack2_up", "match_points", "card_total", "hand_points", "tricks_won"],
      "text": "Your hand, your face-up stack cards and your standing:"
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "the bids",
      "when": {"calc": "round_in_hand == 0"},
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": ["Pass", "53", "66", "79"]
      },
      "store": "bid_choice",
      "text": "Bid in secret: Pass, 53, 66 or 79. Your bid is the number of card points you promise to take as declarer. Your opponent sees your bid only after both bids are in."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "the declarer",
      "when": {"calc": "round_in_hand == 0"},
      "do": [
        {"set": {"players": "all", "key": "bid", "value": {"calc": "bid_low if you.bid_choice == '53' else bid_mid if you.bid_choice == '66' else bid_high if you.bid_choice == '79' else bid_pass"}}},
        {"set": {"key": "seat1_bid", "value": {"calc": "players[0].bid"}}},
        {"set": {"key": "seat2_bid", "value": {"calc": "players[1].bid"}}},
        {"set": {"key": "declarer", "value": {"calc": "forehand if seat1_bid == seat2_bid else (1 if seat1_bid > seat2_bid else 2)"}}},
        {"set": {"key": "contract_bid", "value": {"calc": "default_bid_when_both_pass if max(seat1_bid, seat2_bid) == bid_pass else max(seat1_bid, seat2_bid)"}}},
        {"set": {"key": "defender", "value": {"calc": "2 if declarer == 1 else 1"}}}
      ],
      "text": "Bids: seat 1 bid {seat1_bid}, seat 2 bid {seat2_bid} (0 means Pass). Seat {declarer} is declarer at {contract_bid}; seat {defender} defends."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "the contract",
      "when": {"calc": "round_in_hand == 0"},
      "to": {"where": "you.seat == declarer"},
      "answer": {
        "type": "choice",
        "options": ["Acorns Solo", "Leaves Solo", "Hearts Solo", "Bells Solo", "Wenz"]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} declares {value}."},
      "each": {
        "do": [
          {"set": {"key": "contract", "value": "$answer"}},
          {"set": {"key": "trumps", "value": {"calc": "['Unter of Acorns', 'Unter of Leaves', 'Unter of Hearts', 'Unter of Bells'] if contract == 'Wenz' else ['Ober of Acorns', 'Ober of Leaves', 'Ober of Hearts', 'Ober of Bells', 'Unter of Acorns', 'Unter of Leaves', 'Unter of Hearts', 'Unter of Bells'] + (['Ace of Acorns', 'Ten of Acorns'] if contract == 'Acorns Solo' else ['Ace of Leaves', 'Ten of Leaves'] if contract == 'Leaves Solo' else ['Ace of Hearts', 'Ten of Hearts'] if contract == 'Hearts Solo' else ['Ace of Bells', 'Ten of Bells'])"}}}
        ]
      },
      "text": "You are declarer at {contract_bid}. Choose the contract: Acorns Solo, Leaves Solo, Hearts Solo, Bells Solo or Wenz."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "the Stoß",
      "when": {"calc": "round_in_hand == 0"},
      "to": {"where": "you.seat == defender"},
      "answer": {
        "type": "choice",
        "options": ["Stoß", "No Stoß"]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} chooses {value}."},
      "each": {
        "do": [
          {"set": {"key": "multiplier", "value": {"calc": "multiplier_stoss if $answer == 'Stoß' else multiplier_no_stoss"}}},
          {"set": {"key": "leader", "value": {"calc": "forehand"}}},
          {"set": {"key": "follower", "value": {"calc": "dealer"}}},
          {"set": {"key": "lead_options", "value": {"calc": "players[leader - 1].hand + ([players[leader - 1].stack1_up] if players[leader - 1].stack1_up != '' else []) + ([players[leader - 1].stack2_up] if players[leader - 1].stack2_up != '' else [])"}}}
        ]
      },
      "text": "Seat {declarer} plays {contract} at {contract_bid}. Choose Stoß (multiplier {multiplier_stoss}) or No Stoß (multiplier {multiplier_no_stoss})."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the lead",
      "when": {"calc": "round_in_hand >= 1"},
      "to": {"where": "you.seat == leader"},
      "answer": {
        "type": "choice",
        "options": {"game": "lead_options"}
      },
      "broadcast": {"to": "all", "text": "Seat {seat} leads {value}."},
      "each": {
        "do": [
          {"set": {"key": "led_card", "value": "$answer"}},
          {"set": {"key": "led_suit", "value": {"calc": "'Trump' if led_card in trumps else 'Acorns' if led_card in ['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns'] else 'Leaves' if led_card in ['Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves'] else 'Hearts' if led_card in ['Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts'] else 'Bells'"}}},
          {"set": {"player": "$seat", "key": "stack1_pending_reveal", "value": true, "if": {"calc": "led_card == players[leader - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack1_up", "value": "", "if": {"calc": "led_card == players[leader - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack2_pending_reveal", "value": true, "if": {"calc": "led_card == players[leader - 1].stack2_up"}}},
          {"set": {"player": "$seat", "key": "stack2_up", "value": "", "if": {"calc": "led_card == players[leader - 1].stack2_up"}}},
          {"remove": {"player": "$seat", "key": "hand", "value": {"calc": "led_card"}, "if": {"calc": "led_card in players[leader - 1].hand"}}}
        ]
      },
      "text": "Trick {round_in_hand} of {tricks_per_hand} under {contract}. Lead one available card: a card from your hand or a face-up card on top of one of your stacks."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the follow options",
      "when": {"calc": "round_in_hand >= 1"},
      "do": [
        {"set": {"key": "follow_options", "value": {"calc": "[c for c in players[follower - 1].hand + ([players[follower - 1].stack1_up] if players[follower - 1].stack1_up != '' else []) + ([players[follower - 1].stack2_up] if players[follower - 1].stack2_up != '' else []) if ('Trump' if c in trumps else 'Acorns' if c in ['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns'] else 'Leaves' if c in ['Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves'] else 'Hearts' if c in ['Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts'] else 'Bells') == led_suit]"}}},
        {"set": {"key": "follow_options", "value": {"calc": "follow_options if len(follow_options) > 0 else players[follower - 1].hand + ([players[follower - 1].stack1_up] if players[follower - 1].stack1_up != '' else []) + ([players[follower - 1].stack2_up] if players[follower - 1].stack2_up != '' else [])"}}}
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the follow",
      "when": {"calc": "round_in_hand >= 1"},
      "to": {"where": "you.seat == follower"},
      "answer": {
        "type": "choice",
        "options": {"game": "follow_options"}
      },
      "broadcast": {"to": "all", "text": "Seat {seat} plays {value}."},
      "each": {
        "do": [
          {"set": {"key": "followed_card", "value": "$answer"}},
          {"set": {"key": "followed_suit", "value": {"calc": "'Trump' if followed_card in trumps else 'Acorns' if followed_card in ['Ace of Acorns', 'Ten of Acorns', 'Ober of Acorns', 'Unter of Acorns'] else 'Leaves' if followed_card in ['Ace of Leaves', 'Ten of Leaves', 'Ober of Leaves', 'Unter of Leaves'] else 'Hearts' if followed_card in ['Ace of Hearts', 'Ten of Hearts', 'Ober of Hearts', 'Unter of Hearts'] else 'Bells'"}}},
          {"set": {"player": "$seat", "key": "stack1_pending_reveal", "value": true, "if": {"calc": "followed_card == players[follower - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack1_up", "value": "", "if": {"calc": "followed_card == players[follower - 1].stack1_up"}}},
          {"set": {"player": "$seat", "key": "stack2_pending_reveal", "value": true, "if": {"calc": "followed_card == players[follower - 1].stack2_up"}}},
          {"set": {"player": "$seat", "key": "stack2_up", "value": "", "if": {"calc": "followed_card == players[follower - 1].stack2_up"}}},
          {"remove": {"player": "$seat", "key": "hand", "value": {"calc": "followed_card"}, "if": {"calc": "followed_card in players[follower - 1].hand"}}}
        ]
      },
      "text": "Trick {round_in_hand} under {contract}: seat {leader} led {led_card}. Play one of the cards offered: you must follow the led suit (all trumps are one suit) if you can, otherwise any available card."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick",
      "when": {"calc": "round_in_hand >= 1"},
      "do": [
        {"set": {"key": "led_strength", "value": {"calc": "0 if led_card not in trumps else (trump_strength_ober_acorns if led_card == 'Ober of Acorns' else trump_strength_ober_leaves if led_card == 'Ober of Leaves' else trump_strength_ober_hearts if led_card == 'Ober of Hearts' else trump_strength_ober_bells if led_card == 'Ober of Bells' else trump_strength_unter_acorns if led_card == 'Unter of Acorns' else trump_strength_unter_leaves if led_card == 'Unter of Leaves' else trump_strength_unter_hearts if led_card == 'Unter of Hearts' else trump_strength_unter_bells if led_card == 'Unter of Bells' else trump_strength_solo_suit_ace if led_card in ['Ace of Acorns', 'Ace of Leaves', 'Ace of Hearts', 'Ace of Bells'] else trump_strength_solo_suit_ten)"}}},
        {"set": {"key": "followed_strength", "value": {"calc": "0 if followed_card not in trumps else (trump_strength_ober_acorns if followed_card == 'Ober of Acorns' else trump_strength_ober_leaves if followed_card == 'Ober of Leaves' else trump_strength_ober_hearts if followed_card == 'Ober of Hearts' else trump_strength_ober_bells if followed_card == 'Ober of Bells' else trump_strength_unter_acorns if followed_card == 'Unter of Acorns' else trump_strength_unter_leaves if followed_card == 'Unter of Leaves' else trump_strength_unter_hearts if followed_card == 'Unter of Hearts' else trump_strength_unter_bells if followed_card == 'Unter of Bells' else trump_strength_solo_suit_ace if followed_card in ['Ace of Acorns', 'Ace of Leaves', 'Ace of Hearts', 'Ace of Bells'] else trump_strength_solo_suit_ten)"}}},
        {"set": {"key": "led_rank", "value": {"calc": "plain_rank_ace if led_card in ['Ace of Acorns', 'Ace of Leaves', 'Ace of Hearts', 'Ace of Bells'] else plain_rank_ten if led_card in ['Ten of Acorns', 'Ten of Leaves', 'Ten of Hearts', 'Ten of Bells'] else plain_rank_ober if led_card in ['Ober of Acorns', 'Ober of Leaves', 'Ober of Hearts', 'Ober of Bells'] else plain_rank_unter"}}},
        {"set": {"key": "followed_rank", "value": {"calc": "plain_rank_ace if followed_card in ['Ace of Acorns', 'Ace of Leaves', 'Ace of Hearts', 'Ace of Bells'] else plain_rank_ten if followed_card in ['Ten of Acorns', 'Ten of Leaves', 'Ten of Hearts', 'Ten of Bells'] else plain_rank_ober if followed_card in ['Ober of Acorns', 'Ober of Leaves', 'Ober of Hearts', 'Ober of Bells'] else plain_rank_unter"}}},
        {"set": {"key": "trick_winner", "value": {"calc": "(leader if led_strength > followed_strength else follower) if max(led_strength, followed_strength) > 0 else (follower if followed_suit == led_suit and followed_rank > led_rank else leader)"}}},
        {"set": {"key": "trick_points", "value": {"calc": "(points_ace if led_card in ['Ace of Acorns', 'Ace of Leaves', 'Ace of Hearts', 'Ace of Bells'] else points_ten if led_card in ['Ten of Acorns', 'Ten of Leaves', 'Ten of Hearts', 'Ten of Bells'] else points_ober if led_card in ['Ober of Acorns', 'Ober of Leaves', 'Ober of Hearts', 'Ober of Bells'] else points_unter) + (points_ace if followed_card in ['Ace of Acorns', 'Ace of Leaves', 'Ace of Hearts', 'Ace of Bells'] else points_ten if followed_card in ['Ten of Acorns', 'Ten of Leaves', 'Ten of Hearts', 'Ten of Bells'] else points_ober if followed_card in ['Ober of Acorns', 'Ober of Leaves', 'Ober of Hearts', 'Ober of Bells'] else points_unter)"}}},
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "hand_points", "value": {"calc": "trick_points"}}},
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "tricks_won", "value": 1}},
        {"set": {"key": "leader", "value": {"calc": "trick_winner"}}},
        {"set": {"key": "follower", "value": {"calc": "2 if leader == 1 else 1"}}},
        {"set": {"player": 1, "key": "stack1_up", "value": {"calc": "seat1_stack1_down"}, "if": {"calc": "players[0].stack1_pending_reveal"}}},
        {"set": {"key": "seat1_stack1_down", "value": "", "if": {"calc": "players[0].stack1_pending_reveal"}}},
        {"set": {"player": 1, "key": "stack1_pending_reveal", "value": false}},
        {"set": {"player": 1, "key": "stack2_up", "value": {"calc": "seat1_stack2_down"}, "if": {"calc": "players[0].stack2_pending_reveal"}}},
        {"set": {"key": "seat1_stack2_down", "value": "", "if": {"calc": "players[0].stack2_pending_reveal"}}},
        {"set": {"player": 1, "key": "stack2_pending_reveal", "value": false}},
        {"set": {"player": 2, "key": "stack1_up", "value": {"calc": "seat2_stack1_down"}, "if": {"calc": "players[1].stack1_pending_reveal"}}},
        {"set": {"key": "seat2_stack1_down", "value": "", "if": {"calc": "players[1].stack1_pending_reveal"}}},
        {"set": {"player": 2, "key": "stack1_pending_reveal", "value": false}},
        {"set": {"player": 2, "key": "stack2_up", "value": {"calc": "seat2_stack2_down"}, "if": {"calc": "players[1].stack2_pending_reveal"}}},
        {"set": {"key": "seat2_stack2_down", "value": "", "if": {"calc": "players[1].stack2_pending_reveal"}}},
        {"set": {"player": 2, "key": "stack2_pending_reveal", "value": false}},
        {"set": {"key": "lead_options", "value": {"calc": "players[leader - 1].hand + ([players[leader - 1].stack1_up] if players[leader - 1].stack1_up != '' else []) + ([players[leader - 1].stack2_up] if players[leader - 1].stack2_up != '' else [])"}}}
      ],
      "text": "Seat {trick_winner} wins trick {round_in_hand} ({led_card} against {followed_card}) and takes {trick_points} card points. Any face-down card under a played stack card is now face up."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "the hand is scored",
      "when": {"calc": "round_in_hand == tricks_per_hand"},
      "do": [
        {"set": {"key": "scorer", "value": {"calc": "declarer if players[declarer - 1].hand_points >= contract_bid else defender"}}},
        {"set": {"key": "score_gain", "value": {"calc": "((base_for_53 if contract_bid == bid_low else base_for_66 if contract_bid == bid_mid else base_for_79) + (all_tricks_bonus if players[scorer - 1].tricks_won == tricks_per_hand else 0)) * multiplier"}}},
        {"adjust": {"player": {"calc": "scorer"}, "key": "match_points", "value": {"calc": "score_gain"}}},
        {"adjust": {"players": "all", "key": "card_total", "value": {"calc": "you.hand_points"}}}
      ],
      "text": "Hand {hand_number} is over. Declarer seat {declarer} needed {contract_bid} card points. Seat {scorer} scores {score_gain} match points."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "advance the round",
      "do": [
        {"adjust": {"key": "rounds_played", "value": 1}},
        {"adjust": {"key": "hand_number", "value": 1, "if": {"calc": "round_in_hand == tricks_per_hand and hand_number < hands_in_match"}}},
        {"set": {"key": "round_in_hand", "value": {"calc": "0 if round_in_hand == tricks_per_hand else round_in_hand + 1"}}}
      ]
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last round",
      "when": {"calc": "rounds_played >= total_rounds"},
      "against": ["over"]
    }
  ],
  "end": {
    "over": {
      "when": {"calc": "rounds_played >= total_rounds"},
      "rank_by": "you.match_points * 1000 + you.card_total",
      "text": "Winner: {result}. Match points: Seat 1 {players[0].match_points}, Seat 2 {players[1].match_points}; total card points: Seat 1 {players[0].card_total}, Seat 2 {players[1].card_total}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "DECK. There are {deck_size} cards: Ace, Ten, Ober and Unter in each of four suits (Acorns, Leaves, Hearts, Bells). Card points are Ace {points_ace}, Ten {points_ten}, Ober {points_ober} and Unter {points_unter}, which makes {deck_points} in the deck.\n\nMATCH. The match is {hands_in_match} hands. Each hand is one bidding round followed by {tricks_per_hand} trick rounds ({rounds_per_hand} rounds a hand), which makes {total_rounds} rounds in total. Seat 1 deals hands 1 and 3 and seat 2 deals hands 2 and 4. The non-dealer is called forehand.\n\nDEAL. At the start of each hand all 16 cards are shuffled. Each player receives {private_cards_per_player} private hand cards, seen only by their owner, and {stacks_per_player} stacks, each made of one face-down card under one face-up card. The face-up cards ({face_up_cards_on_table} in total) are visible to both players. Face-down cards are unknown to both players, including their owner.\n\nBIDDING. (1) Both players secretly and simultaneously choose a bid: Pass, {bid_low}, {bid_mid} or {bid_high}. The bid is the number of card points the player promises to take as declarer. (2) The higher bid becomes declarer at that bid. If the bids are equal and not Pass, forehand is declarer at that bid. If both pass, forehand is declarer at {default_bid_when_both_pass}. Both bids are then announced. (3) The declarer chooses a contract and it is announced. Acorns Solo, Leaves Solo, Hearts Solo or Bells Solo: trumps are, from highest to lowest, Ober of Acorns, Ober of Leaves, Ober of Hearts, Ober of Bells, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells, then the Ace and the Ten of the chosen suit; the three other suits each hold only Ace above Ten. Wenz: trumps are, from highest to lowest, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells; each suit holds Ace above Ten above Ober. (4) The defender chooses Stoß or No Stoß, and the choice is announced. The multiplier is {multiplier_stoss} with Stoß and {multiplier_no_stoss} without.\n\nTRICKS ({tricks_per_hand} per hand). Your available cards are your private hand cards plus the face-up card on top of each of your stacks. In the first trick forehand leads; afterwards the winner of the previous trick leads. The leader plays one available card. The other player then plays one available card. All trumps count as one suit, the trump suit, so in a Solo an Ober or Unter is never a card of its printed suit, and in Wenz an Unter is never a card of its printed suit. If the follower has an available card of the led suit, they must play one (only those are offered); otherwise they may play any available card. If any trump was played, the higher trump wins; otherwise the higher card of the led suit wins, and a card of another suit never wins. The winner adds the card points of both cards to their card points for the hand and 1 to their tricks. After the trick, any face-down card whose face-up card was played this trick is turned face up and is available from the next trick on.\n\nHAND SCORING (after trick 8). If the declarer's card points are at least their bid, the declarer scores the contract value in match points; otherwise the defender scores it. Contract value = base, plus {all_tricks_bonus} if the player who scores took all {tricks_per_hand} tricks, multiplied by the Stoß multiplier. The base is {base_for_53} for a bid of 53, {base_for_66} for 66 and {base_for_79} for 79. For example, a 66 bid made with Stoß and not every trick scores 6. Each player's card points for the hand are also added to their running card-point total for the match.\n\nWINNER. After {hands_in_match} hands, the player with more match points wins. If match points are equal, the player with the higher total card points over all hands wins. If both are equal, the match is a draw (the win is shared)."
}
```
````
