"""데이터리터러시 9주차 도해 — 데이터 분석용 AI 모델과 사용법 · 상관과 인과
실행 : .venv/Scripts/python.exe dataliteracy/figures/d09_figures.py
수치 근거 : dataliteracy/data/numbers_d09.py · 교육용 합성 데이터"""
import csv, pathlib
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from _style_ed import *

DATA = pathlib.Path(__file__).parent.parent / "data"
_r = list(csv.DictReader(open(DATA / "ice_cream.csv", encoding="utf-8-sig")))
T = np.array([float(x["temp_c"]) for x in _r]); S = np.array([float(x["ice_cream_sales"]) for x in _r])
D = np.array([float(x["drownings"]) for x in _r]); W = np.array([int(x["week"]) for x in _r])
RAIN = np.array([float(x["rain_days"]) for x in _r])
corr = lambda a, b: float(np.corrcoef(a, b)[0, 1])


def bx(a, x, y, w, h, title, sub=None, color=FG, fc=CARD, fs=14, sfs=11.5, lw=1.5, tc=None):
    a.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc=fc, ec=color, lw=lw))
    if sub:
        a.text(x + w/2, y + h*.70, title, ha="center", va="center", fontsize=fs, fontweight="bold", color=tc or color, fontfamily=SERIF)
        a.text(x + w/2, y + h*.30, sub, ha="center", va="center", fontsize=sfs, color=DIM, linespacing=1.35)
    else:
        a.text(x + w/2, y + h/2, title, ha="center", va="center", fontsize=fs, fontweight="bold", color=tc or color, fontfamily=SERIF)


def ar(a, p, q, color=DIM, lw=1.8):
    a.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>,head_width=.28,head_length=.5", color=color, lw=lw, shrinkA=0, shrinkB=0))


def fig_two_kinds():
    fig, a = plt.subplots(figsize=(11.2, 4.4)); clean(a); a.set_xlim(0, 11.2); a.set_ylim(0, 4.4)
    a.text(.05, 4.05, "대화형 AI 모델 (LLM)", fontsize=16, fontweight="bold", color=GFX, fontfamily=SERIF)
    bx(a, .05, 2.5, 2.6, 1.25, "입력", "질문 · 파일 · 명세", GFX)
    bx(a, 4.15, 2.5, 2.6, 1.25, "문장 · 코드 생성", "Claude · GPT · Gemini", GFX)
    bx(a, 8.25, 2.5, 2.9, 1.25, "출력", "설명 · 분석 코드 · 요약", GFX)
    ar(a, (2.7, 3.12), (4.1, 3.12), GFX); ar(a, (6.8, 3.12), (8.2, 3.12), GFX)
    a.text(.05, 1.72, "분석 모델 (표 데이터용 머신러닝)", fontsize=16, fontweight="bold", color=VR, fontfamily=SERIF)
    bx(a, .05, .17, 2.6, 1.25, "입력", "숫자 표 (CSV)", VR)
    bx(a, 4.15, .17, 2.6, 1.25, "규칙 학습", "회귀 · 분류 · 군집 · 시계열", VR)
    bx(a, 8.25, .17, 2.9, 1.25, "출력", "예측값 · 그룹 · 이상 신호", VR)
    ar(a, (2.7, .8), (4.1, .8), VR); ar(a, (6.8, .8), (8.2, .8), VR)
    a.annotate("", xy=(5.45, 1.46), xytext=(5.45, 2.46), arrowprops=dict(arrowstyle="-|>,head_width=.3,head_length=.5", color=TRAP, lw=2.4))
    a.text(5.62, 1.97, "LLM이 분석 모델 코드 작성", color=TRAP, fontsize=12.5, fontweight="bold", va="center")
    return save(fig, "d09-two-kinds")


