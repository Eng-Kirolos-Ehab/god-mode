# Changelog

## 2.0.0

**Pick what you install**
- God Mode is now a small core plugin (`god-mode`: router, rules, token protocol, setup) plus 8 optional category plugins in the same marketplace: `gm-web-design`, `gm-qa-audit`, `gm-seo-writing`, `gm-video`, `gm-career`, `gm-automation`, `gm-study`, `gm-interior`.
- First-run setup (`/god-mode:setup`): Claude asks which categories you want (multi-select, with a description and download size for each), installs only those, and lets you change them later. A removal always needs a yes.
- OpenWolf is set up automatically (pinned to 2.5.3). During setup it runs in the current git project, and the session hook reminds Claude to set it up in new git projects. Your existing CLAUDE.md and `.claude/settings.json` are kept.
- One session-start hook in the core. It only prints a note for Claude. It doesn't download or change anything itself.
- The manual installers (`install.sh`, `install.ps1`) show the same category menu, and also take `--categories` / `--all` / `--no-openwolf`.
- `categories.json` is the single source of truth. `tools/build_catalog.py` regenerates the plugin manifests, the marketplace, the sizes, the setup table and the README tables, and fails if a category's list doesn't match its files.

**Practical descriptions, and ask instead of assume**
- Every category and every skill or agent now says what you'd type, what you get, and what it will ask you first. The README skill map is grouped by the same 8 categories as the picker.
- Agents that used to start without basics now ask first in one message: `mobile-app-qa`, `web-auditor`, `seo-ai-visibility`, `dashboard-reviewer`, `mobile-ui-reviewer`. The router has a new rule: ask for user facts once, never invent them.
- `lecture-summary-pdf`: the author's personal formatting choices are now defaults the skill asks about (question count, recap language, cover page).
- `seo-ai-visibility`: its description had an unquoted `: `, which broke the YAML header, so in 1.x the agent loaded without its description. Fixed.
- `color-palette-swap` was described as recoloring a codebase. It recolors a design image (PSD/PNG/JPG) using a palette image. Fixed in the router and the catalog.

**Upgrading from 1.x:** updating `god-mode@god-mode` now gives you the core only. Your next session asks which categories to add back. Pick the ones you used.

## 1.1.0

**promo-film-maker**
- New "which tool for which job" table covering lemo-opuscar, video-use, ffmpeg-skill, claude-shorts, HyperFrames, Remotion, iart-ai motion skills and auto-editor.
- Transcription runs locally by default. No paid API keys without the user's explicit yes.

**job-hunter**
- Gate before building a CV: keyword coverage of at least 60%, seniority, posting age, the title skill, and no repeat applications to the same company.
- One umbrella identity across the CV and LinkedIn, and the same numbers on every form.
- Missing impact numbers are marked `[ASK USER]`, never invented. Early-stage products are described by the scope that was built.
- The PDF text is checked so keywords survive ligatures.
- Expected salary is researched from the market with sources. Current salary is never fabricated.
- Each easy-apply is paired with a direct message to the recruiter.

**EXTERNAL_SKILLS.md**
- Added the video toolkit (video-use, ffmpeg-skill, claude-shorts, HyperFrames, Remotion skill, motion skills, auto-editor, faster-whisper) and threejs-skills.
- New "Before you install" checklist: review first, install only a few skills, turn off telemetry.
- New Windows notes: a full ffmpeg build, pinning `av<16` for faster-whisper, CPU fallback without CUDA, local transcription for video-use, and claude-shorts without WSL.

## 1.0.0
- First public release: router skill, 8 skills, 9 agents, standing rules, token stats.
