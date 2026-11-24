---
name: ljack-game
description: >-
  엘잭 게임 프로토콜 (LJack Game Protocol): 멀티 엔진 런타임 하네스 & 마일스톤 기반 상용 인디 게임 개발 프로토콜 (v1.8.0).
  사용자가 '엘잭 게임', '게임 개발', '인디 게임', '게임 하네스', '상용화', '스팀 출시', 'Pygame', 'Tauri', 'HTML5 캔버스', '고도 엔진', 'Godot', 'Rust', 'Rust+Python' 등을 요청하거나,
  마일스톤(Vertical Slice) 단위의 깊이 있는 콘텐츠 구현, 결정론적 고정 틱 루프, 헤드리스 1만 틱 시뮬레이터, 사용자 플레이 검수 관문(Playable Review Gate),
  인게임 실시간 손맛 튜너(F1/F2 오버레이), 원자적 세이브(Atomic Save), 다국어(i18n) 현지화 및 자동 치환, 상용 릴리즈 닥터,
  그래픽 툴 나침반(UI 벡터, SDXL 일러스트, 도트 스프라이트, 셰이더 이펙트), 오디오 런타임 하네스(WebAudio 제스처 가드, 3-Bus 볼륨, 무음 디바이스 폴백),
  스팀/스토브/itch.io 상용 출시 파이프라인을 원할 때 활성화합니다.
---

# 엘잭 게임 스킬 (LJack Game Protocol)
## 마일스톤 기반 상용 인디 게임 개발 & 멀티 엔진 런타임 하네스 프로토콜 (v1.8.0)

> **💡 시스템 지침 (System Directive)**:  
> 본 프로토콜은 AI 에이전트가 게임을 **얕은 스캐폴드나 스텁(Stub)으로 대충 끝내지 않고**,  
> **Phase 0(기획·볼륨 계약) ➔ Phase 1(수직 슬라이스 반복 구현·실제 플레이/시각 검증) ➔ Phase 2(상용화 마감·릴리즈 닥터)** 순서로 깊이 있게 완주하도록 규정하는 최상위 게임 개발 프로토콜입니다.  
>
> **스킬 조합 규율**: 게임 개발 시 **`ljack-skill`은 중복 로드하지 마십시오** (핵심 하네스·UX·누끼 규율은 본 스킬에 이미 통합되어 있습니다). TypeScript/ESM·HTML5 계층 격리가 필요할 때만 `/ljack-gamecode`를 보조 아키텍처 가드로 함께 사용합니다.

> **⚠️ 버전 독립성 불변 원칙 (Version Independence Principle)**:  
> **본 프로토콜의 버전(v1.8.0)과 대상 게임의 자체 버전은 완전히 별개입니다.**  
> 대상 게임은 사용자가 명시한 버전 또는 표준 SemVer 기본값(`v0.1.0` / `v1.0.0`)부터 온전히 독립적인 생명주기를 갖습니다.

---

## 1. 작업 집중 원칙: Phase 1(코어·콘텐츠) vs Phase 2(상용 마감) 분리

초기 프로토타이핑과 콘텐츠 구현 단계부터 다국어 추출, 배포 패키징, 릴리즈 클리너를 동시에 강제하면 에이전트가 **게임의 재미·볼륨·연출 대신 보일러플레이트 작성에 토큰을 소진하고 조기 종료**합니다. 반드시 아래 단계 경계를 지킵니다.

