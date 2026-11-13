# 엘잭 게임코드 프로토콜 (LJack GameCode Protocol)
## TypeScript/HTML5 계층 격리 & 멀티모달 에셋 브릿지 게임 하네스 (v1.0.0)

`ljack-gamecode`는 TypeScript 및 HTML5 Canvas 게임 개발 시 **스파게티 코드 양산**, **순수 로직 계층의 브라우저 API 오염**, **임의의 도형/사운드 하드코딩**을 차단하는 계약 선행(Contract-First) 기반 게임 코드 하네스입니다.

---

## 📂 모듈 구조

```text
ljack-gamecode/
├── SKILL.md                          # 코어 프로토콜 지침 및 3단계 작업 규약
├── README.md                         # 본 안내서
├── scripts/
│   └── layer_guard.py                # src/logic/ 오염 차단 및 asset_manifest.json 검증기
├── templates/
│   ├── SYSTEM_PROMPT.md              # 상시 고정 시스템 지침 템플릿
│   └── PROMPT_BOOTSTRAP.md           # 초기 코어 파일 4종 스캐폴딩 프롬프트
└── references/
    └── architecture_spec.md          # types.ts, asset_manifest.json, EventBus.ts, AssetHarness.ts 표준 구현
```

---

## 🛡️ 3대 핵심 원칙

1. **레이어 강제 격리 (`Layer Isolation`)**:
   - `src/logic/`은 순수 연산과 `EventBus.emit()`만 수행하며, `window`, `document`, `CanvasRenderingContext2D`, `AudioContext` 등 브라우저 API 접근을 `scripts/layer_guard.py`로 차단합니다.
2. **에셋 브릿지 자동화 (`AssetHarness` + `aiPromptHint`)**:
   - `specs/asset_manifest.json`에 외부 생성형 AI(PixelLab, Recraft, ElevenLabs, Suno 등)용 영문 프롬프트를 등록합니다.
   - 실제 에셋 파일이 준비되면 즉시 로드하며, 미준비/누락 시에는 $O(1)$ 디버그 체크보드/합성 사인파 폴백으로 끊김 없이 실행됩니다.
3. **단계별 원자적 변경 (`Staged Mutation`)**:
   - 계약(`specs/`) ➔ 순수 로직(`src/logic/`) ➔ 뷰/오디오(`src/view/`) 순서로 단계를 분리하고 턴당 2~3개 파일 이내로 변경 범위를 제한하여 코드 품질을 유지합니다.
