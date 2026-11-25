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
