# 01 design

- time: 2026-10-28T03:51:20+00:00 (103.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 cd164491b838fbe3, reply sha256 c18490f33363f802

## Sent

````
Original game: 3Up 3Down
Players in the original: 2 to 6

Original rules:
Each player gets 3 face-down blind cards (3DOWN) they cannot look at, then 6 cards to look at; they choose 3 to place face-up on their blind cards as their 3UP pile. Remaining 3 cards form their starting hand. Remaining deck is draw pile. On your turn clockwise you must play a card >= top of discard pile; you may play multiple copies of same rank together. If you can play, you must; after playing you refill hand to 3 from draw pile if possible. If you cannot play, you take the entire discard pile into your hand. Clear, Clear+1, Clear+2 beat any number and remove the discard pile from game; Clear ends turn, Clear+1 requires one extra play (may draw first), Clear+2 requires two extra plays. Three consecutive same numbers by any players also clears. When draw pile empty and hand empty, play from 3UP, then blindly flip one 3DOWN per turn if legal. First to empty all piles wins.
````

## Reply

````
```json
{
  "original_summary": "3Up 3Down is a 2-6 player shedding game in the Palace/Shithead family. Each player holds a hand, three face-up cards and three blind face-down cards. On your turn you play a card at least as high as the top of the discard pile, or you take the whole pile into your hand. Special Clear cards and three-of-a-kind runs wipe the pile, and the first player to get rid of every card wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Choices matter: when to spend a Clear, whether to dump a pair, which cards to put face-up. Simple policies (always play the lowest legal card) are beatable. However, play is forced whenever a card is legal, which narrows choices a lot. Seat 1 also gets a built-in tempo edge in what is a race to empty."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The deal decides much: who holds the Clears and high cards. The draw-pile refills add luck every turn. The endgame on the 3DOWN cards is pure coin-flipping, since you play cards you cannot see and the outcome is legal or pickup. A skilled player wins more often, but not reliably."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Tracking which cards opponents picked up (they were public on the pile), timing Clears, and holding high cards for the endgame give room to improve. A beginner can still win on a good deal."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, but every picked-up pile was seen. Inferring what an opponent can beat, and whether forcing them to pick up helps you, is real inference and opponent modelling."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The first player with no cards wins. Card legality is a numeric comparison."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Three card zones per player plus a draw pile with refills is a lot of state. 'Clear+1 requires one extra play, Clear+2 two' is a conditional block of extra turns, which the engine's flat step list cannot express. 2-6 players means up to 6 choice steps per round. Repeated whole-pile pickups make game length unbounded."
    }
  ],
  "problems": [
    "P1 Luck: the blind 3DOWN cards are played without any information, so the endgame is a coin flip.",
    "P2 Luck: random draw-pile refills every turn and an unbalanced deal of Clears and high cards make the deal decide too many games (lottery trap).",
    "P3 Platform: Clear+1 and Clear+2 force a variable number of extra plays, a conditional block of steps the engine cannot build.",
    "P4 Platform: up to 6 players exceeds 4 choice steps per round, and too many zones (hand, 3UP, 3DOWN, draw pile) means too many attributes.",
    "P5 Length: pickups can make the game run indefinitely; there is no round cap or fallback winner.",
    "P6 Balance: in a race to shed cards, the first player to act has a free tempo edge.",
    "P7 Narrow choice: the must-play rule often leaves only one legal option, so many turns take no thought."
  ],
  "changes": [
    {
      "what": "Remove the 3DOWN blind cards entirely.",
      "why": "Turns that are pure coin flips teach nothing.",
      "fixes": "P1 Luck: the blind 3DOWN cards are played without any information, so the endgame is a coin flip."
    },
    {
      "what": "Remove the draw pile. Deal all cards at the start by a stratified deal: each player gets exactly 3 low (1-3), 3 mid (4-6) and 3 high (7-9) cards, plus exactly one Clear.",
      "why": "Every hand is worth about the same, while the exact ranks stay hidden. No luck enters during play.",
      "fixes": "P2 Luck: random draw-pile refills every turn and an unbalanced deal of Clears and high cards make the deal decide too many games (lottery trap)."
    },
    {
      "what": "Make the only Clear a single card type that wipes the pile and ends the turn. Drop Clear+1 and Clear+2.",
      "why": "Every turn becomes exactly one play or one pickup, a flat step list.",
      "fixes": "P3 Platform: Clear+1 and Clear+2 force a variable number of extra plays, a conditional block of steps the engine cannot build."
    },
    {
      "what": "Fix the game at 3 players, each with a hidden hand and a public Up pile of 3 chosen cards.",
      "why": "Gives 3 turn choices plus 1 talk step per round, and few attributes. With three players one rival's loss is not automatically your gain.",
      "fixes": "P4 Platform: up to 6 players exceeds 4 choice steps per round, and too many zones (hand, 3UP, 3DOWN, draw pile) means too many attributes."
    },
    {
      "what": "Cap the game at 40 rounds. If nobody has gone out, the player with the fewest cards left wins; a tie for fewest is a draw.",
      "why": "Bounded length with an arithmetic fallback.",
      "fixes": "P5 Length: pickups can make the game run indefinitely; there is no round cap or fallback winner."
    },
    {
      "what": "The first player is chosen at random and receives an extra '1' card in hand. A 1 is a liability, playable only on an empty pile or on a 1.",
      "why": "Offsets the first mover's tempo advantage.",
      "fixes": "P6 Balance: in a race to shed cards, the first player to act has a free tempo edge."
    },
    {
      "what": "Allow a voluntary pickup at any time, even when you hold a legal card.",
      "why": "Taking a pile rich in high cards or Clears-worth of tempo becomes a real decision. This also removes the need for the engine to check whether a pickup was forced.",
      "fixes": "P7 Narrow choice: the must-play rule often leaves only one legal option, so many turns take no thought."
    },
    {
      "what": "Add one simultaneous message round at the start of each round.",
      "why": "Players can propose ganging up on the leader (all play high so the leader must pick up), bluff about their holdings, and test those claims against the public pickup record.",
      "fixes": "P7 Narrow choice: the must-play rule often leaves only one legal option, so many turns take no thought."
    }
  ],
  "keeps": [
    "Shedding race: the first to empty all cards wins.",
    "Play a card at least as high as the top of the pile, or take the whole pile into your hand.",
    "Playing several copies of one rank together.",
    "Clear cards that wipe the pile.",
    "Three consecutive cards of the same rank clear the pile.",
    "A face-up 3UP pile chosen by the player from their own cards and played only after the hand is empty."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (rising-pile shedding, pickups visible to all, Clears, face-up reserve) fits a 3-player sequential card game within the limits once blind cards, refills and the chained extra plays are removed."
  },
  "variation": {
    "name": "Three Up",
    "summary": "A 3-player Palace-style shedding race with no blind cards and no draw pile. Players have balanced hidden hands and choose a public 3-card Up pile. Each turn they beat the pile or take it, with Clears and three-of-a-kind runs wiping it. A short simultaneous talk opens each round.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "CARDS. There are 31 cards:\n- three copies each of ranks 1 to 9 (27 cards);\n- three Clear cards;\n- one extra '1' (the handicap card).\n\nSETUP.\n1. Choose one of the three players at random to be First. Turn order is First, then the next seat, then the last seat, and it stays the same in every round.\n2. Make three separate shuffled stacks: Low (all 1s, 2s, 3s except the handicap card; 9 cards), Mid (all 4s, 5s, 6s; 9 cards) and High (all 7s, 8s, 9s; 9 cards).\n3. Deal each player 3 cards from Low, 3 from Mid, 3 from High, and 1 Clear, for 10 cards each. First also receives the handicap '1', for 11 cards.\n4. Each player privately looks at their cards.\n5. At the same moment, each player chooses exactly 3 of their cards to form their Up pile. These 3 cards are revealed to everyone.\n6. The other cards are the player's Hand, which only that player sees.\n7. The discard Pile starts empty.\n\nWHAT EVERYONE CAN SEE AT ALL TIMES. Everyone can see:\n- every card on the Pile;\n- the top rank of the Pile;\n- the run count (how many cards of the top rank are on top of the Pile in a row);\n- every player's Up pile;\n- every player's card counts;\n- the full history of plays and pickups.\n\nEACH ROUND.\n(a) TALK. Every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages bind no one.\n(b) TURNS. Each player in turn order takes one turn, as described below.\n(c) END CHECK. After every turn, if the player who just acted has no cards left in Hand and Up pile, that player wins and the game ends immediately.\n(d) ROUND CAP. After the last turn of round 40, the game ends.\n\nA TURN. The player chooses one action.\n- PLAY: choose one rank and play one or more copies of that rank together, all from the same source. The source must be your Hand if your Hand has any cards; you may play from your Up pile only when your Hand is empty.\n  - A numbered play is legal only if the Pile is empty or the rank is greater than or equal to the Pile's top rank.\n  - A Clear is always legal and is played alone.\n- PICK UP: take every card on the Pile into your Hand; the Pile becomes empty. You may pick up at any time, even if you have a legal play. If the Pile is already empty, a pick up does nothing.\n- An illegal or unreadable choice counts as PICK UP.\n\nRESOLVING A PLAY.\n- Played numbered cards go on top of the Pile. If the top rank is the same as before, the run count rises by the number of cards played; otherwise the run count equals the number of cards played.\n- If the run count reaches 3 or more, the Pile is cleared: removed from the game, now empty, run count 0.\n- If a Clear is played, the Clear and the whole Pile are removed from the game and the Pile is empty.\n- In every case the turn then ends, and the next player acts on whatever Pile remains (an empty Pile accepts any card).",
    "objective": "The first player to have no cards in Hand and Up pile wins immediately. If nobody has done so after round 40, the player with the fewest cards (Hand plus Up pile) wins. If two or three players tie for fewest, the game is a draw.",
    "expected_effect": "Luck is confined to the exact ranks inside each band of the deal; every hand has one Clear and the same band profile, and the handicap '1' offsets the first mover's tempo. Since every picked-up card was public, strong players track what each opponent holds. They then play to strand a rival (lay a 9 when a rival is known to hold only low cards), save Clears for the moment a big Pile threatens them, and take a voluntary pickup when the Pile holds high cards they can use. The Up-pile choice is a plan: high cards in the Up pile protect the endgame, but revealing them tells opponents what you can still beat. Simple policies all lose to tracking play. 'Always play the lowest legal card' burns tempo and gets stranded. 'Always play the highest' wastes power cards and then must pick up. 'Always pick up' never sheds. Talk passes both tests. The conflict is that only one player can win. The two trailing players want to cooperate against the leader by playing high so the leader must pick up, but each also wants to be the one who benefits. A player who obeys a proposal to 'both play high now' may spend their own last high card and be stranded themselves. Claims such as 'I have no 8s left' can be checked against the public pickup record, so bluffing and trust-reading are real."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 40
  }
}
```
````
