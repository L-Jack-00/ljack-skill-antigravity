# 엘잭 프로토콜 스위트 (LJack Protocol Suite)
## 범용 소프트웨어 & 멀티 엔진 인디 게임 자율 에이전틱 개발 프로토콜

[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Skills-blue.svg)](https://deepmind.google/technologies/antigravity/)
[![LJack Skill](https://img.shields.io/badge/ljack--skill-v7.8.0-green.svg)](#-1-ljack-skill-v780)
[![LJack Game](https://img.shields.io/badge/ljack--game-v1.11.0_Floating_UX-purple.svg)](#-2-ljack-game-v1110-floating-window-ux--input-continuity-edition)
[![LJack GameCode](https://img.shields.io/badge/ljack--gamecode-v1.3.0-teal.svg)](#-3-ljack-gamecode-v130)
[![Engines](https://img.shields.io/badge/Game_Engines-Pygame%20%7C%20Tauri%20%7C%20Godot%20%7C%20Rust-orange.svg)](#-2-ljack-game-v1110-floating-window-ux--input-continuity-edition)
[![Commercial Ready](https://img.shields.io/badge/Steam%20Ready-Atomic%20Save%20%7C%20Audio%20Rig%20%7C%20i18n-success.svg)](#-2-ljack-game-v1110-floating-window-ux--input-continuity-edition)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 AI 에이전트가 소프트웨어 및 게임 개발 시 기술적 결함(빌드, 테스트, 물리, 린트)을 자체 검증과 자가 치유(Self-Healing) 루프로 자율 완주하되, **스텁(Stub)·체크보드 폴백 상태로 조기 종료하지 않고 마일스톤 단위로 깊이 있게 완성**하도록 규정하는 **LJack 런타임 하네스 엔지니어링 프로토콜 모음(Suite)**입니다.  
또한 **수치·손맛·UI·연출 미세조정(Fine-Tuning)**을 요청한 경우에는 전체 적용·검증 절차를 생략하고 **실시간 슬라이더 기반 인터랙티브 샘플**을 먼저 출력하여 사용자가 값을 확정한 뒤 반영하도록 지원합니다.

개발 목적과 아키텍처 제약 수준에 맞추어 **3가지 독립 프로토콜**로 제공됩니다:

---

## 🏛️ 하위 프로토콜 안내

### 1. 🛠️ [ljack-skill](./ljack-skill/) (v7.8.0)
* **목적**: 일반 소프트웨어(CLI, 데스크톱 GUI, 웹 백엔드/프론트엔드, 자동화 도구, Rust-Python 이원화 하네스, REA 역공학 클린룸 재구축). *(게임 개발 시에는 `ljack-game`을 사용하며 중복 호출하지 않습니다.)*
* **10대 기둥 & Fast-Path**: 코어/IO 분리(Rust 코어 + Python 인터페이스 공식 지원), 슈퍼바이저 루프, 명시적 FSM, 이벤트 기반 유휴 대기, 디바운스 종료 `flush()`·오버레이 특이성·JS/TS/CSS 거대 모듈 진단, 물리 입력 자가 치유, 독자 중심 UX 카피 무결성 가드, (GUI) 풀블리드 `1024x1024` 아이콘·누끼 보색 시트(`#479be6`)·인터랙션 접근성(`aria-disabled`), **미세조정 슬라이더 샘플 우선 출력 Fast-Path**.
* **안티-스텁 원칙**: `TODO`/빈 핸들러/더미 응답 잔존 시 완료 보고 금지 및 패키징/정리 단계 후순위화.
* **번들링 도구**:
  - `harness_scaffolder.py`: 10대 기둥 표준 골격 즉시 생성 (CLI, Desktop, API, Rust-Python Hybrid 지원).
  - `harness_doctor.py`: AST 정적 분석 기반 하네스 준수율 채점(0~100) + JS/TS/CSS 거대 모듈·지연 저장 어드바이저리.
  - `ux_copy_linter.py`, `release_cleaner.py` (`--check-staging`), `pixel_luminance_guard.py` (`--mode`, `--preview-sheet`).

### 2. 🎮 [ljack-game](./ljack-game/) (v1.11.0 Floating Window UX & Input Continuity Edition)
* **목적**: 마일스톤 기반 상용 인디 게임 개발 및 Steam/스토브/itch.io 출시 패키징.
* **미세조정 Fast-Path**: 손맛·물리·VFX·UI 배치·밸런스 미세조정 요청 시 Phase 0~2 전체 적용 과정을 생략하고 `<input type="range">` 슬라이더 + 실시간 프리뷰 + JSON 복사 샘플을 우선 출력.
* **3-Phase 실행 파이프라인**:
  - **Phase 0 (볼륨 계약)**: `ROADMAP.md`에 마일스톤(M1~M4)과 적·아이템·스테이지 최소 볼륨 고정.
  - **Phase 1 (수직 슬라이스 집중 구현)**: 초기부터 `i18n`/디버그 봉인/패키징에 토큰을 소진하지 않고 코어 루프·적 AI·연출·SVG/프로시저럴 비주얼·WebAudio 깊이에 집중 (`TODO`/체크보드 폴백 방치 금지).
  - **Phase 2 (플레이어블 검수 & 상용 마감)**: `Playable Review Gate`(F1/F2 손맛 검수) ➔ `localization_linter.py --rewrite --strict` ➔ `PRODUCTION_BUILD` 봉인 ➔ `game_release_doctor.py` 80점+ & 스텁 0건 통과.
* **4대 엔진 생태계 지원**:
  - **Pygame (Python)** / **Tauri + HTML5 (Canvas/WebGL)** / **Godot Engine 4.x** / **Rust + Python Hybrid**
* **상용 인디 게임 10대 핵심 기둥**:
  1. **고정 틱/렌더링 분리 (Fixed 60Hz Loop)**
  2. **헤드리스 1만 틱 & 실제 시각 E2E 검증** (물리·승패 불변식 + DOM/OpenGL Viewport PNG 스크린샷 레이아웃 & 다중 모드 검증)
  3. **입력 버퍼링, 포커스 마스킹, 비간섭 단축키 & 릴리즈 안전망** (비차단 창 토글/`Esc` 시 이동 키 홀드 유지)
  4. **충돌 감사, Reachability, 발 스탠스 캡슐 & 틈새 낙하 역검증** (`CapsuleShape2D`, 발판 틈새 낙하, 상점 `stock >= 1`·소프트락 0건)
  5. **게임 필, 비차단 플로팅 UX, 실시간 튜너 & 전환 위생** ([F1]/[F2], `prefers-reduced-motion`, 플로팅 창 Z-Order/`Esc` LIFO·탭 레이아웃 불변·무지연 토스트, 맵 전환 시 잔존 드랍·텍스트 정리)
  6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**
  7. **원자적 세이브 & 경제 커밋 즉시 저장** (`os.replace`, 랜덤/경제 커밋 동기 저장 + `beforeunload` 플러시)
  8. **다국어(`refresh_labels()`), 아이콘 분리 & 상용 릴리즈 봉인** (`locales/`, `PRODUCTION_BUILD=True`, 앱 아이콘 vs 인게임 SVG 분리)
  9. **🎨 그래픽 실전 툴 나침반 & 하이브리드 비트맵 폰트** (UI=Figma/SVG, 원화=Gemini 멀티레퍼런스/Batch 50%/SDXL 하이브리드, `#FFFFFF`/`#123466` 이원 배경, 스프라이트-히트박스 ±1px 정렬, 다국어 폰트 폴백 체인 & 텍스트 선형 업스케일, 도트=SD1.5, 효과=셰이더, 오프라인 시 SVG/프로시저럴 실구현)
  10. **🎵 무결점 오디오 런타임 하네스** (더미 폴백, WebAudio 제스처 가드, 3-Bus 볼륨)
* **게임 툴킷**:
  - `vector_asset_builder.py`, `game_scaffolder.py`, `game_release_doctor.py` (`--phase 1|2`, 스텁/TODO 탐지, 에셋 실파일 연결률, Tauri/웹 세이브·풀블리드 아이콘·스테이징 캐시 누수 점검), `localization_linter.py`, `tick_sim_runner.py`, `play_preview_launcher.py`, `web_packager.py`.

### 3. 🧩 [ljack-gamecode](./ljack-gamecode/) (v1.3.0)
* **목적**: TypeScript/ESM(`.js + JSDoc`)·HTML5(Canvas/DOM) 기반 게임 제작 시 **계층 격리**, **계약 선행(Contract-First)**, **마일스톤 연속 완주**, **멀티모달 AI 에셋 브릿지**를 강제하는 코드 아키텍처 하네스.
* **3대 제어 메커니즘 & Fast-Path**:
  1. **레이어 강제 격리**: `src/logic/` 내부에서 `window`, `document`, `CanvasRenderingContext2D`, `AudioContext` 등 브라우저 API 호출 및 `TODO`/스텁을 `scripts/layer_guard.py --strict`로 차단.
  2. **에셋 브릿지 + 실구현 우선**: `specs/asset_manifest.json`에 `aiPromptHint` 및 누끼/참조 메타를 등록하되, 실제 파일이 디스크에 없을 때도 체크보드/비프음 폴백에만 머무르지 않고 `src/view/` 내 SVG·프로시저럴 캔버스·WebAudio 효과음을 직접 구현.
  3. **마일스톤 단위 계층 순차 완주 & 미세조정 예외**: `specs/` 계약 ➔ `src/logic/` 순수 로직 ➔ `src/view/` 뷰·오디오 ➔ 테스트 순서를 지키되, 활성 마일스톤을 한 흐름으로 완결 (단, **미세조정 요청 시**에는 전체 계층 적용을 건너뛰고 슬라이더 샘플을 우선 출력).

---

## 📂 모노레포 구조

```text
ljack-skill-antigravity/
├── README.md                         # [본 문서] LJack Protocol Suite 전체 안내
│
├── ljack-skill/                      # 🛠️ 범용 소프트웨어 엔지니어링 프로토콜 (v7.8.0)
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/                      # scaffolder, doctor, ux_copy, cleaner, pixel_guard
│   └── references/                   # rea_cleanroom, domain_guides, troubleshooting_playbook
│
├── ljack-game/                       # 🎮 멀티 엔진 게임 상용화 프로토콜 (v1.11.0)
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/                      # vector_builder, scaffolder, doctor, i18n_linter, sim_runner, preview, web_packager
│   └── references/                   # rust_hybrid, audio, graphics_compass, steam, tauri, godot, game_feel, physics
│
└── ljack-gamecode/                   # 🧩 TypeScript/ESM·HTML5 계층 격리 & AI 에셋 브릿지 하네스 (v1.3.0)
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
  👉 **`/ljack-game`** *(게임 제작 시 `ljack-skill`을 중복 호출하지 마세요)*
* **TypeScript/HTML5 계층 격리 코드 규약 / `specs/` 계약 선행 / `AssetHarness` 에셋 브릿지**:
  👉 **`/ljack-gamecode`** *(필요 시 `ljack-game`과 병행)*
