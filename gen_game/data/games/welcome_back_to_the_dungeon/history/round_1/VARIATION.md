# Variation: Back to the Dungeon: Single Delve

Three or four players share one adventurer and take turns drawing monsters secretly. Each drawn monster goes into the dungeon or is discarded at the cost of a piece of equipment, or the player passes. The last player in runs the dungeon. Two successful runs win, two failures eliminate.

Players: 3 to 4, best with 3

## Review of the original

Welcome Back to the Dungeon is a 2-4 player push-your-luck bluffing game. Players share one adventurer and take turns drawing monsters secretly. Each drawn monster is either added face-down to a shared dungeon, or set aside by removing one of the adventurer's equipment tiles. A player may instead pass. The last player still in must run the dungeon with the remaining equipment: two successful runs win, and two failures eliminate.

- **non_degenerate**: good. No simple policy wins. Always passing first means you never run, so you can never reach two successes and only win if both rivals are eliminated. Always adding means you are often left as the runner of a dungeon packed with your own monsters. Always sacrificing strips the adventurer to base HP, which fails almost any run. Passing, adding and sacrificing each change who runs and with what. One structural edge exists: the winner of a run picks the next adventurer, which snowballs.
- **skill_sensitive**: weak. Reading opponents' draws and timing your pass matter a lot. However, deck order decides which monsters reach which player. A short game ends after two runs, so a lucky early run can decide it. Some of the four adventurers' special tiles also swing results heavily.
- **headroom**: good. Strong players track the dungeon size against what they know they added, infer what others removed or added from their choices, and time their pass. Weak players still score by running easy dungeons. The game is not solved.
- **reasoning_dependent**: good. Each player knows only the monsters they personally drew. The dungeon's contents must be inferred from its public size, the visible equipment loss and the other players' choices to continue or pass.
- **verifiable**: good. Damage is a sum of monster strengths minus those the remaining equipment defeats, compared with HP. A few original tiles (for example, naming a monster type, or once-per-run effects) need extra rules, but these are still arithmetic.
- **fits_platform**: weak. The game is turn-based and text-only. But the bidding phase has variable length, game length is unbounded, there are four adventurers with six unique and partly special tiles each, and the informal table talk that drives the bluffing has no structure. All of these need simplifying to fit the step limits.

## Problems

- Four adventurers with six unique, partly special-ability equipment tiles is too much state and too many rule exceptions for the complexity limits.
- Game length is unbounded: dungeons repeat until someone has two successes or is the last one standing, with no round cap.
- The winner of a run picks the next adventurer, a rich-get-richer seat advantage that also fixes who leads the next bidding.
- Bluffing about what you drew is the heart of the game, but there is no structured way to communicate, so the platform would lose the claim-and-read element.
- Which information is public (dungeon size, remaining equipment, deck size) is implicit in the physical game and must be stated for a text engine.
- Deck luck can decide a short game when no fallback or tiebreak exists.

## Changes

- Use one fixed adventurer: base HP 3 and five equipment items (Armor +5 HP, Shield +3 HP, Torch defeats strength 3 or less, Holy Water defeats Vampires and the Lich, Dragon Spear defeats the Dragon). Use a fixed 13-card monster deck with strengths 1-9. (fixes: Four adventurers with six unique, partly special-ability equipment tiles is too much state and too many rule exceptions for the complexity limits.): Keeps the identity of equipment that adds HP or defeats monster types, while cutting rule exceptions to a single damage calculation.
- One round is one player's turn. Cap the game at 40 rounds, with a tiebreak at the cap: most successes among surviving players, then fewest failures, otherwise a draw. (fixes: Game length is unbounded: dungeons repeat until someone has two successes or is the last one standing, with no round cap.): Gives a bounded, buildable loop and a result decided by arithmetic even if no one reaches two successes.
- No adventurer choice. The first player of each new dungeon is the next surviving player clockwise from the previous runner. (fixes: The winner of a run picks the next adventurer, a rich-get-richer seat advantage that also fixes who leads the next bidding.): Removes the snowball and spreads the leading position evenly.
- Each round, before the active player acts, every surviving player writes one short message at the same time. All messages are then shown. (fixes: Bluffing about what you drew is the heart of the game, but there is no structured way to communicate, so the platform would lose the claim-and-read element.): Gives bluffing a structured channel: claims about what was added or removed, which others must test against public facts.
- Announce each round the dungeon size, the remaining equipment, the deck size and who has passed. Monster identities stay private to whoever drew them. (fixes: Which information is public (dungeon size, remaining equipment, deck size) is implicit in the physical game and must be stated for a text engine.): Makes clear exactly what can be inferred and from what.
- Use several dungeons per game within 40 turns, with a reshuffle each dungeon. Two successes still win, two failures still eliminate, and the tiebreak at the cap counts every run. (fixes: Deck luck can decide a short game when no fallback or tiebreak exists.): More dungeons per game let skill average out over deck order.

