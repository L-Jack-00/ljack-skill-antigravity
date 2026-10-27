---
name: ljack-game
description: >-
  엘잭 게임 프로토콜 (LJack Game Protocol): 멀티 엔진 런타임 하네스 엔지니어링 및 초자율 에이전틱 개발 프로토콜 (v1.3.0).
  사용자가 '엘잭 게임', '게임 개발', '인디 게임', '게임 하네스', '상용화', '스팀 출시', 'Pygame', 'Tauri', 'HTML5 캔버스', '고도 엔진', 'Godot' 등을 요청하거나,
  결정론적 고정 틱 루프, 헤드리스 1만 틱 시뮬레이터, 사용자 플레이 검수 관문(Playable Review Gate),
  인게임 실시간 손맛 튜너(F1/F2 오버레이), 원자적 세이브(Atomic Save), 다국어(i18n) 현지화, 상용 릴리즈 닥터,
  스팀/스토브/itch.io 상용 출시 파이프라인을 원할 때 활성화합니다.
---

# 엘잭 게임 스킬 (LJack Game Protocol)
## 멀티 엔진 런타임 하네스 & 상용 인디 게임 출시 프로토콜 (v1.3.0)

> **💡 시스템 지침 (System Directive)**:  
> 본 스킬은 상용 인디 게임 제작 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/메모리)을 헤드리스 1만 틱 시뮬레이터로 100% 자가 치유하되,  
> **1) 배포 전 사용자 직접 플레이 검수(Playable Review Gate)를 통한 손맛 조율**,  
> **2) 상용 릴리즈 닥터(`game_release_doctor.py`)를 통한 세이브 원자성/다국어/디버그 봉인 점검**을 완결하도록 규정하는 최상위 게임 개발 프로토콜입니다.

> **⚠️ 버전 독립성 불변 원칙 (Version Independence Principle)**:  
> **본 프로토콜의 버전(v1.3.0)과 대상 게임의 자체 버전은 완전히 별개입니다.**  
> 대상 게임은 사용자가 명시한 버전 또는 표준 SemVer 기본값(`v0.1.0` / `v1.0.0`)부터 온전히 독립적인 생명주기를 갖습니다.

---

## 1. 멀티 엔진 게임 런타임 하네스 8대 핵심 기둥

```text
[입력 디바이스: 키보드/마우스/게임패드] ──> [입력 버퍼 큐 & Stuck 방지 가드]
                                                         │
┌────────────────────────────────────────────────────────▼──────────────────────────────┐
│                게임 런타임 하네스 코어 (Pygame / Tauri+HTML5 / Godot 4.x)             │
│                                                                                       │
│  1. 결정론적 고정 틱과 렌더링 분리 (Fixed 60Hz: Pygame Dummy / Accumulator / Physics)│
│  2. 헤드리스 1만 틱 시뮬레이터 (Headless 10k-Tick Sim Rig: 승패/밸런스 0.1초 검증)    │
│  3. 입력 버퍼링 & 안전망 (Input Buffering, Coyote Time, 전역 키 릴리즈 가드)          │
│  4. 충돌 감사 & Reachability Solver (AABB, 서브스텝, 도달 불가능한 맵 사전 감지)       │
│  5. 게임 필 & 실시간 튜너 (F1 인게임 오버레이 실시간 조절 & F2 디스크 핫저장)        │
│  6. ⭐ 플레이어블 검수 관문 (Playable Review Gate: 배포 전 사용자 직접 플레이 피드백) │
│  7. 세이브 데이터 원자적 안전망 (Atomic Save Rig: 전원 차단 시 0바이트 손상 방지)     │
│  8. 다국어 & 상용 릴리즈 봉인 (Production Seal, i18n, Steam/Tauri/Godot 원클릭 배포) │
└────────────────────────────────────────────────────────┬──────────────────────────────┘
                                                         │
         [검증 ALL PASS ➔ 사용자 플레이 검수 ➔ 상용 닥터 감사 ➔ 릴리즈 봉인]
```

- **기둥 1: 고정 틱과 렌더링 분리**: Pygame Dummy 가드, Tauri Accumulator 루프, Godot `_physics_process` 분리.
- **기둥 2: 헤드리스 1만 틱 시뮬레이터**: 렌더링 없이 1만 틱을 0.2초 만에 돌려 무한 루프, 메모리 안정성, 승패 검증.
- **기둥 3: 입력 버퍼링 & 안전망**: 프레임 드랍 시 입력 씹힘 방지 및 게임 종료 시 물리 입력 100% 해제.
- **기둥 4: 충돌 감사 & Reachability Solver**: 투사체 관통 방지 서브스텝 및 도달 불가능 발판(Unwinnable Map) 사전 감지.
- **기둥 5: 게임 필(Game Feel) & 실시간 튜너**: 코요테 타임, 점프 선입력 버퍼, **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 핫저장)** 지원.
- **기둥 6: 플레이어블 검수 관문 (Playable Review Gate)**:
  - 배포 전 사용자에게 로컬 원클릭 실행 명령과 밸런스 파라미터 요약표를 제출하고 직접 손맛 검수 수렴.
