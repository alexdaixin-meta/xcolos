# 01 design

- time: 2026-10-28T04:17:08+00:00 (70.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 d878de8ba4350637, reply sha256 692ced419c81608a

## Sent

````
Original game: 5211
Players in the original: 3 to 8

Original rules:
Shuffle 100 cards (20 each in 5 colors, with point values 1-6; 5 per color are Kododos). Remove a number face-down by player count. Deal 5 cards to each player, rest as draw pile. Each round has 3 simultaneous turns: turn 1 each player plays 2 face-down cards, then draws 2; turns 2-3 each play 1 and draw 1. So 4 cards per player are revealed each round. Scoring: first check if total Kododos in play equals players+2. If yes, only players who played Kododos score them. If not, count cards per color. The most-played color scores, but if its total >= players+3 it busts and is discarded and you check the next most-played. If tied for majority, all tied colors are discarded. Scored cards go to a face-down score pile. Discard others. When draw pile empty, play one final round without drawing, discard last card, sum scores. Highest total wins, tie break most scored cards.
````

## Reply

````
{
  "original_summary": "5211 is a 3-8 player simultaneous card game. Each round every player commits 4 cards from a hidden hand over three face-down turns. The most-played colour scores for the players who played it, unless it 'busts' by being played too much or is tied. A special Kododo count can override everything so that only Kododo players score.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. 'Always play your highest cards' piles onto whatever colour you hold most of, and that colour gets tied or busts. Two players following the same simple policy usually tie, which discards the colour. Play is simultaneous, so no seat has an edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading the table and timing bust risks is a real skill. But hands come from a 100-card shuffled deck with refills, and some cards are removed unseen. A player who draws a strong colour concentration or extra Kododos has a large edge that skill only partly offsets."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Deep play exists: steering the majority, predicting busts, holding Kododos for the exact-count round, using what was revealed in earlier turns. A weak player still scores whenever they happen to join the winning colour."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden and turns are simultaneous. Each player has to infer from earlier revealed cards what colours others are likely to play, and whether a colour is near busting."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Scoring is pure counting: the Kododo total, the per-colour counts, the bust threshold and the card values."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-only and simultaneous. However, a 100-card shuffled deck, per-player refill draws every turn, three play turns and a cascading 'next most-played colour' rule exceed the one-random-draw-per-round and step limits. The game also runs long."
    }
  ],
  "problems": [
    "Luck of the deal and of the per-turn refill draws strongly affects who can control a colour or hit the Kododo count. This is a lottery element.",
    "Per-player refill draws every turn need several random draws per round, which the platform limits to one.",
    "Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps.",
    "The game length (a 100-card deck run down) is too long for the platform.",
    "Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent."
  ],
  "changes": [
    {
      "what": "Every player gets an identical fixed 14-card hand: 4 colours each with values 1, 2 and 3, plus 2 Kododos. There is no deck and no refills.",
      "why": "This removes hand luck entirely. Because played cards are public, a player who tracks the plays knows what everyone has left, so the contest is about predicting intent and timing.",
      "fixes": "Luck of the deal and of the per-turn refill draws strongly affects who can control a colour or hit the Kododo count. This is a lottery element."
    },
    {
      "what": "Removed all in-game drawing. The only random event is a setup deal of distinct secret bonus colours.",
      "why": "This fits the limit of at most one random draw per round.",
      "fixes": "Per-player refill draws every turn need several random draws per round, which the platform limits to one."
    },
    {
      "what": "Each round is two simultaneous card plays: one face-down card, a reveal, then a second face-down card, then a reveal. This replaces the original three turns of 2+1+1 cards.",
      "why": "It keeps the 'see part of the table, then commit more' tension in far fewer steps.",
      "fixes": "Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps."
    },
    {
      "what": "Cut to 4 colours. Resolution is a single rule: the non-busted colour with the strictly highest count scores, and if the top is tied nothing scores.",
      "why": "A single arithmetic comparison replaces the cascade. Ties still kill the colour, as in the original.",
      "fixes": "Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps."
    },
    {
      "what": "The game is fixed at 7 rounds, so all 14 cards are played.",
      "why": "This keeps it short. The forced endgame also rewards planning which cards to save.",
      "fixes": "The game length (a 100-card deck run down) is too long for the platform."
    },
    {
      "what": "Each player gets a secret bonus colour, distinct from everyone else's, and earns +1 per scored card of that colour.",
      "why": "It adds a symmetric hidden type. Each type has equal total value, but it changes which colours you want to win. Players must infer each other's bonus colours from their plays and talk.",
      "fixes": "Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent."
    },
    {
      "what": "Added a simultaneous one-message talk phase before the first card each round.",
      "why": "It allows bluffing and temporary alliances to swing a majority. Since only one player can win and players hold different bonus colours, proposals are self-interested and following one blindly can tie or bust a colour.",
      "fixes": "Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent."
    }
  ],
  "keeps": [
    "Simultaneous face-down card plays from a hidden hand",
    "The most-played colour scores only for those who played it",
    "The bust rule: a colour played too much scores nothing",
    "Ties for the majority kill the tied colours",
    "The Kododo override: an exact Kododo count lets only Kododo players score",
    "Partial reveal mid-round, then further commitment",
    "Highest total wins, with most scored cards as the tie-break"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core majority, bust and Kododo guessing game is strong and inference-heavy. Its problems are deal luck and size, and both can be fixed within the limits."
  },
  "variation": {
    "name": "5211: Mirror Hands",
    "summary": "Every player holds the same 14 cards and a secret bonus colour. Over 7 rounds they each commit two cards, one at a time, trying to be in the colour that wins the majority without busting it, or to hit the exact Kododo count.",
    "players": {"min": 3, "max": 4, "suggested": 4},
    "rules": "SETUP. Let n be the number of players (3 or 4). Every player receives an identical hand of 14 cards:\n- the colours Red, Blue, Green and Yellow, each with values 1, 2 and 3 (12 cards);\n- 2 Kododo cards, which have no colour and are worth 3 each.\nHands are private, but because every hand starts identical and all played cards are revealed, anyone can track what each player has left. Each player is then secretly dealt a bonus colour at random from Red, Blue, Green and Yellow, with no two players sharing one. Only that player knows it. Scores start at 0, and each player's scored-card count starts at 0.\n\nEACH ROUND (7 rounds):\n1. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing said is binding.\n2. First card. Every player at the same time places one card from their hand face down.\n3. Reveal. All first cards are revealed.\n4. Second card. Every player at the same time places one more card from their hand face down.\n5. Reveal. All second cards are revealed. Played cards leave the hands.\n6. Count. Count K, the number of Kododos played this round (out of 2n cards). Count how many cards of each colour were played.\n7. Kododo check. If K equals exactly n-1 (2 Kododos with 3 players, 3 with 4 players), each player scores 3 points per Kododo they played this round and adds that many cards to their scored-card count. No colour scores this round.\n8. Colour check (only if K is not exactly n-1). A colour is busted if its count is n+1 or more (4 or more with 3 players, 5 or more with 4 players). Among the colours that are not busted and have a count of at least 1, find the highest count. If exactly one colour has that highest count, it is the scoring colour. If two or more colours share it, or no colour qualifies, nothing scores this round.\n   Each player scores the face values of their cards of the scoring colour, plus 1 extra point per such card if it is their bonus colour, and adds those cards to their scored-card count.\n   Kododos played in a round where the Kododo check fails score nothing.\n9. Announce the round result and the updated scores.\n\nEND. After round 7, all 14 cards have been played and the game ends.",
    "objective": "The player with the highest total score wins. If players are tied on total score, the one among them with the higher scored-card count wins. If they are still tied, the game is a draw among the tied players.",
    "expected_effect": "Removing deal luck makes the result depend on predicting others' plays.\n\nHow the round plays: the mid-round reveal lets players react, either by joining the emerging leader or by deliberately pushing it to bust or tie. Kododo timing becomes a pure reading game, because everyone knows exactly how many Kododos each opponent has left.\n\nWhat players disagree about: hidden bonus colours mean each player wants a different colour to win. Talk is used to propose a colour, recruit allies and bluff. A player who simply follows a proposal can lose in three ways: two others pile on and bust the colour, a rival splits the vote to force a tie, or the proposer benefits from the bonus while the follower gains only face value.\n\nThe endgame: the fixed 14-card hand rewards planning which high cards and Kododos to save for the late, fully deducible rounds."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 7
  }
}
````
