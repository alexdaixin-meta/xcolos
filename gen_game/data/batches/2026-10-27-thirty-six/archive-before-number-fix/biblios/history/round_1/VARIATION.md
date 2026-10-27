# Variation: Biblios: Scriptorium

Each round the active monk privately sees two manuscript cards, secretly keeps one and sells the other in a sealed-bid auction, pocketing the price. Players fight for majorities in three colours whose VP values Church cards push up and down.

Players: 3 to 4, best with 3

## Review of the original

Biblios is a 2-4 player card game played in two phases. In a drafting 'gift' phase the active player splits drawn cards into one secret card for themselves, one secret card for a later auction, and public cards for the others. In an auction phase the players spend Gold cards to buy the auctioned cards. At the end, the player with the highest total in each of five colours wins that colour's die value, which Church cards can raise or lower; most VP wins.

- **non_degenerate**: good. No simple policy dominates. Hoarding gold gives up cards. Grabbing cards leaves you unable to bid. Majority scoring with dice that can move punishes spreading over every colour. The first player gets slightly more active turns in uneven deck splits, but the edge is small.
- **skill_sensitive**: good. Strong players count cards, read what an opponent must have kept face-down, price auction lots by how they swing majorities, and time Church card use. Luck of the draw matters but is smoothed over around 80 cards.
- **headroom**: good. There is room to keep improving through deeper inference about hidden cards and bidding strategy. A weak player still wins some colours.
- **reasoning_dependent**: good. The secret kept card and the secret auction card are real hidden information. Bids reveal how much players value a lot. The dice create bluffing about which colours matter.
- **verifiable**: good. Colour sums, die values and VP totals are pure arithmetic. The letter tie-break is mechanical.
- **fits_platform**: weak. The original is too large to build here:
- It uses 87 cards, 5 colours and letter tie-breaks.
- The draft has up to 5 sequential placements per turn.
- The open-outcry auction has clockwise raising and re-auctions on failure to pay.
- Stealing a random card is a second random draw.

These break the limits of 4 choice steps and 1 random draw per round and need conditional sub-sequences. Even so, it is turn-based and text-only.

## Problems

- P1: The two-phase structure (a whole draft phase, then a whole auction phase) needs block-level switching, which the engine cannot do.
- P2: The gift turn has many sequential placements and pick-orders, which exceeds 4 choice steps per round.
- P3: Open-outcry clockwise raising with re-auction on non-payment is a long variable-length chain of turns.
- P4: Five colours, 87 cards and letter tie-breaks give too many attributes for the limits and too long a game.
- P5: The penalty for failing to pay (a random steal plus a re-auction) adds a second random draw and a conditional block.
- P6: Gold only enters through lucky draws, so a player who sees no Gold cards is locked out of auctions; this is luck, not skill.

## Changes

- Merge draft and auction into every round. The active player privately sees 2 cards, secretly keeps one and auctions the other. (fixes: P1): This keeps the defining 'secret card for me, other card to market' decision inside a flat step list.
- The gift turn becomes a single choice: which of the 2 cards to keep. (fixes: P2): One choice step instead of many placements.
- The auction becomes one simultaneous sealed bid by the non-active players. The highest unique bid wins. A tie or all zeros discards the card. (fixes: P3, P5): This is one poll with no re-auction loops, and bids can never exceed what a player owns.
- The winning bid is paid to the active player, the seller. (fixes: P6): Gold circulates, so being the seller is a real income source. It also creates a sell-high-versus-keep-the-good-card tension.
- Use 3 colours, a 24-card known deck that is exactly used up, VP shares split on ties, and no letters. (fixes: P4): This fits the attribute and length limits. A fully known deck makes card counting and inference about hidden kept cards possible.
- Church cards stay. Whoever gains one picks one colour to raise or lower by 1, with values limited to 1-5. This is done in a single end-of-round poll. (fixes: P2): This keeps the dice manipulation within the choice-step budget.
- Every player starts with 4 Gold, so no one is locked out. (fixes: P6): Everyone can bid from round 1.

