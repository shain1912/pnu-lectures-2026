# 11주 스타터 — XR Origin 리그 · 텔레포트 · 스냅 턴 · AI 함정 #8

- 과목 : 컴퓨터그래픽스 VF3500076 · 11주 «VR 개발 기초»
- 기준 : **Unity 6 · URP · OpenXR · XR Interaction Toolkit(XRI) 3.x · Meta Quest 3**
- 함께 볼 자료 : 슬라이드 `slides/w11/` · 실기 체크리스트 `labs/w11/VR-실기-체크리스트.md`
- 주의 : 메뉴·컴포넌트·옵션 이름은 패키지 버전에 따라 조금씩 다를 수 있음 → 다르면 비슷한 이름을 찾고, 찾은 이름을 체크리스트에 메모

## 들어 있는 파일

| 파일 | 역할 |
|---|---|
| `Trap_CameraDirectMove.cs` | **AI 함정 #8 재현본** — Main Camera Transform 을 직접 움직이는 «AI 가 흔히 내놓는 코드» + 덮어쓰기 진단 로그 |
| `Fix_RigTeleportToSpot.cs` | **정답본** — 같은 기능을 XR Origin(리그 루트) 이동으로 구현 + 카메라 로컬값 연속성 검증 로그 |
| `README.md` | 리그 구성 · 텔레포트·스냅 턴 설정 순서 · 함정 실험 방법 |

두 스크립트는 **같은 기능**(버튼 → 다음 관찰 지점으로 순간 이동)을 서로 다른 구조로 구현 → 헤드셋에서 나란히 비교하는 용도

---

## 1. 용어 풀이

| 용어 | 쉬운 뜻 |
|---|---|
| XR 리그 (XR Rig) | 헤드셋·컨트롤러를 씬에 연결하는 오브젝트 묶음 |
| XR Origin | 리그의 뿌리 · 플레이 구역 전체의 월드 위치·방향 — **이동 코드가 움직이는 곳** |
| Camera Offset | 트래킹 0 점과 바닥 높이를 맞추는 중간 노드 |
| Main Camera | 내 머리 · **Tracked Pose Driver 전용** — 코드로 쓰지 않음 |
| Tracked Pose Driver | 헤드셋 자세를 매 프레임 Transform 에 기록하는 컴포넌트 (기본 갱신 시점 : Update and Before Render) |
| Locomotion Mediator | XRI 3.x 에서 여러 이동 기능(텔레포트·회전·이동)의 요청을 순서대로 처리하는 중재자 |
| Teleportation Provider | 텔레포트 요청을 받아 XR Origin 을 순간 이동시키는 컴포넌트 |
| Snap Turn Provider | 스틱 입력마다 정해진 각도만큼 리그를 순간 회전시키는 컴포넌트 |
| Teleportation Area / Anchor | 텔레포트 가능한 바닥 / 도착 위치·방향이 정해진 지점 |
| Interaction Layer | 인터랙터(레이 등)가 어떤 대상과 반응할지 거르는 XRI 전용 레이어 (물리 Layer 와 별개) |

---

## 2. XR Origin 리그 구조 — 왜 노드가 셋인가

```
XR Origin (XR Rig)          ← 이동·회전 코드가 움직이는 곳 (텔레포트 · 스냅 턴)
├─ Camera Offset            ← 높이 보정 (Floor 모드 0 m · Device 모드 Camera Y Offset 기본 1.1176 m)
│  ├─ Main Camera           ← Tracked Pose Driver 가 매 프레임 덮어씀 → 코드로 쓰지 않음
│  ├─ Left Controller       ← 손 자세 + 레이·텔레포트 인터랙터
│  └─ Right Controller
└─ Locomotion               ← Locomotion Mediator · Teleportation · Turn · Move (리그를 옮기는 담당자)
```

- 값마다 주인이 하나 : XR Origin = 내 코드·이동 담당자 · Camera Offset = 원점 모드 · Main Camera = 트래킹
- 최종 카메라 위치 = XR Origin 변환 × Camera Offset 변환 × 트래킹 변환 (2주차 부모-자식 체인)
- 손계산 : Origin (5, 0, 3) · Offset 0 · 트래킹 로컬 (0.2, 1.6, −0.1) → 카메라 월드 (5.2, 1.6, 2.9) · 텔레포트로 Origin 만 (8, 0, 3) → 카메라 (8.2, 1.6, 2.9)
- 실제 Starter Assets 프리팹에는 손 트래킹·Poke 인터랙터 등 자식이 더 있음 — 위는 뼈대만

---

## 3. 프로젝트 준비 (처음 한 번)

