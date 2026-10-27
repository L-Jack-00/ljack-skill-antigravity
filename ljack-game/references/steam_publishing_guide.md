# LJack Game Protocol: 스팀(Steam) 상용 출시 및 스팀웍스 연동 가이드

스팀(Steam), 스토브(Stove), itch.io 등 글로벌 상용 플랫폼에 인디 게임을 정식 런칭할 때 필수적으로 거쳐야 하는 4대 상용화 체크리스트와 구현 명세입니다.

---

### 1. 세이브 데이터 원자적 저장 (Atomic Save Rig & Steam Cloud)
- **증상**: 플레이 도중 정전, 강제 종료(`Alt+F4`), 또는 스팀 클라우드 동기화 도중 프로세스가 끊기면 기존 세이브 파일이 0바이트로 손상(Corruption)되어 유저 데이터가 영구 증발함.
- **원자적 저장 표준 공식 (Atomic Write-and-Replace)**:
```python
import os
import json
import tempfile

def save_game_atomic(save_path: str, data: dict):
    dir_name = os.path.dirname(os.path.abspath(save_path))
    os.makedirs(dir_name, exist_ok=True)

    # 1. 임시 파일에 먼저 100% 안전하게 직렬화
    temp_file = tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8")
    try:
        json.dump(data, temp_file, indent=2, ensure_ascii=False)
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()

        # 2. OS 레벨에서 원자적 교체 (중간 정전 시에도 이전 세이브 파일 보존)
        os.replace(temp_file.name, save_path)
    except Exception as e:
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
        raise e
```
- **스팀 클라우드(Steam Cloud) 연동 규격**:
  - Windows: `%APPDATA%\<GameName>\saves\slot1.json`
  - Linux / Steam Deck: `~/.config/<GameName>/saves/slot1.json`
  - 절대경로 하드코딩 금지 ➔ OS 표준 유저 데이터 경로(`QStandardPaths` / `OS.get_user_data_dir()`) 사용.

---

### 2. 스팀웍스(Steamworks) SDK 연동 (도전과제 & 통계)
- **Pygame / Python**: `steamworks-py` 라이브러리 연동
- **Godot 4.x**: `GodotSteam` GDExtension 플러그인 연동
- **Tauri**: `tauri-plugin-steamworks` 연동
- **안전 인터록 (Fallback Guard)**:
  - 스팀 클라이언트가 켜져 있지 않거나 DRM이 없는 itch.io/DRM-Free 버전으로 빌드할 때 게임이 크래시되지 않도록, 반드시 **더미 스팀 어댑터(Steam Mock Adapter)**를 두어 무중단 구동을 보장합니다:
  ```python
  class SteamService:
      def __init__(self):
          self.is_active = False
          try:
              # Steamworks 초기화 시도
              self.is_active = True
          except Exception:
              print("[INFO] Running in DRM-Free / Offline mode.")

      def unlock_achievement(self, ach_id: str):
          if self.is_active:
              # steamworks API 호출
              pass
  ```

---

### 3. 스팀덱(Steam Deck) 적응 규격 (Verified 등급 가이드)
- **기본 해상도**: 1280x800 (16:10) 네이티브 지원 (레터박스 없는 꽉 찬 화면).
- **텍스트 가독성**: 최소 글꼴 크기 10pt 이상(화면 높이의 2.5% 이상) 유지.
- **컨트롤러 글리프(Glyph)**: 화면 UI에 키보드 키(`Space`, `Enter`) 대신 엑스박스/스팀덱 버튼(`[A]`, `[X]`, `[RT]`) 아이콘 자동 전환.
- **성능 프로파일**: 스팀덱 40Hz/60Hz 모드에서 배터리 소모 최적화(CPU 0% 동결 인터록 준수).

---

### 4. 프로덕션 빌드 디버그 봉인 (Production Seal Gate)
- 개발 중 사용했던 `[F1]` 인게임 손맛 튜너, 무적 치트, 디버그 좌표 표시를 상용 빌드 시 자동 차단:
```python
PRODUCTION_BUILD = True # 배포 빌드 시 환경변수 또는 플래그로 자동 설정

if event.key == pygame.K_F1 and not PRODUCTION_BUILD:
    toggle_debug_tuner()
```
