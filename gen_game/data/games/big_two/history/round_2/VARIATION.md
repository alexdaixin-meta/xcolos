# Variation: Little Two

A 3-player, 30-card Big Two. Each player sheds a hidden 9-card hand by beating the pile with singles, pairs, triples or three-card runs, using triples as bombs. Penalties for cards left are added up over 3 deals, and the lowest total wins.

Players: 3 to 3, best with 3

## Review of the original

Big Two is a climbing card game for 2 to 4 players. Players take turns beating the current play with a higher play of the same shape (singles, pairs, triples, five-card poker hands) or passing, and the first to empty their hand wins the deal; the others are charged for the cards they still hold.

- **non_degenerate**: good. 'Always pass' never sheds cards and takes the largest penalty. 'Always play the lowest legal card' breaks up pairs and spends 2s early, and it loses to players who keep control cards for later. The lead goes to the holder of a fixed low card, so the seat edge is small. Choices matter: when to break a combination, when to spend a 2 or a bomb, and when to pass so you can re-enter later.
- **skill_sensitive**: weak. Over many deals a stronger player wins clearly. In a single deal, though, a hand full of 2s and five-card hands usually wins whatever the opponents do, so one deal is noisy.
- **headroom**: good. Card counting, inferring hands from passes, choosing a lead order and timing control cards all keep rewarding skill. A beginner still sheds cards and scores something.
- **reasoning_dependent**: good. Hands are hidden. A pass reveals that a player cannot or will not beat the pile. Planning the order in which to shed a hand takes several turns of foresight.
- **verifiable**: good. The deal winner is whoever empties their hand first, and penalties are counted cards. All of it is arithmetic.
- **fits_platform**: weak. The game is turn-based and text-only, but the full version does not fit. Hands of 13 to 17 cards with five-card poker combinations produce option lists in the hundreds, recognising poker hands needs many steps, and a 52-card deal is long. It has to be shrunk, and the previous build showed that a multi-card play must be parsed card by card.

## Problems

- A 52-card deck with five-card poker hands generates too many options, and classifying the hands needs too many steps for the engine.
- Earlier build defect: a multi-card answer such as '13 14' was applied as its first card only. The play then removed one card, set the wrong pile kind and value, and stored only the first token as last_action.
- Earlier build defect: the rules did not pin down legality per pile kind precisely enough. Lower or mismatched plays were offered, and pairs and triples were not checked with the rank formula.
- A single deal is luck-heavy, and the gambling-style penalty doublings are loosely specified.
- The leader is set by who holds a fixed low card. Over few deals this gives a random seat edge.
- The turn order around a pile clearance was not spelled out step by step, so the engine could mis-sequence who leads.

## Changes

- Use a 30-card deck: cards numbered 1 to 30, 10 ranks by 3 suits. Rank = floor((c+2)/3) and suit = c - 3*(rank-1). Rank 10 plays the role of the 2. Deal 9 cards to each of 3 players and set 3 cards aside face down. (fixes: A 52-card deck with five-card poker hands generates too many options, and classifying the hands needs too many steps for the engine.): This keeps hidden hands and card counting. The 3 unseen aside cards mean no one can deduce the remaining hands with certainty, and option lists stay small.
- Allow only four play kinds: single, pair (2 cards of the same rank), triple (3 cards of the same rank) and run (3 cards of three consecutive ranks). The play's value is its highest card number. A triple played on a single or a pair is a bomb. (fixes: A 52-card deck with five-card poker hands generates too many options, and classifying the hands needs too many steps for the engine.): This keeps Big Two's climbing-with-combinations feel, including dilemmas about breaking a pair to make a run, while staying cheap to enumerate.
- Add an explicit play-application procedure. Split the chosen option on spaces into all its card numbers, remove every one of them from the hand, lower card_count by that number of cards, and set pile_kind from the count and ranks. Set pile_value to the highest number, last_player to the seat, and last_action to the whole option string. (fixes: Earlier build defect: a multi-card answer such as '13 14' was applied as its first card only. The play then removed one card, set the wrong pile kind and value, and stored only the first token as last_action.): This removes the first-token bug, so a two- or three-card play removes all its cards.
- Add an explicit legality table and offer format. Options are written as card numbers in ascending order separated by single spaces. Pairs and triples are checked by equal rank under the formula. Each pile kind admits only the listed responses, and nothing else is ever offered or accepted. (fixes: Earlier build defect: the rules did not pin down legality per pile kind precisely enough. Lower or mismatched plays were offered, and pairs and triples were not checked with the rank formula.): This makes the offered list exactly the legal moves, which is what tests R1, R5, R6 and R7 check.
- Play 3 deals and add up penalties. The penalty is the number of cards left, doubled when 7 or more are left, plus 1 for each rank-10 card still held. The lowest total wins. (fixes: A single deal is luck-heavy, and the gambling-style penalty doublings are loosely specified.): Several deals average out the luck of one hand. The 2s penalty preserves the original's 'don't sit on your twos' tension, and the scoring is precise arithmetic.
- Rotate the leader: seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3. (fixes: The leader is set by who holds a fixed low card. Over few deals this gives a random seat edge.): Every seat leads exactly once, so no seat has a built-in edge.
- Define the sequencing exactly. Each orbit, seats act in the order 1, 2, 3. In a deal's first orbit, seats before the leader skip their turn. When it is the turn of the seat that made the last play, the pile is first cleared and that seat leads. (fixes: The turn order around a pile clearance was not spelled out step by step, so the engine could mis-sequence who leads.): Cycling in seat order makes the last player lead naturally after the others pass. This matches test R3.

## Kept from the original

