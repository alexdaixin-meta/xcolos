# Variation: Blind Officers' Schafkopf

This is a two-player Schafkopf match of four hands. Each hand deals 8 concealed cards to each player and leaves 8 unseen cards in a Blind. Players sealed-bid a contract (Wenz or a Suit Solo, at Simple or Strong level), the defender may double, and 8 must-follow tricks decide whether the contract is made. Match points over four hands decide the winner.

Players: 2 to 2, best with 2

## Review of the original

Officers' Schafkopf is a two-player trick-taking form of Schafkopf. Each player has rows of face-down cards topped by face-up cards. The non-dealer announces a Suit Solo or Wenz contract, the dealer may double, and the declarer needs 61 of the 120 card points to win.

- **non_degenerate**: good. No simple policy dominates. Always declaring loses on weak hands. Always playing the highest card wastes points against trumps. The choice of contract and the double both change the outcome. The original gives the non-dealer the contract choice, but alternating the deal balances this over a match.
- **skill_sensitive**: good. Card play rewards counting trumps and points, managing which hidden card gets uncovered, and choosing the contract. A strong player reliably beats a random one over several deals, though a single deal carries a lot of card luck.
- **headroom**: good. Contract evaluation, the decision to double, and trick-by-trick play under partial information all leave room to improve. A weak player still takes points and sometimes makes contracts.
- **reasoning_dependent**: weak. Up to half the cards are face up, and the down cards surface during play, so much of the game is perfect information late in a hand. Inference is mostly about the face-down cards. This is real but limited.
- **verifiable**: good. Card points are summed, and 61 or more wins for the declarer. This is pure arithmetic.
- **fits_platform**: weak. The rows of down cards topped by up cards, which turn face up when uncovered, are a positional layout. The engine would have to track per-stack state for 16 positions, which is beyond the attribute and step limits. The rules are also ambiguous: '32 cards minus Sixes' and an optional dealing method. A single hand is a single result with no match structure.

## Problems

- The face-up/face-down stack layout needs positional tracking of 16 stacks, which exceeds the attribute and step limits and behaves like a small board.
- With many face-up cards there is little hidden information to reason about once play is under way.
- A single hand is largely decided by the deal, so luck dominates one game.
- The ordered announce-then-double sequence gives the non-dealer a fixed seat edge within a hand.
- The previous variation's bid step said 'one of nine options' but listed eleven, so the legal option list for the simultaneous poll was ambiguous.

## Changes

- Replace the stacks with 8-card concealed hands. The remaining 8 cards become an unseen Blind that is never played. (fixes: The face-up/face-down stack layout needs positional tracking of 16 stacks, which exceeds the attribute and step limits and behaves like a small board.): This removes positional state and creates genuine hidden information. No one knows which 8 cards are out of play, so players must infer the opponent's hand from bids and play.
- Use a 24-card deck (Ace, Ten, King, Ober, Unter, Nine in four suits; 120 card points) with concealed hands and a Blind. (fixes: With many face-up cards there is little hidden information to reason about once play is under way.): This keeps the deck clean and makes the unknown cards the core of the reasoning.
- Play a match of four hands of 8 tricks each (32 rounds), scored in match points with stakes set by contract level and the double. (fixes: A single hand is largely decided by the deal, so luck dominates one game.): Several deals average out card luck. The match score creates planning across hands, such as a trailing player taking on Strong contracts.
- Use a simultaneous sealed bid with Strong above Simple above Pass. Priority breaks same-level ties and alternates by hand. The defender keeps the option to double. (fixes: The ordered announce-then-double sequence gives the non-dealer a fixed seat edge within a hand.): This removes the fixed announcer edge and makes each player predict the other's hand strength.
- State the bid poll as exactly eleven options and list all eleven explicitly. (fixes: The previous variation's bid step said 'one of nine options' but listed eleven, so the legal option list for the simultaneous poll was ambiguous.): The count and the list now agree, so the legal option set is exact.

## Kept from the original

- Bavarian suits: Acorns, Leaves, Hearts, Bells.
- Card values: Ace 11, Ten 10, King 4, Ober 3, Unter 2, Nine 0, totalling 120.
- Contracts: Suit Solo with Obers and Unters as top trumps, and Wenz with only Unters as trumps.
- The defender's double (Stoß).
- Must-follow trick play, with the trick winner leading next.
- A two-player declarer-versus-defender contest over card points.

## The variation's rules

CARDS. There are 24 cards in four suits: Acorns, Leaves, Hearts, Bells. Each suit has Ace (11 card points), Ten (10), King (4), Ober (3), Unter (2) and Nine (0). The deck holds 120 card points.

MATCH. The match is four hands of 8 tricks each, one trick per round: 32 rounds. Both players start with 0 match points. Seat 1 has priority in hands 1 and 3. Seat 2 has priority in hands 2 and 4.

START OF EACH HAND (first round of the hand only).
1) Shuffle and deal 8 cards face down to each player. Each player sees only their own cards. The remaining 8 cards form the Blind. They are never seen by anyone, never played and never scored.
2) Sealed bid. Both players choose at the same moment exactly one of these eleven options:
- Pass;
- Wenz-Simple;
- Acorns-Simple;
- Leaves-Simple;
- Hearts-Simple;
- Bells-Simple;
- Wenz-Strong;
- Acorns-Strong;
- Leaves-Strong;
- Hearts-Strong;
- Bells-Strong.
3) Resolution. If both players pass, the hand is Ramsch. Otherwise Strong beats Simple, and any bid beats Pass. If both players bid at the same level (both Simple or both Strong), the priority player's bid wins whatever the contracts. The winning bidder is the declarer and the other player is the defender. The contract and level are those of the winning bid.
4) Both bids and the resulting contract (or Ramsch) are announced to both players.
5) Double. If the hand is not Ramsch, the defender chooses Double or No double. The choice is announced.

