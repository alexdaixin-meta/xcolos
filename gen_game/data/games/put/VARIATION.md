# Variation: Put: Sixteen Hands

This is a two-player game of three-card Put over 16 hands. The leader leads one card face up and the responder answers it after seeing it. Both players then decide at the same moment whether to Put, knowing the first trick and their own last two cards, and an unmatched Put must be seen or folded. The last two tricks play out automatically, high card against high card and low against low.

Players: 2 to 2, best with 2

## Review of the original

Put is an old two-to-four-player card game played with three-card hands, in which 3 and 2 rank above the Ace. Players play tricks without having to follow suit, and the first to win two tricks takes the hand. Between tricks a player may say 'Put', and the opponent must either fold, conceding 1 point, or 'see it', in which case the whole game rides on that hand. The previous XColos variation replaced the trick play with a single blind choice of card order made by both players at once, and testing found its card phase was a lottery.

- **non_degenerate**: good. In the original, always-Put is beaten by an opponent who sees only with strong cards. Always-fold concedes every Put. Always-see pays out the full game against strong Puts. No simple policy wins, and alternating the deal removes most of the seat edge. The previous variation kept this betting layer, so its failure was elsewhere.
- **skill_sensitive**: weak. The original's skill comes from responding to cards as they are seen and from the Put/fold decision between tricks. The previous variation removed both. It made card play one simultaneous choice of permutation, and if both players randomise uniformly every order is equally good, so card results came from the deal plus random alignment. In the original itself, letting a single seen Put decide the whole game (5 or 7 points) makes the result swing on very few hands.
- **headroom**: weak. The original has bluffing, reading folds and cheap trick-taking. In the previous variation, the only decisions were one Put/See pair per hand, made before any card fell, which left little room to improve. A weak player could still score by luck, but a strong player gained only modestly.
- **reasoning_dependent**: weak. Hands are hidden in the original, so there is real inference, especially after a trick has been seen. The previous variation took away every observation that happened inside a hand: the only information was one public up-card, which the opponent could place anywhere. Inference therefore had nothing to work on.
- **verifiable**: good. Trick results, folds and points all follow from card values and choices by simple comparison and addition. No judge is needed.
- **fits_platform**: weak. The original is text-friendly but open-ended: Puts can come before any trick, and the match is to 5 or 7 points. The previous variation fitted the engine but used 5 choice steps, counting the leader-reply step, which is above the limit of 4. Its Put decision also came only before any card was seen.

## Problems

- P1: In the previous variation, card play is one blind, simultaneous choice of permutation. Against a uniformly random opponent every order is equally good, so trick results are a lottery.
- P2: Every betting decision comes before any card is played, so Put/See cannot use information revealed during the hand. That is the heart of the original game.
- P3: The previous variation needed 5 choice steps (leader call, responder action, leader reply, two orders), which exceeds the limit of 4.
- P4: The stakes are too flat. A seen Put pays 3 against 1 for a plain hand and 1 for a fold, so bluffing and calling carry little weight compared with the card luck.
- P5: The win condition 'more tricks' differs from the original's 'win two tricks', so one trick plus two ties scores, which blurs the trick play.
- P6: With 12 hands at 1-3 points each, chance often decides the match when both players play well.

## Changes

- Trick 1 is played in sequence and in the open. The leader leads one card face up. The responder sees it and then chooses which card to answer with. (fixes: P1): Responding to a seen card rewards real reasoning. The responder can beat cheaply, duck with the lowest card, or spend a high card, and each choice changes what is left. For example, the responder holds 11, 9 and 6, and the leader leads a 4 while holding 12 and 8. Answering with the 6 wins tricks 1 and 3, and so the hand. Answering with the 9 or the 11 loses tricks 2 and 3, and so the hand. A random answer wins only 1 time in 3; correct play wins every time.
- Tricks 2 and 3 are played automatically by a fixed rule. Each player plays their higher remaining card to trick 2 and their lower remaining card to trick 3. (fixes: P1): This removes the blind matching that made the previous variation a lottery. Once trick 1 is played, the rest of the hand is decided by the cards, but each player knows only their own cards. The Put decision then becomes a matter of reading a hidden but fixed outcome. Choosing which card to lead and which to answer with becomes a planning decision, because it decides which two cards are left to meet high-against-high and low-against-low.
- The Put window moves to after trick 1. Both players choose Put or Check at the same moment. If exactly one player Puts, the other chooses See or Fold. If both Put, the Put counts as seen automatically. If both Check, the hand is played for 1 point. (fixes: P2, P3): Betting now uses what has been seen: the trick-1 cards, how the opponent chose to lead or answer, and one's own remaining two cards. Merging the Put and reply decisions keeps the game at exactly 4 choice steps.
- The stakes are raised. A plain hand pays 1 point, a seen Put pays 4, and a fold concedes 1 to the putter. (fixes: P4): Bluffing with a losing hand turns a 1-point loss into a 1-point gain if the opponent folds. Calling a bluff is worth 4. The betting layer now matters as much as the cards, without one hand settling the match the way 'whole game' did.
- The original scoring condition is restored: a player must win at least 2 of the 3 tricks to win the hand. Tied tricks belong to no one, so a trick plus two ties, or a trick each plus a tie, scores nothing. (fixes: P5): This matches the original's trick-and-tie rule. It also makes ducking and tying with an equal card real tactical options.
- The match lasts 16 hands, with the lead alternating so that each seat leads 8 times. (fixes: P6): More hands average out the deal. Exact alternation cancels the responder's information advantage across the match.

