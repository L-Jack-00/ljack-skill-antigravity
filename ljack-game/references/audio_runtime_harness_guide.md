# LJack Game Protocol: 오디오 & 사운드 런타임 하네스 가이드
## 멀티 엔진 무결점 사운드 시스템 & 상용 오디오 파이프라인 (Audio Safety Rig)

> **💡 시스템 지침 (System Directive)**:  
> 상용 인디 게임에서 사운드는 몰입감의 50% 이상을 결정짓지만, 잘못 구현할 경우 **1) 무사운드 환경/CI에서의 크래시**, **2) 웹 브라우저의 오토플레이 차단(Autoplay Block)**, **3) 동시 발음수 폭주로 인한 스피커 찢어짐(Audio Clipping)**, **4) 씬 전환 시 BGM 중복 누수** 등 치명적인 런타임 결함으로 직결됩니다.  
> 본 가이드는 3대 엔진(Pygame, HTML5/Tauri, Godot 4.x) 환경에서 무결점 오디오 런타임 하네스를 구축하는 표준 레시피를 규정합니다.

---

### 1. 상용 게임 오디오 4대 핵심 원칙 (Audio Pillars)

1. **무사운드 디바이스 폴백 안전망 (No-Audio Device Fallback)**:
   - 사용자의 PC에 사운드 카드/스피커가 연결되어 있지 않거나, 헤드리스 CI 서버에서 테스트를 돌릴 때 게임 프로세스가 절대 비정상 종료(Crash)되지 않고 더미(Dummy) 드라이버로 조용히 폴백해야 합니다.
2. **웹/브라우저 오토플레이 잠금 해제 가드 (User Gesture Autoplay Unlock)**:
   - 최신 웹 브라우저(Chrome, Safari, Edge)는 사용자 인터랙션(클릭, 키 입력) 없이 오디오 재생을 엄격히 차단합니다. 첫 입력 시 `AudioContext`를 즉시 활성화(`resume`)하는 인터록을 갖추어야 합니다.
3. **독립 3계층 볼륨 버스 (Master / BGM / SFX Triple Bus)**:
   - 단일 전역 볼륨이 아닌, Master(전체), BGM(음악), SFX(효과음)를 독립 제어하고 F1 손맛 튜너 또는 옵션창에서 실시간 선형/데시벨 조절이 가능해야 합니다.
4. **동시 발음수(Polyphony) 제한 및 채널 누수 방지**:
   - 1프레임에 수십 개의 총알이 발사되거나 몬스터가 동시 타격될 때 동일 SFX가 중첩되어 음압이 찢어지지 않도록, 발음수 캡(Voice Limiter)과 쿨다운(Debounce)을 둡니다.

---

### 2. 엔진별 오디오 하네스 실전 구현 레시피

#### 🎮 [엔진 1: Pygame / Python]
```python
# -*- coding: utf-8 -*-
"""
Pygame Audio Runtime Harness (Dummy Fallback + 3-Bus Volume)
"""
import os
import pygame

class AudioHarness:
    def __init__(self):
        self.audio_available = False
        self.master_vol = 1.0
        self.bgm_vol = 0.8
        self.sfx_vol = 1.0
        self.sfx_cooldowns = {}  # {sfx_id: last_tick}

        # 1. 무음 디바이스 및 헤드리스 안전 초기화
        try:
            # 44.1kHz, 16bit stereo, 512 버퍼 (지연 최소화)
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(16)  # 동시 16채널 확보
            self.audio_available = True
        except pygame.error as e:
            # 사운드 카드 미연결 또는 헤드리스 환경
            os.environ["SDL_AUDIODRIVER"] = "dummy"
            print(f"[AUDIO WARN] Hardware mixer unavailable ({e}). Falling back to dummy driver.")
            self.audio_available = False

    def play_bgm(self, file_path: str, loop: bool = True, fade_ms: int = 1000):
        if not self.audio_available or not os.path.exists(file_path):
            return
        try:
            pygame.mixer.music.fadeout(fade_ms)
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(self.master_vol * self.bgm_vol)
            pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)
        except Exception:
            pass

    def play_sfx(self, sound: pygame.mixer.Sound, sfx_id: str = None, curr_tick: int = 0, min_cooldown: int = 3):
        if not self.audio_available or sound is None:
            return
        
        # 동시 발음 폭주 방지 (3틱 이내 동일 SFX 중복 재생 차단)
        if sfx_id:
            last = self.sfx_cooldowns.get(sfx_id, -999)
            if curr_tick - last < min_cooldown:
                return
            self.sfx_cooldowns[sfx_id] = curr_tick

        sound.set_volume(self.master_vol * self.sfx_vol)
        sound.play()

    def set_volumes(self, master: float = None, bgm: float = None, sfx: float = None):
        if master is not None: self.master_vol = max(0.0, min(1.0, master))
        if bgm is not None: self.bgm_vol = max(0.0, min(1.0, bgm))
        if sfx is not None: self.sfx_vol = max(0.0, min(1.0, sfx))

        if self.audio_available:
            pygame.mixer.music.set_volume(self.master_vol * self.bgm_vol)
```

