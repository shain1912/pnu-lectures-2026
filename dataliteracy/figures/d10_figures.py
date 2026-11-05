"""데이터리터러시 10주차 도해 — 가설·실험군/대조군·무작위 배정
실행 : .venv/Scripts/python.exe dataliteracy/figures/d10_figures.py
수치 근거 : dataliteracy/data/numbers_d10_d11.py · 교육용 합성 데이터"""
import csv, pathlib
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from _style_ed import *

DATA = pathlib.Path(__file__).parent.parent / "data"


def box(a, x, y, w, h, title, sub=None, color=FG, fc=CARD, fs=13, sfs=10.5, lw=1.4):
    a.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc=fc, ec=color, lw=lw))
    if sub:
        a.text(x + w/2, y + h*0.68, title, ha="center", va="center", fontsize=fs, fontweight="bold", color=color, fontfamily=SERIF)
        a.text(x + w/2, y + h*0.28, sub, ha="center", va="center", fontsize=sfs, color=DIM, linespacing=1.4)
    else:
        a.text(x + w/2, y + h/2, title, ha="center", va="center", fontsize=fs, fontweight="bold", color=color, fontfamily=SERIF)


def arrow(a, p, q, color=DIM, lw=1.8):
    a.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>,head_width=.28,head_length=.5", color=color, lw=lw, shrinkA=0, shrinkB=0))


def fig_before_after():
    rng = np.random.default_rng(10)
    d = np.arange(1, 29)
    season = 5 + 4.2 * (d > 13) * (1 - np.exp(-(d - 13) / 2.0))     # 시험 종료 후 앱 사용 증가
    ctrl = season + rng.normal(0, .16, 28)
    trt = season + .6 * (d >= 15) + rng.normal(0, .16, 28)
    naive = np.where(d < 15, ctrl, trt)
    fig, (l, r) = canvas(figsize=(11, 4.4), ncols=2, sharey=True)
    l.plot(d, naive, color=FG, lw=2.4)
    l.axvline(15, color=TRAP, lw=1.4, ls="--")
    l.text(15.4, 1.0, "버튼 교체", color=TRAP, fontsize=12, fontweight="bold")
    l.set_title("전후 비교 : 클릭률 약 2배", loc="left")
    l.text(1.5, 9.6, "버튼 효과로 보임", fontsize=12.5, color=DIM)
    r.plot(d, ctrl, color=FAINT, lw=2.4, label="대조군 : 기존 버튼 유지")
    r.plot(d[14:], trt[14:], color=GFX, lw=2.6, label="실험군 : 새 버튼")
    r.axvline(15, color=TRAP, lw=1.4, ls="--")
    r.axvspan(13, 17, color=WARN, alpha=.14, lw=0)
    r.text(13.1, 1.0, "시험 종료 시점", color=WARN, fontsize=12, fontweight="bold")
    r.annotate("실제 버튼 효과\n약 +0.6점", xy=(26, 9.4), xytext=(19.2, 5.2), fontsize=12.5, color=GFX, fontweight="bold",
               arrowprops=dict(arrowstyle="-", color=GFX, lw=1.2))
    r.set_title("대조군 추가 : 상승 대부분이 시기 효과", loc="left")
    r.legend(loc="upper left", fontsize=11)
    for a in (l, r):
        a.set_xlabel("일자"); a.set_ylim(0, 11.5); a.set_xlim(1, 28)
    l.set_ylabel("클릭률 (%)")
    fig.text(.995, -.02, "교육용 합성 데이터", ha="right", fontsize=10, color=FAINT)
    fig.tight_layout()
    return save(fig, "d10-before-after")


