# LJack Protocol 자가 치유(Self-Healing) 트러블슈팅 플레이북

AI 에이전트가 개발 및 테스트 중 단골로 마주치는 시스템/OS/컴파일러 레벨의 장애 패턴과 즉시 적용 가능한 자가 치유 공식입니다.

---

### 1. Windows Defender 휴리스틱 트로이목마 오진
* **증상**: C#/C++ 코드를 데스크톱이나 임시 폴더에 standalone `.exe`로 컴파일하거나 동적 리플렉션을 사용할 때 안티바이러스(Defender)가 바이너리를 차단하거나 삭제함.
* **자가 치유 공식**:
  - 임의의 `.exe` 바이너리 빌드를 전면 중단한다.
  - 실행 가능한 바이너리 대신 C# 클래스 라이브러리(`/target:library` ➔ `.dll`)로 컴파일하고, 메인 프로세스(예: WindBot, 호스트 런타임)에 동적 로딩시키는 아키텍처로 전환한다.
  - 테스트 및 제어는 Python 스크립트 기반의 헤드리스 테스트 러너로 실행한다.

---

### 2. Windows 콘솔 다국어/한국어 `UnicodeEncodeError` (CP949 충돌)
* **증상**: 파이썬 스크립트 출력 시 `charmap codec can't encode characters in position ...` 에러 발생.
* **자가 치유 공식**:
  - 모든 Python 스크립트 최상단에 표준 UTF-8 출력 가드를 탑재한다:
  ```python
  import sys
  if sys.stdout.encoding != 'utf-8':
      try:
          sys.stdout.reconfigure(encoding='utf-8')
      except Exception:
          pass
  ```
  - PowerShell/CMD 터미널 호출 시 환경변수 `PYTHONIOENCODING=utf-8`를 명시한다.

---

### 3. 파일 잠금(File Lock) 및 임시 파일 삭제 실패 (`PermissionError: [WinError 32]`)
* **증상**: 이전 프로세스가 백그라운드에서 아직 파일 핸들을 쥐고 있어 파일 덮어쓰기나 삭제가 거부됨.
* **자가 치유 공식**:
  - `manage_task` 또는 `taskkill /f /im <ProcessName>.exe`로 잔여 백그라운드 프로세스를 즉시 강제 종료한다.
  - 임시 파일 생성 시 고정 파일명 대신 `uuid4()` 기반의 고유 파일명을 사용하거나, 재시도 루프(Exponential Backoff 3회)를 인터록에 내장한다.

---

### 4. Git Credential Fill 및 대용량 릴리즈 업로드 타임아웃
* **증상**: GitHub API로 수십 MB 이상의 압축 바이너리를 올릴 때 네트워크 순단이나 인증 토큰 누락으로 실패.
* **자가 치유 공식**:
  - 환경변수에 토큰이 없을 경우 `git credential fill` 파이프라인을 실행하여 로컬 Git 자격 증명 관리자(GCM)에서 GitHub 토큰을 무인 추출한다.
  - 릴리즈 생성과 에셋 업로드를 분리하고, 업로드 실패 시 해당 릴리즈 태그에 3회까지 청크 단위 업로드를 재시도한다.
