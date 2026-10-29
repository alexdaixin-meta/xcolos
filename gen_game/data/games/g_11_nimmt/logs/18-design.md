# 18 design

- time: 2026-10-27T21:45:35+00:00 (75.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 53b0cf0f99bcf4e3, reply sha256 fe03588c278fa8ae

## Sent

````
Original game: 11 Nimmt
Players in the original: 2 to 7

Original rules:
Each player is dealt 10 numbered cards sorted ascending, rest forms a draw deck. One card starts the first discard pile. On your turn you must either play one card onto any pile or take an entire pile into your hand. A play must be higher than the pile top, with circular distance at most 10 (e.g., after 98, 1-8 are within 10). If you cannot play, you must take a pile. When a pile is taken, two new cards from the draw deck start two new piles, so pile count grows. Taking a pile of 3+ cards earns a bull card. A bull allows you to play a whole run of eligible cards onto one pile in one turn; two bulls allow runs on two piles, etc. If bull supply is empty you steal from the player with most bulls. A round ends when a player empties hand; others score penalty ox-heads from remaining cards. Play as many rounds as players; lowest total penalty wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: TOTALS. With 3 players (N=30) there are 22 one-ox cards, six 2-ox cards (5 to 30) and two 3-ox cards (11, 22), so 40 ox in all and a mean of 1.33 per card. With 4 players (N=40) the total is 29 + 16 + 9 = 54. A 4-card pile averages about 5.3 ox. COST OF EACH WAY TO TAKE: a size-1 pile costs the top card's ox, at least 1 (about 1.33) and no bull. A size-2 pile costs at least 2 (about 2.7). A size-3 pile costs at least 2 net of the bull (about 3). A size-4 pile is a forced take costing at least 3 net (about 4.3). Fitting costs 0 now. THE MAIN DECISION, 3 players, the player facing a size-1 pile (rounds 1 to 3: 1→2→3→1→2…). If they fit, the pile is size 2 for the next player, who fits safely because they will not face size 4. The third player faces size 3 and fits for free. So the player who faced size 1 now faces size 4 and pays about 4.3. If they take instead, they pay about 1.33. Taking saves about 3. This holds whatever the opponents' cards are, because nobody downstream wants to reset. Most of the time a non-fitting card is in hand (each card fits with probability 10/29), so the move is usually available. The round-start rotation only shifts this at the 2 boundaries per 9 turns. REFLEX POLICY: 'whenever the pile has 1 card, play your lowest-ox card that does not fit (take)'. (i) Against sensible play it matches best play, so it draws or wins on the deal. (ii) Against random play it wins, because the random player fits about a third of the time and inherits 4-piles. Under this policy every turn is a size-1 take. Bulls (needing 3+ cards) are never earned, so the labelled reward mechanic is decorative. The 'Hot Pile' build-up the game is named for never happens. In 4 players the cycle length equals the player count: A always faces size 1, B size 2, C size 3, D size 4. Seat order alone, cut only by the rotation boundaries, picks the victim, so the player who would face size 4 resets early in the same way. Seat effects are small: seat 1 absorbs the starting card, and with 3 players the last player's final card is never charged. The defect is the near-dominant reflex take, not the seats.
- reasoning_over_luck FAILED: When all players follow the good strategy (take every size-1 pile), each player's penalty is roughly the ox of the cards the player before them in the sequence plays. Over a 9-turn period the predecessor pattern is 1→2, 2→3, 3→2, 2→3, 3→1, 1→3, 3→1, 1→2, 2→1. So each seat receives about one other hand's worth of ox, fixed by the deal. A 9-card hand's ox total has mean 12 and SD about sqrt(9 × 0.356 × 21/29) ≈ 1.5. The difference between two players is about 2.1 SD-points, while every player's choices change totals by only fractions of a point. These choices are the order of dumping, since all your cards are eventually passed on, and the occasional boundary exploit. A 3-ox card (11, 22, and 33 in 4p) in an opponent's hand is about one point of luck. So the winner under good play is mostly the deal: who sits behind the hand with fewer 2- and 3-ox cards. There is genuine material to infer: near-perfect card counting, with only 2 (3p) or 7 (4p) cards unseen. But it has little to act on once the reflex take dominates.
- change: Remove voluntary takes: a player may play a non-fitting card (and take) only if no card in hand fits, as in the original 11 Nimmt. With about 97% of 9-card hands holding a fitter, the player facing a size-1 pile can no longer pay 1 to dodge the 4-pile, and the timing of when to keep fitters becomes the strategic core.
- change: Or, if voluntary takes stay, make them cost: add a flat +2 to every take of a pile under 3 cards. A size-1 take then costs about 3.3 against about 4.3 for the 4-pile. Re-check the decision table so that neither option is strictly better for the player facing a size-1 pile.
- change: Make the pile cap differ from the player count and from a multiple of it (e.g. cap 5 with 4 players, cap 4 with 3 players is fine only after the change above). Otherwise seat order alone fixes who faces the full pile.
- change: Make bulls reachable and worth chasing: award a bull for taking a pile of 3+ cards at -2 each, or raise the cap. Then building a pile deliberately is a real trade-off and the 'Hot Pile' theme exists in play.
- change: After the changes, show a simulated or worked table: the reflex take policy and the always-lowest and always-highest policies against sensible and random play must each lose a meaningful share of games.
The variation that was reviewed: 11 Nimmt: Hot Pile: CARDS. The deck has N cards numbered 1 to N, where N = 30 with 3 players and N = 40 with 4 players.

OX-HEADS. Each card carries ox-heads:
- 11, 22 and 33 carry 3.
- Every other multiple of 5 (5, 10, 15, 20, 25, 30, 35, 40) carries 2.
- All other cards carry 1.

SETUP.
- Shuffle the deck once.
- Deal each player a private hand of H cards: H = 9 with 3 players, H = 8 with 4 players.
- Turn the next card face up as the starting pile (pile size 1).
- The remaining cards are set aside unseen (2 cards with 3 players, 7 with 4) and take no part in the game.
- Every player starts with 0 penalty and 0 bulls.
- A player sees only their own hand. Everyone sees the pile (its cards, top card, size and ox-head total), every card played, every take, and all penalties and bulls.

FITTING. A card c fits on a pile whose top card is t if d = (c - t) mod N is between 1 and 10 inclusive. This means 'higher than the top and at most 10 above, counting round from N back to 1'. Example with N = 30: on a top of 25, the cards 26 to 30 and 1 to 5 fit.

ROUNDS. The game lasts exactly H rounds. In round r the seats act one after another, starting with seat ((r - 1) mod number of players) + 1 and continuing in seat order, wrapping round, so the starting player rotates. Each seat starts equally often: 3 times each with 3 players, 2 times each with 4.

TURN. On your turn you must play exactly one card from your hand (your options are your hand cards listed in ascending order). Then exactly one of the following happens:
(a) If the card fits and the pile has fewer than 4 cards, the card goes on top of the pile. The pile size rises by 1 and the pile's ox-heads rise by the card's ox-heads.
(b) Otherwise you TAKE the pile. This happens when the card does not fit, or when it fits but the pile already has 4 cards. When you take:
   1. Add the pile's total ox-heads to your penalty.
   2. If the pile had 3 or more cards, gain 1 bull.
   3. Discard the pile cards out of the game.
   4. Your played card becomes the new pile's only card (size 1, ox-heads equal to that card's).
