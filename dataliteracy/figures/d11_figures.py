"""데이터리터러시 11주차 도해 — A/B 결과·통계적 유의성·p값
실행 : .venv/Scripts/python.exe dataliteracy/figures/d11_figures.py
수치 근거 : dataliteracy/data/numbers_d10_d11.py · 교육용 합성 데이터"""
import numpy as np
from scipy import stats
from matplotlib.patches import FancyBboxPatch
from _style_ed import *

OBS, SE0 = 1.55, 0.678


def fig_variation():
    rng = np.random.default_rng(11)
    fig, axs = canvas(figsize=(11, 3.9), ncols=3, sharey=False)
    for a, n, c in zip(axs, [100, 1000, 4200], [TRAP, WARN, GFX]):
        d = (rng.binomial(n, .1, 40000) - rng.binomial(n, .1, 40000)) / n * 100
        lo, hi = np.percentile(d, [2.5, 97.5])
        w = {100: 1.0, 1000: .3, 4200: .1}[n]
        a.hist(d, bins=np.arange(-14 - w/2, 14 + w, w), color=tint(c, .55), edgecolor="none")
        a.axvline(OBS, color=FG, lw=1.6, ls="--")
        a.set_xlim(-12, 12); a.set_yticks([]); a.spines["left"].set_visible(False); a.grid(False)
        a.set_title(f"집단당 {n:,}명", loc="left", color=c)
        a.set_xlabel("A/A 차이 (%포인트)")
        a.text(.03, .9, f"우연의 폭\n±{1.96 * (0.18 / n) ** .5 * 100:.1f}점", transform=a.transAxes, fontsize=14, fontweight="bold", color=c, fontfamily=SERIF, va="top", linespacing=1.3)
    axs[2].text(OBS + .4, axs[2].get_ylim()[1] * .9, "관측\n+1.55점", fontsize=11.5, color=FG, fontweight="bold", va="top")
    fig.tight_layout()
    return save(fig, "d11-sampling-variation")


def fig_cola():
    fig, a = canvas(figsize=(8.6, 4.2))
    x = [0, 2, 4, 6, 8]; y = [1, 16, 36, 16, 1]
    cs = [FAINT, FAINT, FAINT, FAINT, TRAP]
    a.bar(x, y, width=1.3, color=cs)
    for xx, yy, c in zip(x, y, cs):
        a.text(xx, yy + 1, f"{yy}가지", ha="center", fontsize=13.5, fontweight="bold", color=c if c == TRAP else DIM)
    a.set_xticks(x, [f"{v}잔" for v in x], fontsize=13); a.set_xlabel("맞힌 잔 수 (8잔 중)"); a.set_ylabel("경우의 수 (전체 70가지)")
    a.set_ylim(0, 43); a.grid(axis="x", visible=False)
    a.annotate("전부 정답 1가지\n1/70 ≈ 1.4%", xy=(8, 4.2), xytext=(6.6, 26), fontsize=14.5, fontweight="bold", color=TRAP, fontfamily=SERIF,
               arrowprops=dict(arrowstyle="-", color=TRAP, lw=1.3))
    return save(fig, "d11-cola")


