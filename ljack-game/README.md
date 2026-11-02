# 엘잭 게임 프로토콜 (LJack Game Protocol)
## 멀티 엔진 런타임 하네스 & 상용 인디 게임 출시 프로토콜 (v1.5.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-purple.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-1.5.0-green.svg)](#)
[![Edition](https://img.shields.io/badge/Edition-Audio%20Safety%20%26%20Commercial%20Ready-gold.svg)](#)
[![Engines](https://img.shields.io/badge/Engines-Pygame%20%7C%20Tauri%20%7C%20Godot%20%7C%20Rust-orange.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 게임 개발 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/도달불가/메모리/오디오)을 **헤드리스 1만 틱 시뮬레이터 및 Reachability Solver**로 무중단 자가 치유하되,  
최종 패키징 배포 전 **인게임 실시간 손맛 튜너(F1/F2 오버레이)를 통한 플레이 검수**, **상용 릴리즈 닥터(`game_release_doctor.py`)를 통한 세이브 원자성/다국어/오디오 안전망/UX카피 점검**, 그리고 **그래픽 실전 툴 나침반 및 벡터 에셋 빌더**를 완결하도록 규정하는 최상위 상용 게임 개발 프로토콜입니다.

---

## 📂 저장소 및 모듈 구조 (v1.5.0 Audio Safety Edition)

```text
ljack-game/
├── SKILL.md                          # [Fast-Path 코어] 멀티엔진 10대 기둥, 12대 강령, 6단계 상용화 파이프라인
├── README.md                         # 저장소 안내 및 상용 출시 프로세스 다이어그램
├── scripts/                          # [내장 멀티엔진 & 상용화 자동화 도구]
│   ├── vector_asset_builder.py       # [기둥 9] 초경량 SVG 카드 프레임 및 뱃지 빌더 (comic / metallic)
│   ├── game_scaffolder.py            # [기둥 1, 5, 7, 10] Pygame/Tauri/Godot/Rust 골격 + 세이브 + 오디오 0초 생성
│   ├── game_release_doctor.py        # [기둥 7, 8, 10] 상용 출시 준비도(0~100), 오디오 안전망, UX카피 정적 진단 닥터
│   ├── localization_linter.py        # [기둥 8, UX] 다국어(i18n) 번역 무결성 및 사전 내 개발자 은어 동시 감사기
│   ├── tick_sim_runner.py            # [기둥 2 & 4] Reachability Solver & 헤드리스 1만 틱 초고속 시뮬레이터
│   ├── play_preview_launcher.py      # [기둥 6] 엔진 자동 감지 기반 플레이 검수 브리핑 도구
│   └── web_packager.py               # [기둥 8] WebAssembly(HTML5) 브라우저 원클릭 웹 패키저
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

## 🏛️ 상용 인디 게임 런타임 하네스 10대 핵심 기둥

1. **결정론적 고정 틱과 렌더링 분리 (Fixed 60Hz Loop)**: 가변 FPS 속에서도 물리 속도와 궤적이 변하지 않는 고정 틱.
2. **헤드리스 1만 틱 시뮬레이터 (Headless 10k-Tick Sim Rig)**: 화면/오디오 없이 메모리 상에서 1만 번의 틱을 0.2초 만에 검증.
3. **입력 버퍼링 & 릴리즈 안전망 (Input Buffer & Stuck Guard)**: 입력 씹힘 방지 및 게임 종료 시 키 전역 해제.
4. **충돌 감사 & Reachability Solver**: 벽 뚫림 현상 방지 서브스텝 및 도달 불가능 발판(Unwinnable Map) 수학적 사전 감지.
5. **게임 필(Game Feel) & 실시간 튜너**: 코요테 타임, 점프 선입력, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 지원.
6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**: 배포 전 사용자 직접 플레이 피드백 및 밸런스 튜닝 루프.
7. **세이브 데이터 원자적 안전망 (Atomic Save Rig)**: 정전/강제종료 시 0바이트 세이브 파손 방지 및 스팀 클라우드 호환.
8. **다국어 & 상용 릴리즈 봉인 (Commercial Release Rig)**: `locales/` 다국어 사전 탑재, 상용 빌드 시 F1 튜너 자동 봉인(`PRODUCTION_BUILD=True`), 원클릭 스팀/웹/데스크톱 배포.
9. **🎨 그래픽 실전 툴 나침반 (Game Art Toolchain Compass)**: UI/프레임(Figma/SVG) ➡️ 캐릭터 원화(SDXL) ➡️ 스프라이트(SD1.5/Aseprite) ➡️ 동적 효과(셰이더) 최적 분업.
10. **🎵 무결점 오디오 & 사운드 런타임 하네스 (Audio Safety Rig)**: 사운드카드 미연결 크래시 방지(더미 폴백), WebAudio 브라우저 제스처 가드, 독립 3-Bus(Master/BGM/SFX) 볼륨 및 발음수 캡 제어.

---

## 💡 개발자-AI 상용 게임 7대 마법의 검증 질문

1. **손맛/조작감**: *"점프할 때 코요테 타임이나 선입력 버퍼링이 적용되어 1프레임 차이로 조작이 씹히는 답답함이 없는가?"*
2. **세이브 안정성**: *"게임을 저장하는 찰나에 강제 종료(Alt+F4)되거나 컴퓨터가 꺼져도 이전 세이브가 손상되지 않는가?"*
3. **상용 릴리즈 봉인**: *"일반 유저에게 배포될 빌드에서 [F1] 손맛 튜너나 디버그 콘솔이 안전하게 비활성화(봉인)되어 있는가?"*
4. **오디오 안정성**: *"사운드 카드가 없거나 브라우저 오토플레이 차단 환경에서도 게임이 튕기거나 먹통 되지 않고 정상 작동하는가?"*
5. **다국어 및 UX 카피**: *"UI에 하드코딩된 문자열이 없으며, 인게임 텍스트나 번역 사전에 개발자 은어(하네스, 히트박스, 틱)가 섞여있지 않은가?"*
6. **도달 가능성(Reachability)**: *"맵의 모든 플랫폼이 현재 플레이어의 점프력으로 수학적으로 100% 도달 가능한가?"*
7. **플레이어블 검수 상태**: *"사용자가 지금 바로 로컬 명령어로 플레이해보고 [F1]으로 손맛을 튜닝할 수 있는가?"*