- The climbing mechanic: beat the pile with the same kind at a higher value, or pass.
- Passing does not lock you out; you may re-enter later in the same battle.
- The highest rank plays the role of the 2, and suits break ties.
- Bombs: a triple beats a single or a pair.
- When everyone else passes, the pile clears and the last player to play leads anything.
- The first player to empty their hand wins the deal, and the others are penalised for cards held, with extra penalties for many cards and for unplayed 2s.

## The variation's rules

CARDS. There are 30 cards, numbered 1 to 30. A card c has rank = floor((c+2)/3), from 1 to 10, and suit = c - 3*(rank-1), from 1 to 3. Rank 1 is lowest and rank 10 (cards 28, 29, 30) is highest and plays the role of the 2. Within a rank, a higher suit is a higher card, so a higher card number is always a higher card. Examples: card 13 has rank 5, suit 1; card 14 has rank 5, suit 2; card 16 has rank 6, suit 1.

PLAY KINDS. A play is 1 to 3 cards from your own hand, written as their numbers in ascending order separated by single spaces (for example '13 14').
- Single: 1 card.
- Pair: 2 cards of the same rank. '13 14' is a pair; '14 16' is not.
- Triple: 3 cards of the same rank.
- Run: 3 cards whose ranks are three consecutive numbers (for example ranks 4, 5, 6), in any suits. Ranks do not wrap around.
Any other set of cards is not a play. The value of a play is its highest card number.

SETUP. There are 3 players in seats 1, 2 and 3. Each player has a private hand, a public card_count, a public penalty (starting at 0), public deals_won (starting at 0) and a public last_action (starting as 'no play yet'). The table tracks deal_number (starting at 0), orbit (starting at 0), deal_active (starting false), leader_seat, first_orbit, pile_kind ('empty', 'single', 'pair', 'triple' or 'run'), pile_value and last_player (0 means nobody). The game lasts at most 40 orbits and at most 3 deals.

EACH ORBIT (one engine round):
1. Add 1 to orbit.
2. If deal_active is false and deal_number is less than 3, start a deal. Add 1 to deal_number. Shuffle all 30 cards. Deal 9 into each player's private hand and put the remaining 3 into a hidden aside list that nobody sees. Set every card_count to 9. Set leader_seat to deal_number, so seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3. Set deal_active to true, first_orbit to true, pile_kind to 'empty', pile_value to 0 and last_player to the leader. This is the only random event in an orbit.
3. Seats then take turns in the order seat 1, seat 2, seat 3. A seat skips its turn if deal_active is false, or if first_orbit is true and its seat number is lower than leader_seat. On each turn that is not skipped:
  a. Clearance. If last_player equals this seat, the other two have passed since this seat's last play (or the deal has just started). Set pile_kind to 'empty' and pile_value to 0. This seat now leads.
  b. Options. The seat is offered exactly the following, and nothing else:
     - If pile_kind is 'empty': every single, pair, triple and run that can be made from its hand. Passing is not allowed.
     - If pile_kind is 'single': 'pass', every single with value greater than pile_value, and every triple of any value (a bomb).
     - If pile_kind is 'pair': 'pass', every pair with value greater than pile_value, and every triple of any value (a bomb).
     - If pile_kind is 'triple': 'pass' and every triple with value greater than pile_value.
     - If pile_kind is 'run': 'pass' and every run with value greater than pile_value.
  c. The seat chooses one option. Everyone sees the choice.
  d. Apply the choice. If it is 'pass', set this seat's last_action to 'pass' and change nothing else. Otherwise:
     - Split the option on spaces into all of its card numbers.
     - Remove every one of those cards from the hand.
     - Lower card_count by the number of cards played (1, 2 or 3).
     - Set pile_kind: 1 card is 'single'; 2 cards are 'pair'; 3 cards of one rank are 'triple'; 3 cards of consecutive ranks are 'run'.
     - Set pile_value to the highest card number played.
     - Set last_player to this seat.
     - Set last_action to the full option string.
     A triple that bombs a single or a pair makes pile_kind 'triple', so only a higher triple can follow it.
  e. If this seat's card_count is now 0, it wins the deal. Add 1 to its deals_won. Every other seat with n cards left adds a penalty of n, doubled to 2n if n is 7 or more, plus 1 for each card numbered 28, 29 or 30 still in its hand. Set deal_active to false. The rest of this orbit's turns are skipped.
4. At the end of the orbit, set first_orbit to false.

END. The game ends when deal 3 has ended, or when orbit 40 is complete. If orbit 40 ends while a deal is still active, every seat is penalised for the cards it holds, by the same formula. Deals that never started are not played.

There is no talk phase. All plays and passes are public, and hands and the aside cards stay hidden.

Objective: The player with the lowest total penalty wins. If two or three players tie for lowest, the one among them with the most deals_won wins. If they are still tied, the game is a draw.

Expected effect: Each seat leads exactly one deal, so seats are balanced. Three deals of summed penalties cut the luck of a single hand while keeping the original's tension over cards left and unplayed 2s. Good play means:
- counting which high cards and ranks are gone, remembering that 3 cards are unseen;
- reading passes as signs of weakness;
- deciding when to break a pair or triple to make a run;
- holding a bomb or a rank-10 card to regain the lead;
- leading low combinations to shed while keeping control.
Always passing is impossible when leading and costs heavy penalties otherwise. Always playing the lowest legal card wastes bombs and gets stuck holding 2s, so it loses to careful players. With three players and a single winner, there is no total-difference trap. Talk is left out: it would only carry unverifiable claims about hands or kingmaking pacts, and would not add a real choice. The exact parsing and legality rules make tests R1 (the '13 14' pair removes 2 cards), R5, R6 and R7 hold.

## Complexity (the designer's count, against the limits)

- steps_per_round: 19 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
