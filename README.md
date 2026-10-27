# 엘잭 스킬 (LJack Protocol)
## 범용 런타임 하네스 엔지니어링 & 초자율 에이전틱 개발 프로토콜 (v7.4.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-7.4.0-green.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 Google Antigravity(AGY) 환경에서 AI 에이전트가 사소한 확인을 위해 중간에 멈추지 않고,  
견고한 **[설계/톤앤매너 고정 ➔ 스캐폴딩 ➔ 코딩 ➔ 자체 테스트 ➔ 자가 치유(Self-Healing) ➔ 비주얼/인터랙션/닥터/UX카피 감사 ➔ 격리 패키징 ➔ 원클릭 GitHub 릴리즈]**까지 단일 흐름으로 완주하도록 규정하는 최상위 아키텍처 및 자율 실행 프로토콜입니다.

> **⚠️ 버전 독립성 불변 원칙 (Version Independence Principle)**:  
> 본 프로토콜의 버전(v7.4.0)과 대상 프로젝트(응용프로그램)의 자체 버전은 완전히 별개입니다.  
> 에이전트는 프로젝트 착수 시 절대로 스킬의 버전 번호를 대상 소프트웨어의 버전이나 파일명에 투영하지 않으며, 대상 소프트웨어 고유의 버전 로드맵(SemVer 기본값 `v1.0.0`)을 독립적으로 유지합니다.

---

## 📂 저장소 및 모듈 구조 (v7.4.0 Optimized)

```text
ljack-skill/
├── SKILL.md                          # [Fast-Path 코어] 10대 기둥, 11대 강령, 5단계 파이프라인
├── README.md                         # 저장소 안내 및 설치/동기화 가이드
├── scripts/                          # [내장 자동화 도구 및 린터]
│   ├── harness_scaffolder.py         # [신설] 10대 기둥 골격 0초 생성 (LLM 생성 토큰 12,000개 절감)
│   ├── harness_doctor.py             # [신설] AST 정적 분석 기반 하네스 건강 점수(0~100) 및 3줄 진단
│   ├── ux_copy_linter.py             # UI 표면 개발자 은어 0.1초 전수 검출 린터
│   ├── release_cleaner.py            # 배포 전 임시 로그 소거 및 아티팩트 청결화
│   └── pixel_luminance_guard.py      # 오프스크린 1px 고휘도 테두리 및 알파 마스크 검증
└── references/                       # [심화 도메인 레퍼런스 (토큰 60% 절약)]
    ├── rea_cleanroom.md              # REA(rea-sbk) 연계 클린룸 역공학 가이드
    ├── domain_guides.md              # PyQt6, Web, Data Pipeline별 구현 레시피
    └── troubleshooting_playbook.md   # Windows Defender, CP949 인코딩 등 자가 치유 공식
```

---

## 🚀 다른 컴퓨터에서 설치 및 동기화 방법

새로운 컴퓨터(노트북, 회사 PC 등)에서 본 스킬을 사용하려면 전역 스킬 폴더에 복제(Clone)합니다:

### Windows (PowerShell)
```powershell
# 스킬 폴더가 없으면 생성 후 Clone
git clone https://github.com/L-Jack-00/ljack-skill-antigravity.git "$HOME\.gemini\config\skills\ljack-skill"
```

### Mac / Linux
```bash
git clone https://github.com/L-Jack-00/ljack-skill-antigravity.git ~/.gemini/config/skills/ljack-skill
```

### 업데이트 동기화 (새 버전 반영)
```bash
cd ~/.gemini/config/skills/ljack-skill
git pull
```

---

## 🏛️ 런타임 하네스 엔지니어링 10대 핵심 기둥

