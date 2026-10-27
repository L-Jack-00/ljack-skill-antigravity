# LJack Game Protocol: 게임 필(Game Feel) & 손맛 튜닝 가이드

플레이어가 "조작이 답답하다"거나 "게임이 엉성하다"고 느끼는 대부분의 원인은 그래픽이 아니라 **조작 반응성(Input Forgiveness)과 물리적 피드백(Juice)**의 결여에서 발생합니다.

LJack Game Protocol에서는 다음 5대 손맛 레시피를 기본 탑재하도록 권장합니다:

---

### 1. 코요테 타임 (Coyote Time: 낭떠러지 점프 유예)
- **문제**: 발판 끝에서 정확히 점프하려다 1프레임 차이로 허공에서 떨어져 조작감이 불쾌해짐.
- **해법**: 발판을 벗어난 직후 약 5~8틱(약 0.08~0.13초) 동안은 공중에 떠 있어도 점프 입력을 유효하게 인정.
```python
if is_grounded:
    coyote_timer = 6  # 6틱 동안 버퍼 유지
elif coyote_timer > 0:
    coyote_timer -= 1

if jump_pressed and (is_grounded or coyote_timer > 0):
    vy = jump_force
    coyote_timer = 0
```

---

### 2. 점프 버퍼링 (Jump Buffering: 착지 전 선입력)
- **문제**: 착지 직전에 점프 키를 미리 눌렀으나 착지 순간 키가 떼어져 점프가 씹힘.
- **해법**: 공중에 있을 때 점프 키가 눌리면 4~6틱 동안 "점프 예약" 플래그를 유지하고, 착지하는 즉시 자동으로 점프 발동.
```python
if jump_pressed:
    jump_buffer_timer = 6

if is_grounded and jump_buffer_timer > 0:
    vy = jump_force
    jump_buffer_timer = 0
```

---

### 3. 가변 점프 높이 & 낙하 가속 (Variable Jump & Fall Multiplier)
- **문제**: 점프 키를 살짝 톡 치든 길게 꾹 누르든 항상 똑같은 높이로 뛰면 캐릭터가 붕 떠 보임(Floaty).
- **해법**:
  - 점프 키를 떼었을 때 상승 중이라면 상승 속도를 즉시 절반으로 감속(`vy *= 0.5`).
  - 정점을 지나 하강(`vy > 0`)할 때는 중력을 1.5배~2배 강하게 적용하여 착지감을 묵직하게 형성.

---

### 4. 히트스톱 (Hitstop / Freeze-Frame: 타격 찰나 정지)
- **문제**: 공격이 적중했을 때 캐릭터와 적이 아무 저항 없이 스르륵 통과하면 타격감이 전무함.
- **해법**: 강한 타격 순간 2~5틱(0.03~0.08초) 동안 양쪽 스프라이트의 업데이트를 일시 동결하고, 이후 넉백 및 피격 이펙트 재생.

---

### 5. 감쇄 스크린 셰이크 (Decay Screen Shake)
- **문제**: 피격/폭발 시 화면이 딱딱하게 고정되어 있으면 충격량이 체감되지 않음.
- **해법**: 폭발 강도(Trauma)를 1.0으로 설정하고 매 틱마다 $0.9$배로 지수 감쇄시키며 카메라 오프셋에 난수 노이즈 반영:
```python
camera_offset_x = (random.random() * 2 - 1) * trauma * max_shake
trauma = max(0.0, trauma - 0.05)
```
