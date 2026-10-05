# Game generation pipeline

Status: proposal, 2026-10-05. Nothing here is built.

The platform runs games and records every step and the outcome. The next goal
is to produce many reasonable games for RL reasoning training, without writing
each one by hand. This document records the proposed pipeline and how a
generated game is judged.

## What a good game is

A game is worth keeping for RL reasoning if it is:

- **Valid.** It loads, terminates, replays identically from a seed, and leaks
  nothing.
- **Non-degenerate.** No policy dominates, no seat has a built-in edge, and
  choices change the outcome.
- **Skill-sensitive.** Better players score better, and skill outweighs luck.
- **Headroom.** The strongest model does not saturate it and the weakest does
  not sit at the floor.
- **Reasoning-dependent.** A simple heuristic or recall of a known game does
  not match a reasoning model.
- **Verifiable.** The outcome is arithmetic, not a model's opinion.

Verifiable means generated games use calc endings, not prose endings that need
a judge. A model-decided `winner` is noisy and costs a call per match; it is
fine for Mafia but is not a basis for an RL reward.

## Pipeline

1. **Inventory (offline crawl).** Collect candidate games into structured
   records: source, rules text, player count, hidden information, simultaneous
   or sequential play, how it ends, licence notes. Deduplicate by mechanic, not
   title. Mark famous games for a contamination note.
2. **Feasibility and rules.** A model decides whether an inventory game can be
   expressed in the engine, then iterates on a written rules document: who
   acts, what is hidden, what ends the game, what the numbers are. The verdict
   is structured: `fits`, `fits with a workaround`, or `does not fit`, with
   reasons drawn from a fixed list of engine limits (flat steps, sequential ask
   per seat, no player-attribute operand, and so on).
3. **Encode.** Using the rules document, a model writes the game JSON against
   `design/actions.md`, with existing games as examples. The strict loader's
   errors go back to the model as repair feedback.
4. **Evaluate and iterate** (see below).

The rules document is deliberate. It separates "is the game faithful?" from "is
the encoding correct?", and it gives a human something to read when a game
fails.

### Sources

In priority order:

- Game-theory and experimental-economics games: ultimatum, trust, public
  goods, beauty contest, auctions, Colonel Blotto, war of attrition, bargaining.
  Small and verifiable. The auction and RPS come from this family.
- Imperfect-information card games: Kuhn and Leduc poker, liar's dice,
  trick-taking variants. Hidden hands fit the existing visibility model.
- Social deduction: Avalon, Secret Hitler, Werewolf variants, Coup. Closest to
  the product pitch, and where the flat-step gaps show up.
- Mechanic catalogues (OpenSpiel's list, BoardGameGeek tags) for ideas and
  reference behaviour only. Do not import their code.

Rules are not copyrightable but names, text and art are. Reimplement from the
mechanics. Mutating famous games (payoffs, hidden information, order, player
count) also reduces recall.

### Mutation

Beyond direct ports, variants come from explicit operators applied to a
verified base game, not free-form rewriting:

- parameters (budgets, rounds, payoffs, player count)
- information (hide a public attribute, add a private signal, reveal late)
- structure (turn order, simultaneous versus sequential, add communication)
- asymmetry (different roles or resources per seat)
- objective (what counts as winning)

Every variant traces back to a verified base.

## Evaluation tiers

Cheap checks run first. Only survivors move to the expensive ones.

**Tier 0: validity (offline, free).**
Loads, terminates, deterministic by seed, `--check` finds no log or visibility
violation, and no exploit through engine edges (stalling, the 5-refusal cap,
`repeat`'s `max` abandonment).

**Tier 1: degeneracy (bots, offline).**
- Dominance: play random, greedy and always-pass policies against each other.
  A policy that wins everywhere means a dominated game. This is how Trust was
  found to be dominated by Guard, by hand.
- Balance: win rate by seat, draw rate.
- Decision weight: replace one seat's choice at one step with random and
  measure how much the outcome moves. Steps that never matter are filler.
- Hidden information: run one seat with its hidden attributes masked. If
  nothing changes, the hidden information is decoration.

**Tier 2: skill ladder (cheap models).**
Random, heuristic, small model, strong model, many seeds per pairing. Require a
monotone ladder with clear gaps. The headline metric is skill variance against
seed variance; if luck swamps skill, the reward is noise. Require headroom.

**Tier 3: reasoning needed (expensive, survivors only).**
Reasoning against no reasoning, rules visible against not. If a heuristic bot
matches the strong model, the game needs no reasoning. Check that
hidden-information steps are used; the auction's predict/adjust records give a
direct belief-accuracy measure. Check contamination: a mutant that plays like
the original means the model is recalling.

## Two loops

The loops are separate on purpose.

**Inner loop: fix one game.** Inputs are load errors and tier metrics. A critic
diagnoses one named failure and applies one mutation aimed at it:

- dominated: change payoffs
- saturated: add hidden information or rounds
- noisy: more rounds or less chance

Re-evaluate on fresh seeds. Cap the iterations, drop games that do not improve,
and record each game's lineage. It ends when the game passes or is abandoned.

**Outer loop: improve the prompts.** It changes the step 2 and step 3 prompts
using aggregate failure patterns across many games, and runs far less often
than the inner loop. Changing the prompt after each single failure overfits it
to whichever games failed first.

**Regression set for the outer loop.** The four existing games (Mafia, RPS,
auction, plus the Mafia oracle for reference) have known-good JSON. Give the
pipeline only their rules and check whether it recovers working games. Re-run
after every prompt change. This is the first thing to build.

**Human gate.** Before a game is accepted, a person reads a few transcripts.
Metrics miss dull or misleading games. Use held-out models and seeds so the
loop does not tune a game to one model.

## Engine gaps

The feasibility labels in step 2 double as a gap census. Aggregated over the
inventory, the "does not fit" and "workaround" reasons become a ranked list of
engine gaps backed by many games. This follows the existing rule that a gap is
closed when real games demand it; the inventory supplies the games.

The generator writes only inside the current expressive subset. A failed
attempt that needed something the engine lacks is logged with its reason and
does not push the engine to change by itself.

## RL export

Each accepted game ships with:

- a seeded reset
- a verifiable scalar outcome
- per-step records in a fixed format
- a length bound

## Missing pieces

- A cheap per-game heuristic bot. A model can write it from the rules.
- A harness that runs the tiers over a batch and writes one metrics record per
  game. `cli --matches` is the base; tiers 1 and 2 are orchestration on top.
- An inventory schema and crawler.

## Open questions

- Inventory scale: tens of hand-picked games, or thousands crawled? Decides
  whether feasibility labels need human spot-checks.
- Which model runs step 2? It sets the quality of rules documents, the part
  least covered by tests.
- Which models form the skill ladder, and what is the budget per game? That
  sets how many seeds Tier 2 can afford.
- What counts as acceptable headroom (for example, a strong model at 60-85%)?
- Is every accepted game human-reviewed, or a sample?
- Reward source: outcome only, or also per-step signals such as belief
  accuracy? This decides what every generated game must include.
- First batch: game-theory plus card games (easiest to verify), or an early
  Avalon / Secret Hitler port to surface engine gaps?
