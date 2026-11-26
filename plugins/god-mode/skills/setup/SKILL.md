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
| # | Category (plugin id) | Size | What it does for you | Try saying | Extras |
|---|---|---|---|---|---|
| 1 | **Web & Design** (`gm-web-design`) | 52 KB | Copy a website you like into a Next.js project, recolor a design image with a new palette, and get a scored review of a site or dashboard on a phone. | "clone https://example.com into Next.js" · "recolor this design with this palette (attach both images)" | — |
| 2 | **QA & Audit** (`gm-qa-audit`) | 4.3 KB | Test a mobile app before you publish it, or find out why a website is broken or slow, with a backup and rollback for every fix. | "test this build before I upload it" · "my site is stuck loading / shows 500" | — |
| 3 | **SEO & Writing** (`gm-seo-writing`) | 35 KB | Get found on Google and in AI answers, and make AI-sounding text read like a person wrote it. | "why isn't my site showing on Google or in ChatGPT?" · "make this sound less like AI (paste text)" | — |
| 4 | **Video & Marketing** (`gm-video`) | 2.7 KB | Turn a product or a raw recording into a promo film, a trailer or vertical shorts with captions, plus the post and store text to go with it. | "make a 30-second promo for my app" | Optional video toolkit (ffmpeg, faster-whisper, video tools) ≈1 GB, offered separately and only if you say yes. |
| 5 | **Career** (`gm-career`) | 28 KB | Fix your CV and LinkedIn for ATS, check which jobs you really fit, and get a tailored CV and application drafts for each one. You send them. | "analyze my CV for this job (paste both)" · "apply to this job (paste the post)" | — |
| 6 | **Automation & Agents** (`gm-automation`) | 11 KB | Pull data from a website without scraping the page, and hand a big task to a manager agent that splits it across specialists. | "get the flight prices from A to B on <site>" · "someone handle the launch checklist" | — |
| 7 | **Study** (`gm-study`) | 6.0 KB | Upload a lecture and get one printable PDF: mind maps, diagrams, exam traps and a question bank with answers. | "لخّص المحاضرة دي (attach the PDF)" | — |
| 8 | **Interior Design** (`gm-interior`) | 13 KB | Plan a room from your photos and measurements: layout, furniture, lighting, a bill of quantities and a mood board. | "design my living room 4×5 m (attach photos)" | — |
| 9 | **Content & Hooks** 🆕 (`gm-content`) | 30 KB | Write scroll-stopping hooks, titles and 3-column scripts for reels and shorts, then turn the approved script into a polished motion video with sound effects on the beat. Handles Arabic and other right-to-left text. | "write 5 hooks and a 20-second reel script for my app" · "animate this approved script as a 9:16 reel" | Optional: earshot for sound effects (Python, CPU only); a video renderer such as HyperFrames or Remotion. |
| 10 | **Business** 🆕 (`gm-business`) | 3.3 KB | Read a contract, offer or scope document before you sign: every obligation with its date, the risky clauses ranked, the questions to ask and the wording to request. | "review this contract before I sign (paste it)" | — |

Core (always installed): 25 KB. OpenWolf: ≈3 MB (npm), pinned to 2.5.3.
<!-- CATALOG:END -->

## Update mode

When the session hook says God Mode was updated, only the new categories need a question. Ask about those alone (one multiSelect question, plus a "Not now" option), install what the user picks, then save `"version"` in `setup.json` (step 6). Skip OpenWolf and the video toolkit unless the user asks for them.

## Steps

1. **See what's installed.** Run `claude plugin list` and note which `gm-*@god-mode` plugins are already installed and enabled. If the command isn't available, read `installed_plugins.json` in the Claude config folder (`$CLAUDE_CONFIG_DIR` or `~/.claude/plugins/`).

2. **Ask with the AskUserQuestion tool.** Use one question per group of 4 categories (a question holds at most 4 options), each with `multiSelect: true`: categories 1–4, 5–8, then 9–10. Categories marked 🆕 in the catalog are new in this version: keep the 🆕 in their option label.
   - Option **label**: the category name, a middle dot, then its size, e.g. `Career · 9 KB`. Add `✓` at the end if it's already installed.
   - Option **description**: the "What it does for you" text, then `e.g.` and the first "Try saying" example, plus the Extras text when there is one. Keep it practical: what the user types and what they get back.
   - Question header: `Categories`, `More` and `New`. Question text, e.g.: "Which God Mode categories do you want? Pick any number. Sizes are download sizes."
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
