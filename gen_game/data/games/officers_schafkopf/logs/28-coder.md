# 28 coder

- time: 2026-10-28T03:02:11+00:00 (122.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 918ea3d5e0794256, reply sha256 dd3addda490bbe71

## Sent

````
# Task: write the XColos game file for "Blind Officers' Schafkopf"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. There are 24 cards in four suits: Acorns, Leaves, Hearts, Bells. Each suit has Ace (11 card points), Ten (10), King (4), Ober (3), Unter (2) and Nine (0). The deck holds 120 card points.

MATCH. The match is four hands of 8 tricks each, one trick per round: 32 rounds. Both players start with 0 match points. Seat 1 has priority in hands 1 and 3. Seat 2 has priority in hands 2 and 4.

START OF EACH HAND (first round of the hand only).
1) Shuffle and deal 8 cards face down to each player. Each player sees only their own cards. The remaining 8 cards form the Blind. They are never seen by anyone, never played and never scored.
2) Sealed bid. Both players choose at the same moment exactly one of these eleven options:
- Pass;
- Wenz-Simple;
- Acorns-Simple;
- Leaves-Simple;
- Hearts-Simple;
- Bells-Simple;
- Wenz-Strong;
- Acorns-Strong;
- Leaves-Strong;
- Hearts-Strong;
- Bells-Strong.
3) Resolution. If both players pass, the hand is Ramsch. Otherwise Strong beats Simple, and any bid beats Pass. If both players bid at the same level (both Simple or both Strong), the priority player's bid wins whatever the contracts. The winning bidder is the declarer and the other player is the defender. The contract and level are those of the winning bid.
4) Both bids and the resulting contract (or Ramsch) are announced to both players.
5) Double. If the hand is not Ramsch, the defender chooses Double or No double. The choice is announced.

CONTRACTS.
- Wenz: the trumps are the four Unters only, ranked Acorns Unter > Leaves Unter > Hearts Unter > Bells Unter. In every suit the non-trump cards rank Ace > Ten > King > Ober > Nine. Unters belong to no plain suit.
- Suit Solo (Acorns, Leaves, Hearts or Bells, as named): there are 12 trumps, ranked from high to low:
  - the four Obers (Acorns > Leaves > Hearts > Bells);
  - then the four Unters (Acorns > Leaves > Hearts > Bells);
  - then the Ace, Ten, King and Nine of the named suit.
  Obers and Unters belong to no plain suit. In the other three suits the non-trump cards rank Ace > Ten > King > Nine.
- Ramsch: trumps and ranks exactly as in Wenz.

TRICKS (every round).
1) The leader plays any card from their hand. In the first trick of a hand the leader is the declarer, or the priority player in Ramsch. Afterwards the leader is the winner of the previous trick.
2) The other player then plays a card. If a trump was led, they must play a trump if they have one. If a plain suit was led, they must play a non-trump card of that suit if they have one. Otherwise they may play any card.
3) The trick is won by the highest trump in it. If it has no trump, it is won by the higher card of the led suit.
4) The trick winner adds the card points of both cards to their card-point total for the hand, and leads next.
5) The two cards, the trick winner and both players' card-point totals for the hand are announced.

END OF EACH HAND (after the 8th trick). Let D be the declarer's card points and F the defender's card points.
- A Simple contract is made if D >= F + 10.
- A Strong contract is made if D >= 2 x F and D >= 30.
- Stake: Simple is 2 match points and Strong is 4 match points. The stake is doubled if the defender chose Double (Simple 4, Strong 8).
- If the contract is made, the declarer gains the stake. Otherwise the defender gains the stake.
- Ramsch: the player with fewer card points gains 1 match point. If the card points are equal, nobody scores.
- Card-point totals reset to 0 and the next hand begins.

END. After the fourth hand the match ends.

How the winner is decided: After the fourth hand, the player with more match points wins. Equal match points is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Blind Officers' Schafkopf (2 to 2 players, best with 2)

