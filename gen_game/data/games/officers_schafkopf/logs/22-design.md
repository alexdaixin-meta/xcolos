# 22 design

- time: 2026-10-28T02:52:05+00:00 (38.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 3dfc30e925bc8b37, reply sha256 c73eb4de5905c5d4

## Sent

````
Original game: Officers' Schafkopf
Players in the original: 2 to 2

Original rules:
Played with 32 Bavarian cards minus Sixes. Deal 4 down cards to each player, then 4 up cards to non-dealer. Non-dealer announces a contract: Suit Solo (Acorns, Leaves, Hearts, Bells with 4 Obers and 4 Unters plus suit as trumps) or Wenz (only Unters trumps). Dealer gets 4 up cards and may double (Stoß). Deal remaining 8 down and 8 up so each has two rows of 4 down each topped by up cards, or deal as hands. Non-dealer leads with an upcard. Must follow suit if possible, else trump or discard. When an upcard is played, the downcard beneath is turned face up and becomes playable after the trick. Winner leads next. 120 card-points in pack. Declarer needs 61 to win, defender 60.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: 1) Contradiction in the bid step. The rules say 'one of nine options', then list ELEVEN: Pass, five contracts at Simple, and five at Strong. The parenthetical (Pass, or 5 contracts x 2 levels) also gives 11. A model with only these words cannot tell whether two options are meant to be removed (e.g. Wenz-Strong) or whether 'nine' is a typo. The legal option list for the simultaneous poll must be exact.

2) Everything else is complete:
- Resolution is defined: Strong > Simple > Pass, and a same-level tie goes to priority.
- The first-trick leader is defined, including in Ramsch.
- Follow-suit is defined, with the trump/plain distinction correct per contract: Obers and Unters belong to no plain suit in a Solo, and Unters to no plain suit in Wenz or Ramsch.
- Rankings are total, there are no equal cards, and all 16 cards are played over 8 tricks.
- Scoring and Ramsch ties are defined.
- The match is finite: 32 rounds, decided by arithmetic on stored match points.

3) Limits: 32 rounds <= 40; 15 steps <= 20; 18 attributes <= 20; random draws: one shuffle in the first round of a hand <= 1. Choice steps in the first round of a hand are bid, double, lead and follow = 4 <= 4. Hidden elements: two hands plus the Blind, at most 3.

4) Engine: the hand-start steps need `when` conditions on single steps, which is allowed. The trick winner under six ranking regimes is a complex rule check that the referee may rule. Card points and match points are then arithmetic.

5) Talk: 2 players, none needed. The simultaneous bid is correctly a poll.

6) Fixed-length repetition: each hand is a fresh deal with a stake set by hand quality, so there is no cooperate/betray structure for a safe option to dominate late. A trailing player in hand 4 must bid Strong, which is a genuine decision.

Fails solely on the bid-option inconsistency.
- change: Fix the bid option list so the count and the list agree. State 'one of eleven options' and list all eleven: Pass; Wenz, Acorns, Leaves, Hearts or Bells at Simple; the same five at Strong. Or, if nine was intended, explicitly remove two options (e.g. Wenz-Strong and one other) and list exactly nine.
The variation that was reviewed: Blind Officers' Schafkopf: CARDS. 24 cards in four suits: Acorns, Leaves, Hearts, Bells. Each suit has Ace (11 card points), Ten (10), King (4), Ober (3), Unter (2) and Nine (0). The deck holds 120 card points.

MATCH. Four hands of 8 tricks each, one trick per round: 32 rounds. Both players start with 0 match points. Seat 1 has priority in hands 1 and 3; seat 2 has priority in hands 2 and 4.

