---
name: hook-writer
description: Writes the opening hook, the title + cover pairing and a 3-column script (spoken words | on screen | sound) for a reel, short, TikTok or promo, in any language, with every hook scored. Use when the user asks for a hook, an opening line, a reel/short script, a caption, or a title and cover for a product, app or brand video. It writes; it doesn't render (use motion-polish or your video tool for that).
argument-hint: "[product or idea, platform, length, language]"
license: MIT
---

# hook-writer

The first 3 seconds decide whether a short video is watched. This skill writes them, scores them, and writes the script underneath. It renders nothing and publishes nothing.

## Before you write
1. **Brand voice.** Read `<config>/god-mode/voice.md`, where `<config>` is `$CLAUDE_CONFIG_DIR` or `~/.claude`. If it doesn't exist, ask once for:
   - 2–3 posts or captions they liked, or wrote themselves;
   - words they never want used;
   - who the audience is.
   Write the file in the shape of [references/voice-template.md](references/voice-template.md). A script in the wrong voice is worse than none.
2. **Facts.** Get the product's real facts from the user or their docs. Never invent a number, a speed, a price or a feature. If a hook needs a number you don't have, ask, or write it without one.
3. **Ask once if it's missing:** platform and length (9:16 reel 15–30 s, or 16:9), language, and the **one** thing the viewer must remember.

## Hooks: write 5, keep 2
- Write 5 hooks, each against a different formula from [scripts/hooks.json](scripts/hooks.json): statistic, someone's result, before/after, the mistake, demo-first, the clock, and so on.
- Each hook does three jobs at once. It names the viewer's situation, opens a question, and proves the payoff exists.
- **Score them.** `hookscore.py` reads English only:
  - English hooks: `python scripts/hookscore.py --hook "<hook>"`, or one per line in a file: `python scripts/hookscore.py hooks.txt`.
  - Other languages: write a faithful English back-translation and score that. Then check the original by hand. Each failure is a fix, not a footnote:
    - The first 6 words name the viewer's situation.
    - There's a concrete thing in it: a number, a name, a time or a file type.
    - There's no slogan or metaphor.
    - It reads aloud in under 3 s.
    - It doesn't answer its own question.
- Show the top 2 with the score panel, your manual check, and one line on which formula each uses and why.
- The score is a filter, not a promise. A low score means "look again".

## Title + cover = one unit
- Title of 40 characters or fewer for mobile. The cover has **3 words max**, different words from the title but the same promise.
- Cover brief: the main subject, the 3 words, the background contrast, and where the logo sits.

## Script: 3 columns
| Time | Spoken / caption (exact words) | On screen (what moves) | Sound cue |
|---|---|---|---|
- 0–3 s is the hook. 3–8 s says what the video will show, then starts showing it. The body is one idea per beat, something new every 2–4 s. The payoff delivers the hook's promise. The end is one call to action.
- Every row has an on-screen action. A line with nothing to look at is a bad row.
- Sound cues accent events. Not every motion needs a sound.
- Give the runtime (about 150 spoken words a minute in English; measure other languages by reading aloud).

## Hand back
1. The 2 best hooks (score panel + manual check).
2. Title + cover brief.
3. The script table, with its runtime.
4. Caption + hashtags, in the brand voice.
5. Last line, always: **"Approve, or change something?"** Nothing gets rendered or published before the user approves the wording.

Next: `motion-polish` (same category) turns an approved script into a polished video.
