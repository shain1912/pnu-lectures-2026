"""
2주차 도해 — 그래픽스 수학 기초 · VR 좌표계 체인

실행:  .venv/Scripts/python.exe figures/w02_figures.py
출력:  figures/out/w02-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon, FancyBboxPatch, FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from _style import *   # noqa: F403


# =====================================================================
# 1. 내적 — "b 를 a 위에 눕히면 얼마나 되는가"
# =====================================================================
def fig_dot_product():
    fig, ax = plt.subplots(figsize=(9.4, 4.8)); clean(ax)

    a = np.array([4.4, 0.0])
    b = np.array([2.7, 2.4])
    ahat = a / np.linalg.norm(a)
    proj = ahat * float(np.dot(b, ahat))
    theta = np.degrees(np.arctan2(b[1], b[0]))

    ax.plot([-0.5, 5.6], [0, 0], color=LINE, lw=1.0, zorder=1)

    # 투영 길이 강조
    ax.plot([0, proj[0]], [0, 0], color=WARN, lw=8, alpha=0.9,
            solid_capstyle="butt", zorder=3)
    ax.plot([b[0], proj[0]], [b[1], proj[1]], color=DIM,
            ls=(0, (3, 3)), lw=1.5, zorder=4)
    # 직각 표시
    d = 0.22
    perp = np.array([-ahat[1], ahat[0]])
    corner = proj + perp * d
    ax.plot([proj[0] + ahat[0]*0, corner[0]], [proj[1], corner[1]], color=DIM, lw=1.1)
    ax.plot([corner[0], corner[0] - ahat[0]*d], [corner[1], corner[1] - ahat[1]*d],
            color=DIM, lw=1.1)

    vec(ax, (0, 0), a, GFX, "a", label_off=(0.14, -0.42), fs=17)
    vec(ax, (0, 0), b, VR, "b", label_off=(0.12, 0.14), fs=17)

    ax.add_patch(Arc((0, 0), 1.5, 1.5, theta1=0, theta2=theta,
                     color=DIM, lw=1.4))
    note(ax, 0.95, 0.30, "θ", color=DIM, fs=14)
    note(ax, proj[0] / 2, -0.55, "b 의 a 방향 성분", color=WARN, fs=12, ha="center")

    ax.text(5.9, 2.15,
            "a · b  =  |a| |b| cos θ",
            color=GFX, fontsize=17, fontweight="bold", family=CODE)
    ax.text(5.9, 1.50,
            "        =  |a| × (투영 길이)",
            color=DIM, fontsize=14, family=CODE)
    ax.text(5.9, 0.55,
            "a·b > 0   앞쪽\n"
            "a·b = 0   정확히 직각\n"
            "a·b < 0   뒤쪽",
            color=FG, fontsize=12.5, family=CODE, linespacing=1.9, va="top")

    ax.set_xlim(-0.9, 10.6); ax.set_ylim(-1.15, 3.15)
    ax.set_aspect("equal")
    ax.set_title("내적 — 두 방향이 같은 쪽을 보는 정도", pad=14, loc="left")
    return save(fig, "w02-dot-product")


# =====================================================================
# 2. 외적 — 면적과 법선
# =====================================================================
def fig_cross_product():
    fig = plt.figure(figsize=(8.6, 5.4))
    ax = fig.add_subplot(111, projection="3d")
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

    a = np.array([3.0, 0.2, 0.0])
    b = np.array([0.9, 2.6, 0.6])
    c = np.cross(a, b)
    cn = c / np.linalg.norm(c) * 2.6

    quad = np.array([[0, 0, 0], a, a + b, b])
    ax.add_collection3d(Poly3DCollection(
        [quad], facecolor=GFX, alpha=0.16, edgecolor=GFX, linewidth=1.4))

    for v, col, lab in ((a, GFX, "a"), (b, VR, "b"), (cn, WARN, "a × b")):
        ax.quiver(0, 0, 0, *v, color=col, lw=3.0, arrow_length_ratio=0.13)
        ax.text(*(v * 1.13), lab, color=col, fontsize=15, fontweight="bold")

    ax.text2D(0.03, 0.93,
              "|a × b|  =  평행사변형의 넓이\n"
              "a × b     는 a, b 양쪽에 수직  →  면의 법선(normal)",
              transform=ax.transAxes, color=FG, fontsize=13,
              family=CODE, linespacing=2.0, va="top")
    ax.text2D(0.03, 0.06,
              "Unity : 왼손 좌표계 → 오른손 법칙으로 외운 방향과 부호 반대",
              transform=ax.transAxes, color=TRAP, fontsize=11)

    L = 3.4
    ax.set_xlim(0, L); ax.set_ylim(0, L); ax.set_zlim(0, L)
    ax.set_box_aspect((1, 1, 1))
    for pane, axis in ((ax.xaxis, "x"), (ax.yaxis, "y"), (ax.zaxis, "z")):
        pane.set_pane_color((0.043, 0.051, 0.071, 1.0))
        pane._axinfo["grid"]["color"] = (0.12, 0.14, 0.19, 1.0)
    ax.tick_params(colors=FAINT, labelsize=8)
    ax.view_init(elev=22, azim=32)
    ax.set_title("외적 — 두 벡터가 만드는 면", color=FG, fontsize=15,
                 fontweight="bold", loc="left", pad=2)
    return save(fig, "w02-cross-product")


# =====================================================================
# 3. 회전행렬의 정체 — 열(column)은 기저 벡터가 도착한 자리다  ★핵심
# =====================================================================
def fig_basis_rotation():
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9))
    th = np.radians(35)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])

    for ax, M, title in ((axes[0], np.eye(2), "변환 전"),
                         (axes[1], R, "35° 회전 후")):
        clean(ax)
        i, j = M[:, 0], M[:, 1]
        sq = np.array([[0, 0], i, i + j, j])
        ax.add_patch(Polygon(sq, closed=True, facecolor=GFX, alpha=0.13,
                             edgecolor=GFX, lw=1.3))
        for k in range(-1, 3):
            ax.plot([-1.4, 2.4], [k, k], color="#1a1f2b", lw=0.8, zorder=0)
            ax.plot([k, k], [-1.4, 2.4], color="#1a1f2b", lw=0.8, zorder=0)
        vec(ax, (0, 0), i, AX_X, "i", label_off=(0.1, -0.28), fs=16)
        vec(ax, (0, 0), j, AX_Y, "j", label_off=(-0.3, 0.1), fs=16)
        ax.set_xlim(-1.35, 2.35); ax.set_ylim(-1.15, 1.95)
        ax.set_aspect("equal")
        ax.set_title(title, loc="left", pad=10, fontsize=14)

    axes[1].text(-1.2, -0.85,
                 "i → (cos θ,  sin θ)      j → (−sin θ,  cos θ)",
                 color=DIM, fontsize=12, family=CODE)

    # 행별로 따로 그려야 좌우 정렬이 흐트러지지 않는다
    fig.text(0.245, -0.045, "R  =  [ cos θ   −sin θ ]",
             color=GFX, fontsize=15.5, family=CODE, ha="left", fontweight="bold")
    fig.text(0.245, -0.145, "      [ sin θ    cos θ ]",
             color=GFX, fontsize=15.5, family=CODE, ha="left", fontweight="bold")
    fig.text(0.605, -0.045, "←  1열 = i 가 도착한 자리", color=DIM, fontsize=12.5, ha="left")
    fig.text(0.605, -0.145, "←  2열 = j 가 도착한 자리", color=DIM, fontsize=12.5, ha="left")
    fig.text(0.5, -0.275,
             "행렬 암기 불필요 — 기저 벡터의 도착 위치만 알면 행렬 유도 가능",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")

    fig.suptitle("행렬의 열 = 기저 벡터가 도착한 자리", color=FG, fontsize=16,
                 fontweight="bold", x=0.055, ha="left", y=1.03)
    return save(fig, "w02-basis-rotation", pad=0.42)


# =====================================================================
# 4. 동차좌표 — 이동은 왜 선형변환이 아닌가
# =====================================================================
def fig_homogeneous():
    fig = plt.figure(figsize=(11.4, 4.9))
    axA = fig.add_subplot(1, 2, 1)
    axB = fig.add_subplot(1, 2, 2, projection="3d")

    # --- A : 2D 에서의 문제
    clean(axA)
    for k in range(-1, 4):
        axA.plot([-1.3, 3.6], [k, k], color="#1a1f2b", lw=0.8, zorder=0)
        axA.plot([k, k], [-1.3, 3.3], color="#1a1f2b", lw=0.8, zorder=0)

    tri = np.array([[0.2, 0.2], [1.5, 0.35], [0.75, 1.5]])
    axA.add_patch(Polygon(tri, closed=True, facecolor=GFX, alpha=0.2,
                          edgecolor=GFX, lw=1.5))
    axA.add_patch(Polygon(tri + np.array([1.7, 1.3]), closed=True,
                          facecolor=VR, alpha=0.2, edgecolor=VR, lw=1.5, ls="--"))
    axA.plot(0, 0, "o", color=WARN, ms=11, zorder=9)
    note(axA, 0.12, -0.55, "원점", color=WARN, fs=12)
    axA.annotate("", xy=(2.4, 1.8), xytext=(0.8, 0.6),
                 arrowprops=dict(arrowstyle="-|>", color=VR, lw=2.2))

    axA.text(-1.2, 3.0,
             "회전·스케일 :  원점이 제자리\n"
             "이동          :  원점 이동  →  선형변환 불가",
             color=FG, fontsize=12, family=CODE, linespacing=2.0, va="top")
    axA.set_xlim(-1.3, 3.6); axA.set_ylim(-1.0, 3.3)
    axA.set_aspect("equal")
    axA.set_title("문제 — 2D 행렬로 이동 표현 불가", loc="left", fontsize=13.5, pad=10)

    # --- B : w=1 평면으로 올리기
    fig.patch.set_facecolor(BG); axB.set_facecolor(BG)
    W = 3.2
    plane = np.array([[0, 0, 1], [W, 0, 1], [W, W, 1], [0, W, 1]])
    axB.add_collection3d(Poly3DCollection([plane], facecolor=GFX, alpha=0.10,
                                          edgecolor=GFX, linewidth=1.2))
    tri3 = np.hstack([tri, np.ones((3, 1))])
    axB.add_collection3d(Poly3DCollection([tri3], facecolor=GFX, alpha=0.45,
                                          edgecolor=GFX, linewidth=1.4))
    tri3b = tri3 + np.array([1.7, 1.3, 0])
    axB.add_collection3d(Poly3DCollection([tri3b], facecolor=VR, alpha=0.45,
                                          edgecolor=VR, linewidth=1.4))
    axB.quiver(0, 0, 0, 0, 0, 1.9, color=WARN, lw=2.4, arrow_length_ratio=0.14)
    axB.text(0.1, 0.1, 2.05, "w", color=WARN, fontsize=14, fontweight="bold")
    axB.text(W * 0.55, W * 0.9, 1.15, "w = 1 평면", color=GFX, fontsize=12)

    axB.text2D(0.0, 0.99,
               "해결 — 한 차원 추가  (x, y) → (x, y, 1)\n"
               "3D 의 전단(shear) = 2D 의 이동",
               transform=axB.transAxes, color=FG, fontsize=12,
               family=CODE, linespacing=2.0, va="top")

    axB.set_xlim(0, W); axB.set_ylim(0, W); axB.set_zlim(0, 2.2)
    axB.set_box_aspect((1, 1, 0.72))
    for pane in (axB.xaxis, axB.yaxis, axB.zaxis):
        pane.set_pane_color((0.043, 0.051, 0.071, 1.0))
        pane._axinfo["grid"]["color"] = (0.12, 0.14, 0.19, 1.0)
    axB.tick_params(colors=FAINT, labelsize=7)
    axB.view_init(elev=17, azim=-58)

    fig.text(0.5, -0.06,
             "점은 (x, y, z, 1) · 방향은 (x, y, z, 0)  —  방향 벡터는 이동의 영향 없음",
             color=LAB, fontsize=13, family=CODE, ha="center", fontweight="bold")
    return save(fig, "w02-homogeneous", pad=0.4)


# =====================================================================
# 5. 변환 순서 — R·T 와 T·R 은 다른 결과다
# =====================================================================
def fig_order_matters():
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8))
    d, th = 2.6, np.radians(55)

    def unit_square(c, ang):
        s = 0.42
        pts = np.array([[-s, -s], [s, -s], [s, s], [-s, s]])
        Rm = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        return pts @ Rm.T + c

    for ax in axes:
        clean(ax)
        for k in range(-4, 5):
            ax.plot([-4.2, 4.2], [k, k], color="#161b25", lw=0.7, zorder=0)
            ax.plot([k, k], [-2.2, 3.6], color="#161b25", lw=0.7, zorder=0)
        ax.plot(0, 0, "o", color=WARN, ms=9, zorder=9)
        ax.set_xlim(-1.6, 4.3); ax.set_ylim(-1.5, 2.95)
        ax.set_aspect("equal")

    # --- 왼쪽 : R · T  (이동 먼저 → 원점 기준으로 회전)
    ax = axes[0]
    ax.add_patch(Polygon(unit_square((0, 0), 0), facecolor=FAINT, alpha=0.22,
                         edgecolor=FAINT, lw=1.2))
    ax.add_patch(Polygon(unit_square((d, 0), 0), facecolor=GFX, alpha=0.18,
                         edgecolor=GFX, lw=1.3, ls="--"))
    p = (d * np.cos(th), d * np.sin(th))
    ax.add_patch(Polygon(unit_square(p, th), facecolor=GFX, alpha=0.55,
                         edgecolor=GFX, lw=1.8))
    arc = np.linspace(0, th, 60)
    ax.plot(d * np.cos(arc), d * np.sin(arc), color=GFX, ls=(0, (3, 3)), lw=1.6)
    badge(ax, 0.55, -1.05, "① 이동", FAINT)
    badge(ax, 3.05, 2.42, "② 원점 기준 회전", GFX)
    ax.set_title("R · T   (이동 → 회전)", loc="left", color=GFX, fontsize=14.5, pad=10)

    # --- 오른쪽 : T · R  (회전 먼저 → 그 다음 이동)
    ax = axes[1]
    ax.add_patch(Polygon(unit_square((0, 0), 0), facecolor=FAINT, alpha=0.22,
                         edgecolor=FAINT, lw=1.2))
    ax.add_patch(Polygon(unit_square((0, 0), th), facecolor=VR, alpha=0.18,
                         edgecolor=VR, lw=1.3, ls="--"))
    ax.add_patch(Polygon(unit_square((d, 0), th), facecolor=VR, alpha=0.55,
                         edgecolor=VR, lw=1.8))
    ax.annotate("", xy=(d - 0.5, 0), xytext=(0.6, 0),
                arrowprops=dict(arrowstyle="-|>", color=VR, lw=2.2))
    badge(ax, 0.0, -1.05, "① 제자리 회전", FAINT)
    badge(ax, 2.2, 0.95, "② 이동", VR)
    ax.set_title("T · R   (회전 → 이동)", loc="left", color=VR, fontsize=14.5, pad=10)

    fig.text(0.5, -0.05,
             "같은 R, 같은 T — 순서만 바꿔도 결과 차이   →   행렬 곱의 교환법칙 불성립",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")
    fig.text(0.5, -0.135,
             "Unity 의 transform.Rotate() 와 transform.RotateAround() 의 차이도 이 순서 문제",
             color=DIM, fontsize=11.5, ha="center", family=CODE)
    return save(fig, "w02-order-matters", pad=0.4)


# =====================================================================
# 6. 오일러각 — 같은 각도, 다른 순서
# =====================================================================
def _rot(axis, deg_):
    t = np.radians(deg_); c, s = np.cos(t), np.sin(t)
    if axis == "x": return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y": return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _draw_triad(ax, M, title):
    fig_ = ax.figure
    ax.set_facecolor(BG)
    for v, col, lab in ((np.array([1.9, 0, 0]), AX_X, "X"),
                        (np.array([0, 1.9, 0]), AX_Y, "Y"),
                        (np.array([0, 0, 1.9]), AX_Z, "Z")):
        w = M @ v
        ax.quiver(0, 0, 0, *w, color=col, lw=3.0, arrow_length_ratio=0.16)
        ax.text(*(w * 1.16), lab, color=col, fontsize=13, fontweight="bold")

    # 방향을 알아볼 수 있는 납작한 판
    s = 1.15
    plate = np.array([[-s, -s * 0.45, 0], [s, -s * 0.45, 0],
                      [s, s * 0.45, 0], [-s, s * 0.45, 0]]) @ M.T
    ax.add_collection3d(Poly3DCollection([plate], facecolor=GFX, alpha=0.32,
                                         edgecolor=GFX, linewidth=1.3))
    L = 2.1
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L, L)
    ax.set_box_aspect((1, 1, 1))
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.set_pane_color((0.043, 0.051, 0.071, 1.0))
        pane._axinfo["grid"]["color"] = (0.11, 0.13, 0.18, 1.0)
    ax.tick_params(colors=BG, labelsize=1)
    ax.view_init(elev=20, azim=38)
    ax.set_title(title, color=FG, fontsize=13.5, fontweight="bold", pad=-4)


def fig_euler_order():
    fig = plt.figure(figsize=(11.4, 4.6))
    fig.patch.set_facecolor(BG)

    ax1 = fig.add_subplot(1, 3, 1, projection="3d")
    _draw_triad(ax1, np.eye(3), "시작")

    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    _draw_triad(ax2, _rot("y", 90) @ _rot("x", 90), "X 90°  →  Y 90°")

    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    _draw_triad(ax3, _rot("x", 90) @ _rot("y", 90), "Y 90°  →  X 90°")

    fig.text(0.5, 0.015,
             "같은 (90°, 90°) 에서 다른 결과  →  '회전 순서(rotation order)' 지정 필요\n"
             "Unity 인스펙터 Rotation 적용 순서 : Z → X → Y",
             color=FG, fontsize=12.5, ha="center", linespacing=2.0)
    fig.suptitle("오일러각 — 순서 지정 없이는 의미 없음",
                 color=FG, fontsize=16, fontweight="bold", x=0.05, ha="left", y=0.99)
    return save(fig, "w02-euler-order", pad=0.35)


# =====================================================================
# 7. 짐벌락 — 자유도가 사라지는 지점
# =====================================================================
def fig_gimbal_dof():
    fig, ax = canvas(figsize=(9.6, 4.6))

    p = np.linspace(-90, 90, 721)
    align = np.abs(np.sin(np.radians(p)))

    ax.axhspan(0.985, 1.02, color=TRAP, alpha=0.13, zorder=0)
    ax.plot(p, align, color=GFX, lw=3.0, zorder=5)
    ax.axhline(0.985, color=TRAP, lw=1.3, ls=(0, (4, 3)), zorder=4)

    for x in (-90, 90):
        ax.plot([x, x], [0, 1], color=TRAP, lw=1.2, ls=":", zorder=3)
        ax.plot(x, 1, "o", color=TRAP, ms=11, zorder=9)

    ax.annotate("짐벌락\n요(Y) 와 롤(Z) 이 같은 축으로 정렬",
                xy=(90, 1.0), xytext=(44, 0.72),
                color=TRAP, fontsize=12.5, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="-|>", color=TRAP, lw=1.8),
                linespacing=1.7)
    ax.annotate("피치 0° — 세 축이 서로 직각\n자유도 3 유지",
                xy=(0, 0.0), xytext=(0, 0.34),
                color=LAB, fontsize=12, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=LAB, lw=1.6),
                linespacing=1.7)

    ax.set_xlim(-92, 92); ax.set_ylim(0, 1.1)
    ax.set_xticks([-90, -60, -30, 0, 30, 60, 90])
    ax.set_xlabel("피치 (X축 회전, °)")
    ax.set_ylabel("두 축의 정렬도  |Y · Z|")
    ax.set_title("짐벌락 — 오일러각의 구조적 결함",
                 loc="left", pad=14, fontsize=14.5)
    ax.text(-88, 1.03, "1.000 = 축이 완전히 겹침 (자유도 3 → 2)",
            color=TRAP, fontsize=11, family=CODE)
    return save(fig, "w02-gimbal-dof")


# =====================================================================
# 8. VR 좌표계 체인  ★PART II 핵심
# =====================================================================
def fig_vr_chain():
    fig, ax = plt.subplots(figsize=(12.0, 5.0)); clean(ax)

    nodes = [
        ("World",           "월드 원점",            GFX,  "씬 전체의 기준"),
        ("XR Origin",       "플레이 공간 원점",      GFX,  "바닥 중앙 · 개발자가 배치"),
        ("Camera Offset",   "눈높이 보정",          GFX,  "앉기/서기 모드"),
        ("Main Camera",     "HMD",                 VR,   "트래킹이 매 프레임 덮어씀"),
        ("Eye  L / R",      "좌 · 우 눈",           VR,   "IPD 만큼 좌우로"),
    ]
    W, H, gap = 2.05, 1.12, 0.42
    y = 1.45
    for i, (title, sub, col, foot) in enumerate(nodes):
        x = i * (W + gap)
        ax.add_patch(FancyBboxPatch((x, y), W, H, boxstyle="round,pad=0.06,rounding_size=0.14",
                                    facecolor=BG_SOFT, edgecolor=col, lw=1.8, zorder=4))
        ax.text(x + W / 2, y + H * 0.63, title, color=col, fontsize=12.5,
                fontweight="bold", ha="center", va="center", family=CODE, zorder=6)
        ax.text(x + W / 2, y + H * 0.26, sub, color=FG, fontsize=10.5,
                ha="center", va="center", zorder=6)
        ax.text(x + W / 2, y - 0.30, foot, color=FAINT, fontsize=9.6,
                ha="center", va="top", zorder=6, linespacing=1.6)
        if i < len(nodes) - 1:
            ax.annotate("", xy=(x + W + gap - 0.05, y + H / 2), xytext=(x + W + 0.05, y + H / 2),
                        arrowprops=dict(arrowstyle="-|>", color=LINE, lw=2.0))

    dev_w = 3 * W + 2 * gap
    ax.add_patch(FancyBboxPatch((-0.12, y - 0.72), dev_w + 0.24, H + 1.35,
                                boxstyle="round,pad=0.02,rounding_size=0.16",
                                facecolor="none", edgecolor=LAB, lw=1.5,
                                ls=(0, (5, 4)), zorder=2))
    ax.text(dev_w / 2, y + H + 0.78, "개발자 통제 영역", color=LAB,
            fontsize=13, fontweight="bold", ha="center")

    usr_x = 3 * (W + gap) - 0.12
    usr_w = 2 * W + gap + 0.24
    ax.add_patch(FancyBboxPatch((usr_x, y - 0.72), usr_w, H + 1.35,
                                boxstyle="round,pad=0.02,rounding_size=0.16",
                                facecolor="none", edgecolor=TRAP, lw=1.5,
                                ls=(0, (5, 4)), zorder=2))
    ax.text(usr_x + usr_w / 2, y + H + 0.78, "사용자의 목이 통제하는 영역  —  직접 조작 금지",
            color=TRAP, fontsize=13, fontweight="bold", ha="center")

    ax.text(0, 0.42,
            "이동은 XR Origin 으로.  Main Camera 의 Transform 을 직접 조작하면\n"
            "트래킹 값과 충돌 → 화면 떨림, 사용자 멀미 유발  ← 11주차 AI 함정 #8",
            color=FG, fontsize=12.5, linespacing=2.0, va="top")

    ax.set_xlim(-0.5, 5 * W + 4 * gap + 0.5); ax.set_ylim(-0.62, 3.35)
    ax.set_title("VR 의 좌표계 체인 — 조작 가능한 변환과 조작 금지 변환",
                 loc="left", pad=16, fontsize=15)
    return save(fig, "w02-vr-chain")


# =====================================================================
# 9. 목 모델 — 회전 중심이 눈이 아니다
# =====================================================================
def fig_neck_model():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.0))

    NECK = np.array([0.0, 0.0])
    EYE = np.array([0.62, 1.05])

    def head(ax, pivot, ang, alpha, col):
        t = np.radians(ang)
        R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
        cen = pivot + R @ (np.array([0.0, 0.95]) - pivot + pivot - pivot)
        c = pivot + R @ (np.array([0.0, 0.95]) - pivot)
        e = pivot + R @ (EYE - pivot)
        circ = plt.Circle(c, 0.62, facecolor=col, alpha=alpha * 0.35,
                          edgecolor=col, lw=1.6, zorder=4)
        ax.add_patch(circ)
        ax.plot([pivot[0], c[0]], [pivot[1], c[1]], color=col, lw=3,
                alpha=alpha, zorder=3)
        ax.plot(*e, "o", color=WARN, ms=9, zorder=8, alpha=alpha)
        # 시선
        gaze = R @ np.array([1.15, 0.0])
        ax.annotate("", xy=e + gaze, xytext=e,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.0, alpha=alpha))
        return e

    for ax in axes:
        clean(ax)
        ax.set_xlim(-1.5, 2.9); ax.set_ylim(-0.9, 2.9)
        ax.set_aspect("equal")

    # --- 왼쪽 : 목을 축으로 (실제)
    ax = axes[0]
    e0 = head(ax, NECK, 0, 0.35, FAINT)
    e1 = head(ax, NECK, -38, 1.0, LAB)
    ax.plot(*NECK, "o", color=TRAP, ms=11, zorder=9)
    note(ax, -1.35, -0.55, "● 회전 중심 = 목뼈", color=TRAP, fs=11.5)
    arc = np.linspace(0, np.radians(-38), 40)
    r = np.linalg.norm(EYE - NECK)
    ax.plot(NECK[0] + r * np.sin(arc + np.arctan2(EYE[0], EYE[1])),
            NECK[1] + r * np.cos(arc + np.arctan2(EYE[0], EYE[1])),
            color=WARN, ls=(0, (3, 3)), lw=1.8, zorder=6)
    note(ax, 1.35, 1.55, "눈이 호를 그리며\n위치까지 변화", color=WARN, fs=11.5)
    ax.set_title("실제 사람 — 목을 축으로 회전", loc="left", color=LAB,
                 fontsize=14, pad=10)

    # --- 오른쪽 : 눈을 축으로 (틀린 모델)
    ax = axes[1]
    head(ax, EYE, 0, 0.35, FAINT)
    head(ax, EYE, -38, 1.0, TRAP)
    ax.plot(*EYE, "o", color=TRAP, ms=11, zorder=9)
    note(ax, -1.35, -0.55, "● 회전 중심 = 눈", color=TRAP, fs=11.5)
    note(ax, 1.15, 2.35, "눈이 제자리에서 회전\n→ 몸의 감각과 불일치", color=TRAP, fs=11.5)
    ax.set_title("순진한 구현 — 카메라를 제자리 회전", loc="left", color=TRAP,
                 fontsize=14, pad=10)

    fig.text(0.5, -0.045,
             "목뼈에서 눈까지 약 10 cm  —  이 오프셋 누락 시 고개를 돌릴 때마다 세상이 미끄러짐\n"
             "전정계가 그 어긋남을 정확히 감지  →  멀미 원인",
             color=FG, fontsize=12.5, ha="center", linespacing=2.0)
    return save(fig, "w02-neck-model", pad=0.4)


# =====================================================================
if __name__ == "__main__":
    import sys
    figs = [
        fig_dot_product, fig_cross_product, fig_basis_rotation,
        fig_homogeneous, fig_order_matters, fig_euler_order,
        fig_gimbal_dof, fig_vr_chain, fig_neck_model,
    ]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료 — figures/out/")
