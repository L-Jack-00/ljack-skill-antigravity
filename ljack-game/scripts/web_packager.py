#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Game Protocol v1.1.0] WebAssembly / HTML5 Web Game Packager
==================================================================
Prepares and packages Python/Pygame projects for instant browser execution
using WebAssembly (Pygbag / Canvas HTML5).

Enables sharing games with friends, mobile browsers, or Itch.io
without requiring any local Python installation.

Usage:
    python web_packager.py <game_directory> [--out-dir dist_web]
"""

import os
import sys
import shutil
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TEMPLATE_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{game_title} - LJack Web Preview</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Consolas', monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }}
        #game-container {{
            background: #1e293b;
            border: 2px solid #6366f1;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            padding: 20px;
            text-align: center;
            max-width: 840px;
        }}
        h1 {{ margin-top: 0; color: #a5b4fc; }}
        .badge {{ background: #4f46e5; padding: 4px 10px; border-radius: 12px; font-size: 12px; }}
        .cmd-box {{
            background: #090d16;
            padding: 12px;
            border-radius: 6px;
            border-left: 4px solid #10b981;
            text-align: left;
            margin: 15px 0;
            user-select: all;
        }}
    </style>
</head>
<body>
    <div id="game-container">
        <h1>🎮 {game_title} <span class="badge">WebAssembly Ready</span></h1>
        <p>Built with <strong>LJack Game Protocol</strong> (Zero-Token Harness & Deterministic Tick Engine).</p>
        
        <div class="cmd-box">
            <strong># Instant Local Web Host via Pygbag:</strong><br>
            pip install pygbag<br>
            python -m pygbag {game_dir_name}
        </div>

        <p style="color: #94a3b8; font-size: 14px;">
            Once started, open <a href="http://localhost:8000" target="_blank" style="color: #38bdf8;">http://localhost:8000</a> in your web browser.
        </p>
    </div>
</body>
</html>
"""

def package_web(game_dir: str, out_dir: str = "dist_web"):
    game_dir = os.path.abspath(game_dir)
    out_dir_abs = os.path.join(game_dir, out_dir)
    
    print("=" * 65)
    print(" [LJack Game Protocol] WebAssembly / HTML5 Packager")
    print("=" * 65)
    print(f"[*] Target Game: {game_dir}")
    print(f"[*] Output Dir : {out_dir_abs}")

    os.makedirs(out_dir_abs, exist_ok=True)

    game_title = os.path.basename(game_dir)
    html_content = TEMPLATE_INDEX_HTML.format(
        game_title=game_title,
        game_dir_name=os.path.basename(game_dir)
    )

    index_path = os.path.join(out_dir_abs, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Ensure main.py entrypoint exists for pygbag compatibility
    run_game_path = os.path.join(game_dir, "run_game.py")
    main_py_path = os.path.join(game_dir, "main.py")
    if os.path.isfile(run_game_path) and not os.path.isfile(main_py_path):
        shutil.copy2(run_game_path, main_py_path)
        print(f" [+] Created WebAssembly entrypoint: main.py (copied from run_game.py)")

    print(f" [+] Generated Web Portal: {os.path.relpath(index_path, game_dir)}")
    print("-" * 65)
    print("[SUCCESS] Web package prepared successfully.")
    print("Run web preview:")
    print(f"  cd \"{os.path.dirname(game_dir)}\" && python -m pygbag \"{os.path.basename(game_dir)}\"")
    print("=" * 65)
    return 0

def main():
    parser = argparse.ArgumentParser(description="LJack Game Web Packager")
    parser.add_argument("game_dir", nargs="?", default=".", help="Target game directory")
    parser.add_argument("--out-dir", default="dist_web", help="Output web directory")
    args = parser.parse_args()

    return package_web(args.game_dir, args.out_dir)

if __name__ == "__main__":
    sys.exit(main())
