"""
데이터리터러시 10·11주 manim 애니메이션 (에디토리얼 지면 팔레트)

렌더 : dataliteracy/figures/anim/render.py 참고
  .venv/Scripts/python.exe -m manim -r 1600,900 --fps 30 --media_dir dataliteracy/figures/anim/media \
      dataliteracy/figures/anim/d10_d11_anim.py RandomBalance

수식은 LaTeX 의존을 피하려고 전부 Text 로 그림 · 난수 시드 고정
"""
import numpy as np
from manim import *

BG, CARD, HAIR = "#f5f1e8", "#fbf8f1", "#cfc6b2"
INK, INK2, INK3 = "#1b1a17", "#4a463e", "#8a8476"
TEAL, MAG, RED, OLIVE, OCHRE = "#0d6b78", "#a3245e", "#c2401d", "#4f7a16", "#a8701a"
SANS, SERIF = "Pretendard", "Noto Serif KR"

config.background_color = BG


def kr(t, size=30, color=INK, w=NORMAL, **kw):
    return Text(t, font=SANS, font_size=size, color=color, weight=w, **kw)


def se(t, size=44, color=INK, **kw):
    return Text(t, font=SERIF, font_size=size, color=color, weight=BOLD, **kw)


def rule(y, x0=-7.1, x1=7.1, color=INK, sw=2):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=sw)


