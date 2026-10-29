# Variation: Officers' Schafkopf: Bidding Match

A two-player Schafkopf match of 4 short hands with a 16-card deck and the Officers' face-down/face-up layout. Players bid simultaneously for the right to declare, the declarer picks a Solo or Wenz, the defender may Stoß, and 8 tricks are played. Match points decide the winner.

Players: 2 to 2, best with 2

## Review of the original

Officers' Schafkopf is a two-player version of the Bavarian trick-taking game. Each player has a private hand plus rows of face-down cards topped by face-up cards. The non-dealer announces a contract (a Suit Solo or a Wenz) and may be doubled (Stoß), then 16 tricks are played with must-follow rules. The declarer needs 61 of the 120 card points to win.

- **non_degenerate**: weak. Contract choice, the Stoß and card play all change the outcome, and no trivial policy wins. But the non-dealer is forced to declare on whatever cards they get, and the dealer always gets to react. In a single deal the seat and the cards decide much of the result, and a lone hand has no way to even out who declares.
- **skill_sensitive**: weak. Card play rewards counting and inference over a long game. But one deal of 32 cards decides the winner, and a declarer handed a weak hand with no way out usually loses whatever their skill. Luck of the deal dominates a one-hand match.
- **headroom**: good. Trump management, counting card points, reading the opponent's hand from the visible up cards and from their contract, and timing which up cards to release give a deep skill ceiling. A beginner can still take tricks and points.
- **reasoning_dependent**: good. Hand cards are private and the down cards are unknown even to their owner. Players must infer holdings from the contract, the Stoß decision and the play, and plan which down cards they will uncover.
- **verifiable**: good. The card-point total against the 61 threshold is pure arithmetic.
- **fits_platform**: bad. 32 tracked cards, two rows of four stacks per player and 16 tricks make a state far larger than the attribute limit. The optional 'deal as hands' rule is ambiguous, and with only one deal there is no match structure.

## Problems

- The state is too large: 32 cards in four stack positions per player plus a hand exceeds the platform's attribute and step limits.
- One deal decides everything, so luck of the cards swamps skill.
- The non-dealer is forced to declare whatever they hold, so a bad deal for the forced declarer is close to an automatic loss. This is a seat and deal edge with no decision to correct it.
- Winning is binary (61 or not). It gives no reward for judging how strong a hand is, so there is little to reason about before play beyond picking the trump suit.
- The rules are underspecified for building: 'or deal as hands' is optional, the trump order is not stated, and the scoring of doubles is not stated.

## Changes

