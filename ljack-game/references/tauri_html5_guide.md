# LJack Game Protocol: Tauri + HTML5/Canvas 게임 하네스 가이드

Tauri와 HTML5(Canvas 2D / WebGL)를 결합한 게임 개발 시, LJack 8대 기둥(결정론적 고정 틱, 헤드리스 1만 틱 러너, 인게임 실시간 손맛 튜너, 플레이어블 검수 관문)을 구현하는 표준 레시피입니다.

---

### 1. 결정론적 고정 타임스텝 게임 루프 (Fixed-Delta Accumulator)
- **핵심 문제**: 브라우저의 `requestAnimationFrame`은 60Hz, 120Hz, 144Hz, 또는 백그라운드 탭에서 FPS가 수시로 변하므로, 렌더링 루프에 물리 연산을 묶으면 캐릭터 속도와 점프 궤적이 망가집니다.
- **해법**: 델타 누적기(Accumulator) 패턴으로 렌더링 프레임레이트와 관계없이 항상 정확히 60Hz($\Delta t = 1/60$초) 단위로만 물리 시뮬레이션을 수행합니다.

```javascript
// src/core/loop.js
const FIXED_DT = 1 / 60; // 60Hz 고정 틱
let accumulator = 0.0;
let lastTime = performance.now();

function gameLoop(currentTime) {
    const frameDelta = Math.min((currentTime - lastTime) / 1000.0, 0.25); // 나선형 지연(Spiral of death) 방지
    lastTime = currentTime;
    accumulator += frameDelta;

    while (accumulator >= FIXED_DT) {
        engine.stepTick(activeInputs); // 결정론적 고정 틱 1회 연산
        accumulator -= FIXED_DT;
    }

    renderer.draw(world, accumulator / FIXED_DT); // 보간(Interpolation) 렌더링
    requestAnimationFrame(gameLoop);
}
```

---

### 2. Node.js 헤드리스 1만 틱 초고속 시뮬레이터 (`tests/test_sim_headless.js`)
- 브라우저나 DOM 객체(`window`, `document`)에 직접 의존하지 않는 순수 JS/TS 도메인 코드로 작성하여, Node.js 또는 Bun 환경에서 화면 없이 **1만 번의 틱을 0.05초 만에 메모리 상에서 검증**합니다.
```bash
node tests/test_sim_headless.js
```
- 승패 도달 가능성, 물리 충돌 무결성, 메모리 누수 0건 판정 후 플레이어블 검수로 전진.

---

### 3. 인게임 실시간 HTML 손맛 튜너 (F1 오버레이 & 핫저장)
- 캔버스 위에 반투명 오버레이 레이어(`<div id="live-tuner">`)를 얹어, 플레이 도중 `[F1]` 키로 열고 실시간 슬라이더나 방향키로 파라미터를 조절합니다.
- `[F2]` 누를 때:
  - 브라우저 모드: `localStorage.setItem("game_balance", JSON.stringify(params))`
  - Tauri 모드: `window.__TAURI__.core.invoke("save_balance", { params })`로 디스크 파일 핫저장.

---

### 4. 원클릭 Tauri 데스크톱 패키징 및 웹 배포
- 데스크톱 네이티브 배포 (크기 ~10MB, 초경량, 메모리 30MB 미만):
  ```bash
  npm run tauri build
  ```
- 웹 브라우저 배포 (Itch.io / 정적 웹 호스팅):
  ```bash
  npm run build
  ```
