You are a game designer adapting an existing game for XColos, a platform that trains and tests language
models on strategic reasoning: inference from limited information, opponent modelling, planning over several
rounds, and acting on all three. It runs turn-based, text-only games between models and scores them by arithmetic.
A game earns its place only if playing it well takes thinking: it must be BALANCED (no seat or simple policy has the
edge), PLAYABLE (complete, clear rules a model can follow, inside the platform's restrictions), and reward REASONING
over luck (what wins is inference, planning and opponent modelling, not the draw).

You are given a game's rules. Do three things.

1. REVIEW the original against these criteria, giving each a verdict (good, weak or bad) and concrete evidence.
   Test it: ask what a thoughtless policy would score, whether anything is hidden, whether the stated winner rule
   makes cooperation or the interesting choice pointless, whether luck swamps skill.
  non_degenerate: No policy wins just by being simple (always defect, always pass, always the highest bid), no seat has a built-in edge, and choices change the outcome.
  skill_sensitive: A better player beats a worse one reliably; skill outweighs luck.
  headroom: A strong player can keep improving, and a weak one can still score; not solved, not hopeless.
  reasoning_dependent: Doing well takes inference from limited information: hidden state, an opponent's likely type or move, or a plan over several rounds. Perfect-information games with nothing to infer fail this.
  verifiable: The result follows by arithmetic from what happened. No judge decides it.
  fits_platform: Turn-based and text-only, decided by arithmetic, inside what the engine supports, with no spatial board, and short enough to play.

2. List the PROBLEMS you found, then the CHANGES that fix them. Reorganise and rebalance freely: payoffs, number
   of rounds, a private signal or hidden type, a communication phase, the objective or winner rule, who knows what,
   the player count. Every change must say which problem it fixes. Keep what makes the game recognisably itself.
   Do not add a board, grid, map or movement. Do not rely on a judge: the winner must follow from arithmetic on
   numbers the engine tracks. The engine decides a winner (or a draw); it cannot reward a player by their own
   score except through who ends higher, so choose the winner rule with that in mind.

3. Write the VARIATION: the complete rules of the changed game, in plain words, self-contained, with every number
   stated, so someone could build it without seeing the original.

THE "HIGHER TOTAL WINS" TRAP. The platform decides only who wins. In a two-player game where the higher total wins, only the
DIFFERENCE between the totals matters, so any option that cannot lose (it pays the same whatever the opponent does, or the
opponent can at best match it) makes the cooperative or risky option pointless: the stag hunt, the prisoner's dilemma and
their relatives all collapse this way, and "both cooperate" can only draw. Before you finish, take every simple policy
(always the first option, always the last, always pass, always the highest bid) against EVERY opponent action and against
random play, with YOUR winner rule, and check that each can lose. If one cannot, change the objective or the payoffs.
Objectives that work: a target a player must reach to win, so only sustained cooperation reaches it; a margin rule; three or
more players, so one rival's gain is not another's loss; a pot that only builds if everyone commits; a hidden type, so the
best action differs by who you are.

THE LOTTERY TRAP. Check the outcome when everyone plays the intended good strategy, not only the thoughtless ones. If the
winner is then decided by a random draw (who was dealt the better hidden type, who drew the better card), reasoning does
not decide the game. Make a hidden type matter for WHAT to do, not for who ends ahead: give types that are worth the same
in total, or compare players on something both can reach, or let play after the draw correct for it.

MODEL. If your game is a repeated game in which, every round, all players choose AT THE SAME MOMENT from the same list of
actions, and a player's payoff for the round depends only on their own action, their private type (if any) and how many
players chose each action, ALSO give `model`, so the rules can be played with numbers before anything is built:
  {"players": n, "rounds": n, "actions": ["C", "D"],
    "types": {"values": ["High", "Low"], "probs": [0.5, 0.5]} or null,
    "payoff": one expression for a player's payoff in ONE round,
    "winner": {"kind": "highest_total"} or {"kind": "target", "target": a number}}
The expression may use `action`, `type`, `round`, `n_<A>` (how many players, you included, chose action A), `o_<A>` (how many
others did), numbers, `if ... else`, `and`/`or`/`not`, comparisons, + - * / and min/max/abs, and nothing else. For example:
`(6 if type == 'High' else 5) if action == 'C' and n_C == 3 else 0`. A "target" winner means every player whose total reaches the
number wins (one player: a win; several: a draw; none: a draw). Make the model say exactly what your rules say. The pipeline
plays every simple policy through it and sends back the numbers; a game that does not fit sets `model` to null.

COMPLEXITY. The platform builds a game from your rules automatically, and it only builds simple-enough games
correctly. Stay within these limits, and report your variation's numbers honestly in `complexity`: steps_per_round at most 12; choice_steps_per_round at most 4; attributes at most 20; hidden_elements at most 3; random_draws_per_round at most 1; rounds at most 15.
A step is one thing that happens in a round (a question put to players, an announcement, a change to the scores or
state, a check for the end); count the steps you would need. Prefer ONE
strong hidden element (a private type, or a hidden state, or private signals) over several, and at most one chance
event per round. A richer game that cannot be built is worth less than a simpler one that can. If you cannot make the
game worth training on inside the limits, say so.

DROPPING. Recommend dropping the game, with a reason, instead of adapting it, when:
  too_simple   even with changes it stays a trivial decision: solved, nothing meaningful to hide, no choice that
               takes thought, and no change inside the limits fixes that;
  too_complex  its essence needs more than the limits allow (many roles, long chains of rules, large hidden
               state) and cutting it down would leave a different game.
A drop needs a specific reason in one or two sentences. Do not drop a game just because it needs work: that is your job.

Reply with ONE JSON object and nothing else, with exactly these keys:

  original_summary  one or two sentences on what the original game is
  review            a list with one entry per criterion above, in that order: {"criterion", "verdict", "evidence"}
  problems          a list of strings: what is wrong with the original for XColos's purpose
  changes           a list of {"what", "why", "fixes"}: "fixes" names a problem from `problems`
  keeps             a list of strings: what you preserved of the original game's identity
  recommendation    {"decision": "adapt" or "drop", "kind": "none", "too_simple" or "too_complex", "reason": ...}
  variation         (omit when dropping) {"name", "summary", "players": {"min": n, "max": n}, "rules": the complete
                     rules, "objective": exactly how the winner (or a draw) is decided, "expected_effect": what you
                     expect the changes to do to how it is played}
  model             (omit when dropping) the model above, or null
  complexity        (omit when dropping) {"steps_per_round": n, "choice_steps_per_round": n, "attributes": n, "hidden_elements": n, "random_draws_per_round": n, "rounds": n} for the variation, whole numbers

What the engine supports, from its capability list:
- supported: hidden_hands, roles_with_allies, private_values, sequential_choice, simultaneous_choice, numeric_bids, free_text_talk, private_channel, variable_player_count, fixed_rounds, counted_repetition, elimination
- supported with a workaround (works, but costs extra steps): shared_deck_draw (options can come from a game list; drawing is remove/append operations); payoff_matrix (no lookup operation: rps needs about 13 steps for a 9-cell matrix); player_attribute_compare (no player-attribute operand: keep a table attribute beside the score); arithmetic_ranking (rank endings were replaced by a model-decided winner; an arithmetic one needs calc)
- NOT supported (do not design with it): conditional_subsequence (the step list is flat: a whole BLOCK of steps cannot be chosen instead of another block. This is NOT a limit on conditional scoring or conditional updates: a single step can carry a `when` condition and a single operation an `if`, both arithmetic, so 'the poisoner scores if the choices match, otherwise the chooser' is fine); trading_between_players (no mechanism for a player to propose and a player to accept an exchange); binding_agreements (talk is not enforced; a promise cannot bind); real_time (the engine is turn-based)
- out of scope, never wanted (do not design with it): spatial_board (out of scope by decision: the game depends on a spatial board (a grid, map, movement or adjacency))
A choice made at the same moment by several players must be a simultaneous poll, not turns.

Reply with the JSON object only.