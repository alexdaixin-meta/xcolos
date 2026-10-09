# Task: write the XColos game file for "Coup (XColos)"

You are a coding agent working in the repository at /Users/alexdaixin/AAI_LAB/xcolos. Write ONE file, `gen_game/data/games/coup/game.json`: the game
below as a game definition for the XColos engine. Do not write any other file except `gen_game/data/games/coup/encode_notes.md`.

## The game

Players: 3 to 5.

COMPONENTS. A deck of 15 cards: 3 each of Duke, Assassin, Captain, Ambassador and Contessa. Each player has a coin count.

SETUP. Shuffle the deck and deal 2 cards face down to each player; only the owner sees them. The rest form the face-down deck. Seat order is fixed. The first player starts with 1 coin and every other player with 2. A player's cards are either hidden or revealed. Revealed cards are face up, public and permanent.

TURNS. Players take turns in seat order, skipping eliminated players. Each turn has these steps.

1. STATE. The engine announces every player's coins, revealed cards and number of hidden cards, plus the number of cards in the deck.

2. ACTION. The active player chooses one action, and a target where the action needs one (any other living player). A player who starts the turn with 10 or more coins must choose Coup. The actions are:
- Income: take 1 coin. Cannot be challenged or blocked.
- Foreign Aid: take 2 coins. Cannot be challenged. Any other player may block by claiming Duke.
- Coup: pay 7 coins (only if you have 7); the target loses 1 influence. Cannot be challenged or blocked.
- Tax (claims Duke): take 3 coins. Can be challenged.
- Assassinate (claims Assassin): pay 3 coins (only if you have 3); the target loses 1 influence. Can be challenged. The target may block by claiming Contessa.
- Steal (claims Captain): take 2 coins from the target, or all the target's coins if they have fewer than 2. Can be challenged. The target may block by claiming Captain or Ambassador.
- Exchange (claims Ambassador): take the top card of the deck into your hand, then return one of your hidden cards (your choice, made in step 7) to the deck. Can be challenged.
Costs are paid immediately and are not refunded, even if the action is later blocked or fails a challenge.

3. REACTION. Every other living player answers at the same moment, without seeing the others' answers. The options are:
- Pass;
- Challenge, only if the action claims a role;
- Block as Duke / Block as Contessa / Block as Captain / Block as Ambassador, only where that block is allowed (Duke against Foreign Aid by anyone; Contessa against Assassinate by the target only; Captain or Ambassador against Steal by the target only).
All answers are announced.

4. ACTION CHALLENGE. If anyone challenged, only the first challenger in seat order after the active player counts.
- If the active player holds the claimed role: they reveal it, take the top card of the deck into their hand, and put the revealed card into the deck. The challenger gets 1 pending loss. The action continues.
- Otherwise the active player gets 1 pending loss and the action fails. Any block is ignored, and the turn goes to step 7.

5. BLOCK. If the action is still going ahead and anyone blocked, only the first blocker in seat order after the active player counts. Every living player except that blocker answers Accept or Challenge at the same moment, and the answers are announced.
- If nobody challenges, the action is blocked and has no effect.
- If anyone challenges, only the first challenger in seat order after the blocker counts. If the blocker holds the claimed blocking role, they reveal it, take the top card of the deck, and put the revealed card into the deck; the block challenger gets 1 pending loss and the action is blocked. Otherwise the blocker gets 1 pending loss, the block fails, and the action goes ahead.

6. EFFECT. If the action went ahead (not failed, not blocked), apply it:
- coins move as stated;
- Assassinate and Coup give the target 1 pending loss;
- Exchange gives the active player the top card of the deck and 1 card to return.

7. CARD CHOICE. At the same moment:
- every player with exactly 1 pending loss and 2 hidden cards chooses which hidden card to reveal;
- a player who must return a card for Exchange chooses which of their hidden cards to put into the deck.

