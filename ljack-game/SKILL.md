---
name: ljack-game
description: >-
  엘잭 게임 프로토콜 (LJack Game Protocol): 멀티 엔진 런타임 하네스 엔지니어링 및 상용 인디 게임 개발 프로토콜 (v1.6.0).
  사용자가 '엘잭 게임', '게임 개발', '인디 게임', '게임 하네스', '상용화', '스팀 출시', 'Pygame', 'Tauri', 'HTML5 캔버스', '고도 엔진', 'Godot', 'Rust', 'Rust+Python' 등을 요청하거나,
  결정론적 고정 틱 루프, 헤드리스 1만 틱 시뮬레이터, 사용자 플레이 검수 관문(Playable Review Gate),
  인게임 실시간 손맛 튜너(F1/F2 오버레이), 원자적 세이브(Atomic Save), 다국어(i18n) 현지화 및 자동 치환, 상용 릴리즈 닥터,
  그래픽 툴 나침반(UI 벡터, SDXL 일러스트, 도트 스프라이트, 셰이더 이펙트), 오디오 런타임 하네스(WebAudio 제스처 가드, 3-Bus 볼륨, 무음 디바이스 폴백),
  스팀/스토브/itch.io 상용 출시 파이프라인을 원할 때 활성화합니다.
---

# 엘잭 게임 스킬 (LJack Game Protocol)
## 멀티 엔진 런타임 하네스 & 상용 인디 게임 출시 프로토콜 (v1.6.0)

> **💡 시스템 지침 (System Directive)**:  
> 본 스킬은 인디 게임 제작 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/메모리/오디오)을 헤드리스 1만 틱 시뮬레이터로 자율 검증·해결하되,  
> **1) 배포 전 사용자 직접 플레이 검수(Playable Review Gate)를 통한 손맛 조율**,  
> **2) 상용 릴리즈 닥터(`game_release_doctor.py`)를 통한 세이브 원자성/다국어/오디오 안전망/UX카피/디버그 봉인 점검**,  
> **3) 그래픽 종류별 실전 툴 나침반(`references/game_graphics_toolchain_guide.md`)을 통한 경량 에셋 구축(외부 툴 미보유 시 SVG/프로시저럴 폴백)**,  
> **4) 무결점 오디오 런타임 하네스(`references/audio_runtime_harness_guide.md`)를 통한 크래시 없는 사운드 파이프라인**을 완결하도록 규정하는 최상위 게임 개발 프로토콜입니다.

> **⚠️ 버전 독립성 불변 원칙 (Version Independence Principle)**:  
> **본 프로토콜의 버전(v1.6.0)과 대상 게임의 자체 버전은 완전히 별개입니다.**  
> 대상 게임은 사용자가 명시한 버전 또는 표준 SemVer 기본값(`v0.1.0` / `v1.0.0`)부터 온전히 독립적인 생명주기를 갖습니다.

---

## 1. 멀티 엔진 게임 런타임 하네스 10대 핵심 기둥

```text
[입력 디바이스: 키보드/마우스/게임패드] ──> [입력 버퍼 큐 & Stuck 방지 가드]
                                                         │
┌────────────────────────────────────────────────────────▼──────────────────────────────┐
│        게임 런타임 하네스 코어 (Pygame / Tauri+HTML5 / Godot 4.x / Rust+Python Hybrid) │
│                                                                                       │
│  1. 결정론적 고정 틱과 렌더링 분리 (Fixed 60Hz: Pygame Dummy / Accumulator / Rust FFI) │
│  2. 헤드리스 1만 틱 시뮬레이터 (Headless 10k-Tick Sim Rig: 승패/불변식/안정성 검증)  │
│  3. 입력 버퍼링 & 안전망 (Input Buffering, Coyote Time, 전역 키 릴리즈 가드)          │
│  4. 충돌 감사 & Reachability Solver (AABB/서브스텝/플랫포머 도달성 및 턴제 데드락)   │
│  5. 게임 필 & 실시간 튜너 (F1 인게임 오버레이 실시간 조절 & F2 디스크 핫저장)        │
│  6. ⭐ 플레이어블 검수 관문 (Playable Review Gate: 배포 전 사용자 직접 플레이 피드백) │
│  7. 세이브 데이터 원자적 안전망 (Atomic Save Rig: 저장 중 강제종료 시 파손 방지)     │
│  8. 다국어 & 상용 릴리즈 봉인 (Production Seal, i18n, Steam/Tauri/Godot 배포 준비)    │
│  9. 🎨 그래픽 실전 툴 나침반 (UI=벡터/SVG, 일러스트=SDXL, 도트=SD1.5, 효과=셰이더)   │
│ 10. 🎵 무결점 오디오 런타임 하네스 (Audio Safety: 더미 폴백, WebAudio 가드, 3-Bus)   │
└────────────────────────────────────────────────────────┬──────────────────────────────┘
                                                         │
         [검증 ALL PASS ➔ 사용자 플레이 검수 ➔ 상용 닥터 감사 ➔ 릴리즈 봉인]
```

