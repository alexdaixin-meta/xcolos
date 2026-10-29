# Variation: Diamonds: Three-Hand Vault

A 3-player trick-taking game over 3 hands of 7 tricks. Winning tricks, or deliberately failing to follow suit, triggers suit actions that bank crystals in a showroom (1 point) or a vault (2 points). Clubs automatically robs the richest showroom.

Players: 3 to 3, best with 3

## Review of the original

Diamonds is a trick-taking card game for 2 to 6 players. Winning a trick, or failing to follow suit, triggers a suit action that moves crystals between a public showroom (1 point each) and a hidden vault (2 points each). Suit majorities pay out at the end of each hand, and the highest score after 4 to 6 hands wins.

- **non_degenerate**: weak. In the original, choices clearly matter, because ducking a trick to trigger an off-suit action is a real alternative to winning it. But the previous build had seat imbalance: against random seats, seat 3 won 26 games, seat 1 won 19 and seat 2 won 14. This came from a fixed robbing order and uneven dealer/lead rotation. Thoughtless 'first' and 'last' policies did lose most games (13-46, 19-41, 20-39, 24-33), so no simple policy dominates.
- **skill_sensitive**: good. Choosing when to win a trick and when to void a suit to trigger off-suit actions, tracking suit majorities, and timing Spades conversions against Clubs theft all reward card counting and planning. The deal adds variance, but it is averaged over several hands.
- **headroom**: good. Strong play involves counting cards, voiding suits on purpose through the pass, and denying majorities. A weak player still collects crystals from incidental tricks, and a player who wins no tricks gets a consolation of two Diamond actions.
- **reasoning_dependent**: good. Hands are hidden, so players must infer who is void in which suit from the plays, and must predict whether an opponent will win or duck a trick. Hidden vaults add score uncertainty.
- **verifiable**: good. Every action and every score is crystal arithmetic.
- **fits_platform**: bad. The original is long: up to 6 hands of 10 tricks with up to 6 players. Its Clubs action requires naming a target, and passes of up to 3 cards each take a choice. The previous build reached 8 choice steps per round, against a limit of 4.

## Problems

- Too many choice steps per round (8 against a limit of 4): the Clubs target choice and the multi-card pass each add choice steps.
- Seat imbalance: seat 3 won most often among random seats, from a fixed-seat Clubs tie-break and a dealer/lead rotation that did not give each seat equal leads.
- The game is too long for the platform (up to 60 tricks), which risks the 40-round limit and adds attribute and step load.
- Hidden vaults are not really hidden in a text engine, because every vault action is announced; this is not a flaw for play, but the hidden element is effectively the hands.

## Changes

- Clubs robs automatically: it takes 1 crystal from the opponent with the largest showroom. Ties go to the tied opponent who comes first clockwise from the actor. (fixes: Too many choice steps per round (8 against a limit of 4): the Clubs target choice and the multi-card pass each add choice steps.): This removes a choice step, and the tie-break depends only on the robbed player's position relative to the actor, not on fixed seats.
- The pass becomes exactly 1 card to the left, chosen by all players in one simultaneous poll, and only on the first trick of each hand. (fixes: Too many choice steps per round (8 against a limit of 4): the Clubs target choice and the multi-card pass each add choice steps.): It keeps the original's voiding and pass tactic while costing one choice step on one round in seven. The maximum per round is 3 plays plus 1 pass, which is 4.
- The game is fixed at 3 players, 3 hands and 7 tricks per hand (21 rounds), using a 32-card deck (4 suits, ranks 1-8). 21 cards are dealt and 11 stay unseen. (fixes: The game is too long for the platform (up to 60 tricks), which risks the 40-round limit and adds attribute and step load.): This keeps the game short and under 40 rounds. The unseen cards keep void-inference non-trivial.
- The dealer rotates clockwise each hand, so each seat deals exactly once and the player left of the dealer leads trick 1, giving each seat exactly one opening lead. All end-of-hand actions resolve starting from the player left of the dealer. (fixes: Seat imbalance: seat 3 won most often among random seats, from a fixed-seat Clubs tie-break and a dealer/lead rotation that did not give each seat equal leads.): Every seat gets identical structural treatment across the game.
- Vault totals are not displayed in the score summary, but every action is announced. Ties on score are broken by vault size. (fixes: Hidden vaults are not really hidden in a text engine, because every vault action is announced; this is not a flaw for play, but the hidden element is effectively the hands.): This honestly accepts that vault totals can be worked out from the announcements, and turns the hiddenness into a memory and tracking skill rather than a fake secret. The vault tie-break rewards Spades and Diamond play.

## Kept from the original

