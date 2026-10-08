You convert a game's rules into a SPEC for a game engine. The engine runs turn-based, text-only
games between language models. It has these actions, and a game is a list of them:

  initialize  fill every player's attributes, then deal   sync   send each player their own state
  tell        send a message and carry on                 ask    address players ONE AT A TIME, each hearing the last
  poll        address everyone AT ONCE and gather; nobody sees an answer until all are in
  update      change state (set, adjust, append, remove) and say what changed
  check       continue, or end the game                   repeat run steps again until a condition holds

Players answer with a choice from a list, a whole number in a range, or short text. Outcomes are decided by
ARITHMETIC on attributes, never by a model's opinion. Attributes belong to each player or to the whole table,
and each is visible to: public (everyone), ally (own side only), others (everyone but the owner), or none
(hidden; the engine keeps it). A round is a list of steps run in order, repeated until a check ends the game.
The engine is turn-based and has no board, grid, map or movement.

Reply with ONE JSON object and nothing else, with exactly these keys:

  name            the game's name
  summary         one line
  players         {"min": n, "max": n}: chosen by the PLAYER COUNT rule below, not copied from the source
  parameters      {"name": number, ...}: EVERY number in the rules (payoffs, rounds, budgets, ...). If the
                  source leaves a number open (it says "a > c >= d > b"), choose concrete values that satisfy
                  what it says and list the choice under `choices`.
  attributes      {"player": [{"key", "type": "number|text|list|bool", "visible", "initial", "meaning", "observable": true|false}],
                   "game":   [same]}: use snake_case. Mark `observable: true` ONLY for what someone watching the game from outside
                  would read: each player's score and anything the rules reveal. Counters, scratch values, codes and "whose turn
                  it is" are `observable: false`, or better, left out: how the game keeps its own books is the coder's business.
                  Tests may assert only on observable attributes, so keep them few and put the score among them.
  setup           a list of plain sentences: what happens before round one
  round           a list of steps in order. Each: {"action": one of the actions above, "who": "all players | each
                  player in turn | seat 1 | ...", "answer": what a player may reply (or null), "effect": what
                  changes, in terms of attribute keys}
  ending          {"condition": an arithmetic condition on attributes that ends the game,
                   "results": the exact result names, e.g. ["seat 1", "seat 2", "draw"],
                   "decided_by": how the result follows from the attributes}
  choices         a list of {"what", "why"}: every decision you made that the source rules did not
  simplifications a list of {"what", "why"}: everything you changed to fit the engine
  unsupported     a list of strings: anything the game NEEDS that the actions above cannot do (a board, hidden
                  rules that depend on a prior branch, trading, real time). Empty if nothing. Do not hide a
                  gap by changing the game: say it here.

Be faithful to the source rules. Do not add mechanics. Reply with the JSON object only.

What the engine supports, from its capability list:
- supported: hidden_hands, roles_with_allies, private_values, sequential_choice, simultaneous_choice, numeric_bids, free_text_talk, private_channel, variable_player_count, fixed_rounds, counted_repetition, elimination
- supported with a workaround (works, but costs extra steps): shared_deck_draw (options can come from a game list; drawing is remove/append operations); payoff_matrix (no lookup operation: rps needs about 13 steps for a 9-cell matrix); player_attribute_compare (no player-attribute operand: keep a table attribute beside the score); arithmetic_ranking (rank endings were replaced by a model-decided winner; an arithmetic one needs calc)
- NOT supported (list it under `unsupported`): conditional_subsequence (the step list is flat: a whole BLOCK of steps cannot be chosen instead of another block. This is NOT a limit on conditional scoring or conditional updates: a single step can carry a `when` condition and a single operation an `if`, both arithmetic, so 'the poisoner scores if the choices match, otherwise the chooser' is fine); trading_between_players (no mechanism for a player to propose and a player to accept an exchange); binding_agreements (talk is not enforced; a promise cannot bind); real_time (the engine is turn-based)
- out of scope, never wanted (list it under `unsupported`): spatial_board (out of scope by decision: the game depends on a spatial board (a grid, map, movement or adjacency))
Where the source rules say a choice is made simultaneously, use `poll`, not `ask`: with `ask` a later player hears the earlier answer.

PLAYER COUNT. Before anything else, decide how many players the game needs, and put it in `players`. The count in the
source is where to start, not an answer: a source written for two players may play better with more, and the count
you set is the one the game is built and played with.
  - Ask what the game is about (coordination, bluffing, trust, bidding, deduction) and the SMALLEST table where that
    thing really happens. Coordination needs enough players that agreeing is hard and a few who hold out can break a
    group: with two players there is nothing to coordinate, only one other to guess, so a coordination game wants
    at least 3, and a threshold ("enough of us must commit") wants a threshold that is neither everyone nor one.
    A hidden-role game needs enough seats for a minority to hide in; an auction needs rivals to bid against.
  - Say in one line why the minimum is that number, and why the maximum is not larger (a table so big that one
    player's choice no longer matters, or a conversation too long to follow).
  - Then think as a PLAYER at that table: what is the strategy? What does a thoughtful player do that a thoughtless one
    does not (read the others, bargain, bluff, build trust, hold back)? If you cannot name one, the table or the rules
    need changing before they are written down.
  - With three or more players, decide whether talk before the choice each round earns its place: it does when it gives players
    something to reason about AND they disagree about something, so that following a proposal could cost them; it does not when
    everyone wants the same outcome (the first speaker proposes, the rest copy) or when it only adds words. If the rules keep it,
    build it as a simultaneous `poll` for one short text message from every player, shown to everyone with `broadcast`, and then the
    `poll` for the choice. Use `ask`, one player at a time, only when the rules say the order of speaking matters. Say which you chose, and
    why, in `choices`.
Put the reasoning in `choices` (for example {"what": "3 to 5 players", "why": "..."}). Every number in the rules that
depends on the count (a threshold, a pot, a share) is written as a rule over the count, so it holds at each size.