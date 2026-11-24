---
name: god-mode
description: Master skill that routes any request to the right specialist skill or agent in the God Mode collection, applies a set of battle-tested working rules, and runs a token-saving work protocol. Use at the start of any non-trivial task, when unsure which skill fits, or when the user says "god mode".
argument-hint: "[task in any language]"
license: MIT
---

# God Mode

One entry point for every skill and agent in this collection. Read this file first, then load **only** the skill or agent the task needs. Never load them all.

## 1. Route the task

Match the request to one row. When two rows fit, pick the more specific one. If nothing fits, do the task directly without forcing a skill.

Skills and agents ship in optional categories (the plugin id is in brackets). If the one you need isn't installed, say which category holds it and suggest `/god-mode:setup` to add it. Then do the task as well as you can without it.

| Domain | The request looks like | Use |
|---|---|---|
| Web clone | "copy this site", rebuild a site in Next.js | skill `clone-website` [gm-web-design] |
| Recolor | swap a palette across an existing codebase | skill `color-palette-swap` [gm-web-design] |
| UI colors | pick or check a palette, contrast, shades | `rules/design-color-rules.md` (core) |
| Interior design | room layout, furniture, BOQ, mood board | skill `interior-design-engineer` [gm-interior] |
| Writing | text sounds like AI, polish prose | skill `humanizer` [gm-seo-writing] |
| Careers | CV, LinkedIn, ATS, interview prep, cover letter | skill `cv-optimizer`, agent `job-hunter` [gm-career] |
| Accounts | sign in or sign up on job sites | agent `accounts-keeper` [gm-career] |
| Study | lecture PDF to a designed summary PDF | skill `lecture-summary-pdf` [gm-study] |
| News | Saudi or Gulf news, bilingual SEO article | skill `saudi-news-curator` [gm-seo-writing] |
| Data from sites | get data through a site's own requests | skill `api-anything` [gm-automation] |
| Mobile QA | test an app before a store build | agent `mobile-app-qa` [gm-qa-audit] |
| Web audit | site stuck loading, CORS, 500s, slow | agent `web-auditor` [gm-qa-audit] |
| SEO | indexing, AI crawlers, structured data | agent `seo-ai-visibility` [gm-seo-writing] |
| Video/marketing | promo film, trailer, edit my footage, shorts, captions, launch copy | agent `promo-film-maker` (it picks the right video tool) [gm-video] |
| Dashboards | review an admin, analytics or smart-home dashboard | agent `dashboard-reviewer` [gm-web-design] |
| Mobile web review | phone-width review of a site or portfolio | agent `mobile-ui-reviewer` [gm-web-design] |
| God Mode itself | add or remove categories, first-run setup | skill `setup` (core) |
| Many specialists | broad task, "someone handle this" | agent `office-manager` [gm-automation] |

Recommended extras (installed separately; see [EXTERNAL_SKILLS.md](https://github.com/Eng-Kirolos-Ehab/god-mode/blob/main/EXTERNAL_SKILLS.md)): `ui-ux-pro-max` for UI design, `career-ops` for job tracking, Anthropic's `docx`/`xlsx`/`pptx`/`pdf` for office files.

## 2. Token-saving protocol

1. **Index before reading.** If the project keeps a file index (e.g. `.wolf/anatomy.md`, a README map), check it first. If the description answers the question, don't open the file.
2. **No repeated reads.** Don't re-read a file that hasn't changed this session.
3. **Targeted search.** Grep for the exact symbol and read only that line range of big files.
4. **Parallel calls.** Send independent tool calls in one message.
5. **Few subagents.** Spawn them only for wide searches or when asked. Each one starts cold.
6. **Media stays in scripts.** Handle photos, PDFs and video frames with code. Never paste base64 or huge output into context.
7. **Known fixes first.** If the project keeps a bug log, check it before debugging.

## 3. Learn every session

- User correction → record it as a rule with the date and the reason (in the project's CLAUDE.md or notes file).
- Bug fixed → log the error, root cause, fix and tags.
- Files created or renamed → update the project index.

Read `rules/standing-rules.md` once per session before the first change.

## 4. Safety lines (never cross)

- **No deletes** of the user's files, data or rows without written permission in chat.
- **No sending** emails or messages on the user's behalf unless asked for that specific one. Leave drafts instead.
- **No real-world side effects while testing:** no real orders, payments or deliveries on live systems. Use a test environment.
- **No secrets** in output, commits, or requests to outside services.
- **Back up before any production write**, and write down the rollback.
- **Check the live state** (git remote, deployed version, DB value) before changing it. Don't trust memory.
