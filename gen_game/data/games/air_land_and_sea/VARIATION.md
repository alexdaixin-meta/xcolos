# Variation: Air, Land and Sea: Three Fronts

Two commanders secretly commit one card per round across three theaters for six rounds per battle. Each card goes face-up in its own theater or face-down anywhere as strength 3, and a commander may withdraw early to limit losses. The first to 12 VP wins the match.

Players: 2 to 2, best with 2

## Review of the original

Air, Land and Sea is a two-player card duel fought over a series of battles. Players alternate placing cards into three theaters, either face-up in the card's own theater with its ability or face-down anywhere as strength 2, or they withdraw to concede. Whoever controls more theaters wins the battle, victory points depend on how early a loser withdraws, and the first player to 12 VP wins.

- **non_degenerate**: bad. In the tested variation, 'always first option' won 60-0 as seat 1 and 59-0-1 as seat 2 against random seats, and 'always last option' (withdraw) lost every match. The first option was an always-good action, so the interesting choices (improvise or withdraw) were pointless. The original also gives the first player a built-in edge through tie wins and initiative.
- **skill_sensitive**: weak. The design intent rewards placement and timing, but a fixed policy matched or beat all play, so skill showed up only as 'don't do anything else'. Hand quality from the deal also swings single battles strongly.
- **headroom**: weak. Once 'deploy the first card face-up' is known to win, nothing remains to improve. The original's ability interactions have headroom, but they cannot be built within the limits.
- **reasoning_dependent**: good. The core is reasoning-rich. Opponents' hands are hidden, six cards are undealt, face-down cards hide their identity, and deciding when to withdraw requires predicting the battle's outcome. The tested build simply did not reward any of it.
- **verifiable**: good. Theater control, battle results and VP are sums and comparisons.
- **fits_platform**: weak. The three 'boards' are just three counters per side, which is fine. However, 18 unique card abilities (flip, move, draw, adjacency, ongoing effects) far exceed the step and attribute limits. Alternating turns with a first-player tie edge also introduces seat asymmetry.

## Problems

- P1: The first listed action (deploy face-up) dominated. A thoughtless 'always first option' policy won every decided match from either seat.
- P2: Improvise (face-down, strength 2) was almost never better than deploying, so the hidden-card bluff and flexibility choice was dead.
- P3: Withdraw was a pure giveaway. 'Always last option' lost 100%, and withdrawing never saved enough VP to be a real decision.
- P4: Play reduced to 'dump the strongest card in its own theater'. There was no reason to read the opponent or vary allocation.
- P5: There was seat asymmetry: the first player moves first and wins ties.
- P6: The 18 unique card abilities with flip, move and adjacency effects are too complex to build within 20 steps and 20 attributes.

## Changes

- Split each turn into two choices: which card (hand listed in random dealt order) and which theater (Air, Land, Sea). The card is automatically face-up if the theater matches its own, otherwise face-down. There is no 'deploy' option at the top of a list. (fixes: P1): 'Always first option' now means playing a random card into Air every time. That piles all strength into one theater and usually loses Land and Sea, so the first option is a bad policy rather than a dominant one.
- Face-down cards count as strength 3 (not 2) in any theater. (fixes: P2): Cards of strength 1-3 are now at least as good face-down, and face-down play lets you contest a theater where you hold no matching cards. Improvising becomes a frequent, real decision.
- Battle wins pay 4 VP, or 6 VP for controlling all three theaters. Withdrawing at the start of battle round k gives the opponent 2 + floor((k-1)/2) VP (2, 2, 3, 3, 4, 4). If both withdraw in the same round, nobody scores. (fixes: P3): Conceding early with a bad hand saves 2-4 VP against a likely loss, especially a sweep. Withdrawing every time still never scores, so 'always last option' still loses, while timely withdrawal becomes a skill.
- Both players choose at the same moment each round, and placements are revealed after each round. Face-down identities stay hidden, and six cards per battle are never dealt. (fixes: P4): Each round becomes a blind allocation contest: guess where the opponent will commit, concede a theater cheaply, or win it narrowly. Players must also infer the opponent's remaining hand from the known 18-card deck, revealed face-up cards and the unknown undealt cards.
- Simultaneous turns replace alternation, and tied theaters are controlled by nobody. (fixes: P5): This removes the first-player initiative and tie advantage, so neither seat has a structural edge.
- Card abilities are removed. Cards are only a theater and a strength (1-6). (fixes: P6): This keeps the game inside the step and attribute limits, while placement, bluffing and withdrawal timing carry the depth.

