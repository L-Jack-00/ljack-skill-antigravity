# 엘잭 프로토콜 스위트 (LJack Protocol Suite)
## 범용 소프트웨어 & 멀티 엔진 인디 게임 자율 에이전틱 개발 프로토콜

[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Skills-blue.svg)](https://deepmind.google/technologies/antigravity/)
[![LJack Skill](https://img.shields.io/badge/ljack--skill-v7.6.0-green.svg)](#-1-ljack-skill-v760)
[![LJack Game](https://img.shields.io/badge/ljack--game-v1.7.0_Commercial-purple.svg)](#-2-ljack-game-v170-commercial-edition)
[![LJack GameCode](https://img.shields.io/badge/ljack--gamecode-v1.1.0-teal.svg)](#-3-ljack-gamecode-v110)
[![Engines](https://img.shields.io/badge/Game_Engines-Pygame%20%7C%20Tauri%20%7C%20Godot%20%7C%20Rust-orange.svg)](#-2-ljack-game-v170-commercial-edition)
[![Commercial Ready](https://img.shields.io/badge/Steam%20Ready-Atomic%20Save%20%7C%20Audio%20Rig%20%7C%20i18n-success.svg)](#-2-ljack-game-v170-commercial-edition)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 AI 에이전트가 소프트웨어 및 게임 개발 시 기술적 결함(빌드, 테스트, 물리, 린트)을 자체 검증과 자가 치유(Self-Healing) 루프로 자율 완주하고, 상용화 품질 게이트(세이브 원자성, 다국어, 오디오 안전망, UX 카피)까지 일관되게 적용하도록 규정하는 **LJack 런타임 하네스 엔지니어링 프로토콜 모음(Suite)**입니다.

개발 목적과 아키텍처 제약 수준에 맞추어 **3가지 독립 프로토콜**로 제공됩니다:

---

## 🏛️ 하위 프로토콜 안내

### 1. 🛠️ [ljack-skill](./ljack-skill/) (v7.6.0)
* **목적**: 범용 시스템 소프트웨어, 데스크톱 GUI(PyQt/WinForms), 웹 백엔드/프론트엔드, CLI 데이터 파이프라인, Rust-Python 이원화 하네스, REA 역공학 클린룸 재구축.
* **10대 기둥**: 코어/IO 분리(Rust 코어 + Python 인터페이스 공식 지원), 슈퍼바이저 루프, 명시적 FSM, 이벤트 기반 유휴 대기, 디바운스 종료 `flush()`·오버레이 특이성·JS/TS/CSS 거대 모듈 진단, 물리 입력 자가 치유, 독자 중심 UX 카피 무결성 가드, (GUI) 풀블리드 `1024x1024` 아이콘·누끼 보색 시트(`#479be6`)·인터랙션 접근성(`aria-disabled`).
* **번들링 도구**:
  - `harness_scaffolder.py`: 10대 기둥 표준 골격 즉시 생성 (CLI, Desktop, API, Rust-Python Hybrid 지원).
  - `harness_doctor.py`: AST 정적 분석 기반 하네스 준수율 채점(0~100) + JS/TS/CSS 거대 모듈·지연 저장 어드바이저리.
  - `ux_copy_linter.py`, `release_cleaner.py` (`--check-staging`), `pixel_luminance_guard.py` (`--mode`, `--preview-sheet`).

### 2. 🎮 [ljack-game](./ljack-game/) (v1.7.0 Commercial Edition)
* **목적**: 2D/2.5D 인디 게임, 상용 Steam/스토브 출시 패키징, 물리 시뮬레이션, 게임 루프 최적화.
* **4대 엔진 생태계 지원**:
  - **Pygame (Python)**: 60Hz 고정 틱 루프, 더미 헤드리스 가드, WebAssembly(Pygbag) 배포, 원자적 세이브.
  - **Tauri + HTML5 (Canvas/WebGL)**: 델타 누적기(Accumulator) $\Delta t=1/60$ 루프, WebAudio 제스처 언락 가드, Node/Deno 헤드리스 + DOM E2E 검증, 초경량 데스크톱 빌드 및 스테이징 필터.
  - **Godot Engine 4.x (GDScript/C#)**: `_physics_process` 물리 분리, `godot --headless` 1만 틱 러너, CanvasLayer F1 튜너.
  - **Rust + Python Hybrid**: C-ABI `ctypes` FFI 기반 초고속 Rust 60Hz 결정론적 시뮬레이션 코어 + Pygame 디스플레이/오디오 인터페이스.
* **상용 인디 게임 10대 핵심 기둥**:
  1. **고정 틱/렌더링 분리 (Fixed 60Hz Loop)**
  2. **헤드리스 1만 틱 & DOM E2E 검증** (물리·승패 불변식 + 뷰·모달·호버 검증)
  3. **입력 버퍼링 & 릴리즈 안전망**
  4. **충돌 감사, Reachability & 경제 불변식** (상점 `stock >= 1`·소프트락 0건)
  5. **게임 필, 실시간 튜너 & 서브 뷰 위생** ([F1]/[F2], `prefers-reduced-motion`, 뷰 전환 잔존 배너/툴팁 정리)
  6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**
  7. **원자적 세이브 & 경제 커밋 즉시 저장** (`os.replace`, 랜덤/경제 커밋 동기 저장 + `beforeunload` 플러시)
  8. **다국어, 아이콘 분리 & 상용 릴리즈 봉인** (`locales/`, `PRODUCTION_BUILD=True`, 앱 아이콘 vs 인게임 SVG 분리)
  9. **🎨 그래픽 실전 툴 나침반** (UI=Figma/SVG, 원화=Gemini 멀티레퍼런스/Batch 50%/SDXL 하이브리드, `#FFFFFF`/`#123466` 이원 배경, 도트=SD1.5, 효과=셰이더)
  10. **🎵 무결점 오디오 런타임 하네스** (더미 폴백, WebAudio 제스처 가드, 3-Bus 볼륨)
* **게임 툴킷**:
  - `vector_asset_builder.py`, `game_scaffolder.py`, `game_release_doctor.py` (Tauri/웹 세이브·풀블리드 아이콘·스테이징 캐시 누수 점검 포함), `localization_linter.py` (`--extract`, `--rewrite`, `--strict`), `tick_sim_runner.py`, `play_preview_launcher.py`, `web_packager.py`.

### 3. 🧩 [ljack-gamecode](./ljack-gamecode/) (v1.1.0)
* **목적**: TypeScript/ESM(`.js + JSDoc`)·HTML5(Canvas/DOM) 기반 게임 제작 시 **엄격한 계층 격리**, **계약 선행(Contract-First)**, **외부 생성형 AI 에셋 브릿지**를 강제하는 코드 아키텍처 하네스 (특정 모델에 종속되지 않는 범용 설계).
* **3대 제어 메커니즘**:
  1. **레이어 강제 격리**: `src/logic/` 내부에서 `window`, `document`, `CanvasRenderingContext2D`, `AudioContext` 등 브라우저 API 호출을 정적 린터(`scripts/layer_guard.py`, `--logic-dir`/`--view-dir` 커스텀 ESM 폴더 및 거대 파일 경고 지원)로 차단.
  2. **에셋 브릿지 자동화 (`AssetHarness` + `aiPromptHint`)**: `specs/asset_manifest.json`(또는 `assets/asset_manifest.json`)에 외부 AI 생성 도구용 영문 프롬프트 및 멀티레퍼런스/누끼 메타(`styleRef`, `characterRef`, `backdropColor`, `cutoutMode`, `forbiddenMotifs`, `rawCachePath`)를 선행 등록하고, 미준비 시 $O(1)$ 폴백 제공.
  3. **단계별 원자적 변경**: `specs/` 계약(영속 UI 메타데이터 포함) ➔ `src/logic/` 순수 로직 ➔ `src/view/` 뷰·테마 CSS·오디오 순으로 단계당 변경 파일 수 제한(DOM+테마 CSS 3파일 분할 예외 지원).

---

## 📂 모노레포 구조

```text
ljack-skill-antigravity/
├── README.md                         # [본 문서] LJack Protocol Suite 전체 안내
│
├── ljack-skill/                      # 🛠️ 범용 소프트웨어 엔지니어링 프로토콜 (v7.6.0)
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/                      # scaffolder, doctor, ux_copy, cleaner, pixel_guard
│   └── references/                   # rea_cleanroom, domain_guides, troubleshooting_playbook
│
├── ljack-game/                       # 🎮 멀티 엔진 게임 상용화 프로토콜 (v1.7.0 Commercial)
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/                      # vector_builder, scaffolder, doctor, i18n_linter, sim_runner, preview, web_packager
│   └── references/                   # rust_hybrid, audio, graphics_compass, steam, tauri, godot, game_feel, physics
│
└── ljack-gamecode/                   # 🧩 TypeScript/ESM·HTML5 계층 격리 & AI 에셋 브릿지 하네스 (v1.1.0)
    ├── SKILL.md
    ├── README.md
    ├── scripts/                      # layer_guard.py
    ├── templates/                    # SYSTEM_PROMPT.md, PROMPT_BOOTSTRAP.md
    └── references/                   # architecture_spec.md
```

---

## 🚀 설치 및 동기화 가이드

새로운 환경에서 세 스킬을 전역 스킬 폴더에 한 번에 설치하고 동기화하는 방법입니다:

### Windows (PowerShell)
```powershell
$repoUrl = "https://github.com/L-Jack-00/ljack-skill-antigravity.git"
$skillsDir = "$HOME\.gemini\config\skills"
$tempClone = "$env:TEMP\ljack-suite"

if (Test-Path $tempClone) { Remove-Item -Recurse -Force $tempClone }
git clone --depth 1 $repoUrl $tempClone

foreach ($skill in @("ljack-skill", "ljack-game", "ljack-gamecode")) {
    New-Item -ItemType Directory -Path "$skillsDir\$skill" -Force | Out-Null
    Copy-Item -Path "$tempClone\$skill\*" -Destination "$skillsDir\$skill" -Recurse -Force
}

Remove-Item -Recurse -Force $tempClone
Write-Host "[PASS] LJack Protocol Suite (ljack-skill, ljack-game, ljack-gamecode) installed!"
```

### Mac / Linux (Bash)
```bash
repoUrl="https://github.com/L-Jack-00/ljack-skill-antigravity.git"
skillsDir="$HOME/.gemini/config/skills"
tempClone="/tmp/ljack-suite"

rm -rf "$tempClone"
git clone --depth 1 "$repoUrl" "$tempClone"

for skill in ljack-skill ljack-game ljack-gamecode; do
  mkdir -p "$skillsDir/$skill"
  cp -r "$tempClone/$skill/"* "$skillsDir/$skill/"
done

rm -rf "$tempClone"
echo "[PASS] LJack Protocol Suite installed successfully!"
```

---

## 💡 호출 가이드 (슬래시 커맨드)

* **일반 소프트웨어 / 시스템 도구 / 데스크톱 GUI / 웹 API / Rust+Python / 역공학**:
  👉 **`/ljack-skill`**
* **인디 게임 / 상용 Steam 출시 / Pygame / Tauri+HTML5 / Godot Engine 4.x / Rust 게임 코어**:
  👉 **`/ljack-game`**
* **TypeScript/HTML5 계층 격리 코드 규약 / `specs/` 계약 선행 / `AssetHarness` 에셋 브릿지**:
  👉 **`/ljack-gamecode`**
