# kermione

One-command installer for [God Mode](https://github.com/Eng-Kirolos-Ehab/god-mode), a plugin for Claude Code. God Mode routes each request to one fitting skill or agent, and works under fixed safety and token-saving rules.

```bash
npx kermione@godmode
```

Works on Windows, macOS and Linux. Run it inside your project folder.

## What happens

1. Adds the God Mode marketplace to Claude Code and installs the core (router, rules, setup).
2. Shows the categories with a description and size for each. Move with the arrows, select with space, `a` for all, enter to finish.
3. Installs the ones you picked.
4. Sets up [OpenWolf](https://www.npmjs.com/package/openwolf), a local project index, in the current git project. Your existing settings and CLAUDE.md are kept.

## Categories

Web & Design · QA & Audit · SEO & Writing · Video & Marketing · Career · Automation & Agents · Study · Interior Design

## Options

| Option | Effect |
|---|---|
| `--all` | install every category without the menu |
| `--categories gm-career,gm-video` | install these categories |
| `--no-openwolf` | skip OpenWolf |
| `--help` | show help |

## Requirements and safety

Node 18+ and the Claude Code CLI. The installer has no dependencies and needs no API keys. It runs `claude plugin` and `npx openwolf`, and it reads the category list from GitHub.

To change categories later, type `/god-mode:setup` in Claude Code. To remove it, use `/plugin uninstall god-mode` and the `gm-*` plugins.

## بالعربي

أمر واحد يسطّب God Mode على Claude Code: موزّع بيختار المهارة أو الوكيل المناسب لكل طلب، مع قواعد أمان وتوفير توكنز. بتختار الأقسام اللي محتاجها بس، ومن غير مفاتيح API.

MIT license.
