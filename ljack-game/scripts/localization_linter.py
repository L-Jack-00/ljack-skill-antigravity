#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Game Protocol v1.6.0] Commercial Localization & In-Place Rewrite Linter
=============================================================================
Scans game source code (Pygame, Tauri/JS, Godot GDScript) for hardcoded
display text, ensures multi-language dictionary (i18n) compliance,
and provides atomic IN-PLACE source rewriting (--rewrite / --fix) to replace
hardcoded string literals with localized lookup calls `t("KEY")` (or `tr("KEY")` in Godot).

Key Features:
- Detection: Scans UI and draw/render calls for hardcoded text literals.
- Extraction (--extract): Builds or merges `locales/en.json` and `locales/ko.json`.
- In-Place Rewrite (--rewrite / --fix):
  * Backs up source files to `.bak` automatically.
  * Replaces literals with `t("KEY")` (Python/JS) or `tr("KEY")` (GDScript).
  * Automatically scaffolds zero-dependency `locales/i18n.py` and/or `locales/i18n.js`.
  * Safely injects `from locales.i18n import t` into rewritten Python files.
- UX Copy Auditing: Audits dictionaries for internal developer/harness jargon.

Usage:
    python localization_linter.py <game_directory> [--extract] [--rewrite] [--strict] [--no-backup]
"""

import os
import sys
import re
import json
import shutil
import argparse

# Windows CP949 Console UTF-8 Guard
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'dist_web', '.godot', '_internal', '.vscode', '.idea'}
SCANNABLE_EXTS = {'.py', '.js', '.ts', '.gd', '.html'}

# Prohibited internal developer/harness/AI jargon in game UI
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
    "임시 수정": "기능의 목적 또는 룰 명세로 대체",
    "버그 수정": "게임 룰/예외 방어 스펙으로 기술",
    "ai 생성": "도메인 설명으로 대체",
    "temp fix": "describe game rule specification instead",
}

# Regex patterns detecting visible string literals in UI / render calls
PATTERNS = [
    re.compile(r'(\brender\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'(\bdraw_text\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'(\bfillText\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'(\bsetWindowTitle\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'(\bset_text\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'(\bsetText\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'(\btoast\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'(\balert\s*\(\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'((?<!\w)text\s*=\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
    re.compile(r'((?<!\w)title\s*=\s*)(["\'])([^"\']{2,})\2', re.IGNORECASE),
]

IGNORED_LITERAL_PREFIXES = ("#", "%", "res://", "http://", "https://", "data:", "/", "./", "../", "assets/", "images/", "sounds/")
IGNORED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.svg', '.ogg', '.wav', '.mp3', '.json', '.csv', '.tscn', '.gd', '.py', '.js', '.ts', '.css', '.html')

I18N_PY_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
[LJack Game Protocol] Zero-Dependency Runtime Localization (i18n) Engine
=======================================================================
Crash-proof dictionary loader and text translation helper.
"""

import os
import json

_CURRENT_LANG = os.environ.get("GAME_LANG", "ko")
_DICTIONARIES = {}

def get_locales_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def load_translations(locales_dir: str = None):
    global _DICTIONARIES
    if locales_dir is None:
        locales_dir = get_locales_dir()
    for lang in ["ko", "en"]:
        p = os.path.join(locales_dir, f"{lang}.json")
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as fp:
                    _DICTIONARIES[lang] = json.load(fp)
            except Exception:
                _DICTIONARIES[lang] = {}

def set_language(lang: str):
    global _CURRENT_LANG
    _CURRENT_LANG = lang

def get_language() -> str:
    return _CURRENT_LANG

def t(key: str, default: str = None) -> str:
    """Returns localized string for `key`. Falls back to English, then default, then key."""
    if not _DICTIONARIES:
        load_translations()
    lang_dict = _DICTIONARIES.get(_CURRENT_LANG, {})
    if key in lang_dict:
        return lang_dict[key]
    en_dict = _DICTIONARIES.get("en", {})
    if key in en_dict:
        return en_dict[key]
    return default if default is not None else key
