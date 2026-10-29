# Variation: Growl: Trial by Moonlight

7 players, 2 secret wolves. Each day everyone talks at once and then votes. The top vote-getter is put on Trial and their true role is revealed. Wolves die, while innocent humans are cleared but wounded. Each silent night, wolves Maul and everyone Salves. Wolves win at parity, or if humans are fewer than twice the wolves after the Final Night (round 5). Humans win by killing both wolves or by keeping that 2:1 ratio.

Players: 7 to 7, best with 7

## Review of the original

Growl is a 4-10 player hidden-team card game. Cards from a shared face-up deck are handed to other players, and on Night phases each player silently passes one card left and one right. Wounds kill a player, and bites secretly turn humans into werewolves. Humans win if at least one human survives the Final Night.

- **non_degenerate**: bad. In the original, whoever sits next to a wolf receives its bites, so seat adjacency decides much of who gets infected. In the previous variation, a thoughtless wolf policy won about 70% at 6 players: bloc-vote one human and focus both Mauls on one target (or focus Bites for a hidden infection swing). A round-6 timeout also handed the win to any surviving wolf. Balance swung from about 70/30 at 6 players to about 45/55 at 7.
- **skill_sensitive**: weak. The previous variation's human win rate moved from about 0.15 to about 0.65 depending on one random exposure draw. The day-1 lynch and Salve choices were blind guesses. A strong human reasoner was not clearly better than a random voter.
- **headroom**: weak. Wolves had real decisions (Maul, Bite or a disguising Salve). Humans had almost no reliable signal: Charm feedback could clear a human but never identify a wolf. So the human side had little room to improve.
- **reasoning_dependent**: weak. Hidden roles give plenty to infer, but the only hard evidence of a wolf was a random 2/N exposure each night. Vote patterns helped only a little.
- **verifiable**: good. Deaths, infections and team victory all follow from counters and comparisons.
- **fits_platform**: weak. The original uses seat adjacency (pass left and right), a seeded deck and hands. The previous variation fit the step limits but hid five kinds of information: roles, bites, night actions, the den, and private Charm feedback. The limit is 3. Some edge cases were also unstated: Mauling a wolf, when a new wolf joins the den, and the order of death versus infection.

## Problems

- P1: The wolf bloc-vote plus focus-Maul or focus-Bite policy wins about 70% at 6 players without reasoning.
- P2: The hidden Bite infection is a double swing (one human fewer, one wolf more) with no public trace, and it can win by round 2.
- P3: The round-6 timeout gives the win to any surviving wolf, so wolves can stall.
- P4: Humans have no reliable inference source. A random exposure draw decides most games, which is the lottery trap.
- P5: Balance swings strongly with player count.
- P6: Five hidden elements exceed the limit of 3 (bites counters and private Charm feedback are extra).
- P7: Edge cases are unstated: Mauling a wolf, death versus infection order, self-targeting.
- P8: Day lynches of innocents are blind coin flips, so passive, blending wolves win about half the time against humans who cannot reason from anything.

## Changes

- Replace the random exposure and the blind lynch with a Trial. The day's unique top vote-getter has their role revealed publicly and truthfully. A wolf is killed. A human is publicly cleared but takes 1 wound from the mob. (fixes: P4): Humans get a deterministic, public inference source that good voting exploits. Mis-accusations still cost something: the cleared human becomes easy to kill. Vote records then become evidence, because whoever pushed a cleared human is suspect.
- Remove the random exposure draw entirely. There are no random draws after setup. (fixes: P4): The outcome is no longer decided by whether a draw landed on a wolf.
- Make vote records public and run the Trial every day. (fixes: P1): Two wolves who bloc-vote a human get exposed. That human is revealed as cleared, so their voters (2 of whom are wolves) become the obvious suspects next day, at about 2/3 accuracy. This punishes the thoughtless bloc policy and rewards reading votes.
- Drop Bite, bites counters and infection. (fixes: P2): This removes the hidden double swing and one hidden element.
- Drop Charm and its private feedback; its inspection role moves into the public Trial. (fixes: P6): This removes another hidden element.
- Replace the wolf timeout with a ratio rule. After the Final Night (round 5), humans win if living humans are at least 2 times living wolves; otherwise wolves win. Parity at any check still wins for wolves, and 0 wolves still wins for humans. (fixes: P3, P8): Passive wolves who never Maul lose: 5 humans is at least 2x2. Stalling is not a win. Wolves must make 2 kills by round 5, or 3 for an early parity win. If one wolf is found, humans need only keep 2 alive.
- Fix the game at 7 players: 2 wolves and 5 humans. (fixes: P5): Balance no longer swings with player count, and one size can be checked by path reasoning.
- Use one wound limit of 2 for everyone: each Maul adds 1 wound and each Salve removes 1, applied in a fixed order. (fixes: P1): A kill needs both wolves on one fresh target, or one wolf on an already-wounded player. Salves are then a real guessing duel against the wolves rather than a blind lottery, because wounds are public.
- State the edge cases. A Maul may target a wolf, with normal effect. No one may target themselves. Mauls apply before Salves. The death check comes after Salves. Trial wounds can kill a player who was already wounded. (fixes: P7): This makes the rules complete and unambiguous.

