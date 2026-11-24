"""Summarise an OpenWolf token ledger (.wolf/token-ledger.json) into stats/token-stats.json.

Usage: python tools/token_stats.py path/to/.wolf/token-ledger.json
"""
import collections, json, sys

ledger = json.load(open(sys.argv[1], encoding="utf-8"))
life = ledger["lifetime"]
months = collections.defaultdict(lambda: {"sessions": 0, "repeated_reads_blocked": 0, "input_tokens": 0, "output_tokens": 0})
for s in ledger["sessions"]:
    m = (s.get("ended") or s.get("started") or "")[:7]
    if not m:
        continue
    t = s.get("totals", {})
    months[m]["sessions"] += 1
    months[m]["repeated_reads_blocked"] += t.get("repeated_reads_blocked", 0)
    months[m]["input_tokens"] += t.get("input_tokens_estimated", 0)
    months[m]["output_tokens"] += t.get("output_tokens_estimated", 0)

used, saved = life["total_tokens_estimated"], life["estimated_savings_vs_bare_cli"]
lookups = life["anatomy_hits"] + life["anatomy_misses"]
out = {
    "tokens_used": used,
    "tokens_saved_estimate": saved,
    "without_protocol_estimate": used + saved,
    "reduction_pct": round(100 * saved / (used + saved), 1),
    "work_sessions": life["total_sessions"],
    "file_reads": life["total_reads"],
    "file_writes": life["total_writes"],
    "repeated_reads_blocked": life["repeated_reads_blocked"],
    "index_hit_rate_pct": round(100 * life["anatomy_hits"] / lookups, 1) if lookups else 0,
    "by_month": dict(sorted(months.items())),
}
json.dump(out, open("stats/token-stats.json", "w"), indent=2)
print(json.dumps({k: v for k, v in out.items() if k != "by_month"}, indent=2))
