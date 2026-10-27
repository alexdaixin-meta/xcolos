# Variation: Decrypto Duel

Two teams of two each hold four secret keywords. Each round both Encryptors secretly choose a code and give meaning-only clues, which are revealed at the same time. Every player then guesses at once: Decoders decode their own team's code, and Encryptors try to intercept the other team's. Two Interceptions win, two Miscommunications lose, and the game lasts at most 8 rounds.

Players: 4 to 4, best with 4

## Review of the original

Decrypto is a team word game. Each team has four secret numbered keywords, and each round an Encryptor gives clues to a secret 3-digit code. Teammates try to decode it while the opposing team tries to intercept it, using the growing public record of past clues. Two Interceptions win the game; two Miscommunications lose it.

- **non_degenerate**: good. Every simple policy loses. A Decoder who always guesses 1-2-3 is right 1 time in 24 and picks up Miscommunications within two rounds. An Encryptor who always gives the most obvious clue gets intercepted once the history builds, because opponents map clue to number. One who gives obscure clues gets miscommunicated. One who repeats the same code pattern gets intercepted. In the original, White reading first is a small edge. The previous variation removed it by revealing both teams' clues at once, and that is kept.
- **skill_sensitive**: good. The core decision is to pitch a clue clear enough for a teammate but not for opponents who see every past clue. Its quality depends on modelling both audiences. The only luck is which keywords are dealt; codes are chosen, not drawn. A shared list of comparable concrete nouns keeps the deal roughly even.
- **headroom**: good. A weak team can still decode plain clues and score correct decodes. A strong team plans across rounds: it rotates clue angles per keyword so the public history stays ambiguous, and it exploits patterns in the opponent's history to intercept. No fixed clue policy is optimal.
- **reasoning_dependent**: good. The opposing keywords are hidden. Interception means inferring them from accumulated clue-to-number pairs and the opponent's habits. Encrypting means predicting what the opponent has already inferred. This is inference from limited information plus planning over several rounds.
- **verifiable**: weak. Token counting is arithmetic, but clue validity needs a ruling. That is allowed as a referee rule check. The previous variation's text was still ambiguous: an invalid clue could cost one or two Miscommunications, which can decide the game. 'Private information' was undefined, and the word list was missing.
- **fits_platform**: good. The game is turn-based and text-only, with no board. Hidden team hands and simultaneous polls are supported. Eight rounds at most. Fits within 13 steps, 2 choice steps and about 16 attributes once the rules are made unambiguous.

## Problems

- Invalid-clue penalty was double-counted or unclear: step 3 gave 1 Miscommunication and also said the decode 'counts as failed', which step 6 might penalise again. Two Miscommunications end the game.
- It was unclear whether a team with an invalid answer still gains a correct decode if its Decoder guesses right. That count is a tiebreaker.
- It was unclear whether an invalid team's true code can still be intercepted.
- Guesses were not required to use three different digits, and a malformed guess had no defined outcome.
- The shared word list was never given, so the deal could not be built.
- 'Private information' was undefined in a game whose keywords are themselves private, so the clue rule could not be applied consistently.
- In round 1, Encryptors are asked for interception guesses that are not scored; whether they must answer was unclear.

## Changes

- An invalid Encryptor answer costs exactly 1 Miscommunication in total. That team's Decoder guess is ignored, its decode is not scored in step 6, and its correct-decode count does not change. (fixes: Invalid-clue penalty was double-counted or unclear: step 3 gave 1 Miscommunication and also said the decode 'counts as failed', which step 6 might penalise again. Two Miscommunications end the game.): Removes the one-or-two-token ambiguity that could decide the game.
- State explicitly that an invalid team's decode is skipped entirely, so a correct guess by its Decoder earns nothing. (fixes: It was unclear whether a team with an invalid answer still gains a correct decode if its Decoder guesses right. That count is a tiebreaker.): Makes the tiebreaker count well defined.
- From round 2 on, an invalid team's true code can still be intercepted normally. If the code itself is malformed, it cannot be matched, so no interception is possible. (fixes: It was unclear whether an invalid team's true code can still be intercepted.): Defines the interaction, and keeps an invalid clue costly without giving opponents a free token.
- Every guess must be three different digits from 1 to 4. Any other guess, or no answer, counts as a wrong guess. (fixes: Guesses were not required to use three different digits, and a malformed guess had no defined outcome.): Gives every possible answer a defined result.
- Supply a fixed list of 40 concrete nouns. At setup, 8 different words are dealt at random, 4 per team. (fixes: The shared word list was never given, so the deal could not be built.): The deal becomes buildable with list operations. Comparable nouns keep teams roughly even.
- Define forbidden clue content precisely. A clue may not use personal or shared experience between teammates, refer to the game itself (seats, rounds, codes, numbers, earlier clues), or refer to the other team's words. Only the general-knowledge meaning of the team's own keyword is allowed. (fixes: 'Private information' was undefined in a game whose keywords are themselves private, so the clue rule could not be applied consistently.): Gives the referee a clear test.
- In round 1, Encryptors still answer the guess poll, but their interception guesses are ignored. (fixes: In round 1, Encryptors are asked for interception guesses that are not scored; whether they must answer was unclear.): Keeps the step list flat and the same every round.

