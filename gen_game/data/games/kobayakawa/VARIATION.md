# Variation: Kobayakawa Duel Rounds with Table Talk

Each round, players hold one hidden card and may swap it, publicly bluff about their strength, then simultaneously bet to fight. The lowest card among the fighters gains K, and the highest total takes the pot plus a kamon from the centre. Most kamons after 10 rounds wins.

Players: 3 to 5, best with 4

## Review of the original

Kobayakawa is a 3-6 player bluffing and betting game. Each player holds one hidden card. In a draw phase they may improve their card or change the shared Kobayakawa card. Players then bet a kamon to fight. Among the fighters, the lowest card adds the Kobayakawa value, and the highest total takes the pot plus one kamon from the centre. Most kamons at the end wins.

- **non_degenerate**: good. Always PASS never gains. The other players start with 15 kamons between them (at 3 players), and every contested fight moves a kamon from the centre to them, so their average rises above 5 and someone passes the passer: always PASS loses. Always FIGHT loses its stake whenever it holds a middle card against two or more fighters, and it is easy to exploit. Ties go to the lower card, not to a seat, so no seat has an edge. The lowest-card bonus means neither high nor low cards are safe, so the choices change the outcome.
- **skill_sensitive**: weak. In the reviewed variation the fight poll was simultaneous and silent. Whether a card wins depends mostly on how many others fight: a middle card wins against one opponent but not two. Players could only guess the field size, so a large share of results came from guessing rather than reading opponents.
- **headroom**: good. There is a lot to learn: using K and the public discards to estimate card ranges, reading KEEP/SWAP as a signal, and managing stakes over 10 rounds. A weak player still wins some fights through the lowest-card bonus.
- **reasoning_dependent**: good. Cards are hidden and the discards are partial public signals. The value of a card depends on the opponents' likely cards and on how many of them fight, so inference is required.
- **verifiable**: good. Totals, the winner, pot transfers and the final kamon counts are all arithmetic on tracked numbers.
- **fits_platform**: weak. It fits the limits: one shuffle per round, fixed 10 rounds, 15 steps. However, the original's sequential fight information was removed and nothing replaced it. The playable review failed it for having no talk in a 3-5 player game with opposed interests.

## Problems

- The fight decision depends strongly on how many others fight, but the simultaneous silent poll gives no way to learn or influence that, so the poll is largely blind guessing.
- The game has 3-5 players with directly opposed (zero-sum) interests, which is exactly where bluff talk adds reasoning, yet the design was silent on talk and failed the playable check.

## Changes

- Add one simultaneous, non-binding public talk step after the discards are announced and before the fight poll. Every player writes one short message at the same moment, then all messages are shown. (fixes: The fight decision depends strongly on how many others fight, but the simultaneous silent poll gives no way to learn or influence that, so the poll is largely blind guessing.): Players can now claim strength, threaten to fight, or bluff to deter others. Listeners must judge those claims against K, the discards and past behaviour, which replaces the sequential information of the original with something to reason about.
- State explicitly that messages may be false and bind nobody, and that the fight poll stays simultaneous so no seat speaks or acts last. (fixes: The game has 3-5 players with directly opposed (zero-sum) interests, which is exactly where bluff talk adds reasoning, yet the design was silent on talk and failed the playable check.): Bluffing stays costly to believe, and no fixed seat gains a positional edge.

## Kept from the original

- One hidden card per player and a public Kobayakawa value K
- Lowest card among the fighters adds K, and the highest total wins
- Kamon stakes, the winner takes the pot plus 1 from the centre
- A draw phase that can replace the card, with the discard shown face up as a public signal
- A lone fighter wins without revealing
- Most kamons at the end wins

## The variation's rules

SETUP: Each player starts with 5 kamons. The centre starts with 10 kamons. The game lasts exactly 10 rounds.

EACH ROUND:
1. Deal. Shuffle a fresh deck of 15 cards numbered 1 to 15. Deal each player one face-down hand card, which only that player sees. Deal each player one face-down reserve card, which nobody sees. Turn one more card face up: this is the Kobayakawa card, value K. Announce K.
2. Draw choice. All players choose KEEP or SWAP at the same moment. A SWAP player discards their hand card face up, takes their reserve card as their new hand card, and looks at it. Reserve cards of KEEP players are not used. Announce every discarded card and who discarded it.
3. Talk. Every player writes one short public message at the same moment, without seeing the others' messages. Then all messages are shown to everyone. Messages may say anything, including false claims about one's card or intentions. Nothing said is binding.
4. Fight choice. All players choose FIGHT or PASS at the same moment. A player with 0 kamons must PASS. Each FIGHT player puts 1 kamon into the pot.
5. Resolve.
   - No fighters: nothing happens.
   - Exactly one fighter: that player takes their own kamon back. Their card is not revealed, and the centre pays nothing.
   - Two or more fighters: all fighters reveal their cards. Each fighter's total equals their card, except that the fighter with the lowest card adds K to it. The fighter with the highest total wins. If totals tie, the tied fighter with the lower card wins. The winner takes the whole pot. If the centre has at least 1 kamon, the winner also takes 1 kamon from the centre. Losing fighters lose their stakes.
6. Announce all fighters, revealed cards, totals, the winner, and every player's kamon count.
7. After round 10 the game ends.

Objective: After round 10, the player with the most kamons wins. If two or more players tie for most, the game is a draw.

Expected effect: Talk gives the fight poll something to reason about. The game is zero-sum on the pot, so players disagree about who should fight. Each player wants weak rivals to fight into their strong card and strong rivals to stay out. A player with a middle card benefits from claiming 'I have 14, stay out' to shrink the field. A player who simply follows that claim and passes with a card that would have won forfeits the pot and the centre kamon. A player who believes a fake 'I'm passing' and fights a middle card into three fighters loses the stake. Players must weigh claims against K, the public discards, KEEP/SWAP signals and each speaker's honesty in earlier rounds. There is no cooperative option, so endgame unraveling does not apply. Always PASS loses whenever any contested fight occurs, and always FIGHT loses stakes against attentive players.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
