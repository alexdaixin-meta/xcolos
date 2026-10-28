# 27 critic

- time: 2026-10-28T02:14:58+00:00 (87.4s)  model: claude-opus-5-5
- system prompt: [system/37afe4a1-critic.md](system/37afe4a1-critic.md) (sha256 37afe4a1837f349a)
- sent sha256 4432b053d3342f02, reply sha256 1acd243835796113

## Sent

````
ORIGINAL GAME: Growl
Setup a shared face-up deck containing Night cards seeded at 1/3, 2/3 and bottom of deck, plus Bite, Wound, Charm, Salve and Gold cards. Deal each player one starter Bite or Gold to secretly set Wolf Zeros; then deal 3 cards for a 4-card hand, redrawing if 3 wounds. On your turn draw the top deck card aloud: if it is a Night card resolve its effect then start Night Phase, otherwise you must give it to another living player who adds it to hand. Players die instantly when wounds minus salves reach 3, and humans secretly become werewolves when bites minus charms reach 3. During Night Phase no talking is allowed and each living player must pass one chosen card left and one right face-down, but humans may not pass Bites. After receiving, check death/turn. Game ends after Final Night is resolved or only two alive remain; if at least one human lives humans win, otherwise wolves win.

PROPOSED VARIATION: Growl: Scent of Blood
Players: 6 to 7
Rules: PARAMETERS: max_rounds = 6; bite_limit = 3; wound_limit = 2. Starting wolves = 2.

TABLE STATE: round (public, starts 0); living_wolves and living_humans (hidden counts); exposed_player, exposed_card and exposed_target (announced each morning); wolves_won (starts -1).

PLAYER STATE:
- is_wolf (1 or 0): known to the player and to all other wolves.
- bites (starts 0): known only to its owner, who is told the value each morning.
- wounds (starts 0): public.
- alive (starts 1): public.
- revealed_role: public, blank until death, then 'Wolf' or 'Human'.
- vote_target and votes_received: public after each vote.
- night_card and night_target: private, except when exposed.

SETUP:
1. Choose 2 players uniformly at random as wolves (is_wolf = 1). All others are humans (is_wolf = 0).
2. Tell each player privately whether they are a Wolf or a Human. Each wolf is told who the other wolf is.
3. Set living_wolves = 2 and living_humans = players - 2.

EACH ROUND (only living players act; dead players are skipped):
1. Morning announcement: round increases by 1. Publicly show every player's wounds and alive status, and the revealed_role of the dead. From round 2 on, announce last night's exposure: 'exposed_player played exposed_card on exposed_target'. Privately tell each living player their current bites.
2. Talk: every living player writes one short message at the same time. All messages are then shown to everyone. Lying is allowed, and nothing is binding.
3. Vote: at the same time, each living player names one other living player (vote_target). Abstaining is not allowed.
4. Tally: votes_received = the number of votes each player got. Publicly show every player's vote_target and every votes_received.
5. Execution: if exactly one player has the most votes, that player dies. Set alive = 0 and reveal their role publicly. If the top count is tied, no one dies.
6. Count: living_wolves = living players with is_wolf = 1; living_humans = living players with is_wolf = 0.
7. Day end check: if living_wolves = 0 the game ends and the humans win. If living_wolves >= living_humans the game ends and the wolves win.
8. Wolf den: every living wolf writes one short message at the same time. Messages are shown only to living wolves. Humans see nothing and are not told what was said.
9. Night action: at the same time and in silence, each living player chooses one card and one other living player as its target. A human may choose Charm or Salve. A wolf may choose Bite, Maul, Charm or Salve. The card always goes to the chosen target; there is no pass.
10. Bites and Mauls: each Bite on a human adds 1 to the target's bites (a Bite on a wolf has no effect). Each Maul adds 1 to the target's wounds.
11. Charms: each player who played Charm is privately told 'your target had bites' or 'your target had no bites', judged after step 10 and before any Charm is applied. Then each Charm lowers the target's bites by 1, to a minimum of 0.
12. Salves: each Salve lowers the target's wounds by 1, to a minimum of 0.
13. Exposure: draw one living player uniformly at random. Record their name, card and target as exposed_player, exposed_card and exposed_target, to be announced next morning.
14. Death check: any living player with wounds >= 2 dies (alive = 0) and their role is revealed publicly.
15. Infection: any living human with bites >= 3 becomes a wolf. Set is_wolf = 1 and bites = 0. They are told privately, together with the names of all living wolves, and all wolves are told who the new wolf is. A new wolf acts as a wolf from the next round.
16. Count: recompute living_wolves and living_humans.
17. Night end check: if living_wolves = 0, the humans win. Otherwise, if living_wolves >= living_humans, the wolves win. Otherwise, if round = max_rounds, the wolves win, because a wolf survived.
18. If the game has not ended, start the next round.