8. RESOLVE.
- A player with 1 pending loss and 2 hidden cards reveals the chosen card.
- A player whose pending losses are equal to or more than their hidden cards reveals all of them and is eliminated. Their coins leave the game.
- The Exchange card goes into the deck.
- If any card was put into the deck this turn, the deck is shuffled.
- Pending losses reset to 0.
The engine announces what was revealed (never what was returned).

9. END CHECK. If only one player has hidden cards, that player wins. Otherwise the turn passes to the next living player in seat order.

CAP. If 40 turns have been played without a winner, the game ends. The player with the most hidden cards wins; if tied, the tied player with the most coins wins; if still tied, the game is a draw.

There is no free discussion. Claims, challenges and blocks are the only communication.

How the winner is decided: The last player with at least one hidden card wins. If 40 turns pass first, the player with the most hidden cards wins, ties are broken by most coins, and any remaining tie is a draw. Everything is decided by counting cards and coins.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Coup (XColos) (3 to 5 players)

Each player holds two hidden role cards. On your turn you take an action, and some actions require claiming a role you may not hold. Other players can challenge or block. Lose both cards and you are out; the last player holding a hidden card wins.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 2); everyone sees it. Coins held. Seat 1 starts with 1 and every other seat with 2. Set to 0 when the player is eliminated.
  - each player: hidden_cards (list, starts []); only its owner sees it. The player's face-down role cards. Only the owner sees them. A challenge is checked against this list.
  - each player: revealed_cards (list, starts []); everyone sees it. Face-up role cards the player has lost. They are public and stay revealed.
  - each player: hidden_count (number, starts 2); everyone sees it. How many hidden cards the player holds. Always equals the length of hidden_cards outside an Exchange. 0 means eliminated.
  - each player: alive (bool, starts True); everyone sees it. False once the player has no hidden cards left.
  - each player: pending_loss (number, starts 0); everyone sees it. Influence the player must lose in this turn's resolve step. Reset to 0 at the end of every turn.
  - each player: must_return (number, starts 0); everyone sees it. 1 when the player owes the deck one hidden card from an Exchange this turn, otherwise 0.
  - each player: reaction (text, starts ''); everyone sees it. This turn's answer to the action: pass, challenge, block_duke, block_contessa, block_captain or block_ambassador. All reactions are announced.
  - each player: block_response (text, starts ''); everyone sees it. This turn's answer to a block: accept or challenge. Announced.
  - each player: reveal_choice (text, starts ''); only its owner sees it. The hidden card the player chose to reveal when losing one of two cards.
  - each player: return_choice (text, starts ''); only its owner sees it. The hidden card the player chose to put back in the deck after an Exchange. Never announced.
  - the table: deck (list, starts ['Duke', 'Duke', 'Duke', 'Assassin', 'Assassin', 'Assassin', 'Captain', 'Captain', 'Captain', 'Ambassador', 'Ambassador', 'Ambassador', 'Contessa', 'Contessa', 'Contessa']); hidden from all players. The face-down deck. Drawing takes a random card from it, so it is always shuffled.
  - the table: deck_count (number, starts 15); everyone sees it. Number of cards in the deck. Announced every turn.
  - the table: turn_count (number, starts 0); everyone sees it. Turns played so far.
  - the table: active_seat (number, starts 1); everyone sees it. Seat of the player taking the current turn.
  - the table: action (text, starts ''); everyone sees it. This turn's action: income, foreign_aid, coup, tax, assassinate, steal or exchange.
  - the table: claimed_role (text, starts ''); everyone sees it. The role the action claims (Duke for tax, Assassin for assassinate, Captain for steal, Ambassador for exchange), or empty if it claims none.
  - the table: target (number, starts 0); everyone sees it. Seat targeted by coup, assassinate or steal. 0 if the action has no target.
  - the table: action_status (text, starts 'going'); everyone sees it. going, failed (the action challenge succeeded) or blocked.
  - the table: challenger (number, starts 0); everyone sees it. The first seat after the active player that challenged the action. 0 if nobody did.
  - the table: blocker (number, starts 0); everyone sees it. The first seat after the active player that blocked. 0 if nobody did.
  - the table: block_role (text, starts ''); everyone sees it. The role the counting blocker claims.
  - the table: block_challenger (number, starts 0); everyone sees it. The first seat after the blocker that challenged the block. 0 if nobody did.
  - the table: stolen (number, starts 0); hidden from all players. Coins moved by this turn's Steal: the smaller of 2 and the target's coins.
  - the table: living_count (number, starts 0); everyone sees it. Number of players with at least one hidden card.
  - the table: winner (text, starts ''); everyone sees it. The result once the game ends: 'seat N' or 'draw'.
  - parameters, each kept as a table attribute: deck_size = 15, copies_per_role = 3, hand_size = 2, first_player_start_coins = 1, other_player_start_coins = 2, forced_coup_threshold = 10, income_gain = 1, foreign_aid_gain = 2, coup_cost = 7, tax_gain = 3, assassinate_cost = 3, steal_amount = 2, exchange_draw = 1, exchange_return = 1, loss_per_hit = 1, turn_cap = 40

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. The deck holds 15 cards: 3 each of Duke, Assassin, Captain, Ambassador and Contessa.
  2. Each player draws 2 cards at random from deck into hidden_cards, so deck_count becomes 15 - 2 x player count and every hidden_count becomes 2.
  3. Seat 1 gets coins = 1 and every other seat gets coins = 2.
  4. living_count is set to the player count, turn_count to 0 and active_seat to 1.
  5. Each player is sent their own hidden_cards.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] engine. What happens: Start of turn: action_status = going; challenger = blocker = block_challenger = target = stolen = 0; action, claimed_role, block_role and every player's reaction, block_response, reveal_choice and return_choice are cleared; turn_count += 1.
  2. [tell] all players. What happens: Announce each player's coins, revealed_cards and hidden_count, plus deck_count and active_seat.
  3. [sync] all players. What happens: Send each player their own hidden_cards.
  4. [ask] the player at active_seat answers: One choice of action: income, foreign_aid, coup (only if coins >= 7), tax, assassinate (only if coins >= 3), steal or exchange. If coins >= 10 at the start of the turn, the only option is coup.. What happens: action = the answer; claimed_role = Duke for tax, Assassin for assassinate, Captain for steal, Ambassador for exchange, empty otherwise.
  5. [ask] the player at active_seat, when action is coup, assassinate or steal answers: The seat of any other player with alive = true.. What happens: target = the chosen seat.
  6. [update] engine. What happens: Pay costs now, with no refund later: if action = coup, active coins -= 7; if action = assassinate, active coins -= 3.
  7. [tell] all players. What happens: Announce the active seat's action, claimed_role and target.
  8. [poll] every living player except the active player, when action is foreign_aid, tax, assassinate, steal or exchange answers: pass; challenge (only if claimed_role is set); block_duke (anyone, only against foreign_aid); block_contessa (only the target, only against assassinate); block_captain or block_ambassador (only the target, only against steal).. What happens: Each answering player's reaction = the answer.
  9. [tell] all players. What happens: Announce every player's reaction.
  10. [update] engine. What happens: challenger = the first seat in seat order after active_seat with reaction = challenge, 0 if none. blocker = the first seat after active_seat whose reaction starts with block_, 0 if none. block_role = that block's role.
  11. [update] engine, when challenger > 0. What happens: Action challenge. If claimed_role is in the active player's hidden_cards: remove one claimed_role card from the active player's hidden_cards and append it to deck, then draw one card at random from deck into the active player's hidden_cards; challenger's pending_loss += 1. Otherwise: active player's pending_loss += 1, action_status = failed, blocker = 0.
  12. [tell] all players, when challenger > 0. What happens: Announce whether the challenged claim was true and who takes the pending loss. The card the active player draws is not named.
  13. [poll] every living player except the blocker, when action_status = going and blocker > 0 answers: accept or challenge. What happens: Each answering player's block_response = the answer.
  14. [tell] all players, when action_status = going and blocker > 0. What happens: Announce every player's block_response.
  15. [update] engine, when action_status = going and blocker > 0. What happens: block_challenger = the first seat in seat order after blocker with block_response = challenge, 0 if none. If block_challenger = 0: action_status = blocked. Otherwise, if block_role is in the blocker's hidden_cards: move that card from the blocker's hidden_cards to deck, draw one card at random from deck into the blocker's hidden_cards, block_challenger's pending_loss += 1, action_status = blocked. Otherwise: blocker's pending_loss += 1 and the action goes ahead (action_status stays going).
  16. [update] engine, when action_status = going. What happens: Effect. income: active coins += 1. foreign_aid: active coins += 2. tax: active coins += 3. steal: stolen = the smaller of 2 and the target's coins, target coins -= stolen, active coins += stolen. coup or assassinate: target pending_loss += 1. exchange: draw one card at random from deck into the active player's hidden_cards and set the active player's must_return = 1.
  17. [poll] every player with (pending_loss = 1 and hidden_count = 2) or must_return = 1 answers: One card from the player's own hidden_cards. A player who both loses a card and owes an Exchange return answers twice: the card to reveal and the card to return.. What happens: reveal_choice = the card to reveal; return_choice = the card to return to the deck.
  18. [update] engine. What happens: Resolve. A player with pending_loss = 1 and hidden_count = 2 moves reveal_choice from hidden_cards to revealed_cards. A player with must_return = 1 moves return_choice from hidden_cards to deck. Any player with pending_loss >= hidden_count and pending_loss > 0 moves all of hidden_cards to revealed_cards, alive = false, coins = 0. Then hidden_count = length of hidden_cards for every player, deck_count = length of deck, living_count = number of players with alive = true. Every pending_loss and must_return goes back to 0.
  19. [tell] all players. What happens: Announce every card revealed this turn and every player eliminated. Returned cards are never named.
  20. [check] engine. What happens: End the game if living_count = 1 or turn_count >= 40, otherwise continue.
  21. [update] engine. What happens: active_seat = the next seat after active_seat in seat order, wrapping around and skipping players with alive = false.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck has 15 cards (3 each of Duke, Assassin, Captain, Ambassador, Contessa), each player has hidden_count = 2, and deck_count = 15 - 2 x player count.
  R2. When the game is set up, seat 1 has coins = 1 and every other seat has coins = 2.
  R3. When a player takes Income unchallenged and unblocked, then their coins rise by exactly 1, and no player is offered a challenge or block.
  R4. When a player takes Foreign Aid and nobody blocks, then their coins rise by 2.
  R5. When a player takes Foreign Aid and another player blocks as Duke and nobody challenges the block, then the active player's coins do not change.
  R6. When a player takes Foreign Aid, then challenge is not offered against the action.
  R7. When a player with 7 or more coins takes Coup on a target, then their coins fall by 7 and the target loses 1 hidden card; nobody may challenge or block.
  R8. When a player has fewer than 7 coins, then Coup is not among their options.
  R9. When a player starts their turn with 10 or more coins, then Coup is their only option.
  R10. When a player takes Tax and nobody challenges, then their coins rise by 3.
  R11. When a player with 3 or more coins takes Assassinate, then their coins fall by 3 at once, even if the action is later blocked or fails a challenge.
  R12. When a player has fewer than 3 coins, then Assassinate is not among their options.
  R13. When Assassinate goes ahead unblocked, then the target loses 1 hidden card.
  R14. When the target of Assassinate blocks as Contessa and nobody challenges the block, then the target loses no card and the assassin's 3 coins are not refunded.
  R15. When a player Steals from a target with 2 or more coins and the action goes ahead, then the target's coins fall by 2 and the active player's coins rise by 2.
  R16. When a player Steals from a target with 1 coin and the action goes ahead, then the target ends with 0 coins and the active player gains 1; with 0 coins, nobody's coins change.
  R17. When the target of a Steal blocks as Captain or as Ambassador and nobody challenges the block, then no coins move.
  R18. When a player other than the target answers a Steal or Assassinate, then they are not offered block_contessa, block_captain or block_ambassador.
  R19. When a player takes Exchange and the action goes ahead, then they draw 1 card from the deck and return 1 hidden card of their choice, ending with the same hidden_count and the same deck_count.
  R20. When an Exchange returns a card, then the returned card is never announced.
  R21. When a challenged active player holds the claimed role, then that card goes into the deck, they draw a replacement (keeping hidden_count), the first challenger in seat order after them loses 1 hidden card, and the action continues.
  R22. When a challenged active player does not hold the claimed role, then they lose 1 hidden card, the action has no effect, and any block is ignored.
  R23. When several players challenge the action, then only the first challenger in seat order after the active player can lose a card from it.
  R24. When several players block, then only the first blocker in seat order after the active player counts.
  R25. When a challenged blocker holds the blocking role, then that card goes into the deck, they draw a replacement, the first block challenger in seat order after the blocker loses 1 hidden card, and the action is blocked.
  R26. When a challenged blocker does not hold the blocking role, then the blocker loses 1 hidden card and the action goes ahead.
  R27. When the Assassinate target's Contessa block is challenged and they do not hold Contessa, then the target gets 2 pending losses and, holding 2 hidden cards, is eliminated.
  R28. When a player with 2 hidden cards gets exactly 1 pending loss, then they reveal the one card they choose and keep the other hidden.
  R29. When a player's pending losses are equal to or more than their hidden cards, then all their hidden cards are revealed, alive becomes false, and their coins become 0.
  R30. When a card is revealed, then it moves to revealed_cards, stays public, and never returns to the hand.
  R31. When a turn ends, then every pending_loss is 0.
  R32. When a turn ends and the game goes on, then the next turn belongs to the next seat with alive = true, skipping eliminated seats.
  R33. When a target is chosen, then it must be another player with alive = true.
  R34. When only one player has hidden_count >= 1, then the game ends and that seat wins.
  R35. When 40 turns have been played and more than one player is alive, then the seat with the most hidden cards wins; a tie goes to the most coins; a remaining tie is a draw.
  R36. When players react to an action or a block, then they answer in a poll, and no one sees another's answer until all are in.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: living_count = 1 or turn_count >= 40
  - the result is one of: seat 1, seat 2, seat 3, seat 4, seat 5, draw
  - how the result is decided: If living_count = 1, the result is the seat with hidden_count >= 1. Otherwise, after 40 turns, the result is the seat with the highest hidden_count; if several tie, the tied seat with the most coins; if they are still tied, draw.
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

