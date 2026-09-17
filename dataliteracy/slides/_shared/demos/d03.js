/* ============================================================
   데이터리터러시 3주차 데모 — 평균 대치가 분포를 어떻게 망가뜨리는가
   three.js 를 쓰지 않는다. 2D 캔버스만으로 충분하고 가볍다.
   ============================================================ */
(function () {
  "use strict";
  window.CGDemos = window.CGDemos || {};

  var C = {
    gfx: "#35d6e6", vr: "#ff5fa2", trap: "#ff5a4d", lab: "#a8e05f",
    warn: "#ffc44d", fg: "#e8ecf4", dim: "#9aa4b8", faint: "#5f6980",
    grid: "#1e2431", line: "#2a3040", bg: "#06070a"
  };

  /* 재현 가능한 난수 — 수업마다 같은 그림이 나와야 한다 */
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function normals(n, mu, sd, seed) {
    var r = mulberry32(seed), out = [];
    for (var i = 0; i < n; i++) {
      var u = 1 - r(), v = r();
      out.push(mu + sd * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v));
    }
    return out;
  }
  function mean(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s / a.length; }
  function sd(a) {
    var m = mean(a), s = 0;
    for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
    return Math.sqrt(s / a.length);
  }

  window.CGDemos["imputation"] = function (host) {
    var cv = document.createElement("canvas");
    cv.style.width = "100%";
    cv.style.display = "block";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d");

    var H = 320;
    var DATA = normals(600, 40, 12, 20260910).filter(function (v) { return v > 2 && v < 88; });
    /* 어느 값이 비는지는 고정해 두고, 슬라이더로 «몇 %까지» 비울지만 바꾼다 */
    var r = mulberry32(77);
    var order = DATA.map(function (v, i) { return { v: v, k: r(), i: i }; })
                    .sort(function (a, b) { return a.k - b.k; });

    var pctS = host.parentNode.querySelector("[data-pct]");
    var pctV = host.parentNode.querySelector("[data-pct-v]");
    var out = host.parentNode.querySelector("[data-out]");

    var BINS = 34, LO = 0, HI = 90;

    function hist(vals) {
      var h = new Array(BINS).fill(0);
      for (var i = 0; i < vals.length; i++) {
        var b = Math.floor((vals[i] - LO) / (HI - LO) * BINS);
        if (b >= 0 && b < BINS) h[b]++;
      }
      return h;
    }

    function panel(x0, w, vals, color, title) {
      var h = hist(vals);
      var maxH = Math.max.apply(null, h);
      var top = 58, bot = H - 46, ph = bot - top;
      var bw = w / BINS;

      ctx.strokeStyle = C.line; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x0, bot + 0.5); ctx.lineTo(x0 + w, bot + 0.5); ctx.stroke();

      ctx.fillStyle = color;
      for (var i = 0; i < BINS; i++) {
        var bh = maxH ? h[i] / maxH * ph : 0;
        ctx.fillRect(x0 + i * bw + 0.6, bot - bh, bw - 1.2, bh);
      }

      var m = mean(vals), s = sd(vals);
      var mx = x0 + (m - LO) / (HI - LO) * w;
      ctx.strokeStyle = C.fg; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(mx, top - 6); ctx.lineTo(mx, bot); ctx.stroke();

      ctx.fillStyle = color;
      ctx.font = "600 15px Pretendard, sans-serif";
      ctx.fillText(title, x0, 26);
      ctx.fillStyle = C.fg;
      ctx.font = "500 14px 'JetBrains Mono', monospace";
      ctx.fillText("평균 " + m.toFixed(1) + "   표준편차 " + s.toFixed(1), x0, 46);

      /* 눈금 */
      ctx.fillStyle = C.faint;
      ctx.font = "11px 'JetBrains Mono', monospace";
      for (var t = 0; t <= 80; t += 20) {
        var tx = x0 + (t - LO) / (HI - LO) * w;
        ctx.fillText(String(t), tx - 6, bot + 18);
      }
      return s;
    }

    function render() {
      var w = host.clientWidth || 900;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = w * dpr; cv.height = H * dpr;
      cv.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = C.bg; ctx.fillRect(0, 0, w, H);

      var pct = +pctS.value;
      pctV.textContent = pct + " %";

      var nMiss = Math.round(order.length * pct / 100);
      var obs = order.slice(nMiss).map(function (o) { return o.v; });
      if (obs.length < 5) obs = order.slice(-5).map(function (o) { return o.v; });

      var filled = obs.slice();
      var om = mean(obs);
      for (var i = 0; i < nMiss; i++) filled.push(om);

      var pad = 26, gap = 46;
      var pw = (w - pad * 2 - gap) / 2;
      var s0 = panel(pad, pw, DATA, C.gfx, "원래 분포 (결측 없음)");
      var s1 = panel(pad + pw + gap, pw, filled, C.trap, "평균으로 채운 뒤");

      var drop = (1 - s1 / s0) * 100;
      out.innerHTML =
        "결측 <b>" + pct + "%</b>　" +
        '<b class="gfx-txt">원래 표준편차 ' + s0.toFixed(1) + "</b> → " +
        '<b class="trap-txt">' + s1.toFixed(1) + "</b>　" +
        '<b style="color:' + (drop > 12 ? "#ff5a4d" : "#9aa4b8") + '">' +
        drop.toFixed(0) + "% 감소</b>" +
        (drop > 12 ? '　<span class="trap-txt">← 없는 차이가 «유의» 로 나오기 시작하는 구간</span>' : "");
    }

    pctS.addEventListener("input", render);
    if (window.ResizeObserver) new ResizeObserver(render).observe(host);
    render();

    /* deck.js 의 렌더 루프와 맞추기 위한 최소 인터페이스.
       매 프레임 다시 그릴 필요는 없으므로 draw 는 비워 둔다. */
    return { draw: function () {} };
  };
})();
