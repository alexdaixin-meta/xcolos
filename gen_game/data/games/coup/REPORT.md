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
- attributes: designed 18, built 51, limit 20
- hidden_elements: designed 2, built 14, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every seat holds 2 hidden cards and the deck holds 15 - 2x3 = 9 (checked after one Income, which moves no card)
- pass: Setup with 5 players: deck holds 5 (checked after one Income)
- pass: Setup: seat 1 starts with 1 coin (2 after one Income), the other seats with 2
- pass: Income gives exactly 1 coin and nobody can challenge or block it
- pass: Foreign Aid nobody blocks gives 2 coins
- pass: Foreign Aid blocked as Duke, nobody challenges: no coins
- pass: Foreign Aid cannot be challenged
- pass: Coup costs 7, target loses one card, no challenge or block
- pass: With 6 coins Coup is not offered
- pass: At 10 coins Coup is the only option
- pass: Tax nobody challenges gives 3 coins
- pass: Assassinate pays 3 even when it fails a challenge
- pass: Assassinate pays 3 even when blocked
- pass: With 2 coins Assassinate is not offered
- pass: Unblocked Assassinate: target loses one card
- pass: Contessa block unchallenged: target keeps cards, no refund
- pass: Steal from a target with 4 coins moves 2
- pass: Steal from a target with 1 coin moves 1
- pass: Steal from a target with 0 coins moves nothing
- pass: Steal blocked as Captain, unchallenged: no coins move
- pass: Steal blocked as Ambassador, unchallenged: no coins move
- pass: Only the Steal target is offered the Captain/Ambassador blocks
- pass: Only the Assassinate target is offered the Contessa block
- pass: Exchange keeps hidden_count and deck size
- pass: Exchange return is not revealed
- pass: Challenged true Tax: challenger loses a card, Tax still pays
- pass: Challenged bluff Tax: bluffer loses a card, no coins
- pass: Challenged bluff Steal: no coins move and the block is ignored
- pass: Two challengers of a true Tax: only the first after the active seat loses
- pass: Two Duke blockers: only the first counts (its true Duke beats the block challenge)
- pass: Challenged true Captain block: block challenger loses, Steal blocked
- pass: Challenged false Duke block: blocker loses, Foreign Aid pays
- pass: False Contessa block challenged: target takes 2 losses and is eliminated
- pass: One loss from two cards: the player reveals the card they choose
- pass: Loss on the last card: all revealed, out, coins 0
- pass: A revealed card stays revealed on the next turn
- pass: A loss does not carry into the next turn
- pass: Next turn skips an eliminated seat
- pass: Coup target must be a living other seat; the chosen seat takes the hit
- pass: Last opponent loses their last card: seat 1 wins
- pass: Turn 40 ends the game: most hidden cards wins
- pass: Reactions are polled: both challengers are offered challenge, first one loses
- pass: Steal target choice offers only other living seats
- pass: Exchange reactions: only pass and challenge, no blocks
- pass: Tax reactions: no blocks offered
- pass: Foreign Aid reactions: pass and block_duke only
- pass: Assassinate reactions: target may block as Contessa, others only pass/challenge
- pass: Steal reactions: target may block as Captain/Ambassador, others only pass/challenge
- pass: Exchange with 4 players: deck stays at 15 - 8 = 7 and hand stays at 2
- pass: Eliminated seat: alive false, no cards, no coins, and skipped and never polled next turn
- pass: 4 players, seats 3 and 4 already out: seat 2 coups seat 1's last card and wins
- pass: Turn 40, two seats tie on hidden cards: the one with more coins wins
- pass: Turn 40, tied on hidden cards and coins: draw
- pass: Challenged true Steal: claimant keeps 2 hidden cards and the deck keeps 9 (the drawn card is chance, not asserted)
- pass: Challenged true Contessa block: blocker keeps 2 hidden cards, deck keeps 9, block challenger loses (drawn card is chance)
- pass: Three seats challenge a true Duke block: only the first after the blocker loses
- pass: Challenged true Exchange: proven card goes back, Exchange still runs, counts unchanged (which cards are drawn is chance)
- pass: Target challenges a true Assassinate: loses one card to the challenge and one to the action, so is eliminated

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `sync` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 1': 7, 'seat 3': 13, 'seat 2': 10, 'seat 4': 5, 'seat 5': 5}, 17-66 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 46.2 decisions, prompts of 513 characters on average (longest 627)

## Reasoning and balance (not checked here: real models will play it later)

- not run

## Triage (whose problem each failure was)

- round 1: fix_game: The game already allows Coup at 7 or more coins and Assassinate at 3 or more. The only problem is that the rules text in `meta.rules` copies the phrase 'only if you have 7' (and 'only if you have 3'), which a player can read as 'exactly'. The coder can fix this by editing `meta.rules`; the logic and the design don't need to change.

## Choices the rules did not make

- 3 to 5 players: Bluffing needs at least 3 players: a claim faces more than one possible challenger, and Foreign Aid can be blocked by a third party. With 2, every claim is a one-on-one guess. 5 is the maximum because a 15-card deck dealt 2 each leaves 5 cards for draws and exchanges; with more players the deck thins out and the counting gets too long to follow. This matches the source.
- The strategy is what makes it a game: A thoughtful player tracks the revealed cards and past claims to judge whether a claim is likely true (3 copies per role), bluffs roles that are still plausible, saves the forced Coup for the strongest rival, and challenges only when being wrong costs less than letting the action through.
- No talk step: The source says there is no free discussion. Claims, challenges and blocks are the only communication.
- Action choice by ask, reactions and block responses by poll: The active player acts alone. The source says reactions and block responses are made at the same moment without seeing each other, so they use poll.
- Card choice by poll: The source says reveal and return choices are made at the same moment.
- Each player is offered only the reactions they may legally make: The source limits Challenge to claimed roles, Duke blocks to Foreign Aid, and Contessa, Captain and Ambassador blocks to the target. Offering only legal options enforces this.
- A turn is one round: Seat order with skipping is kept by active_seat, so the turn cap of 40 counts directly as turn_count.
- A player who both loses a card and owes an Exchange return answers both in the card-choice poll: The source does not say how the two choices combine. In practice this is rare, because the active player in an Exchange only takes a pending loss when the Exchange failed.
- A card put into the deck goes to the bottom of the deck until the end-of-turn shuffle: The design says the revealed or returned card is 'put into the deck' and that the deck is shuffled at the end of the turn, but not where it goes in between. Without a position, a same-turn Exchange could draw straight back the card just proven, which makes the replacement meaningless. A play review found the gap (round 4).

## Simplifications

- 'Top card of the deck' is a random draw from the deck list, and 'shuffle the deck' is dropped: The deck is hidden and drawing is random, so every draw is the same as taking the top of a freshly shuffled deck. The source's reshuffle is already implied.
- The many branches of a turn (challenge, block, block challenge, effect) are written as flat steps, each with an arithmetic `when` condition on action_status, challenger and blocker: The engine has no block-of-steps branching, but each branch here is a single update or poll, so per-step conditions express the rules exactly.
- The 40-turn tiebreak (most hidden cards, then most coins, then draw) is computed from hidden_count and coins with arithmetic: The engine's arithmetic ranking is a workaround that needs calc. The outcome stays decided by counting, as the source requires.
- Card-choice options come from the player's own hidden_cards list: Taking options from a list is the engine's workaround for choosing from a hand.

## Encoding attempts

- 1: passed
