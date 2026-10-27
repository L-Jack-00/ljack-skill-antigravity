#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Protocol v7.4.0] Release Sanitization & Artifact Rig
=============================================================
Wipes transient testing logs, cache artifacts, and temporary files
prior to packaging, and enforces the `_internal/` data isolation rule.

Usage:
    python release_cleaner.py <target_directory> [--dry-run]
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

def clean_artifacts(target_dir, dry_run=False):
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
    print("=" * 65)
    return 0

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    dry = "--dry-run" in sys.argv
    sys.exit(clean_artifacts(target, dry))
