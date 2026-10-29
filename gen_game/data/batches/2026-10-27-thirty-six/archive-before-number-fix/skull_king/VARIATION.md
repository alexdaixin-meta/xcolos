# Variation: Skull King: Blind Broadsides

A short Skull King for 3 to 4 players played over 10 rounds of 3 cards. Players bid their exact trick count after seeing 3 revealed spare cards. Each trick is played by everyone revealing a card at the same moment. Any exact bid scores the same 30 points, so the game is about predicting and timing, not about being dealt the Skull King.

Players: 3 to 4, best with 4

## Review of the original

Skull King is a trick-taking game for 2 to 8 players over 10 hands of growing size. Players bid exactly how many tricks they will win, then play tricks with suits, black trump and special cards (Pirates, Mermaids, Escapes, the Skull King). Exact bids score big and capture bonuses, missed bids lose points, and the highest total wins.

- **non_degenerate**: weak. Testing the previous Short Seas variation: no simple policy wins outright. Always bidding 3 misses most hands, and always bidding 0 fails on strong hands. But trick play reduced to 'highest card when I need a trick, lowest when I don't', so choices changed the outcome only a little. The rotating trick-1 leader gave a small seat edge over 8 rounds with 3 players, since 8 is not a multiple of 3.
- **skill_sensitive**: bad. There were no suits and nothing to follow. The Skull King and Pirate B were near-certain tricks and cards of 9 or less almost never won, so the deal fixed each hand's trick count. Exact-bid pay rose with the bid (+20 per trick), and the +30 and +50 bonuses went only to holders of the top cards. The per-round ceiling was 30 for a weak hand and 60 to 110 for a strong one, and the deal decided an estimated 50 to 60% of results.
- **headroom**: weak. Bidding was little more than counting top cards and play was near-forced, so a competent player reached the ceiling quickly. Beyond that, results were noise from the deal.
- **reasoning_dependent**: weak. Hands were hidden and bids were public, so some inference existed. But 6 to 9 undealt cards were never revealed, which made card counting thin. Sequential play with no follow rule left little to read about opponents.
- **verifiable**: good. Trick winners and scores follow by arithmetic from the cards played and the bids. No judge is needed.
- **fits_platform**: bad. Sequential trick play meant 9 to 12 player choices per round plus the bid, against a limit of 4 choice steps. 'Winner leads the next trick' changes the acting order at runtime, which a flat step list cannot express without many conditional copies. The honest step count was well over 20.

## Problems

- P1: Sequential play inside each trick gives 10 to 13 choice steps per round, over the limit of 4.
- P2: 'The winner of a trick leads the next' changes the turn order at runtime, which needs conditional blocks of steps the engine cannot build.
- P3: Per-trick resolution (maximum, Mermaid/Skull King check, Pirate bonus, trick count, card removal) and four-case scoring push the round past 20 steps.
- P4: Exact-bid pay grows with the bid, so strong hands have a much higher ceiling than weak ones and the deal decides the winner.
- P5: The Skull King capture bonus (+30 per Pirate) and the Mermaid bonus (+50) are large automatic rewards for whoever was dealt those cards.
- P6: With sequential, unconstrained play the trick count is almost fixed by the deal, leaving little to plan or out-guess.
- P7: Undealt cards are never revealed, so there is little hidden-information inference beyond the bids.
- P8: The rotating trick-1 leader over 8 rounds gives seats unequal numbers of leads.

## Changes

- Every trick is a simultaneous poll: all players pick a card from their hand at the same moment, then all cards are revealed together. The round has exactly 4 choice steps: the bid and three tricks. (fixes: P1): This keeps choices within the limit. It also turns each trick into a guessing contest about when opponents will spend their high cards.
- Leaders and turn order are removed entirely. (fixes: P2, P8): Simultaneous tricks need no acting order, so there is no runtime reordering and no seat advantage from leading.
- Trick resolution becomes a single winner rule with one small bonus, and scoring becomes a single formula. Played cards are removed by the poll itself. (fixes: P3): Each trick then costs 3 steps (poll, reveal, resolve), giving 17 steps per round.
- Every exact bid, of any size including 0, scores a flat +30. A miss costs 10 points per trick of difference. (fixes: P4): A weak hand that correctly bids 0 earns exactly as much as a strong hand that correctly bids 3. Points come from predicting your result accurately, not from being dealt power.
- The Pirate capture bonus is removed. Only one small bonus remains: +10 when the Mermaid captures the Skull King, paid only if the bid is exact. (fixes: P5): This keeps the iconic Mermaid-beats-Skull-King moment but shrinks its payoff from 50 to 10. Landing it requires guessing which trick the Skull King will come out in.
- Simultaneous reveal combined with flat exact-bid scoring. (fixes: P6): Middle-strength hands (a 10, 11, 12 or a lone Pirate) must guess when opponents will throw their big cards. They also read the public bids to infer who holds what. A player who needs exactly one trick must time it, and can deliberately waste a strong card where an opponent's card will beat it.
- After the deal, 3 of the undealt cards are turned face up for everyone to see. (fixes: P7): Players can narrow down which top cards are in opponents' hands and cross-check that against the announced bids.
- The game lasts 10 rounds. (fixes: P4, P8): More rounds average out deal variance, and with no seat-based leading there is no rotation to balance. The step budget still fits.

