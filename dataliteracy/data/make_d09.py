"""
9주 실습용 합성 데이터 (교육용 합성 · 실제 통계로 해석 금지)

ice_cream.csv : 2년 104주 해변 도시 주간 자료
  week, month, temp_c, ice_cream_sales, drownings, rain_days
생성 규칙
  temp_c          : 계절 곡선 + 잡음
  ice_cream_sales : 기온에 비례 + 잡음
  drownings       : 기온에 비례 + 잡음
  아이스크림과 익사 사이 직접 연결 없음 → 둘의 상관은 전부 기온 경유

실행 : py dataliteracy/data/make_d09.py  (시드 고정)
"""
import csv
import math
import pathlib
import random

HERE = pathlib.Path(__file__).parent
rnd = random.Random(20261030)
rows = []
for w in range(1, 105):
    phase = 2 * math.pi * (w - 16) / 52
    temp = 15 + 11 * math.sin(phase) + rnd.gauss(0, 1.6)
    sales = 260 + 42 * temp + rnd.gauss(0, 70)
    drown = 0.9 + 0.26 * temp + rnd.gauss(0, 0.95)
    month = int(((w - 1) % 52) / 52 * 12) + 1
    rain = max(0, min(7, round(2.5 + 1.2 * math.sin(phase) + rnd.gauss(0, 1.3))))
    rows.append([w, month, round(temp, 1), round(max(0, sales)), max(0, round(drown)), rain])

with open(HERE / "ice_cream.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(["week", "month", "temp_c", "ice_cream_sales", "drownings", "rain_days"])
    wr.writerows(rows)
print("rows", len(rows))
