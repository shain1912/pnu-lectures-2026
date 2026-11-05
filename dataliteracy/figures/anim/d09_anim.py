"""데이터리터러시 9주 manim 애니메이션 (에디토리얼 지면 팔레트)
렌더 : .venv/Scripts/python.exe dataliteracy/figures/anim/render_d09.py
수식은 LaTeX 의존을 피하려고 Text 로 그림 · 난수 시드 고정"""
import csv, pathlib
import numpy as np
from manim import *

BG, CARD, HAIR = "#f5f1e8", "#fbf8f1", "#cfc6b2"
INK, INK2, INK3 = "#1b1a17", "#4a463e", "#8a8476"
TEAL, MAG, RED, OLIVE, OCHRE = "#0d6b78", "#a3245e", "#c2401d", "#4f7a16", "#a8701a"
SANS, SERIF = "Pretendard", "Noto Serif KR"
config.background_color = BG

_r = list(csv.DictReader(open(pathlib.Path(__file__).parents[2] / "data" / "ice_cream.csv", encoding="utf-8-sig")))
T = np.array([float(x["temp_c"]) for x in _r]); S = np.array([float(x["ice_cream_sales"]) for x in _r]); D = np.array([float(x["drownings"]) for x in _r])


def kr(t, size=30, color=INK, w=NORMAL, **kw):
    return Text(t, font=SANS, font_size=size, color=color, weight=w, **kw)


def se(t, size=44, color=INK, **kw):
    return Text(t, font=SERIF, font_size=size, color=color, weight=BOLD, **kw)


def temp_col(t):
    return interpolate_color(ManimColor(TEAL), ManimColor(RED), float(np.clip((t + 2) / 30, 0, 1)))


class Stratify(Scene):
    """전체 상관 → 기온 색칠 → 기온 효과 제거"""

    def construct(self):
        r = lambda a, b: float(np.corrcoef(a, b)[0, 1])
        ax = Axes(x_range=[0, 1600, 400], y_range=[0, 14, 2], x_length=7.6, y_length=4.9, tips=False,
                  axis_config=dict(color=INK2, stroke_width=2, include_ticks=False)).move_to([2.35, -.5, 0])
        xl = kr("아이스크림 판매량", 24, INK3).next_to(ax, DOWN, buff=.12); yl = kr("익사 사고", 24, INK3).rotate(PI / 2).next_to(ax, LEFT, buff=.12)
        title = se("두 숫자가 함께 움직이는 104주", 42).to_edge(UP, buff=.42)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), run_time=.9)
        dots = VGroup(*[Dot(ax.c2p(s, d), radius=.065, color=INK3) for s, d in zip(S, D)])
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=.012), run_time=1.5)
        m, b = np.polyfit(S, D, 1)
        line = Line(ax.c2p(S.min(), m * S.min() + b), ax.c2p(S.max(), m * S.max() + b), color=RED, stroke_width=5)
        val = se(f"r = {r(S, D):.2f}", 62, RED).move_to([-4.9, .9, 0])
        cap = kr("판매 금지 → 사고 감소?", 26, INK2, BOLD).next_to(val, DOWN, buff=.18)
        self.play(Create(line), FadeIn(val), run_time=.8); self.play(FadeIn(cap), run_time=.4); self.wait(1.4)

        t2 = se("숨은 변수 : 기온으로 점 색칠", 42, OCHRE).to_edge(UP, buff=.42)
        cold = kr("추운 주", 24, TEAL, BOLD); hot = kr("더운 주", 24, RED, BOLD)
        leg = VGroup(cold, hot).arrange(RIGHT, buff=.5).next_to(cap, DOWN, buff=.5)
        self.play(ReplacementTransform(title, t2), FadeOut(line),
                  *[d.animate.set_color(temp_col(t)) for d, t in zip(dots, T)], FadeIn(leg), run_time=1.2)
        self.wait(1.3)
        msg = kr("추운 주는 왼쪽 아래 · 더운 주는 오른쪽 위", 26, OCHRE, BOLD).move_to([0, -3.65, 0])
        self.play(FadeIn(msg), run_time=.4); self.wait(1.4)

        # 기온 효과 제거 : 잔차로 이동
        rs = S - np.polyval(np.polyfit(T, S, 1), T); rd = D - np.polyval(np.polyfit(T, D, 1), T)
        t3 = se("기온으로 설명되는 부분을 빼면", 42, OLIVE).to_edge(UP, buff=.42)
        ax2 = Axes(x_range=[-240, 240, 80], y_range=[-3.2, 3.2, 1], x_length=7.6, y_length=4.9, tips=False,
                   axis_config=dict(color=INK2, stroke_width=2, include_ticks=False)).move_to(ax)
        xl2 = kr("기온으로 설명 안 되는 판매량", 24, INK3).next_to(ax2, DOWN, buff=.12)
        yl2 = kr("기온으로 설명 안 되는 사고", 24, INK3).rotate(PI / 2).next_to(ax2, LEFT, buff=.12)
        val2 = se(f"r = {r(rs, rd):.2f}", 62, OLIVE).move_to(val)
        cap2 = kr("기온 효과를 빼면 관계 소멸", 26, OLIVE, BOLD).next_to(val2, DOWN, buff=.18)
        self.play(ReplacementTransform(t2, t3), FadeOut(msg), Transform(ax, ax2), Transform(xl, xl2), Transform(yl, yl2),
                  *[d.animate.move_to(ax2.c2p(a, c)).set_color(OLIVE) for d, a, c in zip(dots, rs, rd)],
                  ReplacementTransform(val, val2), ReplacementTransform(cap, cap2), FadeOut(leg), run_time=2.2)
        self.wait(3.2)


