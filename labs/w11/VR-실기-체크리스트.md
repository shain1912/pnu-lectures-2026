# 11주 VR 실기 체크리스트 — 내 실험실에 내가 들어가기

- 과목 : 컴퓨터그래픽스 VF3500076 · 11주 «VR 개발 기초 : XR Plugin 세팅, HMD·컨트롤러 입력, 시점 이동과 텔레포트»
- 시간 : 15:30–17:00 (90분) · **2인 1조** (착용자 1 · 스포터 1 · 10분마다 교대)
- 기준 : Unity 6 · URP · OpenXR · XR Interaction Toolkit(XRI) 3.x · Meta Quest 3
- 함께 볼 자료 : `starters/w11/README.md` (설정 상세 · 함정/정답 스크립트)
- 제출 : 이 문서의 체크 결과 + 마지막 절 «1분 소감 메모» (수업 안에서)

---

## 0. 처음 보는 용어 풀이

| 용어 | 쉬운 뜻 |
|---|---|
| XR 리그 (XR Rig) | 헤드셋·컨트롤러를 씬에 연결하는 오브젝트 묶음 — Unity 에서는 `XR Origin (XR Rig)` 프리팹 |
| XR Origin | 리그의 뿌리 · 내 플레이 구역 전체가 가상 세계 어디에 놓일지 정하는 노드 · **이동 코드는 여기를 움직임** |
| Camera Offset | XR Origin 과 카메라 사이의 높이 보정 노드 |
| Main Camera | 내 머리 · **Tracked Pose Driver 가 매 프레임 헤드셋 자세로 덮어씀 → 코드로 쓰지 않음** |
| Tracked Pose Driver | 헤드셋·컨트롤러의 위치·방향을 매 프레임 Transform 에 기록하는 컴포넌트 |
| 트래킹 원점 모드 | 트래킹 좌표의 0 점을 바닥(Floor)에 둘지, 앱 시작 시 헤드셋 위치(Device)에 둘지 |
| 가디언 (Guardian / 경계) | 헤드셋에 설정하는 안전 구역 테두리 · 벗어나면 경고 |
| 스포터 (Spotter) | 착용자 대신 주변을 봐 주는 짝 |
| 텔레포트 | 포물선 레이로 조준한 곳으로 순간 이동 — 이동 중 장면이 흐르지 않음 |
| 스냅 턴 | 스틱을 튕길 때마다 정해진 각도(기본 45°)만큼 순간 회전 |
| 벡션 (Vection) | 몸은 가만히 있는데 시야 흐름만으로 움직인다고 느끼는 착각 — 멀미의 주요 원인 (7주) |
| APK | 안드로이드 앱 설치 파일 — Quest 는 안드로이드 기반 |

---

## 1. 착용 전 — 안전 · 위생 (교수 브리핑 후 체크)

- [ ] 플레이 구역 **1인 2 m × 2 m** 확보 · 주변 의자·가방 치움
- [ ] 헤드셋 켜고 **가디언(경계) 설정** 완료 · 바닥 높이 확인
- [ ] **위생 커버 1인 1매** 착용
- [ ] 역할 확인 : 착용자 ________ · 스포터 ________ (10분 후 교대)
- [ ] 창가 **직사광선** 확인 — 렌즈에 햇빛이 모이면 화면 손상 · 내려놓을 때 렌즈를 아래로
- [ ] 안경 착용자 : 안경 스페이서 사용 여부 확인 (렌즈 긁힘 방지)

**스포터가 할 일**

- 착용자 주변의 사람·물체·케이블 감시
- 말로 안내 : «오른쪽에 책상 있어요» 처럼 **방향 + 물체**
- 착용자 몸을 잡아끌지 않음 (갑작스러운 접촉 → 놀람·넘어짐)
- 10분 타이머 관리

**멀미 대응 — 참지 말고 말하기 (벗어도 감점 없음)**

| 단계 | 신호 | 조치 |
|---|---|---|
| 1 | 미열감 · 침 분비 증가 | 이동 중단 · 정지 상태 유지 |
| 2 | 어지러움 · 두통 | 헤드셋 해제 · 착석 · 창밖 먼 곳 응시 |
| 3 | 메스꺼움 | 세션 종료 · **당일 재체험 금지** |