START OF EACH HAND (first round of the hand only).
1) Shuffle and deal 8 cards face down to each player. Each player sees only their own cards. The remaining 8 cards form the Blind: they are never seen by anyone, never played and never scored.
2) Sealed bid. Both players choose at the same moment one of nine options: Pass; Wenz-Simple; Acorns-Simple; Leaves-Simple; Hearts-Simple; Bells-Simple; Wenz-Strong; Acorns-Strong; Leaves-Strong; Hearts-Strong; Bells-Strong. (Pass, or a contract — Wenz or one of the four suit Solos — combined with a level, Simple or Strong.)
3) Resolution. If both pass, the hand is Ramsch. Otherwise Strong beats Simple and any bid beats Pass; if both bid the same level, the priority player's bid wins. The winning bidder is the declarer, the other player is the defender, and the contract and level are those of the winning bid.
4) Both bids and the resulting contract are announced to both players.
5) Double. If the hand is not Ramsch, the defender chooses Double or No double. The choice is announced.

CONTRACTS.
- Wenz: trumps are the four Unters only, ranked Acorns Unter > Leaves Unter > Hearts Unter > Bells Unter. In every suit the non-trump cards rank Ace > Ten > King > Ober > Nine.
- Suit Solo (Acorns, Leaves, Hearts or Bells as named): there are 12 trumps, ranked from high to low:
  - the four Obers (Acorns > Leaves > Hearts > Bells);
  - then the four Unters (Acorns > Leaves > Hearts > Bells);
  - then the Ace, Ten, King and Nine of the named suit.
  In the other three suits the non-trump cards rank Ace > Ten > King > Nine.
- Ramsch: trumps and ranks exactly as in Wenz.

TRICKS (every round).
1) The leader plays any card from their hand. In the first trick of a hand the leader is the declarer, or the priority player in Ramsch. Afterwards the leader is the winner of the previous trick.
2) The other player then plays a card. If a trump was led they must play a trump if they have one; if a plain suit was led they must play a non-trump card of that suit if they have one. Otherwise they may play any card.
3) The trick is won by the highest trump in it; if it has no trump, by the higher card of the led suit.
4) The trick winner adds the card points of both cards to their card-point total for the hand, and leads next.
5) The two cards, the trick winner and both players' card-point totals for the hand are announced.

END OF EACH HAND (after the 8th trick). Let D be the declarer's card points and F the defender's.
- Simple contract is made if D >= F + 10. Strong contract is made if D >= 2 x F and D >= 30.
- Stake: Simple 2 match points, Strong 4 match points; doubled if the defender chose Double (Simple 4, Strong 8).
- If made, the declarer gains the stake; otherwise the defender gains the stake.
- Ramsch: the player with fewer card points gains 1 match point; if equal, nobody scores.
- Card-point totals reset to 0 and the next hand begins.