class RandomBalance(Scene):
    """자원자 모집 vs 동전 배정 — 숨은 특성이 어느 쪽으로 쏠리는가"""

    def grid_pos(self, cx, i, cols=6, gap=.42, top=1.05):
        return np.array([cx + (i % cols - (cols - 1) / 2) * gap, top - (i // cols) * gap, 0])

    def setup_groups(self):
        lt, rt = kr("실험군", 30, INK, BOLD).move_to([-3.6, 1.75, 0]), kr("대조군", 30, INK, BOLD).move_to([3.6, 1.75, 0])
        div = DashedLine([0, 2, 0], [0, -2.6, 0], color=HAIR)
        return lt, rt, div

    def construct(self):
        rng = np.random.default_rng(706)   # 자원자 80/17 · 무작위 24:24, 54/46 : 도해 기댓값과 근접한 시드
        n = 48
        hidden = np.array([1] * 24 + [0] * 24)
        rng.shuffle(hidden)
        def dot(h):
            return Circle(.15, color=INK if h else INK3, fill_color=INK if h else CARD, fill_opacity=1, stroke_width=2)
        dots = VGroup(*[dot(h) for h in hidden]).arrange_in_grid(4, 12, buff=.24).move_to([0, .1, 0])
        title = se("같은 48명 · 절반은 숨은 특성 보유", 42).to_edge(UP, buff=.5)
        legend = VGroup(dot(1).scale(.8), kr("동기 높음 (겉으로 안 보임)", 24, INK2), dot(0).scale(.8), kr("보통", 24, INK2)).arrange(RIGHT, buff=.2).to_edge(DOWN, buff=.55)
        self.play(FadeIn(title), LaggedStartMap(GrowFromCenter, dots, lag_ratio=.012), FadeIn(legend), run_time=1.6)
        self.wait(.8)

        # 자원자 모집
        t1 = se("① 자원자 모집 : 원하는 사람만 새 방식", 42, RED).to_edge(UP, buff=.5)
        lt, rt, div = self.setup_groups()
        self.play(ReplacementTransform(title, t1), FadeIn(lt), FadeIn(rt), Create(div), run_time=.9)
        vol = np.array([rng.random() < (.85 if h else .2) for h in hidden])
        l = r = 0
        anims = []
        for i, d in enumerate(dots):
            if vol[i]:
                anims.append(d.animate.move_to(self.grid_pos(-3.6, l))); l += 1
            else:
                anims.append(d.animate.move_to(self.grid_pos(3.6, r))); r += 1
        self.play(LaggedStart(*anims, lag_ratio=.02), run_time=2.2)
        fa, fb = hidden[vol].mean() * 100, hidden[~vol].mean() * 100
        na = se(f"{fa:.0f}%", 62, RED).move_to([-3.6, -1.75, 0]); nb = se(f"{fb:.0f}%", 62, RED).move_to([3.6, -1.75, 0])
        la = kr("동기 높은 사람 비율", 22, INK2).next_to(na, DOWN, buff=.08); lb = kr("동기 높은 사람 비율", 22, INK2).next_to(nb, DOWN, buff=.08)
        self.remove(legend)
        self.play(FadeIn(na, scale=1.2), FadeIn(nb, scale=1.2), FadeIn(la), FadeIn(lb), run_time=.7)
        self.wait(1.8)
        verdict = kr("새 방식 전에 이미 다른 두 집단 → 효과와 동기 구분 불가", 30, RED, BOLD).move_to([0, -3.35, 0])
        self.play(FadeIn(verdict, shift=UP * .1), run_time=.5); self.wait(1.8)

        # 동전 배정
        t2 = se("② 무작위 배정 : 한 명씩 동전 던지기", 42, OLIVE).to_edge(UP, buff=.5)
        grid = VGroup(*[d.copy() for d in dots]).arrange_in_grid(4, 12, buff=.24).move_to([0, .1, 0])
        self.play(ReplacementTransform(t1, t2), FadeOut(na), FadeOut(nb), FadeOut(la), FadeOut(lb), FadeOut(verdict),
                  LaggedStart(*[d.animate.move_to(g.get_center()) for d, g in zip(dots, grid)], lag_ratio=.006), run_time=1.3)
        # 한 명씩 독립 난수 — 수업 재현을 위해 시드 고정
        rand = np.array([rng.random() < .5 for _ in range(n)])
        coin = Circle(.42, color=OCHRE, fill_color=OCHRE, fill_opacity=.18, stroke_width=4).move_to([0, 2.05, 0])
        coin_t = se("?", 34, OCHRE).move_to(coin)
        self.play(FadeIn(coin), FadeIn(coin_t), run_time=.3)
        l = r = 0
        for i, d in enumerate(dots):
            head = rand[i]
            rt_ = 0.2 if i < 5 else 0.052
            label = se("앞" if head else "뒤", 30, OCHRE).move_to(coin)
            target = self.grid_pos(-3.6, l) if head else self.grid_pos(3.6, r)
            l, r = (l + 1, r) if head else (l, r + 1)
            self.play(Transform(coin_t, label), d.animate.move_to(target), run_time=rt_)
        fa, fb = hidden[rand].mean() * 100, hidden[~rand].mean() * 100
        na = se(f"{fa:.0f}%", 62, OLIVE).move_to([-3.6, -1.75, 0]); nb = se(f"{fb:.0f}%", 62, OLIVE).move_to([3.6, -1.75, 0])
        la = kr("동기 높은 사람 비율", 22, INK2).next_to(na, DOWN, buff=.08); lb = kr("동기 높은 사람 비율", 22, INK2).next_to(nb, DOWN, buff=.08)
        self.play(FadeOut(coin), FadeOut(coin_t), FadeIn(na, scale=1.2), FadeIn(nb, scale=1.2), FadeIn(la), FadeIn(lb), run_time=.6)
        verdict = kr("동전은 동기를 모름 → 측정 안 한 특성까지 비슷하게 분배", 30, OLIVE, BOLD).move_to([0, -3.35, 0])
        self.play(FadeIn(verdict, shift=UP * .1), run_time=.5)
        self.wait(3)


class NullDistribution(Scene):
    """A/A 반복 → 우연의 분포 → 관측값 바깥 면적 = p값"""

    def construct(self):
        rng = np.random.default_rng(62)   # 400회 중 9회(2.25%) · 수식값 2.2% 와 근접한 시드
        N, sims = 4200, 400
        diffs = (rng.binomial(N, .1081, sims) - rng.binomial(N, .1081, sims)) / N * 100   # 수식과 같은 합동 비율
        title = se("같은 버튼 2개로 실험 반복 (효과 0)", 42).to_edge(UP, buff=.45)
        sub = kr("집단당 4,200명 · 실험 1회 = 점 1개", 26, INK2).next_to(title, DOWN, buff=.14)
        self.play(FadeIn(title), FadeIn(sub), run_time=.7)
        ax = NumberLine(x_range=[-3, 3, 1], length=12.4, color=INK2, include_numbers=False, stroke_width=2).move_to([0, -2.55, 0])
        ticks = VGroup(*[kr(f"{v:+d}점" if v else "0", 22, INK2).next_to(ax.n2p(v), DOWN, buff=.14) for v in range(-3, 4)])
        cap = kr("B − A 클릭률 차이", 22, INK3).next_to(ax, DOWN, buff=.55)
        self.play(Create(ax), FadeIn(ticks), FadeIn(cap), run_time=.7)
        w = .1
        counts = {}
        dots = VGroup()
        h = .082
        def place(d):
            k = int(np.round(d / w))
            counts[k] = counts.get(k, 0) + 1
            return np.array([ax.n2p(k * w)[0], ax.n2p(0)[1] + h * (counts[k] - .3), 0])
        anims = []
        for i, d in enumerate(diffs):
            p = place(d)
            dd = Dot(p, radius=.037, color=TEAL)
            dots.add(dd)
            anims.append(dd)
        first, rest = anims[:8], anims[8:]
        counter = kr("실험 0회", 28, INK, BOLD).move_to([-5.2, 1.5, 0])
        self.add(counter)
        for i, d in enumerate(first):
            start = d.copy().move_to([d.get_x(), 1.9, 0])
            lab = kr(f"{diffs[i]:+.2f}점", 24, TEAL, BOLD).next_to(start, UP, buff=.08)
            self.add(lab)
            self.play(Transform(start, d), run_time=.32)
            self.remove(lab, start); self.add(d)
            c2 = kr(f"실험 {i+1}회", 28, INK, BOLD).move_to(counter); self.remove(counter); counter = c2; self.add(counter)
        batch = 20
        for j in range(0, len(rest), batch):
            part = rest[j:j + batch]
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .6) for d in part], lag_ratio=.05), run_time=.26)
            c2 = kr(f"실험 {min(8+j+batch, sims)}회", 28, INK, BOLD).move_to(counter); self.remove(counter); counter = c2; self.add(counter)
        msg = kr("효과 0 에서도 차이 발생 = 표본 변동", 30, TEAL, BOLD).move_to([-3.75, .95, 0]).align_to(counter, LEFT)
        self.play(FadeIn(msg), run_time=.5); self.wait(1.2)

        obs = 1.55
        lin = DashedLine(ax.n2p(obs), ax.n2p(obs) + UP * 2.45, color=RED, stroke_width=4)
        linl = DashedLine(ax.n2p(-obs), ax.n2p(-obs) + UP * 2.45, color=RED, stroke_width=3)
        lab = kr("실제 결과 +1.55점", 28, RED, BOLD).next_to(lin, UP, buff=.08)
        self.play(Create(lin), FadeIn(lab), run_time=.6)
        self.play(Create(linl), run_time=.4)
        outside = [d for d, v in zip(dots, diffs) if abs(v) >= obs]
        self.play(*[d.animate.set_color(RED).scale(1.5) for d in outside], run_time=.7)
        share = len(outside) / sims * 100
        res = VGroup(se(f"바깥 점 {len(outside)}개 / {sims}회 ≈ {share:.1f}%", 42, RED), kr("수식 계산값  p = 0.022", 28, INK2, BOLD)).arrange(DOWN, buff=.12, aligned_edge=LEFT).move_to([-3.2, 1.0, 0])
        self.play(FadeOut(msg), FadeOut(counter), FadeIn(res, shift=UP * .1), run_time=.6)
        self.wait(3.2)


