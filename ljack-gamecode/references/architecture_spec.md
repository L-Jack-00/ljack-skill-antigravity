# LJack GameCode 아키텍처 명세 및 참조 구현

## 1. 개요 및 설계 의도
`ljack-gamecode` 프로토콜은 TypeScript/HTML5 기반 게임 개발 과정에서 AI 에이전트나 개발자가 스파게티 코드를 양산하거나, 순수 게임 로직에 브라우저 렌더링/오디오 API가 침투하거나, 임의의 도형/사운드를 무분별하게 하드코딩하는 현상을 차단하기 위해 설계되었습니다.

### 핵심 제약 3대 원칙
1. **레이어 강제 격리 (Layer Isolation Guard)**:
   - `specs/types.ts`: 전역 타입 계약.
   - `specs/asset_manifest.json`: 에셋 메타데이터 및 AI 프롬프트 힌트.
   - `src/core/`: `EventBus`, `AssetHarness` 등 엔진 기반 인프라.
   - `src/logic/`: 순수 게임 로직 (`scripts/layer_guard.py` 정적 린터로 브라우저/DOM API 오염 차단).
   - `src/view/`: 렌더러 및 오디오 컨트롤러.
2. **에셋 브릿지 자동화 (AI Prompt Hint Injection)**:
   - 뷰 코드 내 `new Audio("assets/...")` 직접 생성 및 `ctx.fillRect` 임시 그래픽 남발 금지.
   - `specs/asset_manifest.json`에 `aiPromptHint`(PixelLab, Recraft, ElevenLabs, Suno 등 타깃) 선행 등록.
   - 실제 에셋 파일이 준비되면 즉시 로드하며, 누락/로딩 중일 때는 `AssetHarness`가 $O(1)$ 프로시저럴(마젠타 체크보드 / Web Audio 감쇠 사인파) 폴백을 자동 공급.
3. **단계별 원자적 변경 (Staged Atomic Mutation)**:
   - 일반 기능 구현 시 단일 단계에서 최대 2~3개 파일로 변경 범위를 제한하여 회귀 방지.
   - 계약(`specs/types.ts`, `specs/asset_manifest.json`) 선행 갱신 ➔ 순수 로직(`src/logic/`) ➔ 뷰/오디오 바인딩(`src/view/`) 3단계 준수.

---

## 2. 4대 코어 기반 파일 표준 구현 예시

### 2.1 `specs/types.ts`
```typescript
export type AssetType = 'sprite' | 'spritesheet' | 'ui_vector' | 'audio_sfx' | 'audio_bgm';

export interface SpriteMetadata {
  frameWidth: number;
  frameHeight: number;
  frameCount: number;
  fps: number;
  pivot: { x: number; y: number };
}

export interface AudioMetadata {
  volume: number;
  loop: boolean;
  pitchVariance?: number;
}

export interface AssetEntry {
  id: string;
  type: AssetType;
  path: string;
  aiPromptHint: string;
  spriteMeta?: SpriteMetadata;
  audioMeta?: AudioMetadata;
}

export interface AssetManifest {
  version: string;
  assets: Record<string, AssetEntry>;
}

export interface GameEventMap {
  PLAY_SFX: { assetId: string; volumeScale?: number };
  PLAY_BGM: { assetId: string; loop?: boolean };
  ENTITY_DAMAGED: { entityId: string; amount: number; sourceId?: string };
  STATE_CHANGED: { previousState: string; nextState: string; timestamp: number };
  [key: string]: unknown;
}
```