- **기둥 1: 고정 틱과 렌더링 분리**: Pygame Dummy 가드, Tauri Accumulator 루프, Godot `_physics_process`, Rust 코어 + Python FFI 이원화 분리 (TypeScript/HTML5에서 엄격한 파일 계층 격리가 필요할 경우 `/ljack-gamecode` 규약과 함께 운용 가능).
- **기둥 2: 헤드리스 1만 틱 시뮬레이터**: 렌더링 없이 1만 틱 이상을 오프라인으로 고속 실행해 무한 루프, NaN 오염, 메모리 누수, 승패 불변식을 검증.
- **기둥 3: 입력 버퍼링 & 안전망**: 프레임 드랍 시 입력 씹힘 방지 및 게임 종료 시 물리 입력 해제.
- **기둥 4: 충돌 감사 & Reachability Solver**:
  - 플랫포머/액션: 투사체 관통 방지 서브스텝 및 도달 불가능 발판(`tick_sim_runner.py`) 수학적 사전 감지.
  - 턴제/카드(TCG)/퍼즐: 드로우·자원 고갈, 턴 무한 루프 등 도메인별 소프트락(Softlock) 0건 시뮬레이션 검증.
- **기둥 5: 게임 필(Game Feel) & 실시간 튜너**: 코요테 타임, 점프 선입력 버퍼, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 지원.
- **기둥 6: 플레이어블 검수 관문 (Playable Review Gate)**:
  - 배포 전 사용자에게 로컬 실행 명령과 밸런스 파라미터 요약표를 제출하고 직접 손맛 검수 수렴.
- **기둥 7: 세이브 데이터 원자적 안전망 (Atomic Save Rig)**:
  - 임시 파일 쓰기 및 `os.replace` 원자적 교체로 충돌/정전 시 세이브 파일 깨짐(Corruption) 방어.
- **기둥 8: 다국어 & 상용 릴리즈 봉인 (Commercial Release Rig)**:
  - `locales/` 다국어 사전 탑재, 상용 빌드 시 `F1` 손맛 튜너 자동 봉인(`PRODUCTION_BUILD=True`), **독자 중심 문서화(README/주석 내 변경점 찌꺼기 배제)**, 스팀/웹/데스크톱 배포 패키징 지원 (스팀 AppID 및 SDK 연동은 개발자 자격 정보 제공 시 활성화).
- **기둥 9: 🎨 그래픽 실전 툴 나침반 (Game Art Toolchain Compass)**:
  - UI/프레임/뱃지는 **Figma / SVG 벡터**로 가볍고 깨짐 없게 구축 (내장 `scripts/vector_asset_builder.py` 즉시 활용 가능).
  - 캐릭터/배경 원화는 **SDXL 1.0 + ComfyUI**로 가운데 일러스트에만 분리 투입.
  - 2D 도트 스프라이트는 **SD 1.5 + Pixel LoRA ➡️ Aseprite**로 격자 통일.
  - 회전/발광 이펙트는 **게임 엔진 2D 셰이더**로 경량 동적 구현.
  - *외부 이미지 생성 툴이 없는 로컬 코딩 환경에서는 SVG/프로시저럴 플레이스홀더와 에셋 ID 분리 구조로 우선 구현한 뒤 추후 최종 아트로 교체합니다.*
