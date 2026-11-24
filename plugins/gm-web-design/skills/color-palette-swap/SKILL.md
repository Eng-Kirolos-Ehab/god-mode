---
name: color-palette-swap
description: |
  Use this skill whenever the user uploads a design file (PSD, PNG, or JPG) along with a color palette image and wants to recolor the design using the new palette. Triggers on phrases like: "غير الالوان", "بديل الالوان", "color palette swap", "recolor my design", "change colors using this palette", "استخدم البالت ده", "طبق الالوان دي", "color mapping", "هديك صورة و color palette". 
  
  This skill extracts dominant colors from the source design, extracts hex colors from the palette image, maps them intelligently (dark-to-dark and light-to-light), and produces TWO output PNGs:
  - Result 1: Dark→Dark, Light→Light mapping
  - Result 2: Aesthetically optimized alternative mapping
  
  Always use this skill when both a design image AND a palette image are provided together.
---

# Color Palette Swap Skill

## Overview
Take a source design (PSD/PNG/JPG) + a color palette image → produce 2 recolored PNG outputs using intelligent color mapping.

## Workflow

### Step 1: Read the input files
- Source design: PSD, PNG, or JPG (uploaded by user)
- Palette image: PNG/JPG containing color swatches and/or hex codes

If input is PSD, convert to PNG first:
```bash
pip install psd-tools pillow scikit-learn numpy --break-system-packages -q
python scripts/psd_to_png.py <input.psd>
```

### Step 2: Extract colors from palette image
Run the palette extractor — it reads the image, detects distinct color swatches, and extracts hex values (OCR on hex codes if present, otherwise k-means clustering):
```bash
python scripts/extract_palette.py <palette_image>
```
Output: JSON list of hex colors sorted by luminance (dark → light)

### Step 3: Extract dominant colors from source design
```bash
python scripts/extract_source_colors.py <source_image>
```
Output: JSON mapping of dominant hex colors sorted by luminance (dark → light)

### Step 4: Generate Result 1 — Dark-to-Dark / Light-to-Light
Map source colors to palette colors by luminance rank order:
- Darkest source color → Darkest palette color
- Lightest source color → Lightest palette color
- Middle tones → Middle palette colors (interpolated)

```bash
python scripts/apply_palette.py <source_image> --mapping result1_mapping.json --output result1.png
```

### Step 5: Generate Result 2 — Aesthetic Alternative
Use a smarter approach:
- Analyze the source design's color roles (background, accent, detail, shadow)
- Map palette colors to maximize contrast and visual harmony
- Prioritize the most saturated palette color for accent/highlight elements
- Use the most neutral palette color for backgrounds

```bash
python scripts/apply_palette.py <source_image> --mapping result2_mapping.json --output result2.png
```

### Step 6: Present both results
Copy outputs to /mnt/user-data/outputs/ and present both PNG files to the user with a brief explanation of the mapping logic used in each.

---

## Implementation Details

### Color Mapping Algorithm
1. Convert all colors to HSL
2. Sort source colors by Lightness (L channel)
3. Sort palette colors by Lightness (L channel)
4. For Result 1: zip them in order
5. For Result 2: also consider Saturation and Hue to find the best perceptual match

### Pixel-Level Recoloring
Use LAB color space for perceptually accurate replacement:
- For each pixel, find the nearest source dominant color (by euclidean distance in LAB)
- Replace with the mapped palette color
- Preserve original lightness variation within each color zone (multiply blend)

### Preserving Design Detail
- Do NOT flatten colors — preserve the shading/gradient within each color region
- Apply color as a "hue shift" relative to the original, not a flat fill
- Use soft masking with blur radius=2px at color boundaries

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/psd_to_png.py` | Convert PSD to PNG using psd-tools |
| `scripts/extract_palette.py` | Extract + sort colors from palette image |
| `scripts/extract_source_colors.py` | Extract dominant colors from design |
| `scripts/apply_palette.py` | Apply color mapping to produce output PNG |

---

## Error Handling
- If PSD conversion fails: try ImageMagick (`convert input.psd output.png`)
- If palette has < 2 colors detected: ask user to provide a clearer palette image
- If source image has very few distinct colors: lower the k-means cluster count

## Output
Always produce exactly **2 PNG files**:
- `result1_dark_to_dark.png` — luminance-matched mapping
- `result2_aesthetic.png` — aesthetically optimized mapping

Present both with `present_files` tool.
