/* ============================================================
   12주차 데모
   1) frame-budget   : 프레임 예산 막대 — CPU·GPU 중 어느 쪽이 넘치는가
   2) comfort-budget : 컴포트 예산 시뮬레이터 — 가속·시야각·베그넷·프레임률·지연
   둘 다 2D canvas · 교육용 단순 모델 (계수·가중치는 설명용 임의값)
   ============================================================ */
(function () {
  "use strict";
  window.CGDemos = window.CGDemos || {};

  var COL = {
    bg: "#06070a", panel: "#0e1118", line: "#2a3040", fg: "#e8ecf4", dim: "#9aa4b8",
    faint: "#5f6980", gfx: "#35d6e6", vr: "#ff5fa2", trap: "#ff5a4d", lab: "#a8e05f",
    warn: "#ffc44d"
  };
  var FONT = '"Pretendard Variable", Pretendard, "Malgun Gothic", sans-serif';

  /* host 안에 canvas 생성 · 폭 변화 추적 */
  function makeCanvas(host, h) {
    var cv = document.createElement("canvas");
    cv.style.display = "block";
    cv.style.width = "100%";
    cv.style.height = h + "px";
    host.insertBefore(cv, host.firstChild);
    var g = cv.getContext("2d");
    var st = { cv: cv, g: g, w: 0, h: h, dirty: true };
    function fit() {
      var w = host.clientWidth || 1100;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (w === st.w && cv.width === Math.round(w * dpr)) return;
      st.w = w;
      cv.width = Math.round(w * dpr);
      cv.height = Math.round(h * dpr);
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      st.dirty = true;
    }
    fit();
    if (window.ResizeObserver) new ResizeObserver(fit).observe(host);
    st.fit = fit;
    return st;
  }

  /* 슬라이더·셀렉트 묶음 읽기 : data-k / data-v */
  function bindControls(host, fmt, onChange) {
    var ui = host.parentNode;
    var inputs = ui.querySelectorAll("[data-k]");
    var defaults = {};
    var val = {};
    function read() {
      Array.prototype.forEach.call(inputs, function (el) {
        val[el.dataset.k] = parseFloat(el.value);
        var out = ui.querySelector('[data-v="' + el.dataset.k + '"]');
        if (out && fmt[el.dataset.k]) out.textContent = fmt[el.dataset.k](val[el.dataset.k]);
      });
      onChange(val);
    }
    Array.prototype.forEach.call(inputs, function (el) {
      defaults[el.dataset.k] = el.value;
      el.addEventListener("input", read);
      el.addEventListener("change", read);
    });
    var rb = ui.querySelector("[data-reset]");
    if (rb) rb.addEventListener("click", function () {
      Array.prototype.forEach.call(inputs, function (el) { el.value = defaults[el.dataset.k]; });
      read();
    });
    read();
    return val;
  }

  function clamp01(x) { return Math.max(0, Math.min(1, x)); }

  function roundRect(g, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    g.beginPath();
    g.moveTo(x + r, y);
    g.arcTo(x + w, y, x + w, y + h, r);
    g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r);
    g.arcTo(x, y, x + w, y, r);
    g.closePath();
  }

  /* ============================================================
     1) 프레임 예산 막대
     ============================================================ */
  window.CGDemos["frame-budget"] = function (host) {
    var H = 372;
    var c = makeCanvas(host, H);
    var g = c.g;
    var FFR = [1.0, 0.9, 0.82, 0.74];
    var FFR_NAME = ["끔", "낮음", "중간", "높음"];
    var m = null;

    function model(v) {
      var cpu = [
        { n: "게임 로직", ms: 2.0, c: COL.lab },
        { n: "물리", ms: 0.8, c: COL.lab },
        { n: "드로우콜 준비", ms: v.dc * 0.022, c: COL.gfx },
        { n: "그림자 패스 준비", ms: v.sh * v.dc * 0.008, c: COL.warn }
      ];
      var pix = 5.0 * v.rs * v.rs * FFR[v.ffr | 0] * (1 + 0.65 * (v.od - 1));
      var gpu = [
        { n: "정점 처리", ms: v.tri * 0.03, c: COL.gfx },
        { n: "그림자맵", ms: v.sh * 1.1, c: COL.warn },
        { n: "두 눈 픽셀", ms: pix, c: COL.vr },
        { n: "합성", ms: 0.8, c: COL.dim }
      ];
      function sum(a) { return a.reduce(function (s, x) { return s + x.ms; }, 0); }
      return { cpu: cpu, gpu: gpu, cpuT: sum(cpu), gpuT: sum(gpu),
               budget: 1000 / v.hz, hz: v.hz, v: v };
    }

    bindControls(host, {
      dc: function (x) { return x.toFixed(0); },
      tri: function (x) { return x.toFixed(0) + "만"; },
      od: function (x) { return x.toFixed(1) + "겹"; },
      sh: function (x) { return x.toFixed(0) + "개"; },
      rs: function (x) { return x.toFixed(2); }
    }, function (v) { m = model(v); c.dirty = true; });

    function bar(y, label, parts, total, sx, x0, budget) {
      g.font = "700 19px " + FONT;
      g.fillStyle = COL.fg; g.textBaseline = "middle";
      g.fillText(label, 22, y + 22);
      var x = x0;
      parts.forEach(function (p) {
        var w = p.ms * sx;
        if (w <= 0.5) return;
        g.fillStyle = p.c + "33";
        g.strokeStyle = p.c; g.lineWidth = 1.5;
        roundRect(g, x, y, w, 44, 5); g.fill(); g.stroke();
        if (w > 74) {
          g.font = "15px " + FONT; g.fillStyle = p.c;
          g.fillText(p.n, x + 8, y + 15);
          g.fillText(p.ms.toFixed(1) + " ms", x + 8, y + 33);
        }
        x += w;
      });
      var over = total > budget;
      g.font = "700 19px " + FONT;
      g.fillStyle = over ? COL.trap : COL.lab;
      g.fillText(total.toFixed(1) + " ms", x + 10, y + 22);
    }

    function render() {
      c.fit();
      var W = c.w;
      g.fillStyle = COL.bg; g.fillRect(0, 0, W, H);
      if (!m) return;
      var x0 = 150, right = W - 110;
      var maxMs = Math.max(20, Math.ceil(Math.max(m.cpuT, m.gpuT) + 2));
      var sx = (right - x0) / maxMs;

      /* 눈금 */
      g.strokeStyle = COL.line; g.lineWidth = 1;
      g.font = "15px " + FONT; g.fillStyle = COL.faint; g.textBaseline = "middle";
      for (var t = 0; t <= maxMs; t += 5) {
        var xx = x0 + t * sx;
        g.beginPath(); g.moveTo(xx, 50); g.lineTo(xx, 236); g.stroke();
        g.fillText(t + " ms", xx - 14, 40);
      }
      /* 예산선 */
      var bx = x0 + m.budget * sx;
      g.strokeStyle = COL.warn; g.lineWidth = 3; g.setLineDash([8, 6]);
      g.beginPath(); g.moveTo(bx, 46); g.lineTo(bx, 246); g.stroke();
      g.setLineDash([]);
      g.font = "700 16px " + FONT; g.fillStyle = COL.warn;
      g.fillText(m.hz + " Hz 마감 " + m.budget.toFixed(1) + " ms", Math.min(bx + 8, W - 190), 258);

      bar(70, "CPU", m.cpu, m.cpuT, sx, x0, m.budget);
      bar(160, "GPU", m.gpu, m.gpuT, sx, x0, m.budget);

      /* 판정 */
      var worst = Math.max(m.cpuT, m.gpuT);
      var slow = m.cpuT >= m.gpuT ? "CPU" : "GPU";
      var ok = worst <= m.budget;
      var y = 300;
      roundRect(g, 18, y - 22, W - 36, 74, 10);
      g.fillStyle = ok ? "rgba(168,224,95,0.08)" : "rgba(255,90,77,0.10)"; g.fill();
      g.font = "700 20px " + FONT; g.fillStyle = ok ? COL.lab : COL.trap;
      g.fillText(ok ? "통과 — 매 프레임 마감 안에 도착 · " + m.hz + " fps 유지"
                    : "초과 — " + slow + " 병목 · 마감 놓침 → 재투영 · 저더 · 프레임률 강등 위험", 34, y);
      g.font = "16px " + FONT; g.fillStyle = COL.dim;
      var tip;
      if (ok) tip = "여유 " + (m.budget - worst).toFixed(1) + " ms · 느린 쪽 = " + slow + " (" + worst.toFixed(1) + " ms)";
      else if (slow === "GPU") tip = "GPU 쪽을 줄여야 효과 : 반투명 겹 · 렌더 스케일 · FFR · 그림자 광원  (드로우콜만 줄이면 변화 작음)";
      else tip = "CPU 쪽을 줄여야 효과 : 드로우콜 (Static·재질 통일) · 그림자 광원  (FFR·해상도는 효과 없음)";
      g.fillText(tip, 34, y + 28);
    }

    return {
      draw: function () {
        if (!c.dirty) return;
        c.dirty = false;
        render();
      }
    };
  };

  /* ============================================================
     2) 컴포트 예산 시뮬레이터
     ============================================================ */
  window.CGDemos["comfort-budget"] = function (host) {
    var H = 380;
    var c = makeCanvas(host, H);
    var g = c.g;
    var v = {};
    var FPS_R = { 45: 1, 60: 0.6, 72: 0.3, 90: 0.1, 120: 0 };

    bindControls(host, {
      acc: function (x) { return x === 0 ? "즉시" : x.toFixed(2) + " m/s²"; },
      fov: function (x) { return x.toFixed(0) + "°"; },
      vig: function (x) { return x.toFixed(2); },
      lat: function (x) { return x.toFixed(0) + " ms"; }
    }, function (nv) { v = nv; });

    /* ---- 이동 시뮬레이션 : 출발 → 순항 → 정지 반복 ---- */
    var VMAX = 3.0;
    var sim = { t: 0, z: 0, vel: 0, phase: 0, timer: 0, acc: 0 };
    function step(dt) {
      var a = v.acc;
      var prev = sim.vel;
      sim.timer += dt;
      if (sim.phase === 0) {              /* 가속 */
        sim.vel = a === 0 ? VMAX : Math.min(VMAX, sim.vel + a * dt);
        if (sim.vel >= VMAX) { sim.phase = 1; sim.timer = 0; }
      } else if (sim.phase === 1) {       /* 순항 */
        if (sim.timer > 2.2) { sim.phase = 2; sim.timer = 0; }
      } else if (sim.phase === 2) {       /* 감속 */
        sim.vel = a === 0 ? 0 : Math.max(0, sim.vel - a * dt);
        if (sim.vel <= 0) { sim.phase = 3; sim.timer = 0; }
      } else {                            /* 정지 */
        if (sim.timer > 1.2) { sim.phase = 0; sim.timer = 0; }
      }
      sim.acc = dt > 0 ? (sim.vel - prev) / dt : 0;
      sim.z += sim.vel * dt;
      sim.t += dt;
    }

    /* 위험도 모델 (교육용) */
    function risk() {
      var A = v.acc === 0 ? 0.1 : clamp01(v.acc / 3);
      var feff = v.fov * (1 - 0.55 * v.vig);
      var Fn = clamp01((feff - 40) / 70);
      var motion = A * (0.4 + 0.6 * Fn);
      var R = FPS_R[v.fps | 0] != null ? FPS_R[v.fps | 0] : 0.3;
      var L = clamp01((v.lat - 15) / 85);
      var parts = [
        { n: "가속 충돌", p: 40 * motion, max: 40, c: COL.vr },
        { n: "주변 흐름", p: 15 * Fn, max: 15, c: COL.gfx },
        { n: "프레임률", p: 15 * R, max: 15, c: COL.warn },
        { n: "지연", p: 30 * L, max: 30, c: COL.trap }
      ];
      var total = parts.reduce(function (s, x) { return s + x.p; }, 0);
      return { parts: parts, total: total, feff: feff };
    }

    /* 미리보기 상태 (프레임률 흉내 : 정해진 간격에만 갱신) */
    var shown = { z: 0, yaw: 0, vel: 0, at: 0 };
    var acc = 0;
    var yawHist = [];                    /* 지연 흉내 : 과거 머리 방향 */
    var vigNow = 0;
    var last = performance.now();

    function headYaw(t) { return 0.10 * Math.sin(t * 1.25) + 0.04 * Math.sin(t * 2.9); }

    function drawPreview(x0, y0, W, Hh, r) {
      g.save();
      roundRect(g, x0, y0, W, Hh, 12); g.clip();
      g.fillStyle = "#000"; g.fillRect(x0, y0, W, Hh);

      /* 사람 시야 약 200° 중 미리보기 프레임 = 120° 로 고정 · 그 안에 HMD 시야각만 밝힘 */
      var cx = x0 + W / 2, cy = y0 + Hh * 0.46;
      var HUMAN = 120 * Math.PI / 180;
      var f = (W / 2) / Math.tan(HUMAN / 2);
      var shift = Math.tan(shown.yaw) * f;      /* 화면에 그려진 머리 방향 */

      /* 장면 : 바닥 선 · 벽 기둥 */
      g.fillStyle = "#101521"; g.fillRect(x0, y0, W, Hh);
      var vx = cx - shift;
      var camH = 1.6, wallX = 2.2;
      g.lineWidth = 1.4;
      /* 바닥 세로 선 (진행 방향) */
      g.strokeStyle = "rgba(53,214,230,0.45)";
      for (var lx = -6; lx <= 6; lx += 1) {
        g.beginPath(); g.moveTo(vx, cy);
        var zn = 0.6;
        g.lineTo(vx + lx * f / zn * 0.5, cy + camH * f / zn * 0.5); g.stroke();
      }
      /* 바닥 가로 선 + 벽 기둥 (1 m 간격) */
      var zoff = shown.z % 1.5;
      for (var k = 0; k < 40; k++) {
        var z = 0.35 + k * 1.5 - zoff;
        if (z <= 0.3) continue;
        var sy = cy + camH * f / z;
        if (sy > y0 + Hh + 40) continue;
        var half = 7 * f / z;
        g.strokeStyle = "rgba(53,214,230," + (0.55 * Math.min(1, 3 / z)).toFixed(3) + ")";
        g.beginPath(); g.moveTo(vx - half, sy); g.lineTo(vx + half, sy); g.stroke();
        /* 기둥 : 좌우 벽 */
        var px = wallX * f / z, top = cy - 1.4 * f / z, bot = sy;
        var pw = Math.max(2, 0.25 * f / z);
        g.fillStyle = "rgba(255,95,162," + (0.75 * Math.min(1, 2.5 / z)).toFixed(3) + ")";
        g.fillRect(vx - px - pw, top, pw, bot - top);
        g.fillRect(vx + px, top, pw, bot - top);
      }
      /* 실제 머리 방향 (지연 없이) */
      var trueShift = Math.tan(headYaw(sim.t)) * f;
      g.strokeStyle = COL.warn; g.setLineDash([5, 5]); g.lineWidth = 1.5;
      g.beginPath(); g.moveTo(cx - trueShift, y0 + 14); g.lineTo(cx - trueShift, y0 + Hh - 14); g.stroke();
      g.setLineDash([]);
      g.strokeStyle = COL.fg; g.lineWidth = 1.5;
      g.beginPath(); g.moveTo(vx - 9, cy); g.lineTo(vx + 9, cy); g.moveTo(vx, cy - 9); g.lineTo(vx, cy + 9); g.stroke();

      /* HMD 시야각 밖 = 검정 (렌즈 테두리) */
      var hw = Math.tan(Math.min(v.fov, 119) * Math.PI / 360) * f;
      g.fillStyle = "#000";
      g.fillRect(x0, y0, cx - hw - x0, Hh);
      g.fillRect(cx + hw, y0, x0 + W - (cx + hw), Hh);

      /* 베그넷 : 이동 중에만 · 부드럽게 닫힘 */
      var moving = shown.vel > 0.05;
      var target = moving ? v.vig : 0;
      vigNow += (target - vigNow) * 0.12;
      if (vigNow > 0.01) {
        var outer = hw * 1.05;
        var inner = hw * (1 - 0.62 * vigNow);
        var grd = g.createRadialGradient(cx, cy, Math.max(4, inner * 0.72), cx, cy, outer);
        grd.addColorStop(0, "rgba(0,0,0,0)");
        grd.addColorStop(0.55, "rgba(0,0,0," + (0.7 * vigNow).toFixed(3) + ")");
        grd.addColorStop(1, "rgba(0,0,0," + Math.min(1, 1.1 * vigNow).toFixed(3) + ")");
        g.fillStyle = grd;
        g.fillRect(cx - hw, y0, hw * 2, Hh);
      }
      g.restore();

      g.strokeStyle = COL.line; g.lineWidth = 2;
      roundRect(g, x0, y0, W, Hh, 12); g.stroke();

      /* 캡션 */
      g.font = "15px " + FONT; g.textBaseline = "alphabetic";
      g.fillStyle = COL.dim;
      g.fillText("미리보기 폭 = 사람 시야 120° · 밝은 영역 = HMD 시야각 " + v.fov + "°", x0 + 12, y0 + Hh - 12);
      g.fillStyle = COL.warn;
      g.fillText("점선 = 실제 머리 방향 · 십자 = 화면이 그린 방향", x0 + 12, y0 + 22);
      var ph = ["가속", "순항", "감속", "정지"][sim.phase];
      g.fillStyle = sim.phase === 0 || sim.phase === 2 ? COL.vr : COL.fg;
      g.font = "700 17px " + FONT;
      g.fillText(ph + "  " + sim.vel.toFixed(1) + " m/s", x0 + W - 150, y0 + 22);
    }

    function drawGauges(x0, y0, W, Hh, rk) {
      var lvl = rk.total < 25 ? "낮음" : rk.total < 50 ? "주의" : "높음";
      var lc = rk.total < 25 ? COL.lab : rk.total < 50 ? COL.warn : COL.trap;
      g.textBaseline = "alphabetic";
      g.font = "700 17px " + FONT; g.fillStyle = COL.dim;
      g.fillText("위험도 지표 (0~100 · 교육용)", x0, y0 + 18);
      g.font = "700 46px " + FONT; g.fillStyle = lc;
      g.fillText(rk.total.toFixed(0), x0, y0 + 70);
      var nw = g.measureText(rk.total.toFixed(0)).width;
      g.font = "700 22px " + FONT;
      g.fillText(lvl, x0 + nw + 14, y0 + 68);

      var by = y0 + 98;
      rk.parts.forEach(function (p, i) {
        var yy = by + i * 46;
        g.font = "16px " + FONT; g.fillStyle = COL.fg;
        g.fillText(p.n, x0, yy + 4);
        g.fillStyle = COL.dim;
        g.fillText(p.p.toFixed(1) + " / " + p.max, x0 + W - 70, yy + 4);
        g.fillStyle = "#1b2030";
        roundRect(g, x0, yy + 12, W, 14, 7); g.fill();
        g.fillStyle = p.c;
        roundRect(g, x0, yy + 12, Math.max(2, W * p.p / 40), 14, 7); g.fill();
      });
      var ny = by + 4 * 46 + 6;
      g.font = "15px " + FONT; g.fillStyle = COL.dim;
      g.fillText("유효 시야각 (베그넷 반영) " + rk.feff.toFixed(0) + "°", x0, ny);
      g.fillText("참고 : 전방 가속 임계 평균 0.70 m/s²", x0, ny + 22);
      g.fillStyle = COL.faint;
      g.fillText("가중치 임의 · 실제 멀미 확률 아님", x0, ny + 44);
    }

    return {
      draw: function () {
        c.fit();
        var now = performance.now();
        var dt = Math.min((now - last) / 1000, 0.1);
        last = now;
        step(dt);

        /* 지연 : 과거 머리 방향 사용 */
        yawHist.push({ t: sim.t, y: headYaw(sim.t) });
        while (yawHist.length > 2 && yawHist[1].t < sim.t - v.lat / 1000) yawHist.shift();
        var delayedYaw = yawHist[0].y;

        /* 프레임률 : 1/fps 마다만 새 그림 */
        acc += dt;
        var period = 1 / (v.fps || 90);
        if (acc >= period) {
          acc = acc % period;
          shown.z = sim.z; shown.yaw = delayedYaw; shown.vel = sim.vel;
        }

        var W = c.w;
        g.fillStyle = COL.bg; g.fillRect(0, 0, W, H);
        var pw = Math.round(W * 0.64);
        drawPreview(14, 14, pw - 14, H - 28);
        drawGauges(pw + 26, 22, W - pw - 50, H - 40, risk());
      }
    };
  };
})();
