/* ============================================================
   데이터리터러시 9주차 데모 2종
   fit-lab      : 모델 복잡도 조작 · 학습·검증 오차 비교 (과적합)
   confound-sim : 교란 강도 조작 · 기온 고정 전후 상관 비교 (교란)
   ============================================================ */
(function () {
  "use strict";
  window.CGDemos = window.CGDemos || {};
  var C = { teal: "#0d6b78", mag: "#a3245e", red: "#c2401d", olive: "#4f7a16", ochre: "#a8701a",
            ink: "#1b1a17", ink2: "#4a463e", ink3: "#8a8476", hair: "#cfc6b2", paper: "#fbf8f1" };
  var FONT = '"Pretendard Variable", Pretendard, "Malgun Gothic", sans-serif';

  function rng(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function gauss(r) { return Math.sqrt(-2 * Math.log(1 - r())) * Math.cos(2 * Math.PI * r()); }
  function canvasFor(host, H) {
    var cv = document.createElement("canvas");
    cv.style.width = "100%"; cv.style.display = "block";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d");
    return { cv: cv, ctx: ctx, begin: function () {
      var w = host.clientWidth || 1100, dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = w * dpr; cv.height = H * dpr; cv.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = C.paper; ctx.fillRect(0, 0, w, H);
      return w;
    } };
  }

  /* 최소제곱 다항 회귀 — x는 [-1,1] 범위로 스케일, 르장드르 기저로 수치 안정화 */
  function basis(x, deg) {
    var p = [1, x];
    for (var n = 1; n < deg; n++) p.push(((2 * n + 1) * x * p[n] - n * p[n - 1]) / (n + 1));
    return p.slice(0, deg + 1);
  }
  function fit(xs, ys, deg) {
    var m = deg + 1, A = [], i, j, k;
    for (i = 0; i < m; i++) { A.push(new Array(m + 1).fill(0)); }
    xs.forEach(function (x, q) {
      var b = basis(x, deg);
      for (i = 0; i < m; i++) { for (j = 0; j < m; j++) A[i][j] += b[i] * b[j]; A[i][m] += b[i] * ys[q]; }
    });
    for (i = 0; i < m; i++) A[i][i] += 1e-9;
    for (i = 0; i < m; i++) {
      var piv = i;
      for (k = i + 1; k < m; k++) if (Math.abs(A[k][i]) > Math.abs(A[piv][i])) piv = k;
      var tmp = A[i]; A[i] = A[piv]; A[piv] = tmp;
      for (k = i + 1; k < m; k++) {
        var f = A[k][i] / A[i][i];
        for (j = i; j <= m; j++) A[k][j] -= f * A[i][j];
      }
    }
    var w = new Array(m).fill(0);
    for (i = m - 1; i >= 0; i--) {
      var s = A[i][m];
      for (j = i + 1; j < m; j++) s -= A[i][j] * w[j];
      w[i] = s / A[i][i];
    }
    return function (x) { var b = basis(x, deg), v = 0; for (var q = 0; q < m; q++) v += w[q] * b[q]; return v; };
  }

  window.CGDemos["fit-lab"] = function (host) {
    var pc = canvasFor(host, 400), ctx = pc.ctx, root = host.parentNode;
    var dS = root.querySelector("[data-deg]"), dV = root.querySelector("[data-deg-v]");
    var nS = root.querySelector("[data-n]"), nV = root.querySelector("[data-n-v]");
    var out = root.querySelector("[data-out]"), seed = 909, dirty = true;
    function truth(x) { return 0.8 * Math.sin(3.2 * x) + 0.35 * x; }
    function sample(r, n) {
      var xs = [], ys = [];
      for (var i = 0; i < n; i++) { var x = -1 + 2 * r(); xs.push(x); ys.push(truth(x) + 0.28 * gauss(r)); }
      return { xs: xs, ys: ys };
    }
    function mae(f, d) { var s = 0; d.xs.forEach(function (x, i) { s += Math.abs(f(x) - d.ys[i]); }); return s / d.xs.length; }
    function render() {
      var w = pc.begin(), r = rng(seed), n = +nS.value, deg = +dS.value;
      var tr = sample(r, n), va = sample(rng(seed + 1), 200);
      var f = fit(tr.xs, tr.ys, deg);
      var split = w * 0.6, top = 44, base = 400 - 40;
      function X(x) { return 26 + (x + 1) / 2 * (split - 50); }
      function Y(y) { return base - (Math.max(-2.2, Math.min(2.2, y)) + 2.2) / 4.4 * (base - top); }
      ctx.font = "700 19px " + FONT; ctx.fillStyle = C.ink; ctx.textAlign = "left";
      ctx.fillText("모델 곡선 · 파랑 = 학습 " + n + "개 · 분홍 = 검증 200개", 26, 28);
      ctx.fillStyle = C.mag; ctx.globalAlpha = 0.28;
      va.xs.forEach(function (x, i) { ctx.beginPath(); ctx.arc(X(x), Y(va.ys[i]), 3, 0, 7); ctx.fill(); });
      ctx.globalAlpha = 1; ctx.fillStyle = C.teal;
      tr.xs.forEach(function (x, i) { ctx.beginPath(); ctx.arc(X(x), Y(tr.ys[i]), 5, 0, 7); ctx.fill(); });
      ctx.save(); ctx.beginPath(); ctx.rect(20, top - 6, split - 36, base - top + 12); ctx.clip();
      ctx.strokeStyle = C.red; ctx.lineWidth = 3; ctx.beginPath();
      for (var i = 0; i <= 300; i++) { var x = -1 + i / 150; var px = X(x), py = Y(f(x)); if (i) ctx.lineTo(px, py); else ctx.moveTo(px, py); }
      ctx.stroke(); ctx.restore(); ctx.lineWidth = 1;

      /* 복잡도별 오차 곡선 */
      var maxD = Math.min(15, n - 1), tE = [], vE = [], d;
      for (d = 0; d <= maxD; d++) { var g = fit(tr.xs, tr.ys, Math.max(d, 1)); if (d === 0) { var m = tr.ys.reduce(function (a, b) { return a + b; }, 0) / n; g = function () { return m; }; } tE.push(mae(g, tr)); vE.push(Math.min(2, mae(g, va))); }
      var x0 = split + 42, x1 = w - 26, cb = base, ct = top + 16, ymax = 1.2;
      function X2(q) { return x0 + q / 15 * (x1 - x0); }
      function Y2(v) { return cb - Math.min(v, ymax) / ymax * (cb - ct); }
      ctx.fillStyle = C.ink; ctx.font = "700 19px " + FONT; ctx.textAlign = "left";
      ctx.fillText("복잡도별 오차 (MAE)", x0 - 20, 28);
      ctx.strokeStyle = C.ink2; ctx.beginPath(); ctx.moveTo(x0, ct); ctx.lineTo(x0, cb); ctx.lineTo(x1, cb); ctx.stroke();
      [[tE, C.teal], [vE, C.mag]].forEach(function (s) {
        ctx.strokeStyle = s[1]; ctx.lineWidth = 3; ctx.beginPath();
        s[0].forEach(function (v, q) { if (q) ctx.lineTo(X2(q), Y2(v)); else ctx.moveTo(X2(q), Y2(v)); }); ctx.stroke();
      });
      ctx.lineWidth = 1;
      var dd = Math.min(deg, maxD);
      ctx.strokeStyle = C.ink; ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(X2(dd), ct); ctx.lineTo(X2(dd), cb); ctx.stroke(); ctx.setLineDash([]);
      var best = 1; vE.forEach(function (v, q) { if (q >= 1 && v < vE[best]) best = q; });
      ctx.fillStyle = C.olive; ctx.beginPath(); ctx.arc(X2(best), Y2(vE[best]), 7, 0, 7); ctx.fill();
      ctx.font = "16px " + FONT; ctx.fillStyle = C.ink3; ctx.textAlign = "center";
      ctx.fillText("단순", x0 + 18, cb + 22); ctx.fillText("복잡", x1 - 16, cb + 22);
      ctx.font = "700 16px " + FONT; ctx.textAlign = "right";
      ctx.fillStyle = C.teal; ctx.fillText("학습 오차", x1, ct + 16); ctx.fillStyle = C.mag; ctx.fillText("검증 오차", x1, ct + 38);
      ctx.fillStyle = C.olive; ctx.fillText("● 검증 최소", x1, ct + 60);
      var te = mae(f, tr), ve = mae(f, va);
      dV.textContent = deg + "차"; nV.textContent = n + "개";
      out.innerHTML = "복잡도 <b>" + deg + "차</b> · 학습 오차 <b>" + te.toFixed(2) + "</b> · 검증 오차 <b style='color:" + (deg === best ? C.olive : C.red) + "'>" + ve.toFixed(2) + "</b> · 검증 최소 복잡도 <b>" + best + "차</b>";
    }
    [dS, nS].forEach(function (s) { s.addEventListener("input", function () { dirty = true; }); });
    root.querySelector("[data-rerun]").addEventListener("click", function () { seed += 11; dirty = true; });
    window.addEventListener("resize", function () { dirty = true; });
    return { draw: function () { if (dirty) { dirty = false; render(); } } };
  };

  window.CGDemos["confound-sim"] = function (host) {
    var pc = canvasFor(host, 400), ctx = pc.ctx, root = host.parentNode;
    var cS = root.querySelector("[data-conf]"), cV = root.querySelector("[data-conf-v]");
    var eS = root.querySelector("[data-direct]"), eV = root.querySelector("[data-direct-v]");
    var tg = root.querySelector("[data-strat]"), out = root.querySelector("[data-out]");
    var seed = 87, dirty = true, strat = false;
    function fmt(v) { var s = v.toFixed(2); return s === "-0.00" ? "0.00" : s; }
    function fmt(v) { var s = v.toFixed(2); return s === "-0.00" ? "0.00" : s; }
    function pearson(a, b) {
      var n = a.length, ma = 0, mb = 0, i; for (i = 0; i < n; i++) { ma += a[i]; mb += b[i]; } ma /= n; mb /= n;
      var sa = 0, sb = 0, sab = 0; for (i = 0; i < n; i++) { sa += (a[i] - ma) * (a[i] - ma); sb += (b[i] - mb) * (b[i] - mb); sab += (a[i] - ma) * (b[i] - mb); }
      return sab / Math.sqrt(sa * sb || 1);
    }
    function residual(y, t) {
      var n = y.length, mt = 0, my = 0, i; for (i = 0; i < n; i++) { mt += t[i]; my += y[i]; } mt /= n; my /= n;
      var st = 0, sty = 0; for (i = 0; i < n; i++) { st += (t[i] - mt) * (t[i] - mt); sty += (t[i] - mt) * (y[i] - my); }
      var b = sty / (st || 1); return y.map(function (v, q) { return v - my - b * (t[q] - mt); });
    }
    function render() {
      var w = pc.begin(), r = rng(seed), conf = +cS.value / 100, dir = +eS.value / 100, n = 300, T = [], A = [], B = [], i;
      for (i = 0; i < n; i++) {
        var t = gauss(r), a = conf * t + Math.sqrt(1 - conf * conf) * gauss(r);
        var b = conf * t + dir * a + Math.sqrt(Math.max(0.05, 1 - conf * conf)) * gauss(r);
        T.push(t); A.push(a); B.push(b);
      }
      var rAll = pearson(A, B), rA = residual(A, T), rB = residual(B, T), rPart = pearson(rA, rB);
      var xs = strat ? rA : A, ys = strat ? rB : B;
      var split = w * 0.6, top = 46, base = 400 - 34;
      function X(v) { return 34 + (Math.max(-3.4, Math.min(3.4, v)) + 3.4) / 6.8 * (split - 60); }
      function Y(v) { return base - (Math.max(-3.4, Math.min(3.4, v)) + 3.4) / 6.8 * (base - top); }
      ctx.font = "700 19px " + FONT; ctx.fillStyle = C.ink; ctx.textAlign = "left";
      ctx.fillText(strat ? "기온 효과 제거 : 기온으로 설명 안 되는 부분끼리" : "전체 : 점 색 = 기온 (파랑 추움 · 빨강 더움)", 26, 28);
      ctx.strokeStyle = C.hair; ctx.strokeRect(34, top, split - 60, base - top);
      xs.forEach(function (v, q) {
        var f = Math.max(0, Math.min(1, (T[q] + 2) / 4));
        ctx.fillStyle = strat ? C.olive : "rgb(" + Math.round(13 + f * 181) + "," + Math.round(107 - f * 43) + "," + Math.round(120 - f * 91) + ")";
        ctx.globalAlpha = 0.75; ctx.beginPath(); ctx.arc(X(v), Y(ys[q]), 3.6, 0, 7); ctx.fill();
      });
      ctx.globalAlpha = 1;
      var x0 = split + 26, col = strat ? C.olive : C.red;
      ctx.fillStyle = C.ink; ctx.font = "700 19px " + FONT; ctx.fillText("상관계수 r", x0, 28);
      ctx.fillStyle = C.red; ctx.font = "900 62px " + FONT; ctx.fillText(fmt(rAll), x0, 100);
      ctx.font = "700 17px " + FONT; ctx.fillText("전체", x0, 126);
      ctx.fillStyle = C.olive; ctx.font = "900 62px " + FONT; ctx.fillText(fmt(rPart), x0, 208);
      ctx.font = "700 17px " + FONT; ctx.fillText("기온 효과 제거 후", x0, 234);
      ctx.fillStyle = C.ink2; ctx.font = "17px " + FONT;
      var m = Math.abs(rPart) >= 0.12 ? "제거 후 남는 r = 직접 관계 후보"
        : (Math.abs(rAll) >= 0.3 ? "제거 후 r ≈ 0 → 전체 r 대부분 교란" : "r ≈ 0 · 잡음과 구분 불가");
      ctx.fillText(m, x0, 280);
      ctx.fillText("n = " + n + " · 교육용 합성 데이터", x0, 308);
      cV.textContent = conf.toFixed(2); eV.textContent = dir.toFixed(2);
      tg.textContent = strat ? "전체 보기" : "기온 효과 제거";
      out.innerHTML = "기온 영향 <b>" + conf.toFixed(2) + "</b> · 직접 효과 <b>" + dir.toFixed(2) + "</b> → 전체 r <b style='color:" + C.red + "'>" + fmt(rAll) + "</b> · 기온 효과 제거 r <b style='color:" + C.olive + "'>" + fmt(rPart) + "</b>";
    }
    [cS, eS].forEach(function (s) { s.addEventListener("input", function () { dirty = true; }); });
    tg.addEventListener("click", function () { strat = !strat; dirty = true; });
    root.querySelector("[data-rerun]").addEventListener("click", function () { seed += 13; dirty = true; });
    window.addEventListener("resize", function () { dirty = true; });
    return { draw: function () { if (dirty) { dirty = false; render(); } } };
  };
})();
