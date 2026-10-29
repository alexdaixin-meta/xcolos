# Variation: Cat in the Sack: Sealed Stages (Revised)

3-5 players each feed one secret card into a shared sack every round, may make an unenforced claim about it, then bid in three sealed stages as sack cards are revealed. Passing earns a growing reward. After 9 rounds, the highest cat points plus mice wins.

Players: 3 to 5, best with 4

## Review of the original

Felicity the Cat in the Sack is a 3-5 player bluffing auction. Each round every player secretly adds one card from an identical hand (cats worth -8 to 15, a rabbit, two dogs) to a face-down 'sack'. The sack cards are revealed one by one while players bid mice or drop out for a growing consolation reward. After 9 rounds, the player with the most cat points plus leftover mice wins.

- **non_degenerate**: good. Always passing earns 2 mice a round, so 15+18 = 33 points and no cats. A sack of 3-5 cards averages roughly +10 to +15 in cat value, so a player who wins sacks at bids of 3-6 nets more than the +2 from passing, and always passing loses to sensible bidding. Always bidding everything at stage 1 wins one sack and then leaves the player broke for 8 rounds, so it loses. Always bidding the minimum raise ends up holding sacks that carry the -8 or a dog, so it can lose. Seat order only decides whose card is revealed first and who wins tied bids, and that rotates to the sack winner, so no seat has a fixed edge.
- **skill_sensitive**: good. The previous variation has no random draws per round. The only luck is the one card removed from each hand at setup, and since your own card goes into a sack anyone can win, that removal mostly changes what you know, not your score. Outcomes come from choosing which card to feed which sack, reading rivals' cards from their bids, and valuing sacks. One flaw was that gap (a) left bid visibility undefined, so the inference a skilled player should make was not guaranteed to be possible.
- **headroom**: good. A weak player still scores through pass rewards and the occasional good sack. A strong player can keep improving by counting which cards each rival has already played (nine cards each, all eventually public), timing the dogs, and exploiting the stage-3 consolation of 5 against the pass reward of 4. Card counting gets sharper in the late rounds, so play there is not solved.
- **reasoning_dependent**: weak. Hidden sack cards and private hands give real inference, but the previous variation did not say whether individual bids are shown (gap a). It also had no talk, so the main channel for reading rivals (how hard the owner of a hidden card bids, and what they claim) was undefined or missing.
- **verifiable**: weak. Scoring is pure arithmetic (cat points plus mice). However, the all-pass case (gap b) and the wording of the immediate win and stage-3 consolation (gap d) were ambiguous, so two builds could award mice differently.
- **fits_platform**: good. The previous variation is turn-based, text-only and has no board. It uses simultaneous polls and is within all limits: 15 steps, 4 choice steps, 13 attributes, 2 hidden elements, 0 random draws per round, 9 rounds.

## Problems

- P1: It is never stated what is revealed after each bidding stage (individual bids or only the standing bid), so players cannot know what they observe about rivals' hidden cards.
- P2: The all-pass case is ambiguous: it is unclear whether other passers collect the reward when the previous leader is stuck with the sack, and what everyone gets when all pass at stage 1.
- P3: Talk is undecided in a 3-5 player game with private card knowledge and conflicting interests over each sack. Claims about card faces would give rich material to reason about, but there is no place for them.
- P4: The wording of the immediate win ('at their bid') and the stage-3 consolation ('every other player still in') is imprecise.
- P5: Adding a separate talk step would push choice steps to 5, over the limit of 4.

## Changes

- After every stage, each player's number (their bid, or 0 for a pass) is announced by name, together with the new standing bid, the leader and every player's mice. (fixes: P1): This makes observations exact, so a player can infer, for example, that the owner of hidden card 3 bidding high suggests it is a good cat.
- All-pass rules stated exactly. At stage 1, if all pass, every player gains 2 and the sack is discarded unopened. At stage 2 or 3, if all players still in pass, the previous leader takes the sack at the standing bid and gets no reward, while every other passer gains that stage's reward. (fixes: P2): This removes the ambiguity, so every build pays out the same mice.
- Simultaneous talk is folded into the placement poll. While placing their card face down, each player writes one short message. All messages are shown once the sack is laid out, before stage 1. Claims are not enforced. (fixes: P3, P5): This gives players claims to make, test and bluff about (for example 'mine is the 15' or 'mine is the small dog'). It passes both talk tests: players disagree because only one player wins the game and each sack, and it adds no extra choice step.
- Reworded: the immediate win happens 'at the standing bid just set'. The consolation reads 'each player who bid at stage 3 but is not the leader gains 5'. (fixes: P4): This states clearly who pays what and who is consoled.

## Kept from the original

- Identical 10-card hands with cats -8, -5, 3, 5, 8, 11, 15, a rabbit, a large dog and a small dog, with one random card removed unseen from each hand.
- A sack built from one face-down card per player, revealed one card at a time during the auction.
- Dropping out earns a growing consolation of mice.
- The dog rule: a lone large dog eats the highest cat and a lone small dog eats the lowest; two dogs cancel.
- The sack winner becomes the next start player.
- 9 rounds, scored as cat points plus mice, with cat points as the tie-break.

