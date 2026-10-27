#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Game Protocol v1.2.0] Multi-Engine Playable Review Gate Helper
=====================================================================
Detects engine ecosystem (Pygame, Tauri/HTML5, Godot 4.x), extracts
game-feel tuning parameters, and generates structured Playable Review
briefs for the user.

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

def detect_engine_and_inspect(game_dir: str):
    game_dir = os.path.abspath(game_dir)
    print("=" * 65)
    print(" [LJack Game Protocol v1.2.0] Playable Review Gate Inspection")
    print("=" * 65)
    print(f"[*] Target Directory: {game_dir}")

    is_godot = os.path.isfile(os.path.join(game_dir, "project.godot"))
    is_tauri = os.path.isfile(os.path.join(game_dir, "index.html")) or os.path.isdir(os.path.join(game_dir, "src-tauri"))
    is_pygame = os.path.isfile(os.path.join(game_dir, "run_game.py")) or os.path.isfile(os.path.join(game_dir, "src", "core", "state.py"))

    engine_name = "Unknown"
    launch_cmd = ""
    state_file = ""

    if is_godot:
        engine_name = "Godot Engine 4.x (GDScript)"
        launch_cmd = f"godot --path \"{game_dir}\""
        state_file = os.path.join(game_dir, "scripts", "core", "state.gd")
    elif is_tauri:
        engine_name = "Tauri + HTML5 / Canvas"
        launch_cmd = f"cd \"{game_dir}\" && (npm run tauri dev || npx serve .)"
        state_file = os.path.join(game_dir, "src", "core", "state.js")
    elif is_pygame:
        engine_name = "Pygame (Python 2D)"
        launch_cmd = f"python \"{os.path.join(game_dir, 'run_game.py')}\""
        state_file = os.path.join(game_dir, "src", "core", "state.py")
    else:
        engine_name = "Generic / Text Engine"
        launch_cmd = f"python \"{os.path.join(game_dir, 'run_game.py')}\""

    params = {}
    if state_file and os.path.isfile(state_file):
        try:
            with open(state_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if any(k in line.lower() for k in ["gravity", "speed", "jump", "hp", "fall"]):
                        if "=" in line:
                            parts = line.split("=")
                            name_side = parts[0].replace("var", "").replace("this.", "").strip()
                            key = name_side.split(":")[0].strip()
                            val = parts[1].replace(";", "").replace(",", "").strip()
                            params[key] = val
        except Exception:
            pass

    print(f"[*] Detected Engine : {engine_name}")
    print("-" * 65)
    print("🎮 [PLAYABLE REVIEW BRIEF FOR USER]")
    print("▶ Run Game Locally (One-Click Launch):")
    print(f"  {launch_cmd}")
    print("\n▶ Detected Game-Feel Tuning Parameters (Hot-Reloadable):")
    if params:
        for k, v in params.items():
            print(f"  - {k:<18} : {v}")
    else:
        print("  - Default internal balance configuration active.")

    print("-" * 65)
    print("★ Playable Review Checklist for User:")
    print("  1. Jump & Movement  : Does the horizontal speed and jump arc feel responsive?")
    print("  2. In-Game Tuner    : Press [F1] to fine-tune gravity and speed live!")
    print("  3. Difficulty Curve : Are platforms, obstacles, and enemy pacing fair?")
    print("  4. Final Approval   : Reply with feedback or 'Approved' to trigger packaging.")
    print("=" * 65)
    return 0

def main():
    parser = argparse.ArgumentParser(description="LJack Playable Review Helper")
    parser.add_argument("game_dir", nargs="?", default=".", help="Target game directory")
    args = parser.parse_args()

    return detect_engine_and_inspect(args.game_dir)

if __name__ == "__main__":
    sys.exit(main())