1. Unity Hub → 에디터에 **Android Build Support** 모듈 (OpenJDK · Android SDK & NDK 포함)
2. Package Manager
   - **XR Plugin Management**
   - **OpenXR Plugin**
   - **XR Interaction Toolkit** (3.x) → Samples 탭 → **Starter Assets** Import
   - (선택) Samples → 에디터용 시뮬레이터 (버전에 따라 XR Device Simulator / XR Interaction Simulator)
3. Project Settings → **XR Plug-in Management** → **Android 탭** → OpenXR 체크 → **Meta Quest** 기능 그룹 체크
4. XR Plug-in Management → OpenXR → **Interaction Profiles** : Oculus Touch Controller Profile 또는 Meta Quest Touch Plus Controller Profile 추가
5. **Project Validation** 창 → **Fix All** (IL2CPP · ARM64 · 최소 API 레벨 등을 권장값으로)
6. Player : Color Space = **Linear** · Active Input Handling = **Input System Package (New)** 또는 Both
7. File → **Build Profiles** → Android → Switch Platform

> 첫 빌드는 빈 씬 + 큐브 + XR Origin 으로 → 파이프라인 문제와 씬 문제를 분리

---

## 4. 리그 배치 (실험실 씬 포팅)

1. 실험실 씬 복제 → `Lab_VR.unity`
2. 기존 Main Camera · 카메라 조작 스크립트 삭제
3. `Assets/Samples/XR Interaction Toolkit/<버전>/Starter Assets/Prefabs/` 의 **XR Origin (XR Rig)** 프리팹을 씬에 배치 → 바닥 위 y = 0
4. XR Origin 컴포넌트 → **Tracking Origin Mode = Floor**
5. 씬에 `XR Interaction Manager` 1개 확인 (프리팹·자동 생성 · 중복이면 정리)
6. 10주 UI 를 쓰려면 EventSystem 에 **XR UI Input Module** 사용 (Starter Assets 안내에 따름)
7. 기준 큐브(높이 1 m) 배치 → 헤드셋에서 허리 근처인지 확인 (1 unit = 1 m)

---

## 5. 텔레포트 · 스냅 턴 설정 순서 (XRI 3.x Starter Assets)

1. XR Origin (XR Rig) 의 자식 **Locomotion** 확인 → **Locomotion Mediator** · **Teleportation**(Teleportation Provider) · **Turn**(Snap Turn Provider · Continuous Turn Provider) 존재
2. **바닥** : Collider 가 있는 바닥 오브젝트에 **Teleportation Area** 추가
   - Interaction Layer Mask = **Teleport** (Starter Assets 의 텔레포트 레이는 Teleport 레이어만 조준 · 레이어가 없으면 프로젝트 검증 안내에 따라 추가)
3. **관찰 지점** : 빈 오브젝트 + Collider(얇은 원판 등)에 **Teleportation Anchor** 추가 → 도착 후 바라볼 방향 = 오브젝트의 forward(파란 화살표)
4. **회전** : Snap Turn Provider 사용
   - Turn Amount 기본 **45°** (22.5° 로 줄이면 방향 감각 유지 · 조작 횟수 증가)
   - 연속 회전 끄기 : 컨트롤러 오브젝트의 **Controller Input Action Manager** → **Smooth Turn Enabled** 해제
5. **연속 이동 끄기** : 같은 곳의 **Smooth Motion Enabled** 해제 → 오늘은 텔레포트 전용 (연속 이동 = 12주 동의 후 실습)
6. 빌드 → 확인 : 바닥 텔레포트 · 앵커 도착 방향 · 45° × 4번 = 뒤로 돌기

| 증상 | 원인 후보 |
|---|---|
| 레이가 바닥을 무시 | Teleportation Area 의 Interaction Layer Mask ≠ Teleport · 바닥 Collider 없음 |
| 텔레포트 후 바닥에 묻힘 | 바닥 Collider 높이 · XR Origin y · Tracking Origin Mode |
| 스냅 턴이 안 됨 / 부드럽게 돎 | Smooth Turn Enabled 가 켜짐 · Turn 액션 바인딩 |
| 스틱을 밀면 미끄러지듯 이동 | Smooth Motion Enabled 가 켜짐 → 해제 |

---

## 6. AI 함정 #8 실험 — 같은 기능, 두 구조

### 6-1. 준비

1. 실험실 씬에 빈 오브젝트 `Spots` → 자식으로 관찰 지점 3개 (바닥 위 y = 0 · forward 를 볼 대상 쪽으로)
2. 빈 오브젝트 `TrapTest` 에 `Trap_CameraDirectMove` 추가 → Spots 3개 연결 · 버튼 액션 연결 (에디터는 N 키)
3. 빈 오브젝트 `FixTest` 에 `Fix_RigTeleportToSpot` 추가 → Teleportation Provider(Locomotion/Teleportation) · Spots 연결
4. **둘 중 하나만** 활성화해서 빌드

