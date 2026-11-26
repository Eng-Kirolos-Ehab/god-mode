---
name: motion-polish
description: Turns an approved script into a polished code-made motion video (9:16 or 16:9) on top of the video tool you already use (HyperFrames, Remotion or plain HTML + ffmpeg) - picks a style preset, applies spring easing, targeted motion blur and cuts on the beat, handles right-to-left text (Arabic, Hebrew, Persian), places sound effects on the frame, and reviews its own frame sheets before delivery. Use when the user wants a reel, short, promo or app demo animated in code, or says a video looks "generic", "AI", "cheap" or "boring". Not for editing camera footage.
argument-hint: "[approved script or idea, format, length]"
license: MIT
---

# motion-polish

A polish layer. Your renderer builds the frames; this skill decides how they look, move and sound, then checks the result before the user sees it.

## Inputs (stop and ask if missing)
- An **approved** script (for example from `hook-writer`): time | words | on screen | sound. No approved wording means no render.
- Format (default 9:16 1080×1920), length, the brand color, the logo, and real product screenshots. Never invent UI or numbers. Anything illustrative is labelled "Example".
- The renderer: use the one installed (HyperFrames, Remotion, or HTML with frame capture + ffmpeg). If none is installed, say which one is missing and stop.

## Flow (always in this order)
1. **Pick a style** from [references/styles.md](references/styles.md). Use one per video, or one per section of a montage, and say why in one line.
2. **Beat map.** Choose the music (or none) and get its BPM. Every scene change lands on a beat, and the key moment (reveal, before→after) lands on the drop. Nothing stays still for more than 1 s.
3. **4 stills first.** Render the 4 key frames, look at them, and fix them. Only then render the full video.
4. **Draft render** at 30 fps and half resolution to judge the rhythm, then the **master**.
5. **Sound pass**: [references/sound.md](references/sound.md).
6. **Self-review**, then deliver.

## Motion rules (what stops it looking "AI")
- **One accent color.** One visual system from start to end: shapes transform instead of hard-cutting between unrelated looks.
- **One thing moves at a time**, unless a single control drives everything.
- **Easing:** springs with damping ≥ 0.72, or `cubic-bezier(.6,0,.2,1)` for moves and `cubic-bezier(.2,.8,.2,1)` for entrances. Never linear, never bounce.
- **Camera:** one transform on a container. Interpolate zoom in log space. Never zoom in and out back to back. A small punch per beat (+1.2%) is OK after the drop.
- **Targeted motion blur** on the 1–3 slam moves only. Never blur text meant to be read, and never blur across a hard cut. Crossfade a text's fill rather than scaling a blurry copy.
- **Cut on the beat, at peak speed.** Direction and speed match on both sides of the cut.

## Right-to-left and non-Latin text
- Set `dir="rtl"` on RTL blocks and load a font that covers the script. Check one frame for empty boxes (missing glyphs).
- **Never animate joined scripts (Arabic, Persian, Urdu…) letter by letter**: it breaks the letter joining. Reveal by word or by line, with a mask or opacity.
- Wrap mixed Latin text and numbers in `<bdi>` so they don't jump sides.
- On-screen text matches the spoken words in the same beat. Captions stay inside the 9:16 safe area (not the top ~220 px or the bottom ~380 px).

## Self-review (the judge is not the builder)
```bash
ffmpeg -i out/final.mp4 -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 out/contact.png
ffmpeg -i out/final.mp4 -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 out/phone.png
ffmpeg -i out/final.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12
```
- Open both sheets and score 1–10 on: hook in the first 2 s · readable at 360 px · motion quality (no dead frames) · something new every 2–4 s · text correct (joined, right direction, no missing glyphs) · brand and facts accurate · sound in sync.
- Fix every shot that scores 7 or below, then re-check only that shot. For a big film, run the critique as a separate subagent that didn't build it.

## Deliver
The MP4 path, the contact sheet, the scores, and what you'd still improve. Never publish on the user's behalf.
