# 엘잭 프로토콜 스위트 (LJack Protocol Suite)
## 범용 소프트웨어 & 인디 게임 초자율 에이전틱 개발 프로토콜

[![Antigravity Skills](https://img.shields.io/badge/Antigravity-Skills-blue.svg)](https://deepmind.google/technologies/antigravity/)
[![LJack Skill](https://img.shields.io/badge/ljack--skill-v7.4.0-green.svg)](#-1-ljack-skill-v740)
[![LJack Game](https://img.shields.io/badge/ljack--game-v1.1.0-purple.svg)](#-2-ljack-game-v110)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 Google Antigravity(AGY) 환경에서 AI 에이전트가 사소한 확인을 위해 멈추지 않고 자체 테스트, 무중단 자가 치유(Self-Healing), 격리 패키징, 원클릭 배포까지 단일 흐름으로 완주하도록 규정하는 **LJack 런타임 하네스 엔지니어링 프로토콜 모음(Suite)**입니다.

소프트웨어 제작과 인디 게임 제작의 도메인 특성에 맞추어 **2가지 독립 프로토콜**로 제공됩니다:

---

## 🏛️ 하위 프로토콜 안내

### 1. 🛠️ [ljack-skill](./ljack-skill/) (v7.4.0)
* **목적**: 범용 시스템 소프트웨어, 데스크톱 GUI(PyQt/WinForms), 웹 백엔드/프론트엔드, CLI 데이터 파이프라인, REA 역공학 클린룸 재구축.
* **10대 기둥**: 코어/IO 분리, 슈퍼바이저 루프, FSM, CPU 0% 동결, 물리 입력 자가 치유, UX 카피 무결성 가드, 1px 휘도 감사.
* **토큰 제로 도구**:
  - `harness_scaffolder.py`: 10대 기둥 표준 뼈대 0초 생성 (LLM 생성 토큰 12,000개 절감).
  - `harness_doctor.py`: AST 정적 분석 기반 하네스 준수율 채점(0~100) 및 3줄 핵심 진단.
  - `ux_copy_linter.py`, `release_cleaner.py`, `pixel_luminance_guard.py`.

### 2. 🎮 [ljack-game](./ljack-game/) (v1.1.0)
* **목적**: 2D 아케이드/인디 게임, 물리 시뮬레이션, 게임 루프 최적화.
* **8대 기둥**: 결정론적 60Hz 고정 틱, 헤드리스 1만 틱 시뮬레이터, 물리 터널링 방지, 입력 버퍼링, 5대 손맛 레시피(코요테 타임/점프 선입력/히트스톱).
* **⭐ 플레이어블 검수 관문 (Playable Review Gate)**:
  - 기술적 결함(충돌, 도달 불가 맵, 메모리 누수)은 1만 틱 시뮬레이터와 Reachability Solver로 100% 자가 치유.
  - 최종 패키징 배포 전 **반드시 사용자에게 직접 플레이(`python run_game.py`) 및 인게임 실시간 손맛 튜너(F1/F2 오버레이)를 제공하여 조작감을 검수**받는 6단계 파이프라인 탑재.
* **게임 툴킷**:
  - `game_scaffolder.py`: Pygame 골격 및 F1 실시간 손맛 튜너 0초 생성 (토큰 15,000개 절감).
  - `tick_sim_runner.py`: Reachability Solver(도달 불가 맵 감사) 및 헤드리스 1만 틱 시뮬레이터.
  - `play_preview_launcher.py`: 사용자 검수용 밸런스 파라미터 요약기.
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
│   └── references/                   # cleanroom, domain_guides, troubleshooting
│
└── ljack-game/                       # 🎮 게임 개발 & 플레이어블 검수 프로토콜 (v1.1.0)
    ├── SKILL.md                      # 게임 Fast-Path 코어 지침
    ├── README.md                     # ljack-game 상세 설명서
    ├── scripts/                      # game_scaffolder, tick_sim_runner, play_preview_launcher, web_packager
    └── references/                   # game_feel_tuning, collision_and_physics
```

---

## 🚀 설치 및 Antigravity 연동 가이드

새로운 컴퓨터(PC/노트북)에서 두 스킬을 Antigravity 전역 스킬 폴더에 한 번에 설치하고 동기화하는 방법입니다:

### Windows (PowerShell)
```powershell
# 1. 임시 작업 디렉토리 또는 원하는 위치에 Clone
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

* **일반 소프트웨어 / 시스템 도구 / 데스크톱 GUI / 웹 API / 역공학**:  
  👉 **`/ljack-skill`**
* **2D 인디 게임 / 아케이드 / 물리 시뮬레이션 / 게임 밸런스 검수**:  
  👉 **`/ljack-game`**
