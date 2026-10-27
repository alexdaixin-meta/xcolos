# Variation: Decrypto: Points Race

Two teams of two hide four keywords each. Each round, an Encryptor chooses a secret 3-digit code and gives three one-word clues for it. Teammates score by decoding the code, and opponents score more for intercepting it. After 8 rounds the higher team total wins.

Players: 4 to 4, best with 4

## Review of the original

Decrypto is a team word game. Each team privately holds four numbered keywords. Each round a rotating Encryptor gives three meaning-based clues for a secret 3-digit code so that teammates can decode it while the opposing team, who see only the public clue history, try to intercept it; teams race to 2 Interceptions or away from 2 Miscommunications.

- **non_degenerate**: bad. In the previous build every match, random or thoughtless, ended as a four-seat draw: first@seat1, last@seat1 and the others all drew 60 of 60. The token race is symmetric and both teams trip the same trigger in lockstep. Interception needs an exact 3-digit hit (1 in 24 at random), so random teams almost never intercept, both rack up Miscommunications, and the draw rule fires. Nothing a player chose moved the result.
- **skill_sensitive**: weak. In the tabletop game, skill (clues that are clear to teammates and obscure to rivals, and reading the opponents' clue history) dominates. In the built version, all-or-nothing exact-code scoring and a shared draw trigger meant better guessing almost never changed the token count, so skill could not show.
- **headroom**: good. Pitching clues at the right obscurity, tracking which clue themes have leaked for each keyword number, and spotting an opponent's code habits can improve almost without limit. A weak team can still decode its own clues.
- **reasoning_dependent**: good. Keywords are hidden from the opponents. Intercepting requires inferring the keyword behind each number from the accumulating clue history, and encrypting requires modelling what the teammate knows versus what the rivals can infer.
- **verifiable**: weak. The token outcomes are arithmetic, but the core rule that clues point 'by meaning only, never by spelling or position' needs a judge. The platform cannot decide whether a clue relates to its keyword.
- **fits_platform**: weak. The game is text-only and turn-based. However, its variable team sizes, sequential announce order, open-ended length until a token race resolves, and judge-dependent clue legality all strain the engine. The token race also produced only draws.

## Problems

- P1: The symmetric token race (2 Interceptions win, 2 Miscommunications lose) makes both teams hit the same trigger together, so every match drew: choices did not change the result.
- P2: Scoring is all-or-nothing on the exact 3-digit code, so better-than-random guessing almost never moves the score and skill cannot be seen.
- P3: There is no tiebreak, so equal token counts always end in a draw.
- P4: The clue rule 'by meaning only' needs a judge and cannot be checked by arithmetic.
- P5: A random code card per team per round needs two random draws per round, above the platform limit. It also adds luck without adding a decision.
- P6: Open-ended length and sequential announcing (White first, Black's intercept announced first) give an order asymmetry and an unpredictable game length.
- P7: Interception and decoding are worth the same token weight, so the encryptor's core tension (be clear to the teammate, opaque to rivals) is not sharply priced.

## Changes

- Replace the token race with a fixed 8-round game in which teams earn points every round, and the higher team total wins. (fixes: P1): Every round's guesses now move the score, so totals diverge and results vary with play instead of collapsing into a shared trigger.
- Score guesses position by position. A decode earns 1 point per correctly placed digit plus 1 bonus for the exact code (max 4). An interception earns 1 point per correctly placed digit plus 2 bonus for the exact code (max 5). (fixes: P2): Partial credit rewards better-than-random inference every round. The larger exact-interception bonus makes leaking a whole code costly, which prices the clear-versus-obscure tension.
- Break ties first by total exact interceptions, then by total exact decodes; only then is the game a draw. (fixes: P3): Ties now go to the team that showed more inference, so draws are rare.
- Use only arithmetic clue checks: one word, 2-20 letters, does not contain and is not contained in any of the team's own keywords (ignoring case), and does not repeat any earlier clue by either team. An invalid clue set makes that team's decode score 0 and gives the opponents 3 points. (fixes: P4): The meaning check is removed. Clue legality is computable, and breaking the rules has a fixed, arithmetic cost.
- The Encryptor chooses the team's secret code from the 24 possible codes, instead of drawing a code card. (fixes: P5): This removes the per-round random draws. It also adds a decision: a predictable code pattern (always the first code) is intercepted from the public history, so code choice becomes opponent modelling.
- Make every step simultaneous: both Encryptors choose codes, both write clues, then all four players guess at once. Fix the game at 4 players, two teams of 2, with roles alternating each round. (fixes: P6): This removes the read-first and announce-first order advantage, gives every seat the same position, and makes the length fixed and short.
- In each guess step, each team's Decoder decodes the own team's clues while that team's Encryptor intercepts the opponents' clues. Interceptions score nothing in round 1, as in the original. (fixes: P7): Every player has a reasoning task each round. Separating the two jobs makes the cost of a leaky clue (opponent points) and the value of a clear clue (own points) directly comparable.

## Kept from the original

- Two teams, each privately holding four numbered keywords that the other team never sees.
- A rotating Encryptor who gives three one-word clues for a 3-digit code made of distinct digits 1-4.
- Teammates decode while opponents try to intercept, using the public history of clues and revealed codes.
- No clue may ever be reused.
- No interception scoring in round 1.
- True codes are revealed after each round, so the clue history becomes a growing puzzle for the opponents.
- The central tension: be clear to your partner, opaque to your rivals.

## The variation's rules

SETUP. Four players: seats 1 and 2 form team Red, seats 3 and 4 form team Blue. Eight distinct keywords are drawn at random from a fixed list of 40 common nouns. The first four go to Red, numbered 1-4; the next four go to Blue, numbered 1-4. Each team's keywords are shown only to that team's two players. Each team starts with 0 points, 0 exact interceptions and 0 exact decodes. A public history lists, for each team and each past round, its three clues and its revealed true code.

CODES. A code is three different digits from 1-4 in order. There are 24 codes, offered in this order: 123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432.

ROLES. In odd rounds, seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders. In even rounds, the roles swap.

EACH ROUND (8 rounds):
1. Roles for the round are announced.
2. Code choice (simultaneous, secret): each Encryptor chooses one of the 24 codes for their team. No one else sees it.
3. Clues (simultaneous): each Encryptor writes three clues, one per digit of the code in order. Clue 1 should point to the team keyword numbered by the first digit, and so on.
4. Clue check. A clue is valid only if all of these hold: it is a single word with no spaces; it is 2-20 letters long; ignoring case, it does not contain any of the team's own four keywords and is not contained in any of them; it is not identical, ignoring case, to any clue either team has given in an earlier round. A team with any invalid clue this round is marked invalid.
5. All six clues are shown to everyone.
6. Guesses (simultaneous): each Decoder chooses one of the 24 codes as a decode of their own team's clues. Each Encryptor chooses one of the 24 codes as an interception of the opposing team's clues.
7. Decode scoring, for each team that is not invalid: the team gains 1 point for each position (first, second, third) where the Decoder's guess matches the team's true code. If all three match, the team gains 1 more point and 1 exact decode. A team marked invalid gains 0 decode points this round.
8. Interception scoring, rounds 2-8 only: each team gains 1 point for each position where its Encryptor's interception matches the opposing team's true code. If all three match, the team gains 2 more points and 1 exact interception. In round 1 interceptions score nothing.
9. Invalid penalty: if a team is marked invalid, the opposing team gains 3 points.
10. Both true codes, all guesses and all points gained are announced, and the clues and codes are added to the public history.

No other talk is allowed. The clues are the only communication.

END. After round 8 the game ends.

Objective: The team with more points after round 8 wins, and both of its players win. If points are tied, the team with more exact interceptions wins. If still tied, the team with more exact decodes wins. If still tied, the game is a draw.

Expected effect: Scores now diverge every round, so random play gives varied winners and choices decide results. A thoughtless policy that always picks the first code (123) and always guesses 123 decodes perfectly, but from round 2 a thinking opponent intercepts it exactly for 5 points a round while decoding its own varied codes for 3-4. The thoughtless team falls about 4 points behind per round, so it loses; the same holds for always-last. Strong teams vary their codes, give clues tied to their private keywords but phrased away from earlier themes for the same number, and mine the opponents' history to intercept. The larger exact-interception bonus punishes transparent clues, and decode points punish over-obscure ones. Talk is left out: the two teams are strictly opposed, and teammates sharing information outside the clues would remove the puzzle.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 8 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
