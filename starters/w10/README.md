# 10주차 스타터 — 같은 메뉴 UI 두 벌 (Overlay · World Space)

**컴퓨터그래픽스 (VF3500076) · 10주 인터랙션 설계 · AI 함정 #7**

- 목적 : 같은 메뉴를 **Screen Space Overlay 버전**(함정 재현본)과 **World Space 버전**(정답본) 두 벌로 만들어 보관 → 11주차 헤드셋 안에서 비교
- 이 폴더 = **스크립트 4개 + 씬 구성 안내** · Unity 씬·프리팹 파일은 각자 프로젝트에서 아래 절차로 생성 (Unity 버전마다 씬 파일 호환 문제 회피)
- 기준 : Unity 6 · URP · Input System 패키지 · (11주 이후) XR Interaction Toolkit 3.x

---

## 0. 용어 풀이

| 용어 | 쉬운 뜻 |
|---|---|
| Canvas (캔버스) | 버튼·글자 같은 UI 를 올려 두는 바탕판 |
| Render Mode | 그 바탕판을 **어디에 그릴지** — 화면 위(Overlay) · 카메라 앞(Camera) · 공간 속(World Space) |
| 액션 맵 (Action Map) | 상황별 입력 묶음 — 게임 중 `Player` · 메뉴 중 `UI` |
| 상태 기계 | «지금 어떤 상태인가» 하나만 기억하고, 사건이 오면 다음 상태로 넘어가는 설계 |
| 각크기 | 물체가 눈에서 차지하는 각도(°) — 실제 크기와 거리를 함께 반영 |
| DMM | 1 m 거리 기준으로 환산한 크기(mm) — 크기(mm) ÷ 거리(m) |

---

## 1. 파일

| 파일 | 역할 | 붙이는 곳 |
|---|---|---|
| `Scripts/GameStateMachine.cs` | Menu · Playing · Paused 상태 기계 · Player ↔ UI 액션 맵 전환 · 시간 정지 | 빈 오브젝트 `GameState` |
| `Scripts/PauseMenuUI.cs` | 메뉴 버튼 연결 · 이벤트 구독/해제 짝 · 클릭 콜백 횟수 로그 | 메뉴 패널 |
| `Scripts/CanvasAudit.cs` | 모든 루트 캔버스의 모드·Scale·거리·각크기·DMM 출력 + 판정 | 아무 오브젝트 1개 |
| `Scripts/WorldSpaceCanvasPlacer.cs` | 캔버스를 World Space 로 바꿔 1.5 m 앞에 배치 · 비교용 Overlay 되돌리기 | Canvas |

---

## 2. 공통 준비 (5분)

1. 지각 실험실 프로젝트 열기 (새로 만들 경우 **Universal 3D** 템플릿)
2. `Scripts/` 의 4개 파일을 프로젝트 `Assets/Scripts/W10/` 로 복사
3. **Project Settings → Player → Other Settings → Active Input Handling** = `Input System Package (New)` 확인
4. `Assets/InputSystem_Actions` 더블클릭 → **Player** 맵에 액션 `Pause` 추가
   - Action Type : `Button`
   - 바인딩 : `Escape [Keyboard]` · `Start [Gamepad]`
   - 저장 (Save Asset)
5. Main Camera 위치 : **(0, 1.6, 0)** — 눈높이 1.6 m 가정 (11주차에는 XR Origin 이 대신함)

---

## 3. A 버전 — Overlay (함정 재현본)

> AI 에게 «점수와 일시정지 버튼이 있는 HUD 만들어줘» 만 요청했을 때 나오는 구성과 동일

1. Hierarchy → **UI → Canvas** 생성 → 이름 `Menu_Overlay`
   - Render Mode : `Screen Space - Overlay` (기본값)
   - Canvas Scaler : `Scale With Screen Size` · Reference 1920×1080
2. Canvas 안에 **Panel** → 그 안에 **Text - TextMeshPro** 2개 (`점수 1,240` · `일시정지 상태`) · **Button - TextMeshPro** 2개 (`계속` · `종료`)
   - 처음 TMP 를 쓰면 «Import TMP Essentials» 창 → Import
3. Panel 에 `PauseMenuUI` 부착 → 버튼·텍스트·`GameState` 연결
4. EventSystem : 자동 생성된 것 사용 → 입력 모듈이 **Input System UI Input Module** 인지 확인 (구 Standalone 이면 «Replace with InputSystemUIInputModule» 버튼)
5. 빈 오브젝트 `GameState` → `GameStateMachine` 부착
   - actions : `InputSystem_Actions` · pause : `Player/Pause` · resume : `UI/Cancel` · menuPanel : Panel
