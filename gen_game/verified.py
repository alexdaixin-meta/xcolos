"""VERIFIED.md: the prompt that built the game, shown to be the one that was sent, and what the game did.

It reads the artifacts and the call log and checks them against each other, rather than reporting what the
flow believes it did: the coder's saved prompt is compared with the prompt the log says was sent, the game
file is run through the same checks the flow uses, and the scenarios and tiers are run again.
"""

from __future__ import annotations

import json
from pathlib import Path

from gen_game import calls, encode as enc, evaluate, scenarios


def write(folder: Path) -> Path:
    folder = Path(folder)
    out = [f"# Verification of {folder.name}", ""]
    log = [json.loads(l) for l in (folder / "logs" / "calls.jsonl").read_text().splitlines()] if (folder / "logs" / "calls.jsonl").exists() else []

    out += ["## Every model call, in order", "", "| n | step | model | seconds | sent | reply | |", "|---|---|---|---|---|---|---|"]
    for c in log:
        out.append(f"| {c['n']:02d} | {c['step']} | {c['model']} | {c['seconds']} | {c['sent_chars']} chars | {c['reply_chars']} chars | "
                   f"{'ERROR: ' + c['error'] if c['error'] else ''} |")
    out.append("")

    out += ["## The prompt the coder was given", ""]
    coder_calls = [c for c in log if c["step"] == "coder"]
    for name in ("CODER_PROMPT.md", "AGENT_PROMPT.md"):
        path = folder / name
        if not path.exists():
            continue
        text = path.read_text()
        h = calls.sha(text)
        first = next((c for c in coder_calls if c["sent_sha256"] == h), None)
        out.append(f"- `{name}`: sha256 {h[:16]}, {len(text)} chars. " + (
            f"MATCHES call {first['n']:02d}: this is exactly what was sent." if first else
            "no coder call in the log carries this hash" + (" (an agent reads this file itself; see logs/agent_output.md)" if name == "AGENT_PROMPT.md" else "")))
    if coder_calls:
        last = coder_calls[-1]
        out.append(f"- the coder was called {len(coder_calls)} time(s); the last was call {last['n']:02d}")
    out.append("")

    game_path = folder / "game.json"
    if game_path.exists():
        out += ["## The game file", ""]
        out.append(f"- `game.json`: sha256 {calls.sha(game_path.read_text())[:16]}")
        spec = json.loads((folder / "spec.json").read_text()) if (folder / "spec.json").exists() else {}
        tests = json.loads((folder / "scenarios.json").read_text()) if (folder / "scenarios.json").exists() else None
        obj, defn, problem = enc.check(game_path.read_text(), folder.name, set(spec.get("parameters", {})), tests)
        out.append(f"- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): "
                   + ("**all pass**" if defn else f"**FAIL: {problem[:400]}**"))
        if defn:
            results = scenarios.run_all(defn, tests or [])
            out.append(f"- independent scenarios: {sum(o.passed for o in results)} of {len(results)} pass")
            t0 = evaluate.tier0(defn)
            out.append(f"- tier 0 (valid, ends, replays identically): {'passed' if t0['passed'] else 'FAILED'}; results over {t0['metrics']['matches']} random matches: {t0['metrics']['results']}")
            out.append("- reasoning and balance: not checked here (real models will play it later)")
        out.append("")
    (folder / "VERIFIED.md").write_text("\n".join(out) + "\n")
    return folder / "VERIFIED.md"
