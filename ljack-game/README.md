# 엘잭 게임 프로토콜 (LJack Game Protocol)
## 멀티 엔진 런타임 하네스 & 상용 인디 게임 출시 프로토콜 (v1.3.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-purple.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-1.3.0-green.svg)](#)
[![Edition](https://img.shields.io/badge/Edition-Commercial%20Ready-gold.svg)](#)
[![Engines](https://img.shields.io/badge/Engines-Pygame%20%7C%20Tauri%20%7C%20Godot-orange.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 게임 개발 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/도달불가/메모리)을 **헤드리스 1만 틱 시뮬레이터 및 Reachability Solver**로 무중단 자가 치유하되,  
최종 패키징 배포 전 **인게임 실시간 손맛 튜너(F1/F2 오버레이)를 통한 플레이 검수** 및 **상용 릴리즈 닥터(`game_release_doctor.py`)를 통한 세이브 원자성/다국어/디버그 봉인 점검**을 완결하도록 규정하는 최상위 상용 게임 개발 프로토콜입니다.

---

## 📂 저장소 및 모듈 구조 (v1.3.0 Commercial Edition)

```text
ljack-game/
├── SKILL.md                          # [Fast-Path 코어] 멀티엔진 8대 기둥, 10대 강령, 6단계 상용화 파이프라인
├── README.md                         # 저장소 안내 및 상용 출시 프로세스 다이어그램
├── scripts/                          # [내장 멀티엔진 & 상용화 자동화 도구]
│   ├── game_scaffolder.py            # [기둥 1, 5, 7] Pygame/Tauri/Godot 골격 + 세이브 + 다국어 0초 생성
│   ├── game_release_doctor.py        # [신설] 상용 출시 준비도(0~100) 및 스팀/스토브 승인 게이트 진단 닥터
│   ├── localization_linter.py        # [신설] 다국어(i18n) 번역 무결성 검증 및 하드코딩 텍스트 추출기
│   ├── tick_sim_runner.py            # [기둥 2 & 4] Reachability Solver & 헤드리스 1만 틱 시뮬레이터
│   ├── play_preview_launcher.py      # [기둥 6] 엔진 자동 감지 기반 플레이 검수 브리핑 도구
│   └── web_packager.py               # [기둥 8] WebAssembly(HTML5) 브라우저 원클릭 웹 패키저
└── references/                       # [심화 게임 도메인 & 상용 출시 레퍼런스]
    ├── steam_publishing_guide.md     # [신설] 스팀 상용 출시, 원자적 세이브, Steamworks SDK, 스팀덱 대응
    ├── tauri_html5_guide.md          # Tauri + HTML5/Canvas 게임 하네스 구현 가이드
    ├── godot_engine_guide.md         # Godot 4.x GDScript 헤드리스 및 F1 튜너 가이드
    ├── game_feel_tuning.md           # 코요테 타임, 점프 버퍼링, 히트스톱 등 손맛 5대 레시피
    └── collision_and_physics.md      # AABB 충돌 및 고속 투사체 터널링 방지 서브스텝 명세
```

---

## 🏛️ 상용 인디 게임 런타임 하네스 8대 핵심 기둥

1. **결정론적 고정 틱과 렌더링 분리 (Fixed 60Hz Loop)**: 가변 FPS 속에서도 물리 속도와 궤적이 변하지 않는 고정 틱.
2. **헤드리스 1만 틱 시뮬레이터 (Headless 10k-Tick Sim Rig)**: 화면/오디오 없이 메모리 상에서 1만 번의 틱을 0.2초 만에 검증.
3. **입력 버퍼링 & 릴리즈 안전망 (Input Buffer & Stuck Guard)**: 입력 씹힘 방지 및 게임 종료 시 키 전역 해제.
4. **충돌 감사 & Reachability Solver**: 벽 뚫림 현상 방지 서브스텝 및 도달 불가능 발판(Unwinnable Map) 수학적 사전 감지.
5. **게임 필(Game Feel) & 실시간 튜너**: 코요테 타임, 점프 선입력, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 지원.
6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**: 배포 전 사용자 직접 플레이 피드백 및 밸런스 튜닝 루프.
7. **세이브 데이터 원자적 안전망 (Atomic Save Rig)**: 정전/강제종료 시 0바이트 세이브 파손 방지 및 스팀 클라우드 호환.
8. **다국어 & 상용 릴리즈 봉인 (Commercial Release Rig)**: `locales/` 다국어 사전 탑재, 상용 빌드 시 F1 튜너 자동 봉인(`PRODUCTION_BUILD=True`), 원클릭 스팀/웹/데스크톱 배포.
