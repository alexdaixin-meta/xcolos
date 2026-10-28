# 01 design

- time: 2026-10-28T03:55:45+00:00 (92.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 b6e16bb0d6664c21, reply sha256 908e3c84330711ea

## Sent

````
Original game: Yaniv
Players in the original: 2 to 8

Original rules:
Each player is dealt 5 cards from a 54-card deck including jokers. Values: Ace=1, 2-10 face, J/Q/K=10, Joker=0. A draw pile and one upcard discard pile remain. On a turn you may discard: one card, two+ equal rank, or 3+ same-suit consecutive ranks with Ace low. After discarding you must draw one card: top of draw pile or only the first or last card of the previous set from discard. If draw pile empties, reshuffle discards except last play. At start of your turn if hand sum is below the Yaniv threshold (commonly 5-7) you may call Yaniv instead of playing. All hands are revealed. Lowest hand wins the round with 0. Others score their hand sum. If caller is not strictly lowest (Asaf), caller gets hand sum +30 penalty. Total score accumulates across rounds. A player exceeding 200 points is eliminated; last remaining or lowest total when first elimination occurs wins.
````

## Reply

````
```json
{
  "original_summary": "Yaniv is a draw-and-discard card game for 2 to 8 players. Each player tries to lower the point total of a hidden 5-card hand and call 'Yaniv' when it is low enough. A caller who is not strictly lowest is caught ('Asaf') and takes a 30-point penalty. Points pile up over many deals until someone passes 200, and the lowest total wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. 'Always call at the threshold' is punished by Asaf whenever an opponent waited and holds less. 'Never call' banks the full hand sum every time someone else calls. 'Always discard the highest card' throws away pairs that would shrink the hand faster. The only seat edge is a mild one from turn order, which goes to whoever moves first after the deal."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Skill matters in card tracking, in choosing which card to keep, and in timing the call against what opponents have picked up. Over one deal, though, the 5-card deal and the blind draws dominate. Only the long multi-deal game lets skill show. With 2 to 8 players and a 200-point limit, games run very long."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still scores by dumping high cards and calling when eligible. A strong player keeps improving by tracking which cards each opponent took from the discard pile, estimating their hand sums, and baiting or avoiding Asaf."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Discards and pickups from the discard pile are public, so each opponent's hand sum must be inferred from partial evidence. Deciding when to call is a judgement about opponents' likely totals."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Round scores are hand sums plus a fixed penalty, and the winner is the lowest total. All of it is arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based and text-only, but the original does not fit the build limits. Up to 8 players each take sequential turns with two choices, which is far more than 4 choice steps per round. Every player's draw is a separate random event, against a limit of 1 per round. Same-suit run validation, reshuffling the discard pile and a 200-point limit together mean long chains of rules and games far beyond 40 rounds."
    }
  ],
  "problems": [
    "Sequential turns for many players need far more than 4 choice steps per round and multiple random draws per round.",
    "Each player drawing their own blind card is several chance events per round.",
    "Same-suit runs, suit tracking and reshuffling the discard pile add long rule chains for little strategic gain.",
    "The 200-point elimination limit makes games far too long for a 40-round cap.",
    "Turn order gives a small structural seat edge, since the first player after the deal can act on an untouched hand.",
    "Within a single deal luck is heavy, so the game must run several deals inside the round cap for skill to show.",
    "Simultaneous calls by several players are not defined in the original and must be, once players act at the same time."
  ],
  "changes": [
    {
      "what": "Each round all players act at the same moment with two simultaneous choices: (1) call Yaniv, or discard one card or a set of equal-value cards; (2) take the face-up card or the blind card.",
      "why": "This collapses N sequential turns into 2 choice steps per round, whatever the player count, and removes turn order.",
      "fixes": "Sequential turns for many players need far more than 4 choice steps per round and multiple random draws per round."
    },
    {
      "what": "There is one shared blind card per round, hidden until after choices. Everyone who chose 'blind' receives a copy of it. That blind card then becomes the next round's face-up card. Cards are drawn from a shoe with the 54-card deck's frequencies, reshuffled every draw.",
      "why": "Exactly one chance event per round. The face-up card is known and the blind card is a gamble, so the original choice between the discard pile and the deck survives. Taking the known card reveals part of your hand to opponents.",
      "fixes": "Each player drawing their own blind card is several chance events per round."
    },
    {
      "what": "Runs are removed. Players may discard one card, or two or more cards of equal value. Because hands shrink more slowly without runs, the call threshold is raised from 7 to 10.",
      "why": "This keeps the hand-shrinking value of sets and the logic of holding pairs. It drops suit tracking and run validation.",
      "fixes": "Same-suit runs, suit tracking and reshuffling the discard pile add long rule chains for little strategic gain."
    },
    {
      "what": "The elimination limit drops to 100 points and the game is capped at 40 rounds. The game ends on the first elimination or after round 40, and the lowest total wins.",
      "why": "Several deals fit inside the cap, so card luck averages out across deals while the game stays short.",
      "fixes": "The 200-point elimination limit makes games far too long for a 40-round cap."
    },
    {
      "what": "All players act simultaneously, so no one moves first. Every hand is dealt at the same moment.",
      "why": "This removes the seat advantage completely.",
      "fixes": "Turn order gives a small structural seat edge, since the first player after the deal can act on an untouched hand."
    },
    {
      "what": "Deals continue inside the 40 rounds. A deal left unfinished at round 40 is scored with no zero for anyone. The player count is 3 to 4.",
      "why": "Running several deals makes inference and call timing outweigh any single deal. The no-zero ending punishes stalling.",
      "fixes": "Within a single deal luck is heavy, so the game must run several deals inside the round cap for skill to show."
    },
    {
      "what": "Simultaneous calls are defined. A caller scores 0 only if their hand sum is strictly lower than every other player's. Any other caller is caught (Asaf) and scores hand sum + 30. Non-callers holding the lowest sum score 0, and everyone else scores their hand sum.",
      "why": "This gives a precise arithmetic resolution for simultaneous play and keeps Asaf as the central risk.",
      "fixes": "Simultaneous calls by several players are not defined in the original and must be, once players act at the same time."
    }
  ],
  "keeps": [
    "Hidden hands whose point total each player tries to lower.",
    "The original card values: Ace 1, 2 to 10 face value, J/Q/K 10, Joker 0.",
    "Discarding single cards or sets of equal value, then drawing one card.",
    "The choice between a known face-up card and an unknown blind card.",
    "Calling Yaniv below a threshold, and the Asaf 30-point penalty for a caller who is not strictly lowest.",
    "Points building up over several deals, an elimination limit, and the lowest total winning."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Yaniv fits the platform once turns become simultaneous and draws are shared: hidden hands, public discards and pickups, and the risky call. Hand-sum inference and call timing are strong reasoning tests."
  },
  "variation": {
    "name": "Simultaneous Yaniv",
    "summary": "Three or four players hold hidden hands and all act at once each round. Each discards cards and takes either the known face-up card or a shared hidden blind card, trying to get their hand low enough to call Yaniv without being undercut (Asaf). Several deals are played within 40 rounds, and the lowest total wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "CARDS. Card values: Ace = 1, 2 to 10 = face value, Jack/Queen/King = 10, Joker = 0. Suits do not matter. Every card is drawn from a shoe with the frequencies of a 54-card deck, which is reshuffled before every draw:\n- each value from 1 to 9: 4 in 54;\n- value 10 (10, J, Q, K): 16 in 54;\n- value 0 (Joker): 2 in 54.\n\nDEALING. At the start of the game and at the start of every new deal, every player is dealt 5 cards and one face-up card is turned over. This counts as the single chance event of that round. Each player sees only their own hand. Everyone sees the face-up card, every player's hand size, and every player's running total.\n\nEACH ROUND:\n(1) Public announcement: round number, face-up card, all hand sizes, all totals, and the previous round's discards and pickups.\n(2) Each player is privately shown their hand and its sum.\n(3) FIRST CHOICE, simultaneous. Each player secretly chooses one of:\n- CALL, allowed only if their hand sum is 10 or less;\n- DISCARD a single card from their hand;\n- DISCARD two or more cards of equal value from their hand.\nAn illegal answer is replaced by discarding the single highest card.\n(4) SECOND CHOICE, simultaneous. Every player who did not call secretly chooses FACE-UP (take a copy of the current face-up card) or BLIND (take a copy of this round's blind card, unseen). Callers make no second choice.\n(5a) If at least one player called, there is a SHOWDOWN. Discards and pickups are cancelled and all hands are revealed as they stood. Let L be the lowest hand sum among all players.\n- A caller whose sum is strictly lower than every other player's sum scores 0.\n- Any other caller is caught (Asaf) and scores hand sum + 30.\n- A non-caller whose sum equals L scores 0.\n- Every other non-caller scores their hand sum.\nScores are added to totals. If no player has 100 or more, a new deal begins next round.\n(5b) If no one called:\n- the discarded cards are removed;\n- one blind card is drawn (the round's chance event);\n- each BLIND chooser receives that card and each FACE-UP chooser receives the face-up card;\n- all discards are announced publicly, along with who took FACE-UP and who took BLIND;\n- the blind card's value is then revealed and becomes the face-up card for the next round.\nA player's hand cannot drop below 1 card, because a draw always follows a discard.\n(6) End check:\n- If any player's total is 100 or more after a showdown, the game ends.\n- After round 40, if a deal is still in progress, all hands are revealed and every player adds their full hand sum, with no zeros. The game then ends.",
    "objective": "When the game ends, the player with the strictly lowest total wins. If two or more players tie for the lowest total, the game is a draw.",
    "expected_effect": "Players must track each opponent's likely hand sum from public evidence: hand size, which cards they discarded, and whether they took the known face-up card. They must time their calls against those estimates. Calling the moment you reach 10 risks Asaf against a patient opponent. Waiting risks being caught with a big hand. Choosing between FACE-UP and BLIND trades a known value, which also reveals information to opponents, against a hidden gamble. Keeping pairs to shrink the hand competes with dumping high cards. No seat has an edge, and playing several deals lets skill outweigh any one deal. Talk is left out: players' interests do conflict, but every claim would concern a hand sum nobody can verify, and the real evidence is already in the public discards and pickups. Talk would add words without adding reasoning, and it would cost steps."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 2,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