```text
[Phase 0: 스펙 & 콘텐츠 볼륨 계약]
  - ROADMAP.md (또는 specs/milestones.json)에 마일스톤(M1~M4)과 최소 볼륨 목표 고정
       ↓
[Phase 1: 마일스톤별 수직 슬라이스(Vertical Slice) 연속 구현]  ◀── 출시 QA(i18n/봉인/패키징) 보류
  - M1(코어 조작·전투·타격감) ➔ M2(적/스테이지/패턴 볼륨) ➔ M3(성장·경제·오디오/VFX)
  - 매 마일스톤마다: 구현 ➔ 1만 틱/헤드리스 검증 ➔ 실제 실행/브라우저 시각·인터랙션 검증
  - ⛔ Anti-Stub: TODO, 빈 핸들러, 체크보드/비프음 방치 상태에서 완료 보고 절대 금지
       ↓
[Phase 2: 상용화 마감 & 플레이어블 검수 관문]
  - 사용자 플레이 검수(Playable Review Gate, F1/F2 튜닝)
  - i18n(--rewrite --strict) ➔ 원자적 세이브/플러시 ➔ F1 봉인 ➔ game_release_doctor.py (80점+ & 스텁 0건)
```

---

## 2. 안티-스텁 & 깊이 완주 규율 (Anti-Stub & Deep Execution Rules)

에이전트가 작업을 짧게 끊고 대충 마무리하는 현상을 막기 위해 다음 5대 규율을 강제합니다.

1. **규모가 클수록 마일스톤으로 쪼개어 각 단계를 완결한다**:
   - 한 번에 전체 게임을 얕게 훑지 않고 `M1 -> M2 -> M3 -> M4` 마일스톤을 순서대로 깊게 구현합니다.
   - 사용자가 특정 마일스톤 또는 전체 구현을 지시한 경우, **승인 관문(기획 상충·외부 자격 증명·최종 검수)**에 걸리지 않는 한 중간에 멈추거나 사용자에게 떠넘기지 않고 할당된 범위의 **Definition of Done(DoD)**을 끝까지 달성합니다.
2. **스캐폴드는 시작점이지 완성품이 아니다**:
   - `scripts/game_scaffolder.py`가 만든 기본 발판 4개/샘플 데모를 그대로 두고 "기본 게임 구현 완료"로 보고할 수 없습니다.
   - 착수 시 합의한 콘텐츠 볼륨(적 종류 수, 스킬/카드/아이템 수, 스테이지/웨이브 수, UI 화면 수)이 실제로 데이터·로직·렌더링에 반영되어야 합니다.
3. **폴백(Fallback) 방치 금지**:
   - 마젠타 체크보드, 단조로운 사인파 비프음, `ctx.fillRect` 단색 사각형만 남긴 상태는 "비상 폴백"이지 구현 완료가 아닙니다.
   - 외부 AI 에셋 파일이 아직 없는 환경이라면 **내장 `scripts/vector_asset_builder.py`, SVG 일러스트, 다층 프로시저럴 캔버스 드로잉, WebAudio 신스/엔벨로프 효과음**을 실제로 구현해 플레이어 눈에 상용 수준에 가까운 시각/청각 피드백이 보이게 만듭니다.
4. **숫자 틱 + 실제 화면/플레이 검증 필수**:
   - `tick_sim_runner.py` 통과만으로 끝내지 않습니다.
   - 웹/HTML5/Tauri 게임은 헤드리스 브라우저 DOM E2E(타이틀→시작→핵심 루프→상점/메뉴→게임오버/재시작, 0 console errors)와 **실제 스크린샷/레이아웃 확인**을 거쳐 UI 겹침·잘림·미작동 버튼을 직접 고친 뒤 보고합니다.
5. **스텁/더미 코드 잔존 금지**:
   - `TODO`, `FIXME`, `NotImplementedError`, 빈 이벤트 콜백, 하드코딩된 고정 승리 리턴이 남아 있으면 마일스톤 완료로 간주하지 않습니다.

---

## 3. 멀티 엔진 게임 런타임 하네스 10대 핵심 기둥

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
         [Phase 1 마일스톤 검증 PASS ➔ Phase 2 플레이 검수 ➔ 상용 닥터 감사 ➔ 릴리즈 봉인]
