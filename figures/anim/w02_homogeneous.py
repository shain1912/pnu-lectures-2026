"""
2주차 애니메이션 — 동차좌표: 이동을 선형변환으로 만드는 법

렌더:
  .venv/Scripts/python.exe -m manim -qh figures/anim/w02_homogeneous.py Homogeneous

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
WARN  = "#ffc44d"
LINE  = "#2a3040"

SANS = "Pretendard"
MONO = "Consolas"

config.background_color = BG


def kr(t, size=30, color=FG, **kw):
    return Text(t, font=SANS, font_size=size, color=color, **kw)


def code(t, size=26, color=GFX, **kw):
    return Text(t, font=MONO, font_size=size, color=color, **kw)


class Homogeneous(ThreeDScene):
    def construct(self):
        # ------------------------------------------------ 0. 제목
        title = kr("이동은 왜 선형변환이 아닌가", 44)
        sub = kr("한 차원 추가로 해결하는 방법", 26, DIM).next_to(title, DOWN, 0.35)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(sub), run_time=0.6)

        # ------------------------------------------------ 1. 2D 평면
        plane = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-3.5, 3.5, 1],
            background_line_style={"stroke_color": LINE, "stroke_width": 1.2,
                                   "stroke_opacity": 0.7},
            axis_config={"stroke_color": FAINT, "stroke_width": 2},
        )
        tri_pts = [np.array([0.3, 0.3, 0]), np.array([2.2, 0.5, 0]), np.array([1.1, 2.1, 0])]
        tri = Polygon(*tri_pts, color=GFX, fill_color=GFX, fill_opacity=0.28, stroke_width=3)
        origin = Dot(ORIGIN, color=WARN, radius=0.11)
        olabel = kr("원점", 20, WARN).next_to(origin, DOWN + LEFT, 0.15)

        self.play(Create(plane), run_time=1.0)
        self.play(FadeIn(tri), FadeIn(origin), FadeIn(olabel), run_time=0.7)
        self.wait(0.5)

        # ------------------------------------------------ 2. 회전 — 원점은 제자리
        cap = kr("회전 · 스케일 — 원점은 제자리", 28, GFX).to_edge(UP, buff=0.5)
        self.play(FadeIn(cap), run_time=0.5)
        self.play(Rotate(tri, angle=PI / 2, about_point=ORIGIN), run_time=1.6)
        self.play(Indicate(origin, color=WARN, scale_factor=1.6), run_time=0.8)
        self.play(Rotate(tri, angle=-PI / 2, about_point=ORIGIN), run_time=1.0)
        self.wait(0.4)

        # ------------------------------------------------ 3. 이동 — 원점이 움직인다
        cap2 = kr("이동 — 원점 이동", 28, TRAP).to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(cap, cap2), run_time=0.5)

        shift_v = np.array([2.4, -1.4, 0])
        ghost = tri.copy().set_stroke(opacity=0.35).set_fill(opacity=0.08)
        oghost = origin.copy().set_opacity(0.35)
        self.add(ghost, oghost)
        self.play(tri.animate.shift(shift_v), origin.animate.shift(shift_v),
                  olabel.animate.shift(shift_v), run_time=1.6)
        self.play(Indicate(origin, color=TRAP, scale_factor=1.8), run_time=0.9)

        verdict = kr("선형변환 : 원점 고정", 26, FG)
        verdict2 = kr("이동 : 원점 이동  →  2×2 행렬로 표현 불가", 26, TRAP)
        vg = VGroup(verdict, verdict2).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(vg), run_time=0.8)
        self.wait(1.8)

        self.play(FadeOut(vg), FadeOut(ghost), FadeOut(oghost),
                  tri.animate.shift(-shift_v), origin.animate.shift(-shift_v),
                  olabel.animate.shift(-shift_v), run_time=1.0)

        # ------------------------------------------------ 4. 3차원으로 들어올리기
        cap3 = kr("해결 — 한 차원 추가", 28, LAB_ := WARN).to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(cap2, cap3), run_time=0.5)
        self.add_fixed_in_frame_mobjects(cap3)

        lift = kr("(x, y)  →  (x, y, 1)", 30, GFX).to_edge(DOWN, buff=0.6)
        self.add_fixed_in_frame_mobjects(lift)
        self.play(FadeIn(lift), run_time=0.6)

        self.play(FadeOut(olabel), run_time=0.3)
        self.move_camera(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=0.78, run_time=2.2)

        # w = 1 평면
        w1 = Rectangle(width=12, height=7, stroke_color=GFX, stroke_width=2,
                       fill_color=GFX, fill_opacity=0.07).shift(OUT * 1.0)
        w1_label = kr("w = 1 평면", 22, GFX).rotate(PI / 2, RIGHT)
        w1_label.move_to(np.array([-4.2, -2.6, 1.25]))

        self.play(tri.animate.shift(OUT * 1.0), FadeIn(w1), FadeIn(w1_label), run_time=1.8)
        self.wait(0.6)

        # w 축
        warrow = Arrow3D(start=ORIGIN, end=OUT * 2.2, color=WARN, thickness=0.014)
        wlab = kr("w", 26, WARN).rotate(PI / 2, RIGHT).move_to(np.array([0.35, 0, 2.35]))
        self.play(GrowFromPoint(warrow, ORIGIN), FadeIn(wlab), run_time=0.9)
        self.wait(0.8)

        # ------------------------------------------------ 5. 3D 전단 = 2D 이동
        cap4 = kr("3차원에서의 전단(shear)", 28, VR).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(cap4)
        self.play(FadeOut(cap3), FadeIn(cap4), run_time=0.5)

        shear = np.array([
            [1, 0, 2.4],
            [0, 1, -1.4],
            [0, 0, 1],
        ])
        ghost3 = tri.copy().set_stroke(opacity=0.3).set_fill(opacity=0.07)
        self.add(ghost3)
        self.play(ApplyMatrix(shear, tri), run_time=2.0)
        self.wait(0.6)

        note = kr("w=1 평면 위에서는 옆으로 밀린 것 = 이동", 24, VR).to_edge(DOWN, buff=0.6)
        self.add_fixed_in_frame_mobjects(note)
        self.play(FadeOut(lift), FadeIn(note), run_time=0.7)
        self.wait(1.2)

        # ------------------------------------------------ 6. 위에서 내려다보면
        cap5 = kr("다시 위에서 내려다보면 — 단순 이동", 28, GFX).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(cap5)
        self.play(FadeOut(cap4), FadeIn(cap5), FadeOut(note), run_time=0.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=2.4)
        self.wait(1.2)

        # ------------------------------------------------ 7. 4×4 행렬
        self.play(*[FadeOut(m) for m in (plane, tri, ghost3, origin, w1, w1_label,
                                         warrow, wlab, cap5)], run_time=0.9)

        mat = code(
            "┌                 ┐\n"
            "│ 1  0  0   tx │\n"
            "│ 0  1  0   ty │\n"
            "│ 0  0  1   tz │\n"
            "│ 0  0  0   1  │\n"
            "└                 ┘",
            26, GFX,
        )
        cap6 = kr("이동 · 회전 · 스케일 · 투영이", 28, FG)
        cap7 = kr("모두 같은 4×4 곱셈으로 통일", 34, GFX)
        cg = VGroup(cap6, cap7).arrange(DOWN, buff=0.2)
        grp = VGroup(mat, cg).arrange(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(grp)
        self.play(FadeIn(mat, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(cg), run_time=0.8)
        self.wait(2.0)

        tail = kr("점은 w=1  ·  방향은 w=0", 26, WARN).next_to(grp, DOWN, 0.6)
        self.add_fixed_in_frame_mobjects(tail)
        self.play(FadeIn(tail), run_time=0.7)
        self.wait(2.2)
