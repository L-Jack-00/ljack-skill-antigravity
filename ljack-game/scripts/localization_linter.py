#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Game Protocol v1.5.0] Commercial Localization & UX Copy Linter
====================================================================
Scans game source code (Pygame, Tauri/JS, Godot GDScript) for hardcoded
display text, ensures multi-language dictionary (i18n) compliance,
and audits translation dictionaries for internal developer/harness jargon
in cooperation with LJack Protocol's UX Copy Gate.

Usage:
    python localization_linter.py <game_directory> [--extract] [--strict]
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

IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'dist_web', '.godot', '_internal'}
SCANNABLE_EXTS = {'.py', '.js', '.ts', '.gd', '.html'}

# Blacklisted developer/harness/AI internal jargon in game user UI
GAME_PROHIBITED_TERMS = {
    "하네스": "안전 가드, 안정화 도구, 또는 구체적 기능 명칭",
    "harness": "safety guard, stability engine, or specific feature name",
    "인터록": "안전 잠금, 오작동 방지, 자동 보호",
    "interlock": "safety lock, protection guard",
    "fsm": "작업 단계, 진행 상태, 게임 모드",
    "자가 치유": "자동 복구, 오류 자동 수정, 안정화",
    "self-healing": "auto-recovery, auto-repair, stabilization",
    "ljack": "시스템, 핵심 엔진 (최종 사용자 UI 노출 금지)",
    "히트박스": "타격 범위, 피격 영역, 경계선",
    "hitbox": "attack range, hit area, boundary",
    "서브스텝": "정밀 물리 계산",
    "substep": "precise physics step",
    "코요테 타임": "조작 보정 유예, 반응성 개선",
    "coyote time": "jump forgiveness, response buffer",
    "치트": "보조 옵션, 편의 기능 (상용 릴리즈 봉인)",
    "시뮬레이터": "연습장, 시뮬레이션 모드, 샌드박스",
}

# Regex patterns catching visible string literals in draw/render/text setters
LITERAL_PATTERNS = [
    re.compile(r'render\s*\(\s*["\']([^"\']{3,})["\']', re.IGNORECASE),
    re.compile(r'draw_text\s*\(\s*["\']([^"\']{3,})["\']', re.IGNORECASE),
    re.compile(r'fillText\s*\(\s*["\']([^"\']{3,})["\']', re.IGNORECASE),
    re.compile(r'text\s*=\s*["\']([^"\']{3,})["\']', re.IGNORECASE),
    re.compile(r'set_text\s*\(\s*["\']([^"\']{3,})["\']', re.IGNORECASE),
]

def audit_localization(game_dir: str, do_extract: bool = False):
    game_dir = os.path.abspath(game_dir)
    print("=" * 65)
    print(" [LJack Game Protocol] Commercial Localization (i18n) Linter")
    print("=" * 65)
    print(f"[*] Target Directory: {game_dir}")

    # Check for locales directory
    locales_dir = os.path.join(game_dir, "locales")
    has_locales = os.path.isdir(locales_dir)

    found_locales = []
    if has_locales:
        for f in os.listdir(locales_dir):
            if f.endswith((".json", ".cfg", ".po")):
                found_locales.append(f)

    print(f"[*] Locales Directory : {'FOUND' if has_locales else 'MISSING'}")
    print(f"[*] Active Locales    : {', '.join(found_locales) if found_locales else 'None'}")
    print("-" * 65)

    hardcoded_strings = []
    total_files = 0

    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SCANNABLE_EXTS:
                total_files += 1
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        for line_no, line in enumerate(fp, start=1):
                            line_s = line.strip()
                            if line_s.startswith(("#", "//", "/*", "*")):
                                continue
                            for pattern in LITERAL_PATTERNS:
                                matches = pattern.findall(line)
                                for m in matches:
                                    if len(m.strip()) > 2 and not m.startswith(("#", "%", "res://")):
                                        hardcoded_strings.append({
                                            "file": os.path.relpath(fpath, game_dir),
                                            "line": line_no,
                                            "text": m.strip()
                                        })
                except Exception:
                    pass

    print(f"[*] Scanned {total_files} source files.")
    print(f"[*] Hardcoded Display Literals Found: {len(hardcoded_strings)}")

    if not has_locales or len(found_locales) < 2:
        print("[WARN] Commercial games on Steam require at least 2 languages (e.g. en.json and ko.json).")

    # UX Copy Integrity Audit on Dictionary strings
    ux_violations = []
    if has_locales:
        for f in os.listdir(locales_dir):
            if f.endswith(".json"):
                fpath = os.path.join(locales_dir, f)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as jfp:
                        data = json.load(jfp)
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(v, str):
                                v_lower = v.lower()
                                for term, sug in GAME_PROHIBITED_TERMS.items():
                                    if term in v_lower:
                                        ux_violations.append({
                                            "file": f,
                                            "key": k,
                                            "term": term,
                                            "text": v,
                                            "suggestion": sug
                                        })
                except Exception:
                    pass

    if ux_violations:
        print(f"\n[FAIL] Found {len(ux_violations)} UX Copy violation(s) in translation dictionaries:")
        for uv in ux_violations:
            print(f"  - {uv['file']} [{uv['key']}] -> \"{uv['text']}\" (Prohibited: '{uv['term']}' -> Suggest: '{uv['suggestion']}')")
    else:
        if has_locales:
            print("[PASS] UX Copy Gate: 0 developer jargon violations in translation files.")

    if hardcoded_strings:
        print("\n[DETECTED HARDCODED TEXT (Sample)]:")
        for item in hardcoded_strings[:8]:
            print(f"  - {item['file']}:{item['line']} -> \"{item['text']}\"")
        if len(hardcoded_strings) > 8:
            print(f"  ... and {len(hardcoded_strings) - 8} more.")

    # Auto-extract feature to bootstrap locales/en.json
    if do_extract and hardcoded_strings:
        os.makedirs(locales_dir, exist_ok=True)
        en_path = os.path.join(locales_dir, "en.json")
        ko_path = os.path.join(locales_dir, "ko.json")

        extracted_dict = {}
        for idx, item in enumerate(hardcoded_strings, 1):
            key = f"STR_{idx:03d}_{re.sub(r'[^A-Z0-9]', '_', item['text'][:15].upper())}".strip('_')
            extracted_dict[key] = item['text']

        with open(en_path, "w", encoding="utf-8") as fp:
            json.dump(extracted_dict, fp, indent=2, ensure_ascii=False)
        with open(ko_path, "w", encoding="utf-8") as fp:
            json.dump(extracted_dict, fp, indent=2, ensure_ascii=False)
        print(f"\n[SUCCESS] Extracted {len(extracted_dict)} string keys into locales/en.json and ko.json!")

    print("=" * 65)
    return len(hardcoded_strings)

def main():
    parser = argparse.ArgumentParser(description="LJack Commercial Localization Linter")
    parser.add_argument("game_dir", nargs="?", default=".", help="Target game directory")
    parser.add_argument("--extract", action="store_true", help="Auto-extract literals to locales/en.json")
    args = parser.parse_args()

    return 0 if audit_localization(args.game_dir, args.extract) == 0 else 0

if __name__ == "__main__":
    sys.exit(main())