def fig_layers():
    fig, a = plt.subplots(figsize=(11.2, 4.2)); clean(a); a.set_xlim(0, 11.2); a.set_ylim(0, 4.2)
    rows = [(2.95, "앱 · 도구", "자동차", "화면 · 파일 업로드 · 코드 실행 · 권한", ["ChatGPT · Codex", "Claude · Claude Code", "Gemini · Antigravity", "OpenCode (모델 선택)"], GFX),
            (1.55, "모델", "엔진", "실제로 답을 만드는 두뇌 · 등급별 속도·성능 차이", ["GPT 계열", "Claude 계열", "Gemini 계열", "오픈 웨이트 모델"], VR),
            (.15, "실행 위치", "차고", "데이터가 머무는 곳 · 보안의 기준", ["업체 서버 (웹·API)", "CLI : 실행은 내 PC · 읽은 내용은 업체 서버", "", "내 PC + 내 모델 (로컬)"], LAB)]
    for y, t, ana, s, items, c in rows:
        a.add_patch(FancyBboxPatch((0, y), 11.2, 1.22, boxstyle="square,pad=0", fc=CARD, ec=c, lw=1.5))
        a.text(.18, y + .84, t, fontsize=15.5, fontweight="bold", color=c, fontfamily=SERIF, va="center")
        a.text(.18, y + .36, "비유 : " + ana, fontsize=11.5, color=WARN, fontweight="bold", va="center")
        a.text(2.25, y + .9, s, fontsize=12, color=DIM, va="center")
        for k, it in enumerate(items):
            if it: a.text(2.25 + k * 2.2, y + .38, it, fontsize=11, color=FG, fontweight="bold", va="center")
    return save(fig, "d09-layers")


def fig_compute():
    fig, a = plt.subplots(figsize=(11.2, 3.9)); clean(a); a.set_xlim(0, 11.2); a.set_ylim(0, 3.9)
    a.text(0, 3.55, "위험 : 말로만 답", fontsize=15, fontweight="bold", color=TRAP, fontfamily=SERIF)
    for x, t, s in [(0, "질문", "«평균 알려줘»"), (3.9, "모델 추정", "실행 없이 숫자 작성"), (7.8, "답변", "그럴듯한 숫자 · 근거 없음")]:
        bx(a, x, 2.1, 3.3, 1.15, t, s, TRAP)
    ar(a, (3.35, 2.67), (3.85, 2.67), TRAP); ar(a, (7.25, 2.67), (7.75, 2.67), TRAP)
    a.text(0, 1.55, "기준 : 코드 실행", fontsize=15, fontweight="bold", color=LAB, fontfamily=SERIF)
    for x, w, t, s in [(0, 2.4, "질문", "«코드로 계산»"), (2.8, 2.4, "코드 작성", "모델 담당"), (5.6, 2.4, "실제 실행", "파일 직접 계산"), (8.4, 2.8, "답변 + 근거", "코드 · 출력 · 행 수")]:
        bx(a, x, .1, w, 1.15, t, s, LAB)
    for x in [2.43, 5.23, 8.03]:
        ar(a, (x, .67), (x + .34, .67), LAB)
    return save(fig, "d09-compute")


def fig_six_step():
    fig, a = plt.subplots(figsize=(11.4, 3)); clean(a); a.set_xlim(0, 11.4); a.set_ylim(0, 3)
    st = [("① 준비", "헤더 · 형식 정리\n민감 정보 제거", GFX), ("② 제공", "파일 첨부 또는\n폴더에서 실행", GFX), ("③ 개요", "행 · 열 · 결측\n열 의미 확인", VR),
          ("④ 심화", "목표 · 제약 ·\n검증 조건 명세", VR), ("⑤ 시각화", "산점도 · 축 · n\n6주 점검 4문", LAB), ("⑥ 검증", "손계산 · 교차 모델\n결론 문장 등급", TRAP)]
    for i, (t, s, c) in enumerate(st):
        x = i * 1.92
        bx(a, x, .4, 1.68, 2.2, t, s, c, fs=14, sfs=10.8)
        if i < 5: ar(a, (x + 1.7, 1.5), (x + 1.9, 1.5), c)
    return save(fig, "d09-six-step")