- **기둥 10: 🎵 무결점 오디오 & 사운드 런타임 하네스 (Audio Safety & Sound Rig)**:
  - 사운드카드 미연결/헤드리스 환경 크래시 방지(Pygame 더미 오디오 폴백).
  - 웹 브라우저(Tauri/HTML5) 오토플레이 차단 해제(User Gesture Unlock Guard).
  - 독립 3계층 볼륨 버스(Master / BGM / SFX) 및 부드러운 페이드 트랜지션.
  - 동시 발음수(Voice Polyphony) 제어로 디스토션 음압 방어.

---

## 2. 자율 게임 에이전트 12대 실행 강령

1. **버전 독립성 준수**: 게임 프로토콜 버전(v1.6.0)과 대상 게임 고유 버전(`v0.1.0`)을 분리한다.
2. **엔진 생태계 적응력**: Pygame, Tauri/HTML5, Godot 4.x, Rust+Python Hybrid 중 사용자가 요청한 스택의 표준 하네스를 즉각 구축한다.
3. **기술 결함은 무중단 자가 치유한다**: 충돌 버그, 맵 차단, 무한 루프는 사용자에게 묻지 않고 헤드리스 시뮬레이션 러너로 스스로 해결한다.
4. **손맛과 재미는 반드시 사용자에게 검수받는다 (Playable Review Gate)**: 배포 전 로컬 실행 스크립트와 밸런스 수치 요약표를 사용자에게 제출하고 직접 플레이 검수를 요청한다.
5. **세이브 데이터 원자성 사수**: 세이브 루틴은 반드시 원자적 교체(`os.replace`) 패턴을 적용하여 저장 중 손상을 방지한다.
6. **상용 빌드 디버그 봉인 의무화**: 배포 전 `PRODUCTION_BUILD` 플래그로 `[F1]` 튜너 및 개발자 치트를 봉인한다.
7. **하드코딩 텍스트 금지 및 자동 치환 (i18n 준수)**: UI와 안내 메시지는 `locales/en.json`, `locales/ko.json` 딕셔너리로 분리하며, `scripts/localization_linter.py --rewrite`를 통해 하드코딩된 리터럴을 `t("KEY")`로 원본 소스 코드에 인플레이스 자동 치환한다.
8. **🎨 그래픽 종류별 실전 툴 나침반 준수**: UI=벡터/SVG, 원화=SDXL, 도트=SD1.5, 효과=셰이더로 분업하되, 외부 생성 도구가 없는 환경에서는 내장 SVG 빌더 및 프로시저럴 플레이스홀더로 선행 구현한다.
9. **🎵 오디오 하네스 무결성 사수**: 무사운드 환경 크래시 방지 더미 폴백, 웹 오토플레이 해제 가드, 3-Bus 볼륨 분리를 적용한다.
10. **사용자 표면 UX 카피 & 독자 중심 문서화 준수 (LJack Skill 연계)**: 인게임 UI 레이블/다국어 사전/웹 패키저 출력물에서 내부 개발 용어(`ljack`, `하네스` 등) 노출을 차단하고, 코드 주석과 README에서 'vX.X 버그 픽스', '임시 땜질' 등 시점 의존 메모를 배제해 게이머/협업자 관점의 목적성 설명만 기술한다.
11. **보일러플레이트 제로 스캐폴더 활용**: `scripts/game_scaffolder.py`를 호출하여 초기 10대 기둥 골격을 즉시 생성한다.
12. **상용 릴리즈 닥터 전수 검사**: 최종 릴리즈 전 `scripts/game_release_doctor.py` 80점 이상 획득을 검증한다.

---

## 3. 개발자-AI 상용 게임 페어 프로그래밍 7대 마법의 검증 질문

