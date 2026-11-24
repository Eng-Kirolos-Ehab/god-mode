---
name: setup
description: God Mode first-run setup and category picker. Asks the user which God Mode categories to install (multi-select, with a description and download size for each), installs only those, and sets up OpenWolf automatically. Use when God Mode's session hook says setup is pending, or when the user says "god mode setup", "add/remove god mode categories", or "/god-mode:setup".
argument-hint: "[optional: category ids to install without asking]"
license: MIT
---

# God Mode setup

God Mode is a small core (this setup, the router, the rules) plus optional **categories**, each its own plugin in the `god-mode` marketplace. Install only what the user picks.

## Catalog

<!-- CATALOG:START -->
| # | Category (plugin id) | Size | What you get | Extras |
|---|---|---|---|---|
| 1 | **Web & Design** (`gm-web-design`) | 51 KB | Clone a website into Next.js, swap a color palette across a codebase, and two reviewers for phone-width pages and dashboards. Contains: skill `clone-website`, skill `color-palette-swap`, agent `dashboard-reviewer`, agent `mobile-ui-reviewer`. | — |
| 2 | **QA & Audit** (`gm-qa-audit`) | 3.5 KB | Agents that test a mobile app before a store build and find why a site is broken or slow (CORS, 500s, routes). Contains: agent `mobile-app-qa`, agent `web-auditor`. | — |
| 3 | **SEO & Writing** (`gm-seo-writing`) | 46 KB | SEO and AI-crawler visibility audits, rewrite text that sounds like AI, and bilingual Arabic/English news articles. Contains: skill `humanizer`, skill `saudi-news-curator`, agent `seo-ai-visibility`. | — |
| 4 | **Video & Marketing** (`gm-video`) | 2.7 KB | Promo films, trailers, shorts and captions with launch copy. Picks the right video tool for each job. Contains: agent `promo-film-maker`. | Optional video toolkit (ffmpeg, faster-whisper, video tools) ≈1 GB, offered separately and only if you say yes. |
| 5 | **Career** (`gm-career`) | 28 KB | CV and LinkedIn optimizer, an ATS-aware job hunter that tailors a CV per job, and a job-site accounts registry. Contains: skill `cv-optimizer`, agent `accounts-keeper`, agent `job-hunter`. | — |
| 6 | **Automation & Agents** (`gm-automation`) | 11 KB | Get data from websites through their own requests, and an office-manager agent that splits big tasks across specialists. Contains: skill `api-anything`, agent `office-manager`. | — |
| 7 | **Study** (`gm-study`) | 5.3 KB | Turn a lecture PDF into a designed A4 study summary with mind maps, diagrams and exam questions. Contains: skill `lecture-summary-pdf`. | — |
| 8 | **Interior Design** (`gm-interior`) | 13 KB | Room layouts, furniture plans, bills of quantities and mood boards. Contains: skill `interior-design-engineer`. | — |

Core (always installed): 19 KB. OpenWolf: ≈3 MB (npm), pinned to 2.5.3.
<!-- CATALOG:END -->

## Steps

1. **See what's installed.** Run `claude plugin list` and note which `gm-*@god-mode` plugins are already installed and enabled. If the command isn't available, read `installed_plugins.json` in the Claude config folder (`$CLAUDE_CONFIG_DIR` or `~/.claude/plugins/`).

2. **Ask with the AskUserQuestion tool.** Use two questions, each with `multiSelect: true`. Put categories 1–4 in the first question and 5–8 in the second, because a question holds at most 4 options.
   - Option **label**: the category name, a middle dot, then its size, e.g. `Career · 9 KB`. Add `✓` at the end if it's already installed.
   - Option **description**: the "What you get" text, plus the Extras text when there is one.
   - Question header: `Categories` and `More`. Question text, e.g.: "Which God Mode categories do you want? Pick any number. Sizes are download sizes."
   - Write the questions in the user's language. Keep the plugin ids in English.
   - If AskUserQuestion isn't available, print the catalog as a numbered list with sizes and ask the user to reply with numbers (e.g. `1 3 5`), or `all`.
   - If the user passed category ids as an argument, skip the question and use those.

3. **Apply the choice.**
   - For each selected category that isn't installed: `claude plugin install <id>@god-mode`.
   - For each installed category the user did **not** select: don't remove it silently. Ask once: "Remove <names>?" Uninstall (`claude plugin uninstall <id>@god-mode`) only on a clear yes.
   - Report each result in one line. If a command fails, show the error and carry on with the rest.

4. **OpenWolf (automatic, no question).** OpenWolf keeps a local project index, memory and bug log, and records token use. It's part of God Mode's token-saving protocol.
   - Run `node --version`. If Node 18+ is missing, tell the user OpenWolf needs Node and skip this step.
   - Find the project root: the folder with `.git`, or the current folder. Skip it if that folder is the user's home folder or a system folder. The session hook will set it up the next time a project is opened.
   - If the project has no `.wolf/` folder, run in the project root: `npx -y openwolf@<version from the catalog> init --agent claude`.
   - Tell the user in one or two lines what it added: a `.wolf/` folder, hooks in `.claude/settings.json`, and a few lines at the top of `CLAUDE.md`. Their existing settings and CLAUDE.md are kept. It runs locally only.

5. **Video toolkit (only if Video & Marketing was selected).** Ask one yes/no question: install the optional video toolkit now? It's about 1 GB: a full ffmpeg build with libx264, faster-whisper, and the video skills listed in [EXTERNAL_SKILLS.md](https://github.com/Eng-Kirolos-Ehab/god-mode/blob/main/EXTERNAL_SKILLS.md). On yes, follow that file, including its "Before you install" checklist and Windows notes. On no, say the `promo-film-maker` agent still works and will tell them what's missing when they need it.

6. **Save the choice** to `<config>/god-mode/setup.json`, where `<config>` is `$CLAUDE_CONFIG_DIR` or `~/.claude`:
   ```json
   {"version": "<core version>", "categories": ["gm-..."], "openwolf": "auto", "updated": "<ISO date>"}
   ```
   Create the folder if it's missing. This file stops the first-run prompt from coming back.

7. **Finish** with a short summary: what was installed, the total size, and OpenWolf's status. Then say: "Restart Claude Code (or run `/reload-plugins`) to load the new categories. Change them any time with `/god-mode:setup`."

## Rules
- Never install a category the user didn't pick, and never remove one without a yes.
- Never add API keys or paid services during setup.
- Pin OpenWolf to the version in the catalog. Don't use `@latest`.
