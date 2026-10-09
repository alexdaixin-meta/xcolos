# coup: needs review

Built from the variation **Coup (XColos)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Each reaction window is a single simultaneous poll. After an action, every other living player answers Pass, Challenge or Block (with the blocking role) at the same time. After a block, every living player except the blocker answers Accept or Challenge at the same time. (fixes: Challenges and blocks are free-for-all interrupts decided by who speaks first, which a turn-based engine cannot express.): Turns the speak-first interrupt into a turn-based step while keeping the rule that anyone may challenge and the right players may block.
- Priority rules. A challenge to the action is resolved before any block. If several players challenge, only the first in seat order after the active player counts. If several players block, only the first in seat order counts. (fixes: When several players want to challenge or block the same action, the original does not say who goes first.): Gives every collision a single arithmetic answer.
- A player who proves a challenged role first takes the top card of the deck as a replacement, then puts the revealed card into the deck. Returned cards stay where they are until the end of the turn, when the deck is shuffled once if any card went back. The game is dealt from one shuffle at the start. (fixes: Shuffling a proven card back and drawing a replacement, plus the Ambassador's draws, can put several random events into one turn, and the limit is one.): Keeps the original's reveal-and-replace (a proven role is not left exposed) using at most one random event per turn. The engine's limit of one random draw per round forces this reordering.
- Ambassador Exchange becomes: draw 1 card from the deck, then return any 1 of your hidden cards. The return is chosen in the same simultaneous card-choice step where other players pick which card to reveal. (fixes: The Ambassador's draw 2, return 2 out of 4 adds a large extra decision and drawing, pushing a turn past the choice-step budget.): Keeps the Ambassador's purpose (secretly changing your hand, which supports later bluffs and makes old claims unreliable) inside the platform's limit of 4 choice steps. Draw 2, return 2 would need its own decision step.
- Safety cap of 40 turns (one turn is one player's action). If the cap is reached, the player with the most hidden cards wins, ties are broken by most coins, and a remaining tie is a draw. (fixes: Nothing bounds the game's length: passive Income play or mutual caution can drag on indefinitely.): Guarantees the match stops. The tiebreak rewards what the game rewards (staying alive and gaining coins), so stalling is not a safe way to win.
- The first player starts with 1 coin, and everyone else starts with 2. (fixes: The first player gets a tempo edge in small games, and the original corrects this only in the 2-player variant.): Offsets the extra tempo of acting first, as the original's own 2-player rule does.
- Losses are counted as pending during the turn and resolved together at its end. A player with exactly 1 pending loss and 2 hidden cards chooses which card to reveal. A player whose pending losses are at least their hidden cards reveals them all and is eliminated. (fixes: Losing influence can happen to several players in one turn (challenger, claimant, blocker, target), and one player can lose two cards in a turn. Each of these needs a defined resolution.): Resolves the original's double loss (for example a failed challenge against an Assassin followed by the assassination) and simultaneous losses by several players in one step, without stopping play for each.
- The table is 3 to 5 players, using a 15-card deck. (fixes: Nothing bounds the game's length: passive Income play or mutual caution can drag on indefinitely.): Three is the smallest table where the core questions actually arise: who challenges when it is not your coins at stake, whom to target, and the threat of a third player profiting from a fight. Five keeps games within the cap and leaves at least 5 cards in the deck.

Objective: The last player with at least one hidden card wins. If 40 turns pass first, the player with the most hidden cards wins, ties are broken by most coins, and any remaining tie is a draw. Everything is decided by counting cards and coins.

## Complexity

- steps_per_round: designed 15, built 20, limit 20
- choice_steps_per_round: designed 4, built 5, limit 4
- attributes: designed 18, built 57, limit 20
- hidden_elements: designed 2, built 11, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every seat holds 2 hidden cards, nothing revealed, all alive (3 players)
- pass: Setup: every seat holds 2 hidden cards, nothing revealed, all alive (5 players)
- pass: Setup: seat 1 starts with 1 coin, the others with 2 (seat 1 then takes Income)
- pass: Income gives exactly 1 coin and nobody loses a card
- pass: Foreign Aid with nobody blocking gives 2 coins
- pass: Foreign Aid blocked as Duke, block accepted: no coins gained
- pass: Foreign Aid cannot be challenged: would-be challengers pass and the aid goes through
- pass: Coup costs 7 and the target loses one card
- pass: With 6 coins Coup is not offered, so the seat falls back to Tax
- pass: With 10 coins Coup is forced even when the seat asks for Income
- pass: Tax with nobody challenging gives 3 coins
- pass: Assassinate's 3 coins are paid even when a challenge makes it fail
- pass: With 2 coins Assassinate is not offered, so the seat falls back to Tax
- pass: Unblocked Assassinate costs 3 and the target loses one card
- pass: Contessa block accepted: target keeps both cards, assassin gets no refund
- pass: Steal from a target with 4 coins moves 2
- pass: Steal from a target with 1 coin moves only 1
- pass: Steal from a target with 0 coins moves nothing
- pass: Steal blocked as Captain, block accepted: no coins move
- pass: Steal blocked as Ambassador, block accepted: no coins move
- pass: A non-target cannot block a Steal: seat 3's block is not offered and the steal goes through
- pass: A non-target cannot block Assassinate as Contessa: the target still loses a card
- pass: Exchange draws 1 and returns 1: still 2 hidden cards, nothing revealed (which card comes back depends on chance)
- pass: The card an Exchange returns is not revealed
- pass: Tax challenged, Duke is held: challenger loses a card, tax still pays 3
- pass: Tax challenged, bluff (no Duke): bluffer loses a card and gains nothing
- pass: Bluffed Steal is challenged: the target's block is ignored, no coins move, only the bluffer loses a card
- pass: Several challenge a true Tax claim: only the first seat after the active seat (wrapping) loses a card
- pass: Two Duke blocks: only seat 2's counts; it is a bluff, so seat 2 loses a card and the aid goes through
- pass: Captain block challenged and the blocker holds Captain: challenger loses a card, steal blocked
- pass: Captain block challenged and it is a bluff: blocker loses a card and the steal moves 2
- pass: A bluffed Contessa block is challenged: the target loses 2 and is out
- pass: Losing one of two cards: the player reveals the card they choose (the second one)
- pass: Coup on a player with one card left: they are out with 0 coins
- pass: A revealed card stays revealed and does not come back through an Exchange
- pass: A loss does not carry into the next turn: the target loses 1 to Coup, then takes Income and keeps 1 card
- pass: The next turn skips an eliminated seat: after seat 1, seat 3 plays (seat 2 is out)
- pass: A Coup target must be another living player: self and the eliminated seat are not offered, so seat 3 is hit
- pass: Last player with hidden cards wins: seat 1 Coups the last rival
- pass: Turn cap: after turn 40 the seat with the most hidden cards wins
- pass: Turn cap: tied on hidden cards, the tied seat with more coins wins
- pass: Turn cap: tied on hidden cards and coins is a draw
- pass: Reactions are a poll: both seats challenge a bluffed Tax, only the bluffer loses a card

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `tell` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 3': 11, 'seat 2': 9, 'seat 1': 12, 'seat 4': 3, 'seat 5': 5}, 31-171 turns

## Reasoning and balance (not checked here: real models will play it later)

- not run

## Triage (whose problem each failure was)

- round 1: fix_game: The tests are correct, but the game file does not use the interface names. It writes `hand_count` and `revealed` where the interface requires `hidden_count` and `revealed_cards`, so the tests read None. It also gives seat 1 the same 2 starting coins as everyone else, so Income takes seat 1 to 3 coins instead of 2.

## Choices the rules did not make

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

## Encoding attempts

- 1: passed
