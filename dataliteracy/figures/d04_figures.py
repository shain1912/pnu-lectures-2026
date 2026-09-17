"""
데이터리터러시 4주차 도해 — 기술통계 기초
평균·중앙값·분산·표준편차, 그리고 분포의 모양

실행:  cd dataliteracy/figures && ../../.venv/Scripts/python.exe d04_figures.py [필터]
출력:  dataliteracy/figures/out/d04-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

from _style import *   # noqa: F403

rng = np.random.default_rng(404)


# --------------------------------------------------------------- 헬퍼
def _sym(n, mu, sd):
    """평균이 정확히 mu, 표준편차가 정확히 sd 인 좌우대칭 표본."""
    z = rng.normal(0, 1, n // 2)
    z = (z - z.mean()) / z.std()
    z = np.concatenate([z, -z])
    return mu + z * sd


def _span_arrow(ax, x0, x1, y, color, text, fs=10.5, up=0.0):
    """양쪽 화살표 + 가운데 라벨."""
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<|-|>", color=color, lw=1.6,
                                shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + up, text, color=color, fontsize=fs,
            ha="center", va="bottom", fontweight="bold", family=CODE)


def _sq(ax, x, y, side, color, label=None, fs=10):
    """면적이 곧 편차제곱인 정사각형."""
    ax.add_patch(Rectangle((x, y), side, side, facecolor=color + "33",
                           edgecolor=color, lw=1.8, zorder=4))
    if label:
        ax.text(x + side / 2, y - 1.7, label, color=color, fontsize=fs,
                ha="center", va="top", fontweight="bold", family=CODE, zorder=6)


# =====================================================================
# 1. 평균 연봉이라는 거짓말
# =====================================================================
def fig_mean_vs_median():
    pay = np.array([2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300,
                    3400, 3600, 3800, 4000, 4200, 4500, 4800, 5200, 6000, 30000])
    staff = pay[:-1]
    mean = pay.mean()          # 4900
    med = np.median(pay)       # 3350
    below = int((pay < mean).sum())   # 17

    fig, axes = plt.subplots(2, 1, figsize=(12.6, 5.6),
                             gridspec_kw=dict(height_ratios=[1.0, 0.72]))

    # ---------------- 위: 20명 전체
    ax = axes[0]; style_axes(ax, grid=False)
    ax.plot(staff, np.zeros_like(staff), "o", ms=12, color=GFX,
            mec=BG, mew=1.5, zorder=6)
    ax.plot(30000, 0, "o", ms=13, color=TRAP, mec=BG, mew=1.5, zorder=6)
    ax.axvline(med, color=LAB, lw=2.2, zorder=4)
    ax.axvline(mean, color=TRAP, lw=2.2, zorder=4)
    ax.add_patch(Rectangle((2200, -0.55), 4200, 1.1, facecolor="none",
                           edgecolor=FAINT, lw=1.2, ls=":", zorder=3))
    ax.annotate("사장 1명 · 3억", xy=(30000, 0.30), xytext=(25200, 1.30),
                color=TRAP, fontsize=12.5, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=1.7))
    ax.text(9000, 0.95, f"20명 중 {below}명이 «평균 이하»",
            color=WARN, fontsize=15, fontweight="bold", va="center")
    ax.text(9000, 0.30, "평균을 여기까지 끌어올린 사람은 단 한 명",
            color=DIM, fontsize=11.5, va="center")
    ax.set_xlim(1800, 31800); ax.set_ylim(-1.5, 1.7)
    ax.set_yticks([])
    ax.set_xticks([5000, 10000, 15000, 20000, 25000, 30000])
    ax.set_xticklabels(["5,000", "10,000", "15,000", "20,000",
                        "25,000", "30,000"], fontsize=10.5)
    ax.set_xlabel("연봉 (만원)  ·  점 하나 = 사람 한 명", labelpad=7, fontsize=11)
    ax.set_title("평균 연봉 4,900만원인 회사", loc="left", pad=14, fontsize=15)

    # ---------------- 아래: 점선 상자 안을 확대
    ax = axes[1]; style_axes(ax, grid=False)
    ax.plot(staff, np.zeros_like(staff), "o", ms=13, color=GFX,
            mec=BG, mew=1.5, zorder=6)
    ax.axvline(med, color=LAB, lw=2.4, zorder=4)
    ax.axvline(mean, color=TRAP, lw=2.4, zorder=4)
    ax.text(med - 90, 0.62, "중앙값 3,350", color=LAB, fontsize=12.5,
            fontweight="bold", ha="right", va="center", family=CODE)
    ax.text(mean + 90, 0.62, "평균 4,900", color=TRAP, fontsize=12.5,
            fontweight="bold", ha="left", va="center", family=CODE)
    ax.annotate("", xy=(6350, 0), xytext=(6150, 0),
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=2.0))
    ax.text(6320, 0.40, "사장은\n저 멀리", color=TRAP, fontsize=10.5,
            ha="center", va="center", linespacing=1.6)
    ax.annotate("", xy=(2280, -0.60), xytext=(4880, -0.60),
                arrowprops=dict(arrowstyle="<|-|>", color=WARN, lw=1.6,
                                shrinkA=0, shrinkB=0))
    ax.text(4120, -0.53, "평균선 왼쪽에 17명", color=WARN, fontsize=11,
            ha="center", va="bottom", fontweight="bold")
    ax.set_xlim(2200, 6400); ax.set_ylim(-1.15, 1.0)
    ax.set_yticks([])
    ax.set_xticks([2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000])
    ax.set_xticklabels(["2,500", "3,000", "3,500", "4,000",
                        "4,500", "5,000", "5,500", "6,000"], fontsize=10.5)
    ax.set_title("점선 상자 안 — 직원 19명만 확대", loc="left",
                 color=DIM, fontsize=12, pad=10)

    fig.subplots_adjust(hspace=0.62, top=0.9, bottom=0.08)
    fig.text(0.5, -0.055,
             "채용공고의 «평균 연봉 4,900만원» — 사실이지만 "
             "그 근처 연봉을 받는 사람은 0명",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")
    fig.text(0.5, -0.135,
             "평균 : 모든 값을 더함 → 아주 큰 값 하나에 끌려감  ·  "
             "중앙값 : «줄을 세웠을 때 한가운데 사람» → 영향 거의 없음",
             color=DIM, fontsize=11.5, ha="center")
    return save(fig, "d04-mean-vs-median", pad=0.4)


# =====================================================================
# 2. 평균이 같아도 같은 데이터가 아니다   ★ 3주차 회수
# =====================================================================
def fig_same_mean_diff_spread():
    fig, axes = plt.subplots(3, 1, figsize=(11.6, 6.6), sharex=True)

    specs = [
        ("A반", 4,  GFX,  "대부분 46~54점 사이에 밀집"),
        ("B반", 11, WARN, "적당한 흩어짐 · 흔한 모양"),
        ("C반", 20, VR,   "30점 미만, 70점 초과도 다수"),
    ]
    bins = np.linspace(0, 100, 41)

    for ax, (name, sd, c, msg) in zip(axes, specs):
        s = np.clip(_sym(1200, 50, sd), 0, 100)
        real = s.std()
        ax.hist(s, bins=bins, color=c, alpha=0.85, zorder=3)
        style_axes(ax, grid=False)
        top = ax.get_ylim()[1]
        ax.set_ylim(0, top * 1.62)
        ax.axvline(50, color=FG, lw=2.0, zorder=5)
        ax.axvspan(50 - real, 50 + real, color=c, alpha=0.13, zorder=2)
        _span_arrow(ax, 50 - real, 50 + real, top * 1.10, c,
                    f"평균 ± 표준편차 = {real:.0f}점", fs=10.5, up=top * 0.04)
        ax.text(1.5, top * 1.44, f"{name} · 평균 50점 · 표준편차 {real:.1f}점",
                color=c, fontsize=12.5, fontweight="bold", va="center")
        ax.text(99, top * 1.44, msg, color=DIM, fontsize=11,
                va="center", ha="right")
        ax.set_yticks([])

    axes[0].set_title("세 반의 기말고사 점수 — 평균은 셋 다 50점",
                      loc="left", pad=12, fontsize=15)
    axes[2].set_xlabel("점수", labelpad=8)
    axes[2].set_xticks([0, 20, 40, 50, 60, 80, 100])
    fig.subplots_adjust(hspace=0.28, top=0.9, bottom=0.12)

    fig.text(0.5, -0.02,
             "평균은 모두 50점 — 세 반에 같은 보충수업이 맞는가?",
             color=FG, fontsize=14, ha="center", fontweight="bold")
    fig.text(0.5, -0.085,
             "3주차 «평균 유지, 표준편차 감소» 의 의미  ·  "
             "가운데가 같아도 흩어진 정도가 다르면 다른 데이터",
             color=LAB, fontsize=12, ha="center")
    return save(fig, "d04-same-mean-diff-spread", pad=0.4)


# =====================================================================
# 3. 분산·표준편차를 손으로 따라가 본다
# =====================================================================
def fig_variance_steps():
    vals = np.array([60, 70, 75, 80, 90])
    mu = vals.mean()               # 75
    dev = (vals - mu).astype(int)  # -15 -5 0 5 15
    sq = dev ** 2                  # 225 25 0 25 225
    var = sq.mean()                # 100
    sd = np.sqrt(var)              # 10

    fig = plt.figure(figsize=(13.0, 7.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[0.80, 1.0], hspace=0.30,
                          left=0.035, right=0.985, top=0.87, bottom=0.13)

    # ---------------- ① 편차 — 평균에서 얼마나 떨어져 있나
    ax = fig.add_subplot(gs[0]); clean(ax)
    ax.plot([56, 94], [0, 0], color=LINE, lw=1.6, zorder=2)
    ax.plot([mu, mu], [-0.35, 1.25], color=FG, lw=2.0, zorder=3)
    ax.text(mu, 1.42, "평균 75점", color=FG, fontsize=12.5,
            fontweight="bold", ha="center", family=CODE)

    for v, d in zip(vals, dev):
        c = LAB if d < 0 else (TRAP if d > 0 else DIM)
        ax.plot(v, 0, "o", ms=14, color=GFX, mec=BG, mew=1.6, zorder=6)
        ax.text(v, -0.42, f"{v}", color=GFX, fontsize=12.5, ha="center",
                va="top", fontweight="bold", family=CODE)
        if d != 0:
            ax.annotate("", xy=(v, 0.62), xytext=(mu, 0.62),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=2.0,
                                        shrinkA=0, shrinkB=0), zorder=5)
            ax.text((v + mu) / 2, 0.76, f"{d:+d}", color=c, fontsize=12,
                    ha="center", fontweight="bold", family=CODE)

    ax.text(56, -1.25,
            "① 각 값에서 평균 빼기 = «편차»",
            color=WARN, fontsize=13.5, va="top", fontweight="bold")
    ax.text(56, -1.85,
            "그대로 더하면  (-15) + (-5) + 0 + 5 + 15 = 0  →  "
            "왼쪽과 오른쪽이 상쇄",
            color=FG, fontsize=12.5, va="top")
    ax.text(56, -2.42,
            "부호를 그대로 두면 «흩어진 정도» 측정 불가 → 다음 단계 필요",
            color=TRAP, fontsize=11.5, va="top")

    ax.set_xlim(54, 96); ax.set_ylim(-3.2, 1.95)
    ax.set_title("다섯 명의 점수   60 · 70 · 75 · 80 · 90", loc="left",
                 pad=14, fontsize=15)

    # ---------------- ②③④ — 한 자를 그대로 쓰는 넓이 그림
    ax = fig.add_subplot(gs[1]); clean(ax)
    ax.set_aspect("equal", adjustable="box", anchor="W")

    # ② 다섯 개의 정사각형
    spots = [(0, 15), (21, 5), (32, 0), (38, 5), (49, 15)]
    for (x0, side), d, s in zip(spots, dev, sq):
        if side == 0:
            ax.plot(x0, 0.6, "x", ms=10, color=DIM, mew=2.2, zorder=5)
            ax.text(x0, -2.0, "0² = 0", color=DIM, fontsize=10,
                    ha="center", va="top", family=CODE)
            continue
        ax.add_patch(Rectangle((x0, 0), side, side, facecolor=WARN + "2e",
                               edgecolor=WARN, lw=1.9, zorder=4))
        ax.text(x0 + side / 2, -2.0, f"{abs(d)}² = {s}", color=WARN,
                fontsize=10.5, ha="center", va="top", fontweight="bold",
                family=CODE)

    ax.text(0, 21.2, "② 제곱 — 편차를 한 변으로 하는 정사각형",
            color=WARN, fontsize=13.5, fontweight="bold")
    ax.text(0, 18.2, "225 + 25 + 0 + 25 + 225 = 500", color=DIM,
            fontsize=11.5, family=CODE)

    # 평균 화살표
    ax.annotate("", xy=(80, 5.0), xytext=(68, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=GFX, lw=2.4,
                                mutation_scale=20))
    ax.text(74, 6.4, "다섯 개를", color=GFX, fontsize=10.5, ha="center")
    ax.text(74, 3.0, "평균내면", color=GFX, fontsize=10.5, ha="center")

    # ③ 대표 정사각형 = 분산
    ax.add_patch(Rectangle((84, 0), sd, sd, facecolor=GFX + "2e",
                           edgecolor=GFX, lw=2.2, zorder=4))
    ax.text(84 + sd / 2, sd / 2, "넓이\n100", color=GFX, fontsize=12.5,
            ha="center", va="center", fontweight="bold", linespacing=1.6,
            zorder=6, family=CODE)
    ax.text(84, 21.2, "③ 평균 = 분산", color=GFX, fontsize=13.5,
            fontweight="bold")
    ax.text(84, 18.2, f"500 ÷ 5 = {var:.0f} 점²", color=DIM,
            fontsize=11.5, family=CODE)

    # ④ 한 변의 길이 = 표준편차
    ax.annotate("", xy=(84, -2.6), xytext=(84 + sd, -2.6),
                arrowprops=dict(arrowstyle="<|-|>", color=LAB, lw=1.9,
                                shrinkA=0, shrinkB=0))
    ax.text(84 + sd / 2, -3.5, "한 변 = 10점", color=LAB, fontsize=11.5,
            ha="center", va="top", fontweight="bold", family=CODE)
    ax.text(72, -9.2, f"④ 제곱근   √100 = {sd:.0f}", color=LAB,
            fontsize=13, fontweight="bold", family=CODE)

    # 오른쪽 해설
    ax.text(110, 21.2, "왜 제곱하는가", color=WARN, fontsize=12.5,
            fontweight="bold", va="top")
    ax.text(110, 18.4,
            "– 부호 제거\n"
            "– 멀리 떨어진 값일수록 크게 반영",
            color=DIM, fontsize=11, va="top", linespacing=1.9)
    ax.text(110, 9.5, "왜 다시 제곱근을 씌우는가", color=LAB, fontsize=12.5,
            fontweight="bold", va="top")
    ax.text(110, 6.8,
            "– 분산의 단위 «점²» → 뜻을 말하기 어려움\n"
            "– 제곱근 → 단위가 «점» 으로 복귀\n"
            "– 평균과 나란히 해석 가능",
            color=DIM, fontsize=11, va="top", linespacing=1.9)

    ax.set_xlim(-2, 156); ax.set_ylim(-12.5, 23)

    fig.text(0.5, 0.058,
             "표준편차 10점 = «다들 평균 75점에서 대체로 10점쯤 떨어져 있다»",
             color=FG, fontsize=15, ha="center", fontweight="bold")
    fig.text(0.5, 0.008,
             "분산 = 편차²의 평균  ·  표준편차 = √분산  ·  "
             "뜻은 «평균에서 얼마나 떨어져 있나» 하나",
             color=DIM, fontsize=12, ha="center")
    return save(fig, "d04-variance-steps", pad=0.3)


# =====================================================================
# 4. 분포의 모양 네 가지   ★ 이봉에서 평균은 빈자리를 가리킨다
# =====================================================================
def fig_distribution_shapes():
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 7.0))

    sym = _sym(2400, 172, 6)
    right = 20 + rng.lognormal(1.05, 0.62, 2400)
    left = 100 - rng.lognormal(1.75, 0.60, 2400)
    left = left[left > 20]
    bimo = np.concatenate([rng.normal(42, 6.5, 1100), rng.normal(84, 6.0, 1100)])

    panels = [
        (axes[0, 0], sym,   GFX,  "① 대칭 — 성인 남성 키",
         "평균과 중앙값 일치 → 평균 하나로 요약해도 되는 경우", "cm", 0),
        (axes[0, 1], right, WARN, "② 오른쪽 꼬리 — 한 달 앱 사용시간",
         "소수 헤비유저가 오른쪽 꼬리 형성 → 평균 > 중앙값", "시간", 1),
        (axes[1, 0], left,  VR,   "③ 왼쪽 꼬리 — 쉬운 시험 점수",
         "대부분 고득점, 소수 저득점 → 평균 < 중앙값", "점", 0),
        (axes[1, 1], bimo,  TRAP, "④ 이봉 — 두 집단 혼합",
         "봉우리 두 개 → 평균 63점 부근이 가장 드묾", "점", 0),
    ]

    for ax, s, c, title, msg, unit, dp in panels:
        style_axes(ax, grid=False)
        ax.hist(s, bins=44, color=c, alpha=0.85, zorder=3)
        m, md = s.mean(), np.median(s)
        top = ax.get_ylim()[1]
        ax.set_ylim(0, top * 1.30)
        ax.axvline(md, color=LAB, lw=2.2, zorder=5)
        ax.axvline(m, color=FG, lw=2.2, ls="--", zorder=5)
        ax.set_yticks([])
        ax.set_title(title, loc="left", color=c, fontsize=13, pad=10)
        ax.text(0.015, 0.965,
                f"평균 {m:.{dp}f}{unit}   ·   중앙값 {md:.{dp}f}{unit}",
                transform=ax.transAxes, color=FG, fontsize=11.5, va="top",
                fontweight="bold", family=CODE, zorder=8,
                bbox=dict(boxstyle="square,pad=0.22", fc=BG, ec="none"))
        ax.text(0.015, -0.20, msg, transform=ax.transAxes, color=DIM,
                fontsize=11, va="top")

    ax = axes[1, 1]
    top4 = ax.get_ylim()[1]
    ax.annotate("", xy=(bimo.mean(), top4 * 0.07),
                xytext=(bimo.mean(), top4 * 0.44),
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=1.9))
    ax.text(bimo.mean(), top4 * 0.50,
            "평균 63점\n아무도 없는 자리",
            color=TRAP, fontsize=11.5, fontweight="bold", ha="center",
            va="bottom", linespacing=1.7, zorder=9,
            bbox=dict(boxstyle="round,pad=0.28", fc=BG, ec="none"))
    ax.text(0.015, 0.875, f"표준편차 {bimo.std():.0f}점",
            transform=ax.transAxes, color=TRAP, fontsize=11.5, va="top",
            fontweight="bold", family=CODE, zorder=8,
            bbox=dict(boxstyle="square,pad=0.22", fc=BG, ec="none"))

    fig.legend(handles=[
        plt.Line2D([], [], color=FG, lw=2.2, ls="--", label="평균"),
        plt.Line2D([], [], color=LAB, lw=2.2, label="중앙값")],
        loc="upper right", bbox_to_anchor=(0.995, 1.045), ncol=2, fontsize=11.5)

    fig.subplots_adjust(hspace=0.60, wspace=0.12, top=0.9, bottom=0.15)
    fig.text(0.5, -0.025,
             f"④의 «평균 {bimo.mean():.0f}점 · 표준편차 {bimo.std():.0f}점» 어느 숫자로도 "
             "«40점대 무리와 80점대 무리» 파악 불가",
             color=TRAP, fontsize=13.5, ha="center", fontweight="bold")
    fig.text(0.5, -0.085,
             "숫자 몇 개로는 모양을 알 수 없음 → 반드시 그려서 확인",
             color=DIM, fontsize=11.5, ha="center")
    return save(fig, "d04-distribution-shapes", pad=0.4)


# =====================================================================
# 5. 앤스컴 4중주 — 숫자가 같다고 데이터가 같은 것이 아니다
# =====================================================================
def fig_anscombe():
    X = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
    X4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
    sets = [
        (X, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
         GFX,  "Ⅰ", "실제 직선 관계"),
        (X, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
         WARN, "Ⅱ", "곡선 관계에 직선 적용"),
        (X, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
         VR,   "Ⅲ", "이상치 하나로 기울기 왜곡"),
        (X4, [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89],
         TRAP, "Ⅳ", "x 값이 하나 빼고 전부 동일"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11.8, 6.9))
    line = np.array([2.5, 20.0])

    for ax, (xs, ys, c, roman, msg) in zip(axes.ravel(), sets):
        style_axes(ax)
        ax.plot(line, 3.0 + 0.5 * line, color=FAINT, lw=1.8, ls="--", zorder=3)
        ax.plot(xs, ys, "o", ms=10, color=c, mec=BG, mew=1.5, zorder=6)
        ax.set_xlim(2.5, 20.5); ax.set_ylim(2.0, 13.6)
        ax.set_xticks([5, 10, 15, 20]); ax.set_yticks([4, 8, 12])
        ax.set_title(f"{roman}.  {msg}", loc="left", color=c, fontsize=13, pad=9)

    fig.subplots_adjust(hspace=0.42, wspace=0.14, top=0.9, bottom=0.14)
    fig.text(0.5, 0.045,
             "x 평균 9.0  ·  y 평균 7.5  ·  x 분산 11.0  ·  y 분산 4.1  ·  "
             "상관계수 0.82  ·  회귀직선 y = 3.00 + 0.50x",
             color=FG, fontsize=12, ha="center", family=CODE)
    fig.text(0.5, -0.005,
             "네 데이터 모두 위 여섯 숫자 동일 — 소수점 셋째 자리에서야 차이",
             color=DIM, fontsize=11.5, ha="center")
    fig.text(0.5, -0.075,
             "요약 숫자가 같아도 다른 데이터 → 그려 보기 전에는 판단 불가",
             color=WARN, fontsize=14.5, ha="center", fontweight="bold")
    return save(fig, "d04-anscombe", pad=0.4)


# =====================================================================
# 6. 평균의 함정 — 실제로 벌어지는 일 셋
# =====================================================================
def fig_mean_trap():
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 5.0))

    # ---------------- ① 평균 수심 1m 인 강
    ax = axes[0]; clean(ax)
    x = np.linspace(0, 6, 400)
    depth = 3.0 * np.exp(-((x - 3) / 1.128) ** 2)
    ax.fill_between(x, -depth, 0, color="#14313f", zorder=2)
    ax.plot(x, -depth, color=GFX, lw=2.0, zorder=4)
    ax.plot([0, 6], [0, 0], color=GFX, lw=1.6, zorder=4)
    ax.plot([-0.2, 6.2], [-1.0, -1.0], color=WARN, lw=1.8, ls="--", zorder=5)
    ax.text(4.15, -0.90, "평균 수심 1.0m", color=WARN, fontsize=11.5,
            va="bottom", ha="right", fontweight="bold", family=CODE)

    px, foot = 3.1, -3.0
    ax.plot([px, px], [foot + 0.65, foot + 1.30], color=TRAP, lw=2.6, zorder=7)
    ax.plot([px - 0.40, px + 0.40], [foot + 1.05, foot + 1.05],
            color=TRAP, lw=2.4, zorder=7)
    ax.plot([px, px - 0.26], [foot + 0.65, foot], color=TRAP, lw=2.4, zorder=7)
    ax.plot([px, px + 0.26], [foot + 0.65, foot], color=TRAP, lw=2.4, zorder=7)
    ax.add_patch(Circle((px, foot + 1.50), 0.18, facecolor=BG, edgecolor=TRAP,
                        lw=2.4, zorder=7))
    ax.annotate("", xy=(px + 0.80, foot), xytext=(px + 0.80, foot + 1.68),
                arrowprops=dict(arrowstyle="<|-|>", color=TRAP, lw=1.5))
    ax.text(px + 0.95, foot + 0.84, "키 1.7m", color=TRAP, fontsize=11,
            va="center", fontweight="bold", family=CODE)
    ax.text(3.0, -3.62, "가운데 수심 3m", color=DIM, fontsize=10.5, ha="center")

    ax.set_xlim(-0.3, 6.3); ax.set_ylim(-4.0, 1.2)
    ax.set_title("① 평균 수심 1m 인 강", loc="left", color=TRAP,
                 fontsize=13.5, pad=10)
    ax.text(0.0, -0.11, "평균은 사실, 그래도 익사 위험",
            transform=ax.transAxes, color=DIM, fontsize=11, va="top")

    # ---------------- ② 만족도 평균 3.0점
    ax = axes[1]; style_axes(ax, grid=False)
    cnt = np.array([45, 5, 0, 5, 45])
    score = np.arange(1, 6)
    mean = float((cnt * score).sum() / cnt.sum())    # 3.00
    ax.bar(score, cnt, width=0.62, color=[TRAP, TRAP, LINE, VR, VR], zorder=4)
    for sc, c in zip(score, cnt):
        if c == 0:
            continue
        ax.text(sc, c + 1.8, f"{c}명", ha="center", color=FG, fontsize=11,
                fontweight="bold", family=CODE)
    ax.annotate("", xy=(mean, 2.0), xytext=(mean, 34),
                arrowprops=dict(arrowstyle="-|>", color=WARN, lw=2.2))
    ax.text(mean, 41, "평균 3.0점 — «보통이네»", color=WARN, fontsize=12,
            fontweight="bold", ha="center")
    ax.text(mean, 36.2, "3점을 준 사람: 0명", color=WARN, fontsize=11.5,
            ha="center", family=CODE)
    ax.set_xticks(score)
    ax.set_xticklabels(["1점\n최악", "2점", "3점", "4점", "5점\n최고"],
                       fontsize=10.5)
    ax.set_yticks([]); ax.set_ylim(0, 56)
    ax.set_title("② 만족도 평균 3.0점", loc="left", color=WARN,
                 fontsize=13.5, pad=10)
    ax.text(0.0, -0.27, "칭찬과 분노가 반반 → 평균에서는 사라짐",
            transform=ax.transAxes, color=DIM, fontsize=11, va="top")

    # ---------------- ③ 표본이 작을 때
    ax = axes[2]; clean(ax)
    rows = ((1.4, [4, 5, 5], "응답 3명", GFX),
            (0.0, [1, 4, 5, 5], "1명 추가 응답", TRAP))
    for y, data, lab, c in rows:
        ax.plot([0.72, 5.35], [y, y], color=LINE, lw=1.2, zorder=2)
        for v in data:
            ax.plot(v, y, "o", ms=14, color=c, mec=BG, mew=1.6, zorder=6)
        m = float(np.mean(data))
        ax.plot(m, y + 0.30, "v", ms=13, color=WARN, zorder=7)
        ax.text(m, y + 0.44, f"평균 {m:.2f}", color=WARN, fontsize=11.5,
                ha="center", fontweight="bold", family=CODE)
        ax.text(0.72, y + 0.52, lab, color=c, fontsize=11.5, ha="left",
                fontweight="bold")

    ax.annotate("", xy=(3.75, 0.85), xytext=(4.67, 0.85),
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=2.2))
    ax.text(4.21, 0.93, "0.92점 이동", color=TRAP, fontsize=11.5,
            ha="center", fontweight="bold", family=CODE)

    for v in range(1, 6):
        ax.text(v, -0.30, f"{v}", color=FAINT, fontsize=10.5, ha="center",
                va="top", family=CODE)
    ax.text(5.35, -0.30, "점", color=FAINT, fontsize=10.5, ha="left", va="top")

    ax.text(0.72, -0.95,
            "별점 4.7(3명) 과 4.7(3,000명) 은\n의미가 다른 숫자",
            color=FG, fontsize=12, va="top", linespacing=1.8,
            fontweight="bold")

    ax.set_xlim(0.55, 5.75); ax.set_ylim(-2.05, 2.4)
    ax.set_title("③ 표본이 작을 때", loc="left", color=TRAP,
                 fontsize=13.5, pad=10)
    ax.text(0.0, -0.11, "한 사람의 응답으로 평균이 크게 이동",
            transform=ax.transAxes, color=DIM, fontsize=11, va="top")

    fig.subplots_adjust(wspace=0.16, top=0.88, bottom=0.28)
    fig.text(0.5, -0.02,
             "평균은 요약일 뿐 · 데이터 설명으로는 부족",
             color=FG, fontsize=15, ha="center", fontweight="bold")
    fig.text(0.5, -0.085,
             "요약을 믿기 전 확인할 세 가지 — "
             "흩어진 정도 · 분포 모양 · 표본 크기",
             color=LAB, fontsize=12.5, ha="center")
    return save(fig, "d04-mean-trap", pad=0.4)


# =====================================================================
if __name__ == "__main__":
    import sys

    figs = [fig_mean_vs_median, fig_same_mean_diff_spread, fig_variance_steps,
            fig_distribution_shapes, fig_anscombe, fig_mean_trap]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
