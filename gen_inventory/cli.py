"""Command line for the inventory.

    python3 -m gen_inventory add record.json     store a candidate and run the gates
    python3 -m gen_inventory check [id]          re-run the gates on one game, or all
    python3 -m gen_inventory recheck             re-run after the manifest changed
    python3 -m gen_inventory list [--status s]   one line per game
    python3 -m gen_inventory show id             the whole record
    python3 -m gen_inventory queue               ready games, in the order to port them
    python3 -m gen_inventory gaps                engine limits, ranked by games blocked
    python3 -m gen_inventory index               rewrite INDEX.md (every change does this)
    python3 -m gen_inventory discover            list new leads from the sources; reads no pages
    python3 -m gen_inventory crawl --model SPEC  list a source's games, rate them 1-5, read the best, run the gates
    python3 -m gen_inventory calibrate --model SPEC   does a high rating predict a game that passes?
    python3 -m gen_inventory crawled             rewrite CRAWLED.md: every page read, by website
    python3 -m gen_inventory suggest --model SPEC   a model proposes sites and search phrases; kept in SOURCES.md
    python3 -m gen_inventory sources [approve|reject|crawl HOST]   the list of sites, and their status
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from gen_inventory.inventory import DEFAULT_DIR, Inventory
from gen_inventory.schema import RecordError, STATUSES, from_dict
from gen_inventory.sources import SourceError


def line(r) -> str:
    extra = ""
    if r.status == "duplicate":
        extra = f"  of {r.duplicate_of}"
    elif r.status == "blocked":
        extra = f"  by {', '.join(r.blocked_by)}"
    elif r.status == "ready":
        extra = f"  value {r.value}  {r.reward}  family {r.family_key}"
        if r.workarounds:
            extra += f"  workaround: {', '.join(r.workarounds)}"
    elif r.status in ("incomplete", "rejected"):
        extra = f"  {r.reasons[0]}" if r.reasons else ""
    return f"{r.id:<24} {r.status:<10}{extra}"


def open_log(args):
    from gen_inventory import crawl

    return crawl.CrawlLog(args.dir.parent / "crawl_log.jsonl" if args.dir != DEFAULT_DIR else crawl.LOG_PATH)


def log_report(log, inv: Inventory) -> Path:
    path = inv.index_path.with_name("CRAWLED.md")
    path.write_text(log.render())
    return path


def open_registry(args):
    from gen_inventory import sources

    return sources.Registry(args.dir.parent / "sources.json" if args.dir != DEFAULT_DIR else sources.REGISTRY_PATH)


def sources_report(args, inv: Inventory) -> Path:
    from gen_inventory import sources

    log, reg = open_log(args), open_registry(args)
    path = inv.index_path.with_name("SOURCES.md")
    path.write_text(reg.render(sources.yields_from(log.entries.values())))
    return path


def inventory_summary(inv: Inventory) -> str:
    from gen_inventory import index

    recs = inv.all()
    counts = Counter(index.disposition(r) for r in recs)
    lines = [", ".join(f"{n} {d}" for d, n in counts.items())]
    fams = Counter(r.family_key for r in recs if r.status in ("ready", "ported", "evaluated", "accepted"))
    lines.append("games: " + ", ".join(sorted(r.name for r in recs if r.status != "duplicate"))[:1500])
    gaps = inv.gaps()
    if gaps:
        lines.append("engine gaps blocking games: " + ", ".join(f"{k} ({n})" for k, n in gaps.most_common(8)))
    return "\n".join(lines)


def suggest_command(args, inv: Inventory) -> int:
    from gen_inventory import sources
    from xcolos.flow.backends import from_spec

    reg, log = open_registry(args), open_log(args)
    got = sources.suggest(from_spec(args.model), reg, inventory_summary(inv),
                          sources.yields_from(log.entries.values()), n=args.n)
    for s in got.new_sources:
        print(f"new site     {s['host']}  ({s['kind']})  {s['why']}")
    for host, q in got.new_queries:
        print(f"new phrase   {host}: {q}")
    for why in got.skipped:
        print(f"skipped      {why}")
    print(f"\n{len(got.new_sources)} sites suggested (status: suggested, nothing reads them until approved), "
          f"{len(got.new_queries)} phrases added")
    print(sources_report(args, inv))
    return 0


def sources_command(args, inv: Inventory) -> int:
    from gen_inventory import sources

    reg = open_registry(args)
    if args.action:
        if not args.host:
            raise sources.SourceError(f"{args.action} needs a host")
        status = {"approve": "approved", "reject": "rejected", "crawl": "crawling"}[args.action]
        entry = reg.get(args.host)
        if status == "crawling" and not (entry and entry["status"] in ("approved", "crawling")):
            raise sources.SourceError(f"{args.host} must be approved before it is crawled")
        reg.set_status(args.host, status)
    for s in reg.sources:
        print(f"{s['host']:<28} {s['status']:<10} {s['kind']:<13} {len(s['queries'])} phrases  {s['why'][:70]}")
    print(sources_report(args, inv))
    return 0


def wikipedia_source(args):
    from gen_inventory import crawl

    reg = open_registry(args)
    wiki = reg.get("en.wikipedia.org")
    config = json.loads(crawl.CONFIG_PATH.read_text())["wikipedia"]
    # What to search comes from the registry, so a phrase a model suggested is
    # read on the next crawl and recorded once.
    if wiki and wiki["status"] == "crawling":
        config = {**config, "queries": reg.queries("en.wikipedia.org"), "categories": reg.categories("en.wikipedia.org")}
    return crawl.Wikipedia(config)


def make_fetcher():
    from gen_inventory import web

    return web.Fetcher()


def source_for(args):
    """The reader for `--site`: Wikipedia's own, or the generic one for an approved site."""
    from gen_inventory import generic, sources

    host = getattr(args, "site", None) or "en.wikipedia.org"
    if host == "en.wikipedia.org":
        return wikipedia_source(args)
    entry = open_registry(args).get(host)
    if entry is None or entry["status"] not in ("approved", "crawling"):
        raise sources.SourceError(f"{host} is not approved; run: python3 -m gen_inventory sources approve {host}")
    return generic.GenericSite(host, entry["url"], make_fetcher())


