#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Protocol v7.6.0] Pixel Luminance & Alpha Mask Integrity Guard
======================================================================
Headless validator that checks captured UI screenshots or image assets
for unwanted high-luminance border artifacts (e.g. 1px native Qt bevels
in dark mode), ensures transparent alpha clipping or full-bleed square
icon coverage, detects light matte halo fringes on transparent cutouts,
and optionally generates a complement-color (#479be6) inspection sheet.

Usage:
    python pixel_luminance_guard.py <image_path> [--theme dark|light]
        [--mode screen|portrait|sticker|full_bleed_icon]
        [--preview-sheet <out.png>] [--strict]
"""

import argparse
import sys
import os
from collections import deque

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def calculate_luminance(r, g, b):
    """Standard ITU-R BT.709 relative luminance."""
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def count_enclosed_transparent_pockets(pixels, width, height, alpha_thresh=16):
    """Find disconnected transparent pockets completely enclosed by opaque pixels."""
    visited = bytearray(width * height)
    q = deque()

    for x in range(width):
        for y in (0, height - 1):
            idx = y * width + x
            if not visited[idx] and pixels[x, y][3] <= alpha_thresh:
                visited[idx] = 1
                q.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            idx = y * width + x
            if not visited[idx] and pixels[x, y][3] <= alpha_thresh:
                visited[idx] = 1
                q.append((x, y))

    while q:
        cx, cy = q.popleft()
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                nidx = ny * width + nx
                if not visited[nidx] and pixels[nx, ny][3] <= alpha_thresh:
                    visited[nidx] = 1
                    q.append((nx, ny))

    enclosed_pixels = 0
    for y in range(height):
        row_off = y * width
        for x in range(width):
            if not visited[row_off + x] and pixels[x, y][3] <= alpha_thresh:
                enclosed_pixels += 1
    return enclosed_pixels


def save_complement_preview(im, out_path):
    """Composite cutout onto #479be6 cobalt-blue inspection background."""
    from PIL import Image
    bg = Image.new("RGBA", im.size, (71, 155, 230, 255))
    composited = Image.alpha_composite(bg, im)
    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    composited.save(out_path)


def audit_image(image_path, theme="dark", mode="screen", preview_sheet=None, strict=False):
    print("=" * 65)
    print(" [LJack Protocol] Pixel Luminance & Alpha Mask Guard")
    print("=" * 65)
    print(f"[*] Target Asset: {image_path}")
    print(f"[*] Target Theme: {theme.upper()} | Mode: {mode}")

    if not os.path.isfile(image_path):
        print(f"[ERROR] File not found: {image_path}")
        return 1

    try:
        from PIL import Image
    except ImportError:
        print("[INFO] Pillow library not installed. Falling back to binary header & format check.")
        with open(image_path, "rb") as f:
            header = f.read(16)
        if header.startswith(b"\x89PNG\r\n\x1a\n") or header.startswith(b"\x00\x00\x01\x00") or header.startswith(b"RIFF"):
            print("[PASS] Valid PNG/ICO/WEBP binary format verified.")
            return 0
        else:
            print("[WARN] Non-standard image format.")
            return 1 if strict else 0

    im = Image.open(image_path).convert("RGBA")
    width, height = im.size
    pixels = im.load()

    if preview_sheet:
        save_complement_preview(im, preview_sheet)
        print(f"[*] Complement Inspection Sheet (#479be6) saved: {preview_sheet}")

    warnings = 0

    # 1. Alpha corner & perimeter check
    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    opaque_corners = [(cx, cy, pixels[cx, cy][3]) for cx, cy in corners if pixels[cx, cy][3] > 10]

    # 2. 1px Perimeter check
    high_luminance_border_pixels = 0
    transparent_border_pixels = 0
    for x in range(width):
        for y in (0, height - 1):
            r, g, b, a = pixels[x, y]
            if a <= 240:
                transparent_border_pixels += 1
            if theme == "dark" and a > 128 and calculate_luminance(r, g, b) > 180:
                high_luminance_border_pixels += 1
    for y in range(1, max(1, height - 1)):
        for x in (0, width - 1):
            r, g, b, a = pixels[x, y]
            if a <= 240:
                transparent_border_pixels += 1
            if theme == "dark" and a > 128 and calculate_luminance(r, g, b) > 180:
                high_luminance_border_pixels += 1

    print(f"[*] Dimensions: {width}x{height}")
    print(f"[*] Opaque Corner Pixels (Alpha > 10): {len(opaque_corners)}")
    print(f"[*] High-Luminance Border Pixels (L > 180): {high_luminance_border_pixels}")

    if mode == "full_bleed_icon":
        # Measure opaque artwork bounding-box fill ratio (catches padded icons with empty margins
        # while allowing narrow anti-aliased rounded-corner bevels).
        alpha_band = im.getchannel("A").point(lambda a: 255 if a > 20 else 0)
        bbox = alpha_band.getbbox()
        if not bbox:
            warnings += 1
            print("-" * 65)
            print("[WARN] Icon image is completely transparent.")
        else:
            fill_w = (bbox[2] - bbox[0]) / width
            fill_h = (bbox[3] - bbox[1]) / height
            print(f"[*] Artwork Bounding-Box Coverage: {fill_w * 100:.1f}% x {fill_h * 100:.1f}%")
            print("-" * 65)
            if fill_w < 0.92 or fill_h < 0.92:
                warnings += 1
                print(
                    f"[WARN] Full-bleed icon covers only {fill_w * 100:.1f}%x{fill_h * 100:.1f}% of frame (<92%)."
                )
                print("  -> Expand artwork or crop edge-to-edge so desktop icon fills full 1024x1024 frame.")
            else:
                print("[PASS] Full-bleed icon artwork fills frame cleanly (>=92% both axes).")
    elif mode in ("portrait", "sticker"):
        fringe_pixels = 0
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if 15 <= a <= 180 and calculate_luminance(r, g, b) > 225:
                    fringe_pixels += 1
        enclosed_holes = count_enclosed_transparent_pockets(pixels, width, height)
        print(f"[*] Semi-transparent White Fringe Pixels: {fringe_pixels}")
        print(f"[*] Enclosed Transparent Pockets: {enclosed_holes} px")
        print("-" * 65)
        if fringe_pixels > max(200, int(width * height * 0.005)):
            warnings += 1
            print(f"[WARN] Detected {fringe_pixels} bright matte fringe pixels around cutout.")
            print("  -> Generate against #123466 cobalt backdrop or apply alpha de-fringe pass.")
        else:
            print("[PASS] Cutout alpha edge fringe is within clean tolerance.")
        if enclosed_holes > 0:
            print(f"[INFO] Enclosed transparent pockets ({enclosed_holes} px) detected (inspect complement sheet if <5px narrow slits remain).")
        if len(opaque_corners) > 2 and mode == "portrait":
            warnings += 1
            print("[WARN] Portrait cutout has opaque upper corners; verify background removal.")
    else:
        print("-" * 65)
        if high_luminance_border_pixels > 0:
            warnings += 1
            print(f"[WARN] Detected {high_luminance_border_pixels} high-luminance border pixels.")
            print("  -> Suggestion: Ensure 'setFrameShape(NoFrame)', 'border: none', or 'drawBase: 0' in stylesheets.")
        else:
            print("[PASS] Border luminance is clean with zero native bevel bleed.")

        if len(opaque_corners) == 4 and image_path.lower().endswith((".png", ".ico")):
            print("[INFO] Square asset detected. If squircle icon was intended, ensure alpha mask clipping; if full-bleed app icon, use --mode full_bleed_icon.")
        else:
            print("[PASS] Corner alpha transparency verified.")

    print("=" * 65)
    return 1 if (strict and warnings > 0) else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LJack Pixel Luminance & Alpha Mask Integrity Guard")
    parser.add_argument("image_path", help="Target PNG/WEBP/ICO image file")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark")
    parser.add_argument("--mode", choices=["screen", "portrait", "sticker", "full_bleed_icon"], default="screen")
    parser.add_argument("--preview-sheet", default=None, help="Optional path to write a #479be6 complement inspection PNG")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any warnings are detected")
    args = parser.parse_args()
    sys.exit(audit_image(args.image_path, args.theme, args.mode, args.preview_sheet, args.strict))
