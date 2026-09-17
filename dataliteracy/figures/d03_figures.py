"""
데이터리터러시 3주차 도해 — 데이터 정제와 전처리

실행:  .venv/Scripts/python.exe dataliteracy/figures/d03_figures.py [필터]
출력:  dataliteracy/figures/out/d03-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from _style import *   # noqa: F403

rng = np.random.default_rng(11)


def _cell(ax, x, y, w, h, text, color=FG, fill=BG_SOFT, edge=LINE, fs=10, bold=False):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, lw=1.1, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, color=color, fontsize=fs, ha="center",
            va="center", zorder=6, family=CODE,
            fontweight="bold" if bold else "normal")


# =====================================================================
# 1. 실제 데이터는 이렇게 생겼다
# =====================================================================
def fig_dirty_data():
    fig, ax = plt.subplots(figsize=(12.2, 5.2)); clean(ax)

    head = ["지역", "인구", "면적", "조사일"]
    body = [
        ["서울특별시", "9,411,440", "605.2", "2026-01-01"],
        ["서울시",     "9411440",   "605.2", "2026.01.01"],
        ["부산",       "-",         "770.1", "2026-01-01"],
        ["대구",       "2,374,960", "미상",  ""],
        ["ë¶€ì‚°",     "3,349,016", "770.1", "26/1/1"],
    ]
    W, H, X0, Y0 = 2.5, 0.6, 0.3, 1.5
    for j, c in enumerate(head):
        _cell(ax, X0 + j * W, Y0 + len(body) * H, W, H, c,
              color=GFX, fill="#101820", edge="#1d5a66", bold=True)
    for i, r in enumerate(body):
        for j, v in enumerate(r):
            _cell(ax, X0 + j * W, Y0 + (len(body) - 1 - i) * H, W, H, v)

    TW = W * len(head)
    notes = [
        (4, "같은 도시가 두 이름 — 중복인가 다른 관측인가"),
        (3, "천 단위 쉼표 → 숫자 대신 «문자» 로 인식"),
        (2, "빈칸을 «-» 로 표기"),
        (1, "«미상» 과 빈칸 — 뜻이 같은가 다른가"),
        (0, "인코딩 깨짐 (CP949 를 UTF-8 로 읽음)"),
    ]
    for i, txt in notes:
        y = Y0 + i * H + H / 2
        ax.annotate("", xy=(X0 + TW + 0.12, y), xytext=(X0 + TW + 0.75, y),
                    arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=1.4))
        ax.text(X0 + TW + 0.85, y, txt, color=TRAP, fontsize=10.5, va="center")

    ax.text(X0, Y0 - 0.6, "작은 표 하나에 이미 문제 다섯 가지",
            color=FG, fontsize=13.5, fontweight="bold")
    ax.text(X0, Y0 - 1.2,
            "내려받은 공공데이터의 흔한 상태  ·  "
            "분석 시간의 절반 이상이 정제에 소요",
            color=DIM, fontsize=12)

    ax.set_xlim(0, X0 + TW + 6.6); ax.set_ylim(-0.5, Y0 + len(body) * H + H + 0.8)
    ax.set_title("현실의 데이터", loc="left", pad=14, fontsize=15)
    return save(fig, "d03-dirty-data")


# =====================================================================
# 2. 빈칸에도 이유가 있다
# =====================================================================
def fig_missing_why():
    fig, ax = plt.subplots(figsize=(12.0, 4.6)); clean(ax)

    kinds = [
        ("우연한 결측", "커피에 젖은 설문지 한 장",
         "삭제해도 대체로 안전", LAB),
        ("다른 변수에 따른 결측", "고학년일수록 소득 문항 건너뜀",
         "학년 정보로 보완 가능", WARN),
        ("값 자체가 원인인 결측", "고소득자일수록 소득 미기재",
         "삭제 시 결론 전체 왜곡", TRAP),
    ]
    W = 3.9
    for i, (t, ex, act, c) in enumerate(kinds):
        x = i * (W + 0.25)
        ax.add_patch(FancyBboxPatch((x, 0.7), W, 2.5,
                                    boxstyle="round,pad=0.03,rounding_size=0.12",
                                    facecolor=BG_SOFT, edgecolor=c, lw=1.9, zorder=3))
        ax.text(x + W / 2, 2.85, t, color=c, fontsize=13, fontweight="bold",
                ha="center", zorder=6)
        ax.text(x + W / 2, 2.2, ex, color=FG, fontsize=10.5, ha="center",
                zorder=6, linespacing=1.7)
        ax.text(x + W / 2, 1.25, act, color=c, fontsize=11, ha="center",
                zorder=6, fontweight="bold")

    ax.text(0, 3.75, "결측 여부보다 «왜 비었나» 가 중요",
            color=FG, fontsize=14, fontweight="bold")
    ax.text(0, 0.15,
            "«결측치 처리해줘» 만 요청 시 AI는 세 경우를 구분 없이 동일하게 처리\n"
            "세 번째를 두 번째처럼 처리 → 코드는 정상 실행, 결론만 틀림",
            color=TRAP, fontsize=12, linespacing=1.9, va="top")

    ax.set_xlim(-0.2, 3 * (W + 0.25) + 0.1); ax.set_ylim(-1.0, 4.2)
    ax.set_title("결측치 — 세 가지 이유", loc="left", pad=12, fontsize=15)
    return save(fig, "d03-missing-why")


# =====================================================================
# 3. 평균으로 채우면 무슨 일이 생기는가  ★
# =====================================================================
def fig_mean_imputation():
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.6))

    full = rng.normal(40, 12, 500)
    full = full[full > 0]
    mask = rng.random(len(full)) < 0.35          # 35% 결측
    obs = full[~mask]
    imputed = np.concatenate([obs, np.full(mask.sum(), obs.mean())])

    bins = np.linspace(0, 85, 34)

    ax = axes[0]; style_axes(ax)
    ax.hist(full, bins=bins, color=GFX, alpha=0.8)
    ax.axvline(full.mean(), color=FG, lw=2)
    ax.set_title(f"원래 분포        평균 {full.mean():.1f}  ·  표준편차 {full.std():.1f}",
                 loc="left", color=GFX, fontsize=12.5, pad=10)
    ax.set_yticks([])

    ax = axes[1]; style_axes(ax)
    ax.hist(imputed, bins=bins, color=TRAP, alpha=0.8)
    ax.axvline(imputed.mean(), color=FG, lw=2)
    ax.set_title(f"평균으로 채운 뒤   평균 {imputed.mean():.1f}  ·  표준편차 {imputed.std():.1f}",
                 loc="left", color=TRAP, fontsize=12.5, pad=10)
    ax.set_yticks([])
    ax.annotate("없던 봉우리 발생",
                xy=(obs.mean(), ax.get_ylim()[1] * 0.82),
                xytext=(obs.mean() + 16, ax.get_ylim()[1] * 0.93),
                color=TRAP, fontsize=11.5, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=1.7))

    fig.text(0.5, -0.03,
             "평균은 유지, «흩어진 정도» 는 감소  ·  "
             "이 데이터로 검정 시 없는 차이가 유의하게 나옴",
             color=FG, fontsize=13, ha="center", fontweight="bold")
    fig.text(0.5, -0.115,
             "AI가 가장 자주 선택하는 기본 처리 — 11주차 p값과 직결",
             color=DIM, fontsize=11.5, ha="center")
    return save(fig, "d03-mean-imputation", pad=0.4)


# =====================================================================
# 4. 같은 데이터, 다른 정제, 다른 결론  ★
# =====================================================================
def fig_same_data_diff_conclusion():
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.8))

    # A: 100명 배포, 60명 응답, 30명 전환 / B: 100명 배포, 90명 응답, 40명 전환
    labels = ["A안", "B안"]

    ax = axes[0]; style_axes(ax)
    v1 = [30 / 60 * 100, 40 / 90 * 100]
    ax.bar(labels, v1, color=[GFX, VR], width=0.5)
    for i, v in enumerate(v1):
        ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", color=FG, fontsize=13,
                fontweight="bold")
    ax.set_ylim(0, 62); ax.set_ylabel("전환율")
    ax.set_title("무응답을 «빼고» 계산", loc="left", color=GFX, fontsize=13, pad=10)
    ax.text(0.5, 56, "A안 승", color=GFX, fontsize=14, fontweight="bold", ha="center")

    ax = axes[1]; style_axes(ax)
    v2 = [30, 40]
    ax.bar(labels, v2, color=[GFX, VR], width=0.5)
    for i, v in enumerate(v2):
        ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", color=FG, fontsize=13,
                fontweight="bold")
    ax.set_ylim(0, 62); ax.set_ylabel("전환율")
    ax.set_title("무응답을 «실패» 로 간주", loc="left", color=VR, fontsize=13, pad=10)
    ax.text(0.5, 56, "B안 승", color=VR, fontsize=14, fontweight="bold", ha="center")

    fig.text(0.5, -0.03,
             "숫자 조작 없음  ·  정제 규칙 한 줄로 승자 역전",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")
    fig.text(0.5, -0.115,
             "«어떻게 정제했는가» 기록이 없는 분석 → 검증 불가",
             color=TRAP, fontsize=12, ha="center")
    return save(fig, "d03-same-data-diff-conclusion", pad=0.4)


# =====================================================================
# 5. 정제 로그 — 되돌릴 수 있게 적는다
# =====================================================================
def fig_cleaning_log():
    fig, ax = plt.subplots(figsize=(12.0, 4.8)); clean(ax)

    head = ["무엇을", "왜", "어떻게", "영향받은 행"]
    rows = [
        ["'-', '미상' → 빈칸", "결측 표기가 세 가지", "전부 NA 로 통일", "412"],
        ["인구 열 문자→숫자", "쉼표 때문에 문자였음", "쉼표 제거 후 정수", "1,204"],
        ["'서울시'→'서울특별시'", "같은 지역 다른 표기", "행정표준코드 기준", "37"],
        ["통학 480분 유지", "제주 통학, 오류 아님", "제거하지 않음", "2"],
    ]
    W = [4.0, 3.4, 3.2, 1.7]
    H, X0, Y0 = 0.66, 0.2, 1.0
    x = X0
    for j, c in enumerate(head):
        _cell(ax, x, Y0 + len(rows) * H, W[j], H, c,
              color=LAB, fill="#101a10", edge="#3c5220", fs=11, bold=True)
        x += W[j]
    for i, r in enumerate(rows):
        x = X0
        for j, v in enumerate(r):
            _cell(ax, x, Y0 + (len(rows) - 1 - i) * H, W[j], H, v, fs=9.5)
            x += W[j]

    ax.text(X0, Y0 - 0.55,
            "핵심은 네 번째 줄 — «지우지 않기로 한 결정» 도 기록",
            color=LAB, fontsize=13, fontweight="bold")
    ax.text(X0, Y0 - 1.15,
            "정제 로그 있음 → 결론이 의심받을 때 원인이 된 결정 추적 가능\n"
            "정제 로그 없음 → «데이터가 그렇게 나왔다» 는 설명뿐",
            color=DIM, fontsize=11.5, linespacing=1.9, va="top")

    ax.set_xlim(0, sum(W) + 0.6); ax.set_ylim(-0.6, Y0 + len(rows) * H + H + 0.7)
    ax.set_title("정제 로그", loc="left", pad=14, fontsize=15)
    return save(fig, "d03-cleaning-log")


# =====================================================================
if __name__ == "__main__":
    import sys
    figs = [fig_dirty_data, fig_missing_why, fig_mean_imputation,
            fig_same_data_diff_conclusion, fig_cleaning_log]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