- **기둥 7: 세이브 데이터 원자적 안전망 (Atomic Save Rig)**:
  - 임시 파일 쓰기 및 `os.replace` 원자적 교체로 충돌/정전 시 세이브 파일 깨짐(Corruption) 원천 방어.
- **기둥 8: 다국어 & 상용 릴리즈 봉인 (Commercial Release Rig)**:
  - `locales/` 다국어 사전 탑재, 상용 빌드 시 `F1` 손맛 튜너 자동 봉인(`PRODUCTION_BUILD=True`), 원클릭 스팀/웹/데스크톱 배포.

---

## 2. 초자율 게임 에이전트 10대 실행 강령

1. **버전 독립성 준수**: 게임 프로토콜 버전(v1.3.0)과 대상 게임 고유 버전(`v0.1.0`)을 분리한다.
2. **엔진 생태계 적응력**: Pygame, Tauri/HTML5, Godot 4.x 중 사용자가 요청한 스택의 표준 하네스를 즉각 구축한다.
3. **기술 결함은 무중단 자가 치유한다**: 충돌 버그, 맵 차단, 무한 루프는 사용자에게 묻지 않고 1만 틱 러너로 스스로 해결한다.
4. **손맛과 재미는 반드시 사용자에게 검수받는다 (Playable Review Gate)**: 배포 전 로컬 실행 스크립트와 밸런스 수치 요약표를 사용자에게 제출하고 직접 플레이 검수를 요청한다.
5. **세이브 데이터 원자성 절대 사수**: 세이브 루틴은 반드시 원자적 교체(`os.replace`) 패턴을 적용하여 데이터 유실을 0%로 만든다.
6. **상용 빌드 디버그 봉인 의무화**: 배포 전 `PRODUCTION_BUILD` 플래그로 `[F1]` 튜너 및 치트를 봉인한다.
7. **하드코딩 텍스트 금지 (i18n 준수)**: UI와 안내 메시지는 `locales/en.json`, `locales/ko.json` 딕셔너리로 분리한다.
8. **제로-토큰 스캐폴더 즉각 활용**: `scripts/game_scaffolder.py`를 호출하여 뼈대 코드 생성 토큰 15,000개를 아낀다.
9. **상용 릴리즈 닥터 전수 검사**: 최종 릴리즈 전 `scripts/game_release_doctor.py` 80점 이상 획득을 검증한다.
10. **선제적 게임 맹점 보고**: 완료 시 `[🔭 게임 밸런스 및 상용화 확장 레이더]` 섹션을 의무 보고한다.

---

## 3. 개발자-AI 상용 게임 페어 프로그래밍 7대 마법의 검증 질문

1. **손맛/조작감**: *"점프할 때 코요테 타임이나 선입력 버퍼링이 적용되어 1프레임 차이로 조작이 씹히는 답답함이 없는가?"*
2. **세이브 안정성**: *"게임을 저장하는 찰나에 강제 종료(Alt+F4)되거나 컴퓨터가 꺼져도 이전 세이브가 손상되지 않는가?"*
3. **상용 릴리즈 봉인**: *"일반 유저에게 배포될 빌드에서 [F1] 손맛 튜너나 디버그 콘솔이 안전하게 비활성화(봉인)되어 있는가?"*
4. **다국어 현지화**: *"코드 내에 하드코딩된 한글/영어 문자열이 없으며, locales/ 사전으로 글로벌 유저를 지원할 수 있는가?"*
5. **도달 가능성(Reachability)**: *"맵의 모든 플랫폼이 현재 플레이어의 점프력으로 수학적으로 100% 도달 가능한가?"*
6. **플레이어블 검수 상태**: *"사용자가 지금 바로 로컬 명령어로 플레이해보고 [F1]으로 손맛을 튜닝할 수 있는가?"*
7. **배포 청결도**: *"상용 패키징 내에 임시 테스트 로그나 찌꺼기 파일이 단 1개도 남아있지 않은가?"*

---

## 4. 상용 게임 자율 실행 6단계 표준 파이프라인