## Kept from the original

- Two teams with four secret numbered keywords that stay the same all game.
- An Encryptor gives one meaning-only clue per digit of a 3-digit code; no clue may be reused.
- Teammates decode while opponents intercept, using the public history of clues and true codes.
- Two Interceptions win and two Miscommunications lose; Encryptors rotate.
- No interception in round 1.
- From the previous variation: simultaneous clue reveal (no seat edge), an 8-round cap and the tiebreak ladder.

## The variation's rules

SETUP. There are four players. Seats 1 and 2 form Team White; seats 3 and 4 form Team Black.

The word list is these 40 words: apple, anchor, bridge, candle, castle, cloud, crown, desert, diamond, dragon, drum, eagle, engine, feather, forest, ghost, glacier, hammer, island, jungle, key, ladder, lantern, mirror, moon, needle, ocean, piano, pirate, pyramid, rocket, saddle, shadow, ship, snake, spider, sword, tiger, volcano, whistle.

At the start, the engine shuffles the list and deals 8 different words: the first 4 to White as keywords 1, 2, 3, 4 and the next 4 to Black as keywords 1, 2, 3, 4. A team's keywords are shown only to its two members and never change.

The engine tracks for each team: Interceptions (start 0), Miscommunications (start 0) and Correct Decodes (start 0). It also keeps a public history listing, for every finished round, each team's three clues and true code. All counters are public.

ROLES. In odd rounds (1, 3, 5, 7), seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders. In even rounds (2, 4, 6, 8), seats 2 and 4 are Encryptors and seats 1 and 3 are Decoders.

CLUE RULES. A clue is one word or a short phrase. It must point to the matching keyword of the clue-giver's own team by its general meaning only. A clue may NOT:
(1) point to the keyword by spelling, letters, sound, rhyme, length or alphabetical position;
(2) contain the keyword, a part of it, or a word with the same root;
(3) repeat, word for word, a clue the same team used in an earlier round;
(4) refer to the game itself: seats, rounds, codes, digits or keyword numbers, earlier clues, or the other team's words;
(5) refer to private information, meaning anything not available from general knowledge, such as personal experiences, in-jokes or anything known only to the teammates.

EACH ROUND:
1. ANNOUNCE. The engine announces the round number and who is Encryptor and Decoder on each team.
2. ENCRYPT (simultaneous; Encryptors only). Each Encryptor privately submits a secret code and three clues. The code is three different digits from 1 to 4, in any order (for example 3-1-4). The three clues are given in code order: the first clue for the first digit's keyword, and so on.
3. CHECK. For each team, a referee rules the Encryptor's answer valid or invalid. It is valid only if the code is three different digits from 1 to 4 and all three clues obey the clue rules. If it is invalid, that team gains exactly 1 Miscommunication now. Its Decoder's guess this round will be ignored: step 6 does not score that team's decode at all, gives no further Miscommunication and adds no Correct Decode.
4. REVEAL. Both teams' clues are shown to all four players at once. Codes stay secret.
5. GUESS (simultaneous; all four players). Each Decoder submits a guess of their own team's code. Each Encryptor submits a guess of the opposing team's code. A guess must be three different digits from 1 to 4. Any other answer, or no answer, counts as a wrong guess. In round 1, Encryptors still answer, but their guesses are ignored.
6. SCORE.
   (a) DECODE, only for a team whose answer was valid in step 3. If the Decoder's guess equals the team's true code digit by digit in order, the team gains 1 Correct Decode. Otherwise it gains 1 Miscommunication.
   (b) INTERCEPT, from round 2 on, for both teams, whether or not the opposing answer was valid. If an Encryptor's guess equals the opposing team's true code digit by digit in order, the Encryptor's team gains 1 Interception. A code with repeated or out-of-range digits can never be matched.
7. HISTORY. Both true codes are shown to everyone and added to the public history beside that round's clues.
8. END CHECK. The game ends now if any team has 2 or more Interceptions or 2 or more Miscommunications, or if round 8 has just finished. Otherwise the next round begins.

There is no discussion phase. Teammates may communicate only through official clues.

Objective: When the game ends, apply these rules in order:
1. If exactly one team has 2 or more Interceptions together with fewer than 2 Miscommunications, that team wins.
2. Otherwise, if exactly one team has 2 or more Miscommunications, the other team wins.
3. Otherwise (both teams triggered an end condition in the same round, or round 8 ended):
   (a) the team with the higher net score (Interceptions minus Miscommunications) wins;
   (b) if tied, the team with more Interceptions wins;
   (c) if still tied, the team with more Correct Decodes wins;
   (d) if still tied, the game is a draw.

Expected effect: Every penalty and edge case now has exactly one outcome, so the game can be built and played without interpretation. Play centres on two-audience clue pitching. Early rounds favour clear clues; as the history accumulates, Encryptors must vary their angle on each keyword while opponents piece together the hidden words to intercept. An invalid clue costs exactly one token, which makes rule-bending a real but bounded risk. Talk is left out: the only conflict is between the teams, there is nothing to negotiate in this zero-sum duel, and talk between teammates would bypass the clue channel that is the whole game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 8 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
