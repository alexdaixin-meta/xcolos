A game design for XColos (a platform that runs turn-based, text-only games between language models, decided by
arithmetic) was handed to a coder to build as a game file for the platform's engine, and building or testing it
went wrong. You are given the game's rules, its interface (the attribute names and result names the file must
use), and the evidence of what went wrong. Decide who needs to act:

  fix_game        The rules are sound and the platform can express them, but the game file is wrong or incomplete: a
                  mistake in the file, a rule not implemented, a misread of the rules. Give the coder concrete guidance.
  revise_rules    The rules are the problem: a test is right and the rules are unbalanced or ambiguous, the design is
                  too complex to build correctly, or it relies on something awkward the platform can only approximate
                  badly. Say how the designer should change the rules (simplify, rebalance, drop a mechanic).
  platform_limit  The rules are sound and balanced, and they REQUIRE something the platform cannot do (see the
                  restrictions below, and the evidence). Choose this only when the evidence shows the capability is
                  missing, not merely that the coder made an error: a loader error about a wrong key is the coder's,
                  a rule that needs, for example, one player to propose and another to accept an exchange is the
                  platform's. Name exactly what is missing.

If the same kind of failure has repeated across several attempts with the coder fixing things each time, that points to
revise_rules or platform_limit, not another fix_game.

What the engine supports, from its capability list:
- supported: hidden_hands, roles_with_allies, private_values, sequential_choice, simultaneous_choice, numeric_bids, free_text_talk, private_channel, variable_player_count, fixed_rounds, counted_repetition, elimination
- supported with a workaround (works, but costs extra steps): shared_deck_draw (options can come from a game list; drawing is remove/append operations); payoff_matrix (no lookup operation: rps needs about 13 steps for a 9-cell matrix); player_attribute_compare (no player-attribute operand: keep a table attribute beside the score); arithmetic_ranking (rank endings were replaced by a model-decided winner; an arithmetic one needs calc)
- NOT supported (do not design with it): conditional_subsequence (the step list is flat: no run-this-block-instead-of-that); trading_between_players (no mechanism for a player to propose and a player to accept an exchange); binding_agreements (talk is not enforced; a promise cannot bind); real_time (the engine is turn-based)
- out of scope, never wanted (do not design with it): spatial_board (out of scope by decision: the game depends on a spatial board (a grid, map, movement or adjacency))
A choice made at the same moment by several players must be a simultaneous poll, not turns.

Reply with ONE JSON object and nothing else:
  {"decision": "fix_game" or "revise_rules" or "platform_limit",
    "reason": one or two sentences saying why,
    "guidance": what the coder (fix_game) or the designer (revise_rules) should do; empty for platform_limit,
    "missing": for platform_limit only, exactly what the platform cannot do; otherwise empty}