## Kept from the original

- Bid exactly how many tricks you will win, scored only on exactness.
- Highest card wins the trick, with the special-card hierarchy: Escape loses, Mermaid beats numbers, Pirates beat the Mermaid, the Skull King beats Pirates, and the Mermaid beats the Skull King.
- Zero bids as a real strategy.
- Hidden hands and public bids.
- Highest total after a fixed number of hands wins.

## The variation's rules

CARDS. Each card has a power number. The deck holds 18 cards:
- the numbers 1 to 12 (power equal to the number);
- two Escapes (power 0);
- the Mermaid (power 20);
- Pirate A (power 30);
- Pirate B (power 31);
- the Skull King (power 40).

CONSTANTS. rounds = 10, hand_size = 3, tricks per round = 3, revealed cards = 3, bids from 0 to 3.

R1 SETUP. When the game starts, every player's score is 0 and the round counter is 0.

R2 ROUND START.
- round increases by 1.
- Every player's tricks_won is set to 0, bonus to 0 and hand to empty.
- The public list 'revealed' is set to empty.

R3 SHUFFLE. The deck is reset to all 18 cards and shuffled. This is the round's only chance event.

R4 DEAL. Each player receives 3 cards from the top of the deck into a private hand that only they can see.

R5 REVEAL. The next 3 cards of the deck are moved to 'revealed' and shown to everyone. These cards are out of play this round. The remaining undealt cards (3 with 4 players, 6 with 3 players) stay hidden.

R6 BID. All players bid at the same moment, without seeing other bids. The options are exactly 0, 1, 2 or 3, and the choice is stored as the number bid.

R7 ANNOUNCE. All bids are shown to everyone.

R8 TRICKS. Three tricks are played. Each trick has three steps.

(a) PLAY. All players at the same moment choose one card from their own hand. The chosen card is removed from the hand and becomes that player's 'played' card.

(b) SHOW. All played cards are revealed together.

(c) RESOLVE. The trick winner is decided as follows:
- If the played cards include both the Mermaid and the Skull King, the Mermaid's player wins the trick, even if a Pirate was also played, and that player's bonus increases by 10.
- Otherwise the card with the highest power wins.
- Only the two Escapes share a power, and there are at least 3 players, so a unique winner always exists.
- The winner's tricks_won increases by 1.

R9 SCORING. After the third trick, each player's score changes as follows:
- if tricks_won equals bid (including bid 0 with 0 tricks): +30 + bonus;
- otherwise: −10 × |bid − tricks_won|, and the bonus is lost.

R10 END. If round equals 10, the game ends. Otherwise the next round starts at R2.

There is no discussion phase.

Objective: After round 10, the player with the highest score wins. If two or more players tie for the highest score, the game is a draw.

Expected effect: Every exact bid is worth the same 30, so a weak hand bidding 0 is as valuable as a Skull King hand bidding 3. The deal matters little, and the skill is in reading your hand against the revealed cards and the public bids. Middle hands must time their one good card for a trick where opponents are likely holding back, and must dump losers where someone who announced a high bid will win. The Mermaid holder tries to guess the Skull King's trick for +10, while the Skull King holder tries to dodge the Mermaid. Simple policies lose:
- Always bid 0 and play lowest scores +30 on weak hands but misses whenever dealt the Skull King or Pirates. A player who bids accurately beats it.
- Always bid 3 and play highest rarely hits.
- Random play misses most bids.
There is no seat edge because nothing is sequential. Talk is left out because players' interests do conflict, but every claim would be cheap and unverifiable. The public bids already carry the real signal, a costly commitment about one's hand, while free talk would only add noise and steps.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
