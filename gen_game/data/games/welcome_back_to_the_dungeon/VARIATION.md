# Variation: Dungeon Dare

Three players share one adventurer. On your turn you secretly draw a monster and either hide it in the dungeon, remove a piece of equipment, or pass. The last player left must run the dungeon plus 2 unknown cards from the deck. Survive for 2 points. If the runner fails, the passers who helped stock the dungeon score instead.

Players: 3 to 3, best with 3

## Review of the original

Welcome Back to the Dungeon is a 2-4 player push-your-luck bluffing game. Players take turns drawing monsters and either secretly adding them to a shared dungeon or removing one of a shared adventurer's equipment tiles. Each player stays in or passes, and the last player left must run the dungeon with what remains. Two successful runs win, and two failures eliminate a player.

- **non_degenerate**: bad. In the previously built variation, always taking the last option (stripping equipment and never passing) won 88% of decided matches from seat 1 and 92% from seat 2. Always taking the first option (passing) lost 60 of 60 games. Removing an item also removed the drawn monster, so a non-passer kept the dungeon small. Random opponents stripped items and passed early, which handed the stubborn player near-empty runs. Seat results against random seats were also uneven (seat 1 won 12, seats 2 and 3 won 24 each).
- **skill_sensitive**: weak. In the original, reading opponents' passes and tracking which equipment is gone matters. In the tested variation a fixed policy beat thinking, so skill was swamped by a structural exploit. Deck order matters a lot in short runs.
- **headroom**: good. Card counting over a 13-card deck, inferring opponents' secret additions from their behaviour, and timing the pass leave plenty of room to improve. A weak player can still win a run.
- **reasoning_dependent**: good. The dungeon is face-down, and each player knows only the cards they handled. Whether to stay in depends on inferring what others added and whether they are about to pass.
- **verifiable**: good. Damage, HP, successes and failures are pure arithmetic on revealed cards.
- **fits_platform**: weak. The game is text-only and turn-based. However, the original has player-chosen adventurers, elimination with open-ended length, and a reshuffle plus a draw in the same moment. Each turn must be reduced to one choice and one random event.

## Problems

- P1: Never passing (always stripping or always adding) is a winning policy, because a run rarely faces real danger. Removing an item also removed the monster, and nothing outside the dungeon threatens the runner.
- P2: Passing earns nothing, so early passing is pure loss and later passing has no positive payoff. The trade-off between staying and leaving is lopsided.
- P3: There are seat imbalances: a fixed first player and a winner-chooses-adventurer rule give persistent edges.
- P4: Elimination and 'two successes' make length open-ended and can leave a player idle. One lucky run decides a lot.
- P5: Platform limits: a turn must contain at most one random event and few choices. The original reshuffles and draws in the same step and has several adventurers with different kits.

## Changes

- The runner also fights the top 2 cards still in the deck, revealed at run time. The adventurer's base HP is lowered to 3, so a run with no equipment is almost always lethal. (fixes: P1: Never passing (always stripping or always adding) is a winning policy.): Every run now carries hidden danger, and stripping all the equipment then running is suicide. A player who never passes ends up running a stripped dungeon and fails.
- Points replace successes and eliminations. A successful runner gains 2 points. A failed runner loses 1 point (not below 0). When the runner fails, each player who passed earns 1 point, but only if they added at least one monster to that dungeon. (fixes: P2: Passing earns nothing.): Passing at the right moment now pays: build a deadly dungeon, then leave. Passing immediately pays nothing, so always-pass sits at 0 and loses. Running pays more than passing, so someone still wants to stay in.
- The leader (first to act) rotates seat by seat each dungeon. There is one fixed adventurer kit. (fixes: P3: There are seat imbalances.): This removes the persistent first-seat effect and the winner's choice of adventurer.
- The first to 4 points wins, checked after each run, with a cap of 40 turns. At the cap the highest total wins, and a tie for highest is a draw. There is no elimination. (fixes: P4: Elimination and 'two successes' make length open-ended.): Gives a bounded length, keeps all players active, and one run is not decisive.
- One engine round is one player's turn. The only random event is the shuffle at the start of a new dungeon. Drawing takes the top card of the already-shuffled deck. (fixes: P5: Platform limits.): This fits the limit of one random draw per round and a flat step list.
- A short simultaneous message phase is held each turn before the active player acts. (fixes: P2: Passing earns nothing.): Players disagree about who should be left holding the dungeon. Bluffing about what you added ('only goblins in there') is the heart of the original.

## Kept from the original

- A shared adventurer with equipment that adds HP or defeats monster types.
- Drawing a monster in secret, then adding it face-down to the dungeon or removing equipment.
- Passing out of the bidding; the last player left must run the dungeon.
- Revealing the dungeon card by card, with equipment cancelling monsters and damage compared to HP.
- Bluffing and inference about the face-down dungeon from what others did.

