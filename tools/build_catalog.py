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
        listed = {(i["type"], i["name"]) for i in c.get("items", [])}
        actual = {("skill", s) for s in what["skills"]} | {("agent", a) for a in what["agents"]}
        if listed != actual:
            raise SystemExit(f"{c['id']}: items in categories.json {sorted(listed)} != files {sorted(actual)}")
        for i in c["items"]:
            i["path"] = f"plugins/{c['id']}/skills/{i['name']}" if i["type"] == "skill" else f"plugins/{c['id']}/agents/{i['name']}.md"
            for k in ("say", "get", "asks"):
                if not i.get(k):
                    raise SystemExit(f"{c['id']}/{i['name']}: missing '{k}'")
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
        "categories": [{k: c[k] for k in ("id", "name", "emoji", "description", "extras", "skills", "agents", "items", "bytes", "size")} for c in cats],
    })

    # Plain TSV for install.sh (no JSON parser needed). Line 1 = meta, then one line per category.
    clean = lambda s: (s or "").replace("\t", " ").replace("\n", " ")
    tsv = [f"#meta\t{version}\t{core_size}\t{human(core_size)}\t{cfg['openwolf']['version']}"]
    tsv += [f"{c['id']}\t{clean(c['name'])}\t{c['size']}\t{c['bytes']}\t{clean(c['description'])}\t{clean(c['extras'])}" for c in cats]
    (ROOT / "catalog.generated.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8", newline="\n")

    rows = ["| # | Category (plugin id) | Size | What it does for you | Try saying | Extras |", "|---|---|---|---|---|---|"]
    for i, c in enumerate(cats, 1):
        tries = " · ".join(f"\"{it['say']}\"" for it in c["items"][:2])
        rows.append(f"| {i} | **{c['name']}** (`{c['id']}`) | {c['size']} | {c['description']} | {tries} | {c['extras'] or '—'} |")
    table = "\n".join(rows) + f"\n\nCore (always installed): {human(core_size)}. OpenWolf: {cfg['openwolf']['approx_download']}, pinned to {cfg['openwolf']['version']}."
    setup = core / "skills" / "setup" / "SKILL.md"
    text = setup.read_text(encoding="utf-8")
    new, n = re.subn(r"(<!-- CATALOG:START -->\n).*?(\n<!-- CATALOG:END -->)", lambda m: m.group(1) + table + m.group(2), text, flags=re.S)
    if n != 1:
        raise SystemExit("CATALOG markers not found in the setup SKILL.md")
    setup.write_text(new, encoding="utf-8")

    write_readme(cfg, cats, core_size)

    for c in cats:
        print(f"{c['id']:<16} {c['size']:>8}  {len(c['skills'])} skills, {len(c['agents'])} agents")
    print(f"core             {human(core_size):>8}")


def replace_block(text: str, name: str, body: str) -> str:
    new, n = re.subn(rf"(<!-- {name}:START -->).*?(<!-- {name}:END -->)", lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), text, flags=re.S)
    if n != 1:
        raise SystemExit(f"{name} markers not found in README.md")
    return new


def write_readme(cfg: dict, cats: list[dict], core_size: int) -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")

    cat_rows = ["| # | Category | Plugin id | Size | What it does for you |", "|---|---|---|---|---|"]
    for i, c in enumerate(cats, 1):
        extra = f" *{c['extras']}*" if c["extras"] else ""
        cat_rows.append(f"| {i} | {c['emoji']} **{c['name']}** | `{c['id']}` | {c['size']} | {c['description']}{extra} |")
    text = replace_block(text, "CATEGORIES", f"The core ({human(core_size)}) is always installed. Everything else is optional:\n\n" + "\n".join(cat_rows))

    def table(items: list[dict]) -> str:
        out = ["| Name | Type | Say something like | You get | It asks you for |", "|---|---|---|---|---|"]
        for it in items:
            out.append(f"| [{it['name']}]({it['path']}) | {it['type']} | \"{it['say']}\" | {it['get']} | {it['asks']} |")
        return "\n".join(out)

    mm = ["```mermaid", "mindmap", "  root((God Mode))", "    Core"] + [f"      {it['name']}" for it in cfg["core"]["items"]]
    for c in cats:
        mm.append(f"    {c['name']}")
        mm += [f"      {it['name']}" for it in c["items"]]
    mm.append("```")
    parts = ["\n".join(mm), "", f"<details open>\n<summary><b>🧭 {cfg['core']['name']} · {human(core_size)}</b></summary>\n\n{table(cfg['core']['items'])}\n</details>"]
    for c in cats:
        parts.append(f"<details>\n<summary><b>{c['emoji']} {c['name']} · {c['size']}</b> (<code>{c['id']}</code>)</summary>\n\n{c['description']}\n\n{table(c['items'])}\n</details>")
    text = replace_block(text, "SKILLMAP", "\n\n".join(parts))
    readme.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
