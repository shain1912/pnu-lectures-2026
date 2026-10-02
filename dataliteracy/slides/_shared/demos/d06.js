/* ============================================================
   데이터리터러시 6주차 데모 — 차트 조작기
   왼쪽: 4분기 매출 막대 (y축 시작값 · 정렬 · 3D 효과)
   오른쪽: 같은 데이터의 분포 (구간 개수)
   2D 캔버스만 사용
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

  window.CGDemos["chart-trick"] = function (host) {
    var cv = document.createElement("canvas");
    cv.style.width = "100%";
    cv.style.display = "block";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d");

    var H = 312;
    var LABELS = ["1분기", "2분기", "3분기", "4분기"];
    var SALES = [100, 101, 102, 104];

    /* 오른쪽 분포용 표본 — 두 집단 혼합, 수업마다 같은 모양 */
    var rnd = mulberry32(20261103), SAMPLE = [], i, a, b, z;
    for (i = 0; i < 900; i++) {
      a = 1 - rnd(); b = rnd();
      z = Math.sqrt(-2 * Math.log(a)) * Math.cos(2 * Math.PI * b);
      SAMPLE.push((i % 2 ? 78 : 42) + z * 7.2);
    }

    var baseS = host.parentNode.querySelector("[data-base]");
    var binS = host.parentNode.querySelector("[data-bin]");
    var baseV = host.parentNode.querySelector("[data-base-v]");
    var binV = host.parentNode.querySelector("[data-bin-v]");
    var sortB = host.parentNode.querySelector("[data-sort]");
    var cubeB = host.parentNode.querySelector("[data-3d]");
    var out = host.parentNode.querySelector("[data-out]");

    var sorted = false, cube = false;

    function peaks(h) {
      var mx = Math.max.apply(null, h), n = 0;
      for (var k = 1; k < h.length - 1; k++) {
        if (h[k] > h[k - 1] && h[k] >= h[k + 1] && h[k] > mx * 0.32) n++;
      }
      if (h[0] > h[1] && h[0] > mx * 0.32) n++;
      return n;
    }

    function render() {
      var w = host.clientWidth || 900;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = w * dpr; cv.height = H * dpr;
      cv.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = C.bg; ctx.fillRect(0, 0, w, H);

      var base = +baseS.value, bins = +binS.value;
      baseV.textContent = base;
      binV.textContent = bins + "개";

      /* ── 왼쪽: 막대 ─────────────────────────────────── */
      var L = 44, R = Math.round(w * 0.52), TOP = 46, BOT = 252;
      var hi = base + (104 - base) * 1.22;
      if (hi - base < 2) hi = base + 2;
      function Y(v) { return BOT - (v - base) / (hi - base) * (BOT - TOP); }

      var idx = [0, 1, 2, 3];
      if (sorted) idx.sort(function (p, q) { return SALES[q] - SALES[p]; });

      ctx.strokeStyle = C.grid; ctx.lineWidth = 1;
      ctx.font = "11px 'JetBrains Mono', monospace";
      ctx.fillStyle = C.faint; ctx.textAlign = "right";
      for (var g = 0; g <= 4; g++) {
        var gv = base + (hi - base) * g / 4, gy = Y(gv);
        ctx.beginPath(); ctx.moveTo(L, gy + .5); ctx.lineTo(R, gy + .5); ctx.stroke();
        ctx.fillText(gv.toFixed(0), L - 8, gy + 4);
      }

      var bw = (R - L) / 4, dx = cube ? 9 : 0, dy = cube ? 11 : 0;
      ctx.textAlign = "center";
      for (i = 0; i < 4; i++) {
        var v = SALES[idx[i]];
        var x0 = L + i * bw + bw * 0.22, bwd = bw * 0.46;
        var y0 = Y(v), hgt = BOT - y0;
        var col = base > 0 ? C.trap : C.gfx;

        if (cube) {
          ctx.fillStyle = col + "55";
          ctx.beginPath();
          ctx.moveTo(x0, y0); ctx.lineTo(x0 + dx, y0 - dy);
          ctx.lineTo(x0 + bwd + dx, y0 - dy); ctx.lineTo(x0 + bwd, y0);
          ctx.closePath(); ctx.fill();
          ctx.fillStyle = col + "33";
          ctx.beginPath();
          ctx.moveTo(x0 + bwd, y0); ctx.lineTo(x0 + bwd + dx, y0 - dy);
          ctx.lineTo(x0 + bwd + dx, BOT - dy); ctx.lineTo(x0 + bwd, BOT);
          ctx.closePath(); ctx.fill();
        }
        ctx.fillStyle = col;
        ctx.fillRect(x0, y0, bwd, hgt);

        ctx.fillStyle = C.fg;
        ctx.font = "600 13px 'JetBrains Mono', monospace";
        ctx.fillText(String(v), x0 + bwd / 2 + dx / 2, y0 - dy - 8);
        ctx.fillStyle = C.dim;
        ctx.font = "12px Pretendard, sans-serif";
        ctx.fillText(LABELS[idx[i]], x0 + bwd / 2, BOT + 18);
      }

      ctx.strokeStyle = C.line; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(L, BOT + .5); ctx.lineTo(R, BOT + .5); ctx.stroke();

      ctx.fillStyle = C.dim;
      ctx.font = "600 13px Pretendard, sans-serif";
      ctx.textAlign = "left";
      ctx.fillText("분기 매출 (억원)", L, 26);
      if (sorted) {
        ctx.fillStyle = C.warn;
        ctx.font = "12px Pretendard, sans-serif";
        ctx.fillText("내림차순 정렬 — 시간 순서 소멸", L, BOT + 42);
      }

      /* ── 오른쪽: 분포 ───────────────────────────────── */
      var HL = R + 64, HR = w - 18;
      var LO = 10, HI = 110;
      var h = new Array(bins).fill(0), k;
      for (i = 0; i < SAMPLE.length; i++) {
        k = Math.floor((SAMPLE[i] - LO) / (HI - LO) * bins);
        if (k >= 0 && k < bins) h[k]++;
      }
      var mxh = Math.max.apply(null, h) || 1;
      var hw = (HR - HL) / bins;
      ctx.fillStyle = C.vr + "cc";
      for (i = 0; i < bins; i++) {
        var bh = h[i] / mxh * (BOT - TOP - 16);
        if (bh > 0) ctx.fillRect(HL + i * hw, BOT - bh, Math.max(hw - 1, 1), bh);
      }
      ctx.strokeStyle = C.line; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(HL, BOT + .5); ctx.lineTo(HR, BOT + .5); ctx.stroke();

      ctx.fillStyle = C.dim;
      ctx.font = "600 13px Pretendard, sans-serif";
      ctx.textAlign = "left";
      ctx.fillText("통학 시간 분포 (분)", HL, 26);
      ctx.font = "11px 'JetBrains Mono', monospace";
      ctx.fillStyle = C.faint;
      ctx.textAlign = "center";
      [20, 50, 80, 110].forEach(function (t) {
        ctx.fillText(String(t), HL + (t - LO) / (HI - LO) * (HR - HL), BOT + 18);
      });

      /* ── 읽기값 ─────────────────────────────────────── */
      var real = (104 - 100) / 100 * 100;
      var ratio = base >= 100 ? Infinity : (104 - base) / (100 - base);
      var np = peaks(h);
      var peakTxt = np >= 5 ? "다수" : np + "개";
      var ratioTxt = isFinite(ratio) ? "1 : " + ratio.toFixed(1) : "측정 불가";
      var impress = base === 0
        ? '<span class="lab-txt">보이는 대로 4% 증가</span>'
        : (ratio >= 3
            ? '<span class="trap-txt">' + ratio.toFixed(0) + "배 급증 인상</span>"
            : '<span style="color:' + C.warn + '">실제보다 큰 변화 인상</span>');

      out.innerHTML =
        "실제 증가 <b>" + real.toFixed(1) + "%</b>　" +
        "막대 길이 비 <b>" + ratioTxt + "</b>　→ " + impress +
        '<br><span class="muted">구간 ' + bins + "개 → 봉우리 " + peakTxt +
        "　·　같은 데이터, 조작 결과만 변경</span>";
    }

    baseS.addEventListener("input", render);
    binS.addEventListener("input", render);
    sortB.addEventListener("click", function () {
      sorted = !sorted;
      sortB.textContent = sorted ? "원래 순서" : "값 순 정렬";
      render();
    });
    cubeB.addEventListener("click", function () {
      cube = !cube;
      cubeB.textContent = cube ? "3D 끄기" : "3D 효과";
      render();
    });
    if (window.ResizeObserver) new ResizeObserver(render).observe(host);
    render();

    return { draw: function () {} };
  };
})();
