# Variation: Hanabi Trio

A 3-colour, 30-card cooperative Hanabi for 2 to 4 players. Each player sees everyone's cards except their own and the team must build Red, Green and Blue piles from 1 to 5 using hints, discards and plays. The team wins if it scores at least 10 of 15 before running out of fuses, cards or turns.

Players: 2 to 4, best with 3

## Review of the original

Hanabi is a cooperative card game for 2 to 5 players. Each player holds a hand they cannot see but everyone else can, and the team builds five colour piles from 1 to 5 using limited hint tokens, discards and risky plays. The team's score is the sum of the pile tops.

- **non_degenerate**: good. Every simple policy fails. Always discarding scores 0. Always playing blind burns the 3 fuses within a few turns and usually ends below 5. Always hinting runs out of tokens and then has to fall back on another action. No seat has an edge because all share one score. Which card to hint, play or discard decides the outcome.
- **skill_sensitive**: good. Good teams that make sound inferences reach 20+ of 25. Careless teams lose fuses and discard 5s, and score under 10. The shuffle matters at the margin: a 5 buried at the bottom of the deck, or both copies of a 2 discarded early, can cap the score. Skill dominates over many games.
- **headroom**: good. A weak team still lands some 1s and 2s. Strong play keeps improving through hint efficiency, finesse-style inference and token economy. Even expert human groups do not always reach the maximum score.
- **reasoning_dependent**: good. Your own hand is hidden, so every play rests on inference. You use the hints you received, the cards you can see and what a hint implies about why it was given. Doing this well requires modelling your partners' intentions and planning tokens over many turns.
- **verifiable**: good. Pile heights, fuses and the score are pure arithmetic on recorded plays.
- **fits_platform**: weak. The game is turn-based and text-only, and its hidden hands are supported. However, 50 cards in 5 colours and 60+ turns exceed the 40-round limit. The result is a team score rather than a winner. The previous build also kept card faces in a lookup table separate from the hands, which drifted out of sync.

## Problems

