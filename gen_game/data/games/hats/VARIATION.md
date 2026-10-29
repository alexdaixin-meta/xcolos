# Variation: Ripening Hats

Players secretly pick hats from a tea table each round. Each colour's value grows while it is left alone and resets when taken, and two players reaching for the same colour both get nothing. Each player has a secret favourite colour worth +3 per hat. Nobody sees who took what, only which colours were taken or fought over.

Players: 3 to 4, best with 4

## Review of the original

Hats is a 2-4 player card game. Players swap numbered hat cards with a shared tea table to collect types. A type scores according to its position on the table. A secret favourite type, revealed from the last card in hand, adds a bonus, black hats score 1, and a cookie goes to the player with the most distinct types.

- **non_degenerate**: bad. In the previous variation favourites were all different, so 'always collect my favourite' was never contested unless a rival paid his own round to block it. Pushes needed 2 votes on one colour and never fired under sensible self-interested play. The thoughtless policy 'collect and push favourite' therefore scored 12*(start position+3) and won whenever its favourite started high. The random start gave a dealt edge of up to 48 points. Always Black (12) loses, and always Red loses unless Red is your favourite, but one fixed policy plus a lucky deal decides most games.
- **skill_sensitive**: bad. With everyone playing the obvious strategy, the 4-player totals were 96/84/72/60, set purely by the random table order. Push coalitions shifted at most 1 point per hat and could be countered by any tying vote, so a better player could not reliably overcome a bad deal.
- **headroom**: weak. A weak player scores easily, since any uncontested colour pays at least 4. A strong player has little to improve: collect favourite every round is near-optimal, and the remaining levers (coalitions, sacrificial blocks) rarely change the winner.
- **reasoning_dependent**: bad. Per-colour hat counts were announced every round, so every favourite was public after round 1. The one hidden element collapsed and nothing was left to infer. The original card game has more hidden hand information, but the variation threw it away.
- **verifiable**: good. All scoring is arithmetic on positions, counts and bonuses. No judge is needed.
- **fits_platform**: weak. The game is turn-based, text-only and 12 rounds long. However, 6 hat counters per player across 4 players plus positions, favourites and scores exceeds 33 attributes against a limit of 20. The push unique-max-and-swap, the 6-way collision check and the cookie unique-max over players push the step count beyond the honest estimate and need calc workarounds. The original card game (42-card deck, hands, tableaux, partner exchanges) is far beyond the limits.

## Problems

- P1: Start-order luck. The random table order gives a favourite up to 4 points per hat over another, which decides the winner when everyone plays well (lottery trap).
- P2: Favourites become public after round 1 because per-colour collections are announced with attribution, so there is nothing to infer.
- P3: Pushes never fire under sensible play (each player votes a different colour, the threshold is 2), so the scoring order is frozen and push-related reasoning is moot.
- P4: Collecting your favourite is a free, uncontested default. No decision is made and the near-dominant thoughtless policy wins.
- P5: The black hat is dominated and exists only as a cookie token. The cookie needs per-player per-kind flags that blow the attribute budget.
- P6: The attribute count (more than 33) and steps (unique-max, swap, cookie) exceed platform limits, and the stated complexity was wrong.
- P7: Because favourites were known and uncontested, talk had little to work on beyond fragile push coalitions.

## Changes

