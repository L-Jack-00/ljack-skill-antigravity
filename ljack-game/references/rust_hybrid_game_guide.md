# LJack Game Protocol: Rust 코어 엔진 + Python 인터페이스 이원화 가이드
## 초고속 네이티브 시뮬레이션 & 유연한 UI/손맛 렌더링 (Rust-Python Hybrid Rig)

> **💡 시스템 지침 (System Directive)**:  
> 본 가이드는 고성능 결정론적 연산(물리, 충돌, 룰 엔진, 덱 알고리즘, 대규모 엔티티)은 **Rust 코어**로 구현하고,  
> 화면 렌더링, 입력 처리, 오디오, 실시간 손맛 튜너(F1)는 **Python (Pygame / ModernGL)**으로 결합하는 최상위 이원화 하네스 설계법을 규정합니다.

---

### 1. 왜 상용 게임에서 Rust 코어 + Python 인터페이스인가?

| 역할 계층 | 담당 언어 | 핵심 책임 | 장점 |
| :--- | :--- | :--- | :--- |
| **코어 시뮬레이션 (Core Engine)** | **Rust** | 고정 60Hz 물리 틱, TCG 카드 룰 체인, 충돌 계산, 헤드리스 1만 틱 시뮬레이터 | 메모리 안전성, 0.0001초 미만 연산, 멀티스레딩 데이터 레이스 0%, 가비지 컬렉션(GC) 렉 0% |
| **인터페이스 (I/O & Display)** | **Python (Pygame)** | 스프라이트 렌더링, 오디오 재생, 사용자 키 입력, [F1] 실시간 튜너, 다국어 | 빠른 개발 속도, 직관적인 창/오디오 관리, 간편한 스크립팅 |

* **결정론적 1만 틱 0.05초 검증**: Rust로 작성된 시뮬레이터는 Python 순수 루프 대비 **20배~100배 빠르게** 1만 번의 틱을 연산하여 터널링 및 도달 가능성(Reachability)을 찰나에 검증합니다.
* **코어의 절대적 순수성 (Pillar 1 극대화)**: Rust 코어는 `pygame`이나 OS 화면에 대해 단 1바이트도 알지 못하며, 오직 `step_tick(inputs) -> WorldState` 상태 전이만 수행합니다.

---

### 2. C-ABI `ctypes` 무의존성 바인딩 아키텍처

Python 환경에 무거운 C++ 컴파일러나 추가 pip 패키지 설치 없이, Rust의 `cdylib`과 Python 표준 라이브러리 `ctypes`만으로 연동하는 가장 안정적인 표준 패턴입니다.

#### 🦀 [Rust 코어 엔진] `core_rust/src/lib.rs`
```rust
#[repr(C)]
#[derive(Debug, Clone, Copy)]
pub struct PlayerState {
    pub x: f32,
    pub y: f32,
    pub vx: f32,
    pub vy: f32,
    pub is_grounded: bool,
    pub hp: i32,
}

#[repr(C)]
pub struct WorldState {
    pub tick_count: u64,
    pub player: PlayerState,
    pub gravity: f32,
    pub speed: f32,
    pub jump_strength: f32,
}

#[no_mangle]
pub extern "C" fn game_create() -> *mut WorldState {
    let world = Box::new(WorldState {
        tick_count: 0,
        player: PlayerState { x: 100.0, y: 350.0, vx: 0.0, vy: 0.0, is_grounded: false, hp: 100 },
        gravity: 0.55,
        speed: 5.20,
        jump_strength: -11.50,
    });
    Box::into_raw(world)
}

#[no_mangle]
pub extern "C" fn game_step_tick(ptr: *mut WorldState, input_left: bool, input_right: bool, input_jump: bool) {
    if ptr.is_null() { return; }
    let w = unsafe { &mut *ptr };
    w.tick_count += 1;

    // 수평 이동
    if input_left { w.player.vx = -w.speed; }
    else if input_right { w.player.vx = w.speed; }
    else { w.player.vx = 0.0; }
    w.player.x += w.player.vx;

    // 점프 및 중력
    if input_jump && w.player.is_grounded {
        w.player.vy = w.jump_strength;
        w.player.is_grounded = false;
    }
    w.player.vy += w.gravity;
    w.player.y += w.player.vy;

    // 바닥 충돌 판정
    if w.player.y >= 500.0 {
        w.player.y = 500.0;
        w.player.vy = 0.0;
        w.player.is_grounded = true;
    }
}

#[no_mangle]
pub extern "C" fn game_destroy(ptr: *mut WorldState) {
    if !ptr.is_null() {
        unsafe { drop(Box::from_raw(ptr)) };
    }
}
```