## Rounds and the safety cap

If the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed
round count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The `end` rules fire the real endings from the state; add one more
ending that fires when the cap is reached and decides the winner as the script says, so a match that hits the cap still ends with a result.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `coins` (number, visible: public, starts 2): Coins held. Seat 1 starts with 1 and every other seat with 2. Set to 0 when the player is eliminated.
- each player: `revealed_cards` (list, visible: public, starts []): Face-up role cards the player has lost. They are public and stay revealed.
- each player: `hidden_count` (number, visible: public, starts 2): How many hidden cards the player holds. Always equals the length of hidden_cards outside an Exchange. 0 means eliminated.
- each player: `alive` (bool, visible: public, starts True): False once the player has no hidden cards left.
- the table: `turn_count` (number, visible: public, starts 0): Turns played so far.
- the table: `winner` (text, visible: public, starts ''): The result once the game ends: 'seat N' or 'draw'.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 15, copies_per_role = 3, hand_size = 2, first_player_start_coins = 1, other_player_start_coins = 2, forced_coup_threshold = 10, income_gain = 1, foreign_aid_gain = 2, coup_cost = 7, tax_gain = 3, assassinate_cost = 3, steal_amount = 2, exchange_draw = 1, exchange_return = 1, loss_per_hit = 1, turn_cap = 40
- the game ends with exactly one of these results, named exactly: `seat 1`, `seat 2`, `seat 3`, `seat 4`, `seat 5`, `draw`
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

