# 01 design

- time: 2026-10-28T01:31:46+00:00 (67.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 28f615d7c208be2b, reply sha256 78c216f660fcd2a6

## Sent

````
Original game: Indian Poker
Players in the original: 4 to 10

Original rules:
Use a standard 52-card deck. Deal one card face down to each player. On a signal, all players lift their card to their forehead without looking at it, so each player sees all other cards but not his own. Optional rule ranks suits Spades high, then Hearts, Diamonds, Clubs. Conduct one round of betting in turn order: players may check, bet, call, raise or fold based on what they see and opponents' actions. After betting, all remaining players reveal their own cards. Highest rank wins the pot. If suits are ranked, break ties by suit. If only one player remains after folds, they win.
````

## Reply

````
```json
{
  "original_summary": "Indian Poker (Blind Man's Bluff) deals each of 4 to 10 players one card that they hold to their forehead, so each player sees every card but their own. One round of poker betting in turn order follows, and the highest card among players who did not fold wins the pot.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Folding, calling and raising do change the outcome, and no single action is always best. But betting goes in turn order, so the last seat to act sees everyone else's bets before deciding, which is a built-in positional edge in a single hand. 'Always fold' only ever loses the ante, which is safe but losing. Nothing structurally breaks the game."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "The original is one hand with one card each. Who holds the highest card decides it almost entirely. A brilliant reader of other players still loses when dealt a 3, and a thoughtless caller wins when dealt an ace."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "There is real depth: you infer your own card from the cards you see and from how others bet against you. But a single hand gives no room for a strong player's edge to accumulate, so improvement barely shows in results."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "This is the game's core strength. Your own card is the one thing hidden from you. You must estimate it from the distribution of the cards you see and from how opponents, who can see your card, choose to bet. That is classic opponent modelling and inference from limited information."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The winner is the highest card among players who stayed in (suits break ties), and chip movements are arithmetic. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Hidden cards, private views and numeric bets are all supported. However, open-ended poker betting (check, bet, raise and re-raise in turn order until everyone has matched) is a loop of unknown length, which the flat step list cannot express. A single hand is also too short to score meaningfully."
    }
  ],
  "problems": [
    "A single hand makes the result almost pure card luck; skill cannot show.",
    "Open-ended sequential betting (raise and re-raise until matched) is an unbounded loop the engine cannot build.",
    "Turn-order betting gives a fixed positional edge to whoever acts last.",
    "There is no multi-round planning: no chip management, no reputation, nothing carried between decisions.",
    "Folding costs only the ante, so very tight play is cheap and the game can stall into everyone folding.",
    "The table-talk and bluffing that make the game fun in person are informal, so a text platform has no defined channel for them."
  ],
  "changes": [
    {
      "what": "Play a match of 16 hands, with chips carried from hand to hand. The winner is the player with the most chips at the end.",
      "why": "Card luck evens out over 16 hands, while good reading, folding and bluffing accumulate. Chip management and reputation across hands add planning.",
      "fixes": "A single hand makes the result almost pure card luck; skill cannot show."
    },
    {
      "what": "Replace open betting with two fixed simultaneous decisions. First, everyone at the same moment chooses Fold or a bet of 1, 2 or 3 chips. Then the bets are revealed, and every remaining player at the same moment chooses Call (match the highest bet) or Fold.",
      "why": "This keeps the bet, see and respond structure of poker in a fixed number of steps the engine can build.",
      "fixes": "Open-ended sequential betting (raise and re-raise until matched) is an unbounded loop the engine cannot build."
    },
    {
      "what": "Make all betting decisions simultaneous.",
      "why": "No seat ever acts with more information than another, so position gives no edge.",
      "fixes": "Turn-order betting gives a fixed positional edge to whoever acts last."
    },
    {
      "what": "If every player folds, or nobody is left to contest the pot, the whole pot carries over to the next hand.",
      "why": "Mass folding feeds a bigger future pot, which raises the stakes and punishes passive play relative to opponents who contest it.",
      "fixes": "Folding costs only the ante, so very tight play is cheap and the game can stall into everyone folding."
    },
    {
      "what": "Before betting each hand, every player writes one short public message at the same moment, and all messages are then shown. Players may say anything, including true or false claims about other players' cards.",
      "why": "This formalises Indian Poker's table talk. You can try to scare a strong player out or lure a weak one in, but the other players see that player's card and know whether you lied. That rewards bluffing, reading and tracking reputation.",
      "fixes": "The table-talk and bluffing that make the game fun in person are informal, so a text platform has no defined channel for them."
    },
    {
      "what": "Use a fixed ante, a bet cap of 3 chips and 40 starting chips. A player who has fewer than 4 chips at the start of a hand is eliminated and keeps that total.",
      "why": "Losses per hand are bounded, so chip management across the match matters and one hand cannot decide everything.",
      "fixes": "There is no multi-round planning: no chip management, no reputation, nothing carried between decisions."
    }
  ],
  "keeps": [
    "Each player sees every card except their own.",
    "You infer your own card from what you see and from how others bet against you.",
    "Ante, bet, call or fold, then a showdown where the highest card among those still in wins the pot.",
    "A standard 52-card deck, with suits breaking ties in the order Spades, Hearts, Diamonds, Clubs.",
    "Table talk and bluffing as part of play."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (you are the only one blind to your own card) is an excellent inference and opponent-modelling engine. It only needs a multi-hand structure, bounded simultaneous betting and a defined talk channel."
  },
  "variation": {
    "name": "Forehead Poker Match",
    "summary": "A 16-hand Indian Poker match for 4 to 6 players. Everyone sees every card but their own. Each hand has one simultaneous public message, one simultaneous bet and one simultaneous call-or-fold decision. Chips carry over, and the most chips after 16 hands wins.",
    "players": {
      "min": 4,
      "max": 6,
      "suggested": 4
    },
    "rules": "SETUP: Each player starts with 40 chips. The pot starts at 0. The match lasts 16 hands.\n\nCARD STRENGTH: A standard 52-card deck is used. Rank from high to low is A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2. Between equal ranks, suit decides, from high to low: Spades, Hearts, Diamonds, Clubs. No two cards are ever equal.\n\nEACH HAND:\n1. ELIGIBILITY: Any active player with fewer than 4 chips is eliminated. They take no further part, and their current chips are their final total.\n2. DEAL: The full deck is shuffled and one card is dealt to each active player. Each player is privately told the card of every other active player, but never their own.\n3. ANTE: Each active player pays 1 chip into the pot.\n4. TALK: Every active player writes one short message (at most 40 words) at the same moment, without seeing the others. All messages are then shown to everyone. Messages may say anything, including claims about anyone's card, and none of them binds anyone.\n5. FIRST BET: Every active player, at the same moment, chooses one option: Fold, Bet 1, Bet 2 or Bet 3. A player who bets pays that many chips into the pot immediately. A player who folds is out of this hand and has lost only the ante.\n6. REVEAL BETS: Every player's choice from step 5 is shown to everyone. Let H be the highest bet made.\n7. CALL OR FOLD: Every player who bet in step 5, at the same moment, chooses Call or Fold. Calling costs H minus that player's own step-5 bet, paid into the pot. A player whose bet was already H calls for free. Folding forfeits everything that player has put in this hand.\n8. SHOWDOWN: Find the players who called.\n   - Two or more callers: their cards are compared, and the caller with the strongest card wins the whole pot.\n   - Exactly one caller: that player wins the whole pot without comparison.\n   - No callers: the pot stays and carries over to the next hand.\n   All cards are then revealed to everyone, so players can check what was said and bet.\n9. Winnings are added to the winner's chips, the pot resets to 0 (unless it carried over), and the next hand begins.\n\nEND: The match ends after hand 16, or earlier if only one player is still active. Any pot remaining at that moment is discarded.",
    "objective": "The player with the most chips at the end of the match wins. Eliminated players count with the chips they held when eliminated. If two or more players tie for the most chips, the game is a draw among them.",
    "expected_effect": "The game becomes a contest of reading your own invisible card. A player infers their card's strength from the cards they can see (if everyone else holds low cards, yours is probably higher) and from how others bet and talk, since every opponent can see your card exactly.\n\nSimple policies lose:\n- Always Fold loses 1 chip per hand and finishes about 16 chips down.\n- Always Bet 3 and Call is exploited. Opponents see its card, so they fold when it is high (it wins only the antes) and call when it is low (it loses 4 chips each time).\n- Always Bet 1 and Call never pressures anyone and pays to see every losing showdown.\n- Random play bleeds chips to anyone who folds when they see the table is strong.\n\nWhen everyone plays well, card luck still swings individual hands, but over 16 hands the player who folds weak cards cheaply, extracts value with strong ones and bluffs effectively finishes ahead.\n\nTalk passes both tests. On reasoning, players can bluff and bait, for example telling a player holding the 2 'you look strong' to lure them into calling, or telling the player holding the ace 'there is a king out there' to scare them off. Each listener must weigh who gains from the claim and that speaker's past honesty, which can be checked because cards are revealed after each hand. On conflict, only one player can win and every pot is zero-sum, so following another player's advice about your own card is exactly how a credulous player loses: the speaker only says 'call' when your call pays them.\n\nNo seat has an edge because all choices are simultaneous. The carry-over pot stops everyone from folding into a stall."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 3,
    "attributes": 10,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 16
  }
}
```
````
