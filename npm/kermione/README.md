# kermione

Install [God Mode](https://github.com/Eng-Kirolos-Ehab/god-mode) for Claude Code in one command:

```bash
npx kermione@godmode
```

It adds the God Mode marketplace to Claude Code, installs the core, shows a menu of 8 categories (Web & Design, QA & Audit, SEO & Writing, Video & Marketing, Career, Automation & Agents, Study, Interior Design), each with a description and download size, installs the ones you pick, and sets up OpenWolf in the current git project.

Use ↑/↓ to move, space to select, `a` for all and enter to finish.

Options: `--all`, `--categories gm-career,gm-video`, `--no-openwolf`.

Requires Node 18+ and the Claude Code CLI. No dependencies. It only runs `claude plugin ...` and `npx openwolf`.
