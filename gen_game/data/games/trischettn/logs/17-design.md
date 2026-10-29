# 17 design

- time: 2026-10-28T02:54:11+00:00 (78.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 8a5c5a1e95e35b74, reply sha256 ae76419d59a2ced1

## Sent

````
Original game: Trischettn
Players in the original: 2 to 4

Original rules:
Two-player base: remove Sixes from Salzburg pattern to make 32 cards. No trumps. Rank per suit: 10 high, then 9, Ace, King, Ober, Unter, 8, 7. Deal 8 each, remaining 16 as talon. Must follow suit if able; highest of led suit wins trick. Winner draws from talon, then opponent draws, winner leads next. After talon empty play out hand. Card points: Ace=1, Ten/Nine/King/Ober/Unter=1/3 each, last trick=1. Fractions rounded down after summing, so 11 points per deal without bonuses. Declarations score bonus when on lead after winning a trick: three Tens/Nines/Aces=3, four=4, Napoli=Ten+Nine+Ace of same suit=3. Cards can be reused in multiple declarations. Play to 31 points, sometimes 41. For 3 players deal 10 each discard 2, otherwise same. For 4 deal 8 each, declarations only on first trick, partnership signaling gestures allowed.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Simplify or drop the declaration mechanic. One option is to remove declarations entirely, which leaves a plain trick-taking game with card values and the last-trick bonus. Another is to make declaring automatic and unconditional: at the start of each deal, once hands are dealt, score each player's qualifying sets to their deal points. Then there is no leader-won-previous-trick gate, no opt-in poll and no once-per-deal mark, and a step runs every deal. If declarations stay, limit them to one easily counted pattern, such as three or more cards of one rank among Ten, Nine or Ace. Keep the scratch values off the shown state, and drop `declared_cards_shown` from the interface if nothing needs to display it. Also give `talon_up` a non-empty placeholder value (for example 'none') once the talon runs out, so a required public field is never blank.
the game file could not be built. What the checks found on the attempts:
- attempt 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (decl_answer, drawn_hidden_card); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 2: it plays, but part of it does nothing: player attribute `declared_this_deal` is never changed in 3 random matches, so nothing updates it. Steps that name it: start a deal, the declaration is scored. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `declared_cards_shown` is never changed in 3 random matches, so nothing updates it. Steps that name it: start a deal, the declaration is scored. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `decl_value` is never changed in 3 random matches, so nothing updates it. Steps that name it: work out the leader's declaration. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `decl_cards` is never changed in 3 random matches, so nothing updates it. Steps that name it: work out the leader's declaration. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- attempt 3: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (drawn_hidden_card, talon_up); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 4: it plays, but part of it does nothing: player attribute `declared_this_deal` is never changed in 3 random matches, so nothing updates it. Steps that name it: start a deal, the declaration. They never c

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Trischettn is an Austrian trick-taking game for 2 to 4 players with a 32-card Salzburg deck and no trumps. Cards rank 10, 9, Ace, King, Ober, Unter, 8, 7, and players must follow suit. After each trick both players draw from a talon, winner first. Players score card points, a last-trick point and declaration bonuses (three or four Tens, Nines or Aces, or a Napoli of Ten, Nine and Ace of one suit), playing to 31 or 41 points.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. 'Always play the highest legal card' throws away Tens and Nines on tricks it cannot win and gives up the lead pointlessly. 'Always play the lowest' hands over every point-bearing trick. The seat that leads first has a small edge in a single deal, but over a match to 31 the lead changes hands constantly."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card play rewards counting and timing, and following suit makes the endgame a counting exercise. But declarations are scored straight from the cards a player is dealt or happens to draw: three Aces is worth 3 of the 11 points in a deal, for no decision at all. That pushes the result toward the deal."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Beginners can follow suit and still win tricks. Strong players count the 32 cards, read the opponent's hand from their follows and draws, decide when to win a trick for a talon card, and play out the talon-empty endgame exactly."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the talon are hidden. Once the talon is empty, a counting player can deduce the opponent's whole hand, so memory and inference decide the endgame."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners, card points, the last-trick bonus and declarations are all arithmetic. The one problem is rounding fractions after summing, which is fiddly but deterministic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "A match to 31 needs roughly three deals of 16 tricks, which exceeds 40 rounds. Declarations are gated on winning the previous trick, opt-in, and allow reuse of cards. The previous build attempts failed on exactly these: attributes that never changed, and blank scratch fields. The 4-player variant relies on partnership gestures, and the 3-player variant adds a discard."
    }
  ],
  "problems": [
    "Declarations are scored mostly from luck of the deal or draw and outweigh card-play decisions (3-4 of about 11 points per deal).",
    "The declaration mechanic (only after winning a trick, opt-in, once-per-deal marks, cards reusable) produced attributes that never changed in testing (declared_this_deal, declared_cards_shown, decl_value, decl_cards), so the game could not be built.",
    "Scratch fields (decl_answer, drawn_hidden_card) and a talon_up field that went blank when the talon ran out appeared empty in the state shown to players.",
    "Playing to 31 or 41 points takes about 48 or more tricks, beyond the 40-round limit, and an open-ended match length is hard to build.",
    "Card points in thirds with rounding down after summing are awkward to track and create artificial ties.",
    "The 3- and 4-player variants add discards and partnership gestures that the engine cannot support cleanly.",
    "A completely hidden talon makes the decision to win or lose a trick for its draw rather thin."
  ],
  "changes": [
    {
      "what": "Remove declarations entirely.",
      "why": "Declarations were mainly a reward for the deal. Removing them makes card play decide the score and deletes every attribute that failed to update.",
      "fixes": "Declarations are scored mostly from luck of the deal or draw and outweigh card-play decisions (3-4 of about 11 points per deal)."
    },
    {
      "what": "Delete the declaration bookkeeping (declared_this_deal, declared_cards_shown, decl_value, decl_cards, decl_answer). No scratch attribute is kept that some step does not change every trick.",
      "why": "Every remaining attribute changes in normal play.",
      "fixes": "The declaration mechanic (only after winning a trick, opt-in, once-per-deal marks, cards reusable) produced attributes that never changed in testing (declared_this_deal, declared_cards_shown, decl_value, decl_cards), so the game could not be built."
    },
    {
      "what": "Remove drawn_hidden_card from shown state. Every public field starts with a non-empty value: led_card and followed_card start as 'none', and talon_up shows 'none' once the talon is empty.",
      "why": "The state shown to players never contains a blank field.",
      "fixes": "Scratch fields (decl_answer, drawn_hidden_card) and a talon_up field that went blank when the talon ran out appeared empty in the state shown to players."
    },
    {
      "what": "Fixed match of exactly 2 deals of 16 tricks (32 rounds, one trick per round). Player A leads the first trick of deal 1 and Player B leads the first trick of deal 2.",
      "why": "This fits the round limit, balances the opening lead, and lets a second deal reduce the luck of a single deal.",
      "fixes": "Playing to 31 or 41 points takes about 48 or more tricks, beyond the 40-round limit, and an open-ended match length is hard to build."
    },
    {
      "what": "Score in whole pips: Ace 3, Ten/Nine/King/Ober/Unter 1, Eight/Seven 0, last trick of a deal 3. This gives 35 pips per deal, the original 11-and-a-bit points times three, with no rounding.",
      "why": "Integer arithmetic only. Each deal's total is odd, so a single deal cannot tie.",
      "fixes": "Card points in thirds with rounding down after summing are awkward to track and create artificial ties."
    },
    {
      "what": "The game is for 2 players only.",
      "why": "The 2-player form is the base game and the one that fits the engine.",
      "fixes": "The 3- and 4-player variants add discards and partnership gestures that the engine cannot support cleanly."
    },
    {
      "what": "The top card of the talon lies face up (talon_up). The trick winner takes that visible card and the loser takes the next, hidden card. A new top card is then turned face up.",
      "why": "Players must decide whether winning a trick is worth it for the visible card, and the loser's hidden draw is an inference target for the winner.",
      "fixes": "A completely hidden talon makes the decision to win or lose a trick for its draw rather thin."
    }
  ],
  "keeps": [
    "32-card Salzburg deck in four suits, no trumps",
    "Rank order 10, 9, Ace, King, Ober, Unter, 8, 7 within each suit",
    "8 cards each and a 16-card talon; trick winner draws first, then the loser; trick winner leads next",
    "Must follow suit if able; highest card of the led suit wins",
    "Play out the hands after the talon is empty",
    "Original relative card values (Ace worth three times a Ten/Nine/court card) and the last-trick bonus"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core trick-taking with a talon is a sound inference and counting game. Removing the luck-driven, hard-to-build declarations and fixing the match length makes it buildable and skill-driven."
  },
  "variation": {
    "name": "Trischettn Duel",
    "summary": "A two-player, two-deal Trischettn without trumps or declarations. A face-up talon card goes to each trick's winner, and the talon-empty endgame rewards exact card counting.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK. The deck has 32 cards in four suits: Hearts, Bells, Leaves, Acorns. Each suit holds these ranks, from strongest to weakest: Ten, Nine, Ace, King, Ober, Unter, Eight, Seven (strength 8 down to 1). There are no trumps.\n\nCARD VALUES (pips).\n- Ace: 3 pips.\n- Ten, Nine, King, Ober and Unter: 1 pip each.\n- Eight and Seven: 0 pips.\n- Winning the 16th (last) trick of a deal: 3 extra pips.\nEach deal therefore contains 35 pips in total.\n\nMATCH. The match is exactly 2 deals of 16 tricks each, 32 rounds in all. Each round is one trick.\n\nSTART OF A DEAL (in round 1 and round 17 only).\n1. Shuffle all 32 cards.\n2. Deal 8 cards face down to each player as a private hand.\n3. The remaining 16 cards form the talon, face down. Its top card is turned face up as the 'talon up' card, visible to both players.\n4. Both players' deal pips are set to 0.\n5. The leader of the first trick is Player A in deal 1 and Player B in deal 2.\n\nEACH TRICK.\n1. The leader plays any one card from their hand face up.\n2. The follower then plays one card. If they hold any card of the led suit, they must play a card of that suit. Only legal cards are offered. If they hold none, they may play any card.\n3. Winning the trick: if both cards are of the led suit, the one of higher strength wins. Otherwise the leader wins.\n4. The trick winner adds the pips of both cards to their deal pips. If this was the 16th trick of the deal, the winner adds 3 more.\n5. If the talon is not empty:\n   - the winner takes the face-up 'talon up' card into their hand, so both players know it;\n   - the loser takes the next talon card face down, so only the loser sees it;\n   - if any talon cards remain, the new top card is turned face up as 'talon up'; otherwise 'talon up' becomes 'none'.\n   The 16-card talon empties after exactly 8 tricks. The last 8 tricks are played from hand with no drawing.\n6. The trick winner leads the next trick.\n\nEND OF A DEAL (after trick 16). Each player adds their deal pips to their match total.\n\nPUBLIC INFORMATION. Both players see:\n- the deal number and trick number;\n- who leads;\n- both cards of the current trick (shown as 'none' before they are played);\n- the 'talon up' card, or 'none';\n- the number of cards left in the talon;\n- both players' deal pips and match totals.\nEach player privately sees only their own hand.\n\nEND OF MATCH. After round 32, the player with the higher match total wins. Equal totals are a draw.",
    "objective": "After 2 deals (32 tricks), each player's match total is the sum of their pips from both deals, out of 70 pips available. The higher total wins. If both totals are 35, the match is a draw.",
    "expected_effect": "Without declarations, every pip comes from card play, so counting and timing decide the match. The face-up talon card creates a real trade-off on each of the first 8 tricks: spend a strong card to win the trick and take a visible Ten or Ace, or duck cheaply and accept a hidden card. The winner must then infer what the loser drew. Once the talon is empty, a player who has tracked every played and visible card can deduce the opponent's whole hand and play the last 8 tricks perfectly. That final phase, worth over a third of the deal including the 3-pip last trick, separates strong from weak players. Alternating the first lead and playing two deals balances the seats and dampens the luck of a single deal. Simple policies lose to thoughtful play: always-highest wastes Tens and Nines, always-lowest concedes the Aces, and random play loses the endgame. Talk is omitted because there are only two players."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 2,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 32
  }
}
```
````
