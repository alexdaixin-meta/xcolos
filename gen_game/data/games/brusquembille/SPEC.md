# Mirror Brusquembille

Two-player, 16-trick card game. Each player draws from an identical private 16-card pile, and the follower must follow suit only in the last three tricks.

Players: 2 to 2, best with 2

## Parameters

- `ace_points` = 11
- `ten_points` = 10
- `king_points` = 4
- `seven_points` = 0
- `suits` = 4
- `ranks` = 4
- `pile_size` = 16
- `pile_points` = 100
- `hand_size` = 3
- `pile_after_deal` = 13
- `tricks` = 16
- `last_drawing_trick` = 13
- `first_must_follow_trick` = 14
- `last_trick_bonus` = 1
- `total_points` = 201

## Round

1. **sync** (all players): Each player sees their own hand plus the public trump, leader, trick, both scores, both pile_count values and played_cards. Neither sees pile_1 or pile_2.
2. **ask** (the seat equal to leader): led_card = the chosen card. Remove it from the leader's hand and append it to played_cards. Announce it to both players.
3. **ask** (the seat not equal to leader): follow_card = the chosen card. Remove it from the follower's hand and append it to played_cards. Announce it to both players.
4. **update** (all players): Set trick_winner. If exactly one of led_card and follow_card is of the trump suit, its player wins. Otherwise, if both cards share a suit, the follower wins only when follow_card's point value is strictly greater than led_card's (Ace 11 > Ten 10 > King 4 > Seven 0), and the leader wins otherwise, including identical cards. Otherwise (different suits, neither trump) the leader wins. Announce the winner.
5. **update** (trick_winner): Add points(led_card) + points(follow_card) to the winner's score, plus 1 if trick == 16. Points are A=11, T=10, K=4, 7=0. Announce both scores.
6. **update** (all players): leader = trick_winner.
7. **update** (trick_winner, then the other seat): Only when trick <= 13: the winner moves one random card from their own pile (pile_1 or pile_2) into their hand and loses 1 pile_count. Then the loser does the same from their own pile. Both hands are back to 3 cards.
8. **update** (all players): trick += 1.
9. **check** (all players): End the game if trick > 16. Otherwise play the next trick.

## Ending

- ends when: trick > 16
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After 16 tricks, the player with the higher score wins. The 201 points cannot split evenly, so there is no draw.

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer set 2. The game is a two-player duel of mirrored piles, and every rule (leader/follower, the 201-point total that rules out ties) assumes two seats.
- No talk step: The source has no communication, and in a zero-sum two-player duel talk adds nothing to reason about.
- Card codes as rank letter plus suit letter (A/T/K/7 with S/H/D/C): A compact text form for list membership and suit/rank tests.
- Same-suit comparison by point value: The point values 11 > 10 > 4 > 0 are strictly ordered like the ranks, so comparing points is the same as comparing ranks.
- The follower is asked after the leader, with ask: The rules are sequential: the follower sees the led card before choosing.
- Strategy at this table: A thoughtful player tracks the cards played to infer which cards the opponent still has between hand and pile, saves trumps and high cards for valuable tricks, and plans for the forced-follow endgame of tricks 14 to 16.

## Simplifications

- Drawing the 'top card' of a shuffled pile is a random draw from the pile list: The order is hidden from everyone and fixed by a random shuffle, so a seeded random draw is equivalent.
- Each pile is a hidden table attribute (pile_1, pile_2) rather than a player attribute: The rules hide a pile even from its owner, and a player attribute cannot be hidden from its owner. Each pile is still drawn only by its own seat, and its public size is kept in that player's pile_count.
- Card points and the trick winner are worked out by conditional arithmetic over the card codes: The engine has no lookup table, so the 4 rank values and the suit/trump tests are written as if-chains in the update steps.

## Unsupported (needs engine work)

- none
