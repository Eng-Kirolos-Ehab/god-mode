#!/usr/bin/env python3
"""
Extract colors from a palette image.
Tries OCR for hex codes first, falls back to k-means clustering.
Outputs JSON list of hex colors sorted dark → light.
"""
import sys, json, re
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def luminance(hex_color: str) -> float:
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    # Perceptual luminance
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def rgb_to_hex(r, g, b) -> str:
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def extract_via_kmeans(img: Image.Image, n_colors: int = 8) -> list:
    img_rgb = img.convert('RGB')
    # Resize for speed
    img_small = img_rgb.resize((200, 200), Image.LANCZOS)
    pixels = np.array(img_small).reshape(-1, 3).astype(float)
    
    k = min(n_colors, len(pixels) // 10)
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    centers = kmeans.cluster_centers_
    hexes = [rgb_to_hex(*c) for c in centers]
    return hexes

def extract_hex_from_text(img: Image.Image) -> list:
    """Try to find hex codes in image using basic OCR."""
    try:
        import pytesseract
        text = pytesseract.image_to_string(img)
        pattern = r'#?[0-9A-Fa-f]{6}'
        found = re.findall(pattern, text)
        hexes = []
        for h in found:
            if not h.startswith('#'):
                h = '#' + h
            hexes.append(h.lower())
        return list(set(hexes))
    except Exception:
        return []

def extract_palette(image_path: str, n_colors: int = 8) -> list:
    img = Image.open(image_path)
    
    # Try OCR first
    hex_colors = extract_hex_from_text(img)
    
    # If OCR found fewer than 2, use k-means
    if len(hex_colors) < 2:
        hex_colors = extract_via_kmeans(img, n_colors)
    
    # Sort by luminance dark → light
    hex_colors = sorted(set(hex_colors), key=luminance)
    return hex_colors

if __name__ == "__main__":
    image_path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    colors = extract_palette(image_path, n)
    print(json.dumps(colors, indent=2))