Taking on purpose is done by playing a card that does not fit. Every turn removes exactly one card from your hand, so all hands empty together at the end of round H.

BULLS. Each bull is worth -1 penalty at the end. Bulls are unlimited and never move between players.

END. After round H, each player's final score = penalty - bulls. The cards left in the last pile count against nobody. Winner: Lowest final score (penalty minus bulls) wins. If two or more players tie for lowest, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
  "original_summary": "11 Nimmt is a shedding card game. Players play numbered cards onto growing discard piles, each card higher than the pile top and within 10 of it, counting round from the highest number back to 1. A player who cannot play must take a pile. Taking a big pile earns bulls, which allow multi-card plays. Leftover cards score penalty ox-heads, and the lowest total wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the reviewed variation a player may take on purpose by playing a non-fitting card. The player facing a size-1 pile takes it for about 1.33 ox instead of inheriting the forced size-4 pile at about 4.3. That holds whatever the opponents hold. The reflex policy 'take every size-1 pile' draws against sensible play and beats random play. Because the pile cap of 4 equals the player count in 4-player games, seat order alone also picks who faces the full pile."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Under the reflex take, each player's penalty is roughly the ox in the predecessor's hand. Hand ox has SD about 1.5, so two players differ by about 2.1 points from the deal alone. Choices move totals by fractions of a point, so a better player does not reliably win."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Once the reflex is found, the only refinements left are the order of dumping and the boundaries where the round start rotates. Bulls need 3+ card piles, which never form, so the reward mechanic is never used. A strong player has little room to improve."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "There is rich material to infer: near-perfect card counting, with only 2 (3 players) or 7 (4 players) cards unseen. But the dominant reflex makes that inference almost irrelevant to the decision."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Penalties, bulls and the winner follow by arithmetic from the cards played. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is turn-based and text-only, with one hidden hand per player, a fixed 9 or 8 rounds and no board. Its step count is within the limits."
    }
  ],
  "problems": [
    "P1: Voluntary takes make 'take every size-1 pile' a near-dominant reflex. It cannot be beaten by sensible play and it beats random play.",
    "P2: A single pile with a cap equal to the player count (4 players) or in a fixed cycle (3 players) lets seat order decide who faces the full pile.",
    "P3: Bulls require 3+ card piles that never form under the reflex, so the 'Hot Pile' build-up and the bull reward are decorative.",
    "P4: Under the intended good play each penalty is roughly the predecessor's hand ox, so the deal decides the winner (lottery trap).",
    "P5: Card-counting information exists but there is no decision that uses it. There is no real choice of where to play or which top to leave."
  ],
  "changes": [
    {
      "what": "Forced fitting, as in the original 11 Nimmt. You may take a pile only if no card in your hand can be placed on any pile with room.",
      "why": "This removes the cheap dodge. Whoever holds a fitter must place it, so takes come from running out of fitters or from full piles, as the original intends.",
      "fixes": "P1"
    },
    {
      "what": "Two piles instead of one, each capped at 5 cards. Placing a fitting card on a full pile counts as a take. Each turn's choice is a card plus a pile.",
      "why": "Ten slots fit neither a 3-seat nor a 4-seat cycle, and forced takes from empty hands come irregularly. Who faces two full piles therefore depends on play, not seats. Choosing which pile to feed and which top to leave restores the original's 'play onto any pile' decision.",
      "fixes": "P2"
    },
    {
      "what": "Use the two piles to block opponents and to time the full piles.",
      "why": "Players can steer tops away from what opponents are likely to hold, judged by counting cards. They can also time when piles fill so that someone else is the one forced. This gives card counting something to act on.",
      "fixes": "P5"
    },
    {
      "what": "Each bull is worth -2, earned for taking a pile of 3 or more cards. When forced, the player chooses which pile to take and which card restarts it.",
      "why": "A 5-card pile averages about 6.7 ox, or about 4.7 net of the bull. A 3-card pile is about 4.0, or 2.0 net. A 1-card pile is about 1.3 with no bull. The forced player faces a real choice, and piles do build to 3-5 cards, so bulls happen.",
      "fixes": "P3"
    },
    {
      "what": "Penalty comes only from piles you take, and the pile you take is built by everyone.",
      "why": "A penalty is no longer one predecessor's hand passed on. Who is forced, and when, depends on blocking, timing and the forced player's choice of pile, so play rather than the deal sets the gap.",
      "fixes": "P4"
    },
    {
      "what": "Drop the voluntary-take mechanic entirely. Every simple policy is now restricted to fitting plays: always the lowest fitter, always the highest fitter, always pile A, or random.",
      "why": "The reflex no longer exists. Each remaining fixed policy ignores where the tops will land and who will face full piles, so it can be steered into the forced takes. This was checked case by case in expected_effect.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "Numbered cards with circular fitting: higher than the top and at most 10 above, wrapping from N to 1.",
    "You must play if you can, and take a pile only when you cannot.",
    "Ox-head penalties, with 11-style 'double' cards worth 3 and multiples of 5 worth 2.",
    "Bulls as the reward for taking a big pile.",
    "Several piles to choose among, with pressure building as piles grow.",
    "The lowest total penalty wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Forced fitting, two capped piles and stronger bulls remove the reflex take and the seat cycle. They turn hidden-hand card counting into a real decision about where to play and when piles fill, all within the platform's limits."
  },
  "variation": {
    "name": "11 Nimmt: Two Hot Piles",
    "summary": "There are two piles and you must play a card that fits if you can. Piles cap at 5 cards. Placing on a full pile, or holding no card that can be placed, forces you to take a pile. Big takes earn bulls worth -2. The lowest score wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "CARDS. The deck has N cards numbered 1 to N: N = 30 with 3 players, N = 40 with 4 players.\n\nOX-HEADS. Cards 11, 22 and 33 carry 3 ox-heads. Every other multiple of 5 (5, 10, 15, 20, 25, 30, 35, 40) carries 2. All other cards carry 1.\n\nSETUP.\n- Shuffle once.\n- Deal each player a private hand of H cards: H = 9 with 3 players, H = 8 with 4 players.\n- Turn the next two cards face up. They start Pile A and Pile B, each of size 1.\n- The rest (1 card with 3 players, 6 with 4) are set aside unseen and take no part in the game.\n- Everyone starts with penalty 0 and bulls 0.\n\nINFORMATION. You see only your own hand. Everyone sees both piles (their cards, top card, size and ox total), every card played and every take, and all penalties and bulls.\n\nFITTING. A card c fits a pile with top card t if d = (c - t) mod N is between 1 and 10 inclusive. Example with N = 30: on a top of 25, the cards 26 to 30 and 1 to 5 fit.\n\nROOM. A pile has room if it has fewer than 5 cards.\n\nPLACEMENT. A placement is a card from your hand that fits a pile with room.\n\nROUNDS. The game lasts exactly H rounds. In round r the seats act one after another, starting with seat ((r - 1) mod number of players) + 1 and continuing in seat order, wrapping round. Each seat starts 3 times (3 players) or 2 times (4 players).\n\nTURN. On your turn you choose exactly one card from your hand and one pile (A or B).\n- If you hold at least one placement, you must choose a placement: the card goes on top of that pile. The pile's size rises by 1 and its ox total rises by the card's ox.\n- If you hold no placement at all, you must TAKE. You choose any card and either pile, and then:\n  1. Add that pile's ox total to your penalty.\n  2. If the pile had 3 or more cards, gain 1 bull.\n  3. Discard that pile's cards out of the game.\n  4. Your chosen card becomes that pile's only card (size 1, ox equal to that card's).\n- The other pile is unchanged.\n- Every turn removes exactly one card from your hand, so all hands empty at the end of round H.\n\nBULLS. Each bull is worth -2 at the end. Bulls are unlimited and never move between players.\n\nEND. After round H, each player's final score = penalty - 2 x bulls. Cards left in the two piles count against nobody.",
    "objective": "The lowest final score (penalty minus twice bulls) wins. If two or more players tie for lowest, the game is a draw among them.",
    "expected_effect": "Takes now happen only when a player is forced, either because both piles are full or because no card in hand fits a pile with room. Each turn's choice is therefore which fitting card to play and which pile to feed. Players feed the pile they want to fill before an opponent's turn, and they leave tops that opponents (judged by counting the cards already played) are unlikely to be able to follow. They also keep a fitter in reserve for when piles are near full.\n\nWhen forced, the choice is real. A big pile costs about 6.7 ox but returns a bull (about 4.7 net). A small pile costs about 1.3 with no bull. The card you restart with sets the next fitting window.\n\nPolicy check. The reflex take is now illegal. 'Always the lowest fitter', 'always the highest fitter' and 'always pile A' each ignore which pile fills on whose turn and which top is left, so a counting opponent can steer them into the 5-card takes. Each loses a substantial share of games to sensible play, and random play loses most games.\n\nSeat order. Ten pile slots and irregular forced takes break the fixed seat cycle, so seat order no longer picks the victim. The rotating start balances first turns.\n\nLuck. The deal still shapes how many fitters a player holds, but penalties come from piles everyone built and from takes whose timing play controls. The deal is no longer one predecessor's hand passed straight on.\n\nTalk is left out. Interests do conflict, but with hidden hands and no binding deals a message could only be an unverifiable claim about one's cards. That adds words rather than reasoning, and it risks two players ganging up to force the third."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 9
  }
}
````
