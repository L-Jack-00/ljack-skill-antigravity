# 엘잭 스킬 (LJack Protocol)
## 범용 런타임 하네스 엔지니어링 & 초자율 에이전틱 개발 프로토콜 (v5.4.0)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://deepmind.google/technologies/antigravity/)
[![Version](https://img.shields.io/badge/Version-5.4.0-green.svg)](#)
[![License](https://img.shields.io/badge/License-Private-red.svg)](#)

본 저장소는 Google Antigravity(AGY) 환경에서 AI 에이전트가 사소한 확인을 위해 중간에 멈추지 않고,  
견고한 **[설계 ➔ 코딩 ➔ 빌드 ➔ 자체 테스트 ➔ 자가 치유(Self-Healing) ➔ 종합 감사 ➔ 패키징]**까지 단일 흐름으로 완주하도록 규정하는 최상위 아키텍처 및 자율 실행 프로토콜입니다.

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

## 🏛️ 런타임 하네스 엔지니어링 8대 핵심 기둥

1. **코어와 입출력 분리 (Decoupling Core from I/O)**: 비즈니스 로직과 외부 UI/하드웨어 인터페이스 분리
2. **슈퍼바이저-워커 모델 (Supervisor-Worker Model)**: 블로킹 없는 가벼운 메인 감시 루프 및 비동기 워커 분기
3. **명시적 상태(FSM)와 공유 컨텍스트(Blackboard)**: 예측 가능한 단일 상태 소유권 및 다중 조건 평가
4. **무부하 라이프사이클 및 안전 인터록 (Lifecycle & Safety Interlock)**: CPU 0% 동결(Pause) 및 최우선 비상정지
5. **다중 뷰 조작 일관성 및 상태 보존 (Interaction Invariance)**: 뷰 모드 간 단축키 100% 보존 및 좌표 불변성
6. **물리적 입력 자가 치유 & 저수준 훅 인터록 (Physical Input Safety)**: Stuck 방지 전역 해제 가드 및 OS 훅 가로채기
7. **릴리즈 아티팩트 청결화 & 서페이스 격리 (Release Sanitization)**: Mock 하네스 프로덕션 격리 및 테스트 로그 자동 소거
8. **선제적 맹점 레이더 & 폐루프 엔지니어링 (Closed-Loop Timing)**: 연산 소요 시간 및 OS 스케줄러 오차 피드백 감산 보정

---

## 💡 개발자-AI 3대 마법의 검증 질문

1. **맹점 발굴**: *"시니어 시스템 엔지니어 입장에서 내가 배경지식이 없어 놓친 OS/하드웨어 레벨의 맹점(Unknown Unknowns)이나 안티패턴 3가지를 짚어줘."*
2. **부하/내구성 검증**: *"이 코드가 프로덕션 환경에서 10만 번 연속으로 돌거나 극단적인 부하를 받으면 가장 먼저 터질 병목이 어디야?"*
3. **아키텍처 비판**: *"이 구현을 시니어 아키텍트 관점의 악마의 대변인(Devil's Advocate) 입장에서 비판해줘."*
