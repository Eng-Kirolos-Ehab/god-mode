#!/usr/bin/env python3
"""
Apply a color palette mapping to a source image.
Preserves shading/detail within each color zone.

Usage:
  python apply_palette.py <source> <palette_image> --mode [dark_to_dark|aesthetic] --output <out.png>
"""
import sys, json, argparse
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


# ── helpers ──────────────────────────────────────────────────────────────────

def hex_to_rgb(h: str):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b) -> str:
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def luminance(rgb) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def saturation(rgb) -> float:
    r, g, b = [x / 255.0 for x in rgb]
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == 0:
        return 0
    return (mx - mn) / mx

def rgb_to_lab(rgb):
    """Convert RGB (0-255) → CIE Lab."""
    r, g, b = [x / 255.0 for x in rgb]
    def linearize(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = linearize(r), linearize(g), linearize(b)
    # D65
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    x, y, z = x / 0.95047, y / 1.0, z / 1.08883
    def f(t):
        return t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116
    L = 116 * f(y) - 16
    a = 500 * (f(x) - f(y))
    b_ = 200 * (f(y) - f(z))
    return np.array([L, a, b_])


# ── color extraction ──────────────────────────────────────────────────────────

def extract_colors(image: Image.Image, n: int = 8):
    img = image.convert('RGB')
    img.thumbnail((400, 400), Image.LANCZOS)
    px = np.array(img).reshape(-1, 3).astype(float)
    k = min(n, max(2, len(px) // 100))
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(px)
    labels = km.labels_
    centers = km.cluster_centers_
    counts = np.bincount(labels)
    # sort by dominance
    idx = np.argsort(-counts)
    colors = [tuple(centers[i].astype(int)) for i in idx[:n]]
    return colors

def extract_palette_colors(palette_img: Image.Image, n: int = 8):
    """Extract colors from palette image — tries to find distinct swatches."""
    img = palette_img.convert('RGB')
    px = np.array(img).reshape(-1, 3).astype(float)
    k = min(n, max(2, len(px) // 50))
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(px)
    return [tuple(c.astype(int)) for c in km.cluster_centers_]


# ── mapping strategies ────────────────────────────────────────────────────────

def map_dark_to_dark(source_colors, palette_colors):
    """Sort both by luminance, zip them."""
    src_sorted = sorted(source_colors, key=luminance)
    pal_sorted = sorted(palette_colors, key=luminance)
    # Stretch/compress palette to match source count
    n = len(src_sorted)
    m = len(pal_sorted)
    mapping = {}
    for i, src in enumerate(src_sorted):
        j = round(i * (m - 1) / max(n - 1, 1))
        mapping[src] = pal_sorted[j]
    return mapping

def map_aesthetic(source_colors, palette_colors):
    """
    Aesthetic mapping:
    - Most saturated source → most saturated palette (accent)
    - Darkest source → darkest palette (shadow/outline)
    - Lightest source → lightest palette (highlight/background)
    - Rest: luminance-proportional
    """
    src_by_lum = sorted(source_colors, key=luminance)
    pal_by_lum = sorted(palette_colors, key=luminance)
    
    src_by_sat = sorted(source_colors, key=saturation, reverse=True)
    pal_by_sat = sorted(palette_colors, key=saturation, reverse=True)
    
    mapping = {}
    used_pal = set()
    
    # 1. Most saturated → most saturated
    if src_by_sat and pal_by_sat:
        mapping[src_by_sat[0]] = pal_by_sat[0]
        used_pal.add(id(pal_by_sat[0]))
    
    # 2. Darkest → darkest
    if src_by_lum:
        remaining_pal = [p for p in pal_by_lum if id(p) not in used_pal]
        if remaining_pal:
            mapping[src_by_lum[0]] = remaining_pal[0]
            used_pal.add(id(remaining_pal[0]))
    
    # 3. Lightest → lightest
    if len(src_by_lum) > 1:
        remaining_pal = [p for p in reversed(pal_by_lum) if id(p) not in used_pal]
        if remaining_pal:
            mapping[src_by_lum[-1]] = remaining_pal[0]
            used_pal.add(id(remaining_pal[0]))
    
    # 4. Rest: luminance rank among remaining
    remaining_src = [s for s in src_by_lum if s not in mapping]
    remaining_pal = [p for p in pal_by_lum if id(p) not in used_pal]
    for i, src in enumerate(remaining_src):
        if not remaining_pal:
            # fallback: reuse closest lum
            closest = min(palette_colors, key=lambda p: abs(luminance(p) - luminance(src)))
            mapping[src] = closest
        else:
            j = round(i * (len(remaining_pal) - 1) / max(len(remaining_src) - 1, 1))
            mapping[src] = remaining_pal[j]
    
    return mapping


# ── pixel recoloring ──────────────────────────────────────────────────────────

def recolor_image(source: Image.Image, mapping: dict) -> Image.Image:
    """
    For each pixel, find nearest source dominant color in LAB space,
    replace with mapped palette color, preserving local lightness variation.
    """
    img = source.convert('RGB')
    arr = np.array(img, dtype=np.float32)
    H, W, _ = arr.shape
    
    src_colors = list(mapping.keys())
    tgt_colors = [mapping[k] for k in src_colors]
    
    # Pre-compute LAB for source cluster centers
    src_lab = np.array([rgb_to_lab(c) for c in src_colors])  # (K, 3)
    
    # Flatten image
    pixels = arr.reshape(-1, 3)  # (N, 3)
    
    # Compute LAB for every pixel
    # Vectorized approximate conversion for speed
    px_norm = pixels / 255.0
    
    # Batch nearest-neighbor in RGB space (fast approximation, good enough)
    src_arr = np.array(src_colors, dtype=np.float32)  # (K, 3)
    # (N, K) distances
    diffs = pixels[:, None, :] - src_arr[None, :, :]  # (N, K, 3)
    dists = np.sum(diffs ** 2, axis=2)                # (N, K)
    nearest = np.argmin(dists, axis=1)                # (N,)
    
    # For each pixel: compute its lightness relative to cluster center,
    # apply that same relative lightness to the target color
    result = np.zeros_like(pixels)
    
    tgt_arr = np.array(tgt_colors, dtype=np.float32)  # (K, 3)
    
    for k in range(len(src_colors)):
        mask = (nearest == k)
        if not mask.any():
            continue
        
        src_lum = max(luminance(src_colors[k]), 1e-6)
        tgt_lum = max(luminance(tgt_colors[k]), 1e-6)
        
        src_px = pixels[mask]           # pixels in this cluster
        px_lum = (0.2126 * src_px[:, 0] +
                  0.7152 * src_px[:, 1] +
                  0.0722 * src_px[:, 2])  # per-pixel luminance
        
        # Ratio of pixel lum to cluster center lum → preserve local variation
        ratio = (px_lum / src_lum)[:, None]  # (M, 1)
        ratio = np.clip(ratio, 0.1, 3.0)
        
        # Apply ratio to target color
        recolored = tgt_arr[k][None, :] * ratio
        result[mask] = np.clip(recolored, 0, 255)
    
    out_arr = result.reshape(H, W, 3).astype(np.uint8)
    
    # Preserve alpha channel if present
    if source.mode == 'RGBA':
        alpha = np.array(source.split()[3])
        out = Image.fromarray(out_arr, 'RGB').convert('RGBA')
        out.putalpha(Image.fromarray(alpha))
        return out
    
    return Image.fromarray(out_arr, 'RGB')


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Source design image')
    parser.add_argument('palette', help='Color palette image')
    parser.add_argument('--mode', choices=['dark_to_dark', 'aesthetic'], default='dark_to_dark')
    parser.add_argument('--output', default='result.png')
    parser.add_argument('--n-source', type=int, default=8)
    parser.add_argument('--n-palette', type=int, default=8)
    args = parser.parse_args()
    
    print(f"Loading source: {args.source}")
    source_img = Image.open(args.source)
    
    print(f"Loading palette: {args.palette}")
    palette_img = Image.open(args.palette)
    
    print(f"Extracting {args.n_source} dominant colors from source...")
    source_colors = extract_colors(source_img, args.n_source)
    print(f"  Source colors: {[rgb_to_hex(*c) for c in source_colors]}")
    
    print(f"Extracting {args.n_palette} colors from palette...")
    palette_colors = extract_palette_colors(palette_img, args.n_palette)
    print(f"  Palette colors: {[rgb_to_hex(*c) for c in palette_colors]}")
    
    print(f"Computing {args.mode} mapping...")
    if args.mode == 'dark_to_dark':
        mapping = map_dark_to_dark(source_colors, palette_colors)
    else:
        mapping = map_aesthetic(source_colors, palette_colors)
    
    print("Mapping:")
    for src, tgt in mapping.items():
        print(f"  {rgb_to_hex(*src)} → {rgb_to_hex(*tgt)}")
    
    print("Recoloring image...")
    result = recolor_image(source_img, mapping)
    
    result.save(args.output, 'PNG')
    print(f"Saved: {args.output}")


if __name__ == '__main__':
    main()
