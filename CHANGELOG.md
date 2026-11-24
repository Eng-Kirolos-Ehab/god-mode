# Changelog

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