CONTRACTS.
- Wenz: the trumps are the four Unters only, ranked Acorns Unter > Leaves Unter > Hearts Unter > Bells Unter. In every suit the non-trump cards rank Ace > Ten > King > Ober > Nine. Unters belong to no plain suit.
- Suit Solo (Acorns, Leaves, Hearts or Bells, as named): there are 12 trumps, ranked from high to low:
  - the four Obers (Acorns > Leaves > Hearts > Bells);
  - then the four Unters (Acorns > Leaves > Hearts > Bells);
  - then the Ace, Ten, King and Nine of the named suit.
  Obers and Unters belong to no plain suit. In the other three suits the non-trump cards rank Ace > Ten > King > Nine.
- Ramsch: trumps and ranks exactly as in Wenz.

TRICKS (every round).
1) The leader plays any card from their hand. In the first trick of a hand the leader is the declarer, or the priority player in Ramsch. Afterwards the leader is the winner of the previous trick.
2) The other player then plays a card. If a trump was led, they must play a trump if they have one. If a plain suit was led, they must play a non-trump card of that suit if they have one. Otherwise they may play any card.
3) The trick is won by the highest trump in it. If it has no trump, it is won by the higher card of the led suit.
4) The trick winner adds the card points of both cards to their card-point total for the hand, and leads next.
5) The two cards, the trick winner and both players' card-point totals for the hand are announced.

END OF EACH HAND (after the 8th trick). Let D be the declarer's card points and F the defender's card points.
- A Simple contract is made if D >= F + 10.
- A Strong contract is made if D >= 2 x F and D >= 30.
- Stake: Simple is 2 match points and Strong is 4 match points. The stake is doubled if the defender chose Double (Simple 4, Strong 8).
- If the contract is made, the declarer gains the stake. Otherwise the defender gains the stake.
- Ramsch: the player with fewer card points gains 1 match point. If the card points are equal, nobody scores.
- Card-point totals reset to 0 and the next hand begins.

END. After the fourth hand the match ends.

Objective: After the fourth hand, the player with more match points wins. Equal match points is a draw.

Expected effect: The Blind hides 8 cards, so players must infer the opponent's holdings from the sealed bid, the double and the cards played, rather than read them off the table.

The sealed bid with alternating priority makes bidding a prediction of the opponent's strength. Overbidding Strong on a mediocre hand loses to a double.

Across four hands, the match score drives risk. A trailing player must declare Strong or double aggressively, and a leader can pass safely into Ramsch.

No simple policy is safe:
- Always Pass loses whenever the opponent declares and makes a contract.
- Always Strong fails its contracts on weak hands and gets doubled.
- Always Double pays out double whenever the declarer makes the contract.

Card luck is reduced by four deals and by playing skill. With two players no talk phase is used.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 32 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