## Kept from the original

- The 52-card deck with Three highest, then Two, Ace, King and so on down to Four, with no suits or trumps and no need to follow.
- Three-card hands, where winning two of three tricks takes the hand and tied tricks belong to no one.
- The Put call, with the choice to fold (conceding 1) or to see it for a much bigger stake.
- Calling Put after seeing cards fall, so bluffing and reading the opponent stay central.
- The lead alternating between the two players from hand to hand.

## The variation's rules

CARDS. Use a deck of 52 cards made of four copies of each value from 1 to 13. Value 13 is a Three (highest), 12 a Two, 11 an Ace, 10 a King, 9 a Queen, 8 a Jack, 7 a Ten, 6 a Nine, 5 an Eight, 4 a Seven, 3 a Six, 2 a Five and 1 a Four (lowest). There are no suits. In any trick the higher value wins, and equal values tie the trick, which then belongs to no one.

SETUP. Both players start with a score of 0. The match is exactly 16 hands. Seat 1 leads in odd-numbered hands and seat 2 leads in even-numbered hands. The other seat is the responder.

EACH HAND, in this order:
1. Reset. Restore and shuffle the full 52-card deck. Clear each player's hand, played card, call, response and trick count, and clear the stake and the folded marker.
2. Deal. Deal 3 cards to each player. Each player sees only their own cards.
3. Lead (leader's choice). The leader chooses one of their 3 cards and plays it face up.
4. Announce the lead to both players.
5. Answer (responder's choice). Having seen the lead, the responder chooses one of their 3 cards and plays it face up.
6. Trick 1. Compare the two cards; the higher wins trick 1 and an equal pair is a tie. Announce the result.
7. Put window (both players at the same moment). Each player privately chooses Put or Check, without seeing the other's choice.
8. Announce both calls.
9. Reply. This step happens only if exactly one player chose Put. The player who chose Check now chooses See or Fold. If both chose Put, the Put counts as seen. If both chose Check, there is no Put. The stake for the hand is 4 if a Put was seen (by See or by both Putting), 1 if both Checked.
10. Fold. If a player folded, the player who Put scores 1 point and the hand ends there; skip to step 15. The remaining cards are not shown.
11. Trick 2. Each player automatically plays the higher of their two remaining cards. Compare them as in trick 1.
12. Trick 3. Each player automatically plays their last card. Compare them as in trick 1.
13. Reveal. Show all cards and each player's number of tricks won.
14. Hand scoring. A player who won at least 2 of the 3 tricks scores the stake (1 or 4). If neither player won 2 tricks, because of tied tricks, no one scores.
15. End check. After hand 16 the match ends; otherwise the next hand begins.

There is no talk phase.

Objective: After 16 hands, the player with the higher total score wins. If the totals are equal, the match is a draw.

Expected effect: Card play now rewards thought. Leaders weigh up whether to lead high to take trick 1 or to lead low and save their strength for the high-against-high trick. Responders choose between the cheapest card that beats the lead and throwing away their lowest card, and the worked example shows that this beats random answering. Because tricks 2 and 3 are fixed once trick 1 has been played, the Put window works like a river bet in poker. Each player knows their own two remaining cards and has watched how the opponent led or answered, and must infer whether they hold the winning pair. Bluff-Puts gain 1 point when the opponent folds and lose 4 when seen. That makes every simple policy exploitable. Always-Put loses to an opponent who sees only with strong cards and folds weak ones. Always-Check concedes the 4-point hands to selective Putters. Always-Fold gives away a point on every Put. Always-See pays 4 to every strong Put. Over 16 hands with the lead alternating, deal luck and seat advantage largely cancel out, so reading the opponent and accurate betting decide the match.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 16 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
