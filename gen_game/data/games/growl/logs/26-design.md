# 26 design

- time: 2026-10-28T02:11:57+00:00 (181.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 4f137db3f26a9b74, reply sha256 d9a5acef701629fd

## Sent

````
Original game: Growl
Players in the original: 4 to 10

Original rules:
Setup a shared face-up deck containing Night cards seeded at 1/3, 2/3 and bottom of deck, plus Bite, Wound, Charm, Salve and Gold cards. Deal each player one starter Bite or Gold to secretly set Wolf Zeros; then deal 3 cards for a 4-card hand, redrawing if 3 wounds. On your turn draw the top deck card aloud: if it is a Night card resolve its effect then start Night Phase, otherwise you must give it to another living player who adds it to hand. Players die instantly when wounds minus salves reach 3, and humans secretly become werewolves when bites minus charms reach 3. During Night Phase no talking is allowed and each living player must pass one chosen card left and one right face-down, but humans may not pass Bites. After receiving, check death/turn. Game ends after Final Night is resolved or only two alive remain; if at least one human lives humans win, otherwise wolves win.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Win paths. Humans win if living_wolves = 0, or if round 8 is reached with living_wolves < living_humans (wolves_won = 0). Wolves win only by reaching living_wolves >= living_humans. The single wolf has two tools. (a) Infection: 3 net Bites on one human, with bite_limit = 3. (b) Using its one vote to push humans to their deaths, which needs wound_limit = 2. The wolf has no kill of its own.

Test the passive human policy (call it P):
- Every living human names the player to their left, so each player gets 1 vote and the top count is tied.
- At night, Salve whoever is wounded.
- Charm anyone who claims to have been bitten.

Round by round under P, 5 players (1 wolf, 4 humans):
- Wolf votes along: everyone has 1 vote, a tie, nobody is wounded.
- Wolf deviates and votes X, giving X 2 votes as the unique top: X goes to 1 wound and stays alive, because the death check needs 2. That night some human Salves X, so X is back to 0. Net effect 0.
- A human can only die after two wounds with no Salve between them. Under P that never happens. The exception is the wolf itself, which no human Salves.
- Infection: the wolf Bites V each night. V sees their own bites rise and claims it in talk. The wolf can also make a false claim to spread the Charms. That costs at most 2 Charms plus 1 Salve, which is 3 cards, against 4 human cards available in 5p and 6 in 7p.
- Net bites on V never reach 3. The wolf, acting alone, can at best keep 1 bite on V for a night.

Result of P against every wolf line:
| Wolf line | Outcome |
|---|---|
| vote along | 1v4 at round 8, Humans WIN |
| deviate vote | target salved, 1v4, Humans WIN |
| bite + false claim | charmed, 1v4, Humans WIN |
| random play | Humans WIN |

P never loses. It is a thoughtless stall that needs no inference and has a strictly safe outcome. Seat edge: the single wolf seat, with probability 1/n of being drawn, has close to 0% win rate under competent human play. If humans play randomly, accidental unsalved double-wounds can occasionally give the wolf parity, but the wolf's chances still stay far below 50%. The design's stated tension, infection versus lynching, is not borne out by the numbers. The game is described as a social-deduction contest, but by its arithmetic it is a human stall.
- playable FAILED: Limits are within bounds:
- steps_per_round 14 (cap 20)
- choice steps: Talk, Accusation, Night target, Night card = 4 (cap 4)
- attributes: 3 params + 4 table + 9 player = 16 (cap 20)
- hidden_elements 2, random_draws 0, rounds 8
- no board, clock or trading

Talk is simultaneous and placed correctly, since the wolf and the humans disagree.

Gaps in the rules:
(1) It is not stated whether vote_target or votes_received are shown after the tally. Voting patterns are the only possible clue to the wolf, so a model cannot know what it learns.
(2) It is not stated whether night targets or cards are ever revealed.
(3) There is no rule saying whether a player learns that their bites went up. 'Visible to its owner' implies they can read it, but the timing is not specified.
(4) Steps 7 and 8 are separate polls, so a player commits to a target before choosing a card. The text does not say whether the target can be left unused.

Fixed-length check. In this team game, the safe option (stall: tied votes plus Salve) wins every late round for humans. Nothing a wolf does after round 1 changes that. By the brief's own criterion, a fixed-length game where the safe line wins every late round fails.
- reasoning_over_luck FAILED: Luck: the only random element is the wolf assignment. With good play, humans adopt P and win every game regardless of who the wolf is. The result is therefore decided neither by luck nor by reasoning, but by a fixed safe strategy.

Inference: there is almost nothing to infer.
- The wolf's night target is hidden.
- Votes may be hidden (see playable).
- A bitten human learns only that some wolf targeted them, not which one.
- Lynching to find the wolf is a 1/(n-1) guess per execution. Each execution takes 2 rounds and gives the wolf parity progress whenever it hits a human.

Rational humans therefore never investigate. A strong reasoner and a weak one both choose 'stall and heal' and get the same result. A reasoning wolf has no lever that beats it, so skilled play is not favoured.
- change: Remove the timer win for humans. If round = max_rounds with a wolf still alive, the wolves win, or the result is scored on parity progress. Humans must then actually find and kill the wolf.
- change: Give the wolves a direct kill. For example, a wolf Bite also adds 1 wound to its target, or there is a separate wolf kill each night. A Salve should cancel at most one such wound.
- change: Limit Salves so that stalling is impossible. Options: each player may Salve at most twice per game, or a Salve cannot remove a wound gained in that same round's vote, or wound_limit = 1 for the day vote.
- change: Use 2 wolves for 6-7 players, or lower bite_limit to 2, and recompute so that the wolf team's win rate under good play on both sides is roughly 35-55%.
- change: Add a source of inference and state its visibility. Publish each round's vote tally and each player's vote_target. Optionally tell a Charm sender whether their target had bites > 0, so that Charm claims can be checked.
- change: State explicitly when a player sees their own bites change, and whether night targets or cards are ever revealed.
The variation that was reviewed: Growl: Night Passes: PARAMETERS (table): max_rounds = 8, bite_limit = 3, wound_limit = 2.

TABLE STATE (hidden from players unless stated): round (public, starts 0); living_wolves; living_humans; wolves_won (starts -1).

PLAYER STATE:
- is_wolf: 1 or 0, visible to the player and to fellow wolves only.
- bites: starts 0, visible to its owner only.
- wounds: public, starts 0.
- alive: public, starts 1.
- revealed_role: public, blank until death.
- vote_target, night_target, night_card, votes_received: hidden bookkeeping.

SETUP:
1. One player is chosen uniformly at random and gets is_wolf = 1. Every other player gets is_wolf = 0.
2. Each player is told privately whether they are a Wolf or a Human. Wolves are told who the other wolves are.
3. living_wolves = 1 and living_humans = number of players - 1.

EACH ROUND (living players only take part; dead players are skipped):
1. Announce: round increases by 1. Show every player's wounds and alive status, and the revealed_role of dead players.
2. Talk: everyone writes one short message at the same time. All messages are then shown to everyone. Lying is allowed, and nothing said is binding.
3. Accusation: at the same time, each living player names one other living player (their vote_target).
4. Tally: reset votes_received to 0 for all players, then add 1 to the votes_received of each player who was named.
5. Wound: if exactly one player has the most votes, that player's wounds increase by 1. If the top count is tied, no one is wounded.
6. Death check: any living player with wounds >= wound_limit dies. Set alive = 0, and set revealed_role to 'Wolf' if is_wolf = 1, otherwise 'Human'.
7. Night target: at the same time and in silence, each living player names one other living player (their night_target).
8. Night card: at the same time, each living player chooses Bite, Charm or Salve (their night_card).
9. Bites resolve: for each living player with is_wolf = 1 who chose Bite, their target's bites increase by 1. A Bite chosen by a human has no effect.
10. Charms resolve: for each Charm sent, the target's bites decrease by 1, to a minimum of 0.
11. Salves resolve: for each Salve sent, the target's wounds decrease by 1, to a minimum of 0.
12. Infection: every living player with is_wolf = 0 and bites >= bite_limit becomes a wolf. Set is_wolf = 1 and bites = 0. They are told privately, along with the identities of the other wolves. Because Bites were already resolved in step 9, a new wolf's first Bite counts from the next night.
13. Tally: living_wolves = number of living players with is_wolf = 1; living_humans = number of living players with is_wolf = 0.
14. End check: the game ends if living_wolves >= living_humans, or living_wolves = 0, or round = max_rounds. On ending, set wolves_won = 1 if living_wolves >= living_humans, otherwise wolves_won = 0. Winner: At the end, each player (alive or dead) scores result = 1 - abs(is_wolf - wolves_won), using their final is_wolf. Infected players count as wolves. Every player with result 1 wins and every player with result 0 loses, so the winner is decided by team.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Growl is a 4-10 player hidden-role card game. Players pass cards from a shared face-up deck and, at Night, pass one card face-down to each neighbour. Wolves spread Bites that secretly turn humans into wolves when bites minus charms reach 3, and Wounds kill at 3. Humans win if any human survives the Final Night. The previous XColos variation turned this into a vote-and-night-card game: one wolf, wounds from day votes (2 kill), Bites to infect (3 convert), and a human win if the 8-round timer ran out.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the previous variation the passive human policy P never loses: everyone votes left so the vote is always tied, Salve anyone wounded, and Charm anyone who claims a bite. A day vote alone could not kill (wound_limit 2, Salve between). The lone wolf had no kill of its own. Its infection needed 3 net Bites against several Charms per night, and the timer handed humans the win. Every wolf line, and random play, lost to P. The wolf seat was close to 0% under competent play."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "A strong human and a weak human both play 'stall and heal' and get the same result. A strong wolf has no lever that beats the stall. Skill changes nothing once humans adopt P."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "The game is effectively solved for the human side (stall), and hopeless for the wolf side. There is nothing for either side to improve at."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "bad",
      "evidence": "Hidden state existed: the wolf's identity, night targets and bites. But no rule ever surfaced a clue. Votes were not stated to be public, night actions were never revealed, and Charm claims could not be checked. Investigating was strictly worse than stalling, so nothing was inferred. The original card game's real clue (a Bite must come from a neighbour, since humans cannot pass Bites) was lost."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Team membership, the parity check and the round counter decide the winner by arithmetic. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It was within the limits (14 steps, 4 choice steps, 16 attributes, 2 hidden elements, no draws, 8 rounds), turn-based and text-only. But it left gaps a model cannot resolve. Were vote targets shown? Were night actions ever revealed? When does a player see their own bites? Could a night target go unused?"
    }
  ],
  "problems": [
    "P1 Timer favours humans: running out the clock with a living wolf was a human win, so stalling (tied votes) was a guaranteed safe strategy.",
    "P2 Day votes were toothless: wound_limit 2 plus unlimited Salves meant a vote never killed, so humans never had to commit to an accusation.",
    "P3 Wolves had no kill and only one wolf: infection at 3 net Bites by a single wolf was always out-Charmed. The wolf team's win rate was near 0%.",
    "P4 No source of inference: votes, night actions and Charm results were never revealed, so there was nothing to deduce and no reason to investigate.",
    "P5 Rule gaps: vote visibility, night-action visibility, the timing of a player seeing their own bites, and whether a night target could go unused were unspecified.",
    "P6 Wolves had no way to coordinate, so two-wolf plans (a double Bite or a double Maul) depended on luck."
  ],
  "changes": [
    {
      "what": "If the last round ends with any wolf alive, the wolves win. Humans win only by eliminating every wolf. Wolves also win immediately at parity (living wolves >= living humans).",
      "why": "Tied votes now lose for humans, so they must accuse and execute. A wolf that survives by blending in is rewarded.",
      "fixes": "P1 Timer favours humans"
    },
    {
      "what": "A day vote with a unique top count executes that player at once and reveals their role. A tied top count executes no one. Every vote target and the full tally are published.",
      "why": "Accusations have real stakes: a wrong execution costs humans a member and moves the wolves toward parity. The public voting record becomes evidence.",
      "fixes": "P2 Day votes were toothless; P4 No source of inference"
    },
    {
      "what": "Start with 2 wolves (6-7 players). Wolves may play Maul (+1 wound; 2 wounds kill) or Bite (+1 bite; 3 bites convert a human), as well as Charm or Salve. Humans may play only Charm or Salve, one card per night.",
      "why": "Wolves now have a kill (two Mauls on one unsalved target) and a realistic infection route. Humans can protect only one player each per night, so healing everyone is impossible. As a rough guide, random humans against wolves that never act win about 33% at 6 players. Real wolf pressure and real human deduction both move this, which targets a balanced middle.",
      "fixes": "P3 Wolves had no kill and only one wolf"
    },
    {
      "what": "Exposure: each night, after the cards resolve, one living player is drawn uniformly at random. Their card and target are announced publicly next morning.",
      "why": "This is the single random draw. It restores Growl's core clue that only a wolf can pass a Bite: an exposed Bite or Maul proves a wolf. Every aggressive wolf action therefore carries a risk, and wolves must plan when to strike and when to play a harmless card as cover.",
      "fixes": "P4 No source of inference"
    },
    {
      "what": "Charm feedback: whoever plays a Charm is privately told whether the target had any bites (after tonight's Bites, before any Charm). Each player privately sees their own bite count every morning.",
      "why": "Claims of being bitten become checkable. A wolf who falsely claims a bite to draw Charms can be caught, but only by those who Charmed it, who may themselves be lying in talk.",
      "fixes": "P4 No source of inference; P5 Rule gaps"
    },
    {
      "what": "Wolf den: each night, living wolves exchange one private message seen only by wolves. The night action is one combined choice of card plus target, and the card always goes to that target.",
      "why": "Wolves can plan double Bites or double Mauls. Combining card and target keeps choice steps at 4 and removes the 'unused target' ambiguity.",
      "fixes": "P6 Wolves had no way to coordinate; P5 Rule gaps"
    },
    {
      "what": "Every visibility rule is stated explicitly: what is public, what is private to whom, and when.",
      "why": "A model must know exactly what it learns in order to reason.",
      "fixes": "P5 Rule gaps"
    }
  ],
  "keeps": [
    "Hidden wolves among humans, team win by final allegiance.",
    "Bite, Charm and Salve cards; infection when bites reach a limit, with Charms removing bites.",
    "Wounds kill at a limit, Salves heal them.",
    "Infected humans silently switch sides and win with the wolves.",
    "Only wolves can play a Bite, so a seen Bite proves a wolf (the original's key deduction).",
    "Day talk, then a silent Night in which everyone secretly plays a card on someone.",
    "The game ends at parity or after a fixed number of nights."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The hidden-role, infection and card-passing core is rich in inference and fits the limits. The failures came from the winner rule and missing information, which the changes fix."
  },
  "variation": {
    "name": "Growl: Scent of Blood",
    "summary": "Six or seven players, two secret wolves. By day everyone talks and votes, and a unique top vote executes. By night everyone secretly plays one card on one player: wolves can Bite (convert) or Maul (kill), and everyone can Charm or Salve. One random player's night card is exposed each morning, and Charmers learn whether their target was really bitten. Humans must find and execute every wolf within 6 rounds; wolves win at parity or by surviving.",
    "players": {"min": 6, "max": 7, "suggested": 6},
    "rules": "PARAMETERS: max_rounds = 6; bite_limit = 3; wound_limit = 2. Starting wolves = 2.\n\nTABLE STATE: round (public, starts 0); living_wolves and living_humans (hidden counts); exposed_player, exposed_card and exposed_target (announced each morning); wolves_won (starts -1).\n\nPLAYER STATE:\n- is_wolf (1 or 0): known to the player and to all other wolves.\n- bites (starts 0): known only to its owner, who is told the value each morning.\n- wounds (starts 0): public.\n- alive (starts 1): public.\n- revealed_role: public, blank until death, then 'Wolf' or 'Human'.\n- vote_target and votes_received: public after each vote.\n- night_card and night_target: private, except when exposed.\n\nSETUP:\n1. Choose 2 players uniformly at random as wolves (is_wolf = 1). All others are humans (is_wolf = 0).\n2. Tell each player privately whether they are a Wolf or a Human. Each wolf is told who the other wolf is.\n3. Set living_wolves = 2 and living_humans = players - 2.\n\nEACH ROUND (only living players act; dead players are skipped):\n1. Morning announcement: round increases by 1. Publicly show every player's wounds and alive status, and the revealed_role of the dead. From round 2 on, announce last night's exposure: 'exposed_player played exposed_card on exposed_target'. Privately tell each living player their current bites.\n2. Talk: every living player writes one short message at the same time. All messages are then shown to everyone. Lying is allowed, and nothing is binding.\n3. Vote: at the same time, each living player names one other living player (vote_target). Abstaining is not allowed.\n4. Tally: votes_received = the number of votes each player got. Publicly show every player's vote_target and every votes_received.\n5. Execution: if exactly one player has the most votes, that player dies. Set alive = 0 and reveal their role publicly. If the top count is tied, no one dies.\n6. Count: living_wolves = living players with is_wolf = 1; living_humans = living players with is_wolf = 0.\n7. Day end check: if living_wolves = 0 the game ends and the humans win. If living_wolves >= living_humans the game ends and the wolves win.\n8. Wolf den: every living wolf writes one short message at the same time. Messages are shown only to living wolves. Humans see nothing and are not told what was said.\n9. Night action: at the same time and in silence, each living player chooses one card and one other living player as its target. A human may choose Charm or Salve. A wolf may choose Bite, Maul, Charm or Salve. The card always goes to the chosen target; there is no pass.\n10. Bites and Mauls: each Bite on a human adds 1 to the target's bites (a Bite on a wolf has no effect). Each Maul adds 1 to the target's wounds.\n11. Charms: each player who played Charm is privately told 'your target had bites' or 'your target had no bites', judged after step 10 and before any Charm is applied. Then each Charm lowers the target's bites by 1, to a minimum of 0.\n12. Salves: each Salve lowers the target's wounds by 1, to a minimum of 0.\n13. Exposure: draw one living player uniformly at random. Record their name, card and target as exposed_player, exposed_card and exposed_target, to be announced next morning.\n14. Death check: any living player with wounds >= 2 dies (alive = 0) and their role is revealed publicly.\n15. Infection: any living human with bites >= 3 becomes a wolf. Set is_wolf = 1 and bites = 0. They are told privately, together with the names of all living wolves, and all wolves are told who the new wolf is. A new wolf acts as a wolf from the next round.\n16. Count: recompute living_wolves and living_humans.\n17. Night end check: if living_wolves = 0, the humans win. Otherwise, if living_wolves >= living_humans, the wolves win. Otherwise, if round = max_rounds, the wolves win, because a wolf survived.\n18. If the game has not ended, start the next round.\n\nWHAT IS NEVER REVEALED: the night cards and targets of anyone except the exposed player, other players' bites, wolf den messages, and any Charm feedback except to the player who played that Charm.",
    "objective": "Team game, decided by arithmetic. If the game ends with living_wolves = 0, wolves_won = 0. If it ends with living_wolves >= living_humans, or at the end of round 6 with any wolf alive, wolves_won = 1. Each player, alive or dead, scores result = 1 - |final is_wolf - wolves_won|. Players with result 1 win and players with result 0 lose, so the winning side is the whole team, and infected players count as wolves. There are no draws.",
    "expected_effect": "Stalling is dead: tied votes lead to a wolf win at round 6, and always healing does not find wolves. Humans must convert clues into executions. Those clues are exposed cards (a Bite or Maul proves a wolf), the public voting record, Charm feedback that tests bite claims, and who heals or protects whom. Wolves face a planning trade-off. Each Bite or Maul risks exposure, roughly 1 in 6 per action, but without them they rely on misdirected lynches, which random humans survive about a third of the time. The wolf den lets two wolves plan a double Maul kill, or a two-night infection that flips a human and can reach parity. Talk earns its place because the sides truly disagree. Wolves want a human executed, or a tie. Humans want a wolf executed. Wolves will push accusations, fake bite claims and fake Charm feedback. A human who simply follows the loudest accuser, or agrees to an 'everyone vote left' tie, can execute a teammate or run out the clock and lose. Converted humans flip sides silently, so even confirmed allies can turn."
  },
  "model": null,
  "complexity": {"steps_per_round": 18, "choice_steps_per_round": 4, "attributes": 19, "hidden_elements": 3, "random_draws_per_round": 1, "rounds": 6}
}
```
````
