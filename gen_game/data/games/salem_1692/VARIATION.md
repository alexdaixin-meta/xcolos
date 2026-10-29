# Variation: Salem 1692: Gossip, Gallows and Hex

One hidden Witch, one Constable and Townsfolk. Each round a random player privately gets a clue about the Witch's location. The Witch might be that player, and the Witch can secretly invert one clue (two at N=6). Players talk, accuse, try the majority suspect and survive the night.

Players: 5 to 6, best with 5

## Review of the original

Salem 1692 is a 4-12 player hidden-role card game. Secret Witches try to kill the town while townsfolk play accusation cards to force reveals of each other's Tryal cards, with conspiracy card-passing and nightly kill/save phases. The reviewed variation reduced it to 5-6 players with 1 Witch, 1 Constable, a private Gossip clue each round, simultaneous talk, accusation tokens with a majority trial, and a night kill/protect.

- **non_degenerate**: bad. In the reviewed variation the Gossip was always a non-Witch, so a lone claim was always true and two claims put the Witch among the two claimants. The mechanical Town policy 'trust the lone claim, or lynch a claimant if two claim, then lynch the remaining candidate' never loses at N=5 against any Witch policy: silent, fake claim, random accusations or voting with the Town. Seats are neutral because roles are random, but the Town side has a forced win.
- **skill_sensitive**: weak. Town skill matters a little at N=6. Witch skill hardly matters: Town wins about 100% at N=5 and about 85-90% at N=6 whatever the Witch does. A skilled Witch is not reliably better than a careless one.
- **headroom**: weak. Town play is essentially solved by one deduction rule. The Witch has no lever that improves results, so there is no room to get better on one side and no realistic way to win on the other.
- **reasoning_dependent**: weak. There is hidden state (roles, the Gossip, the clue), but the clue is always truthful, so the inference is mechanical. What is left to decide comes down to coin-flip lynches between symmetric claimants and the night guess, not to modelling a deceptive opponent.
- **verifiable**: good. Trials follow from vote counts against T = floor(L/2)+1, deaths from comparing the kill and protect targets, and wins from reveal, parity or the round count. All of it is arithmetic on tracked numbers.
- **fits_platform**: good. It is turn-based and text-only, with simultaneous polls, private info, elimination and no board. About 13 steps, 4 choice steps and up to 6 rounds, all within limits. The one loose end was the Constable's previous protection target, an unstated hidden record.

## Problems

- P1: The Gossip is never the Witch, so a lone Gossip claim is always truthful and the Town can trust it blindly.
- P2: Any Witch counter-claim proves the Witch is one of two claimants. The Witch has no bluff that survives deduction.
- P3: The Witch has no counterplay against the information flow. Town wins about 100% at N=5 and about 85-90% at N=6 under good play, a lottery-free but one-sided game.
- P4: Because of P3, Witch skill is nearly irrelevant and Town play is a fixed recipe. Opponent modelling is absent.
- P5: The Constable's 'not the same player as last night' restriction needs a hidden stored target that was never declared as a hidden element. It adds state without adding much decision.
- P6: N=6 gives the Town one more lynch than N=5, so one Witch power level cannot balance both sizes.

## Changes

- The Gossip is drawn uniformly from ALL living players, including the Witch. A Witch-Gossip is told only 'You are the Gossip' and receives no result. (fixes: P1): Any lone claim may now be the Witch inventing a clue. Uncontested claims carry real risk, since the prior chance the claimant is the Witch is 1/L.
- Add the HEX, a once-per-game Witch power (twice at N=6, never twice in a row). The Witch privately decides, before round 1 and then during each night for the next round, whether to hex the next Gossip result. A hexed result given to a Town Gossip is inverted (IS becomes IS NOT and vice versa). The Gossip is not told. (fixes: P2, P3, P4): Even an honest Gossip can unknowingly point the wrong way, and only the Witch knows when. The Witch must time the hex, and the Town must judge which round's clue to trust from how claims, votes and deaths fit together. At N=5, if the Witch hexes round 1 with probability 1/2, the round 1 claim leaves every other player equally likely (1/5 each), so blind trust fails. If the Witch never hexes early, later clues become suspect instead.
- The hex is spent even when the Witch turns out to be the Gossip that round. (fixes: P4): Hexing carries a real cost and risk, and the rule saves an engine refund operation.
- Remove the Constable's no-repeat restriction. The Constable may protect any living player except themself, any number of times. (fixes: P5): This removes an undeclared private record and keeps hidden elements at 3. The interesting choice, whom the Witch will target, remains.
- Give the Witch 1 hex at N=5 and 2 hexes at N=6. (fixes: P6): N=6 gives the Town about one extra lynch attempt before parity. A second hex offsets it.
- Fold the hex decision into the night poll: everyone answers 'hex: yes/no' alongside their night target, and only the Witch's answer counts. Round 1's hex is decided in a setup step. (fixes: P3): Keeps choice steps at 4 per round, and nobody can tell who holds the power by who is asked.

## Kept from the original

- A hidden Witch among townsfolk, revealed by public accusation reaching a threshold (accusation tokens play the role of red accusation cards and the 7-accusation trigger).
- A night phase where the Witch picks a kill and the Constable picks a save, with death only if they differ.
- A trial reveals the accused's role. Town wins when the Witch is exposed, and the Witch wins by thinning the town to parity.
- Free bluffing talk: anyone may claim roles or clues, lie or accuse.
- The Witch's ability to corrupt what the town learns, echoing the Conspiracy's corruption of the town.

## The variation's rules