## Kept from the original

- Three theaters (Air, Land, Sea) on each side, with control by higher total strength and the battle won by controlling more theaters.
- An 18-card deck of Air, Land and Sea cards, with six dealt to each player per battle.
- Face-up deployment in a card's own theater versus face-down improvisation anywhere at a fixed strength.
- Withdrawal as a concession whose cost grows the later you withdraw.
- A match of several battles, with the first to 12 VP winning.

## The variation's rules

DECK. There are 18 cards. Each has a theater (Air, Land or Sea) and a strength from 1 to 6, giving exactly one card of each strength per theater (Air 1-6, Land 1-6, Sea 1-6). Both players know the full deck list.

MATCH STRUCTURE. The match lasts at most 36 rounds. It is a sequence of battles, and each battle lasts up to 6 battle rounds. Battle round 1 of the first battle is match round 1. When a battle ends, the next battle begins in the next match round, but only if at least 6 match rounds remain (the next round is 31 or earlier). Otherwise the match ends.

START OF A BATTLE (battle round 1 only). Shuffle all 18 cards. Deal 6 privately to each player; this is the round's one random draw. The remaining 6 stay unseen for this battle. Each player's hand is shown to them in the order dealt. Both players' strength in each theater is set to 0.

EACH BATTLE ROUND, in order:
1. WITHDRAW DECISION (simultaneous). Each player secretly chooses 'Fight' or 'Withdraw'.
   - If exactly one player withdraws in battle round k, the other player gains 2 + floor((k-1)/2) VP. That is 2 VP in rounds 1-2, 3 VP in rounds 3-4 and 4 VP in rounds 5-6. The battle ends immediately.
   - If both withdraw, nobody scores and the battle ends.
2. CARD CHOICE (simultaneous). Each player secretly picks one card from their hand.
3. THEATER CHOICE (simultaneous). Each player secretly names Air, Land or Sea.
4. PLACEMENT. Each chosen card leaves its owner's hand and is placed on its owner's side in the named theater.
   - If the named theater matches the card's own theater, the card is face-up and adds its printed strength.
   - Otherwise it is face-down and adds exactly 3 strength.
5. REVEAL. Both players are told every new placement. Face-up cards show their identity. A face-down card is shown only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced.
6. If this was battle round 6 (both hands empty), the battle is resolved.

RESOLVING A BATTLE.
- In each theater, the player with the higher strength controls it. A tie means nobody controls it.
- The player controlling more theaters wins the battle. If both control the same number, the player with the higher total strength across all three theaters wins.
- If that is also equal, the battle is drawn and nobody scores.
- The winner gains 4 VP, or 6 VP if they control all three theaters.
- All face-down identities are then revealed to both players.

AFTER EACH ROUND, the match ends if either player has 12 or more VP.

Objective: The first player to reach 12 VP at the end of a round wins. Only one player can score in any battle, so both can never reach 12 together. If the match ends because the round limit allows no further full battle, the player with more VP wins. Equal VP is a draw.

Expected effect: Thoughtless policies now lose. 'Always first option' (Fight, the first dealt card, Air) stacks everything in Air and is out-controlled in Land and Sea. 'Always last option' withdraws every battle and never scores. Random play spreads cards badly and wastes high cards face-down. Good play involves several skills: playing 4-6s face-up and 1-3s face-down to contest weak theaters; reading where the opponent is committing from earlier reveals; deliberately conceding one theater to win two narrowly; counting the opponent's possible remaining cards from the known deck, their face-ups and the six unknown undealt cards; and withdrawing early from hopeless hands to deny a 4-6 VP win. Simultaneous play and nobody-wins-ties remove the seat edge. The deal varies hand strength, but early withdrawal caps the loss from a bad hand, and a 12 VP race over several battles lets skill dominate. Talk is omitted because the game has two players and is purely competitive.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
