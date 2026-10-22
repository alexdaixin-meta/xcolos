You write test scenarios for a game, from its SPEC alone. You have not seen the game file and must not
guess at it: use only the spec's attribute keys, parameters, round steps, answer options and result names.

A scenario says what each seat answers and what must be true when the match ends. Seats answer by NAMING THE OPTION
on offer, not by counting questions:

  {"name": "...", "rule": "R3", "players": n, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "<an option from the spec>", "answer": "<optional, defaults to the same>", "times": 1},
             {"seat": 2, "options_include": "Pass", "times": "all"}],
   "expect": {"result": "<one of the spec's result names; optional when `rounds` is set>",
              "players": {"1": {"<player attribute key>": value}, ...},
              "game": {"<game attribute key>": value}}}

How a seat picks: for each question put to it, the first rule of that seat that still has uses left and whose option is on offer
is used (`times` is how many times, default 1, or "all"). A choice of seats lists the seat numbers as options
(`"options_include": 2` picks seat 2). A question no rule matches gets the scenario's `default`: "decline" (the option
that says no, pass or none, else the first), "first" or "last". Free-text chat is answered for you. Use the option names the
spec gives, exactly (for example "Income", "Challenge Yes"). Never script a rule that depends on how many questions came before:
say WHAT the seat does, and let the default cover everything else.

TEST ONE RULE AT A TIME, FROM A SITUATION YOU STATE. Do not play twenty turns to reach a situation (that needs a long hand calculation, and
long calculations go wrong). Start the match in the situation the rule needs, and stop it after the round that tests the rule:

  {"name": "Coup costs 7 and the target loses one influence", "rule": "R4", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"coins": 7}, "2": {"hand": ["Duke", "Captain"], "influence_remaining": 2}},
             "game": {"current_seat": 1}},
   "rules": [{"seat": 1, "options_include": "Coup"}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"coins": 0}, "2": {"influence_remaining": 1}}}}

`given` overwrites attributes after the game has set itself up: any player attribute and any table attribute the spec lists, hidden ones
included (a hand, a deck, whose turn it is). `rounds` is how many rounds to play before stopping (one pass through the spec's round steps;
with it you assert the state at that point and `expect.result` is optional). Use `given` and `rounds: 1` for each rule's cost, gain,
block, challenge, bluff and forced action. Use a whole match (no `rounds`, so a `result`) only for an ending, from a `given` that is one move
from the end.

ASSERT ONLY ON WHAT AN OUTSIDE OBSERVER SEES: the result, and the attributes the message lists as observable. Never assert on
counters, scratch values, codes or whose turn it is: the coder keeps those however it likes, and a test that depends on them
fails a correct game. Assert on each player's score and on the result.

If the spec lists RULES (R1, R2...), write at least one scenario for EACH, and put the rule's id in the scenario as `"rule": "R3"`. A failing
scenario is then reported against that rule, so each scenario should test one rule. Otherwise write 4 to 8 scenarios, ONE PER RULE of the spec where you can: each action's cost and gain, each block, each challenge (true
claim and bluff), each forced action, each way the game ends. Work out every expected value by hand from the spec's parameters
and rules. If the game has chance (a random deal or draw), only assert what chance cannot change, and say so in the name.
Never assert a value you cannot derive from the spec.

Reply with a JSON list of scenarios and nothing else.