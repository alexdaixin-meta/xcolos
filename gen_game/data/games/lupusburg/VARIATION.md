# Variation: Lupusburg Nights II

A hidden-role deduction game for 4 to 6 players over at most 5 rounds. Peeks reveal only whether a house is 'Special' (Werewolf or Thief), so players must combine kills, thefts, lynch results and talk to tell the two apart before risking an accusation. The Werewolf scores for every round he survives.

Players: 4 to 6, best with 5

## Review of the original

Lupusburg is a hidden-role social deduction game for 4 to 8 players. Each player hides characters (one Werewolf, one Thief, the rest Townsfolk) and a chest under two houses. Each night the Thief hunts chests and the Werewolf kills a house; each day players bet coins on who is the Werewolf and vote to lynch a house. Points come from surviving characters, an intact chest and correct bets.

- **non_degenerate**: weak. The original's tapping, pointing and bag of coins do not translate to text, and bets drawn from a bag reward the draw. In the previous variation, silent hoarding of a lucky round-1 peek was the dominant policy. 'Never accuse' is never punished, and the Werewolf's result swings between about 2 and about 9 on whether a blind peek hits him early.
- **skill_sensitive**: bad. In the previous variation, about 41-42% of games had someone find the Werewolf with a blind round-1 peek. A Townsfolk player found the Thief in 31-34% of games. Either find was worth +6, equal to the whole base score, so the luck of the deal outweighed reasoning.
- **headroom**: good. Reading kill patterns, theft announcements, vote patterns and lies in talk gives a strong player room to improve. A weak player still keeps house and chest points.
- **reasoning_dependent**: weak. The hidden state is rich, but the previous variation let a single uninformed peek replace inference. Once found, the accuser had no further need to reason or persuade.
- **verifiable**: good. All scoring is arithmetic on houses, chests, accusations and lynch outcomes tracked by the engine.
- **fits_platform**: good. Once the night actions are made simultaneous secret choices, the game is text-only and needs no board. Five rounds and about 11 steps per round fit the limits.

## Problems

- P1: A blind round-1 peek that lands on the Werewolf or Thief house gives a confirmed, risk-free accusation worth as much as a whole game's base score. This is the lottery trap.
- P2: Accusation rewards (up to 6) exceed the base score (6), so house and chest play barely matters next to one lucky hit.
- P3: A finder gains by hiding what he knows: publicising it raises k and cuts his payout, so talk carries no true information and the others have nothing to judge.
- P4: The Werewolf seat is itself a deal lottery. Found early he ends near 2; unfound he ends near 9. Whether he is found depends mostly on blind peeks, not on his deception.
- P5: Accusing is safe once a peek confirms the target, so accusation choices need no reasoning about evidence.

## Changes

- Peeks never reveal the exact role. A peek reports only 'Townsfolk' or 'Special', where Special means Werewolf or Thief. The Thief's owner, knowing his own role, can of course deduce that a Special house that is not his own is the Werewolf. (fixes: P1): Finding a Special house shows only that its owner is one of two roles. To tell Werewolf from Thief, players must use theft announcements, kill choices, lynch results, votes and talk.
- No accusations may be made in round 1. (fixes: P1): A round-1 peek can never be cashed in at once. By round 2, more public evidence exists to tell the roles apart.
- A correct accusation scores max(1, 5 - r - (k - 1)), which is 3 at most, in round 2. A wrong accusation scores -3. (fixes: P2, P5): A coin-flip accusation between Werewolf and Thief has expected value 0. The best possible hit (3) is half the base score of 6, so houses and chests still matter.
- In the round the Werewolf house is lynched, every player who voted for it scores +2. (fixes: P3): A finder gains by persuading others to vote with him. Listeners must judge whether a claim of 'I found Special at X' is honest, and whether it points at the Werewolf or the Thief.
- The Werewolf's owner scores +1 for each round that ends without the Werewolf house being lynched, plus +2 if the Werewolf house is alive at the end. This replaces the flat +5. (fixes: P4): His score grows steadily with every round he survives through deception. Being found early costs a few points rather than everything, and the growth is driven by inference, not blind peeks.

## Kept from the original

- Two houses per player, with hidden characters and a hidden chest
- One Werewolf who kills a house each night and one Thief who hunts for chests
- Burgomaster-style private peeks at other players' houses
- Day discussion followed by a vote to lynch one house
- Bets (accusations) on who holds the Werewolf, rewarding early correct suspicion
- The Werewolf wins alone if he slaughters every other character
- Points for living characters, a surviving chest and correct bets

## The variation's rules

SETUP
- Seats are numbered 1..N, where N is 4 to 6.
- Each player owns two houses, Left and Right. A house is named by owner and side.
- The engine secretly deals characters. Exactly one house holds the Werewolf and exactly one holds the Thief. They belong to two different players, each in a random one of that player's houses. Every other house holds a Townsfolk.
- The Werewolf's owner and the Thief's owner have no chest. Every other player has one chest, hidden under a randomly chosen one of his two houses.
- Each player privately learns the characters under his own two houses and, if he has one, his chest side.
- Everyone knows these dealing rules.
- Each player starts with one unused accusation.
- The game lasts at most 5 rounds.

