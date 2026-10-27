# Variation: 11 Nimmt: Two Hot Piles

There are two piles and you must play a card that fits if you can. Piles cap at 5 cards. Placing on a full pile, or holding no card that can be placed, forces you to take a pile. Big takes earn bulls worth -2. The lowest score wins.

Players: 3 to 4, best with 3

## Review of the original

11 Nimmt is a shedding card game. Players play numbered cards onto growing discard piles, each card higher than the pile top and within 10 of it, counting round from the highest number back to 1. A player who cannot play must take a pile. Taking a big pile earns bulls, which allow multi-card plays. Leftover cards score penalty ox-heads, and the lowest total wins.

- **non_degenerate**: bad. In the reviewed variation a player may take on purpose by playing a non-fitting card. The player facing a size-1 pile takes it for about 1.33 ox instead of inheriting the forced size-4 pile at about 4.3. That holds whatever the opponents hold. The reflex policy 'take every size-1 pile' draws against sensible play and beats random play. Because the pile cap of 4 equals the player count in 4-player games, seat order alone also picks who faces the full pile.
- **skill_sensitive**: weak. Under the reflex take, each player's penalty is roughly the ox in the predecessor's hand. Hand ox has SD about 1.5, so two players differ by about 2.1 points from the deal alone. Choices move totals by fractions of a point, so a better player does not reliably win.
- **headroom**: weak. Once the reflex is found, the only refinements left are the order of dumping and the boundaries where the round start rotates. Bulls need 3+ card piles, which never form, so the reward mechanic is never used. A strong player has little room to improve.
- **reasoning_dependent**: weak. There is rich material to infer: near-perfect card counting, with only 2 (3 players) or 7 (4 players) cards unseen. But the dominant reflex makes that inference almost irrelevant to the decision.
- **verifiable**: good. Penalties, bulls and the winner follow by arithmetic from the cards played. No judge is needed.
- **fits_platform**: good. It is turn-based and text-only, with one hidden hand per player, a fixed 9 or 8 rounds and no board. Its step count is within the limits.

## Problems

- P1: Voluntary takes make 'take every size-1 pile' a near-dominant reflex. It cannot be beaten by sensible play and it beats random play.
- P2: A single pile with a cap equal to the player count (4 players) or in a fixed cycle (3 players) lets seat order decide who faces the full pile.
- P3: Bulls require 3+ card piles that never form under the reflex, so the 'Hot Pile' build-up and the bull reward are decorative.
- P4: Under the intended good play each penalty is roughly the predecessor's hand ox, so the deal decides the winner (lottery trap).
- P5: Card-counting information exists but there is no decision that uses it. There is no real choice of where to play or which top to leave.

## Changes

- Forced fitting, as in the original 11 Nimmt. You may take a pile only if no card in your hand can be placed on any pile with room. (fixes: P1): This removes the cheap dodge. Whoever holds a fitter must place it, so takes come from running out of fitters or from full piles, as the original intends.
- Two piles instead of one, each capped at 5 cards. Placing a fitting card on a full pile counts as a take. Each turn's choice is a card plus a pile. (fixes: P2): Ten slots fit neither a 3-seat nor a 4-seat cycle, and forced takes from empty hands come irregularly. Who faces two full piles therefore depends on play, not seats. Choosing which pile to feed and which top to leave restores the original's 'play onto any pile' decision.
- Use the two piles to block opponents and to time the full piles. (fixes: P5): Players can steer tops away from what opponents are likely to hold, judged by counting cards. They can also time when piles fill so that someone else is the one forced. This gives card counting something to act on.
- Each bull is worth -2, earned for taking a pile of 3 or more cards. When forced, the player chooses which pile to take and which card restarts it. (fixes: P3): A 5-card pile averages about 6.7 ox, or about 4.7 net of the bull. A 3-card pile is about 4.0, or 2.0 net. A 1-card pile is about 1.3 with no bull. The forced player faces a real choice, and piles do build to 3-5 cards, so bulls happen.
- Penalty comes only from piles you take, and the pile you take is built by everyone. (fixes: P4): A penalty is no longer one predecessor's hand passed on. Who is forced, and when, depends on blocking, timing and the forced player's choice of pile, so play rather than the deal sets the gap.
- Drop the voluntary-take mechanic entirely. Every simple policy is now restricted to fitting plays: always the lowest fitter, always the highest fitter, always pile A, or random. (fixes: P1): The reflex no longer exists. Each remaining fixed policy ignores where the tops will land and who will face full piles, so it can be steered into the forced takes. This was checked case by case in expected_effect.

