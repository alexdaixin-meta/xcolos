# Variation: Knock Brag (3-player)

Three players each hold three hidden cards and trade with a three-card table hand (one card face up) while every exchange is announced. The round's leader may knock to freeze their hand, after which the others get one final action. The worst hand at the showdown loses a life, a knocker who ends worst loses two, and the last player standing wins.

Players: 3 to 3, best with 3

## Review of the original

Bastard Brag is a 3-card Brag variant. Players take turns swapping cards with a three-card table hand (one card face up, two face down) or swapping their whole hand for it, until someone knocks. In the lives version the worst hand at showdown loses a life, and the last player with lives wins.

- **non_degenerate**: good. Only the single worst hand is punished, so no fixed policy is safe. Always knocking at once locks in a random hand and risks the penalty. Never knocking leaves the timing to others. Always taking the face-up card tells everyone what you hold. Seat order rotates, so no seat keeps an edge.
- **skill_sensitive**: weak. Any one deal is noisy. Over several lives, though, the better player wins more often: they track what others take and leave, choose between blind and open swaps, and time the knock. The betting version adds bluffing, but it relies on chips and pot sizes the platform cannot reward.
- **headroom**: good. A weak player still survives deals, because only the worst hand loses. A strong player improves through card counting, reading the exposed cards, knock timing and judging when a mediocre hand is good enough.
- **reasoning_dependent**: good. Hands and the face-down table cards are hidden. The announcements (what was taken, what was left, what was exposed) let a player infer what opponents hold. Knocking is a bet on where you rank among the hidden hands.
- **verifiable**: good. Hand ranking and life loss are mechanical. Suit tie-breaks and flushes add bookkeeping but need no judge.
- **fits_platform**: weak. Turn-based and text-only. However, 3 to 10 players, a 52-card deck with suits and flushes, open-ended knocking and the betting version push past the step limits and need a lookup the engine lacks. The previous variation also left several cases undefined and was over its step budget.

## Problems

- The previous variation did not say who wins when every remaining player ties for the lowest score and would reach 0 lives, nor what happens when a knocker is eliminated alongside others.
- The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous.
- The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round.
- The previous variation did not say whether runs wrap, whether the shuffle shares a round with the showdown (only 1 random draw is allowed per round), or whether a knock counts as a turn.
- With knocks allowed from any seat mid-pass, players who acted earlier in the pass would get no final action, or the round would have to wrap around.
- Suits, flushes and suit tie-breaks in the original need lookup tables the engine lacks.
- The betting version's chip pot cannot be rewarded by a platform that only decides a winner.

## Changes