class CIStack(Scene):
    """같은 실험 20번 → 95% 신뢰구간 20개 → 약 19개가 참값 포함"""

    def construct(self):
        rng = np.random.default_rng(31)   # 19/20 이 되는 시드
        N, pa, pb = 4200, .10, .12
        title = se("같은 실험 20번 · 95% 신뢰구간 20개", 42).to_edge(UP, buff=.42)
        self.play(FadeIn(title), run_time=.5)
        ax = NumberLine(x_range=[-1, 5, 1], length=8.9, color=INK2, stroke_width=2).move_to([2.35, -3.1, 0])
        ticks = VGroup(*[kr(f"{v:+d}점" if v else "0", 22, INK2).next_to(ax.n2p(v), DOWN, buff=.1) for v in range(-1, 6)])
        true_l = Line(ax.n2p(2), ax.n2p(2) + UP * 5.3, color=INK, stroke_width=3)
        true_t = kr("참값 +2점", 24, INK, BOLD).next_to(true_l, UP, buff=.04)
        zero = DashedLine(ax.n2p(0), ax.n2p(0) + UP * 5.25, color=INK3, stroke_width=2)
        self.play(Create(ax), FadeIn(ticks), Create(true_l), FadeIn(true_t), Create(zero), run_time=.8)
        hit = 0
        cnt = kr("포함 0 / 0", 34, OLIVE, BOLD).move_to([-5.2, 1.5, 0])
        self.add(cnt)
        for i in range(20):
            a, b = rng.binomial(N, pa) / N, rng.binomial(N, pb) / N
            d = (b - a) * 100
            s = np.sqrt(a * (1 - a) / N + b * (1 - b) / N) * 100
            lo, hi = d - 1.96 * s, d + 1.96 * s
            ok = lo <= 2 <= hi
            hit += ok
            y = ax.n2p(0)[1] + .3 + i * .248
            c = TEAL if ok else RED
            seg = Line([ax.n2p(lo)[0], y, 0], [ax.n2p(hi)[0], y, 0], color=c, stroke_width=6 if ok else 7)
            pt = Dot([ax.n2p(d)[0], y, 0], radius=.055, color=c)
            self.play(GrowFromCenter(seg), FadeIn(pt), run_time=.2 if i > 2 else .45)
            c2 = kr(f"포함 {hit} / {i+1}", 34, OLIVE, BOLD).move_to(cnt); self.remove(cnt); cnt = c2; self.add(cnt)
            if not ok:
                miss = kr("빗나간 구간", 24, RED, BOLD).next_to(seg, RIGHT if hi < 3.3 else LEFT, buff=.14)
                self.play(FadeIn(miss), run_time=.3); self.wait(.5)
        print("hit", hit)
        end = VGroup(kr("«95%» = 방법의 성공률", 26, INK, BOLD), kr("구간 하나의 확률 표현 아님", 22, INK2)).arrange(DOWN, buff=.1, aligned_edge=LEFT).move_to([-5.05, .35, 0])
        self.play(FadeIn(end), run_time=.5)
        self.wait(3)


