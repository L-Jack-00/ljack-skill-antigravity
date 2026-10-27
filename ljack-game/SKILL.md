---
name: ljack-game
description: >-
  엘잭 게임 프로토콜 (LJack Game Protocol): 멀티 엔진 런타임 하네스 엔지니어링 및 초자율 에이전틱 개발 프로토콜 (v1.2.0).
  사용자가 '엘잭 게임', '게임 개발', '인디 게임', '게임 하네스', 'Pygame', 'Tauri', 'HTML5 캔버스', '고도 엔진', 'Godot' 등을 요청하거나,
  결정론적 고정 틱 루프, 헤드리스 1만 틱 시뮬레이터, 사용자 플레이 검수 관문(Playable Review Gate),
  인게임 실시간 손맛 튜너(F1/F2 오버레이), 도달 가능성(Reachability) 맵 감사, 충돌 터널링 방지,
  Pygame/Tauri/Godot 원클릭 웹 및 데스크톱 배포를 원할 때 활성화합니다.
---

# 엘잭 게임 스킬 (LJack Game Protocol)
## 멀티 엔진 런타임 하네스 엔지니어링 & 초자율 에이전틱 개발 프로토콜 (v1.2.0)

> **💡 시스템 지침 (System Directive)**:  
> 본 스킬은 게임 제작 시 AI 에이전트가 기술적 결함(물리/충돌/터널링/도달불가/메모리)을 헤드리스 1만 틱 시뮬레이터로 100% 자가 치유하되,  
> **최종 패키징 배포 전 반드시 사용자에게 인게임 실시간 손맛 튜너(F1)와 함께 [플레이어블 프리뷰 & 사용자 검수 관문 (Playable Review Gate)]을 열어 피드백을 수렴**하도록 규정하는 최상위 게임 개발 프로토콜입니다.

> **⚠️ 버전 독립성 불변 원칙 (Version Independence Principle)**:  
> **본 프로토콜의 버전(v1.2.0)과 대상 게임의 자체 버전은 완전히 별개입니다.**  
> 대상 게임은 사용자가 명시한 버전 또는 표준 SemVer 기본값(`v0.1.0` / `v1.0.0`)부터 온전히 독립적인 생명주기를 갖습니다.

---

## 1. 멀티 엔진 게임 런타임 하네스 8대 핵심 기둥

게임 하네스는 불규칙한 FPS와 입력 속에서도 게임 로직이 예측 가능하고 결정론적으로 구동되도록 감싸주는 **실행 및 시뮬레이션 뼈대**입니다.

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
│  7. 세이브 데이터 스키마 버전 안전망 (Save State Migration Guard)                     │
│  8. 에셋 알파 무결성 & 원클릭 배포 (Pybag Web / Tauri Desktop / Godot Export)        │
└────────────────────────────────────────────────────────┬──────────────────────────────┘
                                                         │
                      [검증 ALL PASS ➔ 사용자 플레이 검수 ➔ 최종 패키징]
