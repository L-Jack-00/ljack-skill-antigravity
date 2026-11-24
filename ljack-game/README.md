# 엘잭 게임 프로토콜 (LJack Game Protocol)
## 마일스톤 기반 상용 인디 게임 개발 & 멀티 엔진 런타임 하네스 프로토콜 (v1.8.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-purple.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-1.8.0-green.svg)](#)
[![Edition](https://img.shields.io/badge/Edition-Vertical%20Slice%20%26%20Anti--Stub-gold.svg)](#)
[![Engines](https://img.shields.io/badge/Engines-Pygame%20%7C%20Tauri%20%7C%20Godot%20%7C%20Rust-orange.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 모듈은 AI 에이전트가 게임을 얕은 스캐폴드나 스텁(Stub)으로 대충 끝내지 않고, **Phase 0(스펙·볼륨 계약) ➔ Phase 1(마일스톤 수직 슬라이스 반복 구현·시뮬레이션/시각 검증) ➔ Phase 2(플레이어블 검수·상용 릴리즈 닥터 마감)** 순서로 깊이 있게 완주하도록 설계된 상용 인디 게임 개발 프로토콜입니다.

> **스킬 조합 안내**: 게임 개발 시 일반 소프트웨어용 `ljack-skill`은 중복 로드하지 마십시오 (`ljack-game`에 핵심 하네스 규율이 통합되어 있습니다). TypeScript/ESM·HTML5 계층 격리가 필요할 때만 `ljack-gamecode`를 보조 아키텍처 가드로 병행합니다.

---

## 📂 저장소 및 모듈 구조 (v1.8.0)

```text
ljack-game/
├── SKILL.md                          # [코어 지침] Phase 분리 파이프라인, 안티-스텁 규율, 10대 기둥
├── README.md                         # 저장소 안내 및 마일스톤 개발 프로세스
├── scripts/                          # [내장 멀티엔진 & 상용화 자동화 도구]
│   ├── vector_asset_builder.py       # [기둥 9] 초경량 SVG 카드 프레임 및 뱃지 빌더 (comic / metallic)
│   ├── game_scaffolder.py            # [기둥 1, 5, 7, 10] Pygame/Tauri/Godot/Rust 골격 + 세이브 + 오디오 즉시 생성
│   ├── game_release_doctor.py        # [기둥 7, 8, 10] 상용 출시 준비도(0~100), 스텁/에셋 탐지, UX카피 정적 진단 닥터
│   ├── localization_linter.py        # [기둥 8, UX] 다국어(i18n) 무결성 검사, --rewrite 자동 치환, --strict CI 게이트
│   ├── tick_sim_runner.py            # [기둥 2 & 4] Reachability Solver & 헤드리스 1만 틱 고속 시뮬레이터
│   ├── play_preview_launcher.py      # [기둥 6] 엔진 자동 감지 기반 플레이 검수 브리핑 도구
│   └── web_packager.py               # [기둥 8] WebAssembly(HTML5) 브라우저 웹 프리뷰 패키저
└── references/                       # [심화 게임 도메인 & 상용 출시 레퍼런스]
    ├── rust_hybrid_game_guide.md     # [기둥 1] Rust 60Hz 결정론적 코어 & Pygame C-ABI FFI 연동
    ├── audio_runtime_harness_guide.md# [기둥 10] 무음 디바이스 크래시 방지, WebAudio 제스처 가드, 3-Bus 볼륨 공식
    ├── game_graphics_toolchain_guide.md # [기둥 9] 상황별 툴 선정(UI=SVG, 원화=SDXL, 도트=SD1.5, 효과=셰이더) 가이드
    ├── steam_publishing_guide.md     # 스팀 상용 출시, 원자적 세이브, Steamworks SDK, 스팀덱 대응
    ├── tauri_html5_guide.md          # Tauri + HTML5/Canvas 게임 하네스 구현 가이드
    ├── godot_engine_guide.md         # Godot 4.x GDScript 헤드리스 및 F1 튜너 가이드
    ├── game_feel_tuning.md           # 코요테 타임, 점프 버퍼링, 히트스톱 등 손맛 5대 레시피
    └── collision_and_physics.md      # AABB 충돌 및 고속 투사체 터널링 방지 서브스텝 명세
```

---

## 🏛️ 3-Phase 실행 흐름 & 10대 핵심 기둥

1. **Phase 0 (볼륨 계약)**: `ROADMAP.md`에 마일스톤(M1~M4)과 적·스킬·스테이지 최소 볼륨을 못 박습니다.
2. **Phase 1 (코어 & 콘텐츠 집중)**: 출시 막판 QA(`i18n`, 디버그 봉인, 패키징)를 미루고, 고정 60Hz 루프·입력 버퍼링·적 AI·연출·SVG/프로시저럴 비주얼·WebAudio를 마일스톤 단위로 깊게 구현하고 1만 틱 + 화면/E2E 검증으로 자가 치유합니다.
3. **Phase 2 (상용화 마감)**: `Playable Review Gate`(F1/F2 손맛 검수) ➔ 다국어 치환(`--rewrite --strict`) ➔ 원자적 세이브/플러시 ➔ `PRODUCTION_BUILD` 봉인 ➔ `game_release_doctor.py` 80점+ & 스텁 0건 통과.

### 10대 핵심 기둥 요약
1. **결정론적 고정 틱과 렌더링 분리 (Fixed 60Hz Loop)**
2. **헤드리스 1만 틱 & DOM E2E 시뮬레이터**
3. **입력 버퍼링 & 릴리즈 안전망 (Input Buffer & Stuck Guard)**
4. **충돌 감사 & Reachability / 소프트락 검증**
5. **게임 필(Game Feel) & 실시간 튜너 ([F1]/[F2])**
6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**
7. **세이브 데이터 원자적 안전망 (Atomic Save & 즉시 커밋)**
8. **다국어 & 상용 릴리즈 봉인 (Commercial Release Rig)**
9. **🎨 그래픽 실전 툴 나침반 & SVG/프로시저럴 실구현**
10. **🎵 무결점 오디오 & 사운드 런타임 하네스 (Audio Safety Rig)**