### 2.2 `specs/asset_manifest.json`
```json
{
  "version": "1.0.0",
  "assets": {
    "SPR_TEST_ACTOR": {
      "id": "SPR_TEST_ACTOR",
      "type": "spritesheet",
      "path": "assets/sprites/test_actor.png",
      "aiPromptHint": "Top-down retro hero character running animation, 4 frames, 64x64, pixel art style, transparent background",
      "spriteMeta": {
        "frameWidth": 64,
        "frameHeight": 64,
        "frameCount": 4,
        "fps": 8,
        "pivot": { "x": 32, "y": 32 }
      }
    },
    "SFX_TEST_IMPACT": {
      "id": "SFX_TEST_IMPACT",
      "type": "audio_sfx",
      "path": "assets/audio/sfx_impact.wav",
      "aiPromptHint": "Crisp metallic sword collision sound effect, 0.3s duration, zero reverb, retro arcade SFX",
      "audioMeta": {
        "volume": 0.8,
        "loop": false,
        "pitchVariance": 0.08
      }
    },
    "BGM_TEST_THEME": {
      "id": "BGM_TEST_THEME",
      "type": "audio_bgm",
      "path": "assets/audio/bgm_theme.mp3",
      "aiPromptHint": "Upbeat 16-bit chiptune dungeon exploration theme, 120 BPM, synth bass and arpeggio, seamless loopable, instrumental only",
      "audioMeta": {
        "volume": 0.6,
        "loop": true
      }
    }
  }
}
```

### 2.3 `src/core/EventBus.ts`
```typescript
import { GameEventMap } from '../../specs/types';

type EventCallback<T> = (payload: T) => void;

export class EventBus<Events extends Record<string, unknown> = GameEventMap> {
  private static instance: EventBus<Record<string, unknown>>;
  private listeners: Map<keyof Events, Set<EventCallback<unknown>>> = new Map();

  public static getInstance<E extends Record<string, unknown> = GameEventMap>(): EventBus<E> {
    if (!EventBus.instance) {
      EventBus.instance = new EventBus<E>() as unknown as EventBus<Record<string, unknown>>;
    }
    return EventBus.instance as unknown as EventBus<E>;
  }

  public on<K extends keyof Events>(event: K, callback: EventCallback<Events[K]>): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback as EventCallback<unknown>);
  }

  public off<K extends keyof Events>(event: K, callback: EventCallback<Events[K]>): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.delete(callback as EventCallback<unknown>);
      if (callbacks.size === 0) {
        this.listeners.delete(event);
      }
    }
  }

  public emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      // Snapshot copy prevents mutation issues if a listener unsubscribes itself during emit
      for (const cb of [...callbacks]) {
        (cb as EventCallback<Events[K]>)(payload);
      }
    }
  }

  public clear(): void {
    this.listeners.clear();
  }
}
```

