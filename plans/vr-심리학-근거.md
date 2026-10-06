# VR 심리학·지각 연구 근거 모음

- 용도 : 컴퓨터그래픽스(VR 포함) 5~15주 강의자료 설계용 1차 출처 모음 · 부산대 디자인 2학년 · 조성호
- 작성 기준 : 동료심사 논문 · 제조사 공개 가이드라인 · LaValle 『Virtual Reality』(Cambridge University Press, 2023, 전문 무료 <https://lavalle.pl/vr/>)
- 표기 규칙
  - 각 주장 끝에 출처 URL
  - **«확실하지 않음»** : 재현 실패, 표본 과소, 학계 논쟁 중, 2차 출처만 확보
  - **«확인 필요»** : 수치를 1차 출처에서 확인하지 못해 비워 둔 항목
- 금지 사항 : 출처 없는 숫자 기재

---

## 1. 프레즌스·몰입

### 핵심 결론

- 몰입 (immersion) : 시스템 속성 · 객관 측정 대상
- 프레즌스 (presence) : 사용자의 주관 경험 · 의식 상태
- Slater 의 2분법 : 장소 착각 (Place Illusion, PI) + 개연성 착각 (Plausibility Illusion, Psi)
- 설문 기반 프레즌스 측정은 구성 타당도 논쟁 지속 -> 설문 단독 결론 금지

### 근거 연구

| 연구 | 지면 | 표본 | 핵심 수치·내용 | 출처 |
|---|---|---|---|---|
| Slater & Wilbur (1997) | Presence: Teleoperators and Virtual Environments 6(6):603–616 | 이론 논문 | 몰입의 4축 : inclusive · extensive · surrounding · vivid + 신체 일치도 · 자율 반응 | <https://www.semanticscholar.org/paper/A-Framework-for-Immersive-Virtual-Environments-on-Slater-Wilbur/3c62e25f7f6a035ef59eefd7ff13ca42c59a716f> |
| Slater (2009) | Philosophical Transactions of the Royal Society B 364(1535):3549–3557 · DOI 10.1098/rstb.2009.0138 | 이론 논문 | PI(«being there») 와 Psi(«지금 일어나는 중») 는 직교 성분 -> 둘이 동시 성립 시 현실적 반응 발생 | <https://www.macs.hw.ac.uk/~ruth/year4VEs/Resources/Slater2009RoyalSoc.html> |
| Slater (2018) | British Journal of Psychology 109(3) | 이론 논문 | 몰입 = 기술 속성 · 프레즌스 = 착각 경험 으로 용어 재정리 | <https://bpspsychub.onlinelibrary.wiley.com/doi/abs/10.1111/bjop.12305> |
| Witmer & Singer (1998) PQ | Presence 7(3) | — | 4개 하위척도 : involvement/control · sensory fidelity · naturalness · interface quality | <https://www8.informatik.umu.se/~jwworth/PresenceMeasurement.pdf> |
| IPQ (Schubert et al. 2001) | — | — | 14문항 · 7점 리커트 · 하위척도 3개 (spatial presence · involvement · realness) + 일반 프레즌스 1문항 | <https://arxiv.org/pdf/2504.10162> |
| SUS (Slater·Usoh·Steed) | Presence · 1994 초판 3문항, Usoh et al. 2000 6문항 | — | 7점 척도 · 요인구조 미설정 | <https://www8.informatik.umu.se/~jwworth/PresenceMeasurement.pdf> |
| Usoh et al. (2000) | Presence 9(5) | — | WS·SUS 모두 가상환경과 실제 현실을 변별하지 못함 -> 변별 타당도 결함 | <https://www.researchgate.net/publication/2457864_Using_Presence_Questionnaires_in_Reality> |
| Slater (2004) «How colorful was your day?» | Presence 13(4):484–493 | 온라인 응답자 74명 | 임의로 만든 가상 속성 «경험의 색채감» 도 과제 성취·기분과 상관 -> 사후 설문만으로는 존재하지 않는 구성도 측정되는 것처럼 보임 | <https://dl.acm.org/doi/10.1162/1054746041944849> |
| Schwind et al. (2019) | CHI 2019 | — | 프레즌스 설문 시행 자체가 응답에 영향 -> 시행 순서·기준 조건 설계 필요 | <https://dl.acm.org/doi/10.1145/3290605.3300590> |
| Feick et al. (2024) IPQ 20년 분석 | ACM (DOI 10.1145/3689046) | 다수 논문 집계 | IPQ 점수 분포 기반 해석 구간 제안 | <https://dl.acm.org/doi/10.1145/3689046> |

### 비판점 (슬라이드에 반드시 병기)

- 사후 설문 : 요구 특성 (demand characteristics) · 회상 편향 취약
- 척도 간 환산 불가 : PQ·IPQ·SUS 점수 직접 비교 금지
- 실제 현실과 가상환경을 변별하지 못한 보고 존재 -> 절대 점수의 의미 제한
- **«확실하지 않음»** : Witmer & Singer PQ 문항 수는 판본별 차이 (19문항·32문항 보고 혼재) -> **«확인 필요»**

### 수업 적용

- 11주 VR 개발 기초 : «몰입 = 하드웨어 사양 / 프레즌스 = 사용자 보고» 로 용어 분리 후 Quest 3 사양표와 연결
- 14주 플레이테스트 : IPQ 14문항 한국어 번역본을 조별 교차 체험 평가지로 사용 + 설문 한계 1장 병기
- 15주 시연 : 프레즌스 점수를 성적 지표로 쓰지 않음 (Slater 2004 근거 제시)

---

## 2. 사이버멀미

### 핵심 결론

- 이론 두 갈래 : 감각 충돌 이론 (sensory conflict) vs 자세 불안정 이론 (postural instability) · 단일 이론으로 전체 설명 미달
- 유발 요인 서열 : 회전 광학 흐름 > 병진 광학 흐름, 지연 증가 · 가속 노출 · 넓은 주변시 자극
- 완화 기법 효과 크기 : 주변시 FOV 제한 ≈ −0.40 (메타분석), 시점 스냅 −40~50% (단일 연구)
- 개인차가 평균 효과보다 큼 -> 개인별 설정 노출 필요

### 2-1. 이론 대립

| 이론 | 출처 | 요지 | 반증·한계 |
|---|---|---|---|
| 감각 충돌 (Reason & Brand 1975 계열) | LaValle 12.3 «Comfort and VR Sickness» <https://lavalle.pl/vr/vrch12.pdf> | 시각이 보고하는 가속과 전정계가 감지하는 가속의 불일치 -> 증상 | 증상 발생 시점·개인차 예측력 부족 |
| 자세 불안정 (Riccio & Stoffregen 1991) | Ecological Psychology 3(3) <https://www.semanticscholar.org/paper/An-ecological-Theory-of-Motion-Sickness-and-Riccio-Stoffregen/f692ee14557eda16583dbd5d9e18ca13f0d3ed55> | 머리·몸 자세 제어의 불안정이 선행 원인 | 예측 검증 일부 성공, 전면 대체는 미달 |
| 자세 불안정 경험 검증 (Smart, Stoffregen & Bardy 2002) | Human Factors 44(3) <https://journals.sagepub.com/doi/10.1518/0018720024497745> | 멀미 발생자에서 증상 이전에 자세 흔들림의 변동성·속도·범위 증가 | 표본 한정 · 상관 설계 |

- **«확실하지 않음»** : 두 이론의 우열은 논쟁 중 · 교재에 «하나가 정설» 로 제시 금지

### 2-2. SSQ (Kennedy et al. 1993) 구성과 해석 한계

- 지면 : International Journal of Aviation Psychology 3(3):203–220
- 구성 : 증상 16개 · 각 0~3 (none·slight·moderate·severe) · 하위척도 3개
  - Nausea (N) : 위 불편감 · 침 분비 증가 · 구역
  - Oculomotor (O) : 눈 피로 · 두통 · 시야 흐림
  - Disorientation (D) : 어지러움 · 현훈 · 초점 조절 곤란
- 총점 산출 : 하위척도별 가중치 적용 후 합산
- 출처 : <https://www.semanticscholar.org/paper/Simulator-Sickness-Questionnaire:-An-enhanced-for-Kennedy-Lane/0543a8a6e1d57deead06199b5876e6ea21defacb>
- 한계
  - 비행 시뮬레이터 모집단에서 개발 -> HMD 모집단 규준 미확립
  - 표준화·공식 번역 부재 (Balk et al., SSQ Twenty Years Later) <https://www.researchgate.net/publication/321841849_Simulator_Sickness_Questionnaire_Twenty_Years_Later>
  - 사전 측정 시행 시 증상 암시 효과 가능 -> 사전·사후 설계의 교란
- **«확실하지 않음»** : SSQ 총점의 «위험 구간» 절단점은 합의 미달

### 2-3. 유발 요인별 수치

| 요인 | 수치 | 연구 | 출처 |
|---|---|---|---|
| 정속 병진 속도 임계값 | 전방 1.183 m/s (SD 0.836) · 측방 0.890 m/s (SD 0.594) | Terenzi & Zaal (SJSU·NASA Ames, AIAA SciTech 2020) · 참가자 18명 · 중위 연령 24세 | <https://ntrs.nasa.gov/citations/20200000787> |
| 정속 회전 속도 임계값 | 롤 0.364 rad/s ≈ 20.9°/s (SD 0.201) · 요 0.473 rad/s ≈ 27.1°/s (SD 0.381) | 같은 연구 | 같은 출처 |
| 가속 임계값 | 전방 0.700 m/s² · 측방 0.586 m/s² · 롤 0.474 rad/s² · 요 0.478 rad/s² | 같은 연구 | 같은 출처 |
| 회전 vs 병진 | 회전 임계값이 유의하게 낮음 : b=0.310 (SE 0.055), t(37.9)=5.653, p<0.001 | 같은 연구 | 같은 출처 |
| 콘텐츠 종류별 SSQ 총점 | 게임 34.26 (29.57–38.95) · 360 영상 27.42 (20.69–34.15) · 미니멀 21.71 (12.36–31.06) · 경관 17.33 (10.79–23.87) · 전체 28.00 (24.66–31.35) | Saredakis et al. (2020) Frontiers in Human Neuroscience 14:96 · 논문 55편 · 참가자 3,016명 · 여성 41% | <https://www.frontiersin.org/articles/10.3389/fnhum.2020.00096/full> |
| 이동 방식별 SSQ 총점 | 컨트롤러 32.55 (28.28–36.81) · 정지 28.04 (21.34–34.73) · 실보행 16.99 (10.67–23.32) | 같은 메타분석 | 같은 출처 |
| 노출 시간별 SSQ 총점 | 10분 미만 23.47 · 10분 이상 33.42 · 20분 이상 27.35 | 같은 메타분석 | 같은 출처 |
| 지연 변동 | 기저 지연 약 70 ms 에 0.2 Hz · 진폭 100 ms 변동 추가 -> SSQ·MSAQ 상승 | St. Pierre et al. (2015) Applied Ergonomics | <https://www.sciencedirect.com/science/article/abs/pii/S0141938214000791> |
| 절대 지연 | 5·46·87·128·169·212 ms 조건에서 지연 증가에 따라 FMS 상승 (Kim et al. 2020) | Stauffert·Niebling·Latoschik 리뷰 경유 | <https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2020.582204/full> |
| 주변시 광학 흐름 제한 | 전체 효과 −0.40 [−0.62, −0.18] · 연구 97편 | Visual Factors in Cybersickness 메타분석 (Multisensory Research, 온라인 선공개) | <https://brill.com/view/journals/msr/aop/article-10.1163-22134808-bja10181/article-10.1163-22134808-bja10181.xml> · <https://pubmed.ncbi.nlm.nih.gov/41389808/> |

- 광학 흐름 속도 : 3 m/s -> 10 m/s 구간에서 증상 상승, 10 m/s 초과 구간은 상관 약화 (프레즌스 저하 가능성) · 2차 출처 요약 -> **«확실하지 않음»**

### 2-4. 개인차

| 변수 | 보고 | 출처 |
|---|---|---|
| 연령 (성인 표본) | 평균 35세 이상 표본 SSQ 14.30 (4.58–24.02, 연구 4편) vs 35세 미만 28.44 (25.46–31.42, 연구 50편) | Saredakis et al. 2020 <https://www.frontiersin.org/articles/10.3389/fnhum.2020.00096/full> |
| 연령 (아동) | 12세 미만에서 감수성 최고 · 성인기까지 급감 후 완만 감소 | LaValle 12.3 <https://lavalle.pl/vr/vrch12.pdf> |
| 성별 | Saredakis 메타분석에서 여성 비율과 SSQ 상관 없음 · 다른 문헌은 여성 고감수성 주장 -> 결론 미합의 | 같은 두 출처 |
| 사전 경험 | 반복 노출 4일 설계에서 적응 발생 | Cybersickness Abatement from Repeated Exposure (2024) <https://pubmed.ncbi.nlm.nih.gov/39418159/> |
| 최선의 예측 변수 | 과거 멀미 경험 유무 | LaValle 12.3 <https://lavalle.pl/vr/vrch12.pdf> |
| 중도 포기율 | 평균 15.6% (최소 0% · 최대 100%) · 실증 연구 44편 집계 | Souchet et al. (2023) Virtual Reality <https://link.springer.com/article/10.1007/s10055-022-00672-0> |
| 발생률 | 현세대 HMD 사용자 최소 1/3 경험 · 그중 5% 중증 | 같은 리뷰 <https://link.springer.com/article/10.1007/s10055-022-00672-0> |
| 광시야 자극 실험실 기준 (optokinetic drum) | 어지러움 50~100% · 위 증상 20~60% | LaValle 12.3 <https://lavalle.pl/vr/vrch12.pdf> |
| 후유 증상 | 증상 경험자 대부분 30분 후에도 약화된 증상 잔존 · 소수 극단 사례는 수시간~수일 | LaValle 12.3 <https://lavalle.pl/vr/vrch12.pdf> |

- **«확실하지 않음»** : 성별 차이 · 10 m/s 이상 구간 포화 · 반복 노출 적응의 지속 기간

### 2-5. 완화 기법 효과 크기

| 기법 | 효과 | 연구 설계 | 출처 |
|---|---|---|---|
| 주변시 FOV 제한 (일괄) | −0.40 [−0.62, −0.18] | 메타분석 97편 | <https://pubmed.ncbi.nlm.nih.gov/41389808/> |
| 동적 FOV 제한 (베그넷팅) | 멀미 유의 감소 · 프레즌스 저하 없음 · 참가자 다수가 개입 사실 미인지 | Fernandes & Feiner, IEEE 3DUI 2016, pp.201–210 · 참가자 30명 · 다일 2회기 · Best Paper | <https://www.semanticscholar.org/paper/Combating-VR-sickness-through-subtle-dynamic-Fernandes-Feiner/c2378b9809763e862533c1edd2771b1b68fde5ad> |
| 시점 스냅 (스냅턴) | 회전 임계 25°/s · 점프 22.5° 조건에서 SSQ 회전 −40% · 병진 −50% · 프레즌스·오류율·성능 변화 없음 | Farmani & Teather, Graphics Interface 2018 | <https://www.csit.carleton.ca/~rteather/pdfs/GI_2018_viewpoint_snapping.pdf> |
| 텔레포트 | 컨트롤러 연속 이동 대비 구역·안구운동 하위척도 낮음 · 경로 적분·탐색 속도는 저하 | 미로 탐색 비교 연구 (Scientific Reports 2025) | <https://www.nature.com/articles/s41598-025-12143-y> |
| 실보행 | SSQ 16.99 (10.67–23.32) · 컨트롤러 32.55 대비 최저 | Saredakis et al. 2020 | <https://www.frontiersin.org/articles/10.3389/fnhum.2020.00096/full> |
| 고정 기준점 · 코 모형 (nasum virtualis) | 토스카나 빌라 씬 +94.2초 · 롤러코스터 씬 +2.2초 연장 · 참가자 미인지 | Whittinghill et al. (Purdue, GDC 2015 발표) | <https://www.purdue.edu/newsroom/archive/releases/2015/Q1/virtual-nose-may-reduce-simulator-sickness-in-video-games.html> |
| 베그넷팅 + 증폭 회전 조합 | 베그넷팅 적용 조건에서 오히려 멀미 증가 보고 | Assessing vignetting as a means to reduce VR sickness during amplified head rotations (2018) | <https://www.researchgate.net/publication/326760789_Assessing_vignetting_as_a_means_to_reduce_VR_sickness_during_amplified_head_rotations> |

- **«확실하지 않음»** — 코 모형 : 학술 발표 자료 · 동료심사 지면 미확인 · 두 씬 간 효과 차이가 94.2초 대 2.2초로 극단 -> 일반화 금지
- **«확실하지 않음»** — 베그넷팅 : 적용 맥락(증폭 회전 여부)에 따라 효과 방향 역전 보고 공존

### 수업 적용

- 7주 애니메이션·물리 : 고정 타임스텝·보간과 전정-시각 충돌을 같은 슬라이드에서 연결 (LaValle 8.1~8.4)
- 11주 VR 기초 : 멀미 대응 프로토콜 고지 슬라이드에 Souchet 15.6% 중도 포기율 · Saredakis 콘텐츠별 SSQ 표 삽입
- 12주 VR 인터랙션 심화 : 스냅턴 25°/s·22.5° 를 과제 기본값으로 지정 + Farmani & Teather −40/−50% 수치 제시
- 14주 플레이테스트 : 실습 전후 SSQ 측정 · 해석 한계 1장 병기 · 20분 이상 노출 금지 규칙 근거 제시

---

## 3. 벡션 (vection) 과 광학 흐름

### 핵심 결론

- 벡션 : 실제 이동 없이 시각 자극만으로 발생하는 자기 운동 지각 -> 시각 유발 멀미의 선행 조건
- 잠복 시간 (onset latency) 수초 단위 · HMD 가 외부 디스플레이보다 짧음
- 주변시 우위설은 수정 중 : 망막 면적·지각 거리 통제 시 중심시도 유효

### 근거 연구

| 항목 | 수치 | 연구 | 출처 |
|---|---|---|---|
| 벡션 잠복 시간 | 8초 노출 조건 평균 약 4초 · 8~64초 노출 범위에서 잠복 시간 일정 | Seno et al. (2018) i-Perception | <https://pmc.ncbi.nlm.nih.gov/articles/PMC6055108/> |
| 디스플레이별 잠복 시간 | HMD 평균 4.4초 < 외부 디스플레이 평균 6.2초 | Palmisano et al. (2018) PLOS ONE | <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0195886> |
| 진동 프라이밍 효과 | 통제 조건 8~9초 -> 조합 조건 외부 디스플레이 4.6초 · HMD 1.7초 | 같은 연구 | 같은 출처 |
| 자극 FOV | HMD 대각 100° 자극 가능 -> 외부 디스플레이보다 넓은 광학 흐름 제공 | 같은 연구 | 같은 출처 |
| 최소 자극 면적 | 동기화된 운동 자극 패치 한 쌍 · 총 시야 10 제곱도 수준에서도 벡션 유발 | Vection induced by a pair of patches… (2023) | <https://pmc.ncbi.nlm.nih.gov/articles/PMC10521291/> |
| 주변시 우위 재검토 | 망막 면적·지각 거리 통제 시 모든 망막 영역이 동등하게 유효할 가능성 | 원거리 주변시 광학 흐름 연구 (Journal of Vision) | <https://jov.arvojournals.org/article.aspx?articleid=2642896> |
| 전정 자극 결합 | 시각 자극 방향과 일치하는 짧은 신체 운동 -> 잠복 시간 단축 · 상충 자극 -> 지연 | Palmisano et al. (2018) | <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0195886> |

- 교재 매핑 : LaValle 6.2 «Perception of Motion» · 8.4 «Mismatched Motion and Vection» <https://lavalle.pl/vr/vrch6.pdf> · <https://lavalle.pl/vr/vrch8.pdf>
- **«확실하지 않음»** : 방사형 흐름이 층류형(lamellar) 흐름보다 자기 운동 유발에 유효하다는 비교는 2차 요약으로만 확보 -> 1차 출처 **«확인 필요»**

### 수업 적용

- 7주 : 광학 흐름 데모 (입자장 전방 이동) 를 Unity 로 만들어 잠복 시간 4초 체감 -> 멀미 유발 조건 이해
- 11주 : 시점 이동 설계 시 «주변시 광학 흐름 양» 을 조절 변수로 명시
- 12주 : 공간 UI 와 벡션 충돌 (화면 고정 요소 금지) 을 LaValle 12.2 권고와 연결

---

## 4. 지연 (latency)

### 핵심 결론

- motion-to-photon 지연 지각 임계값은 단일 값이 아님 : 머리 회전 가속에 반비례
- 훈련된 관찰자의 변별 임계값 최저 3.2 ms 보고 -> «20 ms 이하면 무조건 비지각» 주장 부정확
- 예측 (prediction) 은 지연 보상에 필수 · 과예측 시 오버슈트·흔들림 부작용

### 근거 연구

| 항목 | 수치 | 연구 | 출처 |
|---|---|---|---|
| 평균 75% 지연 임계값 | 55.6 ms (SD 23.4) · 범위 19.2~154.1 ms | Jerald (2009) UNC 박사학위논문 / TR 10-013 · 실험 4 · 참가자 8명 모집 중 6명 분석 · 가속 분위 6구간 | <https://www.cs.unc.edu/techreports/10-013.pdf> |
| 평균 50% 지연 임계값 | 38.7 ms (SD 18.4) · 범위 −0.2~103.2 ms | 같은 연구 | 같은 출처 |
| 평균 변별 임계값 (JND) | 16.9 ms (SD 10.4) · 범위 3.2~60.5 ms | 같은 연구 | 같은 출처 |
| 최소 변별 임계값 | 3.2 ms -> 종단 지연 3 ms 수준이면 비지각 수준으로 판단 | 같은 연구 | 같은 출처 |
| 지연 임계값 모형 | 머리 요(yaw) 최대 가속의 역함수 · 선형 모형보다 적합 | 같은 연구 · Jerald & Whitton (2012) ACM TAP | <https://www.cs.unc.edu/techreports/10-013.pdf> · <https://dl.acm.org/doi/10.1145/2134203.2134207> |
| 머리 운동 속도별 허용 한계 | 인체 최대 속도 회전 시 약 23 ms · 20°/s 조건 최대 약 41 ms | Perceptual Tolerance to Motion-To-Photon Latency with Head Movement in VR (IEEE) | <https://ieeexplore.ieee.org/document/8954518/> |
| 지연 증가와 멀미 | 5~212 ms 범위에서 지연 증가 -> FMS 상승 (Kim et al. 2020) | Stauffert et al. 리뷰 | <https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2020.582204/full> |
| 지연 변동의 영향 | 기저 약 70 ms + 0.2 Hz · 진폭 100 ms 변동 -> SSQ 상승 (0 Hz 조건 대비) | St. Pierre et al. (2015) Applied Ergonomics | <https://www.sciencedirect.com/science/article/abs/pii/S0141938214000791> |
| 역치 미달 흔들림 | 지각 임계값 아래 jitter 도 시각 불편감 유발 가능 | Subthreshold Jitter in VR Can Induce Visual Discomfort (ACM 2025) | <https://dl.acm.org/doi/10.1145/3746059.3747607> |
| 보상 기법 | forward prediction · asynchronous time warp · view reprojection 가 표준 대응 | 저지연 HMD 지각 요구 조건 리뷰 | <https://arxiv.org/pdf/2603.15796> |

### 예측의 부작용

- 과예측 (overprediction) : 지연 구간을 넘어 예측 -> 오버슈트 (실제보다 큰 이동 또는 조기 정지) · 실제 머리 움직임과 괴리
- 스무딩 과다 : 센서 잡음·드리프트 억제 목적이나 응답 둔화 유발
- 출처 : 예측 추적 특허 명세 <https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9348410>
- **«확실하지 않음»** : 과예측 부작용의 정량 효과 크기 (오버슈트 각도·불편감 증가량) 를 동료심사 지면에서 확보하지 못함 -> **«확인 필요»**
- 참고 기준 : Valve Steam Frame Verified 라벨이 90 fps 요구 (2차 출처) <https://vr.org/articles/steam-frame-verified-90fps-stricter-than-quest-pico> · 1차 문서 <https://partner.steamgames.com/doc/steamhardware/steamframe/vrpreferences> -> **«확인 필요»** (1차 문서 내 90 fps 명시 여부)

### 수업 적용

- 11주 motion-to-photon 예산 분해 슬라이드 : 센서 -> 융합 -> 렌더 -> 스캔아웃 각 구간에 ms 배정 · Jerald 3.2 ms / 16.9 ms / 55.6 ms 세 수치를 «최소 변별 · 평균 JND · 평균 75% 임계» 로 구분 제시
- 11주 : «20 ms 규칙» 을 업계 관행으로 소개하되 Jerald 수치로 단서 병기
- 14주 성능 프로파일링 : 프레임 변동(variance) 자체가 증상 요인임을 St. Pierre 0.2 Hz 결과로 근거 제시

---

## 5. 깊이 지각

### 핵심 결론

- 단안 단서가 양안 단서보다 수적으로 많음 · 거리대별 유효 단서 서열 변화
- HMD 거리 과소추정 : 모델 거리의 평균 74% (1993~2012 집계)
- 조절-수렴 충돌 (VAC) 이 시각 피로의 주요 요인 · 실용 권고 대략 ±0.5 D 이내

### 5-1. 단서별 기여

| 구분 | 내용 | 출처 |
|---|---|---|
| 거리 3구간 | personal space (약 2 m 이내) · action space (약 2~30 m) · vista space (약 30 m 이상) | Cutting & Vishton (1995) <http://wexler.free.fr/library/files/cutting%20(0)%20perceiving%20layout%20and%20knowing%20distances.pdf> |
| 근거리 단서 서열 | 차폐 (occlusion) > 양안 부등 > 운동 시차 > 상대 크기 > 조절·수렴 > 상대 밀도 | 같은 출처 |
| 정확도 | 2 m 이내는 거의 미터 정확 · 30 m 초과는 뚜렷한 압축 | 같은 출처 |
| 단안·양안 분류 | 단안 단서 종류가 양안보다 많음 -> 사진 한 장에서 깊이 추론 가능 | LaValle 6.1 <https://lavalle.pl/vr/vrch6.pdf> |

### 5-2. VR 거리 과소추정 (distance compression)

| 항목 | 수치 | 연구 | 출처 |
|---|---|---|---|
| 평균 추정 비율 | 모델 거리의 74% (과소추정 약 26%) | Renner, Velichkovsky & Helmert (2013) Psychological Bulletin · 논문 78편 (1993~2012) | <https://tu-dresden.de/mn/psychologie/applied-cognition/ressourcen/dateien/personal/Renner_Perception_virtual_distances_Review.pdf> |
| 최근 기기 범위 | 평균 74~82% 보고 | 현대 HMD 거리 지각 검토 | <https://psych.utah.edu/_resources/documents/people/committee-docs/spring-2023/creemregehr-2022-perceiving-distance-in-virtual-reality.pdf> |
| 측정 방법 의존성 | 측정법·이동 방식·translation gain 에 따라 추정값 변동 | Measuring egocentric distance perception in VR (PLOS ONE) | <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0224651> |
| 보정 가능성 | 피드백·연습으로 보정 가능 | 상기 검토 문헌 | <https://www.tandfonline.com/doi/pdf/10.1080/10447318.2023.2234117> |

- **«확실하지 않음»** : 최신 HMD 에서 압축 크기가 감소했는지 여부 · 측정 방법 간 불일치가 커 단일 수치 제시 부적절

### 5-3. 조절-수렴 충돌 (VAC) 과 시각 피로

| 항목 | 내용 | 연구 | 출처 |
|---|---|---|---|
| 기본 기제 | 디스플레이에서 초점 단서(조절·망막 흐림)는 화면 깊이를 지시 · 수렴은 묘사된 장면 깊이를 지시 -> 충돌 | Hoffman, Girshick, Akeley & Banks (2008) Journal of Vision | <https://jov.arvojournals.org/article.aspx?articleid=2122611> |
| 결과 | 시각 성능 저하 · 시각 피로 유발 | 같은 연구 | 같은 출처 |
| 편안 영역 (zone of comfort) | 동일 디옵터 충돌이 근거리보다 원거리에서 덜 편안 · 음(negative) 충돌은 원거리에서, 양(positive) 충돌은 근거리에서 상대적 유리 | Shibata, Kim, Hoffman & Banks (2011) Journal of Vision 11(8) | <https://jov.arvojournals.org/article.aspx?articleid=2121032> |
| 기존 모형 평가 | Percival · Sheard 기준은 스테레오 3D 에 과관대 -> 더 엄격한 모형 제안 | 같은 연구 | 같은 출처 |
| 실무 권고 | 조절-수렴 불일치 약 ±0.5 D 이내 유지 권고 (Shibata 2011 참조 후속 문헌) | 2차 출처 | <https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/ei/35/2/SDA-390> |
| 변화 속도 | 충돌의 변화율(rate of change) 도 불편감에 영향 | Vision Research (2014) | <https://www.sciencedirect.com/science/article/pii/S0042698914002545> |
| 제조사 배치 권고 | 메뉴 항목 0.75~3.5 m · 중요 콘텐츠 0.5~10 m · 스테레오 깊이 지각 한계 약 20 m | Oculus Best Practices Guide v0.008 (2014) | <https://s3.amazonaws.com/arena-attachments/238441/2330603062c2e502c5c2ca40443c2fa4.pdf> |

- **«확인 필요»** : ±0.5 D 권고가 Shibata et al. 2011 원문에 명시된 값인지 · 후속 문헌의 해석값인지 1차 확인 미완

### 수업 적용

- 5주 조명·재질 : 차폐·텍스처 기울기·상대 크기가 단안 깊이 단서임을 라이팅 결과물과 함께 제시 (LaValle 6.1)
- 6주 셰이더 : 노멀맵이 제공하는 단서는 음영 기반 단안 단서 · 시차 단서 부재 -> 가까이서 평면성 노출
- 12주 공간 UI : 패널 배치 거리 결정 근거로 VAC 편안 영역 + Oculus 0.75~3.5 m 제시
- 13주 기획 : 씬 스케일 검수 항목에 «거리 과소추정 74%» 를 넣어 실측 대비 과대 제작 유도

---

## 6. 시각 해상도·주변시

### 핵심 결론

- 전통 기준 : 20/20 시력 = 30 cycles/degree = 60 PPD
- 최근 측정 : 집단 평균 94 PPD (무채색) · 개인 최대 120 PPD -> 60 PPD 는 하한
- 포비티드 렌더링 : 주변시 셰이딩 축소로 5~6배 가속 보고 · 지각 허용 범위는 편심각 기준으로 정의

### 근거 연구

| 항목 | 수치 | 연구 | 출처 |
|---|---|---|---|
| 20/20 기준 | 30 cycles/degree -> 최소 60 pixels/degree | LaValle 5.4 | <https://lavalle.pl/vr/vrch5.pdf> |
| 시력 한계 | 약 60~77 cycles/degree (망막 직접 자극 조건) · 약 1%가 60 cycles/degree 수준 | LaValle 5.4 | 같은 출처 |
| VR 패널 요구 PPI | 초점거리 1.5인치 가정 시 60 cycles/degree 달성에 약 2,291.6 PPI 필요 · 60 cycles/degree 극단 조건은 4,583 PPI | LaValle 5.4 | 같은 출처 |
| 스마트폰 비교 | 326 PPI 로 12인치 거리 «retina» 조건 충족 · 당시 최고 밀도 패널 801 PPI -> VR 요구의 약 1/3 | LaValle 5.4 | 같은 출처 |
| 최근 지각 한계 측정 | 집단 평균 94 PPD (무채색) · 89 PPD (색) · 개인 최대 120 PPD | Resolution limit of the eye (2025) | <https://pmc.ncbi.nlm.nih.gov/articles/PMC12559231/> |
| 광수용체 밀도 | 중심와 최고 · 편심각 증가에 따라 급감 (LaValle Figure 5.5) | LaValle 5.1~5.2 | <https://lavalle.pl/vr/vrch5.pdf> |
| 포비티드 렌더링 가속 | 1920×1080 데스크톱에서 5~6배 가속 · 셰이딩 픽셀 수 10~15배 감소 | Guenter, Finch, Drucker, Tan, Snyder (2012) ACM TOG | <https://www.microsoft.com/en-us/research/wp-content/uploads/2012/11/foveated_final15.pdf> |
| 허용 편심각 개선 | Guenter 2012 대비 중심와 쪽으로 최대 30° 더 가깝게 셰이딩 축소 가능 · 지각 가능한 에일리어싱·블러 없음 | Patney et al. (2016) | <https://cwyman.org/papers/siga16_gazeTrackedFoveatedRendering.compressed.pdf> |
| 품질 보정 기법 | 에일리어싱 구간의 주변시 대비 강화 -> 비포비티드 영상과 동등한 지각 품질 | 같은 연구 | 같은 출처 |
| 급강하 모형 | 최소 탐지 각크기가 편심각에 선형 증가 가정 -> 계층 크기·샘플링률 자동 산출 | 같은 연구 | 같은 출처 |

- **«확인 필요»** : 중심와 추세포 밀도의 절대값 (cones/mm²) · 1차 해부 문헌 미확보
- **«확실하지 않음»** : 94 PPD 측정은 단일 최근 연구 · 60 PPD 관행과의 차이는 측정 패러다임 차이 가능

### 수업 적용

- 6주 셰이더 : 텍스처 해상도·밉맵 논의에 «60 PPD vs 94 PPD» 로 «화면에서 더 쓸 수 있는 디테일» 판단 근거 제공
- 11주 : Quest 3 패널 PPD 를 LaValle 2,291.6 PPI 계산과 대조 -> 왜 텍스트가 흐릿한지 설명
- 12주 VR 최적화 : 포비티드 렌더링 가속 5~6배 · 셰이딩 픽셀 10~15배 감소 수치로 최적화 우선순위 제시

---

## 7. 신체 소유감·아바타

### 핵심 결론

- 고무손 착각 : 시각-촉각 동기 자극으로 비자기 신체에 소유감 전이
- 가상 신체로 확장 성립 · 1인칭 시점 + 거울 반사 조건에서 효과 보고
- 프로테우스 효과 : 아바타 외형이 행동 변화 유발 · 메타분석 효과 크기 r = .22~.26 (소~중)
- 측정 타당도 논쟁 : 고유감각 이동(proprioceptive drift) 과 주관 소유감의 해리 · 요구 특성 교란

### 근거 연구

| 연구 | 지면 | 표본 | 핵심 내용 | 출처 |
|---|---|---|---|---|
| Botvinick & Cohen (1998) | Nature 391(6669):756 | — | 고무손 착각 보고 · 시간·공간 동기 및 해부학적 타당 위치 필요 · 비동기 자극 시 약화·소멸 | <https://www.nature.com/articles/35784> |
| Slater et al. (2009) | Frontiers in Neuroscience | — | 물리적 고무손 없이 가상 팔로 소유감 착각 유도 | <https://pubmed.ncbi.nlm.nih.gov/20011144/> |
| Peck, Seinfeld, Aglioti & Slater (2013) | Consciousness and Cognition 22:779–787 | — | 밝은 피부 참가자가 어두운 피부 가상 신체에 체화 -> IAT 암묵 인종 편향 유의 감소 (밝은 피부·보라 피부·신체 없음 조건 대비) | <https://www.semanticscholar.org/paper/5e0e23f8e56d50b6622e845c99b84ea6cb7e0eb1> |
| Banakou, Hanumanthu & Slater (2016) | Frontiers in Human Neuroscience | — | 체화 효과의 지속적 편향 감소 보고 | <https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2016.00601/full> |
| Yee & Bailenson (2007) | Human Communication Research 33(3) | 2개 실험 | 실험1 : 매력적 아바타 -> 자기 개방·대인 거리에서 더 친밀 · 실험2 : 큰 키 아바타 -> 협상에서 더 공격적, 직후 실제 협상 과제까지 전이 | <https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-2958.2007.00299.x> |
| Ratan, Beyea, Li & Graciano (2020) | Media Psychology 23(5):651–675 | 실험 46편 | 프로테우스 효과 크기 r = .22~.26 (포함 기준별) · 소~중 수준 | <https://www.tandfonline.com/doi/pdf/10.1080/15213269.2019.1623698> |

### 측정 타당도 논쟁

| 쟁점 | 내용 | 출처 |
|---|---|---|
| 고유감각 이동과 소유감 해리 | 손 위치 감각 변화와 소유감 강도 사이 인과 연결 없음 | <https://link.springer.com/article/10.3758/s13414-015-1016-0> · <https://pmc.ncbi.nlm.nih.gov/articles/PMC3125296/> |
| 요구 특성 교란 | 동기·비동기 통제 조건에 대한 참가자 기대가 달라 -> 비동기 통제의 차이가 가설 인지로 교란 | Royal Society Open Science 8(11):210911 (2021) <https://royalsocietypublishing.org/rsos/article/8/11/210911/95790/Hypothesis-awareness-confounds-asynchronous> |
| 재현 연구 | Lush (2020) 순서 효과 재현·확장 | Collabra 10(1) (2024) <https://online.ucpress.edu/collabra/article/10/1/116190/200587/Order-Effects-on-the-Rubber-Hand-Illusion> |
| 반대 증거 | 최근 메타분석은 고유감각 이동 과제와 주관 착각 경험의 정적 상관 보고 | <https://pmc.ncbi.nlm.nih.gov/articles/PMC11652674/> |

- **«확실하지 않음»** : 고무손 착각의 측정 지표 타당도 · 요구 특성 설명이 효과 전체를 대체하는지 여부는 논쟁 중
- **«확실하지 않음»** : Peck 2013 의 편향 감소 효과는 표본 규모·지속 기간 측면에서 추가 재현 필요

### 수업 적용

- 7주 애니메이션 : IK·아바타 모션이 소유감 조건(1인칭 시점·시각-촉각 동기)과 연결됨을 제시 (LaValle 10.3)
- 11주 : 아바타 손 모델 유무를 비교 체험 과제로 설계
- 13주 기획 : 아바타 외형 결정이 행동 변화 유발 가능 -> 프로테우스 효과 r ≈ .22~.26 과 윤리 검토 항목 병기

---

## 8. 공간 UI·인터랙션 지각

### 핵심 결론

- 제조사 가이드라인은 거리·각도·최소 타깃 크기를 수치로 규정 · 근거 논문 미첨부 사례 다수
- 직접 터치 UI : 42~46 cm 권고 · 패널형 UI : 약 1~1.5 m 권고
- 핸드 트래킹은 컨트롤러 대비 완료 시간·정확도 열위 보고 다수 · 과제별 차이 없는 결과도 존재

### 8-1. 배치 거리·각도

| 항목 | 수치 | 출처 종류 | 출처 |
|---|---|---|---|
| 터치 유도 패널 거리 | 42~46 cm | 제조사 가이드 (Meta) | <https://developers.meta.com/horizon/design/hands-ui-best-practices/> |
| 패널형 UI 거리 | 약 1~1.5 m | 같은 가이드 | 같은 출처 |
| 메뉴 항목 거리 | 0.75~3.5 m | Oculus Best Practices v0.008 (2014) | <https://s3.amazonaws.com/arena-attachments/238441/2330603062c2e502c5c2ca40443c2fa4.pdf> |
| 중요 콘텐츠 깊이 | 0.5~10 m · 스테레오 깊이 지각 한계 약 20 m | 같은 문서 | 같은 출처 |
| 최소 각 타깃 크기 | 직접 터치·레이캐스트 공통 약 2.5~3° | Meta 가이드 | <https://developers.meta.com/horizon/design/hands-ui-best-practices/> |
| 본문 텍스트 크기 | 24 DMM · 레이 히트 타깃 64×64 DMM + 패딩 16 DMM | Google Daydream 앱 품질 요건 | <https://developers.google.com/vr/distribute/daydream/design-requirements> |
| 텍스트 배치 원칙 | 양안 수렴 가능 거리 확보 -> 이중상 회피 | Google Fonts «Designing for AR/VR» | <https://fonts.google.com/knowledge/using_type_in_ar_and_vr/designing_for_ar_vr> |
| 접근성 | 머리 회전 범위·자세 부담 고려 항목 제시 | Meta Accessibility | <https://developers.meta.com/vr/design/accessibility/> |
| 이동 편안함 | 가속·회전 설계 권고 | Meta Locomotion comfort and usability | <https://developers.meta.com/horizon/design/locomotion-comfort-usability/> |

- **«확실하지 않음»** : 편안한 시야 범위 «좌우 30° · 최대 회전 55°» 는 2차 출처(블로그 정리) 로만 확보 -> **«확인 필요»** (1차 가이드 원문 조항)

### 8-2. 손 닿는 범위·피로

| 항목 | 내용 | 출처 |
|---|---|---|
| 자세 원칙 | 팔을 몸 가까이 · 팔꿈치를 허리 높이로 유지하도록 설계 · 심장 높이 이상 손 사용은 급격한 피로 유발 | <https://developers.meta.com/horizon/design/hands-ui-best-practices/> |
| 누적 피로 | 지속적 뻗기·집기·팔 들기 -> 어깨·팔 피로 누적 (gorilla arm) | 같은 출처 |
| 레이아웃 | 자주 쓰는 요소를 패널 하단 절반에 배치 -> 팔 뻗기 감소 · 머리 중립 자세 유지 | 같은 출처 |
| 레이캐스트 | 원거리 선택 권고 사항 별도 문서 | <https://developers.meta.com/vr/design/raycasting_bp/> |

### 8-3. 핸드 트래킹 vs 컨트롤러

| 비교 항목 | 결과 | 연구 | 출처 |
|---|---|---|---|
| 완료 시간 | Whack-a-Mole 과제 평균 0.78초 (컨트롤러) vs 1.00초 (핸드 트래킹) | VR 숙련 사용자 대상 비교 연구 | <https://link.springer.com/article/10.1007/s10055-026-01333-2> |
| 과제별 차이 | 일부 미니게임에서 두 방식 간 유의차 없음 | 같은 연구 | 같은 출처 |
| 정확도·오류율 | reach-grab-place 과제에서 컨트롤러가 완료 시간·조작 품질 우위 | 입력 양식 비교 연구 (Journal of Environmental Psychology 2023) | <https://www.sciencedirect.com/science/article/pii/S0272494423001858> |
| 정확도-시간-자연스러움 상충 | 직접 조작에서 정확도·완료 시간·자연스러움 간 trade-off 존재 | MTI 6(1):6 | <https://doi.org/10.3390/mti6010006> |
| 기제 | 물리 버튼·트리거의 이산 입력 vs 연속 동작 인식의 불확실성 | 상기 비교 연구 | <https://link.springer.com/article/10.1007/s10055-026-01333-2> |

- **«확실하지 않음»** : 핸드 트래킹 성능 격차는 기기 세대·과제 유형에 따라 결론 변동 · 최신 비교 연구의 지면·연도 표기는 **«확인 필요»**

### 수업 적용

- 10주 인터랙션 설계 : Overlay · World Space UI 두 벌 제작 과제에 «42~46 cm / 1~1.5 m / 최소 2.5~3°» 를 설계 제약으로 명시
- 12주 VR 인터랙션 심화 : Grab/Ray 구현 후 손 피로 체감 과제 -> 팔꿈치 허리 높이 원칙 검증
- 12주 : 핸드 트래킹 vs 컨트롤러 동일 과제 측정 (완료 시간·오류) -> 0.78초 vs 1.00초 와 자기 데이터 비교

---

## 9. 교육·훈련 효과

### 핵심 결론

- 몰입형 VR 학습 효과 : 전체 g ≈ 0.20~0.38 (소) · K-6 대상 g = 1.06 (대) -> 학령·설계 의존
- 몰입 자체가 학습을 보장하지 않음 : 프레즌스 상승 + 인지 부하 상승 -> 학습 저하 사례
- 외과 술기 훈련은 수술실 성과 지표로 전이 확인 (수술 시간 단축 분 단위)
- 신기성 효과 (novelty effect) : 감소 예측과 상반되는 결과도 보고 -> 단정 금지

### 근거 연구

| 연구 | 지면 | 범위 | 핵심 수치 | 출처 |
|---|---|---|---|---|
| Coban, Bolat & Goksu (2022) | Educational Research Review | 2016~2020.9 논문 집계 | 몰입형 VR 학습 성과 전체 g = 0.38 (소) · K-12 효과 > 고등교육 | <https://www.sciencedirect.com/science/article/abs/pii/S1747938X22000215> |
| Villena-Taranilla et al. (2022) | Educational Research Review | K-6 | 비몰입 방식 대비 g = 1.06 · 짧은 개입에서 효과 큼 | <https://www.sciencedirect.com/science/article/pii/S1747938X22000033> |
| Wu et al. (2020) · Luo et al. (2021) | — | — | g = 0.20~0.38 범위 보고 | <https://www.sciencedirect.com/science/article/pii/S1747938X22000033> |
| Makransky, Terkildsen & Mayer (2019) | Learning and Instruction 60:225–236 · DOI 10.1016/j.learninstruc.2017.12.007 | 과학 실험실 시뮬레이션 | 몰입형 VR 조건에서 프레즌스 상승 · 인지 과부하 상승 · 학습 성과 저하 | <https://www.sciencedirect.com/science/article/abs/pii/S0959475217303274> |
| Huang et al. (2021) | Journal of Computer Assisted Learning 37(3) | 다회기 설계 | 회기 반복에도 동기·참여·성과 전반 하락 없음 -> 신기성 효과 예측과 상반 | <https://onlinelibrary.wiley.com/doi/10.1111/jcal.12520> |
| 신기성 효과 평가 (2024) | Virtual Reality (Springer) | 몰입형 VR 학습 경험 | 신기성 효과 평가 방법·결과 보고 | <https://link.springer.com/article/10.1007/s10055-023-00926-5> |
| 복강경 담낭절제 메타분석 (2022) | BJS Open 6(4):zrac086 | RCT 집계 | 과제 완료 시간 MD −8.35분 (95% CI 13.10~3.60, p<0.001) | <https://academic.oup.com/bjsopen/article/6/4/zrac086/6645553> |
| Cochrane (Nagendran et al. 2013) | Cochrane Database | 3편 · 참가자 49명 | 보조 훈련 없음 대비 수술 시간 MD −11.76분 (95% CI −15.23~−8.30) | <https://pubmed.ncbi.nlm.nih.gov/23980026/> |
| 로봇 수술 VR 시뮬레이터 (2021) | BJS Open 5(2):zraa066 | 4편 중 3편 | 시간·기술 지표에서 수술실 전이 확인 | <https://academic.oup.com/bjsopen/article/5/2/zraa066/6231803> |

- **«확인 필요»** : 몰입 수준별 효과 크기 (몰입 1.11 · 준몰입 0.19 · 비몰입 0.32) 와 개입 길이별 효과 (단기 0.72 · 장기 0.47) 의 1차 출처 미특정
- **«확실하지 않음»** : 외과 메타분석은 이질성 큼 · 환자 결과·비용 개선 여부 미확인 (원문 한계 서술)
- **«확실하지 않음»** : 신기성 효과의 존재·크기는 상반 결과 공존 -> «VR 효과는 신기성 때문» 단정 금지

### 수업 적용

- 13주 기획 : 팀 프로젝트의 «교육용 VR» 기획 시 g = 0.38 vs g = 1.06 대비표로 «대상·개입 길이 설계가 효과를 좌우» 근거 제시
- 14주 : 플레이테스트 설계에 Makransky 결과 반영 -> 재미·프레즌스 지표와 학습·수행 지표를 분리 측정
- 15주 발표 평가 : «몰입 수준 높음» 주장만으로 효과 주장 금지 규칙 명시

---

## 10. 윤리·안전

### 핵심 결론

- 연구 윤리 : VR 특수성(장기 몰입·행동 변화 전이) 반영한 전용 행동 지침 존재
- 아동 : 제조사 연령 정책 + 휴식 간격 권고 명문화
- 실험 참여 : 사전 동의 · 중도 포기 보장 · 반복 증상 측정이 관례

### 10-1. 연구 윤리 지침

| 항목 | 내용 | 출처 |
|---|---|---|
| 전용 행동 지침 | Madary & Metzinger (2016) Frontiers in Robotics and AI 3:3 · 연구 윤리 6주제 (실험 환경의 한계 · 사전 동의 · 임상 위험 · 이중 용도 · 온라인 연구 · 지침 자체의 한계) + 일반 사용자 위험 4주제 (장기 몰입 · 사회·물리 환경 방치 · 위험 콘텐츠 · 프라이버시) | <https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00003/full> |
| 핵심 금지 | 비자발적 고통 또는 심각·지속 피해가 예견되는 실험 금지 · 치료·임상 응용은 의료 인력 입회 조건 | 같은 출처 |
| 측정 관례 | 증상 반복 측정 : 사전 · 10분 · 30분 · 종료 직후 · 종료 60분 후 | LaValle 12.4 <https://lavalle.pl/vr/vrch12.pdf> |
| 실험자 요구 특성 | 참가자가 실험자를 만족시키려는 경향 -> 설계·보고에 반영 필요 | <https://lavalle.pl/vr/vrch12.pdf> |
| 중도 포기 | VR 부작용으로 인한 중도 포기 평균 15.6% -> 동의서에 즉시 중단 권리 명기 필요 | <https://link.springer.com/article/10.1007/s10055-022-00672-0> |

### 10-2. 아동·장시간 착용

| 항목 | 내용 | 출처 |
|---|---|---|
| 연령 정책 | 13세 이상 Meta 계정 사용 · 10~12세는 보호자 관리 계정 (Quest 2·3) · 10세 미만 사용 불가 | <https://www.meta.com/quest/parent-info/> · <https://familycenter.meta.com/our-products/horizon-and-quest/> |
| 휴식 간격 | 초기 사용 시 30분마다 휴식 · 불편감 발생 시 즉시 중단 · 어린 사용자는 더 자주·더 길게 휴식 | <https://www.meta.com/quest/safety-center/> |
| 일일 시간 제한 | 보호자 설정 가능 · 기본값 2시간 | <https://familycenter.meta.com/our-products/horizon-and-quest/> |
| 신체 위험 | 근육·눈 피로 · 아동의 눈·목·등 발달 미완 · 헤드셋 착용 적합성 미달 가능 | <https://www.meta.com/legal/quest/health-and-safety-warnings/quest-3/> |
| 중단 신호 | 시야 흐림 · 목 자주 만짐 · 자세·동작 변화 · 통증·두통·구역 호소 | <https://www.meta.com/quest/parent-info/> |
| 정책 검토 | 아동·청소년 VR 위험 정리 (시민단체) | <https://pirg.org/edfund/resources/vr-risks-for-kids/> |
| 정부 보고서 | 가정용 VR 시스템 안전성 검토 (영국, 2020) | <https://assets.publishing.service.gov.uk/media/5f763502d3bf7f7c2bcf9eb9/safety-domestic-vr-systems.pdf> |
| 후유 증상 | 증상 경험자 대부분 30분 후 약화 잔존 · 소수는 수시간~수일 | LaValle 12.3 <https://lavalle.pl/vr/vrch12.pdf> |

- **«확인 필요»** : 대학 수업 상황에 적용할 공식 권고 (연속 착용 최대 시간) 의 학술 근거 · 제조사 문서 외 1차 자료 미확보

### 수업 적용

- 11주 현장 운영 : 30분 휴식 간격 · 즉시 중단 권리 · 위생 커버 규칙을 1장 고지 슬라이드로 제시 (출처 병기)
- 11·12주 : 체험 전 간단 동의 절차 (목적 · 증상 가능성 · 중단 자유 · 대체 과제 보장) 운영
- 14주 : 플레이테스트 시 SSQ 측정 시점을 LaValle 12.4 권고(사전·10분·30분·직후)로 설계
- 13주 기획 : 아바타·체화 소재 사용 시 Madary & Metzinger 지침 항목을 기획서 체크리스트로 사용

---

## 11. 수업 연결 표 (주차 × 활용 연구 × 슬라이드 수치)

| 주차 | 주차 주제 | 활용 연구 | 슬라이드에 넣을 수치 | 출처 |
|---|---|---|---|---|
| 5주 | 조명과 재질 : 라이팅 모델·PBR·라이트매핑 | Cutting & Vishton (1995) | 거리 3구간 : 2 m 이내 / 2~30 m / 30 m 이상 · 근거리 단서 서열 (차폐 > 양안 부등 > 운동 시차 > 상대 크기) | <http://wexler.free.fr/library/files/cutting%20(0)%20perceiving%20layout%20and%20knowing%20distances.pdf> |
| 5주 | 같음 | LaValle 6.1 | 단안 단서 종류가 양안보다 다수 -> 사진 한 장에서 깊이 추론 | <https://lavalle.pl/vr/vrch6.pdf> |
| 6주 | 셰이더 기초 : Shader Graph·텍스처·UV | LaValle 5.4 | 60 PPD (= 30 cycles/degree) · VR 요구 약 2,291.6 PPI · 당시 최고 패널 801 PPI | <https://lavalle.pl/vr/vrch5.pdf> |
| 6주 | 같음 | Resolution limit of the eye (2025) | 집단 평균 94 PPD (무채색) · 89 PPD (색) · 개인 최대 120 PPD | <https://pmc.ncbi.nlm.nih.gov/articles/PMC12559231/> |
| 7주 | 애니메이션·물리 엔진 기초 | Terenzi & Zaal (2020) | 요 회전 임계 0.473 rad/s ≈ 27.1°/s · 롤 0.364 rad/s ≈ 20.9°/s · 전방 병진 1.183 m/s | <https://ntrs.nasa.gov/citations/20200000787> |
| 7주 | 같음 | Seno et al. (2018) · Palmisano et al. (2018) | 벡션 잠복 시간 평균 약 4초 · HMD 4.4초 < 외부 디스플레이 6.2초 | <https://pmc.ncbi.nlm.nih.gov/articles/PMC6055108/> · <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0195886> |
| 7주 | 같음 | Riccio & Stoffregen (1991) · Smart et al. (2002) | 이론 2종 대립 구조 · 증상 이전 자세 흔들림 증가 | <https://www.semanticscholar.org/paper/An-ecological-Theory-of-Motion-Sickness-and-Riccio-Stoffregen/f692ee14557eda16583dbd5d9e18ca13f0d3ed55> · <https://journals.sagepub.com/doi/10.1518/0018720024497745> |
| 10주 | 인터랙션 설계 : 입력·UI/UX·이벤트 | Meta Hands UI best practices | 터치 패널 42~46 cm · 패널 UI 1~1.5 m · 최소 각 타깃 2.5~3° | <https://developers.meta.com/horizon/design/hands-ui-best-practices/> |
| 10주 | 같음 | Google Daydream 품질 요건 | 본문 24 DMM · 레이 타깃 64×64 DMM + 패딩 16 DMM | <https://developers.google.com/vr/distribute/daydream/design-requirements> |
| 11주 | VR 개발 기초 : XR 세팅·HMD 입력·텔레포트 | Jerald (2009) | 최소 변별 3.2 ms · 평균 JND 16.9 ms (SD 10.4) · 평균 75% 임계 55.6 ms (SD 23.4) | <https://www.cs.unc.edu/techreports/10-013.pdf> |
| 11주 | 같음 | Saredakis et al. (2020) | 전체 SSQ 28.00 (24.66–31.35) · 게임 34.26 · 360 영상 27.42 · 실보행 16.99 · 컨트롤러 32.55 | <https://www.frontiersin.org/articles/10.3389/fnhum.2020.00096/full> |
| 11주 | 같음 | Souchet et al. (2023) | 사용자 최소 1/3 증상 · 5% 중증 · 중도 포기 평균 15.6% | <https://link.springer.com/article/10.1007/s10055-022-00672-0> |
| 11주 | 같음 | Meta 안전 문서 | 30분 휴식 간격 · 13세 이상 · 10~12세 보호자 관리 · 기본 일일 2시간 | <https://www.meta.com/quest/safety-center/> |
| 11주 | 같음 | Renner et al. (2013) | HMD 거리 추정 평균 모델 거리의 74% | <https://tu-dresden.de/mn/psychologie/applied-cognition/ressourcen/dateien/personal/Renner_Perception_virtual_distances_Review.pdf> |
| 12주 | VR 인터랙션 심화 : Grab/Ray·공간 UI·최적화 | Farmani & Teather (2018) | 스냅턴 25°/s · 22.5° -> SSQ 회전 −40% · 병진 −50% | <https://www.csit.carleton.ca/~rteather/pdfs/GI_2018_viewpoint_snapping.pdf> |
| 12주 | 같음 | Fernandes & Feiner (2016) | 참가자 30명 · 동적 FOV 제한으로 멀미 감소 · 프레즌스 저하 없음 | <https://www.semanticscholar.org/paper/Combating-VR-sickness-through-subtle-dynamic-Fernandes-Feiner/c2378b9809763e862533c1edd2771b1b68fde5ad> |
| 12주 | 같음 | 메타분석 (97편) | 주변시 광학 흐름 제한 효과 −0.40 [−0.62, −0.18] | <https://pubmed.ncbi.nlm.nih.gov/41389808/> |
| 12주 | 같음 | Guenter et al. (2012) · Patney et al. (2016) | 5~6배 가속 · 셰이딩 픽셀 10~15배 감소 · 중심와 쪽 30° 추가 허용 | <https://www.microsoft.com/en-us/research/wp-content/uploads/2012/11/foveated_final15.pdf> · <https://cwyman.org/papers/siga16_gazeTrackedFoveatedRendering.compressed.pdf> |
| 12주 | 같음 | Shibata et al. (2011) · Oculus BP | VAC 편안 영역 모형 · 메뉴 0.75~3.5 m · 중요 콘텐츠 0.5~10 m | <https://jov.arvojournals.org/article.aspx?articleid=2121032> · <https://s3.amazonaws.com/arena-attachments/238441/2330603062c2e502c5c2ca40443c2fa4.pdf> |
| 13주 | 팀 프로젝트 기획 | Coban et al. (2022) · Villena-Taranilla et al. (2022) | 전체 g = 0.38 · K-6 g = 1.06 | <https://www.sciencedirect.com/science/article/abs/pii/S1747938X22000215> · <https://www.sciencedirect.com/science/article/pii/S1747938X22000033> |
| 13주 | 같음 | Yee & Bailenson (2007) · Ratan et al. (2020) | 프로테우스 효과 r = .22~.26 · 큰 키 아바타 -> 협상 공격성 상승 및 실제 과제 전이 | <https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-2958.2007.00299.x> · <https://www.tandfonline.com/doi/pdf/10.1080/15213269.2019.1623698> |
| 13주 | 같음 | Madary & Metzinger (2016) | 연구 윤리 6주제 + 사용자 위험 4주제 | <https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00003/full> |
| 14주 | 팀 프로젝트 구현·플레이테스트·프로파일링 | Kennedy et al. (1993) | SSQ 16증상 · 0~3점 · 하위척도 3개 (N·O·D) | <https://www.semanticscholar.org/paper/Simulator-Sickness-Questionnaire:-An-enhanced-for-Kennedy-Lane/0543a8a6e1d57deead06199b5876e6ea21defacb> |
| 14주 | 같음 | Saredakis et al. (2020) | 노출 시간별 SSQ : 10분 미만 23.47 · 10분 이상 33.42 · 20분 이상 27.35 | <https://www.frontiersin.org/articles/10.3389/fnhum.2020.00096/full> |
| 14주 | 같음 | St. Pierre et al. (2015) | 기저 약 70 ms + 0.2 Hz · 진폭 100 ms 변동 -> SSQ 상승 | <https://www.sciencedirect.com/science/article/abs/pii/S0141938214000791> |
| 14주 | 같음 | Makransky et al. (2019) | 프레즌스 상승 + 인지 부하 상승 -> 학습 저하 | <https://www.sciencedirect.com/science/article/abs/pii/S0959475217303274> |
| 14주 | 같음 | 핸드 트래킹 비교 연구 | Whack-a-Mole 0.78초 (컨트롤러) vs 1.00초 (핸드 트래킹) | <https://link.springer.com/article/10.1007/s10055-026-01333-2> |
| 14주 | 같음 | LaValle 12.4 | 증상 측정 시점 : 사전 · 10분 · 30분 · 직후 · 60분 후 | <https://lavalle.pl/vr/vrch12.pdf> |
| 15주 | 기말 : 팀 프로젝트 최종 발표·VR 시연 | Slater (2004) | 온라인 응답자 74명 · 임의 구성 «경험의 색채감» 도 과제 성취와 상관 -> 설문 단독 결론 금지 | <https://dl.acm.org/doi/10.1162/1054746041944849> |
| 15주 | 같음 | Slater (2009) | PI · Psi 2분법으로 시연 평가 기준 분리 | <https://www.macs.hw.ac.uk/~ruth/year4VEs/Resources/Slater2009RoyalSoc.html> |
| 15주 | 같음 | Souchet et al. (2023) | 중도 포기 15.6% -> 시연 중단 선택권 안내 근거 | <https://link.springer.com/article/10.1007/s10055-022-00672-0> |

---

## 12. LaValle 『Virtual Reality』 장·절 매핑

- 전문 : <https://lavalle.pl/vr/> (Cambridge University Press, 2023)

| 주차 | LaValle 절 | 제목 | 용도 |
|---|---|---|---|
| 5주 | 4.1~4.2 · 6.1 | Light Propagation · Lenses and Images · Perception of Depth | 라이팅·단안 깊이 단서 |
| 5·6주 | 7.1~7.3 | Graphical Rendering · Ray Tracing and Shading Models · Rasterization | 렌더링 파이프라인 |
| 6주 | 5.1~5.2 · 5.4 | From the Cornea to Photoreceptors · From Photoreceptors to the Visual Cortex · Implications for VR | 해상도 요구 조건 계산 |
| 7주 | 8.1 · 8.2 · 8.3 | Velocities and Accelerations · The Vestibular System · Physics in the Virtual World | 물리·전정계 |
| 7주 | 6.2 · 8.4 | Perception of Motion · Mismatched Motion and Vection | 벡션 |
| 10주 | 10.1 · 10.3 | Motor Programs and Remapping · Manipulation | 입력 리매핑·조작 |
| 11주 | 9.1~9.3 · 10.2 | Tracking 2D·3D Orientation·Position · Locomotion | 트래킹·이동 |
| 11·12주 | 7.4 | VR Rendering Problems (왜곡 보정·이미지 워핑) | 지연 보상·왜곡 |
| 12주 | 12.2 | Recommendations for Developers | 공간 UI 금지 규칙 (화면 고정 요소 금지 등) |
| 14주 | 12.3 | Comfort and VR Sickness | 멀미 이론·개인차·후유 증상 |
| 14·15주 | 12.4 | Experiments on Human Subjects | 측정 시점·요구 특성·IRB |
| 13주 | 10.4 · 13 | Social Interaction · Frontiers | 아바타·확장 주제 |

---

## 13. «확실하지 않음» 항목 모음

| 번호 | 항목 | 이유 | 수업 처리 |
|---|---|---|---|
| 1 | 감각 충돌 이론 vs 자세 불안정 이론의 우열 | 학계 논쟁 지속 · 단일 이론으로 전체 설명 미달 | 두 이론 병기 · 정설 표현 금지 |
| 2 | SSQ 총점의 «위험 구간» 절단점 | 합의 미달 · HMD 모집단 규준 부재 | 상대 비교만 사용 |
| 3 | 사이버멀미 성별 차이 | Saredakis 메타분석 무차이 · 타 문헌 여성 고감수성 주장 | 미합의로 서술 |
| 4 | 코 모형 (nasum virtualis) 효과 | 학술 발표 자료 · 동료심사 지면 미확인 · 두 씬 효과 94.2초 대 2.2초로 극단 | 참고 사례로만 제시 |
| 5 | 베그넷팅 효과 방향 | 증폭 회전 조건에서 증가 보고 공존 | 조건 의존으로 서술 |
| 6 | 광학 흐름 10 m/s 초과 구간 포화 | 2차 출처 요약만 확보 | 수치 미사용 |
| 7 | 방사형 흐름 > 층류형 흐름 (벡션 유발) | 1차 출처 미특정 | 비교 주장 미사용 |
| 8 | 과예측 (overprediction) 부작용 정량 | 특허 명세 외 동료심사 정량 결과 미확보 | 정성 서술만 |
| 9 | 최신 HMD 에서 거리 압축 감소 여부 | 측정법 간 불일치 큼 (74~82% 범위) | 74% 를 2013년 집계값으로 명시 |
| 10 | 조절-수렴 ±0.5 D 권고 | 원문 명시 여부 미확인 (후속 문헌 해석 가능) | «후속 문헌 권고» 로 표기 |
| 11 | 94 PPD 측정 | 단일 최근 연구 · 60 PPD 관행과 측정 패러다임 차이 가능 | 두 값 병기 |
| 12 | 고무손 착각 측정 지표 타당도 | 고유감각 이동과 소유감 해리 · 요구 특성 교란 · 재현 연구 진행 중 | 논쟁 명시 |
| 13 | Peck 2013 암묵 편향 감소 | 표본 규모·지속 기간 추가 재현 필요 | 단일 연구로 표기 |
| 14 | 핸드 트래킹 성능 격차 | 기기 세대·과제 유형에 따라 결론 변동 · 최신 비교 연구 지면·연도 표기 미확정 | 과제 의존으로 서술 |
| 15 | 신기성 효과의 존재·크기 | 상반 결과 공존 (Huang 2021 하락 없음) | 단정 금지 |
| 16 | 외과 VR 훈련 메타분석 | 이질성 큼 · 환자 결과·비용 개선 미확인 | 원문 한계 병기 |
| 17 | 몰입 수준별·개입 길이별 효과 크기 | 1차 출처 미특정 | 수치 미사용 |
| 18 | 편안한 시야 범위 좌우 30° · 최대 55° | 2차 출처(블로그 정리) 만 확보 | 수치 미사용 |
| 19 | Witmer & Singer PQ 문항 수 | 판본별 차이 (19·32 보고 혼재) | 문항 수 미기재 |
| 20 | Valve 90 fps 요구 | 1차 문서 내 조항 확인 미완 | 2차 출처 표기 |
| 21 | Terenzi & Zaal 참가자 성별 내역 | 본문에 18명 · «남 11 · 여 6» 로 합계 불일치 | 표본 수 18명만 기재 |

---

## 14. «더 조사 필요» 목록

1. **SSQ 대안 척도** : VRSQ (Kim et al. 2018) · CSQ-VR · FMS 의 구성과 HMD 규준 수치 · 한국어 타당화 여부
2. **과예측 정량** : 예측 지평(prediction horizon) 별 오버슈트 각도와 불편감 증가량을 보고한 동료심사 연구
3. **ATW/reprojection 지각 비용** : 재투영 아티팩트의 탐지 임계값 (디스오클루전 폭·속도 기준)
4. **포비티드 렌더링 수용 범위** : Quest 3·Quest Pro 급 기기에서 ETFR 적용 시 지각 저하 임계 편심각 수치
5. **거리 압축 최신값** : 2018년 이후 HMD 를 쓴 보행 기반 거리 추정 연구의 평균 비율
6. **조절-수렴 1차 수치** : Shibata et al. 2011 원문의 편안 영역 디옵터 경계값 표
7. **중심와 추세포 밀도 1차 출처** : Curcio et al. 계열 해부 문헌의 cones/mm² 수치
8. **핸드 트래킹 최신 비교** : Quest 3 핸드 트래킹 대상 Fitts 법칙 처리율(throughput, bits/s) 보고 연구
9. **공간 UI 근거 논문** : 제조사 권고 거리(42~46 cm · 0.75~3.5 m) 의 근거가 된 실험 연구
10. **대학 수업용 노출 시간 권고** : 연속 착용 최대 시간·회기 간 간격에 관한 학술 근거 또는 기관 지침
11. **한국 대학 IRB 관행** : 수업 내 VR 체험의 동의 절차 요구 수준 (수업 활동 vs 연구 구분)
12. **디자인 전공 적합 사례** : 시각 디자인·제품 디자인 교육에서 VR 사용 효과를 보고한 메타분석 또는 RCT
13. **벡션 1차 비교 연구** : 방사형 vs 층류형 흐름, 중심시 vs 주변시 비교의 원 논문 (Telford et al. 1992 계열) 수치
14. **Visual Factors in Cybersickness 메타분석 서지** : 저자·연도·권호 확정 (현재 온라인 선공개 상태)
15. **반복 노출 적응 지속 기간** : 적응 효과가 며칠·몇 주 유지되는지 측정한 종단 연구