def fig_pvalue():
    fig, a = canvas(figsize=(10.6, 4.3))
    x = np.linspace(-3.4, 3.4, 800); y = stats.norm.pdf(x, 0, SE0)
    a.plot(x, y, color=FG, lw=2.2)
    a.fill_between(x, y, where=x >= OBS, color=TRAP, alpha=.75); a.fill_between(x, y, where=x <= -OBS, color=TRAP, alpha=.75)
    a.axvline(OBS, ymax=.72, color=TRAP, lw=1.6, ls="--")
    a.text(OBS + .06, stats.norm.pdf(0, 0, SE0) * .74, "관측 차이\n+1.55점", fontsize=13.5, color=TRAP, fontweight="bold", linespacing=1.3)
    a.annotate("이보다 극단적인 쪽\n오른쪽 약 1.1%", xy=(2.0, .018), xytext=(2.15, .2), fontsize=12.5, color=TRAP, fontweight="bold", arrowprops=dict(arrowstyle="-", color=TRAP))
    a.annotate("반대 방향\n왼쪽 약 1.1%", xy=(-2.0, .018), xytext=(-3.25, .2), fontsize=12.5, color=TRAP, fontweight="bold", arrowprops=dict(arrowstyle="-", color=TRAP))
    a.text(0, stats.norm.pdf(0, 0, SE0) * .34, "«차이 없음» 세계에서\n나올 수 있는 차이들", ha="center", fontsize=13, color=DIM, linespacing=1.35)
    a.set_yticks([]); a.spines["left"].set_visible(False); a.grid(False); a.set_ylim(0, .66); a.set_xlim(-3.4, 3.4)
    a.set_xlabel("B − A 클릭률 차이 (%포인트)")
    a.set_title("p = 빨간 면적 합 = 0.022", loc="left", color=TRAP, fontsize=17)
    return save(fig, "d11-pvalue-definition")


def fig_ci():
    cases = [("집단 100명 · 10% → 13%", 3.0, -5.83, 11.83, .506, TRAP), ("집단 1,000명 · 10% → 13%", 3.0, .21, 5.79, .036, WARN), ("집단 10,000명 · 10% → 13%", 3.0, 2.12, 3.88, .0001, LAB),
             ("집단 1,000,000명 · 10.0% → 10.1%", .1, .02, .18, .019, VR), ("학식 쿠폰 · 10.04% → 11.59%", 1.55, .22, 2.88, .022, GFX)]
    fig, a = canvas(figsize=(11, 4.3))
    for i, (t, m, lo, hi, p, c) in enumerate(cases[::-1]):
        a.plot([lo, hi], [i, i], color=c, lw=4, solid_capstyle="butt")
        a.scatter([m], [i], color=c, s=95, zorder=3, edgecolor=BG)
        ptxt = "p < 0.001" if p < .001 else f"p = {p:.3f}"
        a.text(12.4, i, f"{lo:+.2f} ~ {hi:+.2f}   {ptxt}", va="center", fontsize=13, color=c, fontweight="bold")
    a.set_yticks(range(5), [c[0] for c in cases[::-1]], fontsize=13.5); a.tick_params(axis="y", length=0, colors=FG)
    a.axvline(0, color=FG, lw=1.8); a.axvline(2, color=WARN, lw=1.3, ls="--")
    a.text(0, 4.62, "차이 0", ha="right", fontsize=11.5, color=FG, fontweight="bold")
    a.text(2.1, 4.62, "실질 기준 +2점", fontsize=11.5, color=WARN, fontweight="bold")
    a.set_xlim(-7, 19.5); a.set_ylim(-.5, 4.95); a.set_xticks(range(-6, 13, 2)); a.set_xlabel("B − A 차이 (%포인트) · 막대 = 95% 신뢰구간"); a.grid(axis="y", visible=False)
    return save(fig, "d11-confidence-interval")


