# 16 coder

- time: 2026-10-28T05:49:34+00:00 (204.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 7a956655f74006cd, reply sha256 74ebd20710bb0705

## Sent

````
# Task: write the XColos game file for "Simultaneous Yaniv: Claims"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

CARDS. Card values: Ace = 1, 2 to 10 = face value, Jack/Queen/King = 10, Joker = 0. Suits do not matter. Every card comes from a shoe with the frequencies of a 54-card deck, reshuffled before every draw:
- each value from 1 to 9: 4 in 54;
- value 10: 16 in 54;
- value 0: 2 in 54.

SETUP. Before round 1, each player is dealt 5 cards. Each player sees only their own hand. Everyone sees every player's hand size and running total, which starts at 0.

EACH ROUND:
(1) PUBLIC ANNOUNCEMENT. The round number, every player's hand size and total, and the previous round's public results (discards, claims, who took BLIND) are announced.
(2) PRIVATE VIEW. Each player is privately shown their hand and its sum.
(3) FIRST CHOICE, simultaneous. Each player secretly chooses exactly one of:
- CALL, allowed only if their hand sum is 7 or less;
- DISCARD one card;
- DISCARD two or more cards of equal value;
- DISCARD a RUN of three or more cards with consecutive values. Ace counts as 1. Jokers cannot be in a run. A run may contain at most one card of value 10, so 8-9-10 is allowed but 9-10-10 is not.
A player must keep at least 1 card after discarding, so a player holding 1 card may not discard it and must CALL if allowed. If not allowed to call, that player discards nothing this round and still draws one card in step 9. Any illegal answer is replaced by discarding the single highest card (or by discarding nothing, for a player with 1 card).
(4) SHOWDOWN, only if at least one player called. All discards are cancelled and all hands are revealed as they stood. Let L be the lowest hand sum.
- A caller whose sum is strictly lower than every other player's sum scores 0.
- Any other caller is caught (Asaf) and scores their hand sum + 30.
- A non-caller whose sum equals L scores 0.
- Every other non-caller scores their hand sum.
Scores are added to totals. If no total is 150 or more and this is not round 40, every player is dealt a fresh hand of 5 cards. This re-deal is this round's only random draw. Steps 5 to 10 are skipped this round.
(5) OFFERS, only if no one called. Every player's discard is announced publicly: who discarded which values. The discarded cards leave play. Each player's discard creates an OFFER:
- a single card or an equal-value set offers one card of that value;
- a run offers two cards, its lowest and its highest value.
(6) SECOND CHOICE, simultaneous, only if no one called. Each player secretly chooses either BLIND, or to CLAIM one specific offered card belonging to another player. A player may not claim from their own offer. A player who discarded nothing still makes this choice. An illegal answer becomes BLIND.
(7) CONTESTS. If two or more players claim the same offered card, none of them receives it, and each of them is treated as having chosen BLIND. A card claimed by exactly one player goes to that player.
(8) BLIND DRAW, only if no one called. One card is drawn from the shoe. This is this round's only random draw.
(9) DELIVERY. Each successful claimant adds the claimed card to their hand. Each BLIND player adds a copy of the blind card to their hand and is privately told its value. The blind card's value is not told to anyone else until a showdown.
(10) PUBLIC RESULT. It is announced who claimed which card, which claims failed through contest, and who took BLIND. The blind card's value is not announced.
(11) FINAL SHOWDOWN. If this is round 40 and no showdown happened this round, all hands are revealed. Every player whose hand sum equals the lowest hand sum scores 0, and every other player scores their hand sum. There are no callers and no Asaf.
(12) END CHECK. The game ends if any total is 150 or more after a showdown, or after round 40.

How the winner is decided: When the game ends, the player with the strictly lowest total wins. If two or more players tie for the lowest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Simultaneous Yaniv: Claims (3 to 5 players, best with 4)

Low-hand card game played in simultaneous turns: each round players secretly call or discard, then secretly claim another player's discarded card or take a shared blind draw. A caller who is not strictly lowest is caught (Asaf) for +30, and the lowest total when someone reaches 150 or after 40 rounds wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Card values the player holds (0 to 10). Revealed to all at a showdown.
  - each player: hand_sum (number, starts 0); only its owner sees it. Sum of the values in hand.
  - each player: hand_size (number, starts 0); everyone sees it. Number of cards in hand.
  - each player: total (number, starts 0); everyone sees it. Running score. Lower is better.
  - each player: round_score (number, starts 0); everyone sees it. Points scored at the latest showdown.
  - each player: first_choice (text, starts ''); only its owner sees it. This round's secret first choice: CALL, a list of discarded values, or NONE.
  - each player: called (bool, starts False); everyone sees it. Whether the player called this round. Revealed at the showdown.
  - each player: discard (list, starts []); everyone sees it. Values discarded this round. Announced at the offers step.
  - each player: claim (text, starts ''); everyone sees it. This round's second choice: BLIND or an offer id. Made secretly and announced in the public result.
  - each player: claim_failed (bool, starts False); everyone sees it. Whether this round's claim was lost to a contest.
  - each player: took_blind (bool, starts False); everyone sees it. Whether the player received the blind card this round.
  - the table: shoe (list, starts '[0,0, 1x4, 2x4, 3x4, 4x4, 5x4, 6x4, 7x4, 8x4, 9x4, 10x16] (54 values)'); hidden from all players. Card source. Every draw picks a value at random and does not remove it (reshuffled before every draw).
  - the table: round (number, starts 1); everyone sees it. Current round number.
  - the table: called_count (number, starts 0); everyone sees it. Number of players who called this round.
  - the table: lowest_sum (number, starts 0); everyone sees it. L, the lowest hand sum at a showdown.
  - the table: offers (list, starts []); everyone sees it. Offered cards this round, each 'seat S: value V'.
  - the table: blind_card (number, starts 0); hidden from all players. Value of this round's blind card. Each BLIND player gets a copy and is told the value privately.
  - the table: last_results (text, starts ''); everyone sees it. Previous round's public results: discards, claims, failed claims, BLIND takers, or the showdown outcome.
  - parameters, each kept as a table attribute: hand_size_start = 5, call_limit = 7, asaf_penalty = 30, end_total = 150, max_rounds = 40, min_set_size = 2, min_run_length = 3, max_tens_in_run = 1, min_cards_kept = 1, shoe_size = 54, copies_per_value_1_to_9 = 4, copies_value_10 = 16, copies_value_0 = 2, run_offer_cards = 2, set_or_single_offer_cards = 1, contest_threshold = 2, blind_draws_per_round = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's total is set to 0 and round is set to 1.
  2. The shoe holds 54 values: two 0s, four each of 1 to 9, and sixteen 10s.
  3. Each player is dealt 5 cards. Each card is a value drawn at random from the shoe without removing it, appended to that player's hand.
  4. Each player's hand_sum and hand_size are computed. hand_size is public and the hand is private.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [tell] all players. What happens: Announce round, every player's hand_size and total, and last_results.
  2. [sync] all players. What happens: Each player privately sees their own hand and hand_sum.
  3. [poll] all players answers: CALL, or the list of card values from own hand to discard (one card, two or more equal values, or a run of 3 or more consecutive values). A 1-card player with hand_sum <= 7 is offered only CALL. A 1-card player with hand_sum > 7 is offered only NONE.. What happens: first_choice := the answer.
  4. [update] all players. What happens: Any illegal first_choice is replaced: a player with hand_size >= 2 discards their single highest card; a player with hand_size 1 discards nothing (NONE). Then called := (first_choice == CALL), and called_count := the number of players with called true. JUDGED: a referee rules true or false on "This player's first choice is legal: CALL with hand_sum at most 7; or values all held in their hand that form a single card, two or more cards of equal value, or a run of three or more consecutive values with no 0 and at most one 10; and at least one card is left in hand."; write this step's `when` as {"prose": that sentence, verbatim}.
  5. [update] all players. What happens: When called_count >= 1 (showdown): all discards are cancelled and lowest_sum := the minimum hand_sum. For each player: if called and hand_sum == lowest_sum and the count of players with hand_sum == lowest_sum is 1, round_score := 0; else if called, round_score := hand_sum + 30; else if hand_sum == lowest_sum, round_score := 0; else round_score := hand_sum. total += round_score. last_results records the revealed hands, the callers and the scores.
  6. [tell] all players. What happens: When called_count >= 1: reveal every hand, hand_sum, called, round_score and total.
  7. [check] all players. What happens: When called_count >= 1: end the game if any total >= 150 or round == 40.
  8. [update] all players. What happens: When called_count >= 1 and round < 40: each hand is cleared and gets 5 random draws from the shoe (without removal). hand_sum and hand_size are recomputed.
  9. [update] all players. What happens: When called_count == 0: discard := the discarded values, which are removed from hand; hand_sum and hand_size are recomputed. offers := for each player who discarded one card or an equal-value set, one entry 'seat S: value V'; for each player who discarded a run, two entries, its lowest and its highest value. A player who discarded nothing makes no offer.
  10. [tell] all players. What happens: When called_count == 0: announce every player's discard and the offers list.
  11. [poll] all players answers: BLIND, or one entry of offers that belongs to another seat.. What happens: When called_count == 0: claim := the answer. An illegal answer becomes BLIND.
  12. [update] all players. What happens: When called_count == 0 (contests): for each offer entry claimed by 2 or more players, each of those players gets claim_failed := true and claim := BLIND. took_blind := (claim == BLIND).
  13. [update] all players. What happens: When called_count == 0: blind_card := one value drawn at random from the shoe (without removal). Each player whose claim is an offer appends that offer's value to hand. Each player with took_blind appends blind_card to hand. hand_sum and hand_size are recomputed.
  14. [tell] each player with took_blind true. What happens: When called_count == 0: privately tell the player the value of blind_card.
  15. [update] all players. What happens: When called_count == 0: last_results := who claimed which card, which claims failed through contest, and who took BLIND. The blind_card value is not included.
  16. [tell] all players. What happens: When called_count == 0: announce last_results.
  17. [update] all players. What happens: When round == 40 and called_count == 0 (final showdown): lowest_sum := the minimum hand_sum. Each player gets round_score := 0 if hand_sum == lowest_sum, else round_score := hand_sum. total += round_score.
  18. [tell] all players. What happens: When round == 40 and called_count == 0: reveal every hand, hand_sum, round_score and total.
  19. [update] all players. What happens: Reset called, discard, claim, claim_failed, took_blind and offers. round += 1.
  20. [check] all players. What happens: End the game if any total >= 150 or round > 40.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Card values: Ace = 1, 2 to 10 = face value, J/Q/K = 10, Joker = 0. Every draw is a random value from a 54-card shoe (two 0s, four each of 1 to 9, sixteen 10s), reshuffled before each draw.
  R2. Before round 1, each player is dealt 5 cards and every total is 0.
  R3. When a player's hand_sum is 7 or less, then CALL is a legal first choice; when it is 8 or more, CALL is illegal.
  R4. When a player discards, then the discard is exactly one card, two or more cards of equal value, or a run of 3 or more consecutive values.
  R5. When a run contains a 0 or more than one 10, then it is illegal; 8-9-10 is legal and 9-10-10 is not.
  R6. When a discard would leave 0 cards in hand, then it is illegal.
  R7. When a player holds 1 card and hand_sum <= 7, then that player must CALL; when they hold 1 card and hand_sum > 7, then they discard nothing and still make the second choice.
  R8. When a first choice is illegal, then it is replaced by discarding the single highest card, or by discarding nothing for a player with 1 card.
  R9. When at least one player calls, then all discards are cancelled and a showdown is held on the hands as they stood.
  R10. At a showdown, when a caller's hand_sum is strictly lower than every other player's, then that caller scores 0.
  R11. At a showdown, when a caller is not strictly lowest, then the caller is caught (Asaf) and scores hand_sum + 30 (a caller with sum 6 tied at 6 scores 36).
  R12. At a showdown, when a non-caller's hand_sum equals the lowest sum L, then they score 0; otherwise they score their hand_sum.
  R13. After a showdown, when no total is 150 or more and the round is not 40, then every player is dealt a fresh hand of 5 cards, and steps 5 to 10 are skipped.
  R14. When no one calls, then every discard is announced publicly and leaves play.
  R15. When a single card or an equal-value set is discarded, then it makes one offer of that value; when a run is discarded, then it makes two offers, its lowest and its highest value.
  R16. When no one calls, then each player chooses BLIND or a claim on one offered card of another player; claiming one's own offer is illegal and becomes BLIND.
  R17. When two or more players claim the same offered card, then none of them receives it and each is treated as BLIND.
  R18. When exactly one player claims an offered card, then that card is added to that player's hand.
  R19. When no one calls, then one blind card is drawn, and each BLIND player adds a copy of it to their hand and is privately told its value.
  R20. When the public result is announced, then it names who claimed which card, which claims failed through contest, and who took BLIND, but not the blind card's value.
  R21. When round 40 ends with no showdown that round, then all hands are revealed, each player at the lowest sum scores 0 and every other player scores their hand_sum.
  R22. When any total is 150 or more after a showdown, or round 40 is over, then the game ends.
  R23. When the game ends, then the player with the strictly lowest total wins; when two or more tie for lowest, then the game is a draw (shared result).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First choice (step 3) | asked: all players | options: A player with 2 or more cards and hand_sum <= 7: CALL, or any legal discard from their hand (one card, an equal-value set of 2 or more, or a run of 3 or more consecutive values with no 0 and at most one 10), keeping at least 1 card. A player with 2 or more cards and hand_sum > 7: any such legal discard only. A player with 1 card and hand_sum <= 7: CALL only. A player with 1 card and hand_sum > 7: NONE only.
  - Second choice (step 6) | asked: all players, including those who discarded nothing | options: BLIND, or any entry of offers that belongs to a seat other than their own.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: any player's total >= 150 after a showdown, or round > 40 (after round 40 is played)
  - each player's standing: -you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with the lowest total wins. Players level at the lowest total share the result (the source calls this a draw).
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

- each player: `hand_size` (number, visible: public, starts 0): Number of cards in hand.
- each player: `total` (number, visible: public, starts 0): Running score. Lower is better.
- each player: `round_score` (number, visible: public, starts 0): Points scored at the latest showdown.
- the table: `round` (number, visible: public, starts 1): Current round number.
- parameters (each must be an attribute holding this value, never a number buried in a step): hand_size_start = 5, call_limit = 7, asaf_penalty = 30, end_total = 150, max_rounds = 40, min_set_size = 2, min_run_length = 3, max_tens_in_run = 1, min_cards_kept = 1, shoe_size = 54, copies_per_value_1_to_9 = 4, copies_value_10 = 16, copies_value_0 = 2, run_offer_cards = 2, set_or_single_offer_cards = 1, contest_threshold = 2, blind_draws_per_round = 1
- the game ends with ONE ending whose `rank_by` is `-you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Move the initial 5-card deal (hand, hand_sum, hand_size) out of the round step list and into setup, so it happens once before round 1 and is not repeated in round 1. A state the tests inject before round 1 must survive into the first choice. Inside rounds, re-deal only in the showdown branch, guarded by the conditions called_count >= 1, no total >= end_total and round < max_rounds. Also recheck the first-choice options and fallbacks: offer CALL when hand_sum <= call_limit. With 1 card, the only options are CALL or nothing. Never offer a discard that would leave fewer than min_cards_kept cards; for a [4,4] hand, offer 'discard 4' but not 'discard 4 x2'. Runs must have no 0 and at most max_tens_in_run 10s. An illegal answer falls back to discarding the single highest card. Keep every parameter as an attribute.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "simultaneous_yaniv_claims",
    "name": "Simultaneous Yaniv: Claims",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Secretly call or discard, then claim another player's discard or take the shared blind card; a caught caller pays Asaf, and the lowest total wins."
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
        "key": "hand_sum",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "called",
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
        "key": "claim",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "claim_failed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "took_blind",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "first_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "claim_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "claim_try",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "result_line",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_blind",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "shoe",
        "visible": "none",
        "type": "list",
        "initial": [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "called_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lowest_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offers",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "blind_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_results",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "all_values",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      },
      {
        "key": "value_names",
        "visible": "none",
        "type": "list",
        "initial": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
      },
      {
        "key": "idx",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
      },
      {
        "key": "hand_size_start",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "call_limit",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "asaf_penalty",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "end_total",
        "visible": "public",
        "type": "number",
        "initial": 150
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "min_set_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "min_run_length",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_tens_in_run",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_cards_kept",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "shoe_size",
        "visible": "public",
        "type": "number",
        "initial": 54
      },
      {
        "key": "copies_per_value_1_to_9",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "copies_value_10",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "copies_value_0",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "run_offer_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "set_or_single_offer_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "contest_threshold",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "blind_draws_per_round",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "totals and round",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "fill the shoe",
      "do": [
        {
          "set": {
            "key": "shoe",
            "value": {
              "calc": "[0 for j in idx if j < copies_value_0] + [v for v in all_values if v >= 1 and v <= 9 for j in idx if j < copies_per_value_1_to_9] + [10 for j in idx if j < copies_value_10]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)] for j in idx if j < hand_size_start]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "count the hands",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "tell",
      "phase": "announce",
      "label": "public announcement",
      "to": "all",
      "text": "Round {round} of {max_rounds}. Cards in hand and totals [seat, cards, total]: {[[p.seat, p.hand_size, p.total] for p in players]}. Previous round: {last_results}"
    },
    {
      "use": "sync",
      "phase": "announce",
      "label": "private view",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "hand_sum"
      ],
      "text": "Your hand and its sum:"
    },
    {
      "use": "update",
      "phase": "first choice",
      "label": "legal first choices",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "first_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "first_offer",
            "value": {
              "calc": "(['CALL'] if you.hand_sum <= call_limit else []) + (['NONE'] if you.hand_size <= min_cards_kept and you.hand_sum > call_limit else []) + ['discard ' + value_names[v] for v in all_values if v in you.hand and you.hand_size > min_cards_kept] + ['discard ' + value_names[v] + ' x' + value_names[k] for v in all_values for k in all_values if k >= min_set_size and k <= count(x == v for x in you.hand) and k <= you.hand_size - min_cards_kept] + ['run ' + value_names[s] + '-' + value_names[e] for s in all_values for e in all_values if s >= 1 and e - s + 1 >= min_run_length and e - s + 1 <= you.hand_size - min_cards_kept and (1 if e == 10 else 0) <= max_tens_in_run and all(w in you.hand for w in all_values if w >= s and w <= e)]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "first choice",
      "label": "first choice",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "first_offer"
        }
      },
      "store": "first_choice",
      "text": "Choose in secret: CALL (only if your hand sum is {call_limit} or less), or a discard: 'discard V' is one card of value V, 'discard V xK' is K cards of value V, 'run S-E' is one card of each value from S to E. You always keep at least {min_cards_kept} card. NONE means you discard nothing."
    },
    {
      "use": "update",
      "phase": "first choice",
      "label": "settle the first choices",
      "when": {
        "prose": "This player's first choice is legal: CALL with hand_sum at most 7; or values all held in their hand that form a single card, two or more cards of equal value, or a run of three or more consecutive values with no 0 and at most one 10; and at least one card is left in hand."
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.first_choice not in you.first_offer and you.hand_size > min_cards_kept"
            },
            "key": "first_choice",
            "value": {
              "calc": "'discard ' + value_names[max(you.hand)]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.first_choice not in you.first_offer and you.hand_size <= min_cards_kept"
            },
            "key": "first_choice",
            "value": "NONE"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": {
              "calc": "you.first_choice == 'CALL'"
            }
          }
        },
        {
          "set": {
            "key": "called_count",
            "value": {
              "calc": "count(p.first_choice == 'CALL' for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "showdown",
      "when": {
        "calc": "count(p.first_choice == 'CALL' for p in players) >= 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": {
              "calc": "you.first_choice == 'CALL'"
            }
          }
        },
        {
          "set": {
            "key": "called_count",
            "value": {
              "calc": "count(p.first_choice == 'CALL' for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "discard",
            "value": []
          }
        },
        {
          "set": {
            "key": "lowest_sum",
            "value": {
              "calc": "min([p.hand_sum for p in players])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "round_score",
            "value": {
              "calc": "0 if (you.called and you.hand_sum == lowest_sum and count(p.hand_sum == lowest_sum for p in players) == 1) else (you.hand_sum + asaf_penalty if you.called else (0 if you.hand_sum == lowest_sum else you.hand_sum))"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.round_score"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "[[p.seat, p.hand, p.hand_sum, p.called, p.round_score, p.total] for p in players]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "result_line",
            "value": {
              "calc": "'Seat ' + value_names[you.seat] + (' called and was strictly lowest, scoring 0' if (you.called and you.round_score == 0) else (' called and was caught (Asaf)' if you.called else (' did not call and was at the lowest sum, scoring 0' if you.round_score == 0 else ' did not call and scored their hand sum'))) + '. '"
            }
          }
        },
        {
          "set": {
            "key": "last_results",
            "value": {
              "calc": "'Showdown: ' + max([p.result_line for p in players if p.seat == 1] + ['']) + max([p.result_line for p in players if p.seat == 2] + ['']) + max([p.result_line for p in players if p.seat == 3] + ['']) + max([p.result_line for p in players if p.seat == 4] + ['']) + max([p.result_line for p in players if p.seat == 5] + [''])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "showdown",
      "label": "showdown reveal",
      "when": {
        "calc": "called_count >= 1"
      },
      "to": "all",
      "text": "Showdown! Discards are cancelled. Lowest hand sum: {lowest_sum}. Revealed [seat, hand, hand sum, called, round score, total]: {revealed}. {last_results}"
    },
    {
      "use": "check",
      "phase": "showdown",
      "label": "after the showdown",
      "when": {
        "calc": "called_count >= 1 and any(p.total >= end_total for p in players)"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "fresh hands",
      "when": {
        "calc": "called_count >= 1 and round < max_rounds and not any(p.total >= end_total for p in players)"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)] for j in idx if j < hand_size_start]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        }
      ],
      "text": "Every player is dealt a fresh hand of {hand_size_start} cards."
    },
    {
      "use": "update",
      "phase": "offers",
      "label": "discards and offers",
      "when": {
        "calc": "count(p.first_choice == 'CALL' for p in players) == 0"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": false
          }
        },
        {
          "set": {
            "key": "called_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "discard",
            "value": {
              "calc": "[v for v in all_values if you.first_choice == 'discard ' + value_names[v]] + [v for v in all_values for k in all_values for j in all_values if j < k and you.first_choice == 'discard ' + value_names[v] + ' x' + value_names[k]] + [w for s in all_values for e in all_values for w in all_values if w >= s and w <= e and you.first_choice == 'run ' + value_names[s] + '-' + value_names[e]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[v for v in all_values for j in idx if j < count(x == v for x in you.hand) - count(y == v for y in you.discard)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "offers",
            "value": {
              "calc": "['seat ' + value_names[p.seat] + ': value ' + value_names[v] for p in players if len(p.discard) > 0 for v in ([min(p.discard)] if min(p.discard) == max(p.discard) else [min(p.discard), max(p.discard)])]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_offer",
            "value": {
              "calc": "['BLIND'] + [o for o in offers if o not in ['seat ' + value_names[you.seat] + ': value ' + value_names[v] for v in all_values]]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "offers",
      "label": "announce the offers",
      "when": {
        "calc": "called_count == 0"
      },
      "to": "all",
      "text": "No one called. Discards [seat, values]: {[[p.seat, p.discard] for p in players]}. The discarded cards leave play. Offers: {offers}."
    },
    {
      "use": "poll",
      "phase": "claims",
      "label": "second choice",
      "when": {
        "calc": "called_count == 0"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "claim_offer"
        }
      },
      "store": "claim",
      "text": "Choose in secret: BLIND (take a copy of the blind card), or claim one offered card from another player. If two or more players claim the same card, none of them gets it and each takes BLIND instead."
    },
    {
      "use": "update",
      "phase": "claims",
      "label": "contests and delivery",
      "when": {
        "calc": "called_count == 0"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "claim_try",
            "value": {
              "calc": "you.claim"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_failed",
            "value": {
              "calc": "you.claim != 'BLIND' and count(p.claim == you.claim for p in players) >= contest_threshold"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.claim_failed"
            },
            "key": "claim",
            "value": "BLIND"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "took_blind",
            "value": {
              "calc": "you.claim == 'BLIND'"
            }
          }
        },
        {
          "set": {
            "key": "blind_card",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.claim != 'BLIND'"
            },
            "key": "hand",
            "value": {
              "calc": "sum([v for v in all_values for s in all_values if you.claim == 'seat ' + value_names[s] + ': value ' + value_names[v]])"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.took_blind"
            },
            "key": "hand",
            "value": {
              "calc": "blind_card"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.took_blind"
            },
            "key": "last_blind",
            "value": {
              "calc": "blind_card"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "claims",
      "label": "the blind card",
      "when": {
        "calc": "called_count == 0"
      },
      "to": {
        "where": "you.took_blind"
      },
      "text": "You took BLIND. The blind card added to your hand is {last_blind}."
    },
    {
      "use": "update",
      "phase": "claims",
      "label": "record the results",
      "when": {
        "calc": "called_count == 0"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "result_line",
            "value": {
              "calc": "'Seat ' + value_names[you.seat] + ': ' + (you.first_choice if len(you.discard) > 0 else 'no discard') + ', ' + (('took BLIND' + (' (claim on ' + you.claim_try + ' failed: contested)' if you.claim_failed else '')) if you.took_blind else ('claimed ' + you.claim)) + '. '"
            }
          }
        },
        {
          "set": {
            "key": "last_results",
            "value": {
              "calc": "max([p.result_line for p in players if p.seat == 1] + ['']) + max([p.result_line for p in players if p.seat == 2] + ['']) + max([p.result_line for p in players if p.seat == 3] + ['']) + max([p.result_line for p in players if p.seat == 4] + ['']) + max([p.result_line for p in players if p.seat == 5] + [''])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "claims",
      "label": "public result",
      "when": {
        "calc": "called_count == 0"
      },
      "to": "all",
      "text": "Result: {last_results}"
    },
    {
      "use": "update",
      "phase": "final",
      "label": "final showdown",
      "when": {
        "calc": "round == max_rounds and called_count == 0"
      },
      "do": [
        {
          "set": {
            "key": "lowest_sum",
            "value": {
              "calc": "min([p.hand_sum for p in players])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "round_score",
            "value": {
              "calc": "0 if you.hand_sum == lowest_sum else you.hand_sum"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.round_score"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "[[p.seat, p.hand, p.hand_sum, p.round_score, p.total] for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "final",
      "label": "final reveal",
      "when": {
        "calc": "round == max_rounds and called_count == 0"
      },
      "to": "all",
      "text": "Final showdown after round {round}. Lowest hand sum: {lowest_sum}. Revealed [seat, hand, hand sum, round score, total]: {revealed}."
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "reset",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "discard",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_failed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "took_blind",
            "value": false
          }
        },
        {
          "set": {
            "key": "offers",
            "value": []
          }
        },
        {
          "set": {
            "key": "called_count",
            "value": 0
          }
        },
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end of round",
      "label": "end check",
      "when": {
        "calc": "any(p.total >= end_total for p in players) or round > max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "any(p.total >= end_total for p in players) or round > max_rounds"
      },
      "rank_by": "-you.total",
      "text": "Winner: {result} (lowest total). Final totals [seat, total]: {[[p.seat, p.total] for p in players]}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 41,
    "actions_max": 4000,
    "deadline_s": 120
  },
  "rules": "CARDS. Ace = 1, 2 to 10 = face value, Jack/Queen/King = 10, Joker = 0. Suits do not matter. Every card comes from a shoe with the frequencies of a {shoe_size}-card deck, reshuffled before every draw: each value from 1 to 9: {copies_per_value_1_to_9} in {shoe_size}; value 10: {copies_value_10} in {shoe_size}; value 0: {copies_value_0} in {shoe_size}.\n\nSETUP. Before round 1, each player is dealt {hand_size_start} cards. Each player sees only their own hand. Everyone sees every player's hand size and running total, which starts at 0.\n\nEACH ROUND:\n(1) PUBLIC ANNOUNCEMENT. The round number, every player's hand size and total, and the previous round's public results (discards, claims, who took BLIND) are announced.\n(2) PRIVATE VIEW. Each player is privately shown their hand and its sum.\n(3) FIRST CHOICE, simultaneous. Each player secretly chooses exactly one of: CALL, allowed only if their hand sum is {call_limit} or less (with a sum of 8 or more, CALL is not allowed); DISCARD one card; DISCARD {min_set_size} or more cards of equal value; DISCARD a RUN of {min_run_length} or more cards with consecutive values. Ace counts as 1. Jokers cannot be in a run. A run may contain at most {max_tens_in_run} card of value 10, so 8-9-10 is allowed but 9-10-10 is not. A player must keep at least {min_cards_kept} card after discarding, so a player holding 1 card may not discard it and must CALL if allowed. If not allowed to call, that player discards nothing this round (NONE) and still makes the second choice and draws a card. Any illegal answer is replaced by discarding the single highest card (or by discarding nothing, for a player with 1 card). You are only offered legal choices: 'discard V' is one card of value V, 'discard V xK' is K cards of value V, 'run S-E' is one card of each value from S to E.\n(4) SHOWDOWN, only if at least one player called. All discards are cancelled and all hands are revealed as they stood. Let L be the lowest hand sum. A caller whose sum is strictly lower than every other player's sum scores 0. Any other caller is caught (Asaf) and scores their hand sum + {asaf_penalty} (a caller with sum 6 tied at 6 scores 36). A non-caller whose sum equals L scores 0. Every other non-caller scores their hand sum. Scores are added to totals. If no total is {end_total} or more and this is not round {max_rounds}, every player is dealt a fresh hand of {hand_size_start} cards; this re-deal is the round's only random draw. Steps 5 to 10 are skipped this round. If no one calls, there is no showdown and the round continues with step 5.\n(5) OFFERS, only if no one called. Every player's discard is announced publicly: who discarded which values. The discarded cards leave play. Each player's discard creates an OFFER: a single card or an equal-value set offers {set_or_single_offer_cards} card of that value; a run offers {run_offer_cards} cards, its lowest and its highest value. A player who discarded nothing makes no offer.\n(6) SECOND CHOICE, simultaneous, only if no one called. Each player secretly chooses either BLIND, or to CLAIM one specific offered card belonging to another player. A player may not claim from their own offer. A player who discarded nothing still makes this choice. An illegal answer becomes BLIND.\n(7) CONTESTS. If {contest_threshold} or more players claim the same offered card, none of them receives it, and each of them is treated as having chosen BLIND. A card claimed by exactly one player goes to that player.\n(8) BLIND DRAW, only if no one called. One card is drawn from the shoe. This is the round's only random draw.\n(9) DELIVERY. Each successful claimant adds the claimed card to their hand. Each BLIND player adds a copy of the blind card to their hand and is privately told its value. The blind card's value is not told to anyone else until a showdown.\n(10) PUBLIC RESULT. It is announced who claimed which card, which claims failed through contest, and who took BLIND. The blind card's value is not announced.\n(11) FINAL SHOWDOWN. If this is round {max_rounds} and no showdown happened this round, all hands are revealed. Every player whose hand sum equals the lowest hand sum scores 0, and every other player scores their hand sum. There are no callers and no Asaf.\n(12) END CHECK. The game ends if any total is {end_total} or more after a showdown, or after round {max_rounds}; otherwise the next round begins.\n\nWINNING. When the game ends, the player with the strictly lowest total wins. If two or more players tie for the lowest total, the game is a draw: they share the result."
}
```
````
