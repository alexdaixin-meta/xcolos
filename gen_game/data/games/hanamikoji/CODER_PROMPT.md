# Task: write the XColos game file for "Hanamikoji: Five Geisha"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

COMPONENTS.
- There are 5 Geisha, numbered 1 to 5, with Charm 3, 3, 4, 5, 6.
- There are 21 Item cards. Each card shows a Geisha number: three 1s, three 2s, four 3s, five 4s and six 5s.
- Each Geisha has a marker. Each marker is on Player 1's side, Player 2's side, or in the middle. All markers start in the middle.

PLAYER STATE.
- hand: private cards.
- secret: 0 or 1 face-down card.
- unused_actions: a list.
- kept: the cards placed on the player's side, visible to both.
- charm.
- geisha_count.
- standing.

GAME STATE.
- deck, removed_card, discard (hidden).
- hand_number (1–4), round_in_hand (1–8), starting_seat.
- marker_1 to marker_5.

ACTION NAMES.
The four actions are spelled exactly: Secret, Trade-off, Gift, Competition.

STRUCTURE.
The game is 4 hands of 8 rounds, 32 rounds in total. Hands 1 and 2 form Pair 1; hands 3 and 4 form Pair 2. Player 1 is the starting seat in hands 1 and 3; Player 2 is the starting seat in hands 2 and 4.

START OF A HAND (round_in_hand = 1, before anything else).
1. Shuffle all 21 Items and set 1 aside face-down as removed_card. Nobody sees it.
2. Deal 6 cards privately to each player. The remaining 8 cards form the deck.
3. Empty both secrets. Empty the discard.
4. Set both players' unused_actions to [Secret, Trade-off, Gift, Competition].
5. If this is hand 1 or hand 3, empty both players' kept lists. In hands 2 and 4, kept lists carry over unchanged. Markers always carry over.

EACH ROUND (one turn).
1. The active player is the starting seat in odd rounds (1, 3, 5, 7) and the other player in even rounds (2, 4, 6, 8). Each player therefore takes 4 turns per hand.
2. The active player draws the top card of the deck into their hand.
3. The active player chooses one action. The options offered are exactly the actions currently in their unused_actions list. The list is never rebuilt from the round number.
4. That action is removed from their unused_actions list.
5. The active player names the hand cards the action uses, by Geisha number, from cards they actually hold.
6. The action is resolved:
   - Secret: move 1 hand card face-down to the player's secret.
   - Trade-off: move 2 hand cards face-down to the discard. They are out of play for this hand.
   - Gift: reveal 3 hand cards. The opponent chooses 1 of them, and it goes to the opponent's kept. The other 2 go to the active player's kept.
   - Competition: reveal 4 hand cards split into Pair A (2 cards) and Pair B (2 cards). The opponent chooses Pair A or Pair B, and it goes to the opponent's kept. The other pair goes to the active player's kept.

CARD BUDGET.
Each player holds 6 cards and draws 4 per hand, 10 in total. The actions use exactly 1+2+3+4 = 10 cards, so the chosen action is always affordable. In round 8 the active player has exactly one action left, which may be Trade-off, and must take it.

END OF A HAND (after round 8).
Each player's secret card is revealed and appended to their kept list.

END OF A PAIR (after hands 2 and 4 only, after the step above). Run these steps in this order:
(a) For each Geisha g, count the cards of number g in each player's kept. If one player's count is strictly higher, marker_g moves to that player's side. On a tie the marker stays where it is.
(b) For each player, charm is the total Charm of the Geisha whose markers are on their side, and geisha_count is the number of markers on their side. standing = charm.
(c) Win check:
   - A player with charm 11 or more wins.
   - Otherwise, a player with geisha_count 3 or more wins.
   - Both players cannot reach the same goal. If one reaches 11 charm and the other reaches 3 Geisha, the 11-charm player wins.
   - If someone wins, the game ends.

AFTER HAND 4.
If no one has won, the player with the higher charm wins. If charm is tied, the player with the higher geisha_count wins. Otherwise the game is a draw.

How the winner is decided: The win check runs at the end of each pair, after hand 2 and after hand 4. A player whose markers total 11 or more Charm wins. Otherwise, a player holding 3 or more markers wins; if one player has 11 Charm and the other has 3 markers, the 11-Charm player wins. If no one has won after hand 4, the higher Charm wins, then the higher Geisha count; otherwise the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hanamikoji: Five Geisha (2 to 2 players, best with 2)

