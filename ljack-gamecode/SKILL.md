---
name: ljack-gamecode
description: >-
  엘잭 게임코드 프로토콜 (LJack GameCode Protocol, v1.0.0): 엄격한 계층 격리, 계약 선행(Contract-First),
  외부 멀티모달 AI 에셋 브릿지 기반 TypeScript/HTML5 게임 아키텍처 하네스.
  사용자가 'ljack-gamecode', '게임코드', '게임 코드 하네스', '레이어 격리', 'aiPromptHint', '에셋 매니페스트',
  '원자적 작업', 'Contract First', '스파게티 방지' 등을 요청하거나,
  src/logic 내 브라우저 미디어 API 차단, 단계별 파일 격리 구현, 외부 AI 도구(PixelLab, Recraft, ElevenLabs, Suno 등) 프롬프트 연동 및
  $O(1)$ 프로시저럴 폴백 기반의 견고한 TypeScript/HTML5 게임 아키텍처를 구축하고자 할 때 활성화합니다.
---

# 엘잭 게임코드 프로토콜 (LJack GameCode Protocol)
## 엄격 계층 격리 & 멀티모달 에셋 브릿지 TypeScript/HTML5 게임 하네스 (v1.0.0)

> **💡 시스템 지침 (System Directive)**:  
> 본 프로토콜은 TypeScript/HTML5 게임 개발 시 **스파게티 코드 양산**, **`update()` 루프 내 렌더링/사운드 임의 하드코딩**, **장문 컨텍스트에서의 계층 혼재**를 원천 차단하기 위해 고안된 **제약 기반 아키텍처 하네스(Constraint-Driven Architecture Harness)**입니다.  
> 
> 상시 시스템 지침(`SYSTEM_PROMPT.md`)과 세션 초기화(`PROMPT_BOOTSTRAP.md`)로 이원화되어 작동하며, **계약 선행(Contract-First) ➔ 순수 로직(Pure Logic) ➔ 뷰 바인딩(View & Audio)**의 3단계 파이프라인을 엄격히 강제합니다.

---

## 1. 3대 하네스 제어 메커니즘 (Core Guards)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   LJack GameCode 3대 제어 메커니즘                      │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 레이어 강제 격리 (Layer Isolation Guard)                            │
│    - src/logic/ 내부에서 window, Canvas, AudioContext 등 DOM/미디어 API │
│      호출 금지 (scripts/layer_guard.py 정적 린터로 즉시 차단)          │
│    - 순수 상태 계산 및 EventBus.emit()만 허용                          │
│                                                                        │
│ 2. 에셋 브릿지 자동화 (AI Prompt Hint Injection)                        │
│    - 임의의 ctx.fillRect() / new Audio() 임시 하드코딩 남발 금지       │
│    - specs/asset_manifest.json에 PixelLab/Recraft/ElevenLabs/Suno 등   │
│      외부 AI 생성 도구용 영문 프롬프트(aiPromptHint)와 규격 선행 등록  │
│    - 실제 파일 로딩 실패 시 AssetHarness가 O(1) 체크보드/사인파 폴백   │
│                                                                        │
│ 3. 단계별 원자적 변경 (Staged Atomic Mutation)                         │
│    - 기능 추가/수정 시 단일 단계당 최대 2~3개 파일로 변경 범위 제한     │
│    - specs/types.ts & asset_manifest.json 계약 정합성 선행 검증        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 4대 디렉토리 계층 격리 원칙 (Strict Layering)

| 디렉토리 / 파일 | 역할 및 제약 조건 |
| :--- | :--- |
| **`specs/types.ts`** | 전역 데이터 구조, 엔티티 상태, 이벤트 페이로드, 에셋 스키마 정의. **(모든 기능 구현 시 최우선 수정 대상)** |
| **`specs/asset_manifest.json`** | 모든 그래픽/오디오 리소스의 `AssetID`, 경로, 규격, 외부 생성형 AI용 영문 프롬프트(`aiPromptHint`) 레지스트리. |
| **`src/core/`** | `EventBus.ts`, `AssetHarness.ts`, 메인 루프 등 엔진 공통 인프라 계층. |
| **`src/logic/`** | 순수 게임 규칙, 물리 연산, 수식, 상태 머신.<br>**[필수 제약]**: `window`, `document`, `CanvasRenderingContext2D`, `AudioContext`, `HTMLImageElement` 등 브라우저/DOM API 접근 불가 (헤드리스 Node 테스트 100% 호환 유지). |
| **`src/view/`** | `src/logic/`의 상태를 읽어 Canvas에 렌더링하고 `EventBus`를 구독하여 `AssetHarness` 사운드를 재생하는 뷰 계층. |

---

## 3. 외부 멀티모달 AI 에셋 브릿지 규약

