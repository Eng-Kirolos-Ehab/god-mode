# External skills & plugins

God Mode recommends these but does not copy them. Each stays under its own license. Install each from its source.

| Name | Domain | Source | Install |
|---|---|---|---|
| ui-ux-pro-max | Web & Design | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | follow the repo README |
| motionsites-web-builder | Web & Design | [motionsites.ai](https://motionsites.ai) | free skill from MotionSites |
| career-ops | Career | [santifer/career-ops](https://github.com/santifer/career-ops) | `npx @santifer/career-ops` |
| lemo-opuscar | Video | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | `/plugin marketplace add lemomo-ai/lemo-opuscar` |
| video-use | Video | [browser-use/video-use](https://github.com/browser-use/video-use) | follow its `install.md` (needs ffmpeg + ffprobe) |
| ffmpeg-skill | Video | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | `npx ffmpeg-skill`, then `npx ffmpeg-skill doctor` |
| claude-shorts | Video | [AgriciDaniel/claude-shorts](https://github.com/AgriciDaniel/claude-shorts) | `bash setup.sh && bash install.sh` (see Windows notes) |
| HyperFrames | Video | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes` |
| Remotion skill | Video | [haidrrrry/claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill) | copy `remotion-motion-graphics/` into your skills folder |
| motion skills | Video | [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) (index of packs) | `npx skills add iart-ai/<pack>`. Install only the packs you need |
| threejs-skills | 3D / Web | [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) | `npx skills add cloudai-x/threejs-skills` |
| auto-editor | Video | [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | `pip install auto-editor` |
| faster-whisper | Speech-to-text | [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | `pip install faster-whisper` |

## Before you install any of these
- Read the repo first. Check the install script, any hooks or MCP servers it adds, and any network calls. Prefer installing from a clone you reviewed over a fresh `npx` or `curl | sh`.
- Every installed skill's description loads into every session. Install the few packs you'll use, not whole collections.
- Turn off telemetry where offered (HyperFrames: `HYPERFRAMES_NO_TELEMETRY=1`).
- Several video skills trigger on the same words. The `promo-film-maker` agent has a table of which tool fits which job.

## Video toolkit: Windows notes (tested late 2026)
- **ffmpeg:** use a full GPL build that includes `libx264` (for example the BtbN Windows builds), with `ffprobe` next to it on PATH. Minimal builds can't encode H.264.
- **faster-whisper + PyAV:** PyAV 16 or newer breaks faster-whisper 1.2.x (`open() got an unexpected keyword argument 'metadata_errors'`). Pin `pip install "av<16"`.
- **faster-whisper on an NVIDIA PC without the CUDA 12 runtime:** `device="auto"` fails with `cublas64_12.dll not found`. Use `device="cpu"` with `compute_type="int8"`.
- **video-use without ElevenLabs:** you can swap its Scribe call for local faster-whisper by returning the same JSON shape: `words[]` entries with `type` set to `word` or `spacing`, plus `start`, `end`, `text` and `speaker_id`.
- **claude-shorts on Windows without WSL:** create a venv anywhere, junction it to `~/.shorts-skill`, add a `bin` junction pointing to `Scripts`, and copy `python.exe` to `python3.exe`. Skip PyTorch, which is only used to detect a GPU; it falls back to CPU. It also needs `jq` on PATH. Pass `--model small` on CPU, because the default `large-v3` is slow.
- **pip conflicts:** run `pip check` after every install. Heavy packages can quietly upgrade shared ones like `typing-extensions`.
| vercel | Deploy | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | `/plugin install vercel@claude-plugins-official` |
| figma | Design | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | `/plugin install figma@claude-plugins-official` |
| rust-analyzer-lsp | Engineering | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | `/plugin install rust-analyzer-lsp@claude-plugins-official` |
| docx / xlsx / pptx / pdf | Docs | [anthropics/skills](https://github.com/anthropics/skills) | built into Claude apps |
| OpenWolf | Token protocol | [openwolf on npm](https://www.npmjs.com/package/openwolf) | `npx openwolf init` |

## Engineering skills

Copy only the folders you want into `~/.claude/skills/`.

| Skill | Source | Use it for |
|---|---|---|
| `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | schema, RLS, indexes, slow queries |
| `webapp-testing` | [anthropics/skills](https://github.com/anthropics/skills) | testing a local web app with Playwright (needs Python Playwright) |
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) | new UI with its own visual direction |
| `systematic-debugging`, `verification-before-completion`, `writing-plans`, `executing-plans`, `test-driven-development` | [obra/superpowers](https://github.com/obra/superpowers) | engineering process |

The full superpowers plugin also adds a session hook that asks Claude to check for a skill before every reply. It overlaps with this router, so copy the single skills instead. Read each skill before you install it.

## The safety gate (use it for every outside skill)

Added in 2.2.0. It runs in order, and you stop at the first failure.

1. **Back up** your skills folder, plugins folder and settings (`tar -czf backup.tgz ~/.claude/skills ~/.claude/plugins ~/.claude/settings.json`). In Git Bash, use `/c/...` paths or `--force-local`, because `tar` reads `C:/...` as a remote host.
2. **Pin a copy:** `git clone --depth 1` into a quarantine folder, and note the commit.
3. **Scan offline** with [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) (Apache-2.0): `pip install skillspector` in its own virtual environment, then `skillspector scan <folder> --recursive --no-llm --format json > report.json`. `--no-llm` keeps everything on your machine. On Windows, leave out `--output` and redirect stdout instead.
4. **Read where each finding is.** The scanner is strict: docs, tests and benchmarks that mention `.env` or API keys score CRITICAL even in official plugins. What matters is code that runs at use time, such as network calls, hooks, edits to `settings.json` or the status line, or reading your chat transcripts.
5. **Check for overlap.** A skill with the same name, or one that does the same job as one you have, is a "no". Every description you add loads into every session.
6. **Install in the narrowest scope:** a single skill folder before a whole plugin, and `--scope local` for a trial. Then confirm it loads, and write down the command that removes it.

## Vetted in 2.2.0

These passed the gate above. Commits were reviewed in Nov 2026.

| Name | Source | What it adds | Notes |
|---|---|---|---|
| SkillSpector | [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | the scanner used by the gate | a tool, not a skill; Python 3.12–3.13 |
| earshot | [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot) (MIT) | sound effects from words, a bank aimed at picture, loudness measurements; used by `motion-polish` | `pip install` in its own venv, plus `librosa` for `measure`. The `listen` extra pulls torch (~1 GB) and is optional. Its MCP server is optional too, and skipping it saves tokens. The Gemini critique uploads audio, so use it only by choice |
| replica-skill | [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) (MIT) | 11 skills to clone an app and improve it from its users' reviews | text-only skills, no hooks |
| claude-code-setup | Anthropic, in `claude-plugins-official` | recommends hooks, skills, MCP servers and subagents for a codebase (read-only) | `claude plugin install claude-code-setup@claude-plugins-official` |
| agent-skills (pick only these) | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT) | `security-and-hardening`, `performance-optimization`, `accessibility-engineering`, `api-and-interface-design`, `ci-cd-and-automation`, `observability-and-instrumentation`, `documentation-and-adrs`, `deprecation-and-migration`, `doubt-driven-development`, `idea-refine`, `shipping-and-launch` | Copy single folders. Skip its `test-driven-development`, which has the same name as superpowers'. Skip the debugging, review, planning, simplification, frontend and router skills too, because God Mode and superpowers cover them. `doubt-driven-development` suggests sending code to other model CLIs; keep the review inside Claude if your code is private |
| Ponytail (optional) | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT) | "write the least code that works" mode, plus a cost board | Adds 3 hooks to every session (start, prompt, subagent) and reads your transcripts locally to compute cost. Its webhook is off unless you set one. It will offer to change your status line. Try it with `--scope local` in one project first |
