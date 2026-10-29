# Variation: Psychological Jujitsu: Hidden Favourites

This is GOPS for 3 to 4 players. Each player secretly holds a bonus prize value worth +5 extra if won. A short simultaneous talk phase comes before each bid, and tied top bids cancel so that the next-highest bid takes the prize.

Players: 3 to 4, best with 3

## Review of the original

Psychological Jujitsu (also called GOPS) is a sealed-bid card game. Each round a random prize card from 1 to 13 is turned up, and every player secretly bids one card from an identical hand of 13. The highest bid takes the prize's points, each card can be used only once, and the highest total after 13 rounds wins.

- **non_degenerate**: good. Every player starts with an identical hand, so no seat has an edge. Simple policies all lose to an attentive opponent. 'Always play my lowest card' loses every prize to someone bidding one higher. 'Always play my highest card' is beaten by giving up the first round with an Ace and then beating each later bid by exactly one, which wins 12 of 13 prizes. 'Bid equal to the prize' is beaten by bidding prize+1 and dumping Aces on the prizes you give up. Random bidding wastes high cards on low prizes.
- **skill_sensitive**: good. The random prize order affects both players equally. Skill lies in spending budget efficiently, and that reliably beats naive play. Two-player GOPS has a non-trivial equilibrium, and strong exploitative play wins most matches against fixed patterns.
- **headroom**: good. A weak player still wins some prizes, since every bid takes something. A strong player keeps improving through budget planning (how much is left for the remaining prizes), modelling the opponent's tendencies and endgame calculation, and the game is not practically solved for multiplayer.
- **reasoning_dependent**: weak. The opponent's current bid is hidden, and predicting it is the core of the game. However, the remaining hands are common knowledge once bids are revealed, and no player has private information of their own. The only things to infer are the upcoming prize order, which is pure chance, and the opponent's tendencies. With 3 or more players, the original rule of discarding the prize on a tie is crude, and the game mostly becomes 2-player duels.
- **verifiable**: good. The prize winner is found by comparing numbers, and scores are sums of card values. No judgement is needed.
- **fits_platform**: good. It uses simultaneous numeric choices from a tracked hand, a shuffled prize list and 13 rounds. There is no board, and it is text-only and short.

## Problems

- There is no private information. Hands are fully deducible, so the only inference is guessing an opponent's style, which limits hidden-state reasoning.
- The original gives two tie rules as alternatives. A rule set must pick one, and with 3 or more players the 'discard everything' rule throws away many prizes and blunts interaction.
- Models may lose track of which cards remain, which turns bad play into bookkeeping errors rather than reasoning errors.
- The rules do not say what happens if a player names a card they no longer hold.
- The original never says how a tie for the highest final total is resolved.

## Changes

- Each player is secretly dealt a different 'bonus card' value from 5 to 9. Winning that prize earns +5 extra points. (fixes: There is no private information. Hands are fully deducible, so the only inference is guessing an opponent's style, which limits hidden-state reasoning.): This gives each player a private stake that shapes what they should do. Rivals must infer it from unusually strong bids on middling prizes. Every bonus is the same flat +5 and drawn from a narrow mid range, so it changes what to fight for without deciding who ends ahead.
- The game is fixed at 3 to 4 players, and the original's 'next highest' variant is adopted. Tied highest bids are cancelled and the prize goes to the highest bid that is not tied. If every bid is tied, the prize is discarded. (fixes: The original gives two tie rules as alternatives. A rule set must pick one, and with 3 or more players the 'discard everything' rule throws away many prizes and blunts interaction.): This creates real multi-way tactics. Two rivals clashing at the top can hand the prize to a third player's modest bid. Because only one player can win, it also gives talk something to fight over.
- A short simultaneous message phase is added before each bid. (fixes: There is no private information. Hands are fully deducible, so the only inference is guessing an opponent's style, which limits hidden-state reasoning.): With one winner and hidden bonus cards, players can bluff about their bonus, threaten to contest a prize, or try to coordinate against the leader. The tie rule makes naive coordination dangerous: if two players agree to both bid 13, they cancel out and hand the prize to the next highest bidder.
- At the start of each round, the engine announces every player's remaining hand, every score and the remaining prize values. (fixes: Models may lose track of which cards remain, which turns bad play into bookkeeping errors rather than reasoning errors.): This removes bookkeeping failure so that results reflect strategy.
- An invalid or missing bid is replaced by that player's lowest remaining card. (fixes: The rules do not say what happens if a player names a card they no longer hold.): The rules become complete and build-able, and an invalid bid carries a mild penalty.
- Final ties are resolved as a draw among the tied leaders. (fixes: The original never says how a tie for the highest final total is resolved.): The winner rule becomes complete and purely arithmetic.

## Kept from the original

- Identical hands of Ace to King (1 to 13), each card usable only once.
- A shuffled prize pile of 1 to 13, revealed one card per round over 13 rounds.
- Simultaneous secret bids, with the highest bid winning the prize's face value.
- The original's 'discard tied bids, award to next highest' tie variant.
- Highest total wins.

## The variation's rules

SETUP: Each player receives a hand of 13 cards valued 1 to 13 (Ace=1 up to King=13). The prize pile holds 13 cards valued 1 to 13 and is shuffled face-down. Each player is then privately told one bonus value, drawn at random without replacement from {5,6,7,8,9}, so no two players share a bonus value. Only that player knows their bonus value. All scores start at 0.

EACH ROUND (13 rounds):
1. The engine reveals the top card of the prize pile as this round's prize. It also announces every player's remaining hand, every current score and the prize values still in the pile.
2. Talk: everyone writes one short message (at most 40 words) at the same time without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.
3. Bid: everyone secretly chooses one card from their remaining hand at the same time. If a player names a card they do not hold, or gives no valid bid, their lowest remaining card is used.
4. All bids are revealed, and each bid card is removed from its owner's hand permanently.
5. Resolution: any bid value chosen by two or more players is cancelled. The highest bid that is not cancelled wins the prize. If every bid is cancelled, the prize is discarded and nobody scores. Example: bids 10, 10 and 4 give the prize to the player who bid 4.
6. The winner adds the prize's value to their score. If the prize's value equals the winner's secret bonus value, they add 5 more points.
7. The result is announced: all bids, who won the prize (if anyone), and the new scores. When a bonus is scored, the announcement says only '+5 bonus' with the winner's new total, so the bonus value becomes known only through that event.

END: After 13 rounds, all hands and the prize pile are empty. Bonus values are revealed.

Objective: The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw among them.

Expected effect: Players must budget 91 points of bidding power across 13 prizes, predict rivals' bids and exploit the cancellation rule, for example by bidding moderately when two rivals are likely to clash high. The hidden bonus makes a 5 to 9 prize worth up to 14 to one player. Rivals must notice who bids suspiciously high on mid prizes and deny them, while the holder weighs revealing their interest against paying for it. Talk passes both tests. Players disagree because only one can win, every prize goes to at most one player, and bonus values differ. A player who just follows a proposal such as 'let's both bid King on this to stop the leader' can cancel out with their partner and hand the prize to the leader, or can be betrayed by a partner who secretly bids lower and spends less. Bluffing about one's bonus value can steer rivals' spending. Simple policies all lose: 'always highest' and 'always lowest' are beaten by one-up bidding, and players copying the same pattern cancel each other out.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 13 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
