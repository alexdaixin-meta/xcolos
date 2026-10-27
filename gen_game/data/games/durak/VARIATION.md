# Variation: Duel Durak

Two-player Durak with fixed 8-card hands, 20 unseen set-aside cards, a trump chosen by offer-and-pick, and at most one throw-in per bout. The first player to shed all their cards wins.

Players: 2 to 2, best with 2

## Review of the original

Durak is a Russian shedding card game for 2 to 6 players with a 36-card deck and a trump suit. Attackers lead cards, the defender must beat each one or pick up the whole table, extra cards of matching rank can be thrown in, and the last player left holding cards is the loser (the durak).

- **non_degenerate**: good. No simple policy is safe. Always TAKE piles cards into your own hand and loses. Always beating with the lowest legal card spends trumps on cheap attacks. Always attacking with the lowest card lets the defender discard cheaply. Seat order matters only through who holds the lowest trump, and that is random.
- **skill_sensitive**: weak. Card counting, saving trumps and choosing throw-ins give a real edge. With 2 to 6 players and a talon that keeps refilling hands, the deal and the draws swing many games.
- **headroom**: good. It is played seriously by humans. Beginners can still empty their hands. Experts improve through memory, inference about the opponent's hand and timing.
- **reasoning_dependent**: good. Hands are hidden. What the opponent plays, takes or declines to beat reveals their hand, and good play needs a plan for when to spend trumps.
- **verifiable**: good. Who runs out of cards is plain fact, and legality is arithmetic on suit and rank.
- **fits_platform**: weak. Multi-player throw-ins of up to 6 cards and draw-to-6 refills make a bout far longer than the step limits allow. Durak needs a cut-down version.

## Problems

- P1: The full multi-player bout (up to 6 attacks, several throwers, a refill order) exceeds the step and choice limits per round.
- P2: The refilling talon adds a lot of luck and many random draws per round.
- P3 (built version): the throw-in option list was built from the attacker's whole hand instead of only the cards whose rank matches a card on the table, so illegal cards (for example id 20 when the table held ranks 6 and 7) were offered.
- P4 (built version): after the defender beat the attack with their last card, the attacker was still offered throw-ins. The bout must instead end beaten off and the defender wins.
- P5 (built version): the rule text left the matching test, the skip condition and the fallback for a missing answer implicit, so the builder improvised them.

## Changes

- Two players. Each bout has at most 4 choices: attack, defend, one throw-in, defend the throw-in. (fixes: P1): Keeps attack, beat-or-take and throw-in while fitting at most 4 choice steps per round.
- Deal 8 each from the shuffled 36 and set the other 20 aside unseen. There is no talon and no refill. (fixes: P2): Only one random event (the shuffle). The unseen 20 keep the opponent's hand uncertain, so inference still matters.
- The throw-in options are defined as an explicit computed list: PASS, plus each attacker card c with c mod 9 equal to (attack card mod 9), or equal to (defence card mod 9) when a defence card was played. The list never includes other hand cards. (fixes: P3): This states the matching test as one arithmetic comparison per card, so the builder cannot offer the whole hand.
- The throw-in list is built only when the defender said TAKE, or still holds at least 1 card, and the attacker holds at least 1 card. Otherwise the list is just PASS and the bout resolves straight away. (fixes: P4): Enforces that you cannot throw in against an empty-handed defender. Beating your last card ends the bout and wins.
- The rules are written as a numbered step list. Each step states its condition and the fallback for a missing or illegal answer: attack falls back to the lowest card id, defence to TAKE, throw-in to PASS. (fixes: P5): Removes the ambiguity the builder filled in wrongly.
- The first player to empty their hand wins. If both empty in the same bout, it is a draw. There is a 40-round cap, after which fewer cards wins and equal counts draw. (fixes: P1): This is the durak ending without a talon, with a guaranteed finish. No total is compared, so the higher-total trap does not arise.

## Kept from the original

- The 36-card deck from 6 to Ace in four suits, with a trump suit.
- Attack, then the defender beats with a higher card of the same suit or with a trump, or takes the table.
- Throwing in a card of a rank already on the table.
- A successful defender becomes the attacker. A defender who takes is attacked again.
- Shedding all your cards is the goal. Being left holding cards loses.

## The variation's rules

