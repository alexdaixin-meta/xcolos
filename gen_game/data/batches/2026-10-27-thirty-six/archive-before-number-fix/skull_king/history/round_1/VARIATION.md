# Variation: Skull King: Three-Card Raids

3 to 5 players, 8 rounds. Each round everyone is dealt 3 cards from an 18-card deck, bids at the same time how many of the 3 tricks they will win, then plays 3 tricks with everyone playing at the same time. Exact bids score, misses cost, and the highest total wins.

Players: 3 to 5, best with 4

## Review of the original

Skull King is a trick-taking game for 2 to 8 players played over 10 hands of growing size. Each hand, players bid at the same time how many tricks they will win, then play tricks with follow-suit rules, a black trump suit and special cards (Pirates, Mermaids, Skull King, Escapes). Exact bids score well, missed bids lose points, and the highest total wins.

- **non_degenerate**: good. No simple policy wins. Always bidding 0 fails whenever forced high cards win tricks, and the failed zero bid costs a lot. Always bidding high misses most hands. Seat order matters a little, because the lead player and the last player have different information, but the lead rotates.
- **skill_sensitive**: weak. Exact bidding rewards reading your hand and anticipating others. But with hands of 1 to 10 cards, a 70-card deck and big special-card bonuses (+50 for a Mermaid capturing the Skull King), the deal swings single hands heavily. Skill shows over many games more than within one.
- **headroom**: good. Calibrating bids, dumping cards to hit a bid, timing specials and forcing opponents to miss give deep play. A novice still scores by bidding plainly.
- **reasoning_dependent**: good. Hands are hidden, and the bids made at the same moment reveal partial information. Players must infer who holds the specials and plan card use across the tricks of a hand.
- **verifiable**: good. Trick winners and scores follow from fixed rules and arithmetic.
- **fits_platform**: bad. Ten hands of up to 10 sequential tricks with follow-suit checks need far more than 4 choice steps and 20 steps per round. The 70-card deck with suits and lead rules makes a very large state. Rounds grow to 10 tricks each.

## Problems

- Too long and too many choices per round: a hand of i cards needs i sequential trick turns per player, far over 4 choice steps and 20 steps per round.
- Follow-suit, lead-suit and trump rules plus the Scary Mary declaration create long rule chains that are hard to build and check.
- Large deck and growing hand sizes give a big hidden state, and hand-to-hand luck swings (large special bonuses) can swamp skill within one game.
- Trick-winner resolution with special-card exceptions needs to be expressible as arithmetic to be built reliably.

## Changes

- Every round is one hand of exactly 3 cards: one bid poll then 3 tricks, each played as a poll where everyone plays at the same time. (fixes: Too long and too many choices per round: a hand of i cards needs i sequential trick turns per player, far over 4 choice steps and 20 steps per round.): Gives 4 choice steps per round and about 12 steps in total. Playing at the same time keeps the core tension of guessing what others will commit, without turn order.
- Remove suits, follow-suit, trump and Scary Mary. Use an 18-card deck where each card has a power number (Escape 0, numbers 1-12, Mermaid 20, Pirates 30 and 31, Skull King 40), with one exception: the Mermaid wins any trick containing the Skull King. (fixes: Follow-suit, lead-suit and trump rules plus the Scary Mary declaration create long rule chains that are hard to build and check.): The trick winner becomes a single max-and-one-exception calculation while keeping the signature Pirate, Mermaid and Skull King cycle.
- Trick winner rule written as arithmetic on power values, with distinct values for the two Pirates so there are no ties among cards that can win. (fixes: Trick-winner resolution with special-card exceptions needs to be expressible as arithmetic to be built reliably.): The engine can compute the winner directly, and no judge is needed.
- Fixed 3-card hands over 8 rounds with a small deck. All played cards are public, and 3 to 6 cards stay unseen each round depending on player count. Bonuses are moderate (+20 per Pirate captured by the Skull King, +40 for the Skull King captured by the Mermaid) and paid only on an exact bid. (fixes: Large deck and growing hand sizes give a big hidden state, and hand-to-hand luck swings (large special bonuses) can swamp skill within one game.): Smaller, repeated, comparable hands average out deal luck. Card counting and reading bids become the decisive skill, and the bonuses stay flavourful without dominating.

