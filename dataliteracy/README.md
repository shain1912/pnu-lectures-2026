# 데이터리터러시의이해 강의자료

- 과목 : SF1101084 · 001분반 · AI융합교육원 · 전학년 · 선수과목 없음
- 시간 : 금 10:00–13:00 (3시간 연강)
- 담당 : 조성호
- 운영 : 데이터 분석 과정 + 바이브코딩
  - 수집 설계 → 정제 → 기술통계 → 시각화 → 상관 → 인과 → A/B 테스트 → 발표

## 슬라이드 주소

전체 목록 → **https://shain1912.github.io/pnu-lectures-2026/**

| 주차 | 제목 | 슬라이드 | PDF | 오프라인 zip |
|---|---|---|---|---|
| 2 | 데이터의 종류와 수집 설계 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w02/ | [PDF](dist/d02-데이터의종류와수집설계.pdf) | [zip](dist/d02-interactive-slides.zip) |
| 3 | 데이터 정제와 전처리 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w03/ | [PDF](dist/d03-데이터정제와전처리.pdf) | [zip](dist/d03-interactive-slides.zip) |
| 4 | 기술통계 기초 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w04/ | [PDF](dist/d04-기술통계기초.pdf) | [zip](dist/d04-interactive-slides.zip) |

5주차 이후 계획 → [plans/데이터리터러시-5-16주-계획.md](../plans/데이터리터러시-5-16주-계획.md)

## 조작

| 키 | 동작 |
|---|---|
| 방향키 / 스페이스 | 다음·이전 슬라이드 |
| `Esc` | 전체 슬라이드 목록 |
| `S` | 발표자 노트 (새 창) |
| 마우스 | 데모 슬라이더 조작 |

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `slides/wNN/index.html` | 주차별 슬라이드 원본 |
| `slides/_shared/` | 테마 CSS · reveal 초기화 · 데모 (`d03.js` 결측 대치, `d04.js` 대표값) |
| `figures/dNN_figures.py` | matplotlib 도해 생성 스크립트 |
| `figures/out/` | 도해 결과 (SVG · PNG) |
| `dist/` | 인쇄용 PDF · 오프라인 zip |

## 다시 만드는 법

```bash
# 도해
py dataliteracy/figures/d04_figures.py

# PDF + zip  (dataliteracy 폴더에서 로컬 서버 실행 후)
py -m http.server 8766
SLIDE_PORT=8766 node slides/build.mjs 02 03 04
```

## AI 함정 시리즈

| 주 | 번호 | 함정 |
|---|---|---|
| 2 | #1 | 존재하지 않는 데이터 제시 (데이터 환각) |
| 3 | #2 | 알리지 않은 결측 채우기·삭제 |
| 4 | #3 | 평균 하나로 끝낸 요약 |

문의 : `seongho.cho@kodekorea.kr`