def calibrate_command(args, inv: Inventory) -> int:
    from gen_inventory import rate
    from xcolos.flow.backends import from_spec

    pairs = rate.calibrate(rate.Rater(from_spec(args.model), inv.manifest), source_for(args), open_log(args), inv)
    print(f"{len(pairs)} pages read in full, rated afterwards\n")
    print(rate.crosstab(pairs))
    return 0


def crawl_command(args, inv: Inventory) -> int:
    from gen_inventory import crawl

    source = source_for(args)
    log = open_log(args)
    budget = args.rate_budget
    if budget is None and source.host != "en.wikipedia.org":
        budget = 12 * args.target
    extractor = rater = None
    if args.cmd == "crawl":
        # The platform's own model adapters: one backend interface, not two.
        from gen_inventory.rate import Rater
        from xcolos.flow.backends import from_spec

        if not args.rate_only:
            extractor = crawl.Extractor(from_spec(args.model), inv.manifest)
        if not args.no_rate:
            rater = Rater(from_spec(args.rate_model or args.model), inv.manifest)

    def show(outcome: str, lead, detail: str) -> None:
        print(f"{outcome:<22} {lead.title}" + (f"  ({detail})" if detail else ""), flush=True)

    counts = crawl.crawl(source, inv, extractor, log, limit=args.limit, target=getattr(args, "target", None),
                         retry_failed=getattr(args, "retry_failed", False), rater=rater,
                         min_rating=getattr(args, "min_rating", 3), rate_only=getattr(args, "rate_only", False),
                         rate_budget=budget, on_event=show)
    log_report(log, inv)
    sources_report(args, inv)
    for note in getattr(source, "notes", []):
        print(f"note: {note}")
    for err in dict.fromkeys(getattr(rater, "errors", [])):
        print(f"note: a rating call failed: {err}")
    print("\n" + (", ".join(f"{n} {k}" for k, n in sorted(counts.items())) or "nothing new"))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gen_inventory", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR, help="inventory directory")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add")
    p.add_argument("file", type=Path)
    p = sub.add_parser("check")
    p.add_argument("id", nargs="?")
    sub.add_parser("recheck")
    p = sub.add_parser("list")
    p.add_argument("--status", choices=STATUSES)
    p = sub.add_parser("show")
    p.add_argument("id")
    sub.add_parser("queue")
    sub.add_parser("gaps")
    sub.add_parser("index")
    sub.add_parser("crawled")
    p = sub.add_parser("suggest")
    p.add_argument("--model", required=True)
    p.add_argument("--n", type=int, default=6)
    p = sub.add_parser("sources")
    p.add_argument("action", nargs="?", choices=("approve", "reject", "crawl"))
    p.add_argument("host", nargs="?")
    p = sub.add_parser("discover")
    p.add_argument("--limit", type=int, default=50)
    p = sub.add_parser("crawl")
    p.add_argument("--model", required=True,
                   help="a backend spec: anthropic[:model], muse[:model], command:<program>, echo:<reply>")
    p.add_argument("--target", type=int, default=50, help="stop once this many games have been crawled in all")
    p.add_argument("--limit", type=int, default=None, help="also stop after reading this many pages this run")
    p.add_argument("--retry-failed", action="store_true")
    p.add_argument("--rate-model", help="backend for the rating step (default: --model)")
    p.add_argument("--min-rating", type=int, default=3, choices=range(1, 6), help="read only leads rated at least this")
    p.add_argument("--rate-only", action="store_true", help="enumerate and rate, read nothing in full")
    p.add_argument("--site", default="en.wikipedia.org", help="which approved site to read (default: Wikipedia)")
    p.add_argument("--rate-budget", type=int, default=None,
                   help="most new leads to rate this run (default: all on Wikipedia, 12 per target game elsewhere)")
    p.add_argument("--no-rate", action="store_true", help="skip rating; every lead is eligible")
    p = sub.add_parser("calibrate")
    p.add_argument("--model", required=True, help="backend for the rater")
    p.add_argument("--site", default="en.wikipedia.org", help="which site's pages to rate (default: Wikipedia)")

    args = ap.parse_args(argv)
    inv = Inventory(args.dir)

    try:
        if args.cmd == "add":
            rec = inv.add(from_dict(json.loads(args.file.read_text())))
            print(line(rec))
            for reason in rec.reasons:
                print(f"  {reason}")
        elif args.cmd == "check":
            for rec in [inv.check(args.id)] if args.id else inv.check_all():
                print(line(rec))
        elif args.cmd == "recheck":
            moved = inv.recheck()
            for game_id, before, after in moved:
                print(f"{game_id:<24} {before} -> {after}")
            print(f"{len(moved)} moved")
        elif args.cmd == "list":
            for r in inv.all():
                if not args.status or r.status == args.status:
                    print(line(r))
        elif args.cmd == "show":
            print(json.dumps(inv.get(args.id).to_dict(), indent=2))
        elif args.cmd == "queue":
            for r in inv.queue():
                print(line(r))
        elif args.cmd == "index":
            inv.write_index()
            print(inv.index_path)
        elif args.cmd == "calibrate":
            return calibrate_command(args, inv)
        elif args.cmd == "suggest":
            return suggest_command(args, inv)
        elif args.cmd == "sources":
            return sources_command(args, inv)
        elif args.cmd == "crawled":
            print(log_report(open_log(args), inv))
        elif args.cmd in ("discover", "crawl"):
            return crawl_command(args, inv)
        elif args.cmd == "gaps":
            for need, n in inv.gaps().most_common():
                print(f"{n:>3}  {need}")
            if not inv.gaps():
                print("no game is blocked")
    except (RecordError, KeyError, OSError, json.JSONDecodeError, SourceError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