class KMeansSteps(Scene):
    """K-평균 : 중심 놓기 → 가까운 중심 선택 → 중심 이동 반복"""

    def construct(self):
        g = np.random.default_rng(5)
        C = np.array([[-2.6, 1.0], [2.7, 1.1], [.2, -1.5]])
        P = np.vstack([c + g.normal(0, .55, (22, 2)) for c in C])
        cols = [TEAL, MAG, OCHRE]
        title = se("K-평균 : 비슷한 것끼리 3그룹", 42).to_edge(UP, buff=.42)
        self.play(FadeIn(title), run_time=.5)
        off = np.array([1.75, -.35])
        pos = lambda p: np.array([p[0] + off[0], p[1] + off[1], 0])
        dots = VGroup(*[Dot(pos(p), radius=.085, color=INK3) for p in P])
        self.play(LaggedStartMap(GrowFromCenter, dots, lag_ratio=.01), run_time=.9)
        cent = np.array([[-1.0, 2.0], [-1.6, -1.6], [3.0, -1.7]])
        def star(p, c):
            return Square(.34, color=INK, fill_color=c, fill_opacity=1, stroke_width=3).rotate(PI / 4).move_to(pos(p))
        stars = VGroup(*[star(p, c) for p, c in zip(cent, cols)])
        step = kr("① 중심 3개를 아무 곳에", 28, INK, BOLD).move_to([-5.0, 1.5, 0]).align_on_border(LEFT, buff=.35)
        self.play(GrowFromCenter(stars), FadeIn(step), run_time=.7); self.wait(.8)
        it = kr("반복 0회", 26, INK2).move_to([-5.9, -.3, 0]).align_on_border(LEFT, buff=.35)
        self.add(it)
        for k in range(5):
            d = ((P[:, None] - cent[None]) ** 2).sum(2); lab = d.argmin(1)
            if k <= 1:
                s = kr("② 가장 가까운 중심 선택", 28, INK, BOLD).move_to(step).align_on_border(LEFT, buff=.35); self.remove(step); step = s; self.add(step)
            self.play(*[dt.animate.set_color(cols[l]) for dt, l in zip(dots, lab)], run_time=.65 if k < 2 else .3)
            newc = np.array([P[lab == j].mean(0) for j in range(3)])
            if k <= 1:
                s = kr("③ 그룹 평균으로 중심 이동", 28, INK, BOLD).move_to(step).align_on_border(LEFT, buff=.35); self.remove(step); step = s; self.add(step)
            self.play(*[st.animate.move_to(pos(p)) for st, p in zip(stars, newc)], run_time=.7 if k < 2 else .35)
            cent = newc
            i2 = kr(f"반복 {k+1}회", 26, INK2).move_to(it).align_on_border(LEFT, buff=.35); self.remove(it); it = i2; self.add(it)
        s = kr("④ 움직임 멈춤 → 완료", 28, OLIVE, BOLD).move_to(step).align_on_border(LEFT, buff=.35); self.remove(step); step = s; self.add(step)
        note = VGroup(kr("그룹 이름은 사람이 부여", 25, RED, BOLD), kr("정답 라벨 없음", 25, RED, BOLD)).arrange(DOWN, buff=.1, aligned_edge=LEFT).move_to([-5.2, -1.8, 0]).align_on_border(LEFT, buff=.35)
        self.play(FadeIn(note), run_time=.5); self.wait(3)