def fig_model_map():
    fig, a = plt.subplots(figsize=(11.4, 4.9)); clean(a); a.set_xlim(0, 11.4); a.set_ylim(0, 4.9)
    rows = [("숫자를 맞히기", "다음 주 판매량은?", "회귀", "선형 회귀 · 랜덤 포레스트", GFX),
            ("범주를 맞히기", "쿠폰을 쓸까 안 쓸까?", "분류", "로지스틱 회귀 · 결정 트리", GFX),
            ("정답 없이 묶기", "비슷한 고객끼리 몇 그룹?", "군집", "K-평균", VR),
            ("시간 흐름 예측", "다음 학기 이용량은?", "시계열", "계절 기준선 · 시간순 검증", VR),
            ("드문 값 찾기", "평소와 다른 결제는?", "이상 탐지", "IQR 규칙 · Isolation Forest", TRAP),
            ("글 다루기", "후기가 긍정인가 부정인가?", "텍스트", "LLM 분류 · 임베딩", LAB)]
    a.text(.05, 4.62, "하고 싶은 일", fontsize=12, color=FAINT, fontweight="bold"); a.text(2.85, 4.62, "질문 예", fontsize=12, color=FAINT, fontweight="bold")
    a.text(6.25, 4.62, "유형", fontsize=12, color=FAINT, fontweight="bold"); a.text(8, 4.62, "첫 시도 모델", fontsize=12, color=FAINT, fontweight="bold")
    for i, (w, q, ty, m, c) in enumerate(rows):
        y = 3.9 - i * .76
        a.text(.05, y + .25, w, fontsize=14, fontweight="bold", color=FG, fontfamily=SERIF, va="center")
        a.text(2.85, y + .25, q, fontsize=12.2, color=DIM, va="center")
        a.add_patch(FancyBboxPatch((6.2, y + .02), 1.35, .46, boxstyle="square,pad=0", fc=tint(c, .12), ec=c, lw=1.3))
        a.text(6.875, y + .25, ty, fontsize=12.5, color=c, fontweight="bold", ha="center", va="center")
        ar(a, (5.82, y + .25), (6.16, y + .25), DIM, 1.4); ar(a, (7.58, y + .25), (7.92, y + .25), DIM, 1.4)
        a.text(8, y + .25, m, fontsize=12.2, color=FG, fontweight="bold", va="center")
        if i < 5: a.plot([0, 11.4], [y - .12, y - .12], color=LINE, lw=.8)
    return save(fig, "d09-model-map")


def fig_regression():
    fig, a = canvas(figsize=(9.2, 4.5))
    m, b = np.polyfit(T, S, 1); xs = np.array([T.min(), T.max()])
    a.scatter(T, S, s=36, color=tint(GFX, .55), edgecolor=GFX, lw=.5)
    a.plot(xs, m * xs + b, color=TRAP, lw=2.8)
    a.annotate(f"판매량 ≈ {b:.0f} + {m:.1f} × 기온", xy=(15, m * 15 + b), xytext=(2, 1320), fontsize=15, fontweight="bold", color=TRAP, fontfamily=SERIF, arrowprops=dict(arrowstyle="-", color=TRAP))
    a.text(13.5, 300, f"기온 1도 오를 때\n판매량 약 {m:.0f}개 증가 관측\nn = {len(T)}주", fontsize=12.5, color=DIM, linespacing=1.4)
    a.set_xlabel("주 평균 기온 (℃)"); a.set_ylabel("아이스크림 판매량 (개)")
    fig.text(.99, -.02, "교육용 합성 데이터", ha="right", fontsize=10, color=FAINT)
    return save(fig, "d09-regression")


def fig_classifier():
    g = np.random.default_rng(12)
    n = 220
    X = np.c_[g.uniform(0, 10, n), g.uniform(0, 10, n)]
    y = ((X[:, 0] > 4) & (X[:, 1] > 3.5)).astype(int)
    y = np.where(g.random(n) < .07, 1 - y, y)
    tr, va = np.arange(n) < 160, np.arange(n) >= 160
    models = [("로지스틱 회귀 : 직선 경계", LogisticRegression().fit(X[tr], y[tr]), GFX), ("결정 트리 : 스무고개 경계", DecisionTreeClassifier(max_depth=3, random_state=1).fit(X[tr], y[tr]), VR)]
    fig, axs = canvas(figsize=(11, 4.3), ncols=2)
    xx, yy = np.meshgrid(np.linspace(0, 10, 300), np.linspace(0, 10, 300))
    for a, (t, mdl, c) in zip(axs, models):
        z = mdl.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        a.contourf(xx, yy, z, levels=[-.5, .5, 1.5], colors=[tint(FAINT, .10), tint(c, .16)])
        a.contour(xx, yy, z, levels=[.5], colors=[c], linewidths=2)
        a.scatter(X[y == 0, 0], X[y == 0, 1], s=20, facecolor=CARD, edgecolor=DIM, lw=.8, label="미사용")
        a.scatter(X[y == 1, 0], X[y == 1, 1], s=20, color=c, label="쿠폰 사용")
        acc = (mdl.predict(X[va]) == y[va]).mean() * 100
        a.set_title(f"{t} · 검증 정확도 {acc:.0f}%", loc="left", color=c); a.set_xlabel("주간 앱 접속 (회)"); a.set_ylabel("학식 이용 (회)"); a.grid(False); a.legend(loc="lower left", fontsize=11, frameon=True, facecolor=BG, edgecolor=LINE, framealpha=.95)
        print("  ", t, round(acc, 1))
    fig.tight_layout()
    return save(fig, "d09-classifier")