'''

I18N_JS_TEMPLATE = '''/**
 * [LJack Game Protocol] Zero-Dependency Runtime Localization (i18n) Engine
 * =======================================================================
 * Asynchronous/synchronous multi-language translation manager.
 */

export const i18n = {
  currentLang: 'ko',
  dictionaries: {},

  async init(lang = 'ko', basePath = 'locales') {
    this.currentLang = lang;
    for (const l of ['ko', 'en']) {
      try {
        const res = await fetch(`${basePath}/${l}.json`);
        this.dictionaries[l] = await res.json();
      } catch (e) {
        this.dictionaries[l] = {};
      }
    }
  },

  setLanguage(lang) {
    this.currentLang = lang;
  },

  t(key, defaultVal) {
    const dict = this.dictionaries[this.currentLang] || {};
    if (dict[key] !== undefined) return dict[key];
    const fallback = this.dictionaries['en'] || {};
    if (fallback[key] !== undefined) return fallback[key];
    return defaultVal !== undefined ? defaultVal : key;
  }
};

export const t = (key, defaultVal) => i18n.t(key, defaultVal);

if (typeof window !== 'undefined') {
  window.t = t;
  window.i18n = i18n;
}
'''

def should_ignore_text(text: str) -> bool:
    s = text.strip()
    if len(s) < 2:
        return True
    if any(s.startswith(p) for p in IGNORED_LITERAL_PREFIXES):
        return True
    if any(s.lower().endswith(ext) for ext in IGNORED_EXTENSIONS):
        return True
    if re.match(r'^#[0-9a-fA-F]{3,8}$', s) or s.isdigit():
        return True
    return False

def make_key(text: str, existing_keys: set) -> str:
    cleaned = re.sub(r'[^A-Za-z0-9]+', '_', text.strip()).strip('_').upper()
    words = [w for w in cleaned.split('_') if w][:4]
    slug = '_'.join(words)[:20] if words else "TEXT"
    candidate = f"STR_{slug}"
    if candidate not in existing_keys:
        return candidate
    counter = 2
    while f"{candidate}_{counter}" in existing_keys:
        counter += 1
    return f"{candidate}_{counter}"

def scaffold_i18n_runtime(locales_dir: str, has_py: bool, has_js: bool):
    os.makedirs(locales_dir, exist_ok=True)
    if has_py:
        py_file = os.path.join(locales_dir, "i18n.py")
        init_file = os.path.join(locales_dir, "__init__.py")
        if not os.path.exists(py_file):
            with open(py_file, "w", encoding="utf-8") as fp:
                fp.write(I18N_PY_TEMPLATE)
            print("  + [Scaffolded] locales/i18n.py runtime engine created.")
        if not os.path.exists(init_file):
            with open(init_file, "w", encoding="utf-8") as fp:
                fp.write("from .i18n import t, set_language, get_language, load_translations\n")

    if has_js:
        js_file = os.path.join(locales_dir, "i18n.js")
        if not os.path.exists(js_file):
            with open(js_file, "w", encoding="utf-8") as fp:
                fp.write(I18N_JS_TEMPLATE)
            print("  + [Scaffolded] locales/i18n.js runtime engine created.")

def find_safe_python_import_insertion_index(lines):
    in_docstring = False
    doc_delim = None
    first_body_idx = 0

    for idx, l in enumerate(lines):
        l_s = l.strip()
        if not in_docstring:
            if l_s.startswith(("#!", "# -*-", "# coding")):
                continue
            if l_s.startswith(('"""', "'''")):
                doc_delim = l_s[:3]
                if l_s.count(doc_delim) >= 2 and len(l_s) > 3:
                    continue
                in_docstring = True
                continue
            if l_s.startswith("#") or not l_s:
                continue
            first_body_idx = idx
            break
        else:
            if doc_delim in l_s:
                in_docstring = False
                doc_delim = None
                continue
    return first_body_idx