Two-player Schafkopf variant: sealed contract bids, an optional double, 8 tricks per hand from a 24-card deck with an unseen Blind, over 4 hands (32 rounds), scored in match points.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The cards this player holds, named like 'Acorns Ace', 'Bells Unter'.
  - each player: bid (text, starts ''); everyone sees it. This hand's sealed bid (one of the 11 options). It is revealed only after both players have bid.
  - each player: bid_level (number, starts 0); everyone sees it. Bid level: Pass 0, Simple 1, Strong 2.
  - each player: card_points (number, starts 0); everyone sees it. Card points won in tricks this hand. Reset to 0 at the end of each hand.
  - each player: match_points (number, starts 0); everyone sees it. Match points across the match (the score).
  - the table: deck (list, starts []); hidden from all players. Undealt cards during the deal (24 at the start of each hand).
  - the table: blind (list, starts []); hidden from all players. The 8 undealt cards of the hand. Never seen, played or scored.
  - the table: hand_number (number, starts 1); everyone sees it. The current hand, 1 to 4 (5 means the match is over).
  - the table: trick_number (number, starts 1); everyone sees it. The trick within the current hand, 1 to 8.
  - the table: priority_seat (number, starts 1); everyone sees it. Seat with priority: 1 in hands 1 and 3, 2 in hands 2 and 4.
  - the table: contract (text, starts ''); everyone sees it. Wenz, Acorns, Leaves, Hearts, Bells, or Ramsch.
  - the table: level (text, starts ''); everyone sees it. Simple or Strong (empty in Ramsch).
  - the table: declarer_seat (number, starts 0); everyone sees it. The declarer's seat (0 in Ramsch).
  - the table: defender_seat (number, starts 0); everyone sees it. The defender's seat (0 in Ramsch).
  - the table: doubled (bool, starts False); everyone sees it. Whether the defender chose Double this hand.
  - the table: trump_list (list, starts []); everyone sees it. This hand's trumps, ordered from highest to lowest.
  - the table: leader_seat (number, starts 0); everyone sees it. The seat that leads the current trick.
  - the table: led_card (text, starts ''); everyone sees it. The card led in the current trick.
  - the table: follow_card (text, starts ''); everyone sees it. The card played second in the current trick.
  - the table: trick_winner (number, starts 0); everyone sees it. The seat that won the last trick.
  - parameters, each kept as a table attribute: deck_size = 24, suits = 4, cards_per_suit = 6, deck_card_points = 120, points_ace = 11, points_ten = 10, points_king = 4, points_ober = 3, points_unter = 2, points_nine = 0, hands = 4, tricks_per_hand = 8, total_rounds = 32, cards_dealt_per_player = 8, blind_size = 8, bid_options = 11, wenz_trumps = 4, suit_solo_trumps = 12, simple_margin = 10, strong_multiplier = 2, strong_minimum_points = 30, simple_stake = 2, strong_stake = 4, double_factor = 2, ramsch_award = 1, starting_match_points = 0, level_pass = 0, level_simple = 1, level_strong = 2, trump_strength_base = 100, plain_rank_ace = 6, plain_rank_ten = 5, plain_rank_king = 4, plain_rank_ober = 3, plain_rank_nine = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Both players start with 0 match points.
  2. hand_number is set to 1 and trick_number to 1.
  3. The full 24-card deck consists of Acorns, Leaves, Hearts and Bells, each with Ace, Ten, King, Ober, Unter and Nine. It is rebuilt at the start of every hand.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_number == 1: set game.deck to all 24 cards. Draw 8 cards at random from deck into each player's hand. Move the remaining 8 cards to game.blind, leaving deck empty. Set every card_points to 0, doubled to false, contract and level to empty, and declarer_seat and defender_seat to 0. Set priority_seat to 1 if hand_number is odd, else 2.
  2. [sync] all players. What happens: When trick_number == 1: each player is sent their own hand.
  3. [poll] all players answers: one of: Pass, Wenz-Simple, Acorns-Simple, Leaves-Simple, Hearts-Simple, Bells-Simple, Wenz-Strong, Acorns-Strong, Leaves-Strong, Hearts-Strong, Bells-Strong. What happens: When trick_number == 1: store each answer in that player's bid. Set bid_level to 0 for Pass, 1 for any -Simple bid, 2 for any -Strong bid. No one sees a bid until both are in.
  4. [update] all players. What happens: When trick_number == 1, resolve the bids. If both bid_level == 0: contract = Ramsch, declarer_seat = 0, defender_seat = 0, leader_seat = priority_seat, trump_list = [Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter]. Otherwise the declarer is the seat with the higher bid_level; if the levels are equal, the declarer is priority_seat. Set declarer_seat to that seat and defender_seat to the other. Take contract (the word before the dash) and level (Simple or Strong) from the declarer's bid. Set leader_seat = declarer_seat. If contract == Wenz, trump_list = [Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter]. If contract is a suit X, trump_list = [Acorns Ober, Leaves Ober, Hearts Ober, Bells Ober, Acorns Unter, Leaves Unter, Hearts Unter, Bells Unter, X Ace, X Ten, X King, X Nine].
  5. [tell] all players. What happens: When trick_number == 1: announce both bids, the contract and level (or Ramsch), and the declarer.
  6. [ask] the seat in game.defender_seat answers: one of: Double, No double. What happens: When trick_number == 1 and contract != Ramsch: set doubled = true if the answer is Double, else false.
  7. [tell] all players. What happens: When trick_number == 1 and contract != Ramsch: announce whether the defender doubled.
  8. [ask] the seat in game.leader_seat answers: any one card from their own hand. What happens: Set led_card to the chosen card and remove it from the leader's hand.
  9. [ask] the seat that is not game.leader_seat answers: one legal card from their own hand (see offers). What happens: Set follow_card to the chosen card and remove it from the follower's hand.
  10. [update] all players. What happens: Compute each card's strength. A card in trump_list scores 100 + (length of trump_list - its position, where the first position is 0). A card not in trump_list whose suit matches led_card's suit (led_card itself not being a trump) scores its plain rank: Ace 6, Ten 5, King 4, Ober 3, Nine 1. Any other card scores 0. trick_winner = leader_seat if strength(led_card) > strength(follow_card), else the other seat. Add the card points of both cards (Ace 11, Ten 10, King 4, Ober 3, Unter 2, Nine 0) to the trick winner's card_points. Set leader_seat = trick_winner.
  11. [tell] all players. What happens: Announce led_card, follow_card, the trick_winner, and both players' card_points.
  12. [update] all players. What happens: When trick_number == 8, score the hand. Let D = the declarer's card_points and F = the defender's card_points. Stake = 2 if level is Simple, 4 if level is Strong; doubled if doubled == true. Simple is made if D >= F + 10. Strong is made if D >= 2*F and D >= 30. If made, the declarer's match_points += stake; otherwise the defender's match_points += stake. If contract == Ramsch, the player with fewer card_points gets match_points += 1, and nobody scores if the totals are equal. Then set both card_points to 0, hand_number += 1, trick_number = 1. Otherwise (trick_number < 8): trick_number += 1.
  13. [tell] all players. What happens: When a hand has just been scored (trick_number == 1 and hand_number > 1): announce whether the contract was made (or the Ramsch result), the stake awarded, and both match_points.
  14. [check] all players. What happens: End the game if hand_number > 4; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand starts, then each player receives 8 cards from the 24-card deck into hand, and the other 8 go to blind, which is never played or scored.
  R2. When it is hand 1 or 3, then priority_seat is 1; when it is hand 2 or 4, then priority_seat is 2.
  R3. When a hand starts, then both players bid simultaneously, choosing one of 11 options: Pass, or one of Wenz/Acorns/Leaves/Hearts/Bells at the Simple or Strong level.
  R4. When both players pass, then contract is Ramsch and nobody is declarer.
  R5. When one player bids Strong and the other bids Simple or Pass, then the Strong bidder is declarer.
  R6. When one player bids Simple and the other passes, then the Simple bidder is declarer.
  R7. When both players bid at the same level, then the priority player's bid wins, whatever the contracts.
  R8. When the bids are resolved, then both bids and the resulting contract are announced to both players.
  R9. When the hand is not Ramsch, then the defender chooses Double or No double, and the choice is announced.
  R10. When the contract is Wenz or Ramsch, then the only trumps are the 4 Unters, ranked Acorns > Leaves > Hearts > Bells, and plain suits rank Ace > Ten > King > Ober > Nine.
  R11. When the contract is a suit solo, then there are 12 trumps ranked: the 4 Obers (Acorns > Leaves > Hearts > Bells), then the 4 Unters in the same order, then Ace, Ten, King, Nine of the named suit; the other suits rank Ace > Ten > King > Nine.
  R12. When it is the first trick of a hand, then the declarer leads, or the priority player leads in Ramsch.
  R13. When a trick after the first starts, then the previous trick's winner leads.
  R14. When a trump is led and the follower holds a trump, then the follower must play a trump.
  R15. When a plain suit is led and the follower holds a non-trump card of that suit, then the follower must play one.
  R16. When the follower cannot follow as required, then the follower may play any card.
  R17. When a trick contains a trump, then the highest trump wins it; otherwise the higher card of the led suit wins it.
  R18. When a trick is won, then the winner's card_points increase by the card points of both cards (Ace 11, Ten 10, King 4, Ober 3, Unter 2, Nine 0).
  R19. When a trick ends, then both cards, the winner and both card_points totals are announced.
  R20. When a Simple contract ends, then it is made if the declarer's card points D >= the defender's card points F + 10.
  R21. When a Strong contract ends, then it is made if D >= 2 x F and D >= 30.
  R22. When a contract is made, then the declarer gains the stake (Simple 2, Strong 4); when it is not made, then the defender gains it.
  R23. When the defender chose Double, then the stake is doubled (Simple 4, Strong 8).
  R24. When a Ramsch hand ends, then the player with fewer card points gains 1 match point, and nobody scores if the card points are equal.
  R25. When a hand ends, then both card_points reset to 0.
  R26. When the fourth hand (round 32) ends, then the match ends, the player with more match_points wins, and equal match_points is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Sealed bid (first round of each hand) | asked: both seats | options: Pass, Wenz-Simple, Acorns-Simple, Leaves-Simple, Hearts-Simple, Bells-Simple, Wenz-Strong, Acorns-Strong, Leaves-Strong, Hearts-Strong, Bells-Strong
  - Double (first round of a non-Ramsch hand) | asked: the defender only; the declarer is not asked | options: Double, No double
  - Lead a card | asked: the seat in leader_seat | options: every card in their hand
  - Follow a card | asked: the seat that did not lead | options: If led_card is in trump_list and the follower holds any card in trump_list: only those trumps. If led_card is not a trump and the follower holds non-trump cards of led_card's suit: only those. Otherwise: every card in their hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.hand_number > 4
  - each player's standing: you.match_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After four hands (32 tricks), the player with more match points wins. Equal match points share the win, which is a draw.
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

