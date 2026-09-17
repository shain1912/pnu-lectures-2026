"""
4주차 애니메이션 — 원근투영: 절두체가 정육면체로 눌린다

렌더:
  .venv/Scripts/python.exe -m manim -qm --media_dir figures/anim/media \
      figures/anim/w04_projection.py Projection

LaTeX 의존을 피하려고 수식은 전부 Text(monospace) 로 그린다.
"""
from manim import *

BG    = "#0b0d12"
FG    = "#e8ecf4"
DIM   = "#9aa4b8"
FAINT = "#5f6980"
GFX   = "#35d6e6"
VR    = "#ff5fa2"
TRAP  = "#ff5a4d"
LAB   = "#a8e05f"
WARN  = "#ffc44d"
LINE  = "#2a3040"

SANS = "Pretendard"
MONO = "Consolas"

config.background_color = BG


def kr(t, size=30, color=FG, **kw):
    return Text(t, font=SANS, font_size=size, color=color, **kw)


def code(t, size=26, color=GFX, **kw):
    return Text(t, font=MONO, font_size=size, color=color, **kw)


def flat(t, size=22, color=GFX):
    """3D 공간에 눕혀 놓는 라벨 (xz 평면, 카메라 쪽을 본다)."""
    return kr(t, size, color).rotate(PI / 2, RIGHT)


# ---------------------------------------------------------------- 절두체 파라미터
EYE = np.array([-3.2, 0.0, 0.0])   # 카메라 위치 (월드)
N, F = 1.5, 5.0                    # near / far (카메라로부터의 깊이)
H = 0.6                            # near 평면 반높이
S = 1.3                            # NDC 정육면체 반변
CX = 3.25                          # 정육면체 중심의 깊이 위치

A = (F + N) / (F - N)
B = 2 * F * N / (F - N)


def ndc_z(d):
    """뷰 공간 깊이 d -> NDC 깊이 [-1, 1]. 1/d 에 비례하는 비선형 사상."""
    return A - B / d


def squash(p):
    """월드 점 p 를 '눌린 뒤' 위치로 보내기."""
    d, y, z = p[0] - EYE[0], p[1] - EYE[1], p[2] - EYE[2]
    half = H * d / N                       # 그 깊이에서의 절두체 반높이
    return EYE + np.array([CX + S * ndc_z(d), S * y / half, S * z / half])


def register(mob):
    for m in mob.family_members_with_points():
        m.src = m.points.copy()
        m.dst = np.array([squash(pt) for pt in m.points])


def apply_morph(mob, t):
    for m in mob.family_members_with_points():
        m.set_points(interpolate(m.src, m.dst, t))


def box(center_d, side, color, op=0.30):
    c = Cube(side_length=side, fill_color=color, fill_opacity=op,
             stroke_color=color, stroke_width=2.0)
    c.move_to(EYE + np.array([center_d, 0.0, 0.0]))
    return c


def bar(center_d, half_len, z0, color=WARN):
    o = EYE + np.array([center_d, 0.0, z0])
    return Line(o + np.array([0, 0, -half_len]), o + np.array([0, 0, half_len]),
                color=color, stroke_width=7)