```

- **기둥 1: 고정 틱과 렌더링 분리**:
  - *Pygame*: `clock.tick(60)` & `SDL_VIDEODRIVER=dummy` 헤드리스 가드.
  - *Tauri / HTML5*: `requestAnimationFrame` 가변 FPS 속에서 $\Delta t = 1/60$ 누적기(Accumulator) 루프.
  - *Godot 4.x*: `_physics_process(delta)` 물리 연산과 `_process(delta)` 렌더링 보간 완전 분리.
- **기둥 2: 헤드리스 1만 틱 시뮬레이터**: 화면 렌더링 없이 메모리 상에서 1만 번의 틱을 0.2초 만에 돌려 승패 도달 가능성, 점수, 메모리 안정성 자가 검증.
- **기둥 3: 입력 버퍼링 & 안전망**: 프레임 드랍 시 입력 씹힘 방지 및 게임 일시정지/종료 시 물리 입력 100% 해제.
- **기둥 4: 충돌 감사 & Reachability Solver**: 투사체 터널링 방지 서브스텝 및 점프 궤적 수식 기반 **클리어 불가능한 맵(Unwinnable Map) 사전 감지**.
- **기둥 5: 게임 필(Game Feel) & 실시간 튜너**: 코요테 타임(6틱), 점프 선입력 버퍼(6틱), **인게임 실시간 손맛 튜너([F1] 오버레이, [F2] 디스크 핫저장)** 지원.
- **기둥 6: 플레이어블 검수 관문 (Playable Review Gate)**:
  - 헤드리스 검증 ALL PASS 완료 후, 최종 배포 전 반드시 로컬 원클릭 실행 방법과 현재 밸런스 파라미터 요약표를 사용자에게 제시.
  - 사용자의 손맛/난이도 피드백(실시간 튜너 활용)을 반영하여 최종 승인(Approved) 시에만 배포 단계로 전진.
- **기둥 7: 세이브 데이터 버전 안전망**: 세이브 파일 JSON/CFG 포맷 변경 시 이전 데이터 자동 마이그레이션.
- **기둥 8: 에셋 알파 무결성 & 멀티엔진 원클릭 배포**: WebAssembly/HTML5 웹 패키징, Tauri 10MB 단일 EXE, Godot CLI 바이너리 배포.

---

## 2. 초자율 게임 에이전트 10대 실행 강령

1. **버전 독립성 준수**: 게임 프로토콜 버전(v1.2.0)과 대상 게임 고유 버전(`v0.1.0`)을 분리한다.
2. **엔진 생태계 적응력**: Pygame, Tauri/HTML5, Godot 4.x 중 사용자가 요청한 스택의 표준 하네스를 즉각 구축한다.
3. **기술 결함은 무중단 자가 치유한다**: 충돌 버그, 맵 차단, 무한 루프는 사용자에게 묻지 않고 1만 틱 러너로 스스로 해결한다.
4. **손맛과 재미는 반드시 사용자에게 검수받는다 (Playable Review Gate)**:  
   - 기술 테스트가 끝나면 **배포 전에 반드시 로컬 실행 스크립트와 밸런스 수치 요약표를 사용자에게 제출하고 직접 플레이 검수를 요청**한다.
   - 사용자 피드백(점프 높이, 적 스피드 등)을 수렴하여 파라미터를 튜닝한 뒤 최종 승인을 받는다.
5. **제로-토큰 스캐폴더 즉각 활용**: `scripts/game_scaffolder.py --type pygame|tauri|godot`를 호출하여 뼈대 코드 생성 토큰 15,000개를 아낀다.
6. **결정론적 고정 틱 원칙**: 프레임레이트(FPS)가 변해도 캐릭터 이동 속도와 물리 궤적은 100% 동일해야 한다.
7. **물리 터널링 & 도달 불가 맵 절대 금지**: 서브스텝 충돌 검사 및 Reachability Solver 수학 검증을 의무 적용한다.
8. **5대 손맛 레시피 기본 탑재**: 코요테 타임, 점프 버퍼링, 낙하 가속, 히트스톱, 스크린 셰이크를 고려한다.
9. **사용자 표면 UX 카피 정제**: 게임 내 UI 및 상태창에 개발자 내부 은어가 노출되지 않도록 한다.
10. **선제적 게임 맹점 보고**: 완료 시 `[🔭 게임 밸런스 및 확장 제안 레이더]` 섹션을 의무 보고한다.

---

## 3. 개발자-AI 게임 페어 프로그래밍 6대 마법의 검증 질문

1. **손맛/조작감**: *"점프할 때 코요테 타임이나 선입력 버퍼링이 적용되어 있어 1프레임 차이로 조작이 씹히는 답답함이 없는가?"*
2. **물리 터널링 & 도달 가능성**: *"최고 속도로 돌진할 때 벽을 뚫는 현상이 없으며, 맵의 모든 발판이 수학적으로 도달 가능한 거리/높이에 있는가?"*
3. **1만 틱 밸런스 내구성**: *"헤드리스로 1만 번 돌렸을 때 점수가 오버플로우되거나 클리어 불가능한 데드락 상태에 빠지지 않는가?"*
4. **엔진 네이티브 호환성**: *"Pygame 더미 가드, Tauri IPC 바인딩, Godot _physics_process가 환경에 구애받지 않고 무중단 실행되는가?"*
5. **플레이어블 검수 상태**: *"사용자가 지금 바로 로컬 명령어로 플레이해보고 [F1]으로 손맛을 튜닝할 수 있는 상태가 준비되었는가?"*
6. **배포 완성도**: *"패키징 시 불필요한 테스트 코드나 임시 파일 없이 단일 포터블 번들 또는 웹 포털로 구동되는가?"*

---

## 4. 게임 자율 실행 6단계 표준 파이프라인

```text
[1단계: 게임 기획 승인 & 제로-토큰 멀티엔진 스캐폴딩]
  - 엔진 스택(Pygame / Tauri / Godot) 결정 ➔ scripts/game_scaffolder.py 호출 (토큰 15,000개 절약)
       ↓
