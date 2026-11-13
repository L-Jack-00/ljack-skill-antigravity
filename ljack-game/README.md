# 엘잭 게임 프로토콜 (LJack Game Protocol)
## 멀티 엔진 런타임 하네스 & 상용 인디 게임 출시 프로토콜 (v1.6.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-purple.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-1.6.0-green.svg)](#)
[![Edition](https://img.shields.io/badge/Edition-Portability%20%26%20Commercial%20Ready-gold.svg)](#)
[![Engines](https://img.shields.io/badge/Engines-Pygame%20%7C%20Tauri%20%7C%20Godot%20%7C%20Rust-orange.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 모듈은 게임 개발 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/소프트락/메모리/오디오)을 **헤드리스 1만 틱 시뮬레이터**로 자율 검증·치유하되,  
최종 패키징 배포 전 **인게임 실시간 손맛 튜너(F1/F2 오버레이)를 통한 플레이 검수**, **상용 릴리즈 닥터(`game_release_doctor.py`)를 통한 세이브 원자성/다국어/오디오 안전망/UX카피 점검**, 그리고 **그래픽 실전 툴 나침반 및 벡터 에셋 빌더**를 완결하도록 규정하는 상용 게임 개발 프로토콜입니다.

---

## 📂 저장소 및 모듈 구조 (v1.6.0)

```text
ljack-game/
├── SKILL.md                          # [코어 지침] 멀티엔진 10대 기둥, 12대 강령, 6단계 상용화 파이프라인
├── README.md                         # 저장소 안내 및 상용 출시 프로세스
├── scripts/                          # [내장 멀티엔진 & 상용화 자동화 도구]
│   ├── vector_asset_builder.py       # [기둥 9] 초경량 SVG 카드 프레임 및 뱃지 빌더 (comic / metallic)
│   ├── game_scaffolder.py            # [기둥 1, 5, 7, 10] Pygame/Tauri/Godot/Rust 골격 + 세이브 + 오디오 즉시 생성
│   ├── game_release_doctor.py        # [기둥 7, 8, 10] 상용 출시 준비도(0~100), 오디오 안전망, UX카피 정적 진단 닥터
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

## 🏛️ 상용 인디 게임 런타임 하네스 10대 핵심 기둥

1. **결정론적 고정 틱과 렌더링 분리 (Fixed 60Hz Loop)**: 가변 FPS 속에서도 물리 속도와 궤적이 변하지 않는 고정 틱.
2. **헤드리스 1만 틱 시뮬레이터 (Headless 10k-Tick Sim Rig)**: 화면/오디오 없이 메모리 상에서 1만 틱 이상을 오프라인 고속 검증.
3. **입력 버퍼링 & 릴리즈 안전망 (Input Buffer & Stuck Guard)**: 입력 씹힘 방지 및 게임 종료 시 키 전역 해제.
4. **충돌 감사 & Reachability / 소프트락 검증**: 벽 뚫림 방지 서브스텝, 플랫포머 발판 도달성 사전 감지, 턴제/퍼즐 영구 고착 검증.
5. **게임 필(Game Feel) & 실시간 튜너**: 코요테 타임, 점프 선입력, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 지원.
6. **⭐ 플레이어블 검수 관문 (Playable Review Gate)**: 배포 전 사용자 직접 플레이 피드백 및 밸런스 튜닝 루프.
7. **세이브 데이터 원자적 안전망 (Atomic Save Rig)**: 정전/강제종료 시 세이브 파일 파손 방지 및 스팀 클라우드 호환.
8. **다국어 & 상용 릴리즈 봉인 (Commercial Release Rig)**: `locales/` 다국어 사전 탑재(`--rewrite` 자동 치환), 상용 빌드 시 F1 튜너 자동 봉인(`PRODUCTION_BUILD=True`).
9. **🎨 그래픽 실전 툴 나침반 (Game Art Toolchain Compass)**: UI/프레임(Figma/SVG) ➡️ 캐릭터 원화(SDXL) ➡️ 스프라이트(SD1.5/Aseprite) ➡️ 동적 효과(셰이더) 분업 (외부 툴 부재 시 SVG/프로시저럴 선행 구현).
10. **🎵 무결점 오디오 & 사운드 런타임 하네스 (Audio Safety Rig)**: 사운드카드 미연결 크래시 방지(더미 폴백), WebAudio 브라우저 제스처 가드, 독립 3-Bus(Master/BGM/SFX) 볼륨 및 발음수 캡 제어.

---

## 💡 개발자-AI 상용 게임 7대 마법의 검증 질문

1. **손맛/조작감**: *"점프할 때 코요테 타임이나 선입력 버퍼링이 적용되어 1프레임 차이로 조작이 씹히는 답답함이 없는가?"*
2. **세이브 안정성**: *"게임을 저장하는 찰나에 강제 종료(Alt+F4)되거나 컴퓨터가 꺼져도 이전 세이브가 손상되지 않는가?"*
3. **상용 릴리즈 봉인**: *"일반 유저에게 배포될 빌드에서 [F1] 손맛 튜너나 디버그 콘솔이 안전하게 비활성화(봉인)되어 있는가?"*
4. **오디오 안정성**: *"사운드 카드가 없거나 브라우저 오토플레이 차단 환경에서도 게임이 튕기거나 먹통 되지 않고 정상 작동하는가?"*
5. **다국어 및 독자 중심 문서화**: *"UI에 하드코딩된 문자열이 없으며, 인게임 텍스트나 코드 주석/README에 '나만 아는 변경 이력'이나 '임시 땜질 메모' 없이 처음 온 기여자나 유저가 읽기 쉬운 언어로 정제되어 있는가?"*
6. **도달 가능성 / 소프트락 방지**: *"플랫포머의 모든 발판이나 턴제/퍼즐의 모든 진행 상태가 수학적·논리적으로 클리어 가능하며 영구 고착(Softlock)이 없는가?"*
7. **플레이어블 검수 상태**: *"사용자가 지금 바로 로컬 명령어로 플레이해보고 [F1]으로 손맛을 튜닝할 수 있는가?"*