CARDS. There are 36 cards with ids 0 to 35.
- Suit = floor(id/9): 0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades.
- Rank = (id mod 9) + 6: 6, 7, 8, 9, 10, Jack 11, Queen 12, King 13, Ace 14.
- Two cards have the same rank when their ids are equal mod 9.

BEATING. A card d beats a card a if either:
(i) floor(d/9) = floor(a/9) and d > a, or
(ii) floor(d/9) = trump and floor(a/9) is not trump.

SETUP (before round 1):
- The deck 0..35 is shuffled once.
- Seat 1 gets shuffled positions 1-8 and seat 2 gets positions 9-16. Both hands are sorted ascending.
- Positions 17-36 (20 cards) form the set_aside pile. It is never seen and never drawn from.
- Each seat sees only its own hand. Both are told that each player holds 8 cards.
- Table values: trump = -1, attacker = none, bout = 0, discard = empty.

ROUND 1 (trump choice).
- Step A: Seat 2 chooses one pair of suits from these six: Clubs and Diamonds; Clubs and Hearts; Clubs and Spades; Diamonds and Hearts; Diamonds and Spades; Hearts and Spades. A missing or illegal answer means Clubs and Diamonds.
- Step B: Seat 1 chooses one suit of that pair. A missing or illegal answer means the first suit named. That suit becomes trump and is announced.
- First attacker: the seat holding the lowest-id card of the trump suit. If neither seat holds a trump, seat 2 attacks first.

ROUNDS 2 to 40 (one bout per round). The defender is the seat that is not the attacker.
- Step 1 (reset): table_cards = empty, attack_card = -1, defence_card = -1, throw_card = -1, defender_took = false.
- Step 2 (attack): The attacker chooses any card from their hand. A missing or illegal answer means their lowest-id card. The card moves from their hand to table_cards as attack_card and is shown to both players.
- Step 3 (defence options): The defender's options are TAKE, plus every card in the defender's hand that beats attack_card.
- Step 4 (defence): The defender chooses. A missing or illegal answer means TAKE. If they choose a card, it moves from their hand to table_cards as defence_card. If they choose TAKE, defender_took = true.
- Step 5 (throw-in options): The option list is built as follows.
  - Start with [PASS].
  - Only if (defender_took is true OR the defender holds at least 1 card) AND the attacker holds at least 1 card: for each card c in the attacker's hand, add c if c mod 9 = attack_card mod 9, or if defence_card is not -1 and c mod 9 = defence_card mod 9.
  - No other card is ever added. In particular, if the defender beat the attack with their last card, the list is only [PASS].
- Step 6 (throw-in): The attacker chooses one option. A missing or illegal answer means PASS. A chosen card moves from the attacker's hand to table_cards as throw_card and is shown. At most 1 card is thrown in per bout.
- Step 7 (second defence options): This step and Step 8 happen only if throw_card is not -1 and defender_took is false. The options are TAKE, plus every card in the defender's hand that beats throw_card.
- Step 8 (second defence): The defender chooses. A missing or illegal answer means TAKE. A chosen card moves from their hand to table_cards. TAKE sets defender_took = true.
- Step 9 (resolve):
  - If defender_took is true, all table_cards go into the defender's hand, sorted, and the attacker stays the attacker. The result is announced as 'taken'.
  - Otherwise all table_cards go to discard, the defender becomes the next attacker, and the result is announced as 'beaten off'.
- Step 10: Update both hand sizes, announce them, and set bout = bout + 1.
- Step 11 (end check):
  - If exactly one seat holds 0 cards, that seat wins and the game ends.
  - If both hold 0, the game is a draw.
- After round 40, the seat with fewer cards wins. Equal counts are a draw.

Objective: The first seat to hold 0 cards at an end check wins. If both seats hold 0 at the same check, the game is a draw. If round 40 ends with both still holding cards, the seat with fewer cards wins, and equal counts are a draw.

Expected effect: The game plays as real Durak in miniature. Players count the cards they have seen, and because 20 cards are unseen they must infer the rest of the opponent's hand from what the opponent takes and what they beat with. They choose when to spend trumps, and they use throw-ins to force a pickup or to dump a matching card. The trump offer is a small bluff-and-read: seat 2 offers suits that suit its own hand, and seat 1 infers which suit to refuse. The throw-in now offers only rank-matching cards and is skipped against an empty-handed defender, which matches rules R10 and R11. There is no talk, because this is a two-player zero-sum game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
