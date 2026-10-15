# 12주차 스타터 — 멀미 유발 씬 + 완화본

- 과목 : 컴퓨터그래픽스 VF3500076 · 12주 VR 인터랙션 심화
- 기준 : Unity 6 · URP · XR Interaction Toolkit 3.x · Input System · Meta Quest 3
- 함께 볼 것 : [워크북](../../labs/w12/워크북.md) · [SSQ 설문지](../../rubrics/SSQ-설문지.md) · [멀미 실습 동의서](../../setup/멀미실습-동의서.md)

> **안전 먼저** — 유발본 체험은 동의서를 낸 사람만 · 앉아서 · 스포터 옆에 두고 · 최대 3분.
> 체험자가 «그만» 하면 이유를 묻지 않고 즉시 중단.

---

## 1. 들어 있는 것

| 파일 | 역할 | 오늘 수업과의 연결 |
|---|---|---|
| `Scripts/SicknessLocomotion.cs` | **멀미 유발본** — SmoothDamp 가속 이동 + 부드러운 회전 90°/s · 자동 주행 · 3분 상한 | AI 함정 #9 재현 |
| `Scripts/ComfortLocomotion.cs` | **완화본 ①** — 등속 · 즉시 전환 이동 + 스냅 턴 22.5° | 유발 요인 ① 가속 · ② 회전 |
| `Scripts/BlinkTeleport.cs` | **완화본 ②** — 광선으로 지점 선택 → 0.15초 암전 → 순간 이동 | 유발 요인 ① 가속 · ③ 흐름 |
| `Scripts/ComfortVignette.cs` | **완화본 ③** — 움직일 때만 시야 가장자리 어둡게 + 암전 기능 | 유발 요인 ③ 주변 흐름 |
| `Scripts/ComfortModeSwitcher.cs` | 유발본 ↔ 완화본 버튼 전환 (빌드 한 번으로 교차 체험) | 실습 진행 |
| `Scripts/MotionLogger.cs` | 속도·가속도·회전 속도·프레임타임 기록 + 세션 요약 | «체감» 대신 «숫자» |
| `Scripts/FlowCorridor.cs` | 기둥·줄무늬 복도 자동 생성 (주변 광학 흐름 최대) · 정적 배칭 | 유발 요인 ③ · Part I 배칭 |

### 용어 풀이

