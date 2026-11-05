"""10·11주 덱에 인용하는 수치 계산 (시드 고정). 실행 결과를 덱 수치의 근거로 사용."""
import csv, math, pathlib
import numpy as np
from scipy import stats
HERE = pathlib.Path(__file__).parent

def two_prop(a, na, b, nb):
    pa, pb = a/na, b/nb
    p = (a+b)/(na+nb)
    se0 = math.sqrt(p*(1-p)*(1/na+1/nb))
    z = (pb-pa)/se0
    pv = 2*(1-stats.norm.cdf(abs(z)))
    se1 = math.sqrt(pa*(1-pa)/na + pb*(1-pb)/nb)
    d = pb-pa
    return dict(pa=round(pa*100,2), pb=round(pb*100,2), d=round(d*100,2), se0=round(se0*100,3),
                z=round(z,2), p=round(pv,4), lo=round((d-1.96*se1)*100,2), hi=round((d+1.96*se1)*100,2))

def n_per_arm(p1, p2, alpha=.05, power=.8):
    za, zb = stats.norm.ppf(1-alpha/2), stats.norm.ppf(power)
    pb = (p1+p2)/2
    return math.ceil((za*math.sqrt(2*pb*(1-pb))+zb*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2/(p1-p2)**2)

print("== 표본 크기 (기준 10%, 양측 5%, 검정력 80%)")
for d in [.10,.05,.03,.02,.01,.005]:
    print(f"  +{d*100:.1f}점 → 군당 {n_per_arm(.10,.10+d):,}")
print("  5%→6% :", n_per_arm(.05,.06))

print("== CSV")
for name in ["ab_result.csv","ab_null.csv"]:
    r = list(csv.DictReader(open(HERE/name,encoding="utf-8-sig")))
    A=[x for x in r if x["variant"]=="A"]; B=[x for x in r if x["variant"]=="B"]
    a,b=sum(int(x["clicked"]) for x in A),sum(int(x["clicked"]) for x in B)
    print(name,len(A),len(B),a,b,two_prop(a,len(A),b,len(B)))
    print("  SRM chi2 p", round(stats.chisquare([len(A),len(B)]).pvalue,3))
    print("  left_app", sum(int(x['left_app']) for x in A)/len(A), sum(int(x['left_app']) for x in B)/len(B))
    for key,vals in [("year",["1학년","2학년","3학년","4학년"]),("device",["모바일","PC"])]:
        for v in vals:
            print("  ",v, round(sum(x[key]==v for x in A)/len(A)*100,1), round(sum(x[key]==v for x in B)/len(B)*100,1))
    # 일별 누적 p
    ca=cb=na=nb=0; tr=[]
    for d in range(1,15):
        for x in r:
            if int(x["day"])==d:
                if x["variant"]=="A": na+=1; ca+=int(x["clicked"])
                else: nb+=1; cb+=int(x["clicked"])
        tr.append(two_prop(ca,na,cb,nb)["p"])
    print("  daily cum p", tr)

print("== 결과 사례")
for lab,c in dict(gamma=(50,1000,58,1000),big_tiny=(100000,1000000,101000,1000000),wide=(100,1000,130,1000),small=(10,100,13,100),same_rate_big=(1000,10000,1300,10000)).items():
    print(lab,two_prop(*c))
print("== 동전 100번 60번 양측", round(stats.binomtest(60,100,.5).pvalue,4), " 55번", round(stats.binomtest(55,100,.5).pvalue,3), "콜라 1/70", round(1/70,4))

rng=np.random.default_rng(20261121)
print("== A/A 차이 폭 (기준 10%) 95% 범위")
for n in [100,1000,4200,10000]:
    d=(rng.binomial(n,.1,200000)-rng.binomial(n,.1,200000))/n*100
    print(n, np.round(np.percentile(d,[2.5,97.5]),2))
print("== A/A 8회 예시 (군 500명)")
print(((rng.binomial(500,.1,8)-rng.binomial(500,.1,8))/500*100).round(1))

print("== A/A 1000회 유의 비율 (군 4200)")
a=rng.binomial(4200,.1,20000);b=rng.binomial(4200,.1,20000)
p=(a+b)/8400;z=(b-a)/4200/np.sqrt(p*(1-p)*2/4200);print(round(float((np.abs(z)>1.96).mean())*100,1))

print("== peeking 시뮬 (효과 0, 군 4200, 균등 확인)")
N=4200; sims=20000
ca=rng.binomial(1,.1,(1,1))
res={}
for k in [1,2,5,10,14,20,50,100]:
    pts=np.linspace(N/k,N,k).astype(int)
    a=np.zeros(sims,int);b=np.zeros(sims,int);prev=0;hit=np.zeros(sims,bool)
    for n in pts:
        step=n-prev;prev=n
        a+=rng.binomial(step,.1,sims);b+=rng.binomial(step,.1,sims)
        p=(a+b)/(2*n);se=np.sqrt(p*(1-p)*2/n)
        z=np.where(se>0,(b-a)/n/np.where(se>0,se,1),0)
        hit|=np.abs(z)>1.96
    res[k]=round(float(hit.mean())*100,1)
print(res)

print("== 다중 비교")
for k in [1,5,10,20,50]:
    print(k, round((1-.95**k)*100,1), "기대", k*.05, "본페로니", round(.05/k,4))

print("== 3주 연결 : 평균 대치의 효과")
# 지출 금액 지표, 결측 40%를 평균으로 대치
r2=np.random.default_rng(3)
n=200
A=r2.normal(5000,1500,n);B=r2.normal(5350,1500,n)
mask_a=r2.random(n)<.4;mask_b=r2.random(n)<.4
oa,ob=A[~mask_a],B[~mask_b]
ia=A.copy();ib=B.copy();ia[mask_a]=oa.mean();ib[mask_b]=ob.mean()
print("관측", len(oa),len(ob),round(oa.std(ddof=1)),round(ob.std(ddof=1)),"p",round(stats.ttest_ind(oa,ob,equal_var=False).pvalue,4))
print("대치", len(ia),len(ib),round(ia.std(ddof=1)),round(ib.std(ddof=1)),"p",round(stats.ttest_ind(ia,ib,equal_var=False).pvalue,4))
print("diff",round(ob.mean()-oa.mean()))
