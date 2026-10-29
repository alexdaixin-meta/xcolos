# Variation: Growl: Charmed Nights

Hidden werewolves bite one human each night. Humans spend a limited supply of Charms either to cure a bitten human or to calm a suspected wolf. By day they hand out drawn cards and vote to wound suspects, reasoning from anonymous night reports and public tallies.

Players: 5 to 7, best with 6

## Review of the original

Growl is a hidden-role social deduction card game for 4 to 10 players. Players pass Bite, Charm, Wound and Salve cards: openly by day from a shared face-up deck, and face-down to their neighbours by night. Humans turn into werewolves when net Bites reach 3, and the humans win if at least one human is alive after the Final Night.

- **non_degenerate**: bad. In the tested variation, the policy 'wolf always bites the left neighbour' wins most games against both random and sensible humans. Humans cannot discard Bites. A held Charm is forced out each night, and the sender's own net rises. Charms sent to a wolf are lost. Conversion hands the new wolf about 4 Bites of ammunition. Ties go to the wolves, and seats 1 and 2 get extra Day turns. A blind fixed policy should not win this often.
- **skill_sensitive**: weak. Choosing who receives each day card takes skill. Under good play, though, the wolf converts one human by about night 3 and another by about night 7 whatever the humans do, so the role deal largely decides the winner. Human success then depends on Wound cards arriving on human turns.
- **headroom**: weak. The wolf side is close to solved: focus-bite one target and mimic whatever claims the humans make. Human play has little room to improve, because no tool lets good inference change the outcome.
- **reasoning_dependent**: good. Roles are hidden, infection totals are private, and night passes are anonymous, so there is plenty to infer. The weakness is that the inference cannot be acted on effectively.
- **verifiable**: good. Deaths, conversions and the team win all follow from counters and a count of roles. No judge is needed.
- **fits_platform**: weak. Passing cards left and right relies on seat adjacency, and the original has a deck with seeded Night cards. Both cost steps. The previous variation already moved to a random day draw and free targeting, which fits the engine.

## Problems

- P1: Wolves are structurally favoured. Day Bites given to a wolf become ammunition, humans cannot get rid of Bites, and all Bite pressure ends up in humans.
- P2: Protection drains itself. Humans are forced to pass held Charms, a held Charm counts toward the holder's own safety so passing it raises the passer's net, and a Charm sent to a wolf is simply lost.
- P3: Conversion recycles ammunition. A new wolf keeps 3 or more Bites and can spend them all at once.
- P4: Humans have no verifiable tool. Bite claims cannot be checked, the wolf can make the same claims, and a correct suspicion cannot be turned into action.
- P5: The blind 'focus-bite the left neighbour' policy wins most games, so the wolf side needs no inference.
- P6: Lottery outcome. Under good play the team you are dealt decides the result.
- P7: Seat edge. 12 rounds over 5 players gives seats 1 and 2 an extra Day turn.
- P8: The tie rule plus double-rate biting with 2 wolves at 7 players tilts the game further toward the wolves.

## Changes

- Wolves no longer hold Bite ammunition. Each living wolf may bite one target per night. A day Bite card given to a wolf is discarded with no effect, and only the wolf learns this. (fixes: P1): This removes ammunition hoarding and recycling, and makes a day Bite a cost to whoever gives it to a human.
- Charms become something you spend, not something you hold for protection. Holding Charms does not protect you. A Charm passed to a human removes 1 of that human's Bites (minimum 0). A Charm passed to a wolf CALMS it: that wolf's bite tonight is cancelled. No one is ever forced to pass. 'None' is always a legal night action. (fixes: P2): Spending a Charm no longer endangers the spender. A Charm aimed at a wolf is a strong, correct-guess reward instead of a loss. One Charm cancels one Bite, either as a cure or as a block.
- A converted human's Bites reset to 0. They bite once per night like any wolf, starting the following night. (fixes: P3): Conversion no longer delivers a burst of stored Bites.
- After each night, the engine publicly announces two numbers: how many Bites landed on humans, and how many wolves were calmed. (fixes: P4): Each charmer knows their own target, so these totals let humans test claims and narrow down the wolf by arithmetic. They also reveal a conversion when the landed count rises.
- Add a Day accusation vote held at the same moment for everyone. A player named by strictly more than half of the living players takes 1 Wound. Death occurs at Wounds minus Salves of 2 or more. (fixes: P4): Humans get a way to act on their inference. Because a wrong majority wounds a human, a careless vote helps the wolves.
- Re-checked the simple policies under the new rules. Against humans who cure the claimed victim, block suspects and vote, focus-biting fails: one cure per night keeps the victim below 3 Bites, about 13 Charms against 12 bites. Against random humans it still wins. (fixes: P5): The fixed wolf policy no longer dominates. It loses to thoughtful play, so the gap between good and careless players returns.
- Tuned the supply of resources. Humans start with 2 Charms each, or 3 at 7 players. Day card odds are Wound 30%, Charm 30%, Salve 25%, Bite 15%. There is 1 wolf at 5 or 6 players and 2 at 7. (fixes: P6): Human cures and blocks roughly match wolf bite volume, so under good play neither side should be favoured by the deal; my estimate is each side wins 40 to 60%.
- The number of rounds is twice the player count: 10, 12 or 14. (fixes: P7): Every seat gets 2 Day turns while all players are alive.
- At 7 players the second wolf is offset by 3 starting Charms per human. The wolves-win-ties rule is kept only because humans now have cures, blocks and votes. (fixes: P8): Offsets double-rate biting without making the wolf side hopeless at 5 players, where the wolves need 1 conversion plus 1 human death.