1. **손맛/조작감**: *"점프할 때 코요테 타임이나 선입력 버퍼링이 적용되어 1프레임 차이로 조작이 씹히는 답답함이 없는가?"*
2. **세이브 안정성**: *"게임을 저장하는 찰나에 강제 종료(Alt+F4)되거나 컴퓨터가 꺼져도 이전 세이브가 손상되지 않는가?"*
3. **상용 릴리즈 봉인**: *"일반 유저에게 배포될 빌드에서 [F1] 손맛 튜너나 디버그 콘솔이 안전하게 비활성화(봉인)되어 있는가?"*
4. **오디오 안정성**: *"사운드 카드가 없거나 브라우저 오토플레이 차단 환경에서도 게임이 튕기거나 먹통 되지 않고 정상 작동하는가?"*
5. **다국어 및 독자 중심 문서화**: *"UI에 하드코딩된 문자열이 없으며, 인게임 텍스트나 코드 주석/README에 '나만 아는 변경 이력'이나 '임시 땜질 메모' 없이 처음 온 기여자나 유저가 읽기 쉬운 언어로 정제되어 있는가?"*
6. **도달 가능성 / 소프트락 방지**: *"플랫포머의 모든 발판이나 턴제/퍼즐의 모든 진행 상태가 수학적·논리적으로 클리어 가능하며 영구 고착(Softlock)이 없는가?"*
7. **플레이어블 검수 상태**: *"사용자가 지금 바로 로컬 명령어로 플레이해보고 [F1]으로 손맛을 튜닝할 수 있는가?"*

---

## 4. 상용 게임 자율 실행 6단계 표준 파이프라인

```text
[1단계: 게임 기획 승인 & 멀티엔진 표준 스캐폴딩]
  - 엔진 스택 결정 ➔ scripts/game_scaffolder.py 호출 (세이브 매니저, 다국어, 오디오 하네스 탑재)
       ↓
[2단계: 헤드리스 1만 틱 시뮬레이터 & 도달성/불변식 검증 구축]
  - 메모리 상에서 고속으로 물리/상태 전이와 도메인 불변식(발판 도달성/소프트락)을 검증하는 10k-Tick 러너 구축
       ↓
[3단계: 게임 메카닉, 입력 버퍼 및 렌더링/손맛/오디오 구현]
  - Fixed 60Hz 루프, 코요테 타임, 점프 선입력, F1 실시간 튜너 오버레이, 3-Bus 볼륨 탑재
       ↓
[4단계: 무중단 헤드리스 자가 치유 루프]
  - scripts/tick_sim_runner.py 가동 ➔ 1만 틱 시뮬레이션 ALL PASS (터널링 0건, 맵 도달불가/소프트락 0건)
       ↓
[5단계: ⭐ 플레이어블 프리뷰 & 사용자 검수 관문 (Playable Review Gate)]
  - scripts/play_preview_launcher.py로 조작법 및 밸런스 파라미터 요약 추출
  - 🎮 사용자에게 플레이 검수 요청: "인게임에서 [F1]으로 손맛을 실시간 조절하고 [F2]로 저장할 수 있습니다"
  - 🔄 사용자 피드백 즉시 수렴 ➔ 사용자 최종 승인(Approved) 획득
       ↓
[6단계: 상용 릴리즈 닥터 검증 & 프로덕션 봉인 배포 완결]
  - scripts/game_release_doctor.py 검사 (80점 이상 통과) ➔ localization_linter --strict 통과 ➔ F1 튜너 봉인 ➔ 배포 패키징
```

---

## 5. 내장 자동화 도구 및 참조 레퍼런스

### 🛠️ 내장 스크립트 도구 (`scripts/`)
- `scripts/vector_asset_builder.py`: 초경량 SVG 카드 프레임 및 뱃지 빌더 (comic 카툰풍 / metallic 메탈릭풍 지원).
- `scripts/game_scaffolder.py`: Pygame, Tauri, Godot, Rust+Python Hybrid 10대 기둥 골격 즉시 생성.
- `scripts/game_release_doctor.py`: 상용 출시 준비도(0~100), 오디오 안전망, UX 카피 무결성 및 스토어 승인 게이트 정적 진단 닥터.
- `scripts/localization_linter.py`: 다국어(i18n) 번역 무결성 감사, `--strict` CI 게이트, `--rewrite` 기반 원본 소스 코드 인플레이스 자동 치환(`t("KEY")`) 및 런타임 헬퍼 스캐폴딩 도구.
- `scripts/tick_sim_runner.py`: Reachability Solver 및 헤드리스 1만 틱 고속 시뮬레이터.
- `scripts/play_preview_launcher.py`: 엔진 자동 감지 기반 플레이 검수 브리핑 도구.
- `scripts/web_packager.py`: WebAssembly(HTML5) 브라우저 웹 프리뷰 패키저.

