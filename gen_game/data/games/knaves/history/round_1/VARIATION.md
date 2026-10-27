# Variation: Knaves' Wager

A short three-player Knaves played with a 20-card deck over 6 hands of 6 tricks. Players take tricks, avoid the Jacks and secretly predict their trick count each hand for a bonus.

Players: 3 to 3, best with 3

## Review of the original

Knaves is a three-player trick-taking game with a 52-card deck and a trump suit set by a turned-up card. Each trick taken scores +1, and capturing the four Jacks costs -1, -2, -3 or -4 points. The first player to reach 20 points over several hands wins.

- **non_degenerate**: good. No simple policy is safe. Always playing your highest card wins tricks but also collects the Jacks that others discard, and a Jack trick can be worth -3 overall. Always playing your lowest card gives up tricks. Every card choice changes who takes which trick and who eats which Jack. One seat imbalance exists: the rules never rotate the deal or the first lead, so eldest always leads first.
- **skill_sensitive**: weak. Card play, counting and Jack-dumping are real skills. But with 17-card hands, a hand rich in trumps and aces takes many tricks almost regardless of play, and nothing makes up for a weak deal. Over a few hands to 20, the deal often decides the winner.
- **headroom**: good. There is a lot to improve at: counting trumps, inferring voids from discards, timing when to win or lose a trick, and steering Jacks to the leader. A weak player still takes some tricks and scores.
- **reasoning_dependent**: good. Hands are hidden. Every play leaks information (failing to follow reveals a void), and planning which tricks to win or duck over a whole hand takes inference and opponent modelling.
- **verifiable**: good. The trick winner follows from suit and rank. Scores are trick counts minus fixed Jack penalties, and the target is a plain number.
- **fits_platform**: bad. Hidden hands and sequential plays are supported. But one hand is 17 tricks, and reaching 20 points can take three or more hands, so 50+ rounds against a 40-round limit. A 52-card deck is also a lot of state to track. 'First to 20' can be reached by two players in the same hand, with no tie rule.

## Problems

- Length: 17 tricks per hand, played to 20 points, exceeds the 40-round limit and has an unpredictable length.
- Lottery: hand strength largely decides trick count, and nothing in the scoring rewards playing a weak hand well, so the deal often decides the winner.
- Seat edge: the rules never rotate the deal or the first lead.
- The winner rule is incomplete: two players can pass 20 in the same hand, and there is no tie rule.
- Scale: a 52-card deck with 17-card hands is far more state than needed to keep the game's decisions.

## Changes

- Shrink the deck to 20 cards (A, K, Q, J, 10 in each suit). Deal 6 cards to each player. Turn the 19th card up for trump and leave the 20th face down, out of play. (fixes: Scale: a 52-card deck with 17-card hands is far more state than needed to keep the game's decisions.): This keeps the original's structure of three equal hands, one turned-up trump card and leftover cards out of play, at a size the engine can track. Each hand becomes 6 tricks.
- Play exactly 6 hands (36 tricks, one trick per round). The highest total wins, and a tie for highest is a draw. (fixes: Length: 17 tricks per hand, played to 20 points, exceeds the 40-round limit and has an unpredictable length.): This gives a fixed length inside 40 rounds and a complete winner rule. Endgame unraveling does not apply, because this is not a cooperation game.
- Rotate the dealer every hand. The player left of the dealer (eldest) leads the first trick. Over 6 hands, each player is dealer twice and eldest twice. (fixes: Seat edge: the rules never rotate the deal or the first lead.): This removes any built-in seat advantage.
- Add a secret simultaneous bid at the start of each hand. Each player predicts how many tricks they will take (0 to 6). Bids are revealed before the first lead, and an exact bid earns +4. (fixes: Lottery: hand strength largely decides trick count, and nothing in the scoring rewards playing a weak hand well, so the deal often decides the winner.): A weak hand can now score well by bidding low and ducking accurately, so the deal changes what to do rather than who wins. Revealed bids give opponents a target to read and disrupt: they can force tricks on a player who bid low, or refuse tricks to one who bid high.
- Make each trick worth 2 points and keep the Jack penalties unchanged (spades -1, clubs -2, diamonds -3, hearts -4). (fixes: Lottery: hand strength largely decides trick count, and nothing in the scoring rewards playing a weak hand well, so the deal often decides the winner.): With only 6 tricks per hand, worth 1 each, the -10 of Jack penalties would swamp trick-taking. At 2 points per trick (12 per hand), tricks and Jacks keep roughly the original balance against each other.

## Kept from the original

- Three players, a trick-taking game with must-follow-suit and a trump suit set by a turned-up card
- A leftover card out of play, as in the original's 52nd card
- Tricks score points; the four Jacks carry graded penalties of -1, -2, -3 and -4 by suit
- The central tension of Knaves: wanting tricks while dodging, and dumping, the expensive Jacks
- Scores accumulate over several hands

## The variation's rules

PLAYERS AND DECK. 3 players sit in a fixed order. The deck has 20 cards: A, K, Q, J, 10 in each of spades, clubs, diamonds and hearts. Within a suit, cards rank A (high), K, Q, J, 10 (low).

HANDS AND ROUNDS. The game is 6 hands of 6 tricks each, 36 rounds in all. Each round is one trick. The dealer for hand 1 is player 1. The dealer moves one seat to the left each hand, so each player deals twice. The player to the dealer's left is eldest for that hand.

DEAL (first round of each hand). Shuffle all 20 cards. Deal 6 cards privately to each player; a hand is seen only by its owner. Turn the 19th card face up: its suit is trump for this hand, and the card itself is out of play. The 20th card stays face down and out of play, and is never revealed during the hand.

BID (first round of each hand, after the deal). All players at the same moment secretly choose a whole number from 0 to 6: the number of tricks they predict they will take this hand. All three bids are then revealed to everyone.

TRICK PLAY (every round). The leader plays any card from their hand face up. The eldest leads the first trick of a hand; afterwards, the winner of the previous trick leads. Then the next player to the left plays, then the third. Each must play a card of the led suit if they have one. If they have none, they may play any card, including a trump. The trick is won by the highest trump in it. If it holds no trump, the highest card of the led suit wins. All plays are visible to everyone as they are made.

TRICK SCORING. The trick winner adds 2 to their hand score. They also take penalties for any Jacks in the trick: Jack of spades -1, Jack of clubs -2, Jack of diamonds -3, Jack of hearts -4. The trick's cards, its winner and the running trick counts are announced.

END OF HAND (after the 6th trick). Any player whose tricks taken equal their bid adds 4 to their hand score. Each player's hand score (2 per trick, minus Jack penalties, plus any bid bonus) is added to their total and announced. Hand scores reset to 0, and the dealer rotates.

END OF GAME. After the 6th hand (round 36), the game ends.

Objective: After 6 hands, the player with the highest total wins. If two or three players tie for the highest total, the game is a draw.

Expected effect: Players must judge their hand to bid, then steer the trick count towards that bid while dumping Jacks on rivals and avoiding taking them. Because bids are public, opponents can see who needs or must avoid tricks and act against them: force a trick on a low bidder, or ruff a high bidder's ace. A weak deal can still win through an accurate low bid and careful ducking, so the deal decides what to do more than who wins. The single unseen card keeps card-counting slightly uncertain. Thoughtless policies lose: always-highest overshoots its bid and collects Jacks, always-lowest misses tricks and often its bid, and random play does both. Talk is left out. Its only real conflict use is two players agreeing to gang up on the leader, which turns the result into kingmaking rather than card reasoning. Free talk could also let players reveal hands. The plays themselves already carry the signals worth reading.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