새로운 시각/청각 요소가 필요할 때 뷰 코드에 도형이나 파일 경로를 임의 하드코딩하지 않고, 반드시 `specs/asset_manifest.json`에 아래 규격의 영문 프롬프트(`aiPromptHint`)를 선행 등록합니다.

- **`sprite` / `spritesheet` (예: PixelLab / Scenario)**:
  - 필수 항목: 시점(Top-down, Side-view), 프레임 수, 해상도(`64x64`), 동작 서술, `transparent background, pixel art style`.
- **`ui_vector` / `icon` (예: Recraft V3 / Midjourney / SVG)**:
  - 필수 항목: 스타일(Vector/Flat), 테두리 규격, 팔레트, `clean game UI asset, isolated on dark background`.
- **`audio_sfx` (예: ElevenLabs Sound Effects)**:
  - 필수 항목: 타격 재질(Metallic, Flesh, Magic), 길이(`0.2s ~ 1.5s`), 특성(`crisp impact, zero reverb, retro arcade SFX`).
- **`audio_bgm` (예: Suno / Udio)**:
  - 필수 항목: 장르, BPM, 악기 구성, `seamless loopable game background music, instrumental only`.

> 런타임 코드에서는 파일 경로 문자열(`"assets/..."`)을 직접 쓰지 않고, 오직 대문자 상수 키(`"SPR_HERO_RUN"`, `"SFX_HIT_CRIT"`)를 통해 `AssetHarness.getGraphic(id)`와 `AssetHarness.playAudio(id)`만 호출합니다. 실제 파일이 디스크에 있으면 즉시 로드하며, 아직 생성 전이거나 누락된 경우에는 $O(1)$ 디버그 체크보드/합성 사인파 폴백으로 무중단 동작합니다.

---

## 4. 작업 실행 3단계 프로토콜 (Execution Workflow)

사용자가 새 기능이나 시스템 추가를 지시하면 반드시 다음 순서를 따릅니다:

```text
[Step 1: Contract & Manifest Update]
  specs/types.ts 인터페이스 정의 + specs/asset_manifest.json (aiPromptHint 포함) 갱신
        ↓
[Step 2: Pure Logic Implementation]
  렌더링과 완전히 분리된 src/logic/ 모듈 작성 (순수 수학/상태 전이/EventBus.emit)
        ↓
[Step 3: View & Audio Binding + Static Guard]
  src/view/에서 AssetHarness와 EventBus를 구독하여 바인딩 후 scripts/layer_guard.py 검증
```

- **단계적 변경 규율**: 일반 기능 추가 및 리팩터링 시 한 번의 응답에서 변경/생성하는 파일은 **최대 2~3개(동일 계층 단위)**로 제한합니다. (초기 부트스트랩 4종 생성은 1단계 계약 2종 + 2단계 코어 2종으로 분할하거나 초기화 전용 일괄 생성으로 처리합니다.)

---

## 5. 적용 및 정적 계층 검증 가이드

### 1) 상시 고정 시스템 프롬프트 적용
프로젝트 루트의 규칙 파일(`.idx/airules.md` 또는 `_harness/SYSTEM_PROMPT.md`)에 저장하거나 Antigravity Rules로 주입합니다.
- 참조 파일: [SYSTEM_PROMPT.md](templates/SYSTEM_PROMPT.md)

### 2) 세션 초기화 부트스트랩 프롬프트 적용
새 프로젝트를 생성하거나 기존 프로젝트를 GameCode 하네스로 전환할 때 채팅창에 전송합니다.
- 참조 파일: [PROMPT_BOOTSTRAP.md](templates/PROMPT_BOOTSTRAP.md)
- 생성되는 4대 기반 파일:
  1. `specs/types.ts`
  2. `specs/asset_manifest.json`
  3. `src/core/EventBus.ts`
  4. `src/core/AssetHarness.ts`

### 3) 정적 계층 격리 가드 (`scripts/layer_guard.py`)
`src/logic/` 내 브라우저 API 오염, `specs/asset_manifest.json`의 `aiPromptHint` 누락, `src/view/` 내 하드코딩된 `new Audio()` / raw 경로 사용을 0.1초 만에 자동 검사합니다:
```bash
python scripts/layer_guard.py <project_directory> [--strict]
```

---

## 6. 내장 도구, 템플릿 및 레퍼런스

- [상시 시스템 프롬프트 템플릿](templates/SYSTEM_PROMPT.md): 에이전트 행동 지침 원문.
- [부트스트랩 프롬프트 템플릿](templates/PROMPT_BOOTSTRAP.md): 초기 4종 파일 스캐폴딩 실행문.
- [아키텍처 및 참조 구현 명세](references/architecture_spec.md): `specs/types.ts`, `EventBus.ts`, `AssetHarness.ts`의 완전한 프로덕션 코드 (실제 에셋 로드 + $O(1)$ 폴백 포함).
- [정적 계층 격리 가드](scripts/layer_guard.py): `src/logic/` 순수성 및 매니페스트 무결성 검사기.
