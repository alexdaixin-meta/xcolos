# Variation: 5211: Mirror Hands

Every player holds the same 14 cards and a secret bonus colour. Over 7 rounds they each commit two cards, one at a time, trying to be in the colour that wins the majority without busting it, or to hit the exact Kododo count.

Players: 3 to 4, best with 4

## Review of the original

5211 is a 3-8 player simultaneous card game. Each round every player commits 4 cards from a hidden hand over three face-down turns. The most-played colour scores for the players who played it, unless it 'busts' by being played too much or is tied. A special Kododo count can override everything so that only Kododo players score.

- **non_degenerate**: good. No simple policy is safe. 'Always play your highest cards' piles onto whatever colour you hold most of, and that colour gets tied or busts. Two players following the same simple policy usually tie, which discards the colour. Play is simultaneous, so no seat has an edge.
- **skill_sensitive**: weak. Reading the table and timing bust risks is a real skill. But hands come from a 100-card shuffled deck with refills, and some cards are removed unseen. A player who draws a strong colour concentration or extra Kododos has a large edge that skill only partly offsets.
- **headroom**: good. Deep play exists: steering the majority, predicting busts, holding Kododos for the exact-count round, using what was revealed in earlier turns. A weak player still scores whenever they happen to join the winning colour.
- **reasoning_dependent**: good. Hands are hidden and turns are simultaneous. Each player has to infer from earlier revealed cards what colours others are likely to play, and whether a colour is near busting.
- **verifiable**: good. Scoring is pure counting: the Kododo total, the per-colour counts, the bust threshold and the card values.
- **fits_platform**: weak. It is text-only and simultaneous. However, a 100-card shuffled deck, per-player refill draws every turn, three play turns and a cascading 'next most-played colour' rule exceed the one-random-draw-per-round and step limits. The game also runs long.

## Problems

- Luck of the deal and of the per-turn refill draws strongly affects who can control a colour or hit the Kododo count. This is a lottery element.
- Per-player refill draws every turn need several random draws per round, which the platform limits to one.
- Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps.
- The game length (a 100-card deck run down) is too long for the platform.
- Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent.

## Changes

- Every player gets an identical fixed 14-card hand: 4 colours each with values 1, 2 and 3, plus 2 Kododos. There is no deck and no refills. (fixes: Luck of the deal and of the per-turn refill draws strongly affects who can control a colour or hit the Kododo count. This is a lottery element.): This removes hand luck entirely. Because played cards are public, a player who tracks the plays knows what everyone has left, so the contest is about predicting intent and timing.
- Removed all in-game drawing. The only random event is a setup deal of distinct secret bonus colours. (fixes: Per-player refill draws every turn need several random draws per round, which the platform limits to one.): This fits the limit of at most one random draw per round.
- Each round is two simultaneous card plays: one face-down card, a reveal, then a second face-down card, then a reveal. This replaces the original three turns of 2+1+1 cards. (fixes: Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps.): It keeps the 'see part of the table, then commit more' tension in far fewer steps.
- Cut to 4 colours. Resolution is a single rule: the non-busted colour with the strictly highest count scores, and if the top is tied nothing scores. (fixes: Three play turns per round plus five colour counts plus a cascading tie and bust resolution need too many steps.): A single arithmetic comparison replaces the cascade. Ties still kill the colour, as in the original.
- The game is fixed at 7 rounds, so all 14 cards are played. (fixes: The game length (a 100-card deck run down) is too long for the platform.): This keeps it short. The forced endgame also rewards planning which cards to save.
- Each player gets a secret bonus colour, distinct from everyone else's, and earns +1 per scored card of that colour. (fixes: Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent.): It adds a symmetric hidden type. Each type has equal total value, but it changes which colours you want to win. Players must infer each other's bonus colours from their plays and talk.
- Added a simultaneous one-message talk phase before the first card each round. (fixes: Hand contents are the only private information. Once hands are luck-driven, the hidden element measures luck more than intent.): It allows bluffing and temporary alliances to swing a majority. Since only one player can win and players hold different bonus colours, proposals are self-interested and following one blindly can tie or bust a colour.

## Kept from the original

- Simultaneous face-down card plays from a hidden hand
- The most-played colour scores only for those who played it
- The bust rule: a colour played too much scores nothing
- Ties for the majority kill the tied colours
- The Kododo override: an exact Kododo count lets only Kododo players score
- Partial reveal mid-round, then further commitment
- Highest total wins, with most scored cards as the tie-break

## The variation's rules

SETUP. Let n be the number of players (3 or 4). Every player receives an identical hand of 14 cards:
- the colours Red, Blue, Green and Yellow, each with values 1, 2 and 3 (12 cards);
- 2 Kododo cards, which have no colour and are worth 3 each.
Hands are private, but because every hand starts identical and all played cards are revealed, anyone can track what each player has left. Each player is then secretly dealt a bonus colour at random from Red, Blue, Green and Yellow, with no two players sharing one. Only that player knows it. Scores start at 0, and each player's scored-card count starts at 0.

EACH ROUND (7 rounds):
1. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing said is binding.
2. First card. Every player at the same time places one card from their hand face down.
3. Reveal. All first cards are revealed.
4. Second card. Every player at the same time places one more card from their hand face down.
5. Reveal. All second cards are revealed. Played cards leave the hands.
6. Count. Count K, the number of Kododos played this round (out of 2n cards). Count how many cards of each colour were played.
7. Kododo check. If K equals exactly n-1 (2 Kododos with 3 players, 3 with 4 players), each player scores 3 points per Kododo they played this round and adds that many cards to their scored-card count. No colour scores this round.
8. Colour check (only if K is not exactly n-1). A colour is busted if its count is n+1 or more (4 or more with 3 players, 5 or more with 4 players). Among the colours that are not busted and have a count of at least 1, find the highest count. If exactly one colour has that highest count, it is the scoring colour. If two or more colours share it, or no colour qualifies, nothing scores this round.
   Each player scores the face values of their cards of the scoring colour, plus 1 extra point per such card if it is their bonus colour, and adds those cards to their scored-card count.
   Kododos played in a round where the Kododo check fails score nothing.
9. Announce the round result and the updated scores.

END. After round 7, all 14 cards have been played and the game ends.

Objective: The player with the highest total score wins. If players are tied on total score, the one among them with the higher scored-card count wins. If they are still tied, the game is a draw among the tied players.

Expected effect: Removing deal luck makes the result depend on predicting others' plays.

How the round plays: the mid-round reveal lets players react, either by joining the emerging leader or by deliberately pushing it to bust or tie. Kododo timing becomes a pure reading game, because everyone knows exactly how many Kododos each opponent has left.

What players disagree about: hidden bonus colours mean each player wants a different colour to win. Talk is used to propose a colour, recruit allies and bluff. A player who simply follows a proposal can lose in three ways: two others pile on and bust the colour, a rival splits the vote to force a tie, or the proposer benefits from the bonus while the follower gains only face value.

The endgame: the fixed 14-card hand rewards planning which high cards and Kododos to save for the late, fully deducible rounds.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 7 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
