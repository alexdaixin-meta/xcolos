# 01 design

- time: 2026-10-28T01:31:46+00:00 (108.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 2e554ce7e7b66f66, reply sha256 c405a11a9406fee9

## Sent

````
Original game: Growl
Players in the original: 4 to 10

Original rules:
Setup a shared face-up deck containing Night cards seeded at 1/3, 2/3 and bottom of deck, plus Bite, Wound, Charm, Salve and Gold cards. Deal each player one starter Bite or Gold to secretly set Wolf Zeros; then deal 3 cards for a 4-card hand, redrawing if 3 wounds. On your turn draw the top deck card aloud: if it is a Night card resolve its effect then start Night Phase, otherwise you must give it to another living player who adds it to hand. Players die instantly when wounds minus salves reach 3, and humans secretly become werewolves when bites minus charms reach 3. During Night Phase no talking is allowed and each living player must pass one chosen card left and one right face-down, but humans may not pass Bites. After receiving, check death/turn. Game ends after Final Night is resolved or only two alive remain; if at least one human lives humans win, otherwise wolves win.
````

## Reply

````
```json
{
  "original_summary": "Growl is a hidden-role social deduction card game for 4 to 10 players. Cards are handed out face-up by day and passed face-down to neighbours by night. Humans secretly turn into werewolves when bites outnumber charms in their hand by 3, and players die when wounds outnumber salves by 3. Humans win if any human survives the Final Night.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Choices matter: who you give a day card to, and what you pass at night. But the winner rule is lopsided. Wolves win only if every human is converted or dead, so humans can win by hoarding charms and having one survivor. Wolves' only hope is snowballing. Seat order also matters, because night passing goes only to left and right neighbours, so where the starting wolves sit shapes the game."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading who is a wolf from day gifts and night receipts is a real skill. However, the secret starter deal, the 3-card opening hands and the deck order decide a lot. A player dealt bites early is near conversion before making a single decision."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players can still contribute by passing charms. Strong players track every public gift, infer hand contents, bluff as wolves and choose whom to protect, so there is a lot of room to improve."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Roles, hands and night passes are hidden. A player must infer who is a wolf from what they received, from public gifts and from talk. Every human must also judge who deserves their protective charm."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Death, infection and the team outcome all follow from card counts. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The original relies on several things the engine cannot build within its limits:\n- a seeded physical deck with Night cards at fixed depths;\n- multi-card hands with many card types, including Gold, which does nothing for the win;\n- left and right adjacency passing;\n- open real-time talk with a silence rule;\n- a variable game length.\nThat is too much hidden state and too many card types for the platform."
    }
  ],
  "problems": [
    "P1: Many full hidden hands of five or six card types exceed the platform's hidden-state and attribute limits.",
    "P2: The seeded deck with Night cards at fixed positions, plus redraw rules, needs more than one random draw per round and a variable game length.",
    "P3: Left and right neighbour passing is an adjacency mechanic and gives seat position a built-in effect.",
    "P4: The winner rule (humans win if a single human survives) heavily favours humans and makes wolf play nearly hopeless unless the infection snowballs.",
    "P5: Opening deals of random bites and starters let luck decide who converts before any reasoning happens.",
    "P6: Open, unstructured talk cannot be run by the engine, and day talk lets the first speaker steer everyone.",
    "P7: Gold cards and multiple Night card effects add rules without adding decisions."
  ],
  "changes": [
    {
      "what": "Replace hands with four counters per player: Bites and Charms (private), Wounds and Salves (public). Only these four card types exist; Gold and Night cards are removed.",
      "why": "This keeps the bites-minus-charms and wounds-minus-salves arithmetic that defines Growl, using a handful of numbers.",
      "fixes": "P1"
    },
    {
      "what": "Removed Gold and Night card effects; every round has one day and one night.",
      "why": "Gold and the Night effects add rules but no decisions.",
      "fixes": "P7"
    },
    {
      "what": "Each round makes one random day draw from fixed odds (Bite 35%, Wound 25%, Salve 25%, Charm 15%). The game always runs one day and one night per round, for 12 rounds.",
      "why": "This gives exactly one chance event per round and a fixed length, with no deck to seed.",
      "fixes": "P2"
    },
    {
      "what": "At night each player passes to ANY other living player of their choice, and the recipient is not told who sent it.",
      "why": "This removes adjacency and seat advantage, and turns night receipts into a deduction puzzle.",
      "fixes": "P3"
    },
    {
      "what": "New winner rule. At the end, wolves win if living wolves are at least as many as living humans; otherwise humans win. Wolves also win at once if every living player is a wolf.",
      "why": "Wolves now need about two conversions or kills rather than all of them, which balances the teams. A human death or a wrongly charmed wolf now matters.",
      "fixes": "P4"
    },
    {
      "what": "Death threshold lowered to Wounds minus Salves of 2, and a dead player's role is revealed.",
      "why": "Day wounds become a real voting weapon, and each death gives public evidence. This partly offsets the tilt toward humans.",
      "fixes": "P4"
    },
    {
      "what": "Fixed, equal starting counters. Every human starts with 1 Bite and 1 Charm; the wolf starts with 3 Bites and 0 Charms. The wolf is chosen by one random draw at setup.",
      "why": "No human starts closer to infection than another, so luck only decides who the wolf is.",
      "fixes": "P5"
    },
    {
      "what": "Each day there is one simultaneous message round before the day card is given. Night stays silent.",
      "why": "Talk becomes structured and engine-runnable, and no one can simply echo the first speaker. The original's silent night is kept.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Hidden werewolves among humans, with infection when bites minus charms reaches 3",
    "Secret conversion: the infected player is told privately and switches sides",
    "Death when wounds outweigh salves",
    "Public day gifts of a drawn card to another player",
    "Secret night passing in which humans may never pass a Bite",
    "No talking at night",
    "Bites passed into humans are stuck there, because humans cannot pass them on, so wolves offload infection while humans circulate charms",
    "Early end when only two players remain"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of hidden infection by card passing reduces cleanly to four counters, one draw and two night choices. It keeps strong hidden-role inference and fits the limits once the deck, adjacency and winner rule are fixed."
  },
  "variation": {
    "name": "Growl: Moonlit Passing",
    "summary": "A team hidden-role game. Each day a drawn card is given publicly; each night every player secretly passes a Bite or a Charm to anyone. Humans turn into wolves when bites outnumber charms by 3, and wolves win if they match the humans in number by the end.",
    "players": {
      "min": 5,
      "max": 7,
      "suggested": 5
    },
    "rules": "SETUP\n- Players sit in a fixed order, numbered 1 to N.\n- Wolves are chosen at random and told privately: 1 wolf with 5 or 6 players, 2 wolves with 7 players. Wolves are NOT told who the other wolves are. Everyone else is a human.\n- Each player has four counters:\n  - Bites (private, known only to the owner)\n  - Charms (private)\n  - Wounds (public)\n  - Salves (public)\n- Humans start with Bites 1, Charms 1, Wounds 0, Salves 0.\n- Wolves start with Bites 3, Charms 0, Wounds 0, Salves 0.\n\nThe game lasts at most 12 rounds. Each round has a Day and a Night.\n\nDAY\n1. Active player. Living players take turns in seat order, skipping dead players. Round 1 starts with player 1.\n2. Draw. The engine draws one day card at random and announces it to all:\n   - Bite 35%\n   - Wound 25%\n   - Salve 25%\n   - Charm 15%\n3. Talk. Every living player writes one short message at the same moment, without seeing the others. Then all messages are shown to everyone.\n4. Give. The active player must give the card to another living player (not themselves). Everyone sees who receives it. The recipient adds 1 to the matching counter. A Bite or Charm received this way is publicly known to have been added, but the recipient's total stays private.\n5. Death check. A player whose Wounds minus Salves is 2 or more dies at once. A dead player's role is revealed, and dead players take no further part.\n\nNIGHT (no messages may be written)\n6. Each living player secretly chooses a target: one other living player.\n7. Each living player secretly chooses a token: Bite or Charm. Legality:\n   - A Bite passes only if the sender is a wolf and holds at least 1 Bite.\n   - A Charm passes only if the sender holds at least 1 Charm.\n   - Humans may never pass Bites. If a human picks Bite, their choice is treated as Charm.\n   - If the chosen token is not legal, the sender passes the other token if that is legal for them. Otherwise nothing passes.\n8. Resolve. All passes happen at the same moment. Each sender loses 1 of the passed token, and each target gains 1.\n9. Report. Each player is told privately how many Bites and how many Charms they received tonight, but never who sent them.\n10. Infection. Any living human whose Bites minus Charms is 3 or more becomes a wolf. They are told privately. Their counters stay as they are, and from now on they may pass Bites. Wolves never change back and cannot be infected further.\n\nEND CHECKS (after every Night)\n11. If every living player is a wolf, the wolves win at once.\n12. If two or fewer players are alive, the game ends now and is scored as below.\n13. Otherwise the game ends after the Night of round 12 and is scored as below.\n\nSCORING\nCount living wolves and living humans. If living wolves are at least as many as living humans, the wolf team wins. Otherwise the human team wins. Team membership is a player's role at the moment the game ends, so converted humans win with the wolves.",
    "objective": "Team win, decided by counting roles at the end:\n- Wolf team wins if, when the game ends, living wolves are at least as many as living humans, or if all living players are wolves.\n- Human team wins otherwise.\n- Each player wins or loses with the team of their role at game end. There are no draws.",
    "expected_effect": "Humans must keep charms circulating among humans, but every charm passed to a hidden wolf is lost to their side. So the central decision each night is a trust judgement: who is truly human? Wolves have bites to offload, and they can pass charms to look human while hoarding the charms they are given. Night receipts are anonymous, so a human who was bitten knows only that some wolf targeted them.\n\nDay gifts of Wounds and Salves act as a public vote to kill or save. Because the dead are revealed, a wrongful kill gives the wolves a number advantage and hands information to everyone.\n\nTalk passes both tests because the teams want opposite outcomes, and converted players switch sides silently. A wolf may propose 'give the wound to player 3' or claim to have been bitten in order to draw charms. A human who simply follows the most confident speaker can wound a fellow human or charm a wolf, and so lose the game. The balance target is that the snowball of conversions roughly matches the humans' ability to deduce, so neither team wins by default."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