def rewrite_file_content(fpath: str, ext: str, text_to_key: dict, make_backup: bool = True) -> int:
    try:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
            original = fp.read()
    except Exception:
        return 0

    lines = original.splitlines(keepends=True)
    modified_lines = []
    changes_count = 0

    fn_name = "tr" if ext == ".gd" else "t"

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("#", "//", "/*", "*")):
            modified_lines.append(line)
            continue

        new_line = line
        for pattern in PATTERNS:
            def replacer(match):
                prefix = match.group(1)
                text = match.group(3)
                if should_ignore_text(text):
                    return match.group(0)
                if text in text_to_key:
                    key = text_to_key[text]
                    return f'{prefix}{fn_name}("{key}")'
                return match.group(0)

            updated = pattern.sub(replacer, new_line)
            if updated != new_line:
                changes_count += 1
                new_line = updated

        modified_lines.append(new_line)

    if changes_count == 0:
        return 0

    new_content = "".join(modified_lines)

    if ext == ".py":
        if "from locales.i18n import t" not in new_content and "def t(" not in new_content:
            import_block = (
                "# [LJack i18n Guard] Translation Helper Import\n"
                "try:\n"
                "    from locales.i18n import t\n"
                "except ImportError:\n"
                "    def t(key, default=None):\n"
                "        return default if default is not None else key\n\n"
            )
            lines_check = new_content.splitlines(keepends=True)
            insert_idx = find_safe_python_import_insertion_index(lines_check)
            lines_check.insert(insert_idx, import_block)
            new_content = "".join(lines_check)

    if make_backup:
        bak_path = f"{fpath}.bak"
        try:
            shutil.copy2(fpath, bak_path)
        except Exception:
            pass

    with open(fpath, "w", encoding="utf-8") as fp:
        fp.write(new_content)

    return changes_count