```

- **기둥 1: 고정 틱과 렌더링 분리**: Pygame Dummy 가드, Tauri Accumulator 루프, Godot `_physics_process`, Rust 코어 + Python FFI 이원화 분리 (TypeScript/HTML5에서 엄격한 파일 계층 격리가 필요할 경우 `/ljack-gamecode` 규약과 병행).
- **기둥 2: 헤드리스 1만 틱 & DOM E2E 검증**:
  - 렌더링 없이 1만 틱 이상을 오프라인으로 고속 실행해 무한 루프, NaN 오염, 메모리 누수, 승패 불변식을 검증.
  - HTML5/Tauri 등 웹 UI 게임에서는 코어 시뮬레이션에 더해 **헤드리스 브라우저 DOM E2E 검증(뷰 전환·모달·호버 프리뷰·스크린샷 레이아웃 확인·0 console errors)**을 함께 수행.
- **기둥 3: 입력 버퍼링 & 안전망**: 프레임 드랍 시 입력 씹힘 방지 및 게임 종료 시 물리 입력 해제.
- **기둥 4: 충돌 감사, Reachability Solver & 경제 불변식**:
  - 플랫포머/액션: 투사체 관통 방지 서브스텝 및 도달 불가능 발판(`tick_sim_runner.py`) 수학적 사전 감지.
  - 턴제/카드(TCG)/로그라이크: 드로우·자원 고갈, 턴 무한 루프, **상점 최소 재고(`stock >= 1`)·허브 전이 불변식** 등 소프트락/경제 붕괴 0건 시뮬레이션 검증.
- **기둥 5: 게임 필(Game Feel), 실시간 튜너 & 서브 뷰 위생**:
  - 코요테 타임, 점프 선입력 버퍼, 히트스톱/카메라 셰이크/파티클, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 및 `prefers-reduced-motion` 애니메이션 배려 지원.
  - **서브 뷰 전환 위생(Sub-view Transition Hygiene)**: 팩 개봉 결과 배너, 호버 프리뷰 툴팁, NPC 감정 복귀 타이머는 뷰 이탈·재진입 시 반드시 초기화.
- **기둥 6: 플레이어블 검수 관문 (Playable Review Gate)**:
  - Phase 2 진입 시 사용자에게 로컬 실행 명령과 밸런스 파라미터 요약표를 제출하고 직접 손맛 검수 수렴.
- **기둥 7: 세이브 데이터 원자성 & 경제 커밋 즉시 저장**:
  - 임시 파일 쓰기 및 `os.replace` 원자적 교체로 충돌/정전 시 세이브 파일 깨짐(Corruption) 방어.
  - **세이브스커밍/유실 방어**: 카드팩 개봉·단품 구매·거래·덱 저장·이벤트 선택 등 모든 랜덤/경제 커밋 직후 디바운스를 기다리지 않고 **즉시 동기 저장(`saveRunNow()`)**하고, `beforeunload`/`pagehide`에도 플러시 가드를 연결.
- **기둥 8: 다국어, 아이콘 분리 & 상용 릴리즈 봉인 (Phase 2 적용)**:
  - `locales/` 다국어 사전 탑재, 상용 빌드 시 `F1` 손맛 튜너 자동 봉인(`PRODUCTION_BUILD=True`), **독자 중심 문서화(README/주석 내 변경점 찌꺼기 배제)**, 스팀/웹/데스크톱 배포 패키징 지원 (스팀 AppID 및 SDK 연동은 개발자 자격 정보 제공 시 활성화).
  - **앱 아이콘 vs 인게임 심볼 분리**: 데스크톱/창 아이콘(`app_icon.png`, `src-tauri/icons/*`, 풀블리드 `1024x1024` 무여백 원본)과 인게임 카드 뒷면/문장 SVG를 분리 관리.
- **기둥 9: 🎨 그래픽 실전 툴 나침반 (Game Art Toolchain Compass)**:
  - UI/프레임/뱃지는 **Figma / SVG 벡터**로 가볍고 깨짐 없게 구축 (내장 `scripts/vector_asset_builder.py` 즉시 활용 가능).
  - 캐릭터/배경 원화 및 NPC 표정 바리에이션(`Base->Excited/Tired/Deal`)은 **Gemini 멀티레퍼런스 이미지 모델 / Batch API** 또는 **SDXL 1.0 + ComfyUI**로 가운데 일러스트에만 분리 투입.
  - **누끼·비용·IP 실전 규율**: `#FFFFFF` vs `#123466` 이원 배경으로 흰색 의복/스티커 경계 보존, `#479be6` 보색 시트 검수, IP 금칙 모티프·임의 레벨 별표 차단, 무료 등급 이미지 차단(`limit: 0`) 확인 및 500장 이상 대량 생성 시 Batch API(50% 절감)·SDXL 하이브리드 적용.
  - 2D 도트 스프라이트는 **SD 1.5 + Pixel LoRA ➡️ Aseprite**로 격자 통일, 회전/발광 이펙트는 **게임 엔진 2D 셰이더**로 동적 구현.
  - *외부 이미지 생성 툴이 없는 로컬 코딩 환경에서는 체크보드 더미로 방치하지 말고 완성도 있는 SVG/프로시저럴 아트와 에셋 ID 분리 구조로 우선 구현한 뒤 추후 최종 아트로 교체합니다.*
- **기둥 10: 🎵 무결점 오디오 & 사운드 런타임 하네스 (Audio Safety & Sound Rig)**:
  - 사운드카드 미연결/헤드리스 환경 크래시 방지(Pygame 더미 오디오 폴백).
  - 웹 브라우저(Tauri/HTML5) 오토플레이 차단 해제(User Gesture Unlock Guard).
  - 독립 3계층 볼륨 버스(Master / BGM / SFX), 페이드 트랜지션, 동시 발음수(Voice Polyphony) 제어.

---

## 4. 자율 게임 에이전트 10대 실행 강령

1. **버전 독립성 준수**: 게임 프로토콜 버전(v1.8.0)과 대상 게임 고유 버전(`v0.1.0`)을 분리한다.
2. **단계 집중과 볼륨 계약 선행**: 착수 시 `ROADMAP.md`에 마일스톤과 최소 콘텐츠 볼륨을 정의하고, Phase 1에서는 게임플레이·콘텐츠·연출 깊이에 집중한다.
3. **스텁·빈 껍데기·폴백 방치 금지**: `TODO`, 빈 핸들러, 체크보드/비프음만 남긴 채 마일스톤을 완료 처리하지 않는다.
4. **기술 결함은 무중단 자가 치유한다**: 충돌 버그, 맵 차단, 무한 루프, 콘솔 에러는 사용자에게 묻지 않고 시뮬레이터와 DOM E2E로 스스로 해결한다.
5. **실제 플레이/시각 검증 수행**: 틱 시뮬레이션뿐 아니라 실제 화면 렌더링·조작 흐름(브라우저/실행 창)에서 UI 깨짐과 인터랙션 결함을 직접 확인한다.
6. **손맛과 재미는 사용자에게 검수받는다 (Playable Review Gate)**: 코어와 콘텐츠가 갖춰진 후 로컬 실행 스크립트와 밸런스 요약표를 제출하고 직접 플레이 검수를 요청한다.
7. **Phase 2 상용 안전망 적용**: 출시 준비 단계에서 원자적 교체(`os.replace` / `saveRunNow()`), `PRODUCTION_BUILD` 디버그 봉인, `localization_linter.py --rewrite --strict` 다국어 치환을 적용한다.
8. **사용자 표면 UX 카피 & 독자 중심 문서화 준수**: 인게임 UI/사전/웹 패키저 출력물에서 내부 개발 용어(`ljack`, `하네스` 등) 노출을 차단하고, 코드 주석과 README에서 시점 의존 메모를 배제한다.
9. **보일러플레이트 스캐폴더는 출발점만 제공**: `scripts/game_scaffolder.py`로 초기 뼈대를 잡되, 즉시 대상 게임 고유의 메카닉과 풍부한 콘텐츠 데이터로 대체·확장한다.
10. **상용 릴리즈 닥터 전수 검사**: 최종 릴리즈 전 `scripts/game_release_doctor.py` 80점 이상 및 스텁 0건을 검증한다.

---

## 5. 상용 게임 자율 실행 3-Phase 표준 파이프라인

```text
[Phase 0: 기획 볼륨 고정 & 엔진 스캐폴딩]
  - ROADMAP.md 작성 (M1~M4 마일스톤, 적/아이템/스테이지 최소 수량, DoD 명시)
  - 엔진 스택 결정 ➔ scripts/game_scaffolder.py 호출 (또는 ljack-gamecode 코어 구축)
       ↓
[Phase 1: 수직 슬라이스 반복 구현 (M1 ➔ M2 ➔ M3)]
  - Fixed 60Hz 루프, 코요테 타임/버퍼링/타격감, 적 AI·레벨·경제·VFX·SVG/프로시저럴 아트·오디오 구현
  - 마일스톤마다: scripts/tick_sim_runner.py (1만 틱) + 실제 실행/DOM E2E & 화면 확인 ➔ 자가 치유
  - ⛔ 스텁 0건 & 마일스톤 볼륨 목표 달성 전까지 다음 마일스톤/종료로 넘어가지 않음
       ↓
[Phase 2: 플레이어블 검수 & 상용 릴리즈 봉인 (M4)]
  - scripts/play_preview_launcher.py로 조작법 및 밸런스 요약 제출 ➔ 사용자 직접 플레이 검수 [F1/F2]
  - 피드백 반영 ➔ localization_linter.py --rewrite --strict ➔ PRODUCTION_BUILD 봉인
  - scripts/game_release_doctor.py (80점+ & 스텁 0건) ➔ 배포 패키징 완결
```

---

## 6. 내장 자동화 도구 및 참조 레퍼런스

### 🛠️ 내장 스크립트 도구 (`scripts/`)
- `scripts/vector_asset_builder.py`: 초경량 SVG 카드 프레임 및 뱃지 빌더 (comic 카툰풍 / metallic 메탈릭풍 지원).
- `scripts/game_scaffolder.py`: Pygame, Tauri, Godot, Rust+Python Hybrid 골격 즉시 생성.
- `scripts/game_release_doctor.py`: 상용 출시 준비도(0~100), **소스 내 `TODO`/`FIXME`/미구현 스텁 탐지 & 에셋 매니페스트 실체 파일 점검**, 저장·오디오 안전망, 풀블리드 아이콘·모션 배려·UX 카피 정적 진단 닥터.
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

## 7. 프로토콜 버전 진화 이력

- **v1.0.0 ~ v1.5.0**: 게임 런타임 하네스 10대 기둥, 헤드리스 1만 틱 러너, F1/F2 튜너, 원자적 세이브, 그래픽 툴 나침반, 오디오 하네스, `--rewrite` i18n 치환기.
- **v1.6.0 ~ v1.7.0**: 상대 경로 이식성, 멀티레퍼런스 AI 누끼/비용 가이드, 즉시 동기 저장, 서브 뷰 전환 위생, 풀블리드 아이콘·DOM E2E 검증.
- **v1.8.0 (Current - Milestone Vertical-Slice & Anti-Stub Edition)**:
  - **Phase 1(코어·콘텐츠) / Phase 2(상용화 마감) 분리**: 개발 초반부터 출시 QA 규칙으로 토큰이 새는 문제를 차단하고 게임플레이·콘텐츠 볼륨에 집중.
  - **안티-스텁 & 깊이 완주 규율 신설**: 스캐폴드 방치, 체크보드/비프음 방치, `TODO`/빈 핸들러 상태에서의 조기 완료 보고 금지 및 `ljack-skill` 중복 호출 배제.
  - **`game_release_doctor.py` 확장**: 소스 내 미구현 스텁(`TODO`/`FIXME`/`NotImplementedError`) 탐지 및 `asset_manifest.json` 실파일 연결률 어드바이저리 추가.