## Kept from the original

- The secret kept card versus the card given to the market, and inferring what others kept
- Gold-based auctions for cards
- Majority scoring per colour, with VP values that Church cards shift
- Gold is only a means: leftover Gold scores nothing except as a tie-break
- A known finite deck that rewards card counting

## The variation's rules

SETUP

The deck has 24 cards, and its full contents are public knowledge:
- Red: 1, 1, 2, 2, 3, 4 (6 cards)
- Blue: 1, 1, 2, 2, 3, 4 (6 cards)
- Green: 1, 1, 2, 2, 3, 4 (6 cards)
- Gold: 2, 2, 3, 3 (4 cards)
- Church (2 cards)

Shuffle the deck. Every player starts with 4 Gold. Each player's Gold amount is private. Each colour has a public VP value that starts at 3 (Red 3, Blue 3, Green 3); a VP value can never go below 1 or above 5. Seat 1 is the active player in round 1. The game lasts exactly 12 rounds, and the active player rotates by seat each round (seat 1, 2, 3, 1, ... or seat 1-4 with 4 players). The deck is exactly used up.

EACH ROUND

1. Draw. Draw the top 2 cards. Only the active player sees them.

2. Keep. The active player secretly chooses one card to keep.
   - A kept colour card goes face-down into the active player's private hand. Its value counts for that colour at the end.
   - A kept Gold card adds its value to the active player's private Gold immediately.
   - A kept Church card is played at step 9.
   - Nobody else learns what was kept, except that a Church card is revealed when it is played.

3. Offer. The other card is revealed to everyone as the lot.

4. Talk. Every player, including the active player, writes one short message at the same time. All messages are then shown to everyone. Talk is not binding.

5. Bid. Every non-active player at the same time submits a whole-number bid from 0 up to their current Gold.

6. Resolve.
   - If one player made the single highest bid and it is at least 1, that player pays the bid from their Gold to the active player's Gold.
   - If the highest bid is tied, or all bids are 0, nobody pays and the lot is discarded.

7. Take. The winner takes the lot face-up, so its colour and value are public.
   - A Gold lot adds its value to the winner's Gold.
   - A Church lot is played at step 9.

8. Announce. The sale price (or 'discarded') is announced.

9. Church. Each player who gained a Church card this round, whether kept or bought, chooses at the same time one colour and either +1 or -1. Apply all changes, limited to the range 1-5. A colour may receive two changes. The new VP values are announced.

10. End check. After round 12, the game ends.

END SCORING

For each colour, each player sums the values of all their colour cards in that colour (kept and bought). The player with the highest sum gains that colour's current VP value. If several players tie for highest, they split the value equally (fractions allowed). A colour in which everyone has 0 scores for no one. Gold scores no VP.

Objective: The player with the most VP wins. If VP totals tie for first, the tied player with the most leftover Gold wins. If that also ties, the game is a draw.

Expected effect: Players must:
- Count the known deck to deduce what each seller kept, from the lot they offered and from bid behaviour.
- Price lots by how they swing contested majorities.
- Decide whether to sell a strong card for Gold or keep it.
- Use Church cards to inflate colours they secretly lead and deflate rivals' colours.

Simple policies lose:
- Always bidding 0 ends with only about 4 kept cards against rivals holding about 8.
- Always bidding all your Gold hands money to sellers and leaves you priced out of decisive lots.
- Always keeping the higher card makes your hidden hand easy to deduce.

Talk passes both tests. Players disagree about which colours are valuable and who should win each lot, since only one player can win. Talk enables bluffing about hidden holdings and proposals to gang up on the leader. A player who believes a seller's claim that 'Blue is dead to me' may overpay for, or skip, a lot and lose a majority the seller secretly holds.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