def fig_importance():
    fA = RandomForestRegressor(n_estimators=300, random_state=9).fit(np.c_[S, RAIN], D)
    fB = RandomForestRegressor(n_estimators=300, random_state=9).fit(np.c_[S, RAIN, T], D)
    print("  중요도 A", np.round(fA.feature_importances_, 2), "B", np.round(fB.feature_importances_, 2))
    fig, (l, r) = canvas(figsize=(10.8, 3.7), ncols=2)
    a1 = fA.feature_importances_ * 100; a2 = fB.feature_importances_ * 100
    l.barh(["비 온 날", "아이스크림 판매량"], [a1[1], a1[0]], color=[FAINT, TRAP], height=.55)
    r.barh(["비 온 날", "아이스크림 판매량", "기온"], [a2[1], a2[0], a2[2]], color=[FAINT, TRAP, GFX], height=.55)
    for a, vals in [(l, [a1[1], a1[0]]), (r, [a2[1], a2[0], a2[2]])]:
        for i, v in enumerate(vals):
            a.text(v + 1.5, i, f"{v:.0f}%", va="center", fontsize=14, fontweight="bold", color=DIM, fontfamily=SERIF)
        a.set_xlim(0, 112); a.set_xlabel("변수 중요도"); a.grid(axis="y", visible=False); a.tick_params(axis="y", length=0, labelsize=12.5, colors=FG)
    l.set_title("기온 제외 : 판매량이 익사 예측 1위", loc="left", color=TRAP); r.set_title("기온 포함 : 판매량 중요도 감소", loc="left", color=GFX)
    fig.tight_layout()
    return save(fig, "d09-importance")


def fig_kmeans():
    g = np.random.default_rng(3)
    visits = np.r_[g.normal(3, .7, 60), g.normal(9, .8, 60)]
    spend = np.r_[g.normal(30000, 2500, 30), g.normal(45000, 2500, 30), g.normal(30000, 2500, 30), g.normal(45000, 2500, 30)]
    Xc = np.c_[visits, spend]
    raw = KMeans(4, n_init=10, random_state=1).fit_predict(Xc)
    sc = KMeans(4, n_init=10, random_state=1).fit_predict(StandardScaler().fit_transform(Xc))
    cols = np.array([GFX, VR, WARN, LAB])
    fig, axs = canvas(figsize=(11, 4.1), ncols=2)
    for a, lb, t in zip(axs, [raw, sc], ["원본 단위 : 금액 크기에 끌려간 묶음", "표준화 후 (5주 z-점수) : 실제 4그룹 복원"]):
        a.scatter(visits, spend / 1000, s=34, c=cols[lb], alpha=.85)
        a.set_title(t, loc="left"); a.set_xlabel("주간 방문 (회)"); a.set_ylabel("월 지출 (천 원)"); a.grid(False)
    fig.tight_layout()
    return save(fig, "d09-kmeans")


