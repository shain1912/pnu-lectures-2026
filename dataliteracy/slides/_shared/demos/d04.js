/* ============================================================
   데이터리터러시 4주차 데모 — 평균은 끌려가고 중앙값은 버틴다
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
  function mean(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s / a.length; }
  function median(a) {
    var b = a.slice().sort(function (x, y) { return x - y; }), n = b.length;
    return n % 2 ? b[(n - 1) / 2] : (b[n / 2 - 1] + b[n / 2]) / 2;
  }
  function sd(a) {
    var m = mean(a), s = 0;
    for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
    return Math.sqrt(s / a.length);
  }

  window.CGDemos["central-tendency"] = function (host) {
    var cv = document.createElement("canvas");
    cv.style.width = "100%";
    cv.style.display = "block";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d");

    var H = 318, N = 45;

    /* 점의 «정체»는 고정해 두고, 슬라이더로 치우침만 바꾼다 */
    var rnd = mulberry32(20261006);
    var Z = [], J = [], i;
    for (i = 0; i < N; i++) {
      var a = 1 - rnd(), b = rnd();
      Z.push(Math.sqrt(-2 * Math.log(a)) * Math.cos(2 * Math.PI * b));
    }
    for (i = 0; i < N; i++) J.push(rnd() * 2 - 1);

    /* 중앙값 아래는 손대지 않는다. 위쪽만 바깥으로 늘려 오른쪽 꼬리를 만든다.
       → 중앙값은 문자 그대로 제자리, 평균만 끌려간다 */
    var DEV = Z.map(function (z) { return 9 * z; });
    var DMAX = Math.max.apply(null, DEV);

    var skewS = host.parentNode.querySelector("[data-skew]");
    var outlS = host.parentNode.querySelector("[data-outlier]");
    var skewV = host.parentNode.querySelector("[data-skew-v]");
    var outlV = host.parentNode.querySelector("[data-outlier-v]");
    var out = host.parentNode.querySelector("[data-out]");

    var LO = 0, HI = 150, BINS = 26;
    var PADL = 34, PADR = 22, FARW = 96;   /* 오른쪽 «화면 밖» 구역은 항상 자리를 잡아 둔다 */
    var HIST_BOT = 190, HIST_TOP = 62;
    var AXIS_Y = 254, DOT_R = 24;
    var TOP = 58, BOT = 282;

    function build(s) {
      var v = [];
      for (var k = 0; k < N; k++) {
        var d = DEV[k];
        if (d > 0) d = d * (1 + 3.6 * s * Math.pow(d / DMAX, 0.7));
        v.push(38 + d);
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

      var skew = +skewS.value, outl = +outlS.value;
      var s = skew / 100;
      var plotW = Math.max(160, w - PADL - PADR - FARW);
      var brkX = PADL + plotW + 16;
      var farX = brkX + (w - PADR - brkX) / 2;
      function X(v) { return PADL + (v - LO) / (HI - LO) * plotW; }

      var vals = build(s);
      var oVal = outl > 0 ? 168 + outl / 100 * 732 : null;
      var all = oVal != null ? vals.concat([oVal]) : vals;

      skewV.textContent = skew === 0 ? "0 · 대칭" : String(skew);
      outlV.textContent = oVal == null ? "없음" : Math.round(oVal).toLocaleString();

      var m = mean(all), md = median(all), s2 = sd(all), diff = m - md;
      var mX = X(m), mdX = X(md);

      /* ── 두 대표값 사이의 «거짓말 폭» ───────────────────── */
      ctx.fillStyle = "rgba(255,90,77,.15)";
      ctx.fillRect(Math.min(mX, mdX), TOP, Math.abs(mX - mdX), BOT - TOP);

      /* ── 히스토그램 ──────────────────────────────────── */
      var h = new Array(BINS).fill(0), bi;
      for (var i = 0; i < all.length; i++) {
        bi = Math.floor((all[i] - LO) / (HI - LO) * BINS);
        if (bi >= 0 && bi < BINS) h[bi]++;
      }
      var maxH = Math.max.apply(null, h) || 1;
      var bw = plotW / BINS, ph = HIST_BOT - HIST_TOP;
      ctx.fillStyle = "rgba(53,214,230,.28)";
      for (i = 0; i < BINS; i++) {
        var bh = h[i] / maxH * ph;
        if (bh > 0) ctx.fillRect(PADL + i * bw + 1, HIST_BOT - bh, bw - 2, bh);
      }

      /* ── 점들이 놓인 수평선 ──────────────────────────── */
      ctx.strokeStyle = C.line; ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(PADL, AXIS_Y + .5); ctx.lineTo(PADL + plotW, AXIS_Y + .5);
      ctx.stroke();

      /* ── 점 ─────────────────────────────────────────── */
      ctx.fillStyle = "rgba(53,214,230,.72)";
      ctx.strokeStyle = "rgba(6,7,10,.9)"; ctx.lineWidth = 1.5;
      for (i = 0; i < N; i++) {
        var px = X(vals[i]), py = AXIS_Y + J[i] * DOT_R;
        ctx.beginPath(); ctx.arc(px, py, 5.4, 0, 6.2832);
        ctx.fill(); ctx.stroke();
      }

      /* ── 눈금 ───────────────────────────────────────── */
      ctx.fillStyle = C.faint;
      ctx.font = "12px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      for (var t = 0; t <= 150; t += 30) ctx.fillText(String(t), X(t), 302);

      /* ── 이상치가 사는 «화면 밖» 구역 ───────────────── */
      ctx.strokeStyle = C.line; ctx.lineWidth = 2;
      ctx.setLineDash([5, 6]);
      ctx.beginPath(); ctx.moveTo(brkX, TOP); ctx.lineTo(brkX, BOT); ctx.stroke();
      ctx.setLineDash([]);

      if (oVal != null) {
        ctx.strokeStyle = "rgba(255,90,77,.5)"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(brkX + 8, AXIS_Y); ctx.lineTo(farX - 14, AXIS_Y); ctx.stroke();
        ctx.fillStyle = C.trap;
        ctx.beginPath(); ctx.arc(farX, AXIS_Y, 9, 0, 6.2832); ctx.fill();
        ctx.font = "600 16px 'JetBrains Mono', monospace";
        ctx.fillText(Math.round(oVal).toLocaleString(), farX, AXIS_Y - 22);
        ctx.fillStyle = C.faint;
        ctx.font = "12px Pretendard, sans-serif";
        ctx.fillText("이상치 1개", farX, AXIS_Y + 34);
      } else {
        ctx.fillStyle = C.faint;
        ctx.font = "12px Pretendard, sans-serif";
        ctx.fillText("이상치 없음", farX, AXIS_Y + 5);
      }

      /* ── 중앙값(라임) ──────────────────────────────── */
      ctx.strokeStyle = C.lab; ctx.lineWidth = 3.5;
      ctx.beginPath(); ctx.moveTo(mdX, TOP); ctx.lineTo(mdX, BOT); ctx.stroke();

      /* ── 평균(흰색) ────────────────────────────────── */
      ctx.strokeStyle = C.fg; ctx.lineWidth = 3.5;
      ctx.beginPath(); ctx.moveTo(mX, TOP); ctx.lineTo(mX, BOT); ctx.stroke();

      /* ── 차이가 벌어지면 그 폭에 이름을 붙인다 ────────── */
      if (mX - mdX > 96) {
        ctx.fillStyle = "rgba(255,90,77,.95)";
        ctx.font = "600 14px Pretendard, sans-serif";
        ctx.fillText("이 폭만큼 왜곡", (mX + mdX) / 2, 222);
      }

      /* ── 라벨은 겹치지 않게 위아래로 나눈다 ─────────── */
      ctx.textAlign = "left";
      ctx.font = "700 16px Pretendard, sans-serif";
      ctx.fillStyle = C.fg;
      ctx.fillText("평균 " + m.toFixed(1), Math.min(mX + 9, w - 120), 34);
      ctx.fillStyle = C.lab;
      ctx.fillText("중앙값 " + md.toFixed(1), Math.min(mdX + 9, w - 130), 54);

      /* ── 읽기값 ─────────────────────────────────────── */
      var alarm = diff > 3;
      out.innerHTML =
        '평균 <b>' + m.toFixed(1) + "</b>　" +
        '중앙값 <b class="lab-txt">' + md.toFixed(1) + "</b>　" +
        '차이 <b style="color:' + (alarm ? C.trap : C.dim) + '">' +
        (diff >= 0 ? "+" : "") + diff.toFixed(1) + "</b>　" +
        '표준편차 <b>' + s2.toFixed(1) + "</b>" +
        (alarm
          ? '<br><span class="trap-txt">평균만 보고 시 이만큼 왜곡 — 절반이 ' +
            md.toFixed(1) + " 아래인데 대표값은 " + m.toFixed(1) + "</span>"
          : '<br><span class="muted">평균과 중앙값이 거의 일치 → 이 경우에만 평균이 대표값으로 적합</span>');
    }

    skewS.addEventListener("input", render);
    outlS.addEventListener("input", render);
    if (window.ResizeObserver) new ResizeObserver(render).observe(host);
    render();

    /* deck.js 의 렌더 루프와 맞추기 위한 최소 인터페이스.
       매 프레임 다시 그릴 필요는 없으므로 draw 는 비워 둔다. */
    return { draw: function () {} };
  };
})();
