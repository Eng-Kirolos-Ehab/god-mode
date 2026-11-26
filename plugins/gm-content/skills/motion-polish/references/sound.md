# Sound pass

Most code-made videos are silent or sound random. Sound is what makes them feel produced.

## Tools (optional, ask before installing)
- **earshot** (MIT, CPU only, no audio model): https://github.com/Leonxlnx/earshot. It makes interface sounds, foley and whooshes from words, and measures loudness. Install it into its own virtual environment (`python -m venv …` then `pip install earshot`), plus `librosa` for `earshot measure`. Its `listen` extra (torch, about 1 GB) and its Gemini critique are optional. The Gemini critique uploads audio, so use it only with the user's OK.
- **Openverse** (free, no key, Creative Commons sounds) when a real recording is needed: `https://api.openverse.org/v1/audio/?q=<words>&license_type=commercial`. Keep the licence and the creator in `sfx/CREDITS.md`, and credit CC-BY sounds in the caption.
- No tool installed? ffmpeg alone can mix and master. Say which sounds are missing.

## Cue sheet first
`sfx/cues.json`: `[{ "t": 1.20, "sound": "whoosh", "gain": 0.3, "pan": -0.2, "why": "title slides in" }]`. Every `t` comes from the timeline (scene start + offset), never a guessed number.

## Visual event → sound
| On screen | Sound | Level |
|---|---|---|
| Hero transition / reveal | whoosh in + ONE impact on the hit (one per video) | 0.25–0.35 |
| Word/line reveal | short airy whoosh, small blip on landing | 0.08–0.15 |
| Badge/icon pops | pop, pitch rising across a sequence | 0.1–0.2 |
| Typing | one key click per character, jitter ±5 ms | 0.08 |
| Success / result | chime in the music's key | 0.2 |
| Build-up | ONE riser per video, ending exactly on the hit | 0.2 |
| Under everything | pad/ambience, ducked ~65 % under the hero hit | 0.03 |
Accent, don't narrate: drift, grain and slow rotation stay silent.

## Make, check, mix, mux
- With earshot:
  - `earshot make "soft glass tap" -o sfx/tap.wav` makes one sound.
  - `earshot make --set ui -o sfx/ui` makes a matching family (ui, game, arcade or film).
  - `earshot sfx render <id>/<variant> -o …` renders one sound from its bank.
- Place cues with ffmpeg: `adelay` per cue, then `amix=normalize=0`.
- Check: `ffmpeg -i sfx/mix.wav -af silencedetect=n=-40dB:d=0.05 -f null -`. Each hit should start where the cue sheet says. If earshot is installed, `earshot measure sfx/mix.wav` gives loudness and peaks.
- Master to −14 LUFS integrated with true peak ≤ −1 dBTP: `-af loudnorm=I=-14:TP=-1.5:LRA=11`. A mix of only sparse sound effects lands around −16 LUFS; that's fine, don't crush it.
- Mux: `ffmpeg -i video.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -shortest out/final.mp4`.
- Only use music whose licence allows the user's use. Never download from sites that need a sign-in.