def fig_timesplit():
    fig, (t, b) = canvas(figsize=(11, 4.1), nrows=2, sharex=True)
    g = np.random.default_rng(9); idx = g.permutation(104)[78:]
    tr = np.ones(104, bool); tr[idx] = False
    t.plot(W, S, color=LINE, lw=1.1, zorder=1)
    t.scatter(W[tr], S[tr], s=16, color=FAINT, zorder=2, label="학습"); t.scatter(W[~tr], S[~tr], s=30, color=TRAP, zorder=3, label="검증")
    t.set_title("무작위 분리 : 미래 주가 학습에 혼입", loc="left", color=TRAP); t.legend(loc="upper right", ncol=2, fontsize=11)
    b.plot(W, S, color=LINE, lw=1.1, zorder=1)
    b.scatter(W[W <= 78], S[W <= 78], s=16, color=FAINT, zorder=2); b.scatter(W[W > 78], S[W > 78], s=30, color=LAB, zorder=3)
    b.axvline(78.5, color=LAB, lw=1.5, ls="--"); b.text(77.5, 120, "여기까지만 학습", ha="right", color=LAB, fontsize=12, fontweight="bold")
    b.set_title("시간순 분리 : 시간 순서 재현 · 기온은 실측값 · RF(주차·기온) 오차 69.4", loc="left", color=LAB); b.set_xlabel("주차")
    for a in (t, b): a.set_ylabel("판매량"); a.set_ylim(0, 1500)
    fig.tight_layout()
    return save(fig, "d09-timesplit")


def fig_baseline():
    fig, a = canvas(figsize=(9.6, 4.1))
    labs = ["평균으로 찍기 (기준선)", "작년 같은 주 (기준선)", "랜덤 포레스트 (기온·계절)", "선형 회귀 (기온만)"]; v = [286.6, 146.2, 84.8, 64.7]; cs = [FAINT, FAINT, VR, LAB]
    y = [3, 2, 1, 0]
    a.barh(y, v, color=cs, height=.56)
    for yy, x, c in zip(y, v, cs):
        a.text(x + 4, yy, f"{x:.1f}개", va="center", fontsize=16, fontweight="bold", color=DIM if c == FAINT else c, fontfamily=SERIF)
    a.set_yticks(y, labs, fontsize=13); a.tick_params(axis="y", length=0, colors=FG); a.set_xlim(0, 345); a.grid(axis="y", visible=False)
    a.set_xlabel("MAE (평균 빗나간 개수) · 작을수록 좋음 · 뒤 26주")
    return save(fig, "d09-baseline")


def fig_spurious():
    fig = plt.figure(figsize=(11, 4.2))
    g = fig.add_gridspec(3, 2, width_ratios=[1.6, 1], hspace=.16, wspace=.2)
    for i, (y, t, c) in enumerate([(T, "기온 (℃)", WARN), (S, "판매량 (개)", GFX), (D, "익사 사고 (건)", TRAP)]):
        a = fig.add_subplot(g[i, 0]); style_axes(a)
        a.plot(W, y, color=c, lw=2); a.set_ylabel(t, fontsize=11)
        if i < 2: a.set_xticklabels([])
        else: a.set_xlabel("주차")
    a = fig.add_subplot(g[:, 1]); style_axes(a)
    a.scatter(S, D, s=30, color=tint(TRAP, .55), edgecolor=TRAP, lw=.5)
    a.set_xlabel("아이스크림 판매량"); a.set_ylabel("익사 사고"); a.set_title(f"r = {corr(S, D):.2f} · n = {len(S)}", loc="left", color=TRAP, fontsize=17)
    fig.text(.99, -.02, "교육용 합성 데이터", ha="right", fontsize=10, color=FAINT)
    return save(fig, "d09-spurious")


def fig_four():
    fig, axs = plt.subplots(1, 4, figsize=(11.2, 3.2))
    def node(a, x, y, t, c=FG):
        a.add_patch(Circle((x, y), .24, fc=CARD, ec=c, lw=1.7, zorder=3)); a.text(x, y, t, ha="center", va="center", fontsize=15, fontweight="bold", color=c, fontfamily=SERIF, zorder=4)
    spec = [("인과", "A가 B를 변화", LAB), ("역인과", "B가 A를 변화", WARN), ("교란", "C가 둘 다 변화", TRAP), ("우연", "연결 없음 · 표본 탓", FAINT)]
    for a, (t, s, c) in zip(axs, spec):
        clean(a); a.set_xlim(0, 2); a.set_ylim(0, 2.1); a.set_aspect("equal")
        a.set_title(t, fontsize=16, color=DIM if c == FAINT else c, fontfamily=SERIF, fontweight="bold")
        a.text(1, .08, s, ha="center", fontsize=11.5, color=DIM)
        node(a, .45, .8, "A"); node(a, 1.55, .8, "B")
    k = dict(arrowstyle="-|>,head_width=.25,head_length=.45", lw=2)
    axs[0].annotate("", xy=(1.3, .8), xytext=(.7, .8), arrowprops=dict(color=LAB, **k))
    axs[1].annotate("", xy=(.7, .8), xytext=(1.3, .8), arrowprops=dict(color=WARN, **k))
    node(axs[2], 1, 1.65, "C", TRAP)
    axs[2].annotate("", xy=(.58, 1.0), xytext=(.85, 1.45), arrowprops=dict(color=TRAP, **k)); axs[2].annotate("", xy=(1.42, 1.0), xytext=(1.15, 1.45), arrowprops=dict(color=TRAP, **k))
    axs[3].text(1, .8, "⋯", ha="center", va="center", fontsize=20, color=FAINT)
    return save(fig, "d09-four-explanations")


