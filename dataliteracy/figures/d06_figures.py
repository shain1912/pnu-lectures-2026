"""
데이터리터러시 6주차 도해 — 차트 선택과 시각화의 함정
차트별 강점, 축 자르기, 이중 축, 구간 폭, 면적 왜곡, 과적합

실행:  cd dataliteracy/figures && ../../.venv/Scripts/python.exe d06_figures.py [필터]
출력:  dataliteracy/figures/out/d06-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon

from _style import *   # noqa: F403

rng = np.random.default_rng(606)

QUARTER = ["1분기", "2분기", "3분기", "4분기"]
SALES = np.array([100.0, 101.0, 102.0, 104.0])


# --------------------------------------------------------------- 헬퍼
def _box(ax, x, y, w, h, text, color, fs=11.5, bold=True, fill=0.10, align="center"):
    """둥근 모서리 라벨 상자."""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.6,rounding_size=1.6",
                                facecolor=color + format(int(fill * 255), "02x"),
                                edgecolor=color, lw=1.6, zorder=4))
    ha = {"center": "center", "left": "left"}[align]
    tx = x + w / 2 if align == "center" else x + 1.2
    ax.text(tx, y + h / 2, text, color=color, fontsize=fs,
            fontweight="bold" if bold else "normal",
            ha=ha, va="center", linespacing=1.65, zorder=6)


def _arrow(ax, x0, y0, x1, y1, color=FAINT, lw=1.6):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0), zorder=3)


def _mini(ax, title, color, strong, weak, avoid):
    """미니 차트 아래에 강점·약점·금지 상황 세 줄."""
    ax.set_title(title, loc="left", color=color, fontsize=12.5, pad=8)
    ax.text(0, -0.16, "강점 : " + strong, transform=ax.transAxes,
            color=LAB, fontsize=10.2, va="top")
    ax.text(0, -0.40, "약점 : " + weak, transform=ax.transAxes,
            color=WARN, fontsize=10.2, va="top")
    ax.text(0, -0.64, "금지 : " + avoid, transform=ax.transAxes,
            color=TRAP, fontsize=10.2, va="top")


def _bars(ax, base, color=GFX, top=None):
    """4분기 매출 막대 · base 가 y축 시작값."""
    ax.bar(QUARTER, SALES - base, bottom=base, width=0.56, color=color, zorder=4)
    ax.set_ylim(base, top if top is not None else SALES.max() * 1.18)
    for q, v in zip(QUARTER, SALES):
        ax.text(q, v + (ax.get_ylim()[1] - base) * 0.03, f"{v:.0f}",
                ha="center", color=FG, fontsize=11, fontweight="bold", family=CODE)


# =====================================================================
# 1. 목적에서 차트로 — 선택 흐름
# =====================================================================
def fig_chart_decision():
    fig, ax = plt.subplots(figsize=(13.2, 6.4))
    clean(ax)

    rows = [
        ("항목 비교",      "막대 · 가로막대",       "y축 0 시작 · 정렬 기준 표기", GFX),
        ("시간 추세",      "선",                    "시간 간격 균일 · 결측 구간 표시", GFX),
        ("분포 모양",      "히스토그램 · 상자그림", "구간 폭에 따라 인상 변화", VR),
        ("두 변수 관계",   "산점도",                "점 과밀 시 투명도 조정 · 7주 연결", VR),
        ("구성 비율",      "누적 막대 · 트리맵",    "파이는 항목 5개 이하", WARN),
    ]
    ys = [50, 39, 28, 17, 6]

    _box(ax, 1, 24.5, 17, 11,
         "무엇을\n보여주는가?", FG, fs=14, fill=0.06)

    for y, (purpose, chart, caution, color) in zip(ys, rows):
        _arrow(ax, 18.6, 30, 23.4, y + 4.2, color=LINE)
        _box(ax, 24, y, 20, 8.4, purpose, color, fs=13)
        _arrow(ax, 44.6, y + 4.2, 49.4, y + 4.2, color=color, lw=1.8)
        _box(ax, 50, y, 24, 8.4, chart, FG, fs=12.5, fill=0.05)
        ax.text(77, y + 4.2, caution, color=DIM, fontsize=11, va="center")

    ax.set_xlim(0, 126); ax.set_ylim(3.5, 60)
    ax.set_title("차트 선택 — 데이터 종류보다 «목적» 이 먼저",
                 loc="left", pad=16, fontsize=15)
    fig.text(0.5, 0.03,
             "같은 데이터라도 묻는 질문이 바뀌면 차트도 교체",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")
    fig.subplots_adjust(top=0.89, bottom=0.11)
    return save(fig, "d06-chart-decision", pad=0.3)


# =====================================================================
# 2. 차트별 강점·약점 한눈 비교
# =====================================================================
def fig_chart_strengths():
    fig, axes = plt.subplots(3, 3, figsize=(14.0, 10.2))
    for a in axes.ravel():
        clean(a)

    cats = ["A", "B", "C", "D"]
    vals = [62, 48, 35, 22]

    # ① 막대
    ax = axes[0, 0]
    ax.bar(cats, vals, color=GFX, width=0.6)
    ax.set_ylim(0, 72)
    _mini(ax, "막대", GFX,
          "항목 5~10개의 값 비교",
          "항목 이름이 길면 겹침",
          "시간 추세 · 항목 20개 초과")

    # ② 가로막대
    ax = axes[0, 1]
    names = ["교통", "식비", "주거", "통신", "여가"]
    ax.barh(names, [55, 44, 38, 24, 18], color=GFX, height=0.6)
    ax.invert_yaxis()
    for i, n in enumerate(names):
        ax.text(-2, i, n, color=DIM, fontsize=9.5, ha="right", va="center")
    ax.set_xlim(0, 62)
    _mini(ax, "가로막대", GFX,
          "긴 항목 이름 · 항목 10개 이상 비교",
          "시간 흐름 표현 곤란",
          "시계열 · 누적 추세")

    # ③ 선
    ax = axes[0, 2]
    t = np.arange(12)
    ax.plot(t, 100 + np.cumsum(rng.normal(2.2, 2.6, 12)), color=GFX, lw=2.4,
            marker="o", ms=4, mec=BG, mew=1.2)
    _mini(ax, "선", GFX,
          "시간에 따른 변화 방향과 속도",
          "항목 간격이 불규칙하면 왜곡",
          "순서 없는 범주 연결")

    # ④ 산점도
    ax = axes[1, 0]
    x = rng.normal(0, 1, 150)
    ax.plot(x, 0.74 * x + rng.normal(0, 0.62, 150), "o", ms=4.5,
            color=VR, mec=BG, mew=0.6, alpha=0.85)
    _mini(ax, "산점도", VR,
          "두 변수 관계 · 군집 · 이상치 동시 확인",
          "점 수천 개면 겹쳐서 밀도 파악 곤란",
          "한 변수만 보여줄 때")

    # ⑤ 히스토그램
    ax = axes[1, 1]
    ax.hist(np.concatenate([rng.normal(42, 7, 600), rng.normal(78, 7, 600)]),
            bins=22, color=VR, alpha=0.9)
    _mini(ax, "히스토그램", VR,
          "한 변수의 분포 모양 · 봉우리 개수",
          "구간 폭에 따라 인상 변화",
          "항목별 값 비교")

    # ⑥ 상자그림
    ax = axes[1, 2]
    data = [rng.normal(60, 8, 200), rng.normal(66, 16, 200), rng.normal(58, 5, 200)]
    bp = ax.boxplot(data, patch_artist=True, widths=0.5,
                    medianprops=dict(color=LAB, lw=2.0),
                    flierprops=dict(marker="o", ms=3.5, mfc=TRAP, mec="none"))
    for b in bp["boxes"]:
        b.set(facecolor=VR + "33", edgecolor=VR, lw=1.6)
    for part in ("whiskers", "caps"):
        for w in bp[part]:
            w.set(color=VR, lw=1.3)
    ax.set_xticks([])
    _mini(ax, "상자그림", VR,
          "여러 집단의 중앙값·흩어짐·이상치 비교",
          "봉우리 개수 표현 불가",
          "이봉 분포 요약 · 표본 10개 미만")

    # ⑦ 누적 막대
    ax = axes[2, 0]
    a, b, c = np.array([30, 34, 28, 36]), np.array([24, 20, 26, 18]), np.array([16, 18, 14, 20])
    ax.bar(cats, a, color=GFX, width=0.6)
    ax.bar(cats, b, bottom=a, color=VR, width=0.6)
    ax.bar(cats, c, bottom=a + b, color=WARN, width=0.6)
    _mini(ax, "누적 막대", WARN,
          "전체 합과 구성 비율 동시 표현",
          "맨 아래 조각 외에는 기준선이 달라 비교 곤란",
          "가운데 조각끼리 정밀 비교")

    # ⑧ 파이
    ax = axes[2, 1]
    ax.pie([46, 27, 17, 10], colors=[GFX, VR, WARN, FAINT],
           startangle=90, wedgeprops=dict(edgecolor=BG, lw=2),
           radius=1.12)
    _mini(ax, "파이", WARN,
          "전체 대비 비중 1~2개 강조",
          "각도·면적 비교의 정확도 낮음",
          "항목 6개 이상 · 시간 변화 · 순위 비교")

    # ⑨ 히트맵
    ax = axes[2, 2]
    m = rng.integers(2, 30, (4, 6)).astype(float)
    m[1, 4] = 46
    ax.imshow(m, cmap="magma", aspect="auto")
    _mini(ax, "히트맵", TRAP,
          "두 범주의 교차 밀도 · 넓은 표의 패턴",
          "색 단계 선택에 따라 인상 변화",
          "정확한 값 비교 · 색각 고려 없는 배색")

    fig.subplots_adjust(hspace=1.02, wspace=0.22, top=0.9, bottom=0.08)
    fig.suptitle("차트별 강점 · 약점 · 금지 상황", x=0.012, ha="left",
                 fontsize=16, color=FG, fontweight="bold", y=0.975)
    return save(fig, "d06-chart-strengths", pad=0.3)


# =====================================================================
# 3. 축 자르기 — 같은 4% 를 다르게 보이게 하는 방법
# =====================================================================
def fig_axis_truncation():
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.6))

    base_r = 99.0
    ratio = (SALES[-1] - base_r) / (SALES[0] - base_r)

    ax = axes[0]; style_axes(ax, grid=False)
    _bars(ax, 0, color=GFX, top=128)
    ax.axhline(0, color=LINE, lw=1.4)
    ax.set_title("y축 0 시작", loc="left", color=LAB, fontsize=14, pad=10)
    ax.text(0.0, -0.13, "막대 길이 비 1 : 1.04  →  보이는 대로 4% 증가",
            transform=ax.transAxes, color=LAB, fontsize=11.5, va="top")
    ax.set_ylabel("매출 (억원)", labelpad=8)

    ax = axes[1]; style_axes(ax, grid=False)
    _bars(ax, base_r, color=TRAP, top=105.4)
    ax.set_title("y축 99 시작", loc="left", color=TRAP, fontsize=14, pad=10)
    ax.text(0.0, -0.13,
            f"막대 길이 비 1 : {ratio:.0f}  →  5배 급증 인상",
            transform=ax.transAxes, color=TRAP, fontsize=11.5, va="top")
    ax.set_yticks([99, 101, 103, 105])

    fig.subplots_adjust(wspace=0.22, top=0.86, bottom=0.27)
    fig.text(0.5, 0.055,
             "같은 데이터 · 같은 숫자 · y축 시작값만 변경",
             color=FG, fontsize=15, ha="center", fontweight="bold")
    fig.text(0.5, 0.005,
             "축 자르기 자체가 금지 항목은 아님 · 자른 사실과 범위를 표기해야 성립",
             color=DIM, fontsize=11.5, ha="center")
    return save(fig, "d06-axis-truncation", pad=0.34)


# =====================================================================
# 4. 이중 축 — 오른쪽 축 범위가 바꾸는 «추월 시점»
# =====================================================================
def fig_dual_axis():
    months = np.arange(1, 13)
    sales = np.array([100, 104, 109, 113, 118, 122, 127, 131, 136, 140, 145, 150], float)
    visit = np.array([4800, 4650, 4500, 4330, 4180, 4020, 3860, 3700, 3550, 3400, 3240, 3100], float)

    def cross(a_lo, a_hi, b_lo, b_hi):
        """두 선이 화면에서 만나는 월 (축 범위에 따라 이동)."""
        an = (sales - a_lo) / (a_hi - a_lo)
        bn = (visit - b_lo) / (b_hi - b_lo)
        d = an - bn
        idx = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
        if len(idx) == 0:
            return None
        i = idx[0]
        return months[i] + d[i] / (d[i] - d[i + 1])

    setups = [
        (90.0, 160.0, 0.0, 5200.0, "오른쪽 축 0 ~ 5,200"),
        (90.0, 160.0, 3000.0, 5000.0, "오른쪽 축 3,000 ~ 5,000"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.4))

    for ax, (a_lo, a_hi, b_lo, b_hi, label) in zip(axes, setups):
        style_axes(ax, grid=False)
        ax.plot(months, sales, color=GFX, lw=2.6, marker="o", ms=5, mec=BG, mew=1.2)
        ax.set_ylim(a_lo, a_hi)
        ax.set_ylabel("매출 (억원)", color=GFX, labelpad=6)
        ax.tick_params(axis="y", colors=GFX)

        ax2 = ax.twinx()
        ax2.plot(months, visit, color=VR, lw=2.6, marker="o", ms=5, mec=BG, mew=1.2)
        ax2.set_ylim(b_lo, b_hi)
        ax2.set_ylabel("방문자 (명)", color=VR, labelpad=8)
        ax2.tick_params(axis="y", colors=VR)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_color(LINE)
        ax2.set_facecolor(BG)

        c = cross(a_lo, a_hi, b_lo, b_hi)
        if c is not None:
            ax.axvline(c, color=WARN, lw=1.8, ls="--", zorder=6)
            ax.text(c + 0.2, a_lo + (a_hi - a_lo) * 0.07,
                    f"교차 {c:.1f}월", color=WARN, fontsize=11.5,
                    fontweight="bold", family=CODE)
        ax.set_xticks([1, 3, 5, 7, 9, 11])
        ax.set_xlabel("월", labelpad=6)
        ax.set_title(label, loc="left", color=FG, fontsize=13.5, pad=10)

    fig.subplots_adjust(wspace=0.45, top=0.86, bottom=0.17)
    fig.text(0.5, 0.028,
             "두 패널의 숫자 동일 · 오른쪽 축 범위만 변경 → 교차 시점 이동",
             color=FG, fontsize=14.5, ha="center", fontweight="bold")
    fig.text(0.5, -0.03,
             "이중 축 : 두 단위의 교차 시점에 의미 없음 · 비율 지수로 환산 후 한 축 사용 권장",
             color=DIM, fontsize=11.5, ha="center")
    return save(fig, "d06-dual-axis", pad=0.36)


# =====================================================================
# 5. 구간 폭 — 같은 데이터, 봉우리 개수 변화
# =====================================================================
def fig_bin_width():
    s = np.concatenate([rng.normal(42, 7.5, 900), rng.normal(78, 7.0, 900)])
    specs = [(3, (25, 115), GFX, "봉우리 1개", "구간이 넓어 두 집단 병합"),
             (24, (10, 110), LAB, "봉우리 2개", "두 집단 구분 가능"),
             (90, (10, 110), TRAP, "봉우리 다수", "잡음까지 봉우리로 표시")]

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.8), sharex=True)
    for ax, (bins, rg, c, peak, msg) in zip(axes, specs):
        style_axes(ax, grid=False)
        ax.hist(s, bins=bins, range=rg, color=c, alpha=0.9, zorder=3)
        ax.set_yticks([])
        ax.set_title(f"구간 {bins}개 — {peak}", loc="left", color=c,
                     fontsize=13, pad=9)
        ax.text(0.0, -0.13, msg, transform=ax.transAxes, color=DIM,
                fontsize=11, va="top")
        ax.set_xticks([20, 50, 80, 110])
        ax.set_xlim(8, 118)

    fig.subplots_adjust(wspace=0.14, top=0.85, bottom=0.28)
    fig.text(0.5, 0.07,
             "세 그림의 원본 데이터 동일 · 구간 개수만 변경",
             color=FG, fontsize=14.5, ha="center", fontweight="bold")
    fig.text(0.5, 0.012,
             "구간 폭 고정값 없음 → 두세 가지로 그려 보고 모양이 유지되는 범위 확인",
             color=LAB, fontsize=11.5, ha="center")
    return save(fig, "d06-bin-width", pad=0.34)


# =====================================================================
# 6. 면적·3D 왜곡
# =====================================================================
def fig_area_illusion():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.6))

    # ---------------- 왼쪽: 원 크기
    ax = axes[0]; clean(ax)
    ax.set_aspect("equal")
    r1 = 1.0
    ax.add_patch(Circle((1.8, 2.0), r1, facecolor=GFX + "44", edgecolor=GFX, lw=2))
    ax.text(1.8, 4.1, "값 100", color=GFX, fontsize=12.5, ha="center",
            fontweight="bold", family=CODE)
    ax.text(1.8, -0.75, "기준", color=GFX, fontsize=11, ha="center")

    ax.add_patch(Circle((6.2, 2.0), 2 * r1, facecolor=TRAP + "33", edgecolor=TRAP, lw=2))
    ax.text(6.2, 4.6, "값 200", color=TRAP, fontsize=12.5, ha="center",
            fontweight="bold", family=CODE)
    ax.text(6.2, -0.75, "반지름 2배", color=TRAP, fontsize=11.5, ha="center",
            fontweight="bold")
    ax.text(6.2, -1.6, "면적 4배 인상", color=TRAP, fontsize=11, ha="center")

    ax.add_patch(Circle((11.2, 2.0), np.sqrt(2) * r1,
                        facecolor=LAB + "33", edgecolor=LAB, lw=2))
    ax.text(11.2, 4.1, "값 200", color=LAB, fontsize=12.5, ha="center",
            fontweight="bold", family=CODE)
    ax.text(11.2, -0.75, "반지름 √2배", color=LAB, fontsize=11.5, ha="center",
            fontweight="bold")
    ax.text(11.2, -1.6, "면적 2배 · 값에 비례", color=LAB, fontsize=11, ha="center")

    ax.set_xlim(-0.6, 14.0); ax.set_ylim(-2.6, 5.4)
    ax.set_title("① 원 크기 — 반지름과 면적", loc="left", color=TRAP,
                 fontsize=13.5, pad=10)

    # ---------------- 오른쪽: 3D 막대의 윗면
    ax = axes[1]; clean(ax)
    dx, dy = 0.42, 5.2
    for i, (x0, h, c) in enumerate([(1.0, 52, GFX), (4.4, 60, TRAP)]):
        w = 1.9
        ax.add_patch(Rectangle((x0, 0), w, h, facecolor=c + "55",
                               edgecolor=c, lw=1.8, zorder=4))
        ax.add_patch(Polygon([(x0, h), (x0 + w, h),
                              (x0 + w + dx * 2, h + dy), (x0 + dx * 2, h + dy)],
                             closed=True, facecolor=c + "88",
                             edgecolor=c, lw=1.6, zorder=5))
        ax.add_patch(Polygon([(x0 + w, 0), (x0 + w + dx * 2, dy),
                              (x0 + w + dx * 2, h + dy), (x0 + w, h)],
                             closed=True, facecolor=c + "33",
                             edgecolor=c, lw=1.4, zorder=5))
        ax.plot([x0 - 0.5, x0 + w + dx * 2 + 0.4], [h, h], color=c, lw=1.2,
                ls=":", zorder=6)
        ax.text(x0 + w / 2, h / 2, f"{h}", color=FG, fontsize=13,
                ha="center", va="center", fontweight="bold", family=CODE, zorder=7)

    for gy in range(0, 81, 20):
        ax.plot([0.3, 8.4], [gy, gy], color="#1e2431", lw=0.9, zorder=2)
        ax.text(0.1, gy, str(gy), color=FAINT, fontsize=10, ha="right",
                va="center", family=CODE)

    ax.plot([7.6, 9.1], [65.2, 72], color=WARN, lw=1.2, zorder=6)
    ax.text(9.3, 72, "보이는 꼭대기 65", color=WARN, fontsize=10.5, va="center")
    ax.plot([7.3, 9.1], [60, 52], color=DIM, lw=1.2, zorder=6)
    ax.text(9.3, 52, "눈금상 값 60", color=DIM, fontsize=10.5, va="center")

    ax.set_xlim(-0.6, 11.4); ax.set_ylim(-14, 88)
    ax.set_title("② 3D 막대 — 값 위치 모호", loc="left", color=TRAP,
                 fontsize=13.5, pad=10)
    ax.text(0.0, -0.06, "윗면과 측면이 더해져 실제 값보다 커 보임 · 3D 효과 사용 금지",
            transform=ax.transAxes, color=DIM, fontsize=11, va="top")

    fig.subplots_adjust(wspace=0.16, top=0.86, bottom=0.17)
    fig.text(0.5, 0.025,
             "길이 비교는 정확 · 면적과 부피 비교는 부정확",
             color=FG, fontsize=14.5, ha="center", fontweight="bold")
    return save(fig, "d06-area-illusion", pad=0.34)


# =====================================================================
# 7. 과적합 — 학습 데이터만 외운 모델
# =====================================================================
def fig_ml_overfitting():
    def truth(x):
        return 55 + 26 * np.sin(x * 2.1)

    xtr = np.linspace(0.05, 2.95, 12)
    ytr = truth(xtr) + rng.normal(0, 4.4, 12)
    xte = np.linspace(0.25, 2.80, 9) + 0.07
    yte = truth(xte) + rng.normal(0, 4.4, 9)

    grid = np.linspace(xtr.min(), xtr.max(), 400)
    over = np.polynomial.Polynomial.fit(xtr, ytr, 11)(grid)
    simple = np.polynomial.Polynomial.fit(xtr, ytr, 3)(grid)
    over_te = np.polynomial.Polynomial.fit(xtr, ytr, 11)(xte)
    simple_te = np.polynomial.Polynomial.fit(xtr, ytr, 3)(xte)

    err_over = np.abs(over_te - yte).mean()
    err_simple = np.abs(simple_te - yte).mean()

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.4), sharey=True)

    ax = axes[0]; style_axes(ax, grid=False)
    ax.plot(grid, over, color=TRAP, lw=2.4, zorder=5)
    ax.plot(grid, simple, color=LAB, lw=2.4, zorder=4)
    ax.plot(xtr, ytr, "o", ms=9, color=GFX, mec=BG, mew=1.5, zorder=7)
    ax.set_title("학습 데이터", loc="left", fontsize=14, pad=10)
    ax.text(0.03, 0.055, "붉은 선 : 12개 점을 모두 통과 · 오차 0",
            transform=ax.transAxes, color=TRAP, fontsize=11.5)
    ax.set_xlim(-0.05, 3.05); ax.set_ylim(0, 110)
    ax.set_xticks([])

    ax = axes[1]; style_axes(ax, grid=False)
    ax.plot(grid, over, color=TRAP, lw=2.4, zorder=5)
    ax.plot(grid, simple, color=LAB, lw=2.4, zorder=4)
    ax.plot(xte, yte, "D", ms=8, color=VR, mec=BG, mew=1.4, zorder=7)
    for x, y, p in zip(xte, yte, over_te):
        ax.plot([x, x], [y, np.clip(p, 0, 110)], color=TRAP, lw=1.2, ls=":", zorder=6)
    ax.set_title("처음 보는 데이터", loc="left", fontsize=14, pad=10)
    ax.text(0.03, 0.055,
            f"붉은 선 평균 오차 {err_over:.0f}  ·  초록 선 평균 오차 {err_simple:.0f}",
            transform=ax.transAxes, color=FG, fontsize=11.5, family=CODE)
    ax.set_xlim(-0.05, 3.05); ax.set_xticks([])

    fig.legend(handles=[
        plt.Line2D([], [], color=TRAP, lw=2.4, label="복잡한 모델 — 과적합"),
        plt.Line2D([], [], color=LAB, lw=2.4, label="단순한 모델"),
        plt.Line2D([], [], color=GFX, marker="o", ls="none", ms=8, label="학습 데이터"),
        plt.Line2D([], [], color=VR, marker="D", ls="none", ms=7, label="검증 데이터")],
        loc="upper center", bbox_to_anchor=(0.5, 1.085), ncol=4, fontsize=11.5)

    fig.subplots_adjust(wspace=0.08, top=0.82, bottom=0.14)
    fig.text(0.5, 0.025,
             "학습 데이터 성적이 좋은 모델과 쓸 만한 모델은 별개",
             color=FG, fontsize=14.5, ha="center", fontweight="bold")
    fig.text(0.5, -0.035,
             "과적합 : 학습 데이터의 잡음까지 외운 상태 → 검증 데이터로만 판별 가능",
             color=LAB, fontsize=12, ha="center")
    return save(fig, "d06-ml-overfitting", pad=0.36)


# =====================================================================
if __name__ == "__main__":
    import sys

    figs = [fig_chart_decision, fig_chart_strengths, fig_axis_truncation,
            fig_dual_axis, fig_bin_width, fig_area_illusion, fig_ml_overfitting]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
