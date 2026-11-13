# 엘잭 스킬 (LJack Protocol)
## 범용 런타임 하네스 엔지니어링 & 자율 에이전틱 개발 프로토콜 (v7.5.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-7.5.0-green.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 모듈은 AI 에이전트가 소프트웨어 개발 시 사소한 기술 확인을 위해 중간에 멈추지 않고,  
견고한 **[설계/톤앤매너 고정 ➔ 스캐폴딩 ➔ 코딩 ➔ 자체 테스트 ➔ 자가 치유(Self-Healing) ➔ 비주얼/인터랙션/닥터/UX카피 감사 ➔ 격리 패키징 및 배포 준비]**까지 단일 흐름으로 완주하도록 규정하는 범용 아키텍처 프로토콜입니다.

> **⚠️ 버전 독립성 불변 원칙 (Version Independence Principle)**:  
> 본 프로토콜의 버전(v7.5.0)과 대상 프로젝트(응용프로그램)의 자체 버전은 완전히 별개입니다.  
> 에이전트는 프로젝트 착수 시 절대로 스킬의 버전 번호를 대상 소프트웨어의 버전이나 파일명에 투영하지 않으며, 대상 소프트웨어 고유의 버전 로드맵(SemVer 기본값 `v1.0.0`)을 독립적으로 유지합니다.

---

## 📂 저장소 및 모듈 구조 (v7.5.0)

```text
ljack-skill/
├── SKILL.md                          # [코어 지침] 10대 기둥, 11대 강령, 5단계 파이프라인
├── README.md                         # 저장소 안내 및 설치/동기화 가이드
├── scripts/                          # [내장 자동화 도구 및 린터]
│   ├── harness_scaffolder.py         # 10대 기둥 골격 즉시 생성 (CLI, Desktop, API, Rust-Python Hybrid)
│   ├── harness_doctor.py             # AST 정적 분석 기반 하네스 건강 점수(0~100) 및 핵심 진단
│   ├── ux_copy_linter.py             # UI 표면 개발자 은어 및 주석 내 작업 메모 자동 스캔
│   ├── release_cleaner.py            # 배포 전 임시 로그 소거 및 아티팩트 청결화
│   └── pixel_luminance_guard.py      # 오프스크린 1px 고휘도 테두리 및 알파 마스크 검증
└── references/                       # [심화 도메인 레퍼런스]
    ├── rea_cleanroom.md              # REA 연계 클린룸 역공학 가이드
    ├── domain_guides.md              # PyQt6/데스크톱, Web, Data Pipeline, Rust-Python Hybrid 구현 레시피
    └── troubleshooting_playbook.md   # Windows Defender, CP949 인코딩 안전망, 독자 중심 주석/README 가이드
```

---

## 🚀 다른 컴퓨터에서 설치 및 동기화 방법

본 스킬은 `ljack-skill-antigravity` 모노레포 하위 폴더(`ljack-skill/`)로 관리됩니다. 아래 스크립트로 전역 스킬 디렉토리에 설치/동기화하세요.

### Windows (PowerShell)
```powershell
$repoUrl = "https://github.com/L-Jack-00/ljack-skill-antigravity.git"
$targetDir = "$HOME\.gemini\config\skills\ljack-skill"
$tempClone = "$env:TEMP\ljack-suite-sync"

if (Test-Path $tempClone) { Remove-Item -Recurse -Force $tempClone }
git clone --depth 1 $repoUrl $tempClone
New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
Copy-Item -Path "$tempClone\ljack-skill\*" -Destination $targetDir -Recurse -Force
Remove-Item -Recurse -Force $tempClone
```

### Mac / Linux (Bash)
```bash
repoUrl="https://github.com/L-Jack-00/ljack-skill-antigravity.git"
targetDir="$HOME/.gemini/config/skills/ljack-skill"
tempClone="/tmp/ljack-suite-sync"

rm -rf "$tempClone"
git clone --depth 1 "$repoUrl" "$tempClone"
mkdir -p "$targetDir"
cp -r "$tempClone/ljack-skill/"* "$targetDir/"
rm -rf "$tempClone"
```

---

## 🏛️ 런타임 하네스 엔지니어링 10대 핵심 기둥