## Kept from the original

- Secret wolves among humans, with wolves knowing each other.
- Wound cards that kill at a threshold and Salve cards that heal them.
- A silent Night in which every player hands one face-down card to another player.
- A Final Night that ends the game, where human survival decides it.
- Table talk with lying allowed, and team victory in which dead players still share their team's result.

## The variation's rules

PARAMETERS: 7 players, 2 wolves, wound limit 2, final round 5.

TABLE STATE: round (public, starts 0); living_wolves and living_humans (computed, used only for end checks, never announced as counts); accused (public, blank or a name); winner (blank, 'Wolves' or 'Humans').

PLAYER STATE:
- is_wolf (1 or 0): known to the player and to the other wolf.
- alive (starts 1): public.
- wounds (starts 0): public.
- cleared (starts 0): public. It becomes 1 when a Trial shows the player is human.
- revealed_role: public. Blank until death or Trial, then 'Wolf' or 'Human'.
- vote_target and votes_received: public after each vote.
- night_card and night_target: private. Never revealed.
- mauls_received and salves_received: private working counters, reset each night.

SETUP:
1. Choose 2 of the 7 players uniformly at random to be wolves; the other 5 are humans.
2. Tell each player privately whether they are a Wolf or a Human. Tell each wolf who the other wolf is.

EACH ROUND (only living players act; dead players are skipped but remain on their team):
1. Morning: round increases by 1. Publicly show every player's alive, wounds, cleared and revealed_role, and name who died last night.
2. Talk: every living player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Lying is allowed, and nothing is binding.
3. Vote: at the same time, each living player names one other living player. Abstaining and self-votes are not allowed.
4. Tally: votes_received = the number of votes each player got. Publicly show every vote_target and every votes_received.
5. Trial: if exactly one player has the most votes, that player is the accused, and their role is revealed publicly. If the top count is tied, there is no Trial today.
6. If the accused is a Wolf: they die (alive = 0, revealed_role = 'Wolf').
7. If the accused is a Human: set cleared = 1 and revealed_role = 'Human', and add 1 to their wounds.
8. Day death check: any living player with wounds >= 2 dies (alive = 0), and their role is revealed publicly.
9. Count: living_wolves = living players with is_wolf = 1; living_humans = living players with is_wolf = 0.
10. Day end check: if living_wolves = 0, the Humans win. Otherwise, if living_wolves >= living_humans, the Wolves win.
11. Wolf den: every living wolf writes one short message at the same time. These messages are shown only to living wolves.
12. Night (silent, no talk): at the same time, each living player chooses one card and one other living player as its target. A human must play Salve. A wolf plays either Maul or Salve. The card goes face-down to the target. Any player, including a wolf, may be targeted. No one may target themselves.
13. Mauls: each living player's wounds += the number of Mauls they received.
14. Salves: then each living player's wounds -= the number of Salves they received, to a minimum of 0.
15. Night death check: any living player with wounds >= 2 dies (alive = 0), and their role is revealed publicly at the next Morning.
16. Count: recompute living_wolves and living_humans.
17. Night end check: if living_wolves = 0, the Humans win. Otherwise, if living_wolves >= living_humans, the Wolves win. Otherwise, if round = 5 (the Final Night), the Humans win if living_humans >= 2 x living_wolves, and the Wolves win otherwise. If no one has won, start the next round.

NEVER REVEALED: anyone's night card or target, how many Mauls or Salves a player received (only resulting wounds and deaths are public), wolf den messages, and the role of a living player who has not been tried.

Objective: This is a team game decided by arithmetic. The game ends at the first of these: living wolves = 0, which is a Humans win; living wolves >= living humans at a day or night check, which is a Wolves win; or the end of round 5, where Humans win if living humans >= 2 x living wolves and Wolves win otherwise. Every player, alive or dead, wins if their team wins and loses otherwise. There are no draws.

Expected effect: Thoughtless policies lose:
- Passive wolves never Maul, so 5 humans stay at least 2x2 at round 5 and they lose.
- Bloc-voting wolves get a human cleared. That human's voters then include both wolves, and reasoning humans try one of them next day at about 2/3 accuracy, which costs the wolves the game, since a lone wolf rarely makes the remaining kills. Estimate about 35% for the thoughtless bloc-and-focus wolf policy against reasoning humans.
- Random-voting humans let the wolves steer Trials onto humans. Each cleared human becomes wounded and easy to kill. Estimate about 75% wolf wins against random humans.

With good play on both sides, the expected result is near 45/55, decided by reasoning:
- Wolves split their votes and mimic human voting.
- Wolves choose between killing cleared, trusted humans and uncleared ones (which thins the suspect pool).
- Wolves sometimes Salve or wound a partner to fake innocence.
- Humans read vote records and claims, and spread Salves to guess where the double Maul lands.

Talk passes both tests. The players disagree because wolves need humans to try innocents. A human who simply follows the first confident proposal can be led by a wolf into a Trial on a human, which wounds a teammate and wastes the day.

Talk is simultaneous, so no one can just echo the first speaker. There is no endgame unraveling, because the game ends on elimination, parity or a ratio, not on a highest total.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 5 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