### 6-2. 관찰

| 확인 | 함정본 | 정답본 |
|---|---|---|
| 에디터(헤드셋 없음)에서 N 키 | 이동하는 것처럼 보임 (설정·버전마다 다름) | 이동 |
| 헤드셋에서 버튼 | 제자리 · 깜빡임 | 관찰 지점으로 순간 이동 |
| 로그 | «지난 프레임에 쓴 값 ≠ 이번 프레임 시작 값» | 카메라 로컬값 튐 경고 없음 |
| 고개 돌림 | 정상 (이동이 안 되므로) | 정상 · 이동 직후에도 자연스러움 |

### 6-3. 왜 이렇게 되는가

```
한 프레임 :  입력 갱신 → Update → LateUpdate → 렌더 직전 → 렌더
              │          │                      │
              TPD 기록   함정본이 카메라에 씀    TPD 가 다시 덮어씀 → 화면에는 트래킹 값
```

- TPD = Tracked Pose Driver · 기본 갱신 시점 «Update and Before Render»
- LateUpdate 에서 비교하면 아직 같은 값 → 그래서 진단 로그는 **다음 프레임 시작**에서 비교

### 6-4. AI 의 «2차 수정» 을 따르면 안 되는 이유

| AI 의 제안 | 결과 | 지각 결과 |
|---|---|---|
| Tracked Pose Driver 끄기 | 머리 회전·이동 반영 안 됨 | 세상이 얼굴에 붙어 따라 돎 → 전정계는 회전, 눈은 정지 → 즉각 멀미 |
| Tracking Type = Rotation Only | 위치 트래킹 소실 (3DoF) | 몸을 숙여도 시점 고정 · 운동 시차 소실 |
| LateUpdate 에서 덮어쓰기 | 덮어쓰기 경쟁 | 프레임마다 값이 오락가락 → 떨림 |

> 2차 수정 버전을 체험해 보는 경우 **10초 이내** · 스포터 대기 · 불편하면 즉시 벗기

### 6-5. 정답 구조의 요점

- `TeleportationProvider.QueueTeleportRequest(new TeleportRequest { … })` → XR Origin 이동 · 카메라는 트래킹이 계속 담당
- XRI 3.x 는 Locomotion Mediator 가 요청을 순서대로 처리 → 다른 이동 기능과 충돌 없음 · XR Origin 의 CharacterController 등과도 함께 동작
- Locomotion 이 없는 단순 프로젝트 : `XROrigin.MoveCameraToWorldLocation(목표)` · `XROrigin.MatchOriginUpCameraForward(up, forward)` · 회전은 `XROrigin.RotateAroundCameraUsingOriginUp(각도)` (머리 위치를 축으로 회전)
- 눈높이 숫자(1.6 등)를 코드에 쓰지 않음 → Floor 모드가 실제 눈높이를 줌

---

## 7. AI 에게 줄 명세 예시 (4칸)

```
[목표]
실험실 씬에서 오른손 A 버튼을 누르면 다음 관찰 지점(Transform 배열)으로 순간 이동한다.

[제약]
- Main Camera 의 Transform 에 쓰지 않는다 (Tracked Pose Driver 전용)
- XRI 3.x 의 TeleportationProvider.QueueTeleportRequest 로 XR Origin 을 이동한다
- 보간·가속 없이 순간 이동 · 도착 방향 = 관찰 지점의 forward
- 입력은 InputActionReference 로 받고, 버튼 하드코딩 금지
- 눈높이 숫자(1.6 등)를 코드에 쓰지 않는다 (Tracking Origin = Floor)

[검증 조건]
- 이동 전후 Main Camera 의 localPosition 을 로그 → 이동 순간에도 연속(튐 없음)
- 헤드셋에서 이동 직후 고개 돌림이 정상 반영
- 도착 후 카메라 월드 y = 실제 눈높이 ± 5 cm

[비목표]
- 연속 이동 · 손 트래킹 · UI
```

---

## 8. 컴파일이 안 될 때

| 오류 | 확인 |
|---|---|
| `TeleportationProvider` · `TeleportRequest` 를 찾을 수 없음 | XRI 버전 확인 · 3.x 는 `UnityEngine.XR.Interaction.Toolkit.Locomotion.Teleportation` 네임스페이스 · 2.x 는 해당 using 줄 삭제 |
| `XROrigin` 을 찾을 수 없음 | XR Core Utils 패키지 (XRI 설치 시 함께 설치됨) · `using Unity.XR.CoreUtils;` |
| `InputActionReference` 를 찾을 수 없음 | Input System 패키지 · Active Input Handling 설정 |
| `FindAnyObjectByType` 이 없음 | 구버전 Unity → `FindObjectOfType<XROrigin>()` 로 교체 |
