# 36 coder

- time: 2026-10-27T10:46:19+00:00 (187.0s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 8939e1a1b3fbaf7b, reply sha256 948a7f7747499999

## Sent

````
# Task: write the XColos game file for "Hanamikoji: Paired Hands"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

COMPONENTS
- 5 Geisha, G1 to G5, with Charm G1=3, G2=3, G3=4, G4=5, G5=6 (total 21).
- 21 Item cards: three of G1, three of G2, four of G3, five of G4 and six of G5. A card is written as its Geisha number, 1 to 5.
- 5 Victory Markers, one per Geisha. Each is on Player 1's side, on Player 2's side, or neutral. All start neutral.
- Each player has four action markers: Secret, Trade-off, Gift and Competition.
- Each player has pair totals: five counts, one per Geisha, of the cards they have kept during the current pair of hands.

STRUCTURE
- There are at most 4 hands of 8 rounds each (32 rounds).
- Hands 1 and 2 form pair 1. Hands 3 and 4 form pair 2.
- Player 1 starts hands 1 and 3. Player 2 starts hands 2 and 4.
- In each hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player is active in rounds 2, 4, 6 and 8. The player who is not active is the opponent.

START OF EACH HAND (before its round 1)
- Shuffle all 21 Items.
- Remove the top card face down. Nobody sees it, and it plays no part this hand.
- Deal 6 cards to each player as a private hand. Each player sees only their own hand, as a sorted list of numbers.
- The other 8 cards form the face-down deck.
- Both players' four actions become unused, and both Secrets are emptied.
- At the start of hands 1 and 3 only, both players' pair totals are reset to 0 0 0 0 0.
- Victory Markers always stay where they are.

EACH ROUND
1. The game announces the hand, the round, the active player, each player's unused actions, both players' pair totals and the marker positions.
2. The active player draws the top deck card and is privately shown their hand.
3. Choice 1: the active player names one unused action: Secret, Trade-off, Gift or Competition.
4. Choice 2: the active player writes the cards the action uses, as space-separated numbers with repeats written out (for example '5 5 2'). The cards are legal if, for each Geisha number, the number of times it is written is at most the number of that card in the player's hand.
   - Secret: exactly 1 number. That card is set face down as their Secret.
   - Trade-off: exactly 2 numbers. Those cards are discarded face down and do not count.
   - Gift: exactly 3 numbers, revealed in the order written as offer 1, 2 and 3.
   - Competition: exactly 4 numbers, all revealed. The first two form pair A and the last two form pair B.
   The named cards leave the active player's hand.
5. Choice 3, only for Gift or Competition: the opponent writes one digit.
   - Gift: 1, 2 or 3. The opponent adds that card to their pair totals, and the active player adds the other two to theirs.
   - Competition: 1 for pair A or 2 for pair B. The opponent adds the chosen pair to their pair totals, and the active player adds the other pair to theirs.
6. The action becomes spent. The game publicly announces the action, and for Gift or Competition the revealed cards and the split. For Secret and Trade-off it announces only that the action was used.

DEFAULTS
- Illegal or missing action: the first unused action in the order Secret, Trade-off, Gift, Competition is used.
- Illegal card answer (wrong count, unreadable or not in hand): the required number of lowest-numbered cards in hand are used, in ascending order. For Competition, the first two of them form pair A.
- Illegal or missing pick: counts as 1.
- Cards always work out: each player holds 6 + 4 = 10 cards and spends 1 + 2 + 3 + 4 = 10.

END OF EACH HAND (after round 8)
- Each player's Secret is revealed and added to their pair totals.
- The game announces both Secrets and both players' pair totals.

END OF EACH PAIR (after hands 2 and 4, following the end-of-hand step)
- For each Geisha, compare the two players' pair totals. A strictly higher total moves that Geisha's marker to that player's side. A tie leaves the marker where it is (neutral, or on a side from pair 1).
- Charm is the sum of the Charm values of the Geisha on a player's side. Geisha count is the number of markers on a player's side.
- The game announces all markers, Charm and Geisha counts.
- Win check:
  - If a player has 11 or more Charm, they win.
  - Otherwise, if a player has 3 or more Geisha, they win.
  - Otherwise, after pair 1 the game continues with hand 3.
  - After pair 2 with no winner, the higher Charm wins. If Charm is equal, the higher Geisha count wins. If both are equal, the game is a draw.

How the winner is decided: After hand 2 and after hand 4: a player with 11 or more Charm from markers on their side wins. Otherwise a player with 3 or more markers on their side wins. Total Charm is 21 and there are 5 Geisha, so at most one player can meet each condition, and Charm is checked first. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count, and otherwise the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hanamikoji: Paired Hands (2 to 2 players, best with 2)

Two players win the favour of five Geisha over up to four hands, played as two pairs, by keeping, discarding, gifting and splitting Item cards with four one-use actions; Victory Markers move after each pair.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Item cards (numbers 1-5) the player privately holds, shown sorted
  - each player: secret (list, starts []); only its owner sees it. The 0 or 1 card set face down by the Secret action this hand
  - each player: unused_actions (list, starts ['Secret', 'Trade-off', 'Gift', 'Competition']); everyone sees it. Action markers not yet spent this hand
  - each player: kept (list, starts []); everyone sees it. Cards kept during the current pair of hands; the pair total for Geisha g is the count of g in this list (Secrets join it only at the end of a hand)
  - each player: charm (number, starts 0); everyone sees it. Sum of Charm of the Geisha whose marker is on this player's side
  - each player: geisha_count (number, starts 0); everyone sees it. Number of Victory Markers on this player's side
  - each player: standing (number, starts 0); everyone sees it. Ranking value: (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count
  - the table: deck (list, starts []); hidden from all players. Face-down draw deck for the current hand
  - the table: removed_card (list, starts []); hidden from all players. The one card set aside unseen at the start of each hand
  - the table: discard (list, starts []); hidden from all players. Face-down cards discarded by Trade-off this hand
  - the table: hand_number (number, starts 1); everyone sees it. Current hand, 1 to 4
  - the table: round_in_hand (number, starts 1); everyone sees it. Current round within the hand, 1 to 8
  - the table: starting_seat (number, starts 1); everyone sees it. Seat that starts the current hand: 1 in hands 1 and 3, 2 in hands 2 and 4
  - the table: active_seat (number, starts 1); everyone sees it. Seat acting this round; the other seat is the opponent
  - the table: chosen_action (text, starts ''); everyone sees it. Action named this round after defaults
  - the table: chosen_cards (list, starts []); hidden from all players. Cards used this round after defaults; revealed publicly only for Gift and Competition
  - the table: pick (number, starts 1); everyone sees it. Opponent's pick: 1-3 for Gift offers, 1 or 2 for Competition pairs A/B
  - the table: marker_1 (number, starts 0); everyone sees it. Victory Marker of Geisha 1: 0 neutral, 1 Player 1's side, 2 Player 2's side
  - the table: marker_2 (number, starts 0); everyone sees it. Victory Marker of Geisha 2
  - the table: marker_3 (number, starts 0); everyone sees it. Victory Marker of Geisha 3
  - the table: marker_4 (number, starts 0); everyone sees it. Victory Marker of Geisha 4
  - the table: marker_5 (number, starts 0); everyone sees it. Victory Marker of Geisha 5
  - the table: game_over (bool, starts False); everyone sees it. Set when a win check ends the game
  - parameters, each kept as a table attribute: geisha_count_total = 5, charm_g1 = 3, charm_g2 = 3, charm_g3 = 4, charm_g4 = 5, charm_g5 = 6, charm_total = 21, cards_g1 = 3, cards_g2 = 3, cards_g3 = 4, cards_g4 = 5, cards_g5 = 6, cards_total = 21, cards_removed_per_hand = 1, hand_size_dealt = 6, deck_size_after_deal = 8, max_hands = 4, rounds_per_hand = 8, max_rounds = 32, hands_per_pair = 2, secret_cards = 1, tradeoff_cards = 2, gift_cards = 3, competition_cards = 4, charm_to_win = 11, geisha_to_win = 3, default_pick = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player 1 and seat 2 is Player 2.
  2. All five Victory Markers start neutral (marker_1..marker_5 = 0).
  3. Charm, geisha_count and standing start at 0 for both players.
  4. hand_number = 1, round_in_hand = 1, starting_seat = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round_in_hand == 1 (start of a hand): build deck as the 21 Items [1,1,1,2,2,2,3,3,3,3,4,4,4,4,4,5,5,5,5,5,5]; move one random card from deck to removed_card (replacing its previous content); move 6 random deck cards into each player's hand (hand emptied first); deck now holds 8; discard emptied; each player's unused_actions = [Secret, Trade-off, Gift, Competition]; each secret emptied; if hand_number is 1 or 3, each kept = []; starting_seat = 1 if hand_number is 1 or 3, else 2.
  2. [update] all players. What happens: active_seat = starting_seat if round_in_hand is odd, else the other seat.
  3. [tell] all players. What happens: Announce hand_number, round_in_hand, active_seat, each player's unused_actions, each player's pair totals (count of 1..5 in kept), and marker_1..marker_5.
  4. [update] the active seat. What happens: Move one random card from deck to the active player's hand (the draw).
  5. [sync] all players. What happens: Each player privately sees their own sorted hand and secret.
  6. [ask] the active seat answers: one of the active player's unused_actions: Secret, Trade-off, Gift, Competition. What happens: chosen_action = the answer; if illegal or missing, chosen_action = the first of Secret, Trade-off, Gift, Competition still in unused_actions.
  7. [ask] the active seat answers: short text: space-separated card numbers, 1 for Secret, 2 for Trade-off, 3 for Gift, 4 for Competition, repeats written out. What happens: If legal, chosen_cards = the written numbers in order; otherwise chosen_cards = the required number of lowest cards in hand in ascending order. Remove chosen_cards from the active player's hand. JUDGED: a referee rules true or false on "The answer is exactly the required number of card numbers for chosen_action (Secret 1, Trade-off 2, Gift 3, Competition 4), and no number appears more often than that card appears in the active player's hand."; write this step's `when` as {"prose": that sentence, verbatim}.
  8. [update] the active seat. What happens: If chosen_action is Secret, append chosen_cards to the active player's secret; if Trade-off, append chosen_cards to discard. Remove chosen_action from the active player's unused_actions.
  9. [ask] the opponent (the seat that is not active_seat) answers: Gift: a choice of 1, 2 or 3; Competition: 1 (pair A = first two cards) or 2 (pair B = last two cards). What happens: When chosen_action is Gift or Competition: the opponent is shown the revealed chosen_cards (Gift as offers 1,2,3; Competition as pair A, pair B); pick = the answer, or 1 if illegal or missing.
  10. [update] both players. What happens: When chosen_action is Gift: append offer number pick to the opponent's kept and the other two offers to the active player's kept. When chosen_action is Competition: append the picked pair to the opponent's kept and the other pair to the active player's kept.
  11. [tell] all players. What happens: Publicly announce the active seat and chosen_action; for Gift or Competition also the revealed chosen_cards and who kept which; for Secret or Trade-off only that the action was used.
  12. [update] all players. What happens: When round_in_hand == 8 (end of hand): reveal each player's secret, append it to that player's kept, and announce both secrets and both players' pair totals.
  13. [update] all players. What happens: When round_in_hand == 8 and hand_number is 2 or 4 (end of pair): for each Geisha g, if count of g in Player 1's kept > count in Player 2's kept then marker_g = 1, if lower then marker_g = 2, if equal marker_g unchanged; for each player charm = sum of Charm (3,3,4,5,6) of Geisha with marker on their side, geisha_count = number of markers on their side, standing = (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count; game_over = true if any player has charm >= 11 or geisha_count >= 3, or if hand_number == 4. Announce all markers, charm and geisha counts.
  14. [check] all players. What happens: End the game if game_over is true; otherwise continue.
  15. [update] all players. What happens: If round_in_hand == 8 then hand_number += 1 and round_in_hand = 1; otherwise round_in_hand += 1.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand starts, then the 21 Items are shuffled, 1 card is set aside unseen, each player is dealt 6 cards privately, and 8 cards remain in the deck.
  R2. When a hand starts, then both players' unused_actions become Secret, Trade-off, Gift, Competition and both secrets are emptied.
  R3. When hand 1 or hand 3 starts, then both players' kept lists are emptied; when hand 2 or 4 starts, kept is unchanged.
  R4. When a new hand starts, then the Victory Markers stay where they are.
  R5. When the hand is 1 or 3, then seat 1 is active in rounds 1, 3, 5, 7 and seat 2 in rounds 2, 4, 6, 8; in hands 2 and 4 it is the reverse.
  R6. When a round starts, then the active player draws 1 card from the deck into their hand.
  R7. When the active player names an action that is spent or invalid, then the first unused action in the order Secret, Trade-off, Gift, Competition is used.
  R8. When the active player uses Secret with 1 legal card, then that card leaves their hand and becomes their secret.
  R9. When the active player uses Trade-off with 2 legal cards, then both cards leave their hand into the discard and count for nobody.
  R10. When the active player uses Gift with cards a b c, then the opponent picks 1, 2 or 3, the opponent adds that card to kept and the active player adds the other two to kept.
  R11. When the active player uses Competition with cards a b c d, then the opponent picks 1 (a b) or 2 (c d), the opponent adds that pair to kept and the active player adds the other pair.
  R12. When the card answer has the wrong count or names cards not in hand, then the required number of lowest cards in hand, in ascending order, is used, and for Competition the first two form pair A.
  R13. When the opponent's pick is illegal or missing, then it counts as 1.
  R14. When an action is used, then it is removed from the active player's unused_actions for the rest of the hand.
  R15. When Secret or Trade-off is used, then only the action's use is announced, not the cards.
  R16. When round 8 of a hand ends, then each player's secret is revealed and added to their kept.
  R17. When a pair ends (after hand 2 or 4) and a player's count of Geisha g in kept is strictly higher than the other's, then marker_g moves to that player's side; on a tie it stays.
  R18. When a pair ends, then charm is the sum of 3,3,4,5,6 over Geisha 1..5 on the player's side and geisha_count is the number of markers on their side.
  R19. When a pair ends and a player has charm >= 11, then that player wins.
  R20. When a pair ends, no player has charm >= 11 and a player has geisha_count >= 3, then that player wins.
  R21. When pair 1 ends with no winner, then the game continues with hand 3.
  R22. When pair 2 ends with no winner by threshold, then the higher charm wins, then the higher geisha_count, and if both are equal it is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choice 1: which action | asked: the active seat | options: exactly the actions still in that player's unused_actions (4 options in the first turn of a hand, 1 in the last)
  - Choice 2: which cards | asked: the active seat | options: free text of space-separated numbers 1-5: 1 number for Secret, 2 for Trade-off, 3 for Gift, 4 for Competition, drawn from their hand
  - Choice 3: the pick | asked: the opponent (the non-active seat), only after Gift or Competition | options: after Gift: 1, 2, 3; after Competition: 1 (pair A), 2 (pair B)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game_over == true, set after a pair (round_in_hand == 8 and hand_number in {2,4}) when any player has charm >= 11 or geisha_count >= 3, or when hand_number == 4
  - each player's standing: you.standing (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player with 11 or more Charm wins. Otherwise a player with 3 or more Geisha wins. If neither holds after hand 4, the higher Charm wins, then the higher Geisha count. Equal standing is a shared result, which is the draw.
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

- each player: `kept` (list, visible: public, starts []): Cards kept during the current pair of hands; the pair total for Geisha g is the count of g in this list (Secrets join it only at the end of a hand)
- each player: `charm` (number, visible: public, starts 0): Sum of Charm of the Geisha whose marker is on this player's side
- each player: `geisha_count` (number, visible: public, starts 0): Number of Victory Markers on this player's side
- each player: `standing` (number, visible: public, starts 0): Ranking value: (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count
- the table: `marker_1` (number, visible: public, starts 0): Victory Marker of Geisha 1: 0 neutral, 1 Player 1's side, 2 Player 2's side
- the table: `marker_2` (number, visible: public, starts 0): Victory Marker of Geisha 2
- the table: `marker_3` (number, visible: public, starts 0): Victory Marker of Geisha 3
- the table: `marker_4` (number, visible: public, starts 0): Victory Marker of Geisha 4
- the table: `marker_5` (number, visible: public, starts 0): Victory Marker of Geisha 5
- parameters (each must be an attribute holding this value, never a number buried in a step): geisha_count_total = 5, charm_g1 = 3, charm_g2 = 3, charm_g3 = 4, charm_g4 = 5, charm_g5 = 6, charm_total = 21, cards_g1 = 3, cards_g2 = 3, cards_g3 = 4, cards_g4 = 5, cards_g5 = 6, cards_total = 21, cards_removed_per_hand = 1, hand_size_dealt = 6, deck_size_after_deal = 8, max_hands = 4, rounds_per_hand = 8, max_rounds = 32, hands_per_pair = 2, secret_cards = 1, tradeoff_cards = 2, gift_cards = 3, competition_cards = 4, charm_to_win = 11, geisha_to_win = 3, default_pick = 1
- the game ends with ONE ending whose `rank_by` is `you.standing`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Fix the start-of-hand deal so it gives exactly hand_size_dealt (6) cards to each player. After removing cards_removed_per_hand (1), the deck should hold deck_size_after_deal (8) before round 1's draw. Check the counted repetition: the loop likely runs hand_size_dealt+1 times, or there is an extra deal step before the loop. After the fix, verify the counts: at hand start each player has 6 cards and the deck has 8; the active player then draws to 7 and spends cards per action. Also check that each round's draw comes from the 8-card deck, so the deck is empty after round 8. Leave the rest as is, but re-run R16 and R17 once the deal is correct: their 'Trade-off never matched' failures may come from the wrong hand sizes changing the flow. If they still fail, they target a seat that was not offered the option.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "hanamikoji_paired_hands",
    "name": "Hanamikoji: Paired Hands",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players court five Geisha over up to four hands in two pairs, keeping, discarding, gifting and splitting Item cards with four one-use actions."
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
        "key": "secret",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "unused_actions",
        "visible": "public",
        "type": "list",
        "initial": [
          "Secret",
          "Trade-off",
          "Gift",
          "Competition"
        ]
      },
      {
        "key": "kept",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pair_totals",
        "visible": "public",
        "type": "list",
        "initial": [
          0,
          0,
          0,
          0,
          0
        ]
      },
      {
        "key": "charm",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "geisha_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "standing",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          1,
          1,
          2,
          2,
          2,
          3,
          3,
          3,
          3,
          4,
          4,
          4,
          4,
          4,
          5,
          5,
          5,
          5,
          5,
          5
        ]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "removed_card",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "discard",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "draw_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "need_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "parsed_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick_options",
        "visible": "none",
        "type": "list",
        "initial": [
          "1",
          "2",
          "3"
        ]
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "chosen_action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "chosen_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "revealed_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "marker_1",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "marker_2",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "marker_3",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "marker_4",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "marker_5",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "game_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "geisha_count_total",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "charm_g1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "charm_g2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "charm_g3",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "charm_g4",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "charm_g5",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "charm_total",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "cards_g1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_g2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_g3",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_g4",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_g5",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_total",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "cards_removed_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_size_dealt",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_size_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "max_hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rounds_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "hands_per_pair",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "secret_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tradeoff_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gift_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "competition_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "charm_to_win",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "geisha_to_win",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "default_pick",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting position",
      "do": [
        {
          "set": {
            "key": "marker_1",
            "value": 0
          }
        },
        {
          "set": {
            "key": "marker_2",
            "value": 0
          }
        },
        {
          "set": {
            "key": "marker_3",
            "value": 0
          }
        },
        {
          "set": {
            "key": "marker_4",
            "value": 0
          }
        },
        {
          "set": {
            "key": "marker_5",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "charm",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "geisha_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "standing",
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
            "key": "round_in_hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "starting_seat",
            "value": 1
          }
        }
      ],
      "text": "Seat 1 is Player 1 and seat 2 is Player 2. All five Victory Markers start neutral."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start of hand",
      "label": "shuffle and deal",
      "when": {
        "calc": "round_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "key": "removed_card",
            "value": {
              "calc": "[draw_card]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "sorted(you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "unused_actions",
            "value": {
              "calc": "['Secret', 'Trade-off', 'Gift', 'Competition']"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "secret",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "kept",
            "value": [],
            "if": {
              "calc": "int((hand_number - 1) / hands_per_pair) * hands_per_pair + 1 == hand_number"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pair_totals",
            "value": {
              "calc": "[count(c == g for c in you.kept) for g in [1, 2, 3, 4, 5]]"
            }
          }
        },
        {
          "set": {
            "key": "starting_seat",
            "value": {
              "calc": "1 if int((hand_number - 1) / hands_per_pair) * hands_per_pair + 1 == hand_number else 2"
            }
          }
        }
      ],
      "text": "Hand {hand_number} begins. The Items are shuffled, one card is set aside unseen, each player is dealt {hand_size_dealt} cards and {deck_size_after_deal} cards form the deck. Seat {starting_seat} starts this hand."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "who is active",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starting_seat if round_in_hand - 2 * int(round_in_hand / 2) == 1 else 3 - starting_seat"
            }
          }
        },
        {
          "set": {
            "key": "chosen_action",
            "value": {
              "calc": "players[active_seat - 1].unused_actions[0]"
            }
          }
        },
        {
          "set": {
            "key": "chosen_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "revealed_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "default_pick"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_answer",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "round",
      "label": "the round",
      "to": "all",
      "text": "Hand {hand_number}, round {round_in_hand}: Seat {active_seat} is active. Unused actions: Seat 1 {players[0].unused_actions}; Seat 2 {players[1].unused_actions}. Pair totals (Geisha 1-5): Seat 1 {players[0].pair_totals}; Seat 2 {players[1].pair_totals}. Markers (0 neutral, 1 Seat 1, 2 Seat 2): G1 {marker_1}, G2 {marker_2}, G3 {marker_3}, G4 {marker_4}, G5 {marker_5}."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "the draw",
      "do": [
        {
          "set": {
            "key": "draw_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "len(deck) > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "draw_card"
            },
            "if": {
              "calc": "len(deck) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "draw_card"
            },
            "if": {
              "calc": "len(deck) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "sorted(you.hand)"
            }
          }
        }
      ],
      "text": "Seat {active_seat} draws a card."
    },
    {
      "use": "sync",
      "phase": "round",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "secret"
      ],
      "text": "Your hand and Secret:"
    },
    {
      "use": "ask",
      "phase": "round",
      "label": "choose an action",
      "when": {
        "calc": "len(players[active_seat - 1].unused_actions) > 1"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "unused_actions"
        }
      },
      "verify": {
        "bind": "action_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "chosen_action",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Name one of your unused actions: Secret ({secret_cards} card kept face down), Trade-off ({tradeoff_cards} cards discarded), Gift ({gift_cards} cards, the opponent takes one) or Competition ({competition_cards} cards in two pairs, the opponent takes a pair)."
    },
    {
      "use": "ask",
      "phase": "round",
      "label": "choose the cards",
      "when": {
        "prose": "The answer is exactly the required number of card numbers for chosen_action (Secret 1, Trade-off 2, Gift 3, Competition 4), and no number appears more often than that card appears in the active player's hand."
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 8
      },
      "store": "card_answer",
      "text": "You are using {chosen_action}. Write the cards from your hand as space-separated numbers, repeats written out (for example '5 5 2'): {secret_cards} for Secret, {tradeoff_cards} for Trade-off, {gift_cards} for Gift (offers 1, 2, 3 in order), {competition_cards} for Competition (first two are pair A, last two pair B). If the answer is not legal, your lowest cards are used in ascending order."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "resolve the cards",
      "do": [
        {
          "set": {
            "key": "need_count",
            "value": {
              "calc": "secret_cards if chosen_action == 'Secret' else (tradeoff_cards if chosen_action == 'Trade-off' else (gift_cards if chosen_action == 'Gift' else competition_cards))"
            }
          }
        },
        {
          "set": {
            "key": "parsed_cards",
            "value": {
              "calc": "[int(ch) for ch in players[active_seat - 1].card_answer if ch in '12345']"
            }
          }
        },
        {
          "set": {
            "key": "chosen_cards",
            "value": {
              "calc": "parsed_cards if (len(parsed_cards) == need_count and all(count(x == v for x in parsed_cards) <= count(x == v for x in players[active_seat - 1].hand) for v in [1, 2, 3, 4, 5])) else [players[active_seat - 1].hand[i] for i in [0, 1, 2, 3] if i < need_count]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "chosen_cards[0]"
            },
            "if": {
              "calc": "len(chosen_cards) > 0"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "chosen_cards[1]"
            },
            "if": {
              "calc": "len(chosen_cards) > 1"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "chosen_cards[2]"
            },
            "if": {
              "calc": "len(chosen_cards) > 2"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "chosen_cards[3]"
            },
            "if": {
              "calc": "len(chosen_cards) > 3"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "secret",
            "value": {
              "calc": "you.secret + chosen_cards"
            },
            "if": {
              "calc": "chosen_action == 'Secret'"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + chosen_cards"
            },
            "if": {
              "calc": "chosen_action == 'Trade-off'"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "unused_actions",
            "value": {
              "calc": "chosen_action"
            }
          }
        },
        {
          "set": {
            "key": "revealed_cards",
            "value": {
              "calc": "chosen_cards if chosen_action in ['Gift', 'Competition'] else []"
            }
          }
        },
        {
          "set": {
            "key": "pick_options",
            "value": {
              "calc": "['1', '2', '3'] if chosen_action == 'Gift' else ['1', '2']"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "round",
      "label": "the pick",
      "when": {
        "calc": "chosen_action in ['Gift', 'Competition']"
      },
      "to": {
        "where": "you.seat != active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "pick_options"
        }
      },
      "verify": {
        "bind": "pick_choice"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "Seat {active_seat} used {chosen_action} and revealed {revealed_cards}. After a Gift, pick 1, 2 or 3: you keep that offer and Seat {active_seat} keeps the other two. After a Competition, pick 1 (pair A, the first two cards) or 2 (pair B, the last two cards): you keep that pair and Seat {active_seat} keeps the other."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "the split",
      "when": {
        "calc": "chosen_action in ['Gift', 'Competition']"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat != active_seat"
            },
            "key": "kept",
            "value": {
              "calc": "you.kept + [chosen_cards[pick - 1]]"
            },
            "if": {
              "calc": "chosen_action == 'Gift'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "kept",
            "value": {
              "calc": "you.kept + [chosen_cards[i] for i in [0, 1, 2] if i != pick - 1]"
            },
            "if": {
              "calc": "chosen_action == 'Gift'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != active_seat"
            },
            "key": "kept",
            "value": {
              "calc": "you.kept + ([chosen_cards[0], chosen_cards[1]] if pick == 1 else [chosen_cards[2], chosen_cards[3]])"
            },
            "if": {
              "calc": "chosen_action == 'Competition'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "kept",
            "value": {
              "calc": "you.kept + ([chosen_cards[2], chosen_cards[3]] if pick == 1 else [chosen_cards[0], chosen_cards[1]])"
            },
            "if": {
              "calc": "chosen_action == 'Competition'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pair_totals",
            "value": {
              "calc": "[count(c == g for c in you.kept) for g in [1, 2, 3, 4, 5]]"
            }
          }
        }
      ],
      "text": "Seat {active_seat} used {chosen_action}, revealing {revealed_cards}. The opponent took choice {pick}; Seat {active_seat} kept the rest. Pair totals (Geisha 1-5): Seat 1 {players[0].pair_totals}; Seat 2 {players[1].pair_totals}."
    },
    {
      "use": "tell",
      "phase": "round",
      "label": "a hidden action",
      "when": {
        "calc": "chosen_action in ['Secret', 'Trade-off']"
      },
      "to": "all",
      "text": "Seat {active_seat} used {chosen_action}. The cards stay face down."
    },
    {
      "use": "update",
      "phase": "end of hand",
      "label": "the Secrets",
      "when": {
        "calc": "round_in_hand >= rounds_per_hand"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "kept",
            "value": {
              "calc": "you.kept + you.secret"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pair_totals",
            "value": {
              "calc": "[count(c == g for c in you.kept) for g in [1, 2, 3, 4, 5]]"
            }
          }
        }
      ],
      "text": "Hand {hand_number} is over. Secrets: Seat 1 {players[0].secret}; Seat 2 {players[1].secret}. Pair totals (Geisha 1-5): Seat 1 {players[0].pair_totals}; Seat 2 {players[1].pair_totals}."
    },
    {
      "use": "update",
      "phase": "end of pair",
      "label": "the Victory Markers",
      "when": {
        "calc": "round_in_hand >= rounds_per_hand and int(hand_number / hands_per_pair) * hands_per_pair == hand_number"
      },
      "do": [
        {
          "set": {
            "key": "marker_1",
            "value": {
              "calc": "1 if players[0].pair_totals[0] > players[1].pair_totals[0] else (2 if players[0].pair_totals[0] < players[1].pair_totals[0] else marker_1)"
            }
          }
        },
        {
          "set": {
            "key": "marker_2",
            "value": {
              "calc": "1 if players[0].pair_totals[1] > players[1].pair_totals[1] else (2 if players[0].pair_totals[1] < players[1].pair_totals[1] else marker_2)"
            }
          }
        },
        {
          "set": {
            "key": "marker_3",
            "value": {
              "calc": "1 if players[0].pair_totals[2] > players[1].pair_totals[2] else (2 if players[0].pair_totals[2] < players[1].pair_totals[2] else marker_3)"
            }
          }
        },
        {
          "set": {
            "key": "marker_4",
            "value": {
              "calc": "1 if players[0].pair_totals[3] > players[1].pair_totals[3] else (2 if players[0].pair_totals[3] < players[1].pair_totals[3] else marker_4)"
            }
          }
        },
        {
          "set": {
            "key": "marker_5",
            "value": {
              "calc": "1 if players[0].pair_totals[4] > players[1].pair_totals[4] else (2 if players[0].pair_totals[4] < players[1].pair_totals[4] else marker_5)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "charm",
            "value": {
              "calc": "(charm_g1 if marker_1 == you.seat else 0) + (charm_g2 if marker_2 == you.seat else 0) + (charm_g3 if marker_3 == you.seat else 0) + (charm_g4 if marker_4 == you.seat else 0) + (charm_g5 if marker_5 == you.seat else 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "geisha_count",
            "value": {
              "calc": "count(m == you.seat for m in [marker_1, marker_2, marker_3, marker_4, marker_5])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "standing",
            "value": {
              "calc": "(1000 if you.charm >= charm_to_win else 0) + (100 if you.geisha_count >= geisha_to_win else 0) + you.charm * 10 + you.geisha_count"
            }
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": {
              "calc": "any(p.charm >= charm_to_win or p.geisha_count >= geisha_to_win for p in players) or hand_number >= max_hands"
            }
          }
        }
      ],
      "text": "The pair is over. Markers (0 neutral, 1 Seat 1, 2 Seat 2): G1 {marker_1}, G2 {marker_2}, G3 {marker_3}, G4 {marker_4}, G5 {marker_5}. Seat 1: Charm {players[0].charm}, Geisha {players[0].geisha_count}. Seat 2: Charm {players[1].charm}, Geisha {players[1].geisha_count}."
    },
    {
      "use": "check",
      "phase": "end of pair",
      "label": "is there a winner",
      "when": {
        "calc": "game_over"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "round",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "hand_number",
            "value": 1,
            "if": {
              "calc": "round_in_hand >= rounds_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "round_in_hand",
            "value": {
              "calc": "1 if round_in_hand >= rounds_per_hand else round_in_hand + 1"
            }
          }
        }
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "game_over"
      },
      "rank_by": "you.standing",
      "text": "Winner: {result}. Seat 1: Charm {players[0].charm}, Geisha {players[0].geisha_count}; Seat 2: Charm {players[1].charm}, Geisha {players[1].geisha_count}."
    }
  },
  "limits": {
    "rounds": 32,
    "rounds_max": 40,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "COMPONENTS. Five Geisha, G1 to G5, with Charm G1={charm_g1}, G2={charm_g2}, G3={charm_g3}, G4={charm_g4}, G5={charm_g5} (total {charm_total}). {cards_total} Item cards: {cards_g1} of G1, {cards_g2} of G2, {cards_g3} of G3, {cards_g4} of G4 and {cards_g5} of G5; a card is written as its Geisha number, 1 to 5. Five Victory Markers, one per Geisha, each on Player 1's side, on Player 2's side, or neutral; all start neutral. Each player has four action markers: Secret, Trade-off, Gift and Competition. Each player has pair totals: five counts, one per Geisha, of the cards they have kept during the current pair of hands. Seat 1 is Player 1 and seat 2 is Player 2.\n\nSTRUCTURE. There are at most {max_hands} hands of {rounds_per_hand} rounds each ({max_rounds} rounds). Hands 1 and 2 form pair 1; hands 3 and 4 form pair 2. Player 1 starts hands 1 and 3; Player 2 starts hands 2 and 4. In each hand the starting player is active in rounds 1, 3, 5 and 7, and the other player is active in rounds 2, 4, 6 and 8. The player who is not active is the opponent.\n\nSTART OF EACH HAND. Shuffle all {cards_total} Items. Remove the top {cards_removed_per_hand} card face down: nobody sees it and it plays no part this hand. Deal {hand_size_dealt} cards to each player as a private hand; each player sees only their own hand, as a sorted list of numbers. The other {deck_size_after_deal} cards form the face-down deck. Both players' four actions become unused, and both Secrets are emptied. At the start of hands 1 and 3 only, both players' pair totals are reset to 0 0 0 0 0; at the start of hands 2 and 4 they are kept. Victory Markers always stay where they are.\n\nEACH ROUND. 1. The game announces the hand, the round, the active player, each player's unused actions, both players' pair totals and the marker positions. 2. The active player draws the top deck card and is privately shown their hand. 3. Choice 1: the active player names one unused action: Secret, Trade-off, Gift or Competition (you are offered only your unused actions; with one left it is used automatically). 4. Choice 2: the active player writes the cards the action uses, as space-separated numbers with repeats written out (for example '5 5 2'). The cards are legal if, for each Geisha number, the number of times it is written is at most the number of that card in the player's hand. Secret: exactly {secret_cards} number; that card is set face down as their Secret. Trade-off: exactly {tradeoff_cards} numbers; those cards are discarded face down and count for nobody. Gift: exactly {gift_cards} numbers, revealed in the order written as offer 1, 2 and 3. Competition: exactly {competition_cards} numbers, all revealed; the first two form pair A and the last two form pair B. The named cards leave the active player's hand. 5. Choice 3, only for Gift or Competition: the opponent writes one digit. Gift: 1, 2 or 3; the opponent adds that card to their pair totals, and the active player adds the other two to theirs. Competition: 1 for pair A or 2 for pair B; the opponent adds the chosen pair to their pair totals, and the active player adds the other pair to theirs. 6. The action becomes spent for the rest of the hand. The game publicly announces the action, and for Gift or Competition the revealed cards and the split. For Secret and Trade-off it announces only that the action was used, never the cards.\n\nDEFAULTS. Illegal or missing action: the first unused action in the order Secret, Trade-off, Gift, Competition is used. Illegal card answer (wrong count, unreadable or not in hand): the required number of lowest-numbered cards in hand are used, in ascending order; for Competition the first two of them form pair A. A legal card answer is used exactly as written. Illegal or missing pick: counts as {default_pick}. Cards always work out: each player holds 6 + 4 = 10 cards and spends 1 + 2 + 3 + 4 = 10.\n\nEND OF EACH HAND (after round 8). Each player's Secret is revealed and added to their pair totals. The game announces both Secrets and both players' pair totals.\n\nEND OF EACH PAIR (after hands 2 and 4, following the end-of-hand step). For each Geisha, compare the two players' pair totals. A strictly higher total moves that Geisha's marker to that player's side. A tie leaves the marker where it is (neutral, or on a side from pair 1). Charm is the sum of the Charm values of the Geisha on a player's side. Geisha count is the number of markers on a player's side. The game announces all markers, Charm and Geisha counts. Win check: if a player has {charm_to_win} or more Charm, they win. Otherwise, if a player has {geisha_to_win} or more Geisha, they win. Otherwise, after pair 1 the game continues with hand 3. After pair 2 with no winner, the higher Charm wins; if Charm is equal, the higher Geisha count wins; if both are equal, the game is a draw (a shared result)."
}
```
````
