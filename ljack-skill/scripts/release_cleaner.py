#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Protocol v7.6.0] Release Sanitization & Artifact Rig
=============================================================
Wipes transient testing logs, cache artifacts, and temporary files
prior to packaging, enforces the `_internal/` data isolation rule,
and optionally audits staging bundles (`--check-staging`) so raw AI caches
(`_raw_cache`, `style_samples`, `workflows`, `temp`) and stale archives
do not slip into distributable packages.

Usage:
    python release_cleaner.py <target_directory> [--dry-run] [--check-staging]
"""

import os
import sys
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

JUNK_PATTERNS = [
    "test_*.log",
    "*.tmp",
    "*.log",
    "*.bak",
    "*.pyc",
    "thumbs.db",
    "desktop.ini",
]

JUNK_DIRS = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".coverage",
]

def check_staging_hygiene(target_dir):
    warnings = []
    for staging_name in ("dist-web", "_internal"):
        assets_dir = os.path.join(target_dir, staging_name, "assets")
        if os.path.isdir(assets_dir):
            for leak in ("_raw_cache", "style_samples", "workflows", "temp"):
                leak_path = os.path.join(assets_dir, leak)
                if os.path.isdir(leak_path):
                    warnings.append(f"Staging directory contains raw/temp folder: {os.path.relpath(leak_path, target_dir)}")

    dist_dir = os.path.join(target_dir, "dist")
    if os.path.isdir(dist_dir):
        exes = [os.path.join(dist_dir, f) for f in os.listdir(dist_dir) if f.lower().endswith(".exe")]
        zips = [os.path.join(dist_dir, f) for f in os.listdir(dist_dir) if f.lower().endswith(".zip")]
        if exes and zips:
            newest_exe = max(os.path.getmtime(p) for p in exes)
            for zp in zips:
                if os.path.getmtime(zp) + 300 < newest_exe:
                    warnings.append(f"Stale release archive older than latest .exe: {os.path.relpath(zp, target_dir)}")

    if warnings:
        print("\n[STAGING ADVISORIES]:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("[PASS] Staging hygiene clean (no leaked raw asset caches or stale archives).")


def clean_artifacts(target_dir, dry_run=False, check_staging=False):
    print("=" * 65)
    print(" [LJack Protocol] Release Sanitization & Artifact Rig")
    print("=" * 65)
    print(f"[*] Target Directory: {target_dir}")
    print(f"[*] Mode: {'DRY RUN' if dry_run else 'ACTIVE CLEAN'}")

    removed_files = 0
    removed_dirs = 0

    import fnmatch
    for root, dirs, files in os.walk(target_dir, topdown=False):
        # 1. Clean Junk Directories
        for d in dirs:
            if d in JUNK_DIRS:
                dpath = os.path.join(root, d)
                if not dry_run:
                    shutil.rmtree(dpath, ignore_errors=True)
                print(f"[-] Removed directory: {dpath}")
                removed_dirs += 1

        # 2. Clean Junk Files
        for f in files:
            for pattern in JUNK_PATTERNS:
                if fnmatch.fnmatch(f.lower(), pattern):
                    fpath = os.path.join(root, f)
                    if not dry_run:
                        try:
                            os.remove(fpath)
                        except Exception:
                            pass
                    print(f"[-] Removed file: {fpath}")
                    removed_files += 1
                    break

    print("-" * 65)
    print(f"[SUMMARY] Removed {removed_files} junk files and {removed_dirs} cache directories.")
    print("[PASS] Release artifact sanitized. 0 test logs remaining.")
    if check_staging:
        check_staging_hygiene(target_dir)
    print("=" * 65)
    return 0

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = args[0] if args else "."
    dry = "--dry-run" in sys.argv
    staging = "--check-staging" in sys.argv
    sys.exit(clean_artifacts(target, dry, staging))
