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
python3 -m gen_inventory crawl --model muse --target 300  # enumerate, rate 1-5, read the best, run the gates;
                                                          # stops once the inventory holds 300 games
python3 -m gen_inventory crawl --site pagat.com --model muse   # the same over another approved site
python3 -m gen_inventory crawl --site pagat.com --model muse --shard 0/3   # one of three processes on one site
python3 -m gen_inventory crawl --model muse --rate-only   # rate only, read nothing in full
python3 -m gen_inventory crawl --model muse --rerate      # rate again every lead never read (the scale changed)
python3 -m gen_inventory dedup --model muse               # one record per game, also across different names
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
   can and cannot do). Strategy comes first: a game decided mostly by luck
   (gambling, push-your-luck, betting against a house) or played alone rates 2,
   below a strategic game the engine cannot run yet, which rates 3. The rating
   and its reason are kept in the log.
3. **Extract, best first.** Leads rated at least `--min-rating` (default 3) are
   read in full, highest rating first. A model fills the record's mechanic fields
   in the fixed vocabulary, or replies `skip`; a reply outside the vocabulary
   goes back with the reason, twice at most. The inventory runs the gates and
   files the record whatever the verdict, so a dropped game is not read again.

Nothing caps a site: every page a site lists is rated, unless `--rate-budget`
says otherwise, and `--target` counts the games in the whole inventory (ready,
blocked or later; duplicates and rejects do not count), not the games from one
site. To read the best leads of every site first, run each site at
`--min-rating 5`, then 4, then 3: a lower `--min-rating` reads the leads that
were rated below it without rating them again, and `--rerate` rates again every
lead that was rated but never read, after the scale changes. Sites can be
crawled at the same time, one process each: a record is written whole or not at
all. A large site can be read by several processes together: `--shard 0/3`,
`--shard 1/3` and `--shard 2/3` split its leads into three shares that never
overlap. Ratings are logged as they are made, so a run stopped halfway keeps
them. `crawl --rate-only` stops after step 2. `calibrate` rates pages that were
already read in full and shows what each rating became, which is how to tell
whether a 5 is worth more than a 2. On the first 64 pages read, under the scale
before 2026-10-26 (when luck still rated 3), a minimum of 3 would have skipped
16 pages: 13 of the 14 that turned out not to be games, and 3 that were. A
minimum of 4 would have skipped 22: the same 13 non-games and 9 real games. That
is why 3 is the default.

A site with nothing but a sitemap needs no configuration. When its addresses say
which pages are games, `crawl_sources.json` can say so under the site's host:
`include_path` and `exclude_path` are regular expressions on the path, and
`title_segment` names the path segment that names the game (`-2` for a site
that files every game as `/<game>/game-rules.php`).

## No game twice

A lead whose title names a game already here (by name or alias) is dropped
before it is rated, and again just before it is read, since a page on another
site may have brought the game in meanwhile. A page whose record the duplicate
gate stops is logged as `duplicate`, with the game it repeats, and its record is
not kept. What names cannot catch, the same game under a name nobody listed,
`dedup --model` catches: a model reads the inventory a line per game and names
the groups that are one game; the game furthest along is kept and takes the
others' names as aliases, and the others are removed (their pages stay in the
log as `duplicate`). `dedup --dry-run` shows the groups and changes nothing.

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
crawl_sources.json what to search, which titles to skip, and which pages of a site are games
generic.py        a reader for any website with a sitemap or links
web.py            fetching politely: robots.txt, a pause, a cache, HTML to text
rate.py           the cheap 1-5 look at every lead, and calibrate
sources.py        the registry of sites and search phrases, and the model that suggests more
dedup.py          one record per game
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
`duplicate`; the crawl does not keep its record (see "No game twice"). The same
mechanic under another theme is kept as a variant in the same family, and the
queue takes new mechanics first.

## Dropped games

`gen_game` (or a person) drops a game it decides is too simple or too complex to be worth building, by
setting `dropped` on its record to the reason. The gates leave such a record alone, so a recheck cannot revive
it, and the index shows it as `dropped` with the reason. Clear `dropped` to put it back through the gates.

## Games that did not pass

`not_passed` is set by `gen_game` when its last run of a game did not pass: a person must review it, a step
or the play-test failed, or it was dropped or blocked. It holds the reason in words and is cleared when a
run passes. It changes no status, so the game is still converted again. The index shows such a game as
`not passed` with the reason, unless it is dropped or blocked. Its game folder holds the same reason
(`gen_game/data/games/<id>/NOT_PASSED.md`, `DROPPED.md` or `PLATFORM_LIMIT.md`).

## The manifest

`capabilities.json` lists what a game can need and what the engine does about
it: `ok`, `workaround` or `blocked`. Each entry says whether its basis is
`documented` (from `design/actions.md` or the milestone design) or `assumed`.
**The assumed entries have not been checked against the engine**; check them
before trusting a verdict that rests on one. Changing a verdict and running
`recheck` moves the games that depended on it.
