/* ============================================================
   7주차 데모 — 벡션·적분 실험실 (2D canvas · three.js 불필요)
     vection    : 광학 흐름 속도 · 시야각 마스크 · 정속 vs 가속 · 요 회전
     integrator : 오일러 / 세미암시적 오일러 / 베를레 궤도 비교
     tunneling  : 고정 타임스텝의 터널링 · 이산 vs 연속 충돌 판정
   컨트롤은 host 의 형제 .demo-ui 안에 둔다 (w05 와 같은 규칙)
   ============================================================ */
(function () {
  "use strict";
  window.CGDemos = window.CGDemos || {};

  var COL = {
    bg: "#06070a", fg: "#e8ecf4", dim: "#9aa4b8", faint: "#5f6980", line: "#2a3040",
    gfx: "#35d6e6", vr: "#ff5fa2", trap: "#ff5a4d", lab: "#a8e05f", warn: "#ffc44d"
  };
  var FONT = '"Pretendard Variable", Pretendard, "Malgun Gothic", sans-serif';

  function q(host, sel) { return host.parentNode.querySelector(sel); }
  function qa(host, sel) { return host.parentNode.querySelectorAll(sel); }

  /* host 안에 2D 캔버스 하나 — 폭은 host 를 따라가고 높이는 고정 */
  function canvas2d(host, h) {
    var cv = document.createElement("canvas");
    cv.style.display = "block";
    cv.style.width = "100%";
    cv.style.height = h + "px";
    host.insertBefore(cv, host.firstChild);
    var g = cv.getContext("2d");
    var o = { cv: cv, g: g, W: 0, H: h };
    function fit() {
      var w = host.clientWidth || 900;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = Math.round(w * dpr);
      cv.height = Math.round(h * dpr);
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      o.W = w;
    }
    fit();
    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        if (host.clientWidth && host.clientWidth !== o.W) fit();
      }).observe(host);
    }
    return o;
  }

  function clock() {
    var last = performance.now();
    return function () {
      var now = performance.now();
      var dt = Math.min((now - last) / 1000, 0.1);
      last = now;
      return dt;
    };
  }

  function txt(g, s, x, y, color, size, align, weight) {
    g.fillStyle = color || COL.fg;
    g.font = (weight || 500) + " " + Math.round((size || 13) * 1.45) + "px " + FONT;
    g.textAlign = align || "left";
    g.textBaseline = "middle";
    g.fillText(s, x, y);
  }

  function setActive(list, attr, value) {
    Array.prototype.forEach.call(list, function (b) {
      var on = b.getAttribute(attr) === String(value);
      b.style.borderColor = on ? COL.gfx : "";
      b.style.color = on ? COL.gfx : "";
    });
  }

  /* ============================================================
     ① 벡션 실험실 — 복도 표면의 점이 다가오며 만드는 광학 흐름
     ============================================================ */
  window.CGDemos["vection"] = function (host) {
    var H = 420;
    var c = canvas2d(host, H);
    var g = c.g;
    var tick = clock();

    var HALF_FOV = 60 * Math.PI / 180;      /* 캔버스 가로 전체 = 수평 120° */
    var N = 900, ZMAX = 60;
    var pts = [];
    function spawn(p, far) {
      /* 복도 : 폭 5 m · 바닥 y=-1.6 · 천장 y=1.4 · 벽 x=±2.5 */
      var s = Math.random() * 4 | 0;
      if (s === 0) { p.x = (Math.random() - 0.5) * 5; p.y = -1.6; }
      else if (s === 1) { p.x = (Math.random() - 0.5) * 5; p.y = 1.4; }
      else { p.x = s === 2 ? -2.5 : 2.5; p.y = -1.6 + Math.random() * 3; }
      p.z = far ? ZMAX * (0.85 + Math.random() * 0.15) : 0.5 + Math.random() * ZMAX;
      p.px = null;
      return p;
    }
    for (var i = 0; i < N; i++) pts.push(spawn({}, false));

    var st = {
      v: 3, contrast: 0.8, fov: 0, mode: "const", t: 0,
      vis: 3, acc: 0, yawRate: 0, yawAcc: 0
    };
    var hist = [];   /* [시각 속도, 시각 가속] 최근 8초 */

    var spd = q(host, "[data-speed]"), spdV = q(host, "[data-speed-val]");
    var con = q(host, "[data-contrast]"), conV = q(host, "[data-contrast-val]");
    var out = q(host, "[data-out]");
    var fovBtns = qa(host, "[data-fov]");
    var modeBtns = qa(host, "[data-mode]");

    function label() {
      if (spdV) spdV.textContent = st.mode === "yaw"
        ? (st.v * 6).toFixed(0) + "°/s" : st.v.toFixed(1) + " m/s";
      if (conV) conV.textContent = Math.round(st.contrast * 100) + "%";
      setActive(fovBtns, "data-fov", st.fov);
      setActive(modeBtns, "data-mode", st.mode);
    }
    if (spd) spd.addEventListener("input", function () { st.v = +spd.value; label(); });
    if (con) con.addEventListener("input", function () { st.contrast = +con.value / 100; label(); });
    Array.prototype.forEach.call(fovBtns, function (b) {
      b.addEventListener("click", function () { st.fov = +b.getAttribute("data-fov"); label(); });
    });
    Array.prototype.forEach.call(modeBtns, function (b) {
      b.addEventListener("click", function () {
        st.mode = b.getAttribute("data-mode"); st.t = 0; hist.length = 0; label();
      });
    });
    label();

    /* 모드별 속도 프로파일 → 시각 속도와 시각 가속 */
    function profile(dt) {
      st.t += dt;
      var vPrev = st.vis, v;
      if (st.mode === "const") v = st.v;
      else if (st.mode === "accel") {
        var T = 5;                                   /* 5초 주기로 0 → 최고 → 0 */
        v = st.v * (0.5 - 0.5 * Math.cos(2 * Math.PI * st.t / T));
      } else if (st.mode === "stop") {
        var ph = st.t % 4;                           /* 2.5초 이동 · 1.5초 정지 */
        v = ph < 2.5 ? st.v : 0;
      } else v = 0;                                  /* yaw : 전진 없음 */
      st.vis = v;
      st.acc = dt > 0 ? (v - vPrev) / dt : 0;
      var w = st.mode === "yaw" ? st.v * 6 * Math.PI / 180 : 0;
      st.yawAcc = dt > 0 ? (w - st.yawRate) / dt : 0;
      st.yawRate = w;
    }

    var stage = {
      draw: function () {
        var dt = tick();
        profile(dt);
        var W = c.W, cx = W / 2, cy = H / 2;
        var f = cx / Math.tan(HALF_FOV);

        g.fillStyle = COL.bg; g.fillRect(0, 0, W, H);

        var rot = -st.yawRate * dt, cs = Math.cos(rot), sn = Math.sin(rot);
        var sumFlow = 0, nFlow = 0;
        var a = 0.15 + 0.85 * st.contrast;
        for (var i = 0; i < pts.length; i++) {
          var p = pts[i];
          p.z -= st.vis * dt;
          if (rot !== 0) {
            var nx = p.x * cs - p.z * sn, nz = p.x * sn + p.z * cs;
            p.x = nx; p.z = nz;
          }
          if (p.z < 0.4 || p.z > ZMAX * 1.05) { spawn(p, st.mode !== "yaw"); if (st.mode === "yaw") p.z = 0.5 + Math.random() * ZMAX; continue; }
          var sx = cx + f * p.x / p.z, sy = cy - f * p.y / p.z;
          if (sx < -40 || sx > W + 40 || sy < -40 || sy > H + 40) { p.px = null; continue; }
          var r = Math.max(0.8, Math.min(4, 9 / p.z));
          var fade = Math.min(1, (ZMAX - p.z) / 12);
          g.globalAlpha = a * fade;
          if (p.px !== null && dt > 0) {
            var dx = sx - p.px, dy = sy - p.py;
            var ang = Math.atan(Math.hypot(dx, dy) / f) * 180 / Math.PI / dt;
            if (isFinite(ang) && ang < 400) { sumFlow += ang; nFlow++; }
            g.strokeStyle = COL.gfx; g.lineWidth = r * 0.9;
            g.beginPath(); g.moveTo(p.px, p.py); g.lineTo(sx, sy); g.stroke();
          }
          g.fillStyle = "#cfe9ee";
          g.beginPath(); g.arc(sx, sy, r, 0, 6.2832); g.fill();
          p.px = sx; p.py = sy;
        }
        g.globalAlpha = 1;

        /* 시야각 마스크 */
        var visFrac = 1;
        if (st.fov > 0) {
          var R = f * Math.tan(st.fov / 2 * Math.PI / 180);
          g.save();
          g.fillStyle = "rgba(4,5,8,0.97)";
          g.beginPath(); g.rect(0, 0, W, H);
          g.arc(cx, cy, R, 0, 6.2832, true);
          g.fill("evenodd");
          var grd = g.createRadialGradient(cx, cy, R * 0.86, cx, cy, R);
          grd.addColorStop(0, "rgba(4,5,8,0)"); grd.addColorStop(1, "rgba(4,5,8,0.97)");
          g.fillStyle = grd; g.beginPath(); g.arc(cx, cy, R, 0, 6.2832); g.fill();
          g.restore();
          /* 원과 캔버스의 교집합 넓이 (근사 : 세로 잘림만 고려) */
          var area = 0, n = 60;
          for (var k = 0; k < n; k++) {
            var yy = -R + (k + 0.5) * (2 * R / n);
            if (Math.abs(yy) > H / 2) continue;
            area += 2 * Math.min(Math.sqrt(R * R - yy * yy), W / 2) * (2 * R / n);
          }
          visFrac = Math.min(1, area / (W * H));
        }

        /* 응시점 */
        g.strokeStyle = COL.warn; g.lineWidth = 2;
        g.beginPath(); g.moveTo(cx - 9, cy); g.lineTo(cx + 9, cy);
        g.moveTo(cx, cy - 9); g.lineTo(cx, cy + 9); g.stroke();
        txt(g, st.fov > 0 ? "시야 " + st.fov + "°" : "시야 전체 (수평 120°)", 14, H - 20, COL.dim, 13);

        /* 그래프 : 시각 속도 · 시각 가속 · 전정 신호(앉아 있음 = 0) */
        var isYaw = st.mode === "yaw";
        hist.push([isYaw ? st.yawRate * 180 / Math.PI : st.vis,
                   isYaw ? st.yawAcc * 180 / Math.PI : st.acc]);
        if (hist.length > 480) hist.shift();
        var gw = 380, gh = 130, gx = W - gw - 12, gy = 12;
        g.fillStyle = "rgba(11,13,18,0.88)"; g.fillRect(gx, gy, gw, gh);
        g.strokeStyle = COL.line; g.lineWidth = 1; g.strokeRect(gx, gy, gw, gh);
        var mid = gy + gh * 0.62;
        g.strokeStyle = COL.vr; g.lineWidth = 2;
        g.beginPath(); g.moveTo(gx + 6, mid); g.lineTo(gx + gw - 6, mid); g.stroke();
        var vmax = isYaw ? 60 : 10, amax = isYaw ? 60 : 8;
        function plot(idx, col, scale, base) {
          g.strokeStyle = col; g.lineWidth = 2; g.beginPath();
          for (var j = 0; j < hist.length; j++) {
            var x = gx + 6 + (gw - 12) * j / 480;
            var val = Math.max(-1.2, Math.min(1.2, hist[j][idx] / scale));
            var y = base - val * gh * 0.32;
            if (j === 0) g.moveTo(x, y); else g.lineTo(x, y);
          }
          g.stroke();
        }
        plot(0, COL.gfx, vmax, mid);
        plot(1, COL.warn, amax, mid);
        txt(g, isYaw ? "시각 회전" : "시각 속도", gx + 8, gy + 16, COL.gfx, 12);
        txt(g, "시각 가속", gx + 128, gy + 16, COL.warn, 12);
        txt(g, "전정 신호 0", gx + 248, gy + 16, COL.vr, 12);

        if (out) {
          var flow = nFlow ? sumFlow / nFlow : 0;
          var accNow = isYaw ? Math.abs(st.yawAcc * 180 / Math.PI) : Math.abs(st.acc);
          var msg = "보이는 면적 " + Math.round(visFrac * 100) + "% · 평균 광학 흐름 약 " +
            flow.toFixed(0) + "°/s · ";
          if (st.mode === "const") msg += "정속 → 시각 가속 0 = 전정 0 : 가속 불일치 없음 (벡션은 생길 수 있음)";
          else if (st.mode === "accel") msg += "가속·감속 → 시각 가속 " + accNow.toFixed(1) + " m/s² vs 전정 0 : 불일치 계속 변동";
          else if (st.mode === "stop") msg += "출발·정지 → 짧고 큰 가속 충격 · 그 사이는 불일치 0";
          else msg += "요 회전 → 시각은 회전 · 전정은 정지 (회전 흐름 = 불편 임계가 더 낮음)";
          out.textContent = msg + " · 교육용 모형";
        }
      }
    };
    return stage;
  };

  /* ============================================================
     ② 적분 실험실 — 같은 원 궤도를 세 적분기로 계산
     GM = 1 · 반지름 1 · 속도 1 → 정답 = 반지름 1 의 원 (주기 2π ≈ 6.28)
     ============================================================ */
  window.CGDemos["integrator"] = function (host) {
    var H = 420;
    var c = canvas2d(host, H);
    var g = c.g;
    var tick = clock();

    var dtIn = q(host, "[data-dt]"), dtV = q(host, "[data-dt-val]");
    var spIn = q(host, "[data-rate]"), spV = q(host, "[data-rate-val]");
    var out = q(host, "[data-out]");
    var togg = qa(host, "[data-int]");
    var resetBtn = q(host, "[data-reset]");

    var M = [
      { key: "euler", name: "오일러", col: COL.trap, on: true },
      { key: "semi", name: "세미암시적", col: COL.gfx, on: true },
      { key: "verlet", name: "베를레", col: COL.lab, on: true }
    ];
    var P = { dt: 0.1, rate: 1, acc: 0, t: 0 };

    function accel(x, y) {
      var r2 = x * x + y * y, r = Math.sqrt(r2), k = -1 / (r2 * r);
      return [k * x, k * y];
    }
    function reset() {
      P.t = 0; P.acc = 0;
      M.forEach(function (m) {
        m.x = 1; m.y = 0; m.vx = 0; m.vy = 1; m.trail = [[1, 0]]; m.gone = false;
        /* 베를레 시작 : 이전 위치를 테일러 전개로 만든다 x(-dt) ≈ x - v dt + ½ a dt² */
        var a = accel(1, 0);
        m.ox = 1 - 0 * P.dt + 0.5 * a[0] * P.dt * P.dt;
        m.oy = 0 - 1 * P.dt + 0.5 * a[1] * P.dt * P.dt;
      });
    }
    function step(m, dt) {
      if (m.gone) return;
      var a;
      if (m.key === "euler") {
        a = accel(m.x, m.y);
        var nx = m.x + m.vx * dt, ny = m.y + m.vy * dt;   /* 옛 속도로 위치 */
        m.vx += a[0] * dt; m.vy += a[1] * dt;
        m.x = nx; m.y = ny;
      } else if (m.key === "semi") {
        a = accel(m.x, m.y);
        m.vx += a[0] * dt; m.vy += a[1] * dt;             /* 속도 먼저 */
        m.x += m.vx * dt; m.y += m.vy * dt;               /* 새 속도로 위치 */
      } else {
        a = accel(m.x, m.y);
        var px = 2 * m.x - m.ox + a[0] * dt * dt;
        var py = 2 * m.y - m.oy + a[1] * dt * dt;
        m.vx = (px - m.ox) / (2 * dt); m.vy = (py - m.oy) / (2 * dt);
        m.ox = m.x; m.oy = m.y; m.x = px; m.y = py;
      }
      var r = Math.hypot(m.x, m.y);
      if (r > 6 || r < 0.05) m.gone = true;
      m.trail.push([m.x, m.y]);
      if (m.trail.length > 2500) m.trail.shift();
    }
    function energy(m) {
      /* 베를레의 속도는 중앙 차분 → 한 스텝 앞 위치(ox, oy)에서의 값 */
      var x = m.key === "verlet" ? m.ox : m.x, y = m.key === "verlet" ? m.oy : m.y;
      return 0.5 * (m.vx * m.vx + m.vy * m.vy) - 1 / Math.hypot(x, y);
    }

    function label() {
      if (dtV) dtV.textContent = P.dt.toFixed(2);
      if (spV) spV.textContent = "×" + P.rate.toFixed(1);
      Array.prototype.forEach.call(togg, function (b) {
        var m = M.filter(function (mm) { return mm.key === b.getAttribute("data-int"); })[0];
        if (!m) return;
        b.textContent = m.name + (m.on ? " 켬" : " 끔");
        b.style.borderColor = m.on ? m.col : ""; b.style.color = m.on ? m.col : "";
      });
    }
    if (dtIn) dtIn.addEventListener("input", function () { P.dt = +dtIn.value; reset(); label(); });
    if (spIn) spIn.addEventListener("input", function () { P.rate = +spIn.value; label(); });
    Array.prototype.forEach.call(togg, function (b) {
      b.addEventListener("click", function () {
        M.forEach(function (m) { if (m.key === b.getAttribute("data-int")) m.on = !m.on; });
        label();
      });
    });
    if (resetBtn) resetBtn.addEventListener("click", function () { reset(); });
    reset(); label();

    return {
      draw: function () {
        /* 고정 타임스텝 누산기 — 3주차의 그 구조 */
        P.acc += tick() * P.rate;
        var guard = 0;
        while (P.acc >= P.dt && guard++ < 400) {
          M.forEach(function (m) { step(m, P.dt); });
          P.acc -= P.dt; P.t += P.dt;
        }
        var W = c.W, cx = W * 0.27, cy = H / 2, S = 150;
        g.fillStyle = COL.bg; g.fillRect(0, 0, W, H);

        /* 정답 원 */
        g.setLineDash([5, 6]); g.strokeStyle = COL.faint; g.lineWidth = 1.5;
        g.beginPath(); g.arc(cx, cy, S, 0, 6.2832); g.stroke(); g.setLineDash([]);
        g.fillStyle = COL.warn; g.beginPath(); g.arc(cx, cy, 7, 0, 6.2832); g.fill();
        txt(g, "중심 (끌어당기는 힘)", cx, cy + 26, COL.dim, 12, "center");

        M.forEach(function (m) {
          if (!m.on) return;
          g.strokeStyle = m.col; g.lineWidth = 2; g.globalAlpha = 0.85;
          g.beginPath();
          m.trail.forEach(function (p, i) {
            var X = cx + p[0] * S, Y = cy - p[1] * S;
            if (i === 0) g.moveTo(X, Y); else g.lineTo(X, Y);
          });
          g.stroke(); g.globalAlpha = 1;
          if (!m.gone) {
            g.fillStyle = m.col;
            g.beginPath(); g.arc(cx + m.x * S, cy - m.y * S, 6, 0, 6.2832); g.fill();
          }
        });

        /* 오른쪽 표 */
        var tx = W * 0.54, ty = 40;
        txt(g, "시간 " + P.t.toFixed(1) + " · 바퀴 " + (P.t / (2 * Math.PI)).toFixed(1) +
            " · dt " + P.dt.toFixed(2), tx, ty - 8, COL.dim, 13);
        txt(g, "적분기", tx, ty + 30, COL.faint, 12);
        txt(g, "반지름 (정답 1)", tx + 170, ty + 30, COL.faint, 12);
        txt(g, "에너지 오차", tx + 340, ty + 30, COL.faint, 12);
        M.forEach(function (m, i) {
          var y = ty + 74 + i * 44;
          var r = Math.hypot(m.x, m.y);
          var e = (energy(m) - (-0.5)) / 0.5 * 100;
          txt(g, m.name, tx, y, m.on ? m.col : COL.faint, 15, "left", 700);
          txt(g, m.gone ? "이탈" : r.toFixed(3), tx + 170, y, m.on ? COL.fg : COL.faint, 15);
          txt(g, m.gone ? "—" : (e >= 0 ? "+" : "") + e.toFixed(1) + "%", tx + 340, y,
              Math.abs(e) > 5 ? COL.trap : (m.on ? COL.fg : COL.faint), 15);
        });
        txt(g, "오일러 = 옛 속도로 이동 → 에너지 증가 → 바깥으로 나선", tx, ty + 240, COL.dim, 12);
        txt(g, "세미암시적 · 베를레 = 오차가 쌓이지 않고 출렁임", tx, ty + 272, COL.dim, 12);

        if (out) {
          var eu = M[0];
          out.textContent = eu.gone
            ? "오일러 궤도 화면 밖 이탈 · 같은 dt 에서 다른 두 적분기는 원 근처 유지"
            : "dt 를 키울수록 오일러의 나선이 빨라짐 · dt 를 줄이면 늦출 수는 있으나 없앨 수는 없음";
        }
      }
    };
  };

  /* ============================================================
     ③ 터널링 실험실 — 0.02초마다 «순간이동» 하는 공과 얇은 벽
     ============================================================ */
  window.CGDemos["tunneling"] = function (host) {
    var H = 380;
    var c = canvas2d(host, H);
    var g = c.g;
    var tick = clock();

    var vIn = q(host, "[data-v]"), vV = q(host, "[data-v-val]");
    var wIn = q(host, "[data-wall]"), wV = q(host, "[data-wall-val]");
    var modeBtns = qa(host, "[data-ccd]");
    var runBtn = q(host, "[data-trials]");
    var out = q(host, "[data-out]");

    var R = 0.1, DT = 0.02, WALL_X = 4, SPAN = 6.4;
    var T = { v: 30, wall: 0.2, ccd: false, x: 0, steps: [], state: "fly", wait: 0, hit: null,
              trials: 0, passes: 0 };

    function launch() {
      T.x = 0.3 + Math.random() * T.v * DT;   /* 시작 위상 무작위 */
      T.steps = [T.x]; T.state = "fly"; T.hit = null; T.wait = 0;
    }
    function physStep() {
      var x0 = T.x, x1 = T.x + T.v * DT;
      var L = WALL_X, Rr = WALL_X + T.wall;
      if (T.ccd) {
        /* 연속 : 이동 경로(선분) 전체를 검사 → 벽 앞면에 닿는 순간 정지 */
        if (x0 + R <= L && x1 + R >= L) { T.x = L - R; T.steps.push(T.x); T.state = "hit"; T.hit = "ccd"; return; }
      }
      T.x = x1; T.steps.push(T.x);
      /* 이산 : 도착한 자리에서만 겹침 검사 */
      if (T.x + R > L && T.x - R < Rr) { T.state = "hit"; T.hit = "overlap"; return; }
      if (T.x - R > Rr + 0.6) T.state = "pass";
    }
    function trialOnce() {
      launch();
      var guard = 0;
      while (T.state === "fly" && guard++ < 2000) physStep();
      return T.state === "pass";
    }

    function label() {
      if (vV) vV.textContent = T.v.toFixed(0) + " m/s";
      if (wV) wV.textContent = T.wall.toFixed(2) + " m";
      setActive(modeBtns, "data-ccd", T.ccd ? "on" : "off");
    }
    if (vIn) vIn.addEventListener("input", function () { T.v = +vIn.value; T.trials = T.passes = 0; launch(); label(); });
    if (wIn) wIn.addEventListener("input", function () { T.wall = +wIn.value; T.trials = T.passes = 0; launch(); label(); });
    Array.prototype.forEach.call(modeBtns, function (b) {
      b.addEventListener("click", function () {
        T.ccd = b.getAttribute("data-ccd") === "on"; T.trials = T.passes = 0; launch(); label();
      });
    });
    if (runBtn) runBtn.addEventListener("click", function () {
      var n = 0;
      for (var i = 0; i < 100; i++) if (trialOnce()) n++;
      T.trials += 100; T.passes += n; launch();
    });
    launch(); label();

    var slow = 0;
    return {
      draw: function () {
        var dt = tick();
        /* 화면 연출 : 실제의 1/12 속도 슬로모션으로 한 스텝씩 */
        slow += dt;
        var interval = Math.max(0.05, 0.22 * 30 / Math.max(T.v, 5));
        if (T.state === "fly" && slow > interval) { slow = 0; physStep(); }
        if (T.state !== "fly") { T.wait += dt; if (T.wait > 1.6) launch(); }

        var W = c.W, pad = 30, S = (W - pad * 2) / SPAN, base = H * 0.5;
        function X(x) { return pad + x * S; }
        g.fillStyle = COL.bg; g.fillRect(0, 0, W, H);
        /* 바닥선 */
        g.strokeStyle = COL.line; g.lineWidth = 1;
        g.beginPath(); g.moveTo(pad, base + R * S + 2); g.lineTo(W - pad, base + R * S + 2); g.stroke();
        /* 벽 */
        g.fillStyle = "rgba(255,90,77,0.25)"; g.strokeStyle = COL.trap; g.lineWidth = 2;
        g.fillRect(X(WALL_X), base - 60, T.wall * S, 120);
        g.strokeRect(X(WALL_X), base - 60, T.wall * S, 120);
        txt(g, "벽 " + T.wall.toFixed(2) + " m", X(WALL_X) + T.wall * S / 2, base - 82, COL.trap, 13, "center");
        /* 스텝별 위치 (유령) */
        T.steps.forEach(function (x, i) {
          var last = i === T.steps.length - 1;
          g.globalAlpha = last ? 1 : 0.35;
          g.strokeStyle = COL.gfx; g.fillStyle = last ? COL.gfx : "transparent"; g.lineWidth = 2;
          g.beginPath(); g.arc(X(x), base, Math.max(R * S, 5), 0, 6.2832);
          if (last) g.fill(); g.stroke();
          g.globalAlpha = 1;
          if (i > 0) {
            g.strokeStyle = COL.faint; g.setLineDash([3, 4]);
            g.beginPath(); g.moveTo(X(T.steps[i - 1]), base + 22); g.lineTo(X(x), base + 22); g.stroke();
            g.setLineDash([]);
          }
        });
        var stepLen = T.v * DT;
        txt(g, "한 스텝 이동 = " + T.v.toFixed(0) + " × 0.02 = " + stepLen.toFixed(2) + " m", pad, 50, COL.dim, 13);
        txt(g, T.ccd ? "연속 판정 (CCD)" : "이산 판정 (Discrete)", W - pad, 50, T.ccd ? COL.lab : COL.warn, 14, "right", 700);
        var msg = T.state === "hit" ? (T.hit === "ccd" ? "경로 검사로 벽 앞에서 정지" : "도착 자리에서 겹침 발견 → 충돌")
          : T.state === "pass" ? "벽을 한 번도 «밟지» 않고 통과 = 터널링" : "";
        txt(g, msg, W / 2, H - 28, T.state === "pass" ? COL.trap : COL.lab, 15, "center", 700);

        if (out) {
          var gap = T.wall + 2 * R;
          var s = "벽 두께 + 공 지름 = " + gap.toFixed(2) + " m vs 한 스텝 " + stepLen.toFixed(2) + " m → " +
            (stepLen > gap ? "건너뛸 수 있음" : "건너뛸 수 없음");
          if (T.trials) s += " · 100회 시행 누적 " + T.trials + "회 중 통과 " + T.passes + "회 (" +
            Math.round(T.passes / T.trials * 100) + "%)";
          out.textContent = s;
        }
      }
    };
  };
})();
