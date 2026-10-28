# 01 design

- time: 2026-10-28T04:07:10+00:00 (67.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 f6c60129d0ec2919, reply sha256 7114d397e51adb46

## Sent

````
Original game: Wyatt Earp
Players in the original: 2 to 4

Original rules:
The game is played over multiple hands. Seven outlaw colors exist. Setup: 10 cards dealt to each player, remaining cards form a draw pile with one discard. Each outlaw has a reward poster starting at $1000. On your turn you must draw: either 2 from draw pile or 1 from discard. Then you may play any number of outlaw cards of one or more colors, but at most one sheriff card. The first play for a color must be a set of at least 3 same-color outlaws. Later any number can be added. When you play N cards of a color, add (N-1)*$1000 to that poster's bounty. Sheriff cards modify CP and bounty: Photo adds 4 CP and $1000, requires color already opened; Stagecoach and Bank Robbery require a shot - reveal top draw card, succeed on outlaw (bullet hole) then add 1 CP+$3000 or 2 CP+$1000. Other sheriffs steal, block, etc. You must discard one card to end turn, with no effect. When draw pile empties first time, reshuffle discard except top card. When it empties second time, hand ends and each poster is split among players proportional to CP in that color. Most total money after agreed number of hands wins.
````

## Reply

````
```json
{
  "original_summary": "Wyatt Earp is a 2-4 player rummy-style card game. Players collect and lay down sets of seven outlaw colours. Each play raises that outlaw's shared reward poster, and at the end of a hand every poster is split among the players in proportion to the capture points they hold in that colour. Sheriff cards add shots, steals and blocks.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy dominates. Always laying down sets as soon as possible feeds bounties that rivals can share, and hoarding risks being caught when the pile runs out. The shared-poster split creates real choices about which colour to back. Turn order gives the first player a slight tempo edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The deal decides a great deal. Who is dealt a long run in one colour, and who draws the sheriff cards (steals, photos), shapes most of a hand. Stagecoach and Bank Robbery are pure coin-flips on the top card. Skill shows over several hands, but luck is large in any one hand."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Timing your melds, reading which colours rivals collect from their discard pickups, and choosing between majority and minority stakes give strong players room to improve. A weak player still collects some share by playing sets."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players infer rivals' colours from discard pickups and from what they play, and they must decide whether to grow a poster they will only partly own."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Bounties, capture points and the proportional split are all arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "It needs a large deck with draw and discard piles and a double reshuffle, about 10-card hands, many distinct sheriff card effects (steal, block, photo, shots), sequential multi-play turns with meld validation, and several hands. That is far beyond 20 steps and 3 hidden elements, and turns are free-form rather than simple polls."
    }
  ],
  "problems": [
    "Card-deck mechanics (draw pile, discard pickup, reshuffles, set validation) and the many distinct sheriff card effects exceed the step and complexity limits.",
    "Luck of the deal and the coin-flip shots weigh heavily against skill within a hand.",
    "Who holds a long run of one colour is decided by the deal, a lottery that good play cannot fully correct.",
    "Sequential turns give a tempo edge to earlier seats.",
    "A full game spans several hands of unbounded length, too long for the platform."
  ],
  "changes": [
    {
      "what": "Replace the card hand with an equal budget of 15 deputies per player, committed to outlaws over 6 rounds (0-5 per round, one outlaw per round).",
      "why": "This keeps the core decision of how much to commit to which outlaw, and when, without deck handling or meld validation.",
      "fixes": "Card-deck mechanics (draw pile, discard pickup, reshuffles, set validation) and the many distinct sheriff card effects exceed the step and complexity limits."
    },
    {
      "what": "Keep the bounty growth rule: committing N deputies at once adds (N-1) x $1000 to the poster. Keep the end-of-game proportional split by capture points.",
      "why": "Large single commitments stay efficient, as with big melds, and shared posters stay double-edged.",
      "fixes": "Card-deck mechanics (draw pile, discard pickup, reshuffles, set validation) and the many distinct sheriff card effects exceed the step and complexity limits."
    },
    {
      "what": "Each player gets one secret informant outlaw, distinct from the other players'. Deputies on that outlaw earn double capture points. Capture points stay hidden until the end; only deputy counts are announced.",
      "why": "Every player gets the same-sized advantage, so the deal changes what to do, not who is ahead. Rivals must infer each informant from behaviour, and nobody knows their exact share of a contested poster.",
      "fixes": "Who holds a long run of one colour is decided by the deal, a lottery that good play cannot fully correct."
    },
    {
      "what": "Replace sheriff cards and shots with one public random event per round: a Sighted outlaw whose poster gains $1000 that round.",
      "why": "This keeps one chance event per round, visible to all before anyone commits. It creates a shared target to contest rather than a private windfall.",
      "fixes": "Luck of the deal and the coin-flip shots weigh heavily against skill within a hand."
    },
    {
      "what": "All commitments are made in a simultaneous poll each round.",
      "why": "This removes seat order advantage and turns crowding a poster into a guessing and reading game.",
      "fixes": "Sequential turns give a tempo edge to earlier seats."
    },
    {
      "what": "An outlaw escapes, paying nobody, unless at least 4 deputies in total were committed to it over the game.",
      "why": "This keeps the original requirement that a colour must be opened with a set of 3 or more. It rewards backing a poster enough, sometimes by joining one that a rival opened.",
      "fixes": "Card-deck mechanics (draw pile, discard pickup, reshuffles, set validation) and the many distinct sheriff card effects exceed the step and complexity limits."
    },
    {
      "what": "A single game of 6 rounds for 3-4 players, with highest money winning.",
      "why": "The game is short and bounded. With three or more players, a gain on one poster is not simply a rival's loss, so backing a shared poster can pay.",
      "fixes": "A full game spans several hands of unbounded length, too long for the platform."
    }
  ],
  "keeps": [
    "Shared outlaw reward posters starting at $1000 that grow as anyone invests in them.",
    "Bounty growth of (N-1) x $1000 for committing N at once, rewarding big plays.",
    "End-of-game split of each poster in proportion to capture points.",
    "A colour must be backed enough (opened) before it pays.",
    "Hidden information about which outlaws each rival is building toward.",
    "Money as the measure of victory."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The shared-poster, proportional-split tension is a strong strategic core. It survives as a simultaneous allocation game with a hidden informant and fits the limits."
  },
  "variation": {
    "name": "Wanted: Dead or Alive",
    "summary": "Bounty hunters secretly commit deputies to five outlaws over six rounds. Each commitment grows the outlaw's shared poster, and posters are split by capture points at the end. Everyone has one secret informant outlaw worth double, so players must read who is really chasing whom.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "OUTLAWS: There are five outlaws: Red, Blue, Green, Yellow and Black. Each has a public poster starting at $1000.\n\nSETUP: Each player receives 15 deputies, which must last the whole game, and $0. Each player is secretly assigned one informant outlaw, chosen at random so that no two players share an informant. Only that player knows it. Each player has a hidden capture-point (CP) count for each outlaw, starting at 0. The game lasts 6 rounds.\n\nEACH ROUND:\n1. Sighting: one outlaw is drawn at random from the five and announced as Sighted. Its poster immediately rises by $1000.\n2. Talk: every player writes one short message at the same time. Nobody sees the others' messages before writing. All messages are then shown to everyone. Talk is not binding.\n3. Commitment: at the same time, every player secretly chooses one outlaw and a number of deputies from 0 to 5. The number may not exceed their remaining deputies; if it does, it is reduced to their remaining deputies.\n4. Reveal: all choices (outlaw and number) are announced. CP is not announced.\n5. Resolution, for each player who committed N of 1 or more deputies:\n   (a) The player's remaining deputies fall by N.\n   (b) The outlaw's public deputy total rises by N.\n   (c) The player's hidden CP on that outlaw rises by N, or by 2N if it is their informant outlaw.\n   (d) The outlaw's poster rises by (N-1) x $1000.\n   Several players may commit to the same outlaw in the same round; each is resolved separately.\n\nEND OF GAME (after round 6):\n- An outlaw with a public deputy total below 4 escapes. Its poster pays nobody.\n- Every other poster is paid out. Each player with CP on that outlaw receives the poster value x (their CP on it / all players' CP on it), rounded down to the dollar.\n- Unused deputies are worth nothing.\n- All CP and informants are revealed, and each player's money is the sum of their payouts.",
    "objective": "The player with the most money after the final payout wins. If two or more players tie for the most, the game is a draw.",
    "expected_effect": "Players balance three plans: going big alone on an outlaw for a fully owned poster, spreading across uncontested outlaws, and crashing a rival's poster to take a share of a bounty the rival built. Each plan beats one of the others: crashing beats going all-in, spreading beats crashing, and all-in beats careless spreading. None is safe. Informants are hidden and CP is never shown, so players must infer from commitment patterns and talk whether a rival on Blue holds double points there. A rival who looks like a crasher may in fact own the poster. The Sighted bonus creates a public focal target each round that is visible before commitments, so it rewards reading the crowd rather than luck. Talk passes both tests. Players disagree about which posters each should back: everyone wants rivals to grow posters they themselves can share, and to stay off their own informant. A player who follows a proposal like 'let's both open Green' can end up a minority shareholder if Green is the proposer's informant, feeding the proposer's double share. Bluffing about your informant and testing others' claims against their revealed commitments is the core use of talk. Because unused deputies are worthless, the last round is a contested, simultaneous dump rather than safe play."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 6
  }
}
```
````
