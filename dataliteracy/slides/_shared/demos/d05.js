/* ============================================================
   데이터리터러시 5주차 데모 — 같은 원점수, 달라지는 z
   평균·표준편차·치우침을 바꾸면 z 와 이상치 기준선이 함께 이동한다.
   2D 캔버스만 사용한다.
   ============================================================ */
(function () {
  "use strict";
  window.CGDemos = window.CGDemos || {};

  var C = {
    gfx: "#35d6e6", vr: "#ff5fa2", trap: "#ff5a4d", lab: "#a8e05f",
    warn: "#ffc44d", fg: "#e8ecf4", dim: "#9aa4b8", faint: "#5f6980",
    grid: "#1e2431", line: "#2a3040", bg: "#06070a"
  };

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function mean(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s / a.length; }
  function sd(a) {
    var m = mean(a), s = 0;
    for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
    return Math.sqrt(s / (a.length - 1));
  }
  function quant(sorted, p) {
    var i = (sorted.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
    return lo === hi ? sorted[lo] : sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
  }
  /* 표준정규 누적분포 근사 — 백분위 표시용 */
  function cdf(z) {
    var t = 1 / (1 + 0.2316419 * Math.abs(z));
    var d = 0.3989423 * Math.exp(-z * z / 2);
    var p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 +
            t * (-1.821256 + t * 1.330274))));
    return z > 0 ? 1 - p : p;
  }

  window.CGDemos["standardize"] = function (host) {
    var cv = document.createElement("canvas");
    cv.style.width = "100%";
    cv.style.display = "block";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d");

    var H = 312, N = 60;

    /* 표본의 «모양»은 고정한다. 슬라이더는 위치·폭·치우침만 바꾼다 */
    var rnd = mulberry32(20261010);
    var Z = [], J = [], i;
    for (i = 0; i < N / 2; i++) {
      var a = 1 - rnd(), b = rnd();
      var z0 = Math.sqrt(-2 * Math.log(a)) * Math.cos(2 * Math.PI * b);
      Z.push(z0); Z.push(-z0);            /* 좌우대칭 → 치우침 0 에서 평균 일치 */
    }
    var zm = mean(Z), zs = sd(Z);
    for (i = 0; i < N; i++) Z[i] = (Z[i] - zm) / zs;
    for (i = 0; i < N; i++) J.push(rnd() * 2 - 1);

    var scoreS = host.parentNode.querySelector("[data-score]");
    var meanS = host.parentNode.querySelector("[data-mean]");
    var sdS = host.parentNode.querySelector("[data-sd]");
    var skewS = host.parentNode.querySelector("[data-skew]");
    var scoreV = host.parentNode.querySelector("[data-score-v]");
    var meanV = host.parentNode.querySelector("[data-mean-v]");
    var sdV = host.parentNode.querySelector("[data-sd-v]");
    var skewV = host.parentNode.querySelector("[data-skew-v]");
    var out = host.parentNode.querySelector("[data-out]");

    var PADL = 36, PADR = 30;
    var HIST_TOP = 74, HIST_BOT = 182;
    var AXIS_Y = 222, DOT_R = 18, TICK_Y = 268;

    function build(mu, s, k) {
      var v = [], d;
      for (var j = 0; j < N; j++) {
        d = Z[j] * s;
        if (d > 0) d = d * (1 + 3.2 * k * Math.pow(d / (3 * s), 0.8));
        v.push(mu + d);
      }
      return v;
    }

    function render() {
      var w = host.clientWidth || 900;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = w * dpr; cv.height = H * dpr;
      cv.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = C.bg; ctx.fillRect(0, 0, w, H);

      var score = +scoreS.value, mu0 = +meanS.value, sd0 = +sdS.value;
      var k = +skewS.value / 100;
      scoreV.textContent = score + "점";
      meanV.textContent = mu0 + "점";
      sdV.textContent = sd0 + "점";
      skewV.textContent = k === 0 ? "0 · 대칭" : String(Math.round(k * 100));

      var vals = build(mu0, sd0, k);
      var m = mean(vals), s = sd(vals);
      var srt = vals.slice().sort(function (x, y) { return x - y; });
      var q1 = quant(srt, 0.25), q3 = quant(srt, 0.75), iqr = q3 - q1;
      var zf = m + 3 * s, iqf = q3 + 1.5 * iqr;
      var zHit = 0, iHit = 0;
      for (i = 0; i < N; i++) {
        if (vals[i] > zf) zHit++;
        if (vals[i] > iqf) iHit++;
      }

      var z = (score - m) / s;
      var pct = cdf(z);

      /* ── x 축 범위 ───────────────────────────────────── */
      var lo = Math.min(srt[0], score, m - 3.4 * s);
      var hi = Math.max(srt[N - 1], score, zf);
      var pad = (hi - lo) * 0.06;
      lo -= pad; hi += pad;
      var plotW = w - PADL - PADR;
      function X(v) { return PADL + (v - lo) / (hi - lo) * plotW; }

      /* ── ±1σ · ±2σ · ±3σ 띠 ─────────────────────────── */
      var bands = [[3, "rgba(255,90,77,.045)"], [2, "rgba(255,196,77,.045)"],
                   [1, "rgba(168,224,95,.06)"]];
      for (i = 0; i < bands.length; i++) {
        ctx.fillStyle = bands[i][1];
        var x0 = X(m - bands[i][0] * s), x1 = X(m + bands[i][0] * s);
        ctx.fillRect(x0, HIST_TOP - 10, x1 - x0, AXIS_Y + DOT_R + 8 - HIST_TOP + 10);
      }

      /* ── 히스토그램 ─────────────────────────────────── */
      var BINS = 30, h = new Array(BINS).fill(0), bi;
      for (i = 0; i < N; i++) {
        bi = Math.floor((vals[i] - lo) / (hi - lo) * BINS);
        if (bi >= 0 && bi < BINS) h[bi]++;
      }
      var maxH = Math.max.apply(null, h) || 1;
      var bw = plotW / BINS, ph = HIST_BOT - HIST_TOP;
      ctx.fillStyle = "rgba(53,214,230,.30)";
      for (i = 0; i < BINS; i++) {
        var bh = h[i] / maxH * ph;
        if (bh > 0) ctx.fillRect(PADL + i * bw + 1, HIST_BOT - bh, bw - 2, bh);
      }

      /* ── 점 ─────────────────────────────────────────── */
      ctx.strokeStyle = C.line; ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(PADL, AXIS_Y + .5); ctx.lineTo(PADL + plotW, AXIS_Y + .5);
      ctx.stroke();
      ctx.strokeStyle = "rgba(6,7,10,.9)"; ctx.lineWidth = 1.4;
      for (i = 0; i < N; i++) {
        ctx.fillStyle = vals[i] > zf ? "rgba(255,90,77,.9)"
          : (vals[i] > iqf ? "rgba(255,196,77,.85)" : "rgba(53,214,230,.7)");
        ctx.beginPath();
        ctx.arc(X(vals[i]), AXIS_Y + J[i] * DOT_R, 5.2, 0, 6.2832);
        ctx.fill(); ctx.stroke();
      }

      /* ── 눈금 ───────────────────────────────────────── */
      ctx.fillStyle = C.faint;
      ctx.font = "12px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      for (var t = -3; t <= 3; t++) {
        var tx = X(m + t * s);
        if (tx < PADL || tx > PADL + plotW) continue;
        ctx.fillText((t === 0 ? "z 0" : (t > 0 ? "+" : "") + t), tx, TICK_Y);
      }

      /* ── 평균선 ─────────────────────────────────────── */
      ctx.strokeStyle = C.fg; ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(X(m), HIST_TOP - 8); ctx.lineTo(X(m), AXIS_Y + DOT_R + 6);
      ctx.stroke();
      ctx.fillStyle = C.fg;
      ctx.font = "700 13px Pretendard, sans-serif";
      ctx.fillText("평균 " + m.toFixed(1), X(m), HIST_TOP - 16);

      /* ── 기준선 두 개 ───────────────────────────────── */
      ctx.strokeStyle = C.trap; ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.moveTo(X(zf), HIST_TOP - 8); ctx.lineTo(X(zf), AXIS_Y + DOT_R + 6);
      ctx.stroke();
      ctx.fillStyle = C.trap;
      ctx.font = "600 12px 'JetBrains Mono', monospace";
      ctx.fillText("z+3  " + zf.toFixed(0), Math.min(X(zf), w - 40), HIST_TOP - 36);

      ctx.strokeStyle = C.lab; ctx.lineWidth = 2;
      ctx.setLineDash([6, 5]);
      ctx.beginPath();
      ctx.moveTo(X(iqf), HIST_TOP - 8); ctx.lineTo(X(iqf), AXIS_Y + DOT_R + 6);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = C.lab;
      ctx.fillText("IQR  " + iqf.toFixed(0), X(iqf), HIST_TOP - 54);

      /* ── 원점수 ─────────────────────────────────────── */
      var sx = X(score);
      ctx.strokeStyle = C.warn; ctx.lineWidth = 3.4;
      ctx.beginPath();
      ctx.moveTo(sx, HIST_TOP - 8); ctx.lineTo(sx, AXIS_Y + DOT_R + 20);
      ctx.stroke();
      ctx.fillStyle = C.warn;
      ctx.beginPath(); ctx.arc(sx, AXIS_Y + DOT_R + 20, 6.5, 0, 6.2832); ctx.fill();
      ctx.font = "700 15px Pretendard, sans-serif";
      ctx.fillText("원점수 " + score, Math.max(60, Math.min(sx, w - 60)), 32);
      ctx.font = "700 17px 'JetBrains Mono', monospace";
      ctx.fillStyle = z >= 0 ? C.gfx : C.vr;
      ctx.fillText("z = " + (z >= 0 ? "+" : "") + z.toFixed(2),
                   Math.max(60, Math.min(sx, w - 60)), 56);

      /* ── 읽기값 ─────────────────────────────────────── */
      var place = z >= 0
        ? "상위 약 " + ((1 - pct) * 100).toFixed(1) + "%"
        : "하위 약 " + (pct * 100).toFixed(1) + "%";
      var miss = iHit - zHit;
      out.innerHTML =
        '원점수 <b>' + score + "</b>　평균 <b>" + m.toFixed(1) +
        "</b>　표준편차 <b>" + s.toFixed(1) + "</b>　z = <b style=\"color:" +
        (z >= 0 ? C.gfx : C.vr) + '">' + (z >= 0 ? "+" : "") + z.toFixed(2) +
        "</b>　" + (k < 0.15 ? place : "<span class=\"muted\">" + place +
        " (대칭 분포 기준)</span>") +
        "<br>이상치 — ±3σ 바깥 <b>" + zHit + "개</b>　IQR 1.5배 바깥 <b>" +
        iHit + "개</b>" +
        (miss > 0
          ? '　<span class="trap-txt">치우침 → 표준편차 팽창 → z 기준이 ' +
            miss + "개 미탐지</span>"
          : '　<span class="muted">두 기준의 결과 일치</span>');
    }

    scoreS.addEventListener("input", render);
    meanS.addEventListener("input", render);
    sdS.addEventListener("input", render);
    skewS.addEventListener("input", render);
    if (window.ResizeObserver) new ResizeObserver(render).observe(host);
    render();

    return { draw: function () {} };
  };
})();
