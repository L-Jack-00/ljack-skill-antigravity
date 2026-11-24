# 엘잭 게임코드 프로토콜 (LJack GameCode Protocol)
## TypeScript/ESM·HTML5 계층 격리 · 마일스톤 연속 완주 · 멀티모달 에셋 브릿지 하네스 (v1.2.0)

`ljack-gamecode`는 TypeScript/ESM(`.js + JSDoc`) 및 HTML5(Canvas + DOM/CSS 하이브리드) 게임 개발 시 **스파게티 코드 양산**, **순수 로직 계층의 브라우저 API 오염**, **임의의 경로 하드코딩**을 차단하면서도, **에이전트가 2~3파일만 수정하고 조기 종료하거나 스텁·체크보드 상태로 방치하지 않도록** 설계된 계약 선행(Contract-First) 게임 코드 하네스입니다.

---

## 📂 모듈 구조

```text
ljack-gamecode/
├── SKILL.md                          # 코어 프로토콜 지침 및 마일스톤 연속 완주 규약
├── README.md                         # 본 안내서
├── scripts/
│   └── layer_guard.py                # src/logic/ 오염 차단, asset_manifest.json 및 스텁(TODO) 검증기
├── templates/
│   ├── SYSTEM_PROMPT.md              # 상시 고정 시스템 지침 템플릿
│   └── PROMPT_BOOTSTRAP.md           # 초기 코어 파일 4종 스캐폴딩 프롬프트
└── references/
    └── architecture_spec.md          # types.ts, asset_manifest.json, EventBus.ts, AssetHarness.ts 표준 구현
```

---

## 🛡️ 3대 핵심 원칙 (v1.2.0)

1. **레이어 강제 격리 (`Layer Isolation`)**:
   - `src/logic/`은 순수 연산과 `EventBus.emit()`만 수행하며, `window`, `document`, `CanvasRenderingContext2D`, `AudioContext` 등 브라우저 API 접근을 `scripts/layer_guard.py`로 차단합니다.
2. **에셋 브릿지 + 실구현 우선 (`Real Visual/Audio First`)**:
   - `specs/asset_manifest.json`에 외부 생성형 AI용 영문 프롬프트 및 참조/누끼 메타를 등록합니다.
   - 실제 에셋 파일이 디스크에 아직 없을 때도 체크보드/비프음 폴백에만 머무르지 않고, `src/view/`에 완성도 있는 SVG/프로시저럴 Canvas·WebAudio 효과음을 구현합니다.
3. **마일스톤 단위 계층 순차 완주 (`Milestone-Scoped Layer Ordering`)**:
   - 계약(`specs/`) ➔ 순수 로직(`src/logic/`) ➔ 뷰/오디오(`src/view/`) ➔ 테스트 순서를 지키되, 2~3파일 제한 때문에 중간에 멈추지 않고 활성 마일스톤이 `layer_guard.py --strict`(계층 오염 0건, TODO/스텁 0건)를 통과할 때까지 연속 완주합니다.