## The variation's rules

COMPONENTS.

Monster deck of 13 cards (name: strength):
- Goblin 1 (x2)
- Skeleton 2 (x2)
- Orc 3 (x2)
- Vampire 4 (x2)
- Golem 5 (x2)
- Lich 6 (x1)
- Demon 7 (x1)
- Dragon 9 (x1)

Adventurer base HP: 3.

Equipment (4 items, all present at the start of each dungeon):
- ARMOR: +4 HP.
- SHIELD: +3 HP.
- TORCH: defeats every monster of strength 3 or less.
- SPEAR: defeats every monster of strength 7 or more.

Each player has a point total starting at 0.

SEATS AND TURNS.
Seats are 1, 2 and 3. The game is played as a series of turns, at most 40. Turns are grouped into dungeons.

STARTING A DUNGEON.
1. At the start of each dungeon, shuffle all 13 monsters into a face-down deck. This shuffle is the only random event.
2. Return all 4 items to the adventurer.
3. Empty the dungeon pile and all players' set-aside piles.
4. Mark all three players as IN, and clear every player's 'added' mark.
5. The leader acts first. Dungeon 1 is led by seat 1, dungeon 2 by seat 2, dungeon 3 by seat 3, dungeon 4 by seat 1, and so on.
6. Turns then pass in seat order (1, 2, 3, 1, ...), skipping players who are OUT.

A TURN (for the active player, who is IN).
(a) Forced pass check: if the deck holds 2 or fewer cards, the active player must PASS this turn. Skip to (d).
(b) Draw: the active player privately looks at the top card of the deck. Only they see it.
(c) Talk: every player, in or out, writes one short message at the same time without seeing the others. Then all messages are shown to everyone. Messages bind no one and may be lies.
(d) Action: the active player chooses one option from this list, in this order, offering only the legal ones.
    - PASS: you become OUT for this dungeon. The card you drew, if any, goes back on top of the deck, unseen by others.
    - ADD: put the drawn monster face-down on the dungeon pile, and mark yourself as 'added' for this dungeon.
    - SACRIFICE_ARMOR, SACRIFICE_SHIELD, SACRIFICE_TORCH, SACRIFICE_SPEAR: available only for items still present. Remove that item from the adventurer for this dungeon. Put the drawn monster face-down in your own set-aside pile; it is out of play and seen only by you. This does NOT mark you as 'added'.
(e) Announcement: everyone learns which option was chosen, which item was removed if any, and how many cards are in the dungeon pile. Nobody learns which monster was drawn.
(f) If exactly one player is still IN, that player becomes the RUNNER and the run happens now (see below). Otherwise the turn passes to the next IN player.

THE RUN.
1. The runner's HP = 3, +4 if ARMOR remains, +3 if SHIELD remains.
2. Reveal every card in the dungeon pile, then the top 2 cards of the deck. All of these are the monsters faced.
3. Each monster is defeated with no damage if TORCH remains and its strength is 3 or less, or if SPEAR remains and its strength is 7 or more. Otherwise it deals damage equal to its strength.
4. If total damage is less than HP, the run SUCCEEDS: the runner gains 2 points.
5. Otherwise the run FAILS:
    - The runner loses 1 point (never below 0).
    - Every OUT player who is marked 'added' for this dungeon gains 1 point.
6. All revealed cards are announced. The dungeon ends, and the next turn starts a new dungeon.

END OF GAME.
- After any run, if any player has 4 or more points, the game ends.
- The game also ends after turn 40, even mid-dungeon. An unfinished dungeon is not scored.

Objective: When the game ends, the player with the most points wins. If two or more players tie for the most points, the game is a draw.

Expected effect: Always passing never adds a monster, so it can never score and loses. Always adding or always sacrificing never passes, so that player is always the runner. Always-sacrificing strips its own equipment and so runs nearly bare against the dungeon plus 2 deck cards, failing at once. Always-adding still runs whatever the opponents built and stripped, which is lethal against random or competent opponents. Both lose points while the passers score. The good line is to stock the dungeon with a monster you know, strip the item that would have beaten it, and pass before you are stuck as runner. Alternatively, stay in when your private knowledge says the dungeon is survivable. Players disagree about who should be left holding the dungeon, and each wants the others to believe it is safe (to keep them in) or deadly (to make them pass while they themselves stay and collect 2 points). A player who simply believes 'it's only goblins' and stays in can end up running a Golem-and-Lich pit for -1 while the liar scores. Rotating the leader evens out seats, and the target of 4 points needs several good decisions rather than one lucky run.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
