# 01 design

- time: 2026-10-27T21:15:21+00:00 (78.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c85c51409fd2e149, reply sha256 ff580a3640333c42

## Sent

````
Original game: 11 Nimmt
Players in the original: 2 to 7

Original rules:
Each player is dealt 10 numbered cards sorted ascending, rest forms a draw deck. One card starts the first discard pile. On your turn you must either play one card onto any pile or take an entire pile into your hand. A play must be higher than the pile top, with circular distance at most 10 (e.g., after 98, 1-8 are within 10). If you cannot play, you must take a pile. When a pile is taken, two new cards from the draw deck start two new piles, so pile count grows. Taking a pile of 3+ cards earns a bull card. A bull allows you to play a whole run of eligible cards onto one pile in one turn; two bulls allow runs on two piles, etc. If bull supply is empty you steal from the player with most bulls. A round ends when a player empties hand; others score penalty ox-heads from remaining cards. Play as many rounds as players; lowest total penalty wins.
````

## Reply

````
```json
{
  "original_summary": "11 Nimmt is a shedding card game for 2 to 7 players. On each turn a player either plays one card onto a pile (higher than its top, within a circular distance of 10) or takes a whole pile into hand. Taking big piles earns bull cards, which allow multi-card runs. A round ends when someone empties their hand, the others score ox-head penalties for the cards they still hold, and the lowest total over several rounds wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins outright. 'Always take a pile' never empties the hand and swells it. 'Always play the lowest legal card' leaves you stuck and forced to take big piles when the tops jump. Choosing which pile to feed or block, and when to take a pile, changes who empties first. With 3 or more players one player's gain is not a direct loss for each rival. Two-player games are pure difference games. Seat order gives the first player a small tempo edge in each round."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Skill matters: pile blocking, timing takes to earn bulls, and saving runs. But fresh piles are seeded from a random draw deck every time a pile is taken, and the deal of 10 cards from 104 varies a lot. Luck has a large share in any single round."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still shed cards and score something. Strong players plan bull runs, track which numbers are gone, and take small piles to reset tops in their favour. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. A player must infer from what opponents play or decline to play which ranges they hold, and plan several turns ahead around bull runs and pile tops."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card legality is arithmetic (higher than the top, circular distance at most 10). Penalties are ox-head sums. The lowest total wins. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The pile count grows without bound, so state is unbounded. Bull runs let a player play an arbitrary number of cards in one turn. Every pile take triggers two random draws. A 104-card deck, 10-card hands and up to 7 rounds of play far exceed the limits of 4 choice steps, 1 random draw per round, 20 attributes and 40 rounds."
    }
  ],
  "problems": [
    "The number of piles grows each time one is taken, giving unbounded state that the engine cannot track within 20 attributes.",
    "Each pile take draws two random cards from the deck, which breaks the limit of one random draw per round and adds luck to every take.",
    "Bull runs allow an unbounded number of cards in one turn, which exceeds the choice-step limit.",
    "The 104-card deck, 10-card hands and multi-round match (as many rounds as players) are too long and too large to build and play inside 40 rounds.",
    "The two-player game is a pure difference game, and seat order gives the first player a tempo edge (they may empty their hand before others have had as many turns).",
    "Random pile seeding and a large random deal let luck swamp skill in a single deal."
  ],
  "changes": [
    {
      "what": "Use exactly 3 piles throughout. A taken pile is immediately restarted, so there are always 3.",
      "why": "This bounds the state to 3 pile lists and keeps the take-or-play pile choice.",
      "fixes": "The number of piles grows each time one is taken, giving unbounded state that the engine cannot track within 20 attributes."
    },
    {
      "what": "When a player takes a pile, they restart it with a card of their own choosing from their hand (which now includes the taken cards). Nothing is drawn from a deck during play.",
      "why": "This removes all in-play randomness and turns the restart into a strategic choice: block opponents or set up your own run.",
      "fixes": "Each pile take draws two random cards from the deck, which breaks the limit of one random draw per round and adds luck to every take."
    },
    {
      "what": "Bulls are capped. Each bull held lets a player add one extra card to the same pile in the same turn, with a maximum of 2 extra cards.",
      "why": "This keeps the bull-run idea while fitting within 4 choice steps.",
      "fixes": "Bull runs allow an unbounded number of cards in one turn, which exceeds the choice-step limit."
    },
    {
      "what": "Use a deck of 1 to 40, circular distance at most 6, 6-card hands, 3 or 4 players, and a single deal of at most 36 or 40 turns. Each engine round is one player's turn.",
      "why": "This scales the game to the round and attribute limits while keeping the density of legal plays similar to the original.",
      "fixes": "The 104-card deck, 10-card hands and multi-round match (as many rounds as players) are too long and too large to build and play inside 40 rounds."
    },
    {
      "what": "Use 3 or 4 players only. When someone empties their hand, the current cycle is completed so that every player has had the same number of turns. The lowest penalty wins.",
      "why": "With 3 or more players the game is not a difference game. Finishing the cycle removes the first seat's tempo edge.",
      "fixes": "The two-player game is a pure difference game, and seat order gives the first player a tempo edge (they may empty their hand before others have had as many turns)."
    },
    {
      "what": "Make the full contents of every pile public, so that every taken card is known to everyone. The initial deal is the only random event.",
      "why": "Hidden information shrinks to the original deal plus the undealt cards. A careful tracker can deduce more and more about opponents' hands, so skill beats luck over a game.",
      "fixes": "Random pile seeding and a large random deal let luck swamp skill in a single deal."
    }
  ],
  "keeps": [
    "Each turn you either play one card onto a pile or take a whole pile into your hand.",
    "A play must be higher than the pile top within a circular distance, with wraparound past the highest card.",
    "If you cannot or do not play, you must take a pile.",
    "Taking a pile of 3 or more cards earns a bull, which allows multi-card runs onto one pile. When the supply runs out, you steal a bull from the player who has the most.",
    "The deal ends when a player empties their hand. Others score ox-head penalties for the cards left in hand, and the lowest penalty wins.",
    "Hands are hidden, and you must read opponents from what they play and decline."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core take-or-play decision, hidden hands and bull runs survive once the piles are fixed at 3, randomness is reduced to the opening deal, and runs are capped. All of these fit the limits."
  },
  "variation": {
    "name": "Eleven Takes: Three Piles",
    "summary": "A compact, luck-light 11 Nimmt for 3 to 4 players. Players shed hidden hands onto 3 public piles using circular ascending plays. They take piles to reset them with a card of their choice, and use capped bull runs. The lowest ox-head penalty after one deal wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP\n1. Use a deck of cards numbered 1 to 40.\n2. Ox-heads per card: 3 if the number is a multiple of 10; 2 if it is a multiple of 5 but not of 10; 1 otherwise. The whole deck holds 52 ox-heads.\n3. Shuffle once. This is the only random event in the game. Deal 6 cards face down to each player as a private hand. Turn 3 cards face up to start Pile A, Pile B and Pile C, one card each. The remaining cards (13 with 4 players, 19 with 3) are set aside unseen for the rest of the game.\n4. Place a supply of bull tokens equal to the number of players minus 1 (3 with 4 players, 2 with 3 players).\n5. Seats are numbered 1 to N. Seat 1 moves first, and play proceeds in seat order.\n\nWHAT IS PUBLIC\n- The full ordered contents of every pile.\n- Each player's hand size and bull count.\n- Every action taken.\nOnly the contents of hands and the set-aside cards are hidden.\n\nLEGAL PLAY\n6. A card c may be played on a pile whose top card is t if (c - t) mod 40 is between 1 and 6. Examples: on 12 you may play 13 to 18; on 37 you may play 38, 39, 40, 1, 2 or 3.\n\nA TURN (one engine round)\n7. The active player privately chooses one action:\n   (a) PLAY card X onto pile P, where X is in their hand and legal on P; or\n   (b) TAKE pile P.\n   A player may take even when a legal play exists. If the chosen action is illegal, or the player has no legal play and chose PLAY, they instead TAKE the smallest pile (ties: A before B before C).\n8. If the player PLAYED: card X goes on top of pile P. If they hold at least 1 bull, they may then add one more card legal on the new top of the same pile. If they hold 2 or more bulls, they may add a second extra card the same way. They may stop at any point. An illegal extra card is ignored and ends the run. Bulls are not spent by using them.\n9. If the player TOOK pile P:\n   - All cards of P go into their hand.\n   - They must then choose any one card from their hand to place face up as the single card of the restarted pile P.\n   - If P held 3 or more cards before it was taken, the player gains a bull from the supply. If the supply is empty, they instead take one bull from the opponent holding the most bulls; ties go to the first such player in seat order after the taker. If no opponent has a bull, nothing happens.\n10. If the active player's hand is now empty, the game will end at the end of the current cycle, that is, after the player in seat N has finished their turn. Every player therefore gets the same number of turns.\n11. Pass the turn to the next seat.\n\nEND OF GAME\n12. The game ends at the end of the cycle in which any player emptied their hand. It also ends after 10 full cycles (40 turns with 4 players) or 12 full cycles (36 turns with 3 players), whichever comes first.\n13. Each player's penalty is the total ox-heads of the cards in their hand. A player with an empty hand scores 0.",
    "objective": "The player with the lowest penalty wins. If two or more players tie for lowest, the game is a draw among them (an engine draw).",
    "expected_effect": "All randomness is in the opening deal, and the full contents of every pile are public. Strong players track every card that has been seen and deduce which numbers opponents can hold. They restart taken piles with cards that block a rival's likely ranges or set up their own bull runs. They also time takes of piles with 3 or more cards to gain bulls, or to steal one from the leader. Taking a 1-card pile becomes a tempo move that does not grow your hand: you swap a card into a better position. Mindless policies lose. 'Always play the lowest legal card' gets stuck behind high tops. 'Always take the smallest pile' never empties a hand and is limited by the cycle cap. 'Always take the biggest pile' piles up ox-heads. Finishing the cycle removes the first seat's edge. A talk phase is left out: talk would add a message to every one of up to 40 sequential turns. In a sequential game where every action is already public, informal ganging up on the leader can be done through play itself, so talk would add words without adding a decision."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 16,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 40
  }
}
```
````