- 오늘의 이동 = **텔레포트 + 스냅 턴만** · 스틱으로 미끄러지듯 움직이는 **연속 이동은 켜지 않음** (12주 동의 후 실습에서만)

**교대 · 반납 순서**

1. 헤드셋 벗기 → 2. 알코올 티슈로 **페이스 인터페이스(얼굴 닿는 부분)** 세척 · 렌즈는 마른 극세사 천만 → 3. 다음 사람 위생 커버 → 4. 착용 → 5. 가디언 확인

---

## 2. ① XR 세팅 → 테스트 빌드 (15:40–16:00)

> 처음 빌드는 **빈 씬 + 큐브 1개 + XR Origin** 으로 → 빌드 파이프라인 문제와 씬 문제를 분리 (원인을 한 번에 하나만)

### 2-1. 사전 확인

- [ ] Meta 개발자 계정 인증 완료 (2주차 과제) · 헤드셋 **개발자 모드** 켜짐
- [ ] **데이터 전송 가능한 USB 케이블** (충전 전용 케이블이면 기기가 안 잡힘)
- [ ] Windows : Oculus ADB Drivers 설치 · macOS : 불필요
- [ ] 노트북 저장 공간 여유 (Android 빌드 지원 모듈 + 빌드 산출물)

### 2-2. 패키지 · 설정

- [ ] Unity Hub → 설치된 에디터에 **Android Build Support** (OpenJDK · Android SDK & NDK 포함) 모듈 확인
- [ ] Package Manager : **XR Plugin Management** · **OpenXR Plugin** · **XR Interaction Toolkit 3.x** 설치
- [ ] XRI → Samples → **Starter Assets** Import
- [ ] Project Settings → XR Plug-in Management → **Android 탭** → OpenXR 체크 → **Meta Quest** 기능 그룹 체크
- [ ] OpenXR → Interaction Profiles : **Oculus Touch Controller Profile** 또는 **Meta Quest Touch Plus Controller Profile** 추가
- [ ] Project Validation → **Fix All** (IL2CPP · ARM64 · 최소 API 레벨 등)
- [ ] Player → Color Space = **Linear** (5주) · Active Input Handling = **Input System Package** 포함

### 2-3. 빌드 반입 (기본 경로 : USB Build and Run)

| 경로 | 조건 | 소요 | 오늘 |
|---|---|---|---|
| **Build and Run (USB)** | ADB 드라이버 · 개발자 모드 · 데이터 케이블 | 3~6분 | **기본** |
| Meta Quest Developer Hub | 앱 설치 · APK 드래그 | 2~4분 | 보조 |
| 무선 디버깅 (adb connect) | 같은 네트워크 · 방화벽 확인 필요 | 최초 5분 | 사용 안 함 |
| Link · Play to Device | 빌드 없이 PC 화면 스트리밍 | 즉시 | 디버깅 전용 · 성능 측정 불가 |

- [ ] 헤드셋 USB 연결 → 헤드셋 안에서 **«USB 디버깅 허용»** 수락 (항상 허용 체크)
- [ ] File → **Build Profiles** → Android → (처음이면) Switch Platform
- [ ] Scene List 에 **테스트 씬만** 체크 → Run Device 에서 Quest 선택 → **Build and Run**
- [ ] 헤드셋에서 큐브가 보임 · 고개를 돌리면 큐브가 제자리에 있음 ✔

빌드 시작 시각 ______ · 헤드셋 실행 시각 ______ → 소요 ______ 분

---

## 3. ② 실험실 씬 포팅 (16:00–16:25)

- [ ] 실험실 씬 **복제** → `Lab_VR.unity` (원본은 보존)
- [ ] 기존 **Main Camera · 카메라 조작 스크립트 삭제** (카메라 2대 · Audio Listener 2개 방지)
- [ ] Starter Assets 의 **XR Origin (XR Rig)** 프리팹 배치 → 바닥 위 **y = 0** · 관찰 시작 지점
- [ ] XR Origin 컴포넌트 → **Tracking Origin Mode = Floor**
- [ ] 씬에 `XR Interaction Manager` 가 1개 있음 (없으면 추가 · 2개 이상이면 정리)
- [ ] 무거우면 일부 오브젝트 비활성화 후 반입 (12주 최적화 재료로 기록)
- [ ] Build Profiles 의 Scene List 를 `Lab_VR` 로 교체 → 빌드

