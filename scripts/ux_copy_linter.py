#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Protocol v7.4.0] UX Copy & Surface Integrity Linter
===========================================================
Scans source code, UI templates, dialogs, tooltips, and release notes
for internal developer/harness/AI jargon and enforces user-friendly,
feature-centric UX copy.

Usage:
    python ux_copy_linter.py <target_directory_or_file> [--strict]
"""

import os
import sys
import re
import argparse

# UTF-8 Output Guard for Windows CP949 consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Blacklisted developer/harness/AI internal jargon in user-facing surfaces
PROHIBITED_TERMS = {
    "하네스": "안전 가드, 안정화 도구, 또는 구체적 기능 명칭",
    "harness": "safety guard, stability engine, or specific feature name",
    "인터록": "안전 잠금, 오작동 방지, 자동 보호",
    "interlock": "safety lock, protection guard, error shield",
    "fsm": "작업 단계, 진행 상태, 모드",
    "자가 치유": "자동 복구, 오류 자동 수정, 안정화",
    "self-healing": "auto-recovery, auto-repair, stabilization",
    "디커플링": "독립 실행, 성능 최적화, 반응 속도 개선",
    "decoupling": "independent processing, performance optimization",
    "ljack": "시스템, 핵심 엔진 (최종 사용자 UI에 프로토콜명 노출 금지)",
    "워커 스레드": "백그라운드 처리, 비동기 작업",
    "worker thread": "background processing, async task",
    "mock": "가상 데이터, 테스트용 설정 (프로덕션 노출 금지)",
    "머신 러닝 수정": "기능 개선, 정확도 향상",
    "llm": "스마트 엔진, 지능형 지원",
}

# Targeted UI/User-facing string patterns
UI_PATTERNS = [
    re.compile(r'setWindowTitle\s*\(\s*["\'](.*?)["\']\s*\)', re.IGNORECASE),
    re.compile(r'setText\s*\(\s*["\'](.*?)["\']\s*\)', re.IGNORECASE),
    re.compile(r'setToolTip\s*\(\s*["\'](.*?)["\']\s*\)', re.IGNORECASE),
    re.compile(r'showMessage\s*\(\s*["\'](.*?)["\']\s*\)', re.IGNORECASE),
    re.compile(r'QMessageBox\.\w+\s*\([^,]+,\s*["\'](.*?)["\']\s*,\s*["\'](.*?)["\']', re.IGNORECASE),
    re.compile(r'alert\s*\(\s*["\'](.*?)["\']\s*\)', re.IGNORECASE),
    re.compile(r'toast\s*\(\s*["\'](.*?)["\']\s*\)', re.IGNORECASE),
    re.compile(r'placeholder\s*=\s*["\'](.*?)["\']', re.IGNORECASE),
    re.compile(r'title\s*=\s*["\'](.*?)["\']', re.IGNORECASE),
]

IGNORED_DIRS = {'.git', '.svn', '__pycache__', 'node_modules', '.idea', '.vscode', 'venv', 'env', '_internal'}
SCANNABLE_EXTS = {'.py', '.cs', '.js', '.ts', '.jsx', '.tsx', '.html', '.json', '.md', '.txt', '.cpp', '.h', '.rs'}

def audit_text(text, file_path, line_no=None, context_label=""):
    violations = []
    text_lower = text.lower()
    for term, suggestion in PROHIBITED_TERMS.items():
        if term in text_lower:
            violations.append({
                "file": file_path,
                "line": line_no,
                "context": context_label or text.strip(),
                "term": term,
                "suggestion": suggestion
            })
    return violations

def scan_file(file_path):
    violations = []
    # Protocol spec files in ljack-skill define the terms themselves, so skip meta-audit
    norm_path = os.path.normpath(file_path).lower()
    if "ljack-skill" in norm_path and (norm_path.endswith("skill.md") or "references" in norm_path or "scripts" in norm_path):
        return violations

    is_markdown_or_text = file_path.endswith(('.md', '.txt'))
    is_release_note = is_markdown_or_text and ('release' in norm_path or 'changelog' in norm_path)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        return violations

    for idx, line in enumerate(lines, start=1):
        # 1. Inspect targeted UI setter functions
        for pattern in UI_PATTERNS:
            matches = pattern.findall(line)
            for m in matches:
                texts_to_check = m if isinstance(m, tuple) else [m]
                for text_item in texts_to_check:
                    violations.extend(audit_text(text_item, file_path, idx, line.strip()))

        # 2. If it's a release note or markdown user doc, inspect directly
        if is_release_note:
            violations.extend(audit_text(line, file_path, idx, line.strip()))

    return violations

def run_audit(target_dir):
    print("=" * 65)
    print(" [LJack Protocol] UX Copy & Surface Integrity Linter")
    print("=" * 65)
    print(f"[*] Scanning path: {target_dir}")

    all_violations = []
    total_files = 0

    if os.path.isfile(target_dir):
        files_to_scan = [target_dir]
    else:
        files_to_scan = []
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SCANNABLE_EXTS:
                    files_to_scan.append(os.path.join(root, file))

    for fpath in files_to_scan:
        total_files += 1
        violations = scan_file(fpath)
        all_violations.extend(violations)

    print(f"[*] Scanned {total_files} files.")
    print("-" * 65)

    if not all_violations:
        print("[PASS] 0 UX Copy violations found. UI surfaces are 100% clean & user-friendly.")
        print("=" * 65)
        return 0

    print(f"[FAIL] Found {len(all_violations)} UX Copy violation(s) in user-facing surfaces:")
    for v in all_violations:
        loc = f"{v['file']}:{v['line']}" if v['line'] else v['file']
        print(f"\n- Location  : {loc}")
        print(f"  Snippet   : \"{v['context']}\"")
        print(f"  Prohibited: [{v['term']}]")
        print(f"  Suggestion: Use '{v['suggestion']}' instead.")
    print("=" * 65)
    return len(all_violations)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(run_audit(target))