6. Play → Escape 로 일시정지 · 메뉴 표시 → «계속» 클릭 · Escape 로 복귀 확인
7. `CanvasAudit` 실행 → 콘솔에 `Overlay 1개` 경고 확인 = **함정 재현 완료**

---

## 4. B 버전 — World Space (정답본)

1. `Menu_Overlay` 를 복제(Ctrl+D) → 이름 `Menu_World` · 원본은 비활성화(체크 해제)해 보관
2. `Menu_World` 에 `WorldSpaceCanvasPlacer` 부착 → 값 확인
   - distance `1.5` · yawOffset `0` · dropBelowEye `0.15` · canvasUnits `600 × 360` · unitScale `0.001`
3. 컴포넌트 ⋮ 메뉴 → **Place World Space** → 콘솔에 `폭 0.60 m · 거리 1.50 m · 각크기 22.6°` 출력
   - 손계산 대조 : 2·atan(0.3 / 1.5) = 2·atan(0.2) ≈ 22.6°
   - 패널 안 요소(버튼·글자)가 넘치면 Panel·버튼 RectTransform 을 캔버스 600×360 안으로 재배치
4. Canvas Scaler 는 World Space 에서 의미가 달라짐 → `Dynamic Pixels Per Unit` 1 · 글자가 흐리면 2~3
5. 글자 크기 점검 : TMP Font Size **36 이상** (36 × 0.001 = 3.6 cm → 1.5 m 에서 24 DMM)
6. `CanvasAudit` 다시 실행 → `World Space · 거리 1.50 m · 정면에서 0° … 통과` · `Overlay 0개`
7. Scene 뷰에서 패널이 카메라 앞 1.5 m, 눈보다 약간 아래에 있는지 육안 확인

### 11주차에 추가할 것 (지금은 생략 가능)

| 부품 | 위치 | 이유 |
|---|---|---|
| Tracked Device Graphic Raycaster | `Menu_World` Canvas | 컨트롤러 광선(3D)으로 버튼 판정 |
| XR UI Input Module | EventSystem (기존 모듈 교체) | 컨트롤러 입력을 UI 이벤트로 변환 |
| XR Ray Interactor 또는 Near-Far Interactor (UI Interaction 켬) | XR Origin 의 손 | 가리킬 광선 |
| Pause 바인딩 | Player/Pause | Quest 컨트롤러 메뉴 버튼 |

- XRI 설치 후 `Place World Space` 를 다시 실행하면 Tracked Device Graphic Raycaster 자동 추가
- 지름길 : **GameObject → XR → UI Canvas / UI EventSystem** (XRI 버전에 따라 메뉴 위치 조금씩 다름)

---

## 5. 두 벌 보관 규칙

- 한 씬에 두 캔버스를 두고 **한쪽만 활성화** 또는 씬 2개 (`W10_Overlay` · `W10_World`)
- 11주차 첫 30분 : 두 벌을 각각 Quest 에 빌드 → 아래 표 채우기

| 버전 | 에디터 예측 | 헤드셋 실제 |
|---|---|---|
| Overlay | 안 보일 것 | |
| World Space 1.5 m | 편안 · 약 23° | |
| World Space 0.3 m (일부러) | 이중상 · 눈 피로 | |

---

## 6. 막힐 때

| 증상 | 확인 |
|---|---|
| `InvalidOperationException … UnityEngine.Input` | 다른 스크립트(또는 AI 코드)가 구 `Input.GetKey` 사용 → InputAction 으로 교체 |
| Escape 로 복귀 안 됨 | resume 에 `UI/Cancel` 지정 여부 · 일시정지 중엔 Player 맵이 꺼져 있음 |
| World Space 패널이 거대 · 안 보임 | Scale 1 그대로 → `Place World Space` 재실행 (0.001) |
| 패널 뒷면만 보임 · 글자 좌우 반전 | 회전 반대 → `Place World Space` 재실행 |
| 클릭 로그가 여러 번 | `OnDisable` 의 RemoveListener 누락 (실습 5 의 의도된 재현일 수도 있음) |
| 버튼이 안 눌림 (에디터) | 씬에 EventSystem 1개 · Canvas 의 Graphic Raycaster · World Space 의 Event Camera 지정 |
