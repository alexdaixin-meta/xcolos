# Variation: Nyet! Trio (Widow edition, compact)

Three players play 6 deals. At the start of each deal they veto options on a two-line board to fix the trump colour and who plays Lone. The Lone takes the Widow and plays 5 tricks against the other two as a Pair. A Lone trick is worth 2 points to the Lone, and a Pair trick is worth 1 point to each Pair member.

Players: 3 to 3, best with 3

## Review of the original

Nyet! is a trick-taking game for 2 to 5 players. Before each hand, players take turns placing veto ('Nyet') tokens on a board of rule options until one option per line survives: first player, discard rule, trump, supertrump and points per trick. Shifting teams then play tricks, scoring tricks plus Loot, and the most total points after 8-10 rounds wins.

- **non_degenerate**: good. No fixed policy wins. Always vetoing the first box or always playing the lowest legal card loses to players who shape trump and the teams to suit their hand. Seat effects in the veto order are real but rotate. In the previous Trio variation one flaw stood out: almost every token went to the LONE line, so trump defaulted to Red and the trump veto was nearly dead.
- **skill_sensitive**: good. Hand strength varies per deal. Over many deals, players gain by reading partners' and opponents' holdings, vetoing trump against weak suits, and choosing when to stand alone. Trick play rewards counting cards and inferring voids. Luck in single deals averages out over 6 or more deals.
- **headroom**: good. Valuing a hand under each possible trump, predicting how others will veto, bluffing in talk, and card-counting with a hidden set-aside pile all leave room to improve. A weak player still wins tricks with good cards.
- **reasoning_dependent**: good. Hands are hidden, and some cards are never revealed. Every veto token signals something about a hand. Players must infer suit lengths from vetoes and from failures to follow suit, and plan across a 5-trick hand.
- **verifiable**: good. Trick winners and scores follow mechanically from the cards played and the surviving rules.
- **fits_platform**: weak. The full game has a 5-line board, multi-player team selection, a Bonus card, supertrump 1s beating trump, Loot and a 60-card deck. That is far beyond the step and attribute limits. The previous cut-down version still exceeded choice steps (8 of 4) and attributes (about 24 of 20).

## Problems

- P1: Too many choice steps. In the flat step list, veto choices (talk plus 3 tokens) and trick choices (Lone discard plus 3 card plays) add up to 8 distinct choice steps against a limit of 4.
- P2: Too many attributes. Four stats per player, 7 separate board boxes and 5 state values come to about 24 against a limit of 20, and the earlier design under-reported this.
- P3: Weak trump veto. Players spent their single token on the LONE line, so trump almost always stayed Red, the first box, and the trump line added little to decide.
- P4: The original's full rule set (supertrump, Loot, Bonus card, team picking, 5 board lines, 60 cards) cannot be built within the limits.

## Changes

- Remove the separate Lone discard choice. The Lone keeps all 6 cards (5 dealt plus the Widow) and plays one per trick. The single card left unplayed after the 5th trick is the hidden discard and is never shown. (fixes: P1: Too many choice steps): This removes a whole choice step but keeps the decision: the Lone still chooses which card to keep back.
- Use three shared sequential choice slots for both veto tokens and card plays. Slot A is First in a veto round and the leader in a trick round. Slots B and C are the next players clockwise. Each slot's options are computed: legal empty boxes in veto rounds, legal cards in hand in trick rounds. Talk runs only in veto rounds. (fixes: P1: Too many choice steps): Talk plus 3 shared slots gives exactly 4 choice steps across the whole flat list.
- Store the Nyet board as one list attribute. Store the current trick as one list, so the led colour comes from its first card. Drop the 'tricks' stat and break ties on score, then lone_tricks, then last_win. Set-aside cards are one list. The Lone's unplayed card simply stays in their hand, so hidden elements fall to 2. (fixes: P2: Too many attributes): This brings attributes to 19 and states the count honestly. The tiebreak still almost always produces a unique winner.
- Allow at most one token on the LONE line per veto round. Rotate the order of the TRUMP line each deal, so the default trump changes. (fixes: P3: Weak trump veto): At least two of the three tokens must now go to the TRUMP line, so trump is genuinely contested. The single LONE token becomes a race that means something different by seat. First tokening 'First' declines to be Lone. Second tokening 'First' claims Lone. Third tokening 'First' forces Second to be Lone. Rotating the trump order stops one colour from being the standing default.
- Keep the reduced core: 3 players, a 24-card deck, a two-line Nyet board, 1 Lone against a Pair, a Widow, and trump-only trick rules. (fixes: P4: Full rule set cannot be built): This is the smallest version that keeps veto-to-set-the-rules, shifting teams and trick play, within the limits.

## Kept from the original

