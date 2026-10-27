# Variation: Skull King: Three-Card Bids

3 to 5 players each receive 3 hidden cards from an 18-card deck and secretly bid how many of the 3 tricks they will win. All bids are then revealed and the tricks are played as simultaneous card reveals. Exact bids score; misses cost. Highest total after 8 rounds wins.

Players: 3 to 5, best with 4

## Review of the original

Skull King is a trick-taking game for 2 to 8 players played over 10 hands of growing size. Before each hand, players bid simultaneously on exactly how many tricks they will win. Exact bids score well and misses are penalised, and special cards (Pirates, Mermaids, the Skull King, Escapes) can override suits and earn capture bonuses.

- **non_degenerate**: good. Bidding exactly is the whole game, so no fixed bid policy wins. Always bidding 0 fails whenever you hold strong cards. Always bidding high fails whenever your hand is weak. Bids are simultaneous and the lead rotates, so there is little built-in seat edge.
- **skill_sensitive**: good. Good players judge how strong a hand is, count which special cards are still out, and play to land exactly on their bid or to push a rival off theirs. The card deal adds luck to any single hand, but over 10 hands accurate bidding dominates.
- **headroom**: good. A weak player still scores on easy small hands. A strong player keeps improving on card counting, reading rivals' bids and deliberate sabotage.
- **reasoning_dependent**: good. Hands are hidden. A player must infer opponents' holdings from their bids and the cards already played, and must plan a sequence of plays to hit an exact count.
- **verifiable**: good. Trick winners and scores follow mechanically from the cards played and the bids.
- **fits_platform**: bad. Ten hands of up to 10 cards each, follow-suit legality, a lead suit defined by the first coloured card, Scary Mary declarations and clockwise sequential play together need far more than 20 steps and 4 choices per round. A 70-card deck is also costly to manage.

## Problems

- Too big for the engine: 10 hands of growing size, up to 10 tricks per hand, follow-suit rules and an 8-player turn order far exceed the steps-per-round and choice limits.
- Suits and the lead-suit rule add long chains of legality checks that the flat step list cannot express cheaply.
- Scary Mary needs an extra declaration choice, which adds a choice step for one card.
- The previous build never actually put the bid to players. Every bid was recorded as 0 and options 0 to 3 were never offered, so the scoring read a bid nobody had made.
- In the previous scoring, a successful zero bid paid 30 against 20 for one trick. That made 'always bid 0 and dump your lowest card' too attractive for a thoughtless policy.

## Changes

- Use a fixed 3-card hand, 3 tricks per round, 8 rounds, and 3 to 5 players. (fixes: Too big for the engine: 10 hands of growing size, up to 10 tricks per hand, follow-suit rules and an 8-player turn order far exceed the steps-per-round and choice limits.): This keeps every round inside 18 steps and 4 choices while preserving the bid-then-play structure.
- Replace suits with one suitless 18-card deck: numbers 1-12, two Escapes (power 0), a Mermaid (20), Pirate A (30), Pirate B (31) and the Skull King (40). Each trick is played as a simultaneous poll and won by the highest power, except that the Mermaid beats the Skull King. (fixes: Suits and the lead-suit rule add long chains of legality checks that the flat step list cannot express cheaply.): This removes follow-suit legality entirely while keeping the special-card hierarchy and its rock-paper-scissors twist.
- Drop Scary Mary. (fixes: Scary Mary needs an extra declaration choice, which adds a choice step for one card.): Saves a choice step. The two Pirates and two Escapes already supply both of her roles.
- Specify the bid step exactly. It is one simultaneous poll of all players whose options are the whole numbers from table attribute bid_min to table attribute bid_max (0, 1, 2, 3), generated from those attributes rather than typed as literals. Each player's chosen option is written into their own bid attribute, all bids are revealed only after everyone has chosen, and the scoring step reads that stored bid. tricks_won and bonus are reset to 0 at round start; bid is not reset to a literal, because the poll writes it. (fixes: The previous build never actually put the bid to players. Every bid was recorded as 0 and options 0 to 3 were never offered, so the scoring read a bid nobody had made.): The tests were right: the rules require players to choose 0 to 3, and the build never asked them.
- A successful zero bid now scores +20 and a failed zero bid -20, instead of ±30. (fixes: In the previous scoring, a successful zero bid paid 30 against 20 for one trick. That made 'always bid 0 and dump your lowest card' too attractive for a thoughtless policy.): A safe zero bid should be worth no more than one exact trick, so ducking every hand stops being the best thoughtless policy.

