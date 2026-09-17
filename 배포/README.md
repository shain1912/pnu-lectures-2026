# 슬라이드 배포 주소

GitHub Pages 로 배포 · 링크만 열면 브라우저에서 바로 실행 · three.js 와 캔버스 데모 동작.

**전체 목록** : https://shain1912.github.io/pnu-lectures-2026/
**저장소** : https://github.com/shain1912/pnu-lectures-2026

## 컴퓨터그래픽스 (VF3500076)

| 주차 | 제목 | 주소 |
|---|---|---|
| 2주차 | 그래픽스 수학 기초 | https://shain1912.github.io/pnu-lectures-2026/slides/w02/ |
| 3주차 | Unity 기초와 게임 루프 | https://shain1912.github.io/pnu-lectures-2026/slides/w03/ |
| 4주차 | 렌더링 파이프라인의 이해 | https://shain1912.github.io/pnu-lectures-2026/slides/w04/ |

## 데이터리터러시의이해 (SF1101084)

| 주차 | 제목 | 주소 |
|---|---|---|
| 2주차 | 데이터의 종류와 수집 설계 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w02/ |
| 3주차 | 데이터 정제와 전처리 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w03/ |
| 4주차 | 기술통계 기초 | https://shain1912.github.io/pnu-lectures-2026/dataliteracy/slides/w04/ |

## 같은 내용의 다른 형식

| 형식 | 주소·위치 | 용도 |
|---|---|---|
| 슬라이드 | 위 표 | 링크 배포 · 데모 동작 |
| 인쇄용 PDF | `https://shain1912.github.io/pnu-lectures-2026/dist/…` | PLATO 첨부 · 데모는 안내 카드로 대체 |
| 오프라인 zip | `https://shain1912.github.io/pnu-lectures-2026/dist/*-interactive-slides.zip` | 인터넷 없는 환경 · 압축 해제 후 index.html |
| 원본 | `slides/wNN/index.html` | 수정 대상 |

## 폴더 구성

- `컴퓨터그래픽스/`, `데이터리터러시/` : 주차별 바로가기(`.url`)와 주소 메모(`.txt`)
- `.url` 더블클릭 → 해당 주차 슬라이드 열림

## 공개 범위

- GitHub 저장소 : **공개** · 주소를 아는 사람 모두 열람 가능
- 참고 교재와 타 교수 강의안 PDF : 저작권 문제로 저장소에서 제외
- 예비 주소(claude.ai) : 비공개 · 필요 시 각 페이지 Share 메뉴에서 공유 범위 지정

## 조작

| 키 | 동작 |
|---|---|
| 방향키 / 스페이스 | 다음·이전 슬라이드 |
| `Esc` | 전체 슬라이드 한눈에 보기 |
| `S` | 발표자 노트 (새 창) |
| 마우스 드래그 | 3D 화면 시점 회전 |

## 갱신

원본 수정 → `node slides/build.mjs 02 03 04` 로 PDF·zip 재생성 → `git push` · 1~2분 뒤 주소에 반영.