def fig_effect_sig():
    fig, a = plt.subplots(figsize=(10.8, 4.5)); clean(a); a.set_xlim(0, 11); a.set_ylim(0, 4.6)
    cells = [(1.1, 2.4, "실질 효과 작음 · 유의", "집단 100만 명 · +0.1점 · p=0.019", "비용 대비 판단 → 대개 보류", VR),
             (6.0, 2.4, "실질 효과 큼 · 유의", "집단 1만 명 · +3점 · p<0.001", "도입 후보", LAB),
             (1.1, .25, "실질 효과 작음 · 비유의", "표본 충분 · 구간도 좁음", "중단 · 다음 아이디어", FAINT),
             (6.0, .25, "효과 커 보임 · 비유의", "집단 100명 · +3점 · p=0.506", "판단 불가 → 표본 재계산 후 새 실험", TRAP)]
    for x, y, t, s, v, c in cells:
        ec = DIM if c == FAINT else c
        a.add_patch(FancyBboxPatch((x, y), 4.75, 1.95, boxstyle="square,pad=0", fc=CARD, ec=ec, lw=1.6))
        a.text(x + .2, y + 1.55, t, fontsize=14.5, fontweight="bold", color=ec, fontfamily=SERIF, va="center")
        a.text(x + .2, y + .95, s, fontsize=12.2, color=DIM, va="center")
        a.text(x + .2, y + .38, "→ " + v, fontsize=13, color=FG, fontweight="bold", va="center")
    a.text(.5, 3.37, "p < 0.05", rotation=90, va="center", ha="center", fontsize=13, color=FG, fontweight="bold")
    a.text(.5, 1.22, "p ≥ 0.05", rotation=90, va="center", ha="center", fontsize=13, color=FG, fontweight="bold")
    return save(fig, "d11-effect-vs-significance")


def fig_multiple():
    rng = np.random.default_rng(204)
    names = ["클릭", "결제", "재방문", "체류", "공유", "이탈", "검색", "장바구니", "쿠폰", "리뷰", "알림", "찜", "환불", "문의", "로그인", "스크롤", "추천", "탈퇴", "구독", "초대"]
    ps = stats.norm.sf(np.abs(rng.normal(0, 1, 20))) * 2
    order = np.argsort(ps); ps = ps[order]; nm = [names[i] for i in order]
    n_sig = int((ps < .05).sum()); print("  유의 지표 수", n_sig, np.round(ps[:3], 3))
    fig, (l, r) = canvas(figsize=(11, 4.2), ncols=2, gridspec_kw=dict(width_ratios=[1.45, 1], wspace=.22))
    cs = [TRAP if p < .05 else FAINT for p in ps]
    l.bar(range(20), ps, color=cs, width=.72)
    l.axhline(.05, color=TRAP, lw=1.5, ls="--"); l.text(.2, .1, "기준 0.05", color=TRAP, ha="left", fontsize=12, fontweight="bold", bbox=dict(fc=BG, ec="none", pad=1), zorder=5)
    l.set_xticks(range(20), nm, rotation=60, fontsize=10); l.set_ylabel("p값"); l.set_ylim(0, 1.02); l.grid(axis="x", visible=False)
    l.set_title(f"효과 0 · 지표 20개 검정 → 유의 {n_sig}개", loc="left", color=TRAP)
    k = np.arange(1, 51); r.plot(k, (1 - .95 ** k) * 100, color=FG, lw=2.4)
    r.scatter([20], [64.2], color=TRAP, s=75, zorder=3); r.text(22, 52, "지표 20개\n64%", color=TRAP, fontsize=14.5, fontweight="bold", fontfamily=SERIF, linespacing=1.25)
    r.scatter([1], [5], color=GFX, s=60, zorder=3); r.text(4, 3, "지표 1개 5%", color=GFX, fontsize=12.5, fontweight="bold")
    r.set_xlabel("검정한 지표 수"); r.set_ylabel("거짓 양성 1개 이상 (%)"); r.set_ylim(0, 100); r.set_xlim(0, 50)
    r.set_title("1 − 0.95^지표 수", loc="left")
    return save(fig, "d11-multiple-comparison")


