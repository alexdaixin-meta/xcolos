# Variation: Diamonds: Three-Hand Vault

A 3-player trick-taking game over 3 hands of 10 tricks. Winning tricks, and playing off-suit when void, trigger crystal actions. Players race to fill their vaults, defend their showrooms and choose whom to rob with Clubs.

Players: 3 to 3, best with 3

## Review of the original

Diamonds is a trick-taking card game for 2 to 6 players. Winning tricks, and playing off-suit when you cannot follow, trigger suit actions that move crystals between a common supply, a public showroom (1 point each) and a hidden vault (2 points each). After 4 to 6 deals, the highest score wins.

- **non_degenerate**: good. Simple policies do not dominate. 'Always play your highest card' wins tricks but throws away off-suit actions and suit majorities. 'Always play low' gives up tricks and the majority bonuses. Choosing when to win, when to dump a Diamond off-suit and whom to rob with Clubs all changes the outcome. A variable player count creates one problem: the seat that leads the first trick rotates unevenly when the number of deals does not divide by the player count.
- **skill_sensitive**: weak. Card play, voiding suits to unlock off-suit actions, and passing are real skills. But one random 10-card deal per hand decides a lot. With 6 players the 60-card deck is fully dealt and each player has little control, so luck weighs heavily over few deals.
- **headroom**: good. Card counting, planning voids, timing Clubs steals against the leader and fighting for suit majorities give a strong player room to improve. A weak player still collects crystals from tricks and the no-trick consolation.
- **reasoning_dependent**: good. Opponents' hands are hidden. Players must infer holdings from passes and from who fails to follow suit, and must plan voids over 10 tricks.
- **verifiable**: good. The score is crystal counts times 1 or 2. Every action follows mechanically from the cards played.
- **fits_platform**: weak. The game is turn-based and text-only, but it does not fit the limits as written. Up to 6 sequential plays per trick exceeds 4 choice steps. 6 deals of 10 tricks is 60 tricks, over 40 rounds. A variable number of passed cards adds another choice. Clubs targeting is unspecified. The hidden vault is fully trackable from public actions, so it is a memory test rather than real hidden information, and it costs a hidden element.

## Problems

- With more than 4 players, one trick needs more than 4 sequential choice steps, which exceeds the platform limit.
- 4 to 6 deals of 10 tricks is up to 60 tricks, over the 40-round limit.
- Few deals of a large, fully dealt deck let the card draw swamp skill, especially at high player counts.
- The first-trick lead rotates unevenly when the number of deals does not divide by the player count, which gives some seats an edge.
- The dealer's choice of passing 1 to 3 cards adds a choice step and a rule that is hard to resolve in the engine, for little strategic value.
- Clubs steals do not say who chooses the victim or when, and end-of-hand Clubs majorities do not say whom they rob.
- The hidden vault is reconstructible from public actions, so it adds bookkeeping rather than inference while using up a hidden element.
- Edge cases are undefined: stealing from an empty showroom, Spades with an empty showroom, ties on final score.

## Changes

