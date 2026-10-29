# 45 coder

- time: 2026-10-28T03:56:46+00:00 (194.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 f80f16269efeac61, reply sha256 b9c31867acdcfb5d

## Sent

````
# Task: write the XColos game file for "Mini Mariáš with Hidden Talon"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

DECK: 24 cards in four suits (Hearts, Bells, Leaves, Acorns). Each suit has A, 10, K, O (Ober), U (Unter) and 9, ranking high to low A, 10, K, O, U, 9. Card points: each Ace 10, each Ten 10, all other cards 0. The side that wins the last (7th) trick of a deal also gets 10. At most 90 card points are available in a deal; fewer if Aces or Tens lie in the talon.

SEATS AND MATCH: Seats 1, 2 and 3. Seat order runs 1, 2, 3, 1 and so on. The match has 5 deals of 8 rounds each, 40 rounds in total. The eldest is Seat 1 in deal 1, Seat 2 in deal 2, Seat 3 in deal 3, Seat 1 in deal 4 and Seat 2 in deal 5. Match scores start at 0 and are public. There is no talk at any time. Hands are shown to their owner sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low.

ROUND 1 OF EACH DEAL (DEAL AND BID):
(a) Shuffle all 24 cards. Deal 7 cards privately to each seat. The remaining 3 cards are the talon. The talon is face down, is never played and is never shown to anyone, including at the end of the deal. Each player sees only their own hand.
(b) All three players bid at the same time without seeing the other bids. The options are PASS, 40, 50 or 60.
(c) If all three pass, the deal is not played. Rounds 2-8 of this deal are skipped with no plays and no scoring.
(d) Otherwise the highest bid wins and that player is the declarer. If several players tie for the highest bid, it goes to the tied player with the lowest match score. If they are still tied, it goes to the tied player who comes first in seat order starting from the eldest.
(e) The declarer chooses trump: Hearts, Bells, Leaves or Acorns.
(f) The declarer, the contract (the winning bid) and trump are announced. The other two players are the defenders, and their card points this deal are pooled together.
(g) Flek: the two defenders each choose FLEK or NO at the same time. Both choices are announced.
(h) Stake V: start at 1 for a 40 contract, 2 for 50 and 4 for 60. Double V if trump is Hearts. Double V again if at least one defender chose FLEK. V is announced.

ROUNDS 2-8 OF EACH DEAL (ONE TRICK PER ROUND):
(a) The declarer leads in round 2. In later rounds, the winner of the previous trick leads. The leader plays any card from their hand face up. Then the next player in seat order plays, then the third. Each card is shown to everyone as it is played.
(b) LEGAL CARDS. The 'currently winning card' is the card that would win the trick right now under rule (c). The following rules apply to every player, whoever is currently winning.
  1. If you hold a card of the suit led, you must play a card of that suit. If the currently winning card is of the suit led, you must play a higher card of that suit if you have one. This includes the case where trump was led. If the currently winning card is a trump and the suit led is not trump, any card of the suit led is legal.
  2. If you hold no card of the suit led but hold a trump, you must play a trump. If a trump has already been played in this trick, you must play a higher trump than the highest one played if you have one; otherwise any trump.
  3. If you hold neither the suit led nor a trump, you may play any card.
(c) The trick is won by the highest trump in it. If it contains no trump, it is won by the highest card of the suit led.
(d) The trick's card points go to the declarer if the declarer won it, or to the defenders' pooled total if either defender won it. In round 8 the last-trick 10 also goes to the side that won the trick. Running totals are announced.
(e) The trick winner leads the next round.

SCORING AT THE END OF ROUND 8 (only if the deal was played): the contract is made if the declarer's card points are at least the contract (40, 50 or 60).
- Made: the declarer gains 2V and each defender loses V.
- Failed: the declarer loses 2V and each defender gains V.
Match scores are announced.

END: the game ends after round 40.

How the winner is decided: After round 40, the player with the highest match score wins. If two or three players tie for the highest score, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Mini Mariáš with Hidden Talon (3 to 3 players, best with 3)

Three players play 5 deals of a 24-card trick-taking game: each deal starts with a sealed bid for a point contract, then 7 tricks with strict follow, overtake and trump rules, and the stake scales with the contract, Hearts trump and flek.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. match score
  - each player: hand (list, starts []); only its owner sees it. cards held this deal, shown to the owner sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low
  - each player: bid (number, starts 0); only its owner sees it. this deal's bid: 0 for PASS, otherwise 40, 50 or 60
  - each player: is_declarer (bool, starts False); everyone sees it. whether this seat is the declarer this deal
  - each player: flek (text, starts ''); everyone sees it. a defender's flek choice this deal: FLEK or NO, empty for the declarer
  - each player: played_card (text, starts ''); everyone sees it. the card this seat played to the current trick
  - the table: round_number (number, starts 0); everyone sees it. rounds played in the match, 1 to 40
  - the table: deal_number (number, starts 0); everyone sees it. the current deal, 1 to 5
  - the table: round_in_deal (number, starts 0); everyone sees it. the round within the deal, 1 to 8
  - the table: eldest (number, starts 1); everyone sees it. the eldest seat this deal: 1, 2, 3, 1, 2 for deals 1 to 5
  - the table: deck (list, starts []); hidden from all players. undealt cards while dealing; each card is written as 'Suit Rank', e.g. 'Hearts A'
  - the table: talon (list, starts []); hidden from all players. the 3 face-down cards, never played and never shown
  - the table: deal_played (bool, starts False); everyone sees it. false when all three players passed this deal
  - the table: declarer (number, starts 0); everyone sees it. the declarer's seat this deal, 0 if none
  - the table: contract (number, starts 0); everyone sees it. the winning bid: 40, 50 or 60
  - the table: trump (text, starts ''); everyone sees it. the trump suit
  - the table: stake_v (number, starts 0); everyone sees it. the stake V this deal
  - the table: declarer_points (number, starts 0); everyone sees it. the declarer's card points this deal
  - the table: defender_points (number, starts 0); everyone sees it. the defenders' pooled card points this deal
  - the table: leader (number, starts 0); everyone sees it. the seat leading the current trick
  - the table: led_suit (text, starts ''); everyone sees it. the suit of the first card of the current trick
  - the table: trick (list, starts []); everyone sees it. the cards played to the current trick, in order
  - the table: winning_seat (number, starts 0); everyone sees it. the seat whose card currently wins the trick, and after the trick, its winner
  - parameters, each kept as a table attribute: deck_size = 24, suits = 4, cards_per_suit = 6, hand_size = 7, talon_size = 3, ace_points = 10, ten_points = 10, other_card_points = 0, last_trick_bonus = 10, max_card_points = 90, deals = 5, rounds_per_deal = 8, tricks_per_deal = 7, total_rounds = 40, bid_low = 40, bid_mid = 50, bid_high = 60, stake_for_40 = 1, stake_for_50 = 2, stake_for_60 = 4, hearts_trump_multiplier = 2, flek_multiplier = 2, declarer_win_multiplier = 2, defender_win_multiplier = 1, starting_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 sit in seat order 1, 2, 3, 1 and so on.
  2. Every match score is set to 0, public.
  3. The 24 cards are Hearts, Bells, Leaves and Acorns, each with A, 10, K, O, U and 9. Rank values from high to low are A=6, 10=5, K=4, O=3, U=2, 9=1.
  4. There is no talk at any time in the match.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_number += 1; round_in_deal = ((round_number - 1) mod 8) + 1; deal_number = floor((round_number - 1) / 8) + 1; when round_in_deal == 1, eldest = ((deal_number - 1) mod 3) + 1.
  2. [update] all players. What happens: When round_in_deal == 1: deck = all 24 cards. Every hand is emptied; bid = 0, flek = '', is_declarer = false, played_card = ''. declarer = 0, contract = 0, trump = '', stake_v = 0, declarer_points = 0, defender_points = 0. Deal 7 cards to each hand, each a random draw removed from deck. The remaining 3 cards are moved from deck to talon.
  3. [sync] all players. What happens: When round_in_deal == 1, each player sees only their own hand, sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low.
  4. [poll] all players answers: one of PASS, 40, 50, 60. What happens: When round_in_deal == 1: bid = 0 for PASS, otherwise the number. Nobody sees another bid.
  5. [update] all players. What happens: When round_in_deal == 1: deal_played = (max bid > 0). If deal_played: among the seats with the highest bid, the one with the lowest score; if still tied, the one first in seat order starting from eldest. That seat becomes declarer, contract = its bid, and its is_declarer = true.
  6. [tell] all players. What happens: When round_in_deal == 1 and not deal_played: 'All three passed; deal {deal_number} is not played.'
  7. [ask] the declarer answers: one of Hearts, Bells, Leaves, Acorns. What happens: When round_in_deal == 1 and deal_played: trump = the answer.
  8. [tell] all players. What happens: When round_in_deal == 1 and deal_played: 'Declarer: Seat {declarer}, contract {contract}, trump {trump}. The other two seats are the defenders.'
  9. [poll] the two defenders answers: one of FLEK, NO. What happens: When round_in_deal == 1 and deal_played: flek = the answer, then both choices are announced.
  10. [update] all players. What happens: When round_in_deal == 1 and deal_played: stake_v = 1 if contract == 40, 2 if 50, 4 if 60; multiply by 2 if trump == Hearts; multiply by 2 again if at least one defender has flek == FLEK. Announce 'Flek: {flek choices}. V = {stake_v}.'
  11. [update] all players. What happens: When round_in_deal >= 2 and deal_played: trick = [], led_suit = '', played_card = '' for every seat, winning_seat = 0. leader = declarer if round_in_deal == 2, otherwise the previous trick's winner.
  12. [ask] the seat equal to leader answers: one card from own hand (any card). What happens: When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick; led_suit = its suit; winning_seat = leader. The card is shown to everyone.
  13. [ask] the next seat after leader in seat order answers: one legal card from own hand (rules R10 to R14). What happens: When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick. winning_seat is updated: a trump beats any non-trump, a higher trump beats a lower trump, and a higher card of led_suit beats the current winner when no trump is in the trick. The card is shown to everyone. JUDGED: a referee rules true or false on "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card."; write this step's `when` as {"prose": that sentence, verbatim}.
  14. [ask] the third seat (the seat before leader in seat order) answers: one legal card from own hand (rules R10 to R14). What happens: When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick; winning_seat is updated as in the previous step. The card is shown to everyone. JUDGED: a referee rules true or false on "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card."; write this step's `when` as {"prose": that sentence, verbatim}.
  15. [update] all players. What happens: When round_in_deal >= 2 and deal_played: pts = 10 x (number of Aces and Tens in trick), plus 10 if round_in_deal == 8. If winning_seat == declarer, declarer_points += pts, otherwise defender_points += pts. Announce 'Seat {winning_seat} wins the trick. Declarer {declarer_points}, defenders {defender_points}.'
  16. [update] all players. What happens: When round_in_deal == 8 and deal_played: if declarer_points >= contract, the declarer's score += 2 x stake_v and each defender's score -= stake_v; otherwise the declarer's score -= 2 x stake_v and each defender's score += stake_v. Announce the result and the match scores.
  17. [check] all players. What happens: End the game if round_number == 40; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a deal starts (rounds 1, 9, 17, 25, 33), then all 24 cards are shuffled, each seat's hand gets 7 cards and the talon gets the remaining 3.
  R2. When cards are dealt, then each player sees only their own hand, and the talon is never shown to anyone, even at the end of the deal.
  R3. When deals 1, 2, 3, 4 and 5 are dealt, then the eldest is Seat 1, 2, 3, 1 and 2 respectively.
  R4. When bidding, then all three players choose PASS, 40, 50 or 60 at the same time, without seeing the other bids.
  R5. When all three players pass, then the deal is not played and rounds 2-8 of that deal have no plays and no scoring.
  R6. When at least one player bids, then the highest bidder becomes declarer and contract equals that bid.
  R7. When several players tie for the highest bid, then the tied player with the lowest match score becomes declarer; if they are still tied, the tied player first in seat order starting from the eldest does.
  R8. When the declarer is chosen, then the declarer picks trump from Hearts, Bells, Leaves and Acorns, and the declarer, the contract and trump are announced.
  R9. When trump is announced, then the two defenders choose FLEK or NO at the same time, and stake_v = 1, 2 or 4 for a 40, 50 or 60 contract, doubled if trump is Hearts and doubled again if at least one defender chose FLEK (e.g. a 60 contract in Hearts with a flek gives V = 16).
  R10. When a player holds a card of the suit led, then they must play a card of that suit.
  R11. When the currently winning card is of the suit led and the player holds a higher card of that suit, then they must play a higher card of that suit, including when trump was led.
  R12. When the currently winning card is a trump and the suit led is not trump, then any card of the suit led is legal for a player who holds that suit.
  R13. When a player holds no card of the suit led but holds a trump, then they must play a trump, and if a trump has already been played to the trick they must play a higher trump than the highest one played if they have one, otherwise any trump.
  R14. When a player holds neither the suit led nor a trump, then they may play any card.
  R15. When a trick is complete, then the highest trump in it wins, or if it contains no trump, the highest card of the suit led wins, with ranks A > 10 > K > O > U > 9.
  R16. When the declarer wins a trick, then declarer_points increases by 10 for each Ace and each Ten in it; when a defender wins it, defender_points increases by the same amount.
  R17. When the round 8 trick (the 7th trick) is won, then the winning side also gets 10 card points.
  R18. When round 2 of a played deal begins, then the declarer leads; in rounds 3 to 8, the winner of the previous trick leads, and play continues in seat order.
  R19. When a played deal ends and declarer_points >= contract, then the declarer gains 2 x stake_v and each defender loses stake_v.
  R20. When a played deal ends and declarer_points < contract, then the declarer loses 2 x stake_v and each defender gains stake_v.
  R21. When round 40 is over, then the game ends, the highest match score wins and players tied at the top share a draw.
  R22. When at any point in the match, then there is no talk between players.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid (round 1 of each deal) | asked: all three seats | options: PASS, 40, 50, 60
  - Trump choice | asked: the declarer only | options: Hearts, Bells, Leaves, Acorns
  - Flek | asked: each of the two defenders; the declarer is not asked | options: FLEK, NO
  - Lead a card | asked: the leader of the trick | options: every card in their hand
  - Play to the trick (second and third seat) | asked: the two seats after the leader, in seat order | options: Holding the suit led, with the currently winning card of the suit led: the cards of that suit higher than it, or if none, any card of that suit. Holding the suit led, with the currently winning card a trump of another suit: any card of the suit led. Void in the suit led but holding a trump: the trumps higher than the highest trump in the trick, or if none, any trump. Holding neither: any card in hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number == 40
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's match score after round 40. The highest score wins, and players tied at the top share the win (a draw among them).
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

- each player: `score` (number, visible: public, starts 0): match score
- the table: `declarer` (number, visible: public, starts 0): the declarer's seat this deal, 0 if none
- the table: `contract` (number, visible: public, starts 0): the winning bid: 40, 50 or 60
- the table: `stake_v` (number, visible: public, starts 0): the stake V this deal
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, suits = 4, cards_per_suit = 6, hand_size = 7, talon_size = 3, ace_points = 10, ten_points = 10, other_card_points = 0, last_trick_bonus = 10, max_card_points = 90, deals = 5, rounds_per_deal = 8, tricks_per_deal = 7, total_rounds = 40, bid_low = 40, bid_mid = 50, bid_high = 60, stake_for_40 = 1, stake_for_50 = 2, stake_for_60 = 4, hearts_trump_multiplier = 2, flek_multiplier = 2, declarer_win_multiplier = 2, defender_win_multiplier = 1, starting_score = 0
- the game ends with ONE ending whose `rank_by` is `you.score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "mini_marias_hidden_talon",
    "name": "Mini Mariáš with Hidden Talon",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, five deals of a 24-card trick-taking game: a sealed bid, a trump call, flek, then seven strict tricks."
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
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "is_declarer",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "flek",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
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
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_in_deal",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eldest",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "talon",
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
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Hearts A",
          "Hearts 10",
          "Hearts K",
          "Hearts O",
          "Hearts U",
          "Hearts 9",
          "Bells A",
          "Bells 10",
          "Bells K",
          "Bells O",
          "Bells U",
          "Bells 9",
          "Leaves A",
          "Leaves 10",
          "Leaves K",
          "Leaves O",
          "Leaves U",
          "Leaves 9",
          "Acorns A",
          "Acorns 10",
          "Acorns K",
          "Acorns O",
          "Acorns U",
          "Acorns 9"
        ]
      },
      {
        "key": "higher_pairs",
        "visible": "none",
        "type": "list",
        "initial": [
          "A0",
          "AK",
          "AO",
          "AU",
          "A9",
          "0K",
          "0O",
          "0U",
          "09",
          "KO",
          "KU",
          "K9",
          "OU",
          "O9",
          "U9"
        ]
      },
      {
        "key": "suit_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Hearts",
          "Bells",
          "Leaves",
          "Acorns"
        ]
      },
      {
        "key": "win_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "high_bid",
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
        "key": "deal_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "declarer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "contract",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "stake_v",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "declarer_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "defender_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "winning_seat",
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
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "talon_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ace_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "ten_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "other_card_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_trick_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "max_card_points",
        "visible": "public",
        "type": "number",
        "initial": 90
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rounds_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "bid_low",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "bid_mid",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "bid_high",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "stake_for_40",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "stake_for_50",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stake_for_60",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "hearts_trump_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "flek_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "declarer_win_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "defender_win_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "match scores start",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "eldest",
            "value": 1
          }
        }
      ],
      "text": "Seats 1, 2 and 3 sit in seat order 1, 2, 3, 1 and so on. Every match score starts at {starting_score}."
    },
    {
      "use": "tell",
      "label": "no talk",
      "to": "all",
      "text": "The deck is Hearts, Bells, Leaves and Acorns, each with A, 10, K, O, U and 9 (high to low). There is no talk at any time in this match."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "count",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_deal",
            "value": {
              "calc": "(round_number - 1) % rounds_per_deal + 1"
            }
          }
        },
        {
          "set": {
            "key": "deal_number",
            "value": {
              "calc": "(round_number - 1) // rounds_per_deal + 1"
            }
          }
        },
        {
          "set": {
            "key": "eldest",
            "value": {
              "calc": "(deal_number - 1) % len(players) + 1"
            },
            "if": {
              "calc": "round_in_deal == 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "reset for a new deal",
      "when": {
        "calc": "round_in_deal == 1"
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
            "key": "talon",
            "value": []
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
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "flek",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_declarer",
            "value": false
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
            "key": "offer",
            "value": []
          }
        },
        {
          "set": {
            "key": "deal_played",
            "value": false
          }
        },
        {
          "set": {
            "key": "declarer",
            "value": 0
          }
        },
        {
          "set": {
            "key": "contract",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trump",
            "value": ""
          }
        },
        {
          "set": {
            "key": "stake_v",
            "value": 0
          }
        },
        {
          "set": {
            "key": "declarer_points",
            "value": 0
          }
        },
        {
          "set": {
            "key": "defender_points",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trick",
            "value": []
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
            "key": "winning_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "win_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "leader",
            "value": 0
          }
        }
      ],
      "text": "Deal {deal_number} of {deals} begins. The eldest is Seat {eldest}. All {deck_size} cards are shuffled."
    },
    {
      "use": "repeat",
      "phase": "deal",
      "label": "deal the cards",
      "until": {
        "calc": "round_in_deal != 1 or len(deck) == 0"
      },
      "max": 10,
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
                "key": "talon",
                "value": {
                  "calc": "deck"
                },
                "if": {
                  "calc": "len(deck) == talon_size"
                }
              }
            },
            {
              "set": {
                "key": "deck",
                "value": [],
                "if": {
                  "calc": "len(deck) == talon_size"
                }
              }
            },
            {
              "set": {
                "players": "all",
                "key": "hand",
                "value": {
                  "calc": "[c for c in full_deck if c in you.hand]"
                },
                "if": {
                  "calc": "len(deck) == 0"
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
      "label": "your hand",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score"
      ],
      "text": "Your hand for deal {deal_number}:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bid",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "PASS",
          "40",
          "50",
          "60"
        ]
      },
      "store": "bid_choice",
      "text": "Deal {deal_number}: bid in secret. Choose PASS, 40, 50 or 60: the card points you promise to take as declarer. Nobody sees another bid. The highest bid becomes declarer; a tie goes to the tied player with the lowest match score, then to the tied player first in seat order from the eldest (Seat {eldest})."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "find the declarer",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "bid_low if you.bid_choice == '40' else (bid_mid if you.bid_choice == '50' else (bid_high if you.bid_choice == '60' else 0))"
            }
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "deal_played",
            "value": {
              "calc": "high_bid > 0"
            }
          }
        },
        {
          "set": {
            "key": "declarer",
            "value": {
              "calc": "[p.seat for p in players if p.bid == high_bid and p.score * 10 + (p.seat - eldest) % len(players) == min([q.score * 10 + (q.seat - eldest) % len(players) for q in players if q.bid == high_bid])][0]"
            },
            "if": {
              "calc": "deal_played"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "high_bid"
            },
            "if": {
              "calc": "deal_played"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == declarer"
            },
            "key": "is_declarer",
            "value": true,
            "if": {
              "calc": "deal_played"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "all passed",
      "when": {
        "calc": "round_in_deal == 1 and not deal_played"
      },
      "to": "all",
      "text": "All three passed; deal {deal_number} is not played."
    },
    {
      "use": "ask",
      "phase": "bid",
      "label": "choose trump",
      "when": {
        "calc": "round_in_deal == 1 and deal_played"
      },
      "to": {
        "where": "you.seat == declarer"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Hearts",
          "Bells",
          "Leaves",
          "Acorns"
        ]
      },
      "verify": {
        "bind": "trump_pick"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "trump",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You are the declarer with a contract of {contract}. Choose trump: Hearts, Bells, Leaves or Acorns. Hearts trump doubles the stake."
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the contract",
      "when": {
        "calc": "round_in_deal == 1 and deal_played"
      },
      "to": "all",
      "text": "Declarer: Seat {declarer}, contract {contract}, trump {trump}. The other two seats are the defenders."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "flek",
      "when": {
        "calc": "round_in_deal == 1 and deal_played"
      },
      "to": {
        "where": "not you.is_declarer"
      },
      "answer": {
        "type": "choice",
        "options": [
          "FLEK",
          "NO"
        ]
      },
      "store": "flek",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says {value}."
      },
      "text": "You are a defender against Seat {declarer}'s contract of {contract} with {trump} trump. Choose FLEK or NO at the same time as the other defender. If at least one defender chooses FLEK, the stake V is doubled; if both choose NO, it is not."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the stake",
      "when": {
        "calc": "round_in_deal == 1 and deal_played"
      },
      "do": [
        {
          "set": {
            "key": "stake_v",
            "value": {
              "calc": "(stake_for_40 if contract == bid_low else (stake_for_50 if contract == bid_mid else stake_for_60)) * (hearts_trump_multiplier if trump == 'Hearts' else 1) * (flek_multiplier if count(p.flek == 'FLEK' for p in players) > 0 else 1)"
            }
          }
        }
      ],
      "text": "V = {stake_v} (contract {contract}, trump {trump})."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "a new trick",
      "when": {
        "calc": "round_in_deal >= 2 and deal_played"
      },
      "do": [
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "declarer if round_in_deal == 2 else winning_seat"
            }
          }
        },
        {
          "set": {
            "key": "trick",
            "value": []
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
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": []
          }
        },
        {
          "set": {
            "key": "winning_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "win_card",
            "value": ""
          }
        }
      ],
      "text": "Trick {round_in_deal} of deal {deal_number} (round {round_number}): Seat {leader} leads. Trump is {trump}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "lead a card",
      "when": {
        "calc": "round_in_deal >= 2 and deal_played"
      },
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "lead_card"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
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
            "append": {
              "key": "trick",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "[s for s in suit_names if s[0] == $answer[0]][0]"
              }
            }
          },
          {
            "set": {
              "key": "win_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "winning_seat",
              "value": "$seat"
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_suit[0] and (win_card[0] != led_suit[0] or (c[-1] + win_card[-1]) in higher_pairs)] if len([c for c in you.hand if c[0] == led_suit[0] and (win_card[0] != led_suit[0] or (c[-1] + win_card[-1]) in higher_pairs)]) > 0 else ([c for c in you.hand if c[0] == led_suit[0]] if len([c for c in you.hand if c[0] == led_suit[0]]) > 0 else ([c for c in you.hand if c[0] == trump[0] and win_card[0] == trump[0] and (c[-1] + win_card[-1]) in higher_pairs] if len([c for c in you.hand if c[0] == trump[0] and win_card[0] == trump[0] and (c[-1] + win_card[-1]) in higher_pairs]) > 0 else ([c for c in you.hand if c[0] == trump[0]] if len([c for c in you.hand if c[0] == trump[0]]) > 0 else you.hand)))"
              }
            }
          }
        ]
      },
      "text": "You lead trick {round_in_deal}. Trump is {trump}. Play any card from your hand."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second card",
      "when": {
        "prose": "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card."
      },
      "to": {
        "where": "you.seat == leader % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "second_card"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
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
            "append": {
              "key": "trick",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "winning_seat",
              "value": "$seat",
              "if": {
                "calc": "($answer[0] == trump[0] and win_card[0] != trump[0]) or ($answer[0] == win_card[0] and ($answer[-1] + win_card[-1]) in higher_pairs)"
              }
            }
          },
          {
            "set": {
              "key": "win_card",
              "value": "$answer",
              "if": {
                "calc": "($answer[0] == trump[0] and win_card[0] != trump[0]) or ($answer[0] == win_card[0] and ($answer[-1] + win_card[-1]) in higher_pairs)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_suit[0] and (win_card[0] != led_suit[0] or (c[-1] + win_card[-1]) in higher_pairs)] if len([c for c in you.hand if c[0] == led_suit[0] and (win_card[0] != led_suit[0] or (c[-1] + win_card[-1]) in higher_pairs)]) > 0 else ([c for c in you.hand if c[0] == led_suit[0]] if len([c for c in you.hand if c[0] == led_suit[0]]) > 0 else ([c for c in you.hand if c[0] == trump[0] and win_card[0] == trump[0] and (c[-1] + win_card[-1]) in higher_pairs] if len([c for c in you.hand if c[0] == trump[0] and win_card[0] == trump[0] and (c[-1] + win_card[-1]) in higher_pairs]) > 0 else ([c for c in you.hand if c[0] == trump[0]] if len([c for c in you.hand if c[0] == trump[0]]) > 0 else you.hand)))"
              }
            }
          }
        ]
      },
      "text": "Trick {round_in_deal}: {led_suit} was led; cards so far {trick}; Seat {winning_seat} is winning. Trump is {trump}. Play one of the legal cards offered."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third card",
      "when": {
        "prose": "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card."
      },
      "to": {
        "where": "you.seat == (leader + 1) % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "third_card"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
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
            "append": {
              "key": "trick",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "winning_seat",
              "value": "$seat",
              "if": {
                "calc": "($answer[0] == trump[0] and win_card[0] != trump[0]) or ($answer[0] == win_card[0] and ($answer[-1] + win_card[-1]) in higher_pairs)"
              }
            }
          },
          {
            "set": {
              "key": "win_card",
              "value": "$answer",
              "if": {
                "calc": "($answer[0] == trump[0] and win_card[0] != trump[0]) or ($answer[0] == win_card[0] and ($answer[-1] + win_card[-1]) in higher_pairs)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": []
            }
          }
        ]
      },
      "text": "Trick {round_in_deal}: {led_suit} was led; cards so far {trick}; Seat {winning_seat} is winning. Trump is {trump}. Play one of the legal cards offered."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "score the trick",
      "when": {
        "calc": "round_in_deal >= 2 and deal_played"
      },
      "do": [
        {
          "set": {
            "key": "trick_points",
            "value": {
              "calc": "sum([ace_points if c[-1] == 'A' else (ten_points if c[-1] == '0' else other_card_points) for c in trick]) + (last_trick_bonus if round_in_deal == rounds_per_deal else 0)"
            }
          }
        },
        {
          "adjust": {
            "key": "declarer_points",
            "value": {
              "calc": "trick_points"
            },
            "if": {
              "calc": "winning_seat == declarer"
            }
          }
        },
        {
          "adjust": {
            "key": "defender_points",
            "value": {
              "calc": "trick_points"
            },
            "if": {
              "calc": "winning_seat != declarer"
            }
          }
        }
      ],
      "text": "Seat {winning_seat} wins the trick {trick}. Declarer {declarer_points}, defenders {defender_points}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the deal",
      "when": {
        "calc": "round_in_deal == rounds_per_deal and deal_played"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.is_declarer"
            },
            "key": "score",
            "value": {
              "calc": "declarer_win_multiplier * stake_v"
            },
            "if": {
              "calc": "declarer_points >= contract"
            },
            "text": "Seat {player}, the declarer, made the contract and gains twice V."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.is_declarer"
            },
            "key": "score",
            "value": {
              "calc": "-defender_win_multiplier * stake_v"
            },
            "if": {
              "calc": "declarer_points >= contract"
            },
            "text": "Seat {player}, a defender, loses V."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.is_declarer"
            },
            "key": "score",
            "value": {
              "calc": "-declarer_win_multiplier * stake_v"
            },
            "if": {
              "calc": "declarer_points < contract"
            },
            "text": "Seat {player}, the declarer, failed the contract and loses twice V."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.is_declarer"
            },
            "key": "score",
            "value": {
              "calc": "defender_win_multiplier * stake_v"
            },
            "if": {
              "calc": "declarer_points < contract"
            },
            "text": "Seat {player}, a defender, gains V."
          }
        }
      ],
      "text": "Deal {deal_number} is over: the declarer took {declarer_points} card points against a contract of {contract}; V = {stake_v}. Match scores are updated."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after round 40",
      "when": {
        "calc": "round_number >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number >= total_rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final match scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "DECK: {deck_size} cards in {suits} suits (Hearts, Bells, Leaves, Acorns). Each suit has A, 10, K, O (Ober), U (Unter) and 9, ranking high to low A, 10, K, O, U, 9. Card points: each Ace {ace_points}, each Ten {ten_points}, all other cards {other_card_points}. The side that wins the last (7th) trick of a deal also gets {last_trick_bonus}. At most {max_card_points} card points are available in a deal; fewer if Aces or Tens lie in the talon.\n\nSEATS AND MATCH: Seats 1, 2 and 3. Seat order runs 1, 2, 3, 1 and so on. The match has {deals} deals of {rounds_per_deal} rounds each, {total_rounds} rounds in total. The eldest is Seat 1 in deal 1, Seat 2 in deal 2, Seat 3 in deal 3, Seat 1 in deal 4 and Seat 2 in deal 5. Match scores start at {starting_score} and are public. There is no talk at any time. Hands are shown to their owner sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low.\n\nROUND 1 OF EACH DEAL (DEAL AND BID):\n(a) Shuffle all {deck_size} cards. Deal {hand_size} cards privately to each seat. The remaining {talon_size} cards are the talon. The talon is face down, is never played and is never shown to anyone, including at the end of the deal. Each player sees only their own hand.\n(b) All three players bid at the same time without seeing the other bids. The options are PASS, {bid_low}, {bid_mid} or {bid_high}.\n(c) If all three pass, the deal is not played. Rounds 2-8 of this deal are skipped with no plays and no scoring.\n(d) Otherwise the highest bid wins and that player is the declarer. If several players tie for the highest bid, it goes to the tied player with the lowest match score. If they are still tied, it goes to the tied player who comes first in seat order starting from the eldest.\n(e) The declarer chooses trump: Hearts, Bells, Leaves or Acorns.\n(f) The declarer, the contract (the winning bid) and trump are announced. The other two players are the defenders, and their card points this deal are pooled together.\n(g) Flek: the two defenders each choose FLEK or NO at the same time. Both choices are announced. If at least one chooses FLEK the stake is doubled; if both choose NO it is not.\n(h) Stake V: start at {stake_for_40} for a 40 contract, {stake_for_50} for 50 and {stake_for_60} for 60. Multiply V by {hearts_trump_multiplier} if trump is Hearts. Multiply V by {flek_multiplier} again if at least one defender chose FLEK. V is announced.\n\nROUNDS 2-8 OF EACH DEAL (ONE TRICK PER ROUND, {tricks_per_deal} tricks):\n(a) The declarer leads in round 2. In later rounds, the winner of the previous trick leads. The leader plays any card from their hand face up. Then the next player in seat order plays, then the third. Each card is shown to everyone as it is played.\n(b) LEGAL CARDS. The 'currently winning card' is the card that would win the trick right now under rule (c). The following rules apply to every player, whoever is currently winning.\n  1. If you hold a card of the suit led, you must play a card of that suit. If the currently winning card is of the suit led, you must play a higher card of that suit if you have one. This includes the case where trump was led. If the currently winning card is a trump and the suit led is not trump, any card of the suit led is legal.\n  2. If you hold no card of the suit led but hold a trump, you must play a trump. If a trump has already been played in this trick, you must play a higher trump than the highest one played if you have one; otherwise any trump.\n  3. If you hold neither the suit led nor a trump, you may play any card.\nYou are only ever offered the cards these rules allow.\n(c) The trick is won by the highest trump in it. If it contains no trump, it is won by the highest card of the suit led.\n(d) The trick's card points go to the declarer if the declarer won it, or to the defenders' pooled total if either defender won it. In round 8 the last-trick {last_trick_bonus} also goes to the side that won the trick. Running totals are announced.\n(e) The trick winner leads the next round.\n\nSCORING AT THE END OF ROUND 8 (only if the deal was played): the contract is made if the declarer's card points are at least the contract (40, 50 or 60).\n- Made: the declarer gains {declarer_win_multiplier}V and each defender loses V.\n- Failed: the declarer loses {declarer_win_multiplier}V and each defender gains V.\nMatch scores are announced.\n\nEND: the game ends after round {total_rounds}. The player with the highest match score wins. If two or three players tie for the highest score, they share the win (a draw among them)."
}
````
