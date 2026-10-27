# 21 design

- time: 2026-10-27T18:37:54+00:00 (77.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 1a7457bdb3405183, reply sha256 e652471ab9503414

## Sent

````
Original game: Modern Art
Players in the original: 3 to 5

Original rules:
Each player gets a hand of painting cards (five artists, each card shows an auction type) and hidden money. In turn order players auction one card from hand: open ascending bids, fixed price named by auctioneer and first to accept buys, once-around where each player bids once must raise, sealed simultaneous bids, or double auction of two same-artist cards using second card's type. Buyer pays auctioneer, or bank if auctioneer wins; if no bids in open, auctioneer gets it free, in fixed must buy. Cards played stay on table. Round ends when a fifth card of any artist is played (that card is discarded). Then artists are ranked by number of cards played that round; top three earn value markers on board. All owned paintings of those artists pay owners equal to total value in artist's column. Used paintings are discarded. After four such rounds player with most money wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rebalance so that refusing to bid is not a safe win. Options:
(1) Raise painting values relative to starting money, e.g. 100/70/40 with less starting money, so buying at a fair price is clearly profitable.
(2) Make hoarding cash cost something, e.g. money counts at half value at game end, or the player with the fewest paintings loses a penalty.
(3) Make it harder for an auctioneer to profit when everyone else passes, e.g. an unsold painting goes to the auctioneer only if they paid a reserve to the bank.
(4) Pay part of each winning bid to the bank rather than to the auctioneer, so passivity is not subsidised.
Keep the rules arithmetic and simultaneous. Then re-check that neither always-min nor always-max bidding beats random seats by a wide margin.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the first option as seat 2 wins 88% of decided matches against random seats
- against random seats the results were {'seat 2': 6, 'seat 3': 19, 'seat 1': 15, 'seat 4': 20}
- a thoughtless policy `first@seat1`: won 49, lost 11, drew 0
- a thoughtless policy `first@seat2`: won 53, lost 7, drew 0
- a thoughtless policy `last@seat1`: won 5, lost 55, drew 0
- a thoughtless policy `last@seat2`: won 7, lost 53, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
  "original_summary": "Modern Art is a 3-5 player auction game. Players take turns auctioning painting cards from hidden hands under several auction formats. At the end of each of four seasons, the artists sold most often that season gain value, and owners of those artists' paintings are paid that artist's accumulated value. The richest player wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the previous variation, always taking the first option (bid minimum, effectively never buy) won 49/60 from seat 1 and 53/60 from seat 2. Hoarding cash and collecting auctioneer income beat random buyers. Always-max lost heavily (5/60, 7/60), so the game was lopsided toward passivity rather than balanced. Seat results against random seats were uneven (seat 2: 6 wins, seat 4: 20)."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The original rewards price judgement and market manipulation. However, when doing nothing wins, a careful bidder is beaten by a non-bidder, so skill is not what decides matches."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Valuing paintings depends on predicting which artists will top the season and on reading the other bidders. A weak player can still buy cheaply and score, and the skill ceiling is high."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and money are hidden. Artist values depend on what others will choose to auction, and bids require modelling rivals' valuations. This is real inference, provided passivity is not dominant."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Rankings, payouts and final money are all counts and sums."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Five auction formats, a variable season length triggered by a fifth card, and four seasons are too many branching step blocks for a flat step list. One sealed-bid format with fixed season lengths fits the platform."
    }
  ],
  "problems": [
    "P1: Never buying is a winning policy. Cash keeps full value and auctioneer income accrues without risk, so always bidding the minimum beats random players about 85% of the time.",
    "P2: Auctioneers are subsidised by others' passivity and by receiving the full winning bid, which inflates the hoarder's income.",
    "P3: Buying at a fair price was not clearly profitable relative to starting money, so paintings were not worth contesting.",
    "P4: Seat outcomes were uneven (seat 2 far weaker under random play), suggesting order or tie-break effects.",
    "P5: Multiple auction formats and a card-triggered season end need conditional blocks of steps the engine cannot build."
  ],
  "changes": [
    {
      "what": "Collection requirement: a player who bought fewer than 2 paintings during the game cannot win (final score treated as 0).",
      "why": "Always-zero bidding now buys nothing and is disqualified, so it loses to any opponent who ever buys. A player must enter auctions.",
      "fixes": "P1"
    },
    {
      "what": "Only half of each winning bid (rounded down) goes to the auctioneer; the rest goes to the bank. If the top bid is 0, the painting is unsold and discarded, and the auctioneer gets nothing.",
      "why": "Auctioneering becomes a modest income rather than a free stream that rewards sitting out. No one profits merely because others pass.",
      "fixes": "P2"
    },
    {
      "what": "Season payouts are 30/20/10 per painting for the top three artists, accumulating across the two seasons (up to 60), against starting money of 60.",
      "why": "A painting of a leading artist is clearly worth more than a typical bid, so buying well is profitable. Overpaying (always-max bids all cash) still loses badly.",
      "fixes": "P3"
    },
    {
      "what": "The auctioneer rotates, so each player auctions exactly 3 times. Bid ties go to the tied bidder nearest the auctioneer's left, which rotates with the auctioneer.",
      "why": "No seat has a fixed tie-break or ordering edge.",
      "fixes": "P4"
    },
    {
      "what": "Use a single sealed simultaneous bid format, 2 seasons of exactly 6 auctions, and 4 artists.",
      "why": "This gives a flat, buildable step list. Sealed bids are a native original format and suit simultaneous polls.",
      "fixes": "P5"
    },
    {
      "what": "Add one simultaneous message per auction after the painting is announced, before bidding.",
      "why": "Players own different artists and only one can win, so talking up an artist, bluffing about one's hand, or signalling disinterest are real strategic acts. Talk is not binding.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "Hidden hands of artist cards and hidden money",
    "The auctioneer chooses which painting to sell and earns from the sale",
    "Sealed simultaneous bidding, one of the original's auction types",
    "Artist value set by how often the artist appears in a season, with the top three paid 30/20/10",
    "Values accumulate across seasons for artists that stay in the top three",
    "Market manipulation: steering which artists lead by what you put up for auction",
    "Most money wins"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of speculative valuation, hidden hands and market steering survives in a compact sealed-bid form. The passivity exploit is fixed by a collection requirement and a reduced auctioneer cut."
  },
  "variation": {
    "name": "Modern Art: Sealed Seasons",
    "summary": "Four collectors take turns putting paintings from hidden hands up for sealed-bid auction over two seasons of six auctions. The most-auctioned artists of each season gain value, and owners are paid. The richest collector who bought at least 2 paintings wins.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP. Four players sit in seats 1-4.\n- The deck has 24 painting cards: 6 each of four artists, Red, Blue, Green and Yellow.\n- Shuffle the deck and deal each player 4 cards as a hidden hand. The remaining 8 cards are set aside unseen.\n- Each player starts with 60 money, kept hidden from the others.\n- Every artist starts with a cumulative value of 0.\n\nSTRUCTURE. The game has 12 auctions in two seasons. Auctions 1-6 are Season 1 and auctions 7-12 are Season 2.\n- The auctioneer of auction k is seat ((k-1) mod 4)+1, so seats 1, 2, 3, 4, 1, 2, ... in rotation.\n- Each player is auctioneer exactly 3 times and will have 1 unused card left at the end.\n\nEACH AUCTION:\n(1) The auctioneer privately chooses one card from their hand. The card is removed from the hand and its artist is announced to all.\n(2) That artist's season count goes up by 1, whether or not the painting sells.\n(3) Every player writes one short message at the same time, without seeing the others' messages. All messages are then shown to everyone. Messages are not binding.\n(4) Every player, including the auctioneer, submits a sealed bid at the same time. A bid is a whole number from 0 up to the bidder's current money.\n(5) Resolution:\n  - If the highest bid is 0, the painting is unsold and discarded.\n  - Otherwise the highest bidder buys it. Ties go to the tied bidder who comes first clockwise starting from the seat to the auctioneer's left, with the auctioneer last.\n  - The buyer pays the bid.\n  - If the buyer is not the auctioneer, the auctioneer receives half the bid rounded down, and the rest goes to the bank. If the auctioneer buys, the whole bid goes to the bank.\n  - The buyer adds the painting to their collection and their count of paintings bought goes up by 1.\n  - The artist and the winning price are announced. Losing bids stay hidden.\n\nSEASON END (after auction 6 and after auction 12):\n(a) Rank the artists by season count. More is higher. Ties are broken by fixed priority Red > Blue > Green > Yellow. An artist with count 0 cannot rank.\n(b) Add 30 to the cumulative value of the 1st artist, 20 to the 2nd and 10 to the 3rd. The 4th artist gains nothing this season.\n(c) Each player is paid, for every painting they own of an artist that placed in the top three THIS season, that artist's cumulative value. Paintings of artists outside this season's top three pay 0.\n(d) All owned paintings are then discarded, and all season counts reset to 0.\n\nGAME END. After the Season 2 payout the game ends.",
    "objective": "Only players who bought at least 2 paintings during the game are eligible. Among eligible players, the one with the most money wins. If two or more eligible players tie for most money, the game is a draw. If no player is eligible, the game is a draw.",
    "expected_effect": "Never bidding now always fails the eligibility rule, so it loses to any opponent who buys twice. Bidding all your money buys an early painting for far more than it can pay out, then leaves you broke, so it loses too. Good play means estimating which artists will top each season from the paintings already shown, the cards you hold and what rivals' auction choices reveal about their hands. It also means bidding below expected payout and choosing which painting to auction so as to push artists you own. Season 2 rewards foresight, because an artist that stays top three pays up to 60.\n\nTalk earns its place because players disagree about which artists should rise: each owns and holds different artists, and only one player can win. A player who follows a rival's call to 'push Blue' may be inflating a market the rival already owns, or may bid against a bluff. A follower can overpay for a painting the speaker never intended to support, or be left short of the 2 required purchases while the speaker buys cheaply."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 3,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 12
  }
}
````