1. **코어와 입출력 분리 (Decoupling Core from I/O)**: 비즈니스 로직과 외부 UI/하드웨어 인터페이스 분리
2. **슈퍼바이저-워커 모델 (Supervisor-Worker Model)**: 블로킹 없는 가벼운 메인 감시 루프 및 비동기 워커 분기
3. **명시적 상태(FSM)와 공유 컨텍스트(Blackboard)**: 예측 가능한 단일 상태 소유권 및 다중 조건 평가
4. **무부하 라이프사이클 및 안전 인터록 (Lifecycle & Safety Interlock)**: CPU 0% 동결(Pause) 및 최우선 비상정지
5. **다중 뷰 조작 일관성 및 상태 보존 (Interaction Invariance)**: 뷰 모드 간 단축키 100% 보존 및 좌표 불변성
6. **물리적 입력 자가 치유 & 저수준 훅 인터록 (Physical Input Safety)**: Stuck 방지 전역 해제 가드 및 OS 훅 가로채기
7. **릴리즈 청결화, 데이터 격리, UX 카피 무결성 & 원클릭 GitHub 배포 (GitHub CD Rig)**: UI 개발자 은어 차단 및 유저 친화적 텍스트 강제, `_internal/` 격리 번들링, GitHub Releases 원클릭 바이너리 자동 퍼블리싱
8. **선제적 맹점 레이더 & 폐루프 엔지니어링 (Closed-Loop Timing)**: 연산 소요 시간 및 OS 스케줄러 오차 피드백 감산 보정
9. **헤드리스 비주얼 회귀 & 픽셀 휘도 감사 하네스 (Visual & Pixel Rig)**: 오프스크린 캡처를 통한 다크/라이트 테마 1px 휘도 린터
10. **인터랙션 시퀀스 상태 머신 합성 하네스 (Event Sequence Rig)**: 마우스 호버-드래그-팝업닫기-외부클릭 연속 조작 시퀀스 자동 검증

---

## 💡 개발자-AI 7대 마법의 검증 질문

1. **맹점 발굴**: *"시니어 시스템 엔지니어 입장에서 내가 배경지식이 없어 놓친 OS/하드웨어 레벨의 맹점(Unknown Unknowns)이나 안티패턴 3가지를 짚어줘."*
2. **부하/내구성 검증**: *"이 코드가 프로덕션 환경에서 10만 번 연속으로 돌거나 극단적인 부하를 받으면 가장 먼저 터질 병목이 어디야?"*
3. **아키텍처 비판**: *"이 구현을 시니어 아키텍트 관점의 악마의 대변인(Devil's Advocate) 입장에서 비판해줘."*
4. **비주얼/UI 완성도 검증**: *"다크모드/고대비 모드나 특이 해상도 환경에서 1px이라도 튀거나 어색해 보이는 네이티브 스타일 잔재나 모서리 알파 결함이 없는지 헤드리스 픽셀 관점에서 점검해줘."*
5. **인터랙션/시퀀스 조작 검증**: *"사용자가 마우스를 빠르게 호버-드래그하거나 팝업을 닫고 클릭하는 등의 불규칙한 조작 시퀀스(Interaction Sequence)나 단축키 충돌에서 터질 수 있는 엣지 케이스를 점검해줘."*
6. **클린룸/역공학 경계 검증**: *"이 구현에서 외부 바이너리나 상용 프로그램을 역공학(REA)해야 할 비공개 독자 부품이 있는가, 아니면 표준 알고리즘 기반으로 LJack 순방향 하네스를 짜는 것이 토큰과 개발 속도 면에서 압도적으로 유리한가?"*
7. **UX 카피 및 사용자 표면 언어 검증**: *"이 프로그램의 윈도우 제목, 메뉴, 툴팁, 안내 팝업, 릴리즈 노트에 '하네스/인터록/FSM/자가치유/AI' 같은 개발자 내부 구현 용어나 수정점 텍스트가 날것 그대로 노출되어 있지는 않은가? 일반 사용자가 보았을 때 직관적이고 친절한 기능 중심의 언어로 다듬어졌는지 UX 카피 감시 에이전트 관점에서 점검해줘."*
