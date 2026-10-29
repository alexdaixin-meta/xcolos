# 23 triage

- time: 2026-10-28T02:09:15+00:00 (18.2s)  model: claude-opus-5-5
- system prompt: [system/7ba6d9a4-triage.md](system/7ba6d9a4-triage.md) (sha256 7ba6d9a4f0852af8)
- sent sha256 e8761c723ba0bca3, reply sha256 b5ba3c82fbe44d01

## Sent

````
RULES:
SETUP
- Players sit in a fixed order, numbered 1 to N, where N is 5, 6 or 7.
- Roles are dealt at random and told privately. There is 1 wolf with 5 or 6 players and 2 wolves with 7. Wolves are not told who the other wolf is. Everyone else is a human.
- Each player has four counters:
  - Bites: private; meaningful only for humans.
  - Charms: private.
  - Wounds: public.
  - Salves: public.
- All counters start at 0, except that each human starts with Charms 2 (Charms 3 at 7 players).
- The game lasts 2 x N rounds: 10, 12 or 14. Each round has a Day and a Night.

DAY
1. Active player. Living players take the active role in seat order, skipping dead players. Round 1 starts with player 1.
2. Draw. The engine draws one card at random and announces it to everyone:
   - Wound 30%
   - Charm 30%
   - Salve 25%
   - Bite 15%
3. Talk. Every living player writes one short message at the same moment, without seeing the others. Then all messages are shown to everyone.
4. Give. The active player gives the card to another living player (not themselves). Everyone sees who receives it.
   - Wound or Salve: add 1 to the recipient's counter, in public.
   - Charm: the recipient gains 1 Charm.
   - Bite: a human recipient gains 1 Bite. If the recipient is a wolf, the card is discarded with no effect, and only that wolf learns this.
5. Accusation. All living players vote at the same moment. Each names one other living player, or 'nobody'. If one player is named by strictly more than half of the living players, that player gains 1 Wound. The vote counts are announced.
6. Death check. A player whose Wounds minus Salves is 2 or more dies. Their role is revealed, and they take no further part. If no wolves are alive, the humans win immediately.

NIGHT (no messages)
7. Action. Each living player secretly chooses one action:
   - 'Bite X': wolves only. A human who chooses Bite is treated as choosing None.
   - 'Charm X': requires at least 1 Charm. The sender loses 1 Charm. If the sender has no Charm, this is treated as None.
   - 'None'.
   X must be another living player.
8. Calm. Every wolf targeted by at least one Charm is calmed: its Bite tonight is cancelled. Charms aimed at wolves are used up.
9. Bites land. Each uncancelled Bite on a human adds 1 to that human's Bites. A Bite aimed at a wolf has no effect.
10. Cures. Each Charm on a human removes 1 of that human's Bites, but never below 0.
11. Private reports. Each player is told privately how many Bites landed on them and how many Charms they received, never who sent them. A wolf that was calmed learns that it was calmed.
12. Public report. The engine announces two numbers: the Bites that landed on humans tonight, and the wolves calmed tonight.
13. Infection. Any living human with Bites of 3 or more becomes a wolf. They are told privately. Their Bites reset to 0 and they keep their Charms. From next night on, they may Bite. Wolves never change back.

END CHECKS (after every Night)
14. If every living player is a wolf, the wolves win.
15. If two or fewer players are alive, the game ends and is scored.
16. After the Night of the final round, the game ends and is scored.

SCORING
Count living wolves and living humans. If living wolves are at least as many as living humans, the wolf team wins. Otherwise the human team wins. Each player belongs to the team of their role when the game ends, so converted humans win with the wolves.

How the winner is decided: This is a team win decided by counting roles. The humans win at once if no wolf is alive after a Day death check. The wolves win at once if every living player is a wolf after a Night. Otherwise, when the game ends (final Night, or two or fewer players alive), the wolf team wins if living wolves are at least as many as living humans, and the human team wins otherwise. There are no draws. Each player wins or loses with the team of their role at game end.

