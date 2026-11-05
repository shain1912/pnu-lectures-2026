"""
10·11주 A/B 실습용 합성 로그 생성기 (교육용 합성 데이터 · 실제 사람 없음)

사례 : 학식 쿠폰 앱 버튼 문구 실험
  A = «쿠폰 받기»  /  B = «오늘 점심 500원 아끼기»
  배정 단위 : 학생 1명 · 기간 : 14일 · 지표 : 버튼 클릭 여부(clicked)
  가드레일  : 앱 종료(left_app)

  ab_result.csv : 효과 있음 — A 클릭률 10% · B 클릭률 12% 근처
  ab_null.csv   : 효과 없음 — A·B 모두 10% (거짓 양성 연습용)

실행 : py dataliteracy/data/make_ab.py
시드 고정 → 항상 같은 파일 생성
"""
import csv
import pathlib
import random

HERE = pathlib.Path(__file__).parent
DAILY = 600
DAYS = 14
YEARS = ["1학년", "2학년", "3학년", "4학년"]
DEVICES = ["모바일", "PC"]


def make(name, p_a, p_b, seed):
    rnd = random.Random(seed)
    rows = []
    vid = 100000
    for day in range(1, DAYS + 1):
        for _ in range(DAILY):
            vid += 1
            variant = "A" if rnd.random() < 0.5 else "B"   # 난수 배정
            year = rnd.choices(YEARS, [0.28, 0.26, 0.24, 0.22])[0]
            device = rnd.choices(DEVICES, [0.82, 0.18])[0]
            base = p_a if variant == "A" else p_b
            clicked = int(rnd.random() < base)
            left_app = int(rnd.random() < 0.30)            # 두 버전 동일 → 부작용 없음
            rows.append([f"S{vid}", day, variant, year, device, clicked, left_app])
    with open(HERE / name, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["student_id", "day", "variant", "year", "device", "clicked", "left_app"])
        w.writerows(rows)
    return rows


def summary(rows):
    out = {}
    for v in "AB":
        r = [x for x in rows if x[2] == v]
        out[v] = (len(r), sum(x[5] for x in r), sum(x[6] for x in r))
    return out


if __name__ == "__main__":
    print("result", summary(make("ab_result.csv", 0.10, 0.12, 20261114)))
    print("null  ", summary(make("ab_null.csv", 0.10, 0.10, 20261121)))