1. **코어와 입출력 분리 (Decoupling Core from I/O)**: 비즈니스 로직과 외부 UI/하드웨어 인터페이스 분리 (Rust+Python 이원화 지원)
2. **슈퍼바이저-워커 모델 (Supervisor-Worker Model)**: 블로킹 없는 가벼운 메인 감시 루프 및 비동기 워커 분기
3. **명시적 상태(FSM)와 공유 컨텍스트(Blackboard)**: 예측 가능한 단일 상태 소유권 및 다중 조건 평가
4. **이벤트 기반 유휴 동결 및 비상정지 (Lifecycle & Safety Interlock)**: Busy-waiting 없는 이벤트 대기(`Event.wait`) 및 최우선 비상정지
5. **다중 뷰 조작 일관성 및 상태 보존 (Interaction Invariance)**: 뷰 모드 간 단축키·좌표·선택 상태 보존
6. **물리적 입력 자가 치유 & 저수준 훅 인터록 (Physical Input Safety)**: 비정상 종료 시 물리 키·마우스 전역 해제 가드 및 OS 훅 바인딩
7. **릴리즈 청결화, 격리, 독자 중심 UX 카피 & 배포 자동화 (CD Rig)**: UI 은어 차단, 주석/README 독자 중심 3불 원칙, `_internal/` 격리 번들링, GitHub Release 자동화
8. **선제적 맹점 레이더 & 폐루프 타이밍 보정 (Closed-Loop Timing)**: 실시간 루프의 OS 타이머 드리프트 감산 보정 및 잠재 맹점 보고
9. **[GUI] 비주얼 회귀 & 픽셀 휘도 감사 하네스 (Visual & Pixel Rig)**: 오프스크린 캡처를 통한 다크/라이트 테마 1px 휘도 린터
10. **[GUI] 인터랙션 시퀀스 상태 검증 (Event Sequence Rig)**: 마우스 호버-드래그-팝업닫기-외부클릭 연속 조작 시퀀스 검증

---

## 💡 개발자-AI 7대 마법의 검증 질문

1. **맹점 발굴**: *"시니어 시스템 엔지니어 입장에서 내가 배경지식이 없어 놓친 OS/하드웨어 레벨의 맹점(Unknown Unknowns)이나 안티패턴 3가지를 짚어줘."*
2. **부하/내구성 검증**: *"이 코드가 장기 실행 환경이나 대량 연속 요청, 극단적인 부하를 받으면 가장 먼저 터질 메모리 누수나 병목이 어디야?"*
3. **아키텍처 비판**: *"이 구현을 시니어 아키텍트 관점의 악마의 대변인(Devil's Advocate) 입장에서 비판해줘."*
4. **비주얼/UI 완성도 검증**: *"다크모드/고대비 모드나 다양한 DPI 해상도 환경에서 1px이라도 튀거나 어색해 보이는 네이티브 스타일 잔재나 모서리 알파 결함이 없는지 점검해줘."*
5. **인터랙션/시퀀스 조작 검증**: *"사용자가 마우스를 빠르게 호버-드래그하거나 팝업을 닫고 클릭하는 등의 불규칙한 조작 시퀀스나 단축키 충돌에서 터질 수 있는 엣지 케이스를 점검해줘."*
6. **클린룸/역공학 경계 검증**: *"이 구현에서 외부 바이너리나 상용 프로그램을 역공학(REA)해야 할 비공개 독자 부품이 있는가, 아니면 표준 알고리즘 기반으로 순방향 구현하는 것이 속도와 유지보수 면에서 유리한가?"*
7. **UX 카피 및 독자 중심 문서화 검증**: *"이 프로그램의 윈도우 제목, 메뉴, 툴팁, 안내 팝업뿐 아니라 코드 주석과 README에 'vX.X 버그 수정', '임시 땜질', 'AI 생성 코드'처럼 제3자가 보았을 때 맥락을 알 수 없는 과거 변경점 위주의 텍스트가 남아있지 않은가? 처음 프로젝트를 접한 협업자나 사용자가 보아도 목적(Why)과 기능(What)을 즉시 이해할 수 있는 독자 중심 문서로 다듬어졌는지 점검해줘."*