```text
[1단계: 게임 기획 승인 & 제로-토큰 멀티엔진 스캐폴딩]
  - 엔진 스택 결정 ➔ scripts/game_scaffolder.py 호출 (세이브 매니저, 다국어 기본 탑재, 토큰 15,000개 절약)
       ↓
[2단계: 헤드리스 1만 틱 시뮬레이터 & 충돌/Reachability 하네스 구축]
  - 메모리 상에서 0.2초 만에 물리/상태 전이와 발판 도달 가능성을 검증하는 10k-Tick 러너 구축
       ↓
[3단계: 게임 메카닉, 입력 버퍼 및 렌더링/손맛 구현]
  - Fixed 60Hz 루프, 코요테 타임, 점프 선입력, F1 실시간 튜너 오버레이 탑재
       ↓
[4단계: 무중단 헤드리스 자가 치유 루프]
  - scripts/tick_sim_runner.py 가동 ➔ 1만 틱 시뮬레이션 ALL PASS (터널링 0건, 맵 도달불가 0건)
       ↓
[5단계: ⭐ 플레이어블 프리뷰 & 사용자 검수 관문 (Playable Review Gate)]
  - scripts/play_preview_launcher.py로 조작법 및 밸런스 파라미터 요약 추출
  - 🎮 사용자에게 플레이 검수 요청: "인게임에서 [F1]으로 손맛을 실시간 조절하고 [F2]로 저장할 수 있습니다"
  - 🔄 사용자 피드백 즉시 수렴 ➔ 사용자 최종 승인(Approved) 획득
       ↓
[6단계: 상용 릴리즈 닥터 검증 & 프로덕션 봉인 배포 완결]
  - scripts/game_release_doctor.py 검사 (80점 이상 통과) ➔ F1 튜너 봉인 ➔ 스팀/웹/데스크톱 원클릭 배포
```

---

## 5. 내장 자동화 도구 및 참조 레퍼런스

### 🛠️ 내장 스크립트 도구 (`scripts/`)
- `scripts/game_scaffolder.py`: Pygame, Tauri, Godot 8대 기둥 골격 및 세이브/다국어 0초 생성 (**토큰 15,000개 절감**).
- `scripts/game_release_doctor.py`: 상용 출시 준비도(0~100) 및 스팀/스토브 승인 게이트 정적 진단 닥터.
- `scripts/localization_linter.py`: 다국어(i18n) 번역 테이블 무결성 검증 및 하드코딩 텍스트 자동 추출기.
- `scripts/tick_sim_runner.py`: Reachability Solver 및 헤드리스 1만 틱 초고속 시뮬레이터.
- `scripts/play_preview_launcher.py`: 엔진 자동 감지 기반 플레이 검수 브리핑 도구.
- `scripts/web_packager.py`: WebAssembly(HTML5) 브라우저 원클릭 웹 패키저.

### 📚 심화 참조 레퍼런스 (`references/`)
- [스팀(Steam) 상용 출시 및 스팀웍스 연동 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/steam_publishing_guide.md): 원자적 세이브, Steamworks SDK, 스팀덱 최적화.
- [Tauri + HTML5/Canvas 게임 하네스 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/tauri_html5_guide.md): Accumulator 고정 틱, Node 헤드리스 테스트, Tauri 배포.
- [고도 엔진 (Godot 4.x) 게임 하네스 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/godot_engine_guide.md): _physics_process 분리, `--headless` 1만 틱, CanvasLayer F1 튜너.
- [게임 필(Game Feel) & 손맛 튜닝 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/game_feel_tuning.md): 코요테 타임, 점프 버퍼링, 히트스톱 공식.
- [충돌 판정 및 물리 터널링 방지 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/collision_and_physics.md): AABB 충돌 및 서브스텝 구현 명세.

---

## 6. 프로토콜 버전 진화 이력

- **v1.0.0**: 게임 런타임 하네스 8대 기둥, 헤드리스 1만 틱 러너, 플레이어블 검수 관문(Playable Review Gate).
- **v1.1.0**: 인게임 실시간 손맛 튜너 (F1/F2 오버레이), Pygame 더미 가드, Reachability Solver(도달 불가 맵 방지), WebAssembly 패키저.
- **v1.2.0**: 멀티 엔진 생태계 전격 지원 (Pygame, Tauri/HTML5, Godot 4.x), 엔진 자동 감지 검수기.
- **v1.3.0 (Current - Commercial Edition)**:
  - **원자적 세이브 안전망 (Atomic Save Rig)**: 정전/강제종료 시 세이브 깨짐 0% 보장.
  - **상용 릴리즈 닥터 (`game_release_doctor.py`)**: 상용 품질(0~100) 및 스팀 출시 게이트 정적 진단.
  - **다국어(i18n) 현지화 린터 (`localization_linter.py`)**: 글로벌 스팀 출시를 위한 다국어 무결성 가드.
  - **스팀 상용 출시 레퍼런스 (`steam_publishing_guide.md`)**: Steamworks SDK 및 스팀덱 대응 공식 수록.