## Kept from the original

- Numbered cards with circular fitting: higher than the top and at most 10 above, wrapping from N to 1.
- You must play if you can, and take a pile only when you cannot.
- Ox-head penalties, with 11-style 'double' cards worth 3 and multiples of 5 worth 2.
- Bulls as the reward for taking a big pile.
- Several piles to choose among, with pressure building as piles grow.
- The lowest total penalty wins.

## The variation's rules

CARDS. The deck has N cards numbered 1 to N: N = 30 with 3 players, N = 40 with 4 players.

OX-HEADS. Cards 11, 22 and 33 carry 3 ox-heads. Every other multiple of 5 (5, 10, 15, 20, 25, 30, 35, 40) carries 2. All other cards carry 1.

SETUP.
- Shuffle once.
- Deal each player a private hand of H cards: H = 9 with 3 players, H = 8 with 4 players.
- Turn the next two cards face up. They start Pile A and Pile B, each of size 1.
- The rest (1 card with 3 players, 6 with 4) are set aside unseen and take no part in the game.
- Everyone starts with penalty 0 and bulls 0.

INFORMATION. You see only your own hand. Everyone sees both piles (their cards, top card, size and ox total), every card played and every take, and all penalties and bulls.

FITTING. A card c fits a pile with top card t if d = (c - t) mod N is between 1 and 10 inclusive. Example with N = 30: on a top of 25, the cards 26 to 30 and 1 to 5 fit.

ROOM. A pile has room if it has fewer than 5 cards.

PLACEMENT. A placement is a card from your hand that fits a pile with room.

ROUNDS. The game lasts exactly H rounds. In round r the seats act one after another, starting with seat ((r - 1) mod number of players) + 1 and continuing in seat order, wrapping round. Each seat starts 3 times (3 players) or 2 times (4 players).

TURN. On your turn you choose exactly one card from your hand and one pile (A or B).
- If you hold at least one placement, you must choose a placement: the card goes on top of that pile. The pile's size rises by 1 and its ox total rises by the card's ox.
- If you hold no placement at all, you must TAKE. You choose any card and either pile, and then:
  1. Add that pile's ox total to your penalty.
  2. If the pile had 3 or more cards, gain 1 bull.
  3. Discard that pile's cards out of the game.
  4. Your chosen card becomes that pile's only card (size 1, ox equal to that card's).
- The other pile is unchanged.
- Every turn removes exactly one card from your hand, so all hands empty at the end of round H.

BULLS. Each bull is worth -2 at the end. Bulls are unlimited and never move between players.

END. After round H, each player's final score = penalty - 2 x bulls. Cards left in the two piles count against nobody.

Objective: The lowest final score (penalty minus twice bulls) wins. If two or more players tie for lowest, the game is a draw among them.

Expected effect: Takes now happen only when a player is forced, either because both piles are full or because no card in hand fits a pile with room. Each turn's choice is therefore which fitting card to play and which pile to feed. Players feed the pile they want to fill before an opponent's turn, and they leave tops that opponents (judged by counting the cards already played) are unlikely to be able to follow. They also keep a fitter in reserve for when piles are near full.

When forced, the choice is real. A big pile costs about 6.7 ox but returns a bull (about 4.7 net). A small pile costs about 1.3 with no bull. The card you restart with sets the next fitting window.

Policy check. The reflex take is now illegal. 'Always the lowest fitter', 'always the highest fitter' and 'always pile A' each ignore which pile fills on whose turn and which top is left, so a counting opponent can steer them into the 5-card takes. Each loses a substantial share of games to sensible play, and random play loses most games.

Seat order. Ten pile slots and irregular forced takes break the fixed seat cycle, so seat order no longer picks the victim. The rotating start balances first turns.

Luck. The deal still shapes how many fitters a player holds, but penalties come from piles everyone built and from takes whose timing play controls. The deal is no longer one predecessor's hand passed straight on.

Talk is left out. Interests do conflict, but with hidden hands and no binding deals a message could only be an unverifiable claim about one's cards. That adds words rather than reasoning, and it risks two players ganging up to force the third.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 9 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
