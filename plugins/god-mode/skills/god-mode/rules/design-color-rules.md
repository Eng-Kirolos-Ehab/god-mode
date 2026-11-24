# Design Color Rules



## 1. Harmonies (pick ONE per design)
- **Monochromatic**: one hue, vary lightness/saturation. Safest, elegant.
- **Analogous**: 3 neighbours on the wheel (e.g. blue→teal→green). Calm, natural.
- **Complementary**: opposites (blue/orange, purple/yellow, red/green). Max punch — use one as dominant, other only as accent.
- **Split-complementary**: base + the two neighbours of its opposite. Contrast with less clash — best default for UI.
- **Triadic**: 3 hues 120° apart. Lively; keep two muted.
- **Tetradic/square**: 4 hues — hard; one must dominate.

## 2. Proportion: 60-30-10
60% dominant (usually a neutral/background), 30% secondary, 10% accent (CTA, highlights). Accent = the most saturated colour and appears least.

## 3. Value beats hue
- Check the design in grayscale: if hierarchy disappears, fix lightness, not hue.
- Contrast: text ≥ 4.5:1, large text/icons/UI ≥ 3:1 (WCAG).

## 4. Building shades & tints
- Work in HSL or better **OKLCH** (perceptually even). Scale = same hue, step lightness (e.g. 50→950).
- **Hue-shift**: darker shades rotate toward cool (blue/purple) and slightly more saturated; lighter tints rotate toward warm (yellow) and less saturated. Avoids "dirty" shades from just adding black.
- Never darken by adding pure black or lighten by pure white only — results go grey/chalky.

## 5. Saturation & neutrals
- Big areas = low saturation; small areas may be saturated.
- Tint the neutrals with the brand hue (greys with 2-5% of the brand colour) — feels cohesive, not "white-coded".
- Dark mode: no pure #000 (use ~#0f1115 tinted), desaturate brand colours ~10-20%, raise lightness slightly.

## 6. Temperature
- Warm (red/orange/yellow) advances, cool (blue/green/purple) recedes → warm accents on cool backgrounds pop.
- Light warm ⇒ shadows cool (and vice versa) — key for realistic photo/composite work.

## 7. Mixing gotchas
- Gradient between complementaries in sRGB goes muddy grey in the middle → route through a middle hue or interpolate in OKLCH (`linear-gradient(in oklch, ...)`).
- Screen = RGB (additive, mixing → white); print = CMYK (subtractive, mixing → dark). Convert/soft-proof before print; neon RGB colours don't print.

## 8. Photoshop application
- Blend modes: **Multiply** darkens/shadows, **Screen** lightens/glow, **Overlay/Soft Light** contrast+tint, **Color** mode recolours while keeping luminance (best for recolouring objects), **Hue/Saturation** modes for partial changes.
- Unify a composite: one Gradient Map or Color Lookup layer on top at 10-30% opacity, or Solid Color layer in Soft Light.
- Classic grade: shadows teal / highlights orange (complementary) via Color Balance or Curves per channel.
- Match colours between images: Image > Adjustments > Match Color, or Curves sampling.

**How to apply:** before any design work, pick a harmony and a 60-30-10 split, build scales in OKLCH with hue-shift, then check contrast and the grayscale view.
