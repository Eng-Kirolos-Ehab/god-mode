#!/usr/bin/env python3
"""
Extract dominant colors from source design image.
Returns JSON list of hex colors sorted dark → light.
"""
import sys, json
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def luminance(hex_color: str) -> float:
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def rgb_to_hex(r, g, b) -> str:
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def extract_dominant(image_path: str, n_colors: int = 8) -> list:
    img = Image.open(image_path).convert('RGB')
    
    # Resize for speed, keep aspect ratio
    img.thumbnail((400, 400), Image.LANCZOS)
    pixels = np.array(img).reshape(-1, 3).astype(float)
    
    # Remove near-white and near-black for better results (but keep them in output)
    k = min(n_colors, max(2, len(pixels) // 100))
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    # Weight by cluster size
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    counts = np.bincount(labels)
    
    # Sort by count descending to get dominant colors
    sorted_indices = np.argsort(-counts)
    top_colors = [rgb_to_hex(*centers[i]) for i in sorted_indices[:n_colors]]
    
    # Re-sort by luminance dark → light
    top_colors = sorted(top_colors, key=luminance)
    return top_colors

if __name__ == "__main__":
    image_path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    colors = extract_dominant(image_path, n)
    print(json.dumps(colors, indent=2))
