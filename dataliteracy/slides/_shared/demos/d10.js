/* ============================================================
   데이터리터러시 10주차 데모 — 배정 방식 비교기
   같은 실험을 200번 반복 · 방식별 사전 특성 차이와 추정 효과의 편향 확인
   모형 : 숨은 특성 u(50%) · 클릭률 = 10% + 교란 강도×u + 2%×처치
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
  function binom(r, n, p) {
    if (n <= 0) return 0;
    if (n < 60) { var k = 0; for (var i = 0; i < n; i++) if (r() < p) k++; return k; }
    return Math.max(0, Math.min(n, Math.round(n * p + gauss(r) * Math.sqrt(n * p * (1 - p)))));
  }

  var MODES = {
    volunteer: { name: "자원자 모집", t1: 0.85, t0: 0.20, color: C.red },
    post:      { name: "사후 비교",   t1: 0.70, t0: 0.30, color: C.ochre },
    random:    { name: "무작위 배정", t1: 0.50, t0: 0.50, color: C.olive }
  };
  var TRUE = 2, REPS = 200;

  window.CGDemos["assign-compare"] = function (host) {
    var cv = document.createElement("canvas");
    cv.style.width = "100%"; cv.style.display = "block";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d"), H = 400;
    var root = host.parentNode;
    var nS = root.querySelector("[data-n]"), nV = root.querySelector("[data-n-v]");
    var cS = root.querySelector("[data-conf]"), cV = root.querySelector("[data-conf-v]");
    var out = root.querySelector("[data-out]");
    var btns = root.querySelectorAll("[data-mode]");
    var mode = "volunteer", seed = 1011, dirty = true, res = null;

    function simulate() {
      var m = MODES[mode], N = +nS.value, conf = +cS.value / 100, r = rng(seed);
      var est = [], preT = [], preC = [];
      for (var k = 0; k < REPS; k++) {
        var u1 = binom(r, N, 0.5), u0 = N - u1;
        var t1 = binom(r, u1, m.t1), t0 = binom(r, u0, m.t0);
        var c1 = u1 - t1, c0 = u0 - t0;
        var nT = t1 + t0, nC = c1 + c0;
        if (!nT || !nC) continue;
        var yT = binom(r, t1, 0.10 + conf + TRUE / 100) + binom(r, t0, 0.10 + TRUE / 100);
        var yC = binom(r, c1, 0.10 + conf) + binom(r, c0, 0.10);
        est.push((yT / nT - yC / nC) * 100);
        preT.push(t1 / nT * 100); preC.push(c1 / nC * 100);
      }
      function mean(a) { return a.reduce(function (s, v) { return s + v; }, 0) / a.length; }
      res = { est: est, mT: mean(est), preT: mean(preT), preC: mean(preC), lastT: preT[preT.length - 1], lastC: preC[preC.length - 1], m: m, N: N };
    }

    function render() {
      simulate();
      var w = host.clientWidth || 1100, dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = w * dpr; cv.height = H * dpr; cv.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = C.paper; ctx.fillRect(0, 0, w, H);
      var m = res.m, split = w * 0.36;

      /* 왼쪽 : 처치 전 특성 */
      ctx.font = "700 19px " + FONT; ctx.fillStyle = C.ink; ctx.textAlign = "left";
      ctx.fillText("처치 전 · 동기 높은 사람 비율", 24, 30);
      var base = H - 46, top = 66, bw = split * 0.26, xs = [split * 0.24, split * 0.62];
      var vals = [res.preT, res.preC], labs = ["실험군", "대조군"];
      ctx.strokeStyle = C.hair; ctx.beginPath(); ctx.moveTo(24, base + .5); ctx.lineTo(split - 16, base + .5); ctx.stroke();
      for (var i = 0; i < 2; i++) {
        var h = (base - top) * vals[i] / 100;
        ctx.fillStyle = m.color; ctx.globalAlpha = i ? 0.45 : 0.9;
        ctx.fillRect(xs[i], base - h, bw, h); ctx.globalAlpha = 1;
        ctx.font = "900 28px " + FONT; ctx.fillStyle = m.color; ctx.textAlign = "center";
        ctx.fillText(vals[i].toFixed(0) + "%", xs[i] + bw / 2, base - h - 8);
        ctx.font = "600 17px " + FONT; ctx.fillStyle = C.ink2;
        ctx.fillText(labs[i], xs[i] + bw / 2, base + 20);
      }

      /* 오른쪽 : 추정 효과 */
      var x0 = split + 26, x1 = w - 30, lo = -6, hi = 22;
      function X(v) { return x0 + (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo) * (x1 - x0); }
      ctx.textAlign = "left"; ctx.font = "700 19px " + FONT; ctx.fillStyle = C.ink;
      ctx.fillText("같은 실험 " + REPS + "번 · 추정된 효과 (점 하나 = 실험 1회)", x0, 30);
      var ax = H - 58;
      ctx.strokeStyle = C.ink2; ctx.beginPath(); ctx.moveTo(x0, ax + .5); ctx.lineTo(x1, ax + .5); ctx.stroke();
      ctx.textAlign = "center"; ctx.font = "16px " + FONT; ctx.fillStyle = C.ink3;
      for (var t = lo; t <= hi; t += 4) {
        ctx.fillRect(X(t), ax, 1, 5);
        ctx.fillText((t > 0 ? "+" : "") + t, X(t), ax + 20);
      }
      ctx.fillText("클릭률 차이 (%포인트)", (x0 + x1) / 2, ax + 39);
      /* 점 : 쌓기 */
      var bins = {}, bwid = 0.5;
      ctx.fillStyle = m.color; ctx.globalAlpha = 0.72;
      var off = 0;
      res.est.forEach(function (v) {
        if (v < lo || v > hi) { off++; return; }
        var b = Math.round(v / bwid); bins[b] = (bins[b] || 0) + 1;
        var yy = ax - 7 - (bins[b] - 1) * 6.2;
        if (yy > 48) { ctx.beginPath(); ctx.arc(X(b * bwid), yy, 3, 0, 7); ctx.fill(); }
      });
      ctx.globalAlpha = 1;
      if (off) { ctx.font = "700 16px " + FONT; ctx.fillStyle = C.ink2; ctx.textAlign = "right"; ctx.fillText("축 밖 " + off + "개", x1, 56); }
      /* 참값·평균 */
      ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.setLineDash([5, 4]);
      ctx.beginPath(); ctx.moveTo(X(TRUE), 44); ctx.lineTo(X(TRUE), ax); ctx.stroke(); ctx.setLineDash([]); ctx.lineWidth = 1;
      ctx.font = "700 16px " + FONT; ctx.fillStyle = C.ink; ctx.textAlign = "right";
      ctx.fillText("실제 효과 +" + TRUE, X(TRUE) - 6, 56);
      var bias = res.mT - TRUE;
      ctx.strokeStyle = m.color; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.moveTo(X(res.mT), 44); ctx.lineTo(X(res.mT), ax); ctx.stroke(); ctx.lineWidth = 1;
      if (Math.abs(bias) > 0.6) {
        ctx.font = "700 16px " + FONT; ctx.fillStyle = m.color; ctx.textAlign = "left";
        ctx.fillText("평균 추정 " + (res.mT >= 0 ? "+" : "") + res.mT.toFixed(1), X(res.mT) + 6, 56);
      }
      nV.textContent = (+nS.value).toLocaleString() + "명";
      cV.textContent = "+" + cS.value + "점";
      btns.forEach(function (b) {
        var on = b.dataset.mode === mode;
        b.style.background = on ? C.ink : ""; b.style.color = on ? "#f5f1e8" : "";
      });
      out.innerHTML = "<b>" + m.name + "</b> · 사전 차이 <b>" + Math.abs(res.preT - res.preC).toFixed(0) +
        "점</b> · 평균 추정 <b>" + (res.mT >= 0 ? "+" : "") + res.mT.toFixed(1) + "점</b> · 편향 <b style='color:" + m.color + "'>" +
        (bias >= 0 ? "+" : "") + bias.toFixed(1) + "점</b>";
    }

    btns.forEach(function (b) { b.addEventListener("click", function () { mode = b.dataset.mode; dirty = true; }); });
    [nS, cS].forEach(function (s) { s.addEventListener("input", function () { dirty = true; }); });
    var re = root.querySelector("[data-rerun]");
    if (re) re.addEventListener("click", function () { seed += 7; dirty = true; });
    window.addEventListener("resize", function () { dirty = true; });

    return { draw: function () { if (dirty) { dirty = false; render(); } } };
  };
})();
