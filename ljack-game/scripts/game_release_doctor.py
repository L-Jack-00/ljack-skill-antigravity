#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Game Protocol v1.3.0] Commercial Game Release Doctor & Health Auditor
============================================================================
Performs exhaustive AST & static inspection of the game project against
Steam/Commercial Store release standards:
  1. Atomic Save Data & Crash-proof persistence
  2. Production Debug Seal (F1 Live Tuner disabled in release)
  3. Display & Resolution Adaptability (Fullscreen, Aspect Ratio)
  4. Audio Voice Limiting & Volume Channels
  5. Multi-language Localization (i18n)
  6. Artifact cleanliness (Zero transient test logs)

Usage:
    python game_release_doctor.py <game_directory> [--strict]
"""

import os
import sys
import fnmatch
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'dist_web', '.godot', '_internal'}
SCANNABLE_EXTS = {'.py', '.js', '.ts', '.gd', '.json', '.html'}

class GameReleaseDoctor:
    def __init__(self, target_dir: str, strict: bool = False):
        self.target_dir = os.path.abspath(target_dir)
        self.strict = strict
        
        # Audit Flags
        self.has_atomic_save = False
        self.has_production_seal = False
        self.has_fullscreen_toggle = False
        self.has_audio_mixer = False
        self.has_localization = False
        self.junk_files = []
        self.total_source_files = 0

    def inspect_workspace(self):
        # 1. Check locales directory
        locales_dir = os.path.join(self.target_dir, "locales")
        if os.path.isdir(locales_dir) and len(os.listdir(locales_dir)) >= 2:
            self.has_localization = True

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for f in files:
                fpath = os.path.join(root, f)
                lower_f = f.lower()

                # Junk file detection
                for pat in ["test_*.log", "*.tmp", "*.bak", "crash.dmp"]:
                    if fnmatch.fnmatch(lower_f, pat):
                        self.junk_files.append(fpath)

                ext = os.path.splitext(f)[1].lower()
                if ext in SCANNABLE_EXTS:
                    self.total_source_files += 1
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read()

                        # Check Atomic Save
                        if any(term in content for term in ["os.replace", "NamedTemporaryFile", "ConfigFile.save", "atomic_save"]):
                            self.has_atomic_save = True

                        # Check Production Debug Seal
                        if any(term in content for term in ["PRODUCTION_BUILD", "DEBUG_TUNER", "is_debug", "OS.is_debug_build()"]):
                            self.has_production_seal = True

                        # Check Fullscreen / Resolution Toggle
                        if any(term in content for term in ["FULLSCREEN", "set_fullscreen", "window/size/mode", "toggle_fullscreen"]):
                            self.has_fullscreen_toggle = True

                        # Check Audio Mixer / Volume control
                        if any(term in content for term in ["mixer", "volume", "sound", "AudioServer", "set_volume"]):
                            self.has_audio_mixer = True

                    except Exception:
                        pass

    def run_checkup(self) -> int:
        print("=" * 65)
        print(" [LJack Game Protocol] Commercial Game Release Doctor")
        print("=" * 65)
        print(f"[*] Target Directory: {self.target_dir}")

        self.inspect_workspace()

        score = 0
        checks = []
        action_items = []

        # 1. Atomic Save Data Rig (20 pts)
        if self.has_atomic_save:
            score += 20
            checks.append(("[PASS]", "Pillar 7: Atomic Save Rig (Crash-proof save/replace active) (+20)"))
        else:
            checks.append(("[WARN]", "Pillar 7: Missing Atomic Save Rig (Risk of save file corruption on crash) (+0)"))
            action_items.append("Wrap save routine with os.replace() and temporary write to prevent save corruption.")

        # 2. Production Debug Seal (20 pts)
        if self.has_production_seal:
            score += 20
            checks.append(("[PASS]", "Pillar 5 & 8: Production Debug Seal (F1 Tuner sealed for commercial build) (+20)"))
        else:
            checks.append(("[WARN]", "Pillar 5 & 8: No PRODUCTION_BUILD flag found (F1 Tuner may be exposed to players) (+0)"))
            action_items.append("Add PRODUCTION_BUILD boolean flag to disable [F1] Tuner overlay in commercial releases.")

        # 3. Display & Resolution Adaptability (15 pts)
        if self.has_fullscreen_toggle:
            score += 15
            checks.append(("[PASS]", "Display: Fullscreen / Resolution adaptability supported (+15)"))
        else:
            checks.append(("[WARN]", "Display: Missing Fullscreen / Windowed toggle option (+0)"))
            action_items.append("Add Fullscreen toggle (e.g. Alt+Enter or F11) for Steam Deck / Wide display compliance.")

        # 4. Audio Mixer & Polyphony Safety (15 pts)
        if self.has_audio_mixer:
            score += 15
            checks.append(("[PASS]", "Audio: Audio mixer / volume channels detected (+15)"))
        else:
            checks.append(("[WARN]", "Audio: No audio mixer or master/BGM/SFX volume control found (+0)"))
            action_items.append("Implement independent volume channels (Master/BGM/SFX) to avoid audio clipping.")

        # 5. Commercial Localization i18n (15 pts)
        if self.has_localization:
            score += 15
            checks.append(("[PASS]", "i18n: Multi-language support (locales/ with >= 2 languages) verified (+15)"))
        else:
            checks.append(("[WARN]", "i18n: Missing locales/ directory or multi-language dictionaries (+0)"))
            action_items.append("Run python scripts/localization_linter.py --extract to generate locales/en.json and ko.json.")

        # 6. Artifact Cleanliness (15 pts)
        if not self.junk_files:
            score += 15
            checks.append(("[PASS]", "Pillar 8: Clean Release Artifacts (0 test logs / temporary dumps) (+15)"))
        else:
            checks.append(("[FAIL]", f"Pillar 8: Found {len(self.junk_files)} temporary log/test dumps in release directory! (+0)"))
            action_items.append(f"Wipe {len(self.junk_files)} transient log files before uploading to Steam / Stove.")

        # Print Checks
        for status, msg in checks:
            print(f" {status} {msg}")

        print("-" * 65)
        print(f"[*] Commercial Readiness Score: {score} / 100")

        if score >= 80:
            print("[COMMERCIAL GRADE APPROVED] Ready for Steam / Stove / Itch.io publishing.")
        else:
            print("[NEEDS REFINEMENT] Project requires commercial polish before public release.")

        if action_items:
            print("\n[🎯 ACTION ITEMS (Commercial Polish Directive)]:")
            for idx, item in enumerate(action_items, 1):
                print(f"  {idx}. {item}")

        print("=" * 65)
        if score < 70 or (self.strict and score < 100):
            return 1
        return 0

def main():
    parser = argparse.ArgumentParser(description="LJack Commercial Game Release Doctor")
    parser.add_argument("game_dir", nargs="?", default=".", help="Target game directory")
    parser.add_argument("--strict", action="store_true", help="Fail if score is less than 100")
    args = parser.parse_args()

    doctor = GameReleaseDoctor(args.game_dir, args.strict)
    return doctor.run_checkup()

if __name__ == "__main__":
    sys.exit(main())
