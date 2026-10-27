# Variation: Tides of Madness: Obsession

A two-player pick-and-pass draft over 3 tides of 5 picks. Players build suit sets, secretly double one Obsession suit each tide, and race for the madness bonus without reaching 9 madness.

Players: 2 to 2, best with 2

## Review of the original

Tides of Madness is a two-player pick-and-pass card draft over three rounds. Players keep one card at a time and pass the rest to build tableaus that score for suit sets. Madness icons give a bonus to whoever has more of them, but a player whose total madness reaches 9 loses instantly.

- **non_degenerate**: good. Choices are simultaneous, so neither seat has a built-in edge. 'Always grab madness' runs into the 9-madness instant loss, and 'never take madness' gives the opponent the 4-point bonus every round. The core tension holds.
- **skill_sensitive**: good. Both players see and draft from both hands, so the deal is largely shared. Skill shows in reading which cards the opponent needs, hate-drafting, and pacing madness. The large variety of unique card powers adds some swing from the deal.
- **headroom**: good. Several things must be balanced at once: set building, denial, madness timing across rounds and the choice of which card to retain. A beginner still scores sets.
- **reasoning_dependent**: weak. With two players and open tableaus, after the first pass you know almost everything. The only hidden facts are the opponent's first look at their hand and the undealt cards. Planning across rounds exists, but there is little to infer.
- **verifiable**: good. Set scoring, madness counts and the threshold are all arithmetic.
- **fits_platform**: weak. It is turn-based and text-only, but the real deck has dozens of unique cards, each with its own scoring condition. That exceeds the attribute and step limits. Hand passing must be built from list swaps, which is possible.

## Problems

- Dozens of unique card scoring rules cannot be built within the limit of 20 attributes and 20 steps per round.
- Two-player drafting with face-up tableaus leaves almost nothing hidden, so there is little to infer about the opponent.
- The original does not say what happens if both players cross 9 madness together, or how a points tie is broken, so the arithmetic winner is incomplete.
- Much of each card's value comes from its specific printed power, which adds luck from the deal unrelated to reasoning.

## Changes

- Replace the unique cards with a 30-card deck: 5 suits of 6 cards, 2 of each suit carrying a madness icon. Scoring is uniform: set points by suit count, +1 per madness card, and a diversity bonus. (fixes: Dozens of unique card scoring rules cannot be built within the limit of 20 attributes and 20 steps per round.): This keeps sets and madness, the heart of the game, while making the cards buildable and their scoring transparent.
- At the start of each tide, each player secretly chooses an Obsession suit whose set points are doubled for that tide. It is revealed only at tide scoring. (fixes: Two-player drafting with face-up tableaus leaves almost nothing hidden, so there is little to infer about the opponent.): This creates a hidden type chosen by the player, so it is not luck. The opponent must infer it from picks to decide what to deny, and a player may bluff by drafting a decoy suit.
- Drafted cards are placed face down until the end of the tide. Retained cards stay face up. (fixes: Two-player drafting with face-up tableaus leaves almost nothing hidden, so there is little to infer about the opponent.): The opponent's first pick from their unseen starting hand stays unknown. They may be hiding a madness card, which changes the race for the madness bonus.
- Give every card equal base value and draft from shared passed hands only. (fixes: Much of each card's value comes from its specific printed power, which adds luck from the deal unrelated to reasoning.): Both players see most of the same cards, so the deal mostly changes what is available to both, not who is ahead.
- Add explicit loss, tie and draw rules: both players crossing 9 madness, points ties broken by lower madness, otherwise a draw. (fixes: The original does not say what happens if both players cross 9 madness together, or how a points tie is broken, so the arithmetic winner is incomplete.): Every ending is then decided by arithmetic.

## Kept from the original

- Two players, three rounds (tides) of simultaneous pick-and-pass drafting from hands that shrink as they are passed.
- Suit sets as the main source of points.
- Madness icons: whoever has more in a tide chooses 4 points or healing, and reaching 9 total madness is an instant loss.
- Retaining one card permanently between tides.

## The variation's rules

DECK. 30 cards in 5 suits: Ruins, Idols, Deep, Stars, Shore. Each suit has 6 cards: 4 plain and 2 with a madness icon (written e.g. 'Deep*').

STRUCTURE. The game has 15 rounds in 3 tides of 5 rounds each: rounds 1-5 are tide 1, rounds 6-10 tide 2, rounds 11-15 tide 3. Each player has a score (starting at 0) and a madness total (starting at 0).

START OF EACH TIDE (rounds 1, 6, 11).
- All 30 cards are shuffled, minus any cards currently retained by players.
- Each player is dealt a private hand of 5. The rest are unused this tide.
- Each player sees only their own hand.
- At the same moment as their first pick, each player secretly chooses one suit as their Obsession for this tide. It is hidden from the opponent until the tide is scored.

EACH ROUND.
- Both players simultaneously choose one card from the hand they currently hold and place it face down in their tableau for this tide.
- Then the two players swap their remaining hands.
- Hands therefore go 5, 4, 3, 2, 1 cards, and the pick in the fifth round of a tide is forced.
- A player always knows the cards they themselves drafted and the hands they saw.

END OF EACH TIDE (rounds 5, 10, 15), in order:
1. Reveal. Both tableaus and both Obsessions are revealed. A player's tide tableau is the 5 cards drafted this tide plus all cards they have retained from earlier tides.
2. Madness. Each player counts madness icons in their tide tableau (retained cards count every tide they are in) and adds that number to their madness total.
3. Set points. For each suit, count the cards of that suit in the tableau: 0 cards = 0 points, 1 = 1, 2 = 3, 3 = 6, 4 or more = 10. Points for the player's Obsession suit are doubled.
4. Extra points. Add +1 point per madness card in the tableau. Add +4 points if the tableau contains at least 4 different suits.
5. Madness bonus. The player with strictly more madness icons in their tide tableau privately chooses one: gain 4 points, or reduce their madness total by 1. If the counts are equal, nobody gets the bonus.
6. Madness check. If a player's madness total is 9 or more, the game ends immediately and that player loses. If both are at 9 or more, the one with the higher madness total loses. If they are equal, the game is a draw.
7. Retain (tides 1 and 2 only). Each player simultaneously chooses one card drafted this tide to retain permanently. It stays face up beside them and is part of every later tide tableau. All other drafted cards return to the deck.

END OF GAME. After the tide 3 scoring, if no one has been eliminated, the winner is decided as stated in the objective.

Objective: A player loses immediately if their madness total reaches 9 or more at a tide's madness check. If both reach it, the higher madness total loses, and equal totals are a draw. Otherwise, after tide 3 the higher score wins. If scores are tied, the lower madness total wins. If that is also tied, the game is a draw.

Expected effect: Players must read the opponent's picks to guess their hidden Obsession, and decide whether to hate-draft that suit or chase their own. They can also bluff by drafting a decoy suit early. Face-down picks hide the opponent's first card, so the madness-bonus race involves estimating their icon count. Retained madness cards compound across tides, which forces planning toward the 9 threshold. Simple policies each lose: grabbing every madness card gives about 3-4 icons a tide plus retained ones and crosses 9 by tide 3. Never taking madness concedes 4 bonus points every tide. Always taking the first card ignores both sets and Obsession.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 15 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
