"""Regenerate every file derived from categories.json.

Run after adding, removing or editing a skill/agent:
    python tools/build_catalog.py

Writes:
  - plugins/<id>/.claude-plugin/plugin.json   (one per category)
  - plugins/god-mode/.claude-plugin/plugin.json (core: router + setup + hook) and its openwolf.version
  - .claude-plugin/marketplace.json            (core + all categories)
  - catalog.generated.json                     (sizes and contents, read by install.sh / install.ps1)
  - catalog.generated.tsv (same, for install.sh)
  - the catalog table inside plugins/god-mode/skills/setup/SKILL.md (between the CATALOG markers)
Standard library only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUTHOR = {"name": "Kirolos Ehab", "url": "https://github.com/Eng-Kirolos-Ehab"}
REPO = "https://github.com/Eng-Kirolos-Ehab/god-mode"
CORE_DIR = "plugins/god-mode"


def size_of(paths: list[Path]) -> int:
    total = 0
    for p in paths:
        if p.is_file():
            total += p.stat().st_size
        elif p.is_dir():
            total += sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
    return total


def human(n: int) -> str:
    return f"{n / 1024:.0f} KB" if n >= 10 * 1024 else f"{n / 1024:.1f} KB"


def contents(plugin_dir: Path) -> dict:
    skills = sorted(p.name for p in (plugin_dir / "skills").glob("*") if p.is_dir()) if (plugin_dir / "skills").exists() else []
    agents = sorted(p.stem for p in (plugin_dir / "agents").glob("*.md")) if (plugin_dir / "agents").exists() else []
    return {"skills": skills, "agents": agents}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    cfg = json.loads((ROOT / "categories.json").read_text(encoding="utf-8"))
    version = cfg["version"]
    market = cfg["marketplace"]

    core = ROOT / CORE_DIR
    core_size = size_of([core / "skills", core / "hooks"])
    (core / "openwolf.version").write_text(cfg["openwolf"]["version"] + chr(10), encoding="utf-8", newline=chr(10))
    cats = []
    for c in cfg["categories"]:
        d = ROOT / "plugins" / c["id"]
        if not d.is_dir():
            raise SystemExit(f"missing plugin folder: {d}")
        what = contents(d)
        if not what["skills"] and not what["agents"]:
            raise SystemExit(f"empty category: {c['id']}")
        size = size_of([d / "skills", d / "agents"])
        write_json(d / ".claude-plugin" / "plugin.json", {
            "name": c["id"],
            "version": version,
            "description": f"God Mode · {c['name']}: {c['description']}",
            "author": AUTHOR,
            "homepage": REPO,
            "repository": REPO,
            "license": "MIT",
        })
        cats.append({**c, **what, "bytes": size, "size": human(size)})

    write_json(core / ".claude-plugin" / "plugin.json", {
        "name": "god-mode",
        "version": version,
        "description": "God Mode core: router skill, standing rules, token-saving protocol and a first-run setup that lets you pick which categories to install. Installs OpenWolf automatically.",
        "author": AUTHOR,
        "homepage": REPO,
        "repository": REPO,
        "license": "MIT",
        "keywords": ["skills", "agents", "router", "token-saving", "productivity", "arabic"],
    })

    plugins = [{
        "name": "god-mode",
        "source": "./plugins/god-mode",
        "description": "Core: router, rules, token protocol, first-run category picker. Install this one.",
        "version": version,
        "license": "MIT",
        "category": "productivity",
    }] + [{
        "name": c["id"],
        "source": f"./plugins/{c['id']}",
        "description": f"{c['name']}: {c['description']}",
        "version": version,
        "license": "MIT",
        "category": "productivity",
    } for c in cats]
    write_json(ROOT / ".claude-plugin" / "marketplace.json", {
        "name": market,
        "owner": AUTHOR,
        "metadata": {"description": "God Mode skill collection for Claude Code", "version": version},
        "plugins": plugins,
    })

    write_json(ROOT / "catalog.generated.json", {
        "version": version,
        "marketplace": market,
        "core": {"bytes": core_size, "size": human(core_size)},
        "openwolf": cfg["openwolf"],
        "categories": [{k: c[k] for k in ("id", "name", "description", "extras", "skills", "agents", "bytes", "size")} for c in cats],
    })

    # Plain TSV for install.sh (no JSON parser needed). Line 1 = meta, then one line per category.
    clean = lambda s: (s or "").replace("\t", " ").replace("\n", " ")
    tsv = [f"#meta\t{version}\t{core_size}\t{human(core_size)}\t{cfg['openwolf']['version']}"]
    tsv += [f"{c['id']}\t{clean(c['name'])}\t{c['size']}\t{c['bytes']}\t{clean(c['description'])}\t{clean(c['extras'])}" for c in cats]
    (ROOT / "catalog.generated.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8", newline="\n")

    rows = ["| # | Category (plugin id) | Size | What you get | Extras |", "|---|---|---|---|---|"]
    for i, c in enumerate(cats, 1):
        inside = ", ".join([f"skill `{s}`" for s in c["skills"]] + [f"agent `{a}`" for a in c["agents"]])
        rows.append(f"| {i} | **{c['name']}** (`{c['id']}`) | {c['size']} | {c['description']} Contains: {inside}. | {c['extras'] or '—'} |")
    table = "\n".join(rows) + f"\n\nCore (always installed): {human(core_size)}. OpenWolf: {cfg['openwolf']['approx_download']}, pinned to {cfg['openwolf']['version']}."
    setup = core / "skills" / "setup" / "SKILL.md"
    text = setup.read_text(encoding="utf-8")
    new, n = re.subn(r"(<!-- CATALOG:START -->\n).*?(\n<!-- CATALOG:END -->)", lambda m: m.group(1) + table + m.group(2), text, flags=re.S)
    if n != 1:
        raise SystemExit("CATALOG markers not found in the setup SKILL.md")
    setup.write_text(new, encoding="utf-8")

    for c in cats:
        print(f"{c['id']:<16} {c['size']:>8}  {len(c['skills'])} skills, {len(c['agents'])} agents")
    print(f"core             {human(core_size):>8}")


if __name__ == "__main__":
    main()