Two players each take four one-shot actions per hand to place Item cards for five Geisha, aiming for 11 Charm or 3 Geisha at the end of each pair of hands.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Item cards held privately, each a Geisha number 1-5
  - each player: secret (list, starts []); only its owner sees it. 0 or 1 face-down card set aside by Secret this hand
  - each player: pending (list, starts []); only its owner sees it. cards picked from hand for the current action, in pick order (picks 1-2 are Pair A and picks 3-4 are Pair B in Competition)
  - each player: unused_actions (list, starts ['Secret', 'Trade-off', 'Gift', 'Competition']); everyone sees it. actions not yet taken this hand
  - each player: kept (list, starts []); everyone sees it. cards placed on this player's side, visible to both
  - each player: charm (number, starts 0); everyone sees it. total Charm of Geisha whose markers are on this player's side
  - each player: geisha_count (number, starts 0); everyone sees it. number of markers on this player's side
  - each player: standing (number, starts 0); everyone sees it. equals charm; the score
  - the table: deck (list, starts []); hidden from all players. undealt Item cards this hand
  - the table: removed_card (list, starts []); hidden from all players. the 1 card set aside face-down each hand
  - the table: discard (list, starts []); hidden from all players. Trade-off cards, out of play this hand
  - the table: hand_number (number, starts 1); everyone sees it. current hand, 1-4
  - the table: round_in_hand (number, starts 1); everyone sees it. current round within the hand, 1-8
  - the table: starting_seat (number, starts 1); everyone sees it. seat that acts in odd rounds: 1 in hands 1 and 3, 2 in hands 2 and 4
  - the table: active_seat (number, starts 1); everyone sees it. seat taking this round's turn
  - the table: last_action (text, starts ''); everyone sees it. action chosen this round
  - the table: marker_1 (number, starts 0); everyone sees it. Geisha 1 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
  - the table: marker_2 (number, starts 0); everyone sees it. Geisha 2 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
  - the table: marker_3 (number, starts 0); everyone sees it. Geisha 3 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
  - the table: marker_4 (number, starts 0); everyone sees it. Geisha 4 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
  - the table: marker_5 (number, starts 0); everyone sees it. Geisha 5 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
  - the table: game_over (number, starts 0); everyone sees it. 1 once a player has won at a pair end, or hand 4 is complete
  - parameters, each kept as a table attribute: geisha_count_total = 5, charm_geisha_1 = 3, charm_geisha_2 = 3, charm_geisha_3 = 4, charm_geisha_4 = 5, charm_geisha_5 = 6, items_total = 21, items_geisha_1 = 3, items_geisha_2 = 3, items_geisha_3 = 4, items_geisha_4 = 5, items_geisha_5 = 6, removed_per_hand = 1, deal_per_player = 6, deck_after_deal = 8, hands = 4, rounds_per_hand = 8, rounds_total = 32, turns_per_player_per_hand = 4, secret_cards = 1, tradeoff_cards = 2, gift_cards = 3, gift_cards_to_opponent = 1, competition_cards = 4, competition_pair_size = 2, win_charm = 11, win_geisha = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player 1 and seat 2 is Player 2.
  2. All five markers start in the middle (marker_1 to marker_5 = 0).
  3. hand_number = 1, round_in_hand = 1, starting_seat = 1, game_over = 0.
  4. Each player's kept list is empty, and charm, geisha_count and standing are 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round_in_hand == 1: build deck as the 21 Items (three 1s, three 2s, four 3s, five 4s, six 5s). Draw 1 at random into removed_card. Draw 6 at random into each player's hand; the remaining 8 stay in deck. Set each secret, pending and discard to empty. Set each unused_actions to [Secret, Trade-off, Gift, Competition]. If hand_number is 1 or 3, set each kept to empty; in hands 2 and 4, kept carries over. Markers carry over.
  2. [update] all players. What happens: active_seat = starting_seat if round_in_hand is odd, otherwise the other seat (3 - starting_seat).
  3. [update] seat active_seat. What happens: Draw 1 card at random from deck (the top of a shuffled deck), append it to the active player's hand and remove it from deck.
  4. [sync] all players. What happens: Each player sees their own hand and secret, and both players' kept, unused_actions, markers and counters.
  5. [ask] seat active_seat answers: one of the active player's unused_actions. What happens: last_action = the choice; remove it from the active player's unused_actions.
  6. [ask] seat active_seat answers: one Geisha number present in the active player's hand. What happens: Move that card from hand to pending (pick 1).
  7. [ask] seat active_seat answers: one Geisha number present in the active player's hand. What happens: When last_action is Trade-off, Gift or Competition: move that card from hand to pending (pick 2).
  8. [ask] seat active_seat answers: one Geisha number present in the active player's hand. What happens: When last_action is Gift or Competition: move that card from hand to pending (pick 3).
  9. [ask] seat active_seat answers: one Geisha number present in the active player's hand. What happens: When last_action is Competition: move that card from hand to pending (pick 4). Picks 1-2 form Pair A and picks 3-4 form Pair B.
  10. [update] seat active_seat. What happens: When last_action is Secret: move the 1 pending card to the active player's secret, face-down.
  11. [update] seat active_seat. What happens: When last_action is Trade-off: move the 2 pending cards to discard, face-down.
  12. [tell] all players. What happens: When last_action is Gift: announce the 3 pending cards. When last_action is Competition: announce Pair A (picks 1-2) and Pair B (picks 3-4).
  13. [ask] the seat that is not active_seat answers: one of the 3 revealed Gift cards, by Geisha number. What happens: When last_action is Gift: append the chosen card to the opponent's kept, append the other 2 pending cards to the active player's kept, and empty pending.
  14. [ask] the seat that is not active_seat answers: Pair A or Pair B. What happens: When last_action is Competition: append the chosen pair to the opponent's kept, append the other pair to the active player's kept, and empty pending.
  15. [update] all players. What happens: When round_in_hand == 8: reveal each player's secret card, append it to their kept, and empty secret.
  16. [update] all players. What happens: When round_in_hand == 8 and hand_number is 2 or 4: (a) for each g in 1-5, count the cards of number g in each player's kept; if Player 1's count is strictly higher, marker_g = 1; if Player 2's is strictly higher, marker_g = 2; on a tie marker_g is unchanged. (b) Each player's charm = sum of the Charm (3,3,4,5,6) of g whose marker_g equals their seat; geisha_count = number of markers equal to their seat; standing = charm. (c) game_over = 1 if either charm >= 11, or either geisha_count >= 3, or hand_number == 4.
  17. [tell] all players. What happens: When round_in_hand == 8 and hand_number is 2 or 4: announce marker_1 to marker_5 and each player's charm and geisha_count.
  18. [check] all players. What happens: End the game if game_over == 1; otherwise continue.
  19. [update] all players. What happens: If round_in_hand < 8: round_in_hand += 1. Otherwise: round_in_hand = 1, hand_number += 1, starting_seat = 3 - starting_seat.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, all 5 markers are in the middle (value 0).
  R2. When a hand starts, 1 of the 21 Items is set aside as removed_card, each player is dealt 6 cards, and 8 cards remain in deck.
  R3. When a hand starts, both secrets and the discard are emptied and both unused_actions are reset to [Secret, Trade-off, Gift, Competition].
  R4. When hand 1 or hand 3 starts, both kept lists are emptied; when hand 2 or 4 starts, kept lists and markers are unchanged.
  R5. Player 1 is starting_seat in hands 1 and 3, and Player 2 in hands 2 and 4.
  R6. In rounds 1, 3, 5 and 7 the starting seat is active; in rounds 2, 4, 6 and 8 the other seat is active.
  R7. At the start of each turn the active player draws 1 card from deck into hand.
  R8. The active player is offered exactly the actions in their unused_actions, and the chosen action is removed from that list.
  R9. In a player's 4th turn of a hand, exactly one action remains and it must be taken.
  R10. When Secret is chosen, 1 hand card moves face-down to the player's secret.
  R11. When Trade-off is chosen, 2 hand cards move face-down to discard and do not score this hand.
  R12. When Gift is chosen, 3 hand cards are revealed, the opponent picks 1 for their kept, and the other 2 go to the active player's kept.
  R13. When Competition is chosen, 4 hand cards are revealed as Pair A and Pair B of 2 cards each, the opponent picks one pair for their kept, and the other pair goes to the active player's kept.
  R14. Cards named for an action must be cards the active player holds.
  R15. After round 8 of every hand, each player's secret card is appended to their kept.
  R16. After hands 2 and 4, for each Geisha g, marker_g moves to the side of the player with strictly more g cards in kept; on a tie it stays where it is.
  R17. After hands 2 and 4, charm = the summed Charm (3,3,4,5,6) of a player's markers, geisha_count = their number of markers, and standing = charm.
  R18. At a pair end, a player with charm >= 11 wins and the game ends.
  R19. At a pair end, if no one has charm >= 11, a player with geisha_count >= 3 wins and the game ends.
  R20. If one player has 11 charm and the other has 3 Geisha, the 11-charm player wins.
  R21. If no one has won after hand 4, the higher charm wins; if charm is tied, the higher geisha_count wins; otherwise the game is a draw.
  R22. After hand 2, if no one has won, play continues to hand 3.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose an action | asked: the active seat only | options: exactly the entries of the active player's unused_actions (4 in the first turn of a hand, 1 in the last)
  - Pick a card for the action (picks 1-4) | asked: the active seat only | options: each distinct Geisha number still in the active player's hand; pick 1 always, pick 2 for Trade-off, Gift or Competition, pick 3 for Gift or Competition, pick 4 for Competition only
  - Choose a Gift card | asked: the non-active seat, only when last_action is Gift | options: the Geisha numbers of the 3 revealed cards
  - Choose a Competition pair | asked: the non-active seat, only when last_action is Competition | options: Pair A, Pair B

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game_over == 1
  - each player's standing: (you.charm >= 11) * 10000 + (you.geisha_count >= 3) * 1000 + you.charm * 10 + you.geisha_count (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player with 11 or more Charm wins first. Otherwise a player with 3 or more Geisha wins. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count. Players level on all of these share the result, which is a draw.
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

