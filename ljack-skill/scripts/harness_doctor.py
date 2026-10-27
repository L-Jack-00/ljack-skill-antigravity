#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[LJack Protocol v7.4.0] Runtime Harness Static Doctor & Health Checker
======================================================================
Performs fast, zero-token AST & static inspection of the target project
to score compliance with the LJack 10 Pillars (I/O Decoupling, FSM,
Zero-load Pause, Emergency Stop, UTF-8 Guard, Headless Tests).

Outputs a concise, 3-line actionable diagnosis, eliminating thousands
of LLM context-reading and self-analysis tokens.

Usage:
    python harness_doctor.py <target_directory> [--strict]
"""

import os
import sys
import ast
import fnmatch
import argparse

# UTF-8 Output Guard for Windows CP949 consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

IGNORED_DIRS = {'.git', '.svn', '__pycache__', 'node_modules', '.idea', '.vscode', 'venv', 'env', '_internal'}

class HarnessDoctor:
    def __init__(self, root_dir: str, strict: bool = False):
        self.root_dir = os.path.abspath(root_dir)
        self.strict = strict
        self.py_files = []
        self.test_files = []
        self.junk_files = []
        
        # Diagnostic Flags
        self.has_utf8_guard = False
        self.has_fsm_or_enum = False
        self.has_emergency_stop = False
        self.has_pause_or_event = False
        self.has_busy_waiting_antipattern = False
        self.has_headless_tests = False
        self.has_cleanup_finally = False

    def collect_files(self):
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for f in files:
                fpath = os.path.join(root, f)
                lower_f = f.lower()
                
                # Check junk
                for pattern in ["test_*.log", "*.tmp", "*.bak"]:
                    if fnmatch.fnmatch(lower_f, pattern):
                        self.junk_files.append(fpath)
                
                if f.endswith(".py"):
                    rel = os.path.relpath(fpath, self.root_dir).lower()
                    if "test" in rel or lower_f.startswith("test_"):
                        self.test_files.append(fpath)
                    else:
                        self.py_files.append(fpath)

    def analyze_ast(self):
        for fpath in self.py_files:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            # 1. UTF-8 Guard check
            if "reconfigure(encoding='utf-8')" in content or "reconfigure(encoding=\"utf-8\")" in content:
                self.has_utf8_guard = True
            elif "PYTHONIOENCODING" in content:
                self.has_utf8_guard = True

            # 2. Text heuristics
            if any(term in content for term in ["emergency_stop", "stop_requested", "_stop_event", "KeyboardInterrupt"]):
                self.has_emergency_stop = True
            if any(term in content for term in ["threading.Event", "asyncio.Event", "_pause_event", "pause()", "resume()"]):
                self.has_pause_or_event = True

            # 3. AST deep inspection
            try:
                tree = ast.parse(content, filename=fpath)
                for node in ast.walk(tree):
                    # FSM / Enum check
                    if isinstance(node, ast.ClassDef):
                        for base in node.bases:
                            if isinstance(base, ast.Name) and "Enum" in base.id:
                                self.has_fsm_or_enum = True
                            elif isinstance(base, ast.Attribute) and base.attr == "Enum":
                                self.has_fsm_or_enum = True

                    # Try-finally cleanup check
                    if isinstance(node, ast.Try) and node.finalbody:
                        self.has_cleanup_finally = True

                    # Busy-waiting anti-pattern detection: while True: pass or while True: sleep(0)
                    if isinstance(node, ast.While):
                        if isinstance(node.test, ast.Constant) and node.test.value is True:
                            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                                self.has_busy_waiting_antipattern = True
            except Exception:
                pass

        if self.test_files:
            self.has_headless_tests = True

    def run_checkup(self) -> int:
        print("=" * 65)
        print(" [LJack Protocol] Runtime Harness Static Doctor & Health Check")
        print("=" * 65)
        print(f"[*] Target Directory: {self.root_dir}")
        
        self.collect_files()
        self.analyze_ast()

        total_py = len(self.py_files) + len(self.test_files)
        print(f"[*] Scanned Python Source Files: {len(self.py_files)}")
        print(f"[*] Scanned Headless Test Files: {len(self.test_files)}")
        print("-" * 65)

        score = 0
        checks = []
        action_items = []

        # Check 1: UTF-8 Console Safety Guard (15 pts)
        if self.has_utf8_guard:
            score += 15
            checks.append(("[PASS]", "Pillar 8: UTF-8 Console Encoding Safety Guard present (+15)"))
        else:
            checks.append(("[WARN]", "Pillar 8: Missing sys.stdout.reconfigure(encoding='utf-8') guard (+0)"))
            action_items.append("Add sys.stdout.reconfigure(encoding='utf-8') at application entrypoint.")

        # Check 2: Core-IO Decoupling & FSM State Machine (20 pts)
        if self.has_fsm_or_enum:
            score += 20
            checks.append(("[PASS]", "Pillar 3: Explicit FSM State Machine / Enum models present (+20)"))
        else:
            checks.append(("[WARN]", "Pillar 3: No explicit Enum/FSM state machine detected (+0)"))
            action_items.append("Define explicit HarnessState(Enum) to eliminate state race conditions.")

        # Check 3: Zero-Load Lifecycle Pause (15 pts)
        if self.has_pause_or_event and not self.has_busy_waiting_antipattern:
            score += 15
            checks.append(("[PASS]", "Pillar 4: Zero-Load Pause (Event-driven lifecycle) present (+15)"))
        elif self.has_busy_waiting_antipattern:
            checks.append(("[FAIL]", "Pillar 4: Busy-waiting anti-pattern (while True: pass) detected! (+0)"))
            action_items.append("Replace busy-waiting spin loops with threading.Event.wait() for CPU 0% idle.")
        else:
            checks.append(("[WARN]", "Pillar 4: No zero-load pause/resume event mechanism found (+0)"))
            action_items.append("Implement threading.Event for non-busy worker pause/resume.")

        # Check 4: Emergency Stop & Safety Interlock (20 pts)
        if self.has_emergency_stop:
            score += 20
            checks.append(("[PASS]", "Pillar 4 & 6: Emergency Stop Interlock & Signal handler present (+20)"))
        else:
            checks.append(("[FAIL]", "Pillar 4 & 6: Missing emergency stop / abort interlock flag (+0)"))
            action_items.append("Add emergency_stop() method and abort flag to worker/supervisor.")

        # Check 5: Headless Test Rig (20 pts)
        if self.has_headless_tests:
            score += 20
            checks.append(("[PASS]", f"Pillar 10: Headless Self-Test Runner detected ({len(self.test_files)} files) (+20)"))
        else:
            checks.append(("[FAIL]", "Pillar 10: Missing Headless Test Runner in tests/ (+0)"))
            action_items.append("Create tests/test_*.py to verify core logic without GUI within 0.5s.")

        # Check 6: Release Cleanliness & Junk Absence (10 pts)
        if not self.junk_files:
            score += 10
            checks.append(("[PASS]", "Pillar 7: Artifact Cleanliness (0 test logs / junk files) (+10)"))
        else:
            checks.append(("[WARN]", f"Pillar 7: Found {len(self.junk_files)} junk/log files in workspace (+0)"))
            action_items.append(f"Run release_cleaner.py to wipe {len(self.junk_files)} temporary log/test files.")

        # Print Check Results
        for status, msg in checks:
            print(f" {status} {msg}")

        print("-" * 65)
        print(f"[*] Harness Health Score: {score} / 100")

        if action_items:
            print("\n[🎯 ACTION ITEMS (Fast-Fix Directive)]:")
            for idx, item in enumerate(action_items, 1):
                print(f"  {idx}. {item}")
        else:
            print("[EXCELLENT] Project meets 100% of LJack Protocol Core Harness criteria.")

        print("=" * 65)

        # Failure condition
        if score < 60 or (self.strict and score < 100):
            return 1
        return 0

def main():
    parser = argparse.ArgumentParser(description="LJack Protocol Runtime Harness Static Doctor")
    parser.add_argument("target_dir", nargs="?", default=".", help="Target directory to inspect")
    parser.add_argument("--strict", action="store_true", help="Fail if score is less than 100")
    args = parser.parse_args()

    doctor = HarnessDoctor(args.target_dir, args.strict)
    return doctor.run_checkup()

if __name__ == "__main__":
    sys.exit(main())
