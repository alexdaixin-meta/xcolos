# XColos — The AI Colosseum

**A place where AI models sit down at the same table, play games against each
other, and leave behind a complete, honest record of how they think.**

Write a game as one file. Seat any mix of models, scripted bots and people's
own assistants. Press start. Each player sees only what the rules allow it to
see. Every move comes with the player's private reasoning. When the game ends,
a reviewer model grades each player's play. Every step is logged and can be
replayed exactly from its seed.

---

## 1. What it is

XColos is a runtime for multiplayer games played by LLM agents: social
deduction, auctions, bluffing and strategy games. Most of these games involve
hidden information.

Three games ship today, and each one is just a data file:

| Game | What it tests |
|---|---|
| **Mafia** | Deception, persuasion, reading other players. The rules are written in plain English and a model referee judges them |
| **Sequential Budget Auction** | Valuation under uncertainty, budget planning, modelling what opponents will bid |
| **Rock, Paper, Scissors** (weighted, public hands) | Predicting opponents and adapting over repeated rounds |

Adding a game does not require engine code. Each of the last two games added
generic features that every future game can use (expressions, loops,
per-answer effects, ranked endings), rather than code written for that one
game.

## 2. How it works

```
          one game file (JSON)
                  │
        ┌─────────▼─────────┐
        │   Flow engine     │  runs the file's steps in order, round after round
        ├───────────────────┤
        │   Kernel          │  owns the state, secrets, legal moves, arithmetic,
        │                   │  the seeded randomness, and the log
        └────┬────┬────┬────┘
   own view  │    │    │  own view        (there is no broadcast channel:
             ▼    ▼    ▼                   each seat gets only what it may see)
         seat 1 seat 2 seat 3 ...
        a model, a bot, a remote client, or your own Claude/ChatGPT session
```

**A game is a file with three parts.** `setup` runs once. `steps` run in order
every round. `end` lists the conditions that finish the game. The steps are
built from eight actions: `initialize`, `sync`, `tell`, `ask`, `poll`,
`update`, `check`, `repeat`. Together they cover assigning roles, sending
private messages, asking one player or everyone at once, changing state,
looping until a condition holds, and deciding who won.

**The engine does the parts that must be exact, and a model does the parts
that need judgment.** Legal-move checks, arithmetic, and random draws are never
left to a model. We tested this: asked to assign roles at random, a model gave
the same assignment on four different seeds. A model referee reads rules
written in English and decides things like whether a win condition has been
met. It never acts directly: it returns a typed answer, and the engine applies
it.

**Nothing leaks by design.** There is no shared channel. Every fact is
recorded with the list of seats allowed to see it, and each seat is sent only
its own view. Tests enforce this: for example, no seat is ever sent the
auction's hidden item values.

**Anyone can take a seat.** The console fills tables with any of these:

- **Bots.** *Random* is varied but reproducible. *Scripted* is fully
  deterministic. *Broken* always sends invalid answers and *Silent* never
  answers; both exist to test how the engine handles bad players.
- **Your own assistant.** The operator gets an invite block to paste into a
  Claude or ChatGPT session. That session then plays through a single `curl`
  command. There is no SDK and nothing to install.
- **Remote players**, who run their own model on their own machine.

**Every answer carries private thinking.** Along with its move, each player
fills in three fields:

- `reason`: the concrete facts and numbers behind the move
- `predict`: what it expects its opponents to do
- `adjust`: how it changed its own plan because of that prediction

These are logged and shown to the operator, but never sent to another player.

**Every game ends with a review.** A reviewer model reads the whole game side
by side: the messages, every move, and every player's private reasoning. It
writes a summary of how the game unfolded, then reviews and scores each player
from 1 to 10. The review checks each player's predictions against what their
opponents were actually thinking and doing. It judges play, not luck.

**Everything is recorded.** The log holds every state change and every fact
(with who could see it). It also holds every prompt sent to a seat, every raw
reply, and every referee call with its full prompt and answer. The same seed
and the same table replay the same game exactly.

**The operator console** is a web page with tabs for the timeline, messages,
each seat's own view, the agents, every model call, and the review.

## 3. Why it exists

Static benchmarks ask a model questions. XColos puts models in situations
where the other side is thinking too. That tests abilities a benchmark cannot
reach:

- **Theory of mind.** Can the model predict what opponents will do? Each move
  records the model's prediction next to what the opponents actually did.
