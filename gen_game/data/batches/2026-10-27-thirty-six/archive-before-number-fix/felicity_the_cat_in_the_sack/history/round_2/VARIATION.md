# Variation: Cat in the Sack: Two-Stage Auction

Each round every player secretly adds a card to a sack ordered from the start player. After one simultaneous message, players bid in two sealed simultaneous stages as the first two sack cards are revealed. Drop-outs collect consolation mice, the buyer pays and takes the sack's cats after the dog rule, and after 9 rounds the highest cats plus mice wins.

Players: 3 to 5, best with 4

## Review of the original

Felicity the Cat in the Sack is a 3-5 player bluffing auction game. Each round every player secretly adds one card (a cat worth -8 to 15, a rabbit, or a dog) to a shared 'sack', and the cards are revealed one by one while players bid mice or drop out for an escalating consolation payment. The buyer gets the sack's cat points after dog effects, and the most cat points plus leftover mice wins.

- **non_degenerate**: good. Always passing collects only small consolation mice and loses to a player who buys good sacks cheaply. Always bidding high overpays for sacks seeded with -8 and -5 cats. Starting first gives some tempo, but the start seat moves to each round's winner.
- **skill_sensitive**: good. Every player plays all of their cards over 9 rounds, so the luck is limited to one random card set aside per hand. What separates players is which card to contribute when, and reading other players' bids as information about their hidden contributions.
- **headroom**: good. Beginners can score by passing and buying the occasional obvious sack. Strong players track which cards each opponent has used, time their dogs and negative cats, and bluff by bidding up a sack that contains their own -8.
- **reasoning_dependent**: good. Each player knows only their own card in the sack, and the cards are revealed gradually. Bids leak information about what others contributed, and hand tracking over 9 rounds rewards planning.
- **verifiable**: good. The score is cat values plus mice, all arithmetic.
- **fits_platform**: weak. The clockwise open-outcry auction with an unbounded number of raises does not fit a flat step list. The previous variation's staged simultaneous auction was built incorrectly: sack_cards was left empty, start_seat was re-randomised, stored bids were overwritten so every sack was treated as all-pass, and stage options were missing. It also needed 5 choice steps (card, talk, 3 bid stages), over the limit of 4.

## Problems

- P1: The open clockwise auction with unlimited raises cannot be built as a flat step list.
- P2: The previous build re-randomised start_seat after setup and left sack_cards empty, so the sack had no cards to value or reveal.
- P3: The previous build overwrote or reset stored bids before resolution, so legal bids were treated as passes and nobody ever won a sack.
- P4: The previous variation used 3 bidding stages plus a card choice and a talk phase, which is 5 choice steps against a limit of 4. Later-stage bid options (for example 3) were never offered.
- P5: The pass and leave rules across stages were complicated (who is out, who gets which reward, what happens when everyone passes). This made the resolution error-prone to build.
- P6: The dog rule's fallback ('lowest negative') was ambiguous.

## Changes

- The auction becomes exactly two simultaneous sealed-bid stages. Stage 1 reveals sack card 1 and lets anyone bid or pass. Stage 2 reveals sack card 2, and the remaining players may raise. The stage-1 leader may also hold, writing 0, to keep their stage-1 bid. The highest effective bid wins. (fixes: P1): This keeps the escalating, information-revealing auction in a fixed number of steps.
- start_seat is drawn once at setup and changes only at the end of a round: to the sack winner, or to the next seat if nobody bought the sack. sack_owners lists the seats in seat order starting from start_seat. sack_cards is filled with each owner's played_card in the same order, immediately after cards are played, and is kept until the round ends. (fixes: P2): The sack must exist, with known owners per position, before revealing and valuing it.
- Each stage writes every submitted number into that player's bid attribute. Legality is checked against the standing_bid in force before the stage, which is 0 at stage 1. Bids are cleared only at the start of the next round. (fixes: P3): Resolution must read the real bids.
- Choices are limited to card, message, stage-1 bid and stage-2 bid, which is 4 choice steps. Every legal value is listed as an option at both stages: stage 1 offers 0 to the player's mice; stage 2 offers 0 and standing_bid+1 to the player's mice. (fixes: P4): This stays inside the choice limit and makes every legal bid choosable.
- Rewards are simplified. Every stage-1 passer gains 2 mice and leaves. Every player still in at stage 2 who does not win gains 3 mice. If everyone passes at stage 1, nobody takes the sack and its cards are discarded. (fixes: P5): Each player is in one of three clear outcomes. This keeps the original's rising consolation payments (2, then 3).
- The dog rule is restated precisely. It applies only if exactly one dog is in the whole sack. The large dog removes the highest positive cat, or the most negative cat if there is no positive one. The small dog removes the most negative cat, or the lowest positive cat if there is no negative one. (fixes: P6): The rule is unambiguous arithmetic.

## Kept from the original

