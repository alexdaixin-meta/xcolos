# 01 design

- time: 2026-10-28T06:07:50+00:00 (81.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 bed217c0f9b7407a, reply sha256 6e877f621159fe08

## Sent

````
Original game: Turn The Tide
Players in the original: 3 to 5

Original rules:
Players receive 12 unique Weather cards numbered 1-60. Each Weather card may show 0, 0.5 or 1 life preserver icon; players take that many tokens, rounding down. Shuffle 24 Tide Level cards face down. A game has as many rounds as players. A round has 12 hands: reveal two Tide cards. All remaining players simultaneously play one Weather card face up. The highest Weather takes the lower Tide card and places it face up on its own pile covering previous tide. The second highest takes the other Tide card. Then the player(s) showing the highest Tide Level among all players must flip one life preserver face down. A player whose last preserver is flipped gets one extra life; eliminated on next loss. Round ends after 12 hands or when only two players remain. Score: 1 per face-up preserver, -1 if eliminated, plus 1 bonus for lowest Tide showing. Hands and deck pass left each round.
````

## Reply

````
```json
{
  "original_summary": "Turn The Tide is a 3-5 player card game. Each hand, everyone plays a numbered Weather card at the same time. The highest card takes the lower of two revealed Tide cards and the second highest takes the higher one, and whoever shows the highest Tide loses a life preserver. Hands pass left each round so every player plays every hand once.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Players start with no Tide card, so a player who keeps playing the lowest card and never takes a Tide sits at level 0, cannot be highest, and earns the lowest-tide bonus. Only the card distribution stops this. Seats are balanced, because every player plays every hand once."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Skill decides the game: timing high and low cards, counting cards already played, and predicting which card each rival will commit. Passing the hands cancels most of the luck of the deal."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "The game is not solved. Mixed-strategy guessing every hand, and planning which cards to save for later hands, reward depth. A weak player still keeps some preservers."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "In the first round the other hands are hidden. In every round the choice is simultaneous, so a player must predict rivals' cards and weigh their own Tide level against the two revealed Tide cards."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every outcome is a comparison of numbers plus a count of tokens."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game has 36-60 hands, more than the 40-round limit. Each hand reveals two Tide cards. The preserver count depends on icons printed on each card. Ending a round early when only two players remain needs block skipping, which the engine lacks."
    }
  ],
  "problems": [
    "Too long: players x 12 hands is 36-60 rounds, over the 40-round limit.",
    "Starting at Tide level 0 makes ducking (never taking a Tide) close to a free safe strategy.",
    "Preserver icons printed per card add attributes and bookkeeping without adding strategy.",
    "Revealing two separate random Tide cards every hand, plus a reshuffle, exceeds one random draw per round.",
    "Ending a round early on elimination needs conditional blocks of steps, which the engine cannot do."
  ],
  "changes": [
    {
      "what": "Each deal is 10 hands, and there are as many deals as players (30 rounds with 3 players, 40 with 4). The Weather deck is cut to 1 to 12 x players.",
      "why": "This keeps the hand-passing fairness while staying within 40 rounds.",
      "fixes": "Too long: players x 12 hands is 36-60 rounds, over the 40-round limit."
    },
    {
      "what": "Every player's Tide level starts each deal at 11, the middle of the 1-20 Tide deck.",
      "why": "Staying out of the scramble no longer guarantees safety, because a low Tide must be won.",
      "fixes": "Starting at Tide level 0 makes ducking (never taking a Tide) close to a free safe strategy."
    },
    {
      "what": "Every player gets exactly 4 lifelines per deal.",
      "why": "This removes the per-card icons. Hand quality is still balanced by passing hands.",
      "fixes": "Preserver icons printed per card add attributes and bookkeeping without adding strategy."
    },
    {
      "what": "The Tide deck (1-20) is shuffled once at the start of each deal, and each hand reveals the next two cards from that ordered deck.",
      "why": "This gives at most one random draw per round.",
      "fixes": "Revealing two separate random Tide cards every hand, plus a reshuffle, exceeds one random draw per round."
    },
    {
      "what": "A player who must lose a lifeline at 0 is Sunk. A Sunk player scores -1 for the deal, cannot lose more, and keeps playing cards. The deal never ends early.",
      "why": "This keeps the cost of over-exposure without needing to skip steps.",
      "fixes": "Ending a round early on elimination needs conditional blocks of steps, which the engine cannot do."
    }
  ],
  "keeps": [
    "Simultaneous play of uniquely numbered Weather cards.",
    "Highest card takes the lower Tide, second highest takes the higher Tide, and the rest take nothing.",
    "A newly taken Tide replaces the old level.",
    "The highest Tide level loses a lifeline, with ties all losing.",
    "Hands pass left between deals, so everyone plays every hand.",
    "Deal scoring is remaining lifelines, -1 if sunk, and +1 for the lowest Tide."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core is a strong simultaneous-guessing and hand-management game. It only needs to be shortened and simplified to fit the limits."
  },
  "variation": {
    "name": "Turn The Tide: Short Seas",
    "summary": "This is a 3-4 player Turn The Tide. Players play numbered Weather cards at the same time to grab or dodge Tide cards. The highest Tide level loses a lifeline, and hands pass between deals so every player plays every hand once.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "SETUP: Let P be the number of players (3 or 4). The Weather deck is the cards 1 to 12xP (1-36 for 3 players, 1-48 for 4), each number once. Shuffle it and deal 10 cards face down to each player as that player's hand. The leftover 2xP cards are set aside unseen for the whole game. Each player knows only their own hand. Each player has a game score of 0. The game has P deals of 10 hands each, so there are 10xP rounds in total, and one round is one hand.\n\nSTART OF EACH DEAL (rounds 1, 11, 21, 31):\n- Shuffle a Tide deck of the cards 1 to 20.\n- Set every player's Tide level to 11.\n- Give every player 4 lifelines.\n- Clear every player's Sunk status.\n- From the second deal on, each player passes their entire current hand of 10 cards to the player on their left before the deal begins. Each player plays each original hand exactly once over the game.\n\nEACH HAND:\n1. Reveal the next two cards of the Tide deck to everyone. Call the smaller one Low Tide and the larger one High Tide.\n2. Every player secretly chooses one Weather card from their hand. All choices are revealed at the same time and those cards are discarded face up.\n3. The player with the highest Weather card sets their Tide level to Low Tide. The player with the second highest Weather card sets their Tide level to High Tide. All other players keep their current Tide level. Weather numbers are unique, so there are no ties.\n4. Find the highest Tide level among all players. Every player at that level loses 1 lifeline, except Sunk players, who lose nothing. A player who would lose a lifeline while at 0 lifelines becomes Sunk instead.\n5. Announce all Weather cards played, all Tide levels, all lifelines and all Sunk statuses.\n\nEND OF EACH DEAL (after rounds 10, 20, 30, 40):\n- Each player who is not Sunk adds their remaining lifelines to their game score.\n- Each Sunk player subtracts 1 from their game score.\n- Among players who are not Sunk, the player or players with the lowest Tide level each add 1.\n\nThere is no talk phase.",
    "objective": "After the last deal (10xP hands), the player with the highest game score wins. If two or more players tie for highest, the game is a draw.",
    "expected_effect": "Starting at level 11 forces players to fight for low Tides rather than hide. Every hand becomes a simultaneous guessing contest. A player can spend a high card for the Low Tide, or play mid and risk being stuck with the High Tide, or play low and keep their current level. Each player must read what rivals will commit given their exposure and their remaining cards. In deal 1 the other hands are hidden. In later deals, the cards played in earlier deals reveal who held which hand, so the inference moves from what rivals hold to when they will spend it. Passing hands and identical lifelines remove deal luck. The Tide deck order is shared and symmetric. Simple policies lose: always-highest wastes its strong cards and later gets stuck high, always-lowest strands itself at 11 or above while others undercut it, and random play loses to card counting. Talk is left out because promises about which card one will play are unverifiable and costless, the played card is already the only real signal, and talk would add steps without adding a decision."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 10,
    "choice_steps_per_round": 1,
    "attributes": 11,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