### 2.4 `src/core/AssetHarness.ts`
```typescript
import { AssetManifest } from '../../specs/types';

export class AssetHarness {
  private static instance: AssetHarness;
  private manifest: AssetManifest | null = null;
  private graphicCache: Map<string, HTMLCanvasElement | HTMLImageElement> = new Map();
  private loadingImages: Set<string> = new Set();
  private audioBufferCache: Map<string, AudioBuffer> = new Map();
  private loadingAudio: Set<string> = new Set();
  private audioCtx: AudioContext | null = null;

  private constructor() {}

  public static getInstance(): AssetHarness {
    if (!AssetHarness.instance) {
      AssetHarness.instance = new AssetHarness();
    }
    return AssetHarness.instance;
  }

  public async initialize(manifestData: AssetManifest): Promise<void> {
    this.manifest = manifestData;
  }

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof document !== 'undefined';
  }

  private ensureAudioContext(): AudioContext | null {
    if (!this.isBrowser()) return null;
    if (!this.audioCtx) {
      const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (!AudioContextClass) return null;
      this.audioCtx = new AudioContextClass();
    }
    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume().catch(() => {
        // Ignore autoplay restriction until first user gesture unlocks audio
      });
    }
    return this.audioCtx;
  }

  public getGraphic(assetId: string): HTMLCanvasElement | HTMLImageElement | null {
    if (!this.isBrowser()) return null;

    const entry = this.manifest?.assets[assetId];

    // Trigger asynchronous load of real image asset on first access
    if (entry?.path && !this.loadingImages.has(assetId)) {
      this.loadingImages.add(assetId);
      const img = new Image();
      img.onload = () => {
        this.graphicCache.set(assetId, img);
      };
      img.onerror = () => {
        // Keep procedural debug checkerboard in cache when asset file is missing
      };
      img.src = entry.path;
    }

    if (this.graphicCache.has(assetId)) {
      return this.graphicCache.get(assetId)!;
    }

    const width = entry?.spriteMeta ? entry.spriteMeta.frameWidth * entry.spriteMeta.frameCount : 64;
    const height = entry?.spriteMeta ? entry.spriteMeta.frameHeight : 64;

    // Immediate O(1) procedural magenta/purple checkerboard fallback while loading or missing
    const fallbackCanvas = document.createElement('canvas');
    fallbackCanvas.width = width;
    fallbackCanvas.height = height;
    const ctx = fallbackCanvas.getContext('2d');
    if (ctx) {
      const tileSize = 8;
      for (let x = 0; x < width; x += tileSize) {
        for (let y = 0; y < height; y += tileSize) {
          ctx.fillStyle = ((x / tileSize + y / tileSize) % 2 === 0) ? '#ff00ff' : '#4b0082';
          ctx.fillRect(x, y, tileSize, tileSize);
        }
      }
      ctx.fillStyle = '#ffffff';
      ctx.font = '10px monospace';
      ctx.fillText(assetId.slice(0, 10), 2, 12);
    }

    this.graphicCache.set(assetId, fallbackCanvas);
    return fallbackCanvas;
  }

  private getOrCreateFallbackTone(ctx: AudioContext): AudioBuffer {
    const sampleRate = ctx.sampleRate;
    const duration = 0.15;
    const frameCount = Math.floor(sampleRate * duration);
    const buffer = ctx.createBuffer(1, frameCount, sampleRate);
    const data = buffer.getChannelData(0);
    const freq = 440;
    for (let i = 0; i < frameCount; i++) {
      const t = i / sampleRate;
      const envelope = 1.0 - (i / frameCount);
      data[i] = Math.sin(2 * Math.PI * freq * t) * envelope;
    }
    return buffer;
  }

  public playAudio(assetId: string, volumeScale: number = 1.0): void {
    const ctx = this.ensureAudioContext();
    if (!ctx) return;

    const entry = this.manifest?.assets[assetId];
    const baseVolume = Math.max(0, Math.min(1, (entry?.audioMeta?.volume ?? 1.0) * volumeScale));
    const pitchVariance = entry?.audioMeta?.pitchVariance ?? 0;

    // Asynchronously fetch and decode real audio file if configured
    if (entry?.path && !this.loadingAudio.has(assetId)) {
      this.loadingAudio.add(assetId);
      fetch(entry.path)
        .then((res) => (res.ok ? res.arrayBuffer() : Promise.reject(new Error('HTTP error'))))
        .then((arr) => ctx.decodeAudioData(arr))
        .then((decoded) => {
          this.audioBufferCache.set(assetId, decoded);
        })
        .catch(() => {
          // Retain synthesized fallback buffer when asset file is unavailable
        });
    }

    let buffer = this.audioBufferCache.get(assetId);
    if (!buffer) {
      buffer = this.getOrCreateFallbackTone(ctx);
      this.audioBufferCache.set(assetId, buffer);
    }

    const source = ctx.createBufferSource();
    source.buffer = buffer;
    source.loop = entry?.audioMeta?.loop ?? false;

    if (pitchVariance > 0) {
      const semitone = (Math.random() * 2 - 1) * pitchVariance;
      source.playbackRate.value = Math.pow(2, semitone);
    }

    const gainNode = ctx.createGain();
    gainNode.gain.value = baseVolume;
    source.connect(gainNode);
    gainNode.connect(ctx.destination);

    source.start(0);
  }
}
```
