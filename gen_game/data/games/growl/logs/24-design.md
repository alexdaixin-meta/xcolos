# 24 design

- time: 2026-10-28T02:09:34+00:00 (81.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 e1a38175408b2387, reply sha256 bca1221a10945f53

## Sent

````
Original game: Growl
Players in the original: 4 to 10

Original rules:
Setup a shared face-up deck containing Night cards seeded at 1/3, 2/3 and bottom of deck, plus Bite, Wound, Charm, Salve and Gold cards. Deal each player one starter Bite or Gold to secretly set Wolf Zeros; then deal 3 cards for a 4-card hand, redrawing if 3 wounds. On your turn draw the top deck card aloud: if it is a Night card resolve its effect then start Night Phase, otherwise you must give it to another living player who adds it to hand. Players die instantly when wounds minus salves reach 3, and humans secretly become werewolves when bites minus charms reach 3. During Night Phase no talking is allowed and each living player must pass one chosen card left and one right face-down, but humans may not pass Bites. After receiving, check death/turn. Game ends after Final Night is resolved or only two alive remain; if at least one human lives humans win, otherwise wolves win.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
1) Ending: use exactly `1 - abs(you.is_wolf - game.wolves_won)`, and make sure `wolves_won` is a declared table attribute. Give each player an `is_wolf` number attribute (hidden) that the deal and infection keep up to date. Do not reintroduce whatever broke the reference in attempt 3. 2) Hide every bookkeeping attribute (`none` visibility on the table, `ally`/private on a player) so no empty fields such as a per-player `vote` or blank `revealed_role` show up in `your_role`. Only `revealed_role` itself should be public, and it is filled at death. 3) Delete any attribute you never update, such as `card_pool`, `seat_labels` and `bite_labels`. Draw the card with the weighted deck recipe from the card_pool_* parameters (remove/append on a game list), or take labels from a list built in a step that actually runs. 4) Make every tracked attribute change on a path that always runs: a) Set `wolves_won` explicitly at game end on both branches, with 1 when living wolves >= living humans and 0 otherwise. If it never moves in random matches, compute the end tallies into table attributes that are always written. b) Set `wolf2` in the deal on every player count, using a sentinel such as -1 when there is only one wolf, or drop it and mark wolves with per-player `is_wolf`. c) Avoid a `just_turned` flag that only rare infections touch. Either track `turned_round` (the round of infection, reset each night) or let the infection step itself delay the new wolf's first Bite by comparing round numbers. 5) Keep all parameters as attributes rather than literals in steps, use simultaneous polls for Talk, Accusation and Night actions, and run the death check and end checks as single steps with `when` conditions.
the game file could not be built. What the checks found on the attempts:
- attempt 1: the game file was refused by the loader: growl: end[0].rank_by: 'game' is not a declared table attribute
- attempt 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (revealed_role, vote, revealed_role, revealed_role) in `your_role`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 3: the game file was refused by the loader: growl: end[0].rank_by: 'game' is not a declared table attribute
- attempt 4: it plays, but part of it does nothing: player attribute `just_turned` is never changed in 3 random matches, so nothing updates it. Steps that name it: the active player, infection. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `card_pool` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `wolves_won` is never changed in 3 random matches, so nothing updates it. Steps that name it: humans win, the game ends. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `wolf2` is never changed in 3 random matches, so nothing updates it. Steps that name it: the table and the deal. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- attempt 5: it plays, but part of it does nothing: game attribute `seat_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bite_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Growl is a 4-10 player hidden-role social game. Face-up cards (Bites, Wounds, Charms, Salves, Gold) are handed to other players by day, and two cards are passed face-down at each Night. Too many Wounds kill a player, and too many Bites secretly turn a human into a werewolf. Humans win if at least one human is alive at the end; otherwise the wolves win.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "No single simple policy dominates: handing Wounds or passing Bites always has to be aimed at someone. However, the humans' win condition (any one human alive after the Final Night) is very loose. The face-up deck and the 'must give the drawn card' rule mean the order of the draw often decides who gets hurt, whatever anyone chooses."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading who passed you a Bite and steering Charms and Salves takes skill. But the starter deal (Bite or Gold), the 3-card hand and the deck order put a lot of variance into who gets infected or killed."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Bluffing about your own Bite count, tracking who passed what, and timing Charms leave plenty of room to improve. A weak player can still ride a winning team."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Roles are hidden, infection is secret and passes are face-down. Players must infer who is a wolf from behaviour and from what arrives in their hand."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Deaths, infections and the winner all follow from counting cards (wounds minus salves, bites minus charms) and checking who is alive."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Passing to left and right needs seat adjacency, and the physical deck with seeded Night cards and redraws needs many steps. Five previous build attempts failed on bookkeeping: an undeclared rank_by, blank fields shown to players, and attributes that never changed (card_pool, wolf2, just_turned, seat_labels, bite_labels, wolves_won)."
    }
  ],
  "problems": [
    "P1: The physical shared deck (seeded Night cards, 4-card hands, redraws) costs many steps and bookkeeping attributes (card_pool, seat_labels, bite_labels) that the builds never updated.",
    "P2: Passing left and right depends on seat adjacency, which is spatial-like and needs extra label lists.",
    "P3: Deck order and the starter deal add luck that swamps the reasoning about who is biting whom.",
    "P4: The humans' winning condition (any one human alive) is too loose, and the ending was built on an undeclared reference ('game'), which the loader refused.",
    "P5: A second-wolf attribute (wolf2) and a just_turned flag only changed on rare paths, so random matches never touched them.",
    "P6: wolves_won was only written on a rarely taken branch, so it never moved.",
    "P7: Internal per-player fields (vote, blank revealed_role) were visible to players and cluttered the state."
  ],
  "changes": [
    {
      "what": "Remove the deck and hands entirely. Each night every living player simultaneously picks a target and one card type (Bite, Charm or Salve) from an unlimited supply. A Bite only counts if the passer is a wolf.",
      "why": "Keeps the essence (secret Bites, Charms and Salves passed at night) with no card pool to maintain, and humans still effectively cannot bite.",
      "fixes": "P1"
    },
    {
      "what": "Players choose a target by name from the living players instead of passing left and right.",
      "why": "Removes adjacency and label lists, and makes the choice of whom to bite or charm a real decision.",
      "fixes": "P2"
    },
    {
      "what": "Wounds come only from a daytime accusation vote, made simultaneously. The unique top-voted player takes 1 Wound; on a tie nobody does.",
      "why": "Replaces luck-of-the-draw Wounds with a deliberate group decision driven by inference about who is a wolf.",
      "fixes": "P3"
    },
    {
      "what": "Exactly one starting wolf, marked by a per-player hidden is_wolf (1 or 0) set in the deal for every player. No wolf2 attribute and no just_turned flag. Infection is resolved in a step after all Bites, so a new wolf's first Bite naturally comes the next night.",
      "why": "is_wolf is always written at the deal, and the step order replaces the rarely touched flag.",
      "fixes": "P5"
    },
    {
      "what": "Living-wolf and living-human tallies are table attributes written every round. wolves_won starts at -1 and is written to 1 or 0 at game end, which always happens.",
      "why": "Every tracked attribute changes on a path that always runs.",
      "fixes": "P6"
    },
    {
      "what": "Winner rule: wolves win if living wolves are at least living humans at any end check; humans win if all wolves are dead, or if humans still outnumber wolves after round 8. Each player's result is 1 - abs(is_wolf - wolves_won), with wolves_won a declared table attribute.",
      "why": "Tightens the loose 'one human alive' rule so both teams must work, and fixes the loader error.",
      "fixes": "P4"
    },
    {
      "what": "Bookkeeping visibility: vote_target, night_target, night_card and votes_received are hidden (none). is_wolf is visible to wolf allies only. bites is private to its owner. Only wounds, alive and revealed_role are public, and revealed_role is filled at death.",
      "why": "Keeps empty internal fields out of what players see.",
      "fixes": "P7"
    },
    {
      "what": "All numbers (max_rounds=8, bite_limit=3, wound_limit=2) are table parameters, not literals in steps.",
      "why": "Makes tuning safe and the build consistent.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "Secret werewolf team versus human majority",
    "Infection: a human turns wolf when net Bites (Bites minus Charms) reach 3, and then switches sides",
    "Death when Wounds reach the limit, with Salves healing Wounds",
    "Night passes are hidden and cannot be traced, so you only know that you were bitten, not by whom",
    "Day discussion followed by a silent night"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The infection-and-deduction core fits in about 14 steps once the physical deck and seating are replaced by targeted simultaneous choices."
  },
  "variation": {
    "name": "Growl: Night Passes",
    "summary": "One hidden werewolf among 5-7 players. Each round the players talk, vote someone a Wound, and then at night secretly send one Bite, Charm or Salve to a player of their choice. Bites from wolves infect humans, who turn wolf at 3 net Bites. Wolves win by equalling the humans.",
    "players": {"min": 5, "max": 7, "suggested": 6},
    "rules": "PARAMETERS (table): max_rounds = 8, bite_limit = 3, wound_limit = 2.\n\nTABLE STATE (hidden from players unless stated): round (public, starts 0); living_wolves; living_humans; wolves_won (starts -1).\n\nPLAYER STATE:\n- is_wolf: 1 or 0, visible to the player and to fellow wolves only.\n- bites: starts 0, visible to its owner only.\n- wounds: public, starts 0.\n- alive: public, starts 1.\n- revealed_role: public, blank until death.\n- vote_target, night_target, night_card, votes_received: hidden bookkeeping.\n\nSETUP:\n1. One player is chosen uniformly at random and gets is_wolf = 1. Every other player gets is_wolf = 0.\n2. Each player is told privately whether they are a Wolf or a Human. Wolves are told who the other wolves are.\n3. living_wolves = 1 and living_humans = number of players - 1.\n\nEACH ROUND (living players only take part; dead players are skipped):\n1. Announce: round increases by 1. Show every player's wounds and alive status, and the revealed_role of dead players.\n2. Talk: everyone writes one short message at the same time. All messages are then shown to everyone. Lying is allowed, and nothing said is binding.\n3. Accusation: at the same time, each living player names one other living player (their vote_target).\n4. Tally: reset votes_received to 0 for all players, then add 1 to the votes_received of each player who was named.\n5. Wound: if exactly one player has the most votes, that player's wounds increase by 1. If the top count is tied, no one is wounded.\n6. Death check: any living player with wounds >= wound_limit dies. Set alive = 0, and set revealed_role to 'Wolf' if is_wolf = 1, otherwise 'Human'.\n7. Night target: at the same time and in silence, each living player names one other living player (their night_target).\n8. Night card: at the same time, each living player chooses Bite, Charm or Salve (their night_card).\n9. Bites resolve: for each living player with is_wolf = 1 who chose Bite, their target's bites increase by 1. A Bite chosen by a human has no effect.\n10. Charms resolve: for each Charm sent, the target's bites decrease by 1, to a minimum of 0.\n11. Salves resolve: for each Salve sent, the target's wounds decrease by 1, to a minimum of 0.\n12. Infection: every living player with is_wolf = 0 and bites >= bite_limit becomes a wolf. Set is_wolf = 1 and bites = 0. They are told privately, along with the identities of the other wolves. Because Bites were already resolved in step 9, a new wolf's first Bite counts from the next night.\n13. Tally: living_wolves = number of living players with is_wolf = 1; living_humans = number of living players with is_wolf = 0.\n14. End check: the game ends if living_wolves >= living_humans, or living_wolves = 0, or round = max_rounds. On ending, set wolves_won = 1 if living_wolves >= living_humans, otherwise wolves_won = 0.",
    "objective": "At the end, each player (alive or dead) scores result = 1 - abs(is_wolf - wolves_won), using their final is_wolf. Infected players count as wolves. Every player with result 1 wins and every player with result 0 loses, so the winner is decided by team.",
    "expected_effect": "Humans must find the wolf through vote patterns and claims before infection snowballs. A bitten player knows their own Bite count but cannot prove it. Wolves can falsely claim to be bitten so that Charms are wasted on them, or quietly concentrate Bites on one quiet target. Talk earns its place because the teams disagree. Wolves want the vote to fall on humans and the Charms to go to the wrong player. A human who simply follows a confident proposal may vote out a fellow human or charm the wolf, and that can hand the wolves parity. Infected humans switch sides mid-game, so earlier trust can become a liability. There is no deck luck: the only random event is the starting wolf, and good play by either team can overcome it."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 8
  }
}
```
````