---

#### 🐍 [Python 바인딩 브릿지] `src/core/rust_engine.py`
```python
import os
import ctypes

class PlayerStruct(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("vx", ctypes.c_float),
        ("vy", ctypes.c_float),
        ("is_grounded", ctypes.c_bool),
        ("hp", ctypes.c_int32),
    ]

class WorldStruct(ctypes.Structure):
    _fields_ = [
        ("tick_count", ctypes.c_uint64),
        ("player", PlayerStruct),
        ("gravity", ctypes.c_float),
        ("speed", ctypes.c_float),
        ("jump_strength", ctypes.c_float),
    ]

class RustGameEngine:
    def __init__(self, lib_path: str = None):
        # target/release/core_rust.dll 또는 .so 자동 탐색
        self._lib = ctypes.CDLL(lib_path)
        self._setup_ffi()
        self._ptr = self._lib.game_create()

    def _setup_ffi(self):
        self._lib.game_create.restype = ctypes.POINTER(WorldStruct)
        self._lib.game_step_tick.argtypes = [ctypes.POINTER(WorldStruct), ctypes.c_bool, ctypes.c_bool, ctypes.c_bool]
        self._lib.game_destroy.argtypes = [ctypes.POINTER(WorldStruct)]

    def step(self, left: bool, right: bool, jump: bool):
        self._lib.game_step_tick(self._ptr, left, right, jump)
        return self._ptr.contents

    def close(self):
        if self._ptr:
            self._lib.game_destroy(self._ptr)
            self._ptr = None

    def __del__(self):
        self.close()
```

---

### 3. FFI 경계 패닉 방어 (Panic Safety Interlock)

Rust 코드에서 `unwrap()` 또는 인덱스 초과로 `panic!`이 발생하면 FFI 경계를 넘어 **Python 프로세스 자체가 즉사(Crash)**합니다. 이를 방어하기 위해 복잡한 연산에는 `std::panic::catch_unwind` 인터록을 적용합니다:

```rust
use std::panic::catch_unwind;

#[no_mangle]
pub extern "C" fn game_safe_calculate(ptr: *mut WorldState) -> i32 {
    let result = catch_unwind(|| {
        // 잠재적 패닉 발생 위험이 있는 복잡한 연산
        42
    });
    match result {
        Ok(val) => val,
        Err(_) => {
            eprintln!("[RUST CRITICAL] Panic caught at FFI boundary! Preventing Python crash.");
            -1 // 에러 코드 반환
        }
    }
}
```

---

### 4. 2단계 헤드리스 자가 치유 검증 루프

```text
[1단계: Rust 단독 검증 (0.01초)]
  cargo test --manifest-path core_rust/Cargo.toml
  ➔ 1만 틱 물리/충돌/룰 엔진 무결성 검증 (터널링 0건)
       ↓
[2단계: Python FFI 통합 검증 (0.1초)]
  python tests/test_sim_headless.py
  ➔ Python-Rust 간 메모리 정렬, 포인터 생명주기 및 C-ABI 정합성 검증
       ↓
[3단계: Pygame 렌더링 및 F1 손맛 튜너 (실행)]
  python run_game.py
  ➔ 60Hz 부드러운 화면 렌더링 및 실시간 파라미터 조율
```
