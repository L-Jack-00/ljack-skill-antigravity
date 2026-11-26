# LJack Game Protocol: 고도 엔진 (Godot Engine 4.x) 하네스 가이드

Godot 4.x(GDScript / C#) 환경에서 LJack 8대 기둥(결정론적 고정 틱, 헤드리스 1만 틱 러너, 인게임 실시간 손맛 튜너, 플레이어블 검수 관문)을 구현하는 표준 레시피입니다.

---

### 1. `_physics_process`와 `_process`의 철저한 분리 (Pillar 1)
- **물리 및 게임 규칙**: 반드시 60Hz 고정 틱인 `_physics_process(delta)`에서만 연산.
- **카메라 및 시각 효과**: 모니터 주사율에 맞춰 가변 주기로 호출되는 `_process(delta)`에서 렌더링 보간 수행.
- **코어 상태 분리**: 게임 로직이 Godot 씬 트리에 종속되지 않도록 순수 `RefCounted` 또는 `Resource` 기반 클래스(`src/core/simulation.gd`)로 작성하여 헤드리스 테스트를 초고속화.

```gdscript
# src/core/simulation.gd
class_name GameEngine extends RefCounted

var world: GameWorld

func step_tick(active_inputs: Dictionary) -> void:
    world.tick_count += 1
    # 60Hz 결정론적 물리 연산 (UI 의존성 0)
    if active_inputs.get("JUMP", false) and world.player.is_grounded:
        world.player.vy = world.jump_strength
```

---

### 2. Godot Headless 1만 틱 초고속 시뮬레이터 (`tests/test_sim_headless.gd`)
- 고도 엔진의 `--headless` 모드를 활용하여 화면과 오디오를 띄우지 않고, 10,000번의 `step_tick`을 0.2초 만에 메모리 상에서 시뮬레이션합니다.
```bash
# Godot 4.x 헤드리스 테스트 러너 실행
godot --headless -s tests/test_sim_headless.gd
```
- 승패 도달 가능성, 물리 터널링, Reachability 수학 검증 ALL PASS 확인 후 사용자 플레이 검수로 전진.

---

### 3. CanvasLayer 기반 인게임 실시간 손맛 튜너 (F1 오버레이)
- `scenes/ui/tuner_overlay.tscn` (CanvasLayer)를 항상 씬 트리에 상주시켜, 플레이 중 `[F1]` 키를 누르면 반투명 인스펙터 패널이 토글됩니다.
- HSlider나 키보드로 중력(`gravity`), 이동속도(`speed`), 점프력(`jump_strength`)을 실시간 조절하면서 캐릭터를 즉시 조작해볼 수 있습니다.
- `[F2]` 키를 누르면 `res://config/balance.cfg`에 `ConfigFile` API로 핫저장:
```gdscript
func save_balance():
    var config = ConfigFile.new()
    config.set_value("game_feel", "gravity", world.gravity)
    config.set_value("game_feel", "speed", world.speed)
    config.save("res://config/balance.cfg")
```

---

### 4. 플레이어블 검수 및 원클릭 익스포트
- **플레이어블 검수 실행** (에디터를 열 필요 없이 프로젝트 루트에서 1초 만에 창 팝업):
  ```bash
  godot --path .
  ```
- **원클릭 배포 패키징**:
  ```bash
  godot --headless --export-release "Windows Desktop" dist/game.exe
  godot --headless --export-release "Web" dist_web/index.html
  ```

---

### 5. 실제 OpenGL 시각 E2E 검증 (`tests/UserE2E.tscn`)
- `--headless` 1만 틱과 물리 봇만으로는 모달 크기 초과, 버튼 텍스트 잘림, 불필요한 스크롤바, 플로팅 HUD 겹침, 미니 모드(예: 360×220) 레이아웃 깨짐을 잡을 수 없습니다.
- 실제 게임 씬을 기동해 상태를 순회하고 **`RenderingServer.frame_post_draw` 직후 Viewport PNG를 저장**한 뒤 이미지 파일로 직접 검수합니다:
  ```gdscript
  await RenderingServer.frame_post_draw
  var img := get_viewport().get_texture().get_image()
  if img != null:
      img.save_png(out_dir + "/01_hud.png")
  ```
- E2E 시나리오에는 **플로팅 포드 간격**, **메뉴 드로어 열기/Esc 닫기**, **EN↔KO 실시간 언어 왕복 후 `refresh_labels()` 전파**, **시각 키 설정 충돌 스왑 및 기본값 복원**, **모드 전환(풀 화면 ↔ 미니 위젯)**을 반드시 포함합니다.

---

### 6. Godot 4.x 헤드리스 & GDScript 실전 함정 체크리스트
- **`class_name` 헤드리스 캐시 이슈**: `--headless` 단일 스크립트 실행 시 새로 추가된 헬퍼 클래스의 전역 `class_name`이 `.godot` 캐시에 아직 없을 수 있으므로 `const Helper := preload("res://src/.../helper.gd")`로 명시 로드.
- **타입 추론 `:=` 주의**: Untyped `Array`/`Dictionary` 인덱싱·조회에 `:=`를 쓰면 Variant 추론 오류가 발생할 수 있으므로 `str(...)`, `int(...)` 또는 명시적 타입(`: String`)을 지정.
- **`RefCounted` 열거형 스코프**: `Control`을 상속하지 않는 `RefCounted` UI 헬퍼에서는 `Control.HORIZONTAL_ALIGNMENT_CENTER` 대신 전역 상수 `HORIZONTAL_ALIGNMENT_CENTER`를 사용.
- **입력 마스킹 & 맵 전환 위생**: 키 설정 리스닝(`is_listening()`) 또는 입력창 포커스 중에는 `_unhandled_input` 전역 단축키를 차단하고, 맵/룸 전환 시 미수령 드랍 플러시·스테이지 오브젝트(`stage_obj` 그룹) 정리로 `(0, 0)` 원점 플로팅 텍스트 잔류를 방지.
