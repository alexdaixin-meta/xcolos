# Diamonds: Three-Hand Vault

A three-player trick-taking game over 3 hands of 7 tricks. Winning tricks, and playing off-suit, trigger suit actions that move crystals into your showroom (worth 1 each) and your vault (worth 2 each).

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 32
- `suits` = 4
- `ranks_per_suit` = 8
- `lowest_rank` = 1
- `highest_rank` = 8
- `hands` = 3
- `tricks_per_hand` = 7
- `total_rounds` = 21
- `cards_dealt_per_player` = 7
- `cards_set_aside` = 11
- `cards_passed_per_player` = 1
- `cards_per_trick` = 3
- `crystals_per_action` = 1
- `zero_trick_diamond_actions` = 2
- `vault_weight` = 2
- `showroom_weight` = 1
- `starting_showroom` = 0
- `starting_vault` = 0
- `rank_tiebreak_multiplier` = 1000

## Round

1. **update** (table): When trick_number == 1: deck = all 32 cards; set_aside = []; every player's hand = []; dealer_seat = hand_number; leader_seat = (dealer_seat mod 3) + 1; reset each player's tricks_won, won_diamonds, won_hearts, won_spades and won_clubs to 0. Announce the new hand and its dealer.
2. **initialize** (all players): When trick_number == 1: deal 7 cards to each player, each one a random draw removed from deck and appended to that player's hand. Then move the remaining 11 deck cards to set_aside.
3. **sync** (all players): When trick_number == 1: each player privately sees their own hand, sorted by suit D,H,S,C and then by ascending rank.
4. **poll** (all players): When trick_number == 1: store the answer in pass_card. Nobody sees another player's choice.
5. **update** (all players): When trick_number == 1: at once, for each seat s, remove pass_card from s.hand and append it to the hand of seat (s mod 3) + 1. Each receiver is told privately which card they received; the third player is not told.
6. **sync** (all players): When trick_number == 1: each player sees their updated sorted hand.
7. **update** (table): trick_cards = []; every played_card = ''.
8. **ask** (seat leader_seat): Remove the card from hand; played_card = the card; append it to trick_cards; led_suit = its suit letter. Announce the card to all.
9. **ask** (seat (leader_seat mod 3) + 1): Remove the card from hand; played_card = the card; append it to trick_cards; announce it to all.
10. **update** (seat (leader_seat mod 3) + 1): If that seat's played_card suit != led_suit, the seat takes the action of the played card's suit (see rules R14-R17) at once. Announce the action and its result.
11. **ask** (seat ((leader_seat + 1) mod 3) + 1): Remove the card from hand; played_card = the card; append it to trick_cards; announce it to all.
12. **update** (seat ((leader_seat + 1) mod 3) + 1): If that seat's played_card suit != led_suit, the seat takes the action of the played card's suit at once. Announce the action and its result.
13. **update** (table): trick_winner = the seat whose played_card has suit == led_suit and the highest rank. The winner gets tricks_won += 1, and for each suit, won_<suit> += the count of that suit in trick_cards. The winner then takes the action of led_suit once. Announce the winner, the action and its result.
14. **update** (table): When trick_number == 7, end of hand, resolved in order: for suit in Diamonds, Hearts, Spades, Clubs, if exactly one player has the strictly highest won_<suit>, that player takes that suit's action once. Then each player with tricks_won == 0 takes the Diamonds action twice (vault += 2). Announce every action.
15. **update** (all players): When trick_number == 7 and hand_number == 3: score = 2 * vault + showroom. Announce scores and vaults.
16. **update** (table): rounds_played += 1. If trick_number == 7, then hand_number += 1 and trick_number = 1; otherwise trick_number += 1 and leader_seat = trick_winner.
17. **check** (table): End the game if rounds_played >= 21; otherwise continue.

## Ending

- ends when: rounds_played >= 21
- ranked by: `you.score * 1000 + you.vault` (the highest wins; players level at the top share the win)
- decided by: Highest score (2 * vault + showroom) after 3 hands wins. A tie on score is broken by more vault crystals. Players still tied share the win, which is the draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3. Seat-based dealer rotation, passing left and the Clubs tie-break all assume 3 seats.
- Strategy at the table: A thoughtful player chooses when to void a suit so that off-suit plays trigger Diamonds or Clubs actions. They track opponents' showrooms to time Clubs and Spades, and weigh winning suit majorities against deliberately taking zero tricks for the +2 vault bonus.
- No talk step: The source rules include no table talk, and adding it would add a mechanic.
- Cards encoded as text 'D7', 'H3', and so on: The suit letter and rank can then be read arithmetically to find led_suit and the trick winner.
- Rank expression score * 1000 + vault: No score can reach 1000 in 21 tricks, so this ranks by score first and vault second. Equal values share the win, which matches the source's draw.
- Final scores computed in a step when hand 3's trick 7 ends: The source scores only at the end of hand 3.

## Simplifications

- Vault is declared public: The source leaves vaults out of summaries, but every vault change is announced to everyone, so vaults are fully trackable. Public visibility gives the same information.
- The trick is played as three separate ask steps addressed by seat expressions relative to leader_seat, each follower's ask followed by an update for an off-suit action: The engine's step list is flat. This keeps clockwise order from a variable leader and resolves each off-suit action before the next player plays.
- Start-of-hand dealing and passing run as steps guarded by trick_number == 1: One round is one trick, so the hand-start steps run only on the first trick of each hand.
- Won cards are tracked only as per-suit counts, not as a pile of cards: The rules use won cards only through their per-suit counts.

## Unsupported (needs engine work)

- none
