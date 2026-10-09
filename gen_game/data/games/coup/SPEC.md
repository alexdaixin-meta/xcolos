# Coup (XColos)

Each player holds two hidden role cards. On your turn you take an action, and some actions require claiming a role you may not hold. Other players can challenge or block. Lose both cards and you are out; the last player holding a hidden card wins.

Players: 3 to 5

## Parameters

- `deck_size` = 15
- `copies_per_role` = 3
- `hand_size` = 2
- `first_player_start_coins` = 1
- `other_player_start_coins` = 2
- `forced_coup_threshold` = 10
- `income_gain` = 1
- `foreign_aid_gain` = 2
- `coup_cost` = 7
- `tax_gain` = 3
- `assassinate_cost` = 3
- `steal_amount` = 2
- `exchange_draw` = 1
- `exchange_return` = 1
- `loss_per_hit` = 1
- `turn_cap` = 40

## Round

1. **update** (engine): Start of turn: action_status = going; challenger = blocker = block_challenger = target = stolen = 0; action, claimed_role, block_role and every player's reaction, block_response, reveal_choice and return_choice are cleared; turn_count += 1.
2. **tell** (all players): Announce each player's coins, revealed_cards and hidden_count, plus deck_count and active_seat.
3. **sync** (all players): Send each player their own hidden_cards.
4. **ask** (the player at active_seat): action = the answer; claimed_role = Duke for tax, Assassin for assassinate, Captain for steal, Ambassador for exchange, empty otherwise.
5. **ask** (the player at active_seat, when action is coup, assassinate or steal): target = the chosen seat.
6. **update** (engine): Pay costs now, with no refund later: if action = coup, active coins -= 7; if action = assassinate, active coins -= 3.
7. **tell** (all players): Announce the active seat's action, claimed_role and target.
8. **poll** (every living player except the active player, when action is foreign_aid, tax, assassinate, steal or exchange): Each answering player's reaction = the answer.
9. **tell** (all players): Announce every player's reaction.
10. **update** (engine): challenger = the first seat in seat order after active_seat with reaction = challenge, 0 if none. blocker = the first seat after active_seat whose reaction starts with block_, 0 if none. block_role = that block's role.
11. **update** (engine, when challenger > 0): Action challenge. If claimed_role is in the active player's hidden_cards: remove one claimed_role card from the active player's hidden_cards and append it to deck, then draw one card at random from deck into the active player's hidden_cards; challenger's pending_loss += 1. Otherwise: active player's pending_loss += 1, action_status = failed, blocker = 0.
12. **tell** (all players, when challenger > 0): Announce whether the challenged claim was true and who takes the pending loss. The card the active player draws is not named.
13. **poll** (every living player except the blocker, when action_status = going and blocker > 0): Each answering player's block_response = the answer.
14. **tell** (all players, when action_status = going and blocker > 0): Announce every player's block_response.
15. **update** (engine, when action_status = going and blocker > 0): block_challenger = the first seat in seat order after blocker with block_response = challenge, 0 if none. If block_challenger = 0: action_status = blocked. Otherwise, if block_role is in the blocker's hidden_cards: move that card from the blocker's hidden_cards to deck, draw one card at random from deck into the blocker's hidden_cards, block_challenger's pending_loss += 1, action_status = blocked. Otherwise: blocker's pending_loss += 1 and the action goes ahead (action_status stays going).
16. **update** (engine, when action_status = going): Effect. income: active coins += 1. foreign_aid: active coins += 2. tax: active coins += 3. steal: stolen = the smaller of 2 and the target's coins, target coins -= stolen, active coins += stolen. coup or assassinate: target pending_loss += 1. exchange: draw one card at random from deck into the active player's hidden_cards and set the active player's must_return = 1.
17. **poll** (every player with (pending_loss = 1 and hidden_count = 2) or must_return = 1): reveal_choice = the card to reveal; return_choice = the card to return to the deck.
18. **update** (engine): Resolve. A player with pending_loss = 1 and hidden_count = 2 moves reveal_choice from hidden_cards to revealed_cards. A player with must_return = 1 moves return_choice from hidden_cards to deck. Any player with pending_loss >= hidden_count and pending_loss > 0 moves all of hidden_cards to revealed_cards, alive = false, coins = 0. Then hidden_count = length of hidden_cards for every player, deck_count = length of deck, living_count = number of players with alive = true. Every pending_loss and must_return goes back to 0.
19. **tell** (all players): Announce every card revealed this turn and every player eliminated. Returned cards are never named.
20. **check** (engine): End the game if living_count = 1 or turn_count >= 40, otherwise continue.
21. **update** (engine): active_seat = the next seat after active_seat in seat order, wrapping around and skipping players with alive = false.

## Ending

- ends when: living_count = 1 or turn_count >= 40
- results: seat 1, seat 2, seat 3, seat 4, seat 5, draw
- decided by: If living_count = 1, the result is the seat with hidden_count >= 1. Otherwise, after 40 turns, the result is the seat with the highest hidden_count; if several tie, the tied seat with the most coins; if they are still tied, draw.

## Choices the source did not make

- 3 to 5 players: Bluffing needs at least 3 players: a claim faces more than one possible challenger, and Foreign Aid can be blocked by a third party. With 2, every claim is a one-on-one guess. 5 is the maximum because a 15-card deck dealt 2 each leaves 5 cards for draws and exchanges; with more players the deck thins out and the counting gets too long to follow. This matches the source.
- The strategy is what makes it a game: A thoughtful player tracks the revealed cards and past claims to judge whether a claim is likely true (3 copies per role), bluffs roles that are still plausible, saves the forced Coup for the strongest rival, and challenges only when being wrong costs less than letting the action through.
- No talk step: The source says there is no free discussion. Claims, challenges and blocks are the only communication.
- Action choice by ask, reactions and block responses by poll: The active player acts alone. The source says reactions and block responses are made at the same moment without seeing each other, so they use poll.
- Card choice by poll: The source says reveal and return choices are made at the same moment.
- Each player is offered only the reactions they may legally make: The source limits Challenge to claimed roles, Duke blocks to Foreign Aid, and Contessa, Captain and Ambassador blocks to the target. Offering only legal options enforces this.
- A turn is one round: Seat order with skipping is kept by active_seat, so the turn cap of 40 counts directly as turn_count.
- A player who both loses a card and owes an Exchange return answers both in the card-choice poll: The source does not say how the two choices combine. In practice this is rare, because the active player in an Exchange only takes a pending loss when the Exchange failed.

## Simplifications

- 'Top card of the deck' is a random draw from the deck list, and 'shuffle the deck' is dropped: The deck is hidden and drawing is random, so every draw is the same as taking the top of a freshly shuffled deck. The source's reshuffle is already implied.
- The many branches of a turn (challenge, block, block challenge, effect) are written as flat steps, each with an arithmetic `when` condition on action_status, challenger and blocker: The engine has no block-of-steps branching, but each branch here is a single update or poll, so per-step conditions express the rules exactly.
- The 40-turn tiebreak (most hidden cards, then most coins, then draw) is computed from hidden_count and coins with arithmetic: The engine's arithmetic ranking is a workaround that needs calc. The outcome stays decided by counting, as the source requires.
- Card-choice options come from the player's own hidden_cards list: Taking options from a list is the engine's workaround for choosing from a hand.

## Unsupported (needs engine work)

- none
