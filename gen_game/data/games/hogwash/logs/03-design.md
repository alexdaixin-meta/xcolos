# 03 design

- time: 2026-10-28T03:42:44+00:00 (81.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ab2e82211f350477, reply sha256 076b200709158462

## Sent

````
Original game: Hogwash
Players in the original: 2 to 8

Original rules:
Deal the 13-rank deck evenly face down. The player left of dealer starts a central pile by playing 1-4 cards face down claiming them as 1s. Play goes clockwise, each turn the required rank increases by 1, wrapping from 13 to 1. The player must discard 1-4 cards face down claiming the required quantity and the required rank. If they lack that rank they must bluff with other cards. After any discard, any opponent may call Hogwash! to challenge the last play. Flip those cards: if they match the claim, the challenger takes the entire central pile into their hand; if they do not match, the bluffer takes the entire pile. First player to empty their hand wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Rank schedule: the rank on turn t is ((t-1) mod 6)+1. With 3 players each seat only ever claims two ranks: P1 claims {1,4}, P2 {2,5}, P3 {3,6}. With 4 players each seat claims three: P1 {1,5,3}, P2 {2,6,4}, P3 {3,1,5}, P4 {4,2,6}. That is symmetric. Move order is not.

Uncontested race (thoughtless 'always play 3, nobody challenges'). A seat goes out on turn seat + P*(plays-1), where P is the player count.
| seat | cards (3p) | plays | out on turn |
| P1 | 8 | 3+3+2 | 7 |
| P2 | 8 | 3+3+2 | 8 |
| P3 | 7 | 3+3+1 | 9 |
The starter-card compensation buys P3 nothing: 7 cards still needs 3 plays.
| seat | cards (4p) | plays | out on turn |
| P1 | 6 | 3+3 | 5 |
| P2 | 6 | 3+3 | 6 |
| P3 | 6 | 3+3 | 7 |
| P4 | 5 | 3+2 | 8 |
P4's discount is likewise wasted.

At every stage P1 is one to three turns ahead. A challenge costs the resolving challenger the whole pile if the claim is true, and early piles are small, so P1's tempo lead survives a fair share of contested play. That is a move-order edge the design claims to offset but does not.

Thoughtless policies, under the winner rule:
- Always-3: almost always a bluff. Holding 3 of the required rank is rare (with 4 copies, P(3+ of R in 8 cards) is about 0.05). Against any challenger it takes the pile, so it loses.
- Always-pass: lets the leader dump unopposed and loses the race.
- Always-challenge: against honest single-card plays it takes the pile. Against random play it catches bluffs (a random card is true about 1/6 of the time) and beats random. Against sensible play it is not dominant.
- Final plays: challenging a player's last play is weakly dominant, because a true claim ends the game anyway. Going out therefore requires a true play. That is good tension, not a broken strategy.

No option is strictly dominant, and every seat can win. The check fails on the uncorrected seat-order tempo edge, plus a cosmetic starter compensation that changes no seat's play count.
- playable FAILED: Complexity is within limits: 14/20 steps, 2/4 choice steps, 13/20 attributes, 2/3 hidden elements, 36/40 rounds. The game is finite: it ends when a hand empties or after turn 36, decided by card counts. The challenge poll is correctly simultaneous. It needs no board or clock.

Problems:
(1) 'P3 places one of their own cards, chosen at random' is a second random event. This contradicts 'shuffle once ... the only random event'. The rules also never say whether P3 knows which card went down, which changes P3's inference about the pile.
(2) Talk is never addressed for a 3-4 player game. Talk is warranted here, because the resolving-challenger rule creates real disagreement. Only the first challenger clockwise risks taking the pile, and later challengers 'suffer nothing'. So the seat at active+2 wants to know whether active+1 will challenge, and active+1 wants active+2 to carry the risk. These players have opposed interests in who calls, and non-binding claims ('I'll pass') would be worth reasoning about. With no talk step they can only guess each other.
(3) Minor gap: it is unclear whether a player holding 0 cards before taking a turn is possible, and the 'never more than they hold' case at 0 cards is unspecified. Step 5 makes it unreachable, but it should be stated.
- change: Remove the move-order tempo edge. For example, when a player empties their hand, finish the current round so every seat has had the same number of turns. All players at 0 cards at the end of that round (after surviving challenges) draw, or the tie is broken by fewest pile pickups. Alternatively, rotate the first active player each game and score over a fixed even set of games.
- change: Replace the cosmetic starter compensation (one card from the last seat) with one that changes the play count, or drop it once the end-of-round rule is added.
- change: Make the starter card non-random. The last seat chooses which card to place, so the shuffle remains the only random event. State explicitly that the placer knows the card.
- change: Add a simultaneous free-text talk step after the claim and before the challenge poll (all write, all are shown, then all choose), so players can negotiate who calls under the resolving-challenger rule. Alternatively, change resolution so all challengers share the outcome (a true claim splits the pile among challengers, remainder to the first clockwise). That removes the coordination gap and makes the absence of talk defensible.
- change: State explicitly that a player with 0 cards has won and never takes another turn.
The variation that was reviewed: Hogwash: Sealed Calls: SETUP
- Deck: 24 cards, ranks 1 to 6, four copies of each.
- Shuffle once at the start of the game; this is the only random event.
- Seat order is Player 1, Player 2, Player 3 (and Player 4 if present). Clockwise means increasing seat number, wrapping from the last seat back to Player 1.
- With 3 players: deal 8 cards each. Then the last seat (Player 3) places one of their own cards, chosen at random, face down as the first card of the central pile. They hold 7.
- With 4 players: deal 6 cards each. Then Player 4 places one random card of their own face down to start the pile. They hold 5.
- Hands are private. Everyone always knows how many cards each player holds and how many are in the pile.
- The required rank starts at 1. Player 1 is the first active player.

EACH TURN (one turn per round)
1. Announce the turn number, the active player and the required rank.
2. Play. The active player secretly chooses 1, 2 or 3 cards from their hand (never more than they hold). The cards go face down onto the top of the central pile. It is announced publicly: 'Player X plays N cards, claiming N cards of rank R', where R is the required rank. The claim is always exactly the required rank and exactly the number of cards played. The cards may be anything; playing other ranks is a bluff.
3. Challenge poll. Every other player simultaneously and secretly chooses CHALLENGE or PASS.
4. Resolution.
   - If nobody challenged, the cards stay in the pile.
   - If one or more challenged, the resolving challenger is the challenger who comes soonest clockwise after the active player.
   - Reveal only the cards just played. If every one of them is rank R, the claim was true and the resolving challenger takes the entire central pile into their hand.
   - If any revealed card is not rank R, the claim was a bluff and the active player takes the entire central pile into their hand.
   - The pile is then empty, and the result (true or bluff, and who took how many cards) is announced. Other challengers suffer nothing.
5. Win check. If any player now holds 0 cards, that player wins immediately. A player who emptied their hand with a bluff that was caught has taken the pile back, so does not win.
6. Advance. The required rank increases by 1, wrapping from 6 to 1. The active player passes to the next seat clockwise.

END
- The game ends when a player empties their hand, or after turn 36.
- After turn 36, the player holding the fewest cards wins. If two or more tie for fewest, the game is a draw. Winner: The first player to hold 0 cards after a turn's resolution wins. If nobody has done so after 36 turns, the single player with the fewest cards wins. A tie for fewest is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
  "original_summary": "Hogwash (also known as Cheat or I Doubt It) is a shedding and bluffing card game. Players take turns discarding cards face down while claiming they are the required rank, which rises by one each turn. Any opponent may call a bluff: a caught bluffer takes the whole pile, and a wrong caller takes it instead. The first player to empty their hand wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "The previous variation, Sealed Calls, has no dominant pure policy. Always-3 is almost always a bluff and gets caught. Always-pass lets the leader dump cards unopposed. Always-challenge takes the pile from honest plays. But seat order gives a built-in tempo edge: uncontested, P1 goes out on turn 7, P2 on turn 8 and P3 on turn 9 (3 players), and P1 to P4 on turns 5 to 8 (4 players). The starter-card compensation never changes anyone's number of plays. With 6 ranks and 3 players, each seat only ever claims two fixed ranks, so a hand rich in your own ranks is a lasting deal advantage. Challenging a final play was also free, because a true last play ended the game anyway."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Several skills decide who wins: when to bluff, sizing plays to the pile's risk, tracking which ranks have been publicly revealed and which ranks opponents have taken back into hand, and reading who will call. Two things blur this: the deal (fixed claim ranks per seat) and the tempo edge."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Card counting, pile-size risk management and challenger coordination can be refined without limit. Even a weak player who plays one honest card at a time can survive and score."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and pile contents are hidden. Every claim must be judged against what you hold, what has been revealed and the claimant's incentives. The resolving-challenger rule adds a who-calls inference. Without talk, players could only guess at that inference."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card checks against the required rank, card counts and a fewest-cards fallback are all arithmetic. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only, has no board and fits within the limits. However, it introduced a second random event (the random starter card) while claiming the shuffle was the only one. It never said whether P3 knew the starter card. It left the zero-card state underspecified and had no talk step, even though the challenger coordination problem calls for one."
    }
  ],
  "problems": [
    "P1: Move-order tempo edge. Earlier seats reach zero cards turns earlier, and winning immediately on emptying rewards seat position rather than play.",
    "P2: The starter-card compensation is cosmetic (it changes no seat's play count) and adds a second random event whose knowledge status is unstated.",
    "P3: With 6 ranks and 3 players (or 4), each seat claims only a fixed subset of ranks, so being dealt your own ranks is a deal-lottery advantage.",
    "P4: Challenging a final play is free, because a true last play ends the game regardless, so that challenge carries no decision.",
    "P5: No talk step, although the resolving-challenger rule gives players opposed interests over who calls.",
    "P6: The zero-card state is underspecified: whether a player with no cards takes turns, votes in polls or can receive the pile."
  ],
  "changes": [
    {
      "what": "When any player empties their hand, the current cycle of seats is finished, so every seat has had exactly the same number of turns before the game ends. Every player then at zero cards is a finisher. Ties among finishers are broken by fewest total cards taken from the pile over the game, otherwise a draw.",
      "why": "Equal turns remove the tempo edge. The uncontested race now ends with all seats out together, a draw, so seat order alone wins nothing. The tiebreak rewards accurate challenging and well-judged bluffing over the whole game.",
      "fixes": "P1"
    },
    {
      "what": "Use a 25-card deck: ranks 1 to 5, five copies of each. Deal 8 each with 3 players or 6 each with 4. The one leftover card goes face down as the first pile card, seen by nobody. There is no player-placed starter card.",
      "why": "The shuffle and deal is the only random event, everyone is dealt the same hand size, and nobody has special knowledge of the starter card.",
      "fixes": "P2"
    },
    {
      "what": "Use 5 ranks instead of 6.",
      "why": "5 shares no factor with 3 or 4, so over five cycles every seat must claim every rank. A hand rich in one rank helps every seat equally often, and no seat is locked to fixed ranks.",
      "fixes": "P3"
    },
    {
      "what": "Because the game no longer ends on the spot, a challenger who calls a true final play takes the whole pile.",
      "why": "Calling a last play now has a real cost, so it becomes a judgement rather than an automatic call.",
      "fixes": "P4"
    },
    {
      "what": "Add a simultaneous talk step after the claim and before the challenge poll. Every player still holding cards, including the active player, writes one short message. All messages are shown, then the poll happens.",
      "why": "The first challenger clockwise carries all the risk and later challengers carry none, so non-active players disagree about who should call. The active player can bluster or bait. Talk gives players promises to test and bluffs to read.",
      "fixes": "P5"
    },
    {
      "what": "State the zero-card rules explicitly. A player with zero cards is finished. They take no further turns (their turn slot passes with no play), do not talk, are always counted as PASS in polls, and can never receive the pile.",
      "why": "Removes ambiguity so the engine can build the game correctly.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Face-down discards claimed as the required rank, which rises by one each turn and wraps around",
    "Bluffing when you lack the rank",
    "Calling a bluff: a caught bluffer takes the whole pile, and a wrong caller takes it instead",
    "Shedding race: emptying your hand is the goal",
    "Hidden hands with public card counts",
    "The resolving-challenger rule from Sealed Calls, now paired with talk"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core bluff-and-call loop is strong reasoning material. The fixes are about fairness and clarity, and they fit easily within the limits."
  },
  "variation": {
    "name": "Hogwash: Even Rounds",
    "summary": "A 3 to 4 player shedding and bluffing game with a 25-card, five-rank deck. Players discard face down claiming the required rank. A sealed challenge poll follows a simultaneous talk step. When someone empties their hand, the cycle of seats is completed so everyone gets equal turns, and ties among finishers go to whoever took the fewest pile cards.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "SETUP\n- Deck: 25 cards, ranks 1 to 5, five copies of each rank.\n- Shuffle once at the start. This shuffle and the deal are the only random events in the game.\n- Seats are Player 1, Player 2, Player 3 (and Player 4 with four players). Clockwise means increasing seat number, wrapping from the last seat to Player 1.\n- With 3 players, deal 8 cards to each player. With 4 players, deal 6 cards to each player.\n- The one remaining card is placed face down as the first card of the central pile. Nobody sees it.\n- Hands are private. Everyone always knows how many cards each player holds and how many cards are in the pile.\n- Each player has a public 'taken' counter, starting at 0. It counts the total number of cards that player has picked up from the pile during the game.\n- Turn 1: the required rank is 1 and Player 1 is the active player.\n- A cycle is one turn for each seat in order, from Player 1 to the last seat. Turns 1 to 3 are cycle 1 with 3 players; turns 1 to 4 are cycle 1 with 4 players; and so on.\n\nFINISHED PLAYERS\n- A player holding 0 cards is finished.\n- A finished player takes no turns: when their turn comes, it passes with no play, and the rank and turn still advance.\n- A finished player writes no messages and is always counted as PASS in challenge polls.\n- A finished player can never receive the pile.\n\nEACH TURN\n1. Announce the turn number, the active player and the required rank R.\n2. Play. The active player secretly chooses 1, 2 or 3 cards from their hand (never more than they hold) and puts them face down on top of the pile.\n   - It is announced: 'Player X plays N cards, claiming N cards of rank R.'\n   - The claim is always exactly rank R and exactly the number of cards played.\n   - The cards may be anything. Playing any card that is not rank R is a bluff.\n3. Talk. Every player who still holds cards, including the active player, writes one short message at the same moment, without seeing the others. All messages are then shown to everyone.\n   - Messages are not binding. Players may promise, threaten, bluff or lie.\n4. Challenge poll. Every non-active player who holds cards simultaneously and secretly chooses CHALLENGE or PASS.\n5. Resolution.\n   - If nobody challenged, the cards stay in the pile.\n   - Otherwise, the resolving challenger is the challenger who comes soonest clockwise after the active player.\n   - Reveal only the cards just played.\n   - If all of them are rank R, the claim was true: the resolving challenger takes the entire pile into their hand.\n   - If any revealed card is not rank R, the claim was a bluff: the active player takes the entire pile into their hand.\n   - Whoever took the pile adds the number of cards taken to their taken counter.\n   - The pile is now empty. The result is announced: true or bluff, who took the pile, and how many cards.\n   - Other challengers lose nothing.\n6. Finish check. Any player now holding 0 cards is finished.\n   - The first time any player becomes finished, the game is marked to end at the end of the current cycle.\n   - A bluff that was caught never finishes the bluffer, because they have taken the pile back.\n7. End check. The game ends if the turn just played was the last seat's turn and either of these is true:\n   - the game has been marked to end; or\n   - this was turn 36.\n8. Advance. The required rank increases by 1, wrapping from 5 back to 1. The next seat clockwise becomes the active player.\n\nNOTES\n- Because 5 ranks share no factor with 3 or 4 seats, every seat is required to claim every rank over the course of five cycles.\n- Because 36 turns is a whole number of cycles for both 3 and 4 players, every seat always gets the same number of turns.",
    "objective": "When the game ends, every seat has had the same number of turns. Find the smallest hand size held by any player; this is 0 if anyone is finished. Among the players holding that many cards, the one with the lowest taken counter wins. If two or more of them tie on the lowest taken counter, the game is a draw.",
    "expected_effect": "Seat order no longer wins anything. If nobody challenges, all players go out in the same cycle with zero taken, a draw (in 3 players, 3+3+2 plays each; in 4 players, 3+3). Winning therefore requires catching others' bluffs while avoiding pickups yourself.\n\nSimple policies each lose:\n- Always-3 bluffs constantly and takes piles.\n- Always-challenge takes the pile from true claims and racks up its taken counter.\n- Always-pass lets bluffers dump cards and can lose the tiebreak race.\n- Always-1-honest-when-possible is too slow to finish.\n\nCalling a final play now costs the challenger the pile if the claim is true, so last plays become real reads.\n\nTalk passes both tests:\n- Players disagree about who should call, because only the first challenger clockwise risks the pile. The seat right after the active player wants a later seat to carry the risk, and each wants the other's taken counter to rise.\n- The active player wants to bait a call on a true play, or bluff confidence on a false one.\n- A player who simply follows another's 'you call, I'll back you' can end up as the resolving challenger on a true claim, swallowing the pile while the advisor loses nothing.\n- A player who believes 'I'll call' and passes can let a bluffer finish."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 3,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 36
  }
}
````