- Fix the game at exactly 3 players. (fixes: With more than 4 players, one trick needs more than 4 sequential choice steps, which exceeds the platform limit.): Each trick then needs 3 sequential plays, plus one simultaneous pass poll on deal rounds, which makes exactly 4 choice steps. Three players also avoid the two-player 'only the difference matters' trap: helping or robbing one rival is not automatically good against the other.
- Play exactly 3 hands of 10 tricks (30 rounds, one trick per round). The deal rotates so that each player leads the first trick of exactly one hand. (fixes: 4 to 6 deals of 10 tricks is up to 60 tricks, over the 40-round limit.): This stays within 40 rounds and gives every seat the same number of first leads.
- Use the same rotation guarantee as above: across the 3 hands, each seat leads the first trick once. (fixes: The first-trick lead rotates unevenly when the number of deals does not divide by the player count, which gives some seats an edge.): This removes the uneven-rotation seat edge.
- Use a 36-card deck (4 suits of ranks 1 to 9). Deal 10 cards to each player and set 6 aside face down and unseen. (fixes: Few deals of a large, fully dealt deck let the card draw swamp skill, especially at high player counts.): A smaller deck makes card counting tractable, which rewards reasoning. The 6 unseen cards keep real uncertainty about which cards are live. Three hands, each followed by a pass, let skill average out the draw.
- Every hand, each player simultaneously passes exactly 2 cards to the player on their left. (fixes: The dealer's choice of passing 1 to 3 cards adds a choice step and a rule that is hard to resolve in the engine, for little strategic value.): This keeps the passing decision (voiding suits, feeding or starving the next player) in a single fixed simultaneous poll.
- Each card play also names a 'Clubs target' (one opponent), which is used if that player gets a Clubs action that trick. An end-of-hand Clubs majority robs the opponent with the largest showroom, with a tie broken toward the opponent on the receiver's left. Stealing from an empty showroom does nothing, and so does Spades with an empty showroom. (fixes: Clubs steals do not say who chooses the victim or when, and end-of-hand Clubs majorities do not say whom they rob.): This makes targeting an explicit opponent-modelling decision (rob the leader, or punish a threat) without adding extra choice steps, and it defines every edge case.
- Make vaults public, and define a tie-break: on equal score, more vault crystals wins; if still tied, the game is a draw. (fixes: The hidden vault is reconstructible from public actions, so it adds bookkeeping rather than inference while using up a hidden element.): This keeps the 2-point versus 1-point tension (vault crystals are also safe from Clubs) and drops bookkeeping that cannot really be hidden. The hidden information goes where inference is genuine: hands and the unseen cards.
- Write out the edge-case rules (empty showroom, Spades with nothing to move, score ties) as part of the rules. (fixes: Edge cases are undefined: stealing from an empty showroom, Spades with an empty showroom, ties on final score.): This leaves nothing for a judge to decide.

## Kept from the original

- Trick-taking with a must-follow-suit rule; the highest card of the led suit wins.
- The four suit actions exactly as in the original: Diamonds puts a crystal from the supply into your vault, Hearts puts one into your showroom, Spades moves one from your showroom to your vault, Clubs steals one from another player's showroom.
- An off-suit play triggers its suit's action immediately; the trick winner takes the led suit's action.
- End-of-hand suit majorities grant suit actions, and ties grant none.
- A player who wins no tricks in a hand receives two Diamond actions.
- Vault crystals are worth 2 points and showroom crystals 1 point; card passing before each hand; several hands; highest score wins.

## The variation's rules

COMPONENTS
- A deck of 36 cards: four suits (Diamonds, Hearts, Spades, Clubs), each ranked 1 to 9.
- An unlimited supply of crystals.
- Each player has a showroom and a vault. Both start empty, and the counts of both are public.
- For each hand, the engine tracks how many cards of each suit every player has won, and how many tricks each player has won. These counts are public.

SEATS
- Players sit in fixed order: A, B, C. 'Left' means the next player in that order (A's left is B, B's left is C, C's left is A).

STRUCTURE
- The game is 3 hands of 10 tricks: 30 rounds, one trick per round.
- Hand 1 is rounds 1 to 10, hand 2 is rounds 11 to 20, hand 3 is rounds 21 to 30.
- The dealer is C for hand 1, A for hand 2 and B for hand 3. The player to the dealer's left leads the first trick of the hand, so A, B and C each lead a hand's first trick exactly once.

DEAL AND PASS (first round of each hand only)
1. Shuffle all 36 cards. Deal 10 cards face down to each player. Set the remaining 6 aside face down; no one sees them during the hand.
2. All players at the same moment secretly choose exactly 2 cards from their hand.
3. Each player then gives those 2 cards to the player on their left. Players see their new hand; the passed cards are not announced to anyone else.
4. Reset every player's won-card counts and trick counts to 0.

PLAYING A TRICK (every round)
1. The leader plays any card from their hand, face up, and names one opponent as their Clubs target.
2. The next player to the left then plays a card and names a Clubs target. Then the third player does the same.
3. The suit of the first card is the led suit. A player who holds a card of the led suit must play one. A player who holds none may play any card.
4. OFF-SUIT ACTION: when a player plays a card not of the led suit, they immediately take that card's suit action, before the next player plays.
5. The highest card of the led suit wins the trick.
6. The winner adds the 3 cards to their won counts by suit (each card counts in its own suit) and adds 1 to their trick count.
7. The winner then takes the led suit's action.
8. The winner leads the next trick of the same hand.
9. Everything played and every action taken is announced to all players.

SUIT ACTIONS (for the player taking the action)
- Diamonds: move 1 crystal from the supply to your vault.
- Hearts: move 1 crystal from the supply to your showroom.
- Spades: move 1 crystal from your showroom to your vault. If your showroom is empty, nothing happens.
- Clubs (from a trick or an off-suit play): move 1 crystal from your named Clubs target's showroom to your own showroom. If that showroom is empty, nothing happens.

END OF HAND (after the 10th trick of each hand)
1. For each suit in turn (Diamonds, Hearts, Spades, Clubs), the player with strictly the most won cards of that suit takes that suit's action once. If the top count is tied, no one takes it.
2. An end-of-hand Clubs action robs the opponent with the largest showroom. If those opponents are tied, it robs the one on the receiver's left.
3. Each player who won 0 tricks in the hand takes two Diamond actions.
4. The 6 set-aside cards are then revealed, and all cards are gathered for the next deal.

SCORING
- Each vault crystal is worth 2 points and each showroom crystal 1 point.
- After the 30th round and the third end-of-hand step, the game ends.

Objective: The player with the highest score (2 x vault + 1 x showroom) wins. If players tie on score, the tied player with more vault crystals wins. If they are still tied, the game is a draw.

Expected effect: Players must count cards across a 36-card deck with 6 unseen cards. They must use the 2-card pass to create voids (so off-suit Diamond dumps become available) without handing the left neighbour a strong suit. They must decide when to take a trick for its led-suit action and when to lose it for an off-suit action, and they must contest the suit majorities. Clubs targeting makes players model the race: robbing the leader helps you and the third player alike, while robbing the weaker player may be safer. Spades lets players bank showroom crystals before they are stolen. Simple policies lose: 'always play highest' wastes off-suit actions and draws Clubs attention, while 'always play lowest' forfeits majorities and still earns the two-Diamond consolation only rarely. With three hands, a pass every hand and one first lead per seat, the deal matters less than play. Talk is deliberately left out. Trick-taking already carries its signals through card play. Open table talk would mostly produce non-binding 'gang up on the leader' calls that no one has to honour. On deal rounds the game already uses all 4 allowed choice steps.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