### 3-1. 스케일 · 눈높이 점검 (1 unit = 1 m)

> 모니터에서는 씬 전체가 10배여도 티가 안 남 · VR 은 **내 눈 간격·눈높이가 1 m 자로 측정되어 들어옴** → 씬 스케일이 틀리면 거인/소인 느낌

| 점검 | 방법 | 기대 | 헤드셋에서 본 결과 |
|---|---|---|---|
| 기준 큐브 | 높이 1 m 큐브 배치 | 내 허리 근처 | |
| 문 | 실험실의 문·출입구 | 약 2 m | |
| 책상 | 책상·테이블 | 약 0.75 m | |
| 눈높이 | 정면 벽에 1.6 m 표시선 | 내 눈 근처 (키에 따라 ±) | |
| 원점 모드 | Device 로 바꿔 한 번 비교 (선택) | 약 1.12 m 로 낮아짐 | |

- 크기가 이상하면 : 모델 임포트의 **Scale Factor · Convert Units** 확인 (cm 단위 모델 → 75 unit 책상 = 75 m)
- 눈높이가 이상하면 : Tracking Origin Mode · XR Origin 의 y · 가디언 바닥 높이 순서로 확인

### 3-2. 지각 실험실 재관찰 (하나 이상 기록)

| 주차 장치 | 헤드셋에서 관찰한 것 | 모니터와 다른 점 |
|---|---|---|
| 5주 깊이 단서 스위치 | | |
| 4주 near 설정 (손을 가까이) | | |
| 6주 밉맵 (바닥 격자) | | |
| 3주 프레임 독립성 (움직이는 물체) | | |

---

## 4. ③ 텔레포트 · 스냅 턴 장착 (16:25–16:45)

> 컴포넌트·옵션 이름은 XRI 3.x Starter Assets 기준 · 버전에 따라 조금씩 다를 수 있음

- [ ] XR Origin (XR Rig) 의 자식 **Locomotion** 확인 → Locomotion Mediator · Teleportation · Turn 존재
- [ ] 바닥 오브젝트에 **Collider** 확인 → **Teleportation Area** 추가 → Interaction Layer Mask = **Teleport**
- [ ] 관찰 지점 3곳에 **Teleportation Anchor** (도착 방향까지 지정 · Anchor 의 파란 화살표 = 도착 후 정면)
- [ ] 회전 : **Snap Turn Provider** 사용 · 연속 회전 끄기 (Controller Input Action Manager → **Smooth Turn Enabled** 해제)
- [ ] 연속 이동 끄기 : 같은 곳의 **Smooth Motion Enabled** 해제 → 오늘은 텔레포트 전용
- [ ] 빌드 → 확인

| 확인 | 결과 |
|---|---|
| 바닥 아무 곳 텔레포트 | ☐ 됨 ☐ 안 됨 |
| 앵커 도착 시 정면 방향 | ☐ 맞음 ☐ 틀림 |
| 스냅 턴 45° (뒤로 돌기 = 4번) | ☐ 됨 ☐ 안 됨 |
| 텔레포트 직후 고개 돌림이 자연스러움 | ☐ 예 ☐ 아니오 |

**흔한 실패**

- 레이가 바닥을 무시 → Teleportation Area 의 Interaction Layer Mask 가 Teleport 가 아님
- 텔레포트 후 바닥에 묻힘·공중에 뜸 → 바닥 Collider 높이와 XR Origin 의 y 확인
- 이동 스크립트를 AI 로 만들었는데 헤드셋에서 안 움직임 → **AI 함정 #8** (아래 5절)

---

## 5. AI 함정 #8 점검 — 카메라 Transform 직접 조작

- [ ] AI 가 만든 이동 코드에서 `Camera.main.transform` · `mainCamera.transform.position =` 검색 → 있으면 함정
- [ ] Main Camera 의 **Tracked Pose Driver** 가 켜져 있고 Tracking Type = Rotation And Position
- [ ] 이동은 **XR Origin** 에 요청 (`TeleportationProvider.QueueTeleportRequest` 등) — `starters/w11/Fix_RigTeleportToSpot.cs`
- [ ] 진단 로그 : 이동 순간에도 Main Camera 의 localPosition 이 **연속**(튀지 않음)

