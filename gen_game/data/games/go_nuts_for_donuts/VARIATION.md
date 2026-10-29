# Variation: Go Nuts for Donuts: Secret Budget

Four players pick donuts simultaneously for 10 rounds from a fixed row of five, and any donut picked by two or more players is discarded. The two best donuts, Glazed and Jelly, need limited premium picks. Each player secretly divides those picks between Glazed and Jelly at the start, so reading rivals' hidden budgets is the key skill.

Players: 4 to 4, best with 4

## Review of the original

Go Nuts for Donuts is a 2-6 player simultaneous-selection game. Each round every player secretly picks one of N+1 face-up donuts. A donut chosen by exactly one player goes to that player, and a donut chosen by two or more is discarded. Some donuts carry action powers, and the most points when the deck runs out wins.

- **non_degenerate**: good. Neither 'always the top donut' nor 'always the cheapest' is safe, because two players on the same card both get nothing. No seat moves first, since the reveal is simultaneous. Choices decide every allocation.
- **skill_sensitive**: weak. The shuffled deck decides which donuts appear and when. Action cards (steal, draw) add swingy luck. Most rounds are an anti-coordination guess in which a good reader gains a modest edge over many rounds.
- **headroom**: good. Reading which donut rivals will crowd onto and taking the uncontested one keeps rewarding improvement. A weak player still picks up leftovers.
- **reasoning_dependent**: weak. The core is predicting rivals' simultaneous picks, which is genuine opponent modelling. However, everything on the table is face-up and scores are public, so there is no private state to infer. Card-specific powers and set scoring reward rules knowledge more than inference.
- **verifiable**: good. Allocation and scoring are pure counting: lone chooser takes the card, and points are summed.
- **fits_platform**: weak. Simultaneous polls fit. A shuffled deck with refills, many distinct card powers (steal, draw, manipulate) and set-based values would blow past the step and attribute limits.

## Problems

- Too many distinct card powers and set rules to build within 20 steps and 20 attributes.
- A shuffled deck makes the offer each round random, adding luck without adding reasoning.
- No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history.
- BUILD FAILURE in the previous variation: the secret split was overwritten after the poll. Every seat ended with glazed_picks 0 and jelly_picks 6, which broke the void test (R7), the void-collision rule (R8), the lone-Glazed payout (R10) and the pick accounting (R16). The cause was a second, unconditional step that reset the stored picks. Storing two mutable pick counters derived from the answer invited exactly this overwrite.
- The previous variation carried redundant table constants (lone_chooser_count, donut_collected_increment, pick_use_per_choice) that added attributes and places for the builder to go wrong.

## Changes

- A fixed row of five donuts every round: Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1. There are no action cards and no deck. (fixes: Too many distinct card powers and set rules to build within 20 steps and 20 attributes.): Keeps the 'pick one of N+1, collisions discard' core while fitting the limits. Removing the random offer means skill, not the shuffle, decides the game.
- No random draws at all: the same five donuts are offered in all 10 rounds. (fixes: A shuffled deck makes the offer each round random, adding luck without adding reasoning.): Luck no longer swamps reading opponents.
- Each player has 6 premium picks for the whole game, the only way to choose Glazed or Jelly. Before round 1 each player secretly sets how many are Glazed (G). The rest (6 - G) are Jelly. Players see each other's choices each round but never each other's G. (fixes: No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history.): Creates one strong hidden element. Players must infer from rivals' play how many Glazed or Jelly picks each still holds, and plan their own budget over 10 rounds.
- Store only the answer split_g plus the counters glazed_used and jelly_used. There are no glazed_picks or jelly_picks attributes. A Glazed choice is void exactly when glazed_used >= split_g, and a Jelly choice is void exactly when jelly_used >= 6 - split_g. split_g is written once by the setup poll, and no other step ever writes it. glazed_used and jelly_used start at 0 and only ever increase by 1 on a non-void choice of that donut. The setup poll offers exactly the options 0 to 6, so there is no default or fallback value. (fixes: BUILD FAILURE in the previous variation: the secret split was overwritten after the poll. Every seat ended with glazed_picks 0 and jelly_picks 6, which broke the void test (R7), the void-collision rule (R8), the lone-Glazed payout (R10) and the pick accounting (R16). The cause was a second, unconditional step that reset the stored picks. Storing two mutable pick counters derived from the answer invited exactly this overwrite.): The overwritten-picks bug came from a second operation resetting derived counters. With nothing derived stored, nothing remains to reset. Void is computed directly from the answer and the usage counters.
- Drop the table constants lone_chooser_count, donut_collected_increment and pick_use_per_choice. Write the literal numbers (1) into the rules. (fixes: The previous variation carried redundant table constants (lone_chooser_count, donut_collected_increment, pick_use_per_choice) that added attributes and places for the builder to go wrong.): Fewer attributes and fewer indirections for the builder to misread.
- Add one simultaneous message per player before each round's choice. (fixes: No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history.): Lets players claim, bluff about remaining picks and try to steer rivals off a donut. Interests conflict because only one player can take each donut and only one player wins.