class Projection(ThreeDScene):
    def construct(self):
        # ============================================================ 0. 제목
        title = kr("원근투영", 46)
        sub = kr("절두체 → 정육면체 변환", 28, GFX).next_to(title, DOWN, 0.35)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(1.8)
        self.play(FadeOut(title), FadeOut(sub), run_time=0.6)

        # ============================================================ 1. 절두체
        self.set_camera_orientation(phi=68 * DEGREES, theta=-76 * DEGREES, zoom=1.0)

        eye = Dot3D(EYE, color=WARN, radius=0.10)
        eye_lab = flat("카메라", 22, WARN).move_to(EYE + np.array([0.05, 0, -0.55]))
        sight = DashedLine(EYE, EYE + np.array([F + 0.4, 0, 0]),
                           color=FAINT, stroke_width=2, dash_length=0.12)

        def quad(d):
            h = H * d / N
            pts = [EYE + np.array([d, sy * h, sz * h])
                   for sy, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            return Polygon(*pts, color=GFX, stroke_width=2.5,
                           fill_color=GFX, fill_opacity=0.09)

        near_q, far_q = quad(N), quad(F)
        edges = VGroup(*[
            Line(near_q.get_vertices()[i], far_q.get_vertices()[i],
                 color=GFX, stroke_width=2.2)
            for i in range(4)
        ])
        near_lab = flat("near", 22, GFX).move_to(EYE + np.array([N - 0.95, 0, -1.08]))
        far_lab = flat("far", 22, GFX).move_to(EYE + np.array([F + 0.42, 0, -2.22]))

        cap = kr("카메라가 보는 범위 = 절두체(frustum)", 28, GFX).to_edge(UP, buff=0.45)
        self.add_fixed_in_frame_mobjects(cap)

        self.play(FadeIn(eye), FadeIn(eye_lab), Create(sight), FadeIn(cap), run_time=1.0)
        self.play(Create(near_q), FadeIn(near_lab), run_time=0.9)
        self.play(Create(far_q), FadeIn(far_lab), Create(edges), run_time=1.4)
        self.wait(1.4)

        # ============================================================ 2. 같은 크기
        cube_n = box(2.0, 0.45, VR)
        cube_f = box(4.2, 0.45, VR)
        bar_n = bar(2.0, 0.24, -0.52)
        bar_f = bar(4.2, 0.24, -0.52)

        cap2 = kr("두 물체의 실제 크기는 동일", 28, VR).to_edge(UP, buff=0.45)
        self.add_fixed_in_frame_mobjects(cap2)
        self.play(FadeOut(cap), FadeIn(cap2),
                  FadeIn(cube_n), FadeIn(cube_f), run_time=0.9)
        self.play(GrowFromCenter(bar_n), GrowFromCenter(bar_f), run_time=0.7)

        note = kr("한 변 0.45  ·  깊이만 차이", 24, WARN).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(note)
        self.play(FadeIn(note), run_time=0.5)
        self.play(Indicate(bar_n, color=WARN, scale_factor=1.3),
                  Indicate(bar_f, color=WARN, scale_factor=1.3), run_time=1.1)
        self.wait(0.6)
        self.play(Indicate(bar_n, color=WARN, scale_factor=1.3),
                  Indicate(bar_f, color=WARN, scale_factor=1.3), run_time=1.1)
        self.wait(1.4)

        # ============================================================ 3. 눌림
        cap3 = kr("투영 행렬 + 원근 나눗셈", 28, WARN).to_edge(UP, buff=0.45)
        self.add_fixed_in_frame_mobjects(cap3)
        eq = code("(x, y, z, w)  ->  (x/w, y/w, z/w)   in  [-1, 1]", 24, WARN)
        eq.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(eq)
        self.play(FadeOut(cap2), FadeIn(cap3), FadeOut(note), FadeIn(eq),
                  FadeOut(near_lab), FadeOut(far_lab), FadeOut(sight), run_time=0.9)

        grp = VGroup(near_q, far_q, edges, cube_n, cube_f, bar_n, bar_f)
        register(grp)
        t = ValueTracker(0.0)
        grp.add_updater(lambda m: apply_morph(m, t.get_value()))
        self.play(t.animate.set_value(1.0), run_time=5.0, rate_func=smooth)
        grp.clear_updaters()
        apply_morph(grp, 1.0)

        m1 = flat("-1", 22, GFX).move_to(EYE + np.array([CX - S - 0.30, 0, -1.98]))
        p1 = flat("+1", 22, GFX).move_to(EYE + np.array([CX + S + 0.30, 0, -1.98]))
        cap4 = kr("절두체 → 정육면체 완료", 28, GFX).to_edge(UP, buff=0.45)
        self.add_fixed_in_frame_mobjects(cap4)
        self.play(FadeOut(cap3), FadeIn(cap4), FadeIn(m1), FadeIn(p1), run_time=0.8)
        self.wait(0.6)
        self.move_camera(theta=-58 * DEGREES, run_time=2.6)
        self.wait(0.6)

        # ============================================================ 4. 결과
        cap5 = kr("먼 쪽일수록 크게 눌림", 28, TRAP).to_edge(UP, buff=0.45)
        self.add_fixed_in_frame_mobjects(cap5)
        self.play(FadeOut(cap4), FadeIn(cap5), FadeOut(eq), run_time=0.6)
        self.play(Indicate(bar_n, color=WARN, scale_factor=1.25),
                  Indicate(bar_f, color=TRAP, scale_factor=1.25), run_time=1.1)

        verdict = kr("원근 효과의 원인 = 이 눌림", 32, FG).to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(verdict)
        self.play(FadeIn(verdict, shift=UP * 0.2), run_time=0.8)
        self.wait(2.6)

        # ============================================================ 5. 깊이 비선형
        self.play(*[FadeOut(m) for m in (grp, eye, eye_lab, m1, p1, cap5, verdict)],
                  run_time=0.8)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=1.0)

        cap6 = kr("깊이 값도 같은 방식으로 눌림", 30, TRAP).to_edge(UP, buff=0.5)
        self.play(FadeIn(cap6), run_time=0.6)

        L, ty, by = 5.2, 1.35, -1.15
        ax_top = Line([-L, ty, 0], [L, ty, 0], color=GFX, stroke_width=3)
        ax_bot = Line([-L, by, 0], [L, by, 0], color=TRAP, stroke_width=3)
        lab_top = kr("뷰 공간 깊이  —  균일", 22, GFX).next_to(ax_top, UP, 0.22)
        lab_bot = kr("NDC 깊이  —  near 쪽에 밀집", 22, TRAP).next_to(ax_bot, DOWN, 0.22)
        n_lab = code("near", 20, DIM).next_to(ax_top.get_start(), LEFT, 0.2)
        f_lab = code("far", 20, DIM).next_to(ax_top.get_end(), RIGHT, 0.2)
        m1b = code("-1", 20, DIM).next_to(ax_bot.get_start(), LEFT, 0.2)
        p1b = code("+1", 20, DIM).next_to(ax_bot.get_end(), RIGHT, 0.2)

        self.play(Create(ax_top), Create(ax_bot), run_time=0.8)
        self.play(FadeIn(lab_top), FadeIn(lab_bot), FadeIn(n_lab), FadeIn(f_lab),
                  FadeIn(m1b), FadeIn(p1b), run_time=0.6)

        ds = [N + i * (F - N) / 10 for i in range(11)]
        tops, bots, links = VGroup(), VGroup(), VGroup()
        for d in ds:
            xt = -L + 2 * L * (d - N) / (F - N)
            xb = L * ndc_z(d)
            tops.add(Line([xt, ty - 0.13, 0], [xt, ty + 0.13, 0],
                          color=GFX, stroke_width=3))
            bots.add(Line([xb, by - 0.13, 0], [xb, by + 0.13, 0],
                          color=TRAP, stroke_width=3))
            links.add(Line([xt, ty - 0.13, 0], [xb, by + 0.13, 0],
                           color=FAINT, stroke_width=1.4, stroke_opacity=0.7))

        self.play(LaggedStart(*[FadeIn(m) for m in tops], lag_ratio=0.06), run_time=1.0)
        self.play(LaggedStart(*[Create(m) for m in links], lag_ratio=0.06),
                  LaggedStart(*[FadeIn(m) for m in bots], lag_ratio=0.06), run_time=1.9)
        self.wait(1.0)

        crowd = SurroundingRectangle(VGroup(*bots[5:]), color=WARN,
                                     stroke_width=2.5, buff=0.14)
        crowd_lab = kr("먼 절반 전체가 이 구간에 밀집", 22, WARN).next_to(crowd, DOWN, 0.28)
        self.play(Create(crowd), FadeIn(crowd_lab), run_time=0.9)
        self.wait(1.8)

        tail = kr("near = 0.01 설정 시 먼 곳의 깊이 구분 불가", 26, FG)
        tail2 = kr("z-fighting 의 출발점", 28, TRAP)
        tg = VGroup(tail, tail2).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.42)
        self.play(FadeOut(crowd_lab), FadeIn(tg), run_time=0.8)
        self.wait(3.0)