- Fix the game at exactly 3 players, each with 3 lives. (fixes: The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round.): This caps a round at 3 choices and 3 hand scores, which brings the round inside the step budget.
- Define a round as one pass in which every active player takes exactly one action, starting with that round's leader. The leader moves one active player clockwise every round. Only the leader may knock, and not in the first round of a deal. After a knock, the other players' turns in that same round are their final actions. (fixes: The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous.): A round now always holds one action per active player. Every non-knocker gets exactly one final action without the pass wrapping around. Because the leader rotates, every player gets knock chances.
- Same rule, applied to the knock: since the knocker always acts first in the round, every other player acts after the knock. (fixes: With knocks allowed from any seat mid-pass, players who acted earlier in the pass would get no final action, or the round would have to wrap around.): No player who acted earlier in the pass misses a final action.
- Force a showdown at the end of deal-round 4 when 3 players are active, or deal-round 3 when 2 are active. The deal-round counter counts the rounds of the current deal. (fixes: The previous variation defined a round as one player's turn, but a knock round held up to 4 actions, so the 40-round cap and the forced-showdown count were ambiguous.): This gives a clear, countable end to each deal. With the rotating leader it also gives each player exactly one chance to knock in a full deal.
- Add the rule: if all remaining players tie for the lowest score, nobody loses a life. Losing lives can then never eliminate everyone. Otherwise the knocker's double penalty applies as normal, and survivors continue. (fixes: The previous variation did not say who wins when every remaining player ties for the lowest score and would reach 0 lives, nor what happens when a knocker is eliminated alongside others.): This closes the empty-table case. A lowest-score tie is the only way every remaining player could reach 0.
- Score each hand with one arithmetic formula on its sorted cards. The showdown only sets a redeal flag. The shuffle and deal happen at the start of the next round. (fixes: The step budget did not fit: a 4-player knock round needed 4 choices plus scoring of 4 hands, life loss, elimination and a full redeal, all in one round.): Scoring needs no lookup and takes 1 step. The shuffle never shares a round with the showdown, so each round has at most 1 random draw.
- State explicitly: runs do not wrap; a knock is the knocker's action for that round; each action is a single compound choice (action type, own card, slot, card to expose). (fixes: The previous variation did not say whether runs wrap, whether the shuffle shares a round with the showdown (only 1 random draw is allowed per round), or whether a knock counts as a turn.): This removes the remaining ambiguities.
- Keep the suitless 36-card deck (values 1 to 9, four of each) and the prial > run > pair > high card ranking. Drop the betting version. (fixes: Suits, flushes and suit tie-breaks in the original need lookup tables the engine lacks.): The suitless deck removes flushes and suit tie-breaks. The ranking order matches the real frequencies in this deck (prial 36, run 448, pair 1728 of the 7140 possible hands). The chip pot cannot be rewarded, so the lives game is the version to keep.
- Use only the lives version, and decide the winner by survival and lives. (fixes: The betting version's chip pot cannot be rewarded by a platform that only decides a winner.): The platform decides only a winner, so a chip pot has nothing to pay into.

## Kept from the original

- A three-card table hand with one card face up and two face down
- The three exchange options: take the face-up card, make a blind swap, or swap the whole hand and expose one card
- Knocking to freeze your hand, followed by one final exchange for every other player
- Lives: the worst hand loses one, players are eliminated at 0, and the last survivor wins
- Prial is the top hand, 3-3-3 is the best prial, and 1-2-3 (A-2-3) is the best run
- Knocking is risky: a knocker who ends with the worst hand is punished harder

## The variation's rules

PLAYERS AND LIVES: Exactly 3 players, in seats 1, 2 and 3 clockwise. Each starts with 3 lives. A player at 0 lives is eliminated and takes no further part. The others are 'active'.

DECK: 36 cards, four copies each of the values 1, 2, 3, 4, 5, 6, 7, 8 and 9. There are no suits.

HAND SCORE (used at the showdown): Sort a hand's three values so that a <= b <= c.
- Prial (a = c): 300 + a. Exception: 3-3-3 scores 310.
- Run (b = a+1 and c = b+1): 200 + c. Exception: 1-2-3 scores 210. Runs do not wrap: 8-9-1 and 9-1-2 are not runs.
- Pair (a = b or b = c, but not a prial): 100 + 10 x b + (a + c - b). That is 100 + 10 x the pair value + the odd card.
- High card (anything else): a + b + c.
Higher is better.

ROUNDS, LEADER AND DEALS: The game is played in rounds, at most 40. In each round every active player takes exactly one action, in clockwise order starting with that round's leader. Seat 1 leads round 1. In each later round the leader is the next active player clockwise from the previous round's leader. This rotation continues across deals and skips eliminated players. A 'deal' is the series of rounds from one dealing of the cards to its showdown. The deal-round counter is 1 in the first round of a deal, 2 in the second, and so on.

DEALING: At the very start of round 1, and at the start of every round that follows a showdown, the deck of 36 is shuffled (the round's one random event). Each active player receives 3 cards face down that only they see. Three cards go to the table: slot U face up, seen by everyone, and slots D1 and D2 face down, seen by nobody. The value of U is announced. The rest of the deck is not used in this deal.

ACTIONS: On your turn choose exactly one action. Give it as a single choice that includes every detail needed (which action, which of your cards, which slot, which card to expose).
(a) TAKE UP: swap one of your cards for the face-up card U. The card you give becomes the new face-up U. Announced: 'X took the face-up [value] and left a face-up [value]'.
(b) BLIND: swap one of your cards for D1 or D2 (your choice of slot) without seeing it first. Your card goes face down into that slot. You now see the card you received. Announced: 'X made a blind swap with D1' (or D2).
(c) WHOLE HAND: take all three table cards into your hand; you now see them. Your old three cards become the table hand. You choose which of them goes face up as U; the other two go face down into D1 and D2. Announced: 'X swapped the whole hand and exposed a [value]'.
(d) KNOCK: keep your hand and make no exchange. Only the round's leader may knock, and only when the deal-round counter is 2 or more. A knock is the knocker's action for that round. Announced: 'X knocks'.

AFTER A KNOCK: The remaining active players in that same round (everyone after the knocker in clockwise order) each take their action as normal, but must choose (a), (b) or (c). These are their final actions. The showdown then happens at the end of that round.

FORCED SHOWDOWN: If nobody has knocked, the showdown happens at the end of the round whose deal-round counter equals the number of active players plus 1. That is the end of deal-round 4 when 3 players are active, or deal-round 3 when 2 are active. There is no knocker.

SHOWDOWN (at the end of the round): All active hands are revealed and scored, and every player's score is announced and recorded as their 'last showdown score'. If every active player has the same score, nobody loses a life. Otherwise every player with the lowest score loses 1 life, except a knocker with the lowest score, who loses 2 lives. Players at 0 lives or fewer are eliminated. The next round then begins with a new deal and the deal-round counter at 1. If no showdown happened, the deal-round counter rises by 1 for the next round.

END: The game ends at once when only one active player remains, or at the end of round 40.

Objective: If only one player remains, that player wins. If round 40 ends with two or three players still active, the player with the most lives wins. A tie on lives is broken by the higher last showdown score among the tied players. If they are still tied, or if no showdown has yet happened, the game is a draw between them.

Expected effect: Each deal becomes a short inference contest. Take-up and whole-hand actions reveal values while blind swaps hide them, so players must track exposed cards to estimate opponents' hands and the face-down slots. Choosing the action is also a choice about how much to reveal. The rotating leader gives every player knock chances. Knocking early on a decent hand denies the others time to improve, but the double penalty makes a knock on a weak hand costly, so knocking is a calculated bet on one's rank. Only the single worst hand is punished, so a merely average hand often survives; the skill is judging 'good enough' from the signals. The all-tied rule and the fixed round structure make every case defined. Talk is left out: all three players want the others to lose, and talk would add bluffing words without changing the information, which comes from the forced announcements.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
