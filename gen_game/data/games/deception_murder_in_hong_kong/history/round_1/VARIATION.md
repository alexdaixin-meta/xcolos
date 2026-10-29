# Variation: Deception: Five Clues

A text-only hidden-role deduction game. A mute Scientist guides the Investigators to the Murderer's secret Clue and Means through five constrained Scene-tile markers. The Murderer and Accomplice mislead, the Witness hints carefully, and each player has one accusation.

Players: 6 to 8, best with 7

## Review of the original

A hidden-role deduction game. A secret Murderer picks one of their own Clue cards and one of their own Means cards as the solution. A public Forensic Scientist, who knows the answer but cannot speak, guides the Investigators only by placing markers on fixed-option Scene tiles. Players discuss and may each spend one badge on a single accusation. A correct accusation wins for the Investigators unless the Murderer then identifies the Witness.

- **non_degenerate**: good. Simple policies all lose. Always-pass Investigators lose because the Murderer wins by default. A blind accusation hits 1 of about 30 to 40 valid Clue+Means pairs. A Scientist who marks options at random gives no information. A silent Murderer side cannot steer suspicion. The Witness rule also stops Investigators from loudly broadcasting what they know.
- **skill_sensitive**: good. Outcomes depend on three skills: how well the Scientist encodes the solution in constrained markers, how well Investigators decode them, and how well the Murderer side misleads. The only luck is the card deal and which tiles appear, and a good Scientist works around both.
- **headroom**: good. Choosing the tile option that points uniquely at one pair among many is open-ended. So is telling genuine reasoning from planted reasoning, and so is the Witness hinting without exposing themselves. Weak Investigators still sometimes stumble on the answer, so weak players can score.
- **reasoning_dependent**: good. Roles and the solution are hidden. Players must infer the solution from indirect markers and infer who is lying from talk. The Murderer must infer the Witness from behaviour.
- **verifiable**: good. An accusation is correct exactly when the named Clue and Means match the secret pair. The Witness guess is a direct identity match. No judgement is needed.
- **fits_platform**: bad. It relies on physical and real-time elements: an eyes-closed setup, physical marker placement, 30-second timed presentations made in turn, optional tile replacement, optional roles, and up to 12 players. With 4 Clue and 4 Means cards each, that is up to 88 cards, far beyond the attribute limit.

## Problems

- Timed 30-second presentations and open-ended discussion are real-time; the engine is turn-based.
- The eyes-closed secret setup and the Scientist's role-revealing gestures are physical actions.
- 4 Clue + 4 Means cards for up to 11 players creates far more state than the 20-attribute limit allows.
- Optional Accomplice/Witness and up to 12 players make the role set ambiguous and the step count large.
- Turn-order presentations let later speakers copy or react to earlier ones, so the first speaker anchors everyone.
- Optional tile replacement plus 6 tiles a round needs more choice steps and random draws per round than allowed.
- Rules for a wrong accusation's announcement, and for murderer-side accusations, are informal.

## Changes

