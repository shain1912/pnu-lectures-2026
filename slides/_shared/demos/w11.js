/* ============================================================
   11주차 데모
   A. tracking-drift : 트래킹 드리프트 · 예측 시뮬레이터 (2D canvas)
      - 왼쪽  : 자이로 적분만 vs 상보 필터 융합 → 시간에 따른 오차
      - 오른쪽 : 시스템 지연 20 ms · 예측 시간 P → 지연 오차와 오버슈트
      - 맨 오른쪽 : 위에서 본 머리 (실제 방향 vs 화면 방향)
   B. xr-rig : XR Origin 리그 계층 · 카메라 직접 이동(함정) vs 리그 이동
   _stage.js 를 먼저 로드할 것 (B 는 three.js r128 필요)
   ============================================================ */
(function () {
  "use strict";
  var S = window.CGStage;
  window.CGDemos = window.CGDemos || {};

  var COL = {
    gfx: "#35d6e6", vr: "#ff5fa2", trap: "#ff5a4d", lab: "#a8e05f",
    warn: "#ffc44d", fg: "#e8ecf4", dim: "#9aa4b8", faint: "#5f6980",
    line: "#2a3040", grid: "#1b2130", bg: "#06070a"
  };
  var FONT = '"Pretendard Variable", Pretendard, "Malgun Gothic", sans-serif';

  /* 고정 시드 난수 — 슬라이더를 움직여도 잡음 모양이 같게 */
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function gauss(r) {
    var u = Math.max(1e-9, r()), v = r();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }
  function q(host, sel) { return host.parentNode.querySelector(sel); }

  /* ============================================================
     A. 트래킹 드리프트 · 예측 시뮬레이터
     ============================================================ */
  var ALPHA_STEPS = [0, 0.0005, 0.002, 0.01, 0.05, 0.2];   /* 1 − α (50 Hz 기준) */
  var LAT = 0.020;                                          /* 시스템 지연 20 ms */

  /* 머리 회전 프로파일 (3 s 반복) : 정지 → 빠른 회전 → 갑작스러운 정지 */
  var PRED = (function () {
    var fs = 1000, T = 3.0, n = Math.round(T * fs);
    var Vp = 200, up = 0.08, down = 0.03;                  /* °/s · 가속 · 감속 구간 */
    var Tc = 60 / Vp - up / 2 - down / 2;                  /* 등속 구간 → 총 60° */
    function vel(t) {
      function seg(t0, sign) {
        var u = t - t0;
        if (u < 0) return 0;
        if (u < up) return sign * Vp * u / up;
        if (u < up + Tc) return sign * Vp;
        if (u < up + Tc + down) return sign * Vp * (1 - (u - up - Tc) / down);
        return 0;
      }
      return seg(0.4, 1) + seg(1.6, -1);
    }
    var w = new Float32Array(n), a = new Float32Array(n);
    var th = -30;
    for (var i = 0; i < n; i++) {
      w[i] = vel(i / fs);
      a[i] = th;
      th += w[i] / fs;
    }
    return { fs: fs, T: T, n: n, w: w, a: a,
             stop1: 0.4 + up + Tc + down, stop2: 1.6 + up + Tc + down };
  })();

  window.CGDemos["tracking-drift"] = function (host) {
    var H = 318;
    var cv = document.createElement("canvas");
    host.insertBefore(cv, host.firstChild);
    var g = cv.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = 0;

    function size() {
      var nw = host.clientWidth || 1100;
      if (nw === W) return;
      W = nw;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      cv.style.height = H + "px";
      dirty = true;
    }

    var noiseS = q(host, "[data-noise]"), noiseV = q(host, "[data-noise-v]");
    var biasS = q(host, "[data-bias]"), biasV = q(host, "[data-bias-v]");
    var timeS = q(host, "[data-time]"), timeV = q(host, "[data-time-v]");
    var alphaS = q(host, "[data-alpha]"), alphaV = q(host, "[data-alpha-v]");
    var predS = q(host, "[data-pred]"), predV = q(host, "[data-pred-v]");
    var out = q(host, "[data-out]");

    var dirty = true, drift = null, pred = null;
    [noiseS, biasS, timeS, alphaS, predS].forEach(function (s) {
      if (s) s.addEventListener("input", function () { dirty = true; });
    });

    /* ---------- 드리프트 계산 (50 Hz) ---------- */
    function simDrift(sigG, bias, T, k) {
      var fs = 50, dt = 1 / fs, n = Math.round(T * fs);
      var r = rng(11);
      var sigRef = 3.0;          /* 가속도계·카메라 기준값의 잡음 (°) */
      var gy = 0, fu = 0;
      var eg = new Float32Array(n), ef = new Float32Array(n);
      for (var i = 0; i < n; i++) {
        var t = i * dt;
        /* 머리가 계속 움직임 — 한 스텝 동안의 정확한 회전량을 써서
           적분 방식 자체의 오차가 그래프에 섞이지 않게 한다 */
        var trueA = 40 * Math.sin((t + dt) * 0.9);
        var trueW = (trueA - 40 * Math.sin(t * 0.9)) / dt;
        var wm = trueW + bias + sigG * gauss(r);
        var ref = trueA + sigRef * gauss(r);
        gy += wm * dt;
        fu = (1 - k) * (fu + wm * dt) + k * ref;
        eg[i] = gy - trueA;
        ef[i] = fu - trueA;
      }
      return { eg: eg, ef: ef, n: n, T: T };
    }

    /* ---------- 예측 계산 (1000 Hz) ---------- */
    function simPred(P, sigG) {
      var n = PRED.n, fs = PRED.fs, L = Math.round(LAT * fs);
      var r = rng(5);
      var shown = new Float32Array(n);
      var lagMax = 0, overMax = 0;
      for (var i = 0; i < n; i++) {
        var j = (i - L + n) % n;
        var wm = PRED.w[j] + sigG * 4 * gauss(r);     /* 고주파 잡음 — 예측이 증폭 */
        shown[i] = PRED.a[j] + P * wm;
        var e = shown[i] - PRED.a[i];
        var t = i / fs;
        var moving = Math.abs(PRED.w[i]) > 150;
        if (moving) lagMax = Math.max(lagMax, Math.abs(e));
        var after1 = t > PRED.stop1 && t < PRED.stop1 + 0.15;
        var after2 = t > PRED.stop2 && t < PRED.stop2 + 0.15;
        if (after1) overMax = Math.max(overMax, e);
        if (after2) overMax = Math.max(overMax, -e);
      }
      return { shown: shown, lag: lagMax, over: Math.max(0, overMax) };
    }

    var cache = document.createElement("canvas");
    var cg = cache.getContext("2d");

    function recompute() {
      var sigG = +noiseS.value, bias = +biasS.value, T = +timeS.value;
      var k = ALPHA_STEPS[+alphaS.value] || 0;
      var P = +predS.value / 1000;
      noiseV.textContent = sigG.toFixed(1) + " °/s";
      biasV.textContent = bias.toFixed(3) + " °/s";
      timeV.textContent = T >= 60 ? (T / 60).toFixed(T % 60 ? 1 : 0) + " 분" : T + " s";
      alphaV.textContent = k === 0 ? "보정 없음" : "α = " + (1 - k).toFixed(4);
      predV.textContent = Math.round(P * 1000) + " ms";
      drift = simDrift(sigG, bias, T, k);
      pred = simPred(P, sigG);
      drift.k = k; drift.bias = bias; pred.P = P;
      paintStatic();
      var gEnd = drift.eg[drift.n - 1], fEnd = drift.ef[drift.n - 1];
      var predTxt = P * 1000 < 15 ? "← 예측 부족 : 화면이 머리를 늦게 따라옴"
        : P * 1000 <= 25 ? "← 지연과 비슷한 예측 : 이동 중 오차 최소"
        : "← 과예측 : 이동 중 앞서가고 정지 순간 튕김";
      out.innerHTML =
        '<b class="trap-txt">자이로만</b> ' + timeV.textContent + " 후 " + gEnd.toFixed(1) + "°" +
        (k ? '　<b class="lab-txt">융합</b> ' + fEnd.toFixed(1) + "°" : "") +
        '　│　<b class="vr-txt">이동 중 오차</b> 최대 ' + pred.lag.toFixed(1) + "°" +
        '　<b style="color:#a8701a">정지 직후 오버슈트</b> ' + pred.over.toFixed(1) + "°" +
        '　<span class="muted">' + predTxt + "</span>";
    }

    /* ---------- 고정 그림 (그래프 2개) ---------- */
    function panel(x, y, w, h, title, sub) {
      cg.fillStyle = COL.fg; cg.font = "600 16px " + FONT;
      cg.textBaseline = "alphabetic"; cg.textAlign = "left";
      cg.fillText(title, x, y - 10);
      if (sub) {
        cg.fillStyle = COL.dim; cg.font = "14px " + FONT;
        cg.fillText(sub, x + cg.measureText(title).width * 1.15 + 14, y - 10);
      }
      cg.strokeStyle = COL.line; cg.lineWidth = 1;
      cg.strokeRect(x + 0.5, y + 0.5, w, h);
    }

    function paintStatic() {
      cache.width = cv.width; cache.height = cv.height;
      cg.setTransform(dpr, 0, 0, dpr, 0, 0);
      cg.fillStyle = COL.bg; cg.fillRect(0, 0, W, H);

      /* ---- 왼쪽 : 드리프트 ---- */
      var lx = 54, ly = 34, lw = W * 0.44 - 54, lh = H - 74;
      panel(lx, ly, lw, lh, "① 추정 오차 (추정 − 실제)", "적분 시간 " + timeV.textContent);
      var m = 1;
      for (var i = 0; i < drift.n; i++) m = Math.max(m, Math.abs(drift.eg[i]));
      var ys = [2, 4, 8, 16, 32, 64, 128]; var ymax = 64;
      for (var s = 0; s < ys.length; s++) if (m <= ys[s] * 0.95) { ymax = ys[s]; break; }
      function Y(v) { return ly + lh / 2 - v / ymax * (lh / 2 - 6); }
      cg.font = "13px " + FONT; cg.fillStyle = COL.dim; cg.textAlign = "right";
      [-ymax, -ymax / 2, 0, ymax / 2, ymax].forEach(function (v) {
        cg.strokeStyle = v === 0 ? "#3a4356" : COL.grid;
        cg.beginPath(); cg.moveTo(lx, Y(v)); cg.lineTo(lx + lw, Y(v)); cg.stroke();
        cg.fillText((v > 0 ? "+" : "") + v + "°", lx - 6, Y(v) + 4);
      });
      cg.textAlign = "center";
      for (var tk = 0; tk <= 4; tk++) {
        var tt = drift.T * tk / 4;
        cg.fillText(tt >= 60 ? (tt / 60).toFixed(tt % 60 ? 1 : 0) + "분" : Math.round(tt) + "s",
                    lx + lw * tk / 4, ly + lh + 17);
      }
      function trace(arr, color, wdt) {
        cg.strokeStyle = color; cg.lineWidth = wdt;
        cg.beginPath();
        var cols = Math.floor(lw);
        for (var c = 0; c <= cols; c++) {
          var i0 = Math.floor(c / cols * (drift.n - 1));
          var i1 = Math.max(i0 + 1, Math.floor((c + 1) / cols * (drift.n - 1)));
          var lo = Infinity, hi = -Infinity;
          for (var k2 = i0; k2 < Math.min(i1, drift.n); k2++) {
            lo = Math.min(lo, arr[k2]); hi = Math.max(hi, arr[k2]);
          }
          if (lo === Infinity) { lo = hi = arr[drift.n - 1]; }
          var px = lx + c;
          if (c === 0) cg.moveTo(px, Y(lo)); else cg.lineTo(px, Y(lo));
          if (hi - lo > 0.01) cg.lineTo(px, Y(hi));
        }
        cg.stroke();
      }
      /* 실제 = 0 선 */
      cg.strokeStyle = COL.gfx; cg.lineWidth = 2;
      cg.beginPath(); cg.moveTo(lx, Y(0)); cg.lineTo(lx + lw, Y(0)); cg.stroke();
      if (drift.k) trace(drift.ef, COL.lab, 1.4);
      trace(drift.eg, COL.trap, 2);
      /* 바이어스만의 기대값 (점선) */
      if (drift.bias > 0) {
        cg.setLineDash([5, 5]); cg.strokeStyle = "rgba(255,196,77,.7)"; cg.lineWidth = 1.2;
        cg.beginPath(); cg.moveTo(lx, Y(0)); cg.lineTo(lx + lw, Y(drift.bias * drift.T)); cg.stroke();
        cg.setLineDash([]);
      }
      cg.textAlign = "left"; cg.font = "13px " + FONT;
      var lgx = lx + 8, lgy = ly + 18;
      [[COL.gfx, "실제 (오차 0)"], [COL.trap, "자이로 적분만"],
       [COL.lab, drift.k ? "상보 필터 융합" : "융합 꺼짐"], [COL.warn, "바이어스 × 시간"]]
        .forEach(function (it) {
          cg.fillStyle = it[0]; cg.fillRect(lgx, lgy - 9, 12, 4);
          cg.fillStyle = COL.dim; cg.fillText(it[1], lgx + 16, lgy - 4);
          lgx += 16 + cg.measureText(it[1]).width + 16;
        });

      /* ---- 오른쪽 : 예측 ---- */
      var rx = W * 0.5, ry = 34, rw = W * 0.34, rh = 160;
      panel(rx, ry, rw, rh, "② 머리 방향", "지연 20 ms · 예측 " + Math.round(pred.P * 1000) + " ms");
      var AMAX = 40;
      function RY(v) { return ry + rh / 2 - v / AMAX * (rh / 2 - 6); }
      function RX(t) { return rx + t / PRED.T * rw; }
      cg.font = "13px " + FONT; cg.fillStyle = COL.dim; cg.textAlign = "right";
      [-30, 0, 30].forEach(function (v) {
        cg.strokeStyle = COL.grid;
        cg.beginPath(); cg.moveTo(rx, RY(v)); cg.lineTo(rx + rw, RY(v)); cg.stroke();
        cg.fillText((v > 0 ? "+" : "") + v + "°", rx - 6, RY(v) + 4);
      });
      function curve(arr, color, wd, y0, scale) {
        cg.strokeStyle = color; cg.lineWidth = wd; cg.beginPath();
        for (var i2 = 0; i2 < PRED.n; i2 += 2) {
          var px2 = RX(i2 / PRED.fs), py2 = y0(arr[i2]);
          if (i2 === 0) cg.moveTo(px2, py2); else cg.lineTo(px2, py2);
        }
        cg.stroke();
      }
      curve(PRED.a, COL.gfx, 2.2, RY);
      curve(pred.shown, COL.vr, 1.6, RY);

      /* 오차 그래프 */
      var ey = ry + rh + 34, eh = H - ey - 26;
      panel(rx, ey, rw, eh, "③ 화면 − 실제", "");
      var EM = 6;
      function EY(v) { return ey + eh / 2 - Math.max(-EM, Math.min(EM, v)) / EM * (eh / 2 - 4); }
      cg.font = "13px " + FONT; cg.fillStyle = COL.dim; cg.textAlign = "right";
      [-EM, 0, EM].forEach(function (v) {
        cg.strokeStyle = v === 0 ? "#3a4356" : COL.grid;
        cg.beginPath(); cg.moveTo(rx, EY(v)); cg.lineTo(rx + rw, EY(v)); cg.stroke();
        cg.fillText((v > 0 ? "+" : "") + v + "°", rx - 6, EY(v) + 4);
      });
      var err = new Float32Array(PRED.n);
      for (var i3 = 0; i3 < PRED.n; i3++) err[i3] = pred.shown[i3] - PRED.a[i3];
      curve(err, COL.trap, 1.6, EY);
      cg.textAlign = "center"; cg.fillStyle = COL.dim;
      [0, 1, 2, 3].forEach(function (t) { cg.fillText(t + "s", RX(t), ey + eh + 16); });
      /* 정지 순간 표시 */
      [PRED.stop1, PRED.stop2].forEach(function (t) {
        cg.strokeStyle = "rgba(255,196,77,.55)"; cg.setLineDash([3, 4]);
        cg.beginPath(); cg.moveTo(RX(t), ry); cg.lineTo(RX(t), ey + eh); cg.stroke();
        cg.setLineDash([]);
      });
      cg.fillStyle = COL.warn; cg.textAlign = "left"; cg.font = "13px " + FONT;
      cg.fillText("멈춤", RX(PRED.stop1) + 4, ry + 16);

      cg.textAlign = "left";
      [[COL.gfx, "실제 머리"], [COL.vr, "화면에 그린 방향"]].forEach(function (it, idx) {
        cg.fillStyle = it[0]; cg.fillRect(rx + rw - 230 + idx * 112, ry + rh - 14, 12, 4);
        cg.fillStyle = COL.dim; cg.fillText(it[1], rx + rw - 214 + idx * 112, ry + rh - 9);
      });
    }

    /* ---------- 매 프레임 : 재생 위치 + 머리 다이얼 ---------- */
    var t0 = performance.now();
    function draw() {
      size();
      if (dirty) { recompute(); dirty = false; }
      g.setTransform(1, 0, 0, 1, 0, 0);
      g.drawImage(cache, 0, 0);
      g.setTransform(dpr, 0, 0, dpr, 0, 0);

      var t = ((performance.now() - t0) / 1000 * 0.5) % PRED.T;    /* 0.5배 느리게 */
      var i = Math.min(PRED.n - 1, Math.floor(t * PRED.fs));
      var rx = W * 0.5, rw = W * 0.34;
      var px = rx + t / PRED.T * rw;
      g.strokeStyle = "rgba(232,236,244,.45)"; g.lineWidth = 1;
      g.beginPath(); g.moveTo(px, 34); g.lineTo(px, H - 26); g.stroke();

      /* 위에서 본 머리 */
      var cx = W * 0.92, cy = H * 0.5, R = Math.min(W * 0.065, 74);
      var aT = PRED.a[i] * Math.PI / 180, aS = pred.shown[i] * Math.PI / 180;
      g.fillStyle = COL.fg; g.font = "600 15px " + FONT; g.textAlign = "center";
      g.fillText("위에서 본 머리", cx, 24);
      g.strokeStyle = COL.line; g.lineWidth = 2;
      g.beginPath(); g.arc(cx, cy, R + 14, 0, Math.PI * 2); g.stroke();
      /* 오차 부채꼴 */
      var a0 = Math.min(aT, aS), a1 = Math.max(aT, aS);
      g.fillStyle = "rgba(255,90,77,.45)";
      g.beginPath(); g.moveTo(cx, cy);
      g.arc(cx, cy, R + 10, -Math.PI / 2 + a0, -Math.PI / 2 + a1); g.closePath(); g.fill();
      function ndl(a, color, len, wdt) {
        g.strokeStyle = color; g.lineWidth = wdt; g.lineCap = "round";
        g.beginPath(); g.moveTo(cx, cy);
        g.lineTo(cx + Math.sin(a) * len, cy - Math.cos(a) * len); g.stroke();
      }
      ndl(aS, COL.vr, R + 6, 6);
      ndl(aT, COL.gfx, R + 12, 3);
      g.fillStyle = "#d8dde8";
      g.beginPath(); g.arc(cx, cy, R * 0.42, 0, Math.PI * 2); g.fill();
      var errDeg = Math.abs(pred.shown[i] - PRED.a[i]);
      g.font = "14px " + FONT;
      g.fillStyle = errDeg > 2 ? COL.trap : COL.lab;
      g.fillText("어긋남 " + errDeg.toFixed(1) + "°", cx, H - 30);
      g.fillStyle = COL.dim; g.font = "12px " + FONT;
      g.fillText("0.5배 느린 재생", cx, H - 12);
    }

    size();
    return { draw: draw };
  };

  /* ============================================================
     B. XR 리그 계층 — 카메라 직접 이동(함정) vs 리그 이동
     ============================================================ */
  function textSprite(text, color) {
    var cv = document.createElement("canvas");
    cv.width = 512; cv.height = 96;
    var g = cv.getContext("2d");
    var tex = new THREE.CanvasTexture(cv);
    function paint(s) {
      g.clearRect(0, 0, 512, 96);
      g.font = "bold 40px " + FONT;
      var w = Math.min(500, g.measureText(s).width + 36);
      g.fillStyle = "rgba(11,13,18,0.88)";
      g.strokeStyle = color; g.lineWidth = 4;
      g.beginPath(); g.rect((512 - w) / 2, 14, w, 66); g.fill(); g.stroke();
      g.fillStyle = color; g.textAlign = "center"; g.textBaseline = "middle";
      g.fillText(s, 256, 48);
      tex.needsUpdate = true;
    }
    paint(text);
    var sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false }));
    sp.scale.set(1.9, 0.36, 1);
    sp.renderOrder = 30;
    sp.userData.paint = paint;
    return sp;
  }

  function headModel(color, wire) {
    var grp = new THREE.Group();
    var mat = wire
      ? new THREE.MeshBasicMaterial({ color: color, wireframe: true, transparent: true, opacity: 0.55 })
      : new THREE.MeshLambertMaterial({ color: color });
    grp.add(new THREE.Mesh(new THREE.SphereGeometry(0.14, 20, 14), mat));
    var visor = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.09, 0.08),
      wire ? mat : new THREE.MeshLambertMaterial({ color: 0x35d6e6 }));
    visor.position.set(0, 0.01, -0.13);
    grp.add(visor);
    /* 시야 방향 표시 — 짧은 절두체 선 */
    var f = 0.55, s = 0.26;
    var pts = [0, 0, 0, -s, s * 0.6, -f, 0, 0, 0, s, s * 0.6, -f, 0, 0, 0, -s, -s * 0.6, -f,
               0, 0, 0, s, -s * 0.6, -f,
               -s, s * 0.6, -f, s, s * 0.6, -f, s, s * 0.6, -f, s, -s * 0.6, -f,
               s, -s * 0.6, -f, -s, -s * 0.6, -f, -s, -s * 0.6, -f, -s, s * 0.6, -f];
    var geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.Float32BufferAttribute(pts, 3));
    var fr = new THREE.LineSegments(geo, new THREE.LineBasicMaterial({
      color: color, transparent: true, opacity: wire ? 0.5 : 0.8 }));
    fr.position.z = -0.12;
    grp.add(fr);
    return grp;
  }

  window.CGDemos["xr-rig"] = function (host) {
    var st = S.make(host, {
      dist: 5.4, phi: 1.18, theta: 0.85, height: 330, fov: 40, ty: 0.8,
      gridSize: 12, gridDiv: 12
    });
    if (!st) return null;
    var C = st.C;

    /* 계층 : rig(XR Origin) → offset(Camera Offset) → cam(Main Camera) */
    var rig = new THREE.Group(), offset = new THREE.Group(), cam = new THREE.Group();
    rig.add(offset); offset.add(cam);
    st.scene.add(rig);
    cam.add(headModel(0xe8ecf4, false));

    /* 리그 바닥 표시 : 플레이 구역 2 m × 2 m + 원점 */
    var area = new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.PlaneGeometry(2, 2)),
      new THREE.LineBasicMaterial({ color: C.lab }));
    area.rotation.x = -Math.PI / 2; area.position.y = 0.01;
    rig.add(area);
    var originMark = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.03, 24),
      new THREE.MeshBasicMaterial({ color: C.lab }));
    rig.add(originMark);
    var fwd = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.22, 12),
      new THREE.MeshBasicMaterial({ color: C.lab }));
    fwd.rotation.x = -Math.PI / 2; fwd.position.set(0, 0.03, -1.15);
    rig.add(fwd);
    var offMark = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.12),
      new THREE.MeshBasicMaterial({ color: C.warn }));
    offset.add(offMark);

    /* 실제 머리 (트래킹 끔 상태에서만 보임) · 함정 위치 표시 */
    var realHead = headModel(0xff5fa2, true);
    realHead.visible = false;
    offset.add(realHead);
    var ghost = headModel(0xff5a4d, true);
    ghost.visible = false;
    st.scene.add(ghost);

    /* 연결선 */
    var linkGeo = new THREE.BufferGeometry();
    linkGeo.setAttribute("position", new THREE.Float32BufferAttribute(new Array(12).fill(0), 3));
    var link = new THREE.LineSegments(linkGeo, new THREE.LineDashedMaterial({
      color: 0x9aa4b8, dashSize: 0.08, gapSize: 0.06 }));
    st.scene.add(link);

    var lbRig = textSprite("XR Origin", "#a8e05f");
    var lbOff = textSprite("Camera Offset", "#ffc44d");
    var lbCam = textSprite("Main Camera", "#e8ecf4");
    st.scene.add(lbRig, lbOff, lbCam);

    var out = q(host, "[data-out]");
    var alertEl = host.querySelector(".demo-alert");
    var modeBtn = q(host, "[data-mode]");
    var tpdBtn = q(host, "[data-tpd]");

    var state = { floor: true, tpd: true, overwrites: 0, ghostT: 0, alertT: 0, alertMsg: "" };
    var t = 0;

    function tracked(time) {
      /* 헤드셋이 보고하는 머리 자세 (플레이 구역 기준 로컬 값) */
      var y = state.floor ? 1.6 : 0.0;
      return {
        x: 0.32 * Math.sin(time * 0.55),
        y: y + 0.03 * Math.sin(time * 1.9),
        z: 0.22 * Math.sin(time * 0.37 + 1),
        yaw: 0.6 * Math.sin(time * 0.8)
      };
    }
    function flash(msg) { state.alertMsg = msg; state.alertT = 2.6; }

    function setMode() {
      offset.position.y = state.floor ? 0 : 1.1176;
      if (modeBtn) modeBtn.textContent = state.floor ? "원점 모드 : Floor" : "원점 모드 : Device";
    }
    setMode();

    var tmpV = new THREE.Vector3(), tmpQ = new THREE.Quaternion();

    function on(sel, fn) { var b = q(host, sel); if (b) b.addEventListener("click", fn); }

    /* 정답 : 리그 루트를 이동 */
    on("[data-rig-move]", function () {
      var dir = new THREE.Vector3(0, 0, -1).applyQuaternion(cam.getWorldQuaternion(tmpQ));
      dir.y = 0; dir.normalize();
      rig.position.addScaledVector(dir, 1.0);
      flash("리그 이동 → 머리 트래킹은 그대로 · 1 m 이동");
    });
    on("[data-rig-turn]", function () {
      /* 카메라 위치를 축으로 리그를 45° 회전 (XROrigin.RotateAroundCameraUsingOriginUp 와 같은 일) */
      var pivot = cam.getWorldPosition(new THREE.Vector3());
      var qy = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), -Math.PI / 4);
      rig.position.sub(pivot).applyQuaternion(qy).add(pivot);
      rig.quaternion.premultiply(qy);
      flash("스냅 턴 45° → 머리 위치를 축으로 리그 회전");
    });
    /* 함정 : 카메라 Transform 직접 이동 */
    on("[data-cam-move]", function () {
      var wp = cam.getWorldPosition(new THREE.Vector3());
      var dir = new THREE.Vector3(0, 0, -1).applyQuaternion(cam.getWorldQuaternion(tmpQ));
      dir.y = 0; dir.normalize();
      wp.addScaledVector(dir, 1.0);
      ghost.position.copy(wp);
      ghost.quaternion.copy(cam.getWorldQuaternion(tmpQ));
      if (state.tpd) {
        ghost.visible = true; state.ghostT = 1.2;
        state.overwrites++;
        flash("카메라에 쓴 값 → 같은 프레임 안에 트래킹이 덮어씀 (" + state.overwrites + "회)");
      } else {
        cam.position.copy(offset.worldToLocal(wp.clone()));
        flash("트래킹 꺼짐 상태 → 카메라는 움직였지만 머리 회전이 화면에 반영 안 됨");
      }
    });
    on("[data-tpd]", function () {
      state.tpd = !state.tpd;
      realHead.visible = !state.tpd;
      if (tpdBtn) tpdBtn.textContent = state.tpd ? "Tracked Pose Driver 켬" : "Tracked Pose Driver 끔 (AI 2차 수정)";
      if (tpdBtn) tpdBtn.style.color = state.tpd ? "" : "#c2401d";
      if (tpdBtn) tpdBtn.style.borderColor = state.tpd ? "" : "#c2401d";
      flash(state.tpd ? "트래킹 복구" : "트래킹 끔 → 머리를 돌려도 화면 고정 = 감각 충돌");
    });
    on("[data-mode]", function () { state.floor = !state.floor; setMode(); });
    on("[data-reset]", function () {
      rig.position.set(0, 0, 0); rig.quaternion.identity();
      state.tpd = true; realHead.visible = false; state.overwrites = 0;
      if (tpdBtn) { tpdBtn.textContent = "Tracked Pose Driver 켬"; tpdBtn.style.color = ""; tpdBtn.style.borderColor = ""; }
      ghost.visible = false;
    });

    function f2(v) { return (v >= 0 ? "+" : "") + v.toFixed(2); }

    var baseDraw = st.draw;
    st.draw = function () {
      var dt = st.tick();
      t += dt;
      var p = tracked(t);
      if (state.tpd) {
        cam.position.set(p.x, p.y, p.z);
        cam.rotation.set(0, p.yaw, 0);
      } else {
        realHead.position.set(p.x, p.y, p.z);
        realHead.rotation.set(0, p.yaw, 0);
      }

      if (state.ghostT > 0) {
        state.ghostT -= dt;
        ghost.visible = state.ghostT > 0;
        ghost.traverse(function (o) {
          if (o.material) o.material.opacity = Math.max(0, state.ghostT / 1.2) * 0.6;
        });
      }

      /* 연결선 · 라벨 */
      var a = rig.getWorldPosition(new THREE.Vector3());
      var b = offset.getWorldPosition(new THREE.Vector3());
      var c = cam.getWorldPosition(new THREE.Vector3());
      var arr = linkGeo.attributes.position.array;
      arr.set([a.x, a.y, a.z, b.x, b.y, b.z, b.x, b.y, b.z, c.x, c.y, c.z]);
      linkGeo.attributes.position.needsUpdate = true;
      link.computeLineDistances();
      lbRig.position.set(a.x, a.y + 0.28, a.z + 0.9);
      lbOff.position.set(b.x + 0.9, b.y + 0.05, b.z);
      lbCam.position.set(c.x, c.y + 0.45, c.z);

      if (state.alertT > 0) {
        state.alertT -= dt;
        if (alertEl) { alertEl.textContent = state.alertMsg; alertEl.classList.add("on"); }
      } else if (alertEl) alertEl.classList.remove("on");

      var lp = cam.position;
      var mismatch = state.tpd ? 0 : Math.abs(p.yaw - cam.rotation.y) * 180 / Math.PI;
      out.innerHTML =
        '<b style="color:#1b1a17">Main Camera</b> 로컬 (' + f2(lp.x) + ", " + f2(lp.y) + ", " + f2(lp.z) + ")" +
        '　월드 (' + f2(c.x) + ", " + f2(c.y) + ", " + f2(c.z) + ")" +
        '　<b style="color:#a8701a">눈높이</b> ' + c.y.toFixed(2) + " m" +
        (state.floor ? "" : ' <span class="trap-txt">(실제 1.60 m 와 다름)</span>') +
        (state.tpd ? "" : '　<b class="trap-txt">머리 회전 − 화면 회전 = ' + mismatch.toFixed(0) + "°</b>");

      baseDraw();
    };
    return st;
  };
})();
