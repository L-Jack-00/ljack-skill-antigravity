# 엘잭 프로토콜 스위트 (LJack Protocol Suite)
## 범용 소프트웨어 & 멀티 엔진 인디 게임 상용화 초자율 에이전틱 개발 프로토콜

[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Skills-blue.svg)](https://deepmind.google/technologies/antigravity/)
[![LJack Skill](https://img.shields.io/badge/ljack--skill-v7.4.0-green.svg)](#-1-ljack-skill-v740)
[![LJack Game](https://img.shields.io/badge/ljack--game-v1.5.0_Commercial-purple.svg)](#-2-ljack-game-v150-commercial-edition)
[![Engines](https://img.shields.io/badge/Game_Engines-Pygame%20%7C%20Tauri%20%7C%20Godot%20%7C%20Rust-orange.svg)](#-2-ljack-game-v150-commercial-edition)
[![Commercial Ready](https://img.shields.io/badge/Steam%20Ready-Atomic%20Save%20%7C%20Audio%20Rig%20%7C%20i18n-success.svg)](#-2-ljack-game-v150-commercial-edition)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 Google Antigravity(AGY) 환경에서 AI 에이전트가 사소한 확인을 위해 멈추지 않고 자체 테스트, 무중단 자가 치유(Self-Healing), 상용화 품질 게이트, 원클릭 배포까지 단일 흐름으로 완주하도록 규정하는 **LJack 런타임 하네스 엔지니어링 프로토콜 모음(Suite)**입니다.

소프트웨어 제작과 인디 게임 제작의 도메인 특성에 맞추어 **2가지 독립 프로토콜**로 제공됩니다:

---

## 🏛️ 하위 프로토콜 안내

### 1. 🛠️ [ljack-skill](./ljack-skill/) (v7.4.0)
* **목적**: 범용 시스템 소프트웨어, 데스크톱 GUI(PyQt/WinForms), 웹 백엔드/프론트엔드, CLI 데이터 파이프라인, Rust-Python 이원화 하네스, REA 역공학 클린룸 재구축.
* **10대 기둥**: 코어/IO 분리 (Rust 코어 + Python 인터페이스 공식 지원), 슈퍼바이저 루프, FSM, CPU 0% 동결, 물리 입력 자가 치유, UX 카피 무결성 가드, 1px 휘도 감사.
* **토큰 제로 도구**:
  - `harness_scaffolder.py`: 10대 기둥 표준 뼈대 0초 생성 (CLI, Desktop, API, Rust-Python Hybrid 지원, LLM 생성 토큰 12,000개 절감).
  - `harness_doctor.py`: AST 정적 분석 기반 하네스 준수율 채점(0~100) 및 3줄 핵심 진단.
  - `ux_copy_linter.py`, `release_cleaner.py`, `pixel_luminance_guard.py`.

### 2. 🎮 [ljack-game](./ljack-game/) (v1.5.0 Commercial Edition)
* **목적**: 2D/2.5D 인디 게임, 상용 Steam 출시 패키징, 물리 시뮬레이션, 게임 루프 최적화.
* **4대 엔진 생태계 지원**:
  - **Pygame (Python)**: 60Hz 고정 틱 루프, 더미 헤드리스 가드, WebAssembly(Pygbag) 배포, 원자적 세이브.
  - **Tauri + HTML5 (Canvas/WebGL)**: 델타 누적기(Accumulator) $\Delta t=1/60$ 루프, WebAudio 제스처 언락 가드, Node.js 헤드리스 1만 틱, ~10MB 초경량 데스크톱 EXE.
  - **Godot Engine 4.x (GDScript/C#)**: `_physics_process` 물리 분리, `godot --headless` 1만 틱 러너, CanvasLayer F1 튜너.
  - **Rust + Python Hybrid (NEW)**: C-ABI `ctypes` FFI 기반 초고속 Rust 60Hz 결정론적 시뮬레이션 코어 + Pygame 디스플레이/오디오 인터페이스.
* **상용 인디 게임 10대 핵심 기둥**:
  1. **고정 틱/렌더링 분리 (Fixed 60Hz Loop)**: 가변 FPS 속에서도 물리 속도와 궤적이 변하지 않는 고정 틱.
  2. **헤드리스 1만 틱 시뮬레이터**: 화면/오디오 없이 메모리 상에서 1만 번의 틱을 0.2초 만에 검증.
  3. **입력 버퍼링 & 릴리즈 안전망**: 프레임 드랍 시 입력 씹힘 방지 및 게임 종료 시 물리 키 전역 해제.
  4. **충돌 감사 & Reachability Solver**: 벽 뚫림 현상 방지 서브스텝 및 도달 불가능 발판 수학적 사전 감지.
  5. **게임 필 & 실시간 튜너**: 코요테 타임, 점프 선입력, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 지원.
  6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**: 배포 전 사용자 직접 플레이 피드백 수렴.
  7. **원자적 세이브(Atomic Save Rig)**: `os.replace` 기반 임시 파일 교체로 정전/강제종료 시 세이브 손상 0% 보장.
  8. **다국어 & 상용 릴리즈 봉인**: `locales/` 다국어 사전 탑재, 상용 빌드 시 F1 튜너 자동 봉인(`PRODUCTION_BUILD=True`).
  9. **🎨 그래픽 실전 툴 나침반**: UI=Figma/SVG, 원화=SDXL, 도트=SD1.5, 효과=셰이더 최적 분업 공식.
  10. **🎵 무결점 오디오 런타임 하네스**: 무음 디바이스 크래시 방지 더미 폴백, WebAudio 제스처 가드, 독립 3-Bus(Master/BGM/SFX) 볼륨 및 발음수 캡 제어.
* **게임 툴킷**:
  - `vector_asset_builder.py`: 초경량 SVG 카드 프레임 및 뱃지 빌더.
  - `game_scaffolder.py`: Pygame / Tauri / Godot / Rust_Pygame 골격 0초 생성 (토큰 15,000개 절감).
  - `game_release_doctor.py`: 상용 출시 준비도(0~100), 오디오 안전망, UX 카피 무결성 진단 닥터.
  - `localization_linter.py`: 다국어 번역 무결성 및 사전 내 개발자 은어 동시 감사기.
  - `tick_sim_runner.py`: Reachability Solver 및 헤드리스 1만 틱 초고속 시뮬레이터.
  - `play_preview_launcher.py`: 엔진 자동 감지 기반 플레이 검수 브리핑 도구.
  - `web_packager.py`: WebAssembly(HTML5) 브라우저 원클릭 웹 패키저.

---

## 📂 모노레포 구조

```text
ljack-skill-antigravity/
├── README.md                         # [본 문서] LJack Protocol Suite 전체 안내
│
├── ljack-skill/                      # 🛠️ 범용 소프트웨어 엔지니어링 프로토콜 (v7.4.0)
│   ├── SKILL.md                      # Fast-Path 코어 지침
│   ├── README.md                     # ljack-skill 상세 설명서
│   ├── scripts/                      # scaffolder, doctor, ux_copy, cleaner, pixel_guard
│   └── references/                   # cleanroom, domain_guides (Rust Hybrid 수록), troubleshooting
│
└── ljack-game/                       # 🎮 멀티 엔진 게임 상용화 프로토콜 (v1.5.0 Commercial)
    ├── SKILL.md                      # 게임 Fast-Path 코어 지침 (10대 기둥, 12대 강령)
    ├── README.md                     # ljack-game 상세 설명서
    ├── scripts/                      # vector_builder, scaffolder, doctor, i18n_linter, sim_runner, preview, web_packager
    └── references/                   # rust_hybrid_guide, audio_guide, graphics_compass, steam_guide, tauri_guide, godot_guide
```

---

## 🚀 설치 및 Antigravity 연동 가이드

새로운 컴퓨터(PC/노트북)에서 두 스킬을 Antigravity 전역 스킬 폴더에 한 번에 설치하고 동기화하는 방법입니다:

### Windows (PowerShell)
```powershell
# 1. 임시 작업 디렉토리에 Clone
$repoUrl = "https://github.com/L-Jack-00/ljack-skill-antigravity.git"
$skillsDir = "$HOME\.gemini\config\skills"
$tempClone = "$env:TEMP\ljack-suite"

if (Test-Path $tempClone) { Remove-Item -Recurse -Force $tempClone }
git clone $repoUrl $tempClone

# 2. ljack-skill과 ljack-game을 전역 skills 디렉토리에 복사
New-Item -ItemType Directory -Path "$skillsDir\ljack-skill" -Force | Out-Null
New-Item -ItemType Directory -Path "$skillsDir\ljack-game" -Force | Out-Null

Copy-Item -Path "$tempClone\ljack-skill\*" -Destination "$skillsDir\ljack-skill" -Recurse -Force
Copy-Item -Path "$tempClone\ljack-game\*" -Destination "$skillsDir\ljack-game" -Recurse -Force

Remove-Item -Recurse -Force $tempClone
Write-Host "[PASS] LJack Protocol Suite (ljack-skill & ljack-game) installed successfully!"
```

### Mac / Linux (Bash)
```bash
repoUrl="https://github.com/L-Jack-00/ljack-skill-antigravity.git"
skillsDir="$HOME/.gemini/config/skills"
tempClone="/tmp/ljack-suite"

rm -rf "$tempClone"
git clone "$repoUrl" "$tempClone"

mkdir -p "$skillsDir/ljack-skill" "$skillsDir/ljack-game"
cp -r "$tempClone/ljack-skill/"* "$skillsDir/ljack-skill/"
cp -r "$tempClone/ljack-game/"* "$skillsDir/ljack-game/"

rm -rf "$tempClone"
echo "[PASS] LJack Protocol Suite installed successfully!"
```

---

## 💡 호출 가이드 (슬래시 커맨드)

* **일반 소프트웨어 / 시스템 도구 / 데스크톱 GUI / 웹 API / Rust+Python / 역공학**:  
  👉 **`/ljack-skill`**
* **인디 게임 / 상용 Steam 출시 / Pygame / Tauri+HTML5 / Godot Engine 4.x / Rust 게임 코어**:  
  👉 **`/ljack-game`**