def fig_hypothesis():
    fig, a = plt.subplots(figsize=(11, 4.3)); clean(a); a.set_xlim(0, 11); a.set_ylim(0, 4.3)
    box(a, .1, 2.35, 5.2, 1.75, "귀무가설 H₀", "«차이 없음» · 기본 입장\n버튼 A와 B의 클릭률 동일", GFX, fs=16, sfs=12.5)
    box(a, 5.7, 2.35, 5.2, 1.75, "대립가설 H₁", "«차이 있음» · 확인하려는 주장\n버튼 B의 클릭률이 A와 상이", VR, fs=16, sfs=12.5)
    y = .85
    a.plot([.5, 10.5], [y, y], color=FG, lw=1.6)
    for x, t, s, c in [(1.7, "① 가설 선언", "데이터 수집 전", TRAP), (5.5, "② 데이터 수집", "기간·표본 고정", DIM), (9.3, "③ 판단", "H₀로 설명 가능한가?", DIM)]:
        a.add_patch(Circle((x, y), .1, fc=c, ec=c, zorder=4))
        a.text(x, y + .36, t, ha="center", fontsize=13, fontweight="bold", color=c)
        a.text(x, y - .42, s, ha="center", fontsize=11.5, color=DIM)
    return save(fig, "d10-hypothesis")