- The complete file format is documented in `design/actions.md`. Read all of it: every key an action accepts is listed there,
  and the loader refuses any other.
- Complete example games to imitate, in `xcolos/games/library/`:
  * xcolos/games/library/rps.json
  * xcolos/games/library/auction.json
  The `auction` example ends with a model-decided `winner`; do NOT copy that part. End with a `result` and a calc condition
  as `rps` does.
- The outcome must be decided by arithmetic: every ending's `when` is a calc condition, no prose conditions; no step uses `llm`
  and every step uses `text`. Choices made at the same moment are a `poll`.
- ENDING STATEMENT: the end screen must say more than who won. Every ending's `text` gives the final scores or the figures that decided it,
  using placeholders such as `{players[0].score}` and `{target}`, and every ending also has an `llm` asking a model for a short
  summary of how the game went (what each player did, the turning point, why this result). `text` is the complete fallback. The model only
  words the announcement; the `result` is still decided by the calc.

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
3. A `check` with `when` and `against`, and the endings in `end`, comparing `players[0].score` and `players[1].score`.
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
        "seat_1_wins",
        "seat_2_wins",
        "draw"
      ]
    }
  ],
  "end": {
    "seat_1_wins": {
      "when": {
        "calc": "players[0].score > players[1].score"
      },
      "result": "seat 1",
      "text": "Seat 1 wins."
    },
    "seat_2_wins": {
      "when": {
        "calc": "players[1].score > players[0].score"
      },
      "result": "seat 2",
      "text": "Seat 2 wins."
    },
    "draw": {
      "when": {
        "calc": "players[0].score == players[1].score"
      },
      "result": "draw",
      "text": "A draw."
    }
  }
}
```

## Check your work

Run this from the repository root, and keep fixing `game.json` until it prints `ok` (give up after about 8 attempts and say
what blocks you):

    python3 -m gen_game verify coup game

It runs the loader, checks the outcome is arithmetic, and plays the game with random seats. It tells you the problem when it
fails. Then check that the game plays the RULES in the script:

    python3 -m gen_game verify coup rules

It plays the game through independent scenarios, one per rule, and names each rule that is broken, in its own words, with what it
expected and what the game did. Fix the game until it prints `ok` too. (If it says no scenarios have been written yet, skip it.)
The scenarios are written by someone else from the rules alone, so the rules list is your checklist: read it, and do not guess.

Do NOT read `gen_game/data/games/coup/scenarios.json` or anything under `gen_game/data/games/coup/history/`, and do not edit code. When you are done, write
`gen_game/data/games/coup/encode_notes.md`: where the rules were ambiguous or the platform could not do what they ask, and what you chose.
If the platform genuinely cannot express something the rules REQUIRE, say so there plainly instead of faking it.

## Guidance from the last attempt

The previous attempt had problems:

1) Rename the player attributes to the interface names: `hand_count` -> `hidden_count` (starts 2) and `revealed` -> `revealed_cards` (starts []). Keep `coins` and `alive`. Update every step that reads or writes them. 2) Rename the table attribute `turn_number` to `turn_count`. It must start at 0 and count turns played. 3) Give every parameter its exact interface name and value: deck_size=15, copies_per_role=3, hand_size=2 (not initial_hand), first_player_start_coins=1, other_player_start_coins=2 (replace the single initial_coins), forced_coup_threshold=10 (not coup_forced_threshold), income_gain=1, foreign_aid_gain=2, coup_cost=7, tax_gain=3 (not duke_tax_gain), assassinate_cost=3 (not assassin_cost), steal_amount=2 (not steal_max), exchange_draw=1, exchange_return=1, loss_per_hit=1, turn_cap=40 (not max_turns). Steps must use these attributes, never literal numbers. 4) Setup: set seat 1's coins to first_player_start_coins (1) and every other seat to other_player_start_coins (2). 5) Keep `hidden_count` equal to the length of the hidden hand at all times outside an Exchange. When a player is eliminated, set it to 0, set alive=false and set coins=0. 6) Set `winner` to exactly 'seat N' or 'draw', and end with the matching result name.
