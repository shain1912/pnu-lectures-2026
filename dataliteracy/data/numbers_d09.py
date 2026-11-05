"""9주 덱에 인용하는 수치 계산 (시드 고정). 실행 결과가 덱 수치의 근거."""
import csv, pathlib, json
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

HERE = pathlib.Path(__file__).parent
r = list(csv.DictReader(open(HERE / "ice_cream.csv", encoding="utf-8-sig")))
T = np.array([float(x["temp_c"]) for x in r]); S = np.array([float(x["ice_cream_sales"]) for x in r])
D = np.array([float(x["drownings"]) for x in r]); W = np.array([int(x["week"]) for x in r])
out = {}
c = lambda a, b: round(float(np.corrcoef(a, b)[0, 1]), 2)
out["n"] = len(r)
out["r_sales_drown"] = c(S, D); out["r_temp_sales"] = c(T, S); out["r_temp_drown"] = c(T, D)
for name, m in [("cold(<10)", T < 10), ("mid(10-20)", (T >= 10) & (T < 20)), ("hot(>=20)", T >= 20)]:
    out[f"strat {name}"] = dict(n=int(m.sum()), r=c(S[m], D[m]))
rs = np.polyfit(T, S, 1); rd = np.polyfit(T, D, 1)
out["partial_r"] = c(S - np.polyval(rs, T), D - np.polyval(rd, T))
out["slope_sales_per_deg"] = round(float(rs[0]), 1); out["intercept"] = round(float(rs[1]), 1)

# 시간순 분리 : 앞 78주 학습 · 뒤 26주 검증
tr, va = W <= 78, W > 78
def mae(y, p): return round(float(mean_absolute_error(y, p)), 1)
month_sin = np.sin(2 * np.pi * W / 52); month_cos = np.cos(2 * np.pi * W / 52)
X = np.c_[T, month_sin, month_cos]
res = {"baseline_mean": mae(S[va], np.full(va.sum(), S[tr].mean()))}
lr = LinearRegression().fit(T[tr].reshape(-1, 1), S[tr]); res["linear_temp"] = mae(S[va], lr.predict(T[va].reshape(-1, 1)))
rf = RandomForestRegressor(n_estimators=300, random_state=9).fit(X[tr], S[tr]); res["forest"] = mae(S[va], rf.predict(X[va]))
out["predict_sales_MAE"] = res
out["forest_importance"] = dict(zip(["temp", "sin", "cos"], np.round(rf.feature_importances_, 2).tolist()))

# 판매량으로 익사 예측 : 예측은 되지만 원인 아님
base = mae(D[va], np.full(va.sum(), D[tr].mean()))
lr2 = LinearRegression().fit(S[tr].reshape(-1, 1), D[tr])
out["predict_drown_from_sales_MAE"] = dict(baseline=base, linear=mae(D[va], lr2.predict(S[va].reshape(-1, 1))), slope_per_100=round(float(lr2.coef_[0] * 100), 2))
# 판매 금지 가상 개입 : 규칙상 익사는 기온만으로 결정 → 판매량을 0으로 바꿔도 불변
out["drown_if_ban"] = dict(actual_mean=round(float(D.mean()), 2), rule="drownings 는 temp_c 만 입력으로 생성")

# 랜덤 분리 vs 시간 분리 (시계열)
rng = np.random.default_rng(9); idx = rng.permutation(len(r)); a, b = idx[:78], idx[78:]
X2 = np.c_[W.astype(float), T]
rf2 = RandomForestRegressor(n_estimators=300, random_state=9)
out["ts_split"] = dict(random=mae(S[b], rf2.fit(X2[a], S[a]).predict(X2[b])), time=mae(S[va], rf2.fit(X2[tr], S[tr]).predict(X2[va])))

# 무작위 분리 반복 : 1회 값은 분리 운에 좌우
_rs = []
for k in range(100):
    i2 = np.random.default_rng(k).permutation(len(r))
    m2 = RandomForestRegressor(n_estimators=100, random_state=9).fit(X2[i2[:78]], S[i2[:78]])
    _rs.append(mean_absolute_error(S[i2[78:]], m2.predict(X2[i2[78:]])))
out["random_split_100"] = dict(mean=round(float(np.mean(_rs)), 1), sd=round(float(np.std(_rs)), 1))

# 작년 같은 주 기준선 (뒤 26주 = 주차-52)
out["seasonal_naive_MAE"] = mae(S[va], S[W[va] - 53])

# 변수 중요도 (도해와 동일 설정)
RAIN = np.array([float(x["rain_days"]) for x in r])
fA = RandomForestRegressor(n_estimators=300, random_state=9).fit(np.c_[S, RAIN], D)
fB = RandomForestRegressor(n_estimators=300, random_state=9).fit(np.c_[S, RAIN, T], D)
out["importance_no_temp"] = dict(zip(["sales", "rain"], np.round(fA.feature_importances_, 2).tolist()))
out["importance_with_temp"] = dict(zip(["sales", "rain", "temp"], np.round(fB.feature_importances_, 2).tolist()))

# 심슨 예시
out["simpson"] = dict(A=[19/20, 40/80, 59/100], B=[72/80, 8/20, 80/100])

# 군집 : 표준화 전후
g = np.random.default_rng(3)
visits = np.r_[g.normal(3, .7, 60), g.normal(9, .8, 60)]
spend = np.r_[g.normal(30000, 2500, 30), g.normal(45000, 2500, 30), g.normal(30000, 2500, 30), g.normal(45000, 2500, 30)]
truth = np.r_[np.zeros(30), np.ones(30), np.full(30, 2), np.full(30, 3)]
def purity(lbl):
    return round(sum(np.bincount(truth[lbl == k].astype(int)).max() for k in set(lbl)) / len(lbl), 2)
Xc = np.c_[visits, spend]
out["kmeans_purity"] = dict(raw=purity(KMeans(4, n_init=10, random_state=1).fit_predict(Xc)), scaled=purity(KMeans(4, n_init=10, random_state=1).fit_predict(StandardScaler().fit_transform(Xc))))

print(json.dumps(out, ensure_ascii=False, indent=1))
