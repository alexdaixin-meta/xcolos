# 03 design

- time: 2026-10-28T01:34:20+00:00 (102.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 4ac1da1f72bad975, reply sha256 9976365139c2d63f

## Sent

````
Original game: Dont Mess With Cthulhu
Players in the original: 3 to 6

Original rules:
Setup: for 4-6 players use 3-4 Investigators vs 2 Cultists, plus extra hidden tokens, shuffle and deal one role face down to each player. Build Investigation deck per player count with Futile cards, Elder Signs equal to player count, and one Cthulhu, shuffle and deal five to each player face down. Each player looks at own cards, notes counts but shuffles so positions unknown, then may lie about contents. Play is four rounds. Each round has actions equal to player count. Active player chooses one face-down Investigation card belonging to another player and reveals it. If Cthulhu is revealed Cultists win instantly. If all Elder Signs revealed Investigators win instantly. Otherwise the owner of the revealed card becomes next Active player. After actions equal to player count, collect remaining face-down cards, reshuffle and redeal evenly, one fewer per player each round. After four rounds without all Signs, Cultists win.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: The variation removes the reshuffle and redeal. Every revealed card is gone for good, and each reveal is a uniformly random card from the named hand. Investigators must reveal ALL N Signs before the single Cthulhu, and within 4N of the 5N cards.

Baseline with uninformed choices (any naming policy independent of hand contents, so the reveal order is a random permutation):
- P(Investigators win) = P(Cthulhu is last among the N+1 special cards) x P(the last Sign is at position 4N or earlier).
- N=4: 1/5 x [C(16,5)+4*C(16,4)]/C(20,5) = 0.2 x (4368+7280)/15504 = 0.2 x 0.751 = 0.150.
- N=6: 1/7 x [C(24,7)+6*C(24,6)]/C(30,7) = 0.143 x (346104+807576)/2035800 = 0.143 x 0.567 = 0.081.
So random play gives Cultists about 85% (N=4) to 92% (N=6).

Ceiling with PERFECT information (Investigators know every hand and never touch the Cthulhu hand except to extract its Signs):
- Signs in the Cthulhu holder's hand must still be drawn at random before Cthulhu, with probability 1/(s+1).
- N=5, s = Signs among the holder's other 4 cards: P(s=0)=0.365, P(s=1)=0.456, P(s=2)=0.161, P(s=3)=0.018.
- Best case = 0.365 + 0.456/2 + 0.161/3 + 0.018/4 = about 0.65, before deception and Cultist-controlled cuts.

In real play:
- Cultists lie: they claim Cthulhu to shield Sign-holding hands, or claim Signs while holding Cthulhu.
- Whenever a hidden Cultist is named, they become active and cut the truthful Cthulhu claimant.
- Investigators therefore realistically sit well under 50%.

Winner-rule test:
- Cultist policy 'always cut a random other player, always say "no Cthulhu, 1 Sign"' wins about 85-92% against any Investigator play that cannot see through the lies.
- The Cultist side never needs to do anything, because the cut limit and the single Cthulhu card both default to Cultists.
- Seat edge: none (roles are random). Team edge: overwhelming for Cultists, so both sides cannot realistically win.
- reasoning_over_luck FAILED: There is real material to infer: claimed hand counts are falsified over time by reveals, and players can track who sends cuts toward whom. But the result is dominated by draws Investigators cannot control.

- Good play cannot remove the core risk. Even with perfect knowledge, Investigators must pull every Sign out of the Cthulhu holder's hand by blind draw. That fails about 35% of the time at N=5, and more often when this hand holds 2 or more Signs.
- Seeing through the deception fully (the ceiling) only brings Investigators to about 65%. Real reasoning lands well below that, at perhaps 30-45%, against a random-play baseline of 8-15%. Skill moves Investigators from 'almost always lose' to 'usually lose'.
- When both sides play their intended strategies (Investigators avoid suspected Cthulhu hands; Cultists lie and cut suspected Cthulhu hands), the decisive event is usually one blind draw from a mixed hand. Chance therefore decides a large share of games, roughly half or more.
- A Cultist who reasons well gains little over one who just cuts randomly, because the defaults already favour them.
- change: Rebalance the win condition so random-play Investigators win about 35-40% and informed play about 55-60%, and show the calculation. For example, put N+2 Elder Signs in the deck but require only N revealed, so a Sign trapped in the Cthulhu hand need not be extracted. Alternatively, keep N Signs but require only N-1.
- change: Restore the original per-round collect, reshuffle and redeal (one fewer card each round), so a Sign is not permanently trapped beside Cthulhu and claims must be re-made and re-inferred each round. Alternatively, allow Investigators to win if every remaining unrevealed Sign is in a hand confirmed to contain Cthulhu.
- change: Reduce blind luck in the reveal. Give each hand fixed, numbered positions, let the active player choose a specific position, and let the hand's owner privately know what each position holds. Then claims such as 'card 3 is safe' become inferable and testable rather than every reveal being a pure random draw.
- change: After rebalancing, re-run the thoughtless-policy check. The Cultist policy 'cut randomly, always claim 1 Sign and no Cthulhu' must lose a meaningful share of games against Investigators who track claims against reveals.
The variation that was reviewed: Don't Cut Cthulhu: SETUP.
1. Role tokens: with 4 players, shuffle 3 Investigator and 2 Cultist tokens, deal 1 to each player and set the 5th aside unseen, so there are 1 or 2 Cultists. With 5 players, use 3 Investigators and 2 Cultists. With 6 players, use 4 Investigators and 2 Cultists. Each player privately learns only their own role. Cultists do not learn who the other Cultist is.
2. Card deck: 5 cards per player in total. The deck holds Elder Signs equal to the number of players, exactly 1 Cthulhu, and the rest Futile cards. With 4 players: 4 Signs, 1 Cthulhu, 15 Futile. With 5 players: 5 Signs, 1 Cthulhu, 19 Futile. With 6 players: 6 Signs, 1 Cthulhu, 23 Futile. Shuffle and deal 5 cards to each player.
3. Each player is told privately how many Signs, Cthulhu and Futile cards their own hand holds. Everyone can always see how many cards each player has left, how many Signs have been revealed, and how many cuts have been made.
4. Player 1 is the first active player. Roles are random, so this gives no team an edge.

EACH ROUND (one cut).
1. Talk: every player writes one short message at the same time without seeing the others. Players may claim anything about their hand or anyone's role, truthfully or not. All messages are then shown to everyone.
2. Cut: the active player names one other player who has at least 1 card left. You may not name yourself.
3. Reveal: one card is taken uniformly at random from the named player's remaining cards and revealed to all. It is removed from that hand and does not return.
4. If it is Cthulhu, the Cultists win immediately.
5. If it is an Elder Sign, add 1 to Signs revealed. If Signs revealed equals the number of players, the Investigators win immediately.
6. The named player becomes the active player for the next round.
7. Add 1 to cuts made. If cuts made equals 4 times the number of players (16, 20 or 24), the game ends and the Cultists win.

Talk is never binding, and no cards or information may be exchanged except through messages. Winner: Team victory decided by counting. If Cthulhu is revealed, every Cultist wins and every Investigator loses. If the number of revealed Elder Signs reaches the player count before that, every Investigator wins and every Cultist loses. If the cut limit of 4 times the player count is reached first, every Cultist wins. With 4 players the unused role token is never a player and wins nothing. There are no draws.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Don't Mess With Cthulhu is a hidden-role bluffing game. Secret Investigators and Cultists take turns choosing face-down cards from other players' hands. Investigators win by revealing every Elder Sign; Cultists win if Cthulhu is revealed or the cut limit runs out. The previous XColos variation removed the reshuffle and made each reveal a uniformly random card from the named hand.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the previous variation, Investigators must reveal all N Signs before the single Cthulhu and within 4N cuts. Uninformed play gives them 15% at 4 players and 8% at 6. The thoughtless Cultist policy (cut a random player, always claim 'no Cthulhu, 1 Sign') wins about 85-92%. Both the cut limit and the Cthulhu card default to the Cultists, so the Cultist side barely has to choose anything. Seats are fair because roles are random, but the teams are not."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Every reveal is a blind random card from the named hand. Even with perfect knowledge, Investigators must pull the Signs out of the Cthulhu holder's hand at random, and the ceiling is about 65% at 5 players. When both sides play well, a single blind draw from a mixed hand decides roughly half the games. A reasoning Cultist gains little over one cutting at random."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "There is material to improve on: tracking claims against reveals, and tracking who cuts toward whom. But Investigators move only from 'almost always lose' to 'usually lose', and Cultists have almost no room to improve over the default."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Roles and hand contents are hidden and claims can be lies, so there is something to infer. Inference cannot be acted on precisely, though: knowing a hand holds 1 Sign and 4 Futile does not let you take the Sign, because the draw is random."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The winner follows from counts: Cthulhu revealed, Signs revealed against the target, and cuts made against the limit. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is turn-based and text-only, with one simultaneous talk step and one named cut per round. It has no board, at most 24 rounds, two hidden elements and one random draw per round."
    }
  ],
  "problems": [
    "P1 Team imbalance: Investigators need all N of N Signs before the single Cthulhu and within 4N cuts. Random play gives them 8-15%, and a thoughtless Cultist policy wins about 85-92%.",
    "P2 Blind-draw luck: each reveal is a random card from the named hand, so even perfect inference cannot target a known Sign or avoid a known Cthulhu. One draw often decides the game.",
    "P3 Trapped Signs: a Sign sitting beside Cthulhu in one hand can only be extracted by gambling on that hand. This caps Investigators at about 65% even with perfect knowledge.",
    "P4 Cultists have no meaningful decisions: the defaults (cut limit, single Cthulhu) win for them, so reasoning Cultists barely outperform random ones.",
    "P5 Claims are hard to test: hand-level counts ('1 Sign') are only slowly falsified by random reveals, so lying is cheap and truth-telling earns little trust."
  ],
  "changes": [
    {
      "what": "Each hand has fixed numbered positions 1-5. The owner privately knows exactly what is in each position. The active player names a player AND a position, and that exact card is revealed. No random card is drawn during play.",
      "why": "Inference becomes action. If you trust a claim that 'my position 3 is a Sign', you can take exactly that card, and you can steer away from a claimed Cthulhu. Each cut is a deliberate bet on someone's honesty, not a lottery.",
      "fixes": "P2 Blind-draw luck"
    },
    {
      "what": "The deck holds N+2 Elder Signs, where N is the player count, but Investigators need only N revealed. The cut limit stays at 4N.",
      "why": "Two Signs can be left behind, so a Sign beside Cthulhu or in a distrusted hand never has to be dug out. Random play rises to about 40% / 34% / 28% for 4 / 5 / 6 players (calculation in expected_effect), leaving room for skill on both sides.",
      "fixes": "P1 Team imbalance"
    },
    {
      "what": "Named positions replace the reshuffle and redeal. Because the active player chooses the exact card, any Sign whose position is known can be taken directly, even from the Cthulhu holder's hand. With the 2-Sign slack, it can also be ignored.",
      "why": "This removes the trap without adding a random redeal step, which keeps the build simple.",
      "fixes": "P3 Trapped Signs"
    },
    {
      "what": "Claims are now about positions ('position 2 is Futile, position 4 is a Sign'), and every reveal publicly confirms or exposes one specific earlier claim.",
      "why": "Position claims are checked exactly and immediately, so trust is earned and lost card by card. This gives Cultists a real decision: when to spend a reputation built on true claims in order to betray.",
      "fixes": "P5 Claims are hard to test"
    },
    {
      "what": "The rules now make clear what Cultists can do. When a Cultist is active, they can try to locate Cthulhu from contradictions in the talk (two players both claiming it, or a cagey hand), or stall by naming claimed-Futile cards. A Cultist holding Cthulhu chooses when to label it falsely as a Sign.",
      "why": "Cultist results now depend on reading the table and timing a lie. Random cutting hits Cthulhu only about 1 time in 20 per cut.",
      "fixes": "P4 Cultists have no meaningful decisions"
    },
    {
      "what": "The simple policies were re-checked under the new rules (see expected_effect).",
      "why": "This confirms that every thoughtless policy can lose, including the Cultist policy of cutting at random and always claiming '1 Sign, no Cthulhu'.",
      "fixes": "P1 Team imbalance"
    }
  ],
  "keeps": [
    "Secret Investigator and Cultist roles dealt at random; with 4 players, one unseen spare role token creates doubt about how many Cultists there are.",
    "A deck of Elder Signs, Futile cards and exactly one Cthulhu, with 5 cards dealt face down to each player.",
    "Owners know their own cards and may lie freely about them.",
    "The active player cuts another player's card, and the owner of the cut card becomes the next active player.",
    "Instant Cultist win on Cthulhu, instant Investigator win on enough Elder Signs, and a cut limit that favours the Cultists."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The hidden-role, claim-and-cut core is strong reasoning material. The previous variation failed because of the random reveal and the all-Signs requirement, and both can be fixed within the limits."
  },
  "variation": {
    "name": "Don't Cut Cthulhu: Named Cards",
    "summary": "A hidden-role bluffing game. Each player privately knows what lies in each numbered position of their own hand. Players make public claims at the same time, then the active player names one exact card of another player to reveal. Investigators need N Elder Signs out of N+2 before Cthulhu appears or the cuts run out. Cultists need Cthulhu revealed or the clock to expire.",
    "players": {
      "min": 4,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP.\n1. Roles. With 4 players, shuffle 3 Investigator and 2 Cultist tokens, deal 1 face down to each player and set the 5th aside unseen, so there are 1 or 2 Cultists. With 5 players, deal 3 Investigators and 2 Cultists. With 6 players, deal 4 Investigators and 2 Cultists. Each player privately learns only their own role. Cultists are not told who the other Cultist is.\n2. Deck. There are 5 cards per player. The deck holds Elder Signs equal to the number of players plus 2, exactly 1 Cthulhu, and Futile cards for the rest. With 4 players: 6 Signs, 1 Cthulhu, 13 Futile (20 cards). With 5 players: 7 Signs, 1 Cthulhu, 17 Futile (25 cards). With 6 players: 8 Signs, 1 Cthulhu, 21 Futile (30 cards). Shuffle and deal 5 cards face down to each player, placed in positions numbered 1 to 5. Positions never move or renumber.\n3. Private knowledge. Each player is told privately exactly what card is in each of their own 5 positions.\n4. Public information, always visible to everyone: which positions of each player are still face down; every card revealed so far, with its owner and position; Signs revealed; cuts made; the target (Signs needed = number of players); the cut limit (4 times the number of players: 16, 20 or 24); and who is active.\n5. Player 1 is the first active player. Roles are random, so this gives no team an edge.\n\nEACH ROUND (one cut).\n1. Talk. Every player writes one short message at the same time, without seeing the others. Messages may claim anything: the contents of any of your positions, guesses about others' roles, or requests about whom to cut. Lying is allowed. All messages are then shown to everyone.\n2. Cut. The active player names one other player and one of that player's face-down positions. You may not name yourself or an already revealed position.\n3. Reveal. That exact card is turned face up for everyone. It stays revealed and is out of play.\n4. If it is Cthulhu, the Cultists win immediately.\n5. If it is an Elder Sign, add 1 to Signs revealed. If Signs revealed equals the number of players (4, 5 or 6), the Investigators win immediately.\n6. The named player becomes the active player for the next round.\n7. Add 1 to cuts made. If cuts made equals 4 times the number of players, the game ends and the Cultists win.\n\nNOTES. Talk is never binding. Nothing may be exchanged except through the public messages. Players can never look at another player's cards. With 4 players, the unused role token is not a player and wins nothing.",
    "objective": "This is a team victory decided by counting. If Cthulhu is revealed, every Cultist wins and every Investigator loses. If Signs revealed reaches the number of players before that, every Investigator wins and every Cultist loses. If cuts made reaches 4 times the number of players first, every Cultist wins and every Investigator loses. Exactly one of these happens, so there are no draws.",
    "expected_effect": "RANDOM BASELINE (positions named with no regard to claims, so the reveal order is a random permutation). Investigators win when Cthulhu falls after the N-th Sign among the N+3 special cards, and the N-th Sign comes within 4N cuts.\n- 4 players: P(Cthulhu ranks 5th or later of 7 specials) = 3/7 = 0.43. P(at most 2 of the 6 Signs are in the last 4 cards) = 1 - (C(6,3)·14 + C(6,4))/C(20,4) = 1 - 295/4845 = 0.94. Combined, about 0.40.\n- 5 players: 3/8 = 0.375 times about 0.89 (1 - 6006/53130), about 0.34.\n- 6 players: 3/9 = 0.333 times about 0.83 (1 - 103670/593775), about 0.28.\nSo random Investigators lose most games but not all, which fixes the 8-15% floor.\n\nINFORMED PLAY. An Investigator holding Cthulhu knows its exact position. Signs can be taken precisely from players whose claims have been confirmed, and 2 Signs can be abandoned. The perfect-information ceiling is now essentially 100%, because nothing random remains during play. What stands between Investigators and the win is deception only.\n\nCHECK OF SIMPLE POLICIES.\n(a) Cultists cut at random and always claim '1 Sign, no Cthulhu'. Each random Cultist cut hits Cthulhu with probability about 1/remaining cards (about 5% per cut), and Cultists are active only when named. Investigators who cut only into claims that have been confirmed, and treat 'always 1 Sign' players as suspects, win an estimated 55-65%. This policy therefore loses a meaningful share.\n(b) Investigators always trust every Sign claim. A Cultist holding Cthulhu labels it a Sign and wins at once. This policy loses heavily.\n(c) Always name the lowest position of the next player. This behaves like random play: 28-40% for Investigators, so it can lose and can win.\n(d) Never talk, or always tell the truth, as an Investigator. Silence gives teammates nothing to chain on. Full truth exposes your Cthulhu position to an active Cultist. Both can lose.\nWith both sides reasoning, I expect a roughly even contest, decided by who reads and times the lies better rather than by any draw.\n\nTALK EARNS ITS PLACE. Players disagree because the teams are hidden. Investigators want a chain of trusted cutters passing the turn among themselves. Cultists want to be trusted, then either bait a cut onto Cthulhu or burn cuts. An Investigator holding Cthulhu faces a real dilemma: warning teammates also tells an active Cultist exactly where to cut. A player who simply follows proposals can lose by cutting a Cultist's falsely labelled 'Sign', or by naming a Cultist and handing them the active turn. Talk is simultaneous, so nobody can tailor a claim to the others' messages within the same round.\n\nLOTTERY CHECK. The deal decides who holds Cthulhu and the Signs, but only changes what each side knows and must hide. A Cultist dealt Cthulhu is dangerous only if trusted, and can be found out through contradictions in their claims. Good play, not the deal, decides the result."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 3,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 24
  }
}
```
````
