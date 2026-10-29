# Variation: Loot: Sealed Raids

Four pirates each own three merchant ships (3, 5 and 7 gold) and a hidden 30-point crew. Each round one owner secretly sails a ship. Everyone commits crew at the same moment, and spent crew is lost. The highest strength takes the gold, and most gold after 12 rounds wins.

Players: 3 to 5, best with 4

## Review of the original

Loot is a 2-8 player card game. Players sail merchant ships worth 2-8 gold. Rivals attack them with colored pirate cards, and whoever holds the highest strength of one color, or the trump captain or Admiral, when their turn comes round claims the ship. Gold from claimed ships is scored, minus merchants left in hand.

- **non_degenerate**: weak. Some simple policies do lose: never attacking forfeits most gold, and hoarding merchants costs gold at the end. But drawing a strong captain or a high merchant gives a large edge that no choice creates. In two-player games, defending everything and attacking little is often enough.
- **skill_sensitive**: weak. Card counting and timing attacks help. However, which captains, Admiral and pirate colors you draw largely decides the contests, so the draw is a large share of the result.
- **headroom**: good. Weak players still win some uncontested ships. Strong players improve by timing boosts, reading which colors rivals hold, and choosing when to sail high merchants.
- **reasoning_dependent**: good. Hands are hidden. Players infer whether a rival can still beat a contest from what has been discarded, and decide whether to commit more cards to a fight or let it go.
- **verifiable**: good. Gold is summed arithmetically from claimed merchants, minus merchants left in hand.
- **fits_platform**: bad. There are many simultaneous ship contests, each tracked per color, with a turn-relative claim timing ('since your last turn'), a 78-card deck and draws every turn. That means many hidden elements, many draws per round and long chains of rules, far beyond the step and attribute limits.

## Problems

- Too many concurrent contests, each with per-color strength tracking and turn-relative claim timing: it cannot be built inside the step and attribute limits.
- Several random draws per turn from a large deck: this exceeds the one-draw-per-round limit and lets the luck of the draw (captains, Admiral, high merchants) swamp skill.
- Endowments are unequal: one player can be dealt captains and 8-gold merchants while another gets 2s and weak pirates, so the draw alone can decide the winner.
- Card counting by color is an important skill, but it rests on a large hidden state that the platform cannot track.

## Changes

- Replace the open-ended multi-ship board with one contest per round. A rotating owner sails one merchant, and every player commits strength to it at the same moment. (fixes: Too many concurrent contests, each with per-color strength tracking and turn-relative claim timing: it cannot be built inside the step and attribute limits.): One contest per round fits about 12 steps and keeps the core attack-versus-defend fight for a merchant.
- Replace the pirate cards with a private budget of 30 crew points per player. Crew committed is spent whether the contest is won or lost, as attacking cards were discarded. (fixes: Several random draws per turn from a large deck: this exceeds the one-draw-per-round limit and lets the luck of the draw (captains, Admiral, high merchants) swamp skill.): This keeps the cost of fighting and the choice to fight or let go, without a deck or any draws.
- Give every player the identical merchant set (3, 5 and 7 gold), one Captain (+6 strength once as an attacker) and one Admiral (an automatic defense once as the owner). (fixes: Endowments are unequal: one player can be dealt captains and 8-gold merchants while another gets 2s and weak pirates, so the draw alone can decide the winner.): Equal endowments mean the result comes from play, not the deal. The trump cards remain as one-shot timing decisions.
- The owner secretly chooses which unsailed merchant to sail. Commitments stay secret, and only the winner, the ship's value and any trump used are announced, so remaining crew stays hidden. (fixes: Card counting by color is an important skill, but it rests on a large hidden state that the platform cannot track.): This replaces card counting with one manageable piece of hidden state: rivals must infer how much crew each player has left from which contests they won, and guess the ship's value from the owner's remaining set and behavior.
- Add one simultaneous message per player before commitments. (fixes: Card counting by color is an important skill, but it rests on a large hidden state that the platform cannot track.): With only one winner, players disagree. Bluffing about a ship's value or one's remaining crew, and proposals to gang up on the leader, are worth reasoning about.

## Kept from the original

- Merchant ships worth gold, sailed by their owner and attacked by rivals
- Fighting costs resources that are lost whether you win or lose
- Ties between top attackers leave the ship with its owner
- A one-shot Captain that boosts an attack and a one-shot Admiral that defends your own ship
- Hidden information about what rivals can still commit
- Most gold wins

## The variation's rules

SETUP: Each player starts with 30 crew (private: only that player and the engine know their remaining crew), 0 gold, three unsailed merchant ships worth 3, 5 and 7 gold, one unused Captain and one unused Admiral. Players are seated 1 to N. The game lasts 3 x N rounds (12 with 4 players).

EACH ROUND:
1. Owner. The owner is player ((round - 1) mod N) + 1. Each player is owner exactly 3 times. The engine announces who the owner is and which of the owner's ships are still unsailed.
2. Sail. The owner privately chooses one of their unsailed ships to sail. If only one remains, it is sailed automatically. Its value is not yet revealed.
3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.
4. Commit. At the same moment, every player secretly chooses a whole number of crew to commit, from 0 up to their remaining crew. In the same poll, the owner may declare their Admiral if it is unused, and each non-owner may declare their Captain if it is unused. Invalid amounts are set to 0. Invalid trump declarations are ignored.
5. Spend. Every player's committed crew is subtracted from their remaining crew, whatever the result.
6. Strength. The owner's defense equals the crew they committed. Each attacker's strength equals the crew they committed, plus 6 if they declared their Captain this round.
7. Resolve. The rules are applied in this order:
   (a) If the owner declared the Admiral, the owner keeps the ship.
   (b) Otherwise, find the highest attacker strength. The ship goes to that attacker only if their strength is strictly greater than the owner's defense and strictly greater than every other attacker's strength.
   (c) In every other case, including ties between the top attackers or an attack that does not beat the defense, the owner keeps the ship.
8. Score. Whoever gets the ship adds its value to their gold.
9. Bookkeeping. The ship is marked sailed. Declared trumps are marked used.
10. Announce. The engine reveals the ship's value, who got it, and who used a Captain or Admiral this round. It does not reveal any crew amounts.
11. Advance. Move to the next round, or end the game after round 3 x N.

END: Unspent crew is worth nothing.

Objective: After the final round, the player with the most gold wins. If two or more players tie for the most gold, the game is a draw.

Expected effect: Every ship now costs crew to fight for, so players must budget 30 crew across 12 contests. They read the 3/5/7 set each owner has left to guess the sailed ship's value, and infer rivals' remaining crew from which contests each player won. Simple policies lose. Never committing lets attackers take your ships with 1 crew. Going all-in early leaves you defenseless later. A flat spread is beaten by rivals who concentrate on 7s or who wait for depleted owners. Timing the Captain and Admiral matters because attackers commit without knowing whether the Admiral is coming. Talk earns its place because only one player can win. Players disagree over whom to attack and whether a ship is worth fighting for. An owner may claim a ship is the 3 to deter raids. A player may propose that everyone gang up on the leader, then hold back crew while others spend theirs. A player who just follows a proposal to attack the leader can lose: they burn crew while the proposer free-rides, or they lose crew to an unannounced Admiral.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
