# 6주차 스타터 — AI 함정 #5 : 밉맵 비활성화 · 알파 블렌딩 남용

**컴퓨터그래픽스 (VF3500076) · 디자인앤테크놀로지전공 · 조성호**

- 기준 환경 : **Unity 6 · URP 3D 템플릿** (Color Space = Linear)
- Unity 프로젝트 전체가 아닌 **스크립트 3개** — 각자 실습 프로젝트(지각 실험실)에 복사해서 사용
- 관련 자료 : 슬라이드 `slides/w06/` · 워크북 `labs/w06/워크북.md` · 과제 `assignments/w06/`

---

## 파일 구성

| 파일 | 역할 | 언제 |
|---|---|---|
| `W06TrapTextureAlpha.cs` | **함정 재현본** — AI 가 내놓을 법한 원본 코드 | 실습 1 · 증상 관찰 |
| `W06FixedTextureAlpha.cs` | **정답본** — 같은 씬 + Inspector 스위치로 A/B 비교 | 실습 2 · 4 |
| `W06Audit.cs` | **진단 스크립트** — 밉맵 없는 텍스처 · Point 필터 · 투명 큐 재질 · 프레임타임 로그 | 검증 리포트 |

---

## 설치

1. `Assets/W06/` 폴더 생성 → 위 `.cs` 3개 복사
2. 새 씬 2개 생성 : `W06_Trap` · `W06_Fixed`
3. 각 씬에 빈 GameObject 생성
   - `W06_Trap` 씬 : `W06TrapTextureAlpha` + `W06Audit` 추가
   - `W06_Fixed` 씬 : `W06FixedTextureAlpha` + `W06Audit` 추가
4. 씬의 Main Camera 는 그대로 둠 — 스크립트가 위치·움직임을 자동 설정
5. Play

> 컴파일 오류가 나면 : 파일 이름과 클래스 이름이 같은지 확인 (`W06Audit.cs` ↔ `class W06Audit`)

---

## 재현본에서 관찰할 증상

| 증상 | 어디서 | 어떻게 확인 |
|---|---|---|
| 먼 바닥의 **물결 무늬(모아레)** | 화면 위쪽 먼 바닥 | Game 뷰 정지 상태 (Move Camera 끄기) |
| 먼 바닥의 **반짝임·지글거림** | 같은 곳 | Move Camera 켬 · Jitter Arcmin 0 ↔ 3 비교 |
| 나뭇잎 **앞뒤 뒤바뀜** | 덤불 | Scene 뷰에서 덤불 주위를 돌며 관찰 |
| 덤불 근처 **프레임 하락** | 덤불을 화면 가득 | `W06Audit` 프레임타임 로그 |

- 스크린샷 한 장으로는 반짝임이 잘 안 보임 → **휴대폰으로 모니터를 10초 녹화**
- `Jitter Arcmin` = 머리 미세 진동 흉내 (1 각분 = 1/60°) · 헤드셋 착용 시 늘 존재하는 흔들림

---

## 진단 체크리스트 (수정 전에 먼저)

- [ ] `W06Audit` 로그에 «밉맵 없음» 경고가 몇 개인가
- [ ] «Point 필터» 경고가 몇 개인가
- [ ] «투명 큐 재질» 이 몇 개이고, 그중 **정말 반투명이 필요한 것**은 몇 개인가
- [ ] Frame Debugger (Window → Analysis → Frame Debugger) 에서 투명 물체 그리기 단계 수
- [ ] 재현본 코드에서 위 결과의 원인이 되는 **줄**을 찾아 표시 (리포트에 줄 번호 기록)

> 원인 줄을 스스로 찾은 뒤 아래 «정답 확인» 을 펼칠 것

---

## 정답본 사용법 — Inspector 스위치

Play 중에 값을 바꾸면 즉시 반영 · Console 에 `mipmapCount` · `renderQueue` 출력

