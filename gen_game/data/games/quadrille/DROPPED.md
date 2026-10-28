# Dropped: too complex

no design got past the critic in 3 rounds; still failing playable: LIMITS: Steps, counted with `when`-gated steps in one flat list: auction reset, deal, bid poll, resolve, declare, announce/partner = 6; trick lead, 3 follows, winner = 5; end of hand count/score, codille, reveal = 3 or more. That is about 1

## The last variation tried

Petite Quadrille III: A four-player, 8-hand miniature of Quadrille played with a 20-card pack. Each hand begins with an auction round, followed by 4 tricks. Four cards lie unseen in a talon. The Taker names trump and calls a King whose holder is a secret partner, or goes solo. Spadille, Manille and Baste are the top trumps.

## What was tried

- design 1: the critic found it not sound (balanced, playable, reasoning_over_luck)
- design 2: the critic found it not sound (playable)
- round 1: behavior problem; triage said fix_game: Two independent tests show the follow poll offering too few cards. In one a seat with no club is denied the Jack of Hearts when Baste is led; in the other a sea
- round 1: build problem; triage said fix_game: Each attempt failed on a different coder mistake: bookkeeping fields shown to players, a list comprehension using range (not an allowed function), reading `you`
- round 1: behavior problem; triage said fix_game: All three failures point at what the game offers and records during the declaration and the follow. The Taker's trump choice did not end up as the intended suit
- design 1: the critic found it not sound (playable, reasoning_over_luck)
- design 2: the critic found it not sound (playable)
- design 3: the critic found it not sound (playable)

To bring the game back, clear `dropped` in its inventory record.
