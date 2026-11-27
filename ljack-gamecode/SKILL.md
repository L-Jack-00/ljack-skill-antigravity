---
name: ljack-gamecode
description: >-
  엘잭 게임코드 프로토콜 (LJack GameCode Protocol, v1.3.0): 계층 격리, 계약 선행(Contract-First),
  마일스톤 연속 완주, 미세조정 슬라이더 샘플 Fast-Path 및 멀티모달 AI 에셋 브릿지 기반 TypeScript/ESM·HTML5(Canvas/DOM) 게임 아키텍처 하네스.
  사용자가 'ljack-gamecode', '게임코드', '게임 코드 하네스', '레이어 격리', 'aiPromptHint', '에셋 매니페스트',
  'Contract First', '스파게티 방지' 등을 요청하거나,
  src/logic 내 브라우저 미디어 API 차단, 마일스톤 단위 계층 순차 구현, 외부 AI 도구(Gemini Nano Banana/Batch, ComfyUI/SDXL, PixelLab, Recraft, ElevenLabs, Suno 등) 프롬프트 연동 및
  실구현 SVG/프로시저럴 아트 + O(1) 안전 폴백 기반의 TypeScript/ESM HTML5 게임 아키텍처를 구축하고자 할 때 활성화합니다.
---

# 엘잭 게임코드 프로토콜 (LJack GameCode Protocol)
## 계층 격리 · 마일스톤 연속 완주 · 멀티모달 에셋 브릿지 TypeScript/ESM·HTML5 하네스 (v1.3.0)

> **💡 시스템 지침 (System Directive)**:  
> 본 프로토콜은 TypeScript/ESM(`.js + JSDoc`) 및 HTML5(Canvas + DOM/CSS 하이브리드) 게임 개발 시 **스파게티 코드 양산**, **`src/logic/`의 브라우저 API 오염**, **임의 파일 경로 하드코딩**을 차단하기 위한 **아키텍처 경계 하네스(Architecture Boundary Harness)**입니다.  
>
> **실행 속도 & 깊이 원칙**: 계층을 분리한다는 이유로 2~3개 파일만 고치고 작업을 조기 종료하지 마십시오. 활성화된 **마일스톤(또는 기능 단위)** 전체가 동작하고 테스트를 통과할 때까지 `계약(specs) ➔ 순수 로직(src/logic) ➔ 뷰/오디오(src/view) ➔ 검증` 흐름을 **중단 없이 연속 완주**합니다. (`ljack-game`과 병행 시 게임 볼륨/Phase 규율은 `ljack-game`을 따르며, `ljack-skill`은 중복 호출하지 않습니다.)
>
> **⚡ 미세조정 Fast-Path (Interactive Slider Sample First)**:  
> 사용자가 신규 시스템이나 아키텍처 추가가 아니라 **물리·타이밍·이펙트 강도·레이아웃 수치 등의 미세조정(Fine-Tuning)**을 요청했다고 판단되는 경우에는 `specs/` ➔ `src/logic/` ➔ `src/view/` ➔ `layer_guard` 전체 적용 과정을 거치지 않습니다. 즉시 대상 파라미터를 `<input type="range">` 슬라이더로 실시간 조작·확인할 수 있는 **단일 인터랙티브 HTML/Canvas 튜닝 샘플**(`generative_ui` 지원 시 인라인 위젯/아티팩트, 수치 리드아웃·초기화·JSON 복사 포함)을 먼저 출력하고, 사용자가 수치를 확정한 뒤에만 본 코드(`specs/`·`src/`)에 반영하고 `layer_guard.py --strict` 검증을 수행합니다.

---

## 1. 3대 하네스 제어 메커니즘 (Core Guards)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                 LJack GameCode 3대 제어 메커니즘 (v1.3.0)               │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 레이어 강제 격리 (Layer Isolation Guard)                            │
│    - src/logic/ 내부에서 window, Canvas, AudioContext 등 DOM/미디어 API │
│      호출 금지 (scripts/layer_guard.py 정적 린터로 즉시 차단)          │
│    - 순수 상태 계산 및 EventBus.emit()만 허용                          │
│                                                                        │
│ 2. 에셋 브릿지 + 실구현 폴백 금지 (Real Visual/Audio First)            │
│    - 외부 AI 에셋 규격은 specs/asset_manifest.json(aiPromptHint) 등록  │
│    - 파일 미존재 시에도 체크보드/단순 비프음으로 방치하지 않고,         │
│      src/view/에 완성도 있는 SVG/프로시저럴 Canvas/WebAudio SFX 구현   │
│    - AssetHarness의 체크보드/사인파는 최종 누락 방어선으로만 사용      │
│                                                                        │
│ 3. 마일스톤 단위 계층 순차 완주 (Milestone-Scoped Layer Ordering)      │
│    - 작업 중단 없이 활성 마일스톤 전체를 끝까지 구현                   │
│    - 파일 편집 순서만 specs/ ➔ src/logic/ ➔ src/view/ ➔ test 순수 유지 │
│    - TODO/FIXME/빈 핸들러 잔존 시 layer_guard.py가 미완료로 경고/차단  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 4대 디렉토리 계층 격리 원칙 (Strict Layering)