---

#### 🌐 [엔진 2: HTML5 / Canvas / Tauri]
```javascript
/**
 * WebAudio 3-Bus Harness with User Gesture Unlock & Tab Focus Mute
 */
class WebAudioHarness {
  constructor() {
    this.ctx = null;
    this.masterGain = null;
    this.bgmGain = null;
    this.sfxGain = null;
    this.isUnlocked = false;

    // 1. AudioContext 및 Gain 버스 트리 구성
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (AudioCtx) {
      this.ctx = new AudioCtx();
      this.masterGain = this.ctx.createGain();
      this.bgmGain = this.ctx.createGain();
      this.sfxGain = this.ctx.createGain();

      this.bgmGain.connect(this.masterGain);
      this.sfxGain.connect(this.masterGain);
      this.masterGain.connect(this.ctx.destination);

      this.masterGain.gain.value = 1.0;
      this.bgmGain.gain.value = 0.8;
      this.sfxGain.gain.value = 1.0;
    }

    // 2. 브라우저 오토플레이 잠금 해제 인터록
    this._attachUnlockHandlers();

    // 3. 브라우저 탭 비활성화 시 자동 뮤트 (성능 및 사용자 배려)
    document.addEventListener("visibilitychange", () => {
      if (document.hidden && this.ctx && this.ctx.state === "running") {
        this.ctx.suspend();
      } else if (!document.hidden && this.ctx && this.isUnlocked && this.ctx.state === "suspended") {
        this.ctx.resume();
      }
    });
  }

  _attachUnlockHandlers() {
    const unlock = () => {
      if (this.ctx && this.ctx.state === "suspended") {
        this.ctx.resume().then(() => {
          this.isUnlocked = true;
          console.log("[AUDIO] WebAudio unlocked via user gesture.");
        });
      } else {
        this.isUnlocked = true;
      }
      window.removeEventListener("pointerdown", unlock);
      window.removeEventListener("keydown", unlock);
    };
    window.addEventListener("pointerdown", unlock, { once: true });
    window.addEventListener("keydown", unlock, { once: true });
  }

  setVolume(master = 1.0, bgm = 0.8, sfx = 1.0) {
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    // 클릭음(Pop noise) 방지를 위한 20ms 선형 램프
    this.masterGain.gain.linearRampToValueAtTime(master, now + 0.02);
    this.bgmGain.gain.linearRampToValueAtTime(bgm, now + 0.02);
    this.sfxGain.gain.linearRampToValueAtTime(sfx, now + 0.02);
  }
}
```

---

#### 🚀 [엔진 3: Godot 4.x (GDScript)]
```gdscript
# AudioHarness.gd (Autoload 싱글톤 권장)
extends Node

# Godot 버스 레이아웃: Master (0), Music (1), SFX (2)
const BUS_MASTER = 0
const BUS_MUSIC = 1
const BUS_SFX = 2

func _ready() -> void:
    # 윈도우 포커스 감지 (포커스 잃으면 자동 감쇄)
    get_tree().root.focus_entered.connect(_on_focus_entered)
    get_tree().root.focus_exited.connect(_on_focus_exited)

# 선형 0.0~1.0을 데시벨(-80dB ~ 0dB)로 변환
func set_master_volume(linear: float) -> void:
    AudioServer.set_bus_volume_db(BUS_MASTER, linear_to_db(clamp(linear, 0.0001, 1.0)))

func set_music_volume(linear: float) -> void:
    AudioServer.set_bus_volume_db(BUS_MUSIC, linear_to_db(clamp(linear, 0.0001, 1.0)))

func set_sfx_volume(linear: float) -> void:
    AudioServer.set_bus_volume_db(BUS_SFX, linear_to_db(clamp(linear, 0.0001, 1.0)))

func _on_focus_exited() -> void:
    AudioServer.set_bus_mute(BUS_MASTER, true)

func _on_focus_entered() -> void:
    AudioServer.set_bus_mute(BUS_MASTER, false)
```

---

### 3. 상용 출시 전 오디오 셀프 체크리스트

| 점검 항목 | 기준 | 미달 시 위험 요소 |
| :--- | :--- | :--- |
| **사운드카드 미연결 테스트** | 헤드리스 또는 오디오 장치 없을 때 크래시 0건 | 스팀 유저 중 일부 환경에서 게임 실행 즉시 튕김 |
| **웹 브라우저 제스처 가드** | 첫 클릭/키입력 시 AudioContext 부드러운 해제 | 콘솔 에러 발생 및 게임 중 배경음 완전 먹통 |
| **볼륨 분리 (3-Bus)** | Master, BGM, SFX 슬라이더 독립 동작 | 스트리머 및 유저가 디스코드 통화 시 BGM만 끄지 못함 |
| **동시 발음수 쿨다운** | 1프레임 내 동일 효과음 중복 믹싱 차단 | 폭발/연타 시 찢어지는 고주파 디스토션 발생 |
| **창 전환/비활성화** | Alt+Tab 시 볼륨 음소거 또는 자동 감쇄 | 백그라운드에서 게임 소리가 계속 시끄럽게 울려 환불 사유 |