- Shrink the deck to 16 cards (Ace, Ten, Ober, Unter in four suits, 104 card points). Each player gets 4 private hand cards and 2 stacks of one face-down card under one face-up card. A hand is 8 tricks and the declarer needs 53. (fixes: The state is too large: 32 cards in four stack positions per player plus a hand exceeds the platform's attribute and step limits.): Keeps the private hand, the face-up and face-down stacks, the revealing of the down card and the Solo/Wenz trump structures, while bringing the state and step count within the limits.
- Play a match of 4 hands with the dealer alternating, scored in match points. (fixes: One deal decides everything, so luck of the cards swamps skill.): Several deals average out card luck, and each player is forehand twice, so no seat has an edge over the match.
- Add a simultaneous sealed bid before the contract: Pass, 53, 66 or 79 card points. The higher bid declares, ties go to forehand, and if both pass, forehand must declare at 53. A higher bid is worth more match points if made and costs as much if failed. (fixes: The non-dealer is forced to declare whatever they hold, so a bad deal for the forced declarer is close to an automatic loss. This is a seat and deal edge with no decision to correct it.): A weak hand can now hand the declaration to the opponent. Bidding forces each player to judge their own strength from partial information and to guess the opponent's bid. Hand evaluation becomes a scored skill.
- Use graded match points: a bid of 53 is worth 2, 66 is worth 3 and 79 is worth 4, plus 1 for taking all 8 tricks, all doubled by Stoß. The winner is the player with more match points, then more total card points. (fixes: Winning is binary (61 or not). It gives no reward for judging how strong a hand is, so there is little to reason about before play beyond picking the trump suit.): This rewards accurate judgement of how much the hand can make rather than a single win/lose line. The Stoß becomes a risk decision with a real price either way.
- State every rule explicitly: the dealing layout, the trump orders for Solo and Wenz, the following rules, and when a down card is revealed and becomes playable. (fixes: The rules are underspecified for building: 'or deal as hands' is optional, the trump order is not stated, and the scoring of doubles is not stated.): So the game can be built and played without guessing.

## Kept from the original

- Two-player Schafkopf trick play with must-follow-suit rules and the winner of a trick leading next.
- The Officers' layout: face-down cards under face-up cards, a down card turned up when the card above it is played and playable from the next trick.
- The contract choice between a Suit Solo (Obers, Unters and the trump suit are trumps) and a Wenz (only Unters are trumps).
- The Stoß doubling by the defender.
- Card-point counting with Ace 11, Ten 10, Ober 3 and Unter 2, and a declarer needing just over half the points.

## The variation's rules

DECK. There are 16 cards: Ace, Ten, Ober and Unter in each of four suits (Acorns, Leaves, Hearts, Bells). Card points are Ace 11, Ten 10, Ober 3 and Unter 2, which makes 104 in the deck.

MATCH. The match is 4 hands. Each hand is one bidding round followed by 8 trick rounds, which makes 36 rounds in total. Player 1 deals hands 1 and 3 and Player 2 deals hands 2 and 4. The non-dealer is called forehand.

DEAL (start of each hand's bidding round, the only random event of the round). Shuffle the 16 cards. Each player receives:
- 4 private hand cards, seen only by their owner;
- 2 stacks, each made of one face-down card under one face-up card.
The face-up cards (4 in total) are visible to both players. Face-down cards are unknown to both players, including their owner.

BIDDING ROUND.
(1) Both players secretly and simultaneously choose a bid: Pass, 53, 66 or 79. The bid is the number of card points the player promises to take as declarer.
(2) The higher bid becomes declarer at that bid. If the bids are equal and not Pass, forehand is declarer at that bid. If both pass, forehand is declarer at 53. Both bids are then announced.
(3) The declarer chooses a contract and it is announced:
- Acorns Solo, Leaves Solo, Hearts Solo or Bells Solo: trumps are, from highest to lowest, Ober of Acorns, Ober of Leaves, Ober of Hearts, Ober of Bells, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells, then the Ace and the Ten of the chosen suit. The three other suits each hold only Ace above Ten.
- Wenz: trumps are, from highest to lowest, Unter of Acorns, Unter of Leaves, Unter of Hearts, Unter of Bells. Each suit holds Ace above Ten above Ober.
(4) The defender chooses Stoß (double) or No Stoß, and the choice is announced. The multiplier is 2 with Stoß and 1 without.

TRICK ROUNDS (8 per hand).
Available cards: a player may play any of their private hand cards or any face-up card on top of one of their stacks.
Lead: in the first trick forehand leads; afterwards the winner of the previous trick leads. The leader plays one available card.
Follow: the other player then plays one available card. All trumps count as one suit, the trump suit, so in a Solo an Ober or Unter is never a card of its printed suit. If the follower has an available card of the led suit, they must play one. Otherwise they may play any available card.
Trick winner: if any trump was played, the higher trump wins. Otherwise the higher card of the led suit wins. The winner adds the card points of both cards to their card-point total for this hand.
Reveal: after the trick, any face-down card whose face-up card was played this trick is turned face up. It is available from the next trick on.

HAND SCORING (after trick 8).
- If the declarer's card points are at least their bid, the declarer scores the contract value in match points. Otherwise the defender scores it.
- Contract value = base, plus 1 if the player who scores took all 8 tricks, multiplied by the Stoß multiplier.
- The base is 2 for a bid of 53, 3 for a bid of 66 and 4 for a bid of 79.
Each player's card points for the hand are also added to their running card-point total for the match. Then all cards are collected for the next deal.

Objective: After 4 hands, the player with more match points wins. If match points are equal, the player with the higher total card points over all 4 hands wins. If both are equal, the match is a draw.

Expected effect: Players must estimate the value of a hand from 4 private cards, 4 visible up cards and 4 unknown down cards, and bid against an opponent's sealed estimate. Overbidding gives away up to 4 match points (8 if doubled), and underbidding or passing lets the opponent declare cheaply. The Stoß becomes a real read on whether the declarer overbid. Card play rewards counting, inferring the opponent's hand from their bid, contract and Stoß decision, and timing when to release up cards to uncover what lies beneath. Simple policies lose:
- Always bidding 79 fails most hands and pays the opponent 4 each time.
- Always passing lets the opponent declare at will, and when forehand it is forced to declare at 53 on any cards.
- Always using Stoß gets punished by strong declarers, and never using it gives up the doubled points from failed contracts.
Alternating the dealer and playing 4 hands removes the seat edge and reduces deal luck. Bidding lets a player with weak cards still gain by defending well and doubling overbids. There is no talk phase because the game has two players with strictly opposed interests.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