WHAT IS NEVER REVEALED: the night cards and targets of anyone except the exposed player, other players' bites, wolf den messages, and any Charm feedback except to the player who played that Charm.
How the winner is decided: Team game, decided by arithmetic. If the game ends with living_wolves = 0, wolves_won = 0. If it ends with living_wolves >= living_humans, or at the end of round 6 with any wolf alive, wolves_won = 1. Each player, alive or dead, scores result = 1 - |final is_wolf - wolves_won|. Players with result 1 win and players with result 0 lose, so the winning side is the whole team, and infected players count as wolves. There are no draws.
The designer's stated complexity: {"steps_per_round": 18, "choice_steps_per_round": 4, "attributes": 19, "hidden_elements": 3, "random_draws_per_round": 1, "rounds": 6}
````

## Reply

````
```json
{"balanced": {"verdict": "fail", "evidence": "**Win thresholds (6 players: 2 wolves, 4 humans).** The wolves win as soon as living_humans <= living_wolves. That means the wolves need to remove only 2 humans (4 -> 2) before the humans find both wolves.\n\n**Thoughtless wolf policy W:** both wolves always vote for the same human, and at night both play Maul on the same human (2 wounds = wound_limit, so the target dies).\n\n**Day 1.** Humans have zero information: there has been no exposure and no Charm yet. A human picking blindly among 5 others has P(wolf) = 2/5 = 0.40. The wolves' 2 bloc votes also split or decide the human votes. Outcomes:\n- Human lynched (about 0.45): 2v3. Night kill: 2v2, wolves win.\n- Tie (about 0.15): 2v4, then the night kill makes 2v3.\n- Wolf lynched (about 0.40).\n\n**Can Salve stop the kill?** Each non-target human salves one of 4 others, so each hits the target with probability about 1/4. With 2 helpers in a 2v3 position, P(at least one save) = 1 - (3/4)^2 = 0.44. The target cannot salve itself.\n\n**Exposure.** The random exposure reveals a mauling wolf with probability W/N, about 1/3, per night.\n\n**Rough path sum, 6 players.** P(humans win) ≈ 0.40 x 0.6 (find the second wolf, helped by the 1/3 exposure) + 0.60 x [0.44 x 0.33 x 0.5 + tie branch about 0.05] ≈ 0.24 + 0.07 ≈ 0.31. So policy W, which never adapts, wins about 70% for the wolves.\n\n**Bite is a stronger, still thoughtless policy.** Two wolves biting the same human X reach bites 2 on night 1. One more bite on night 2 gives bites 3, and X is infected. That is a swing of -1 human and +1 wolf with no public trace: no wound, no death, no revealed role. From 2v4 with no lynch, this alone gives 3v3 and the wolves win at step 17 of round 2. Only a Charm aimed at X by another human prevents it, and blind Charm hit rate is about 1/4 per human.\n\n**Round-6 rule.** Any surviving wolf wins at round 6, which adds a further wolf-only tiebreak.\n\n**Payoff table (team result).**\n| Ending | wolf | human |\n|---|---|---|\n| wolves_won = 1 | 1 | 0 |\n| wolves_won = 0 | 0 | 1 |\n\nThe wolves' bloc-vote plus focus-fire (or focus-bite) policy wins most games without any reasoning.\n\n**7 players** (2v5, 3 human losses allowed) is closer, about 45/55. So the balance also swings strongly with player count. Seat order gives no edge, because all choices are simultaneous. The asymmetry lies entirely in information (wolves know everything relevant) and in the win conditions." },
 "playable": {"verdict": "fail", "evidence": "**Within limits:** 18 steps per round (<= 20). 4 choice steps (talk, vote, den, night) (<= 4). About 16-19 attributes (<= 20). 1 random draw per round (the exposure; the wolf choice is setup only). 6 rounds (<= 40).\n\n**Talk is well placed:** it is simultaneous and placed where wolves and humans disagree.\n\n**Hidden elements exceed the limit of 3.** The game actually hides five independent kinds of information:\n1. Each player's is_wolf.\n2. Each player's bites, private per owner.\n3. Each player's night_card and night_target, except the exposed one.\n4. The wolf-den private channel.\n5. Per-player private Charm feedback.\n\nThe infection notice is also a private message to the new wolf and to all wolves. The stated 'hidden_elements: 3' undercounts.\n\n**Minor ambiguities:**\n- Whether a wolf may target another wolf with Maul is not stated (presumably yes).\n- Whether a newly infected wolf joins the den in the same night is unclear. Step 15 comes after step 8, so it is presumably the next night.\n- Whether a player at wounds 2 who is also at bites 3 dies as a human is resolved by step order (death before infection) but is not stated.\n\nThe rules are otherwise finite and arithmetic." },
 "reasoning_over_luck": {"verdict": "fail", "evidence": "**What humans can infer:**\n- **Charm feedback** says 'had bites' only for bitten humans. A wolf can never have bites, so 'no bites' is consistent with both wolf and unbitten human. The positive signal only clears a human and never identifies a wolf.\n- **Exposure** is the only hard evidence of a wolf. It fires with probability 2/N per night (1/3 at 6 players, 2/7 at 7). It is decided entirely by the random draw.\n- **Day 1** lynch is a blind 2/5 guess.\n- **Salve** saves are blind 1/4 guesses.\n\n**Sensitivity to luck (6 players).** The human win rate is about 0.31 overall. Conditioned on luck, it is about 0.65 if a wolf is exposed on night 1 and about 0.15 if not. Most of the human outcome is set by the exposure draw and the day-1 coin flip, not by reasoning.\n\n**Both sides playing well.** Wolves bloc-vote and focus-fire; humans vote blindly and act on exposures. The result is then mostly 'did the random exposure land on a wolf'.\n\n**Wolf decisions** do carry real reasoning: Maul versus Bite versus a disguising Salve under exposure risk. But the human side, which needs to infer, has almost nothing reliable to infer from. Vote patterns help only marginally, because wolves can blend in with a bloc. A strong human reasoner is not clearly favoured over a random voter." },
 "required_changes": [
  "Give humans an inference source that good play can exploit, not a random draw. For example: Charm reports 'your target is a Wolf / is not a Wolf' (or 'played Bite or Maul last night: yes/no'), or replace the random exposure with a vote-chosen inspection. Keep at most 1 random draw per round, but do not make it the main way wolves are found.",
  "Rebalance the kill and infection economy. Raise wound_limit to 3 or allow at most one Maul per night in total. Make infection need bites >= 3 from at least 2 different nights and reveal publicly that 'someone was infected', so Bite is not a hidden double swing that wins 6-player games by round 2.",
  "Remove the 'any wolf alive at round 6 = wolves win' timeout. Either make the game end only on a parity or elimination condition, or raise max_rounds and give humans the win if they reach the last round with living_humans >= 2 x living_wolves.",
  "Scale the wolf count with players (1 wolf at 6 players, 2 at 7, or a fixed 7 players), and show by path calculation that the always-bloc-vote, always-focus-Maul or focus-Bite wolf policy wins no more than about 55%.",
  "Cut hidden elements to 3. For example: drop the per-player bites counter and infection (or make bites public), and fold the Charm feedback into the inspection mechanic. Keep roles, night actions and the wolf den as the three.",
  "State explicitly: whether a wolf may Maul another wolf; that a newly infected wolf joins the den from the next night; and that death (step 14) is checked before infection (step 15)."
 ]}
```
````