| 스위치 | 값 | 기대 결과 |
|---|---|---|
| Floor Preset | `PointNoMip` | 재현본과 같음 — 모아레 · 반짝임 |
| | `BilinearNoMip` | 계단은 줄지만 **반짝임 그대로** → 필터만으로는 해결 불가 |
| | `TrilinearMip` | 먼 바닥이 평균 회색으로 가라앉음 · 반짝임 소멸 · 먼 곳이 다소 흐림 |
| | `TrilinearMipAniso` | 위 + 비스듬한 먼 바닥 선명도 회복 (권장) |
| Aniso Level | 1 ~ 16 | 4 → 8 → 16 비교 · 커질수록 선명, 비용 증가 |
| Leaf Mode | `AlphaBlend` | 재현본과 같음 — 순서 뒤바뀜 |
| | `AlphaClip` | 순서 문제 소멸 · 가장자리 계단 (MSAA 로 완화) |
| Alpha Clip Threshold | 0.05 ~ 0.95 | 잎 두께 변화 · 출발점 0.5 |

---

## 에디터 설정으로 같은 수정을 할 때 (임포트한 텍스처·머티리얼 에셋)

| 대상 | 위치 | 설정 |
|---|---|---|
| 바닥 텍스처 | 텍스처 Inspector → Advanced | **Generate Mipmap** 켬 (버전에 따라 «Generate Mip Maps») |
| | 텍스처 Inspector | Filter Mode = **Trilinear** · Aniso Level = 4 |
| 잎 텍스처 | 텍스처 Inspector → Advanced | Generate Mipmap 켬 · 필요 시 **Mip Maps Preserve Coverage** 켬 + Alpha Cutoff Value |
| 잎 머티리얼 (URP Lit) | Surface Options | Surface Type = **Opaque** · **Alpha Clipping** 켬 · Threshold 0.5 · Render Face = Both |
| 유리 머티리얼 | Surface Options | Surface Type = Transparent (정말 반투명만) · 서로 교차하지 않게 배치 |
| 프로젝트 | URP Asset → Quality | Anti Aliasing (MSAA) **4x** — 잎 가장자리 계단 완화 |

---

## 알아 둘 한계

- **스크립트로 머티리얼 Surface 를 바꾸는 방식은 에디터 Play 확인용.** 빌드에서는 사용되지 않은 셰이더 변형(키워드 `_ALPHATEST_ON` 등)이 제거(stripping)되어 효과가 사라질 수 있음 → 실제 프로젝트는 **Inspector 에서 만든 머티리얼 에셋**을 사용
- `Shader.Find("Universal Render Pipeline/Lit")` 도 빌드에서는 그 셰이더를 쓰는 에셋이 있어야 포함됨
- 프로퍼티 이름(`_Surface` · `_AlphaClip` · `_Cutoff` · `_SrcBlendAlpha` 등)은 URP 버전에 따라 일부 다를 수 있음 → 동작이 다르면 머티리얼 Inspector 를 Debug 모드로 열어 실제 이름 확인

---

<details>
<summary><b>정답 확인 (실습 후에 펼칠 것)</b></summary>

### 재현본의 함정 위치

| 줄 (대략) | 코드 | 문제 |
|---|---|---|
| `BuildFloor` 첫 줄 | `new Texture2D(…, TextureFormat.RGBA32, false)` | `mipChain = false` → 축소판 없음 → 먼 바닥이 원본에서 한 점만 읽음 → 나이퀴스트 미달 |
| 다음 줄 | `tex.filterMode = FilterMode.Point` | «선명하게» 를 Point 로 해석 → 확대·축소 모두 계단·반짝임 |
| `MakeLeafTexture` | `new Texture2D(size, size, …, false)` | 잎 텍스처도 밉맵 없음 → 멀리서 잎 가장자리 반짝임 |
| `BuildBushes` | `MakeTransparent(mat)` | 구멍만 뚫리면 되는 잎을 알파 블렌딩 → 깊이 기록 안 함(ZWrite 0) → 물체 중심 거리로만 정렬 → 교차한 카드에서 순서 오류 + 오버드로 |

### 왜 Bilinear 로는 안 되는가

- Bilinear 는 **텍셀 4개**만 섞음 → 픽셀 하나가 텍셀 수십 개를 덮는 먼 바닥에서는 여전히 표본 부족
- 해결은 «미리 평균 내 둔 축소판(밉맵)» 에서 읽는 것 → `mipChain = true` + `Apply(true)`

### 왜 Alpha Clipping 인가

- 잎의 알파는 사실상 0 아니면 1 (모양 오리기) → 중간 투명도가 필요 없음
- Opaque + Alpha Clipping → 깊이 버퍼 사용 → 픽셀마다 더 가까운 것만 남음 → **그리는 순서와 무관**
- 렌더 큐 3000 → 2450 (AlphaTest)

</details>