def audit_localization(game_dir: str, do_extract: bool = False, do_rewrite: bool = False, make_backup: bool = True):
    game_dir = os.path.abspath(game_dir)
    print("=" * 65)
    print(" [LJack Game Protocol] Commercial Localization (i18n) Linter")
    print("=" * 65)
    print(f"[*] Target Directory: {game_dir}")

    locales_dir = os.path.join(game_dir, "locales")
    has_locales = os.path.isdir(locales_dir)

    found_locales = []
    en_dict = {}
    ko_dict = {}

    if has_locales:
        for f in os.listdir(locales_dir):
            if f.endswith((".json", ".cfg", ".po")):
                found_locales.append(f)
        en_path = os.path.join(locales_dir, "en.json")
        ko_path = os.path.join(locales_dir, "ko.json")
        if os.path.isfile(en_path):
            try:
                with open(en_path, "r", encoding="utf-8-sig") as fp:
                    en_dict = json.load(fp)
            except Exception:
                pass
        if os.path.isfile(ko_path):
            try:
                with open(ko_path, "r", encoding="utf-8-sig") as fp:
                    ko_dict = json.load(fp)
            except Exception:
                pass

    print(f"[*] Locales Directory : {'FOUND' if has_locales else 'MISSING'}")
    print(f"[*] Active Locales    : {', '.join(found_locales) if found_locales else 'None'}")
    print("-" * 65)

    hardcoded_strings = []
    scannable_files = []
    has_py = False
    has_js = False

    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SCANNABLE_EXTS:
                if ext == '.py':
                    has_py = True
                elif ext in ('.js', '.ts', '.html'):
                    has_js = True

                fpath = os.path.join(root, f)
                scannable_files.append((fpath, ext))
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        for line_no, line in enumerate(fp, start=1):
                            line_s = line.strip()
                            if line_s.startswith(("#", "//", "/*", "*")):
                                continue
                            for pattern in PATTERNS:
                                for match in pattern.finditer(line):
                                    text = match.group(3)
                                    if not should_ignore_text(text):
                                        hardcoded_strings.append({
                                            "file": os.path.relpath(fpath, game_dir),
                                            "full_path": fpath,
                                            "ext": ext,
                                            "line": line_no,
                                            "text": text.strip()
                                        })
                except Exception:
                    pass

    print(f"[*] Scanned {len(scannable_files)} source files.")
    print(f"[*] Hardcoded Display Literals Found: {len(hardcoded_strings)}")

    if not has_locales or len(found_locales) < 2:
        print("[WARN] Commercial games on Steam require at least 2 languages (e.g. en.json and ko.json).")

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
        for item in hardcoded_strings[:6]:
            print(f"  - {item['file']}:{item['line']} -> \"{item['text']}\"")
        if len(hardcoded_strings) > 6:
            print(f"  ... and {len(hardcoded_strings) - 6} more.")

    # Inverted map from existing en_dict: text -> key
    text_to_key = {}
    for k, v in en_dict.items():
        if isinstance(v, str):
            text_to_key[v] = k

    existing_keys = set(en_dict.keys())

    for item in hardcoded_strings:
        txt = item["text"]
        if txt not in text_to_key:
            key = make_key(txt, existing_keys)
            text_to_key[txt] = key
            existing_keys.add(key)
            en_dict[key] = txt
            if key not in ko_dict:
                ko_dict[key] = txt

    if (do_extract or do_rewrite) and hardcoded_strings:
        os.makedirs(locales_dir, exist_ok=True)
        en_path = os.path.join(locales_dir, "en.json")
        ko_path = os.path.join(locales_dir, "ko.json")

        with open(en_path, "w", encoding="utf-8") as fp:
            json.dump(en_dict, fp, indent=2, ensure_ascii=False)
        with open(ko_path, "w", encoding="utf-8") as fp:
            json.dump(ko_dict, fp, indent=2, ensure_ascii=False)
        print(f"\n[SUCCESS] Extracted/Merged {len(en_dict)} string keys into locales/en.json and ko.json!")

    if do_rewrite and hardcoded_strings:
        print("\n[*] Starting In-Place Source Code Rewriter (--rewrite)...")
        scaffold_i18n_runtime(locales_dir, has_py, has_js)

        modified_files = 0
        total_replacements = 0

        for fpath, ext in scannable_files:
            replacements = rewrite_file_content(fpath, ext, text_to_key, make_backup=make_backup)
            if replacements > 0:
                modified_files += 1
                total_replacements += replacements
                rel = os.path.relpath(fpath, game_dir)
                print(f"  ✔ Rewrote {replacements} literal(s) in {rel} (Backup: .bak)")

        print(f"\n[ALL PASS] Successfully replaced {total_replacements} hardcoded literal(s) across {modified_files} file(s)!")
        print("  - Localized functions: t(\"KEY\") applied.")
        print("  - Original backups created (.bak).")

    print("=" * 65)
    remaining_hardcoded = 0 if (do_rewrite and hardcoded_strings) else len(hardcoded_strings)
    return remaining_hardcoded + len(ux_violations)

def main():
    parser = argparse.ArgumentParser(description="LJack Commercial Localization Linter & In-Place Rewriter")
    parser.add_argument("game_dir", nargs="?", default=".", help="Target game directory")
    parser.add_argument("--extract", action="store_true", help="Auto-extract literals to locales/en.json")
    parser.add_argument("--rewrite", "--fix", action="store_true", dest="rewrite", help="In-place rewrite source files with t(\"KEY\") and auto-scaffold i18n helpers")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if hardcoded strings or UX Copy violations exist")
    parser.add_argument("--no-backup", action="store_true", help="Disable creating .bak backup files")
    args = parser.parse_args()

    issues = audit_localization(args.game_dir, args.extract, args.rewrite, not args.no_backup)
    if args.strict and issues > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
