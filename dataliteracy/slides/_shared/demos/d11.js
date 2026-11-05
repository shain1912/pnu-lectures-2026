/* ============================================================
   데이터리터러시 11주차 데모 — 유의성 시뮬레이터
   기준 클릭률 10% · 실제 효과 · 표본 · 중간 확인 횟수를 조작해 실험 1,000번 반복
   중간 확인 : 균등 간격 확인 · 한 번이라도 p<0.05 면 그 자리에서 종료
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
    if (n < 40) { var k = 0; for (var i = 0; i < n; i++) if (r() < p) k++; return k; }
    return Math.max(0, Math.min(n, Math.round(n * p + gauss(r) * Math.sqrt(n * p * (1 - p)))));
  }
  /* 표준정규 양측 p (Abramowitz-Stegun 근사) */
  function pval(z) {
    z = Math.abs(z);
    var t = 1 / (1 + 0.2316419 * z), d = 0.3989423 * Math.exp(-z * z / 2);
    var q = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
    return 2 * q;
  }

  var REPS = 1000;

  window.CGDemos["sig-sim"] = function (host) {
    var cv = document.createElement("canvas");
    cv.style.width = "100%"; cv.style.display = "block";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d"), H = 400, root = host.parentNode;
    var eS = root.querySelector("[data-eff]"), eV = root.querySelector("[data-eff-v]");
    var nS = root.querySelector("[data-n]"), nV = root.querySelector("[data-n-v]");
    var pS = root.querySelector("[data-peek]"), pV = root.querySelector("[data-peek-v]");
    var out = root.querySelector("[data-out]"), al = root.querySelector("[data-alert]");
    var seed = 1121, dirty = true;
    var NS = [100, 200, 500, 1000, 2000, 4200, 8000, 15000, 30000];

    function run() {
      var eff = +eS.value / 100, N = NS[+nS.value], K = +pS.value, r = rng(seed);
      var sig = 0, ps = [], diffs = [], sigDiffs = [];
      for (var s = 0; s < REPS; s++) {
        var a = 0, b = 0, prev = 0, hit = false, lastP = 1, lastD = 0;
        for (var k = 1; k <= K; k++) {
          var n = Math.round(N * k / K), st = n - prev; prev = n;
          a += binom(r, st, 0.10); b += binom(r, st, 0.10 + eff);
          var pa = a / n, pb = b / n, pp = (a + b) / (2 * n);
          var se = Math.sqrt(pp * (1 - pp) * 2 / n);
          var z = se > 0 ? (pb - pa) / se : 0;
          lastP = pval(z); lastD = (pb - pa) * 100;
          if (lastP < 0.05) { hit = true; break; }
        }
        if (hit && (eff === 0 || lastD > 0)) { sig++; sigDiffs.push(lastD); }
        ps.push(lastP); diffs.push(lastD);
      }
      return { sig: sig / REPS * 100, ps: ps, sigDiffs: sigDiffs, eff: eff * 100, N: N, K: K };
    }

    function render() {
      var R = run();
      var w = host.clientWidth || 1100, dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = w * dpr; cv.height = H * dpr; cv.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = C.paper; ctx.fillRect(0, 0, w, H);
      var zero = R.eff === 0, col = zero ? C.red : C.teal, split = w * 0.34;

      /* 왼쪽 : 유의 판정 비율 */
      ctx.textAlign = "left"; ctx.font = "700 19px " + FONT; ctx.fillStyle = C.ink;
      ctx.fillText("실험 " + REPS.toLocaleString() + "번 중 «유의» 판정", 24, 30);
      ctx.font = "900 84px " + FONT; ctx.fillStyle = col;
      ctx.fillText(R.sig.toFixed(1) + "%", 24, 130);
      ctx.font = "700 19px " + FONT; ctx.fillStyle = col;
      ctx.fillText(zero ? "전부 거짓 양성 (효과 0)" : (R.K > 1 ? "올바른 방향 유의 판정 비율" : "검정력 : 올바른 방향으로 찾아낸 비율"), 24, 164);
      /* 게이지 */
      var gx = 24, gy = 190, gw = split - 48;
      ctx.fillStyle = "#ece6d8"; ctx.fillRect(gx, gy, gw, 16);
      ctx.fillStyle = col; ctx.fillRect(gx, gy, gw * Math.min(1, R.sig / 100), 16);
      var mark = zero ? 5 : 80;
      ctx.fillStyle = C.ink; ctx.fillRect(gx + gw * mark / 100 - 1, gy - 5, 2, 26);
      ctx.font = "600 16px " + FONT; ctx.fillStyle = C.ink2;
      ctx.fillText(zero ? "기준 5%" : "목표 80%", Math.min(gx + gw * mark / 100 + 5, gx + gw - 60), gy + 36);
      if (R.sigDiffs.length && !zero) {
        var m = R.sigDiffs.reduce(function (s, v) { return s + Math.abs(v); }, 0) / R.sigDiffs.length;
        ctx.font = "16px " + FONT; ctx.fillStyle = C.ink2;
        ctx.fillText("유의한 실험만의 평균 효과 : " + m.toFixed(2) + "점 (실제 " + R.eff.toFixed(1) + "점)", 24, gy + 66);
      }

      /* 오른쪽 : 최종 p값 히스토그램 */
      var x0 = split + 28, x1 = w - 24, top = 56, base = H - 54;
      ctx.textAlign = "left"; ctx.font = "700 19px " + FONT; ctx.fillStyle = C.ink;
      ctx.fillText("각 실험의 마지막 p값 분포", x0, 30);
      var bins = new Array(20).fill(0);
      R.ps.forEach(function (p) { bins[Math.min(19, Math.floor(p * 20))]++; });
      var mx = Math.max.apply(null, bins.concat([REPS / 20 * 2])), bw = (x1 - x0) / 20;
      bins.forEach(function (c, i) {
        var h = (base - top) * c / mx;
        ctx.fillStyle = i === 0 ? col : "#b7b0a0";
        ctx.fillRect(x0 + i * bw + 1, base - h, bw - 2, h);
      });
      ctx.strokeStyle = C.ink2; ctx.beginPath(); ctx.moveTo(x0, base + .5); ctx.lineTo(x1, base + .5); ctx.stroke();
      ctx.font = "16px " + FONT; ctx.fillStyle = C.ink3; ctx.textAlign = "center";
      [0, 0.2, 0.4, 0.6, 0.8, 1].forEach(function (t) { ctx.fillText(t.toFixed(1), x0 + (x1 - x0) * t, base + 19); });
      ctx.fillText("p값", (x0 + x1) / 2, base + 38);
      ctx.textAlign = "left"; ctx.font = "700 16px " + FONT; ctx.fillStyle = col;
      ctx.fillText("← 첫 칸 p < 0.05", x0 + bw + 6, top + 2);
      if (zero && R.K === 1) { ctx.fillStyle = C.ink2; ctx.font = "16px " + FONT; ctx.textAlign = "right"; ctx.fillText("효과 0 · 확인 1회 → 거의 평평한 분포", x1, top + 2); }

      eV.textContent = "+" + R.eff.toFixed(1) + "점";
      nV.textContent = R.N.toLocaleString() + "명";
      pV.textContent = R.K + "회";
      out.innerHTML = "실제 효과 <b>+" + R.eff.toFixed(1) + "점</b> · 집단당 <b>" + R.N.toLocaleString() + "명</b> · 중간 확인 <b>" + R.K + "회</b> → 유의 판정 <b style='color:" + col + "'>" + R.sig.toFixed(1) + "%</b>";
      if (al) {
        al.classList.toggle("on", zero && R.sig > 8);
        al.textContent = "효과 0인데 거짓 양성 " + R.sig.toFixed(0) + "%";
      }
    }

    [eS, nS, pS].forEach(function (s) { s.addEventListener("input", function () { dirty = true; }); });
    var re = root.querySelector("[data-rerun]");
    if (re) re.addEventListener("click", function () { seed += 13; dirty = true; });
    window.addEventListener("resize", function () { dirty = true; });
    return { draw: function () { if (dirty) { dirty = false; render(); } } };
  };
})();