## Kept from the original

- Hidden werewolves among humans, with infection by accumulated Bites leading to secret conversion into a wolf
- Bite, Charm, Wound and Salve as the four kinds of card, with public Wounds and Salves and private Bites
- A Day phase in which a drawn card is announced and must be given to another player in public
- A silent Night phase of anonymous face-down passing
- Death at 2 net Wounds, team win decided by counting living roles at the end, and converted players switching teams

## The variation's rules

SETUP
- Players sit in a fixed order, numbered 1 to N, where N is 5, 6 or 7.
- Roles are dealt at random and told privately. There is 1 wolf with 5 or 6 players and 2 wolves with 7. Wolves are not told who the other wolf is. Everyone else is a human.
- Each player has four counters:
  - Bites: private; meaningful only for humans.
  - Charms: private.
  - Wounds: public.
  - Salves: public.
- All counters start at 0, except that each human starts with Charms 2 (Charms 3 at 7 players).
- The game lasts 2 x N rounds: 10, 12 or 14. Each round has a Day and a Night.

DAY
1. Active player. Living players take the active role in seat order, skipping dead players. Round 1 starts with player 1.
2. Draw. The engine draws one card at random and announces it to everyone:
   - Wound 30%
   - Charm 30%
   - Salve 25%
   - Bite 15%
3. Talk. Every living player writes one short message at the same moment, without seeing the others. Then all messages are shown to everyone.
4. Give. The active player gives the card to another living player (not themselves). Everyone sees who receives it.
   - Wound or Salve: add 1 to the recipient's counter, in public.
   - Charm: the recipient gains 1 Charm.
   - Bite: a human recipient gains 1 Bite. If the recipient is a wolf, the card is discarded with no effect, and only that wolf learns this.
5. Accusation. All living players vote at the same moment. Each names one other living player, or 'nobody'. If one player is named by strictly more than half of the living players, that player gains 1 Wound. The vote counts are announced.
6. Death check. A player whose Wounds minus Salves is 2 or more dies. Their role is revealed, and they take no further part. If no wolves are alive, the humans win immediately.

NIGHT (no messages)
7. Action. Each living player secretly chooses one action:
   - 'Bite X': wolves only. A human who chooses Bite is treated as choosing None.
   - 'Charm X': requires at least 1 Charm. The sender loses 1 Charm. If the sender has no Charm, this is treated as None.
   - 'None'.
   X must be another living player.
8. Calm. Every wolf targeted by at least one Charm is calmed: its Bite tonight is cancelled. Charms aimed at wolves are used up.
9. Bites land. Each uncancelled Bite on a human adds 1 to that human's Bites. A Bite aimed at a wolf has no effect.
10. Cures. Each Charm on a human removes 1 of that human's Bites, but never below 0.
11. Private reports. Each player is told privately how many Bites landed on them and how many Charms they received, never who sent them. A wolf that was calmed learns that it was calmed.
12. Public report. The engine announces two numbers: the Bites that landed on humans tonight, and the wolves calmed tonight.
13. Infection. Any living human with Bites of 3 or more becomes a wolf. They are told privately. Their Bites reset to 0 and they keep their Charms. From next night on, they may Bite. Wolves never change back.

END CHECKS (after every Night)
14. If every living player is a wolf, the wolves win.
15. If two or fewer players are alive, the game ends and is scored.
16. After the Night of the final round, the game ends and is scored.

SCORING
Count living wolves and living humans. If living wolves are at least as many as living humans, the wolf team wins. Otherwise the human team wins. Each player belongs to the team of their role when the game ends, so converted humans win with the wolves.

Objective: This is a team win decided by counting roles. The humans win at once if no wolf is alive after a Day death check. The wolves win at once if every living player is a wolf after a Night. Otherwise, when the game ends (final Night, or two or fewer players alive), the wolf team wins if living wolves are at least as many as living humans, and the human team wins otherwise. There are no draws. Each player wins or loses with the team of their role at game end.

Expected effect: One Charm now cancels one Bite, either as a cure on the victim or as a block on the wolf. The game therefore turns on whether humans place their scarce Charms and votes accurately.

The night tallies give verifiable clues. If I charmed X and one wolf was calmed, X is under suspicion. A rise in landed Bites reveals a conversion.

Wolves must:
- spread or vary their bites;
- fake bite claims to draw cures away, at the cost of missing out on calming;
- steer accusation votes onto humans, since human deaths count toward wolf parity.

Focus-biting beats careless humans but loses to coordinated cures. Random voting kills humans. Neither side should win more than about 60% under good play; simulation is needed to confirm, and the conversion threshold of 3 is the tuning lever.

Talk is kept because the teams truly disagree. A wolf proposes 'everyone charm Player 3, they were bitten' or 'vote Player 5'. A human who simply follows can waste Charms on a liar or wound a fellow human, and both outcomes push the wolves toward parity.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 14 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
