"""
데이터리터러시 5주차 도해 — z-점수와 표준화
기준이 다른 숫자의 비교, 그리고 이상치 기준의 선택

실행:  cd dataliteracy/figures && ../../.venv/Scripts/python.exe d05_figures.py [필터]
출력:  dataliteracy/figures/out/d05-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from _style import *   # noqa: F403

rng = np.random.default_rng(505)


# --------------------------------------------------------------- 헬퍼
def _bell(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


def _sym(n, mu, sd):
    """평균과 표준편차가 정확히 지정값인 좌우대칭 표본."""
    z = rng.normal(0, 1, n // 2)
    z = (z - z.mean()) / z.std()
    z = np.concatenate([z, -z])
    return mu + z * sd


def _span(ax, x0, x1, y, color, text, fs=11, up=0.0, lw=1.7):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<|-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + up, text, color=color, fontsize=fs,
            ha="center", va="bottom", fontweight="bold", family=CODE)


def _chip(ax, x, y, text, color, fs=12.5, pad=0.5):
    ax.text(x, y, text, color=color, fontsize=fs, fontweight="bold",
            ha="center", va="center", zorder=20, family=CODE,
            bbox=dict(boxstyle=f"round,pad={pad}", fc=BG_SOFT, ec=color, lw=1.4))


def _strip(ax, vals, flagged, y=0.0, jitter=None, r=7.0):
    """한 줄짜리 점 그림. flagged 는 불리언 배열."""
    j = np.zeros_like(vals) if jitter is None else jitter
    ax.plot(vals[~flagged], j[~flagged], "o", ms=r, color=GFX,
            mec=BG, mew=1.2, zorder=5)
    ax.plot(vals[flagged], j[flagged], "o", ms=r + 2.2, color=TRAP,
            mec=BG, mew=1.2, zorder=6)


# =====================================================================
# 1. z-점수 공식의 뜻
# =====================================================================
def fig_zscore_formula():
    mu, sd, raw = 60.0, 10.0, 80.0
    fig, axes = plt.subplots(2, 1, figsize=(12.6, 5.9),
                             gridspec_kw=dict(height_ratios=[1.0, 0.62]))

    # ---------------- 위 : 자 위에 놓인 원점수
    ax = axes[0]; style_axes(ax, grid=False)
    x = np.linspace(20, 100, 500)
    ax.plot(x, _bell(x, mu, sd), color=GFX, lw=2.4, zorder=5)
    ax.fill_between(x, 0, _bell(x, mu, sd), color=GFX, alpha=0.10, zorder=2)

    ymax = _bell(mu, mu, sd)
    for k in (-3, -2, -1, 0, 1, 2, 3):
        xv = mu + k * sd
        ax.plot([xv, xv], [0, ymax * 1.02], color=LINE, lw=1.1,
                ls=(0, (3, 4)), zorder=3)
        ax.text(xv, -ymax * 0.085, f"{int(xv)}", color=FAINT, fontsize=10.5,
                ha="center", va="top", family=CODE)
        ax.text(xv, -ymax * 0.26, f"{k:+d}칸" if k else "0칸",
                color=DIM if k else FG, fontsize=10.5, ha="center", va="top",
                family=CODE, fontweight="bold" if k == 2 else "normal")

    ax.plot([mu, mu], [0, ymax], color=FG, lw=2.6, zorder=6)
    ax.text(mu, ymax * 1.09, "평균 60", color=FG, fontsize=12.5, ha="center",
            fontweight="bold", family=CODE)

    ax.plot([raw, raw], [0, ymax * 0.72], color=WARN, lw=3.0, zorder=7)
    ax.plot(raw, 0, "o", ms=11, color=WARN, mec=BG, mew=1.5, zorder=8)
    ax.text(raw, ymax * 0.80, "원점수 80", color=WARN, fontsize=12.5,
            ha="center", fontweight="bold", family=CODE)

    _span(ax, mu, raw, ymax * 0.46, WARN, "편차 +20점", up=ymax * 0.03)
    _span(ax, mu, mu + sd, ymax * 0.20, LAB, "표준편차 10점", fs=10.5,
          up=ymax * 0.03)

    ax.set_xlim(22, 100); ax.set_ylim(-ymax * 0.42, ymax * 1.30)
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_title("수학 점수 분포 · 평균 60점 · 표준편차 10점", loc="left",
                 pad=12, fontsize=14)

    # ---------------- 아래 : 공식 분해
    ax = axes[1]; clean(ax)
    ax.set_xlim(0, 12); ax.set_ylim(0, 3.1)

    ax.text(0.15, 2.05, "z  =", color=FG, fontsize=22, family=CODE,
            fontweight="bold", va="center")
    _chip(ax, 2.05, 2.05, " 80 ", WARN, fs=20, pad=0.42)
    ax.text(2.95, 2.05, "−", color=DIM, fontsize=20, ha="center", va="center",
            family=CODE)
    _chip(ax, 3.85, 2.05, " 60 ", FG, fs=20, pad=0.42)
    ax.text(4.85, 2.05, "÷", color=DIM, fontsize=20, ha="center", va="center",
            family=CODE)
    _chip(ax, 5.80, 2.05, " 10 ", LAB, fs=20, pad=0.42)
    ax.text(6.75, 2.05, "=", color=DIM, fontsize=20, ha="center", va="center",
            family=CODE)
    _chip(ax, 7.85, 2.05, " +2.0 ", GFX, fs=20, pad=0.42)

    for x0, label, color in ((2.05, "원점수", WARN), (3.85, "평균", FG),
                             (5.80, "표준편차", LAB), (7.85, "z-점수", GFX)):
        ax.text(x0, 1.18, label, color=color, fontsize=12, ha="center",
                va="center", fontweight="bold")

    ax.text(9.35, 2.05, "평균에서\n표준편차 2칸 위", color=GFX, fontsize=12.5,
            va="center", linespacing=1.7, fontweight="bold")
    ax.text(0.15, 0.42,
            "단위 소거 → 점·원·분·kg 처럼 단위가 다른 숫자끼리 비교 가능",
            color=DIM, fontsize=12.5, va="center")

    fig.subplots_adjust(hspace=0.30, top=0.92, bottom=0.04)
    return save(fig, "d05-zscore-formula", pad=0.36)


# =====================================================================
# 2. 같은 80점, 다른 의미
# =====================================================================
def fig_two_subjects():
    data = [("국어", 85.0, 5.0, VR, "−1.0", "하위 약 16%"),
            ("수학", 60.0, 10.0, GFX, "+2.0", "상위 약 2.3%")]
    raw = 80.0

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.0))
    for ax, (name, mu, sd, color, zt, pct) in zip(axes, data):
        style_axes(ax, grid=False)
        x = np.linspace(mu - 4.2 * sd, mu + 4.2 * sd, 600)
        y = _bell(x, mu, sd)
        ax.plot(x, y, color=color, lw=2.4, zorder=5)
        ax.fill_between(x, 0, y, color=color, alpha=0.10, zorder=2)

        left = x <= raw
        ax.fill_between(x[left], 0, y[left], color=color, alpha=0.30, zorder=3)

        ymax = y.max()
        ax.plot([mu, mu], [0, ymax], color=FG, lw=2.2, zorder=6)
        ax.text(mu, ymax * 1.10, f"평균 {int(mu)}", color=FG, fontsize=12,
                ha="center", fontweight="bold", family=CODE)

        ax.plot([raw, raw], [0, ymax * 0.84], color=WARN, lw=3.0, zorder=7)
        ax.plot(raw, 0, "o", ms=11, color=WARN, mec=BG, mew=1.5, zorder=8)
        ax.text(raw, ymax * 0.90, "80점", color=WARN, fontsize=13,
                ha="center", fontweight="bold", family=CODE)

        _chip(ax, mu, -ymax * 0.30, f" z = {zt} ", color, fs=15, pad=0.45)
        ax.text(mu, -ymax * 0.56, pct, color=DIM, fontsize=11.5, ha="center",
                va="center")

        ax.set_xlim(mu - 4.2 * sd, mu + 4.2 * sd)
        ax.set_ylim(-ymax * 0.72, ymax * 1.32)
        ax.set_yticks([])
        ticks = [mu + k * sd for k in (-2, 0, 2)]
        ax.set_xticks(ticks)
        ax.set_xticklabels([f"{int(t)}" for t in ticks], fontsize=11)
        ax.set_title(f"{name} · 평균 {int(mu)}점 · 표준편차 {int(sd)}점",
                     loc="left", color=color, fontsize=13.5, pad=12)

    fig.subplots_adjust(wspace=0.18, top=0.86, bottom=0.18)
    fig.text(0.5, 0.055,
             "같은 80점 · 국어는 평균 아래, 수학은 상위권",
             color=FG, fontsize=15, ha="center", fontweight="bold")
    fig.text(0.5, -0.025,
             "원점수만으로는 비교 불가 → 평균과 표준편차를 함께 넣어야 "
             "같은 잣대 위에 놓임",
             color=DIM, fontsize=12, ha="center")
    return save(fig, "d05-two-subjects", pad=0.4)


# =====================================================================
# 3. 68 - 95 - 99.7
# =====================================================================
def fig_normal_68_95():
    fig, ax = plt.subplots(figsize=(12.4, 5.2))
    style_axes(ax, grid=False)

    x = np.linspace(-4, 4, 800)
    y = _bell(x, 0, 1)
    ax.plot(x, y, color=GFX, lw=2.6, zorder=6)

    bands = [(3, "#1b2535", "99.7%", TRAP), (2, "#1d3340", "95%", WARN),
             (1, "#1f4350", "68%", LAB)]
    for k, fill, label, color in bands:
        m = np.abs(x) <= k
        ax.fill_between(x[m], 0, y[m], color=fill, zorder=3)

    ymax = y.max()
    for k, _, label, color in bands:
        ax.plot([-k, -k], [0, _bell(-k, 0, 1)], color=color, lw=1.8, zorder=5)
        ax.plot([k, k], [0, _bell(k, 0, 1)], color=color, lw=1.8, zorder=5)

    _span(ax, -1, 1, ymax * 0.47, LAB, "±1칸  68%", fs=12, up=0.006)
    _span(ax, -2, 2, ymax * 0.24, WARN, "±2칸  95%", fs=12, up=0.006)
    _span(ax, -3, 3, ymax * 0.05, TRAP, "±3칸  99.7%", fs=12, up=0.006)

    ax.text(3.08, _bell(3, 0, 1) + 0.012, "바깥 0.3%\n= 1,000명 중 3명",
            color=TRAP, fontsize=11, va="bottom", linespacing=1.6,
            fontweight="bold")

    ax.set_xlim(-4.1, 4.1); ax.set_ylim(-0.085, ymax * 1.26)
    ax.set_yticks([])
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_xticklabels(["z = −3", "−2", "−1", "0", "+1", "+2", "+3"],
                       fontsize=11.5)
    ax.set_title("표준화한 값이 놓이는 자리 — 경험 규칙", loc="left",
                 pad=14, fontsize=15)

    fig.subplots_adjust(top=0.88, bottom=0.22)
    fig.text(0.5, 0.045,
             "성립 조건 : 좌우 대칭 종형 분포",
             color=WARN, fontsize=13.5, ha="center", fontweight="bold")
    fig.text(0.5, -0.03,
             "치우친 분포·이봉 분포에서는 이 비율 자체가 성립하지 않음 → "
             "히스토그램 확인이 먼저",
             color=DIM, fontsize=12, ha="center")
    return save(fig, "d05-normal-68-95", pad=0.4)


# =====================================================================
# 4. 이상치 기준 세 가지
# =====================================================================
def fig_outlier_rules():
    base = np.array([
        8, 10, 12, 13, 15, 15, 18, 20, 20, 22, 24, 25, 25, 27, 28, 30, 30,
        32, 33, 35, 35, 38, 40, 42, 45, 45, 48, 50, 52, 55, 58, 60, 62, 65,
        70, 72, 78, 85, 95, 110, 125, 150, 170, 240, 300,
    ], dtype=float)
    jit = (rng.random(base.size) - 0.5) * 0.5

    mu, sd = base.mean(), base.std(ddof=1)
    q1, q3 = np.percentile(base, [25, 75])
    iqr = q3 - q1
    fences = [
        ("z ±3", mu + 3 * sd, base > mu + 3 * sd, GFX,
         f"평균 {mu:.0f} + 3 × 표준편차 {sd:.0f} = {mu + 3 * sd:.0f}분"),
        ("IQR 1.5배", q3 + 1.5 * iqr, base > q3 + 1.5 * iqr, LAB,
         f"3사분위 {q3:.0f} + 1.5 × IQR {iqr:.0f} = {q3 + 1.5 * iqr:.0f}분"),
        ("도메인 규칙", 180.0, base > 180, VR,
         "편도 통학 180분 초과 = 현실성 점검 대상"),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(12.8, 6.2), sharex=True)
    for ax, (name, fence, flag, color, desc) in zip(axes, fences):
        style_axes(ax, grid=False)
        _strip(ax, base, flag, jitter=jit, r=6.4)
        ax.axvline(fence, color=color, lw=2.4, zorder=7)
        ax.text(fence + 5, 0.72, f"{name} 기준선 {fence:.0f}분", color=color,
                fontsize=12, va="center", fontweight="bold", family=CODE)
        ax.text(5, -0.74, desc, color=DIM, fontsize=11, va="center")
        _chip(ax, 318, 0.0, f" {int(flag.sum())}개 ", color, fs=14, pad=0.42)
        ax.set_xlim(-8, 345); ax.set_ylim(-1.05, 1.05)
        ax.set_yticks([])

    axes[0].set_title("같은 데이터 · 기준에 따라 달라지는 이상치 "
                      "(편도 통학시간 45명)", loc="left", pad=14, fontsize=14.5)
    axes[2].set_xticks([0, 60, 120, 180, 240, 300])
    axes[2].set_xticklabels(["0", "60", "120", "180", "240", "300"],
                            fontsize=11)
    axes[2].set_xlabel("통학시간 (분)", labelpad=8, fontsize=11.5)

    fig.subplots_adjust(hspace=0.42, top=0.90, bottom=0.17)
    fig.text(0.5, 0.012,
             "세 기준이 서로 다른 답을 제시 → 기준 선택이 곧 결론 선택",
             color=FG, fontsize=14, ha="center", fontweight="bold")
    return save(fig, "d05-outlier-rules", pad=0.4)


# =====================================================================
# 5. 치우친 분포에서 무너지는 z 기준
# =====================================================================
def fig_skew_breaks_z():
    sym = _sym(60, 50, 9)
    sym = np.append(sym, 96.0)                      # 진짜 극단값 1개

    core = _sym(54, 30, 7)
    tail = np.array([120, 150, 190, 260, 340, 420], dtype=float)
    skew = np.concatenate([core, tail])

    sets = [("좌우 대칭 분포", sym, GFX), ("오른쪽으로 늘어진 분포", skew, TRAP)]
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.4))

    for ax, (name, v, color) in zip(axes, sets):
        style_axes(ax, grid=False)
        mu, sd = v.mean(), v.std(ddof=1)
        q1, q3 = np.percentile(v, [25, 75])
        iqr = q3 - q1
        zf, if_ = mu + 3 * sd, q3 + 1.5 * iqr
        z_hit, i_hit = int((v > zf).sum()), int((v > if_).sum())

        hi = max(v.max(), zf) * 1.12
        bins = np.linspace(0, hi, 34)
        ax.hist(v, bins=bins, color=color, alpha=0.30, zorder=3)
        counts, _ = np.histogram(v, bins=bins)
        top = counts.max()

        jit = (rng.random(v.size) - 0.5) * (top * 0.16)
        ax.plot(v, -top * 0.22 + jit, "o", ms=5.6, color=color, mec=BG,
                mew=1.0, zorder=5)

        lo_y = -top * 0.78
        ax.plot([mu, mu], [lo_y, top * 1.02], color=FG, lw=2.0, zorder=6)
        ax.text(mu, top * 1.07, f"평균 {mu:.0f}", color=FG, fontsize=11.5,
                ha="center", va="bottom", fontweight="bold", family=CODE)

        ax.plot([zf, zf], [lo_y, top * 1.52], color=WARN, lw=2.6, zorder=7)
        ax.text(zf, top * 1.57, f"z +3 기준선 {zf:.0f}", color=WARN,
                fontsize=11.5, ha="center", va="bottom",
                fontweight="bold", family=CODE)

        ax.plot([if_, if_], [lo_y, top * 1.02], color=LAB, lw=2.2,
                ls=(0, (5, 4)), zorder=7)
        ax.text(if_, -top * 0.62, f"IQR 기준선 {if_:.0f}", color=LAB,
                fontsize=11, ha="center", va="center", fontweight="bold",
                family=CODE)

        cc = WARN if z_hit < i_hit else DIM
        ax.text(hi * 0.02, top * 1.90,
                f" 탐지 — z 기준 {z_hit}개 · IQR 기준 {i_hit}개 ",
                color=cc, fontsize=12.5, fontweight="bold", family=CODE,
                ha="left", va="center", zorder=20,
                bbox=dict(boxstyle="round,pad=0.45", fc=BG_SOFT, ec=cc, lw=1.4))

        ax.set_xlim(-hi * 0.03, hi * 1.04)
        ax.set_ylim(-top * 1.15, top * 2.08)
        ax.set_yticks([])
        ax.set_title(name, loc="left", color=color, fontsize=13.5, pad=14)

    axes[0].text(0.02, 0.035, "극단값 1개 · z 기준이 그대로 탐지",
                 transform=axes[0].transAxes, color=DIM, fontsize=11.5,
                 va="center")
    axes[1].text(0.02, 0.035,
                 "극단값 6개가 표준편차를 키움 → 기준선이 밀려 4개 미탐지",
                 transform=axes[1].transAxes, color=TRAP, fontsize=11.5,
                 va="center", fontweight="bold")

    fig.subplots_adjust(wspace=0.16, top=0.86, bottom=0.17)
    fig.text(0.5, 0.03,
             "극단값이 많을수록 z 기준은 극단값을 놓침",
             color=FG, fontsize=15, ha="center", fontweight="bold")
    fig.text(0.5, -0.05,
             "평균·표준편차 자체가 극단값에 끌려가기 때문 · "
             "치우친 분포에서는 IQR 기준이 안정적",
             color=DIM, fontsize=12, ha="center")
    return save(fig, "d05-skew-breaks-z", pad=0.4)


# =====================================================================
if __name__ == "__main__":
    import sys

    figs = [fig_zscore_formula, fig_two_subjects, fig_normal_68_95,
            fig_outlier_rules, fig_skew_breaks_z]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