INTERFACE THE GAME FILE MUST USE:
- each player: `wounds` (number, visible: public, starts 0): Wound counter
- each player: `salves` (number, visible: public, starts 0): Salve counter; offsets wounds in the death check
- each player: `alive` (bool, visible: public, starts True): false once the player has died
- each player: `revealed_role` (text, visible: public, starts ''): the role, made public when the player dies
- each player: `votes_received` (number, visible: public, starts 0): accusation votes naming this player this Day
- each player: `won` (number, visible: public, starts 0): 1 if this player's team won (set at game end)
- the table: `round` (number, visible: public, starts 0): current round number
- the table: `total_rounds` (number, visible: public, starts 0): 2 x N
- the table: `active_seat` (number, visible: public, starts 0): seat of this Day's active player
- the table: `card` (text, visible: public, starts ''): this Day's drawn card
- the table: `recipient_seat` (number, visible: public, starts 0): seat that received this Day's card
- the table: `living_count` (number, visible: public, starts 0): number of living players
- the table: `bites_landed_tonight` (number, visible: public, starts 0): public report: Bites that landed on humans tonight
- the table: `wolves_calmed_tonight` (number, visible: public, starts 0): public report: wolves calmed tonight
- the table: `wolves_won` (number, visible: public, starts 0): 1 if the wolf team won, 0 if the human team won
- the table: `game_over` (number, visible: public, starts 0): 1 once the game has ended
- parameters (each must be an attribute holding this value, never a number buried in a step): min_players = 5, max_players = 7, wolves_at_5_or_6 = 1, wolves_at_7 = 2, human_start_charms_at_5_or_6 = 2, human_start_charms_at_7 = 3, rounds_per_player = 2, card_weight_wound = 30, card_weight_charm = 30, card_weight_salve = 25, card_weight_bite = 15, card_pool_wound = 6, card_pool_charm = 6, card_pool_salve = 5, card_pool_bite = 3, accusation_wounds = 1, death_threshold = 2, infection_threshold = 3, end_alive_at_most = 2, charm_cost = 1
- the game ends with ONE ending whose `rank_by` is `1 - abs(you.is_wolf - game.wolves_won)`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- that ending's `min_to_win` is `1`: a player below it cannot win, and if nobody reaches it the match ends with no winner
- anything else the game needs to keep track of is yours to design: name it as you like.

WHAT WENT WRONG:
the game file could not be built. What the checks found on the attempts:
- attempt 1: the game file was refused by the loader: growl: end[0].rank_by: 'game' is not a declared table attribute
- attempt 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (revealed_role, vote, revealed_role, revealed_role) in `your_role`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 3: the game file was refused by the loader: growl: end[0].rank_by: 'game' is not a declared table attribute
- attempt 4: it plays, but part of it does nothing: player attribute `just_turned` is never changed in 3 random matches, so nothing updates it. Steps that name it: the active player, infection. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `card_pool` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `wolves_won` is never changed in 3 random matches, so nothing updates it. Steps that name it: humans win, the game ends. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `wolf2` is never changed in 3 random matches, so nothing updates it. Steps that name it: the table and the deal. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- attempt 5: it plays, but part of it does nothing: game attribute `seat_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bite_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute
````

## Reply

````
```json
{"decision": "fix_game",
 "reason": "Each attempt fails for a different coder-side reason: a wrong reference in rank_by, bookkeeping fields left visible, attributes that are declared but never set, and attributes written only on rare branches. None of these show the rules are unsound or that the platform lacks a capability; they are mistakes in the file.",
 "guidance": "1) Ending: use exactly `1 - abs(you.is_wolf - game.wolves_won)`, and make sure `wolves_won` is a declared table attribute. Give each player an `is_wolf` number attribute (hidden) that the deal and infection keep up to date. Do not reintroduce whatever broke the reference in attempt 3. 2) Hide every bookkeeping attribute (`none` visibility on the table, `ally`/private on a player) so no empty fields such as a per-player `vote` or blank `revealed_role` show up in `your_role`. Only `revealed_role` itself should be public, and it is filled at death. 3) Delete any attribute you never update, such as `card_pool`, `seat_labels` and `bite_labels`. Draw the card with the weighted deck recipe from the card_pool_* parameters (remove/append on a game list), or take labels from a list built in a step that actually runs. 4) Make every tracked attribute change on a path that always runs: a) Set `wolves_won` explicitly at game end on both branches, with 1 when living wolves >= living humans and 0 otherwise. If it never moves in random matches, compute the end tallies into table attributes that are always written. b) Set `wolf2` in the deal on every player count, using a sentinel such as -1 when there is only one wolf, or drop it and mark wolves with per-player `is_wolf`. c) Avoid a `just_turned` flag that only rare infections touch. Either track `turned_round` (the round of infection, reset each night) or let the infection step itself delay the new wolf's first Bite by comparing round numbers. 5) Keep all parameters as attributes rather than literals in steps, use simultaneous polls for Talk, Accusation and Night actions, and run the death check and end checks as single steps with `when` conditions."
}
```
````
