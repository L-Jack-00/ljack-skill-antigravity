# 엘잭 게임 프로토콜 (LJack Game Protocol)
## 게임 런타임 하네스 엔지니어링 & 초자율 에이전틱 개발 프로토콜 (v1.1.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-purple.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-1.1.0-green.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 게임 개발 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/맵도달불가/무한루프)을 **헤드리스 1만 틱 시뮬레이터 및 Reachability Solver**로 무중단 자가 치유하되,  
최종 패키징 배포 전 반드시 **인게임 실시간 손맛 튜너(F1/F2 오버레이)를 통한 사용자 직접 플레이 검수 관문(Playable Review Gate)**을 거쳐 완성도를 극대화하도록 규정하는 최상위 게임 개발 프로토콜입니다.

---

## 📂 저장소 및 모듈 구조 (v1.1.0)

```text
ljack-game/
├── SKILL.md                          # [Fast-Path 코어] 게임 8대 기둥, 10대 강령, 6단계 파이프라인
├── README.md                         # 저장소 안내 및 설치/동기화 가이드
├── scripts/                          # [내장 게임 자동화 도구]
│   ├── game_scaffolder.py            # [기둥 1 & 5] Pygame 골격 및 F1 실시간 손맛 튜너 0초 생성
│   ├── tick_sim_runner.py            # [기둥 2 & 4] Reachability Solver & 헤드리스 1만 틱 시뮬레이터
│   ├── play_preview_launcher.py      # [기둥 6] 사용자 플레이 검수용 조작법 & 밸런스 파라미터 추출기
│   └── web_packager.py               # [기둥 8] WebAssembly(HTML5) 브라우저 원클릭 웹 패키저
└── references/                       # [심화 게임 도메인 레퍼런스]
    ├── game_feel_tuning.md           # 코요테 타임, 점프 버퍼링, 히트스톱 등 손맛 5대 레시피
    └── collision_and_physics.md      # AABB 충돌 및 고속 투사체 터널링 방지 서브스텝 명세
```

---

## 🏛️ 게임 런타임 하네스 엔지니어링 8대 핵심 기둥

1. **결정론적 고정 틱과 렌더링 분리 (Fixed-Tick Loop)**: 프레임 드랍에도 물리 속도가 변하지 않는 고정 60Hz 틱.
2. **헤드리스 1만 틱 시뮬레이터 (Headless 10k-Tick Sim Rig)**: 화면 없이 메모리 상에서 1만 번의 틱을 0.3초 만에 검증.
3. **입력 버퍼링 & 릴리즈 안전망 (Input Buffer & Stuck Guard)**: 입력 씹힘 방지 및 게임 종료 시 키 전역 해제.
4. **충돌 감사 & 터널링 방지 (AABB & Sub-stepping Rig)**: 벽 뚫림 현상과 모서리 걸림 원천 차단.
5. **게임 필(Game Feel) & 손맛 튜너 (Juice Rig)**: 코요테 타임, 점프 선입력, 낙하 가속, 히트스톱 기본 탑재.
6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**: 배포 전 사용자 직접 플레이 피드백 및 밸런스 튜닝 루프.
7. **세이브 데이터 스키마 버전 안전망 (Save State Migration)**: 세이브 포맷 변경 시 이전 데이터 자동 마이그레이션.
8. **에셋 알파 무결성 & 원클릭 배포 (Sprite Integrity & Packaging)**: 픽셀 투명도 검증 및 포터블 번들링.

---

## 🎮 플레이어블 검수 관문 (Playable Review Gate) 프로세스

```text
[헤드리스 1만 틱 시뮬레이션 100% ALL PASS]
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 🎮 플레이어블 검수 관문 (Playable Review Gate)              │
│ - 로컬 실행 명령어: python run_game.py                      │
│ - 현재 밸런스 파라미터 표 제출 (점프력, 중력, 속도, HP 등)  │
│ - 에이전트 질문: "손맛과 난이도를 직접 플레이해봐 주세요"   │
└─────────────────────────────┬───────────────────────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
        [수정 피드백 요청]            [플레이어 최종 승인]
               │                             │
        (파라미터 미세 튜닝)                 │
               │                             ▼
               └──────────────────────> [원클릭 패키징 배포 완결]
```
