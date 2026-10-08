# gen_inventory

Step 1 of the game-generation pipeline: find candidate games and keep an
inventory of them. Steps 2 to 4 (turn an inventory game into a platform game and
evaluate it) are in `gen_game/`. Both sit beside `xcolos/`, not inside it: nothing
in the platform imports them, and nothing here imports the platform, except for
the model adapters the crawl borrows. Design:
`design/2026-10-05-game-generation-pipeline.md`.

```bash
python3 -m gen_inventory list                 # one line per game
python3 -m gen_inventory add record.json      # store a candidate, run the gates
python3 -m gen_inventory check [id]           # re-run the gates
python3 -m gen_inventory recheck              # after the manifest changed: what moved
python3 -m gen_inventory queue                # ready games, in the order to port them
python3 -m gen_inventory gaps                 # engine limits, ranked by games blocked

python3 -m gen_inventory discover             # new leads from the sources; reads no pages, no model
python3 -m gen_inventory crawl --model muse   # enumerate, rate 1-5, read the best, run the gates (stops at 50 games)
python3 -m gen_inventory crawl --model muse --rate-only   # rate only, read nothing in full
python3 -m gen_inventory calibrate --model muse           # does a high rating predict a game that passes?
python3 -m gen_inventory suggest --model muse             # a model proposes sites and phrases
python3 -m gen_inventory sources                          # the list of sites

python3 gen_inventory/run_tests.py            # gen_inventory's tests
```

## The crawl

`crawl.py` finds candidates and files them, in three phases. Leads come from the
sites in `data/sources.json` (Wikipedia categories first: they are curated;
then search phrases). Which sites to look at is `suggest`'s job (`sources.py`):
a model proposes sites and phrases, the registry keeps each once, and a new site
stays `suggested` until a person approves it and a reader exists for it.

1. **Enumerate, no model.** List the source's games. Drop titles that are plainly
   not a game (the `exclude_title` patterns) and games already in the inventory
   under that name or an alias.
2. **Rate, cheap.** A model sees each new lead's title and the first 500
   characters of its page, ten to a call, and gives 1-5 for fit with the platform
   (`rate.py`; the scale is anchored in what `capabilities.json` says the engine
   can and cannot do). The rating and its reason are kept in the log.
3. **Extract, best first.** Leads rated at least `--min-rating` (default 3) are
   read in full, highest rating first. A model fills the record's mechanic fields
   in the fixed vocabulary, or replies `skip`; a reply outside the vocabulary
   goes back with the reason, twice at most. The inventory runs the gates and
   files the record whatever the verdict, so a dropped game is not read again.

A lower `--min-rating` later reads the leads that were rated below it without
rating them again. `crawl --rate-only` stops after step 2. `calibrate` rates
pages that were already read in full and shows what each rating became, which is
how to tell whether a 5 is worth more than a 2. On the first 64 pages read, a
minimum of 3 would have skipped 16 pages: 13 of the 14 that turned out not to be
games, and 3 that were. A minimum of 4 would have skipped 22: the same 13
non-games and 9 real games. That is why 3 is the default.

The model never sets the source, licence or id; those come from the page. It
paraphrases the rules (the licence is `rules_only`). Anything a game needs that
the manifest has no word for goes in `unmapped`, which blocks the game and
appears in `gaps` as free text: that is how a missing engine feature is found.

`--model` takes the platform's backend specs (`muse`, `anthropic`,
`command:<program>`, `echo:<reply>`), so gen_inventory reuses
`xcolos.flow.backends`; it is the one place it imports the platform.
Every lead's outcome is in `data/crawl_log.jsonl`; a rerun skips them, and
`--retry-failed` reads the failed ones again. Wikipedia rate-limits; the fetch
waits out a 429.

## Files

```
schema.py         the record, its vocabulary, and what makes two games alike
gates.py          the six gates, in order
capabilities.json what the engine can express: the manifest the capability gate reads
inventory.py      the store (one JSON file per game) and the reports over it
crawl.py          discover, pre-gate, extract, admit
crawl_sources.json what to search and which titles to skip
index.py          INDEX.md, generated
cli.py            the command line
data/inventory/   the records
```

## The gates

`completeness` -> `provenance` -> `duplication` -> `capability` ->
`verifiability` -> `value`. The first four can stop a game (`incomplete`,
`rejected`, `duplicate`, `blocked`); a game past them is `ready`. Games that
reach `ported` or later are never touched by a gate.

Duplication has two levels. The same name, or near-identical rules text, is a
`duplicate`. The same mechanic under another theme is kept as a variant in the
same family, and the queue takes new mechanics first.

## Dropped games

`gen_game` (or a person) drops a game it decides is too simple or too complex to be worth building, by
setting `dropped` on its record to the reason. The gates leave such a record alone, so a recheck cannot revive
it, and the index shows it as `dropped` with the reason. Clear `dropped` to put it back through the gates.

## The manifest

`capabilities.json` lists what a game can need and what the engine does about
it: `ok`, `workaround` or `blocked`. Each entry says whether its basis is
`documented` (from `design/actions.md` or the milestone design) or `assumed`.
**The assumed entries have not been checked against the engine**; check them
before trusting a verdict that rests on one. Changing a verdict and running
`recheck` moves the games that depended on it.
