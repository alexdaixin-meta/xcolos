# Variation: Hanabi Duo

A two-player, 12-card Hanabi. Partners see each other's two cards but not their own. They spend scarce hints, discard to regain them, and try to build Red and Blue piles from 1 to 3. The team wins together if its score reaches 4.

Players: 2 to 2, best with 2

## Review of the original

Hanabi is a cooperative card game for 2 to 5 players. Each player holds cards facing outward, so they see everyone's hand except their own. Players spend scarce hint tokens to tell partners about colours or ranks, discard to win tokens back, and try to build five colour piles in order from 1 to 5 before three misplays (fuses) end the game.

- **non_degenerate**: weak. The original has no seat edge because it is fully cooperative, and choices matter a great deal. As tested, though, the previous variation failed this criterion. All 60 random matches ended 'no seat wins', so the result did not respond to what the seats chose. Simple policies such as always hint or always discard score 0. The target and the fuse count were set so that only near-perfect play could ever reach the win line.
- **skill_sensitive**: good. Good Hanabi play reliably beats careless play. Players have to choose which hint to give, read why a partner gave a hint, count cards to deduce their own hand, and judge when a blind play or a discard is worth the risk. The shuffle adds variance, but over many games skill dominates.
- **headroom**: weak. The full game has huge headroom, since perfect scores are rare even for experts. In the tested variation, however, weak and random seats never won at all, so there was no gradient between weak and medium play. A model could not learn from a winless signal.
- **reasoning_dependent**: good. The core is hidden information. You cannot see your own cards, so you must infer them from hints, from the cards you can see, from the discard pile and from what a partner meant by choosing a particular hint. This is theory of mind and planning several turns ahead.
- **verifiable**: good. Whether a play is legal (next rank of its colour), the fuse count and the score (sum of pile tops) are all plain arithmetic. No judge is needed.
- **fits_platform**: bad. The game is turn-based, text-only and has no board. But the full game (50 cards, 5 piles, 2-5 hands of 4-5 cards, per-card hint knowledge) needs far more state than allowed. The previous build had 64 attributes against a limit of 20, because it carried parameters for every player count, derived constants, and bookkeeping such as final-turn counters and an action log.

## Problems

- P1: The tested variation's win line was unreachable for anything but near-perfect play. Every random match ended 'no seat wins', so choices did not visibly change the outcome and weak play got no signal.
- P2: The previous build used 64 attributes, more than three times the limit of 20. The causes were player-count parameters, derived or constant parameters, and extra bookkeeping (final-turn counter, action log, separate hint-gain values, a refund rule for completed piles).
- P3: The full deck and hand structure (5 colours, ranks 1-5, 4-5 card hands, 2-5 players) carries far more hidden state than the platform's limits allow.
- P4: Losing the last fuse wipes out the game completely, and drawing replacements per turn would be a random draw every turn. Together these make results swing on luck and burn the per-round random-draw budget.
- P5: The original's ending (each player gets one extra turn after the deck runs out) needs extra counters and conditional sequencing that the flat step list handles poorly.
- P6: There was no clear account of what a hint records on a card, so hint knowledge had no compact representation.

## Changes

