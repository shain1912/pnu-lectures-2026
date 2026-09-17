"""
4주차 도해 — 렌더링 파이프라인 · 카메라와 뷰포트 · 프로젝션 · HMD 광학

실행:  .venv/Scripts/python.exe figures/w04_figures.py [필터]
출력:  figures/out/w04-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Rectangle, FancyArrowPatch,
                                Circle, Polygon, Arc)

from _style import *   # noqa: F403


def _box(ax, x, y, w, h, label, color, sub=None, fs=11.5, lw=1.8, fill=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=fill or BG_SOFT, edgecolor=color, lw=lw, zorder=4))
    ax.text(x + w / 2, y + h * (0.62 if sub else 0.5), label, color=color,
            fontsize=fs, fontweight="bold", ha="center", va="center",
            family=CODE, zorder=6)
    if sub:
        ax.text(x + w / 2, y + h * 0.26, sub, color=FAINT, fontsize=fs * 0.78,
                ha="center", va="center", family=CODE, zorder=6)


def _span(ax, x0, x1, y, text, color, fs=11):
    """구간 브래킷."""
    ax.plot([x0, x1], [y, y], color=color, lw=1.4, zorder=3)
    for x in (x0, x1):
        ax.plot([x, x], [y - 0.12, y], color=color, lw=1.4, zorder=3)
    ax.text((x0 + x1) / 2, y + 0.14, text, color=color, fontsize=fs,
            ha="center", va="bottom", fontweight="bold")


# =====================================================================
# 1. 파이프라인 전 단계 — 좌표는 여섯 번 다른 집에 산다
# =====================================================================
def fig_pipeline_stages():
    fig, ax = plt.subplots(figsize=(15.2, 5.6)); clean(ax)

    W, H, GAP = 2.30, 1.22, 0.72
    Y = 1.30

    stages = [
        ("모델 공간",  "object space", GFX,
         "(0.5, 1.2, 0.0)",   "오브젝트 자신의 원점 기준\n모델링 결과 그대로"),
        ("월드 공간",  "world space",  GFX,
         "(3.5, 1.2, -8.0)",  "씬 전체가 공유하는 원점\n다른 물체와 같은 좌표계"),
        ("뷰 공간",    "view space",   GFX,
         "(1.9, 0.4, -6.2)",  "카메라가 원점\n정면 = -z"),
        ("클립 공간",  "clip space",   WARN,
         "(x, y, z, w=6.2)",  "아직 4차원\nw 에 거리 값 저장"),
        ("NDC",        "normalized",   LAB,
         "(0.44, 0.15, 0.62)", "-1 ~ +1 정육면체\n화면비·해상도 정보 없음"),
        ("스크린 공간", "screen space", LAB,
         "(1382, 464) px",    "픽셀 좌표\n여기서부터 래스터화"),
    ]

    arrows = [
        ("M", "모델 행렬 · 위치·회전·크기", GFX),
        ("V", "뷰 행렬 · 카메라 변환의 역", GFX),
        ("P", "투영 행렬 · w 에 -z 저장", WARN),
        ("w 로 나누기", "클리핑 후 원근 나눗셈", WARN),
        ("뷰포트 변환", "해상도에 맞춰 확대", LAB),
    ]

    xs = []
    x = 0.0
    for i, (name, eng, c, coord, desc) in enumerate(stages):
        xs.append(x)
        _box(ax, x, Y, W, H, name, c, sub=eng, fs=13)
        ax.text(x + W / 2, Y - 0.30, coord, color=WARN, fontsize=10.5,
                ha="center", va="center", family=CODE)
        ax.text(x + W / 2, Y - 0.72, desc, color=DIM, fontsize=10,
                ha="center", va="top", linespacing=1.7)
        x += W + GAP

    for i, (sym, desc, c) in enumerate(arrows):
        gx0 = xs[i] + W
        gx1 = xs[i + 1]
        cx = (gx0 + gx1) / 2
        ax.add_patch(FancyArrowPatch((gx0 + 0.06, Y + H / 2), (gx1 - 0.06, Y + H / 2),
                                     arrowstyle="-|>", color=c, lw=2.2,
                                     mutation_scale=16, zorder=6))
        ax.text(cx, Y + H + 0.52, sym, color=c, fontsize=12.5, ha="center",
                va="center", fontweight="bold", family=CODE)
        ax.text(cx, Y + H + 0.20, desc, color=DIM, fontsize=9.5, ha="center",
                va="center")

    _span(ax, xs[0], xs[3] + W, Y + H + 1.15,
          "정점 셰이더 담당 구간 — 내 코드의 영역", GFX)
    _span(ax, xs[3] + W + 0.1, xs[5] + W, Y + H + 1.15,
          "GPU 고정 기능 — 수정 불가", LAB)

    ax.add_patch(FancyArrowPatch((xs[5] + W + 0.1, Y + H / 2),
                                 (xs[5] + W + 0.85, Y + H / 2),
                                 arrowstyle="-|>", color=VR, lw=2.2,
                                 mutation_scale=16, zorder=6))
    ax.text(xs[5] + W + 0.95, Y + H / 2, "래스터화\n프래그먼트", color=VR,
            fontsize=10.5, va="center", ha="left", linespacing=1.7,
            fontweight="bold")

    ax.text(0, -0.95,
            "정점 하나가 화면에 찍히기까지 좌표계 여섯 번 전환  —  "
            "카메라 이동 = 실제로는 세상 전체를 반대로 이동",
            color=FG, fontsize=13, fontweight="bold")

    ax.set_xlim(-0.4, xs[5] + W + 3.3); ax.set_ylim(-1.5, Y + H + 1.9)
    ax.set_title("렌더링 파이프라인 — 좌표가 지나가는 여섯 개의 공간",
                 loc="left", pad=14, fontsize=15)
    return save(fig, "w04-pipeline-stages")


# =====================================================================
# 2. 절두체 — 카메라가 볼 수 있는 유일한 부피
# =====================================================================
def fig_frustum():
    fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.6),
                             gridspec_kw=dict(width_ratios=[1.56, 1.0]))

    # ---------------------------------------------------- 왼쪽: 옆에서 본 절두체
    ax = axes[0]; clean(ax); ax.set_aspect("equal")
    t = 0.364                     # tan(세로 시야각/2)
    near, far = 1.5, 7.5
    XMAX = 10.0

    ax.plot([0, XMAX], [0, XMAX * t], color=FAINT, lw=1.2, ls=(0, (5, 4)))
    ax.plot([0, XMAX], [0, -XMAX * t], color=FAINT, lw=1.2, ls=(0, (5, 4)))
    ax.plot([0, XMAX], [0, 0], color=LINE, lw=1.1, ls=(0, (2, 4)))

    ax.add_patch(Polygon([(near, near * t), (far, far * t),
                          (far, -far * t), (near, -near * t)],
                         facecolor=GFX, alpha=0.10, edgecolor=GFX, lw=2.2,
                         zorder=2))

    for xv, name in ((near, "근평면  near = 0.3"), (far, "원평면  far = 1000")):
        ax.plot([xv, xv], [-xv * t - 0.35, xv * t + 0.35], color=GFX, lw=2.0)
        ax.text(xv, xv * t + 0.52, name, color=GFX, fontsize=11, ha="center",
                fontweight="bold", family=CODE)

    ax.add_patch(Arc((0, 0), 3.6, 3.6, angle=0, theta1=-20.4, theta2=20.4,
                     color=WARN, lw=2.0))
    ax.text(2.05, 0.42, "세로 시야각", color=WARN, fontsize=11,
            fontweight="bold")

    ax.add_patch(Circle((0, 0), 0.16, facecolor=FG, edgecolor="none", zorder=8))
    ax.text(-0.15, -0.45, "카메라", color=FG, fontsize=11.5, ha="left",
            fontweight="bold")

    inside = [((3.3, -0.42), 0.42), ((5.8, 0.95), 0.50)]
    for (cx, cy), r in inside:
        ax.add_patch(Circle((cx, cy), r, facecolor=LAB, alpha=0.30,
                            edgecolor=LAB, lw=2.0, zorder=5))

    outside = [((0.8, 0.15), 0.30, "근평면보다 앞 — 제외"),
               ((8.8, 0.55), 0.45, "원평면보다 뒤 — 제외"),
               ((4.2, 2.05), 0.45, "위쪽 평면 밖 — 제외")]
    for (cx, cy), r, lbl in outside:
        ax.add_patch(Circle((cx, cy), r, facecolor="none", edgecolor=TRAP,
                            lw=1.8, ls=(0, (4, 3)), zorder=5))
        ax.plot([cx - r * 0.6, cx + r * 0.6], [cy - r * 0.6, cy + r * 0.6],
                color=TRAP, lw=1.6, zorder=6)
        ax.plot([cx - r * 0.6, cx + r * 0.6], [cy + r * 0.6, cy - r * 0.6],
                color=TRAP, lw=1.6, zorder=6)
    ax.text(0.55, -1.05, "근평면보다 앞", color=TRAP, fontsize=10, ha="center")
    ax.text(8.8, 1.25, "원평면보다 뒤", color=TRAP, fontsize=10, ha="center")
    ax.text(4.2, 2.65, "시야 밖", color=TRAP, fontsize=10, ha="center")

    ax.add_patch(Rectangle((6.9, -1.45), far - 6.9, 0.80, facecolor=WARN,
                           alpha=0.28, edgecolor=WARN, lw=1.8, zorder=5))
    ax.add_patch(Rectangle((far, -1.45), 8.25 - far, 0.80, facecolor="none",
                           edgecolor=FAINT, lw=1.4, ls=(0, (4, 3)), zorder=5))
    ax.text(7.6, -1.72, "걸친 것은 잘림 (클리핑)", color=WARN, fontsize=10,
            ha="center", va="top")

    ax.text(-0.5, -3.22, "축척 미적용 그림", color=FAINT, fontsize=9.5,
            ha="left")
    ax.set_xlim(-0.7, 10.3); ax.set_ylim(-3.4, 3.4)
    ax.set_title("절두체 — 옆에서 본 모습", loc="left", pad=12, fontsize=14)

    # ---------------------------------------------------- 오른쪽: 근평면의 얼굴
    ax = axes[1]; clean(ax); ax.set_aspect("equal")
    w, h = 1.60, 0.90
    ax.add_patch(Rectangle((-w / 2, -h / 2), w, h, facecolor=GFX, alpha=0.12,
                           edgecolor=GFX, lw=2.2))
    ax.annotate("", xy=(-w / 2 - 0.22, h / 2), xytext=(-w / 2 - 0.22, -h / 2),
                arrowprops=dict(arrowstyle="<->", color=WARN, lw=1.6))
    ax.text(-w / 2 - 0.32, 0, "높이", color=WARN, fontsize=11, ha="right",
            va="center", fontweight="bold")
    ax.annotate("", xy=(w / 2, -h / 2 - 0.22), xytext=(-w / 2, -h / 2 - 0.22),
                arrowprops=dict(arrowstyle="<->", color=LAB, lw=1.6))
    ax.text(0, -h / 2 - 0.36, "너비 = 높이 x 종횡비", color=LAB, fontsize=11,
            ha="center", va="top", fontweight="bold")

    ax.text(0, 0.08, "16 : 9", color=FG, fontsize=15, ha="center",
            fontweight="bold", family=CODE)
    ax.text(0, -0.22, "근평면의 얼굴", color=DIM, fontsize=10.5, ha="center")

    ax.text(0, h / 2 + 0.30,
            "높이 = 2 x near x tan(세로 시야각 / 2)",
            color=GFX, fontsize=11.5, ha="center", family=CODE)

    ax.text(0, -1.05,
            "종횡비가 뷰포트와 다르면\n장면 전체가 늘어나거나 눌림\n"
            "일반 게임 세로 60도, Quest 3 약 96도",
            color=DIM, fontsize=10.5, ha="center", va="top", linespacing=1.8)

    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_title("종횡비", loc="left", pad=12, fontsize=14)

    fig.text(0.5, -0.03,
             "이 부피 밖의 모든 것은 렌더링 전에 제외  —  "
             "near 와 far : 깊이 정밀도를 결정하는 두 값",
             color=FG, fontsize=13, ha="center", fontweight="bold")
    return save(fig, "w04-frustum", pad=0.36)


# =====================================================================
# 3. 투영 — 절두체를 정육면체에 밀어 넣는다
# =====================================================================
def fig_projection_squash():
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.6),
                             gridspec_kw=dict(width_ratios=[1.385, 1.0]))
    t = 0.364
    n, f = 1.0, 6.0
    bars = [(1.5, LAB), (3.0, LAB), (5.5, LAB)]
    half = 0.45

    # ---------------------------------------------------- 왼쪽: 뷰 공간
    ax = axes[0]; clean(ax); ax.set_aspect("equal")
    ax.add_patch(Polygon([(n, n * t), (f, f * t), (f, -f * t), (n, -n * t)],
                         facecolor=GFX, alpha=0.09, edgecolor=GFX, lw=2.0))
    ax.plot([0, 6.6], [0, 6.6 * t], color=FAINT, lw=1.1, ls=(0, (5, 4)))
    ax.plot([0, 6.6], [0, -6.6 * t], color=FAINT, lw=1.1, ls=(0, (5, 4)))
    ax.add_patch(Circle((0, 0), 0.13, facecolor=FG, edgecolor="none", zorder=8))

    for z, c in bars:
        ax.add_patch(Rectangle((z - 0.07, -half), 0.14, 2 * half,
                               facecolor=c, alpha=0.85, edgecolor=c, lw=1.5,
                               zorder=6))
        ax.plot([0, z], [0, half], color=FAINT, lw=0.9, ls=(0, (2, 3)), zorder=3)
        ax.plot([0, z], [0, -half], color=FAINT, lw=0.9, ls=(0, (2, 3)), zorder=3)
        ax.text(z, -0.62, f"{z}m", color=LAB, fontsize=10, ha="center",
                va="top", family=CODE, zorder=7)
    ax.text(1.35, 0.68, "셋 다 같은 크기", color=FG, fontsize=11.5,
            fontweight="bold")

    for zt in range(1, 7):
        c = GFX if zt in (1, 6) else DIM
        ax.plot([zt, zt], [-2.42, -2.28], color=c, lw=1.4)
        ax.text(zt, -2.62, f"{zt}", color=c, fontsize=10, ha="center",
                va="top", family=CODE)
    ax.text(1.0, -2.98, "near", color=GFX, fontsize=9.5, ha="center",
            va="top", family=CODE)
    ax.text(6.0, -2.98, "far", color=GFX, fontsize=9.5, ha="center",
            va="top", family=CODE)
    ax.text(3.5, -2.98, "깊이 눈금 균일", color=DIM, fontsize=10.5,
            ha="center", va="top")

    ax.set_xlim(-0.4, 6.8); ax.set_ylim(-3.3, 2.6)
    ax.set_title("뷰 공간 — 절두체", loc="left", pad=12, fontsize=14, color=GFX)

    # ---------------------------------------------------- 오른쪽: NDC
    ax = axes[1]; clean(ax); ax.set_aspect("equal")
    ax.add_patch(Rectangle((-1, -1), 2, 2, facecolor=LAB, alpha=0.09,
                           edgecolor=LAB, lw=2.2))

    def zndc(z):
        return (f + n) / (f - n) - 2 * f * n / ((f - n) * z)

    for zt in range(1, 7):
        zz = zndc(zt)
        ax.plot([zz, zz], [-1, 1], color=LINE, lw=1.0)
        ax.plot([zz, zz], [-1.12, -1.0], color=DIM, lw=1.4)
        ax.text(zz, -1.20, f"{zt}", color=DIM, fontsize=9.5, ha="center",
                va="top", family=CODE)

    for z, c in bars:
        zz = zndc(z)
        hh = half / (t * z)
        ax.add_patch(Rectangle((zz - 0.030, -hh), 0.06, 2 * hh,
                               facecolor=c, alpha=0.9, edgecolor=c, lw=1.4,
                               zorder=6))
        ax.text(zz, hh + 0.05, f"{z}m", color=LAB, fontsize=9.5, ha="center",
                va="bottom", family=CODE, zorder=7)

    ax.text(0, 1.14, "-1 ~ +1 정육면체", color=LAB, fontsize=11.5, ha="center",
            fontweight="bold")
    ax.text(0.02, -1.52, "눈금이 뒤로 갈수록 밀집", color=TRAP, fontsize=11,
            ha="center", fontweight="bold")

    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.75, 1.35)
    ax.set_title("NDC — 정육면체", loc="left", pad=12, fontsize=14, color=LAB)

    arr = FancyArrowPatch((0.508, 0.54), (0.585, 0.54),
                          transform=fig.transFigure, arrowstyle="-|>",
                          color=WARN, lw=3.0, mutation_scale=24, zorder=30)
    fig.add_artist(arr)
    fig.text(0.547, 0.60, "P 곱셈 후\nw(= -z) 로 나눗셈", color=WARN,
             fontsize=11, ha="center", va="bottom", fontweight="bold",
             linespacing=1.7)

    fig.text(0.5, -0.03,
             "먼 물체가 작아지는 원인 : "
             "넓은 뒤쪽을 좁은 앞쪽에 맞춰 누르기 위한 z 나눗셈",
             color=FG, fontsize=13, ha="center", fontweight="bold")
    return save(fig, "w04-projection-squash", pad=0.36)


# =====================================================================
# 4. AI 함정 #3 — 깊이 버퍼 정밀도는 near 가 혼자 결정한다
# =====================================================================
def fig_depth_precision():
    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    style_axes(ax)
    BITS = 24

    d = np.logspace(np.log10(0.1), np.log10(1000), 500)

    def prec(dist, n, far):
        # NDC 한 눈금(2 / 2^BITS)이 그 거리에서 몇 m 에 해당하는가
        return dist ** 2 * (1.0 / n - 1.0 / far) / 2 ** BITS

    curves = [
        (0.01, 1000, TRAP, "-",          3.0,
         "near 0.01 / far 1000   AI 기본값"),
        (0.01, 100,  WARN, (0, (6, 4)),  2.2,
         "near 0.01 / far 100     far 를 10분의 1로"),
        (0.3,  1000, LAB,  "-",          3.0,
         "near 0.3  / far 1000    near 를 30배로"),
    ]
    for n, far, c, ls, lw, lbl in curves:
        m = d >= n
        ax.plot(d[m], prec(d[m], n, far), color=c, lw=lw, ls=ls, label=lbl,
                zorder=5)

    THRESH = 0.01
    ax.axhspan(THRESH, 1e3, color=TRAP, alpha=0.07, zorder=1)
    ax.axhline(THRESH, color=TRAP, lw=1.4, ls=(0, (3, 3)), zorder=3)
    ax.text(0.115, THRESH * 1.55,
            "z-fighting 구간 — 1cm 떨어진 두 면이 같은 깊이로 기록",
            color=TRAP, fontsize=11.5, fontweight="bold", va="bottom")

    for n, far, c in ((0.01, 1000, TRAP), (0.3, 1000, LAB)):
        dc = np.sqrt(THRESH * 2 ** BITS / (1 / n - 1 / far))
        ax.plot([dc, dc], [1e-8, THRESH], color=c, lw=1.3, ls=(0, (2, 3)),
                zorder=4)
        ax.plot([dc], [THRESH], "o", color=c, ms=7, zorder=6)
        ax.text(dc, 3e-8, f" {dc:.0f} m 부터", color=c, fontsize=11,
                ha="left", va="bottom", fontweight="bold")

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.1, 1000); ax.set_ylim(1e-8, 1e2)
    ax.set_xlabel("카메라로부터의 거리 (m)")
    ax.set_ylabel("그 거리에서 구분 가능한 최소 간격 (m)")
    ax.grid(True, which="both", alpha=0.45, linewidth=0.7)
    ax.legend(loc="upper left", fontsize=11.5)

    ax.text(0.115, 1.2e-7,
            "붉은 선과 노란 선은 실제로 겹침\n"
            "정밀도를 좌우하는 값 : 1/near - 1/far  →  far 가 크면 1/far ≈ 0\n"
            "far 를 10분의 1로 줄여도 곡선 변화 0.01% 미만",
            color=FG, fontsize=11.5, va="bottom", linespacing=1.9, zorder=9,
            bbox=dict(boxstyle="round,pad=0.7", fc=BG_SOFT, ec=LINE, lw=1.2,
                      alpha=0.96))

    ax.set_title("24비트 깊이 버퍼 — near 의 영향 > far 의 영향",
                 loc="left", pad=14, fontsize=15)
    fig.text(0.5, -0.03,
             "far 증가의 영향은 미미  —  "
             "문제의 원인은 near = 0.01 설정",
             color=TRAP, fontsize=13, ha="center", fontweight="bold")
    return save(fig, "w04-depth-precision", pad=0.36)


# =====================================================================
# 5. 컬링과 클리핑 — 버리는 단위와 시점이 다르다
# =====================================================================
def fig_cull_clip():
    fig, axes = plt.subplots(1, 3, figsize=(14.2, 6.2))
    XL, YL = (-3.9, 3.9), (-3.5, 6.5)   # 세 판의 축척을 통일한다
    TY = -2.35                          # 설명 글의 공통 시작 높이

    # ---------------------------------------------------- ① 프러스텀 컬링
    ax = axes[0]; clean(ax); ax.set_aspect("equal")
    tt, FARY = 0.70, 5.0
    ax.add_patch(Polygon([(0, 0), (-tt * FARY, FARY), (tt * FARY, FARY)],
                         facecolor=GFX, alpha=0.10, edgecolor=GFX, lw=2.0))
    ax.plot([-tt * FARY, tt * FARY], [FARY, FARY], color=GFX, lw=2.0)
    ax.add_patch(Circle((0, 0), 0.13, facecolor=FG, edgecolor="none", zorder=8))
    ax.text(0.24, -0.05, "카메라", color=FG, fontsize=10.5, va="top")

    keep = [(0.35, 2.0, 0.42), (-1.25, 3.6, 0.48)]
    drop = [(2.75, 1.5, 0.42), (-3.15, 4.2, 0.45), (0.4, 5.85, 0.45)]
    for cx, cy, r in keep:
        ax.add_patch(Rectangle((cx - r, cy - r), 2 * r, 2 * r, facecolor="none",
                               edgecolor=LAB, lw=1.2, ls=(0, (3, 3))))
        ax.add_patch(Circle((cx, cy), r * 0.82, facecolor=LAB, alpha=0.32,
                            edgecolor=LAB, lw=1.8))
    for cx, cy, r in drop:
        ax.add_patch(Circle((cx, cy), r * 0.82, facecolor="none",
                            edgecolor=FAINT, lw=1.6, ls=(0, (4, 3))))
        ax.plot([cx - r * 0.5, cx + r * 0.5], [cy - r * 0.5, cy + r * 0.5],
                color=TRAP, lw=1.6)
        ax.plot([cx - r * 0.5, cx + r * 0.5], [cy + r * 0.5, cy - r * 0.5],
                color=TRAP, lw=1.6)

    ax.text(-3.75, TY,
            "CPU 가 그리기 전에 판단\n"
            "바운딩 볼륨이 절두체 밖이면\n오브젝트 전체 제외\n"
            "버리는 단위: 드로우콜 하나",
            color=DIM, fontsize=10.5, va="top", linespacing=1.85)
    ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_title("① 프러스텀 컬링", loc="left", pad=12, fontsize=14, color=GFX)

    # ---------------------------------------------------- ② 클리핑
    ax = axes[1]; clean(ax); ax.set_aspect("equal")
    A, B, C = (-2.4, 0.8), (3.2, 2.0), (1.2, 5.2)
    p1, p2 = (0.0, 1.3143), (0.0, 3.7333)
    ax.add_patch(Polygon([A, p1, p2], facecolor=TRAP, alpha=0.14,
                         edgecolor=TRAP, lw=1.6, ls=(0, (4, 3)), zorder=3))
    ax.add_patch(Polygon([p1, B, C, p2], facecolor=LAB, alpha=0.26,
                         edgecolor=LAB, lw=2.2, zorder=4))
    ax.plot([p1[0], C[0]], [p1[1], C[1]], color=LAB, lw=1.2, ls=(0, (3, 3)),
            zorder=5)
    ax.plot([0, 0], [-0.7, 6.1], color=WARN, lw=2.2, zorder=6)
    ax.text(0.18, 6.15, "클립 평면", color=WARN, fontsize=11, ha="left",
            va="top", fontweight="bold")
    ax.text(-1.55, 0.35, "제외", color=TRAP, fontsize=10.5, ha="center")
    for p in (p1, p2):
        ax.plot([p[0]], [p[1]], "o", color=WARN, ms=9, zorder=8)
    ax.text(-0.22, 2.52, "새로 만든 정점", color=WARN, fontsize=10.5,
            ha="right", va="center", fontweight="bold")
    ax.text(1.7, 0.35, "삼각형 1개 → 2개", color=LAB, fontsize=10.5,
            ha="center", va="top")

    ax.text(-3.75, TY,
            "클립 공간, w 나눗셈 직전\n"
            "평면과 만나는 자리에 정점을\n새로 만들어 절단\n"
            "버리는 단위: 삼각형의 일부",
            color=DIM, fontsize=10.5, va="top", linespacing=1.85)
    ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_title("② 클리핑", loc="left", pad=12, fontsize=14, color=WARN)

    # ---------------------------------------------------- ③ 백페이스 컬링
    ax = axes[2]; clean(ax); ax.set_aspect("equal")
    N = 10
    R = 2.25
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False) + np.pi / N
    pts = np.stack([R * np.cos(ang), R * np.sin(ang) + 3.1], axis=1)
    eye = np.array([0.0, -1.85])
    ax.add_patch(Circle((eye[0], eye[1]), 0.13, facecolor=FG, edgecolor="none",
                        zorder=8))
    ax.text(0.32, -1.85, "카메라", color=FG, fontsize=10.5, va="center")

    for i in range(N):
        a, b = pts[i], pts[(i + 1) % N]
        mid = (a + b) / 2
        edge = b - a
        nrm = np.array([edge[1], -edge[0]])
        nrm = nrm / np.linalg.norm(nrm)
        facing = np.dot(nrm, mid - eye)
        if facing < 0:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=LAB, lw=3.2, zorder=6)
            ax.annotate("", xy=mid + nrm * 0.55, xytext=mid,
                        arrowprops=dict(arrowstyle="-|>", color=LAB, lw=1.4,
                                        mutation_scale=10), zorder=6)
        else:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=FAINT, lw=1.5,
                    ls=(0, (4, 3)), zorder=5)
            ax.annotate("", xy=mid + nrm * 0.48, xytext=mid,
                        arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.0,
                                        mutation_scale=8), zorder=5)
    for xoff in (-1.0, 0.0, 1.0):
        ax.plot([eye[0], eye[0] + xoff * 1.25], [eye[1], 6.0], color=LINE,
                lw=1.0, ls=(0, (2, 4)), zorder=2)

    ax.text(-3.75, 5.9, "등지고 있는 면 — 제외", color=FAINT, fontsize=10.5,
            va="top")
    ax.text(-3.75, 0.15, "마주 보는 면 — 렌더링", color=LAB, fontsize=10.5,
            fontweight="bold", va="top")

    ax.text(-3.75, TY,
            "래스터화 직전, 화면 좌표\n"
            "세 정점의 감김 방향으로 판별\n"
            "닫힌 물체 → 삼각형의 절반 제외\n"
            "버리는 단위: 삼각형 하나",
            color=DIM, fontsize=10.5, va="top", linespacing=1.85)
    ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_title("③ 백페이스 컬링", loc="left", pad=12, fontsize=14, color=LAB)

    fig.text(0.5, -0.04,
             "컬링 = 제외,  클리핑 = 절단  —  "
             "셋 다 \"안 그리는 법\"이지만 제외 단위와 시점이 서로 다름",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")
    return save(fig, "w04-cull-clip", pad=0.38)


# =====================================================================
# 6. HMD 광학 — 렌즈가 휘니까 미리 반대로 휘어 그린다
# =====================================================================
def _grid_lines(nline=9, npt=260, ext=1.0):
    lines = []
    c = np.linspace(-ext, ext, nline)
    s = np.linspace(-ext, ext, npt)
    for v in c:
        lines.append((s, np.full_like(s, v)))
        lines.append((np.full_like(s, v), s))
    return lines


def fig_barrel_distortion():
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 5.0))
    P_LENS = 0.17                       # 렌즈의 핀쿠션 계수

    rs = np.linspace(0, 2.5, 4096)

    def lens(r, p=P_LENS):              # 렌즈 통과 = 핀쿠션
        return r * (1 + p * r ** 2)

    def pre(r, p=P_LENS):               # 그 역 = 사전 배럴 왜곡
        return np.interp(r, lens(rs, p), rs)

    def warp(x, y, fn, p=P_LENS):
        r = np.hypot(x, y)
        r = np.where(r < 1e-9, 1e-9, r)
        k = fn(r, p) / r
        return x * k, y * k

    lines = _grid_lines()
    panels = [
        (0, "① 원본 렌더", GFX,
         "렌더링하려는 화면\n반듯한 격자", None),
        (1, "② 사전 배럴 왜곡", VR,
         "GPU 가 렌더 타깃에\n실제로 그리는 그림", pre),
        (2, "③ 렌즈를 통과한 상", LAB,
         "눈에 도달하는 결과\n다시 반듯한 격자", "both"),
    ]

    for idx, title, color, desc, fn in panels:
        ax = axes[idx]; clean(ax); ax.set_aspect("equal")
        for xs, ys in lines:
            if fn is None:
                X, Y = xs, ys
            elif fn == "both":
                X, Y = warp(xs, ys, pre)
                X, Y = warp(X, Y, lens)
            else:
                X, Y = warp(xs, ys, fn)
            ax.plot(X, Y, color=color, lw=1.15, alpha=0.9, zorder=4)

        if idx == 1:
            for p, cc, lbl in ((0.13, "#ff5a4d", "R"),
                               (0.17, "#a8e05f", "G"),
                               (0.21, "#4d9cff", "B")):
                bx = np.concatenate([np.linspace(-1, 1, 200),
                                     np.full(200, 1.0),
                                     np.linspace(1, -1, 200),
                                     np.full(200, -1.0)])
                by = np.concatenate([np.full(200, 1.0),
                                     np.linspace(1, -1, 200),
                                     np.full(200, -1.0),
                                     np.linspace(-1, 1, 200)])
                BX, BY = warp(bx, by, pre, p)
                ax.plot(BX, BY, color=cc, lw=1.6, alpha=0.95, zorder=6)
            ax.text(0, -1.52, "색수차 보정 — R·G·B 를 각각 다른 배율로",
                    color=DIM, fontsize=10, ha="center")
            ax.text(0, -1.75, "(차이 과장 표현)", color=FAINT,
                    fontsize=9.5, ha="center")

        if idx == 2:
            bx = np.concatenate([np.linspace(-1, 1, 200), np.full(200, 1.0),
                                 np.linspace(1, -1, 200), np.full(200, -1.0)])
            by = np.concatenate([np.full(200, 1.0), np.linspace(1, -1, 200),
                                 np.full(200, -1.0), np.linspace(-1, 1, 200)])
            BX, BY = warp(bx, by, lens)
            ax.plot(BX, BY, color=TRAP, lw=1.8, ls=(0, (5, 4)), zorder=6)
            ax.text(0, -1.52, "사전보정 없을 때의 휨 (핀쿠션)",
                    color=TRAP, fontsize=10, ha="center", fontweight="bold")

        ax.text(0, 1.42, desc, color=DIM, fontsize=10.5, ha="center",
                va="bottom", linespacing=1.75)
        ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.95, 1.95)
        ax.set_title(title, loc="left", pad=12, fontsize=14, color=color)

    for i, (x0, x1) in enumerate(((0.335, 0.360), (0.645, 0.670))):
        arr = FancyArrowPatch((x0, 0.52), (x1, 0.52),
                              transform=fig.transFigure, arrowstyle="-|>",
                              color=WARN, lw=2.6, mutation_scale=20, zorder=30)
        fig.add_artist(arr)
    fig.text(0.3475, 0.565, "GPU", color=WARN, fontsize=10.5, ha="center",
             fontweight="bold", family=CODE)
    fig.text(0.6575, 0.565, "렌즈", color=WARN, fontsize=10.5, ha="center",
             fontweight="bold", family=CODE)

    fig.text(0.5, 0.062,
             "HMD 렌즈 : 상을 핀쿠션으로 확대  →  GPU 는 미리 배럴로 눌러 렌더링  —  "
             "두 왜곡의 상쇄로 반듯한 상",
             color=FG, fontsize=13, ha="center", fontweight="bold")
    fig.text(0.5, 0.012,
             "가운데가 늘어나 보임  →  렌더 해상도를 디스플레이 해상도보다 크게 설정",
             color=DIM, fontsize=11, ha="center")
    return save(fig, "w04-barrel-distortion", pad=0.38)


# =====================================================================
# 7. 양안 비대칭 절두체 — 두 눈은 같은 장면을 보지 않는다
# =====================================================================
def fig_stereo_frustum():
    fig, ax = plt.subplots(figsize=(12.4, 7.6)); clean(ax)
    ax.set_aspect("equal")

    ex = 0.10                          # 눈 위치 — 눈 간격을 과장해 그린다
    D = 0.42                           # 디스플레이까지의 거리
    T_IN, T_OUT = 0.90, 1.15           # 코쪽 / 귀쪽 탄젠트

    eyes = [(-ex, GFX, "왼쪽 눈"), (ex, VR, "오른쪽 눈")]
    geo = {}
    for sx, c, name in eyes:
        sgn = 1.0 if sx < 0 else -1.0            # 코쪽 방향
        x_in = sx + sgn * T_IN * D
        x_out = sx - sgn * T_OUT * D
        geo[name] = (x_in, x_out)
        ax.add_patch(Polygon([(sx, 0), (x_out, D), (x_in, D)],
                             facecolor=c, alpha=0.11, edgecolor=c, lw=2.0,
                             zorder=3))
        ax.plot([sx, sx], [0, 0.20], color=FAINT, lw=1.0, ls=(0, (2, 4)),
                zorder=4)
        ax.plot([sx, (x_in + x_out) / 2], [0, D], color=c, lw=1.3,
                ls=(0, (6, 4)), zorder=4)
        ax.add_patch(Circle((sx, 0), 0.017, facecolor=c, edgecolor="none",
                            zorder=9))

    # ------------------------------------------------ 양안 융합 영역
    ycross = ex / T_IN
    xin_l = -ex + T_IN * D
    ax.add_patch(Polygon([(0, ycross), (-xin_l, D), (xin_l, D)],
                         facecolor=WARN, alpha=0.11, edgecolor=WARN, lw=1.6,
                         ls=(0, (5, 4)), zorder=5))
    ax.text(0, 0.335, "양안 융합 영역", color=WARN, fontsize=12.5,
            ha="center", fontweight="bold")
    ax.text(0, 0.300, "여기서만 깊이 지각 가능", color=WARN, fontsize=10,
            ha="center")
    ax.text(-0.39, 0.245, "왼쪽 눈에만\n보이는 주변부", color=GFX, fontsize=10,
            ha="center", va="center", linespacing=1.7)
    ax.text(0.39, 0.245, "오른쪽 눈에만\n보이는 주변부", color=VR, fontsize=10,
            ha="center", va="center", linespacing=1.7)

    # ------------------------------------------------ 디스플레이 패널
    ax.plot([-0.64, 0.64], [D, D], color=LINE, lw=1.3)
    for (sx, c, name), yy in zip(eyes, (D + 0.035, D + 0.105)):
        x_in, x_out = geo[name]
        lo, hi = min(x_in, x_out), max(x_in, x_out)
        ax.plot([lo, hi], [yy, yy], color=c, lw=2.6)
        for xv in (lo, hi):
            ax.plot([xv, xv], [yy - 0.014, yy + 0.014], color=c, lw=2.0)
        ax.text((lo + hi) / 2, yy + 0.020, f"{name}의 디스플레이", color=c,
                fontsize=10.5, ha="center", va="bottom", fontweight="bold")

    # ------------------------------------------------ 각도 (왼쪽 눈만)
    ax.add_patch(Arc((-ex, 0), 0.26, 0.26, angle=0, theta1=48, theta2=139,
                     color=GFX, lw=1.6, zorder=6))
    ax.plot([-0.305, -0.205], [0.085, 0.085], color=GFX, lw=1.1, zorder=6)
    ax.text(-0.40, 0.085, "왼쪽 눈\n귀쪽 49도 · 코쪽 42도\n코쪽이 7도 좁음",
            color=GFX, fontsize=10.5, ha="center", va="center", linespacing=1.8)
    ax.text(0.40, 0.085, "오른쪽 눈\n좌우로 뒤집힌 같은 모양",
            color=VR, fontsize=10.5, ha="center", va="center", linespacing=1.8)

    # ------------------------------------------------ 머리 · 코 · IPD
    ax.add_patch(Arc((0, -0.008), 0.30, 0.17, angle=0, theta1=196, theta2=344,
                     color=FAINT, lw=1.6))
    ax.add_patch(Polygon([(0, 0.055), (-0.026, 0.002), (0.026, 0.002)],
                         facecolor=BG_SOFT, edgecolor=FAINT, lw=1.4, zorder=8))
    ax.text(0.034, 0.042, "코", color=FAINT, fontsize=10)

    ax.annotate("", xy=(ex, -0.052), xytext=(-ex, -0.052),
                arrowprops=dict(arrowstyle="<->", color=LAB, lw=1.6))
    ax.text(0, -0.103, "IPD 63 mm  (사람마다 58 ~ 72)", color=LAB,
            fontsize=11.5, ha="center", va="top", fontweight="bold")
    ax.text(0, -0.137, "그림의 눈 간격은 과장 표현", color=FAINT,
            fontsize=9.5, ha="center", va="top")

    ax.set_xlim(-0.72, 0.72); ax.set_ylim(-0.20, 0.60)
    ax.set_title("양안 비대칭 절두체 — 위에서 내려다본 모습", loc="left",
                 pad=14, fontsize=15)

    fig.text(0.5, 0.075,
             "각 눈의 절두체 : 코쪽이 좁고 귀쪽이 넓음  —  "
             "중심축이 정면에서 약 3.5도 바깥으로 기울어진 비대칭 구조",
             color=FG, fontsize=13, ha="center", fontweight="bold")
    fig.text(0.5, 0.040,
             "Unity 의 fieldOfView 는 대칭 절두체만 생성  →  "
             "XR 플러그인이 눈마다 projectionMatrix 를 직접 지정하는 이유",
             color=DIM, fontsize=11.5, ha="center")
    fig.text(0.5, 0.010,
             "이 값을 코드로 덮어쓰면 두 눈의 상 불일치 → 융합 실패 → 20분 뒤 멀미",
             color=DIM, fontsize=11.5, ha="center")
    return save(fig, "w04-stereo-frustum")


# =====================================================================
if __name__ == "__main__":
    import sys
    figs = [fig_pipeline_stages, fig_frustum, fig_projection_squash,
            fig_depth_precision, fig_cull_clip, fig_barrel_distortion,
            fig_stereo_frustum]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