- The Nyet mechanic: players set the round's rules by vetoing options, and the leftover option becomes the rule.
- The trump colour is chosen by elimination.
- Teams shift every hand: one player stands alone against a temporary partnership, with an uneven reward for tricks.
- Standard trick taking: follow the led colour if able, and trump beats the led colour.
- Many hands, scored by cumulative points, with the highest total winning.

## The variation's rules

SETUP
- There are exactly 3 players: P1, P2, P3. Clockwise order is P1 -> P2 -> P3 -> P1.
- The deck has 24 unique cards: four colours (Red, Yellow, Green, Blue), each numbered 1 to 6.
- Each player has score, lone_tricks and last_win, all starting at 0.
- The game lasts 36 rounds: 6 deals of 6 rounds each. Round 1 of each deal (rounds 1, 7, 13, 19, 25, 31) is the VETO round. Rounds 2 to 6 of each deal are TRICK rounds.

VETO ORDER (First, Second, Third)
- Deals 1 and 4: P1, P2, P3.
- Deals 2 and 5: P2, P3, P1.
- Deals 3 and 6: P3, P1, P2.

TRUMP LINE ORDER (rotates each deal)
- Deal 1: Red, Yellow, Green, Blue.
- Deal 2: Yellow, Green, Blue, Red.
- Deal 3: Green, Blue, Red, Yellow.
- Deal 4: Blue, Red, Yellow, Green.
- Deal 5: Red, Yellow, Green, Blue.
- Deal 6: Yellow, Green, Blue, Red.

VETO ROUND
(1) Shuffle all 24 cards. Deal 5 to each player as a private hand. Turn one of the remaining 9 face up: this is the Widow, which everyone sees. The other 8 are set aside face down and are never revealed. Any cards left in hands from the previous deal are discarded unseen before the shuffle.
(2) The Nyet board is cleared. It has two lines: the TRUMP line (4 colour boxes, in this deal's order) and the LONE line (3 boxes: First, Second, Third). Announce the Widow and the board.
(3) Talk: all three players write one short message at the same time, without seeing the others' messages. All messages are then shown to everyone. Talk is not binding.
(4) First, then Second, then Third each places one Nyet token on one empty box. Each sees the tokens already placed. A token may go on any empty TRUMP box. A token may go on a LONE box only if no token is yet on the LONE line: at most one LONE token per deal. A player may not token the last empty box of a line. There is always at least one legal box.
(5) Trump is the first untokened box on the TRUMP line, in this deal's order. The Lone is the first untokened box on the LONE line (First, then Second, then Third). The other two players are the Pair.
(6) The Lone adds the Widow to their hand and holds 6 cards. Announce trump, the Lone and the Pair. The Lone leads the first trick.

TRICK ROUND
(7) The leader plays one card face up. Then the next player clockwise plays one, then the third player plays one. Each sees the cards already played. The led colour is the colour of the leader's card. A player holding a card of the led colour must play one. A player with none may play any card.
(8) Winner: if any trump was played, the highest trump wins. Otherwise the highest card of the led colour wins. Cards are unique, so there is always one winner.
(9) Scoring: if the Lone won, the Lone gains 2 points and 1 lone_trick. If a Pair member won, each Pair member gains 1 point. The winner's last_win is set to the current round number.
(10) The winner leads the next trick of this deal.
(11) Announce the cards played, the winner and all scores.
- After the 5th trick of a deal, the Lone still holds 1 card. It is never played or revealed and is discarded at the next shuffle. Choosing which card to keep back is the Lone's discard.

END
After round 36, the winner is decided as in the objective.

Objective: The highest score wins. If players tie, the tied player with the most lone_tricks wins. If still tied, the tied player with the highest last_win wins (the one who won a trick most recently; this is unique unless no tied player has won a trick). If still tied, the game is a draw.

Expected effect: Playing Lone pays more than playing in the Pair only when the Lone wins 2 or more of the 5 tricks: 2k against 5-k for each Pair member. Every deal is therefore a judgement of hand strength under each possible trump. Because only one LONE token is allowed, at least two tokens fall on the TRUMP line, so trump is genuinely contested. Each token also signals which colours a player is short in. The single LONE token is a race with a different meaning by seat (decline, claim or force), and the rotations remove seat and default-colour edges. Talk passes both tests. Players disagree about trump, since each wants their own long suit, and about who should be Lone, since each wants to be Lone only with a strong hand and wants a weak rival forced into it. A player who simply follows a proposal such as 'I'll token Red, you token First' can be steered into a bad trump or a losing Lone. The Pair cooperates only temporarily, and each Pair member is still a rival on the overall score, so Pair play involves real tension. No endgame unravelling arises, because this is a competitive trick game rather than a cooperation game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
