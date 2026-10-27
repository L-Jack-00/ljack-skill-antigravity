# 엘잭 게임 프로토콜 (LJack Game Protocol)
## 멀티 엔진 런타임 하네스 엔지니어링 & 초자율 에이전틱 개발 프로토콜 (v1.2.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-purple.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-1.2.0-green.svg)](#)
[![Engines](https://img.shields.io/badge/Engines-Pygame%20%7C%20Tauri%20%7C%20Godot-orange.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 게임 개발 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/도달불가/메모리)을 **헤드리스 1만 틱 시뮬레이터 및 Reachability Solver**로 무중단 자가 치유하되,  
최종 패키징 배포 전 반드시 **인게임 실시간 손맛 튜너(F1/F2 오버레이)를 통한 사용자 직접 플레이 검수 관문(Playable Review Gate)**을 거쳐 완성도를 극대화하도록 규정하는 최상위 멀티 엔진 게임 개발 프로토콜입니다.

---

## 🕹️ 지원 엔진 생태계 (3 Major Engine Ecosystems)

1. **Pygame (Python 2D / 2.5D)**:
   - 고정 60Hz 루프, `SDL_VIDEODRIVER=dummy` 헤드리스 가드, WebAssembly(Pygbag) 웹 배포.
2. **Tauri + HTML5 (Canvas / WebGL / PixiJS)**:
   - 델타 누적기(Accumulator) 기반 $\Delta t=1/60$ 고정 틱, Node.js 헤드리스 1만 틱 러너, ~10MB 초경량 네이티브 데스크톱 바이너리.
3. **Godot Engine 4.x (GDScript / C#)**:
   - `_physics_process(delta)` 물리 격리, `godot --headless` 1만 틱 검증기, CanvasLayer F1 손맛 튜너, 원클릭 크로스 플랫폼 익스포트.

---

## 📂 저장소 및 모듈 구조 (v1.2.0)

```text
ljack-game/
├── SKILL.md                          # [Fast-Path 코어] 멀티엔진 8대 기둥, 10대 강령, 6단계 파이프라인
├── README.md                         # 저장소 안내 및 검수 프로세스 다이어그램
├── scripts/                          # [내장 멀티엔진 자동화 도구]
│   ├── game_scaffolder.py            # [기둥 1 & 5] Pygame / Tauri / Godot 골격 0초 생성 (토큰 15,000개 절감)
│   ├── tick_sim_runner.py            # [기둥 2 & 4] Reachability Solver & 헤드리스 1만 틱 시뮬레이터
│   ├── play_preview_launcher.py      # [기둥 6] 엔진 자동 감지 기반 플레이 검수 브리핑 도구
│   └── web_packager.py               # [기둥 8] WebAssembly(HTML5) 브라우저 원클릭 웹 패키저
└── references/                       # [심화 게임 도메인 레퍼런스]
    ├── tauri_html5_guide.md          # Tauri + HTML5/Canvas 게임 하네스 구현 가이드
    ├── godot_engine_guide.md         # Godot 4.x GDScript 헤드리스 및 F1 튜너 가이드
    ├── game_feel_tuning.md           # 코요테 타임, 점프 버퍼링, 히트스톱 등 손맛 5대 레시피
    └── collision_and_physics.md      # AABB 충돌 및 고속 투사체 터널링 방지 서브스텝 명세
```

---

## 🏛️ 게임 런타임 하네스 엔지니어링 8대 핵심 기둥

1. **결정론적 고정 틱과 렌더링 분리 (Fixed 60Hz Loop)**: 가변 FPS 속에서도 물리 속도와 궤적이 변하지 않는 고정 틱.
2. **헤드리스 1만 틱 시뮬레이터 (Headless 10k-Tick Sim Rig)**: 화면/오디오 없이 메모리 상에서 1만 번의 틱을 0.2초 만에 검증.
3. **입력 버퍼링 & 릴리즈 안전망 (Input Buffer & Stuck Guard)**: 입력 씹힘 방지 및 게임 종료 시 키 전역 해제.
4. **충돌 감사 & Reachability Solver**: 벽 뚫림 현상 방지 서브스텝 및 도달 불가능 발판(Unwinnable Map) 수학적 사전 감지.
5. **게임 필(Game Feel) & 실시간 튜너**: 코요테 타임, 점프 선입력, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 지원.
6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**: 배포 전 사용자 직접 플레이 피드백 및 밸런스 튜닝 루프.
7. **세이브 데이터 스키마 버전 안전망 (Save State Migration)**: 세이브 포맷 변경 시 이전 데이터 자동 마이그레이션.
8. **에셋 알파 무결성 & 원클릭 배포**: WebAssembly/HTML5 웹 패키징, Tauri 10MB 바이너리, Godot CLI 빌드.