def fig_stratify():
    fig, axs = canvas(figsize=(11.2, 4), ncols=3)
    a = axs[0]
    im = a.scatter(S, D, c=T, cmap="YlOrRd", s=34, edgecolor=DIM, lw=.3)
    a.set_title(f"전체 r = {corr(S, D):.2f}", loc="left", color=TRAP); a.set_xlabel("판매량"); a.set_ylabel("익사 사고")
    a = axs[1]
    bins = [(T < 10, "10℃ 미만", GFX), ((T >= 10) & (T < 20), "10~20℃", WARN), (T >= 20, "20℃ 이상", TRAP)]
    lab = []
    for m, n, c in bins:
        a.scatter(S[m], D[m], s=28, color=c, alpha=.8, label=f"{n} : r = {corr(S[m], D[m]):.2f}")
        k, b = np.polyfit(S[m], D[m], 1); xs = np.array([S[m].min(), S[m].max()]); a.plot(xs, k * xs + b, color=c, lw=2)
    a.set_title("기온 구간별 : r 감소", loc="left"); a.set_xlabel("판매량"); a.legend(fontsize=10.5, loc="upper left", frameon=True, facecolor=BG, edgecolor=LINE, framealpha=.95)
    a = axs[2]
    rs = S - np.polyval(np.polyfit(T, S, 1), T); rd = D - np.polyval(np.polyfit(T, D, 1), T)
    a.scatter(rs, rd, s=30, color=tint(LAB, .6), edgecolor=LAB, lw=.5)
    a.set_title(f"기온 효과 제거 : r = {corr(rs, rd):.2f}", loc="left", color=LAB); a.set_xlabel("판매량 잔차"); a.set_ylabel("사고 잔차")
    fig.tight_layout()
    return save(fig, "d09-stratify")


def fig_simpson():
    fig, a = canvas(figsize=(9.8, 3.9))
    groups = ["쉬운 과목", "어려운 과목", "전체"]; A = [95, 50, 59]; B = [90, 40, 80]; x = np.arange(3); w = .36
    b1 = a.bar(x - w/2, A, w, color=GFX, label="튜터 A"); b2 = a.bar(x + w/2, B, w, color=VR, label="튜터 B")
    for r, v, nn in zip(b1, A, ["19/20", "40/80", "59/100"]):
        a.text(r.get_x() + r.get_width()/2, v + 1.5, f"{v}%\n{nn}", ha="center", fontsize=12.5, fontweight="bold", color=GFX, linespacing=1.15)
    for r, v, nn in zip(b2, B, ["72/80", "8/20", "80/100"]):
        a.text(r.get_x() + r.get_width()/2, v + 1.5, f"{v}%\n{nn}", ha="center", fontsize=12.5, fontweight="bold", color=VR, linespacing=1.15)
    a.set_xticks(x, groups, fontsize=13.5); a.tick_params(axis="x", length=0, colors=FG); a.set_ylim(0, 122); a.set_ylabel("합격률 (%)"); a.grid(axis="x", visible=False); a.legend(loc="upper center", ncol=2, fontsize=12)
    return save(fig, "d09-simpson")


if __name__ == "__main__":
    for f in [fig_two_kinds, fig_layers, fig_compute, fig_six_step, fig_model_map, fig_regression, fig_classifier, fig_importance, fig_kmeans, fig_timesplit, fig_baseline, fig_spurious, fig_four, fig_stratify, fig_simpson]:
        f()