## Kept from the original

- A shared adventurer whose equipment is stripped as players remove monsters.
- The secret draw: each player knows only the monsters they drew.
- The three-way choice on a turn: add the monster to the dungeon, sacrifice equipment to discard it, or pass and sit out.
- The last player still in must run the dungeon.
- Two successful runs win; two failures eliminate; the last player standing wins.

## The variation's rules

COMPONENTS
- The adventurer has base HP 3 and five equipment items:
  - Armor: +5 HP.
  - Shield: +3 HP.
  - Torch: defeats every monster of strength 3 or less.
  - Holy Water: defeats Vampires and the Lich.
  - Dragon Spear: defeats the Dragon.
- Monster deck (13 cards): Goblin 1 x2, Skeleton 2 x2, Orc 3 x2, Vampire 4 x2, Golem 5 x2, Lich 6 x1, Demon 7 x1, Dragon 9 x1.
- Each player tracks successes (start 0) and failures (start 0).

SETUP
- Seat players in a fixed order. Player 1 begins the first dungeon.
- Shuffle the deck. The dungeon starts empty. All five items are present. No one has passed.

EACH ROUND (one turn)
1. Announcement. The engine announces to everyone:
   - whose turn it is (the active player);
   - the number of cards in the dungeon;
   - which equipment items remain;
   - the number of cards left in the deck;
   - who has passed;
   - everyone's successes and failures.
2. Talk. Every surviving (not eliminated) player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.
3. Pass or draw. The active player chooses PASS or DRAW.
   - If the deck is empty, the active player must PASS.
   - PASS: the player sits out the rest of this dungeon.
4. Secret draw. If the player chose DRAW, they privately see the top card of the deck, which leaves the deck. They then choose one of:
   - ADD: the card goes face-down into the dungeon. Only this player knows what it is.
   - SACRIFICE an item: one remaining equipment item (the player names which) is permanently removed for this dungeon, and the card is discarded unseen by others. This is allowed only if at least one item remains.
5. Advance. The turn passes to the next player clockwise who is neither eliminated nor passed in this dungeon.

THE RUN
- The run happens at the end of a round as soon as exactly one non-eliminated player has not passed. That player is the runner.
- HP = 3, plus 5 if Armor remains, plus 3 if Shield remains.
- Damage = the sum of the strengths of all dungeon cards, minus the strength of each card defeated by a remaining item:
  - Torch defeats strength 1, 2 and 3.
  - Holy Water defeats Vampires and the Lich.
  - Dragon Spear defeats the Dragon.
- All dungeon cards are then revealed to everyone, along with the damage and HP.
- If damage < HP, the runner gains 1 success. Otherwise the runner gains 1 failure.
- A player with 2 failures is eliminated and takes no further part.

NEW DUNGEON
- After a run, reshuffle all 13 monsters into a new deck.
- Empty the dungeon, restore all five items, and clear all passes.
- The next active player is the first surviving player clockwise from the runner.

GAME END
- The game ends immediately when:
  - a player reaches 2 successes (that player wins); or
  - only one player is not eliminated (that player wins).
- Otherwise the game ends after round 40. The surviving player with the most successes wins. If tied, the one among them with the fewest failures wins. If still tied, the game is a draw.

Objective: The first player to reach 2 successes wins. A player is also the winner if every other player has been eliminated by 2 failures. If neither happens by the end of round 40: among non-eliminated players, the highest successes wins, then the fewest failures; any remaining tie is a draw.

Expected effect: Each player sees only part of the dungeon. They weigh the visible dungeon size and the stripped equipment against what they personally added, and decide whether to stay in to become the runner or pass and push the risk onto others.

Adding a big monster is good if you expect a rival to run, and bad if you end up running. Sacrificing equipment removes a threat you know about but weakens any later run. Passing early concedes the chance to score.

Talk passes both tests.
- Reasoning: players make claims such as 'I added the Dragon' or 'that was only a Goblin' to scare rivals into continuing or to tempt them into passing, and others must check those claims against public facts.
- Conflict: only one player can win, and each wants a rival to run a deadly dungeon or to run a safe one themselves. A player who simply believes a claim either passes away a winnable run or runs into a dungeon that wounds them.

Rotating the start player and reshuffling over several dungeons spread out deck luck. The 40-round cap with an arithmetic tiebreak keeps the game finite without rewarding passivity, since a player who never runs has 0 successes.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