def people(a, cx, cy, n, frac, seed, color_hi, w=1.45, cols=7):
    rng = np.random.default_rng(seed)
    hi = int(round(n * frac)); flags = np.array([1] * hi + [0] * (n - hi)); rng.shuffle(flags)
    for i, f in enumerate(flags):
        x = cx - w/2 + (i % cols + .5) * w / cols
        y = cy - (i // cols) * w / cols
        a.add_patch(Circle((x, y), w / cols * .37, fc=color_hi if f else CARD, ec=color_hi if f else FAINT, lw=1))


def fig_assignment():
    fig, a = plt.subplots(figsize=(11, 4.6)); clean(a); a.set_xlim(0, 12); a.set_ylim(0, 4.9); a.set_aspect("equal")
    rows = [("자원자 모집", "원하는 사람만 처치", .81, .16, TRAP), ("사후 비교", "이미 쓴 집단 vs 안 쓴 집단", .70, .30, WARN), ("무작위 배정", "난수로 집단 결정", .50, .50, LAB)]
    for i, (t, s, f1, f2, c) in enumerate(rows):
        x0 = .1 + i * 4
        a.text(x0 + 1.85, 4.6, t, ha="center", fontsize=15, fontweight="bold", color=c, fontfamily=SERIF)
        a.text(x0 + 1.85, 4.2, s, ha="center", fontsize=11, color=DIM)
        a.text(x0 + .9, 3.72, "실험군", ha="center", fontsize=11.5, color=FG, fontweight="bold")
        a.text(x0 + 2.8, 3.72, "대조군", ha="center", fontsize=11.5, color=FG, fontweight="bold")
        people(a, x0 + .9, 3.32, 28, f1, 3 + i, FG, w=1.6)
        people(a, x0 + 2.8, 3.32, 28, f2, 13 + i, FG, w=1.6)
        a.text(x0 + .9, 1.42, f"{f1*100:.0f}%", ha="center", fontsize=19, fontweight="bold", color=c, fontfamily=SERIF)
        a.text(x0 + 2.8, 1.42, f"{f2*100:.0f}%", ha="center", fontsize=19, fontweight="bold", color=c, fontfamily=SERIF)
        verdict = {0: "처치 전부터 집단 차이 큼", 1: "교란 통제 불가", 2: "숨은 특성까지 균형"}[i]
        a.text(x0 + 1.85, .85, verdict, ha="center", fontsize=12.5, color=c, fontweight="bold")
        if i: a.plot([x0 - .15, x0 - .15], [.7, 4.8], color=LINE, lw=1)
    a.add_patch(Circle((.45, .3), .08, fc=FG, ec=FG)); a.text(.6, .3, "숨은 특성 있음 (예 : 동기 높음)", fontsize=11, va="center", color=DIM)
    a.add_patch(Circle((4.2, .3), .08, fc=CARD, ec=FAINT)); a.text(4.35, .3, "없음", fontsize=11, va="center", color=DIM)
    a.text(11.9, .3, "숫자 = 집단 안의 동기 높은 사람 비율 (모형 기댓값)", ha="right", fontsize=11, va="center", color=FAINT)
    return save(fig, "d10-assignment")


def fig_volunteer_bias():
    fig, a = canvas(figsize=(9.6, 3.9))
    labs = ["자원자 모집", "사후 비교", "무작위 배정"]; vals = [8.5, 6.0, 2.0]; cols = [TRAP, WARN, LAB]
    y = [2, 1, 0]
    a.barh(y, vals, color=cols, height=.56)
    for yy, v, c in zip(y, vals, cols):
        a.text(v + .15, yy, f"+{v:.1f}점", va="center", fontsize=16, fontweight="bold", color=c, fontfamily=SERIF)
    a.axvline(2, color=FG, lw=1.8, ls="--")
    a.text(2.08, 2.5, "실제 효과 +2점", fontsize=12.5, color=FG, fontweight="bold")
    a.set_yticks(y, labs, fontsize=13.5); a.tick_params(axis="y", length=0, colors=FG)
    a.set_xlim(0, 10.5); a.set_ylim(-.5, 2.85); a.set_xlabel("추정된 효과 (클릭률 %포인트)"); a.grid(axis="y", visible=False)
    return save(fig, "d10-volunteer-bias")


def fig_unit():
    fig, a = plt.subplots(figsize=(11, 4.3)); clean(a); a.set_xlim(0, 11); a.set_ylim(0, 4.3)
    rows = [
        ("페이지 열 때마다", "같은 학생이 A·B 모두 경험", ["A", "B", "A", "B", "B"], TRAP, "단위 붕괴 → 효과 희석"),
        ("학생 1명 고정", "한 번 받은 버전 유지", ["B", "B", "B", "B", "B"], LAB, "대부분의 앱 화면 실험"),
        ("반·매장 전체", "친구 사이 전파 차단", ["A", "A", "A", "A", "A"], GFX, "오염 우려 시 · 표본 더 필요"),
    ]
    for i, (t, s, seq, c, v) in enumerate(rows):
        y = 3.35 - i * 1.42
        a.text(.05, y + .2, t, fontsize=14.5, fontweight="bold", color=c, fontfamily=SERIF, va="center")
        a.text(.05, y - .22, s, fontsize=11.5, color=DIM, va="center")
        for k, ch in enumerate(seq):
            x = 3.65 + k * .78
            a.add_patch(FancyBboxPatch((x, y - .26), .6, .56, boxstyle="square,pad=0", fc=tint(GFX if ch == "A" else VR, .16), ec=GFX if ch == "A" else VR, lw=1.3))
            a.text(x + .3, y + .02, ch, ha="center", va="center", fontsize=14, fontweight="bold", color=GFX if ch == "A" else VR, fontfamily=SERIF)
        a.text(7.8, y + .02, v, fontsize=12.2, color=c, fontweight="bold", va="center")
        if i < 2: a.plot([0, 11], [y - .66, y - .66], color=LINE, lw=1)
    a.text(3.65, 3.95, "같은 학생의 앱 접속 5회", fontsize=11.5, color=FAINT)
    return save(fig, "d10-unit")


def fig_sample_size():
    fig, a = canvas(figsize=(10.6, 4.5))
    labs = ["+10점", "+5점", "+3점", "+2점", "+1점", "+0.5점"]; v = [199, 686, 1774, 3841, 14751, 57763]
    y = np.arange(len(v))[::-1]
    cs = [FAINT] * 6; cs[3] = GFX; cs[5] = TRAP
    a.barh(y, v, color=cs, height=.62)
    for yy, n, c in zip(y, v, cs):
        a.text(n + 800, yy, f"{n:,}명", va="center", fontsize=14, fontweight="bold", color=c if c != FAINT else DIM, fontfamily=SERIF)
    a.set_yticks(y, labs, fontsize=13.5); a.tick_params(axis="y", length=0, colors=FG)
    a.set_xlim(0, 69000); a.set_xlabel("필요 표본 (집단당 · 기준 클릭률 10% · 유의수준 5% · 검정력 80%)"); a.set_ylabel("찾으려는 효과")
    a.grid(axis="y", visible=False); a.xaxis.set_major_formatter(lambda x, _: f"{int(x):,}")
    a.text(66000, 3.0, "효과 절반 → 표본 약 4배", ha="right", fontsize=14.5, color=FG, fontweight="bold", fontfamily=SERIF)
    return save(fig, "d10-sample-size")


def fig_vibe_loop():
    fig, a = plt.subplots(figsize=(11, 4.7)); clean(a); a.set_xlim(0, 11); a.set_ylim(0, 4.7)
    st = [("① 명세", "사람 : 기획자", "실험 6요소를 문장으로", 1.0, 2.75, GFX),
          ("② 생성", "AI : 개발자", "버전 2개 · 배정 · 로그 코드", 6.4, 2.75, FAINT),
          ("③ 관찰", "사람 : 테스터", "새로고침 · 배정 비율 · 로그 확인", 6.4, .4, VR),
          ("④ 수정", "사람 : 매니저", "틀린 지점 지목 후 재요청", 1.0, .4, LAB)]
    for t, r, s, x, y, c in st:
        a.add_patch(FancyBboxPatch((x, y), 3.6, 1.6, boxstyle="square,pad=0", fc=CARD, ec=c if c != FAINT else DIM, lw=1.6))
        a.text(x + .18, y + 1.15, t, fontsize=16, fontweight="bold", color=c if c != FAINT else FG, fontfamily=SERIF, va="center")
        a.text(x + 3.42, y + 1.15, r, fontsize=12, color=DIM, va="center", ha="right", fontweight="bold")
        a.text(x + .18, y + .5, s, fontsize=12.2, color=FG, va="center")
    arrow(a, (4.7, 3.55), (6.3, 3.55)); arrow(a, (8.2, 2.65), (8.2, 2.1)); arrow(a, (6.3, 1.2), (4.7, 1.2)); arrow(a, (2.8, 2.1), (2.8, 2.65))
    a.text(5.5, 2.37, "코드 작성은 AI · ①③④ 판단은 사람", ha="center", va="center", fontsize=12.2, color=TRAP, fontweight="bold",
           bbox=dict(fc=BG, ec="none", pad=2))
    return save(fig, "d10-vibe-loop")


def fig_balance():
    r = list(csv.DictReader(open(DATA / "ab_result.csv", encoding="utf-8-sig")))
    A = [x for x in r if x["variant"] == "A"]; B = [x for x in r if x["variant"] == "B"]
    keys = [("year", "1학년"), ("year", "2학년"), ("year", "3학년"), ("year", "4학년"), ("device", "모바일"), ("device", "PC")]
    fig = plt.figure(figsize=(11, 4.2))
    g = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.75], wspace=.42)
    for k, (t, vals, c, sub) in enumerate([("정상 배정", (4205, 4195), LAB, "차이 10명 · 적합도 p = 0.91"), ("고장 신호", (4700, 3700), TRAP, "차이 1,000명 · p < 0.0001")]):
        a = fig.add_subplot(g[k]); style_axes(a)
        b = a.bar(["A", "B"], vals, color=[tint(c, .85), tint(c, .45)], width=.62)
        for rect, v in zip(b, vals):
            a.text(rect.get_x() + rect.get_width()/2, v + 90, f"{v:,}", ha="center", fontsize=13.5, fontweight="bold", color=c, fontfamily=SERIF)
        a.set_ylim(0, 5600); a.set_title(t, color=c, loc="left"); a.set_xlabel(sub, fontsize=11.5, color=DIM); a.grid(axis="x", visible=False)
        a.yaxis.set_major_formatter(lambda x, _: f"{int(x):,}")
        if k == 0: a.set_ylabel("배정 인원 (명)")
    a = fig.add_subplot(g[2]); style_axes(a)
    for i, (kk, v) in enumerate(keys[::-1]):
        pa = sum(x[kk] == v for x in A) / len(A) * 100; pb = sum(x[kk] == v for x in B) / len(B) * 100
        a.plot([pa, pb], [i, i], color=LINE, lw=3, zorder=1)
        a.scatter([pa], [i], color=GFX, s=75, zorder=3, label="A" if i == 0 else None)
        a.scatter([pb], [i], color=VR, s=75, zorder=3, label="B" if i == 0 else None)
    a.set_yticks(range(6), [k[1] for k in keys[::-1]], fontsize=12.5); a.tick_params(axis="y", length=0, colors=FG)
    a.set_xlim(0, 100); a.set_xlabel("비율 (%)"); a.set_title("처치 전 특성 균형 : 차이 2점 이내", loc="left", color=LAB); a.legend(loc="center right", fontsize=12); a.grid(axis="y", visible=False)
    return save(fig, "d10-balance")


if __name__ == "__main__":
    for f in [fig_before_after, fig_hypothesis, fig_assignment, fig_volunteer_bias, fig_unit, fig_sample_size, fig_vibe_loop, fig_balance]:
        f()
