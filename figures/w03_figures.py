"""
3주차 도해 — Unity 기초 · 게임 루프 · 프레임 독립성 · motion-to-photon

실행:  .venv/Scripts/python.exe figures/w03_figures.py [필터]
출력:  figures/out/w03-*.svg  +  .png
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

from _style import *   # noqa: F403


def _box(ax, x, y, w, h, label, color, sub=None, fs=11.5, lw=1.8, fill=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=fill or BG_SOFT, edgecolor=color, lw=lw, zorder=4))
    ax.text(x + w / 2, y + h * (0.62 if sub else 0.5), label, color=color,
            fontsize=fs, fontweight="bold", ha="center", va="center",
            family=CODE, zorder=6)
    if sub:
        ax.text(x + w / 2, y + h * 0.26, sub, color=FG, fontsize=fs * 0.82,
                ha="center", va="center", zorder=6)


# =====================================================================
# 1. 씬 그래프 — 부모를 움직이면 자식이 따라온다
# =====================================================================
def fig_scene_graph():
    fig, ax = plt.subplots(figsize=(11.6, 5.0)); clean(ax)

    nodes = {
        "Scene":  (0.4, 3.5, GFX,  None),
        "Car":    (0.4, 2.2, LAB,  "부모"),
        "Body":   (2.9, 1.0, GFX,  "자식"),
        "Wheel L": (5.4, 1.0, GFX, "자식"),
        "Wheel R": (7.9, 1.0, GFX, "자식"),
        "Bolt":   (5.4, -0.3, DIM, "손자"),
    }
    W, H = 1.9, 0.85
    for name, (x, y, c, sub) in nodes.items():
        _box(ax, x, y, W, H, name, c, sub)

    edges = [("Scene", "Car"), ("Car", "Body"), ("Car", "Wheel L"),
             ("Car", "Wheel R"), ("Wheel L", "Bolt")]
    # 직교 엘보로 직접 그린다 — FancyArrowPatch 의 angle 연결은
    # 두 점이 수직으로 정렬되면 "lines do not intersect" 로 터진다.
    for a, b in edges:
        xa, ya, _, _ = nodes[a]; xb, yb, _, _ = nodes[b]
        x1, x2 = xa + W / 2, xb + W / 2
        ymid = (ya + yb + H) / 2
        ax.plot([x1, x1, x2, x2], [ya, ymid, ymid, yb + H],
                color=LINE, lw=1.6, zorder=2, solid_joinstyle="round")

    # 부모를 옮기면 전체가 따라간다
    ax.add_patch(FancyArrowPatch((2.4, 2.62), (3.9, 2.62), arrowstyle="-|>",
                                 color=LAB, lw=2.4, mutation_scale=18, zorder=8))
    badge(ax, 5.6, 2.62, "Car 를 1m 이동 → 아래 전부 1m 이동", LAB, fs=12)

    ax.text(0.4, -1.35,
            "월드 위치 = M(Car) · M(Wheel L) · M(Bolt) · (0,0,0)",
            color=GFX, fontsize=14, family=CODE, fontweight="bold")
    ax.text(0.4, -1.95,
            "계층 = 행렬 곱의 연쇄  —  2주차에 배운 곱셈의 적용",
            color=DIM, fontsize=12)

    ax.set_xlim(-0.2, 11.0); ax.set_ylim(-2.3, 4.8)
    ax.set_title("씬 그래프 — 계층은 곧 변환의 연쇄", loc="left", pad=14, fontsize=15)
    return save(fig, "w03-scene-graph")


# =====================================================================
# 2. 상속 대신 조합 — 컴포넌트란 무엇인가
# =====================================================================
def fig_component():
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.2))

    # ---- 왼쪽: 상속 트리의 조합 폭발
    ax = axes[0]; clean(ax)
    tree = [
        ("Enemy", 3.4, 4.3, 2.6),
        ("FlyingEnemy", 1.2, 3.0, 2.6), ("WalkingEnemy", 5.0, 3.0, 2.8),
        ("FlyingShooter", 0.1, 1.7, 2.7), ("FlyingBomber", 3.0, 1.7, 2.6),
        ("WalkingShooter", 5.9, 1.7, 3.0),
        ("???", 3.0, 0.4, 2.6),
    ]
    for name, x, y, w in tree:
        c = TRAP if name == "???" else FAINT
        _box(ax, x, y, w, 0.72, name, c, fs=10.5, lw=1.4)
    for a, b in [((4.7, 4.3), (2.5, 3.72)), ((4.7, 4.3), (6.4, 3.72)),
                 ((2.5, 3.0), (1.45, 2.42)), ((2.5, 3.0), (4.3, 2.42)),
                 ((6.4, 3.0), (7.4, 2.42)), ((4.3, 1.7), (4.3, 1.12))]:
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-", color=LINE, lw=1.3, zorder=2))
    ax.text(0.1, -0.45, "날면서 폭탄도 쏘는 적은?\n클래스 수 기하급수적 증가",
            color=TRAP, fontsize=12, linespacing=1.8, va="top")
    ax.set_xlim(-0.2, 9.2); ax.set_ylim(-1.6, 5.5)
    ax.set_title("상속 — 조합 증가 시 붕괴", loc="left", color=TRAP,
                 fontsize=14, pad=12)

    # ---- 오른쪽: 컴포넌트 조합
    ax = axes[1]; clean(ax)
    _box(ax, 0.6, 4.5, 6.4, 0.8, "GameObject", FG, fs=13, lw=2.2)
    comps = [
        ("Transform", GFX,  "위치·회전·크기 — 필수"),
        ("MeshRenderer", GFX, "화면에 그리기"),
        ("Rigidbody", LAB,  "물리 적용"),
        ("Collider", LAB,   "충돌 판정"),
        ("MyScript", WARN,  "내가 만든 행동"),
    ]
    for i, (n, c, d) in enumerate(comps):
        y = 3.5 - i * 0.82
        _box(ax, 1.0, y, 2.7, 0.66, n, c, fs=11)
        ax.text(4.0, y + 0.33, d, color=DIM, fontsize=10.5, va="center")
    ax.text(0.6, -0.6, "필요한 부품만 붙이고 떼기\n조합이 늘어도 부품 수는 그대로",
            color=LAB, fontsize=12, linespacing=1.8, va="top")
    ax.set_xlim(0.2, 9.2); ax.set_ylim(-1.6, 5.5)
    ax.set_title("컴포넌트 — 조립", loc="left", color=LAB, fontsize=14, pad=12)

    fig.text(0.5, -0.02,
             "Unity 에서의 제작 = 부품(컴포넌트)을 붙이는 작업",
             color=FG, fontsize=13.5, ha="center", fontweight="bold")
    return save(fig, "w03-component", pad=0.38)


# =====================================================================
# 3. 한 프레임의 해부 — 실행 순서
# =====================================================================
def fig_frame_anatomy():
    fig, ax = plt.subplots(figsize=(12.0, 4.6)); clean(ax)

    stages = [
        ("입력 수집",     1.3, FAINT, "Input"),
        ("FixedUpdate",  2.6, LAB,   "물리 · 0~n회"),
        ("Update",       2.4, GFX,   "게임 로직 · 1회"),
        ("LateUpdate",   2.0, GFX,   "카메라 추적 · 1회"),
        ("렌더링",        2.6, VR,    "화면에 그림"),
        ("vsync 대기",   1.6, WARN,  "다음 프레임까지"),
    ]
    x = 0.0
    for name, w, c, sub in stages:
        ax.add_patch(FancyBboxPatch((x, 1.2), w - 0.12, 1.15,
                                    boxstyle="round,pad=0.02,rounding_size=0.08",
                                    facecolor=BG_SOFT, edgecolor=c, lw=2.0, zorder=4))
        ax.text(x + (w - 0.12) / 2, 1.95, name, color=c, fontsize=12,
                fontweight="bold", ha="center", va="center", family=CODE, zorder=6)
        ax.text(x + (w - 0.12) / 2, 1.52, sub, color=DIM, fontsize=10,
                ha="center", va="center", zorder=6)
        x += w

    total = x
    ax.annotate("", xy=(total - 0.12, 0.72), xytext=(0, 0.72),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.4))
    ax.text(total / 2, 0.42, "한 프레임  —  60fps 라면 16.7ms,  VR 90Hz 라면 11.1ms",
            color=DIM, fontsize=12, ha="center")

    ax.text(0, 3.0, "각 단계에 넣을 코드의 선택 = 초보와 숙련자의 차이",
            color=FG, fontsize=13, fontweight="bold")

    notes = [
        (2.6, LAB,  "Rigidbody 를 미는 코드 — 반드시 여기"),
        (5.0, GFX,  "입력 처리·게임 규칙 — 여기"),
        (7.4, GFX,  "다른 오브젝트를 '따라가는' 코드 — 여기"),
    ]
    for xn, c, t in notes:
        ax.annotate("", xy=(xn, 1.15), xytext=(xn, 0.05),
                    arrowprops=dict(arrowstyle="-", color=c, lw=1.2, ls=(0, (3, 3))))
        ax.text(xn, -0.12, t, color=c, fontsize=10.5, ha="center", va="top")

    ax.set_xlim(-0.3, total + 0.3); ax.set_ylim(-0.9, 3.5)
    ax.set_title("한 프레임의 실행 순서", loc="left", pad=12, fontsize=15)
    return save(fig, "w03-frame-anatomy")


# =====================================================================
# 4. 고정 타임스텝 — 물리는 프레임과 따로 돈다
# =====================================================================
def fig_fixed_timestep():
    fig, ax = plt.subplots(figsize=(11.8, 4.8)); clean(ax)

    T = 0.12
    fix = 0.02

    rows = [("60 fps", 1 / 60, 3.5, GFX), ("30 fps", 1 / 30, 2.3, VR)]
    for label, dt, y, c in rows:
        n = int(T / dt)
        for i in range(n):
            ax.add_patch(Rectangle((i * dt, y), dt * 0.93, 0.62,
                                   facecolor=c, alpha=0.22, edgecolor=c, lw=1.4))
            ax.text(i * dt + dt * 0.46, y + 0.31, "U", color=c, fontsize=10,
                    ha="center", va="center", family=CODE, fontweight="bold")
        ax.text(-0.004, y + 0.31, label, color=c, fontsize=12, ha="right",
                va="center", fontweight="bold")

    y = 1.0
    n = int(T / fix)
    for i in range(n):
        ax.add_patch(Rectangle((i * fix, y), fix * 0.93, 0.62,
                               facecolor=LAB, alpha=0.25, edgecolor=LAB, lw=1.4))
        ax.text(i * fix + fix * 0.46, y + 0.31, "F", color=LAB, fontsize=10,
                ha="center", va="center", family=CODE, fontweight="bold")
    ax.text(-0.004, y + 0.31, "FixedUpdate", color=LAB, fontsize=12, ha="right",
            va="center", fontweight="bold")

    ax.text(0, 4.55, "U = Update (프레임마다)          F = FixedUpdate (0.02초마다 고정)",
            color=DIM, fontsize=12, family=CODE)
    ax.text(0, 0.5,
            "프레임률이 바뀌어도 FixedUpdate 간격은 고정\n"
            "→ 어느 PC에서든 물리 계산 결과 동일",
            color=FG, fontsize=12.5, linespacing=1.9, va="top")

    ax.set_xlim(-0.028, T + 0.004); ax.set_ylim(-0.35, 4.9)
    ax.set_title("Update 와 FixedUpdate 의 서로 다른 시계", loc="left",
                 pad=12, fontsize=15)
    return save(fig, "w03-fixed-timestep")


# =====================================================================
# 5. AI 함정 #2 — deltaTime 을 빼먹으면
# =====================================================================
def fig_deltatime():
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.6))
    t = np.linspace(0, 3, 400)
    speed = 2.0

    # 잘못된 코드: 프레임마다 고정량 이동 → 프레임률에 비례
    ax = axes[0]
    style_axes(ax)
    for fps, c in ((60, GFX), (30, VR)):
        ax.plot(t, speed * fps / 60 * t, color=c, lw=3, label=f"{fps} fps")
    ax.set_title("transform.position += v", loc="left", color=TRAP,
                 fontsize=13.5, pad=10, family=CODE)
    ax.set_xlabel("시간 (초)"); ax.set_ylabel("이동 거리 (m)")
    ax.legend(loc="upper left")
    ax.text(0.12, 5.4, "빠른 PC 에서 두 배 속도", color=TRAP, fontsize=12.5,
            fontweight="bold")
    ax.set_ylim(0, 6.4)

    # 올바른 코드
    ax = axes[1]
    style_axes(ax)
    for fps, c, ls in ((60, GFX, "-"), (30, VR, (0, (5, 4)))):
        ax.plot(t, speed * t, color=c, lw=3, ls=ls, label=f"{fps} fps")
    ax.set_title("transform.position += v * Time.deltaTime", loc="left",
                 color=LAB, fontsize=13.5, pad=10, family=CODE)
    ax.set_xlabel("시간 (초)"); ax.set_ylabel("이동 거리 (m)")
    ax.legend(loc="upper left")
    ax.text(0.12, 5.4, "두 선이 완전히 겹침", color=LAB, fontsize=12.5,
            fontweight="bold")
    ax.set_ylim(0, 6.4)

    fig.text(0.5, -0.04,
             "AI 생성 코드에서 가장 흔히 누락되는 한 단어  —  "
             "\"내 컴퓨터에서는 되는데\" 문제의 주요 원인",
             color=FG, fontsize=13, ha="center", fontweight="bold")
    return save(fig, "w03-deltatime", pad=0.36)


# =====================================================================
# 6. motion-to-photon — 고개를 돌리고 화면이 바뀌기까지
# =====================================================================
def fig_motion_to_photon():
    fig, ax = plt.subplots(figsize=(12.0, 4.4)); clean(ax)

    parts = [
        ("센서 샘플링",   2.0, "#4d9cff"),
        ("센서 융합·예측", 2.5, GFX),
        ("게임 로직",     4.0, LAB),
        ("렌더링",       6.0, VR),
        ("전송·왜곡보정", 2.5, WARN),
        ("디스플레이 점등", 3.0, "#b07dff"),
    ]
    x = 0.0
    Y, H = 1.5, 0.9
    for name, ms, c in parts:
        ax.add_patch(Rectangle((x, Y), ms - 0.08, H, facecolor=c, alpha=0.28,
                               edgecolor=c, lw=1.8, zorder=4))
        ax.text(x + (ms - 0.08) / 2, Y + H * 0.58, name, color=c, fontsize=10.5,
                fontweight="bold", ha="center", va="center", zorder=6)
        ax.text(x + (ms - 0.08) / 2, Y + H * 0.2, f"{ms:g} ms", color=DIM,
                fontsize=9.5, ha="center", va="center", family=CODE, zorder=6)
        x += ms

    total = x
    ax.annotate("", xy=(total, 0.95), xytext=(0, 0.95),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.4))
    ax.text(total / 2, 0.62, f"합계 {total:g} ms", color=FG, fontsize=12.5,
            ha="center", fontweight="bold")

    ax.plot([20, 20], [Y - 0.75, Y + H + 0.5], color=TRAP, lw=2.2, ls=(0, (5, 3)))
    ax.text(20.3, Y + H + 0.55, "20 ms — 이 선을 넘으면\n대부분의 사람이 멀미",
            color=TRAP, fontsize=11.5, va="bottom", linespacing=1.7)

    ax.text(0, Y + H + 0.95, "고개 회전부터 해당 장면의 화면 표시까지",
            color=FG, fontsize=13, fontweight="bold")
    ax.text(0, 0.1,
            "높은 프레임률과 짧은 지연은 별개  —  "
            "90fps 여도 지연이 길면 멀미 발생",
            color=DIM, fontsize=12)

    ax.set_xlim(-0.5, 26); ax.set_ylim(-0.4, 3.9)
    ax.set_title("motion-to-photon latency", loc="left", pad=12, fontsize=15)
    return save(fig, "w03-motion-to-photon")


# =====================================================================
# 7. 프레임 예산 — 왜 11.1ms 인가
# =====================================================================
def fig_frame_budget():
    fig, ax = plt.subplots(figsize=(11.4, 4.6)); clean(ax)

    rows = [
        ("일반 게임 60 Hz", 16.7, 1, GFX, 3.0),
        ("VR 90 Hz",        11.1, 2, VR,  1.6),
    ]
    for label, budget, eyes, c, y in rows:
        ax.add_patch(Rectangle((0, y), budget, 0.85, facecolor=c, alpha=0.18,
                               edgecolor=c, lw=2.0))
        ax.text(-0.35, y + 0.42, label, color=c, fontsize=12.5, ha="right",
                va="center", fontweight="bold")
        ax.text(budget + 0.3, y + 0.42, f"{budget} ms", color=c, fontsize=12,
                va="center", family=CODE)
        if eyes == 2:
            ax.plot([budget / 2, budget / 2], [y, y + 0.85], color=c, lw=1.6,
                    ls=(0, (4, 3)))
            for i, t in enumerate(("왼쪽 눈", "오른쪽 눈")):
                ax.text(budget / 4 + i * budget / 2, y + 0.42, t, color=c,
                        fontsize=10.5, ha="center", va="center")

    ax.text(0, 0.85,
            "한 프레임에 같은 장면을 두 번 렌더링  →  실질 예산은 눈당 약 5.5 ms",
            color=TRAP, fontsize=13, fontweight="bold")
    ax.text(0, 0.25,
            "예산 초과 → 프레임 전체 지연, 헤드셋이 직전 프레임을 비틀어 대신 표시(재투영)\n"
            "그 순간 세상이 흔들림 — 12주차 최적화의 출발점",
            color=DIM, fontsize=11.5, linespacing=1.9, va="top")

    ax.set_xlim(-4.2, 19.5); ax.set_ylim(-0.75, 4.5)
    ax.set_title("VR 의 엄격한 프레임 예산", loc="left", pad=12, fontsize=15)
    return save(fig, "w03-frame-budget")


# =====================================================================
if __name__ == "__main__":
    import sys
    figs = [fig_scene_graph, fig_component, fig_frame_anatomy,
            fig_fixed_timestep, fig_deltatime, fig_motion_to_photon,
            fig_frame_budget]
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for f in figs:
        if only and only not in f.__name__:
            continue
        print(f"[{f.__name__}]")
        f()
    print("\n완료")
