# Variation: Trischettn Duel

A two-player Trischettn over three deals with a 24-card deck. The top talon card is face up, so each trick is fought over a known prize, and each player gets one timed declaration per deal.

Players: 2 to 2, best with 2

## Review of the original

Trischettn is an Austrian Tressette-family trick-taking game with no trumps and a 32-card Salzburg deck. Players must follow suit, the winner of each trick draws first from a talon, and points come from Aces, picture cards, the last trick and declared sets (three or four Tens, Nines or Aces, or the Napoli of Ten, Nine and Ace of one suit). Play continues over many deals until someone reaches 31 or 41 points.

- **non_degenerate**: good. No simple policy wins in trick-taking. 'Always play your highest card' throws Tens and Nines under the opponent's winners. 'Always play your lowest' gives away every contested trick and the 1-point last trick. Because there are no trumps and the next trick's lead depends on who won this one, the choices change the outcome. Seats alternate across deals, so neither seat has a lasting edge.
- **skill_sensitive**: weak. Card counting, tempo and timing declarations are real skills. But the deal decides a lot. Holding three Tens or a Napoli is worth 3 points out of only 11 per deal, and the talon draws are blind. Over the short match a platform can host (a 31-point game would take many deals), luck in a two-player deal is large.
- **headroom**: good. Tracking which high cards have gone and planning when to give up the lead are learnable but not solved. Playing for the last trick and choosing when to declare also have depth. A weak player still wins some tricks and scores card points.
- **reasoning_dependent**: good. Hands and talon are hidden. A player must infer the opponent's holdings from what they follow with or discard, from what they draw and from their declarations. Once the talon is empty, the game rewards exact counting and planning several tricks ahead.
- **verifiable**: good. Trick winners, card points, last-trick bonus and declaration bonuses are all arithmetic. Rounding fractions down is also arithmetic, though fiddly. Partnership 'gestures' in the four-player game are not verifiable.
- **fits_platform**: weak. The game is turn-based and text-only, but it does not fit as written. A race to 31 or 41 can run to hundreds of tricks, far over 40 rounds. Declarations can be made repeatedly with reused cards and need open-ended bookkeeping. The four-player variant relies on physical signalling. The 3- and 4-player variants add discards and partnerships the limits cannot carry.

## Problems

- Match length: playing to 31 or 41 points needs many deals of 16 tricks, far beyond 40 rounds.
- Luck: in a short two-player match the deal (especially being dealt a declaration set) and blind talon draws swamp skill.
- Fractional scoring with rounding after each deal is awkward to track and hides small skill differences.
- Declarations can be repeated without limit and cards reused, which needs heavy bookkeeping. There is also no real decision in them: declaring at the first chance is always right.
- The 3- and 4-player variants rely on discards, partnerships and physical gestures that the engine cannot verify or carry within the limits.

## Changes

- Remove the Sevens and Eights to give a 24-card deck. Deal 6 cards each with a 12-card talon. Play exactly three deals of 12 tricks: 36 rounds, each round one trick. (fixes: Match length: playing to 31 or 41 points needs many deals of 16 tricks, far beyond 40 rounds.): Sevens and Eights are worth nothing, so the points per deal are unchanged. Three shorter deals average out more luck than one long one and fit within 40 rounds.
- The top card of the talon is always face up. The trick winner takes that visible card; the loser takes the next card, which only the loser sees. (fixes: Luck: in a short two-player match the deal (especially being dealt a declaration set) and blind talon draws swamp skill.): Each trick becomes a contest for a known prize. A player must judge whether winning is worth the card it costs, and can partly track what the opponent drew. Blind luck turns into a decision.
- Keep all points in thirds (Ace 3, Ten/Nine/King/Ober/Unter 1, last trick 3, declarations 9 or 12) with no rounding. The match winner is the higher total in thirds over the three deals. (fixes: Fractional scoring with rounding after each deal is awkward to track and hides small skill differences.): Exact integers are simple to track, and small skill edges count instead of vanishing in rounding.
- Each player may declare at most once per deal. A player may do so only while on lead after winning the previous trick. All qualifying sets in hand at that moment score, and their cards are shown to the opponent. (fixes: Declarations can be repeated without limit and cards reused, which needs heavy bookkeeping. There is also no real decision in them: declaring at the first chance is always right.): Timing becomes a real choice. Declaring early banks the bonus but reveals your high cards. Waiting may let a three-set grow into a four-set or add a Napoli from the talon, but you risk losing the lead or the cards. This keeps the original trigger and bookkeeping stays small.
- The first lead alternates between deals. In deal 3 the player currently behind leads first (player 2 if tied). (fixes: Luck: in a short two-player match the deal (especially being dealt a declaration set) and blind talon draws swamp skill.): This removes any seat edge and gives the trailing player a small tempo chance, without deciding anything by itself.
- Fix the game at exactly two players. (fixes: The 3- and 4-player variants rely on discards, partnerships and physical gestures that the engine cannot verify or carry within the limits.): The two-player base is the core of Trischettn. The 3- and 4-player variants need discards, partnerships and gestures that cannot be built or verified.

