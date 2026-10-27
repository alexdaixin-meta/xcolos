# 06 coder

- time: 2026-10-27T18:06:28+00:00 (206.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 4b3f1720191917e3, reply sha256 f673d5e293b07861

## Sent

````
# Task: write the XColos game file for "Diamonds: Three-Hand Vault"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

COMPONENTS
- A deck of 36 cards: four suits (Diamonds, Hearts, Spades, Clubs), each ranked 1 to 9.
- An unlimited supply of crystals.
- Each player has a showroom and a vault. Both start empty, and the counts of both are public.
- For each hand, the engine tracks how many cards of each suit every player has won, and how many tricks each player has won. These counts are public.

SEATS
- Players sit in fixed order: A, B, C. 'Left' means the next player in that order (A's left is B, B's left is C, C's left is A).

STRUCTURE
- The game is 3 hands of 10 tricks: 30 rounds, one trick per round.
- Hand 1 is rounds 1 to 10, hand 2 is rounds 11 to 20, hand 3 is rounds 21 to 30.
- The dealer is C for hand 1, A for hand 2 and B for hand 3. The player to the dealer's left leads the first trick of the hand, so A, B and C each lead a hand's first trick exactly once.

DEAL AND PASS (first round of each hand only)
1. Shuffle all 36 cards. Deal 10 cards face down to each player. Set the remaining 6 aside face down; no one sees them during the hand.
2. All players at the same moment secretly choose exactly 2 cards from their hand.
3. Each player then gives those 2 cards to the player on their left. Players see their new hand; the passed cards are not announced to anyone else.
4. Reset every player's won-card counts and trick counts to 0.

PLAYING A TRICK (every round)
1. The leader plays any card from their hand, face up, and names one opponent as their Clubs target.
2. The next player to the left then plays a card and names a Clubs target. Then the third player does the same.
3. The suit of the first card is the led suit. A player who holds a card of the led suit must play one. A player who holds none may play any card.
4. OFF-SUIT ACTION: when a player plays a card not of the led suit, they immediately take that card's suit action, before the next player plays.
5. The highest card of the led suit wins the trick.
6. The winner adds the 3 cards to their won counts by suit (each card counts in its own suit) and adds 1 to their trick count.
7. The winner then takes the led suit's action.
8. The winner leads the next trick of the same hand.
9. Everything played and every action taken is announced to all players.

SUIT ACTIONS (for the player taking the action)
- Diamonds: move 1 crystal from the supply to your vault.
- Hearts: move 1 crystal from the supply to your showroom.
- Spades: move 1 crystal from your showroom to your vault. If your showroom is empty, nothing happens.
- Clubs (from a trick or an off-suit play): move 1 crystal from your named Clubs target's showroom to your own showroom. If that showroom is empty, nothing happens.

END OF HAND (after the 10th trick of each hand)
1. For each suit in turn (Diamonds, Hearts, Spades, Clubs), the player with strictly the most won cards of that suit takes that suit's action once. If the top count is tied, no one takes it.
2. An end-of-hand Clubs action robs the opponent with the largest showroom. If those opponents are tied, it robs the one on the receiver's left.
3. Each player who won 0 tricks in the hand takes two Diamond actions.
4. The 6 set-aside cards are then revealed, and all cards are gathered for the next deal.

SCORING
- Each vault crystal is worth 2 points and each showroom crystal 1 point.
- After the 30th round and the third end-of-hand step, the game ends.

How the winner is decided: The player with the highest score (2 x vault + 1 x showroom) wins. If players tie on score, the tied player with more vault crystals wins. If they are still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Diamonds: Three-Hand Vault (3 to 3 players, best with 3)

A three-player trick-taking game over 3 hands of 10 tricks. Each suit's action moves crystals into your showroom (1 point each) or your vault (2 points each), or steals from an opponent's showroom.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards held, coded suit letter + rank, e.g. D7, H3, S9, C1
  - each player: pass_cards (list, starts []); only its owner sees it. The 2 cards secretly chosen to pass left this hand
  - each player: showroom (number, starts 0); everyone sees it. Crystals in the showroom, worth 1 point each
  - each player: vault (number, starts 0); everyone sees it. Crystals in the vault, worth 2 points each
  - each player: score (number, starts 0); everyone sees it. 2 x vault + 1 x showroom, recomputed after every change
  - each player: won_diamonds (number, starts 0); everyone sees it. Diamond cards won in tricks this hand
  - each player: won_hearts (number, starts 0); everyone sees it. Heart cards won in tricks this hand
  - each player: won_spades (number, starts 0); everyone sees it. Spade cards won in tricks this hand
  - each player: won_clubs (number, starts 0); everyone sees it. Club cards won in tricks this hand
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won this hand
  - each player: played_card (text, starts ''); everyone sees it. Card this player played to the current trick
  - each player: played_suit (text, starts ''); everyone sees it. Suit letter of played_card
  - each player: played_rank (number, starts 0); everyone sees it. Rank of played_card
  - each player: clubs_target (number, starts 0); everyone sees it. Seat this player named as Clubs target for the current trick
  - the table: deck (list, starts []); hidden from all players. Undealt cards; filled with all 36 cards at the start of each hand
  - the table: set_aside (list, starts []); hidden from all players. The 6 cards set aside face down this hand
  - the table: round_number (number, starts 1); everyone sees it. Current round, 1 to 30, one trick per round
  - the table: hand_number (number, starts 1); everyone sees it. Current hand, 1 to 3
  - the table: dealer (number, starts 3); everyone sees it. Dealer seat this hand (1=A, 2=B, 3=C)
  - the table: leader (number, starts 1); everyone sees it. Seat that leads the current trick
  - the table: led_suit (text, starts ''); everyone sees it. Suit letter of the first card of the current trick
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the last trick
  - parameters, each kept as a table attribute: deck_size = 36, suits = 4, ranks_per_suit = 9, lowest_rank = 1, highest_rank = 9, cards_dealt_per_player = 10, cards_set_aside = 6, cards_passed = 2, hands = 3, tricks_per_hand = 10, total_rounds = 30, cards_per_trick = 3, crystals_per_action = 1, vault_crystal_points = 2, showroom_crystal_points = 1, zero_trick_diamond_actions = 2, dealer_hand_1_seat = 3, dealer_hand_2_seat = 1, dealer_hand_3_seat = 2, rank_tiebreak_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are A=1, B=2, C=3. The left of seat s is seat (s mod 3) + 1.
  2. Every player's showroom, vault and score start at 0.
  3. round_number is set to 1 and hand_number to 1.
  4. The 36 cards are D1-D9, H1-H9, S1-S9 and C1-C9. The crystal supply is unlimited, so it is not tracked.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Start of a hand. Set hand_number = (round_number - 1) / 10 + 1. Set dealer = 3, 1 or 2 for hand 1, 2 or 3. Set leader = (dealer mod 3) + 1. Gather all 36 cards into deck and clear every hand, pass_cards and set_aside. Deal 10 cards at random from deck into each player's hand, then move the remaining 6 into set_aside. Reset won_diamonds, won_hearts, won_spades, won_clubs and tricks_won to 0 for every player.
  2. [sync] all players. What happens: Each player privately sees their own hand.
  3. [poll] all players answers: one card from own hand. What happens: Append the chosen card to pass_cards (first pass card).
  4. [poll] all players answers: one card from own hand not already in pass_cards. What happens: Append the chosen card to pass_cards (second pass card).
  5. [update] all players. What happens: Remove each player's pass_cards from their hand and append them to the hand of the player on their left. Clear pass_cards. Nothing is announced about which cards moved.
  6. [sync] all players. What happens: Each player privately sees their new hand.
  7. [ask] seat game.leader answers: any card from own hand. What happens: Remove the card from the leader's hand. Set the leader's played_card, played_suit and played_rank. Set led_suit = played_suit.
  8. [ask] seat game.leader answers: one of the two other seats. What happens: Set the leader's clubs_target to the named seat. Announce the leader's card and target.
  9. [ask] seat (game.leader mod 3) + 1 answers: a card from own hand of led_suit if any is held, otherwise any card from own hand. What happens: Remove the card from hand. Set played_card, played_suit and played_rank.
  10. [ask] seat (game.leader mod 3) + 1 answers: one of the two other seats. What happens: Set clubs_target. Announce the card and the target.
  11. [update] seat (game.leader mod 3) + 1. What happens: Off-suit action for this player, by played_suit. D: vault +1. H: showroom +1. S: if showroom > 0 then showroom -1 and vault +1. C: if the clubs_target's showroom > 0 then the target's showroom -1 and own showroom +1. Recompute score for affected players and announce the action.
  12. [ask] seat ((game.leader + 1) mod 3) + 1 answers: a card from own hand of led_suit if any is held, otherwise any card from own hand. What happens: Remove the card from hand. Set played_card, played_suit and played_rank.
  13. [ask] seat ((game.leader + 1) mod 3) + 1 answers: one of the two other seats. What happens: Set clubs_target. Announce the card and the target.
  14. [update] seat ((game.leader + 1) mod 3) + 1. What happens: Off-suit action, the same as for the second player: D vault +1; H showroom +1; S if showroom > 0 move 1 from showroom to vault; C if the clubs_target's showroom > 0 move 1 from it to own showroom. Recompute score and announce.
  15. [update] all players. What happens: trick_winner = the seat with the highest played_rank among players whose played_suit == led_suit. The winner adds the 3 played cards to won_diamonds, won_hearts, won_spades and won_clubs by each card's suit, and tricks_won +1. The winner then takes the led_suit action using the winner's own clubs_target: D vault +1; H showroom +1; S if showroom > 0 move 1 from showroom to vault; C if the clubs_target's showroom > 0 move 1 from it to the winner's showroom. Set leader = trick_winner. Recompute every score.
  16. [tell] all players. What happens: Announce the three cards, the Clubs targets, the trick winner, every action taken, and every player's showroom, vault and won counts.
  17. [update] all players. What happens: End of hand, applied in order. (1) Diamonds: if one player has strictly the most won_diamonds, that player's vault +1. (2) Hearts: if one player has strictly the most won_hearts, that player's showroom +1. (3) Spades: if one player has strictly the most won_spades and their showroom > 0, that player moves 1 from showroom to vault. (4) Clubs: if one player has strictly the most won_clubs, they take 1 from the showroom of the opponent with the largest showroom; if those two opponents are tied, the opponent on the receiver's left is robbed; nothing moves if that showroom is 0. (5) Each player with tricks_won == 0 gets vault +2. Recompute every score.
  18. [tell] all players. What happens: Announce the end-of-hand actions, the 6 cards in set_aside (revealed), and every score.
  19. [check] all players. What happens: If round_number == 30, end the game. Otherwise round_number +1 and clear every played_card, played_suit, played_rank, clubs_target and led_suit.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, the deck has 36 cards (4 suits x ranks 1-9) and every showroom, vault and score is 0.
  R2. When a hand starts (rounds 1, 11, 21), each player is dealt 10 cards into hand and the other 6 go to set_aside, unseen.
  R3. When a hand starts, the dealer is C (seat 3) for hand 1, A (seat 1) for hand 2 and B (seat 2) for hand 3, and the dealer's left leads the first trick.
  R4. When a hand starts, all players simultaneously choose exactly 2 different cards from their hand, and those cards move to the hand of the player on their left without being announced.
  R5. When a hand starts, every player's won_diamonds, won_hearts, won_spades, won_clubs and tricks_won are reset to 0.
  R6. When the leader plays, any card from hand may be played and its suit becomes led_suit.
  R7. When a player holds a card of led_suit, they must play a card of led_suit; when they hold none, they may play any card.
  R8. When a player plays a card, they name one of the two other seats as clubs_target.
  R9. When a non-leader plays a card not of led_suit, they immediately take that card's suit action before the next player plays.
  R10. When a Diamonds action is taken, the taker's vault increases by 1.
  R11. When a Hearts action is taken, the taker's showroom increases by 1.
  R12. When a Spades action is taken with showroom > 0, the taker's showroom decreases by 1 and vault increases by 1; with showroom 0, nothing happens.
  R13. When a Clubs action is taken from a trick or an off-suit play, 1 crystal moves from the named clubs_target's showroom to the taker's showroom, or nothing happens if that showroom is 0.
  R14. When all three cards are played, the highest rank of led_suit wins the trick, and the winner adds each card to its suit's won count and adds 1 to tricks_won.
  R15. When a trick is won, the winner takes the led_suit action and leads the next trick.
  R16. When a hand ends, for Diamonds, Hearts, Spades and Clubs in that order, the player with strictly the most won cards of that suit takes that suit's action once; on a tie for the most, no one does.
  R17. When an end-of-hand Clubs action is taken, it robs the opponent with the larger showroom, or the opponent on the receiver's left if the two are tied.
  R18. When a hand ends, each player with tricks_won == 0 takes two Diamond actions (vault +2).
  R19. When a hand ends, the 6 set_aside cards are revealed to all players.
  R20. A player's score is always 2 x vault + 1 x showroom.
  R21. When round 30 and the third end-of-hand step finish, the game ends.
  R22. When the game ends, the highest score wins, ties are broken by more vault crystals, and players still tied share the win (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First pass card (poll at the start of a hand) | asked: all players | options: every card in the player's own hand
  - Second pass card | asked: all players | options: every card in the player's own hand except the one already chosen
  - Leader's card | asked: seat game.leader | options: every card in own hand
  - Following player's card | asked: the second and third players of the trick | options: if the player holds any card of led_suit: only those cards; otherwise: every card in own hand
  - Clubs target | asked: each player after playing a card | options: the two seats other than the player's own

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number == 30 after the end-of-hand step of hand 3
  - each player's standing: you.score * 100 + you.vault (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest score (2 x vault + showroom) wins. On a score tie, more vault crystals wins. Players still level share the win, which is the source's draw.
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

- each player: `showroom` (number, visible: public, starts 0): Crystals in the showroom, worth 1 point each
- each player: `vault` (number, visible: public, starts 0): Crystals in the vault, worth 2 points each
- each player: `score` (number, visible: public, starts 0): 2 x vault + 1 x showroom, recomputed after every change
- the table: `round_number` (number, visible: public, starts 1): Current round, 1 to 30, one trick per round
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, suits = 4, ranks_per_suit = 9, lowest_rank = 1, highest_rank = 9, cards_dealt_per_player = 10, cards_set_aside = 6, cards_passed = 2, hands = 3, tricks_per_hand = 10, total_rounds = 30, cards_per_trick = 3, crystals_per_action = 1, vault_crystal_points = 2, showroom_crystal_points = 1, zero_trick_diamond_actions = 2, dealer_hand_1_seat = 3, dealer_hand_2_seat = 1, dealer_hand_3_seat = 2, rank_tiebreak_multiplier = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 100 + you.vault`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
{
  "schema": 1,
  "meta": {
    "id": "diamonds_three_hand_vault",
    "name": "Diamonds: Three-Hand Vault",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, three hands of ten tricks: every suit's action moves crystals into your showroom (1 point) or vault (2 points), or steals from a rival's showroom."
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
        "key": "pass_cards",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "pass_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "showroom",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "vault",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_diamonds",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_hearts",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_spades",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won_clubs",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_rank",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "clubs_target",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
          "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9",
          "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9",
          "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"
        ]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "set_aside",
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
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "new_hand",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "rounds_played",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "club_receiver",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "club_victim",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dealer",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_suit",
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
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "lowest_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "highest_rank",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "cards_set_aside",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_passed",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "cards_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "crystals_per_action",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "vault_crystal_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "showroom_crystal_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "zero_trick_diamond_actions",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "dealer_hand_1_seat",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "dealer_hand_2_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dealer_hand_3_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the empty showrooms and vaults",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "showroom",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "vault",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 1
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
            "key": "deck",
            "value": {
              "calc": "all_cards"
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
      "label": "start of round",
      "do": [
        {
          "set": {
            "key": "round_number",
            "value": {
              "calc": "rounds_played + 1"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": {
              "calc": "(round_number - 1) % tricks_per_hand == 0"
            }
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
            "players": "all",
            "key": "played_suit",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_rank",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "clubs_target",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": {
              "calc": "int((round_number - 1) / tricks_per_hand) + 1"
            },
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "dealer_hand_1_seat if hand_number == 1 else (dealer_hand_2_seat if hand_number == 2 else dealer_hand_3_seat)"
            },
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "dealer % len(players) + 1"
            },
            "if": {
              "calc": "new_hand"
            },
            "text": "Hand {hand_number} begins. Seat {dealer} deals; seat {leader} leads the first trick."
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_cards"
            },
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": [],
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": [],
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_cards",
            "value": [],
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_pick",
            "value": "",
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_diamonds",
            "value": 0,
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_hearts",
            "value": 0,
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_spades",
            "value": 0,
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won_clubs",
            "value": 0,
            "if": {
              "calc": "new_hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0,
            "if": {
              "calc": "new_hand"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "deal",
      "label": "the deal",
      "when": {
        "calc": "new_hand"
      },
      "until": {
        "calc": "len(deck) <= cards_set_aside"
      },
      "max": 20,
      "steps": [
        {
          "use": "update",
          "label": "one card to each seat",
          "do": [
            {
              "set": {
                "key": "pick",
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
                  "calc": "pick"
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
                "key": "pick",
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
                  "calc": "pick"
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
                "key": "pick",
                "value": {
                  "calc": "deck[int(uniform(0, len(deck)))]"
                }
              }
            },
            {
              "append": {
                "player": 3,
                "key": "hand",
                "value": {
                  "calc": "pick"
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
                "key": "set_aside",
                "value": {
                  "calc": "deck"
                },
                "if": {
                  "calc": "len(deck) == cards_set_aside"
                }
              }
            },
            {
              "set": {
                "key": "deck",
                "value": [],
                "if": {
                  "calc": "len(deck) == cards_set_aside"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your dealt hand",
      "when": {
        "calc": "new_hand"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your hand for hand {hand_number}:"
    },
    {
      "use": "poll",
      "phase": "pass",
      "label": "first pass card",
      "when": {
        "calc": "new_hand"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "pass_pick",
      "text": "Choose the first of the {cards_passed} cards you will pass face down to the player on your left. Nobody else learns which cards you pass."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "first pass card set aside",
      "when": {
        "calc": "new_hand"
      },
      "do": [
        {
          "append": {
            "players": "all",
            "key": "pass_cards",
            "value": {
              "calc": "you.pass_pick"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c != you.pass_pick]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_pick",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "pass",
      "label": "second pass card",
      "when": {
        "calc": "new_hand"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pass_pick",
      "text": "Choose the second card you will pass to the player on your left (a different card from your first)."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "the pass",
      "when": {
        "calc": "new_hand"
      },
      "do": [
        {
          "append": {
            "players": "all",
            "key": "pass_cards",
            "value": {
              "calc": "you.pass_pick"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[c for c in you.hand if c not in you.pass_cards] + players[(you.seat + 1) % len(players)].pass_cards"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_pick",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "pass",
      "label": "your new hand",
      "when": {
        "calc": "new_hand"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "After the pass, your hand is:"
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader plays",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
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
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_suit",
              "value": {
                "calc": "$answer[0]"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_rank",
              "value": {
                "calc": "int($answer[1])"
              }
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[0]"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_suit] if any(c[0] == led_suit for c in you.hand) else you.hand"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "Round {round_number}: you lead this trick. Play any card from your hand; its suit becomes the led suit."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader names a Clubs target",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "player",
        "exclude_self": true
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "clubs_target",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} names seat {value} as their Clubs target."
      },
      "text": "Name one of the two other seats as your Clubs target for this trick."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second player plays",
      "to": {
        "where": "you.seat == leader % len(players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
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
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_suit",
              "value": {
                "calc": "$answer[0]"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_rank",
              "value": {
                "calc": "int($answer[1])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Round {round_number}: the led suit is {led_suit}. You are offered only the cards you may play: led-suit cards if you hold any, otherwise any card."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second player names a Clubs target",
      "to": {
        "where": "you.seat == leader % len(players) + 1"
      },
      "answer": {
        "type": "player",
        "exclude_self": true
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "clubs_target",
              "value": "$answer"
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "vault",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'D'"
              },
              "text": "Off-suit Diamonds: seat {player} moves 1 crystal from the supply to their vault."
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "showroom",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'H'"
              },
              "text": "Off-suit Hearts: seat {player} moves 1 crystal from the supply to their showroom."
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "vault",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'S' and players[$seat - 1].showroom > 0"
              },
              "text": "Off-suit Spades: seat {player} moves 1 crystal from their showroom to their vault."
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "showroom",
              "value": {
                "calc": "-crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'S' and players[$seat - 1].showroom > 0"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "showroom",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'C' and players[$answer - 1].showroom > 0"
              },
              "text": "Off-suit Clubs: seat {player} takes 1 crystal from their Clubs target's showroom into their own."
            }
          },
          {
            "adjust": {
              "player": {
                "calc": "$answer"
              },
              "key": "showroom",
              "value": {
                "calc": "-crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'C' and players[$answer - 1].showroom > 0"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "score",
              "value": {
                "calc": "you.vault * vault_crystal_points + you.showroom * showroom_crystal_points"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} names seat {value} as their Clubs target."
      },
      "text": "Name one of the two other seats as your Clubs target. If your card is not of the led suit, you take its suit action now, before the next player plays."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third player plays",
      "to": {
        "where": "you.seat == (leader + 1) % len(players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
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
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_suit",
              "value": {
                "calc": "$answer[0]"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_rank",
              "value": {
                "calc": "int($answer[1])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Round {round_number}: the led suit is {led_suit}. You are offered only the cards you may play: led-suit cards if you hold any, otherwise any card."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third player names a Clubs target",
      "to": {
        "where": "you.seat == (leader + 1) % len(players) + 1"
      },
      "answer": {
        "type": "player",
        "exclude_self": true
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "clubs_target",
              "value": "$answer"
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "vault",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'D'"
              },
              "text": "Off-suit Diamonds: seat {player} moves 1 crystal from the supply to their vault."
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "showroom",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'H'"
              },
              "text": "Off-suit Hearts: seat {player} moves 1 crystal from the supply to their showroom."
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "vault",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'S' and players[$seat - 1].showroom > 0"
              },
              "text": "Off-suit Spades: seat {player} moves 1 crystal from their showroom to their vault."
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "showroom",
              "value": {
                "calc": "-crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'S' and players[$seat - 1].showroom > 0"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "showroom",
              "value": {
                "calc": "crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'C' and players[$answer - 1].showroom > 0"
              },
              "text": "Off-suit Clubs: seat {player} takes 1 crystal from their Clubs target's showroom into their own."
            }
          },
          {
            "adjust": {
              "player": {
                "calc": "$answer"
              },
              "key": "showroom",
              "value": {
                "calc": "-crystals_per_action"
              },
              "if": {
                "calc": "players[$seat - 1].played_suit != led_suit and players[$seat - 1].played_suit == 'C' and players[$answer - 1].showroom > 0"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "score",
              "value": {
                "calc": "you.vault * vault_crystal_points + you.showroom * showroom_crystal_points"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} names seat {value} as their Clubs target."
      },
      "text": "Name one of the two other seats as your Clubs target. If your card is not of the led suit, you take its suit action now."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is won",
      "do": [
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "max([p.played_rank * rank_tiebreak_multiplier + p.seat for p in players if p.played_suit == led_suit]) % rank_tiebreak_multiplier"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "won_diamonds",
            "value": {
              "calc": "count(p.played_suit == 'D' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "won_hearts",
            "value": {
              "calc": "count(p.played_suit == 'H' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "won_spades",
            "value": {
              "calc": "count(p.played_suit == 'S' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "won_clubs",
            "value": {
              "calc": "count(p.played_suit == 'C' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "tricks_won",
            "value": 1
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "vault",
            "value": {
              "calc": "crystals_per_action"
            },
            "if": {
              "calc": "led_suit == 'D'"
            },
            "text": "Diamonds led: seat {player} moves 1 crystal from the supply to their vault."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "showroom",
            "value": {
              "calc": "crystals_per_action"
            },
            "if": {
              "calc": "led_suit == 'H'"
            },
            "text": "Hearts led: seat {player} moves 1 crystal from the supply to their showroom."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "vault",
            "value": {
              "calc": "crystals_per_action"
            },
            "if": {
              "calc": "led_suit == 'S' and players[trick_winner - 1].showroom > 0"
            },
            "text": "Spades led: seat {player} moves 1 crystal from their showroom to their vault."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "showroom",
            "value": {
              "calc": "-crystals_per_action"
            },
            "if": {
              "calc": "led_suit == 'S' and players[trick_winner - 1].showroom > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "showroom",
            "value": {
              "calc": "crystals_per_action"
            },
            "if": {
              "calc": "led_suit == 'C' and players[players[trick_winner - 1].clubs_target - 1].showroom > 0"
            },
            "text": "Clubs led: seat {player} takes 1 crystal from their Clubs target's showroom into their own."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "players[trick_winner - 1].clubs_target"
            },
            "key": "showroom",
            "value": {
              "calc": "-crystals_per_action"
            },
            "if": {
              "calc": "led_suit == 'C' and players[players[trick_winner - 1].clubs_target - 1].showroom > 0"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            }
          }
        },
        {
          "adjust": {
            "key": "rounds_played",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.vault * vault_crystal_points + you.showroom * showroom_crystal_points"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "trick",
      "label": "the trick result",
      "to": "all",
      "text": "Round {round_number}: {led_suit} was led and seat {trick_winner} won the trick with the highest {led_suit}, takes the {led_suit} action and leads next. Every player's played card, Clubs target, showroom, vault, score and won counts are shown on the table."
    },
    {
      "use": "update",
      "phase": "end of hand",
      "label": "end of hand",
      "when": {
        "calc": "round_number % tricks_per_hand == 0"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.won_diamonds > max([p.won_diamonds for p in players if p.seat != you.seat])"
            },
            "key": "vault",
            "value": {
              "calc": "crystals_per_action"
            },
            "text": "End of hand: seat {player} won the most Diamonds and moves 1 crystal from the supply to their vault."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.won_hearts > max([p.won_hearts for p in players if p.seat != you.seat])"
            },
            "key": "showroom",
            "value": {
              "calc": "crystals_per_action"
            },
            "text": "End of hand: seat {player} won the most Hearts and moves 1 crystal from the supply to their showroom."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.won_spades > max([p.won_spades for p in players if p.seat != you.seat]) and you.showroom > 0"
            },
            "key": "vault",
            "value": {
              "calc": "crystals_per_action"
            },
            "text": "End of hand: seat {player} won the most Spades and moves 1 crystal from their showroom to their vault."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.won_spades > max([p.won_spades for p in players if p.seat != you.seat]) and you.showroom > 0"
            },
            "key": "showroom",
            "value": {
              "calc": "-crystals_per_action"
            }
          }
        },
        {
          "set": {
            "key": "club_receiver",
            "value": {
              "calc": "max([p.seat for p in players if p.won_clubs > max([q.won_clubs for q in players if q.seat != p.seat])] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "club_victim",
            "value": {
              "calc": "((club_receiver % len(players)) + 1) if players[club_receiver % len(players)].showroom >= players[(club_receiver + 1) % len(players)].showroom else (((club_receiver + 1) % len(players)) + 1)"
            },
            "if": {
              "calc": "club_receiver > 0"
            }
          }
        },
        {
          "set": {
            "key": "club_victim",
            "value": 0,
            "if": {
              "calc": "club_receiver == 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "club_receiver"
            },
            "key": "showroom",
            "value": {
              "calc": "crystals_per_action"
            },
            "if": {
              "calc": "club_receiver > 0 and players[club_victim - 1].showroom > 0"
            },
            "text": "End of hand: seat {player} won the most Clubs and takes 1 crystal from seat {club_victim}'s showroom."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "club_victim"
            },
            "key": "showroom",
            "value": {
              "calc": "-crystals_per_action"
            },
            "if": {
              "calc": "club_receiver > 0 and club_victim > 0 and players[club_victim - 1].showroom > 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.tricks_won == 0"
            },
            "key": "vault",
            "value": {
              "calc": "zero_trick_diamond_actions * crystals_per_action"
            },
            "text": "End of hand: seat {player} won no tricks and takes two Diamond actions, adding 2 crystals to their vault."
          }
        },
        {
          "set": {
            "key": "revealed_cards",
            "value": {
              "calc": "set_aside"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.vault * vault_crystal_points + you.showroom * showroom_crystal_points"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "end of hand",
      "label": "end of hand report",
      "when": {
        "calc": "round_number % tricks_per_hand == 0"
      },
      "to": "all",
      "text": "Hand {hand_number} is over. The {cards_set_aside} set-aside cards were: {revealed_cards}. All cards are gathered for the next deal. Every player's showroom, vault and score are shown on the table."
    },
    {
      "use": "check",
      "phase": "end of hand",
      "label": "after the last hand",
      "when": {
        "calc": "round_number == total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number == total_rounds and rounds_played >= total_rounds"
      },
      "rank_by": "you.score * 100 + you.vault",
      "text": "Winner: {result}. Final scores: Seat A {players[0].score} (vault {players[0].vault}), Seat B {players[1].score} (vault {players[1].vault}), Seat C {players[2].score} (vault {players[2].vault})."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 31,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "Three players sit in fixed order: A (seat 1), B (seat 2), C (seat 3). 'Left' means the next player in that order: A's left is B, B's left is C, C's left is A.\n\nThe deck has {deck_size} cards: {suits} suits (Diamonds D, Hearts H, Spades S, Clubs C), each ranked {lowest_rank} to {highest_rank}; cards are written suit letter plus rank, e.g. D7. The crystal supply is unlimited. Each player has a showroom and a vault, both starting empty; their counts are public. For each hand, how many cards of each suit every player has won, and how many tricks each player has won, are public.\n\nThe game is {hands} hands of {tricks_per_hand} tricks: {total_rounds} rounds, one trick per round. The dealer is C for hand 1, A for hand 2 and B for hand 3. The player to the dealer's left leads the first trick of the hand.\n\nDEAL AND PASS (first round of each hand only): all {deck_size} cards are shuffled; {cards_dealt_per_player} cards are dealt face down to each player and the remaining {cards_set_aside} are set aside face down, seen by no one during the hand. All players at the same moment secretly choose exactly {cards_passed} different cards from their hand, and give them to the player on their left. You see your new hand; the passed cards are not announced to anyone else. Every player's won-card counts and trick count are reset to 0.\n\nPLAYING A TRICK (every round): the leader plays any card from their hand face up and names one opponent as their Clubs target. Then the next player to the left plays a card and names a Clubs target, then the third player does the same. The suit of the first card is the led suit. A player who holds a card of the led suit must play one; a player who holds none may play any card (you are only offered the cards you may play). OFF-SUIT ACTION: when a player plays a card not of the led suit, they immediately take that card's suit action, before the next player plays; a card of the led suit gives no immediate action. The highest card of the led suit wins the trick. The winner adds the {cards_per_trick} cards to their won counts by suit (each card counts in its own suit) and adds 1 to their trick count, then takes the led suit's action, and leads the next trick of the same hand. Everything played and every action taken is announced to all players.\n\nSUIT ACTIONS (for the player taking the action):\n- Diamonds: move {crystals_per_action} crystal from the supply to your vault.\n- Hearts: move {crystals_per_action} crystal from the supply to your showroom.\n- Spades: move {crystals_per_action} crystal from your showroom to your vault. If your showroom is empty, nothing happens.\n- Clubs (from a trick or an off-suit play): move {crystals_per_action} crystal from your named Clubs target's showroom to your own showroom. If that showroom is empty, nothing happens.\n\nEND OF HAND (after the 10th trick of each hand): for each suit in turn (Diamonds, Hearts, Spades, Clubs), the player with strictly the most won cards of that suit takes that suit's action once. If the top count is tied, no one takes it. An end-of-hand Clubs action robs the opponent with the largest showroom; if those opponents are tied, it robs the one on the receiver's left (nothing moves if that showroom is empty). Each player who won 0 tricks in the hand takes {zero_trick_diamond_actions} Diamond actions. The {cards_set_aside} set-aside cards are then revealed, and all cards are gathered for the next deal.\n\nSCORING: each vault crystal is worth {vault_crystal_points} points and each showroom crystal {showroom_crystal_points} point; your score is always recomputed as 2 x vault + 1 x showroom. After the 30th round and the third end-of-hand step, the game ends. The player with the highest score wins. If players tie on score, the tied player with more vault crystals wins. If they are still tied, the game is a draw and they share the win."
}
````