[2단계: 헤드리스 1만 틱 시뮬레이터 & 충돌/Reachability 하네스 구축]
  - 메모리 상에서 0.2초 만에 물리/상태 전이와 발판 도달 가능성을 검증하는 10k-Tick 러너 구축
       ↓
[3단계: 게임 메카닉, 입력 버퍼 및 렌더링/손맛 구현]
  - Fixed 60Hz 루프, 코요테 타임, 점프 선입력, 타격 피드백(Juice), F1 실시간 튜너 오버레이 탑재
       ↓
[4단계: 무중단 헤드리스 자가 치유 루프]
  - scripts/tick_sim_runner.py 가동 ➔ 1만 틱 시뮬레이션 ALL PASS (터널링 0건, 맵 도달불가 0건)
       ↓
[5단계: ⭐ 플레이어블 프리뷰 & 사용자 검수 관문 (Playable Review Gate)]
  - scripts/play_preview_launcher.py로 조작법 및 밸런스 파라미터 요약 추출
  - 🎮 사용자에게 플레이 검수 요청: "인게임에서 [F1]으로 손맛을 실시간 조절하고 [F2]로 저장할 수 있습니다"
  - 🔄 사용자 피드백 즉시 수렴 ➔ 사용자 최종 승인(Approved) 획득
       ↓
[6단계: 원클릭 포터블 & Web 배포 완결]
  - Pygbag Web, Tauri Build, Godot Export로 원클릭 번들링 ➔ 잠재 게임 확장 레이더 보고 후 완료
```

---

## 5. 내장 자동화 도구 및 참조 레퍼런스

### 🛠️ 내장 스크립트 도구 (`scripts/`)
- `scripts/game_scaffolder.py`: Pygame, Tauri, Godot 8대 기둥 골격 및 F1 튜너 0초 생성 (**토큰 15,000개 절감**).
- `scripts/tick_sim_runner.py`: Reachability Solver 및 헤드리스 1만 틱 초고속 시뮬레이터.
- `scripts/play_preview_launcher.py`: 엔진 자동 감지 기반 사용자 플레이 검수 브리핑 도구.
- `scripts/web_packager.py`: WebAssembly(HTML5) 브라우저 원클릭 웹 패키저.

### 📚 심화 참조 레퍼런스 (`references/`)
- [Tauri + HTML5/Canvas 게임 하네스 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/tauri_html5_guide.md): Accumulator 고정 틱, Node 헤드리스 테스트, Tauri 배포.
- [고도 엔진 (Godot 4.x) 게임 하네스 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/godot_engine_guide.md): _physics_process 분리, `--headless` 1만 틱, CanvasLayer F1 튜너.
- [게임 필(Game Feel) & 손맛 튜닝 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/game_feel_tuning.md): 코요테 타임, 점프 버퍼링, 히트스톱 공식.
- [충돌 판정 및 물리 터널링 방지 가이드](file:///C:/Users/SBK/.gemini/config/skills/ljack-game/references/collision_and_physics.md): AABB 충돌 및 서브스텝 구현 명세.

---

## 6. 프로토콜 버전 진화 이력

- **v1.0.0**: 게임 런타임 하네스 8대 기둥, 헤드리스 1만 틱 러너, 플레이어블 검수 관문(Playable Review Gate).
- **v1.1.0**: 인게임 실시간 손맛 튜너 (F1/F2 오버레이), Pygame 더미 가드, Reachability Solver(도달 불가 맵 방지), WebAssembly 패키저.
- **v1.2.0 (Current)**:
  - **멀티 엔진 생태계 전격 지원 (Pygame + Tauri/HTML5 + Godot 4.x)**: 3대 엔진별 고정 틱 루프, 헤드리스 1만 틱 러너, F1 튜너 스캐폴딩 내장.
  - **엔진 자동 감지 검수 도구 (`play_preview_launcher.py`)**: Pygame, Tauri, Godot 프로젝트 자동 식별 및 실행 브리핑 지원.
  - **심화 엔진 레퍼런스 번들링**: `tauri_html5_guide.md`, `godot_engine_guide.md` 추가.