- **리그 (XR Origin)** : 플레이어 «몸» 역할의 최상위 오브젝트 — 이걸 옮기면 사람이 이동한 것으로 처리. 카메라는 트래킹이 매 프레임 덮어쓰므로 직접 옮기지 않음 (11주 AI 함정 #8)
- **InputActionReference** : Input System 의 «입력 동작» 하나를 가리키는 칸 — 인스펙터에서 `XRI Default Input Actions` 안의 동작을 끌어 넣음
- **SmoothDamp** : 현재 값을 목표 값으로 «부드럽게» 따라가게 하는 함수 — 부드러움 = 가속 구간 → VR 에서는 멀미 구간
- **스냅 턴 (Snap turn)** : 회전을 연속 동작 대신 일정 각도씩 «건너뛰기»
- **베그넷 (Vignette)** : 시야 가장자리를 어둡게 좁히는 효과

---

## 2. 설치 (10분)

1. **전제** : 11주 실험실 씬이 Quest 에서 실행되는 상태 (XR Plug-in Management → OpenXR · Meta Quest 기능 켬 · XR Origin (XR Rig) 배치)
2. 이 폴더의 `Scripts/` 를 프로젝트 `Assets/Starters/W12/` 에 복사
3. **XRI 기본 이동 끄기** — XR Origin (XR Rig) 아래 `Locomotion` 오브젝트의 이동·회전·텔레포트 Provider 를 비활성화 (스타터 스크립트와 동시에 움직이면 결과가 섞임)
4. **복도** : 빈 오브젝트 `Corridor` 생성 → `FlowCorridor` 부착 → 머티리얼 2개 지정 (밝은 분홍 기둥 · 청록 줄무늬 권장)
5. **오버레이 머티리얼** : Project 창 → Create → Material → Shader `Universal Render Pipeline/Unlit` · Surface Type **Transparent** → 이름 `M_ComfortOverlay`
6. **XR Origin 에 부착** : `SicknessLocomotion` · `ComfortLocomotion` · `BlinkTeleport` · `ComfortVignette` · `MotionLogger` · `ComfortModeSwitcher`
7. **칸 채우기**

| 컴포넌트 | 칸 | 넣을 것 |
|---|---|---|
| 공통 | `rig` · `head` | XR Origin · Main Camera (비우면 자동 탐색) |
| SicknessLocomotion | `autoDrive` | 켬 (체험자는 조작하지 않음 → 조건 통일) |
| ComfortLocomotion | `moveAction` · `turnAction` | `XRI Left Locomotion/Move` · `XRI Right Locomotion/Turn` (또는 `Snap Turn`) |
| BlinkTeleport | `rayOrigin` · `teleportAction` · `fader` | Right Controller · `XRI Right Locomotion/Teleport Mode` · ComfortVignette |
| ComfortVignette | `overlayMaterial` | `M_ComfortOverlay` |
| ComfortModeSwitcher | 각 칸 · `switchAction` | 위 컴포넌트들 · 왼쪽 메뉴 버튼 등 스포터용 버튼 · `startMode = Comfort` |
| ComfortModeSwitcher | `fixedReference` | XR Origin 의 **자식**으로 만든 희미한 바닥 격자 (실제 방 기준 고정 = 유발 요인 ⑥ 대응) |

> 입력 동작 이름은 XRI Starter Assets 버전마다 조금씩 다름 → `XRI Default Input Actions` 에셋을 열어 실제 이름 확인

8. Build and Run (USB) → 헤드셋에서 실행 · OVR Metrics Tool 켜기

---

## 3. 실습 순서 (워크북과 동일)

| 단계 | 모드 | 할 일 |
|---|---|---|
| A | `Sickness` | 스포터가 버튼으로 유발본 전환 → 체험 최대 3분 → SSQ 직전·직후 |
| 휴식 | — | 최소 10분 · 증상 1단계 이하로 돌아왔는지 확인 · 3단계였으면 B 금지 |
| B | `Comfort` | 기저선 SSQ 재측정 → 완화본 체험 (스틱 이동 · 스냅 · 텔레포트) → SSQ |
| 순서 균형 | — | 조의 절반은 **B 를 먼저** (순서 효과 상쇄) |

---

## 4. 측정값 꺼내기

- 에디터 : Console 에 `[MotionLogger]` 요약 한 줄
- Quest : CSV 가 `/sdcard/Android/data/<패키지 이름>/files/motion_<모드>_<시각>.csv`
  - Meta Quest Developer Hub → Device Manager → 파일 탐색, 또는 `adb pull`
  - 요약은 CSV 마지막 줄 (`#` 으로 시작) · `adb logcat -s Unity` 로도 확인
- 워크북 기록표에 옮길 값 : **최대 가속도 · 0.7 m/s² 초과 프레임 수 · 연속 회전 시간 · 11.1 ms 초과 프레임 수**

---

## 5. 실험해 볼 것 (확장)

- `ComfortLocomotion.snapAngle` 22.5 ↔ 45 비교 → 방향 감각 차이 메모
- `ComfortVignette.strength` 0.3 / 0.6 / 0.9 → 답답함 vs 편안함
- `SicknessLocomotion` 에 베그넷만 켜 보기 (`ComfortVignette` 는 리그 움직임으로 자동 작동) → 가속은 그대로 두고 흐름만 줄였을 때
- `FlowCorridor.combineStatic` 켬/끔 → Game 뷰 Stats 의 `Batches` 변화 (Part I 정적 배칭)

---

## 6. 알려진 한계

- `ComfortVignette` 는 원리 확인용 최소 구현 — 카메라 0.3 m 앞 판이라 그보다 가까운 물체(손 등)는 판 앞에 그려질 수 있음 · 정식 프로젝트는 XRI Starter Assets 의 **Tunneling Vignette** 프리팹 권장
- 머리에 붙은 요소는 원칙적으로 금지(10주 함정 #7) · 베그넷·암전은 «정보 없는 가장자리 어둠» 이라 예외 · 글자·아이콘을 올리지 말 것
- `MotionLogger` 의 가속도는 리그 기준 — 사람이 실제로 걷거나 고개를 돌린 움직임은 포함하지 않음 (그건 전정계가 실제로 느끼는 움직임이라 충돌이 아님)
- 수치 기준 0.7 m/s² · 27.1°/s 는 소규모 연구(18명)의 **평균** — 안전선이 아니라 비교 기준
