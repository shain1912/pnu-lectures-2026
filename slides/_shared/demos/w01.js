/* ============================================================
   1주차 데모 — 속는 눈 : 같은 픽셀 값, 다른 색
   Adelson 체커 그림자 착시(1995) 재구성 · 2D canvas (three.js 불필요)
   A 칸(빛 받는 어두운 칸)과 B 칸(그림자 속 밝은 칸)의 RGB 가 정확히 같음
   ============================================================ */
(function () {
  "use strict";
  window.CGDemos = window.CGDemos || {};

  var N = 7;                 /* 7 × 7 체커보드 */
  var LIGHT = 190, DARK = 118;
  var K = DARK / LIGHT;      /* 그림자 계수 → 밝은 칸 × K = 정확히 118 */
  var A = [1, 1];            /* 어두운 칸 · 빛 받는 곳   (i + j 짝수 = 어두운 칸) */
  var B = [4, 3];            /* 밝은 칸 · 그림자 핵심부 */
  var SH = { u: 4.6, v: 3.6, ru: 1.6, rv: 2.0, soft: 1.35 };   /* 그림자 타원 (보드 좌표) */
  var CYL = { u: 4.75, v: 1.85, r: 0.62, h: 2.3 };              /* 원기둥 바닥 중심 */

  function smooth(a, b, x) {
    var t = Math.max(0, Math.min(1, (x - a) / (b - a)));
    return t * t * (3 - 2 * t);
  }

  window.CGDemos["same-pixel"] = function (host) {
    var H = 360;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = host.clientWidth || 1100;

    var cv = document.createElement("canvas");
    cv.style.height = H + "px";
    cv.style.cursor = "crosshair";
    host.insertBefore(cv, host.firstChild);
    var g = cv.getContext("2d", { willReadFrequently: true });

    var off = document.createElement("canvas");   /* 보드 원본 (맥락 포함) */
    var og = off.getContext("2d", { willReadFrequently: true });

    var state = { mask: false, bridge: false, shadow: true, pick: null };
    var dirty = true;
    var geo = null;

    var out = host.parentNode.querySelector("[data-out]");
    var bMask = host.parentNode.querySelector("[data-mask]");
    var bBridge = host.parentNode.querySelector("[data-bridge]");
    var bShadow = host.parentNode.querySelector("[data-shadow]");
    var bReset = host.parentNode.querySelector("[data-reset]");

    /* ---- 보드 좌표 (u, v) ↔ 화면 좌표 (x, y), 단위 : 기기 픽셀 ---- */
    function layout() {
      W = host.clientWidth || W;
      cv.width = Math.round(W * dpr);
      cv.height = Math.round(H * dpr);
      off.width = cv.width; off.height = cv.height;
      var s = 42 * dpr;                      /* 칸 반폭 */
      geo = {
        s: s,
        cx: cv.width * 0.40,
        cy: 34 * dpr,
        toXY: function (u, v) {
          return [this.cx + (u - v) * s, this.cy + (u + v) * s * 0.5];
        },
        toUV: function (x, y) {
          var a = (x - this.cx) / s, b = (y - this.cy) / (s * 0.5);
          return [(a + b) / 2, (b - a) / 2];
        }
      };
    }

    function shadowFactor(u, v) {
      if (!state.shadow) return 1;
      var du = (u - SH.u) / SH.ru, dv = (v - SH.v) / SH.rv;
      var d = Math.sqrt(du * du + dv * dv);
      return K + (1 - K) * smooth(1, SH.soft, d);
    }

    function tileBase(i, j) { return ((i + j) % 2 === 0) ? DARK : LIGHT; }

    function tileCenter(t) { return geo.toXY(t[0] + 0.5, t[1] + 0.5); }

    function tilePath(ctx, t) {
      var p0 = geo.toXY(t[0], t[1]), p1 = geo.toXY(t[0] + 1, t[1]),
          p2 = geo.toXY(t[0] + 1, t[1] + 1), p3 = geo.toXY(t[0], t[1] + 1);
      ctx.beginPath();
      ctx.moveTo(p0[0], p0[1]); ctx.lineTo(p1[0], p1[1]);
      ctx.lineTo(p2[0], p2[1]); ctx.lineTo(p3[0], p3[1]); ctx.closePath();
    }

    /* ---- 원본 보드 그리기 : 픽셀 단위 계산 → 정확한 값 보장 ---- */
    function renderBoard() {
      var w = off.width, h = off.height;
      og.fillStyle = "#06070a";
      og.fillRect(0, 0, w, h);
      var img = og.getImageData(0, 0, w, h);
      var d = img.data;
      for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
          var uv = geo.toUV(x + 0.5, y + 0.5);
          var u = uv[0], v = uv[1];
          if (u < 0 || v < 0 || u >= N || v >= N) continue;
          var i = Math.floor(u), j = Math.floor(v);
          var val = Math.round(tileBase(i, j) * shadowFactor(u, v));
          var k = (y * w + x) * 4;
          d[k] = d[k + 1] = d[k + 2] = val; d[k + 3] = 255;
        }
      }
      og.putImageData(img, 0, 0);

      /* 보드 두께 (옆면) */
      var L = geo.toXY(0, N), Bt = geo.toXY(N, N), R = geo.toXY(N, 0);
      var th = 16 * dpr;
      og.fillStyle = "#3a3f4a";
      og.beginPath();
      og.moveTo(L[0], L[1]); og.lineTo(Bt[0], Bt[1]);
      og.lineTo(Bt[0], Bt[1] + th); og.lineTo(L[0], L[1] + th); og.closePath(); og.fill();
      og.fillStyle = "#4a505c";
      og.beginPath();
      og.moveTo(Bt[0], Bt[1]); og.lineTo(R[0], R[1]);
      og.lineTo(R[0], R[1] + th); og.lineTo(Bt[0], Bt[1] + th); og.closePath(); og.fill();

      /* 원기둥 */
      if (state.shadow) {
        var c = geo.toXY(CYL.u, CYL.v);
        var rx = CYL.r * geo.s * 1.42, ry = rx * 0.5, hh = CYL.h * geo.s;
        var grad = og.createLinearGradient(c[0] - rx, 0, c[0] + rx, 0);
        grad.addColorStop(0, "#3f8f3a");
        grad.addColorStop(0.55, "#7fd26b");
        grad.addColorStop(1, "#2e6a2a");
        og.fillStyle = grad;
        og.beginPath();
        og.ellipse(c[0], c[1], rx, ry, 0, 0, Math.PI);
        og.lineTo(c[0] - rx, c[1] - hh);
        og.ellipse(c[0], c[1] - hh, rx, ry, 0, Math.PI, 0, true);
        og.closePath(); og.fill();
        og.fillStyle = "#9be588";
        og.beginPath(); og.ellipse(c[0], c[1] - hh, rx, ry, 0, 0, Math.PI * 2); og.fill();
      }
    }

    function label(ctx, t, txt) {
      var c = tileCenter(t);
      ctx.font = "700 " + (17 * dpr) + "px Pretendard, 'Malgun Gothic', sans-serif";
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.lineWidth = 4 * dpr; ctx.strokeStyle = "rgba(6,7,10,0.85)";
      ctx.strokeText(txt, c[0], c[1]);
      ctx.fillStyle = "#ffc44d";
      ctx.fillText(txt, c[0], c[1]);
    }

    function paint() {
      g.drawImage(off, 0, 0);

      if (state.mask) {
        /* 맥락 가리기 : A · B 칸만 남기고 전부 중립 회색 */
        g.fillStyle = "rgb(60,64,72)";
        g.fillRect(0, 0, cv.width, cv.height);
        [A, B].forEach(function (t) {
          g.save(); tilePath(g, t); g.clip(); g.drawImage(off, 0, 0); g.restore();
        });
      }
      if (state.bridge) {
        /* 같은 값(118) 띠로 A 와 B 를 잇기 */
        var a = tileCenter(A), b = tileCenter(B);
        g.save();
        g.strokeStyle = "rgb(" + DARK + "," + DARK + "," + DARK + ")";
        g.lineWidth = geo.s * 0.42; g.lineCap = "butt";
        g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke();
        g.restore();
      }
      label(g, A, "A"); label(g, B, "B");

      /* 측정 지점 표시 */
      if (state.pick) {
        var p = state.pick;
        g.strokeStyle = "#ff5fa2"; g.lineWidth = 2 * dpr;
        g.beginPath(); g.arc(p.x, p.y, 7 * dpr, 0, Math.PI * 2); g.stroke();
        g.beginPath();
        g.moveTo(p.x - 12 * dpr, p.y); g.lineTo(p.x + 12 * dpr, p.y);
        g.moveTo(p.x, p.y - 12 * dpr); g.lineTo(p.x, p.y + 12 * dpr); g.stroke();
      }

      /* 오른쪽 판독 패널 */
      var px = cv.width * 0.74, py = 40 * dpr, fs = 17 * dpr;
      g.textAlign = "left"; g.textBaseline = "alphabetic";
      g.font = "600 " + fs + "px Pretendard, 'Malgun Gothic', sans-serif";
      g.fillStyle = "#9aa4b8";
      g.fillText("픽셀 값 판독", px, py);
      var va = sample(tileCenter(A)), vb = sample(tileCenter(B));
      row("A 칸", va, py + 40 * dpr);
      row("B 칸", vb, py + 80 * dpr);
      if (state.pick) row("클릭한 점", state.pick.rgb, py + 120 * dpr);
      g.font = "500 " + (15 * dpr) + "px Pretendard, 'Malgun Gothic', sans-serif";
      g.fillStyle = (va.join() === vb.join()) ? "#a8e05f" : "#ff5a4d";
      g.fillText(va.join() === vb.join() ? "A = B : 같은 숫자" : "A ≠ B : 숫자가 다름", px, py + 170 * dpr);
    }

    function row(name, rgb, y) {
      var px = cv.width * 0.74;
      g.fillStyle = "rgb(" + rgb.join(",") + ")";
      g.fillRect(px, y - 16 * dpr, 22 * dpr, 22 * dpr);
      g.strokeStyle = "#2a3040"; g.lineWidth = 1 * dpr;
      g.strokeRect(px, y - 16 * dpr, 22 * dpr, 22 * dpr);
      g.font = "500 " + (17 * dpr) + "px Pretendard, 'Malgun Gothic', sans-serif";
      g.fillStyle = "#e8ecf4";
      g.fillText(name + "  (" + rgb.join(", ") + ")", px + 32 * dpr, y);
    }

    /* 원본 보드에서 값 읽기 (라벨·띠와 무관한 실제 표면 값) */
    function sample(p) {
      var d = og.getImageData(Math.round(p[0]), Math.round(p[1]), 1, 1).data;
      return [d[0], d[1], d[2]];
    }

    function updateUI() {
      if (bMask) bMask.textContent = state.mask ? "맥락 되돌리기" : "맥락 가리기";
      if (bBridge) bBridge.textContent = state.bridge ? "연결 띠 치우기" : "A–B 연결 띠";
      if (bShadow) bShadow.textContent = state.shadow ? "그림자 원기둥 치우기" : "그림자 원기둥 놓기";
      [[bMask, state.mask], [bBridge, state.bridge], [bShadow, !state.shadow]].forEach(function (p) {
        if (!p[0]) return;
        p[0].style.borderColor = p[1] ? "#ff5fa2" : "";
        p[0].style.color = p[1] ? "#ff5fa2" : "";
      });
      if (!out) return;
      var msg;
      if (!state.shadow) msg = "그림자 제거 → B 의 실제 값이 190 으로 상승 · 그림자가 B 의 숫자를 118 까지 낮췄던 것";
      else if (state.mask) msg = "주변 맥락 제거 → A · B 가 같은 회색으로 보임 · 차이를 만든 것은 픽셀이 아니라 맥락";
      else if (state.bridge) msg = "같은 값(118)의 띠로 연결 → 이음매가 보이지 않음 = 세 곳 모두 같은 색";
      else msg = "질문 : A 와 B 중 어느 칸이 더 어두운가? → 화면을 클릭해 실제 RGB 를 측정";
      out.textContent = msg;
    }

    cv.addEventListener("click", function (e) {
      var r = cv.getBoundingClientRect();
      var x = (e.clientX - r.left) * (cv.width / r.width);
      var y = (e.clientY - r.top) * (cv.height / r.height);
      paint();                                   /* 측정은 지금 보이는 화면 기준 */
      var d = g.getImageData(Math.round(x), Math.round(y), 1, 1).data;
      state.pick = { x: x, y: y, rgb: [d[0], d[1], d[2]] };
      dirty = true;
    });
    if (bMask) bMask.addEventListener("click", function () { state.mask = !state.mask; dirty = true; updateUI(); });
    if (bBridge) bBridge.addEventListener("click", function () { state.bridge = !state.bridge; dirty = true; updateUI(); });
    if (bShadow) bShadow.addEventListener("click", function () {
      state.shadow = !state.shadow; state.pick = null; renderBoard(); dirty = true; updateUI();
    });
    if (bReset) bReset.addEventListener("click", function () {
      state.mask = false; state.bridge = false; state.pick = null;
      if (!state.shadow) { state.shadow = true; renderBoard(); }
      dirty = true; updateUI();
    });

    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        var nw = host.clientWidth;
        if (!nw || Math.abs(nw - W) < 1) return;
        layout(); renderBoard(); state.pick = null; dirty = true;
      }).observe(host);
    }

    layout(); renderBoard(); updateUI();

    return {
      draw: function () {
        if (!dirty) return;
        dirty = false;
        paint();
      }
    };
  };
})();