| 디렉토리 / 파일 | 역할 및 제약 조건 |
| :--- | :--- |
| **`specs/types.ts`** | 전역 데이터 구조, 엔티티 상태, 이벤트 페이로드, **영속 UI 메타데이터(`visitedFlags`, `saveRequiredEvents`)**, 에셋 스키마 정의. (ESM `.js` 프로젝트는 `.d.ts` + JSDoc 활용) **(최우선 수정 대상)** |
| **`specs/asset_manifest.json`** | 모든 그래픽/오디오 리소스의 `AssetID`, 경로, 규격, 외부 AI 프롬프트(`aiPromptHint`) 및 선택 메타(`styleRef`, `characterRef`, `backdropColor`, `cutoutMode`, `forbiddenMotifs`, `rawCachePath`) 레지스트리. |
| **`src/core/`** | `EventBus.ts`, `AssetHarness.ts`, 메인 루프 등 엔진 공통 인프라 계층 (TS/ESM `.js` 호환). |
| **`src/logic/`** | 순수 게임 규칙, 물리 연산, 수식, 상태 머신.<br>**[필수 제약]**: `window`, `document`, `CanvasRenderingContext2D`, `AudioContext`, `HTMLImageElement` 등 브라우저/DOM API 접근 불가 (헤드리스 Node/Deno 테스트 100% 호환 유지). |
| **`src/view/`** | `src/logic/`의 상태를 읽어 Canvas 또는 DOM/CSS UI에 렌더링하고 `EventBus`를 구독하여 `AssetHarness` 및 프로시저럴 SVG/WebAudio를 결합해 풍부한 시각·청각 피드백을 제공하는 뷰 계층. |

---

## 3. 외부 멀티모달 AI 에셋 브릿지 & 실구현 규약

새로운 시각/청각 요소가 필요할 때 파일 경로 문자열(`"assets/..."`)을 뷰 코드에 직접 하드코딩하지 않고, `specs/asset_manifest.json`에 아래 규격의 영문 프롬프트(`aiPromptHint`) 및 참조·누끼 메타를 등록합니다.

- **`portrait` / `illustration` / `logo` (예: Gemini Nano Banana · Batch API / SDXL + ComfyUI)**:
  - 필수/권장 항목: 구도(`3:4 waist-up`), `backdropColor`(`#FFFFFF` vs 흰색 의복·로고용 `#123466`), `cutoutMode`(`portrait`/`sticker`/`full_bleed_icon`), 바리에이션 시 `characterRef`/`styleRef`, 저작권·임의 별표 차단용 `forbiddenMotifs`, 원본 보존 `rawCachePath`.
- **`sprite` / `spritesheet` (예: PixelLab / Scenario)**:
  - 필수 항목: 시점(Top-down, Side-view), 프레임 수, 해상도(`64x64`), 동작 서술, `transparent background, pixel art style`.
- **`ui_vector` / `icon` (예: Recraft V3 / Midjourney / SVG)**:
  - 필수 항목: 스타일(Vector/Flat), 테두리 규격, 팔레트, 풀블리드 앱 아이콘일 경우 `cutoutMode: "full_bleed_icon"`, 일반 UI 에셋은 `clean game UI asset, isolated on dark background`.
- **`audio_sfx` (예: ElevenLabs Sound Effects)**:
  - 필수 항목: 타격 재질(Metallic, Flesh, Magic), 길이(`0.2s ~ 1.5s`), 특성(`crisp impact, zero reverb, retro arcade SFX`).
- **`audio_bgm` (예: Suno / Udio)**:
  - 필수 항목: 장르, BPM, 악기 구성, `seamless loopable game background music, instrumental only`.

