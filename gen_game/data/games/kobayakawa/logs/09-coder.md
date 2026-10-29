# 09 coder

- time: 2026-10-27T08:45:09+00:00 (182.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 ee9f64a8098cda9a, reply sha256 76ff878f16e513d5

## Sent

````
# Task: write the XColos game file for "Kobayakawa: Held Cards"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: Each player starts with 4 kamons and sits in a numbered seat (1 to N). The centre holds 11 kamons and the pot starts at 0. Nobody holds a card. The start player for round 1 is seat 1. The game lasts 10 rounds, or ends sooner if only one player remains.

EACH ROUND:
1. DEAL (the round's only random event). Shuffle all cards numbered 1 to 15 except the hand cards currently held by players. Each active player without a hand card receives one, seen only by that player. Every active player then receives one RESERVE card, face down and unseen. Then deal the KOBAYAKAWA face up and the ALTERNATE face down.
2. ANNOUNCE. The engine announces:
   - the round number;
   - the Kobayakawa value and the current pot;
   - each player's kamons;
   - which players are holding a card kept from an earlier round, and for how many rounds;
   - the start player;
   - the minimum stake: 1 in rounds 1-9, 2 in round 10.
3. DRAW CHOICE (simultaneous). Each active player secretly chooses one option:
   - KEEP: keep your hand card.
   - DRAW: look at your reserve card.
   - SHIFT: vote to replace the Kobayakawa.
4. Each player who chose DRAW privately sees their reserve card.
5. KEEP CHOICE (simultaneous, drawers only). Each drawer keeps OLD (the hand card) or NEW (the reserve card) as their hand card. The other card is discarded face up. All undrawn reserve cards are discarded face down, unseen.
6. REVEAL. The engine announces each player's draw choice and all face-up discards.
7. SHIFT. If at least one player chose SHIFT, the Alternate replaces the Kobayakawa and its value is announced.
8. TALK (simultaneous). Every active player writes one short message without seeing the others; all messages are then shown. Talk is not binding and may be false.
9. FIGHT (sequential). Players act once each in seat order, beginning with the start player and wrapping around. Each player sees all earlier choices.
   - The REQUIRED STAKE is the minimum stake, or the minimum + 1 if any earlier player this round fought HIGH.
   - A player chooses PASS, FIGHT LOW (stake = minimum, allowed only while nobody has fought HIGH) or FIGHT HIGH (stake = minimum + 1).
   - A player must PASS if they have fewer kamons than every stake they are allowed to choose.
10. STAKE. Each fighter pays their stake into the pot. The engine moves centre kamons into the pot: 1 in rounds 1-9, and all remaining centre kamons in round 10.
11. SCORE.
   - Nobody fought: the pot carries to the next round.
   - Exactly one fighter: that player takes the whole pot, and their card is not revealed.
   - Two or more fighters: all fighters' cards are revealed. Each fighter's total is their card value. The fighter with the lowest card adds the Kobayakawa value to their total. The highest total takes the whole pot.
12. TIES. If fighters share the highest total, nobody takes the pot and it carries to the next round. In round 10, the pot is instead split equally among the tied fighters, rounding down, and any remainder is removed from the game.
13. CLEANUP.
   - Every fighter's hand card is discarded; that player will receive a fresh card next round.
   - Every player who passed keeps their hand card, still secret.
   - The next start player is the pot winner. If nobody won the pot, it is the next active seat after this round's start player.
14. ELIMINATION. Any player with 0 kamons is eliminated, and their card is discarded unseen.
15. END CHECK. The game ends after round 10, or as soon as only one active player remains.

How the winner is decided: When the game ends, the player with the most kamons wins. If two or more players tie for the most, the game is a draw. If only one active player remains before round 10, that player wins.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Kobayakawa: Held Cards (3 to 5 players, best with 4)

A bluffing and betting game over 10 rounds. Each player holds one secret card and may keep, swap or shift the bonus card, then decides in seat order whether to fight for the kamon pot. A passer may carry their card into later rounds.

STATE (every item below must exist in the file):
  - each player: kamons (number, starts 4); everyone sees it. the player's kamons; this is the score
  - each player: active (bool, starts True); everyone sees it. false once the player is eliminated at 0 kamons
  - each player: hand (number, starts 0); only its owner sees it. the player's secret hand card, 1-15, or 0 for no card
  - each player: held_rounds (number, starts 0); everyone sees it. how many earlier rounds the current hand card has been kept through by passing; 0 means a fresh card
  - each player: reserve_seen (number, starts 0); only its owner sees it. the reserve card's value, shown only to a player who chose DRAW, otherwise 0
  - each player: draw_choice (text, starts ''); everyone sees it. this round's KEEP, DRAW or SHIFT; gathered by a simultaneous poll and revealed at step 6
  - each player: keep_choice (text, starts ''); only its owner sees it. OLD or NEW, set for drawers only
  - each player: fight_choice (text, starts ''); everyone sees it. this round's PASS, LOW or HIGH
  - each player: stake (number, starts 0); everyone sees it. kamons staked this round
  - each player: shown_card (number, starts 0); everyone sees it. the fighter's card once revealed in a showdown, otherwise 0
  - each player: total (number, starts 0); everyone sees it. the fighter's showdown total: the card, plus the Kobayakawa if it is the lowest fighter's card
  - the table: round (number, starts 1); everyone sees it. the current round, 1-10
  - the table: pot (number, starts 0); everyone sees it. kamons in the pot
  - the table: centre (number, starts 11); everyone sees it. kamons left in the centre
  - the table: deck (list, starts []); hidden from all players. the shuffled cards 1-15, less the hand cards held by players, rebuilt each round
  - the table: reserves (list, starts []); hidden from all players. the face-down reserve cards, one per active seat in seat order, unseen by all
  - the table: kobayakawa (number, starts 0); everyone sees it. the face-up Kobayakawa value
  - the table: alternate (number, starts 0); hidden from all players. the face-down Alternate card
  - the table: face_up_discards (list, starts []); everyone sees it. cards discarded face up this round
  - the table: start_seat (number, starts 1); everyone sees it. the seat that acts first in the fight
  - the table: min_stake (number, starts 1); everyone sees it. the minimum stake: 1 in rounds 1-9, 2 in round 10
  - the table: high_fought (bool, starts False); everyone sees it. true once anyone has fought HIGH this round
  - the table: winner_seat (number, starts 0); everyone sees it. the seat that took the pot this round, or 0 for none
  - parameters, each kept as a table attribute: starting_kamons = 4, centre_kamons = 11, starting_pot = 0, card_min = 1, card_max = 15, total_rounds = 10, min_stake_rounds_1_to_9 = 1, min_stake_round_10 = 2, high_stake_extra = 1, centre_feed_rounds_1_to_9 = 1, first_start_seat = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat players 1 to N.
  2. Set each player's kamons to 4, active to true, hand to 0 and held_rounds to 0.
  3. Set centre to 11, pot to 0, round to 1 and start_seat to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] engine. What happens: Set min_stake = 1 if round <= 9, else 2. Set high_fought = false and winner_seat = 0. Clear face_up_discards, and clear each player's draw_choice, keep_choice, fight_choice, stake, shown_card, total and reserve_seen. Set deck = the cards 1..15 minus every active player's hand (where hand > 0), then shuffle it.
  2. [update] each active player with hand = 0. What happens: Draw one card at random from deck into hand (visible only to the owner) and remove it from deck.
  3. [update] each active player. What happens: Draw one card at random from deck and append it to reserves at that seat's position; remove it from deck. Nobody sees it.
  4. [update] engine. What happens: Draw one card from deck into kobayakawa (public) and one into alternate (hidden), removing each from deck.
  5. [tell] all players. What happens: Announce round, kobayakawa, pot, every player's kamons, every player with held_rounds > 0 and their held_rounds, start_seat, and min_stake.
  6. [sync] all players. What happens: Each player is sent their own state, including their hand.
  7. [poll] all active players answers: one of KEEP, DRAW, SHIFT. What happens: Store the answer in draw_choice. It is not shown until step 6.
  8. [update] each active player with draw_choice = DRAW. What happens: Set reserve_seen = that seat's card in reserves; only the owner sees it.
  9. [poll] active players with draw_choice = DRAW answers: one of OLD, NEW. What happens: Store the answer in keep_choice. If NEW: append hand to face_up_discards, then set hand = reserve_seen. If OLD: append reserve_seen to face_up_discards. Then clear reserves; undrawn reserves are discarded face down, unseen. If a player chose NEW, set held_rounds = 0.
  10. [tell] all players. What happens: Announce every active player's draw_choice and the contents of face_up_discards.
  11. [update] engine. What happens: If the count of players with draw_choice = SHIFT is >= 1, set kobayakawa = alternate and announce the new kobayakawa.
  12. [poll] all active players answers: short text. What happens: Broadcast every message to all as {"to": "all", "text": "Seat {seat} says: {value}"}. Talk is not binding.
  13. [ask] each active player in turn, in seat order starting at start_seat and wrapping around answers: one of the options allowed for this seat: PASS; LOW if high_fought = false and kamons >= min_stake; HIGH if kamons >= min_stake + 1. What happens: Store the answer in fight_choice. If LOW, set stake = min_stake. If HIGH, set stake = min_stake + 1 and high_fought = true. If PASS, set stake = 0.
  14. [update] engine. What happens: For each player: kamons -= stake and pot += stake. Then the centre feeds the pot: if round <= 9, move min(1, centre) from centre to pot; if round = 10, move all of centre to pot.
  15. [update] engine. What happens: Let F = the number of players with fight_choice in {LOW, HIGH}. If F = 1, set winner_seat = that fighter and move the whole pot to their kamons; their card is not revealed. If F >= 2: for each fighter set shown_card = hand and total = hand, and add kobayakawa to the total of the fighter with the lowest hand. If exactly one fighter has the highest total, move the whole pot to them and set winner_seat to their seat. If F = 0, the pot carries.
  16. [update] engine. What happens: If F >= 2 and two or more fighters share the highest total: if round <= 9, the pot carries. If round = 10, each tied fighter gains floor(pot / number tied), and pot is set to 0 (the remainder leaves the game).
  17. [tell] all players. What happens: Announce every fight_choice, every shown_card and total, the pot result, and every player's kamons.
  18. [update] engine. What happens: Each fighter sets hand = 0 and held_rounds = 0. Each active passer keeps hand and adds 1 to held_rounds. For each active player with kamons = 0, set active = false and hand = 0 (their card is discarded unseen). Then set start_seat = winner_seat if winner_seat > 0; otherwise the next active seat after the old start_seat, wrapping. Then add 1 to round.
  19. [check] engine. What happens: End the game if round > 10 or the count of active players <= 1. Otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, then each player has 4 kamons, the centre has 11, the pot is 0, the start seat is 1, and nobody holds a card.
  R2. When a round begins, then the deck is the cards 1-15 minus the hand cards held by active players.
  R3. When a round begins, then each active player with no hand card is dealt one hand card, seen only by them.
  R4. When a round begins, then each active player is dealt one face-down reserve card that nobody sees, then a face-up Kobayakawa and a face-down Alternate are dealt.
  R5. When the round is 1-9, then the minimum stake is 1; when the round is 10, then it is 2.
  R6. When the round is announced, then the announcement gives the round, the Kobayakawa, the pot, every player's kamons, the players holding a kept card with its held_rounds, the start seat and the minimum stake.
  R7. When the draw choice is made, then every active player chooses KEEP, DRAW or SHIFT at the same time, and no choice is seen until all are in.
  R8. When a player chose DRAW, then they alone see their reserve card.
  R9. When a drawer chooses NEW, then the reserve card becomes their hand and the old hand card is discarded face up; when they choose OLD, then the reserve card is discarded face up.
  R10. When drawers have chosen, then every undrawn reserve card is discarded face down and stays unseen.
  R11. When the draw choices are revealed, then every player's draw choice and every face-up discard is announced.
  R12. When at least 1 player chose SHIFT, then the Alternate replaces the Kobayakawa and the new value is announced; when no player chose SHIFT, then the Kobayakawa is unchanged.
  R13. When the talk step runs, then every active player writes one short message at the same time, and all messages are shown to everyone.
  R14. When the fight runs, then each active player acts once, in seat order starting at the start seat and wrapping around, and sees all earlier choices.
  R15. When nobody earlier this round has fought HIGH and the player has at least the minimum stake in kamons, then FIGHT LOW is offered at a stake equal to the minimum.
  R16. When the player has at least the minimum stake + 1 in kamons, then FIGHT HIGH is offered at a stake of the minimum + 1.
  R17. When any earlier player this round fought HIGH, then FIGHT LOW is not offered.
  R18. When a player has fewer kamons than every stake they are allowed, then only PASS is offered.
  R19. When the fight ends, then each fighter pays their stake into the pot.
  R20. When the fight ends in rounds 1-9, then 1 kamon moves from the centre to the pot if the centre has any.
  R21. When the fight ends in round 10, then all remaining centre kamons move to the pot.
  R22. When nobody fights, then the pot carries to the next round.
  R23. When exactly one player fights, then they take the whole pot and their card is not revealed.
  R24. When two or more players fight, then all fighters' cards are revealed, the fighter with the lowest card adds the Kobayakawa value to it, and the unique highest total takes the whole pot.
  R25. When fighters tie for the highest total in rounds 1-9, then nobody takes the pot and it carries.
  R26. When fighters tie for the highest total in round 10, then each tied fighter gets floor(pot / number tied), and the remainder leaves the game.
  R27. When a round is cleaned up, then each fighter's hand card is discarded and their held_rounds is set to 0, and each passer keeps their card and adds 1 to held_rounds.
  R28. When a player wins the pot, then they are the next start player; when nobody wins it, then the next start player is the next active seat after this round's start seat.
  R29. When a player has 0 kamons at the end of a round, then they are eliminated and their card is discarded unseen.
  R30. When round 10 ends, or when only 1 active player remains, then the game ends, and the most kamons wins.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Draw choice | asked: every active seat | options: KEEP, DRAW, SHIFT
  - Keep choice | asked: every active seat that chose DRAW | options: OLD, NEW
  - Talk | asked: every active seat | options: a short free-text message
  - Fight | asked: each active seat in turn from the start seat | options: no HIGH fought yet and kamons >= min+1: PASS, LOW, HIGH. No HIGH fought yet and kamons = min: PASS, LOW. HIGH already fought and kamons >= min+1: PASS, HIGH. Any other case: PASS only.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 10 or count(active players) <= 1
  - each player's standing: you.kamons (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with the most kamons wins. Eliminated players have 0. If only one player remains active, that player has the most kamons and wins. Players tied for the most share the result, which stands for the source's draw.
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

- each player: `kamons` (number, visible: public, starts 4): the player's kamons; this is the score
- each player: `active` (bool, visible: public, starts True): false once the player is eliminated at 0 kamons
- each player: `held_rounds` (number, visible: public, starts 0): how many earlier rounds the current hand card has been kept through by passing; 0 means a fresh card
- each player: `draw_choice` (text, visible: public, starts ''): this round's KEEP, DRAW or SHIFT; gathered by a simultaneous poll and revealed at step 6
- each player: `fight_choice` (text, visible: public, starts ''): this round's PASS, LOW or HIGH
- the table: `round` (number, visible: public, starts 1): the current round, 1-10
- the table: `pot` (number, visible: public, starts 0): kamons in the pot
- the table: `centre` (number, visible: public, starts 11): kamons left in the centre
- the table: `kobayakawa` (number, visible: public, starts 0): the face-up Kobayakawa value
- the table: `start_seat` (number, visible: public, starts 1): the seat that acts first in the fight
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_kamons = 4, centre_kamons = 11, starting_pot = 0, card_min = 1, card_max = 15, total_rounds = 10, min_stake_rounds_1_to_9 = 1, min_stake_round_10 = 2, high_stake_extra = 1, centre_feed_rounds_1_to_9 = 1, first_start_seat = 1
- the game ends with ONE ending whose `rank_by` is `you.kamons`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "kobayakawa_held_cards",
    "name": "Kobayakawa: Held Cards",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Hold one secret card, keep, draw or shift the bonus card, then fight in seat order for the kamon pot over ten rounds."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "kamons",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "active",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "held_rounds",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reserve_seen",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "draw_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "keep_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "fight_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "stake",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "shown_card",
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
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pot",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "centre",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reserves",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "kobayakawa",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "alternate",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "face_up_discards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "start_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_stake",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "high_fought",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "winner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_kamons",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "centre_kamons",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "starting_pot",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "card_max",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "min_stake_rounds_1_to_9",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_stake_round_10",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "high_stake_extra",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "centre_feed_rounds_1_to_9",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_start_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [
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
          11,
          12,
          13,
          14,
          15
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fight_turn",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fighters",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_total",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seat the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "kamons",
            "value": {
              "calc": "starting_kamons"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "active",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "held_rounds",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the centre",
      "do": [
        {
          "set": {
            "key": "centre",
            "value": {
              "calc": "centre_kamons"
            }
          }
        },
        {
          "set": {
            "key": "pot",
            "value": {
              "calc": "starting_pot"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "first_start_seat"
            }
          }
        }
      ]
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
      "label": "a new round",
      "do": [
        {
          "set": {
            "key": "min_stake",
            "value": {
              "calc": "min_stake_rounds_1_to_9 if round < total_rounds else min_stake_round_10"
            }
          }
        },
        {
          "set": {
            "key": "high_fought",
            "value": false
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "face_up_discards",
            "value": []
          }
        },
        {
          "set": {
            "key": "reserves",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "draw_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "keep_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "fight_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stake",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shown_card",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "reserve_seen",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in all_cards if c >= card_min and c <= card_max and c not in [p.hand for p in players if p.active and p.hand > 0]]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 1 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 1 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 1 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 2 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 2 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 2 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 3 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 3 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 3 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 4 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 4 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 4 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 5 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 5 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "player": 5,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 5 and p.active and p.hand == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 1 and p.active for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 1 and p.active for p in players)"
            }
          }
        },
        {
          "append": {
            "key": "reserves",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 1 and p.active for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 2 and p.active for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 2 and p.active for p in players)"
            }
          }
        },
        {
          "append": {
            "key": "reserves",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 2 and p.active for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 3 and p.active for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 3 and p.active for p in players)"
            }
          }
        },
        {
          "append": {
            "key": "reserves",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 3 and p.active for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 4 and p.active for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 4 and p.active for p in players)"
            }
          }
        },
        {
          "append": {
            "key": "reserves",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 4 and p.active for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "any(p.seat == 5 and p.active for p in players)"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 5 and p.active for p in players)"
            }
          }
        },
        {
          "append": {
            "key": "reserves",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "any(p.seat == 5 and p.active for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "kobayakawa",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "alternate",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "the round is announced",
      "to": "all",
      "text": "Round {round} of {total_rounds}. Kobayakawa: {kobayakawa}. Pot: {pot}. Kamons [seat, kamons]: {[[p.seat, p.kamons] for p in players]}. Players holding a kept card [seat, rounds held]: {[[p.seat, p.held_rounds] for p in players if p.active and p.held_rounds > 0]}. Start seat: {start_seat}. Minimum stake: {min_stake}."
    },
    {
      "use": "sync",
      "phase": "announce",
      "label": "your hand",
      "mode": "self",
      "to": "acting",
      "text": "Your state this round:"
    },
    {
      "use": "poll",
      "phase": "draw",
      "label": "draw choice",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "KEEP",
          "DRAW",
          "SHIFT"
        ]
      },
      "store": "draw_choice",
      "text": "Your hand card is {hand}. The Kobayakawa is {kobayakawa}. Choose in secret: KEEP (keep your hand card), DRAW (look at your face-down reserve card, then keep either card) or SHIFT (vote to replace the Kobayakawa with the face-down Alternate). Nobody sees the choices until all are in."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "drawers look at their reserve",
      "when": {
        "calc": "count(p.draw_choice == 'DRAW' for p in acting) > 0"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.active and you.draw_choice == 'DRAW'"
            },
            "key": "reserve_seen",
            "value": {
              "calc": "reserves[count(p.active and p.seat < you.seat for p in players)]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "draw",
      "label": "keep choice",
      "when": {
        "calc": "count(p.draw_choice == 'DRAW' for p in acting) > 0"
      },
      "to": {
        "where": "you.active and you.draw_choice == 'DRAW'"
      },
      "answer": {
        "type": "choice",
        "options": [
          "OLD",
          "NEW"
        ]
      },
      "store": "keep_choice",
      "text": "Your hand card is {hand}; your reserve card is {reserve_seen}. Keep OLD (your hand card; the reserve card is discarded face up) or NEW (the reserve card becomes your hand; your old hand card is discarded face up)."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "drawers keep a card",
      "do": [
        {
          "set": {
            "key": "face_up_discards",
            "value": {
              "calc": "[p.hand if p.keep_choice == 'NEW' else p.reserve_seen for p in players if p.keep_choice in ['NEW', 'OLD']]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.keep_choice == 'NEW'"
            },
            "key": "hand",
            "value": {
              "calc": "you.reserve_seen"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.keep_choice == 'NEW'"
            },
            "key": "held_rounds",
            "value": 0
          }
        },
        {
          "set": {
            "key": "reserves",
            "value": []
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the draw choices",
      "to": "all",
      "text": "Draw choices [seat, choice]: {[[p.seat, p.draw_choice] for p in players if p.active]}. Face-up discards: {face_up_discards}. All undrawn reserve cards are discarded face down, unseen."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the shift",
      "when": {
        "calc": "count(p.draw_choice == 'SHIFT' for p in acting) >= 1"
      },
      "do": [
        {
          "set": {
            "key": "kobayakawa",
            "value": {
              "calc": "alternate"
            }
          }
        }
      ],
      "text": "At least one player chose SHIFT: the Alternate replaces the Kobayakawa. The Kobayakawa is now {kobayakawa}."
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
      "text": "Say one short thing to the table. Talk is not binding and may be false."
    },
    {
      "use": "update",
      "phase": "fight",
      "label": "the fight begins",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.active"
            },
            "key": "fight_choice",
            "value": "PASS"
          }
        },
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "start_seat"
            }
          }
        },
        {
          "set": {
            "key": "fight_turn",
            "value": 0
          }
        },
        {
          "set": {
            "players": "acting",
            "key": "offer",
            "value": {
              "calc": "['PASS'] + (['LOW'] if not high_fought and you.kamons >= min_stake else []) + (['HIGH'] if you.kamons >= min_stake + high_stake_extra else [])"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "label": "the fight",
      "until": {
        "calc": "fight_turn >= count(p.active for p in players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "fight",
          "label": "fight",
          "to": {
            "where": "you.seat == cur_seat and len(you.offer) > 1"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "store": "fight_choice",
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} chooses {value}."
          },
          "text": "Your hand card is {hand}; the Kobayakawa is {kobayakawa}; the pot is {pot}. Choose PASS, or fight from the options offered. LOW stakes {min_stake}; HIGH stakes {min_stake} + {high_stake_extra}. Someone has already fought HIGH this round: {high_fought}."
        },
        {
          "use": "update",
          "phase": "fight",
          "label": "the turn passes on",
          "do": [
            {
              "set": {
                "players": {
                  "where": "you.seat == cur_seat"
                },
                "key": "stake",
                "value": {
                  "calc": "min_stake if you.fight_choice == 'LOW' else (min_stake + high_stake_extra if you.fight_choice == 'HIGH' else 0)"
                }
              }
            },
            {
              "set": {
                "key": "high_fought",
                "value": {
                  "calc": "high_fought or any(p.fight_choice == 'HIGH' for p in players)"
                }
              }
            },
            {
              "set": {
                "key": "cur_seat",
                "value": {
                  "calc": "min([p.seat for p in players if p.active and p.seat > cur_seat]) if any(p.active and p.seat > cur_seat for p in players) else min([p.seat for p in players if p.active])"
                }
              }
            },
            {
              "adjust": {
                "key": "fight_turn",
                "value": 1
              }
            },
            {
              "set": {
                "players": {
                  "where": "you.seat == cur_seat"
                },
                "key": "offer",
                "value": {
                  "calc": "['PASS'] + (['LOW'] if not high_fought and you.kamons >= min_stake else []) + (['HIGH'] if you.kamons >= min_stake + high_stake_extra else [])"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "stake",
      "label": "the stakes",
      "do": [
        {
          "adjust": {
            "key": "pot",
            "value": {
              "calc": "sum([p.stake for p in players])"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.stake > 0 and you.kamons >= you.stake"
            },
            "key": "kamons",
            "value": {
              "calc": "-you.stake"
            }
          }
        },
        {
          "adjust": {
            "key": "pot",
            "value": {
              "calc": "min(centre_feed_rounds_1_to_9, centre) if round < total_rounds else centre"
            }
          }
        },
        {
          "adjust": {
            "key": "centre",
            "value": {
              "calc": "-(min(centre_feed_rounds_1_to_9, centre) if round < total_rounds else centre)"
            }
          }
        }
      ],
      "text": "Stakes are paid and the centre feeds the pot. Pot: {pot}. Centre: {centre}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the showdown",
      "do": [
        {
          "set": {
            "key": "fighters",
            "value": {
              "calc": "count(p.fight_choice in ['LOW', 'HIGH'] for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.fight_choice in ['LOW', 'HIGH'] and fighters >= 2"
            },
            "key": "shown_card",
            "value": {
              "calc": "you.hand"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.fight_choice in ['LOW', 'HIGH'] and fighters >= 2"
            },
            "key": "total",
            "value": {
              "calc": "you.hand + (kobayakawa if you.hand == min([q.hand for q in players if q.fight_choice in ['LOW', 'HIGH']]) else 0)"
            }
          }
        },
        {
          "set": {
            "key": "top_total",
            "value": {
              "calc": "max([p.total for p in players if p.fight_choice in ['LOW', 'HIGH']] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "count(p.fight_choice in ['LOW', 'HIGH'] and p.total == top_total for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.fight_choice in ['LOW', 'HIGH']]) if fighters == 1 else (min([p.seat for p in players if p.fight_choice in ['LOW', 'HIGH'] and p.total == top_total]) if fighters >= 2 and top_count == 1 else 0)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "kamons",
            "value": {
              "calc": "pot"
            },
            "if": {
              "calc": "winner_seat > 0"
            },
            "text": "Seat {player} takes the pot of {pot}."
          }
        },
        {
          "set": {
            "key": "pot",
            "value": 0,
            "if": {
              "calc": "winner_seat > 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.fight_choice in ['LOW', 'HIGH'] and you.total == top_total"
            },
            "key": "kamons",
            "value": {
              "calc": "int(pot / top_count)"
            },
            "if": {
              "calc": "round == total_rounds and fighters >= 2 and top_count >= 2"
            },
            "text": "Seat {player} shares the tied pot in the last round."
          }
        },
        {
          "set": {
            "key": "pot",
            "value": 0,
            "if": {
              "calc": "round == total_rounds and fighters >= 2 and top_count >= 2"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "the results",
      "to": "all",
      "text": "Fight choices [seat, choice]: {[[p.seat, p.fight_choice] for p in players if p.active]}. Revealed cards [seat, card, total]: {[[p.seat, p.shown_card, p.total] for p in players if p.shown_card > 0]}. Pot winner: seat {winner_seat} (0 means nobody). Pot now: {pot}. Kamons [seat, kamons]: {[[p.seat, p.kamons] for p in players]}."
    },
    {
      "use": "update",
      "phase": "cleanup",
      "label": "cleanup",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.fight_choice in ['LOW', 'HIGH']"
            },
            "key": "held_rounds",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "you.fight_choice in ['LOW', 'HIGH']"
            },
            "key": "hand",
            "value": 0
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.active and you.fight_choice == 'PASS'"
            },
            "key": "held_rounds",
            "value": 1
          }
        },
        {
          "set": {
            "players": {
              "where": "you.active and you.kamons <= 0"
            },
            "key": "hand",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "you.active and you.kamons <= 0"
            },
            "key": "active",
            "value": false
          }
        },
        {
          "set_status": {
            "players": {
              "where": "not you.active"
            },
            "to": "out",
            "text": "Seat {player} has 0 kamons and is eliminated; their card is discarded unseen."
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "winner_seat if winner_seat > 0 else (min([p.seat for p in players if p.active and p.seat > start_seat]) if any(p.active and p.seat > start_seat for p in players) else min([p.seat for p in players if p.active] + [start_seat]))"
            }
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
      "phase": "cleanup",
      "label": "end check",
      "when": {
        "calc": "round > total_rounds or count(p.active for p in players) <= 1"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds or count(p.active for p in players) <= 1"
      },
      "rank_by": "you.kamons",
      "text": "Winner: {result}. Final kamons [seat, kamons]: {[[p.seat, p.kamons] for p in players]}."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "SETUP. Each player starts with {starting_kamons} kamons and sits in a numbered seat (1 to N). The centre holds {centre_kamons} kamons and the pot starts at {starting_pot}. Nobody holds a card. The start player for round 1 is seat {first_start_seat}. The game lasts {total_rounds} rounds, or ends sooner if only one player remains.\n\nEACH ROUND:\n1. DEAL. All cards numbered {card_min} to {card_max}, except the hand cards currently held by players, are shuffled. Each active player without a hand card receives one, seen only by that player. Every active player then receives one RESERVE card, face down and unseen. Then the KOBAYAKAWA is dealt face up and the ALTERNATE face down.\n2. ANNOUNCE. The round number, the Kobayakawa value and the pot, each player's kamons, which players hold a card kept from an earlier round and for how many rounds, the start player, and the minimum stake ({min_stake_rounds_1_to_9} in rounds 1-9, {min_stake_round_10} in round 10) are announced.\n3. DRAW CHOICE (simultaneous, secret). Each active player chooses KEEP (keep your hand card), DRAW (look at your reserve card) or SHIFT (vote to replace the Kobayakawa). No choice is seen until all are in.\n4. Each player who chose DRAW privately sees their reserve card; nobody else sees it.\n5. KEEP CHOICE (simultaneous, drawers only). Each drawer keeps OLD (the hand card) or NEW (the reserve card) as their hand card. If NEW, the reserve card becomes your hand and your old hand card is discarded face up (a new card counts as fresh: held rounds 0). If OLD, you keep your hand card and the reserve card is discarded face up. All undrawn reserve cards are discarded face down, unseen.\n6. REVEAL. Every player's draw choice and all face-up discards are announced.\n7. SHIFT. If at least one player chose SHIFT, the Alternate replaces the Kobayakawa and its value is announced. If nobody chose SHIFT, the Kobayakawa is unchanged.\n8. TALK (simultaneous). Every active player writes one short message without seeing the others; all messages are shown to everyone. Talk is not binding and may be false.\n9. FIGHT (sequential). Players act once each in seat order, beginning with the start player and wrapping around; each sees all earlier choices. The required stake is the minimum stake, or the minimum + {high_stake_extra} if any earlier player this round fought HIGH. A player chooses PASS, FIGHT LOW (stake = minimum; offered only while nobody has fought HIGH and you have at least the minimum in kamons) or FIGHT HIGH (stake = minimum + {high_stake_extra}; offered when you have at least that many kamons). Once anyone has fought HIGH, LOW is no longer offered. A player with fewer kamons than every stake they are allowed must PASS and is not asked.\n10. STAKE. Each fighter pays their stake into the pot. Then the centre feeds the pot: {centre_feed_rounds_1_to_9} kamon in rounds 1-9 if the centre has any, and all remaining centre kamons in round 10.\n11. SCORE. If nobody fought, the pot carries to the next round. If exactly one player fought, that player takes the whole pot and their card is not revealed. If two or more fought, all fighters' cards are revealed; each fighter's total is their card value, and the fighter with the lowest card adds the Kobayakawa value to their total. The single highest total takes the whole pot.\n12. TIES. If fighters share the highest total, nobody takes the pot and it carries to the next round. In round 10, the pot is instead split equally among the tied fighters, rounding down, and any remainder is removed from the game.\n13. CLEANUP. Every fighter's hand card is discarded (held rounds back to 0); that player receives a fresh card next round. Every player who passed keeps their hand card, still secret, and their held rounds go up by 1. The next start player is the pot winner; if nobody won the pot, it is the next active seat after this round's start player.\n14. ELIMINATION. Any player with 0 kamons is eliminated, and their card is discarded unseen.\n15. END. The game ends after round {total_rounds}, or as soon as only one active player remains.\n\nWINNING. When the game ends, the player with the most kamons wins (eliminated players have 0). Players tied for the most share the result (a draw). If only one active player remains before round {total_rounds}, that player wins."
}
```
````