- Identical 10-card hands (cats -8, -5, 3, 5, 8, 11, 15; rabbit; large dog; small dog), with one random card per hand set aside unseen.
- 15 starting mice, 9 rounds, and each player secretly adds one card to a shared sack every round.
- Gradual reveal of sack cards during the auction, so bids are made on partial information.
- Escalating consolation mice for dropping out, and the buyer pays the bank.
- The dog rule that removes one cat, and the winner becomes start player.
- Score is cat points plus remaining mice; ties are broken by cat points.

## The variation's rules

CARDS. Every player starts with the same 10 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15 (cats, worth their number), rabbit (worth 0, not a cat), large_dog and small_dog (worth 0).

R1 SETUP. Remove one random card from each player's hand into the face-down set_aside pile, which nobody sees. Each hand now has 9 cards. Hands are private.

R2 SETUP. Each player has 15 mice and 0 cat_points; both are public. Choose start_seat at random. This is the only time start_seat is randomised. Play 9 rounds.

Each round:

R3 PLAY. At the start of the round, set every player's bid to 0 and in_auction to true, standing_bid to 0, leader_seat to 0, sack_done to false and sack_winner to 0. Every player then simultaneously chooses one card from their hand. It leaves their hand and becomes their played_card, which is private.

R4 SACK. sack_owners lists all seats in seat order, beginning with start_seat and continuing to the next higher seat, wrapping from the last seat to seat 1. sack_cards is the list of each owner's played_card in that same order: one card per seat, so 3 to 5 cards. Everyone knows which seat owns each position, but only the owner knows their own card. sack_cards is kept until the end of the round.

R5 TALK. Every player simultaneously writes one short message without seeing the others. Then all messages are shown with names. Talk is not binding; bluffing is allowed.

R6 STAGE 1. Sack card 1 (the start player's card) is revealed to all and added to sack_revealed. The standing_bid is 0. Every player simultaneously writes a whole number from 0 to their mice; every value in that range is an option. The number is stored as that player's bid. A bid of 0 is a pass, and so is any number above the player's mice.

R7 STAGE 1 RESOLUTION. All bids are announced by name. Each passer gains 2 mice and sets in_auction to false. If no one bid, nobody takes the sack: discard sack_cards, set start_seat to the next seat after start_seat, and the round ends. If exactly one player bid, that player wins the sack at once at their bid (go to R10). Otherwise, standing_bid becomes the highest bid. leader_seat is the player with that bid; ties go to the first tied seat in seat order starting from the seat after start_seat.

R8 STAGE 2. Sack card 2 is revealed to all and added to sack_revealed. Each player still in simultaneously writes a number. The options are 0 and every whole number from standing_bid+1 to their mice, where standing_bid is the value set in R7. The number is stored as that player's bid.
- For the leader, 0 means 'hold': their effective bid stays the standing_bid. A legal number above standing_bid is their new effective bid.
- For any other player, a legal number is their effective bid. 0, or any number at or below standing_bid or above their mice, means they drop out with no effective bid.

R9 STAGE 2 RESOLUTION. All stage-2 numbers are announced by name. The winner is the player with the highest effective bid. If tied, the leader wins if they are among the tied players; otherwise the first tied seat in seat order starting from the seat after start_seat wins. Every other player still in at stage 2 gains 3 mice.

R10 TAKING THE SACK. The winner pays their winning bid in mice to the bank. All sack cards are revealed. Dog rule: if exactly one dog is in the whole sack, it removes one cat.
- The large dog removes the highest positive cat. If there is no positive cat, it removes the most negative cat.
- The small dog removes the most negative cat. If there is no negative cat, it removes the lowest positive cat.
- If there is no cat at all, nothing happens.
- If there are zero or two dogs, nothing is removed.
sack_value is the sum of the remaining cat values; the rabbit and dogs count 0. The winner adds sack_value to cat_points (it may be negative). The winner becomes start_seat. All sack cards are then discarded.

R11 END. After round 9, each player's score is cat_points + mice.

Objective: The highest score (cat_points + mice) wins. If players tie, the one with more cat_points among them wins. If still tied, it is a draw between them.

Expected effect: Players weigh when to dump their -8, -5 and dogs into sacks they expect others to buy, and when to commit their 15 or 11 to a sack they plan to win. Stage-1 bids leak information about each bidder's own contribution, so later bidders must infer whether a high bid means a good hidden card or a bluff. Card counting across 9 rounds rewards planning, since everyone knows the full deck minus one set-aside card per player. Talk earns its place because only one player can win. Players disagree about the sack's value: an owner of a -8 wants others to overpay, and an owner of the 15 wants to buy cheaply. A player who simply believes 'my card is the 15, bid it up' can pay 10 mice for a sack worth -5. Simple policies all lose to competent play. Always passing earns at most 18 extra mice, while buyers of good sacks gain more. Always bidding everything empties the purse on poisoned sacks. Random bidding overpays. The random set-aside card is symmetric and only slightly shifts what can be played, so it does not decide the winner.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 9 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