END. After hand 4 the match ends. Winner: After the fourth hand, the player with more match points wins. Equal match points is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Officers' Schafkopf is a two-player trick-taking form of Schafkopf. Each player has rows of face-down cards topped by face-up cards. The non-dealer announces a Suit Solo or Wenz contract, the dealer may double, and the declarer needs 61 of the 120 card points to win.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy dominates. Always declaring loses on weak hands. Always playing the highest card wastes points against trumps. The choice of contract and the double both change the outcome. The original gives the non-dealer the contract choice, but alternating the deal balances this over a match."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Card play rewards counting trumps and points, managing which hidden card gets uncovered, and choosing the contract. A strong player reliably beats a random one over several deals, though a single deal carries a lot of card luck."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Contract evaluation, the decision to double, and trick-by-trick play under partial information all leave room to improve. A weak player still takes points and sometimes makes contracts."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Up to half the cards are face up, and the down cards surface during play, so much of the game is perfect information late in a hand. Inference is mostly about the face-down cards. This is real but limited."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card points are summed, and 61 or more wins for the declarer. This is pure arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The rows of down cards topped by up cards, which turn face up when uncovered, are a positional layout. The engine would have to track per-stack state for 16 positions, which is beyond the attribute and step limits. The rules are also ambiguous: '32 cards minus Sixes' and an optional dealing method. A single hand is a single result with no match structure."
    }
  ],
  "problems": [
    "The face-up/face-down stack layout needs positional tracking of 16 stacks, which exceeds the attribute and step limits and behaves like a small board.",
    "With many face-up cards there is little hidden information to reason about once play is under way.",
    "A single hand is largely decided by the deal, so luck dominates one game.",
    "The ordered announce-then-double sequence gives the non-dealer a fixed seat edge within a hand.",
    "The previous variation's bid step said 'one of nine options' but listed eleven, so the legal option list for the simultaneous poll was ambiguous."
  ],
  "changes": [
    {
      "what": "Replace the stacks with 8-card concealed hands. The remaining 8 cards become an unseen Blind that is never played.",
      "why": "This removes positional state and creates genuine hidden information. No one knows which 8 cards are out of play, so players must infer the opponent's hand from bids and play.",
      "fixes": "The face-up/face-down stack layout needs positional tracking of 16 stacks, which exceeds the attribute and step limits and behaves like a small board."
    },
    {
      "what": "Use a 24-card deck (Ace, Ten, King, Ober, Unter, Nine in four suits; 120 card points) with concealed hands and a Blind.",
      "why": "This keeps the deck clean and makes the unknown cards the core of the reasoning.",
      "fixes": "With many face-up cards there is little hidden information to reason about once play is under way."
    },
    {
      "what": "Play a match of four hands of 8 tricks each (32 rounds), scored in match points with stakes set by contract level and the double.",
      "why": "Several deals average out card luck. The match score creates planning across hands, such as a trailing player taking on Strong contracts.",
      "fixes": "A single hand is largely decided by the deal, so luck dominates one game."
    },
    {
      "what": "Use a simultaneous sealed bid with Strong above Simple above Pass. Priority breaks same-level ties and alternates by hand. The defender keeps the option to double.",
      "why": "This removes the fixed announcer edge and makes each player predict the other's hand strength.",
      "fixes": "The ordered announce-then-double sequence gives the non-dealer a fixed seat edge within a hand."
    },
    {
      "what": "State the bid poll as exactly eleven options and list all eleven explicitly.",
      "why": "The count and the list now agree, so the legal option set is exact.",
      "fixes": "The previous variation's bid step said 'one of nine options' but listed eleven, so the legal option list for the simultaneous poll was ambiguous."
    }
  ],
  "keeps": [
    "Bavarian suits: Acorns, Leaves, Hearts, Bells.",
    "Card values: Ace 11, Ten 10, King 4, Ober 3, Unter 2, Nine 0, totalling 120.",
    "Contracts: Suit Solo with Obers and Unters as top trumps, and Wenz with only Unters as trumps.",
    "The defender's double (Stoß).",
    "Must-follow trick play, with the trick winner leading next.",
    "A two-player declarer-versus-defender contest over card points."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation passed every check except an inconsistent option count in the bid. Fixing that list makes it complete and buildable within the limits."
  },
  "variation": {
    "name": "Blind Officers' Schafkopf",
    "summary": "This is a two-player Schafkopf match of four hands. Each hand deals 8 concealed cards to each player and leaves 8 unseen cards in a Blind. Players sealed-bid a contract (Wenz or a Suit Solo, at Simple or Strong level), the defender may double, and 8 must-follow tricks decide whether the contract is made. Match points over four hands decide the winner.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. There are 24 cards in four suits: Acorns, Leaves, Hearts, Bells. Each suit has Ace (11 card points), Ten (10), King (4), Ober (3), Unter (2) and Nine (0). The deck holds 120 card points.\n\nMATCH. The match is four hands of 8 tricks each, one trick per round: 32 rounds. Both players start with 0 match points. Seat 1 has priority in hands 1 and 3. Seat 2 has priority in hands 2 and 4.\n\nSTART OF EACH HAND (first round of the hand only).\n1) Shuffle and deal 8 cards face down to each player. Each player sees only their own cards. The remaining 8 cards form the Blind. They are never seen by anyone, never played and never scored.\n2) Sealed bid. Both players choose at the same moment exactly one of these eleven options:\n- Pass;\n- Wenz-Simple;\n- Acorns-Simple;\n- Leaves-Simple;\n- Hearts-Simple;\n- Bells-Simple;\n- Wenz-Strong;\n- Acorns-Strong;\n- Leaves-Strong;\n- Hearts-Strong;\n- Bells-Strong.\n3) Resolution. If both players pass, the hand is Ramsch. Otherwise Strong beats Simple, and any bid beats Pass. If both players bid at the same level (both Simple or both Strong), the priority player's bid wins whatever the contracts. The winning bidder is the declarer and the other player is the defender. The contract and level are those of the winning bid.\n4) Both bids and the resulting contract (or Ramsch) are announced to both players.\n5) Double. If the hand is not Ramsch, the defender chooses Double or No double. The choice is announced.\n\nCONTRACTS.\n- Wenz: the trumps are the four Unters only, ranked Acorns Unter > Leaves Unter > Hearts Unter > Bells Unter. In every suit the non-trump cards rank Ace > Ten > King > Ober > Nine. Unters belong to no plain suit.\n- Suit Solo (Acorns, Leaves, Hearts or Bells, as named): there are 12 trumps, ranked from high to low:\n  - the four Obers (Acorns > Leaves > Hearts > Bells);\n  - then the four Unters (Acorns > Leaves > Hearts > Bells);\n  - then the Ace, Ten, King and Nine of the named suit.\n  Obers and Unters belong to no plain suit. In the other three suits the non-trump cards rank Ace > Ten > King > Nine.\n- Ramsch: trumps and ranks exactly as in Wenz.\n\nTRICKS (every round).\n1) The leader plays any card from their hand. In the first trick of a hand the leader is the declarer, or the priority player in Ramsch. Afterwards the leader is the winner of the previous trick.\n2) The other player then plays a card. If a trump was led, they must play a trump if they have one. If a plain suit was led, they must play a non-trump card of that suit if they have one. Otherwise they may play any card.\n3) The trick is won by the highest trump in it. If it has no trump, it is won by the higher card of the led suit.\n4) The trick winner adds the card points of both cards to their card-point total for the hand, and leads next.\n5) The two cards, the trick winner and both players' card-point totals for the hand are announced.\n\nEND OF EACH HAND (after the 8th trick). Let D be the declarer's card points and F the defender's card points.\n- A Simple contract is made if D >= F + 10.\n- A Strong contract is made if D >= 2 x F and D >= 30.\n- Stake: Simple is 2 match points and Strong is 4 match points. The stake is doubled if the defender chose Double (Simple 4, Strong 8).\n- If the contract is made, the declarer gains the stake. Otherwise the defender gains the stake.\n- Ramsch: the player with fewer card points gains 1 match point. If the card points are equal, nobody scores.\n- Card-point totals reset to 0 and the next hand begins.\n\nEND. After the fourth hand the match ends.",
    "objective": "After the fourth hand, the player with more match points wins. Equal match points is a draw.",
    "expected_effect": "The Blind hides 8 cards, so players must infer the opponent's holdings from the sealed bid, the double and the cards played, rather than read them off the table.\n\nThe sealed bid with alternating priority makes bidding a prediction of the opponent's strength. Overbidding Strong on a mediocre hand loses to a double.\n\nAcross four hands, the match score drives risk. A trailing player must declare Strong or double aggressively, and a leader can pass safely into Ramsch.\n\nNo simple policy is safe:\n- Always Pass loses whenever the opponent declares and makes a contract.\n- Always Strong fails its contracts on weak hands and gets doubled.\n- Always Double pays out double whenever the declarer makes the contract.\n\nCard luck is reduced by four deals and by playing skill. With two players no talk phase is used."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 18,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 32
  }
}
```
````