## Kept from the original

- Simultaneous secret selection of one donut from a row of N+1.
- A donut chosen by exactly one player is taken. A donut chosen by two or more is discarded and nobody gets it.
- Donuts of different point values, with the most points winning and more donuts as the tie-break.
- The bluffing and second-guessing of 'will they all go for the big one?'

## The variation's rules

PLAYERS AND DONUTS. Exactly 4 players. Every round the same five donuts are offered: Glazed (9 points), Jelly (6 points), Cruller (4 points), Sprinkle (2 points), Plain (1 point). There are no cards, deck or random events.

STARTING STATE. Every player starts with score 0, donuts 0, glazed_used 0, jelly_used 0. The game lasts exactly 10 rounds.

SECRET SPLIT (once, before round 1). Each player has 6 premium picks for the whole game. All players are asked at the same time: 'How many of your 6 premium picks are Glazed picks?' The options are exactly the whole numbers 0, 1, 2, 3, 4, 5, 6. The answer is stored as that player's split_g and is visible only to that player. That player then has split_g Glazed picks and (6 - split_g) Jelly picks. split_g is set by this poll only and is never changed by any later step. No step resets glazed_used or jelly_used except as stated below.

EACH ROUND:
1. TALK. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.
2. CHOOSE. All players choose at the same time one of: Glazed, Jelly, Cruller, Sprinkle, Plain. Before choosing, each player is privately reminded of their own Glazed picks left (split_g - glazed_used) and Jelly picks left (6 - split_g - jelly_used).
3. VOID CHECK. A player's choice is void if and only if (a) they chose Glazed and glazed_used >= split_g, or (b) they chose Jelly and jelly_used >= 6 - split_g. Every other choice is not void. Cruller, Sprinkle and Plain are never void.
4. COUNT. For each donut, count how many players made a NON-VOID choice of it. Void choices are not counted for any donut.
5. AWARD. For each donut, if exactly 1 player made a non-void choice of it, that player adds the donut's points to their score and adds 1 to donuts. If 2 or more players made a non-void choice of it, it is discarded and none of them gains anything for it. A void choice gains 0.
6. USE PICKS. Every player who made a non-void Glazed choice adds 1 to glazed_used. Every player who made a non-void Jelly choice adds 1 to jelly_used. This happens whether the donut was won or discarded. A void choice uses nothing.
7. REVEAL. Everyone is shown every player's choice (marked VOID if void), what each player gained this round, and all scores and donut counts. Nobody's split_g is ever shown.
8. END CHECK. After round 10 the game ends.

Objective: After round 10, the player with the highest score wins. If several are tied on score, the one among them with the most donuts wins (rank value = score x 100 + donuts). If players are still tied on both, the game is a draw among them.

Expected effect: Players must budget 6 premium picks across 10 rounds and guess when rivals will spend theirs. Each rival's Glazed/Jelly split is hidden but can be inferred from what they have chosen and when their choices turned VOID. Crowding the Glazed donut wastes picks, while slipping into an uncontested Jelly or Cruller pays.

Talk passes both tests. Players disagree because each donut can go to only one player and only one player wins. A message like 'I'm taking Glazed, take Jelly' is self-serving, and a player who follows it may hand the speaker 9 points while burning a Jelly pick on a collision. Players can also bluff about their remaining Glazed picks to scare rivals off.

Simple policies all lose to readers:
- Always Glazed (split 6) collides with anyone else doing it and is void for the last 4 rounds.
- Always Cruller earns 0 once anyone contests it.
- Always Plain caps at 10 points.
- Random play scatters picks into collisions.

The game has no luck and no seat order, so reading rivals decides it.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
