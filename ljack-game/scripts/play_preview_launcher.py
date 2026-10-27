#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Game Protocol v1.0.0] Playable Review Gate Helper
=========================================================
Extracts game balance parameters, controls, and launch commands
to present a structured "Playable Review Request" to the user
prior to any packaging or release deployment.

Usage:
    python play_preview_launcher.py <game_directory>
"""

import os
import sys
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def inspect_review_parameters(game_dir: str):
    print("=" * 65)
    print(" [LJack Game Protocol] Playable Review Gate Inspection")
    print("=" * 65)
    print(f"[*] Target Game Directory: {os.path.abspath(game_dir)}")

    state_path = os.path.join(game_dir, "src", "core", "state.py")
    run_path = os.path.join(game_dir, "run_game.py")

    if not os.path.isfile(run_path):
        print(f"[WARN] Playable launcher 'run_game.py' not found at {run_path}")

    params = {}
    if os.path.isfile(state_path):
        try:
            with open(state_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if any(keyword in line for keyword in ["gravity", "speed", "jump_strength", "hp", "friction"]):
                        parts = line.split(":")
                        if len(parts) == 2:
                            name = parts[0].strip()
                            val_part = parts[1].split("=")[-1].strip() if "=" in parts[1] else parts[1].strip()
                            params[name] = val_part
        except Exception:
            pass

    print("\n🎮 [PLAYABLE REVIEW BRIEF FOR USER]")
    print("-" * 65)
    print("▶ Run Game Locally:")
    print(f"  python \"{os.path.join(game_dir, 'run_game.py')}\"")
    print("\n▶ Detected Tuning Parameters (Game Feel & Balance):")
    if params:
        for k, v in params.items():
            print(f"  - {k:<15} : {v}")
    else:
        print("  - Default internal balance configuration active.")
    
    print("-" * 65)
    print("★ Playable Review Checklist for User:")
    print("  1. Jump Arc & Timing : Does the jump feel responsive or floaty?")
    print("  2. Movement Speed    : Is horizontal velocity well-paced?")
    print("  3. Difficulty Curve  : Are obstacles and enemy patterns fair?")
    print("  4. Polish & Visuals  : Do particles/animations line up with input?")
    print("=" * 65)
    return 0

def main():
    parser = argparse.ArgumentParser(description="LJack Game Playable Review Helper")
    parser.add_argument("game_dir", nargs="?", default=".", help="Target game directory")
    args = parser.parse_args()

    return inspect_review_parameters(args.game_dir)

if __name__ == "__main__":
    sys.exit(main())
