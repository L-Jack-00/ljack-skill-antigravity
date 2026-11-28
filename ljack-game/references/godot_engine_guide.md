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
- E2E 시나리오에는 **플로팅 포드 간격**, **비차단 드래그 창 Z-Order 승격 및 `Esc` LIFO 스택**, **이동 중 단축키 입력 시 이동 유지**, **탭 전환 전후 UI 요소 위치/크기 불변**, **알림 토스트 즉시 교체**, **EN↔KO 실시간 언어 왕복 후 `refresh_labels()` 전파**, **시각 키 설정 충돌 스왑 및 기본값 복원**, **모드 전환(풀 화면 ↔ 미니 위젯)**을 반드시 포함합니다.

---

### 6. Godot 4.x 헤드리스 & GDScript 실전 함정 체크리스트
- **`class_name` 헤드리스 캐시 이슈**: `--headless` 단일 스크립트 실행 시 새로 추가된 헬퍼 클래스의 전역 `class_name`이 `.godot` 캐시에 아직 없을 수 있으므로 `const Helper := preload("res://src/.../helper.gd")`로 명시 로드.
- **타입 추론 `:=` 주의**: Untyped `Array`/`Dictionary` 인덱싱·조회에 `:=`를 쓰면 Variant 추론 오류가 발생할 수 있으므로 `str(...)`, `int(...)` 또는 명시적 타입(`: String`)을 지정.
- **`RefCounted` 열거형 스코프**: `Control`을 상속하지 않는 `RefCounted` UI 헬퍼에서는 `Control.HORIZONTAL_ALIGNMENT_CENTER` 대신 전역 상수 `HORIZONTAL_ALIGNMENT_CENTER`를 사용.
- **입력 마스킹, 비간섭 단축키 & 맵 전환 위생**: 키 설정 리스닝(`is_listening()`) 또는 입력창 포커스 중에는 `_unhandled_input` 전역 단축키를 차단하고, 맵/룸 전환 시 미수령 드랍 플러시·스테이지 오브젝트(`stage_obj` 그룹) 정리로 `(0, 0)` 원점 플로팅 텍스트 잔류를 방지. 반면 **비차단 플로팅 창**을 단축키로 토글하거나 `Esc`로 닫을 때는 모달 전용 입력 강제 해제(`latch_held_actions`)를 호출하지 않아 이동 중 조작이 끊기지 않게 유지.

---

### 7. 비차단 플로팅 창, 하이브리드 비트맵 폰트 & 탭 레이아웃 불변 패턴

#### 7.1 픽셀 아트(`Nearest`) 환경의 하이브리드 비트맵 폰트 & 선형 업스케일링
- **문제**: 도트/픽셀 아트 게임에서 `textures/canvas_textures/default_texture_filter=0`(Nearest)과 `window/stretch/mode="canvas_items"`를 동시에 쓰면, 가변 크기로 래스터화된 UI 폰트가 확대 시 비균일 계단 현상으로 뭉개지거나 다국어 글리프가 누락되어 의도치 않은 시스템 폴백 폰트로 깨져 보이는 문제가 발생합니다.
- **해법**: 주 스크립트용 픽셀 폰트를 `FontVariation.base_font`로 두고 다국어용 임베디드 비트맵/레트로 폰트를 `fallbacks` 체인으로 연결합니다. 각 `FontFile`은 기준 비트맵 크기(`fixed_size`)로 래스터를 고정하고 안티앨리어싱/서브픽셀 배치를 끈 뒤, 실제 UI 텍스트 노드(`Label`/`Button`/`LineEdit`/`RichTextLabel`)에만 `CanvasItem.TEXTURE_FILTER_LINEAR`를 부여해 스프라이트 도트는 날카롭게 유지하면서 글자만 매끄럽게 업스케일링합니다.
```gdscript
static func _configure_crisp_bitmap_font(ff: FontFile, fixed_px: int = 16) -> void:
    ff.disable_embedded_bitmaps = false
    ff.antialiasing = TextServer.FONT_ANTIALIASING_NONE
    ff.hinting = TextServer.HINTING_NORMAL
    ff.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED
    ff.oversampling = 1.0
    if fixed_px > 0:
        ff.fixed_size = fixed_px
        ff.fixed_size_scale_mode = TextServer.FIXED_SIZE_SCALE_ENABLED

# 텍스트 컨트롤 적용 시 (스프라이트 Nearest 유지 + 텍스트만 Linear 스케일링)
ctrl.add_theme_font_override("font", hybrid_font)
ctrl.add_theme_font_size_override("font_size", font_size)
ctrl.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
```

#### 7.2 비차단 드래그 플로팅 창 & `Esc` LIFO 스택
- **구조**: 플레이를 방해하지 않아야 하는 상시 보조 창은 화면 디밍(`Dimmer`)과 키보드 조작 차단을 제거한 독립 `CanvasLayer`로 구성합니다.
- **드래그 & Z-Order**: 상단 타이틀바 드래그 시 뷰포트 경계 안으로 좌표를 클램핑하고, 창 내부 클릭(`gui_input`) 또는 열기 시 포커스 리스트 최상단으로 이동해 `CanvasLayer.layer`를 재정렬합니다.
- **`Esc` 단일 스택 우선순위**: 열린 팝업/입력 포커스 해제 ➔ 포커스 스택 최상단 비차단 창 1개 닫기(이동 키 홀드 유지) ➔ 열린 비차단 창이 0개일 때만 시스템 메인 메뉴 토글.

#### 7.3 탭 전환 시 UI 요소 크기·텍스트 흔들림 방지 (Zero Layout Shift)
- 동일 창 내 탭이나 필터를 전환할 때 창 제목이 바뀌거나 탭 버튼 폭·내용 높이가 달라지면 창 외곽선과 마우스 연속 클릭 위치가 어긋납니다.
- 다음 4가지를 고정합니다:
  1. 창 헤더 타이틀은 활성 탭과 무관한 고정 제목 + 고정 `custom_minimum_size`로 유지.
  2. 모든 탭 버튼에 `custom_minimum_size`와 `clip_text = true`를 지정하고 활성 상태에서도 글자 수/길이를 바꾸지 않는 정적 라벨 사용.
  3. 탭별로 표시/숨김되는 보조 액션 행은 공간 높이(`custom_minimum_size.y`)를 고정해 하위 리스트가 위아래로 밀리지 않게 유지.
  4. 목록 컨테이너에 `scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_SHOW_ALWAYS`를 적용해 스크롤바 출현 여부에 따른 가로 폭 출렁임 방지.
