# LJack Game Protocol: 충돌 판정 및 물리 터널링 방지 가이드

고속 이동 캐릭터나 투사체가 벽을 뚫고 지나가는 **터널링(Tunneling)** 및 벽 모서리 걸림(Snagging)을 원천 차단하는 표준 하네스 패턴입니다.

---

### 1. AABB (Axis-Aligned Bounding Box) 분리 축 검사
- 가벼운 2D 게임의 95%는 회전 없는 AABB로 해결:
```python
def check_aabb_collision(a, b):
    return (
        a.x < b.x + b.w and
        a.x + a.w > b.x and
        a.y < b.y + b.h and
        a.y + a.h > b.y
    )
```

---

### 2. 고속 투사체 터널링 방지 (Sub-Stepping Rig)
- **증상**: 투사체 속도($vx$)가 벽 두께보다 커서 1프레임 만에 벽의 반대편으로 건너뜀.
- **해법**: 단일 틱 내에서 속도 벡터를 최대 크기 $N$px(예: 8px) 이하 단위로 잘게 쪼개어 단계별(Sub-step) 충돌 검사 수행:
```python
step_size = 6.0
distance = math.hypot(vx, vy)
substeps = max(1, int(distance / step_size))
dx, dy = vx / substeps, vy / substeps

for _ in range(substeps):
    proj.x += dx
    proj.y += dy
    if check_wall_collision(proj):
        trigger_impact(proj)
        break
```

---

### 3. 모서리 둥글림 (Corner Snapping: 점프 모서리 걸림 방지)
- **증상**: 머리 위 발판 모서리에 1~2px 차이로 살짝 닿았을 때 점프가 턱 막히며 수직 추락.
- **해법**: 캐릭터 윗면 모서리가 발판 하단 가장자리와 3px 이내로 겹칠 경우, 캐릭터의 $x$ 좌표를 모서리 바깥쪽으로 부드럽게 밀어주어 자연스러운 점프 유도.

---

### 4. 2D 플랫포머 캐릭터 콜라이더 폭 규율 (`CapsuleShape2D` & 시각-물리 ±1px 정렬)
- **치비/SD 캐릭터 함정**: 시각적 머리/망토 폭(예: 34px)에 맞춰 평면 `RectangleShape2D` 바닥 콜라이더를 잡으면, 실제 신발 스탠스(예: 14~16px)보다 넓은 발판 틈새(~20~34px) 위를 양발이 허공에 뜬 채 다리처럼 건너며 떨어지지 않는 현상이 발생합니다.
- **역테이퍼(넓은 몸체 → 좁은 발) 다각형 함정**: 상단이 넓고 하단이 좁은 `ConvexPolygonShape2D` 사다리꼴은 틈새로 낙하할 때 경사진 발목 옆면이 양쪽 발판 모서리에 쐐기처럼 걸릴 수 있습니다.
- **표준 해법**:
  1. 캐릭터 물리 몸체는 **실제 신발/발 스탠스 폭(`PLAYER_HALF_W ≈ 7px`) 기준의 `CapsuleShape2D`**(총 폭 ~14px)로 설정하여 좁은 틈새 낙하·경사로 주행·모서리 미끄러짐을 동시에 보장.
  2. 플랫폼·타일 스프라이트의 시각적 외곽선(테두리·투명 여백)과 실제 물리 히트박스 경계를 **±1px 이내**로 정렬하여 체감 판정 괴리 차단.

---

### 5. 도달성 + 틈새 낙하 역검증 (Reachability & Gap Drop Audit)
- Reachability Solver/물리 봇은 "모든 발판에 올라갈 수 있는가"뿐 아니라 다음 **역검증 불변식**을 함께 검증합니다:
  1. **틈새 낙하(Gap Drop) 검증**: 발 스탠스보다 넓은 발판 틈새(예: `16px`, `33px`)를 걸어 통과하거나 정중앙에 위치시켰을 때 1초 이내 아래층으로 정상 추락하는지 확인.
  2. **평지 스텝업(Step-up) 오작동 차단**: 계단/단차 보정 프로브는 실제 유의미한 상향 단차(예: `dy > 1.5px`)일 때만 작동하도록 제한하여, 동일 높이 발판 틈새를 건너뛰듯 끌어올리는 부작용을 방지.
