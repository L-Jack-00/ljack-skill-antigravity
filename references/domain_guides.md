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
