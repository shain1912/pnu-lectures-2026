# 강의자료 — 조성호 · 부산대학교 2026-2

- **컴퓨터그래픽스** VF3500076 · 디자인앤테크놀로지전공 · VR + 그래픽스 이론 + 프롬프트 실습
- **데이터리터러시의이해** SF1101084 · AI융합교육원 · 데이터 분석 과정 + 바이브코딩

슬라이드 : reveal.js · 도해 : matplotlib · 애니메이션 : manim · 데모 : three.js

## 배포 주소

전체 목록 → **https://shain1912.github.io/pnu-lectures-2026/**

### 컴퓨터그래픽스

| 주차 | 제목 | 슬라이드 |
|---|---|---|
| 1 | 강의 소개와 컴퓨터그래픽스 개요 | https://shain1912.github.io/pnu-lectures-2026/slides/w01/ |
| 2 | 그래픽스 수학 기초 | https://shain1912.github.io/pnu-lectures-2026/slides/w02/ |
| 3 | Unity 기초와 게임 루프 | https://shain1912.github.io/pnu-lectures-2026/slides/w03/ |
| 4 | 렌더링 파이프라인의 이해 | https://shain1912.github.io/pnu-lectures-2026/slides/w04/ |
| 5 | 조명과 재질 | https://shain1912.github.io/pnu-lectures-2026/slides/w05/ |
| 6 | 셰이더 기초 | https://shain1912.github.io/pnu-lectures-2026/slides/w06/ |
| 7 | 애니메이션과 물리 | https://shain1912.github.io/pnu-lectures-2026/slides/w07/ |
| 8 | 중간고사 | https://shain1912.github.io/pnu-lectures-2026/slides/w08/ |
| 9 | 바이브코딩 심화 | https://shain1912.github.io/pnu-lectures-2026/slides/w09/ |
| 10 | 인터랙션 설계 | https://shain1912.github.io/pnu-lectures-2026/slides/w10/ |
| 11 | VR 개발 기초 | https://shain1912.github.io/pnu-lectures-2026/slides/w11/ |
| 12 | VR 인터랙션 심화 | https://shain1912.github.io/pnu-lectures-2026/slides/w12/ |
| 13 | 팀 프로젝트 기획 | https://shain1912.github.io/pnu-lectures-2026/slides/w13/ |
| 14 | 팀 프로젝트 구현 및 플레이테스트 | https://shain1912.github.io/pnu-lectures-2026/slides/w14/ |
| 15 | 기말 VR 전시와 동료 평가 | https://shain1912.github.io/pnu-lectures-2026/slides/w15/ |
| 16 | 프로젝트 피드백과 학기 정리 | https://shain1912.github.io/pnu-lectures-2026/slides/w16/ |

문서 : [강의계획서](syllabus/강의계획서.md) · [AI 사용 정책 · 프롬프트 로그 양식](syllabus/AI-사용-정책.md) · [용어집](syllabus/용어집.md) · [환경 설치 가이드](setup/환경설치-가이드.md) · [빌드 가이드 (Quest)](setup/빌드-가이드.md) · [Quest 운영 매뉴얼](setup/Quest-운영-매뉴얼.md) · [트러블슈팅 FAQ](setup/트러블슈팅-FAQ.md) · [AI 함정 카탈로그](labs/_traps/카탈로그.md) · [루브릭 총괄](rubrics/루브릭-총괄.md) · [팀 프로젝트 가이드북](rubrics/팀프로젝트-가이드북.md) · [SSQ 설문지](rubrics/SSQ-설문지.md)

### 데이터리터러시의이해

| 주차 | 제목 | 슬라이드 | PDF |
|---|---|---|---|
| 2 | 데이터의 종류와 수집 설계 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w02/ | [dist](dataliteracy/dist/d02-데이터의종류와수집설계.pdf) |
| 3 | 데이터 정제와 전처리 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w03/ | [dist](dataliteracy/dist/d03-데이터정제와전처리.pdf) |
| 4 | 기술통계 기초 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w04/ | [dist](dataliteracy/dist/d04-기술통계기초.pdf) |
| 5 | z-점수와 표준화 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w05/ | [dist](dataliteracy/dist/d05-z점수와표준화.pdf) |
| 6 | 차트 선택과 시각화의 함정 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w06/ | [dist](dataliteracy/dist/d06-차트선택과시각화의함정.pdf) |

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `slides/wNN/index.html` | 컴퓨터그래픽스 주차별 슬라이드 원본 |
| `slides/_shared/` | 테마 CSS · reveal 초기화 · three.js 데모 |
| `figures/*_figures.py` | matplotlib 도해 생성 스크립트 |
| `figures/anim/` | manim 애니메이션 소스 |
| `figures/out/` | 렌더링 결과 (SVG · PNG · MP4) |
| `dist/` | 인쇄용 PDF · 오프라인 zip |
| `dataliteracy/` | 데이터리터러시 과목 전체 (같은 구조) |
| `assignments/` | 과제 안내문 |
| `배포/` | 주차별 주소 메모와 바로가기 |
| `PLAN.md` | 16주 강의 설계 |
| `plans/` | 5~16주 상세 계획 · VR 심리·지각 연구 근거 |

## 다시 만드는 법

```bash
# 도해
py figures/w02_figures.py

# 애니메이션
py -m manim -qh figures/anim/w02_homogeneous.py Homogeneous

# PDF + zip  (로컬 서버 필요 : py -m http.server 8765)
node slides/build.mjs 02 03 04
```

## 문체 기준

슬라이드·안내문 모두 **개조식(명사 종결)** · `~합니다`체 미사용.
검사 : `py ~/.claude/skills/korean-slide-gaejosik/scripts/check_slide.py "slides/*/index.html"`

## 라이선스와 범위

- 본 저장소의 슬라이드·도해·코드 : 수업용 자작물
- 참고 교재와 타 교수 강의안 PDF : 저작권 문제로 미포함
- 문의 : `seongho.cho@kodekorea.kr`
