# LJack Protocol 도메인별 런타임 하네스 적용 가이드

본 가이드는 다양한 기술 스택 및 응용 분야에서 LJack 런타임 하네스 10대 핵심 기둥을 구체적으로 적용하는 표준 패턴을 정의합니다.

---

### 1. 데스크톱 GUI / 시스템 자동화 (PyQt6 / WinForms / WPF / Electron)
* **인터랙션 시퀀스 가드**:
  - 마우스 호버 오버레이 뱃지 시 `WA_TransparentForMouseEvents` 속성을 의무 적용하여 드래그/클릭 이벤트가 가로막히지 않도록 보장.
  - 신규 개체 생성 드래그와 기존 개체 변형 조작의 FSM 상태를 명시적으로 분리.
* **비주얼 픽셀 하네스**:
  - 오프스크린 캡처(`widget.grab()`)로 다크모드 내 의도치 않은 1px 고휘도 흰색 라인(`NoFrame`, `border: none`, `drawBase: 0`) 자동 감사.
* **에셋 알파 마스크 무결성**:
  - 앱 아이콘(.ico, .png) 생성 시 스퀘어클 외곽 픽셀의 Alpha=0 투명화 및 멀티 해상도 번들링.
* **물리적 입력 자가 치유**:
  - 키보드/마우스 누름 유지 시 전역 활성 입력 추적기 및 비정상 종료 시 물리적 입력 100% 강제 해제 인터록 탑재.
* **원클릭 배포**:
  - 포터블 빌드(`_internal` 격리) 완료 즉시 GitHub Releases API로 `.zip` 바이너리 자동 등록.

---

### 2. 웹 백엔드 API (FastAPI / NestJS / Spring Boot / Express)
* **코어 분리 (Decoupling Core)**:
  - 비즈니스 도메인 서비스가 HTTP 요청 객체(`Request`), 세션, 또는 특정 ORM 모델에 직접 종속되지 않게 Clean/Hexagonal Architecture 적용.
* **헤드리스 하네스 검증**:
  - 실제 외부 DB/외부 결제 API 없이 메모리 저장소(In-Memory Mock)와 가상 이벤트 버스를 통한 0.5초 유닛/통합 테스트 러너 구축.
* **슈퍼바이저-워커 루프**:
  - 메인 API 루프는 즉시 202 Accepted를 반환하고, 장시간 소요 작업은 Celery/BullMQ/비동기 백그라운드 태스크로 분기.

---

### 3. 프론트엔드 웹 앱 (React / Vue / Next.js / Svelte)
* **상태 머신 우선 검증**:
  - UI 컴포넌트 마운트 없이 Zustand/Redux 상태 머신 및 액션 디스패처를 검증하는 Headless 단위 테스트 우선 작성.
* **비주얼 감사**:
  - 다크/라이트 테마 CSS 토큰 휘도 검사, SVG 파비콘/웹앱 아이콘 외곽 알파 투명도 검증.
* **이벤트 버블링 및 포커스 트랩**:
  - 모달 배경 클릭 시 뒤편 컴포넌트 이벤트 트리거 차단(`stopPropagation`) 및 `Escape` 키 포커스 복원 검증.
* **다중 뷰 일관성**:
  - 모바일 반응형 뷰와 데스크톱 뷰 전환 시 폼 입력 데이터 및 모달 상태 보존.

---

### 4. 데이터 파이프라인 / CLI 도구 (Python / Go / Rust)
* **코어 엔진 분리**:
  - CLI 인자 파서(argparse, clap)와 데이터 변환 파이프라인 엔진 분리.
* **인코딩 안전망**:
  - Windows 콘솔 출력 시 UTF-8 강제 설정(`sys.stdout.reconfigure(encoding='utf-8')`)으로 다국어/로그 깨짐 원천 방어.
* **비상정지 인터록**:
  - 파이프라인 처리 도중 SIGINT(`Ctrl+C`) 수신 시 안전하게 중간 체크포인트를 저장하고 종료하는 인터록 구성.

---

### 5. Rust 코어 + Python 인터페이스 이원화 하네스 (Rust-Python Hybrid Rig)
연산 집약적 로직, 상태 불변성, 고속 동시성은 **Rust 코어**로 구현하고, UI 렌더링, 이벤트 라우팅, 스크립팅은 **Python 인터페이스**로 분리하는 최상위 이원화 아키텍처입니다.

* **코어와 입출력 완전 분리 (기둥 1 & 2의 극대화)**:
  - Rust는 화면/OS/사용자 입력에 대한 의존성이 0인 순수 계산 엔진(`cdylib` / `pyo3`)으로 컴파일.
  - Python(PyQt6, Pygame, NiceGUI, CLI)은 Rust 엔진이 반환한 불변 상태를 렌더링하고 사용자 입력을 이벤트 큐로 Rust에 전달하는 순수 I/O 계층으로 동작.
* **2대 바인딩 구현 전략**:
  1. **C-ABI `ctypes` 방식 (무의존성 Fast-Path)**:
     - Rust에서 `#[repr(C)]` 구조체와 `#[no_mangle] pub extern "C"` 함수를 노출하여 `.dll` / `.so` 빌드.
     - Python 환경에 C++ 컴파일러나 추가 패키지 설치 없이 표준 라이브러리 `ctypes`만으로 즉각 로드.
  2. **`PyO3` + `maturin` 방식 (고성능 네이티브 바인딩)**:
     - 복잡한 객체 그래프나 대용량 메모리 버퍼(`PyArray`, `PyBuffer`) 공유 시 Zero-Copy 바인딩.
     - 장시간 연산 시 GIL 릴리즈(`py.allow_threads`)로 Python GUI 메인 스레드 프리징 원천 방어.
* **FFI 경계 패닉 격리 (Panic Interlock)**:
  - Rust 내부의 `panic!`이 FFI 경계를 넘어 Python 프로세스를 강제 종료(Crash)시키지 않도록 `std::panic::catch_unwind`를 적용하고 에러 코드를 반환.
* **2단계 헤드리스 테스트 파이프라인**:
  - 1단계: Rust 단독 로직 검증 (`cargo test --lib`) ➔ 메모리 상에서 0.05초 만에 10만 회 연산 검증.
  - 2단계: Python 브릿지 통합 검증 (`python tests/test_headless.py`) ➔ FFI 데이터 직렬화 및 예외 처리 검증.