EACH ROUND, in order (r is the round number):

1. NIGHT (simultaneous). Every player secretly names one living house belonging to another player.
   - The Werewolf's owner may instead name his own other house if it is alive. He may never name the Werewolf house.
   - Players with no living houses still take part.

2. PEEKS. Every player except the Werewolf's owner privately learns the result for the house he named.
   - The result is 'Special' if it holds the Werewolf or the Thief, and 'Townsfolk' otherwise.

3. THEFT. This applies only if the Thief house is alive, the Thief has not yet stolen, and the Thief's owner has not been correctly accused as the Thief.
   - If the house the Thief's owner named is its owner's chest house, the Thief steals that chest and the Thief's owner privately learns 'chest stolen'. Otherwise he privately learns 'no chest'.
   - A steal is announced publicly as 'a chest was stolen from player X', without naming the Thief.
   - The Thief steals at most once per game.

4. KILL. The house named by the Werewolf's owner is removed.
   - Its owner and side are announced publicly, but its character is not.
   - The Werewolf's owner privately learns its character.
   - Removing a house never removes a chest. If the removed house is the Thief house, the Thief loses any stolen chest, it returns to its victim, and the Thief can no longer steal.

5. SLAUGHTER CHECK. If no living Thief or Townsfolk house remains, the Werewolf's owner wins alone and the game ends.

6. TALK (simultaneous). Every player writes one short message without seeing the others' messages. All messages are then shown to everyone. Messages may be true or false and nothing said is binding.

7. VOTE AND ACCUSE (simultaneous). Every player, including those with no living houses, names one living house to lynch.
   - From round 2 on, a player who still holds his accusation may also, in the same step, name one other player and one role (Werewolf or Thief) as that player's character. This uses up his accusation.
   - No accusations may be made in round 1.

8. ACCUSATION RESULTS.
   - For each role, let k be the number of players who correctly named that role's owner this round. Each correct accuser scores max(1, 5 - r - (k - 1)). Each wrong accuser scores -3.
   - All accusations made this round (accuser, target, role) are announced publicly, but whether they were correct is not.
   - If the Thief's owner is correctly accused as the Thief, he loses any stolen chest, it returns to its victim, and he can no longer steal.

9. LYNCH. The house with the most votes is removed. If two or more houses tie for most votes, nothing is removed.
   - It is announced only whether the lynched house was 'the Werewolf' or 'not the Werewolf'.
   - If the Thief house is removed, the Thief loses any stolen chest, it returns to its victim, and he can no longer steal.
   - If the Werewolf house was lynched, every player who voted for it scores +2.

10. WEREWOLF ROUND POINT. If the Werewolf house was not lynched this round, the Werewolf's owner scores +1.

11. END CHECK.
   - If the Werewolf house was lynched, the game ends and is scored.
   - Otherwise, if no living Thief or Townsfolk house remains, the Werewolf's owner wins alone.
   - Otherwise, if this was round 5, the game ends and is scored.
   - Otherwise a new round begins.

FINAL SCORING (when the game ends by lynch or after round 5). Each player adds the following to the points already earned in play (accusation results, lynch-vote bonuses, Werewolf round points):
(a) 2 points per living house he owns;
(b) 2 points if he has a chest and it is not currently held by the Thief;
(c) the Thief's owner: +2 if he still holds a stolen chest;
(d) the Werewolf's owner: +2 if the Werewolf house is alive.

Objective: If at a slaughter check or the end check no living Thief or Townsfolk house remains, the Werewolf's owner is the sole winner. Otherwise the player with the highest total wins. If totals tie, the tied player with the higher accusation points wins. If still tied, the one with more living houses wins. If still tied, the game is a draw.

Expected effect: A blind round-1 hit now yields only 'this owner is Werewolf or Thief'. It cannot be cashed in round 1, and a guess between the two roles has expected value 0 (+3 or -3). Under intended play, an uninformed round-1 choice should decide the winner in well under 25% of games (estimated around 10%). Cashing in needs extra evidence: who reports no chest, which houses the Werewolf spares or kills, the timing of theft announcements, and lynch results.

Talk passes both tests.
- Reasoning: finders want to publicise a Special house to collect the +2 lynch-vote bonus.
- Conflict: only one player can win, and the roles want different outcomes. The Werewolf and Thief want to redirect votes and misname each other. Correct accusers want few co-accusers, since k cuts their payout. Townsfolk want the Werewolf lynched but not at the cost of their own houses.
- A player who simply follows a confident claim may be voting for the Thief's house, or accusing on a lie, and lose 3.

The Werewolf's score grows by 1 per round he survives, plus 2 if he is alive at the end. Being caught early costs a few points rather than everything, so his result rewards sustained deception over the deal.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 5 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