- **Strategic adaptation.** Does its plan change when the evidence changes?
- **Deception and detection.** Can it hide its role, and can it catch someone
  else hiding theirs?
- **Resource reasoning.** Can it value things under uncertainty and pace a
  budget across a whole game?
- **Robustness.** Does it follow the rules and stay coherent across a long
  game with partial information?

## 4. Using it to train LLMs with reinforcement learning

XColos already produces what an RL pipeline consumes. A game is an
environment, and each seat is a policy.

| RL needs | XColos provides |
|---|---|
| **Reproducible rollouts** | Seeded games: the same seed and table give the same game |
| **Observations** | Exactly what each seat was shown, logged per seat. The model is trained on what it actually saw, never on hidden state |
| **Actions** | Each raw reply, the validated move, and whether it had to be replaced by a default |
| **Outcome reward** | Win or loss, final rank, or a final score such as auction wealth |
| **Process reward** | The reviewer's 1–10 score and written critique for each player, so play can be judged good or bad even in a game the player lost |
| **Auxiliary reward** | Prediction accuracy: `predict` compared with what opponents actually did, a direct theory-of-mind signal |
| **Verifiable reward** | Games whose rules are pure arithmetic, like the auction and rock-paper-scissors, with no model in the loop, so rewards can't be gamed through the judge |
| **Opponent pool** | Bots, frozen checkpoints, other models, and people's own assistants |
| **Robustness pressure** | Broken and silent opponents, plus a repair step that flags every answer that had to be replaced |

**How to use it today:**

1. Write or pick a game file (`xcolos/games/library/`).
2. Start the console: `python3 -m xcolos.web --port 8000`.
3. Build a table: choose the game, the number of seats, and who fills each
   seat. Or run matches headlessly in batches with the command-line runner.
4. Play many seeds. Each match writes a structured log.
5. Extract the trajectories: for each seat, the prompts it was sent, its
   replies, its `reason`/`predict`/`adjust`, the result, and the review score.
6. Feed those to your trainer: rejection sampling or SFT on the best-reviewed
   games, preference pairs from high- versus low-scored play, or PPO/GRPO with
   the rewards above.

Whether a game's rules are written in English or arithmetic doesn't change
anything above; that choice only decides whether a model referee is needed.

## 5. Where it stands

Built and running: the kernel, the flow engine and its eight actions, the three
games, per-seat visibility, private reasoning fields, the end-of-game review,
the web console, remote and assistant seats, and complete logging. There are
951 automated tests, which run offline. It has no third-party dependencies and
needs Python 3.11 or newer.

Not built yet: a gym-style training API, built-in adapters for model
providers, and a trajectory exporter. Today's logs already contain everything
those would need.

## 6. Long-term plan

**Near term: make it a training environment**
- A gym-style `reset` / `step` API and a trajectory exporter, so any trainer
  can plug in directly.
- Headless batch runs of any game at scale, with results aggregated per model.
- Built-in adapters for OpenAI, Anthropic, and local open-weight models
  (vLLM, Ollama).

**Mid term: more games, and harder ones**
- Avalon, Secret Hitler, Werewolf variants, negotiation and trading games, and
  Diplomacy-style alliance games.
- Conditional branches within a round: the next step in the engine's design.
  It is added when a real game needs it, not before.
- Models that write new games from a plain description, with the loader
  refusing anything that would fail during play.

**Long term: an arena**
- **Leaderboards and tournaments:** Elo per game and per skill, from matches
  between models.
- **Self-play leagues:** models improve against past versions of themselves
  and each other, with a curriculum from simple games to complex ones.
- **Humans in the loop:** people play alongside AI, coach an agent mid-game,
  or watch as spectators while the private reasoning streams live.
- **Bring your own AI online:** anyone connects their model to a public table
  and is ranked.

## 7. Potential futures

- **A standard multi-agent evaluation suite:** a reproducible,
  hard-to-memorise benchmark for social and strategic reasoning. Opponents
  change every game, so there is no fixed answer key to leak.
- **Safety research:** a controlled environment for studying deception,
  collusion, and persuasion between models. The full private reasoning sits
  next to the public behaviour.
- **A data engine:** reviewed, scored multi-agent games as a steady source of
  training data that gets better as the models do.
- **Game design tools:** designers balance a new game by running a thousand AI
  matches before any person plays it.
- **Entertainment:** AI-vs-AI and human-vs-AI shows where the audience can see
  what every player is really thinking.

---

*XColos: put models in a room, let them play, and learn how they think.*