- P1 Length: 50 cards and 5 colours give games of 60+ turns, beyond the 40-round limit and too much state for the builder.
- P2 No winner: the original produces a cooperative score, but the platform decides only who wins.
- P3 Card-face bookkeeping in the previous build: a separate id_faces lookup, built in a different order from the shuffled deck, disagreed with the hands. Discards revealed wrong faces (#12 shown as B2 or R4), and a correct R1 play was judged as a failure, cost a fuse and did not raise the pile.
- P4 Legal options in the previous build were not rebuilt from the active seat's current hand. Seat 2 was offered PLAY/DISCARD #21 while holding #22, #23, #24 and #16. Seat 1 was allowed to discard #11, which it did not hold.
- P5 Turn order and the end-of-deck final round were under-specified, so the build used extra flags such as counter_set_this_turn and was hard to test.
- P6 Attribute budget: the previous design carried redundant state (id_faces, shuffle_keys, id_labels, rank_pool, hint_values, seat_labels, last_move, hand_size), pushing it past 20 attributes.

## Changes

- Use 3 colours (Red, Green, Blue) with the original rank mix: three 1s, two each of 2/3/4 and one 5, giving 30 cards. Allow 2 to 4 players with fixed hand sizes. Cap the game at 40 turns. (fixes: P1 Length): Keeps every game within 40 turns while preserving the rank scarcity that makes discards dangerous.
- Every seat's total always equals team_score. Every seat whose total reaches 10 (of a maximum 15) wins, so the whole team wins together or all lose together. (fixes: P2 No winner): Turns the cooperative score into an arithmetic win condition. 10 is out of reach of thoughtless play but reachable by careful inference.
- Use a single source of truth for card faces. deck_ids and deck_faces are parallel lists, and each seat's hand_ids and hand_faces are parallel lists. Every move takes entries from the same index of both lists and moves them together. There is no separate lookup table. (fixes: P3 Card-face bookkeeping in the previous build): A face can then never disagree with its card. Discard reveals and play judgements always use the true face.
- At the start of every turn, rebuild legal_options for the active seat only, from that seat's current hand_ids. Clear every other seat's options. (fixes: P4 Legal options in the previous build): A seat can only play or discard cards it actually holds.
- Fix turn order explicitly: seat 1 first, then 2, …, num_players, then seat 1 again. Use a single final_turns_left counter, set to num_players + 1 on the turn the last card is drawn and reduced by 1 at the end of every turn, including that one. (fixes: P5 Turn order and the end-of-deck final round): Gives an unambiguous, testable turn order and end of game with no extra flag.
- Remove id_faces, shuffle_keys, id_labels, rank_pool, hint_values, seat_labels, hand_size and last_move. Merge hint and move logging into one action_log. Hand size follows from num_players. The target 10 is a constant in the rules. (fixes: P6 Attribute budget): Brings the state to 19 attributes and removes the stale copies that caused the bugs.

## Kept from the original

- Players hold hands they cannot see but everyone else can.
- There are three action types: give a hint (spend a token and point to every matching card), discard (regain a token) or play (extend a pile or lose a fuse).
- 8 hint tokens and 3 fuses, with a token regained for completing a pile.
- The original rank distribution per colour: three 1s, two 2s, two 3s, two 4s and one 5.
- When the deck runs out, each player gets one final turn.
- The game is fully cooperative and the score is the sum of the pile tops.
- No free talk: information passes only through hints and through what moves imply.

## The variation's rules

R1 Cards. The deck has 30 cards. For each colour Red (R), Green (G) and Blue (B) there are three 1s, two 2s, two 3s, two 4s and one 5. A face is written as colour letter plus rank, e.g. R1, G4, B5.

R2 Shuffle and IDs. At setup the 30 faces are shuffled once into the list deck_faces. The list deck_ids is #1, #2, …, #30 in order, so deck_ids position k and deck_faces position k always belong to the same card. An ID never reveals a face. The front of both lists is the top of the deck. deck_faces is hidden from every player.

R3 Single source of truth. A card's face exists in exactly one place: the faces list paired with the IDs list that currently holds it. That is deck_ids/deck_faces, or a seat's hand_ids/hand_faces, or the discard_pile entry once revealed. Whenever a card moves, its ID and its face are removed from the same index of their two lists and moved together. There is no other record of faces.

R4 Hand sizes. With 2 players each hand has 5 cards and deck_count starts at 20. With 3 players each hand has 4 cards and deck_count starts at 18. With 4 players each hand has 4 cards and deck_count starts at 14.

R5 Dealing. Seat 1 takes the top hand-size cards (ID and face together, in order), then seat 2 takes the next hand-size cards, and so on up to the last seat. Example: with 3 players, seat 1 holds #1-#4, seat 2 #5-#8 and seat 3 #9-#12, and the deck holds #13-#30. deck_count always equals the number of entries in deck_ids.

R6 Visibility. Every player sees every seat's hand_ids. Every player sees every other seat's hand_faces, but never their own. The piles, hint_tokens, fuses, deck_count, discard_pile, action_log, team_score and turns_played are public.

R7 Starting state. pile_red, pile_green and pile_blue start at 0. hint_tokens starts at 8 (maximum 8). fuses starts at 3. team_score starts at 0. discard_pile and action_log start empty. turns_played starts at 0. final_turns_left starts at -1. active_seat starts at 1.

R8 Turn order. One round is one turn by the active seat. Seats act in order 1, 2, …, num_players, then seat 1 again, starting with seat 1. Only the active seat is asked to choose.

R9 Legal options. At the start of each turn, legal_options for the active seat is built from that seat's current hand_ids only. The options are:
- "PLAY #id" for each ID in its hand.
- "DISCARD #id" for each ID in its hand.
- If hint_tokens is at least 1, "HINT s v" for each other seat s and each value v in R, G, B, 1, 2, 3, 4, 5 that matches at least one card in seat s's hand.
Every other seat's legal_options is empty. The active seat chooses exactly one option.

R10 Hint. hint_tokens falls by 1. A line is added to action_log naming the giver, the receiver, the value and every ID in the receiver's hand that matches it, e.g. "turn 4: seat 1 hints seat 2 R = #5, #7". Hints are public and are not otherwise stored. No card moves.

R11 Finding the card. For PLAY or DISCARD of an ID, find that ID's index i in the active seat's hand_ids. The card's face is hand_faces[i]. Remove index i from both hand_ids and hand_faces.

R12 Play succeeds. The play succeeds if the card's rank is exactly 1 more than its colour's pile. That pile becomes the card's rank and team_score rises by 1. If the rank is 5 and hint_tokens is below 8, hint_tokens rises by 1. action_log records "turn t: seat a plays #id = face, success".

R13 Play fails. If the play does not succeed, fuses falls by exactly 1. "#id=face" is added to the end of discard_pile, and action_log records the failure with the face.

R14 Discard. The face is revealed and "#id=face" is added to the end of discard_pile. hint_tokens rises by 1, to at most 8: discarding with 8 tokens leaves 8. action_log records "turn t: seat a discards #id = face".

R15 Drawing. After a PLAY or DISCARD, if deck_ids is not empty, the front entry of deck_ids and the front entry of deck_faces are removed together and added to the end of the active seat's hand_ids and hand_faces. deck_count is set to the length of deck_ids. If this draw made deck_count 0 and final_turns_left is -1, set final_turns_left to num_players + 1. After a HINT, nobody draws.

R16 End of turn. Every seat's total is set to team_score. turns_played rises by 1. If final_turns_left is above 0, it falls by 1. active_seat passes to the next seat (after the last seat, seat 1).

R17 Game end. The game ends at the end of a turn if any of these holds:
- fuses is 0;
- team_score is 15;
- final_turns_left is 0, meaning every player, including the one who drew the last card, has had one more turn after the deck emptied;
- turns_played is 40.

R18 No talk. There is no message phase. Players may communicate only through the moves above.

R19 Result. Every seat whose total is at least 10 wins. Since all totals equal team_score, the team either wins together (team_score 10 or more) or loses together (below 10). Pile progress counts even if the game ended on the third fuse.

Objective: Cooperative target. When the game ends, every seat's total equals team_score, which is pile_red + pile_green + pile_blue (maximum 15). Every seat whose total reaches 10 wins, so all seats win together if team_score ≥ 10. Otherwise no seat wins and the game counts as a loss for the whole team. Pile progress is counted even when the game ended because fuses reached 0.

Expected effect: Each player must infer the face of their own cards from hints, from visible cards, from the discard pile and from why a partner chose that hint over the alternatives. This rewards modelling partners' intentions. Token economy matters: with 8 tokens, single 5s and scarce 2s-4s, careless discards or blind plays cap the score below 10, while careful teams reach 11-15. Simple policies lose. Always discard scores 0. Always play burns 3 fuses fast and typically scores 2-5. Always hint stalls once tokens run out. The target of 10 leaves headroom without being hopeless for a reasonable team. Talk is left out because all players want the same outcome (no conflict) and open talk would simply reveal hands, removing the inference. The fixed card bookkeeping means discards reveal true faces, correct plays raise piles, and only held cards can be played.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