- Fix the game at exactly 2 players, who alternate turns: player 1 then player 2 each round. (fixes: P2: The previous build used 64 attributes, more than three times the limit of 20.): This removes every player-count parameter (hand sizes, per-count settings) and halves the per-player state.
- Use a 12-card deck: 2 colours (Red, Blue), each with three 1s, two 2s and one 3. Hand size is 2. Maximum score is 6. (fixes: P3: The full deck and hand structure carries far more hidden state than the platform's limits allow.): This keeps Hanabi's shape (many 1s, scarce middle ranks, a single precious top card) at a size the engine can hold. Each card is stored as one number: 11/12/13 for Red, 21/22/23 for Blue, 0 for an empty slot.
- Store state in 18 attributes and nothing else. Per player (×2): card A, card B, note A, note B, score. Shared: deck list, discard list, Red pile, Blue pile, hint tokens, fuses, last-action text, round counter. (fixes: P2: The previous build used 64 attributes, more than three times the limit of 20.): This drops derived constants (deck size, zero starts), the final-turn counter, the action log, separate hint-gain values and the pile-completion refund. The last-action text replaces the log.
- Shuffle the deck once at setup. Replacements are always taken from the front of the shuffled list. (fixes: P4: Drawing replacements per turn would burn the per-round random-draw budget.): Drawing becomes a deterministic remove-first operation, so no random draw is used during rounds, yet players still cannot predict the next card.
- Losing the last of 3 fuses ends the game immediately, but the team keeps the score it has built. The target is 4 of the maximum 6. (fixes: P1: The tested variation's win line was unreachable for anything but near-perfect play.): This makes the win line reachable through partial success. Rough estimates put random seats at about 1 win in 10 and good partners at most games. A score of 6 remains a stretch goal. A last fuse also becomes a real decision: a gamble that ends the game is only worth it if the score already wins.
- Same change as above, viewed as a fix for luck: losing the last fuse no longer zeroes the result. (fixes: P4: Losing the last fuse wipes out the game completely, which makes results swing on luck.): With the score kept, one unlucky misplay late in a good game no longer erases everything, so the outcome tracks the quality of play more than a single bad moment.
- The game lasts at most 12 rounds (24 turns). It ends early only if the last fuse is lost or both piles reach 3. When the deck is empty, slots simply stay empty. There are no extra final turns. (fixes: P5: The original's ending needs extra counters and conditional sequencing that the flat step list handles poorly.): A fixed round limit replaces the 'one more turn each' ending with no extra counter. Twenty-four turns is enough to cycle all 12 cards with hints in between.
- Each turn is a single choice from 8 options: Play A, Play B, Discard A, Discard B, Hint colour of partner's A, Hint rank of partner's A, Hint colour of partner's B, Hint rank of partner's B. A hint writes 'is X' or 'not X' into the note of each of the partner's cards. A note is cleared when its card leaves the hand. (fixes: P6: There was no clear account of what a hint records on a card, so hint knowledge had no compact representation.): This gives a compact, exact record of hint knowledge that both players can see. It keeps colour and rank hints and the 'all matching cards' rule, and it fits in one choice step per player.
- Start with 3 hint tokens (maximum 3). A hint costs 1 token. A discard regains 1 token, up to the maximum. A hint chosen with 0 tokens, or aimed at an empty slot, is a wasted turn. (fixes: P2: The previous build used 64 attributes, more than three times the limit of 20.): Scaling the token economy to the small deck keeps the central tension between hinting and discarding without extra parameters.

## Kept from the original

- Cooperative play: both seats win together or lose together.
- You see your partner's cards but never your own.
- Hints cost scarce tokens, name one colour or one rank, and must mark all matching cards, including which cards do not match.
- Discarding is the only way to regain hint tokens, and it can throw away a card the team needed.
- Piles must be built in rank order per colour. A wrong play burns a fuse.
- Score is the sum of the pile tops.
- A single precious top card per colour.
- Card counting from the visible cards, the piles and the discard pile.

## The variation's rules

CARDS. The deck has 12 cards in 2 colours, Red and Blue. Each colour has three 1s, two 2s and one 3. (Engine codes: Red 1/2/3 = 11/12/13, Blue 1/2/3 = 21/22/23, empty slot = 0. Colour is code divided by 10 rounded down; rank is code mod 10.)

SETUP. Shuffle the deck once. Deal 2 cards to each player into slots A and B, taking them from the front of the deck: player 1 gets A then B, then player 2 gets A then B. The 8 remaining cards stay in order face down. Set the Red pile and the Blue pile to 0. Set hint tokens to 3 (the maximum is 3) and fuses to 3. The discard pile starts empty. Every card note starts blank. Both players' scores start at 0.

WHAT EACH PLAYER SEES. On your turn you are shown:
- your partner's two cards;
- the notes on all four cards (yours and your partner's);
- both pile values, the hint tokens and the fuses;
- the full discard pile and the number of cards left in the deck;
- your partner's last action and its result.
You are never shown your own cards. There is no other communication: no messages, only the actions below.

ROUND. Each round player 1 takes a turn, then player 2 takes a turn. There are at most 12 rounds.

TURN. The active player chooses exactly one of these 8 options:
- Play A or Play B: reveal your card in that slot. If its rank is exactly 1 more than its colour's pile, that pile goes up by 1. Otherwise the play fails: the card goes to the discard pile and fuses go down by 1. If the slot is empty, nothing happens.
- Discard A or Discard B: put your card in that slot on the discard pile and gain 1 hint token, up to the maximum of 3. If the slot is empty, nothing happens.
- Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, or Hint rank of partner's B: if you have at least 1 hint token and the named partner slot holds a card, spend 1 token. Then name that card's colour (or rank) to your partner. Each of the partner's non-empty cards gets a note added: 'is Red' (or 'is 2', and so on) if it matches, or 'not Red' (or 'not 2') if it does not. If you have no token or the named slot is empty, nothing happens and the turn is wasted.

DRAWING. After a card leaves a slot (played, successfully or not, or discarded), the player takes the front card of the deck into that slot, and that slot's note is cleared. If the deck is empty, the slot stays empty and its note stays blank.

ANNOUNCEMENT. After every turn, the action and its result are shown to both players: which option was chosen, any card revealed, whether a play succeeded, and the hint named.

SCORE. After every turn, both players' scores are set to the Red pile plus the Blue pile. The two scores are always equal.

END. The game ends immediately when either of these happens after a turn:
- fuses reach 0;
- both piles reach 3.
Otherwise it ends after round 12. In every case the team keeps its current score.

Objective: Cooperative. When the game ends, if the team score (Red pile + Blue pile, shown identically as each player's score) is 4 or more, both seats win. Otherwise no seat wins. This holds whether the game ended on fuses, on a full score of 6, or after round 12.

Expected effect: Thoughtless policies can now sometimes win but usually lose, which gives a gradient that responds to play. Rough estimates:
- Always hint, always discard: score 0, always lose.
- Always Play A: blind plays succeed roughly 40% of the time, and three misses end the game, so this wins only occasionally (an estimated one game in five).
- Uniform random play: discards destroy needed cards and most hints are wasted, so this wins roughly one game in ten.
- Good partners: should win most games and sometimes reach 6.
Good partners spend hints on currently playable cards and read a hint as a signal of playability, not just as a fact. They count copies through the discard pile to protect the single 3s and the last 2s. They also judge when a blind play is worth a fuse, including recognising that the last fuse can be risked once the score already reaches 4. Talk is deliberately absent: with two cooperating players there is no conflict to bargain over, and free messages would leak the hidden hands and remove the inference the game is built on.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
