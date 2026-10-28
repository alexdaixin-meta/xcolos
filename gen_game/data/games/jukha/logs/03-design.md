# 03 design

- time: 2026-10-28T03:50:24+00:00 (56.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 61be43421b9414cc, reply sha256 a985d7bacf020827

## Sent

````
Original game: Jukha
Players in the original: 3 to 13

Original rules:
Use 4 cards of each rank per player plus one Joker in total. Deal all cards clockwise so player left of dealer gets 5, others 4; keep hands hidden. Suits irrelevant. On a turn, if you have 4 cards and they are all equal, show them and exit and cannot lose. Otherwise you must request a card from the player who currently has 5 cards. You may name a rank you want. The 5-card player must offer one card face down and may claim any rank, truthfully or not. You may take it and end your turn with 5 cards, or reject it to ask for a second. If second offered, you must take one of the two offered and other returns. You may instead ask for a third; then you must take the third and both first return. After your turn you have 5 and are asked next. Having 4 of a kind plus extra does not let you exit; you need exactly 4 at start of your turn. Joker cannot exit. Play until only two players remain; they both lose.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: CORE DECISION. A giver holding AAAAX (four A plus one odd card) wins at their next exit check only if the taker takes X. The giver's hand does not change while they sit out the next turn. The giver has two kinds of offer: (XA) X and one A, which leaves AAA unoffered, so blind always gives the taker an A; or (AA) two A, which leaves A,A,X unoffered, so blind gives X with probability 1/3. Claims can be lies, so a taker choosing between the offers is effectively at 1/2.

Giver win probability:
| Giver offer | Taker picks an offer at random | Taker goes blind |
|---|---|---|
| XA | 1/2 | 0 |
| AA | 0 | 1/3 |

Mixed equilibrium: (1-b)/2 = b/3 gives b = 0.6, value 0.2. No option is strictly better.

THOUGHTLESS POLICIES.
- Always Offer 1: a giver puts X in slot 1 and wins every time. Exploitable, so it loses.
- Always blind: the giver switches to AA and wins 1/3 per attempt. Blind still hands the taker whatever the giver left unoffered, so dumping the Joker reaches them 1/3 of the time. The policy also builds only at random. It loses whenever an opponent completes, so it does not never-lose.
- Always request 'none' or always claim truthfully: these only leak information.
No policy wins or draws every time. All three players can realistically exit.

SEAT EDGE (fails). After 30 turns the taker of turn 30 holds 5 cards. Taker of turn t = first giver + t (mod 3), so for t = 30 it is always the FIRST GIVER. Fallback counts the largest group from 5 cards against everyone else's 4. That player also gets the last free choice of which card to take.
- Minimum scores: a 5-card hand without the Joker has max group at least 2 (5 cards into 3 ranks), and at least 2 with the Joker. A 4-card hand with the Joker has 3 ranked cards, so max group at least 1 and score at least -1.
- Example: holding AAAAJ, the 5-card player scores 4-2 = 2, while a 4-card AAAJ holder scores 1.
Blocking play (taker goes blind 60% when the giver looks near-complete) makes 30-turn fallbacks plausible. That turns this deterministic positional edge, fixed by the random first-giver pick, into a real factor.

The opening exit check is a negligible edge: P(4 dealt cards all one rank) = 3*C(4,4)/C(13,4) = 3/715.
- playable FAILED: Limits are met: 10 steps, 3 choice steps (request, offer+claims, take), 14 attributes, 1 hidden element (hidden hands are supported), 1 random draw per round (blind), 30 rounds. No board, clock or judge is needed. The game is finite: either an exit or 30 turns. Omitting free talk is defensible: requests and claims already give the giver and taker something to bluff about and infer from, and the third player has no decision that talk would coordinate.

Ambiguities that block complete play:
1. 'Two different cards' can be read as two different RANKS. Under that reading a giver with AAAAX is forced to offer X and A, and a giver with AAAA can never be asked for two. This changes the core block/complete dilemma.
2. It is not stated whether the taker's choice (Offer 1, Offer 2 or blind) is announced to the third player. 'Every public announcement' does not say whether it counts, and card-counting inference depends on it.
3. The fallback tie rule says 'the game is a draw' without saying whether a strictly lower third player also draws or loses.
4. Fallback compares a 5-card hand with 4-card hands without acknowledging this (see balanced).
- change: Fix the fallback seat edge: the taker of turn 30 is scored on the 4 cards they held at that turn's exit check, excluding the card received on turn 30. All three players are then scored on 4 cards. Alternatively, end the game after turn 30's exit check, before any card passes, so the last giver's 5-card hand is the only special case and is scored on their best 4 with an explicit rule stated.
- change: Reword the offer step to 'two distinct physical cards from your hand (they may be the same rank)', so a giver holding AAAAX may offer two A.
- change: State that the taker's choice (Offer 1, Offer 2 or blind) is announced publicly to all players, while the card's identity stays private to the giver and taker.
- change: Clarify the fallback tie: players tied for the top score draw, and any player with a strictly lower score loses.
The variation that was reviewed: Jukha Three: SETUP. Use 13 cards: four each of ranks A, B and C, plus one Joker. Assign the 3 players to seats 1, 2 and 3 at random; play passes 1 -> 2 -> 3 -> 1. Pick one seat at random to be the first giver. Shuffle and deal 5 cards to the first giver and 4 to each other player. Hands are private. Each player always knows only their own hand and every public announcement.

TURN ORDER. Each turn has a giver, who holds 5 cards, and a taker, the next player in seat order, who holds 4. On the first turn the giver is the first giver. After each turn, the taker of that turn becomes the giver of the next turn, and the next seat becomes the taker.

EACH TURN:
1. Exit check. If the taker's 4 cards are all the same rank (four A, four B or four C), the taker shows them and wins immediately; the game ends. The Joker never counts toward a set.
2. Request. The taker publicly names one rank they want (A, B or C), or says 'none'. This is not binding on anyone.
3. Offer. The giver chooses two different cards from their hand and places them face down as Offer 1 and Offer 2. For each, they publicly claim a rank (A, B, C or Joker), truthfully or not.
4. Take. The taker chooses one of three options: take Offer 1, take Offer 2, or 'blind', which means taking one card chosen uniformly at random from the giver's three cards that were not offered. The taker then privately sees the card they received. The cards not taken stay in the giver's hand, unrevealed to anyone else.
5. Pass. The chosen card moves from the giver's hand to the taker's hand. The taker now holds 5 cards and the giver holds 4.
6. Advance. The turn counter goes up by 1. If it reaches 30, the game ends with the fallback scoring below. Otherwise the next turn begins, with the old taker as the new giver.

FALLBACK SCORING (only if 30 turns pass with no exit). Each player reveals their hand and scores the number of cards in their largest same-rank group among A, B and C, counting at most 4. If they hold the Joker, they subtract 2. The highest score wins. If two or more players tie for the highest score, the game is a draw.

No free talk; the only public statements are requests and claims. Winner: The first player who begins their taking turn holding exactly four cards of one rank (A, B or C) wins, and the other two lose. If no one has done so after 30 turns, the single player with the highest score wins, where score = largest same-rank group (at most 4) minus 2 if holding the Joker. A tie for the top score is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
"original_summary": "Jukha is a 3-13 player hidden-hand passing game. Each turn a player draws one card from whoever holds five, choosing among face-down offers whose ranks the holder may lie about. A player who starts their turn with exactly four of a kind exits safely, and the last two players left lose.",
"review": [
{"criterion": "non_degenerate", "verdict": "weak", "evidence": "The core dilemma works. A giver holding AAAAX wins only if the taker takes X, and that gives a mixed equilibrium (taker goes blind 60% of the time, giver wins 0.2 per attempt) in which no pure policy is safe. Always taking Offer 1 is exploited by putting X in slot 1. Always blind loses to the giver offering two A's, and it builds only at random. The previous variation's fallback still had a deterministic seat edge. After 30 turns the first giver always holds 5 cards and is scored on its largest group, against 4-card hands for the others. Blocking play makes 30-turn games plausible, so this edge, fixed by the random first-giver pick, is a real factor."},
{"criterion": "skill_sensitive", "verdict": "good", "evidence": "Winning depends on tracking which ranks have moved, reading requests and claims (which may be lies), choosing between completing and blocking, and dumping the Joker when the taker is likely to go blind. The only randomness after the deal is the blind pick, and that pick is itself a choice. In the original 13-player version, long chains of passing diluted skill. Three players with three ranks concentrates it."},
{"criterion": "headroom", "verdict": "good", "evidence": "No pure strategy is optimal at the key decision. Card counting, bluffing on claims and timing requests keep rewarding better play. A weak player still completes a set sometimes, because the giver's equilibrium win chance per attempt is 0.2 and offers made at random leak cards."},
{"criterion": "reasoning_dependent", "verdict": "good", "evidence": "Hands are hidden and claims can be false. A player must infer the giver's holding from requests, claims, which offer the taker picked and what they themselves have received, and must model whether the taker will block or go blind."},
{"criterion": "verifiable", "verdict": "weak", "evidence": "An exit is plain arithmetic. The previous variation's fallback left the tie outcome unclear and compared a 5-card hand with 4-card hands. The phrase 'two different cards' could be read as two different ranks, which changes the core dilemma. Whether the taker's choice was announced was also left unstated."},
{"criterion": "fits_platform", "verdict": "good", "evidence": "The game is turn-based, text-only, uses hidden hands (supported) and one random draw per turn. It has 30 turns at most, about 11 steps and 3 choice steps per turn, and no board. The original's 3-13 players and 'last two lose' needed cutting to three players and a single winner, which the previous variation did."}
],
"problems": [
"P1 Seat edge at fallback: the taker of turn 30 is always the first giver, holds 5 cards, and is scored on its largest group against 4-card hands.",
"P2 Ambiguous offer rule: 'two different cards' can be read as two different ranks. That would force a giver holding AAAAX to offer X, collapsing the complete-or-block dilemma.",
"P3 Unstated public information: it is not said whether the taker's choice (Offer 1, Offer 2 or blind) is announced to the third player, and card counting depends on it.",
"P4 Unclear fallback tie: 'draw' does not say what happens to a strictly lower third player. The engine can only declare one winner or a draw."
],
"changes": [
{"what": "At the fallback, the player holding 5 cards (the taker of turn 30) counts its largest same-rank group only among the 4 cards it held at the exit check of turn 30, excluding the card it received that turn. The engine records that card as 'last received'. The Joker penalty still applies to whoever physically holds the Joker, so receiving it on turn 30 still costs 2.", "why": "Every player's group count then comes from exactly 4 cards. The last taker cannot gain a group card from the final pass, but it cannot escape the Joker either, so the final giver's dump remains a real move.", "fixes": "P1 Seat edge at fallback"},
{"what": "The offer step now reads: 'two distinct physical cards from your hand; they may be the same rank'.", "why": "A giver holding AAAAX may offer two A's. That keeps the equilibrium between offering X and an A, and offering two A's.", "fixes": "P2 Ambiguous offer rule"},
{"what": "The taker's choice (Offer 1, Offer 2 or blind) is announced publicly. The identity of the received card stays known only to the giver and the taker. A blind card is seen by the taker; the giver learns it by noticing which card left their hand.", "why": "This defines exactly what the third player can count.", "fixes": "P3 Unstated public information"},
{"what": "At the fallback, a single highest score wins and the other two lose. Any tie for the highest score makes the whole game a draw for all three players.", "why": "The engine supports one winner or a draw. This states the outcome for every player without needing co-winners.", "fixes": "P4 Unclear fallback tie"}
],
"keeps": [
"Hidden hands, and drawing from whoever holds 5 cards",
"Face-down offers with free (possibly false) rank claims, and the option to refuse the offers and take a blind card",
"You exit only with exactly four of a kind at the start of your turn; four of a kind plus an extra card does not count",
"A single Joker that can never complete a set, passed around as a liability",
"Non-binding requests naming the rank you want"
],
"recommendation": {"decision": "adapt", "kind": "none", "reason": "The previous variation's core bluff-and-block dilemma tested well. Only the fallback seat edge and three rule ambiguities needed fixing, and all fit inside the limits."},
"variation": {
"name": "Jukha Three (revised)",
"summary": "Three players pass cards from the 5-card holder to the next player. The giver offers two face-down cards with claimed ranks, which may be lies, and the taker picks one or takes a blind card. The first player to start a taking turn with four of a kind wins. If nobody does within 30 turns, a scoring fallback decides, and every player is scored on 4 cards.",
"players": {"min": 3, "max": 3, "suggested": 3},
"rules": "SETUP. Use 13 cards: four each of ranks A, B and C, plus one Joker. Assign the 3 players to seats 1, 2 and 3 at random; play passes 1 -> 2 -> 3 -> 1. Pick one seat at random to be the first giver. Shuffle and deal 5 cards to the first giver and 4 to each other player. Hands are private. Each player knows only their own hand, the cards they have personally given or received, and the public announcements listed below.\n\nTURN ORDER. Each turn has a giver, who holds 5 cards, and a taker, the next seat in order, who holds 4. On turn 1 the giver is the first giver. After each turn, that turn's taker becomes the next giver, and the following seat becomes the next taker.\n\nEACH TURN (turns are numbered from 1):\n1. Exit check. If the taker's 4 cards are all the same rank (four A, four B or four C), the taker shows them and wins at once, and the other two players lose. The Joker never counts toward a set.\n2. Request (public). The taker names one rank they want (A, B or C) or says 'none'. The request binds no one.\n3. Offer (public claims). The giver chooses two distinct physical cards from their hand; they may be the same rank. The giver places them face down as Offer 1 and Offer 2 and publicly claims a rank for each (A, B, C or Joker). Claims may be true or false.\n4. Take (public choice). The taker announces one of three options: 'Offer 1', 'Offer 2' or 'blind'. Blind means receiving one card chosen uniformly at random from the giver's three unoffered cards. The choice is announced to all players. Only the taker sees the received card. The giver knows which card left their hand. The third player learns only the announced choice. Cards not taken stay in the giver's hand unrevealed.\n5. Pass. The received card moves from the giver's hand to the taker's hand. Record this card privately as the taker's 'last received' card. The taker now holds 5 cards and the giver holds 4.\n6. Advance. Add 1 to the turn counter. If the counter has reached 30, go to FALLBACK. Otherwise begin the next turn.\n\nFALLBACK (only after 30 turns with no exit). All hands are revealed, and each player's score is computed as follows.\n- Group count. This is the largest number of cards of one rank (A, B or C) among the scored cards, at most 4. For the two players holding 4 cards, the scored cards are their whole hand. For the player holding 5 cards (the taker of turn 30), the scored cards are their 5 cards minus their 'last received' card, that is, the 4 cards they held at turn 30's exit check.\n- Joker penalty. The player who physically holds the Joker subtracts 2, whether or not it was their last received card.\n- Outcome. If exactly one player has the highest score, that player wins and the other two lose. If two or three players tie for the highest score, the whole game is a draw.\n\nThere is no free talk. The only public statements are requests, claims and the taker's choice.",
"objective": "The first player who begins their taking turn holding exactly four cards of one rank (A, B or C) wins, and the other two lose. If no one does so in 30 turns, scores are computed: largest same-rank group (at most 4) among the scored cards, where the 5-card holder excludes the card received on turn 30, minus 2 for whoever holds the Joker. A single top scorer wins and the others lose. Any tie for top is a draw for the whole game.",
"expected_effect": "The complete-or-block dilemma is unchanged: the giver holding AAAAX mixes between offering X and an A, and offering two A's, and the taker mixes between picking an offer and going blind. The equilibrium has the taker blind 60% of the time and the giver winning 0.2 per attempt. Scoring on 4 cards removes the deterministic seat edge at the fallback, so the random first-giver pick no longer decides long blocking games. The final giver can still try to dump the Joker on turn 30, and the final taker must weigh that risk. Announcing the taker's choice gives the third player real counting information. Talk is left out on purpose. With three players and one possible winner, players do disagree, but requests and claims already carry the bluffing and inference, and the third player has nothing to coordinate. Free talk would add words without adding a decision."
},
"model": null,
"complexity": {"steps_per_round": 11, "choice_steps_per_round": 3, "attributes": 16, "hidden_elements": 1, "random_draws_per_round": 1, "rounds": 30}
}
````