## Kept from the original

- No trumps, with the rank order 10, 9, Ace, King, Ober, Unter within each suit.
- A player must follow suit if able, and the highest card of the led suit wins the trick.
- The trick winner draws from the talon first and leads next. Once the talon is empty, the hands are played out.
- The original card values (Ace 1 point, picture cards and Tens/Nines 1/3 point each, last trick 1 point), kept exactly in thirds.
- The original declarations (three or four Tens, Nines or Aces; Napoli), made when on lead after winning a trick, with cards usable in several sets.

## The variation's rules

DECK. 24 cards in four suits (Hearts, Bells, Leaves, Acorns), each with Ten, Nine, Ace, King, Ober and Unter. Within a suit the trick-taking order from high to low is Ten, Nine, Ace, King, Ober, Unter. There are no trumps.

CARD VALUES, in thirds of a point. Ace = 3. Ten, Nine, King, Ober and Unter = 1 each. Winning the last (12th) trick of a deal = 3. Each deal therefore has 35 card-and-last-trick thirds.

MATCH. Exactly three deals of 12 tricks each, 36 tricks in all. Each trick is one round.

DEALING. At the start of each deal, shuffle the 24 cards. Deal 6 cards to each player, face down; each player sees only their own hand. The remaining 12 cards form the talon in a fixed shuffled order. The top card of the talon is turned face up and shown to both players. Each player's 'declared this deal' mark is cleared.

FIRST LEAD. Player 1 leads the first trick of deal 1, and player 2 leads the first trick of deal 2. In deal 3, the player with the lower match total leads first; if the totals are tied, player 2 leads.

EACH TRICK.
(1) Both players are shown: their own hand, the face-up talon card (if any), the number of cards left in the talon, the current scores, and every card played so far this deal.
(2) Declaration option. The leader may declare if all three hold: the leader won the previous trick of this deal (so never on the first trick of a deal), the leader has not yet declared this deal, and the leader holds at least one qualifying set. The qualifying sets are:
- three Tens, three Nines or three Aces = 9 thirds;
- all four Tens, Nines or Aces = 12 thirds, instead of the 9 for three of that rank;
- a Napoli, meaning the Ten, Nine and Ace of one suit = 9 thirds per suit.
One card may count in several sets. If the leader declares, every qualifying set in the hand at that moment is scored to the leader's deal points, and the cards forming those sets are shown to the opponent. A player can declare at most once per deal.
(3) The leader plays any card from hand face up.
(4) The follower plays a card. If the follower holds a card of the led suit they must play one; otherwise they may play any card. Only legal cards are offered.
(5) The higher card of the led suit wins the trick. The winner adds the values of both cards to their deal points. If this is the 12th trick, the winner also adds 3.
(6) If the talon is not empty, the trick winner takes the face-up talon card into hand. The loser then takes the next talon card into hand; only the loser sees it. If cards remain, the new top card is turned face up. Talon draws happen after each of the first 6 tricks of a deal. After that the hands are played out.
(7) The trick winner leads the next trick.

END OF DEAL. After the 12th trick, each player's deal points (cards, last trick and any declaration) are added to their match total, and both totals are announced.

Objective: After the third deal, the player with the higher match total in thirds wins. Equal totals are a draw.

Expected effect: Each trick becomes a trade-off between the cards on the table and the visible talon card. Players will sometimes throw a trick to keep a Ten, or spend a high card to grab a face-up Ace or a card that completes a set. One declaration per deal, tied to winning the lead, creates real timing decisions. A player can bank a three-set now and reveal it, or hold on hoping to draw the fourth or a Napoli and risk losing the lead or the cards. Revealed declarations, follow-suit failures and the known talon cards give rich material for inference, and the end of each deal rewards exact counting. Three deals with alternating and catch-up leads reduce both seat and deal luck. No talk phase is needed with two players.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
