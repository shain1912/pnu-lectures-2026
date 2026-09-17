"""
데이터리터러시 2주차 도해 — 데이터의 종류와 구조 · 수집 설계

실행:  .venv/Scripts/python.exe dataliteracy/figures/d02_figures.py [필터]
출력:  dataliteracy/figures/out/d02-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

from _style import *   # noqa: F403

rng = np.random.default_rng(7)


def _cell(ax, x, y, w, h, text, color=FG, fill=BG_SOFT, edge=LINE,
          fs=10.5, bold=False, mono=True):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, lw=1.1, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, color=color, fontsize=fs,
            ha="center", va="center", zorder=6,
            family=CODE if mono else SANS,
            fontweight="bold" if bold else "normal")


# =====================================================================
# 1. 표의 문법 — 행은 관측, 열은 변수
# =====================================================================
def fig_table_grammar():
    fig, ax = plt.subplots(figsize=(11.6, 5.0)); clean(ax)

    cols = ["학생ID", "학과", "학년", "통학시간(분)"]
    rows = [
        ["S001", "디자인", "2", "35"],
        ["S002", "경영", "1", "72"],
        ["S003", "디자인", "3", "18"],
    ]
    W, H, X0, Y0 = 2.1, 0.62, 1.6, 2.4

    for j, c in enumerate(cols):
        _cell(ax, X0 + j * W, Y0 + len(rows) * H, W, H, c,
              color=GFX, fill="#101820", edge="#1d5a66", bold=True)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            _cell(ax, X0 + j * W, Y0 + (len(rows) - 1 - i) * H, W, H, v)

    TW = W * len(cols)
    # 행 = 관측
    ax.annotate("", xy=(X0 - 0.15, Y0 + 2 * H + H / 2), xytext=(X0 - 1.35, Y0 + 2 * H + H / 2),
                arrowprops=dict(arrowstyle="-|>", color=LAB, lw=2.0))
    ax.text(X0 - 1.45, Y0 + 2 * H + H / 2, "행 = 관측 하나", color=LAB, fontsize=12.5,
            ha="right", va="center", fontweight="bold")
    # 열 = 변수
    ax.annotate("", xy=(X0 + 3 * W + W / 2, Y0 + len(rows) * H + H + 0.15),
                xytext=(X0 + 3 * W + W / 2, Y0 + len(rows) * H + H + 1.0),
                arrowprops=dict(arrowstyle="-|>", color=VR, lw=2.0))
    ax.text(X0 + 3 * W + W / 2, Y0 + len(rows) * H + H + 1.1, "열 = 변수 하나",
            color=VR, fontsize=12.5, ha="center", va="bottom", fontweight="bold")

    ax.text(X0, Y0 - 0.75,
            "관측 단위 (unit of observation) : «학생 한 명»",
            color=FG, fontsize=13, fontweight="bold")
    ax.text(X0, Y0 - 1.35,
            "관측 단위 = 수집 설계에서 가장 먼저 정할 항목\n"
            "학생 · 수업 · 학기 중 무엇이 한 줄인가 → 어긋나면 이후 분석 전체 흔들림",
            color=DIM, fontsize=11.5, linespacing=1.9, va="top")

    ax.set_xlim(-1.3, X0 + TW + 1.6); ax.set_ylim(-0.5, Y0 + len(rows) * H + H + 2.1)
    ax.set_title("표의 문법 — 행과 열", loc="left", pad=14, fontsize=15)
    return save(fig, "d02-table-grammar")


# =====================================================================
# 2. 변수의 척도 — 평균을 낼 수 있는가
# =====================================================================
def fig_scales():
    fig, ax = plt.subplots(figsize=(12.0, 4.8)); clean(ax)

    items = [
        ("명목 Nominal", "학과, 성별, 지역", "같다/다르다", "최빈값", TRAP, "평균 금지"),
        ("순서 Ordinal", "학년, 만족도 1~5", "순서 있음", "중앙값", WARN, "평균 주의"),
        ("구간 Interval", "온도(℃), 연도", "간격 일정", "평균 가능", GFX, "0이 '없음'은 아님"),
        ("비율 Ratio", "통학시간, 매출", "절대 0 존재", "모든 연산", LAB, "배수 비교 가능"),
    ]
    W = 2.85
    for i, (name, ex, meaning, stat, c, note) in enumerate(items):
        x = i * (W + 0.18)
        ax.add_patch(FancyBboxPatch((x, 0.6), W, 2.7,
                                    boxstyle="round,pad=0.03,rounding_size=0.12",
                                    facecolor=BG_SOFT, edgecolor=c, lw=1.9, zorder=3))
        ax.text(x + W / 2, 2.95, name, color=c, fontsize=12.5, fontweight="bold",
                ha="center", zorder=6)
        ax.text(x + W / 2, 2.45, ex, color=FG, fontsize=10.5, ha="center", zorder=6)
        ax.text(x + W / 2, 1.95, meaning, color=DIM, fontsize=10, ha="center", zorder=6)
        ax.text(x + W / 2, 1.45, stat, color=c, fontsize=11, ha="center",
                fontweight="bold", zorder=6, family=CODE)
        ax.text(x + W / 2, 0.9, note, color=DIM, fontsize=9.5, ha="center", zorder=6)

    ax.annotate("", xy=(4 * (W + 0.18) - 0.3, 0.15), xytext=(0.1, 0.15),
                arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.8))
    ax.text(4 * (W + 0.18) / 2, -0.25, "가능한 연산 증가",
            color=DIM, fontsize=11.5, ha="center")

    ax.text(0, 3.75,
            "«학과의 평균» 계산은 가능하나 의미 없음",
            color=TRAP, fontsize=13, fontweight="bold")
    ax.text(0, -1.0,
            "AI는 척도를 따지지 않고 계산  →  척도 판단은 사람의 몫",
            color=FG, fontsize=12.5)

    ax.set_xlim(-0.3, 4 * (W + 0.18) + 0.2); ax.set_ylim(-1.5, 4.2)
    ax.set_title("변수의 네 가지 척도", loc="left", pad=12, fontsize=15)
    return save(fig, "d02-scales")


# =====================================================================
# 3. 지저분한 표 vs 깔끔한 표 (tidy)
# =====================================================================
def fig_tidy():
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.6))

    # --- messy : 열 이름이 값이다
    ax = axes[0]; clean(ax)
    W, H, X0, Y0 = 1.55, 0.6, 0.2, 1.4
    head = ["학과", "2024", "2025", "2026"]
    body = [["디자인", "41", "45", "52"], ["경영", "88", "83", "80"]]
    for j, c in enumerate(head):
        _cell(ax, X0 + j * W, Y0 + len(body) * H, W, H, c,
              color=TRAP, fill="#1a1113", edge="#6e2a24", bold=True)
    for i, r in enumerate(body):
        for j, v in enumerate(r):
            _cell(ax, X0 + j * W, Y0 + (len(body) - 1 - i) * H, W, H, v)
    ax.text(X0, Y0 - 0.6, "연도가 «열 이름» 으로 들어간 구조", color=TRAP, fontsize=12,
            fontweight="bold")
    ax.text(X0, Y0 - 1.15, "그래프마다 코드 수정 필요\n"
                           "2027년 자료 추가 시 열 구조 변경",
            color=DIM, fontsize=10.5, linespacing=1.8, va="top")
    ax.set_xlim(0, 4 * W + 0.4); ax.set_ylim(-0.6, Y0 + len(body) * H + H + 0.9)
    ax.set_title("정리 전", loc="left", color=TRAP, fontsize=13.5, pad=10)

    # --- tidy
    ax = axes[1]; clean(ax)
    W2 = 1.55
    head2 = ["학과", "연도", "인원"]
    body2 = [["디자인", "2024", "41"], ["디자인", "2025", "45"],
             ["경영", "2024", "88"], ["경영", "2025", "83"]]
    Y1 = 0.55
    for j, c in enumerate(head2):
        _cell(ax, X0 + j * W2, Y1 + len(body2) * H, W2, H, c,
              color=LAB, fill="#101a10", edge="#3c5220", bold=True)
    for i, r in enumerate(body2):
        for j, v in enumerate(r):
            _cell(ax, X0 + j * W2, Y1 + (len(body2) - 1 - i) * H, W2, H, v)
    ax.text(X0, Y1 - 0.5, "한 행 = 한 관측, 한 열 = 한 변수", color=LAB, fontsize=12,
            fontweight="bold")
    ax.text(X0, Y1 - 1.05, "행만 늘어나고 구조는 그대로\n"
                           "대부분의 분석 도구가 요구하는 형태",
            color=DIM, fontsize=10.5, linespacing=1.8, va="top")
    ax.set_xlim(0, 4 * W + 0.4); ax.set_ylim(-0.6, Y1 + len(body2) * H + H + 0.9)
    ax.set_title("정리 후 (tidy)", loc="left", color=LAB, fontsize=13.5, pad=10)

    fig.text(0.5, -0.10,
             "정제의 목표 : «기계가 읽을 수 있는 표»",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")
    return save(fig, "d02-tidy", pad=0.36)


# =====================================================================
# 4. 생존자 편향 — 돌아온 비행기에만 구멍이 있다
# =====================================================================
def fig_survivorship():
    fig, ax = plt.subplots(figsize=(11.0, 4.8)); clean(ax)

    # 아주 단순한 비행기 실루엣
    body = Rectangle((3.6, 1.5), 3.6, 0.55, facecolor="#171b25", edgecolor=DIM, lw=1.6)
    ax.add_patch(body)
    ax.add_patch(Rectangle((4.9, 0.55), 0.75, 2.5, facecolor="#171b25",
                           edgecolor=DIM, lw=1.6))
    ax.add_patch(Rectangle((3.35, 1.15), 0.5, 1.25, facecolor="#171b25",
                           edgecolor=DIM, lw=1.6))

    hits = [(4.4, 1.75), (5.2, 1.9), (6.0, 1.65), (5.05, 2.55), (5.5, 0.9),
            (6.6, 1.8), (4.9, 1.6), (5.6, 2.3)]
    for x, y in hits:
        ax.plot(x, y, "o", color=GFX, ms=9, alpha=0.85, zorder=6)

    ax.plot(3.55, 1.78, "o", color=TRAP, ms=13, zorder=7)
    ax.plot(7.0, 1.78, "o", color=TRAP, ms=13, zorder=7)
    ax.annotate("구멍 없는 부위", xy=(3.55, 1.78), xytext=(1.3, 3.3),
                color=TRAP, fontsize=12.5, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=1.8))

    ax.text(0.2, 0.15,
            "돌아온 비행기의 구멍 자리를 보강해야 하는가?", color=FG, fontsize=13.5,
            fontweight="bold")
    ax.text(0.2, -0.5,
            "구멍 없는 부위에 맞은 비행기 → «돌아오지 못한» 비행기\n"
            "손에 쥔 데이터 = 살아남은 비행기의 기록뿐",
            color=TRAP, fontsize=12.5, linespacing=1.9, va="top")
    ax.text(0.2, -2.25,
            "이 데이터에 누가 빠져 있는가?  —  분석 전 필수 질문",
            color=LAB, fontsize=12.5, fontweight="bold")

    ax.set_xlim(0, 11.2); ax.set_ylim(-2.6, 4.0)
    ax.set_title("생존자 편향", loc="left", pad=12, fontsize=15)
    return save(fig, "d02-survivorship")


# =====================================================================
# 5. 표본 편향 — 누구에게 물었는가
# =====================================================================
def fig_sampling_bias():
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.6))

    pop = rng.normal(50, 18, 4000)
    pop = pop[(pop > 0) & (pop < 100)]

    # 공정한 표본
    ax = axes[0]; style_axes(ax)
    fair = rng.choice(pop, 300, replace=False)
    ax.hist(pop, bins=30, color=DIM, alpha=0.25, label="모집단")
    ax.hist(fair, bins=30, color=LAB, alpha=0.75,
            weights=np.ones_like(fair) * len(pop) / len(fair), label="표본")
    ax.axvline(pop.mean(), color=DIM, lw=2, ls=(0, (4, 3)))
    ax.axvline(fair.mean(), color=LAB, lw=2.4)
    ax.set_title(f"무작위 추출   표본평균 {fair.mean():.1f}", loc="left",
                 color=LAB, fontsize=13, pad=10)
    ax.set_yticks([]); ax.legend(loc="upper right", fontsize=9)

    # 편향된 표본 — 값이 큰 쪽이 더 잘 응답
    ax = axes[1]; style_axes(ax)
    p = (pop - pop.min()) ** 2
    p = p / p.sum()
    biased = rng.choice(pop, 300, replace=False, p=p)
    ax.hist(pop, bins=30, color=DIM, alpha=0.25, label="모집단")
    ax.hist(biased, bins=30, color=TRAP, alpha=0.75,
            weights=np.ones_like(biased) * len(pop) / len(biased), label="표본")
    ax.axvline(pop.mean(), color=DIM, lw=2, ls=(0, (4, 3)))
    ax.axvline(biased.mean(), color=TRAP, lw=2.4)
    ax.set_title(f"자발적 응답만 수집   표본평균 {biased.mean():.1f}", loc="left",
                 color=TRAP, fontsize=13, pad=10)
    ax.set_yticks([]); ax.legend(loc="upper right", fontsize=9)

    fig.text(0.5, -0.04,
             f"모집단 평균은 둘 다 {pop.mean():.1f}  ·  "
             "표본을 300 → 3만으로 늘려도 오른쪽은 틀린 값 · 정밀해질 뿐 정확해지지 않음",
             color=FG, fontsize=13, ha="center", fontweight="bold")
    return save(fig, "d02-sampling-bias", pad=0.36)


# =====================================================================
# 6. 수집 설계는 거꾸로 간다  ★
# =====================================================================
def fig_collection_design():
    fig, ax = plt.subplots(figsize=(12.2, 4.8)); clean(ax)

    steps = [
        ("① 질문", "무엇을 알고 싶은가", GFX,
         "«우리 학과 학생은\n통학에 얼마나 쓰나»"),
        ("② 조작적 정의", "무엇으로 어떻게 잴 것인가", VR,
         "«통학시간» =\n집 출발~강의실 도착 분"),
        ("③ 관측 단위·변수", "무엇을 한 줄로 볼 것인가", LAB,
         "행 = 학생 1명\n열 = 학과·학년·분"),
        ("④ 출처와 한계", "어디서 얻고 무엇이 빠지는가", WARN,
         "설문 / 자취생은\n어떻게 잡을 것인가"),
    ]
    W, H = 2.7, 1.9
    gap = 0.42
    for i, (t, sub, c, ex) in enumerate(steps):
        x = i * (W + gap)
        ax.add_patch(FancyBboxPatch((x, 1.5), W, H,
                                    boxstyle="round,pad=0.03,rounding_size=0.12",
                                    facecolor=BG_SOFT, edgecolor=c, lw=1.9, zorder=4))
        ax.text(x + W / 2, 3.02, t, color=c, fontsize=13, fontweight="bold",
                ha="center", va="center", zorder=6)
        ax.text(x + W / 2, 2.62, sub, color=FG, fontsize=10, ha="center",
                va="center", zorder=6)
        ax.text(x + W / 2, 1.95, ex, color=DIM, fontsize=9.5, ha="center",
                va="center", zorder=6, linespacing=1.7, family=CODE)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + W + gap - 0.06, 2.45), xytext=(x + W + 0.06, 2.45),
                        arrowprops=dict(arrowstyle="-|>", color=LINE, lw=2.0))

    total = 4 * W + 3 * gap
    ax.annotate("", xy=(0.1, 1.05), xytext=(total - 0.1, 1.05),
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=2.2))
    ax.text(total / 2, 0.72, "흔한 실수 — 데이터부터 뒤지기 (역방향)",
            color=TRAP, fontsize=12, ha="center")

    ax.text(0, 3.85, "데이터를 찾기 전에 질문부터 확정",
            color=FG, fontsize=14, fontweight="bold")
    ax.text(0, 0.05,
            "질문 없이 모은 데이터 → "
            "숫자를 본 뒤 이야기를 끼워 맞추기 쉬움",
            color=DIM, fontsize=12)

    ax.set_xlim(-0.3, total + 0.3); ax.set_ylim(-0.4, 4.4)
    ax.set_title("수집 설계", loc="left", pad=12, fontsize=15)
    return save(fig, "d02-collection-design")


# =====================================================================
if __name__ == "__main__":
    import sys
    figs = [fig_table_grammar, fig_scales, fig_tidy, fig_survivorship,
            fig_sampling_bias, fig_collection_design]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