def fig_peeking():
    fig, a = canvas(figsize=(10.4, 4.2))
    k = ["1회\n(끝에 1번)", "2회", "5회", "10회", "14회\n(매일)", "20회", "50회", "100회"]; v = [5.1, 8.2, 14.0, 19.6, 22.4, 24.0, 31.9, 38.1]
    a.bar(range(8), v, color=[GFX] + [tint(TRAP, .35 + .08 * i) for i in range(7)], width=.68)
    for i, x in enumerate(v):
        a.text(i, x + .9, f"{x:.1f}%", ha="center", fontsize=14, fontweight="bold", color=GFX if i == 0 else TRAP, fontfamily=SERIF)
    a.axhline(5, color=GFX, lw=1.4, ls="--"); a.text(.62, 2.6, "약속한 5%", ha="left", va="center", color=GFX, fontsize=12, fontweight="bold", bbox=dict(fc=BG, ec="none", pad=1.5), zorder=5)
    a.set_xticks(range(8), k, fontsize=12.5); a.set_ylim(0, 45); a.set_xlabel("중간 확인 횟수 (유의 판정 시 즉시 종료)"); a.set_ylabel("거짓 양성 비율 (%)"); a.grid(axis="x", visible=False)
    fig.text(.99, -.02, "효과 0 · 집단당 4,200명 · 20,000회 시뮬레이션", ha="right", fontsize=10, color=FAINT)
    return save(fig, "d11-peeking")


def fig_impute():
    fig, axs = canvas(figsize=(9.6, 3.6), ncols=3, gridspec_kw=dict(wspace=.5))
    data = [("집단당 사용 n", [113, 200], "{:,}명"), ("표준편차 (A집단)", [1620, 1215], "{:,}원"), ("p값", [.1425, .0091], "{:.3f}")]
    for a, (t, v, f) in zip(axs, data):
        b = a.bar(["결측 제외", "평균 대치"], v, color=[FAINT, TRAP], width=.6)
        for j, (rect, x) in enumerate(zip(b, v)):
            a.text(rect.get_x() + rect.get_width()/2, x + max(v) * .03, f.format(x), ha="center", fontsize=14, fontweight="bold", color=TRAP if j else DIM, fontfamily=SERIF)
        a.set_title(t, loc="left", fontsize=13.5); a.set_yticks([]); a.spines["left"].set_visible(False); a.grid(False); a.set_ylim(0, max(v) * 1.25)
    fig.text(.99, -.04, "지출액 지표 · 결측 약 44% · 관측값 평균 차이 297원 동일 · 교육용 합성 데이터", ha="right", fontsize=10, color=FAINT)
    return save(fig, "d11-imputation")


def fig_flow():
    fig, a = plt.subplots(figsize=(11.4, 4.4)); clean(a); a.set_xlim(0, 11.4); a.set_ylim(0, 4.4)
    rows = [(2.75, "10주 · 실험 전", GFX, [("질문·가설", "H₀ · H₁ 선언"), ("6요소 설계", "대상·단위·처치\n지표·기간·표본"), ("사전 등록", "주 지표 1개\n중단 규칙"), ("난수 배정", "같은 사람\n같은 버전")]),
            (.3, "11주 · 실험 후", VR, [("배정 점검", "비율 · 사전 특성\n로그 누락"), ("검정·구간", "기간 종료 후 1회\n손계산 대조"), ("보고 4종", "효과 크기 · 신뢰구간\nn · 검정 횟수"), ("판단", "도입·보류·재실험\n실질 기준 비교")])]
    for y, lab, c, items in rows:
        a.text(.02, y + 1.38, lab, fontsize=14, fontweight="bold", color=c, fontfamily=SERIF)
        for i, (t, s) in enumerate(items):
            x = .02 + i * 2.87
            a.add_patch(FancyBboxPatch((x, y), 2.45, 1.22, boxstyle="square,pad=0", fc=CARD, ec=c, lw=1.5))
            a.text(x + 1.22, y + .94, t, ha="center", va="center", fontsize=14, fontweight="bold", color=FG, fontfamily=SERIF)
            a.text(x + 1.22, y + .42, s, ha="center", va="center", fontsize=11.2, color=DIM, linespacing=1.3)
            if i < 3:
                a.annotate("", xy=(x + 2.84, y + .61), xytext=(x + 2.47, y + .61), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8))
    return save(fig, "d11-ab-flow")


if __name__ == "__main__":
    for f in [fig_variation, fig_cola, fig_pvalue, fig_ci, fig_effect_sig, fig_multiple, fig_peeking, fig_impute, fig_flow]:
        f()