### 📚 심화 참조 레퍼런스 (`references/`)
- [Rust 코어 + Python 인터페이스 이원화 가이드](references/rust_hybrid_game_guide.md): Rust 60Hz 결정론적 시뮬레이션 & Pygame ctypes C-ABI 연동.
- [오디오 & 사운드 런타임 하네스 가이드](references/audio_runtime_harness_guide.md): 무음 디바이스 크래시 방지, WebAudio 제스처 가드, 3-Bus 볼륨 공식.
- [게임 그래픽 종류별 실전 툴 나침반 & 구축 가이드](references/game_graphics_toolchain_guide.md): 상황별 툴 선정(UI=Figma/SVG, 원화=SDXL, 도트=SD1.5, 효과=셰이더) 및 실전 구축법.
- [스팀(Steam) 상용 출시 및 스팀웍스 연동 가이드](references/steam_publishing_guide.md): 원자적 세이브, Steamworks SDK, 스팀덱 최적화.
- [Tauri + HTML5/Canvas 게임 하네스 가이드](references/tauri_html5_guide.md): Accumulator 고정 틱, Node 헤드리스 테스트, Tauri 배포.
- [고도 엔진 (Godot 4.x) 게임 하네스 가이드](references/godot_engine_guide.md): _physics_process 분리, `--headless` 1만 틱, CanvasLayer F1 튜너.
- [게임 필(Game Feel) & 손맛 튜닝 가이드](references/game_feel_tuning.md): 코요테 타임, 점프 버퍼링, 히트스톱 공식.
- [충돌 판정 및 물리 터널링 방지 가이드](references/collision_and_physics.md): AABB 충돌 및 서브스텝 구현 명세.

---

## 6. 프로토콜 버전 진화 이력

- **v1.0.0**: 게임 런타임 하네스 8대 기둥, 헤드리스 1만 틱 러너, 플레이어블 검수 관문(Playable Review Gate).
- **v1.1.0**: 인게임 실시간 손맛 튜너 (F1/F2 오버레이), Pygame 더미 가드, Reachability Solver, WebAssembly 패키저.
- **v1.2.0**: 멀티 엔진 생태계 지원 (Pygame, Tauri/HTML5, Godot 4.x), 엔진 자동 감지 검수기.
- **v1.3.0**: 원자적 세이브 안전망 (Atomic Save Rig), 상용 릴리즈 닥터 (`game_release_doctor.py`), 다국어(i18n) 린터 (`localization_linter.py`), 스팀 상용 출시 레퍼런스.
- **v1.4.0**: **기둥 9(그래픽 실전 툴 나침반)** 정립 및 초경량 SVG 벡터 에셋 빌더 (`vector_asset_builder.py`) 탑재.
- **v1.5.0**: **기둥 10(오디오 안전망)**, Rust+Python Hybrid 이원화 게임 가이드, `localization_linter.py --rewrite` 인플레이스 치환기 탑재.
- **v1.6.0 (Current - Portability & Consistency Polish Edition)**:
  - **상대 경로 이식성 완결**: `SKILL.md` 내 로컬 절대 경로 제거 및 상대 경로 표준화.
  - **플레이어 표면 UX 카피 일관성 개선**: `web_packager.py`의 사용자 노출 HTML에서 내부 프로토콜/하네스 용어 제거.
  - **CI 엄격 검증 지원**: `localization_linter.py`의 `--strict` 종료 코드 지원 및 데드 코드 제거.
  - **비플랫포머 및 오프라인 에셋 폴백 명시**: 턴제/TCG 소프트락 검사 및 외부 AI 에셋 툴 부재 시 SVG/프로시저럴 선행 구축 규약 정립.