## The variation's rules

SETUP
- Each player gets an identical hand of 10 cards: cats worth -8, -5, 3, 5, 8, 11 and 15; a rabbit worth 0; a large dog; and a small dog.
- One random card is removed from each hand and set aside unseen by everyone. Each player keeps 9 cards in a private hand.
- Each player starts with 15 mice and 0 cat points. Both numbers are public throughout.
- Seats are in a fixed order. A random player is the first start player.

EACH ROUND (9 rounds; every player plays exactly one card per round, so every hand is empty after round 9)

1. Fill the sack and talk.
   - All players, at the same moment, choose one card from their hand and place it face down. The card leaves their hand.
   - In the same moment, each player writes one short message (at most 30 words). Messages are free text, may claim anything and are not enforced.

2. Lay out the sack.
   - The sack is laid out in seat order beginning with the start player. Sack card 1 is the start player's card, card 2 belongs to the next player in seat order, and so on.
   - Everyone knows whose card is in each position. Only the owner knows its face.
   - All messages are now shown to everyone, labelled with each writer's name.

3. Stage 1.
   - Sack card 1 is revealed to all. The standing bid is 0 and there is no leader.
   - All players, at the same moment, write a whole number. 0 means pass; anything else is a bid.
   - A bid must be at least the standing bid + 1 and at most the player's current mice. An illegal number counts as a pass.

4. Resolve the stage. Apply these rules after every stage, in this order:
   a. Announce: every bidder's number (bid, or 0 for a pass) is shown to all by name.
   b. All passed at stage 1: if every player passed, every player gains 2 mice, nobody takes the sack, and it is discarded without being opened. Go to step 9.
   c. All passed at stage 2 or 3: if every player still in passed, the leader from the previous stage takes the sack at the standing bid and gains no reward. Every other player who passed at this stage gains the reward for this stage. Go to step 7.
   d. Otherwise:
      - Each player who passed at this stage leaves the auction for the round and gains mice from the bank: 2 at stage 1, 3 at stage 2, 4 at stage 3.
      - The standing bid becomes the highest bid made at this stage, and the player who made it is the leader.
      - If several players made the highest bid, the leader is the first of them in seat order, counting from the player after the start player, with the start player counted last.
      - The new standing bid, the leader and every player's mice are announced.
   e. Immediate win: if exactly one player is still in, that player wins the sack at the standing bid just set. Skip the remaining stages and go to step 7.

5. Stage 2.
   - Played only if two or more players are still in.
   - Sack card 2 is revealed.
   - The players still in, at the same moment, pass (0) or bid between the standing bid + 1 and their current mice. An illegal number is a pass.
   - Resolve as in step 4.

6. Stage 3.
   - Played only if two or more players are still in.
   - Sack card 3 is revealed.
   - The players still in, at the same moment, pass or bid under the same rules.
   - Resolve as in step 4.
   - Then, if two or more players are still in, the leader wins the sack at the standing bid, and each player who bid at stage 3 but is not the leader gains 5 mice.

7. Open the sack.
   - All sack cards are revealed. With 4 or 5 players, cards 4 and 5 are seen for the first time.
   - Dog rule: if exactly one dog is in the sack, it removes one cat. The large dog removes the highest-valued cat; the small dog removes the lowest-valued cat. If no cat is present, nothing is removed. If both dogs are present, neither has any effect.
   - All dogs and any removed cat are discarded.

8. Pay and score.
   - The sack winner pays their winning bid in mice to the bank.
   - The sack winner adds the total value of the cats remaining in the sack to their cat points. Cat points may go negative. The rabbit is worth 0.
   - The sack cards are discarded face up, so everyone can see which cards each player has used.

9. Next start player.
   - The sack winner becomes the start player.
   - If nobody took the sack, the start player passes to the next seat.

END
After round 9, each player's score is cat points + mice.

Objective: The player with the highest score (cat points + mice) wins. If several players tie, the tied player with the most cat points wins. If they are still tied, the game is a draw among them.

Expected effect: Public per-player bids turn every bid into evidence. A high bid from the owner of a still-hidden card, or a quick pass after their own card is revealed, tells the others something. Talk adds a bluffing layer.

What players disagree about: each sack and the game have only one winner. An owner may claim their -8 is the 15 to bait rivals into overpaying for a bad sack, claim their 15 is a dog to win it cheaply themselves, or announce a small dog to scare bidders off a sack holding the -8. A player who simply believes claims can pay 8 mice for a sack worth -5. Because played cards are discarded face up and every hand starts identical, claims become checkable over the rounds, so credibility becomes something to manage.

Passing earns at most 33 points over the game, which loses to anyone buying good sacks cheaply. Spending everything early leaves a player shut out of later sacks. With exact all-pass rules, every build scores the same.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 9 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
