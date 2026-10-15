# 트러블슈팅 FAQ

**컴퓨터그래픽스 (VF3500076) · 디자인앤테크놀로지전공 · 조성호 · 2026-2**

- 학기 중 계속 갱신 · 새 문제를 해결했다면 메일로 제보 → 다음 판에 추가
- 질문 메일에 넣을 것 : **① 무엇을 하려 했나 ② 무엇이 일어났나 (오류 문구 원문 · 캡처) ③ OS · Unity 버전 ④ 이미 해 본 것**
- AI 에게 물어볼 때도 같은 4가지를 붙이면 답이 정확해짐 (1주차 함정 #0 : 컨텍스트 없는 질문 → 그럴듯한 추측)
- **Quest 연결 · APK 빌드 · 헤드셋 실행 문제** → [빌드 가이드](빌드-가이드.md)

| 분야 | 번호 |
|---|---|
| A. 설치 · 계정 | A1 ~ A6 |
| P. 프로젝트 · 에디터 | P1 ~ P7 |
| S. 스크립트 · C# | S1 ~ S6 |
| R. 렌더링 · 화면 | R1 ~ R6 |
| G. Git · GitHub | G1 ~ G7 |

---

## A. 설치 · 계정

<a id="a1"></a>
### A1. Hub 에서 에디터 설치가 멈추거나 실패

- 원인 후보 : 저장 공간 부족 · 네트워크 끊김 · 백신 프로그램의 설치 파일 차단
- 해결
  1. 여유 공간 약 30 GB 이상 확보
  2. Hub 재시작 → Installs 에서 실패한 버전 제거 후 재설치
  3. 백신 실시간 검사를 잠시 끄거나 Unity 설치 폴더를 예외 등록
  4. 학교 와이파이에서 반복 실패 → 다른 네트워크에서 시도

<a id="a2"></a>
### A2. «No valid Unity Editor license» · 라이선스 오류로 에디터가 안 열림

- 원인 : Hub 에 로그인하지 않았거나 라이선스 미등록 · 만료
- 해결 : Hub 로그인 확인 → Preferences(설정) → **Licenses → Add → Get a free personal license** → Hub 와 에디터 재시작
- 오프라인 환경이면 → 인터넷 연결 후 1회 로그인 필요

<a id="a3"></a>
### A3. Android Build Support 를 빼고 설치했음

- 해결 : Hub → **Installs** → 해당 버전 톱니바퀴 아이콘 → **Add modules** → Android Build Support + **OpenJDK** + **Android SDK & NDK Tools** 체크
- 확인 : Installs 목록의 버전 옆 안드로이드 아이콘

<a id="a4"></a>
### A4. macOS 에서 «확인되지 않은 개발자» · «손상된 앱» 경고

- 해결 : **시스템 설정 → 개인정보 보호 및 보안** → 아래쪽 차단 안내 옆 **확인 없이 열기** · 공식 사이트에서 받은 설치 파일인지 먼저 확인
- Apple Silicon Mac 인데 에디터가 느림 → Hub 가 Intel 용(x86_64) 에디터를 받았는지 확인 → Apple silicon 용으로 재설치

<a id="a5"></a>
### A5. VS Code 에서 자동완성 · 오류 밑줄이 안 나옴

- 원인 후보 : Unity 쪽 에디터 연결 누락 · C# Dev Kit 미설정 · 프로젝트 파일 미생성
- 해결 순서
  1. Unity **External Tools → External Script Editor = Visual Studio Code**
  2. 같은 화면의 **Regenerate project files** 클릭
  3. Package Manager 에서 **Visual Studio Editor** 패키지 설치·최신 여부 확인
  4. VS Code 에 **Unity** 확장 설치 · C# Dev Kit 이 .NET SDK 설치를 요구하면 설치
  5. 스크립트는 **Unity 에서 더블클릭**해서 열기 (VS Code 에서 파일만 열면 프로젝트 인식이 안 될 수 있음)

<a id="a6"></a>
### A6. AI 도구 설치 후 터미널에서 «command not found» · «인식되지 않는 명령»

- 원인 : 설치 경로가 PATH(명령을 찾는 폴더 목록)에 아직 반영되지 않음
- 해결
  1. 터미널을 **완전히 닫고 새로 열기** (가장 흔한 해결)
  2. `npm` 으로 설치했다면 `node -v` · `npm -v` 확인 → 안 나오면 Node.js LTS 재설치
  3. Windows 는 PowerShell 실행 정책 오류가 날 수 있음 → 오류 문구를 그대로 도구 공식 문서·FAQ 에서 검색
  4. 그래도 안 되면 다른 설치 방식(설치 스크립트 · 패키지 관리자) 시도

---

## P. 프로젝트 · 에디터

<a id="p1"></a>
### P1. 프로젝트가 한글 경로 · OneDrive 폴더에 있음 → 이상한 오류

- 증상 : 빌드 실패 · 파일 접근 거부 · 에셋이 사라졌다 나타남
- 해결 : Unity 와 에디터를 닫고 → 프로젝트 폴더를 `C:\UnityProjects\` 같은 **영문·공백 없는·동기화 안 되는 경로**로 이동 → Hub 에서 **Add → 이동한 폴더** 로 다시 등록

<a id="p2"></a>
### P2. 프로젝트 첫 실행 · 다른 PC 에서 열기가 너무 오래 걸림

- 원인 : `Library/` 폴더(캐시)를 새로 만드는 중 · 정상 동작
- 대처 : 첫 실행은 수 분~수십 분 · 진행 막대가 움직이면 기다림
- `Library/` 는 지워도 다시 생성됨 → 이상할 때 Unity 를 닫고 `Library/` 삭제 후 재실행하는 것이 «캐시 초기화»

<a id="p3"></a>
### P3. 열자마자 «Enter Safe Mode?» 창

- 원인 : 스크립트 **컴파일 오류**(C# 문법 오류 등) 때문에 정상 모드로 열 수 없음
- 해결 : Safe Mode 로 열기 → **Console** 창의 빨간 오류 클릭 → 해당 줄 수정 → 오류 0개가 되면 자동으로 정상 모드
- AI 가 만든 스크립트를 넣은 직후라면 → 그 파일부터 의심 · 최근 커밋으로 비교 (`git diff`)

<a id="p4"></a>
### P4. «다른 에디터 버전으로 만든 프로젝트» 경고

- 원인 : 프로젝트를 만든 Unity 버전과 지금 여는 버전이 다름
- 원칙 : **수업 공지 버전 하나로 통일** · 업그레이드는 되돌리기 어려움
- 꼭 열어야 하면 → 먼저 커밋 또는 폴더 복사본 만들고 진행

<a id="p5"></a>
### P5. 씬 작업이 저장되지 않았음 · Hierarchy 위에 «Untitled»

- 원인 : 씬 파일로 저장하지 않음 · Unity 는 씬을 **직접 저장**해야 함
- 해결 : **Ctrl + S** (macOS **Cmd + S**) → `Assets/Scenes/` 에 저장 · Hierarchy 맨 위 씬 이름 옆 `*` = 저장 안 된 변경 있음

<a id="p6"></a>
### P6. Play 모드 중에 바꾼 값이 Play 를 끄자 사라짐

- 원인 : Play 모드 변경은 **임시** · 정지하면 원래 값으로 복귀 (설계된 동작)
- 대처 : 좋은 값을 찾으면 컴포넌트 ⋮ 메뉴 → **Copy Component** → 정지 후 **Paste Component Values**
- 예방 : **Preferences → Colors → Playmode tint** 를 눈에 띄는 색으로 → Play 중임을 바로 인지

<a id="p7"></a>
### P7. 창 배치가 엉망 · Scene / Inspector 창이 사라짐

- 해결 : 오른쪽 위 **Layout** 메뉴 → **Default** · 개별 창은 **Window → General** 에서 다시 열기

---

## S. 스크립트 · C#

<a id="s1"></a>
### S1. 스크립트를 오브젝트에 붙일 수 없음 · «The script class cannot be found»

- 원인 후보 : **파일 이름 ≠ 클래스 이름** · 컴파일 오류가 남아 있음 · `MonoBehaviour` 상속 누락
- 해결 : `Spin.cs` 안의 클래스가 `public class Spin : MonoBehaviour` 인지 확인 · Console 오류 0개 확인
- AI 가 파일 이름과 다른 클래스 이름을 쓰는 경우가 흔함 → 명세 [제약] 에 «파일 이름 = 클래스 이름» 추가

<a id="s2"></a>
### S2. «error CS0246: The type or namespace name '…' could not be found»

- 원인 : 필요한 `using` 문 누락 · 해당 기능의 **패키지 미설치** · 오타
- 해결 : 오류에 나온 이름을 검색 → 어느 네임스페이스·패키지 소속인지 확인 → `using` 추가 또는 Package Manager 에서 설치
- 예 : `XRGrabInteractable` 오류 → XR Interaction Toolkit 패키지 필요 (11주차)

<a id="s3"></a>
### S3. «NullReferenceException: Object reference not set to an instance of an object»

- 뜻 : 비어 있는(null) 참조를 사용하려 함
- 흔한 원인 : Inspector 의 변수 칸을 비워 둠 (None) · `GetComponent<…>()` 가 해당 부품을 못 찾음 · `Find` 로 찾는 이름 오타
- 해결 : Console 오류를 더블클릭 → 해당 줄의 변수가 무엇인지 확인 → Inspector 에서 칸 채우기 · 오브젝트에 필요한 컴포넌트 추가

<a id="s4"></a>
### S4. 이동·회전 속도가 컴퓨터마다 다름

- 원인 : `Update` 에서 프레임마다 고정 값만큼 이동 · `Time.deltaTime` 누락 → **AI 함정 #2** (3주차)
- 해결 : `transform.Translate(dir * speed * Time.deltaTime)` 처럼 시간 기준으로
- 검증 : `Application.targetFrameRate` 를 30 · 120 으로 바꿔 10초 후 위치 비교 (`QualitySettings.vSyncCount = 0` 필요)

<a id="s5"></a>
### S5. 회전이 특정 각도에서 이상하게 튀거나 잠김

- 원인 : `eulerAngles` 를 누적해 회전 → 짐벌락 · 값 튐 → **AI 함정 #1** (2주차)
- 해결 : `Quaternion` 으로 누적 (`transform.Rotate(...)` 또는 `Quaternion.AngleAxis(...) * transform.rotation`)

<a id="s6"></a>
### S6. 코드를 고쳤는데 Unity 에 반영이 안 됨

- 확인 : 에디터에서 **저장**했는가 (VS Code 탭의 ● 표시) · Unity 창으로 돌아오면 잠시 컴파일 (오른쪽 아래 회전 아이콘)
- 자동 새로고침이 꺼져 있으면 → **Preferences → Asset Pipeline → Auto Refresh** 확인 · 또는 **Ctrl + R** (macOS **Cmd + R**)

---

## R. 렌더링 · 화면

<a id="r1"></a>
### R1. 물체가 분홍색(마젠타)으로 보임

- 원인 : 머티리얼의 셰이더가 **현재 렌더 파이프라인(URP)과 호환되지 않음** · 주로 Built-in 용 에셋을 가져왔을 때
- 해결 : 머티리얼 셰이더를 **Universal Render Pipeline/Lit** 으로 변경 · 여러 개면 **Window → Rendering → Render Pipeline Converter** 로 일괄 변환
- AI 가 `Shader.Find("Standard")` 를 쓰는 코드도 같은 증상 → URP 셰이더 이름 요구

<a id="r2"></a>
### R2. 장면이 전체적으로 바래 보이거나 너무 어둡거나 밝음

- 확인 1 : **Project Settings → Player → Color Space = Linear** (5주차 · AI 함정 #4)
- 확인 2 : 텍스처 Inspector 의 **sRGB** 체크 — 색 텍스처는 켬 · 노멀맵·마스크 같은 데이터 텍스처는 끔
- 확인 3 : Lighting 창 → Environment 의 환경광 설정 · Global Volume 의 노출(Post Exposure) 값

<a id="r3"></a>
### R3. Game 뷰가 Scene 뷰와 다르게 보임 · 아무것도 안 보임

- 원인 후보 : Main Camera 가 엉뚱한 방향 · 카메라가 물체 안에 있음 · 카메라 **Culling Mask** 에서 레이어 제외 · Game 뷰 **Display** 번호 불일치
- 빠른 해결 : Hierarchy 에서 Main Camera 선택 → **GameObject → Align With View** (Scene 뷰 시점에 카메라를 맞춤)

<a id="r4"></a>
### R4. 겹친 면이 지글지글 깜빡임

- 원인 : 거의 같은 깊이의 두 면 · 깊이 버퍼 정밀도 부족 → **z-fighting** (4주차 · AI 함정 #3)
- 해결 : 카메라 **Clipping Planes near** 를 너무 작게 두지 않기 (예 0.01 → 0.1~0.3) · far 줄이기 · 겹친 면 사이를 조금 띄우기

<a id="r5"></a>
### R5. 그림자가 계단처럼 깨지거나 아예 안 보임

- 안 보임 : 광원 **Shadow Type** 이 No Shadows · URP Asset 의 그림자 설정 꺼짐 · 그림자 거리(Max Distance) 밖
- 계단 현상 : URP Asset 의 **Shadow Resolution** · **Cascade** 수 · Max Distance 조절 (5주차)
- VR 주의 : 실시간 그림자는 비쌈 → 광원 1개만 실시간, 나머지 베이크 (AI 함정 #4)

<a id="r6"></a>
### R6. URP 설정은 어디서 바꾸나

- **Project Settings → Graphics** : 기본으로 쓰는 URP Asset 지정
- **Project Settings → Quality** : 품질 단계별로 다른 URP Asset 지정 가능 → 실제 적용 값은 현재 품질 단계 기준
- URP Asset 파일 (보통 `Assets/Settings/`) 을 선택하면 Inspector 에 그림자·안티에일리어싱·렌더 스케일 등 표시

---

## G. Git · GitHub

<a id="g1"></a>
### G1. `Library/` 폴더가 커밋되어 업로드가 엄청 느리거나 실패

- 원인 : `.gitignore` 없음 · 또는 위치가 틀림 (Assets 와 **같은 폴더**에 있어야 함)
- 해결
  ```bash
  # .gitignore 를 프로젝트 최상위에 둔 뒤
  git rm -r --cached Library Temp Logs obj
  git commit -m "Library 등 자동 생성 폴더 제외"
  ```
- 이미 push 에 실패했다면 위 정리 후 다시 push

<a id="g2"></a>
### G2. push 거절 — «rejected … (fetch first)» · «non-fast-forward»

- 원인 : GitHub 쪽에 내 컴퓨터에 없는 커밋이 있음 (예 : 웹에서 README 생성 · 다른 PC 에서 push)
- 해결 : `git pull --rebase` → 충돌 없으면 `git push`
- 처음 만든 저장소에 README 를 넣어 생긴 경우가 대부분 → 가이드대로 **빈 저장소**로 만들면 예방

<a id="g3"></a>
### G3. «File … is 123.45 MB; this exceeds GitHub's file size limit of 100.00 MB»

- 원인 : 100 MB 넘는 파일 (고해상도 영상·텍스처·빌드 결과 APK 등)
- 해결 : 그 파일을 저장소에서 빼기 (`.gitignore` 추가 + `git rm --cached 파일`) → 이미 커밋 기록에 들어갔다면 그 커밋을 고쳐야 함 → 혼자 해결이 어려우면 질문
- 꼭 필요한 큰 에셋 → **Git LFS** 사용 · 빌드 결과(APK)는 저장소에 넣지 않음

<a id="g4"></a>
### G4. 팀 프로젝트에서 같은 씬을 고쳐 충돌(conflict)

- 원인 : `.unity` 씬 파일 = 텍스트지만 사람이 합치기 어려운 구조
- 예방 : **씬 하나 = 한 사람 담당** · 공용 물체는 **프리팹**으로 쪼개 각자 다른 파일 수정 · 작업 전 `git pull`
- 이미 충돌 : 한쪽 버전을 통째로 채택 (`git checkout --ours 파일` 또는 `--theirs`) 후 변경분 다시 적용 · Unity 의 **Smart Merge (UnityYAMLMerge)** 도구 설정도 가능

<a id="g5"></a>
### G5. 다른 PC 에서 받았더니 머티리얼·스크립트 연결이 전부 끊김 (Missing)

- 원인 : **`.meta` 파일 누락** — Unity 는 `.meta` 안의 고유 번호(GUID)로 파일끼리 연결
- 해결 : `.meta` 파일을 항상 함께 커밋 · `.gitignore` 에서 `*.meta` 를 제외하지 않았는지 확인
- 파일 이동·이름 변경은 **Unity Project 창에서** (탐색기·Finder 에서 하면 `.meta` 와 짝이 깨질 수 있음)

<a id="g6"></a>
### G6. push 할 때 비밀번호를 넣어도 «Authentication failed»

- 원인 : GitHub 는 명령어 push 에 **계정 비밀번호를 받지 않음**
- 해결 (하나 선택)
  - Windows : Git for Windows 의 **Git Credential Manager** 브라우저 로그인 창에서 승인
  - **GitHub CLI** 설치 후 `gh auth login`
  - GitHub 설정 → Developer settings → **Personal access token** 발급 → 비밀번호 칸에 토큰 입력
- 토큰은 비밀번호와 같음 → 저장소·프롬프트·캡처에 노출 금지

<a id="g7"></a>
### G7. AI 에이전트가 파일을 망가뜨렸음 · 이전 상태로 되돌리고 싶음

- 아직 커밋 안 함 : `git status` 로 바뀐 파일 확인 → `git restore 파일` (전체는 `git restore .`) · 새로 생긴 파일은 직접 삭제
- 이미 커밋함 : `git log --oneline` 으로 커밋 확인 → `git revert 커밋번호` (기록을 남기며 되돌리기)
- 예방 : **AI 에게 큰 작업을 맡기기 직전마다 커밋**

---

## Quest · 빌드 관련

- 헤드셋이 PC 에 안 잡힘 · 개발자 모드 · APK 설치 실패 · Build and Run 오류 · macOS 빌드 → **[빌드 가이드](빌드-가이드.md)**
- Meta 개발자 계정 인증 → 2주차 과제 안내문 (`assignments/w02/`)

---

## 갱신 기록

| 날짜 | 내용 |
|---|---|
| 2026-10-15 | 초판 — 설치·프로젝트·스크립트·렌더링·Git 32항목 |
