"""Human-readable views of a match log.

The JSON Lines file is the record. These renderers make it readable without
changing it, which is the whole point of logging everything in a structured way:
one complete record, many views.
"""

from __future__ import annotations

from typing import Any, Iterable

_ARROW = {"to_agent": "->", "from_agent": "<-"}


def timeline(records: Iterable[dict[str, Any]], show: set[str] | None = None) -> str:
    """The god view: everything, in order, grouped by round and phase."""
    show = show or {"process", "fact", "orchestrator", "turn", "result"}
    lines: list[str] = []
    header = None

    for r in records:
        if r["category"] not in show:
            continue

        key = (r.get("round"), r.get("phase"))
        if key != header and r.get("phase"):
            header = key
            lines.append(f"\n=== round {r.get('round')} / {r.get('phase')} ===")

        lines.append(_line(r))
    return "\n".join(lines).strip()


def _line(r: dict[str, Any]) -> str:
    cat, typ = r["category"], r["type"]
    n = r["log_seq"]

    if cat == "fact":
        who = r.get("entitled", [])
        scope = "all" if len(who) > 3 else who
        return f"[{n:4}] fact {typ} -> {scope}: {r.get('payload')}"

    if cat == "orchestrator":
        return f"[{n:4}] orch asks seat {r['seat']} to {r['action_schema']} ({r['reason']})"

    if cat == "turn":
        flag = " DEGRADED" if r.get("degraded") else ""
        act = r.get("action") or {}
        value = act.get("text") or act.get("target")
        return f"[{n:4}] seat {r['seat']} ({r['role']}) {act.get('type')}={value!r}{flag}"

    if cat == "message":
        seat = r["seat"]
        if typ == "to_agent":
            body = (r.get("body") or "").replace("\n", " | ")
            return f"[{n:4}] {_ARROW[typ]} seat {seat} [{r['msg_type']}] {body}"
        return f"[{n:4}] {_ARROW[typ]} seat {seat} {r.get('response')}"

    if cat == "process":
        detail = {k: v for k, v in r.items() if k not in _META}
        return f"[{n:4}] {typ} {detail if detail else ''}".rstrip()

    if cat == "result":
        return (
            f"\n[{n:4}] RESULT {r['status']}: {r['winner']} ({r['reason']})\n"
            f"       turns={r['turns']} rounds={r['rounds']} "
            f"degraded={r['degraded_turns']} roles={r['roles']}"
        )

    detail = {k: v for k, v in r.items() if k not in _META}
    return f"[{n:4}] {cat}/{typ} {detail}"


_META = {"log_seq", "ts", "category", "type", "round", "phase", "turn_seq"}


def seat_transcript(records: Iterable[dict[str, Any]], seat: int) -> str:
    """Exactly what one seat was sent, and what it replied.

    This is the seat's whole world. If it contains something the seat was not
    entitled to, the kernel leaked.
    """
    lines: list[str] = []
    for r in records:
        if r["category"] != "message" or r.get("seat") != seat:
            continue
        if r["type"] == "to_agent":
            lines.append(f"[{r['msg_type']}]")
            lines.append(r.get("body", ""))
        else:
            lines.append(f"  >> {r.get('response')}")
    return "\n".join(lines)


def summarize(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(records)
    counts: dict[str, int] = {}
    for r in rows:
        key = f"{r['category']}/{r['type']}"
        counts[key] = counts.get(key, 0) + 1
    result = next((r for r in rows if r["category"] == "result"), {})
    return {"records": len(rows), "counts": counts, "result": result}