- Trick-taking with must-follow-suit and highest card of the led suit winning.
- Four suit actions: Diamonds (supply to vault), Hearts (supply to showroom), Spades (own showroom to vault) and Clubs (steal into own showroom).
- Off-suit plays immediately trigger the played suit's action.
- The trick winner takes the led suit's action and leads the next trick.
- End-of-hand suit majorities earn suit actions, and ties earn nothing.
- A player who wins no tricks in a hand gets two Diamond actions.
- Vault crystals are worth 2 points and showroom crystals 1 point; the highest score wins.
- A card pass to the left before each hand.

## The variation's rules

COMPONENTS: A deck of 32 cards with 4 suits (Diamonds, Hearts, Spades, Clubs) and ranks 1 to 8 in each suit. Each player has a showroom and a vault, each holding crystals and each starting at 0. The supply of crystals is unlimited. Seats are numbered 1, 2 and 3 clockwise; 'left' means the next seat clockwise.

STRUCTURE: The game is 3 hands of 7 tricks, which is 21 rounds; one round is one trick. In hand 1 the dealer is seat 1, in hand 2 seat 2, and in hand 3 seat 3.

START OF EACH HAND (on trick 1 of the hand): Shuffle all 32 cards and deal 7 to each player face down; the remaining 11 cards are set aside unseen for the hand. Each player privately sees only their own hand. Shown to each player, a hand is listed sorted by suit (Diamonds, Hearts, Spades, Clubs) and then by ascending rank. Then all players at the same moment secretly choose exactly 1 card from their hand to pass to the player on their left. All passes are exchanged at once, and passed cards are not revealed to the third player. Every player's per-hand count of won cards in each suit is reset to 0, and so is their tricks-won count.

PLAYING A TRICK: On trick 1 of a hand, the player left of the dealer leads; on later tricks, the winner of the previous trick leads. The leader plays any card from their hand, and its suit is the led suit. The other two players then play one card each, in clockwise order. A player who holds a card of the led suit must play one. A player who holds no card of the led suit may play any card, and immediately takes the action of the suit of the card they played (see SUIT ACTIONS), resolved before the next player plays. All played cards are shown to everyone.

WINNING A TRICK: The highest-ranked card of the led suit wins the trick, and off-suit cards never win. The winner takes all 3 cards face down, adds 1 to their tricks-won count, and adds the number of cards of each suit in the trick to their won-card count for that suit. The winner then takes the action of the led suit once, and leads the next trick.

SUIT ACTIONS:
- Diamonds: move 1 crystal from the supply to your vault.
- Hearts: move 1 crystal from the supply to your showroom.
- Spades: move 1 crystal from your own showroom to your own vault. If your showroom is empty, nothing happens.
- Clubs: move 1 crystal from the showroom of the opponent whose showroom is largest into your own showroom. If both opponents tie for largest, take it from the tied opponent who sits first clockwise after you. If both opponents' showrooms are empty, nothing happens.
Every action and its result is announced to all players.

END OF HAND (after trick 7): For each suit in the order Diamonds, Hearts, Spades, Clubs, the player with strictly the most won cards of that suit takes that suit's action once; if the top count is tied, no one takes it. Then every player whose tricks-won count for the hand is 0 takes the Diamonds action twice. The dealer passes to the left for the next hand. Resolve all end-of-hand actions in the order given.

VISIBILITY: Showroom counts are always displayed. Vault counts are not displayed in score summaries, but every action that changes a vault is announced, so they can be tracked. Hands, passed cards and the 11 set-aside cards are hidden.

SCORING: At the end of hand 3, each player's score is 2 times their vault crystals plus their showroom crystals.

Objective: The player with the highest score after 3 hands wins. If two or more players tie for highest score, the tied player with more vault crystals wins. If they are still tied, the game is a draw between them.

Expected effect: The previous problems should be gone. Each round has at most 4 choice steps: the 3 sequential card plays, plus the single simultaneous pass poll on trick 1 of a hand. Seat balance should improve, because each seat deals once and leads trick 1 once, and the Clubs tie-break depends on position relative to the actor rather than on fixed seats. Thoughtless policies should keep losing. 'First card' always dumps the lowest Diamond-side card and 'last card' always throws the highest Club-side card, ignoring voids, majorities and showroom exposure, so both concede suit majorities and get robbed. Skilled play rewards several things: passing to void a suit, choosing between winning a trick for its led action and ducking it for an off-suit action, inferring opponents' voids from discards and the 11 unseen cards, timing Spades conversions before Clubs theft, and not becoming the largest showroom. Talk is deliberately left out. The three players' interests do conflict, but simultaneous messages would mostly produce empty 'let's all rob the leader' proposals that cannot be enforced and that the automatic Clubs targeting already implements. Card play itself carries the signalling.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 21 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