> **⚠️ 실구현 폴백 금지 원칙**:  
> 런타임 코드에서는 대문자 상수 키(`"SPR_HERO_RUN"`, `"SFX_HIT_CRIT"`)를 통해 `AssetHarness.getGraphic(id)` / `AssetHarness.playAudio(id)`를 호출하되, 디스크에 외부 AI 이미지·음원 파일이 아직 없는 단계에서는 **`AssetHarness`의 마젠타 체크보드/단순 사인파에 기대어 대충 끝내지 마십시오.** 반드시 `src/view/` 내 전용 렌더러/신스 모듈(SVG 벡터, 다층 프로시저럴 캔버스, WebAudio 필터·엔벨로프 효과음)을 연결해 **체크보드 없이도 즉시 플레이 가능한 비주얼과 사운드**를 제공해야 합니다.

---

## 4. 작업 실행 3단계 프로토콜 (Continuous Milestone Workflow)

새 기능이나 마일스톤을 구현할 때는 아래 순서로 **중간 정지 없이 끝까지 연속 실행**합니다:

```text
[Step 1: Contract & Manifest Update]
  specs/types.ts 인터페이스 정의 + specs/asset_manifest.json (aiPromptHint 포함) 갱신
        ↓ (멈추지 않고 즉시 진행)
[Step 2: Pure Logic Implementation + Headless Test]
  렌더링과 완전히 분리된 src/logic/ 모듈 및 단위/시뮬레이션 테스트 작성·통과
        ↓ (멈추지 않고 즉시 진행)
[Step 3: View & Audio Binding + Static Guard + Visual Check]
  src/view/에서 AssetHarness/SVG/프로시저럴 렌더러/EventBus 바인딩
  ➔ scripts/layer_guard.py --strict 실행 (계층 오염 0건, TODO/스텁 0건)
  ➔ 브라우저/실행 화면에서 실제 동작·UI 레이아웃·콘솔 에러 0건 확인 후 보고
```

- **계층 분리 vs 연속 실행**: 한 번의 턴에서 2~3개 파일만 고치고 사용자에게 턴을 넘기지 마십시오. 내부 편집 순서만 `specs/` ➔ `src/logic/` ➔ `src/view/` ➔ `tests/`로 엄격히 지키되, **요청된 마일스톤이 완전히 플레이·검증 가능할 때까지 한 흐름으로 완결**합니다.

---

## 5. 적용 및 정적 계층 검증 가이드

### 1) 상시 고정 시스템 프롬프트 적용
프로젝트 루트의 규칙 파일(`.idx/airules.md` 또는 `_harness/SYSTEM_PROMPT.md`)에 저장하거나 Antigravity Rules로 주입합니다.
- 참조 파일: [SYSTEM_PROMPT.md](templates/SYSTEM_PROMPT.md)

### 2) 세션 초기화 부트스트랩 프롬프트 적용
새 프로젝트를 생성하거나 기존 프로젝트를 GameCode 하네스로 전환할 때 사용합니다. (기획이 이미 주어진 경우 4개 파일 생성 후 대기하지 않고 즉시 Milestone 1 구현으로 이어갑니다.)
- 참조 파일: [PROMPT_BOOTSTRAP.md](templates/PROMPT_BOOTSTRAP.md)
- 생성되는 4대 기반 파일:
  1. `specs/types.ts`
  2. `specs/asset_manifest.json`
  3. `src/core/EventBus.ts`
  4. `src/core/AssetHarness.ts`

### 3) 정적 계층 격리 & 스텁 가드 (`scripts/layer_guard.py`)
`src/logic/` 내 브라우저 API 오염, `specs/asset_manifest.json` 무결성, `src/view/` 내 하드코딩 경로·거대 단일 파일(1,200줄/100KB+) 분할 권고, **소스 내 미구현 스텁(`TODO`/`FIXME`/`NotImplementedError`)**을 자동 검사합니다:
```bash
python scripts/layer_guard.py <project_directory> [--logic-dir DIR] [--view-dir DIR] [--manifest PATH] [--strict]
```

---

## 6. 내장 도구, 템플릿 및 레퍼런스

- [상시 시스템 프롬프트 템플릿](templates/SYSTEM_PROMPT.md): 에이전트 행동 지침 원문.
- [부트스트랩 프롬프트 템플릿](templates/PROMPT_BOOTSTRAP.md): 초기 4종 파일 스캐폴딩 실행문.
- [아키텍처 및 참조 구현 명세](references/architecture_spec.md): `specs/types.ts`, `EventBus.ts`, `AssetHarness.ts`의 완전한 프로덕션 코드.
- [정적 계층 격리 가드](scripts/layer_guard.py): `src/logic/` 순수성, 매니페스트 무결성 및 스텁 검사기.
