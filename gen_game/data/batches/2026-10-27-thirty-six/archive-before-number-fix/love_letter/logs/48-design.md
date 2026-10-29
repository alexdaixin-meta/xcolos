# 48 design

- time: 2026-10-27T19:36:40+00:00 (69.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 45fb67704f4e4c6b, reply sha256 d3b649edbff0a2fc

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: Things to infer: 4 face-up cards plus public discards allow tight card counting over 9 live cards. Priest peeks and King swaps give known information. Guard guesses and Baron timing reward inference. When both players play well, the winner is still largely set by the deal: who draws Guards early, blind first-turn Guard hits (about 1/5 to 1/7 each), forced Countess and Princess draws, and the burned card. My estimate is that chance decides roughly 40–50% of individual hands even between equal reasoners. A skilled player beats a heuristic one in perhaps 60–65% of hands. The original game dilutes this with first to 7 tokens. This variation cuts it to first to 3, a best-of-five-style race. At p = 0.62 per hand, P(win first to 3) ≈ 0.62³·(1 + 3·0.38 + 6·0.38²) ≈ 0.238·(1 + 1.14 + 0.866) ≈ 0.72. So about 28% of games go to the weaker player, before counting the round cap. The 40-turn cap also cuts in: hands average about 5–7 turns, so 3 tokens need 3–5+ hands (15–35+ turns, more with ties). An unfinished hand at round 40 counts for nothing, so 2–2 or 2–1 games end as draws or on stale leads that depend on how many turns the deck happened to give. The reasoning player is favoured, but not clearly enough, and the short target makes the deal decisive too often.
- change: Reduce the weight of chance by playing all 40 rounds instead of stopping at 3 tokens. Remove target_tokens and the immediate win, so roughly 6–8 hands are played and averaged, and the winner is the player with more tokens after round 40. If an early stop is kept, raise the target to 5, but only together with the next change.
- change: Resolve the hand in progress at round 40 instead of discarding it: on round 40, if hand_over = 0, run the showdown comparison (higher hand card, then higher discard_sum) and award the token. Unfinished hands then no longer produce draws or stale leads, and the final turns carry real decisions.
- change: Tiebreak equal final tokens by total hands survived to showdown, or by cumulative discard_sum kept beside tokens, rather than a draw. This needs one player attribute, so free one by turning a constant parameter (for example deck_size or guess_min) into a literal in the steps, keeping attributes ≤ 20.
- change: Fix steps 9, 10 and 13 so the protected announcement can fire: gate them only on discard_choice, and branch on the opponent's protected value inside the step.
- change: State the hidden elements as 3 (hands, deck order, burned card), and say in step 3 which listed rank is the newly drawn card.
The variation that was reviewed: Love Letter Duel: PARAMETERS: deck_size = 16; out_count = 5; deck_after_deal = 9; guess_min = 2; guess_max = 8; target_tokens = 3; max_rounds = 40.

CARDS (16 total, shown by rank number with a name from the text templates):
- rank 1 Guard ×5
- rank 2 Priest ×2
- rank 3 Baron ×2
- rank 4 Handmaid ×2
- rank 5 Prince ×2
- rank 6 King ×1
- rank 7 Countess ×1
- rank 8 Princess ×1

ZONES: deck (hidden order), out_of_play (5 cards: position 1 is the face-down burned card, positions 2–5 are face up), each player's hand (hidden, seen only by its owner) and each player's discards (public). Every card is in exactly one zone at all times, so the zones always total 16.

GAME ATTRIBUTES: deck, out_of_play, deck_count, the seven parameters, active_seat (starts 1), hand_over (starts 1), discard_choice, guess.

PLAYER ATTRIBUTES: hand, discards, discard_sum, tokens (start 0), protected, eliminated.

The deck starts holding all 16 cards.

TEXT BLOCK (all announcements are full sentences):
- discard: 'Seat {s} discards rank {r} ({name}).'
- hit: 'Hit: Seat {s} guessed rank {g} correctly, so Seat {o} is out of the hand.'
- miss: 'Seat {s} guessed rank {g} wrong: Miss: the guess was wrong.'
- protected: 'The card has no effect because Seat {o} is protected by the Handmaid.'
- peek: 'Seat {o} holds rank {r}.' (private, to the active player)
- baron_out: 'Baron: Seat {l} loses the comparison with rank {r} and is out of the hand.'
- baron_tie: 'Baron: the two hands are equal, so nobody is out.'
- handmaid: 'Seat {s} is protected until their next turn.'
- prince: 'Prince: Seat {t} discards rank {r} and draws a new card.'
- king: 'King: Seat {s} and Seat {o} swap hands.'
- princess: 'Seat {s} discarded the Princess and is out of the hand.'
- showdown: 'Showdown: Seat 1 holds rank {a} and Seat 2 holds rank {b}.'
- tie: 'The hand is tied on cards and discard sums, so nobody scores.'
- token: 'Seat {w} wins the hand and now has {t} tokens.'
- faceup: 'The face-up out-of-play cards are rank {a}, rank {b}, rank {c} and rank {d}.'

EACH ROUND (one turn of the active player):
1. NEW HAND (only when hand_over = 1). Move every card from both hands, both discard lists and out_of_play back into the deck. Shuffle the deck; this is the round's only random draw. Move the top 5 cards to out_of_play. Deal 1 card to each player's hand. Set deck_count = 9. Set protected, eliminated and discard_sum to 0 for both players. Set hand_over = 0.
2. When a new hand was just dealt, announce the faceup text for out_of_play positions 2–5.
3. START TURN. Set the active player's protected to 0. The active player takes the top deck card into their hand, and deck_count goes down by 1. Privately tell them: 'You hold rank X and rank Y.'
4. CHOICE. The active player picks which of their two ranks to discard; this is stored in discard_choice.
5. COUNTESS. If the active player holds rank 7 together with rank 5 or rank 6 and chose anything other than 7, discard_choice is set to 7.
6. DISCARD. Move the chosen card from hand to discards. Add its rank to discard_sum. Announce the discard text.
7. GUARD GUESS (only if discard_choice = 1). The active player names a rank from 2 to 8; it is stored in guess.
8. GUARD RESOLVE (if discard_choice = 1). If the opponent is protected, announce protected. Otherwise, if the opponent's card equals guess, set the opponent's eliminated to 1 and announce hit; if not, announce miss.
9. PRIEST (if 2, opponent not protected). Privately tell the active player the opponent's rank with the peek text. If the opponent is protected, announce protected.
10. BARON (if 3, opponent not protected). Compare the two hand cards. The lower one's owner gets eliminated = 1; announce baron_out. If they are equal, announce baron_tie. If the opponent is protected, announce protected.
11. HANDMAID (if 4). Set the active player's protected to 1. Announce handmaid.
12. PRINCE (if 5). The target is the opponent, or the active player if the opponent is protected. The target moves their hand card to their discards, adds its rank to their discard_sum, and the prince text is announced. If the discarded card is rank 8, the target's eliminated becomes 1. Otherwise the target draws: the top deck card if deck_count > 0 (deck_count goes down by 1), or else the burned card from out_of_play position 1.
13. KING (if 6, opponent not protected). The two players swap hand cards. Announce king, or protected if the opponent is protected.
14. PRINCESS (if 8). The active player's eliminated becomes 1. Announce princess.
15. SHOWDOWN (if nobody is eliminated and deck_count = 0). Announce the showdown text. The lower hand card's owner gets eliminated = 1. If the cards are equal, the lower discard_sum's owner gets eliminated = 1. If those are equal too, announce tie and set hand_over = 1.
16. AWARD (if exactly one player is eliminated). The other player gains 1 token. Announce token. Set hand_over = 1. Set active_seat to the eliminated player, who starts the next hand.
17. PASS (if no token was awarded this round). active_seat switches to the other seat.
18. END CHECK. If a player has 3 tokens, the game ends. Otherwise, if this was round 40, the game ends. Winner: The first player to reach 3 tokens wins immediately. If round 40 ends with nobody at 3 tokens, the player with more tokens wins. Equal tokens is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2–4 player deduction card game played with 16 ranked cards. Each turn a player draws one card and discards one of their two, triggering its effect (guess, peek, compare, protect, force a discard, swap, or eliminate themselves). The last player standing, or the highest hand when the deck runs out, wins a token, and the first player to a set number of tokens wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy is safe. 'Always discard the lower card' gives away predictable hands that Guards and Barons punish. 'Always discard the higher card' throws away Princesses and loses Barons and showdowns. 'Always guess 2' with a Guard misses most of the time. The seat edge is small because the loser of a hand starts the next one. In the reviewed duel variation the main defect was not degeneracy but the short first-to-3 race."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Chance decides roughly 40–50% of individual hands even between equal players: blind Guard hits, forced Princess or Countess draws, the burned card. A skilled player wins perhaps 60–65% of hands. First to 3 tokens turns that into only about 72% of games, and the 40-turn cap with unfinished hands discarded adds draws and stale leads."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "There is a lot to improve at: card counting over the live cards, Guard guess selection, Baron timing, Handmaid timing, Countess bluffs, and using King or Prince after a Priest peek. A weak player still wins hands through the deal."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands, deck order and the burned card are hidden. Each discard leaks information about the card kept, so a player must infer the opponent's card from the visible cards and the pattern of their choices."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Eliminations, showdown comparisons, tokens and tiebreaks are all arithmetic on tracked cards and sums."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only with no board. However, the reviewed duel variation had broken gating on Priest, Baron and King, so the protected message could never fire. It also threw away the hand in progress at round 40, and it listed hidden elements unclearly."
    }
  ],
  "problems": [
    "P1: First to 3 tokens is too short a race. The deal decides about 28% of games even when one player is clearly better.",
    "P2: A hand still unfinished at round 40 scores nothing. This produces draws and stale leads that depend on how many turns the deck happened to give.",
    "P3: Equal final tokens is a plain draw, which happens often over an even number of hands.",
    "P4: The Priest, Baron and King steps were gated on 'opponent not protected', so the protected announcement could never fire. Their effects also lacked a clear branch for a protected opponent.",
    "P5: Hands are long (up to 9+ draws), so few hands are played in 40 turns and per-hand luck is poorly averaged. With only 4 face-up cards, early Guard guesses are close to blind.",
    "P6: Hidden elements were not stated, and the private hand message did not say which card was newly drawn.",
    "P7: Constant parameters used up attribute slots needed for a tiebreak attribute."
  ],
  "changes": [
    {
      "what": "Remove the 3-token immediate win and play all 40 turns. The winner is decided by tokens at the end.",
      "why": "About 8 or more hands are averaged instead of a best-of-five, so the better player wins more reliably.",
      "fixes": "P1"
    },
    {
      "what": "On turn 40, if the hand is still running after the turn's effects, hold a showdown immediately and award the token.",
      "why": "No hand is wasted, and the last turns carry real decisions.",
      "fixes": "P2"
    },
    {
      "what": "Add a career_sum player attribute: the cumulative total of all ranks each player has discarded over the game. It breaks equal tokens before declaring a draw.",
      "why": "Draws become rare. The tiebreak also creates a small real trade-off, because discarding high cards helps the tiebreak but weakens a player's showdown hand.",
      "fixes": "P3"
    },
    {
      "what": "Gate Priest, Baron and King only on which card was discarded. Inside each step, check whether the opponent is protected: if so, announce protected; if not, apply the effect.",
      "why": "Handmaid protection is reported correctly and the effects are unambiguous.",
      "fixes": "P4"
    },
    {
      "what": "Set aside 6 cards per hand instead of 5: 1 face down (burned) and 5 face up. The deck after the deal is then 8 cards, not 9.",
      "why": "Hands are shorter, so more hands fit in 40 turns. More public information also makes Guard guesses and counting depend on inference rather than blind luck.",
      "fixes": "P5"
    },
    {
      "what": "State the hidden elements as three: hands, deck order and the burned card. The private message names which card was kept and which was just drawn.",
      "why": "Gives a clear build and clear information for players.",
      "fixes": "P6"
    },
    {
      "what": "Write constants (16, 6, 8, guess range 2–8, 40) as literals in the steps rather than as attributes.",
      "why": "Frees attribute slots for career_sum and keeps the total at 14.",
      "fixes": "P7"
    }
  ],
  "keeps": [
    "The 16-card deck and the eight card effects, including the Countess rule and Princess self-elimination",
    "Draw one, discard one, apply the effect even if it hurts you",
    "A burned card, face-up set-aside cards in the two-player game, and the Prince drawing the burned card when the deck is empty",
    "Last player standing or highest card at showdown wins the hand, with ties broken by discard sum",
    "Tokens of affection across several hands, and the loser of a hand starts the next one"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction core is strong and fits the engine. The fixes concern averaging luck over more hands, settling the final hand at turn 40, a tiebreak, and correct step gating."
  },
  "variation": {
    "name": "Love Letter Duel: Long Courtship",
    "summary": "A two-player Love Letter played over exactly 40 turns. Each hand sets aside 1 hidden and 5 face-up cards, any hand still running at turn 40 is settled by showdown, and the player with more tokens wins, with ties broken by total ranks discarded across the game.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (16): rank 1 Guard x5, rank 2 Priest x2, rank 3 Baron x2, rank 4 Handmaid x2, rank 5 Prince x2, rank 6 King x1, rank 7 Countess x1, rank 8 Princess x1.\n\nZONES: deck (hidden order); out_of_play (6 cards: position 1 is the face-down burned card, positions 2-6 are face up); each player's hand (hidden, seen only by its owner); each player's discards (public). Every card is always in exactly one zone, so the zones total 16.\n\nHIDDEN ELEMENTS: hands, deck order, burned card.\n\nGAME STATE: deck, out_of_play, deck_count, active_seat (starts 1), hand_over (starts 1), discard_choice, guess.\n\nPLAYER STATE: hand, discards, discard_sum (reset each hand), career_sum (whole game, starts 0), tokens (start 0), protected, eliminated.\n\nThe game lasts exactly 40 rounds. Each round is one turn of the active player:\n1. NEW HAND (only if hand_over = 1). Return all cards to the deck and shuffle it; this is the round's only random draw. Move the top 6 cards to out_of_play (the first one to position 1, face down). Deal 1 card to each player's hand. Set deck_count = 8. Set protected, eliminated and discard_sum to 0 for both players. Set hand_over = 0.\n2. If a new hand was just dealt, announce: 'The face-up out-of-play cards are ranks a, b, c, d, e' (positions 2-6).\n3. START TURN. Set the active player's protected to 0. They take the top deck card, and deck_count goes down by 1. Privately tell them: 'You kept rank X and just drew rank Y.'\n4. CHOICE. The active player chooses which of their two ranks to discard; store it in discard_choice.\n5. COUNTESS. If they hold rank 7 together with rank 5 or rank 6, set discard_choice = 7.\n6. DISCARD. Move the chosen card to their discards. Add its rank to their discard_sum and career_sum. Announce 'Seat s discards rank r (name).'\n7. GUARD GUESS (if discard_choice = 1). The active player names a rank from 2 to 8; store it in guess.\n8. GUARD RESOLVE (if discard_choice = 1). If the opponent is protected, announce that the card has no effect. Otherwise, if the opponent's card equals guess, set the opponent's eliminated = 1 and announce a hit; if not, announce a miss.\n9. PRIEST (if discard_choice = 2). If the opponent is protected, announce no effect. Otherwise, privately tell the active player the opponent's rank, and announce publicly that Seat s looked at Seat o's card.\n10. BARON (if discard_choice = 3). If the opponent is protected, announce no effect. Otherwise compare the two hand cards: the owner of the lower one gets eliminated = 1, and the result is announced with the losing rank. If the cards are equal, announce a tie and nobody is out.\n11. HANDMAID (if discard_choice = 4). Set the active player's protected = 1 and announce it.\n12. PRINCE (if discard_choice = 5). The target is the opponent, or the active player if the opponent is protected. The target moves their hand card to their discards, adds its rank to their discard_sum and career_sum, and the rank is announced. If that card was rank 8, the target's eliminated = 1. Otherwise the target draws the top deck card if deck_count > 0 (deck_count goes down by 1), or else takes the burned card from out_of_play position 1.\n13. KING (if discard_choice = 6). If the opponent is protected, announce no effect. Otherwise the two players swap hand cards, and the swap is announced.\n14. PRINCESS (if discard_choice = 8). The active player's eliminated = 1; announce it.\n15. SHOWDOWN (if nobody is eliminated and (deck_count = 0 or this is round 40)). Announce both hand ranks. The owner of the lower card gets eliminated = 1. If the cards are equal, the owner of the lower discard_sum gets eliminated = 1. If those are also equal, announce that the hand is tied and set hand_over = 1.\n16. AWARD (if exactly one player is eliminated). The other player gains 1 token; announce the new total. Set hand_over = 1. The eliminated player becomes active_seat for the next hand.\n17. PASS (if no token was awarded this round). active_seat switches to the other seat.\n18. END CHECK. After round 40 the game ends.",
    "objective": "After round 40, the player with more tokens wins. If tokens are equal, the player with the higher career_sum (total ranks they discarded over the whole game, including cards a Prince forced them to discard) wins. If both are equal, the game is a draw.",
    "expected_effect": "About 8–10 short hands are averaged, instead of a race to 3 that a lucky start can decide. With 5 face-up cards and only 8 deck cards, Guard guesses and Baron or King timing rest on counting and reading the opponent's discards rather than blind odds, so I estimate a skilled player wins 75–80% of games against a heuristic one. The final turn always matters because the open hand is settled. Simple policies all lose: 'always discard the lower card' is read and punished by Guards and Barons; 'always discard the higher card' loses showdowns and discards Princesses; a fixed Guard guess misses most of the time. When both players play well, deal luck still decides some individual hands, but not the game. Talk is not used because there are only 2 players."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 2,
    "attributes": 14,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
