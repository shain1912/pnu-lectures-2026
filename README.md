# 강의자료 — 조성호 · 부산대학교 2026-2

- **컴퓨터그래픽스** VF3500076 · 디자인앤테크놀로지전공 · VR + 그래픽스 이론 + 프롬프트 실습
- **데이터리터러시의이해** SF1101084 · AI융합교육원 · 데이터 분석 과정 + 바이브코딩

슬라이드 : reveal.js · 도해 : matplotlib · 애니메이션 : manim · 데모 : three.js

## 배포 주소

전체 목록 → **https://shain1912.github.io/pnu-lectures-2026/**

### 컴퓨터그래픽스

| 주차 | 제목 | 슬라이드 | PDF |
|---|---|---|---|
| 2 | 그래픽스 수학 기초 | https://shain1912.github.io/pnu-lectures-2026/slides/w02/ | [dist](dist/w02-그래픽스수학기초.pdf) |
| 3 | Unity 기초와 게임 루프 | https://shain1912.github.io/pnu-lectures-2026/slides/w03/ | [dist](dist/w03-Unity기초와게임루프.pdf) |
| 4 | 렌더링 파이프라인의 이해 | https://shain1912.github.io/pnu-lectures-2026/slides/w04/ | [dist](dist/w04-렌더링파이프라인.pdf) |

### 데이터리터러시의이해

| 주차 | 제목 | 슬라이드 | PDF |
|---|---|---|---|
| 2 | 데이터의 종류와 수집 설계 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w02/ | [dist](dataliteracy/dist/d02-데이터의종류와수집설계.pdf) |
| 3 | 데이터 정제와 전처리 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w03/ | [dist](dataliteracy/dist/d03-데이터정제와전처리.pdf) |
| 4 | 기술통계 기초 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w04/ | [dist](dataliteracy/dist/d04-기술통계기초.pdf) |

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
