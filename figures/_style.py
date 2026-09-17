"""
컴퓨터그래픽스 (VF3500076) · 도해 공통 스타일

슬라이드 테마(slides/_shared/theme.css)와 색·폰트를 정확히 일치시킨다.
SVG 는 텍스트를 path 로 변환해 내보내므로 어느 PC에서 열어도 한글이 깨지지 않는다.

사용:
    from _style import *
    fig, ax = canvas(figsize=(9, 5))
    ...
    save(fig, "w02-dot-product")
"""
from __future__ import annotations

import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

OUT = pathlib.Path(__file__).parent / "out"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- 색 체계
BG      = "#0b0d12"   # 슬라이드 배경
BG_SOFT = "#12151d"
CARD    = "#171b25"
LINE    = "#2a3040"
FG      = "#e8ecf4"
DIM     = "#9aa4b8"
FAINT   = "#5f6980"

GFX  = "#35d6e6"   # 그래픽스 이론
VR   = "#ff5fa2"   # 지각 / HMD
TRAP = "#ff5a4d"   # AI 함정
LAB  = "#a8e05f"   # 실습
WARN = "#ffc44d"

AX_X, AX_Y, AX_Z = "#ff5a4d", "#a8e05f", "#4d9cff"   # Unity 축 색

# ---------------------------------------------------------------- 폰트
_installed = {f.name for f in fm.fontManager.ttflist}
SANS = next((n for n in ("Pretendard", "Pretendard Variable", "Malgun Gothic", "Gulim")
             if n in _installed), "sans-serif")
MONO = next((n for n in ("JetBrains Mono", "D2Coding", "Consolas")
             if n in _installed), "monospace")

# 모노 폰트에는 한글 글리프가 없다. 글리프 단위 폴백(matplotlib 3.6+)으로
# 영문·숫자는 모노, 한글은 Pretendard 로 자동 분배된다.
CODE = [MONO, SANS]

plt.rcParams.update({
    "font.family":        SANS,
    "font.size":          13,
    "axes.unicode_minus": False,          # 한글 폰트의 음수 기호 깨짐 방지
    "svg.fonttype":       "path",         # 폰트 미설치 PC에서도 안 깨지게
    "figure.facecolor":   BG,
    "axes.facecolor":     BG,
    "savefig.facecolor":  BG,
    "text.color":         FG,
    "axes.labelcolor":    DIM,
    "axes.edgecolor":     LINE,
    "xtick.color":        FAINT,
    "ytick.color":        FAINT,
    "grid.color":         "#1e2431",
    "grid.linewidth":     0.8,
    "axes.titlesize":     15,
    "axes.titleweight":   "bold",
    "axes.titlecolor":    FG,
    "legend.frameon":     False,
    "legend.labelcolor":  DIM,
    "lines.solid_capstyle": "round",
})


def canvas(figsize=(9, 5), ncols=1, nrows=1, **kw):
    """기본 축 스타일이 적용된 figure/axes."""
    fig, ax = plt.subplots(nrows, ncols, figsize=figsize, **kw)
    for a in (ax.ravel() if hasattr(ax, "ravel") else [ax]):
        style_axes(a)
    return fig, ax


def style_axes(a, grid=True, box=False):
    a.set_facecolor(BG)
    for side in ("top", "right"):
        a.spines[side].set_visible(box)
    for side in ("left", "bottom"):
        a.spines[side].set_color(LINE)
        a.spines[side].set_linewidth(1.1)
    if grid:
        a.grid(True, alpha=0.55, linewidth=0.8)
        a.set_axisbelow(True)
    return a


def clean(a):
    """좌표축 눈금·테두리를 모두 없앤 도해용 축."""
    a.set_facecolor(BG)
    a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values():
        s.set_visible(False)
    a.grid(False)
    return a


def vec(a, origin, v, color, label=None, lw=2.6, ls="-", alpha=1.0,
        label_off=(0.12, 0.12), fs=13, zorder=5, head=0.22):
    """원점에서 v 만큼 뻗는 화살표 + 라벨."""
    a.annotate("", xy=(origin[0] + v[0], origin[1] + v[1]), xytext=origin,
               arrowprops=dict(arrowstyle="-|>,head_width=%.2f,head_length=%.2f" % (head * 0.62, head),
                               color=color, lw=lw, linestyle=ls, alpha=alpha,
                               shrinkA=0, shrinkB=0),
               zorder=zorder)
    if label:
        a.text(origin[0] + v[0] + label_off[0], origin[1] + v[1] + label_off[1], label,
               color=color, fontsize=fs, fontweight="bold", zorder=zorder + 1)


def note(a, x, y, text, color=DIM, fs=11, **kw):
    return a.text(x, y, text, color=color, fontsize=fs, **kw)


def badge(a, x, y, text, color, fs=11.5, pad=0.42):
    """색 배경 라벨."""
    return a.text(x, y, text, color=color, fontsize=fs, fontweight="bold",
                  ha="center", va="center", zorder=20,
                  bbox=dict(boxstyle=f"round,pad={pad}", fc=BG_SOFT, ec=color, lw=1.3))


def save(fig, name, svg=True, png=True, dpi=200, pad=0.28):
    """out/ 에 SVG(슬라이드용) + PNG(인쇄·미리보기용) 저장."""
    made = []
    if svg:
        p = OUT / f"{name}.svg"
        fig.savefig(p, format="svg", bbox_inches="tight", pad_inches=pad)
        made.append(p)
    if png:
        p = OUT / f"{name}.png"
        fig.savefig(p, format="png", dpi=dpi, bbox_inches="tight", pad_inches=pad)
        made.append(p)
    plt.close(fig)
    for p in made:
        print(f"  -> {p.relative_to(OUT.parent.parent)}  ({p.stat().st_size // 1024} KB)")
    return made
