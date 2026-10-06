"""
5주차 도해 — 조명과 재질 · 색공간 · 깊이 단서 · 베이킹

실행:  .venv/Scripts/python.exe figures/w05_figures.py [필터]
출력:  figures/out/w05-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Rectangle, FancyArrowPatch,
                                Circle, Polygon, Wedge)

from _style import *   # noqa: F403


def _box(ax, x, y, w, h, label, color, sub=None, fs=11.5, lw=1.8, fill=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=fill or BG_SOFT, edgecolor=color, lw=lw, zorder=4))
    ax.text(x + w / 2, y + h * (0.62 if sub else 0.5), label, color=color,
            fontsize=fs, fontweight="bold", ha="center", va="center", zorder=6)
    if sub:
        ax.text(x + w / 2, y + h * 0.25, sub, color=FAINT, fontsize=fs * 0.76,
                ha="center", va="center", family=CODE, zorder=6)


def _panel_title(ax, text, color, sub=None, sub_y=-0.09):
    ax.text(0.5, 1.045, text, transform=ax.transAxes, color=color,
            fontsize=12.5, fontweight="bold", ha="center", va="bottom")
    if sub:
        ax.text(0.5, sub_y, sub, transform=ax.transAxes, color=DIM,
                fontsize=10.2, ha="center", va="top", linespacing=1.6)


# =====================================================================
# 1. 코사인 감소 — 같은 빛다발, 넓어진 면적
# =====================================================================
def fig_cosine_falloff():
    fig = plt.figure(figsize=(14.4, 5.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.18, 1], wspace=0.22)
    axL = clean(fig.add_subplot(gs[0]))
    axR = style_axes(fig.add_subplot(gs[1]))

    # ---------------- 왼쪽 : 빛다발이 깔리는 면적
    axL.plot([-0.3, 9.3], [0, 0], color=LINE, lw=2.4, zorder=3)
    axL.text(9.25, -0.38, "표면", color=FAINT, fontsize=11, ha="right")

    beam = 1.6          # 빛다발 폭
    cases = [
        (0.0,  2.2, GFX,  "θ = 0°",  "N·L = 1.00"),
        (60.0, 6.6, WARN, "θ = 60°", "N·L = 0.50"),
    ]
    for deg, cx, color, tag, val in cases:
        th = np.radians(deg)
        foot = beam / np.cos(th)                      # 표면에 깔리는 폭
        x0, x1 = cx - foot / 2, cx + foot / 2

        # 빛살 3개
        for t in np.linspace(0, 1, 4):
            bx = x0 + foot * t
            top = (bx + 3.3 * np.tan(th), 3.3)
            axL.add_patch(FancyArrowPatch(top, (bx, 0.06), arrowstyle="-|>",
                                          color=color, lw=1.8, alpha=0.9,
                                          mutation_scale=13, zorder=5))
        # 표면 법선
        vec(axL, (cx, 0), (0, 1.5), FG, label="N", lw=2.0,
            label_off=(0.14, -0.1), fs=12, zorder=7)
        # 깔린 구간
        axL.plot([x0, x1], [-0.18, -0.18], color=color, lw=3.4,
                 solid_capstyle="butt", zorder=6)
        axL.text(cx, -0.62, f"면적 {foot / beam:.0f}배", color=color,
                 fontsize=11.5, ha="center", fontweight="bold")
        badge(axL, cx, 3.75, f"{tag}  ·  {val}", color, fs=12)

    axL.text(4.4, 2.0, "같은 굵기의 빛다발", color=DIM, fontsize=11.5,
             ha="center", style="italic")
    axL.annotate("", xy=(5.55, 1.75), xytext=(3.25, 1.75),
                 arrowprops=dict(arrowstyle="<->", color=FAINT, lw=1.2))
    axL.set_xlim(-0.6, 9.6)
    axL.set_ylim(-1.5, 4.4)
    _panel_title(axL, "기울면 같은 빛이 넓게 퍼짐", FG,
                 "밝기 = 빛다발 ÷ 면적  →  면적 2배 = 밝기 1/2")

    # ---------------- 오른쪽 : cos 곡선
    t = np.linspace(0, 90, 400)
    axR.plot(t, np.cos(np.radians(t)), color=GFX, lw=3.0, zorder=5)
    axR.fill_between(t, 0, np.cos(np.radians(t)), color=GFX, alpha=0.10)

    marks = [(0, "1.00", GFX), (30, "0.87", GFX), (60, "0.50", WARN),
             (80, "0.17", TRAP), (90, "0.00", TRAP)]
    for deg, lab, c in marks:
        v = np.cos(np.radians(deg))
        axR.plot([deg], [v], "o", color=c, ms=8, zorder=7)
        axR.annotate(lab, (deg, v), textcoords="offset points",
                     xytext=(9, 9), color=c, fontsize=11.5, fontweight="bold")

    axR.axhline(0, color=LINE, lw=1.2)
    axR.set_xlim(-3, 97)
    axR.set_ylim(-0.08, 1.15)
    axR.set_xticks([0, 30, 60, 90])
    axR.set_xticklabels(["0°", "30°", "60°", "90°"])
    axR.set_xlabel("법선 N 과 광원 방향 L 사이의 각 θ")
    axR.set_ylabel("확산반사 계수  N·L")
    _panel_title(axR, "N · L = cos θ", GFX,
                 "2주차 내적의 재등장 · 음수는 0 으로 절단 (뒷면은 빛 미수광)",
                 sub_y=-0.21)

    fig.text(0.5, -0.08,
             "확산반사 색 = albedo × 광원색 × max(0, N·L) × 세기",
             color=WARN, fontsize=12.5, ha="center", family=CODE)
    return save(fig, "w05-cosine-falloff")


# =====================================================================
# 2. BRDF — 반사가 어느 방향으로 퍼지는가
# =====================================================================
def fig_brdf_lobe():
    fig, axes = plt.subplots(1, 3, figsize=(14.6, 5.2))
    for a in axes:
        clean(a)

    inc = np.radians(135)        # 들어오는 방향 (왼쪽 위에서)
    mirror = np.radians(45)      # 거울 반사 방향

    specs = [
        ("확산 (Lambert)", GFX, None,
         "모든 방향으로 균일\nalbedo 와 N·L 만으로 결정",
         "거친 종이 · 벽 · 천"),
        ("정반사 · roughness 낮음", WARN, 26,
         "거울 방향 주변에 집중\n작고 선명한 하이라이트",
         "금속 · 젖은 바닥 · 유약"),
        ("정반사 · roughness 높음", VR, 3,
         "같은 에너지가 넓게 분산\n크고 흐린 하이라이트",
         "거친 금속 · 무광 플라스틱"),
    ]

    for ax, (title, color, power, desc, ex) in zip(axes, specs):
        # 표면과 법선
        ax.plot([-1.35, 1.35], [0, 0], color=LINE, lw=2.4, zorder=3)
        vec(ax, (0, 0), (0, 1.12), FG, label="N", lw=1.8,
            label_off=(0.08, -0.05), fs=11.5, zorder=8)

        # 들어오는 빛
        ax.add_patch(FancyArrowPatch((np.cos(inc) * 1.25, np.sin(inc) * 1.25),
                                     (0, 0), arrowstyle="-|>", color=LAB,
                                     lw=2.2, mutation_scale=15, zorder=8))
        ax.text(np.cos(inc) * 1.32, np.sin(inc) * 1.32 + 0.1, "L",
                color=LAB, fontsize=12, fontweight="bold", ha="center")

        # 반사 로브
        th = np.linspace(0, np.pi, 240)
        if power is None:
            r = np.full_like(th, 0.78)
        else:
            r = 0.98 * np.clip(np.cos(th - mirror), 0, None) ** power
            r = np.where(r < 0.004, 0.004, r)
        pts = np.column_stack([r * np.cos(th), r * np.sin(th)])
        ax.add_patch(Polygon(np.vstack([[0, 0], pts, [0, 0]]), closed=True,
                             facecolor=color, alpha=0.26, edgecolor=color,
                             lw=2.2, zorder=5))

        if power is not None:
            ax.plot([0, np.cos(mirror) * 1.2], [0, np.sin(mirror) * 1.2],
                    color=FAINT, lw=1.2, ls=(0, (4, 4)), zorder=4)
            ax.text(np.cos(mirror) * 1.3, np.sin(mirror) * 1.3, "거울 방향",
                    color=FAINT, fontsize=9.8, ha="left", va="center")

        ax.set_xlim(-1.5, 1.6)
        ax.set_ylim(-0.42, 1.55)
        _panel_title(ax, title, color, desc + "\n" + ex)

    fig.text(0.5, -0.20,
             "BRDF : 들어온 빛이 어느 방향으로 얼마나 나가는지 알려 주는 함수 "
             "·  로브의 전체 넓이 = 반사 에너지 총량",
             color=DIM, fontsize=12, ha="center")
    fig.text(0.5, -0.275,
             "PBR 의 roughness = 이 로브의 폭 · metallic = 확산 로브의 소멸 여부",
             color=WARN, fontsize=12, ha="center")
    return save(fig, "w05-brdf-lobe")


# =====================================================================
# 3. 감마 vs 선형 — 저장된 숫자와 실제 빛의 양
# =====================================================================
def fig_gamma_linear():
    fig = plt.figure(figsize=(14.6, 5.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.12], wspace=0.24)
    axL = style_axes(fig.add_subplot(gs[0]))
    axR = clean(fig.add_subplot(gs[1]))

    # ---------------- 왼쪽 : 전달 곡선
    x = np.linspace(0, 1, 300)
    axL.plot(x, x, color=FAINT, lw=1.8, ls=(0, (5, 4)), label="같은 값 (기준선)")
    axL.plot(x, x ** 2.2, color=GFX, lw=3.0,
             label="sRGB 값 → 실제 빛의 양")

    axL.plot([0.5, 0.5], [0, 0.5 ** 2.2], color=WARN, lw=1.6, ls=(0, (3, 3)))
    axL.plot([0, 0.5], [0.5 ** 2.2, 0.5 ** 2.2], color=WARN, lw=1.6, ls=(0, (3, 3)))
    axL.plot([0.5], [0.5 ** 2.2], "o", color=WARN, ms=9, zorder=8)
    axL.annotate("저장값 0.5\n실제 빛 0.22", (0.5, 0.5 ** 2.2),
                 textcoords="offset points", xytext=(14, 6),
                 color=WARN, fontsize=12, fontweight="bold")

    axL.set_xlim(0, 1.02)
    axL.set_ylim(0, 1.02)
    axL.set_xlabel("이미지 파일에 저장된 숫자 (sRGB)")
    axL.set_ylabel("화면이 실제로 내보내는 빛의 양 (선형)")
    axL.legend(loc="upper left", fontsize=10.5)
    _panel_title(axL, "중간 회색 0.5 의 함정", WARN,
                 "사람 눈이 어두운 쪽을 잘 구분 → 저장은 비선형, 계산은 선형",
                 sub_y=-0.19)

    # ---------------- 오른쪽 : 처리 순서
    Y = 2.55
    H, W = 0.92, 2.05
    steps = [
        (0.0,  "텍스처",   "sRGB 저장", GFX),
        (2.75, "선형 변환", "값 ^ 2.2", LAB),
        (5.5,  "조명 계산", "곱·덧셈", LAB),
        (8.25, "화면 출력", "값 ^ 1/2.2", GFX),
    ]
    for x, name, sub, c in steps:
        _box(axR, x, Y, W, H, name, c, sub=sub, fs=12.5)
    for i in range(3):
        x0 = steps[i][0] + W
        x1 = steps[i + 1][0]
        axR.add_patch(FancyArrowPatch((x0 + 0.08, Y + H / 2), (x1 - 0.08, Y + H / 2),
                                      arrowstyle="-|>", color=FAINT, lw=2.0,
                                      mutation_scale=15, zorder=6))
    axR.text(5.15, Y + H + 0.42, "이 구간에서만 덧셈·곱셈이 물리와 일치",
             color=LAB, fontsize=11.5, ha="center")
    axR.plot([2.75, 7.55], [Y + H + 0.3, Y + H + 0.3], color=LAB, lw=1.6)

    # 비교 : 같은 광원 두 개
    axR.text(0.0, 1.62, "광원 0.5 두 개를 더하면", color=FG, fontsize=12.5,
             fontweight="bold", ha="left")
    rows = [
        (1.02, "선형 공간 계산", "0.22 + 0.22 = 0.44", LAB, "화면 0.70 · 물리와 일치"),
        (0.30, "감마 공간 계산", "0.5 + 0.5 = 1.00", TRAP, "화면 1.00 · 흰색 포화"),
    ]
    for y, name, expr, c, tail in rows:
        axR.add_patch(FancyBboxPatch((0.0, y), 10.3, 0.56,
                                     boxstyle="round,pad=0.02,rounding_size=0.06",
                                     facecolor=BG_SOFT, edgecolor=c, lw=1.5, zorder=4))
        axR.text(0.22, y + 0.28, name, color=c, fontsize=12, fontweight="bold",
                 va="center", zorder=6)
        axR.text(3.0, y + 0.28, expr, color=FG, fontsize=12, va="center",
                 family=CODE, zorder=6)
        axR.text(10.08, y + 0.28, tail, color=c, fontsize=11.5, va="center",
                 ha="right", zorder=6)

    axR.set_xlim(-0.3, 10.6)
    axR.set_ylim(0.0, 4.5)
    _panel_title(axR, "Unity 의 처리 순서", GFX,
                 "Project Settings → Player → Color Space = Linear 확인")
    return save(fig, "w05-gamma-linear")


# =====================================================================
# 4. 깊이 단서 — 한 눈으로도 거리를 아는 방법
# =====================================================================
def fig_depth_cues():
    fig, axes = plt.subplots(2, 3, figsize=(14.6, 7.4))
    fig.subplots_adjust(hspace=0.55, wspace=0.18)
    ax = axes.ravel()
    for a in ax:
        clean(a)
        a.set_xlim(0, 10)
        a.set_ylim(0, 6)

    # ① 폐색
    a = ax[0]
    a.add_patch(Rectangle((1.2, 1.6), 3.6, 3.0, facecolor=BG_SOFT,
                          edgecolor=GFX, lw=2.0, zorder=4))
    a.add_patch(Rectangle((3.6, 2.4), 3.6, 3.0, facecolor=BG_SOFT,
                          edgecolor=VR, lw=2.0, zorder=5))
    a.text(2.3, 3.1, "뒤", color=GFX, fontsize=12.5, fontweight="bold", zorder=6)
    a.text(6.0, 3.9, "앞", color=VR, fontsize=12.5, fontweight="bold", zorder=6)
    _panel_title(a, "① 폐색", GFX, "가리는 쪽이 앞 · 순서만 알려 주고 거리는 미제공")

    # ② 상대 크기
    a = ax[1]
    for cx, r, c in [(2.1, 1.25, VR), (5.2, 0.78, VR), (7.9, 0.42, VR)]:
        a.add_patch(Circle((cx, 2.6), r, facecolor=BG_SOFT, edgecolor=c,
                           lw=2.0, zorder=4))
    a.annotate("", xy=(8.6, 1.0), xytext=(1.3, 1.0),
               arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.6))
    a.text(4.9, 0.45, "멀어질수록 작게", color=DIM, fontsize=11, ha="center")
    _panel_title(a, "② 상대 크기 · 친숙한 크기", VR,
                 "크기를 아는 물체면 거리까지 추정 가능")

    # ③ 결 기울기
    a = ax[2]
    for i in range(9):
        t = i / 8
        y = 0.9 + 4.3 * t ** 1.9
        half = 4.2 * (1 - 0.72 * t)
        a.plot([5 - half, 5 + half], [y, y], color=LAB,
               lw=2.2 - 1.5 * t, alpha=0.9 - 0.45 * t, zorder=4)
    for k in (-1, 0, 1):
        a.plot([5 + k * 4.2, 5 + k * 1.2], [0.9, 5.2], color=LAB,
               lw=1.1, alpha=0.4, zorder=3)
    _panel_title(a, "③ 결 기울기", LAB, "같은 무늬가 촘촘해지는 비율 = 기울기와 거리")

    # ④ 음영
    a = ax[3]
    gx, gy = np.meshgrid(np.linspace(-1, 1, 220), np.linspace(-1, 1, 220))
    mask = gx ** 2 + gy ** 2 <= 1
    shade = np.clip(0.30 * gx * -1 + 0.95 * gy + 0.25, 0.05, 1)
    img = np.ones(gx.shape) * np.nan
    img[mask] = shade[mask]
    a.imshow(img, extent=(1.1, 4.7, 1.3, 4.9), origin="lower",
             cmap="bone", vmin=0, vmax=1.25, zorder=4)
    a.add_patch(FancyArrowPatch((7.3, 5.4), (5.2, 4.2), arrowstyle="-|>",
                                color=WARN, lw=2.0, mutation_scale=14, zorder=6))
    a.text(7.5, 5.5, "빛", color=WARN, fontsize=12, fontweight="bold")
    a.text(5.6, 2.4, "뇌의 기본 가정 :\n빛은 위에서 내려옴", color=DIM,
           fontsize=10.8, va="center", linespacing=1.7)
    _panel_title(a, "④ 음영", WARN, "밝기 변화로 곡면의 볼록·오목 판별")

    # ⑤ 그림자
    a = ax[4]
    from matplotlib.patches import Ellipse
    for cx, sx, lab, c in [(2.7, 2.7, "접지", LAB), (6.9, 8.4, "공중에 뜸", TRAP)]:
        a.add_patch(Circle((cx, 3.4), 0.72, facecolor=BG_SOFT, edgecolor=c,
                           lw=2.0, zorder=5))
        a.add_patch(Ellipse((sx, 1.35), 1.7, 0.52, facecolor="#242a38",
                            edgecolor="none", zorder=4))
        a.text(cx, 4.55, lab, color=c, fontsize=11.5, fontweight="bold", ha="center")
    a.plot([0.8, 9.4], [1.35, 1.35], color=LINE, lw=2.0, zorder=3)
    a.annotate("", xy=(8.2, 0.75), xytext=(3.0, 0.75),
               arrowprops=dict(arrowstyle="-|>", color=FAINT, lw=1.3))
    a.text(5.6, 0.35, "그림자만 이동", color=FAINT, fontsize=10, ha="center")
    _panel_title(a, "⑤ 그림자", TRAP, "물체는 그대로 · 그림자 위치만 이동 → 높이 지각 변화")

    # ⑥ 대기 원근
    a = ax[5]
    peaks = [(2.0, 3.6, 0.95, FG), (4.6, 3.0, 0.55, DIM), (7.3, 2.5, 0.28, FAINT)]
    for cx, h, alpha, c in peaks:
        a.add_patch(Polygon([[cx - 2.3, 1.2], [cx, 1.2 + h], [cx + 2.3, 1.2]],
                            closed=True, facecolor=c, alpha=alpha,
                            edgecolor="none", zorder=4))
    a.plot([0.5, 9.6], [1.2, 1.2], color=LINE, lw=2.0, zorder=5)
    a.text(5.0, 0.5, "멀수록 흐리고 푸르게", color=DIM, fontsize=11, ha="center")
    _panel_title(a, "⑥ 대기 원근", DIM, "공기 중 산란 · 수백 m 이상에서 유효")

    fig.text(0.5, 0.012,
             "①~⑥ 모두 한쪽 눈만으로 성립하는 단안 단서 — LaValle 『Virtual Reality』 Ch.6",
             color=VR, fontsize=12.5, ha="center")
    fig.text(0.5, -0.03,
             "④ 음영 · ⑤ 그림자 = 조명 설정이 직접 만드는 단서 → 조명은 깊이 지각의 재료",
             color=WARN, fontsize=12.5, ha="center")
    return save(fig, "w05-depth-cues")


# =====================================================================
# 5. 실시간 그림자 vs 베이크 — 프레임 예산 안에서
# =====================================================================
def fig_bake_vs_realtime():
    fig, ax = plt.subplots(figsize=(14.2, 6.0))
    clean(ax)

    BUDGET = 11.1
    SCALE = 0.78          # ms → 그림 단위
    X0 = 2.35

    rows = [
        ("실시간 그림자 3개", TRAP, [
            ("그림자맵 3장", 4.2, TRAP),
            ("왼쪽 눈", 4.0, GFX),
            ("오른쪽 눈", 4.0, GFX),
            ("그 외", 1.6, FAINT),
        ], "13.8 ms  →  90Hz 유지 실패"),
        ("그림자 1개 + 나머지 베이크", LAB, [
            ("맵 1장", 1.4, WARN),
            ("왼쪽 눈", 3.1, GFX),
            ("오른쪽 눈", 3.1, GFX),
            ("그 외", 1.6, FAINT),
        ], "9.2 ms  →  여유 1.9 ms"),
    ]

    for i, (name, c, segs, tail) in enumerate(rows):
        y = 3.3 - i * 1.75
        ax.text(X0 - 0.35, y + 0.34, name, color=c, fontsize=13,
                fontweight="bold", ha="right", va="center")
        x = X0
        for label, ms, sc in segs:
            w = ms * SCALE
            ax.add_patch(Rectangle((x, y), w, 0.68, facecolor=sc, alpha=0.30,
                                   edgecolor=sc, lw=1.8, zorder=4))
            ax.text(x + w / 2, y + 0.34, label, color=sc, fontsize=10.5,
                    ha="center", va="center", zorder=6)
            ax.text(x + w / 2, y - 0.08, f"{ms:g}", color=FAINT, fontsize=9.5,
                    ha="center", va="top", family=CODE, zorder=6)
            x += w
        ax.text(max(x, X0 + BUDGET * SCALE) + 0.3, y + 0.34, tail, color=c,
                fontsize=12, fontweight="bold", va="center")

    # 예산선
    bx = X0 + BUDGET * SCALE
    ax.plot([bx, bx], [0.95, 4.85], color=WARN, lw=2.2, ls=(0, (6, 4)), zorder=8)
    ax.text(bx, 5.0, "90Hz 예산 11.1 ms", color=WARN, fontsize=12.5,
            fontweight="bold", ha="center")

    # 베이크 설명
    notes = [
        ("베이크가 가능한 조건", LAB,
         "광원 Mode = Baked · 물체 Static · Lightmap UV 존재"),
        ("베이크로 사라지는 비용", LAB,
         "그림자맵 생성 패스 · 광원별 음영 계산 → 텍스처 샘플 1회로 대체"),
        ("베이크로 해결 불가", TRAP,
         "움직이는 물체의 그림자 · 켜고 끄는 조명 → 라이트 프로브와 혼합"),
    ]
    for i, (head, c, body) in enumerate(notes):
        y = 0.52 - i * 0.44
        ax.text(X0 - 0.35, y, head, color=c, fontsize=11.5, fontweight="bold",
                ha="right", va="center")
        ax.text(X0, y, body, color=DIM, fontsize=11.5, va="center")

    ax.set_xlim(-2.0, X0 + 16.5 * SCALE)
    ax.set_ylim(-0.95, 5.4)
    fig.text(0.5, -0.02,
             "수치 예시 — 실제 값은 씬·기기에 따라 상이 · VR 은 눈 두 개분을 한 프레임에 처리",
             color=FAINT, fontsize=11.5, ha="center")
    return save(fig, "w05-bake-vs-realtime")


# =====================================================================
if __name__ == "__main__":
    import sys
    figs = [fig_cosine_falloff, fig_brdf_lobe, fig_gamma_linear,
            fig_depth_cues, fig_bake_vs_realtime]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