| 버전 | 헤드셋에서 이동 | 고개 돌림 | 체감 |
|---|---|---|---|
| 함정 (`Trap_CameraDirectMove.cs`) | | | |
| 정답 (`Fix_RigTeleportToSpot.cs`) | | | |

> 함정 버전에서 AI 가 «Tracked Pose Driver 끄기» 로 고치라고 하면 **따르지 않음** — 머리를 돌려도 세상이 따라 도는 최악의 감각 충돌. 체험은 10초 이내로만.

---

## 6. ④ 10주 UI 두 벌 비교

| 판 | 헤드셋에서 보이는가 | 어디에 보이는가 | 읽기 편함 (0~3) | 메모 |
|---|---|---|---|---|
| Screen Space Overlay | ☐ 예 ☐ 아니오 | | | |
| World Space 0.5 m | | | | |
| World Space 1.2 m | | | | |
| World Space 2 m | | | | |
| World Space 0.3 m (두 눈 상이 겹쳐지는가) | | | | |

- 가장 읽기 편한 거리 : ______ m
- 함정 #7 원인을 한 문장으로 : ______________________________________________

---

## 7. 성능 기록 (선택 · 12주 비교용)

| 항목 (Quest 3 · URP) | 목표 | 경고 | 내 씬 |
|---|---|---|---|
| 프레임률 | 90Hz 고정 (11.1 ms) | 72Hz 강등 시 재설계 | |
| 드로우콜 | 씬당 150 이하 | 300 초과 | |
| 삼각형 | 프레임당 50만 이하 | 100만 초과 | |
| 실시간 그림자 | 0~1개 광원 | 2개 이상 | |
| 텍스처 | 2048 이하 · 밉맵 켬 | 4096 다수 | |

- 프레임률 확인 : **OVR Metrics Tool** (헤드셋 화면에 성능 수치를 띄우는 Meta 도구)

---

## 8. 1분 소감 메모 (헤드셋 벗은 직후 · 1분 안에)

> 기억이 사라지기 전에 · 착용자가 말하고 스포터가 받아 적어도 됨 · **12주 컴포트 설계의 입력 데이터**

```
이름 : ____________   조 : ____   착용 시간 : ____ 분   세션 : A / B

놀란 점 1개 (모니터와 가장 달랐던 것)
: ______________________________________________________________

불편한 점 1개 (어지러움 · 눈 피로 · 크기 이상 · 무게 등)
: ______________________________________________________________

불편 정도 (하나에 ○)   0 없음   1 약간   2 뚜렷함   3 중단함

불편했던 순간 (☐ 텔레포트 직후  ☐ 스냅 턴  ☐ 고개를 빨리 돌릴 때  ☐ 가만히 있을 때  ☐ 기타 ______)

다시 들어가면 바꾸고 싶은 것 1개
: ______________________________________________________________
```

---

## 9. 막혔을 때 (자주 나오는 문제)

| 증상 | 확인할 것 |
|---|---|
| Build and Run 에 Quest 가 안 보임 | 케이블(데이터 전송용) · 헤드셋 안 «USB 디버깅 허용» · ADB 드라이버 · 개발자 모드 |
| 빌드는 됐는데 헤드셋에서 검은 화면 | XR Plug-in Management Android 탭의 OpenXR 체크 · Meta Quest 기능 그룹 |
| 컨트롤러가 안 보임·안 눌림 | Interaction Profile 추가 여부 · Starter Assets 의 입력 액션 에셋 연결 |
| 헤드셋에서 고개를 돌려도 화면 고정 | Main Camera 의 Tracked Pose Driver 꺼짐 (AI 함정 #8 의 2차 수정) |
| 바닥 아래·천장에 서 있음 | Tracking Origin Mode · XR Origin y · 가디언 바닥 재설정 |
| «트래킹 손실» 경고 | 실습실 조명 · 무늬 없는 벽 앞 · 창가 직사광선 (SLAM 실패 환경) |
| 프레임이 끊김 | 실시간 그림자 광원 수 (5주) · 텍스처 크기 (6주) → 기록만 하고 12주에 최적화 |
