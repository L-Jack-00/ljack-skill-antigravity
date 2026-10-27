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