## Kept from the original

- Bidding at the same time on exactly how many tricks you will win, then trying to hit it exactly.
- Exact-bid scoring of 20 per trick, a risky zero bid, and penalties for missing.
- The Escape, number, Mermaid, Pirate and Skull King hierarchy, including the Mermaid beating the Skull King.
- Capture bonuses for the Skull King taking Pirates and the Mermaid taking the Skull King.
- Several players, highest total wins.

## The variation's rules

DECK (18 cards, each with a power value): number cards 1 through 12 (power equals the number); Escape x2 (power 0); Mermaid x1 (power 20); Pirate A (power 30); Pirate B (power 31); Skull King x1 (power 40).

SETUP: Every player starts at 0 points. The game lasts exactly 8 rounds.

EACH ROUND:
1. DEAL (the round's only random event): Shuffle all 18 cards and deal 3 to each player, privately. The remaining cards stay face down and unseen for the whole round.
2. BID: All players at the same time secretly choose a bid of 0, 1, 2 or 3 (how many tricks they will win this round).
3. REVEAL BIDS: All bids are announced to everyone.
4. TRICK 1: All players at the same time choose one card from their hand to play. All played cards are revealed together and removed from hands.
5. RESOLVE TRICK 1: If the Mermaid and the Skull King were both played, the Mermaid's player wins the trick. Otherwise the card with the highest power wins the trick. If every card played has power 0 (all Escapes), nobody wins the trick. Add 1 to the winner's tricks-won count. Capture bonuses are recorded for the winner: if the Skull King won, count the Pirates in the trick (each is worth a +20 bonus); if the Mermaid won and the Skull King is in the trick, record a +40 bonus. Announce the winner.
6. TRICK 2 and RESOLVE TRICK 2: same as steps 4 and 5.
7. TRICK 3 and RESOLVE TRICK 3: same as steps 4 and 5 (each player plays their last card).
8. SCORING, for each player:
   - Bid 0 and won 0 tricks: +30.
   - Bid 0 and won 1 or more tricks: -30.
   - Bid k of 1 or more and won exactly k tricks: +20 times k, plus all capture bonuses that player recorded this round.
   - Bid k of 1 or more and won a different number: -10 times the absolute difference between bid and tricks won. No bonuses.
   - Capture bonuses are paid only on an exact bid (zero bids cannot have bonuses, since bonuses require winning a trick).
9. ANNOUNCE: Each player's tricks won, points this round and running total are announced. Reset tricks won and bonuses to 0.
10. END CHECK: After round 8 the game ends.

INFORMATION: Your own hand is private. Bids, every played card, trick winners and scores are public. There is no talk phase.

Objective: After 8 rounds, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

Expected effect: Players must judge their hand's strength against unseen cards (3 to 6 of 18 stay hidden), read opponents' public bids to infer who holds the specials, and time their plays: dump a high card when a stronger special is likely to come out, save the Mermaid to ambush the Skull King, or throw an Escape to avoid an unwanted trick. Because tricks are played at the same time, every trick is a small guessing game about when opponents will commit their strong cards. Breaking another player's bid by stealing or refusing a trick is a real tactic. Deal luck is limited: a weak hand can bid 0 for +30, close to a strong hand's 2-trick +40, and 8 short hands average out. Simple policies lose. Always bidding 0 fails whenever a forced high card wins (-30). Always bidding 3 misses most hands. Random bids and plays lose to calibrated players. Talk is left out: bids already serve as public, costly signals. With one winner, free talk would mostly add cheap bluffs about which trick a player will spend the Skull King on, and the extra steps are not worth it.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 8 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