- each player: `kept` (list, visible: public, starts []): cards placed on this player's side, visible to both
- each player: `charm` (number, visible: public, starts 0): total Charm of Geisha whose markers are on this player's side
- each player: `geisha_count` (number, visible: public, starts 0): number of markers on this player's side
- each player: `standing` (number, visible: public, starts 0): equals charm; the score
- the table: `marker_1` (number, visible: public, starts 0): Geisha 1 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
- the table: `marker_2` (number, visible: public, starts 0): Geisha 2 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
- the table: `marker_3` (number, visible: public, starts 0): Geisha 3 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
- the table: `marker_4` (number, visible: public, starts 0): Geisha 4 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
- the table: `marker_5` (number, visible: public, starts 0): Geisha 5 marker: 0 middle, 1 Player 1's side, 2 Player 2's side
- parameters (each must be an attribute holding this value, never a number buried in a step): geisha_count_total = 5, charm_geisha_1 = 3, charm_geisha_2 = 3, charm_geisha_3 = 4, charm_geisha_4 = 5, charm_geisha_5 = 6, items_total = 21, items_geisha_1 = 3, items_geisha_2 = 3, items_geisha_3 = 4, items_geisha_4 = 5, items_geisha_5 = 6, removed_per_hand = 1, deal_per_player = 6, deck_after_deal = 8, hands = 4, rounds_per_hand = 8, rounds_total = 32, turns_per_player_per_hand = 4, secret_cards = 1, tradeoff_cards = 2, gift_cards = 3, gift_cards_to_opponent = 1, competition_cards = 4, competition_pair_size = 2, win_charm = 11, win_geisha = 3
- the game ends with ONE ending whose `rank_by` is `(you.charm >= 11) * 10000 + (you.geisha_count >= 3) * 1000 + you.charm * 10 + you.geisha_count`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Remove the static `all_items` attribute. It is your own helper, not part of the interface. At the start of each hand (when round_in_hand = 1), rebuild the full 21-card deck with steps that actually run: empty the deck, then append the cards according to the parameters (items_geisha_1 copies of 1 through items_geisha_5 copies of 5). Then shuffle, move 1 card to removed_card, deal deal_per_player cards to each hand, and leave deck_after_deal cards in the deck. If you would rather keep a master list, it must be rewritten by a running step each hand, for example by refilling it before copying it into the deck. Keep the earlier fixes in place. Any condition that reads `you` (such as the secret checks) must sit in a per-player step or loop, or name the player explicitly through the active-seat attribute. Prompts may use only {value} and {seat}: show hand and unused_actions through the player's private state or the options list, not as placeholders. Bookkeeping attributes (chosen, last_action, pending picks, the counters) must be hidden, with `none` on the table and `ally` on players. Before you submit, check that every attribute you declare is changed by some step in a random match.
