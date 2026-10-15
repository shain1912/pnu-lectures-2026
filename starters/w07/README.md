# 7주차 스타터 — AI 함정 #6 : Transform 직접 이동으로 Rigidbody 무력화

**컴퓨터그래픽스 (VF3500076) · 디자인앤테크놀로지전공 · 조성호**

- 기준 : Unity 6 · URP · Input System 패키지 (새 프로젝트 기본값)
- 용도 : 수업 실습 50분 · 지각 실험실 씬 누적 · **8주 중간 프로젝트 검증 리포트의 재료**
- 함께 볼 것 : 슬라이드 7주차 «AI 함정 #6» · 워크북 `labs/w07/워크북.md`

---

## 파일 구성

| 폴더 | 파일 | 역할 |
|---|---|---|
| `Trap/` | `TrapMover.cs` | **함정 재현본** — Rigidbody 달린 공을 `transform.position` 으로 이동 |
| `Fixed/` | `RigidbodyMover.cs` | **정답본 ①** — 동적 Rigidbody 를 `linearVelocity` 로 이동 · CCD · Interpolate |
| `Fixed/` | `KinematicMover.cs` | **정답본 ②** — Is Kinematic 발판·문을 `MovePosition` 으로 이동 · 벽 정지는 `SweepTest` |
| `Fixed/` | `FastProjectile.cs` | **정답본 ③** — 빠른 물체의 Collision Detection 모드를 부등식으로 결정 |
| `Tools/` | `WallPassTest.cs` | 측정 — 같은 속도로 N회 발사 → 벽 통과 횟수 로그 |
| `Tools/` | `JitterMeter.cs` | 측정 — 벽에 밀어붙이는 3초 동안의 흔들림 폭 (m) |
| `Tools/` | `FixedStepProbe.cs` | 측정 — 화면 프레임마다 물리 스텝 횟수 패턴 (`0101…` = 떨림 원인) |

> 씬 파일(.unity)은 제공하지 않음 · 아래 5분 세팅으로 직접 구성 → 씬 구성 자체가 «Rigidbody·Collider 이해» 연습

---

## 5분 씬 세팅

1. **바닥** : `3D Object → Plane` · Scale (3, 1, 3)
2. **얇은 벽** : `3D Object → Cube` · Position (0, 1.5, 4) · Scale (6, 3, **0.2**) → 두께 0.2 m
3. **플레이어 공** : `3D Object → Sphere` · Position (0, 0.5, 0)
   - `Add Component → Rigidbody`
   - `TrapMover` 추가 (함정 재현 단계) · `JitterMeter` 추가 (Axis = Z)
4. **측정 오브젝트** : 빈 GameObject `Probe` → `FixedStepProbe` · `WallPassTest` 추가 → WallPassTest 의 `wall` 에 벽 Cube 지정
5. **Input System 확인** : `Edit → Project Settings → Player → Active Input Handling` = Input System Package (New) 또는 Both

---

## 실습 순서 (워크북과 동일)

| 단계 | 할 일 | 기록 |
|---|---|---|
| ① 재현 | `TrapMover` 로 WASD 이동 · 벽에 밀기 · Space 대시 | 떨림 여부 · 통과 여부 · J 키 흔들림 폭 |
| ② 측정 | `WallPassTest` 모드 3종 × 속도 10 / 40 m/s | 20회 중 통과 횟수 |
| ③ 수정 | `TrapMover` 제거 → `RigidbodyMover` 추가 | 같은 측정 반복 |
| ④ 떨림 | `FixedStepProbe` 패턴 기록 → Interpolate 끄고/켜고 비교 | 패턴 문자열 · 체감 |
| ⑤ 확장 | `Edit → Project Settings → Time → Fixed Timestep` = 0.0111 로 바꿔 재측정 | 패턴 변화 |

---

## 함정 요약 — 증상 · 원인 · 진단 · 수정

| | 내용 |
|---|---|
| **증상** | 벽 앞에서 부들부들 떨림 · 대시 시 얇은 벽 통과 · 부딪힌 상대가 안 밀림 |
| **원인** | `transform.position` 대입 = 순간이동 → Rigidbody 속도는 0 그대로 → 물리 엔진은 «속도 0 인 물체가 벽 속에 있음» 으로만 인식 → 밀어내기만 함 · `Update` 에서 실행 → 경로 검사(CCD) 무의미 |
| **진단** | 스크립트에서 `transform.position` · `transform.Translate` 검색 · 이동이 `Update` 인지 `FixedUpdate` 인지 · 실행 중 Rigidbody 속도 확인 · `WallPassTest` 반복 측정 |
| **수정** | 동적 물체 : `FixedUpdate` 에서 `rb.linearVelocity` 또는 `AddForce` · 빠른 물체 : Collision Detection = Continuous 계열 · 떨림 : Interpolate · 정해진 경로 물체 : Is Kinematic + `MovePosition` |

---

## 자주 나오는 질문

- **`rb.velocity` 를 쓰니 경고가 떠요** → Unity 6 에서 `linearVelocity` 로 이름 변경 · 옛 이름은 Obsolete
- **MovePosition 으로 바꿨는데도 벽을 통과해요** → Is Kinematic 물체는 스스로 벽에 막히지 않음 · 막혀야 하는 플레이어는 `RigidbodyMover`(동적) 또는 `CharacterController` · 발판이 멈춰야 하면 `KinematicMover` 의 `blockByWalls` 켜기
- **Continuous Dynamic 을 모든 물체에 켜면 안 되나요** → 비용 큼 · `속도 × Fixed Timestep > 가장 얇은 벽 + 물체 크기` 인 물체만
- **통과 0회가 나왔는데 검증 끝인가요** → 속도·벽 두께·Fixed Timestep 조건을 함께 기록 · 조건이 바뀌면 재측정
