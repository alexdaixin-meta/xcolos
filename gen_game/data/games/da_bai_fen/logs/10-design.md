# 10 design

- time: 2026-10-28T03:10:57+00:00 (87.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 4771307c60e8c87d, reply sha256 64298a167b39f1b6

## Sent

````
Original game: Da Bai Fen
Players in the original: 4 to 4

Original rules:
Four players in fixed partnerships (facing) use 54 cards including two jokers. Point cards are K=10, 10=10, 5=5 for 100 total. Each side has a level 2-Ace; declarers' level is the trump rank. 18 trumps: both jokers (red high), all cards of trump rank, and all cards of trump suit. During the deal 12 cards each are drawn one by one from a central packet; any player holding the trump rank may expose it face up to make its suit trumps. If none exposed, the top of the 6-card kitty determines trumps. Leader takes kitty and discards 6 face down. Void-trump hand may claim a redeal. Play is anticlockwise. Single or multiple cards of one suit may be led, but a multiple lead is only legal if no remaining card of that suit in any hand beats any led card. Follow suit with same number of cards if able; else discard anything. Highest trump wins, or highest of led suit if no trump. Earliest of equal trumps wins. Points in declarers' tricks vs opponents: points taken determine if declarers stay and score level-ups or opponents become new declarers and may score.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Bring each round down to at most 4 choice steps by removing the separate trump-naming decision. Either fix the trump suit by hand number (hand 1 Spades, hand 2 Hearts, hand 3 Clubs, hand 4 Diamonds), or make the trump suit the suit of the declarer's first lead, so naming trumps is part of a play the declarer already makes. Then rework the balance so card play actually decides matches. Make sure the deal is a real fresh random draw each hand, not a fixed order that hands NS the same strong cards every time. Rotate the leader and declarer so neither team gets a structural edge from leading first or declaring in hands 1 and 3. Check that the score bands are not tilted toward NS. A shorter design is also worth considering, for example fewer hands, or tricks with fewer forced follow-suit plays, so that playing well and playing randomly lead to clearly different results.
the game was built and behaves as specified, but evaluation found design flaws:
- every random match ended 'seats 1 and 3': choices do not change the result
- the built game has 5 choice steps per round, over the limit of 4
- against random seats the results were {'seats 1 and 3': 60}
- a thoughtless policy `first@seat1`: won 0, lost 0, drew 60
- a thoughtless policy `first@seat2`: won 0, lost 60, drew 0
- a thoughtless policy `last@seat1`: won 0, lost 0, drew 60
- a thoughtless policy `last@seat2`: won 0, lost 60, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Da Bai Fen is a four-player partnership trick-taking game from China played with 54 cards. Point cards are 5s (5 points), 10s and Kings (10 points each). Trumps are set by a declared rank and suit, the declarers take a 6-card kitty, and the points the opponents capture decide whether the declarers keep the lead and go up in level.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the full card game choices matter and no fixed policy wins. The previous adaptation was degenerate, though: every random match ended 'seats 1 and 3', seat 2 lost all 60 games whether it played first-card or last-card, and seat 1's thoughtless policies drew 60/60. That points to a fixed or tilted deal and a structural edge for the team that leads and declares first. Choices did not change the result."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, skill (counting trumps, feeding points to partner, holding control for the end) matters across many hands. The single-hand deal luck is large, however, and the previous build showed no sensitivity to play at all: results were identical regardless of policy."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Trick-taking with hidden hands has deep play: card counting, inferring voids from discards, partner signalling, timing trumps, and fighting for the last trick. A random player still wins some tricks."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the kitty are hidden. Players must infer holdings from what has been played and from failures to follow suit, read partner's intent, and plan which trick to win. This is strong partial-information inference."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners and captured points are pure arithmetic on cards played."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The original has 12-card hands, trump exposure during a one-by-one deal, kitty exchange, multi-card leads with a global legality check, redeal claims and a level ladder. That is far too many choice steps and rules. The previous build still had 5 choice steps per round against a limit of 4."
    }
  ],
  "problems": [
    "P1: The previous build had 5 choice steps per round (a separate trump/declaration decision on top of four card plays), over the limit of 4.",
    "P2: The deal was not a fresh random deal, or the first-lead and declarer roles were tilted. Seats 1 and 3 won every match whatever anyone did, so choices did not change the result.",
    "P3: Single-deal card luck can swamp skill in a short match, so the stronger partnership does not reliably win.",
    "P4: The original's multi-card leads (legal only if no unseen card beats them), trump exposure during the deal, kitty discard and redeal claims are long rule chains the engine cannot build reliably.",
    "P5: The level ladder (2 to Ace) needs many hands to resolve and is too long for a match.",
    "P6: Play-legality questions (follow suit with the same number of cards) were left to judgement, inviting mistakes or illegal plays by thoughtless policies."
  ],
  "changes": [
    {
      "what": "Each round is exactly one trick: four sequential card plays and nothing else. The trump suit is fixed by hand number (Spades in hands 1 and 3, Hearts in hands 2 and 4), with both jokers as the top trumps. There is no trump-naming or exposure decision.",
      "why": "This brings choice steps to exactly 4 per round and removes the extra declaration step.",
      "fixes": "P1"
    },
    {
      "what": "Hands 1 and 2 are fresh random shuffles. Hands 3 and 4 are duplicate replays of hands 1 and 2: the identical cards and kitty, with every hand rotated one seat, so the other partnership holds each set of cards and the same cards lead first.",
      "why": "The deal is genuinely random each match, yet each partnership plays both sides of every deal. Card luck cancels out and only the quality of play differs.",
      "fixes": "P2, P3"
    },
    {
      "what": "First leads by hand are seat 1, seat 2, seat 2 and seat 3. Each partnership leads first in exactly two hands, and the replay makes each team lead with the same cards the other team led with.",
      "why": "This removes any structural first-lead edge for seats 1 and 3.",
      "fixes": "P2"
    },
    {
      "what": "The deck is cut to 26 cards: four suits of A, K, Q, J, 10, 5 plus two jokers. Each player gets 6 cards and 2 go face down to the kitty. Only single cards are led. There is no kitty exchange and no redeal. Instead the kitty's points, doubled, go to the team that wins the last trick of the hand.",
      "why": "The game becomes buildable while keeping the point cards (still 100 points in the deck), the jokers, the trump suit, the kitty and an end-of-hand fight. Doubled kitty points reward saving control for the final trick.",
      "fixes": "P4"
    },
    {
      "what": "The level ladder is replaced by total captured points over the four hands. The higher partnership total wins, and equal totals are a draw.",
      "why": "This gives a short match decided by arithmetic. Under duplicate dealing the point total measures play directly.",
      "fixes": "P5"
    },
    {
      "what": "The engine offers each player only legal cards. You must play a card of the led suit if you hold one, with trump-suit cards and jokers counting as the trump suit; otherwise you may play any card.",
      "why": "This makes legality mechanical, so no judge and no illegal plays are involved.",
      "fixes": "P6"
    },
    {
      "what": "There is no talk phase.",
      "why": "Partners would simply announce their hands, deleting the inference that makes the game worth playing. The conflict is between teams, and inside a team there is nothing to bargain. Signalling happens through card play, as in the original.",
      "fixes": "P3"
    }
  ],
  "keeps": [
    "Four players in two fixed facing partnerships (seats 1 and 3 against seats 2 and 4), playing anticlockwise.",
    "Point cards 5 = 5, 10 = 10, K = 10, totalling 100 points.",
    "Two jokers as the highest trumps (big above small), with a trump suit beating all other suits.",
    "Follow suit if able; otherwise play anything. The highest trump wins, else the highest card of the led suit.",
    "A hidden face-down kitty whose points matter at the end of the hand.",
    "The core skill of capturing and feeding point cards to your partner's winning tricks."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game's essence (partnership trick-taking for point cards with trumps and a kitty) fits in four sequential plays per round. Duplicate dealing removes the seat and luck bias that broke the previous build."
  },
  "variation": {
    "name": "Da Bai Fen Duplicate",
    "summary": "A short partnership point-trick game over 4 hands of 6 tricks. Hands 3 and 4 replay the deals of hands 1 and 2 with the partnerships' cards swapped, so the team that plays the same cards better wins.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "SEATS AND TEAMS: Seats are numbered 1, 2, 3, 4 in anticlockwise order. Team A is seats 1 and 3; Team B is seats 2 and 4. Play always proceeds anticlockwise: after seat 1 comes 2, then 3, then 4, then 1.\n\nCARDS: The deck has 26 cards: the Big Joker, the Small Joker, and four suits (Spades, Hearts, Clubs, Diamonds) each containing A, K, Q, J, 10, 5. Point values are 5 = 5 points, 10 = 10 points, K = 10 points, and all other cards 0. Each suit holds 25 points, so the deck holds 100.\n\nTRUMPS: Hands 1 and 3 have Spades as trump; hands 2 and 4 have Hearts as trump. The trumps are, from high to low: Big Joker, Small Joker, then A, K, Q, J, 10, 5 of the trump suit. Both jokers belong to the trump suit for following purposes. In every non-trump suit the order is A, K, Q, J, 10, 5.\n\nTHE MATCH has 4 hands of 6 tricks each, 24 rounds in total. Each round is one trick.\n\nDEALING: At the start of hand 1 the 26 cards are shuffled at random. Each seat receives 6 cards, which are private to that seat, and the remaining 2 cards form the kitty, face down and seen by no one. Hand 2 is a new random shuffle, dealt the same way. Hand 3 replays hand 1: every seat receives the exact 6 cards held in hand 1 by the seat before it in seat order (seat 2 gets seat 1's hand 1 cards, seat 3 gets seat 2's, seat 4 gets seat 3's, seat 1 gets seat 4's), and the kitty is the same 2 cards. Hand 4 replays hand 2 in the same rotated way. Players are told when a hand is a replay.\n\nFIRST LEADER of each hand: seat 1 in hand 1, seat 2 in hand 2, seat 2 in hand 3, seat 3 in hand 4. In each replay, the first leader holds the same cards as the first leader of the original hand.\n\nA TRICK (one round): The leader plays any one card from their hand face up. Then the other three seats, in anticlockwise order, each play one card. Each player sees all cards already played to the trick.\n- Following: If the led card is a trump (a joker or a trump-suit card), each player must play a trump if they hold one. Otherwise each player must play a card of the led suit if they hold one. A player with no card of the required suit may play any card.\n- The engine lists only the legal cards as options.\n- Winning: If any trump was played, the highest trump wins the trick. Otherwise the highest card of the led suit wins. Off-suit non-trump cards never win.\n\nAFTER EACH TRICK: All four cards are announced along with the winner. The winner's team adds the point value of the four cards to its match total. The winner leads the next trick of the same hand.\n\nEND OF HAND: After the 6th trick the kitty is revealed. Its point value multiplied by 2 is added to the match total of the team that won the 6th trick. The next hand begins with its own deal and first leader.\n\nINFORMATION: Each player always sees their own cards, all cards played so far in the hand, both teams' match totals, the trump suit, the trick number and the hand number. Other players' hands and the kitty stay hidden until the kitty is revealed at the end of the hand. There is no table talk.",
    "objective": "After hand 4, the team with the higher match total (captured card points plus doubled kitty points) wins. If the totals are equal, the match is a draw.",
    "expected_effect": "Because each partnership plays both sides of every random deal, deal luck cancels. A team that counts trumps, infers voids from discards, feeds 10s and Kings onto tricks its partner is winning, ducks low cards to the opponents, and keeps a high trump for the 6th trick (doubled kitty) will outscore a weaker team holding the very same cards. Thoughtless policies such as always playing the first or last legal card can lose to any thinking or even random opponent. If all four seats play the same thoughtless policy, the duplicate structure tends toward a draw rather than a fixed seat win. The first-lead advantage is split evenly: each team leads first twice, with mirrored cards."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 17,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 24
  }
}
```
````