class Peeking(Scene):
    """효과 0 실험 40개를 매일 확인 → 경계 터치 즉시 종료"""

    def construct(self):
        rng = np.random.default_rng(13)   # 조기 9개(22.5%) · 끝 2개(5%) · 시뮬레이션 평균과 근접한 시드
        K, days = 40, 14
        daily = 300
        a = rng.binomial(daily, .1, (K, days)).cumsum(1); b = rng.binomial(daily, .1, (K, days)).cumsum(1)
        n = daily * np.arange(1, days + 1)
        p = (a + b) / (2 * n); z = (b - a) / n / np.sqrt(p * (1 - p) * 2 / n)
        early = np.abs(z).max(1) > 1.96; final = np.abs(z[:, -1]) > 1.96
        title = se("효과 0 실험 40개를 매일 확인", 42).to_edge(UP, buff=.42)
        ax = Axes(x_range=[0, 14, 2], y_range=[-3.5, 3.5, 1.96], x_length=9.4, y_length=5.2, tips=False,
                  axis_config=dict(color=INK2, stroke_width=2, include_ticks=False)).move_to([1.95, -.55, 0])
        up = DashedLine(ax.c2p(0, 1.96), ax.c2p(14, 1.96), color=RED, stroke_width=3); dn = DashedLine(ax.c2p(0, -1.96), ax.c2p(14, -1.96), color=RED, stroke_width=3)
        lbl = kr("p < 0.05 경계", 24, RED, BOLD).next_to(up, UP, buff=.06)
        cap = kr("실험 일수 (1~14일)", 22, INK3).next_to(ax, DOWN, buff=.1)
        yl = kr("차이의 z값", 22, INK3).rotate(PI / 2).next_to(ax, LEFT, buff=.08)
        self.play(FadeIn(title), Create(ax), Create(up), Create(dn), FadeIn(lbl), FadeIn(cap), FadeIn(yl), run_time=1)
        lines = []
        for k in range(K):
            pts = [ax.c2p(0, 0)] + [ax.c2p(d + 1, z[k, d]) for d in range(days)]
            lines.append(VMobject(color=INK3, stroke_width=2, stroke_opacity=.55).set_points_as_corners(pts))
        cnt_stop = 0
        panel_t = kr("확인 1일 차", 26, INK2, BOLD).move_to([-5.35, 1.8, 0])
        n_stop = se("0개", 62, RED).move_to([-5.35, .9, 0]); n_lab = kr("중간에 «유의» 종료", 24, RED, BOLD).next_to(n_stop, DOWN, buff=.08)
        self.add(panel_t, n_stop, n_lab)
        stopped = np.zeros(K, bool); drawn = [[] for _ in range(K)]
        for d in range(days):
            segs, marks = [], []
            for k in range(K):
                if stopped[k]:
                    continue
                y0 = 0 if d == 0 else z[k, d - 1]; x0 = d
                c = RED if abs(z[k, d]) > 1.96 else INK3
                s = Line(ax.c2p(x0, y0), ax.c2p(d + 1, z[k, d]), color=c, stroke_width=3.5 if c == RED else 1.8, stroke_opacity=1 if c == RED else .6)
                segs.append(Create(s))
                if abs(z[k, d]) > 1.96:
                    stopped[k] = True; marks.append(Dot(ax.c2p(d + 1, z[k, d]), radius=.09, color=RED))
            self.play(*segs, run_time=.42, rate_func=linear)
            if marks:
                self.play(*[GrowFromCenter(m) for m in marks], run_time=.18)
            t = kr(f"확인 {d+1}일 차", 26, INK2, BOLD).move_to(panel_t); self.remove(panel_t); panel_t = t; self.add(panel_t)
            ns = se(f"{int(stopped.sum())}개", 62, RED).move_to(n_stop); self.remove(n_stop); n_stop = ns; self.add(n_stop)
        print("early", int(early.sum()), "final", int(final.sum()))
        res = VGroup(kr("끝에 1번만 확인", 24, TEAL, BOLD), se(f"{int(final.sum())}개", 62, TEAL)).arrange(DOWN, buff=.08).move_to([-5.35, -1.6, 0])
        self.play(FadeIn(res, shift=UP * .1), run_time=.6)
        msg = kr("약속한 5% = 2개", 24, INK, BOLD).move_to([-5.35, -3.05, 0])
        self.play(FadeIn(msg), run_time=.4)
        self.wait(3.2)
