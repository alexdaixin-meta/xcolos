# 06 design

- time: 2026-10-28T01:38:47+00:00 (107.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 afa8cb4227b334ff, reply sha256 76faa974b5d33a31

## Sent

````
Original game: Salem 1692
Players in the original: 4 to 12

Original rules:
Each player gets face-down Tryal cards; any Witch card makes you a Witch forever, even if later lost. One Town Hall power each. Deal 3 playing cards. Put Conspiracy in deck and Night at bottom; set Black Cat aside. At Dawn, Witches eyes-open secretly give Black Cat to any player. First player is Black Cat holder. On your turn you must either draw 2 cards (Black cards revealed and resolved instantly) or play any number of cards on others, never yourself. Green cards are one-shot, Blue stay, Red are accusations. At 7 accusations the accuser reveals one of that player's Tryal cards; if Witch revealed, that player dies. When Conspiracy is drawn, reveal one Tryal on Black Cat holder, then each player takes one unrevealed Tryal from left, becoming Witch if they gain a Witch card. When Night is drawn, all close eyes, Witches choose a kill, Constable chooses a save; if different player, victim dies. Witches win when all non-Witches dead; Town wins when all Witch Tryal cards are revealed.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: The Gossip is always a non-Witch, so a true Gossip claim is always truthful. Two claims in one round prove the Witch is one of the two claimants.

N=5 (1 Witch, 1 Constable, 3 Townsfolk). The Gossip has 4 living others: 2 neighbours and 2 non-neighbours. Either result therefore leaves a candidate set S of exactly 2 players.

Case A, the Witch stays silent:
- The real Gossip claims, giving S = {X, Y}.
- Round 1: the 4 non-Witches all vote X, giving 4 tokens against T=3, so X is tried.
  - X is the Witch (50%): Town wins.
  - X is not (50%): X is revealed as Town, so Y is certainly the Witch.
- Night: the Witch kills one player. L=3: Witch plus 2 Town. Parity does not trigger.
- Round 2: T=2. Both Town vote Y, giving Y 2 tokens against at most 1 for anyone else. Y is tried and Town wins.

Case B, the Witch counter-claims Gossip:
- Two claimants mean the Witch is one of them.
- Town lynches one: right 50%. If wrong, the same Round 2 finish follows. Town wins.

The Witch cannot block a lynch, because 4 votes beat T=3 and the Witch has only 1 vote. Silence is no better for the Witch than claiming.

WINNER-RULE table, Town policy 'trust the lone Gossip claim, or lynch a claimant if two claim; then lynch the remaining candidate':
- Witch silent: Town wins.
- Witch fakes a Gossip claim: Town wins.
- Witch accuses randomly: Town wins.
- Witch votes with the Town: Town wins.
This mechanical policy never loses at N=5, and so fails the check.

N=6 (1 Witch, 1 Constable, 4 Town). P(Witch among the 2 neighbours of the 5 others) = 2/5:
- S size 2 (p=0.4): a wrong lynch leaves L=5. The night kill leaves L=4: Witch plus 3 Town, and the Witch is now identified. Round 2: T=3, and 3 votes try the Witch. Town wins about 100%.
- S size 3 (p=0.6): first lynch right 1/3. If wrong, the candidates fall to 2. Round 2 adds a new Gossip, whose result usually splits the two (only one is a neighbour), plus 50% even if it does not. The Constable can also save. Rough estimate: Town wins about 75-85% of this branch.
- Overall Town wins about 85-90% at N=6 and about 100% at N=5.

There is no seat edge, because roles are random. Still, the Witch side cannot realistically win against competent Town play. The 'social deduction' label is undercut by the numbers.
- reasoning_over_luck FAILED: With all sides playing the intended good strategy, Town wins about 100% at N=5 and about 85-90% at N=6 (see balanced). The Witch's reasoning is therefore nearly irrelevant: a skilled Witch is not clearly favoured over an unskilled one, because no bluff survives the 'two claimants means one is the Witch' deduction.

Town's inference is real but mechanical. The residual uncertainty, in the N=6 S=3 branch, is settled by:
- coin-flip lynches between symmetric claimants who make identical 'I'm Town, it's the other one' arguments;
- the 1/3 versus 2/5 Gossip geometry chosen by the random draw;
- the Witch-versus-Constable night guess.

So there is something to infer, but there is almost no opponent modelling on the Witch side. The outcome hinges on the deduction from the Gossip draw rather than on contested reasoning.
- change: Draw the Gossip uniformly from ALL living players, including the Witch. If the Witch is drawn, it is told it is the Gossip and receives no true result. A lone claim can then be a lie, and a double claim no longer pins the Witch to two players.
- change: Weaken the information: the Gossip learns 'the Witch IS / IS NOT among these 3 players' about a random set of 3 living others, OR the result is wrong with a stated probability such as 1 in 3.
- change: Give the Witch side real counterplay. Options: a second Witch at N=6 (the Witches know each other and the parity check counts living Witches against living non-Witches), OR a once-per-game Witch 'frame' that replaces the Gossip result with a false one.
- change: Re-run the N=5 and N=6 analysis after the changes and show that the Town win rate under good play is roughly 40-60%, with no fixed Town or Witch policy that never loses.
- change: State explicitly that the Constable's previous protection target is private to the Constable, and count it in hidden_elements if the engine stores it privately.
The variation that was reviewed: Salem 1692: Gossip and Gallows (revised): SETUP. Seat the players in a circle, numbered 1 to N (N = 5 or 6). Deal hidden roles at random: exactly 1 Witch, 1 Constable, and the rest Townsfolk. Each player sees only their own role. Every player starts alive with 0 accusation tokens. The game lasts at most 6 rounds.

TERMS. L is the number of living players at the moment of checking. A player's 'living neighbours' are the nearest living player clockwise and the nearest living player counter-clockwise, skipping dead players. When L = 3, these are simply the other two living players. Dead players take no further part, cannot vote, cannot be voted for and hold no tokens.

EACH ROUND, in this order:
1. GOSSIP DRAW. The engine draws one living player uniformly at random from the living players who are NOT the Witch. That player is the Gossip and is told so privately. Nobody else learns who the Gossip is.
2. GOSSIP RESULT. The Gossip is privately told either 'The Witch IS one of your two living neighbours' or 'The Witch is NOT one of your two living neighbours'. Nobody else learns the result.
3. TALK A. Every living player writes one short message at the same time, without seeing the others. Then all messages are shown to everyone. Players may claim to be the Gossip, claim any role, accuse, lie or stay silent. Nothing said is binding.
4. TALK B. Every living player again writes one short message at the same time, having seen all the Talk A messages but not each other's Talk B messages. Then all are shown to everyone.
5. ACCUSATION. All living players simultaneously name one other living player, never themselves. Each named player gains 1 accusation token per vote received. Tokens from earlier rounds are kept.
6. ANNOUNCE. Every vote and every living player's token total are made public.
7. TRIAL CHECK. Let T = floor(L/2) + 1: T is 4 when 6 are alive, 3 when 5 or 4 are alive, and 2 when 3 are alive. If exactly one living player holds strictly more tokens than every other living player, AND that player holds at least T tokens, that player is tried. Otherwise nobody is tried this round, and every player keeps their tokens. This applies both to a tie for the most tokens and to a sole leader with fewer than T tokens.
8. TRIAL. The tried player's role is revealed to all. If they are the Witch, the game ends immediately and the Town wins. Otherwise they are hanged (eliminated), and every living player's tokens reset to 0.
9. PARITY CHECK. If the Witch is alive and there is at most 1 living non-Witch, the game ends and the Witch wins.
10. NIGHT. Every living player privately names one living player as their night target. Only two choices count:
    - The Witch's choice is the kill. It must be a living player other than the Witch.
    - The Constable's choice is the protection. It must be a living player other than the Constable, and it may NOT be the same player the Constable protected on the previous night.
    Everyone else's choice is ignored; everyone names a target so that nobody can tell who holds an active role. If the Constable is dead, there is no protection.
11. NIGHT RESOLUTION. If the kill target is different from the protection target, the kill target dies, their role is revealed to all, and their tokens are removed. The other players' tokens are unchanged. If the two targets are the same, nobody dies, and it is announced only that the night passed peacefully. The engine records the Constable's protection target for the next night's restriction.
12. PARITY CHECK. Repeat the check in step 9.
13. ROUND END. If this was round 6 and the game has not ended, the Witch wins. Otherwise begin the next round. Winner: Team game, no draws. The Town (the Constable and all Townsfolk, alive or dead) wins together the moment the Witch is tried and revealed. The Witch wins if, after a trial or a night, the Witch is alive and at most 1 non-Witch is alive, or if the Witch is still alive at the end of round 6.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Salem 1692 is a 4-12 player hidden-role card game. Secret Witches try to kill the town while townsfolk play accusation cards to force reveals of each other's Tryal cards, with conspiracy card-passing and nightly kill/save phases. The reviewed variation reduced it to 5-6 players with 1 Witch, 1 Constable, a private Gossip clue each round, simultaneous talk, accusation tokens with a majority trial, and a night kill/protect.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the reviewed variation the Gossip was always a non-Witch, so a lone claim was always true and two claims put the Witch among the two claimants. The mechanical Town policy 'trust the lone claim, or lynch a claimant if two claim, then lynch the remaining candidate' never loses at N=5 against any Witch policy: silent, fake claim, random accusations or voting with the Town. Seats are neutral because roles are random, but the Town side has a forced win."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Town skill matters a little at N=6. Witch skill hardly matters: Town wins about 100% at N=5 and about 85-90% at N=6 whatever the Witch does. A skilled Witch is not reliably better than a careless one."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Town play is essentially solved by one deduction rule. The Witch has no lever that improves results, so there is no room to get better on one side and no realistic way to win on the other."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "There is hidden state (roles, the Gossip, the clue), but the clue is always truthful, so the inference is mechanical. What is left to decide comes down to coin-flip lynches between symmetric claimants and the night guess, not to modelling a deceptive opponent."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trials follow from vote counts against T = floor(L/2)+1, deaths from comparing the kill and protect targets, and wins from reveal, parity or the round count. All of it is arithmetic on tracked numbers."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is turn-based and text-only, with simultaneous polls, private info, elimination and no board. About 13 steps, 4 choice steps and up to 6 rounds, all within limits. The one loose end was the Constable's previous protection target, an unstated hidden record."
    }
  ],
  "problems": [
    "P1: The Gossip is never the Witch, so a lone Gossip claim is always truthful and the Town can trust it blindly.",
    "P2: Any Witch counter-claim proves the Witch is one of two claimants. The Witch has no bluff that survives deduction.",
    "P3: The Witch has no counterplay against the information flow. Town wins about 100% at N=5 and about 85-90% at N=6 under good play, a lottery-free but one-sided game.",
    "P4: Because of P3, Witch skill is nearly irrelevant and Town play is a fixed recipe. Opponent modelling is absent.",
    "P5: The Constable's 'not the same player as last night' restriction needs a hidden stored target that was never declared as a hidden element. It adds state without adding much decision.",
    "P6: N=6 gives the Town one more lynch than N=5, so one Witch power level cannot balance both sizes."
  ],
  "changes": [
    {
      "what": "The Gossip is drawn uniformly from ALL living players, including the Witch. A Witch-Gossip is told only 'You are the Gossip' and receives no result.",
      "why": "Any lone claim may now be the Witch inventing a clue. Uncontested claims carry real risk, since the prior chance the claimant is the Witch is 1/L.",
      "fixes": "P1"
    },
    {
      "what": "Add the HEX, a once-per-game Witch power (twice at N=6, never twice in a row). The Witch privately decides, before round 1 and then during each night for the next round, whether to hex the next Gossip result. A hexed result given to a Town Gossip is inverted (IS becomes IS NOT and vice versa). The Gossip is not told.",
      "why": "Even an honest Gossip can unknowingly point the wrong way, and only the Witch knows when. The Witch must time the hex, and the Town must judge which round's clue to trust from how claims, votes and deaths fit together. At N=5, if the Witch hexes round 1 with probability 1/2, the round 1 claim leaves every other player equally likely (1/5 each), so blind trust fails. If the Witch never hexes early, later clues become suspect instead.",
      "fixes": "P2, P3, P4"
    },
    {
      "what": "The hex is spent even when the Witch turns out to be the Gossip that round.",
      "why": "Hexing carries a real cost and risk, and the rule saves an engine refund operation.",
      "fixes": "P4"
    },
    {
      "what": "Remove the Constable's no-repeat restriction. The Constable may protect any living player except themself, any number of times.",
      "why": "This removes an undeclared private record and keeps hidden elements at 3. The interesting choice, whom the Witch will target, remains.",
      "fixes": "P5"
    },
    {
      "what": "Give the Witch 1 hex at N=5 and 2 hexes at N=6.",
      "why": "N=6 gives the Town about one extra lynch attempt before parity. A second hex offsets it.",
      "fixes": "P6"
    },
    {
      "what": "Fold the hex decision into the night poll: everyone answers 'hex: yes/no' alongside their night target, and only the Witch's answer counts. Round 1's hex is decided in a setup step.",
      "why": "Keeps choice steps at 4 per round, and nobody can tell who holds the power by who is asked.",
      "fixes": "P3"
    }
  ],
  "keeps": [
    "A hidden Witch among townsfolk, revealed by public accusation reaching a threshold (accusation tokens play the role of red accusation cards and the 7-accusation trigger).",
    "A night phase where the Witch picks a kill and the Constable picks a save, with death only if they differ.",
    "A trial reveals the accused's role. Town wins when the Witch is exposed, and the Witch wins by thinning the town to parity.",
    "Free bluffing talk: anyone may claim roles or clues, lie or accuse.",
    "The Witch's ability to corrupt what the town learns, echoing the Conspiracy's corruption of the town."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core is a sound one-hidden-role deduction game. Adding a Witch-capable Gossip and a timed hex gives the Witch real counterplay within the limits."
  },
  "variation": {
    "name": "Salem 1692: Gossip, Gallows and Hex",
    "summary": "One hidden Witch, one Constable and Townsfolk. Each round a random player privately gets a clue about the Witch's location. The Witch might be that player, and the Witch can secretly invert one clue (two at N=6). Players talk, accuse, try the majority suspect and survive the night.",
    "players": {
      "min": 5,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP. Seat the players in a circle numbered 1 to N (N = 5 or 6). Deal hidden roles at random: exactly 1 Witch, 1 Constable, and the rest Townsfolk. Each player sees only their own role. Every player starts alive with 0 accusation tokens. The Witch starts with HEXES = 1 if N = 5, or HEXES = 2 if N = 6. The game lasts at most 6 rounds.\n\nDAWN (once, before round 1). Every player privately answers 'hex: yes' or 'hex: no'. Only the Witch's answer counts: if yes, the round-1 hex is active and the Witch's HEXES falls by 1. Everyone else's answer is ignored. Everyone answers so that nobody can tell who holds the power.\n\nTERMS. L is the number of living players at the moment of checking. A player's two living neighbours are the nearest living player clockwise and the nearest living player counter-clockwise, skipping dead players. When L = 3, these are the other two living players. Dead players cannot speak, vote, be voted for or hold tokens.\n\nEACH ROUND, in this order:\n1. GOSSIP DRAW. The engine draws one living player uniformly at random from ALL living players, the Witch included. That player is the Gossip and is told so privately. Nobody else learns who the Gossip is.\n2. GOSSIP RESULT. If the Gossip is the Witch, the Witch is told only 'You are the Gossip' and gets no result. Otherwise the engine works out the TRUE statement, either 'The Witch IS one of your two living neighbours' or 'The Witch is NOT one of your two living neighbours'. If the hex is active this round, the Gossip is told the opposite statement. If not, the Gossip is told the true statement. The Gossip is never told whether a hex was active. The hex then ends. It lasts only one round, and it is spent even if the Witch was the Gossip.\n3. TALK A. Every living player writes one short message at the same time, without seeing the others. Then all are shown to everyone. Anyone may claim to be the Gossip, claim any role or result, accuse, lie or stay silent. Nothing said is binding.\n4. TALK B. Every living player writes a second short message at the same time, having seen all Talk A messages but not each other's Talk B messages. Then all are shown.\n5. ACCUSATION. All living players simultaneously name one other living player, never themselves. Each named player gains 1 token per vote received. Tokens are kept from round to round.\n6. ANNOUNCE. All votes and every living player's token total are made public.\n7. TRIAL CHECK. Let T = floor(L/2) + 1 (4 with 6 alive, 3 with 5 or 4 alive, 2 with 3 alive). If exactly one living player holds strictly more tokens than every other living player AND holds at least T tokens, that player is tried. Otherwise nobody is tried and all tokens are kept.\n8. TRIAL. The tried player's role is revealed to all. If they are the Witch, the game ends immediately and the Town wins. Otherwise they are hanged (eliminated) and every living player's tokens reset to 0.\n9. PARITY CHECK. If the Witch is alive and at most 1 living non-Witch remains, the game ends and the Witch wins.\n10. NIGHT. Every living player privately names one living player other than themself as a target, and privately answers 'hex: yes' or 'hex: no'. Only these answers count:\n   - The Witch's target is the kill.\n   - The Constable's target is the protection. The Constable may protect the same player on any number of nights. If the Constable is dead, there is no protection.\n   - The Witch's hex answer counts only if it is yes, the Witch has HEXES of at least 1, and the hex was NOT active in the current round. In that case the hex is active for the next round and HEXES falls by 1. Otherwise no hex is active next round.\n   All other targets and answers are ignored.\n11. NIGHT RESOLUTION. If the kill target differs from the protection target, the kill target dies, their role is revealed to all, and their tokens are removed. Other players' tokens are unchanged. If the two targets are the same, nobody dies, and it is announced only that the night passed peacefully.\n12. PARITY CHECK. Repeat step 9.\n13. ROUND END. If this was round 6 and the game has not ended, the Witch wins. Otherwise begin the next round.\n\nThe number of hexes the Witch has left and whether a hex is active are never announced.",
    "objective": "Team game with no draws. The Town (the Constable and all Townsfolk, alive or dead) wins together the moment the Witch is tried and revealed. The Witch wins if, after a trial or a night, the Witch is alive with at most 1 living non-Witch, or if the Witch is still alive at the end of round 6.",
    "expected_effect": "Every clue is now doubtful in two ways: the claimant may be the Witch (chance 1/L), or the clue may have been hexed (a round the Witch chooses).\n\nAt N=5 with the hex mixed half-and-half in round 1, a lone claim leaves all four other players at 1/5 each, the same as no clue, so 'trust the lone claim' loses about 4 times in 5 in that line. If the Witch saves the hex, the round-1 clue is reliable except when the Witch was the Gossip (1/5), but the Town must then doubt round 2. A Town that waits a round (no majority, absorb a night kill) gains a cleaner clue at the cost of a life.\n\nRough estimates, to be confirmed by simulation:\n- N=5: Town about 50-60% (one round-1 lynch at roughly 1/4 to 2/5 depending on Witch timing, then a near coin-flip at L=3, or an extra round when the Constable saves).\n- N=6 with 2 hexes: a similar range.\n\nSimple policies all lose sometimes:\n- Witch 'always hex round 1' is beaten by a Town that discounts round 1 and trusts round 2.\n- Witch 'never hex' makes clues reliable about 4/5 of the time.\n- Witch 'counter-claim Gossip' still exposes the Witch to a 50% lynch.\n- Witch 'stay silent' lets an honest clue stand.\n- Town 'trust any lone claim' and Town 'never lynch round 1' each lose to the matching Witch timing.\n\nTalk passes both tests. Players disagree because the Witch wants a Townsperson hanged while each Townsperson wants the Witch hanged and knows only their own innocence. A Townsperson who simply follows the first confident Gossip claim can hang a fellow Townsperson: the claim may come from the Witch, or from an honest Gossip whose result the Witch hexed. Talk lets players test claims against earlier clues, revealed roles and voting patterns. The Witch must decide when to stay silent, when to fake a claim, and when to back a clue it knows was inverted."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 4,
    "attributes": 13,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 6
  }
}
```
````