class Overfit(Scene):
    """복잡도 증가 : 학습 오차는 감소 · 검증 오차는 다시 상승"""

    def construct(self):
        g = np.random.default_rng(21)
        f = lambda x: .9 * np.sin(x * 1.3) + .15 * x
        xt = np.sort(g.uniform(-3, 3, 14)); yt = f(xt) + g.normal(0, .32, 14)
        xv = np.sort(g.uniform(-3, 3, 16)); yv = f(xv) + g.normal(0, .32, 16)
        ax = Axes(x_range=[-3.4, 3.4, 1], y_range=[-3, 3, 1], x_length=7.4, y_length=4.9, tips=False,
                  axis_config=dict(color=INK2, stroke_width=2, include_ticks=False)).move_to([2.5, -.5, 0])
        title = se("곡선을 복잡하게 만들수록", 42).to_edge(UP, buff=.42)
        self.play(FadeIn(title), Create(ax), run_time=.7)
        tr = VGroup(*[Dot(ax.c2p(a, b), radius=.09, color=TEAL) for a, b in zip(xt, yt)])
        leg1 = kr("학습 데이터 (모델이 본 것)", 24, TEAL, BOLD).move_to([-4.6, 1.75, 0]).align_on_border(LEFT, buff=.4)
        self.play(LaggedStartMap(GrowFromCenter, tr, lag_ratio=.03), FadeIn(leg1), run_time=.8)

        def curve(deg):
            z = np.polyfit(xt, yt, deg)
            xs = np.linspace(xt.min(), xt.max(), 260)
            ys = np.clip(np.polyval(z, xs), -2.95, 2.95)
            return VMobject(color=RED, stroke_width=5).set_points_as_corners([ax.c2p(a, b) for a, b in zip(xs, ys)]), z

        def mae(z, x, y):
            return float(np.mean(np.abs(np.polyval(z, x) - y)))

        rows = []
        y0 = .85
        cur = None
        for i, (deg, name) in enumerate([(1, "직선"), (5, "완만한 곡선"), (11, "구불구불한 곡선")]):
            c, z = curve(deg)
            lab = kr(f"{name} · 학습 오차 {mae(z, xt, yt):.2f}", 25, INK, BOLD).move_to([-4.6, y0 - i * .55, 0]).align_on_border(LEFT, buff=.4)
            if cur is None:
                self.play(Create(c), FadeIn(lab), run_time=1)
            else:
                self.play(Transform(cur, c), FadeIn(lab), run_time=1.1)
            cur = cur if cur is not None else c
            rows.append((deg, name, z, lab)); self.wait(.8)
        t2 = se("처음 보는 데이터로 시험", 42, MAG).to_edge(UP, buff=.42)
        va = VGroup(*[Dot(ax.c2p(a, b), radius=.09, color=MAG) for a, b in zip(xv, yv)])
        leg2 = kr("검증 데이터 (처음 본 것)", 24, MAG, BOLD).next_to(leg1, DOWN, buff=.08).align_to(leg1, LEFT)
        self.play(ReplacementTransform(title, t2), LaggedStartMap(GrowFromCenter, va, lag_ratio=.03), FadeIn(leg2), run_time=1)
        newrows = []
        best = min(rows, key=lambda q: mae(q[2], xv, yv))
        for i, (deg, name, z, lab) in enumerate(rows):
            e = mae(z, xv, yv)
            c = OLIVE if deg == best[0] else RED
            nl = VGroup(kr(f"{name}", 25, INK, BOLD), kr(f"학습 {mae(z, xt, yt):.2f} · 검증 {e:.2f}", 25, c, BOLD)).arrange(DOWN, buff=.04, aligned_edge=LEFT).move_to([-4.6, .35 - i * .95, 0]).align_on_border(LEFT, buff=.4)
            self.play(ReplacementTransform(lab, nl), run_time=.55); newrows.append(nl)
        print("overfit", [(d, round(mae(z, xt, yt), 2), round(mae(z, xv, yv), 2)) for d, n, z, l in rows])
        msg = kr("학습 점수만 좋음 = 문제집 답 암기", 28, RED, BOLD).move_to([0, -3.65, 0])
        self.play(FadeIn(msg), run_time=.5); self.wait(3.4)