## Kept from the original

- Simultaneous secret bidding on an exact number of tricks, then playing to hit that number.
- The special-card hierarchy: Escapes lose, Pirates beat numbers and the Mermaid, the Skull King beats Pirates, and the Mermaid beats the Skull King.
- The original scoring shape: +20 per trick when exact, -10 per trick of error when missed, a separate zero-bid payoff, a +30 bonus per Pirate captured by the Skull King and a +50 bonus for capturing the Skull King with the Mermaid.
- Highest total after a fixed number of hands wins, with several players so one rival's loss is not automatically your gain.

## The variation's rules

SETUP
- Every player's score starts at 0. The round counter starts at 0.
- Table parameters: hand_size = 3, tricks_per_round = 3, rounds = 8, bid_min = 0, bid_max = 3.
- The deck has 18 cards, each identified by its power:
  - number cards 1 to 12 (one of each);
  - two Escapes, each of power 0;
  - one Mermaid, power 20;
  - Pirate A, power 30;
  - Pirate B, power 31;
  - the Skull King, power 40.

EACH ROUND (8 rounds)
1. Add 1 to the round counter. Set every player's tricks_won to 0 and bonus to 0. Empty every hand.
2. Gather all 18 cards into the deck and shuffle it. This is the round's only random event.
3. Deal 3 cards from the deck to each player, one at a time in seat order. Each hand is private: only its owner sees it. The undealt cards stay in the deck and are never revealed that round.
4. BID, as one simultaneous poll of all players:
   - The options are exactly the whole numbers from bid_min to bid_max, which are 0, 1, 2 and 3.
   - Each player picks one option without seeing anyone else's choice.
   - Each player's chosen number is stored as that player's bid.
5. Once every bid is in, announce all bids to everyone.
6. Play three tricks. For each trick:
   a. PLAY, as a simultaneous poll. Each player chooses one card from their own current hand. The chosen card is removed from that hand, and all played cards are then revealed to everyone.
   b. RESOLVE the trick:
      - If both the Mermaid and the Skull King were played, the player of the Mermaid wins the trick.
      - Otherwise the player of the highest-power card wins.
      - Ties cannot occur: the only equal cards are the two Escapes, and with at least 3 players at least one non-Escape card is always played.
   c. AWARD:
      - Add 1 to the winner's tricks_won.
      - If the Skull King won the trick, add 30 to its player's bonus for each Pirate played in that trick.
      - If the Mermaid won the trick and the Skull King was played in it, add 50 to the Mermaid player's bonus.
7. SCORE each player, reading their stored bid:
   - If bid is 1, 2 or 3 and tricks_won equals bid: gain 20 × bid + bonus.
   - If bid is 1, 2 or 3 and tricks_won differs from bid: lose 10 × |tricks_won − bid|. The bonus is not scored.
   - If bid is 0 and tricks_won is 0: gain 20.
   - If bid is 0 and tricks_won is 1 or more: lose 20.
8. If the round counter equals 8, the game ends. Otherwise start the next round.

There is no discussion phase.

Objective: After round 8, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw among them.

Expected effect: Each round becomes a small exact-prediction puzzle.
- Bidding: players must judge how strong their 3 cards are against the unseen ones. Special cards are double-edged: the Skull King usually wins, but loses to the Mermaid.
- Play: bids are revealed before any card is played, so players can model rivals. They can try to push a tied leader off an exact bid, or avoid winning a trick they cannot afford.
- Thoughtless policies: always bidding 0 loses whenever strong cards force a win. Always bidding 3 rarely succeeds. Always bidding 1 is exposed to sabotage. All of these lose to accurate bidders.
- Luck: over 8 rounds, bidding accuracy and play outweigh hand quality, because a weak hand bid exactly still scores while a strong hand bid wrong loses.
- Why no talk: the only conflict is that just one player can win, and claims about hidden hands are free and unverifiable. Talk would add words but no plan anyone could commit to, so it is left out.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 8 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
