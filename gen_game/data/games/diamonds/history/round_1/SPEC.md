# Diamonds: Three-Hand Vault

A three-player trick-taking game over 3 hands of 10 tricks. Each suit's action moves crystals into your showroom (1 point each) or your vault (2 points each), or steals from an opponent's showroom.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 36
- `suits` = 4
- `ranks_per_suit` = 9
- `lowest_rank` = 1
- `highest_rank` = 9
- `cards_dealt_per_player` = 10
- `cards_set_aside` = 6
- `cards_passed` = 2
- `hands` = 3
- `tricks_per_hand` = 10
- `total_rounds` = 30
- `cards_per_trick` = 3
- `crystals_per_action` = 1
- `vault_crystal_points` = 2
- `showroom_crystal_points` = 1
- `zero_trick_diamond_actions` = 2
- `dealer_hand_1_seat` = 3
- `dealer_hand_2_seat` = 1
- `dealer_hand_3_seat` = 2
- `rank_tiebreak_multiplier` = 100

## Round

1. **update** (all players): Start of a hand. Set hand_number = (round_number - 1) / 10 + 1. Set dealer = 3, 1 or 2 for hand 1, 2 or 3. Set leader = (dealer mod 3) + 1. Gather all 36 cards into deck and clear every hand, pass_cards and set_aside. Deal 10 cards at random from deck into each player's hand, then move the remaining 6 into set_aside. Reset won_diamonds, won_hearts, won_spades, won_clubs and tricks_won to 0 for every player.
2. **sync** (all players): Each player privately sees their own hand.
3. **poll** (all players): Append the chosen card to pass_cards (first pass card).
4. **poll** (all players): Append the chosen card to pass_cards (second pass card).
5. **update** (all players): Remove each player's pass_cards from their hand and append them to the hand of the player on their left. Clear pass_cards. Nothing is announced about which cards moved.
6. **sync** (all players): Each player privately sees their new hand.
7. **ask** (seat game.leader): Remove the card from the leader's hand. Set the leader's played_card, played_suit and played_rank. Set led_suit = played_suit.
8. **ask** (seat game.leader): Set the leader's clubs_target to the named seat. Announce the leader's card and target.
9. **ask** (seat (game.leader mod 3) + 1): Remove the card from hand. Set played_card, played_suit and played_rank.
10. **ask** (seat (game.leader mod 3) + 1): Set clubs_target. Announce the card and the target.
11. **update** (seat (game.leader mod 3) + 1): Off-suit action for this player, by played_suit. D: vault +1. H: showroom +1. S: if showroom > 0 then showroom -1 and vault +1. C: if the clubs_target's showroom > 0 then the target's showroom -1 and own showroom +1. Recompute score for affected players and announce the action.
12. **ask** (seat ((game.leader + 1) mod 3) + 1): Remove the card from hand. Set played_card, played_suit and played_rank.
13. **ask** (seat ((game.leader + 1) mod 3) + 1): Set clubs_target. Announce the card and the target.
14. **update** (seat ((game.leader + 1) mod 3) + 1): Off-suit action, the same as for the second player: D vault +1; H showroom +1; S if showroom > 0 move 1 from showroom to vault; C if the clubs_target's showroom > 0 move 1 from it to own showroom. Recompute score and announce.
15. **update** (all players): trick_winner = the seat with the highest played_rank among players whose played_suit == led_suit. The winner adds the 3 played cards to won_diamonds, won_hearts, won_spades and won_clubs by each card's suit, and tricks_won +1. The winner then takes the led_suit action using the winner's own clubs_target: D vault +1; H showroom +1; S if showroom > 0 move 1 from showroom to vault; C if the clubs_target's showroom > 0 move 1 from it to the winner's showroom. Set leader = trick_winner. Recompute every score.
16. **tell** (all players): Announce the three cards, the Clubs targets, the trick winner, every action taken, and every player's showroom, vault and won counts.
17. **update** (all players): End of hand, applied in order. (1) Diamonds: if one player has strictly the most won_diamonds, that player's vault +1. (2) Hearts: if one player has strictly the most won_hearts, that player's showroom +1. (3) Spades: if one player has strictly the most won_spades and their showroom > 0, that player moves 1 from showroom to vault. (4) Clubs: if one player has strictly the most won_clubs, they take 1 from the showroom of the opponent with the largest showroom; if those two opponents are tied, the opponent on the receiver's left is robbed; nothing moves if that showroom is 0. (5) Each player with tricks_won == 0 gets vault +2. Recompute every score.
18. **tell** (all players): Announce the end-of-hand actions, the 6 cards in set_aside (revealed), and every score.
19. **check** (all players): If round_number == 30, end the game. Otherwise round_number +1 and clear every played_card, played_suit, played_rank, clubs_target and led_suit.

## Ending

- ends when: round_number == 30 after the end-of-hand step of hand 3
- ranked by: `you.score * 100 + you.vault` (the highest wins; players level at the top share the win)
- decided by: Highest score (2 x vault + showroom) wins. On a score tie, more vault crystals wins. Players still level share the win, which is the source's draw.

## Choices the source did not make

- 3 players exactly (suggested 3): The designer fixed 3 seats. The dealer rotation, 'left', the 36-card deal (3 x 10 + 6) and the end-of-hand Clubs tie rule all assume 3 players.
- No talk step: The source has no table talk, and adding it would add a mechanic. Strategy lives in passing, suit play, off-suit timing and Clubs targeting: hold Hearts to build a showroom, use Spades to bank it, and point Clubs at the leader.
- Card codes such as D7 and seat numbers A=1, B=2, C=3: Gives arithmetic a concrete suit letter and rank to compare.
- The pass is two simultaneous polls of one card each: A question returns one choice; two polls keep the pass secret and simultaneous.
- Every player names a Clubs target with every card, even when Clubs cannot apply: The source says every player names one; it is used only if a Clubs action fires.
- Ranking expression score*100 + vault: Vault stays well below 100, so this ranks by score first and vault second, and remaining ties share the win (the draw).
- End-of-hand suit actions are applied one after another, each seeing the previous result: The source says 'for each suit in turn', so a Hearts crystal can be banked by a following Spades action.

## Simplifications

- The crystal supply is not tracked: The source says it is unlimited.
- Each player's turn is split into two asks: card, then Clubs target: A question returns a single choice.
- Follow-suit is enforced by restricting the offered cards: Options are filtered from the hand list by led_suit instead of checking after the play.

## Unsupported (needs engine work)

- none
