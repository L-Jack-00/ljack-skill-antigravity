#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack GameCode Protocol v1.1.0] Static Layer Isolation & Manifest Guard
========================================================================
Zero-dependency static verifier for LJack GameCode projects:
  1. Layer Isolation Guard: Ensures pure logic directory (default `src/logic/`)
     contains zero browser, DOM, Canvas, or WebAudio API calls so headless
     simulation remains 100% pure (supports TS, TSX, ESM .js + JSDoc).
  2. Asset Manifest Audit: Validates `specs/asset_manifest.json` structure,
     required `aiPromptHint` + `path`, and optional multi-reference/cutout
     metadata (`cutoutMode`, `backdropColor`, `forbiddenMotifs`, `styleRef`,
     `characterRef`, `rawCachePath`).
  3. Hardcoded Asset Path Guard: Flags direct `new Audio(...)` or raw
     `"assets/..."` references inside view directory (`src/view/`) that
     bypass `AssetHarness`.

Usage:
    python layer_guard.py <project_directory> [--logic-dir DIR] [--view-dir DIR] [--manifest PATH] [--strict]
"""

import os
import sys
import re
import json
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

FORBIDDEN_LOGIC_PATTERNS = [
    (re.compile(r'\bwindow\b'), "Browser `window` object accessed inside src/logic/"),
    (re.compile(r'\bdocument\b'), "DOM `document` object accessed inside src/logic/"),
    (re.compile(r'\bCanvasRenderingContext2D\b|\bgetContext\s*\('), "Canvas 2D rendering API accessed inside src/logic/"),
    (re.compile(r'\bAudioContext\b|\bwebkitAudioContext\b|\bnew\s+Audio\b'), "WebAudio/Audio API accessed inside src/logic/"),
    (re.compile(r'\bHTMLImageElement\b|\bnew\s+Image\b'), "DOM Image API accessed inside src/logic/"),
    (re.compile(r'\brequestAnimationFrame\b'), "Browser animation frame API accessed inside src/logic/"),
    (re.compile(r'\blocalStorage\b|\bsessionStorage\b'), "Browser storage API accessed inside src/logic/"),
]

VIEW_HARDCODE_PATTERNS = [
    (re.compile(r'\bnew\s+Audio\s*\('), "Direct `new Audio()` call bypassing AssetHarness.playAudio()"),
    (re.compile(r'["\']assets/[^"\']+["\']'), "Raw asset file path literal in src/view/; use AssetID key with AssetHarness"),
]

SCANNABLE_EXTS = {'.ts', '.tsx', '.js', '.jsx', '.mjs'}
SIZE_CHECK_EXTS = {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.css'}
IGNORED_DIRS = {'.git', 'node_modules', 'dist', 'dist-web', 'target', '__pycache__', '.deno'}


def scan_oversized_files(base_dir: str, max_lines: int = 1200, max_bytes: int = 102400) -> list:
    advisories = []
    if not os.path.isdir(base_dir):
        return advisories
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for fname in files:
            if os.path.splitext(fname)[1].lower() not in SIZE_CHECK_EXTS:
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, base_dir)
            try:
                size_bytes = os.path.getsize(fpath)
                with open(fpath, "r", encoding="utf-8-sig", errors="ignore") as fp:
                    line_count = sum(1 for _ in fp)
                if line_count > max_lines or size_bytes > max_bytes:
                    advisories.append(
                        f"{rel} ({line_count} lines, {size_bytes // 1024} KB) exceeds modularity budget ({max_lines} lines / {max_bytes // 1024} KB)."
                    )
            except Exception:
                pass
    return advisories


def scan_files(base_dir: str, patterns: list) -> list:
    findings = []
    if not os.path.isdir(base_dir):
        return findings

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for fname in files:
            if os.path.splitext(fname)[1].lower() not in SCANNABLE_EXTS:
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, base_dir)
            try:
                with open(fpath, "r", encoding="utf-8-sig", errors="ignore") as fp:
                    in_block_comment = False
                    for line_no, line in enumerate(fp, start=1):
                        stripped = line.strip()
                        if stripped.startswith("/*"):
                            in_block_comment = True
                        if in_block_comment:
                            if "*/" in stripped:
                                in_block_comment = False
                            continue
                        if stripped.startswith("//"):
                            continue
                        # Strip inline // comments before checking
                        code_only = line.split("//", 1)[0]
                        for rx, msg in patterns:
                            if rx.search(code_only):
                                findings.append(f"{rel}:{line_no} -> {msg}")
            except Exception:
                pass
    return findings


VALID_CUTOUT_MODES = {"portrait", "sticker", "full_bleed_icon", "none"}


def validate_manifest(manifest_path: str) -> list:
    errors = []
    if not os.path.isfile(manifest_path):
        return [f"Missing asset manifest: {manifest_path}"]
    try:
        with open(manifest_path, "r", encoding="utf-8-sig") as fp:
            data = json.load(fp)
    except Exception as exc:
        return [f"Invalid JSON in specs/asset_manifest.json: {exc}"]

    assets = data.get("assets")
    if not isinstance(assets, dict):
        return ["specs/asset_manifest.json must contain an `assets` object map."]

    for asset_id, entry in assets.items():
        if not isinstance(entry, dict):
            errors.append(f"Asset '{asset_id}' must be an object.")
            continue
        if not entry.get("aiPromptHint"):
            errors.append(f"Asset '{asset_id}' is missing required `aiPromptHint`.")
        if not entry.get("path"):
            errors.append(f"Asset '{asset_id}' is missing `path`.")

        cutout_mode = entry.get("cutoutMode")
        if cutout_mode is not None and cutout_mode not in VALID_CUTOUT_MODES:
            errors.append(
                f"Asset '{asset_id}' has invalid `cutoutMode` '{cutout_mode}' (allowed: {sorted(VALID_CUTOUT_MODES)})."
            )

        forbidden_motifs = entry.get("forbiddenMotifs")
        if forbidden_motifs is not None and (
            not isinstance(forbidden_motifs, list) or not all(isinstance(x, str) for x in forbidden_motifs)
        ):
            errors.append(f"Asset '{asset_id}' field `forbiddenMotifs` must be a list of strings.")

        backdrop_color = entry.get("backdropColor")
        if backdrop_color is not None and not (
            isinstance(backdrop_color, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", backdrop_color)
        ):
            errors.append(f"Asset '{asset_id}' field `backdropColor` must be #RRGGBB hex (got {backdrop_color!r}).")

        for ref_key in ("styleRef", "characterRef", "rawCachePath"):
            ref_val = entry.get(ref_key)
            if ref_val is not None and not (isinstance(ref_val, str) and ref_val.strip()):
                errors.append(f"Asset '{asset_id}' field `{ref_key}` must be a non-empty string if present.")
    return errors


def resolve_subdir(project_dir: str, configured: str) -> str:
    return configured if os.path.isabs(configured) else os.path.join(project_dir, configured)


def run_guard(
    project_dir: str,
    strict: bool = False,
    logic_sub: str = os.path.join("src", "logic"),
    view_sub: str = os.path.join("src", "view"),
    manifest_sub: str = None,
) -> int:
    project_dir = os.path.abspath(project_dir)
    print("=" * 65)
    print(" [LJack GameCode Protocol] Static Layer & Manifest Guard")
    print("=" * 65)
    print(f"[*] Target Directory: {project_dir}")

    logic_dir = resolve_subdir(project_dir, logic_sub)
    view_dir = resolve_subdir(project_dir, view_sub)
    if manifest_sub:
        manifest_path = resolve_subdir(project_dir, manifest_sub)
    else:
        default_spec = os.path.join(project_dir, "specs", "asset_manifest.json")
        fallback_asset = os.path.join(project_dir, "assets", "asset_manifest.json")
        manifest_path = default_spec if os.path.isfile(default_spec) or not os.path.isfile(fallback_asset) else fallback_asset

    logic_violations = scan_files(logic_dir, FORBIDDEN_LOGIC_PATTERNS)
    view_warnings = scan_files(view_dir, VIEW_HARDCODE_PATTERNS)
    manifest_errors = validate_manifest(manifest_path)
    size_advisories = scan_oversized_files(view_dir) + scan_oversized_files(logic_dir)

    if logic_violations:
        print(f"\n[FAIL] Found {len(logic_violations)} Layer Isolation violation(s) in {logic_sub}:")
        for v in logic_violations:
            print(f"  - {v}")
    else:
        print(f"[PASS] Layer Isolation: {logic_sub} is 100% free of browser/DOM/audio APIs.")

    if manifest_errors:
        print(f"\n[FAIL] Found {len(manifest_errors)} Asset Manifest issue(s):")
        for e in manifest_errors:
            print(f"  - {e}")
    else:
        print(f"[PASS] Asset Manifest ({os.path.relpath(manifest_path, project_dir)}): schema, `aiPromptHint`, and extended metadata verified.")

    if view_warnings:
        print(f"\n[WARN] Found {len(view_warnings)} hardcoded asset reference(s) in {view_sub}:")
        for w in view_warnings:
            print(f"  - {w}")
    else:
        print("[PASS] View Binding: Zero raw asset paths or direct Audio instantiations found.")

    if size_advisories:
        print(f"\n[ADVISORY] Oversized file modularity warnings ({len(size_advisories)}):")
        for adv in size_advisories:
            print(f"  - {adv}")

    print("=" * 65)
    has_errors = bool(logic_violations or manifest_errors)
    if has_errors or (strict and view_warnings):
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="LJack GameCode Static Layer & Manifest Guard")
    parser.add_argument("project_dir", nargs="?", default=".", help="Target game project directory")
    parser.add_argument("--logic-dir", default=os.path.join("src", "logic"), help="Pure logic directory to guard")
    parser.add_argument("--view-dir", default=os.path.join("src", "view"), help="View directory to scan")
    parser.add_argument("--manifest", default=None, help="Path to asset_manifest.json (defaults to specs/ or assets/)")
    parser.add_argument("--strict", action="store_true", help="Fail on view warnings as well as logic/manifest errors")
    args = parser.parse_args()
    return run_guard(args.project_dir, args.strict, args.logic_dir, args.view_dir, args.manifest)


if __name__ == "__main__":
    sys.exit(main())