- Replace timed in-turn presentations with one written message per round from every player except the Scientist, followed by an accusation poll. (fixes: Timed 30-second presentations and open-ended discussion are real-time; the engine is turn-based.): This is turn-based and text-only.
- The engine deals roles privately. The Murderer chooses the solution as a private choice. The engine privately tells the Accomplice and the Witness who is on the Murderer side. (fixes: The eyes-closed secret setup and the Scientist's role-revealing gestures are physical actions.): Reproduces the secret setup without physical gestures.
- Each non-Scientist holds 2 Clue words and 2 Means words dealt from fixed lists, instead of 4 and 4. (fixes: 4 Clue + 4 Means cards for up to 11 players creates far more state than the 20-attribute limit allows.): Keeps the state within limits while leaving 4 candidate pairs per player and 20 to 28 candidates in total.
- Fix the player range at 6 to 8. The role set is always Scientist, Murderer, Accomplice and Witness, with the rest Investigators. (fixes: Optional Accomplice/Witness and up to 12 players make the role set ambiguous and the step count large.): Gives one unambiguous role table and a bounded state.
- Use 5 rounds with one Scene tile per round. Rounds 1 and 2 use the fixed Cause of Death and Location tiles. Rounds 3 to 5 each draw one tile from a deck of 6. There is no replacement. (fixes: Optional tile replacement plus 6 tiles a round needs more choice steps and random draws per round than allowed.): One Scientist choice and at most one random draw per round, while still giving 5 constrained hints.
- Every accusation is announced with its result. Any correct accusation counts as solved, whoever made it. An accusation naming a Clue and a Means from different players is automatically wrong. (fixes: Rules for a wrong accusation's announcement, and for murderer-side accusations, are informal.): Makes resolution pure arithmetic and makes wrong guesses informative for later rounds.
- Talk is simultaneous: all messages are written without seeing the others, then shown together. (fixes: Turn-order presentations let later speakers copy or react to earlier ones, so the first speaker anchors everyone.): Every player commits to a reading independently.

## Kept from the original

- A mute Forensic Scientist who knows the answer and can only mark one option on fixed-option Scene tiles.
- A secret Murderer whose solution is one of their own Clues plus one of their own Means.
- An Accomplice who knows the solution and misleads.
- A Witness who knows the culprits but not the solution and must hint without being exposed.
- One badge per player for a single accusation.
- The Witness rule: a correct accusation can be stolen by the Murderer naming the Witness.
- The Murderer side wins if the case is never solved.

## The variation's rules

ROLES. One player is publicly the Forensic Scientist (seat 1). The engine secretly and randomly deals the other players these roles: 1 Murderer, 1 Accomplice, 1 Witness, and Investigators for the rest (2, 3 or 4 Investigators with 6, 7 or 8 players). The Murderer and Accomplice are the Murderer side. The Scientist, Witness and Investigators are the Investigator side. The Accomplice is told who the Murderer is. The Witness is told who the Murderer and Accomplice are, but not which of the two is which, and not the solution. The Scientist is told all roles.

CARDS. Every player except the Scientist is dealt, face up for all to see, 2 Clue words from the Clue list and 2 Means words from the Means list, with no repeats.
- Clue list (16): Glove, Train Ticket, Lipstick, Key, Diary, Ring, Cigarette, Phone, Wallet, Photo, Watch, Umbrella, Receipt, Hair, Button, Mask.
- Means list (16): Rope, Poison, Knife, Pillow, Hammer, Pistol, Insulin, Brick, Drowning, Electric Wire, Scarf, Bare Hands, Fire, Bottle, Axe, Car.

SOLUTION. The Murderer privately chooses one of their own 2 Clues as the Key Evidence and one of their own 2 Means as the Means of Murder. The engine then privately tells the Scientist and the Accomplice the solution.

SCENE TILES. Each tile lists 6 options.
- Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident.
- Location: Living Room, Bedroom, Bathroom, Kitchen, Street, Office.
The Deck holds 6 tiles:
- Time of Death: Dawn, Morning, Noon, Afternoon, Evening, Night.
- Weather: Sunny, Stormy, Dry, Humid, Cold, Hot.
- Victim's Build: Large, Thin, Tall, Short, Disfigured, Fit.
- Trace at Scene: Fingerprint, Footprint, Bruise, Blood Stain, Body Fluid, Scar.
- Corpse Condition: Still Warm, Stiff, Decayed, Incomplete, Intact, Twisted.
- Duration of Crime: Instant, Brief, Gradual, Prolonged, Days, Unclear.

BADGES. Every player except the Scientist starts with 1 badge.

EACH ROUND (5 rounds):
1. Tile. In round 1 the tile is Cause of Death. In round 2 it is Location. In rounds 3, 4 and 5, one tile is drawn at random from the Deck and removed.
2. Marker. The Scientist privately chooses exactly one of the tile's 6 options, and the marked option is announced to all. The Scientist may never send any other message.
3. Talk. Every player except the Scientist writes one short message at the same time. All messages are then shown to everyone.
4. Accusation. Every player who still has a badge chooses at the same time either PASS or one accusation: one Clue word and one Means word currently on the table. Anyone who accuses loses their badge.
5. Resolution. Every accusation is announced with its accuser. An accusation is correct only if its Clue is the Key Evidence and its Means is the Means of Murder, and each is announced as correct or wrong. A pair taken from two different players' cards is always wrong. If any accusation is correct, the case is SOLVED and play moves to the Witness Hunt. Otherwise the next round begins.

WITNESS HUNT. When the case is solved, the Murderer privately names one player other than the Scientist, the Accomplice and themself. If that player is the Witness, the Murderer side wins. Otherwise the Investigator side wins.

END. If the case is not solved by the end of round 5, the Murderer side wins.

Objective: Team win, decided purely by matching. If any accusation exactly matches the secret Clue and Means, and the Murderer then fails to name the Witness, the Scientist, the Witness and all Investigators win. If the Murderer names the Witness correctly after a solve, or if no correct accusation happens within 5 rounds, the Murderer and Accomplice win. There are no draws.

Expected effect: The Scientist must choose markers that single out one pair among 20 to 28 candidates using weak tiles. Investigators must decide when to spend their only badge: early guesses are wasteful, but announced wrong guesses prune the candidates for everyone. Talk passes both tests. Players genuinely disagree: the Murderer side wants the wrong pair accused and wants to spot the Witness. A player who simply follows a confident proposal may be following the Accomplice and burn their badge on a decoy. A Witness who steers too openly gets named, which turns a solved case into a loss. Thoughtless policies all lose sometimes: always-pass Investigators lose by default, a random accuser rarely hits, a random Scientist gives no information, and a Murderer who names the Witness at random hits only 1 time in 3 to 5.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 5 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
