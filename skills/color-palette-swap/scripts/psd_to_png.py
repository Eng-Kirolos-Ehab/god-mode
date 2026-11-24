#!/usr/bin/env python3
"""Convert PSD file to PNG."""
import sys
from pathlib import Path

def convert_psd(input_path: str) -> str:
    output_path = str(Path(input_path).with_suffix('.png'))
    try:
        from psd_tools import PSDImage
        psd = PSDImage.open(input_path)
        psd.composite().save(output_path)
        print(f"Converted PSD to: {output_path}")
        return output_path
    except Exception as e:
        print(f"psd-tools failed: {e}, trying ImageMagick...")
        import subprocess
        result = subprocess.run(['convert', input_path, output_path], capture_output=True)
        if result.returncode == 0:
            print(f"ImageMagick converted to: {output_path}")
            return output_path
        raise RuntimeError(f"Could not convert PSD: {result.stderr}")

if __name__ == "__main__":
    path = convert_psd(sys.argv[1])
    print(path)