SETUP. Seat the players in a circle numbered 1 to N (N = 5 or 6). Deal hidden roles at random: exactly 1 Witch, 1 Constable, and the rest Townsfolk. Each player sees only their own role. Every player starts alive with 0 accusation tokens. The Witch starts with HEXES = 1 if N = 5, or HEXES = 2 if N = 6. The game lasts at most 6 rounds.

DAWN (once, before round 1). Every player privately answers 'hex: yes' or 'hex: no'. Only the Witch's answer counts: if yes, the round-1 hex is active and the Witch's HEXES falls by 1. Everyone else's answer is ignored. Everyone answers so that nobody can tell who holds the power.

TERMS. L is the number of living players at the moment of checking. A player's two living neighbours are the nearest living player clockwise and the nearest living player counter-clockwise, skipping dead players. When L = 3, these are the other two living players. Dead players cannot speak, vote, be voted for or hold tokens.

EACH ROUND, in this order:
1. GOSSIP DRAW. The engine draws one living player uniformly at random from ALL living players, the Witch included. That player is the Gossip and is told so privately. Nobody else learns who the Gossip is.
2. GOSSIP RESULT. If the Gossip is the Witch, the Witch is told only 'You are the Gossip' and gets no result. Otherwise the engine works out the TRUE statement, either 'The Witch IS one of your two living neighbours' or 'The Witch is NOT one of your two living neighbours'. If the hex is active this round, the Gossip is told the opposite statement. If not, the Gossip is told the true statement. The Gossip is never told whether a hex was active. The hex then ends. It lasts only one round, and it is spent even if the Witch was the Gossip.
3. TALK A. Every living player writes one short message at the same time, without seeing the others. Then all are shown to everyone. Anyone may claim to be the Gossip, claim any role or result, accuse, lie or stay silent. Nothing said is binding.
4. TALK B. Every living player writes a second short message at the same time, having seen all Talk A messages but not each other's Talk B messages. Then all are shown.
5. ACCUSATION. All living players simultaneously name one other living player, never themselves. Each named player gains 1 token per vote received. Tokens are kept from round to round.
6. ANNOUNCE. All votes and every living player's token total are made public.
7. TRIAL CHECK. Let T = floor(L/2) + 1 (4 with 6 alive, 3 with 5 or 4 alive, 2 with 3 alive). If exactly one living player holds strictly more tokens than every other living player AND holds at least T tokens, that player is tried. Otherwise nobody is tried and all tokens are kept.
8. TRIAL. The tried player's role is revealed to all. If they are the Witch, the game ends immediately and the Town wins. Otherwise they are hanged (eliminated) and every living player's tokens reset to 0.
9. PARITY CHECK. If the Witch is alive and at most 1 living non-Witch remains, the game ends and the Witch wins.
10. NIGHT. Every living player privately names one living player other than themself as a target, and privately answers 'hex: yes' or 'hex: no'. Only these answers count:
   - The Witch's target is the kill.
   - The Constable's target is the protection. The Constable may protect the same player on any number of nights. If the Constable is dead, there is no protection.
   - The Witch's hex answer counts only if it is yes, the Witch has HEXES of at least 1, and the hex was NOT active in the current round. In that case the hex is active for the next round and HEXES falls by 1. Otherwise no hex is active next round.
   All other targets and answers are ignored.
11. NIGHT RESOLUTION. If the kill target differs from the protection target, the kill target dies, their role is revealed to all, and their tokens are removed. Other players' tokens are unchanged. If the two targets are the same, nobody dies, and it is announced only that the night passed peacefully.
12. PARITY CHECK. Repeat step 9.
13. ROUND END. If this was round 6 and the game has not ended, the Witch wins. Otherwise begin the next round.

The number of hexes the Witch has left and whether a hex is active are never announced.

Objective: Team game with no draws. The Town (the Constable and all Townsfolk, alive or dead) wins together the moment the Witch is tried and revealed. The Witch wins if, after a trial or a night, the Witch is alive with at most 1 living non-Witch, or if the Witch is still alive at the end of round 6.

Expected effect: Every clue is now doubtful in two ways: the claimant may be the Witch (chance 1/L), or the clue may have been hexed (a round the Witch chooses).

At N=5 with the hex mixed half-and-half in round 1, a lone claim leaves all four other players at 1/5 each, the same as no clue, so 'trust the lone claim' loses about 4 times in 5 in that line. If the Witch saves the hex, the round-1 clue is reliable except when the Witch was the Gossip (1/5), but the Town must then doubt round 2. A Town that waits a round (no majority, absorb a night kill) gains a cleaner clue at the cost of a life.

Rough estimates, to be confirmed by simulation:
- N=5: Town about 50-60% (one round-1 lynch at roughly 1/4 to 2/5 depending on Witch timing, then a near coin-flip at L=3, or an extra round when the Constable saves).
- N=6 with 2 hexes: a similar range.

Simple policies all lose sometimes:
- Witch 'always hex round 1' is beaten by a Town that discounts round 1 and trusts round 2.
- Witch 'never hex' makes clues reliable about 4/5 of the time.
- Witch 'counter-claim Gossip' still exposes the Witch to a 50% lynch.
- Witch 'stay silent' lets an honest clue stand.
- Town 'trust any lone claim' and Town 'never lynch round 1' each lose to the matching Witch timing.

Talk passes both tests. Players disagree because the Witch wants a Townsperson hanged while each Townsperson wants the Witch hanged and knows only their own innocence. A Townsperson who simply follows the first confident Gossip claim can hang a fellow Townsperson: the claim may come from the Witch, or from an honest Gossip whose result the Witch hexed. Talk lets players test claims against earlier clues, revealed roles and voting patterns. The Witch must decide when to stay silent, when to fake a claim, and when to back a clue it knows was inverted.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