- Replace the random positional order with a public VALUE for each colour. All colours start at 2. A colour gains +1 each round it is not successfully collected (capped at 7) and drops back to 1 when someone collects it. (fixes: P1): Every colour starts identical, so no favourite is dealt an advantage. The table is shaped entirely by what players do, like the original board, where taking a card changes what sits there.
- Replace pushing with the growth/reset rule above. Leaving a colour alone is now the way to 'push' it up, and taking it resets it. (fixes: P3): Value changes now fire every round from players' own choices. The question becomes timing: let your favourite ripen, or cash it now before someone else takes it?
- Keep choices and scores private. Each round announce only, per colour, whether it was collected, contested or untouched, plus how many players took Black. Never announce who took what. Each player sees only their own score until the end. (fixes: P2): Favourites stay genuinely hidden. Players must infer from aggregate patterns which colours someone is protecting and which are free to take, and whether a contest was a block or an accident.
- Make the favourite bonus position-independent (+3 per favourite hat, added privately). Let colour values grow so that ripe colours, including other players' favourites, are worth taking at up to 7. (fixes: P4): Your favourite is worth value+3 to you but only its value to rivals. If you let it ripen, an opportunist may take it at 7. If you take it every round, you earn only 1+3=4 per round while others harvest the ripening colours. 'Always favourite' becomes beatable and every pick is a timing and prediction decision.
- Contests give nothing and do not reset the colour, which keeps growing. The game uses 3-4 players, so 4 or 5 colours compete for a handful of pickers. (fixes: P4): This creates a chicken game over the ripest colours. Grabbing the top value collides with anyone else who reads the table the same way, so players must predict rivals rather than follow a fixed rule.
- Black is always available for a guaranteed 1 point. The cookie and per-kind tracking are dropped. (fixes: P5): Black becomes a real safe fallback when a collision is likely, especially in contested rounds, instead of a cookie token. Removing per-kind flags cuts about 24 attributes.
- Track only 5 colour values, 5 per-round chooser counts, and per player a private score and a private favourite. Step count is recounted honestly. (fixes: P6): This totals 19 attributes for 4 players and about 10 steps, inside the limits.
- Keep simultaneous one-message talk before each choice. (fixes: P7): Players now disagree about who gets the ripe colours. Claims such as 'I'm taking Blue' are cheap bluffs meant to scare others off. Promises to leave someone's favourite alone can be broken, and the aggregate outcome partly reveals who broke them.

## Kept from the original

- Hat types of different colours collected from a shared tea table whose values change as hats are taken
- A secret favourite type revealed at the end that boosts that type's hats
- Black hats as a guaranteed 1-point fallback
- Collision on the same hat: you cannot both take it
- Highest total wins, with 3-4 players, as in the original's multiplayer modes

## The variation's rules

SETUP. There are 5 hat colours, listed in this fixed order: Red, Blue, Green, Yellow, Purple. Each colour has a public value, and all five start at 2. Each player is dealt a secret favourite colour at random, all different; only that player knows it. Every player has a private score starting at 0, which only that player can see.

EACH ROUND (12 rounds):
1. Announce to everyone: the round number and the current value of each of the 5 colours.
2. Talk: everyone writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.
3. Choice: everyone simultaneously and secretly chooses one of Red, Blue, Green, Yellow, Purple or Black.
4. Collection. A player who chose Black adds 1 to their score. A player who chose a colour that no other player chose this round collects it: they add that colour's current value to their score, plus 3 more if it is their favourite. A colour chosen by two or more players is contested, and none of them gains anything.
5. Announce to everyone, without naming players: for each colour, whether it was COLLECTED (exactly one chooser), CONTESTED (two or more) or UNTOUCHED (no one), and how many players chose Black. Individual choices and scores are never announced.
6. Value update. Each colour that was collected this round resets to 1. Each colour that was contested or untouched gains +1, to a maximum of 7.
7. After round 12 the game ends.

END. All favourites and scores are revealed.

Objective: The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw.

Expected effect: No colour starts ahead, so the deal only decides what each player wants, not who leads. Each round is a timing and prediction problem.

Taking your favourite every round yields only 4 per round. Letting it ripen risks an opportunist sniping it at up to 7. Grabbing the ripest colour collides with anyone else who reads the table the same way. Black is the safe 1.

Players must infer from the unattributed COLLECTED/CONTESTED patterns which colours rivals are protecting, which are free, and whether a contest was a block or a coincidence.

Simple policies all lose to some play:
- Always Black scores 12 and loses to almost anyone.
- Always one fixed colour collides with that colour's fan or gets 1 per round.
- Always favourite scores about 49 and loses to a player who alternates between their favourite at 2-3 and an unclaimed colour at 6-7.
- Always highest value is predictable. It collides with copycats and can be pre-empted, and it often cashes only 2-3 per round.

Talk passes both tests. Players disagree over who gets each ripe colour, since only one can collect it and only one player wins. A player who just follows a rival's claim ('I'm taking Purple, stay off it') hands that rival 7 points. A player who honours a pact to leave someone's favourite alone may watch that player snipe theirs. Claims can be bluffs, and the anonymous outcome only partly exposes who lied.

The winner rule is a race, not a cooperation dilemma, so endgame unravelling does not apply. The last rounds become a sharp chicken game over the ripest colours.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
