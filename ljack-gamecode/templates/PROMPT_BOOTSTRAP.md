지금부터 이 워크스페이스를 'LJack GameCode' 계층 격리형 게임 개발 아키텍처로 초기화한다.
아직 구체적인 게임 컨텐츠 코드를 짜지 말고, 아래 명세에 따라 하네스 코어 기반 파일 4개를 정확한 경로에 생성하라. (초기 부트스트랩 예외로 아래 4종을 한 번에 스캐폴딩하거나, Step 1 계약 2종 + Step 2 코어 2종으로 나누어 생성할 수 있다.)

### 생성할 파일 목록 및 상세 스펙

1. `specs/types.ts`
   - `AssetType`: `'sprite' | 'spritesheet' | 'ui_vector' | 'audio_sfx' | 'audio_bgm'`
   - `SpriteMetadata`: `{ frameWidth: number; frameHeight: number; frameCount: number; fps: number; pivot: { x: number; y: number } }`
   - `AudioMetadata`: `{ volume: number; loop: boolean; pitchVariance?: number }`
   - `AssetEntry`: `{ id: string; type: AssetType; path: string; aiPromptHint: string; spriteMeta?: SpriteMetadata; audioMeta?: AudioMetadata }`
   - `AssetManifest`: `{ version: string; assets: Record<string, AssetEntry> }`
   - `GameEventMap`: 이벤트 버스에서 사용할 기본 이벤트 페이로드 인터페이스 (`PLAY_SFX`, `PLAY_BGM`, `ENTITY_DAMAGED`, `STATE_CHANGED`)

2. `specs/asset_manifest.json`
   - 하네스 작동 테스트를 위한 기본 에셋 3종 등록:
     * `SPR_TEST_ACTOR` (PixelLab 타겟 64x64 4프레임 스프라이트 시트 명세)
     * `SFX_TEST_IMPACT` (ElevenLabs 타겟 0.3초 타격음 명세, `pitchVariance: 0.08`)
     * `BGM_TEST_THEME` (Suno 타겟 루프형 BGM 명세)

3. `src/core/EventBus.ts`
   - `specs/types.ts`의 `GameEventMap`을 제네릭으로 받는 타입 안전(Type-safe) 동기식 Pub/Sub 이벤트 버스 클래스(`on`, `off`, `emit`, `clear`).

4. `src/core/AssetHarness.ts`
   - `specs/asset_manifest.json`을 로드하여 $O(1)$ `Map`에 캐싱하는 리소스 매니저.
   - **실제 에셋 우선 로드 + $O(1)$ 폴백**:
     * 그래픽(`getGraphic(id)`): `entry.path`의 실제 이미지 로드를 비동기로 시도하되, 로드 완료 전이나 파일 누락/오류 시에는 `spriteMeta`의 `frameWidth * frameCount` 규격에 맞춘 마젠타/퍼플 체크보드 디버그 `HTMLCanvasElement`를 즉시 반환(완료 시 실제 이미지로 자동 교체).
     * 오디오(`playAudio(id)`): `entry.path`의 실제 오디오 파일을 비동기 `fetch` + `decodeAudioData`로 디코딩 캐싱하며, 미로드/실패 시 `Web Audio API`로 0.15초 감쇠 사인파 `AudioBuffer`를 합성해 `pitchVariance` 난수 변조와 함께 재생.
     * 헤드리스 환경(`typeof window === 'undefined'`)에서도 예외 없이 안전하게 No-Op 처리.

위 4개 파일의 전체 프로덕션 코드를 누락이나 생략(`// ...`) 없이 작성하라. 완료 후 내가 기획할 게임 장르와 코어 루프 명세를 대기하라.
