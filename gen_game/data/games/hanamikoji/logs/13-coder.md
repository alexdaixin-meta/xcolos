# 13 coder

- time: 2026-10-27T10:00:57+00:00 (127.0s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 6b00831e47409b47, reply sha256 c6897c334e0d9c43

## Sent

````
# Task: write the XColos game file for "Hanamikoji: Compact Build"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

COMPONENTS
- Seven Geisha, G1 to G7. Charm values: G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5 (21 in total).
- 21 Item cards. Each Geisha has as many Items as her Charm value: two G1, two G2, two G3, three G4, three G5, four G6, five G7. A card is named by its Geisha (for example 'G6').
- Each player has four action types: Secret, Trade-off, Gift, Competition.

TRACKED STATE (17 attributes)
1. deck: ordered list of cards, hidden.
2. pile: the out-of-play list, hidden from everyone forever.
3. hand_A: Player A's ordered hand, seen only by A.
4. hand_B: Player B's ordered hand, seen only by B.
5. secret_A: seen only by A until the end of the hand.
6. secret_B: seen only by B until the end of the hand.
7. counts_A: 7 numbers, A's placed cards per Geisha.
8. counts_B: 7 numbers, B's placed cards per Geisha.
9. markers: 7 entries, each 'A', 'N' or 'B'. All start 'N'.
10. actions_A: A's unused actions this hand.
11. actions_B: B's unused actions this hand.
12. hand_number: 1 to 4.
13. turn_number: 1 to 8 within the hand.
14. standing: [Charm held by A, Charm held by B, Geisha held by A, Geisha held by B], all starting 0.
15. chosen_action.
16. offer: the cards revealed this turn, in order, split into Pair 1 and Pair 2 for Competition.
17. pick.

HIDDEN ELEMENTS (3)
(1) The hidden pile: the deck order plus the out-of-play pile, which holds the removed card and all Trade-off cards.
(2) The private hands.
(3) The secret cards.

STRUCTURE
- One engine round is one turn. A hand has 8 turns, and the game lasts at most 4 hands, so at most 32 rounds.
- Active player: in hands 1 and 3, Player A acts on odd turns and B on even turns. In hands 2 and 4, Player B acts on odd turns and A on even turns.

HAND ORDER
- Cards dealt to a hand keep the order they were dealt in.
- A drawn card goes to the end of the hand.
- When cards leave a hand, the remaining cards keep their order.

STEPS OF EACH ROUND
1. (Turn 1 only) Shuffle all 21 Items.
2. (Turn 1 only) The first card goes to the pile. Cards 2–7 go to the first player's hand and cards 8–13 to the second player's hand, where the first player is the one who acts on turn 1. Cards 14–21 form the deck in that order. Both action lists are reset to all four actions. Both count lists are reset to seven zeros. Both secrets are emptied. Markers and standing are NOT reset.
3. The active player moves the first card of the deck to the end of their hand.
4. Show both players: the markers, both count lists, both unused-action lists, the standing, the hand number and the turn number. Each player privately sees their own hand and their own secret.
5. CHOICE: the active player names one unused action and the cards for it:
   - Secret: 1 card.
   - Trade-off: 2 cards.
   - Gift: 3 cards.
   - Competition: 4 cards, the first two being Pair 1 and the last two Pair 2.
6. FALLBACK: the choice is illegal if it names a spent action, a card not held (counting duplicates), or the wrong number of cards. In that case the engine uses the active player's first unused action in the order Secret, Trade-off, Gift, Competition, filled with the first cards of their hand in hand order. A legal fallback always exists, because a player's hand always holds at least as many cards as their remaining actions need: 7 cards against at most 4 needed on their first turn, and exactly the number needed on their last.
7. The chosen cards leave the hand:
   - Secret: the card becomes the active player's secret.
   - Trade-off: both cards go face-down to the pile.
   - Gift or Competition: the cards go to the offer.
8. (Gift or Competition only) The offer is revealed to both players.
9. (Gift or Competition only) CHOICE: the opponent picks. For Gift they pick card 1, 2 or 3 of the offer. For Competition they pick Pair 1 or Pair 2.
10. (Gift or Competition only) An invalid pick becomes option 1.
11. Placement:
   - Gift: the picked card adds 1 to the opponent's count for its Geisha, and the other two cards add 1 each to the active player's counts.
   - Competition: the picked pair adds to the opponent's counts and the other pair to the active player's counts.
   Placed cards are public.
12. The used action is removed from the active player's action list. The offer, chosen action and pick are cleared. The turn number goes up by 1.
13. (After turn 8 only) Both secrets are revealed, each adds 1 to its owner's count for its Geisha, and both secrets are emptied.
14. (After turn 8 only) One calculation, for each Geisha i from 1 to 7:
   - if counts_A[i] > counts_B[i], markers[i] becomes 'A';
   - if counts_B[i] > counts_A[i], markers[i] becomes 'B';
   - otherwise markers[i] is unchanged.
   Then standing is set to [sum of Charm of the 'A' markers, sum of Charm of the 'B' markers, number of 'A' markers, number of 'B' markers].
15. (After turn 8 only) Announce the markers and the standing.
16. (After turn 8 only) Winner check:
   - A player with 11 or more Charm wins. Only one player can, since the total Charm is 21.
   - Otherwise, a player with 4 or more Geisha wins. Only one player can.
   - Otherwise, if this was hand 4, the game ends: higher Charm wins, then more Geisha, else a draw.
17. (After turn 8 only, if the game has not ended) The hand number goes up by 1 and the turn number is set back to 1. The next hand's first player is the other player.

INFORMATION
- Public: placed cards and counts, revealed offers, picks, markers, standing, and spent actions.
- Private: each hand, and each secret until the end of the hand.
- Never revealed: the pile.
- Players may use the known 21-card composition to deduce unseen cards.

How the winner is decided: At the end of each hand, a player whose markers total 11 or more Charm wins. Otherwise, a player holding 4 or more Geisha markers wins. If neither has happened after hand 4, higher Charm held wins, then more Geisha held, and if both are equal the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hanamikoji: Compact Build (2 to 2 players, best with 2)

Two players spend four one-use actions each hand to place Item cards for seven Geisha. They win a Geisha's favour by placing more of her Items, and the first to 11 Charm or 4 Geisha at a hand's end wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. This player's ordered hand of Item cards (hand_A for seat 1, hand_B for seat 2). Cards dealt keep their dealt order, a drawn card goes to the end, and the cards left behind keep their order.
  - each player: secret (list, starts []); only its owner sees it. The card held by Secret this hand, at most 1 (secret_A, secret_B). It is revealed and scored after turn 8.
  - each player: counts (list, starts [0, 0, 0, 0, 0, 0, 0]); everyone sees it. Cards this player has placed per Geisha, G1..G7, this hand (counts_A, counts_B).
  - each player: actions (list, starts ['Secret', 'Trade-off', 'Gift', 'Competition']); everyone sees it. This player's unused actions this hand (actions_A, actions_B).
  - each player: charm (number, starts 0); everyone sees it. Sum of the Charm of the Geisha whose marker is on this player's side (standing[0] for A, standing[1] for B).
  - each player: geisha (number, starts 0); everyone sees it. Number of Geisha markers on this player's side (standing[2] for A, standing[3] for B).
  - the table: deck (list, starts []); hidden from all players. The ordered draw deck. Each hand it is refilled from the 21 Items: G1 x2, G2 x2, G3 x2, G4 x3, G5 x3, G6 x4, G7 x5.
  - the table: pile (list, starts []); hidden from all players. Out-of-play cards: the 1 removed card and all Trade-off cards. Never revealed.
  - the table: markers (list, starts ['N', 'N', 'N', 'N', 'N', 'N', 'N']); everyone sees it. For each Geisha G1..G7: 'A' (seat 1), 'B' (seat 2) or 'N'. Never reset between hands.
  - the table: charm_values (list, starts [2, 2, 2, 3, 3, 4, 5]); everyone sees it. Charm of G1..G7.
  - the table: hand_number (number, starts 1); everyone sees it. Current hand, 1 to 4.
  - the table: turn_number (number, starts 1); everyone sees it. Turn within the hand, 1 to 8. It is 9 briefly during end-of-hand scoring.
  - the table: active_seat (number, starts 1); everyone sees it. Seat acting this turn: 1 + ((hand_number + turn_number) mod 2).
  - the table: chosen_action (text, starts ''); everyone sees it. The action the active player chose this turn.
  - the table: offer (list, starts []); hidden from all players. Cards the active player selected this turn, in order. For Competition, entries 1-2 are Pair 1 and entries 3-4 are Pair 2. Revealed to both players for Gift and Competition only.
  - the table: pick (text, starts ''); everyone sees it. The opponent's pick: 'card 1', 'card 2' or 'card 3' for Gift, or 'Pair 1' or 'Pair 2' for Competition.
  - parameters, each kept as a table attribute: charm_g1 = 2, charm_g2 = 2, charm_g3 = 2, charm_g4 = 3, charm_g5 = 3, charm_g6 = 4, charm_g7 = 5, total_charm = 21, total_items = 21, items_per_geisha_equals_charm = 1, geisha_count = 7, max_hands = 4, turns_per_hand = 8, cards_removed_per_hand = 1, starting_hand_size = 6, deck_size_after_deal = 8, cards_drawn_per_turn = 1, secret_cards = 1, tradeoff_cards = 2, gift_cards = 3, competition_cards = 4, gift_cards_to_opponent = 1, competition_cards_per_pair = 2, charm_to_win = 11, geisha_to_win = 4

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player A and seat 2 is Player B.
  2. Markers start as seven 'N', and each player's charm and geisha start at 0.
  3. hand_number is 1 and turn_number is 1; the shuffle and deal happen in the first step of round one.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When turn_number = 1: deck is set to the 21 Items (G1 x2, G2 x2, G3 x2, G4 x3, G5 x3, G6 x4, G7 x5) and pile to []. Every hand, secret and offer is emptied, every counts becomes [0,0,0,0,0,0,0], and every actions becomes [Secret, Trade-off, Gift, Competition]. Then, drawing at random from deck (the shuffle): 1 card is appended to pile; 6 cards, one at a time, to the hand of the first player (seat 1 + ((hand_number + 1) mod 2)); 6 cards to the other seat's hand. The remaining 8 stay in deck in the order drawn. markers, charm and geisha are not reset.
  2. [update] all players. What happens: active_seat = 1 + ((hand_number + turn_number) mod 2).
  3. [update] the active seat. What happens: The first card of deck is removed from deck and appended to the end of the active seat's hand.
  4. [sync] all players. What happens: Each player sees markers, both counts, both actions, both charm and geisha, hand_number and turn_number, plus their own hand and own secret.
  5. [ask] the active seat answers: one of the active seat's actions list (unused actions only). What happens: chosen_action = the answer. An invalid answer becomes the first unused action in the order Secret, Trade-off, Gift, Competition.
  6. [ask] the active seat answers: one card from the active seat's hand (first selected card). What happens: That card is removed from hand (one copy) and appended to offer. An invalid answer becomes the first card of hand.
  7. [ask] the active seat answers: one card from the active seat's remaining hand (second selected card). What happens: When chosen_action is not Secret: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand.
  8. [ask] the active seat answers: one card from the active seat's remaining hand (third selected card). What happens: When chosen_action is Gift or Competition: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand.
  9. [ask] the active seat answers: one card from the active seat's remaining hand (fourth selected card). What happens: When chosen_action is Competition: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand.
  10. [update] the active seat. What happens: When chosen_action is Secret: the offer card moves to the active seat's secret. When chosen_action is Trade-off: both offer cards are appended to pile. In both cases offer is emptied.
  11. [tell] all players. What happens: When chosen_action is Gift or Competition: the offer is revealed to both players, in order. For Competition it is shown as Pair 1 = cards 1-2 and Pair 2 = cards 3-4.
  12. [ask] the seat that is not active (3 - active_seat) answers: card 1, card 2 or card 3. What happens: When chosen_action is Gift: pick = the answer. An invalid answer becomes card 1.
  13. [ask] the seat that is not active (3 - active_seat) answers: Pair 1 or Pair 2. What happens: When chosen_action is Competition: pick = the answer. An invalid answer becomes Pair 1.
  14. [update] all players. What happens: When chosen_action is Gift: the picked offer card adds 1 to the opponent's counts at its Geisha, and each of the other two offer cards adds 1 to the active seat's counts at its Geisha. Announce the placement publicly.
  15. [update] all players. What happens: When chosen_action is Competition: each card of the picked pair adds 1 to the opponent's counts at its Geisha, and each card of the other pair adds 1 to the active seat's counts at its Geisha. Announce the placement publicly.
  16. [update] all players. What happens: chosen_action is removed from the active seat's actions. offer, chosen_action and pick are cleared. turn_number goes up by 1.
  17. [update] all players. What happens: When turn_number = 9: each player's secret is revealed to all and adds 1 to that player's counts at its Geisha, then every secret is emptied.
  18. [update] all players. What happens: When turn_number = 9: for each Geisha i from 1 to 7, markers[i] = 'A' if seat 1 counts[i] > seat 2 counts[i]; 'B' if seat 2 counts[i] > seat 1 counts[i]; otherwise unchanged. Then seat 1 charm = sum of charm_values[i] over markers 'A' and seat 1 geisha = number of 'A'; seat 2 charm = sum over markers 'B' and seat 2 geisha = number of 'B'.
  19. [tell] all players. What happens: When turn_number = 9: announce markers and both players' charm and geisha.
  20. [check] all players. What happens: When turn_number = 9: end the game if any player's charm >= 11, or any player's geisha >= 4, or hand_number = 4. Otherwise continue.
  21. [update] all players. What happens: When turn_number = 9: hand_number goes up by 1 and turn_number = 1. The next hand's first player is then the other seat, by the active_seat formula.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand begins (turn_number = 1), then all 21 Items are shuffled: 1 card goes to pile, 6 to the first player's hand, 6 to the second player's hand, and 8 form the deck.
  R2. When a hand begins, then both actions lists become [Secret, Trade-off, Gift, Competition], both counts become seven zeros and both secrets are emptied, while markers, charm and geisha are kept.
  R3. When hand_number is 1 or 3, then seat 1 (A) acts on odd turns and seat 2 (B) on even turns; when hand_number is 2 or 4, then seat 2 acts on odd turns and seat 1 on even turns.
  R4. When a turn starts, then the active player moves the first card of deck to the end of their hand, so their hand grows by 1 and the deck shrinks by 1.
  R5. When the active player chooses Secret, then 1 card leaves their hand and becomes their secret, hidden from the opponent until after turn 8.
  R6. When the active player chooses Trade-off, then 2 cards leave their hand and go to the pile, which is never revealed.
  R7. When the active player chooses Gift, then 3 cards leave their hand and are revealed, and the opponent picks 1 of them.
  R8. When the opponent picks a Gift card, then that card adds 1 to the opponent's counts for its Geisha and the other 2 cards add 1 each to the active player's counts.
  R9. When the active player chooses Competition, then 4 cards leave their hand and are revealed as Pair 1 (cards 1-2) and Pair 2 (cards 3-4), and the opponent picks one pair.
  R10. When the opponent picks a Competition pair, then its 2 cards add to the opponent's counts and the other 2 cards add to the active player's counts.
  R11. When a Gift or Competition pick is invalid, then it becomes option 1 (card 1 or Pair 1).
  R12. When an action choice or card choice is invalid, then the engine uses the first unused action in the order Secret, Trade-off, Gift, Competition, and the first cards of the hand in hand order.
  R13. When an action is used, then it is removed from that player's actions and cannot be chosen again this hand, so each player uses each of the 4 actions exactly once per hand.
  R14. When turn 8 ends, then both secrets are revealed and each adds 1 to its owner's counts for its Geisha.
  R15. When turn 8 ends, then for each Geisha the player with strictly more placed cards takes her marker, and on a tie the marker stays where it was.
  R16. When markers are updated, then each player's charm is the sum of Charm (G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5) of their markers, and their geisha is the number of their markers.
  R17. When a hand ends and a player has 11 or more charm, then the game ends and that player wins.
  R18. When a hand ends, no player has 11 charm and a player has 4 or more geisha, then the game ends and that player wins.
  R19. When hand 4 ends with no earlier win, then the player with higher charm wins; on equal charm the player with more geisha wins; if both are equal, the game is a draw.
  R20. When a hand ends without the game ending, then hand_number goes up by 1, turn_number returns to 1, and the other player acts first in the new hand.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose an action | asked: the active seat | options: exactly the entries still in that seat's actions list (of Secret, Trade-off, Gift, Competition)
  - Select the 1st card | asked: the active seat | options: any card in that seat's current hand
  - Select the 2nd card (Trade-off, Gift or Competition only) | asked: the active seat | options: any card still in that seat's hand after earlier selections this turn
  - Select the 3rd card (Gift or Competition only) | asked: the active seat | options: any card still in that seat's hand after earlier selections this turn
  - Select the 4th card (Competition only) | asked: the active seat | options: any card still in that seat's hand after earlier selections this turn
  - Pick from a Gift | asked: the non-active seat | options: card 1, card 2, card 3
  - Pick from a Competition | asked: the non-active seat | options: Pair 1, Pair 2

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: turn_number = 9 and (max over players of charm >= 11 or max over players of geisha >= 4 or hand_number = 4)
  - each player's standing: you.charm * 10 + you.geisha (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Charm held, then Geisha held. A player with 11+ Charm always has the higher Charm (the total is 21). A player with 4+ Geisha always has at least equal Charm and more Geisha whenever neither player has 11 Charm. So this one ranking reproduces the 11-Charm win, the 4-Geisha win and the hand-4 tie-break. Equal Charm and equal Geisha is a draw, a shared win.
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

- each player: `counts` (list, visible: public, starts [0, 0, 0, 0, 0, 0, 0]): Cards this player has placed per Geisha, G1..G7, this hand (counts_A, counts_B).
- each player: `charm` (number, visible: public, starts 0): Sum of the Charm of the Geisha whose marker is on this player's side (standing[0] for A, standing[1] for B).
- each player: `geisha` (number, visible: public, starts 0): Number of Geisha markers on this player's side (standing[2] for A, standing[3] for B).
- the table: `markers` (list, visible: public, starts ['N', 'N', 'N', 'N', 'N', 'N', 'N']): For each Geisha G1..G7: 'A' (seat 1), 'B' (seat 2) or 'N'. Never reset between hands.
- the table: `hand_number` (number, visible: public, starts 1): Current hand, 1 to 4.
- parameters (each must be an attribute holding this value, never a number buried in a step): charm_g1 = 2, charm_g2 = 2, charm_g3 = 2, charm_g4 = 3, charm_g5 = 3, charm_g6 = 4, charm_g7 = 5, total_charm = 21, total_items = 21, items_per_geisha_equals_charm = 1, geisha_count = 7, max_hands = 4, turns_per_hand = 8, cards_removed_per_hand = 1, starting_hand_size = 6, deck_size_after_deal = 8, cards_drawn_per_turn = 1, secret_cards = 1, tradeoff_cards = 2, gift_cards = 3, competition_cards = 4, gift_cards_to_opponent = 1, competition_cards_per_pair = 2, charm_to_win = 11, geisha_to_win = 4
- the game ends with ONE ending whose `rank_by` is `you.charm * 10 + you.geisha`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1. Declare each player's `counts` with the starting value [0, 0, 0, 0, 0, 0, 0], as the interface requires. Keep the turn-1 reset to zeros as well.
2. Give every fixed lookup list its full contents as its starting value: `geisha_names` ['G1'..'G7'], `geisha_index`, `charm_values` [2,2,2,3,3,4,5] (built from the charm_gN parameters) and `all_items` (the 21 cards). Do not fill these only in the turn-1 setup steps, because play can start on any turn.
3. Check the placement steps after the pick (step 11):
   - Gift: the picked offer card adds 1 to the opponent's count at that Geisha's index, and the other two cards add 1 each to the active player's counts.
   - Competition: Pair 1 is offer cards 1–2 and Pair 2 is cards 3–4. The picked pair goes to the opponent and the other pair to the active player.
   - Make sure placement runs before the offer is cleared, and that the index lookup resolves a card name like 'G6' to position 6.
4. Verify with a mid-hand scenario that both seats' counts change as expected.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "hanamikoji_compact",
    "name": "Hanamikoji: Compact Build",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players spend four one-use actions each hand to win the favour of seven Geisha: first to 11 Charm or 4 Geisha at a hand's end wins."
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
        "key": "counts",
        "visible": "public",
        "type": "list",
        "initial": [0, 0, 0, 0, 0, 0, 0]
      },
      {
        "key": "actions",
        "visible": "public",
        "type": "list",
        "initial": ["Secret", "Trade-off", "Gift", "Competition"]
      },
      {
        "key": "charm",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "geisha",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "markers",
        "visible": "public",
        "type": "list",
        "initial": ["N", "N", "N", "N", "N", "N", "N"]
      },
      {
        "key": "charm_values",
        "visible": "public",
        "type": "list",
        "initial": [2, 2, 2, 3, 3, 4, 5]
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "turn_number",
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
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
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
        "key": "drawn",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "newdeck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "geisha_names",
        "visible": "none",
        "type": "list",
        "initial": ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]
      },
      {
        "key": "geisha_index",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6]
      },
      {
        "key": "all_items",
        "visible": "none",
        "type": "list",
        "initial": ["G1", "G1", "G2", "G2", "G3", "G3", "G4", "G4", "G4", "G5", "G5", "G5", "G6", "G6", "G6", "G6", "G7", "G7", "G7", "G7", "G7"]
      },
      {
        "key": "charm_g1",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "charm_g2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "charm_g3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "charm_g4",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "charm_g5",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "charm_g6",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "charm_g7",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "total_charm",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "total_items",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "items_per_geisha_equals_charm",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "geisha_count",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "max_hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "turns_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cards_removed_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_hand_size",
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
        "key": "cards_drawn_per_turn",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "gift_cards_to_opponent",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "competition_cards_per_pair",
        "visible": "public",
        "type": "number",
        "initial": 2
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
        "initial": 4
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
      "do": [
        {
          "set": {
            "key": "charm_values",
            "value": {
              "calc": "[charm_g1, charm_g2, charm_g3, charm_g4, charm_g5, charm_g6, charm_g7]"
            }
          }
        },
        {
          "set": {
            "key": "markers",
            "value": ["N", "N", "N", "N", "N", "N", "N"]
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
            "key": "geisha",
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
            "key": "turn_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        }
      ],
      "text": "Seat 1 is Player A and seat 2 is Player B. All seven markers start neutral."
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
      "phase": "deal",
      "label": "shuffle and deal",
      "when": {
        "calc": "turn_number == 1"
      },
      "do": [
        {"set": {"key": "deck", "value": {"calc": "all_items"}}},
        {"set": {"key": "pile", "value": []}},
        {"set": {"key": "offer", "value": []}},
        {"set": {"key": "newdeck", "value": []}},
        {"set": {"players": "all", "key": "hand", "value": []}},
        {"set": {"players": "all", "key": "secret", "value": []}},
        {"set": {"players": "all", "key": "counts", "value": [0, 0, 0, 0, 0, 0, 0]}},
        {"set": {"players": "all", "key": "actions", "value": ["Secret", "Trade-off", "Gift", "Competition"]}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "pile", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "deck", "value": {"calc": "newdeck"}}},
        {"set": {"key": "newdeck", "value": []}},
        {"set": {"key": "drawn", "value": ""}}
      ],
      "text": "Hand {hand_number} begins. The {total_items} Items are shuffled: {cards_removed_per_hand} card goes face down out of play, each player is dealt {starting_hand_size} cards, and {deck_size_after_deal} cards form the deck. Both players regain all four actions; placed counts reset, markers stay."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the active player draws",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "1 + ((hand_number + turn_number) % 2)"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "deck[0]"
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
              "calc": "drawn"
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
              "calc": "drawn"
            },
            "if": {
              "calc": "len(deck) > 0"
            }
          }
        }
      ],
      "text": "Hand {hand_number}, turn {turn_number}: seat {active_seat} acts and draws the top card of the deck."
    },
    {
      "use": "sync",
      "phase": "draw",
      "label": "the state of play",
      "mode": "self",
      "to": "all",
      "text": "Where things stand:"
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "choose an action",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "actions"
        }
      },
      "verify": {
        "bind": "act"
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
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} uses {value}."
      },
      "text": "Hand {hand_number}, turn {turn_number}. Choose one of your unused actions: Secret (keep 1 card hidden, scored at hand end), Trade-off (discard 2 cards face down), Gift (offer 3 cards, opponent takes 1, you place 2), Competition (offer two pairs, opponent takes one pair, you place the other). You then pick the cards one at a time."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the first card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card1"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You chose {act}. Select the first card for it from your hand (for Competition, cards 1 and 2 form Pair 1)."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the second card",
      "when": {
        "calc": "chosen_action in ['Trade-off', 'Gift', 'Competition']"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card2"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "{act}: select the second card from your remaining hand."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the third card",
      "when": {
        "calc": "chosen_action in ['Gift', 'Competition']"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card3"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "{act}: select the third card from your remaining hand (for Competition, cards 3 and 4 form Pair 2)."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the fourth card",
      "when": {
        "calc": "chosen_action == 'Competition'"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card4"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Competition: select the fourth card from your remaining hand; it completes Pair 2."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "secret or trade-off",
      "when": {
        "calc": "chosen_action in ['Secret', 'Trade-off']"
      },
      "do": [
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "secret",
            "value": {
              "calc": "offer[0]"
            },
            "if": {
              "calc": "chosen_action == 'Secret' and len(offer) >= 1"
            }
          }
        },
        {
          "append": {
            "key": "pile",
            "value": {
              "calc": "offer[0]"
            },
            "if": {
              "calc": "chosen_action == 'Trade-off' and len(offer) >= 2"
            }
          }
        },
        {
          "append": {
            "key": "pile",
            "value": {
              "calc": "offer[1]"
            },
            "if": {
              "calc": "chosen_action == 'Trade-off' and len(offer) >= 2"
            }
          }
        },
        {
          "set": {
            "key": "offer",
            "value": []
          }
        }
      ],
      "text": "Seat {active_seat} used {act}; the card(s) stay hidden."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the offer is revealed",
      "when": {
        "calc": "chosen_action in ['Gift', 'Competition']"
      },
      "to": "all",
      "text": "Seat {active_seat} plays {act} and reveals, in order: {offer}. For a Gift these are card 1, card 2 and card 3. For a Competition, Pair 1 is the first two cards and Pair 2 the last two."
    },
    {
      "use": "ask",
      "phase": "resolve",
      "label": "pick from the gift",
      "when": {
        "calc": "chosen_action == 'Gift'"
      },
      "to": {
        "where": "you.seat == 3 - active_seat"
      },
      "answer": {
        "type": "choice",
        "options": ["card 1", "card 2", "card 3"]
      },
      "verify": {
        "bind": "gift_pick"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} takes {value} of the Gift."
      },
      "text": "Seat {active_seat} offers you a Gift: {offer} (card 1, card 2, card 3). The card you pick is placed on your side; the other two go to seat {active_seat}."
    },
    {
      "use": "ask",
      "phase": "resolve",
      "label": "pick from the competition",
      "when": {
        "calc": "chosen_action == 'Competition'"
      },
      "to": {
        "where": "you.seat == 3 - active_seat"
      },
      "answer": {
        "type": "choice",
        "options": ["Pair 1", "Pair 2"]
      },
      "verify": {
        "bind": "comp_pick"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} takes {value} of the Competition."
      },
      "text": "Seat {active_seat} offers you a Competition: {offer}. Pair 1 is the first two cards, Pair 2 the last two. The pair you pick is placed on your side; the other pair goes to seat {active_seat}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "place the gift",
      "when": {
        "calc": "chosen_action == 'Gift' and len(offer) >= 3"
      },
      "do": [
        {
          "set": {
            "key": "pick",
            "value": "card 1",
            "if": {
              "calc": "pick not in ['card 1', 'card 2', 'card 3']"
            }
          }
        },
        {
          "set": {
   
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {secret} (in `reveal_the_secrets_set`: 'Seat 1 reveals the secret card {secret}.'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {secret} (in `reveal_the_secrets_set`: 'Seat 2 reveals the secret card {secret}.'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "hanamikoji_compact",
    "name": "Hanamikoji: Compact Build",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players spend four one-use actions each hand to win the favour of seven Geisha: first to 11 Charm or 4 Geisha at a hand's end wins."
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
        "key": "counts",
        "visible": "public",
        "type": "list",
        "initial": [0, 0, 0, 0, 0, 0, 0]
      },
      {
        "key": "actions",
        "visible": "public",
        "type": "list",
        "initial": ["Secret", "Trade-off", "Gift", "Competition"]
      },
      {
        "key": "charm",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "geisha",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "markers",
        "visible": "public",
        "type": "list",
        "initial": ["N", "N", "N", "N", "N", "N", "N"]
      },
      {
        "key": "charm_values",
        "visible": "public",
        "type": "list",
        "initial": [2, 2, 2, 3, 3, 4, 5]
      },
      {
        "key": "standing",
        "visible": "public",
        "type": "list",
        "initial": [0, 0, 0, 0]
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "turn_number",
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
        "key": "offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "pick_index",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "drawn",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "newdeck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "secret_a",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "secret_b",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "geisha_names",
        "visible": "none",
        "type": "list",
        "initial": ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]
      },
      {
        "key": "geisha_index",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6]
      },
      {
        "key": "all_items",
        "visible": "none",
        "type": "list",
        "initial": ["G1", "G1", "G2", "G2", "G3", "G3", "G4", "G4", "G4", "G5", "G5", "G5", "G6", "G6", "G6", "G6", "G7", "G7", "G7", "G7", "G7"]
      },
      {
        "key": "charm_g1",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "charm_g2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "charm_g3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "charm_g4",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "charm_g5",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "charm_g6",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "charm_g7",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "total_charm",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "total_items",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "items_per_geisha_equals_charm",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "geisha_count",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "max_hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "turns_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cards_removed_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_hand_size",
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
        "key": "cards_drawn_per_turn",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "gift_cards_to_opponent",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "competition_cards_per_pair",
        "visible": "public",
        "type": "number",
        "initial": 2
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
        "initial": 4
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
      "do": [
        {
          "set": {
            "key": "charm_values",
            "value": {
              "calc": "[charm_g1, charm_g2, charm_g3, charm_g4, charm_g5, charm_g6, charm_g7]"
            }
          }
        },
        {
          "set": {
            "key": "markers",
            "value": ["N", "N", "N", "N", "N", "N", "N"]
          }
        },
        {
          "set": {
            "key": "standing",
            "value": [0, 0, 0, 0]
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
            "key": "geisha",
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
            "key": "turn_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        }
      ],
      "text": "Seat 1 is Player A and seat 2 is Player B. All seven markers start neutral."
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
      "phase": "deal",
      "label": "shuffle and deal",
      "when": {
        "calc": "turn_number == 1"
      },
      "do": [
        {"set": {"key": "deck", "value": {"calc": "all_items"}}},
        {"set": {"key": "pile", "value": []}},
        {"set": {"key": "offer", "value": []}},
        {"set": {"key": "newdeck", "value": []}},
        {"set": {"players": "all", "key": "hand", "value": []}},
        {"set": {"players": "all", "key": "secret", "value": []}},
        {"set": {"players": "all", "key": "counts", "value": [0, 0, 0, 0, 0, 0, 0]}},
        {"set": {"players": "all", "key": "actions", "value": ["Secret", "Trade-off", "Gift", "Competition"]}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "pile", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "1 + ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": {"calc": "2 - ((hand_number + 1) % 2)"}, "key": "hand", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "drawn", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "newdeck", "value": {"calc": "drawn"}}},
        {"remove": {"key": "deck", "value": {"calc": "drawn"}}},
        {"set": {"key": "deck", "value": {"calc": "newdeck"}}},
        {"set": {"key": "newdeck", "value": []}},
        {"set": {"key": "drawn", "value": ""}}
      ],
      "text": "Hand {hand_number} begins. The {total_items} Items are shuffled: {cards_removed_per_hand} card goes face down out of play, each player is dealt {starting_hand_size} cards, and {deck_size_after_deal} cards form the deck. Both players regain all four actions and placed counts reset to zero; markers and standing stay."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the active player draws",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "1 + ((hand_number + turn_number) % 2)"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "deck[0]"
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
              "calc": "drawn"
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
              "calc": "drawn"
            },
            "if": {
              "calc": "len(deck) > 0"
            }
          }
        }
      ],
      "text": "Hand {hand_number}, turn {turn_number}: seat {active_seat} acts and draws the top card of the deck."
    },
    {
      "use": "sync",
      "phase": "draw",
      "label": "the state of play",
      "mode": "self",
      "to": "all",
      "text": "Where things stand:"
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "choose an action",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "actions"
        }
      },
      "verify": {
        "bind": "act"
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
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} uses {value}."
      },
      "text": "Hand {hand_number}, turn {turn_number}. Choose one of your unused actions: Secret (keep 1 card hidden, scored at hand end), Trade-off (discard 2 cards face down), Gift (offer 3 cards, opponent takes 1, you place 2), Competition (offer two pairs, opponent takes one pair, you place the other). You then select the cards one at a time."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the first card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card1"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You chose {chosen_action}. Select the first card for it from your hand (for Competition, cards 1 and 2 form Pair 1)."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the second card",
      "when": {
        "calc": "chosen_action in ['Trade-off', 'Gift', 'Competition']"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card2"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "{chosen_action}: select the second card from your remaining hand."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the third card",
      "when": {
        "calc": "chosen_action in ['Gift', 'Competition']"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card3"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "{chosen_action}: select the third card from your remaining hand (for Competition, cards 3 and 4 form Pair 2)."
    },
    {
      "use": "ask",
      "phase": "choose",
      "label": "select the fourth card",
      "when": {
        "calc": "chosen_action == 'Competition'"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card4"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "offer",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Competition: select the fourth card from your remaining hand; it completes Pair 2."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "secret or trade-off",
      "when": {
        "calc": "chosen_action in ['Secret', 'Trade-off']"
      },
      "do": [
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "secret",
            "value": {
              "calc": "offer[0]"
            },
            "if": {
              "calc": "chosen_action == 'Secret' and len(offer) >= 1"
            }
          }
        },
        {
          "append": {
            "key": "pile",
            "value": {
              "calc": "offer[0]"
            },
            "if": {
              "calc": "chosen_action == 'Trade-off' and len(offer) >= 2"
            }
          }
        },
        {
          "append": {
            "key": "pile",
            "value": {
              "calc": "offer[1]"
            },
            "if": {
              "calc": "chosen_action == 'Trade-off' and len(offer) >= 2"
            }
          }
        },
        {
          "set": {
            "key": "offer",
            "value": []
          }
        }
      ],
      "text": "Seat {active_seat} used {chosen_action}; the card(s) stay hidden."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the offer is revealed",
      "when": {
        "calc": "chosen_action in ['Gift', 'Competition']"
      },
      "to": "all",
      "text": "Seat {active_seat} plays {chosen_action} and reveals, in order: {offer}. For a Gift these are card 1, card 2 and card 3. For a Competition, Pair 1 is the first two cards and Pair 2 the last two."
    },
    {
      "use": "ask",
      "phase": "resolve",
      "label": "pick from the gift",
      "when": {
        "calc": "chosen_action == 'Gift'"
      },
      "to": {
        "where": "you.seat == 3 - active_seat"
      },
      "answer": {
        "type": "choice",
        "options": ["card 1", "card 2", "card 3"]
      },
      "verify": {
        "bind": "gift_pick"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} takes {value} of the Gift."
      },
      "text": "Seat {active_seat} offers you a Gift: {offer} (card 1, card 2, card 3). The card you pick is placed on your side; the other two are placed on seat {active_seat}'s side."
    },
    {
      "use": "ask",
      "phase": "resolve",
      "label": "pick from the competition",
      "when": {
        "calc": "chosen_action == 'Competition'"
      },
      "to": {
        "where": "you.seat == 3 - active_seat"
      },
      "answer": {
        "type": "choice",
        "options": ["Pair 1", "Pair 2"]
      },
      "verify": {
        "bind": "comp_pick"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} takes {value} of the Competition."
      },
      "text": "Seat {active_seat} offers you a Competition: {offer}. Pair 1 is the first two cards, Pair 2 the last two. The pair you pick is placed on your side; the other pair is placed on seat {active_seat}'s side."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "place the offer",
      "when": {
        "calc": "chosen_action in ['Gift', 'Competition']"
      },
      "do": [
        {
          "set": {
            "key": "pick",
            "value": "card 1",
            "if": {
              "calc": "chosen_action == 'Gift' and pick not in ['card 1', 'card 2', 'card 3']"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": "Pair 1",
            "if": {
              "calc": "chosen_action == 'Competition' and pick not in ['Pair 1', 'Pair 2']"
            }
          }
        },
        {
          "set": {
            "key": "pick_index",
            "value": {
              "calc": "1 if pick in ['card 2', 'Pair 2'] else (2 if pick == 'card 3' else 0)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3 - active_seat"
            },
            "key": "counts",
            "value": {
              "calc": "[you.counts[i] + (1 if offer[pick_index] == geisha_names[i] else 0) for i in geisha_index]"
            },
            "if": {
              "calc": "chosen_action == 'Gift' and len(offer) >= 3"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "counts",
            "value": {
              "calc": "[you.counts[i] + count(j != pick_index and offer[j] == geisha_names[i] for j in [0, 1, 2]) for i in geisha_index]"
            },
            "if": {
              "calc": "chosen_action == 'Gift' and len(offer) >= 3"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3 - active_seat"
            },
            "key": "counts",
            "value": {
              "calc": "[you.counts[i] + count(offer[j] == geisha_names[i] for j in [2 * pick_index, 2 * pick_index + 1]) for i in geisha_index]"
            },
            "if": {
              "calc": "chosen_action == 'Competition' and len(offer) >= 4"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "counts",
            "value": {
              "calc": "[you.counts[i] + count(offer[j] == geisha_names[i] for j in [2 - 2 * pick_index, 3 - 2 * pick_index]) for i in geisha_index]"
            },
            "if": {
              "calc": "chosen_action == 'Competition' and len(offer) >= 4"
            }
          }
        }
      ],
      "text": "Placement: seat {active_seat}'s {chosen_action} of {offer} is placed; the opponent took {pick}, the rest go to seat {active_seat}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "end of turn",
      "do": [
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "actions",
            "value": {
              "calc": "chosen_action"
            },
            "if": {
              "calc": "chosen_action != ''"
            }
          }
        },
        {
          "set": {
            "key": "offer",
            "value": []
          }
        },
        {
          "set": {
            "key": "chosen_action",
            "value": ""
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        },
        {
          "adjust": {
            "key": "turn_number",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "reveal secrets and score markers",
      "when": {
        "calc": "turn_number == turns_per_hand + 1"
      },
      "do": [
        {
          "set": {
            "key": "secret_a",
            "value": {
              "calc": "players[0].secret[0] if len(players[0].secret) > 0 else 'none'"
            }
          }
        },
        {
          "set": {
            "key": "secret_b",
            "value": {
              "calc": "players[1].secret[0] if len(players[1].secret) > 0 else 'none'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "counts",
            "value": {
              "calc": "[you.counts[i] + count(c == geisha_names[i] for c in you.secret) for i in geisha_index]"
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
            "key": "markers",
            "value": {
              "calc": "[('A' if players[0].counts[i] > players[1].counts[i] else ('B' if players[1].counts[i] > players[0].counts[i] else markers[i])) for i in geisha_index]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "charm",
            "value": {
              "calc": "sum([charm_values[i] for i in geisha_index if markers[i] == ('A' if you.seat == 1 else 'B')])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "geisha",
            "value": {
              "calc": "count(markers[i] == ('A' if you.seat == 1 else 'B') for i in geisha_index)"
            }
          }
        },
        {
          "set": {
            "key": "standing",
            "value": {
              "calc": "[players[0].charm, players[1].charm, players[0].geisha, players[1].geisha]"
            }
          }
        }
      ],
      "text": "Turn 8 is over. Secrets revealed: seat 1 kept {secret_a}, seat 2 kept {secret_b}; each is added to its owner's counts."
    },
    {
      "use": "tell",
      "phase": "scoring",
      "label": "announce the markers",
      "when": {
        "calc": "turn_number == turns_per_hand + 1"
      },
      "to": "all",
      "text": "End of hand {hand_number}. Markers G1..G7 (A = seat 1, B = seat 2, N = neutral): {markers}. Standing [seat 1 Charm, seat 2 Charm, seat 1 Geisha, seat 2 Geisha]: {standing}."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the hand",
      "when": {
        "calc": "turn_number == turns_per_hand + 1"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "the next hand",
      "when": {
        "calc": "turn_number == turns_per_hand + 1"
      },
      "do": [
        {
          "adjust": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "turn_number",
            "value": 1
          }
        }
      ],
      "text": "Hand {hand_number} is next; the other player acts first."
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "turn_number == turns_per_hand + 1 and (max([p.charm for p in players]) >= charm_to_win or max([p.geisha for p in players]) >= geisha_to_win or hand_number >= max_hands)"
      },
      "rank_by": "you.charm * 10 + you.geisha",
      "text": "Winner: {result}. Final standing: Seat 1 {players[0].charm} Charm and {players[0].geisha} Geisha; Seat 2 {players[1].charm} Charm and {players[1].geisha} Geisha."
    }
  },
  "limits": {
    "rounds": 32,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Seat 1 is Player A and seat 2 is Player B. There are seven Geisha, G1 to G7, with Charm {charm_g1}, {charm_g2}, {charm_g3}, {charm_g4}, {charm_g5}, {charm_g6} and {charm_g7} ({total_charm} in total). There are {total_items} Item cards: each Geisha has as many Items as her Charm (two G1, two G2, two G3, three G4, three G5, four G6, five G7). A card is named by its Geisha, for example 'G6'. You may use this known composition to deduce unseen cards.\n\nThe game lasts at most {max_hands} hands of {turns_per_hand} turns. At the start of each hand all {total_items} Items are shuffled: {cards_removed_per_hand} card goes face down out of play into the pile, the first player of the hand is dealt {starting_hand_size} cards, the other player {starting_hand_size} cards, and the remaining {deck_size_after_deal} form the deck. Both players get back all four actions (Secret, Trade-off, Gift, Competition), both placed counts reset to zero and both secrets are emptied. Markers and standing are NOT reset.\n\nIn hands 1 and 3 seat 1 acts on odd turns and seat 2 on even turns; in hands 2 and 4 seat 2 acts on odd turns and seat 1 on even turns. On your turn you first draw the top card of the deck to the end of your hand. Then you choose one unused action and select its cards one at a time from your hand:\n- Secret ({secret_cards} card): the card becomes your secret, hidden from your opponent until the end of the hand.\n- Trade-off ({tradeoff_cards} cards): both cards go face down to the pile, which is never revealed.\n- Gift ({gift_cards} cards): the cards are revealed as card 1, card 2, card 3. Your opponent picks one: the picked card adds 1 to the opponent's count for its Geisha, and the other two add 1 each to your counts.\n- Competition ({competition_cards} cards): the cards are revealed as Pair 1 (cards 1-2) and Pair 2 (cards 3-4). Your opponent picks one pair: its two cards add to the opponent's counts, and the other pair adds to your counts.\nYou are only offered actions you have not used this hand and cards you actually hold; a used action is gone for the rest of the hand, so each player uses each action exactly once per hand. An invalid action or card choice becomes your first unused action (order Secret, Trade-off, Gift, Competition) with the first cards of your hand; an invalid pick becomes card 1 or Pair 1. Placed cards, counts, offers, picks, markers, standing and spent actions are public; hands and secrets are private.\n\nAfter turn 8 both secrets are revealed and each adds 1 to its owner's count for its Geisha. Then for each Geisha, the player with strictly more placed cards takes her marker; on a tie the marker stays where it was. Your Charm is the total Charm of the Geisha whose markers are on your side, and your Geisha is how many markers you hold.\n\nAt the end of each hand: a player with {charm_to_win} or more Charm wins. Otherwise a player with {geisha_to_win} or more Geisha wins. Otherwise, if it was hand {max_hands}, the higher Charm wins, then more Geisha; if both are equal the game is a draw (shared win). If the game does not end, the next hand begins and the other player acts first."
}
```
````