- each player: `card_points` (number, visible: public, starts 0): Card points won in tricks this hand. Reset to 0 at the end of each hand.
- each player: `match_points` (number, visible: public, starts 0): Match points across the match (the score).
- the table: `hand_number` (number, visible: public, starts 1): The current hand, 1 to 4 (5 means the match is over).
- the table: `contract` (text, visible: public, starts ''): Wenz, Acorns, Leaves, Hearts, Bells, or Ramsch.
- the table: `declarer_seat` (number, visible: public, starts 0): The declarer's seat (0 in Ramsch).
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, suits = 4, cards_per_suit = 6, deck_card_points = 120, points_ace = 11, points_ten = 10, points_king = 4, points_ober = 3, points_unter = 2, points_nine = 0, hands = 4, tricks_per_hand = 8, total_rounds = 32, cards_dealt_per_player = 8, blind_size = 8, bid_options = 11, wenz_trumps = 4, suit_solo_trumps = 12, simple_margin = 10, strong_multiplier = 2, strong_minimum_points = 30, simple_stake = 2, strong_stake = 4, double_factor = 2, ramsch_award = 1, starting_match_points = 0, level_pass = 0, level_simple = 1, level_strong = 2, trump_strength_base = 100, plain_rank_ace = 6, plain_rank_ten = 5, plain_rank_king = 4, plain_rank_ober = 3, plain_rank_nine = 1
- the game ends with ONE ending whose `rank_by` is `you.match_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "blind_officers_schafkopf",
    "name": "Blind Officers' Schafkopf",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Schafkopf: sealed contract bids, an optional double and 8 tricks per hand from a 24-card deck with an unseen Blind, over 4 hands."
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
        "key": "bid",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_level",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "match_points",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "blind",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Acorns Ace",
          "Acorns Ten",
          "Acorns King",
          "Acorns Ober",
          "Acorns Unter",
          "Acorns Nine",
          "Leaves Ace",
          "Leaves Ten",
          "Leaves King",
          "Leaves Ober",
          "Leaves Unter",
          "Leaves Nine",
          "Hearts Ace",
          "Hearts Ten",
          "Hearts King",
          "Hearts Ober",
          "Hearts Unter",
          "Hearts Nine",
          "Bells Ace",
          "Bells Ten",
          "Bells King",
          "Bells Ober",
          "Bells Unter",
          "Bells Nine"
        ]
      },
      {
        "key": "suit_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Acorns",
          "Leaves",
          "Hearts",
          "Bells"
        ]
      },
      {
        "key": "index_list",
        "visible": "none",
        "type": "list",
        "initial": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
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
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "contract",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "level",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "declarer_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "defender_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "doubled",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "trump_list",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "follow_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "led_suit_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "led_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "follow_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_points",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_made",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_result",
        "visible": "public",
        "type": "text",
        "initial": "no hand scored yet"
      },
      {
        "key": "last_scorer",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_stake",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_card_points",
        "visible": "public",
        "type": "number",
        "initial": 120
      },
      {
        "key": "points_ace",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "points_ten",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "points_king",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "points_ober",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "points_unter",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "points_nine",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "blind_size",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "bid_options",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "wenz_trumps",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "suit_solo_trumps",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "simple_margin",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "strong_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "strong_minimum_points",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "simple_stake",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "strong_stake",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "double_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "ramsch_award",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_match_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "level_pass",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "level_simple",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "level_strong",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "trump_strength_base",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "plain_rank_ace",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "plain_rank_ten",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "plain_rank_king",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "plain_rank_ober",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "plain_rank_nine",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the match begins",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "match_points",
            "value": {
              "calc": "starting_match_points"
            }
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
            "key": "deck",
            "value": {
              "calc": "all_cards"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "shuffle and deal",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {"set": {"key": "deck", "value": {"calc": "all_cards"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "blind", "value": {"calc": "deck"}}},
        {"set": {"key": "deck", "value": {"calc": "[]"}}},
        {"set": {"players": "all", "key": "card_points", "value": 0}},
        {"set": {"players": "all", "key": "bid", "value": "not yet bid"}},
        {"set": {"players": "all", "key": "bid_level", "value": 0}},
        {"set": {"key": "doubled", "value": false}},
        {"set": {"key": "contract", "value": "undecided"}},
        {"set": {"key": "level", "value": "undecided"}},
        {"set": {"key": "led_card", "value": "none yet"}},
        {"set": {"key": "follow_card", "value": "none yet"}},
        {"set": {"key": "declarer_seat", "value": 0}},
        {"set": {"key": "defender_seat", "value": 0}},
        {"set": {"key": "priority_seat", "value": {"calc": "1 if int(hand_number / 2) * 2 != hand_number else 2"}}}
      ],
      "text": "Hand {hand_number} of {hands}: the cards are shuffled and dealt. Seat {priority_seat} has priority."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "all",
      "mode": "self",
      "fields": [
        "hand"
      ],
      "text": "Your cards for this hand:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Pass",
          "Wenz-Simple",
          "Acorns-Simple",
          "Leaves-Simple",
          "Hearts-Simple",
          "Bells-Simple",
          "Wenz-Strong",
          "Acorns-Strong",
          "Leaves-Strong",
          "Hearts-Strong",
          "Bells-Strong"
        ]
      },
      "store": "bid",
      "text": "Hand {hand_number}: choose your sealed bid. Your opponent bids at the same moment and sees your bid only when both are in. Strong beats Simple, any bid beats Pass; at the same level the priority player (seat {priority_seat}) wins whatever the contracts. If both pass, the hand is Ramsch."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "resolve the bids",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid_level",
            "value": {
              "calc": "level_pass if you.bid == 'Pass' else (level_strong if you.bid in ['Wenz-Strong', 'Acorns-Strong', 'Leaves-Strong', 'Hearts-Strong', 'Bells-Strong'] else level_simple)"
            }
          }
        },
        {
          "set": {
            "key": "declarer_seat",
            "value": {
              "calc": "0 if max([p.bid_level for p in players]) == level_pass else (players[0].seat if players[0].bid_level > players[1].bid_level else (players[1].seat if players[1].bid_level > players[0].bid_level else priority_seat))"
            }
          }
        },
        {
          "set": {
            "key": "defender_seat",
            "value": {
              "calc": "[p.seat for p in players if p.seat != declarer_seat][0]"
            },
            "if": {
              "calc": "declarer_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": "Ramsch",
            "if": {
              "calc": "declarer_seat == 0"
            }
          }
        },
        {
          "set": {
            "key": "level",
            "value": "",
            "if": {
              "calc": "declarer_seat == 0"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "[s for s in ['Wenz'] + suit_names if players[declarer_seat - 1].bid in [s + '-Simple', s + '-Strong']][0]"
            },
            "if": {
              "calc": "declarer_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "level",
            "value": {
              "calc": "'Strong' if players[declarer_seat - 1].bid_level == level_strong else 'Simple'"
            },
            "if": {
              "calc": "declarer_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "priority_seat if declarer_seat == 0 else declarer_seat"
            }
          }
        },
        {
          "set": {
            "key": "trump_list",
            "value": {
              "calc": "[s + ' Unter' for s in suit_names] if contract in ['Wenz', 'Ramsch'] else [s + ' Ober' for s in suit_names] + [s + ' Unter' for s in suit_names] + [contract + ' Ace', contract + ' Ten', contract + ' King', contract + ' Nine']"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the bids are revealed",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "all",
      "text": "Bids: seat 1 bid {players[0].bid}, seat 2 bid {players[1].bid}. Contract: {contract} {level}. Declarer: seat {declarer_seat}; defender: seat {defender_seat} (0 means nobody, in Ramsch). Seat {leader_seat} leads the first trick. Trumps, high to low: {trump_list}."
    },
    {
      "use": "ask",
      "phase": "double",
      "label": "double",
      "when": {
        "calc": "trick_number == 1 and contract != 'Ramsch'"
      },
      "to": {
        "where": "you.seat == defender_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Double",
          "No double"
        ]
      },
      "verify": {
        "bind": "double_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "doubled",
              "value": {
                "calc": "$answer == 'Double'"
              }
            }
          }
        ]
      },
      "text": "You are the defender against {contract} {level}. Double or No double? Double doubles the stake whoever wins it (Simple 4, Strong 8); No double leaves it at Simple 2, Strong 4."
    },
    {
      "use": "tell",
      "phase": "double",
      "label": "the double is announced",
      "when": {
        "calc": "trick_number == 1 and contract != 'Ramsch'"
      },
      "to": "all",
      "text": "The defender, seat {defender_seat}, chose {double_choice}. Doubled: {doubled}."
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
      "verify": {
        "bind": "lead_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "led_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "[s for s in suit_names if led_card in [s + ' Ace', s + ' Ten', s + ' King', s + ' Ober', s + ' Unter', s + ' Nine']][0]"
              }
            }
          },
          {
            "set": {
              "key": "led_suit_cards",
              "value": {
                "calc": "[led_suit + ' Ace', led_suit + ' Ten', led_suit + ' King', led_suit + ' Ober', led_suit + ' Unter', led_suit + ' Nine']"
              }
            }
          },
          {
            "set": {
              "players": {
                "where": "you.seat != leader_seat"
              },
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c in trump_list] if (led_card in trump_list and len([c for c in you.hand if c in trump_list]) > 0) else ([c for c in you.hand if c in led_suit_cards and c not in trump_list] if (led_card not in trump_list and len([c for c in you.hand if c in led_suit_cards and c not in trump_list]) > 0) else you.hand)"
              }
            }
          }
        ]
      },
      "text": "Hand {hand_number}, trick {trick_number} of {tricks_per_hand}, contract {contract} {level}. Trumps, high to low: {trump_list}. Lead any card from your hand."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "follow a card",
      "to": {
        "where": "you.seat != leader_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "follow_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "follow_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Seat {leader_seat} led {led_card}. Trumps, high to low: {trump_list}. Play a card: you are offered only the cards you may l
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `suit_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `index_list` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "blind_officers_schafkopf",
    "name": "Blind Officers' Schafkopf",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Schafkopf: sealed contract bids, an optional double and 8 tricks per hand from a 24-card deck with an unseen Blind, over 4 hands."
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
        "key": "bid",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_level",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "match_points",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "blind",
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
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "contract",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "level",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "declarer_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "defender_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "doubled",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "trump_list",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "follow_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "led_suit_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "led_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "follow_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_points",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_made",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_result",
        "visible": "public",
        "type": "text",
        "initial": "no hand scored yet"
      },
      {
        "key": "last_scorer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_stake",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_card_points",
        "visible": "public",
        "type": "number",
        "initial": 120
      },
      {
        "key": "points_ace",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "points_ten",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "points_king",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "points_ober",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "points_unter",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "points_nine",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "blind_size",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "bid_options",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "wenz_trumps",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "suit_solo_trumps",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "simple_margin",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "strong_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "strong_minimum_points",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "simple_stake",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "strong_stake",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "double_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "ramsch_award",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_match_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "level_pass",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "level_simple",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "level_strong",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "trump_strength_base",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "plain_rank_ace",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "plain_rank_ten",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "plain_rank_king",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "plain_rank_ober",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "plain_rank_nine",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the match begins",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "match_points",
            "value": {
              "calc": "starting_match_points"
            }
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
            "key": "deck",
            "value": {
              "calc": "['Acorns Ace', 'Acorns Ten', 'Acorns King', 'Acorns Ober', 'Acorns Unter', 'Acorns Nine', 'Leaves Ace', 'Leaves Ten', 'Leaves King', 'Leaves Ober', 'Leaves Unter', 'Leaves Nine', 'Hearts Ace', 'Hearts Ten', 'Hearts King', 'Hearts Ober', 'Hearts Unter', 'Hearts Nine', 'Bells Ace', 'Bells Ten', 'Bells King', 'Bells Ober', 'Bells Unter', 'Bells Nine']"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "shuffle and deal",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {"set": {"key": "deck", "value": {"calc": "['Acorns Ace', 'Acorns Ten', 'Acorns King', 'Acorns Ober', 'Acorns Unter', 'Acorns Nine', 'Leaves Ace', 'Leaves Ten', 'Leaves King', 'Leaves Ober', 'Leaves Unter', 'Leaves Nine', 'Hearts Ace', 'Hearts Ten', 'Hearts King', 'Hearts Ober', 'Hearts Unter', 'Hearts Nine', 'Bells Ace', 'Bells Ten', 'Bells King', 'Bells Ober', 'Bells Unter', 'Bells Nine']"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "blind", "value": {"calc": "deck"}}},
        {"set": {"key": "deck", "value": {"calc": "[]"}}},
        {"set": {"players": "all", "key": "card_points", "value": 0}},
        {"set": {"players": "all", "key": "bid", "value": "not yet bid"}},
        {"set": {"players": "all", "key": "bid_level", "value": 0}},
        {"set": {"key": "doubled", "value": false}},
        {"set": {"key": "contract", "value": "undecided"}},
        {"set": {"key": "level", "value": "undecided"}},
        {"set": {"key": "led_card", "value": "none yet"}},
        {"set": {"key": "follow_card", "value": "none yet"}},
        {"set": {"key": "declarer_seat", "value": 0}},
        {"set": {"key": "defender_seat", "value": 0}},
        {"set": {"key": "priority_seat", "value": {"calc": "1 if int(hand_number / 2) * 2 != hand_number else 2"}}}
      ],
      "text": "Hand {hand_number} of {hands}: the cards are shuffled and dealt. Seat {priority_seat} has priority."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "all",
      "mode": "self",
      "fields": [
        "hand"
      ],
      "text": "Your cards for this hand:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Pass",
          "Wenz-Simple",
          "Acorns-Simple",
          "Leaves-Simple",
          "Hearts-Simple",
          "Bells-Simple",
          "Wenz-Strong",
          "Acorns-Strong",
          "Leaves-Strong",
          "Hearts-Strong",
          "Bells-Strong"
        ]
      },
      "store": "bid",
      "text": "Hand {hand_number}: choose your sealed bid. Your opponent bids at the same moment and sees your bid only when both are in. Strong beats Simple, any bid beats Pass; at the same level the priority player (seat {priority_seat}) wins whatever the contracts. If both pass, the hand is Ramsch."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "resolve the bids",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid_level",
            "value": {
              "calc": "level_pass if you.bid == 'Pass' else (level_strong if you.bid in ['Wenz-Strong', 'Acorns-Strong', 'Leaves-Strong', 'Hearts-Strong', 'Bells-Strong'] else level_simple)"
            }
          }
        },
        {
          "set": {
            "key": "declarer_seat",
            "value": {
              "calc": "0 if max([p.bid_level for p in players]) == level_pass else (players[0].seat if players[0].bid_level > players[1].bid_level else (players[1].seat if players[1].bid_level > players[0].bid_level else priority_seat))"
            }
          }
        },
        {
          "set": {
            "key": "defender_seat",
            "value": {
              "calc": "[p.seat for p in players if p.seat != declarer_seat][0]"
            },
            "if": {
              "calc": "declarer_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": "Ramsch",
            "if": {
              "calc": "declarer_seat == 0"
            }
          }
        },
        {
          "set": {
            "key": "level",
            "value": "",
            "if": {
              "calc": "declarer_seat == 0"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "[s for s in ['Wenz', 'Acorns', 'Leaves', 'Hearts', 'Bells'] if players[declarer_seat - 1].bid in [s + '-Simple', s + '-Strong']][0]"
            },
            "if": {
              "calc": "declarer_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "level",
            "value": {
              "calc": "'Strong' if players[declarer_seat - 1].bid_level == level_strong else 'Simple'"
            },
            "if": {
              "calc": "declarer_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "priority_seat if declarer_seat == 0 else declarer_seat"
            }
          }
        },
        {
          "set": {
            "key": "trump_list",
            "value": {
              "calc": "['Acorns Unter', 'Leaves Unter', 'Hearts Unter', 'Bells Unter'] if contract in ['Wenz', 'Ramsch'] else ['Acorns Ober', 'Leaves Ober', 'Hearts Ober', 'Bells Ober', 'Acorns Unter', 'Leaves Unter', 'Hearts Unter', 'Bells Unter', contract + ' Ace', contract + ' Ten', contract + ' King', contract + ' Nine']"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the bids are revealed",
      "when": {
        "calc": "trick_number == 1"
      },
      "to": "all",
      "text": "Bids: seat 1 bid {players[0].bid}, seat 2 bid {players[1].bid}. Contract: {contract} {level}. Declarer: seat {declarer_seat}; defender: seat {defender_seat} (0 means nobody, in Ramsch). Seat {leader_seat} leads the first trick. Trumps, high to low: {trump_list}."
    },
    {
      "use": "ask",
      "phase": "double",
      "label": "double",
      "when": {
        "calc": "trick_number == 1 and contract != 'Ramsch'"
      },
      "to": {
        "where": "you.seat == defender_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Double",
          "No double"
        ]
      },
      "verify": {
        "bind": "double_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "doubled",
              "value": {
                "calc": "$answer == 'Double'"
              }
            }
          }
        ]
      },
      "text": "You are the defender against {contract} {level}. Double or No double? Double doubles the stake whoever wins it (Simple 4, Strong 8); No double leaves it at Simple 2, Strong 4."
    },
    {
      "use": "tell",
      "phase": "double",
      "label": "the double is announced",
      "when": {
        "calc": "trick_number == 1 and contract != 'Ramsch'"
      },
      "to": "all",
      "text": "The defender, seat {defender_seat}, chose {double_choice}. Doubled: {doubled}."
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
      "verify": {
        "bind": "lead_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "led_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "[s for s in ['Acorns', 'Leaves', 'Hearts', 'Bells'] if led_card in [s + ' Ace', s + ' Ten', s + ' King', s + ' Ober', s + ' Unter', s + ' Nine']][0]"
              }
            }
          },
          {
            "set": {
              "key": "led_suit_cards",
              "value": {
                "calc": "[led_suit + ' Ace', led_suit + ' Ten', led_suit + ' King', led_suit + ' Ober', led_suit + ' Unter', led_suit + ' Nine']"
              }
            }
          },
          {
            "set": {
              "players": {
                "where": "you.seat != leader_seat"
              },
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c in trump_list] if (led_card in trump_list and len([c for c in you.hand if c in trump_list]) > 0) else ([c for c in you.hand if c in led_suit_cards and c not in trump_list] if (led_card not in trump_list and len([c for c in you.hand if c in led_suit_cards and c not in trump_list]) > 0) else you.hand)"
              }
            }
          }
        ]
      },
      "text": "Hand {hand_number}, trick {trick_number} of {tricks_per_hand}, contract {contract} {level}. Trumps, high to low: {trump_list}. Lead any card from your hand."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "follow a card",
      "to": {
        "where": "you.seat != leader_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "follow_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "follow_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Seat {leader_seat} led {led_card}. Trumps, high to low: {trump_list}. Play a card: you are offered only the cards you may legally play (a trump if a trump was led and you hold one; a non-trump of the led suit if a plain suit was led and you hold one; otherwise any card)."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is decided",
      "do": [
        {
          "set": {
            "key": "led_strength",
            "value": {
              "calc": "trump_strength_base + len(trump_list) - [i for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] if i < len(trump_list) and trump_list[i] == led_card][0] if led_card in trump_list else (plain_rank_ace if led_card == led_suit + ' Ace' else (plain_rank_ten if led_card == led_suit + ' Ten' else (plain_rank_king if led_card == led_suit + ' King' else (plain_rank_ober if led_card == led_suit + ' Ober' else plain_rank_nine))))"
            }
          }
        },
        {
          "set": {
            "key": "follow_strength",
            "value": {
              "calc": "trump_strength_base + len(trump_list) - [i for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] if i < len(trump_list) and trump_list[i] == follow_card][0] if follow_card in trump_list else ((plain_rank_ace if follow_card == led_suit + ' Ace' else (plain_rank_ten if follow_card == led_suit + ' Ten' else (plain_rank_king if follow_card == led_suit + ' King' else (plain_rank_ober if follow_card == led_suit + ' Ober' else plain_rank_nine)))) if (led_card not in trump_list and follow_card in led_suit_cards) else 0)"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "leader_seat if led_strength > follow_strength else [p.seat for p in players if p.seat != leader_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "trick_points",
            "value": {
              "calc": "(points_ace if led_card in ['Acorns Ace', 'Leaves Ace', 'Hearts Ace', 'Bells Ace'] else (points_ten if led_card in ['Acorns Ten', 'Leaves Ten', 'Hearts Ten', 'Bells Ten'] else (points_king if led_card in ['Acorns King', 'Leaves King', 'Hearts King', 'Bells King'] else (points_ober if led_card in ['Acorns Ober', 'Leaves Ober', 'Hearts Ober', 'Bells Ober'] else (points_unter if led_card in ['Acorns Unter', 'Leaves Unter', 'Hearts Unter', 'Bells Unter'] else points_nine))))) + (points_ace if follow_card in ['Acorns Ace', 'Leaves Ace', 'Hearts Ace', 'Bells Ace'] else (points_ten if follow_card in ['Acorns Ten', 'Leaves Ten', 'Hearts Ten', 'Bells Ten'] else (points_king if follow_card in ['Acorns King', 'Leaves King', 'Hearts King', 'Bells King'] else (points_ober if follow_card in ['Acorns Ober', 'Leaves Ober', 'Hearts Ober', 'Bells Ober'] else (points_unter if follow_card in ['Acorns Unter', 'Leaves Unter', 'Hearts Unter', 'Bells Unter'] else points_nine)))))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == trick_winner"
            },
            "key": "card_points",
            "value": {
              "calc": "trick_points"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "trick",
      "label": "the trick is announced",
      "to": "all",
      "text": "Trick {trick_number}: seat {leader_seat} won it. Led card {led_card}, followed by {follow_card}; the trick held {trick_points} card points. Card points this hand: seat 1 {players[0].card_points}, seat 2 {players[1].card_points}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the hand",
      "do": [
        {
          "set": {
            "key": "hand_made",
            "value": {
              "calc": "False if contract == 'Ramsch' else ((sum([p.card_points for p in players if p.seat == declarer_seat]) >= sum([p.card_points for p in players if p.seat == defender_seat]) + simple_margin) if level == 'Simple' else (sum([p.card_points for p in players if p.seat == declarer_seat]) >= strong_multiplier * sum([p.card_points for p in players if p.seat == defender_seat]) and sum([p.card_points for p in players if p.seat == declarer_seat]) >= strong_minimum_points))"
            },
            "if": {
              "calc": "trick_number == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "last_stake",
            "value": {
              "calc": "(ramsch_award if players[0].card_points != players[1].card_points else 0) if contract == 'Ramsch' else (simple_stake if level == 'Simple' else strong_stake) * (double_factor if doubled else 1)"
            },
            "if": {
              "calc": "trick_number == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "last_scorer",
            "value": {
              "calc": "(0 if players[0].card_points == players[1].card_points else (players[0].seat if players[0].card_points < players[1].card_points else players[1].seat)) if contract == 'Ramsch' else (declarer_seat if hand_made else defender_seat)"
            },
            "if": {
              "calc": "trick_number == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "last_result",
            "value": {
              "calc": "('Ramsch: card points equal, nobody scores' if last_scorer == 0 else 'Ramsch: fewer card points scores') if contract == 'Ramsch' else (contract + ' ' + level + (' made by the declarer' if hand_made else ' failed, the defender scores'))"
            },
            "if": {
              "calc": "trick_number == tricks_per_hand"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == last_scorer"
            },
            "key": "match_points",
            "value": {
              "calc": "last_stake"
            },
            "if": {
              "calc": "trick_number == tricks_per_hand and last_scorer > 0"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_points",
            "value": 0,
            "if": {
              "calc": "trick_number == tricks_per_hand"
            }
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": 1,
            "if": {
              "calc": "trick_number == tricks_per_hand"
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
      "use": "tell",
      "phase": "score",
      "label": "the hand result",
      "when": {
        "calc": "trick_number == 1 and hand_number > 1"
      },
      "to": "all",
      "text": "Hand over: {last_result}. Seat {last_scorer} gains {last_stake} match points (seat 0 means nobody). Match points: seat 1 {players[0].match_points}, seat 2 {players[1].match_points}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the fourth hand",
      "when": {
        "calc": "hand_number > hands"
      },
      "against": [
        "match_over"
      ]
    }
  ],
  "end": {
    "match_over": {
      "when": {
        "calc": "hand_number > hands"
      },
      "rank_by": "you.match_points",
      "text": "Winner: {result}. Final match points: Seat 1 {players[0].match_points}, Seat 2 {players[1].match_points}."
    }
  },
  "limits": {
    "rounds": 32,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {deck_size} cards in {suits} suits: Acorns, Leaves, Hearts, Bells. Each suit has Ace ({points_ace} card points), Ten ({points_ten}), King ({points_king}), Ober ({points_ober}), Unter ({points_unter}) and Nine ({points_nine}). The deck holds {deck_card_points} card points.\n\nMATCH. The match is {hands} hands of {tricks_per_hand} tricks each, one trick per round: {total_rounds} rounds. Both players start with {starting_match_points} match points. Seat 1 has priority in hands 1 and 3. Seat 2 has priority in hands 2 and 4.\n\nSTART OF EACH HAND. 1) Shuffle and deal {cards_dealt_per_player} cards face down to each player. Each player sees only their own cards. The remaining {blind_size} cards form the Blind. They are never seen by anyone, never played and never scored. 2) Sealed bid. Both players choose at the same moment exactly one of these {bid_options} options: Pass; Wenz-Simple; Acorns-Simple; Leaves-Simple; Hearts-Simple; Bells-Simple; Wenz-Strong; Acorns-Strong; Leaves-Strong; Hearts-Strong; Bells-Strong. 3) Resolution. If both players pass, the hand is Ramsch and nobody is declarer. Otherwise Strong beats Simple, and any bid beats Pass. If both players bid at the same level (both Simple or both Strong), the priority player's bid wins whatever the contracts. The winning bidder is the declarer and the other player is the defender. The contract and level are those of the winning bid. 4) Both bids and the resulting contract (or Ramsch) are announced to both players. 5) Double. If the hand is not Ramsch, the defender chooses Double or No double. The choice is announced. Double doubles the stake; No double leaves it as it is. In Ramsch nobody is asked.\n\nCONTRACTS. Wenz: the trumps are the {wenz_trumps} Unters only, ranked Acorns Unter > Leaves Unter > Hearts Unter > Bells Unter. In every suit the non-trump cards rank Ace > Ten > King > Ober > Nine. Unters belong to no plain suit. Suit Solo (Acorns, Leaves, Hearts or Bells, as named): there are {suit_solo_trumps} trumps, ranked from high to low: the four Obers (Acorns > Leaves > Hearts > Bells); then the four Unters (Acorns > Leaves > Hearts > Bells); then the Ace, Ten, King and Nine of the named suit. Obers and Unters belong to no plain suit. In the other three suits the non-trump cards rank Ace > Ten > King > Nine. Ramsch: trumps and ranks exactly as in Wenz.\n\nTRICKS. 1) The leader plays any card from their hand. In the first trick of a hand the leader is the declarer, or the priority player in Ramsch. Afterwards the leader is the winner of the previous trick. 2) The other player then plays a card. If a trump was led, they must play a trump if they have one. If a plain suit was led, they must play a non-trump card of that suit if they have one. Otherwise they may play any card. You are offered only the cards you may legally play. 3) The trick is won by the highest trump in it. If it has no trump, it is won by the higher card of the led suit (a card of another suit never wins). 4) The trick winner adds the card points of both cards to their card-point total for the hand, and leads next. 5) The two cards, the trick winner and both players' card-point totals for the hand are announced.\n\nEND OF EACH HAND (after the 8th trick). Let D be the declarer's card points and F the defender's card points. A Simple contract is made if D >= F + {simple_margin}; otherwise it fails. A Strong contract is made if D >= {strong_multiplier} x F and D >= {strong_minimum_points}; otherwise it fails. Stake: Simple is {simple_stake} match points and Strong is {strong_stake} match points. The stake is multiplied by {double_factor} if the defender chose Double (Simple 4, Strong 8), and unchanged if not. If the contract is made, the declarer gains the stake. Otherwise the defender gains the stake. Ramsch: the player with fewer card points gains {ramsch_award} match point. If the card points are equal, nobody scores. Card-point totals reset to 0 and the next hand begins.\n\nEND. After the fourth hand the match ends. The player with more match points wins. Equal match points is a draw (the win is shared)."
}
```
````
