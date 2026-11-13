#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack GameCode Protocol v1.0.0] Static Layer Isolation & Manifest Guard
========================================================================
Zero-dependency static verifier for LJack GameCode projects:
  1. Layer Isolation Guard: Ensures `src/logic/` contains zero browser, DOM,
     Canvas, or WebAudio API calls so headless simulation remains 100% pure.
  2. Asset Manifest Audit: Validates `specs/asset_manifest.json` structure
     and verifies every asset defines an `aiPromptHint`.
  3. Hardcoded Asset Path Guard: Flags direct `new Audio(...)` or raw
     `"assets/..."` references inside `src/view/` that bypass `AssetHarness`.

Usage:
    python layer_guard.py <project_directory> [--strict]
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


def scan_files(base_dir: str, patterns: list) -> list:
    findings = []
    if not os.path.isdir(base_dir):
        return findings

    for root, _, files in os.walk(base_dir):
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
    return errors


def run_guard(project_dir: str, strict: bool = False) -> int:
    project_dir = os.path.abspath(project_dir)
    print("=" * 65)
    print(" [LJack GameCode Protocol] Static Layer & Manifest Guard")
    print("=" * 65)
    print(f"[*] Target Directory: {project_dir}")

    logic_dir = os.path.join(project_dir, "src", "logic")
    view_dir = os.path.join(project_dir, "src", "view")
    manifest_path = os.path.join(project_dir, "specs", "asset_manifest.json")

    logic_violations = scan_files(logic_dir, FORBIDDEN_LOGIC_PATTERNS)
    view_warnings = scan_files(view_dir, VIEW_HARDCODE_PATTERNS)
    manifest_errors = validate_manifest(manifest_path)

    if logic_violations:
        print(f"\n[FAIL] Found {len(logic_violations)} Layer Isolation violation(s) in src/logic/:")
        for v in logic_violations:
            print(f"  - {v}")
    else:
        print("[PASS] Layer Isolation: src/logic/ is 100% free of browser/DOM/audio APIs.")

    if manifest_errors:
        print(f"\n[FAIL] Found {len(manifest_errors)} Asset Manifest issue(s):")
        for e in manifest_errors:
            print(f"  - {e}")
    else:
        print("[PASS] Asset Manifest: specs/asset_manifest.json schema & aiPromptHint verified.")

    if view_warnings:
        print(f"\n[WARN] Found {len(view_warnings)} hardcoded asset reference(s) in src/view/:")
        for w in view_warnings:
            print(f"  - {w}")
    else:
        print("[PASS] View Binding: Zero raw asset paths or direct Audio instantiations found.")

    print("=" * 65)
    has_errors = bool(logic_violations or manifest_errors)
    if has_errors or (strict and view_warnings):
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="LJack GameCode Static Layer & Manifest Guard")
    parser.add_argument("project_dir", nargs="?", default=".", help="Target game project directory")
    parser.add_argument("--strict", action="store_true", help="Fail on view warnings as well as logic/manifest errors")
    args = parser.parse_args()
    return run_guard(args.project_dir, args.strict)


if __name__ == "__main__":
    sys.exit(main())
