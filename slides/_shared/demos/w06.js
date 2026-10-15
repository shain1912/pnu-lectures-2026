/* ============================================================
   6주차 데모
   1) ppd-lab    — PPD · 앨리어싱 실험실 (2D canvas, 픽셀 단위 광선 추적)
                   PPD 슬라이더 · 밉맵 on/off(Point / Trilinear / Aniso) ·
                   머리 미세 진동(각분) · 중심/주변 시야 마스크(포비티드)
   2) uv-unwrap  — 정육면체 ↔ UV 전개도 펼치기 · seam 표시 (three.js r128)
   _stage.js 를 먼저 로드할 것 (uv-unwrap 만 사용)
   ============================================================ */
(function () {
  "use strict";
  window.CGDemos = window.CGDemos || {};

  function q(host, sel) { return host.parentNode.querySelector(sel); }

  /* ============================================================
     1) PPD · 앨리어싱 실험실
     ------------------------------------------------------------
     - 화면 = 시야 가로 FOVH° 구간. 내부 해상도 = PPD × FOVH 픽셀
       → 낮은 PPD 일수록 굵은 픽셀로 확대 표시 (nearest)
     - 바닥 : 눈높이 1.6 m, 칸 1 m 바둑판 (텍스처 256², 칸 32 텍셀)
     - 필터 : point(밉맵 없음) / trilinear(밉맵) / aniso 4x
     - 머리 진동 : yaw·pitch 를 각분 단위로 미세하게 흔듦
     - 시야 마스크 : 원 밖은 3×3 블록당 1회만 계산 (고정 / 시선 추적)
     ============================================================ */
  window.CGDemos["ppd-lab"] = function (host) {
    var DISP_H = 390;
    var FOVH = 18;            /* 도 */
    var EYE = 1.6;            /* m */
    var TEX = 256;            /* 텍셀 */
    var TPM = 32;             /* 텍셀 / m  (텍스처 1장 = 8 m = 8칸, 칸 1 m) */
    var CYCLE = 2.0;          /* 흰+검 한 주기 = 2 m */
    var FOVEA_DEG = 3;        /* 고해상도 원 반지름 */
    var BLOCK = 3;

    /* ---- 캔버스 ---- */
    var cv = document.createElement("canvas");
    cv.style.width = "100%";
    cv.style.height = DISP_H + "px";
    cv.style.display = "block";
    cv.style.imageRendering = "pixelated";
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext("2d");
    var off = document.createElement("canvas");
    var octx = off.getContext("2d");

    /* ---- 밉맵 체인 (회색조) ---- */
    var mips = [];
    (function build() {
      var a = new Float32Array(TEX * TEX);
      for (var y = 0; y < TEX; y++)
        for (var x = 0; x < TEX; x++)
          a[y * TEX + x] = (((x >> 5) + (y >> 5)) & 1) ? 1 : 0;
      mips.push({ s: TEX, d: a });
      var s = TEX;
      while (s > 1) {
        var ns = s >> 1, b = new Float32Array(ns * ns), p = mips[mips.length - 1].d;
        for (var j = 0; j < ns; j++)
          for (var i = 0; i < ns; i++) {
            var k = (2 * j) * s + 2 * i;
            b[j * ns + i] = (p[k] + p[k + 1] + p[k + s] + p[k + s + 1]) * 0.25;
          }
        mips.push({ s: ns, d: b });
        s = ns;
      }
    })();
    var MAXL = mips.length - 1;

    function bilinear(L, u, v) {           /* u,v : 레벨 0 텍셀 단위 */
      var m = mips[L], s = m.s, d = m.d;
      var sc = s / TEX;
      var x = u * sc - 0.5, y = v * sc - 0.5;
      var x0 = Math.floor(x), y0 = Math.floor(y);
      var fx = x - x0, fy = y - y0;
      var msk = s - 1;
      var xa = x0 & msk, xb = (x0 + 1) & msk, ya = y0 & msk, yb = (y0 + 1) & msk;
      var t = d[ya * s + xa] + (d[ya * s + xb] - d[ya * s + xa]) * fx;
      var b = d[yb * s + xa] + (d[yb * s + xb] - d[yb * s + xa]) * fx;
      return t + (b - t) * fy;
    }
    function trilinear(u, v, lod) {
      if (lod <= 0) return bilinear(0, u, v);
      if (lod >= MAXL) return bilinear(MAXL, u, v);
      var l0 = Math.floor(lod), f = lod - l0;
      var a = bilinear(l0, u, v);
      return a + (bilinear(l0 + 1, u, v) - a) * f;
    }
    function point(u, v) {
      var x = Math.floor(u) & (TEX - 1), y = Math.floor(v) & (TEX - 1);
      return mips[0].d[y * TEX + x];
    }

    /* ---- 상태 ---- */
    var st = { ppd: 25, filter: 0, jit: 3, fov: 0 };
    var FILTERS = ["밉맵 끔 (Point)", "밉맵 켬 (Trilinear)", "Trilinear + 이방성 4x"];
    var FOVS = ["시야 마스크 끔", "고정 포비티드", "시선 추적 (마우스)"];
    var gaze = { x: 0.5, y: 0.5 };
    var dirty = true;

    var ppdIn = q(host, '[data-k="ppd"]'), ppdV = q(host, '[data-v="ppd"]');
    var jitIn = q(host, '[data-k="jit"]'), jitV = q(host, '[data-v="jit"]');
    var fBtn = q(host, "[data-filter]"), fovBtn = q(host, "[data-fov]");
    var out = q(host, "[data-out]");
    var presets = host.parentNode.querySelectorAll("[data-ppd]");

    function ui() {
      if (ppdIn) ppdIn.value = st.ppd;
      if (ppdV) ppdV.textContent = st.ppd;
      if (jitV) jitV.textContent = st.jit + "′";
      if (fBtn) {
        fBtn.textContent = "필터 : " + FILTERS[st.filter];
        fBtn.style.borderColor = st.filter ? "#4f7a16" : "#c2401d";
        fBtn.style.color = st.filter ? "#4f7a16" : "#c2401d";
      }
      if (fovBtn) {
        fovBtn.textContent = FOVS[st.fov];
        fovBtn.style.borderColor = st.fov ? "#a3245e" : "";
        fovBtn.style.color = st.fov ? "#a3245e" : "";
      }
      Array.prototype.forEach.call(presets, function (b) {
        var on = +b.dataset.ppd === st.ppd;
        b.style.borderColor = on ? "#35d6e6" : "";
        b.style.color = on ? "#35d6e6" : "";
      });
      dirty = true;
    }
    if (ppdIn) ppdIn.addEventListener("input", function () { st.ppd = +ppdIn.value; ui(); });
    if (jitIn) jitIn.addEventListener("input", function () { st.jit = +jitIn.value; ui(); });
    if (fBtn) fBtn.addEventListener("click", function () { st.filter = (st.filter + 1) % 3; ui(); });
    if (fovBtn) fovBtn.addEventListener("click", function () {
      st.fov = (st.fov + 1) % 3; gaze.x = 0.5; gaze.y = 0.5; ui();
    });
    Array.prototype.forEach.call(presets, function (b) {
      b.addEventListener("click", function () { st.ppd = +b.dataset.ppd; ui(); });
    });
    cv.addEventListener("pointermove", function (e) {
      if (st.fov !== 2) return;
      var r = cv.getBoundingClientRect();
      gaze.x = (e.clientX - r.left) / r.width;
      gaze.y = (e.clientY - r.top) / r.height;
      dirty = true;
    });

    /* ---- 렌더 ---- */
    var img = null, buf = null, W = 0, H = 0;
    var t0 = performance.now();
    var lastInfo = "";

    function render() {
      var cw = Math.max(200, host.clientWidth || 800);
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (cv.width !== Math.round(cw * dpr) || cv.height !== Math.round(DISP_H * dpr)) {
        cv.width = Math.round(cw * dpr); cv.height = Math.round(DISP_H * dpr);
      }
      var nW = Math.max(16, Math.round(st.ppd * FOVH));
      var nH = Math.max(8, Math.round(nW * DISP_H / cw));
      if (nW !== W || nH !== H) {
        W = nW; H = nH;
        off.width = W; off.height = H;
        img = octx.createImageData(W, H);
        buf = new Float32Array(W * H);
      }
      var f = (W / 2) / Math.tan(FOVH / 2 * Math.PI / 180);   /* 픽셀 단위 초점거리 */
      var fovV = 2 * Math.atan((H / 2) / f) * 180 / Math.PI;

      /* 카메라 자세 : 지평선이 위쪽 14% 에 오도록 기울임 + 미세 진동 */
      var t = (performance.now() - t0) / 1000;
      var A = st.jit / 60 * Math.PI / 180;                       /* 각분 → 라디안 */
      var yaw = A * (0.6 * Math.sin(2 * Math.PI * 1.1 * t) + 0.4 * Math.sin(2 * Math.PI * 2.9 * t + 1.3));
      var basePitch = Math.atan((0.5 - 0.14) * H / f);
      var pitch = basePitch + A * (0.6 * Math.sin(2 * Math.PI * 0.8 * t + 0.5) + 0.4 * Math.sin(2 * Math.PI * 3.3 * t));
      var cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
      /* 카메라 축 (월드) : 전방 F, 오른쪽 R, 아래 D (화면 y 증가 방향) */
      var Fx = sy * cp, Fy = -sp, Fz = cy * cp;
      var Rx = cy, Ry = 0, Rz = -sy;
      var Dx = -sy * sp, Dy = -cp, Dz = -cy * sp;
      var camX = 0.13, camZ = 0.0;

      var gx = gaze.x * W, gy = gaze.y * H;
      var fr = Math.tan(FOVEA_DEG * Math.PI / 180) * f, fr2 = fr * fr;
      var useFov = st.fov > 0;
      var data = img.data, mode = st.filter;
      var shaded = 0;

      for (var y = 0; y < H; y++) {
        var py = y + 0.5 - H / 2;
        for (var x = 0; x < W; x++) {
          var idx = y * W + x;
          if (useFov) {
            var ddx = x - gx, ddy = y - gy;
            if (ddx * ddx + ddy * ddy > fr2) {
              var bx = x - x % BLOCK, by = y - y % BLOCK;
              if (bx !== x || by !== y) { buf[idx] = buf[by * W + bx]; continue; }
            }
          }
          shaded++;
          var px = x + 0.5 - W / 2;
          var dx = Fx * f + Rx * px + Dx * py;
          var dy = Fy * f + Ry * px + Dy * py;
          var dz = Fz * f + Rz * px + Dz * py;
          if (dy > -1e-6) {                       /* 하늘 */
            buf[idx] = -1 - Math.min(1, (y / H));
            continue;
          }
          var s = EYE / -dy;
          var wx = camX + s * dx, wz = camZ + s * dz;
          var u = wx * TPM, v = wz * TPM, g;
          if (mode === 0) {
            g = point(u, v);
          } else {
            /* dP/dx = s (R - (R.y/d.y) d)  ·  dP/dy = s (D - (D.y/d.y) d) */
            var kx = Ry / dy, ky = Dy / dy;
            var ax = s * (Rx - kx * dx) * TPM, az = s * (Rz - kx * dz) * TPM;
            var bxv = s * (Dx - ky * dx) * TPM, bzv = s * (Dz - ky * dz) * TPM;
            var la = Math.sqrt(ax * ax + az * az), lb = Math.sqrt(bxv * bxv + bzv * bzv);
            if (mode === 1) {
              g = trilinear(u, v, Math.log2(Math.max(la, lb, 1e-6)));
            } else {
              var maj = Math.max(la, lb), mn = Math.max(Math.min(la, lb), 1e-6);
              var n = Math.min(4, Math.max(1, Math.ceil(maj / mn)));
              var lod = Math.log2(Math.max(maj / n, mn));
              var mx = la >= lb ? ax : bxv, mz = la >= lb ? az : bzv;
              g = 0;
              for (var k = 0; k < n; k++) {
                var o = (k + 0.5) / n - 0.5;
                g += trilinear(u + mx * o, v + mz * o, lod);
              }
              g /= n;
            }
          }
          buf[idx] = g;
        }
      }

      /* 색 입히기 */
      for (var i = 0, j = 0; i < W * H; i++, j += 4) {
        var val = buf[i];
        if (val < 0) {                       /* 하늘 그라데이션 */
          var h = -val - 1;
          data[j] = 10 + 6 * h; data[j + 1] = 14 + 8 * h; data[j + 2] = 26 + 12 * h;
        } else {
          data[j] = 18 + val * 182; data[j + 1] = 22 + val * 192; data[j + 2] = 30 + val * 200;
        }
        data[j + 3] = 255;
      }
      octx.putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(off, 0, 0, cv.width, cv.height);

      /* ---- 오버레이 ---- */
      var sx = cv.width / W, syy = cv.height / H;
      /* 깊이 방향 나이퀴스트 한계 거리 : 한 주기(1 m) 의 세로 각크기 ≈ H·cycle/d² */
      var dN = Math.sqrt(EYE * CYCLE * st.ppd * (180 / Math.PI) / 2);
      var ang = Math.atan(EYE / dN) - basePitch;            /* 화면 중심 기준 아래쪽 각 */
      var yN = (H / 2 + f * Math.tan(ang)) * syy;
      ctx.save();
      ctx.font = Math.round(13 * dpr) + "px Pretendard, 'Malgun Gothic', sans-serif";
      if (yN > 0 && yN < cv.height) {
        ctx.strokeStyle = "#ff5fa2"; ctx.lineWidth = 2 * dpr;
        ctx.setLineDash([8 * dpr, 6 * dpr]);
        ctx.beginPath(); ctx.moveTo(0, yN); ctx.lineTo(cv.width, yN); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = "rgba(11,13,18,.82)";
        var lab = "나이퀴스트 한계 ≈ " + dN.toFixed(0) + " m · 이 선 위쪽(더 먼 바닥) = 칸 한 주기 < 2 픽셀";
        var tw = ctx.measureText(lab).width;
        ctx.fillRect(cv.width - tw - 18 * dpr, yN + 5 * dpr, tw + 12 * dpr, 20 * dpr);
        ctx.fillStyle = "#ff5fa2";
        ctx.fillText(lab, cv.width - tw - 12 * dpr, yN + 20 * dpr);
      }
      if (useFov) {
        ctx.strokeStyle = "#ffc44d"; ctx.lineWidth = 2 * dpr;
        ctx.beginPath();
        ctx.ellipse(gx * sx, gy * syy, fr * sx, fr * syy, 0, 0, Math.PI * 2);
        ctx.stroke();
      }
      ctx.restore();

      var total = W * H;
      var info = "PPD " + st.ppd + " · 내부 해상도 " + W + "×" + H +
        " · 필터 : " + FILTERS[st.filter] + " · 머리 진동 " + st.jit + "′" +
        " · 나이퀴스트 한계 약 " + dN.toFixed(0) + " m";
      if (useFov) {
        info += " · 셰이딩 " + total.toLocaleString() + " → " + shaded.toLocaleString() +
          " (" + Math.round((1 - shaded / total) * 100) + "% 절감, 원 밖 3×3 블록)";
      }
      if (out && info !== lastInfo) { out.textContent = info; lastInfo = info; }
      dirty = false;
    }

    ui();
    return {
      draw: function () {
        /* 진동이 없으면 바뀐 게 있을 때만 다시 그림 */
        if (st.jit > 0 || dirty) render();
      }
    };
  };

  /* ============================================================
     2) UV 펼치기 — 정육면체 ↔ 십자 전개도
     ============================================================ */
  window.CGDemos["uv-unwrap"] = function (host) {
    var S = window.CGStage;
    var st = S.make(host, {
      dist: 10.5, phi: 1.2, theta: 0.55, height: 340, fov: 42,
      grid: false, lights: false, clear: 0x080a0f
    });
    if (!st) return null;

    /* ---- 전개도 텍스처 (4 × 3 칸, 512 × 384) ---- */
    var FACES = [
      /* 이름, 칸(col,row; row 0 = 위), 색, 꼭짓점 4개 (u0v0, u1v0, u1v1, u0v1) */
      { n: "앞 +Z", c: 1, r: 1, col: "#35d6e6", p: [[-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]] },
      { n: "오른 +X", c: 2, r: 1, col: "#a8e05f", p: [[1, -1, 1], [1, -1, -1], [1, 1, -1], [1, 1, 1]] },
      { n: "뒤 −Z", c: 3, r: 1, col: "#ffc44d", p: [[1, -1, -1], [-1, -1, -1], [-1, 1, -1], [1, 1, -1]] },
      { n: "왼 −X", c: 0, r: 1, col: "#ff5fa2", p: [[-1, -1, -1], [-1, -1, 1], [-1, 1, 1], [-1, 1, -1]] },
      { n: "위 +Y", c: 1, r: 0, col: "#7aa2ff", p: [[-1, 1, 1], [1, 1, 1], [1, 1, -1], [-1, 1, -1]] },
      { n: "아래 −Y", c: 1, r: 2, col: "#c49bff", p: [[-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1]] }
    ];
    var TW = 512, TH = 384, CELL = 128;
    var tc = document.createElement("canvas");
    tc.width = TW; tc.height = TH;
    var g = tc.getContext("2d");
    g.fillStyle = "#151922"; g.fillRect(0, 0, TW, TH);
    g.strokeStyle = "#232a38"; g.lineWidth = 1;
    for (var gx = 0; gx <= TW; gx += 16) { g.beginPath(); g.moveTo(gx, 0); g.lineTo(gx, TH); g.stroke(); }
    for (var gy = 0; gy <= TH; gy += 16) { g.beginPath(); g.moveTo(0, gy); g.lineTo(TW, gy); g.stroke(); }
    g.fillStyle = "#5f6980"; g.font = "15px Pretendard, 'Malgun Gothic', sans-serif";
    g.fillText("빈 공간", 18, 30); g.fillText("(메모리 낭비)", 18, 50);
    FACES.forEach(function (fc) {
      var x0 = fc.c * CELL, y0 = fc.r * CELL;
      g.fillStyle = fc.col; g.globalAlpha = 0.22; g.fillRect(x0, y0, CELL, CELL);
      g.globalAlpha = 1;
      g.strokeStyle = fc.col; g.lineWidth = 2;
      for (var k = 1; k < 4; k++) {
        g.beginPath(); g.moveTo(x0 + k * 32, y0); g.lineTo(x0 + k * 32, y0 + CELL); g.stroke();
        g.beginPath(); g.moveTo(x0, y0 + k * 32); g.lineTo(x0 + CELL, y0 + k * 32); g.stroke();
      }
      g.lineWidth = 4; g.strokeRect(x0 + 2, y0 + 2, CELL - 4, CELL - 4);
      g.fillStyle = "#e8ecf4"; g.font = "bold 22px Pretendard, 'Malgun Gothic', sans-serif";
      g.textAlign = "center"; g.fillText(fc.n, x0 + CELL / 2, y0 + 74);
      /* 위쪽 화살표 : 방향 확인용 */
      g.beginPath(); g.moveTo(x0 + 64, y0 + 14); g.lineTo(x0 + 54, y0 + 30); g.lineTo(x0 + 74, y0 + 30);
      g.closePath(); g.fill();
      g.textAlign = "left";
    });
    var tex = new THREE.CanvasTexture(tc);

    /* ---- 지오메트리 : 면마다 독립 꼭짓점 4개 (총 24) ---- */
    var pos3 = [], posF = [], uvs = [], idx = [];
    FACES.forEach(function (fc, fi) {
      var u0 = fc.c / 4, u1 = (fc.c + 1) / 4;
      var v1 = 1 - fc.r / 3, v0 = 1 - (fc.r + 1) / 3;
      var uv = [[u0, v0], [u1, v0], [u1, v1], [u0, v1]];
      fc.uv = uv;
      for (var k = 0; k < 4; k++) {
        pos3.push(fc.p[k]);
        posF.push([(uv[k][0] - 0.5) * 8, (uv[k][1] - 0.5) * 6, 0]);
        uvs.push(uv[k][0], uv[k][1]);
      }
      var b = fi * 4;
      idx.push(b, b + 1, b + 2, b, b + 2, b + 3);
    });
    var geo = new THREE.BufferGeometry();
    var posArr = new Float32Array(24 * 3);
    geo.setAttribute("position", new THREE.BufferAttribute(posArr, 3));
    geo.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
    geo.setIndex(idx);
    var mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide }));
    st.scene.add(mesh);

    /* ---- 모서리 : seam 판정 ---- */
    function key3(p) { return p.join(","); }
    var edges = [];   /* {a,b (꼭짓점 번호), seam} */
    FACES.forEach(function (fc, fi) {
      for (var k = 0; k < 4; k++) edges.push({ a: fi * 4 + k, b: fi * 4 + (k + 1) % 4, f: fi });
    });
    edges.forEach(function (e) {
      var A = key3(pos3[e.a]), B = key3(pos3[e.b]);
      var twin = edges.filter(function (o) {
        return o !== e && ((key3(pos3[o.a]) === A && key3(pos3[o.b]) === B) ||
                           (key3(pos3[o.a]) === B && key3(pos3[o.b]) === A));
      })[0];
      var ua = posF[e.a], ub = posF[e.b];
      var ta = key3(pos3[twin.a]) === A ? posF[twin.a] : posF[twin.b];
      var tb = key3(pos3[twin.a]) === A ? posF[twin.b] : posF[twin.a];
      var same = Math.abs(ua[0] - ta[0]) + Math.abs(ua[1] - ta[1]) +
                 Math.abs(ub[0] - tb[0]) + Math.abs(ub[1] - tb[1]) < 1e-6;
      e.seam = !same;
    });
    var nSeam = edges.filter(function (e) { return e.seam; }).length / 2;
    var nJoin = 12 - nSeam;

    var lineArr = new Float32Array(edges.length * 2 * 3);
    var colArr = new Float32Array(edges.length * 2 * 3);
    var lgeo = new THREE.BufferGeometry();
    lgeo.setAttribute("position", new THREE.BufferAttribute(lineArr, 3));
    lgeo.setAttribute("color", new THREE.BufferAttribute(colArr, 3));
    var lines = new THREE.LineSegments(lgeo, new THREE.LineBasicMaterial({
      vertexColors: true, depthTest: false, transparent: true }));
    lines.renderOrder = 5;
    st.scene.add(lines);

    var showSeam = true;
    var cRed = new THREE.Color(0xff5a4d), cDim = new THREE.Color(0x9aa4b8);
    function paintEdges() {
      edges.forEach(function (e, i) {
        var c = (e.seam && showSeam) ? cRed : cDim;
        for (var k = 0; k < 2; k++) {
          colArr[(i * 2 + k) * 3] = c.r; colArr[(i * 2 + k) * 3 + 1] = c.g; colArr[(i * 2 + k) * 3 + 2] = c.b;
        }
      });
      lgeo.attributes.color.needsUpdate = true;
    }

    /* ---- 컨트롤 ---- */
    var T = 0, target = 0, playing = false, dir = 1;
    var tIn = S.el(host, '[data-k="t"]'), tV = S.el(host, '[data-v="t"]');
    var playBtn = S.el(host, "[data-play]"), seamBtn = S.el(host, "[data-seam]");
    var out = S.el(host, "[data-out]");
    if (tIn) tIn.addEventListener("input", function () {
      playing = false; target = +tIn.value / 100; label();
    });
    if (playBtn) playBtn.addEventListener("click", function () {
      playing = !playing; label();
    });
    if (seamBtn) seamBtn.addEventListener("click", function () {
      showSeam = !showSeam; paintEdges(); label();
    });
    function label() {
      if (playBtn) playBtn.textContent = playing ? "정지" : "자동 재생";
      if (seamBtn) seamBtn.textContent = showSeam ? "seam 강조 끔" : "seam 강조 켬";
    }

    function ease(x) { return x * x * (3 - 2 * x); }
    function update() {
      var e = ease(T);
      for (var i = 0; i < 24; i++) {
        for (var a = 0; a < 3; a++) posArr[i * 3 + a] = pos3[i][a] * (1 - e) + posF[i][a] * e;
      }
      geo.attributes.position.needsUpdate = true;
      geo.computeBoundingSphere();
      /* 접힌 상자는 가까이, 펼친 전개도는 멀리서 보이도록 카메라 거리 조절 */
      st.orbit.r = 5.6 + (10.5 - 5.6) * e;
      st.place();
      edges.forEach(function (ed, i) {
        [ed.a, ed.b].forEach(function (vi, k) {
          for (var a = 0; a < 3; a++) lineArr[(i * 2 + k) * 3 + a] = posArr[vi * 3 + a];
        });
      });
      lgeo.attributes.position.needsUpdate = true;
      lgeo.computeBoundingSphere();
      if (tV) tV.textContent = Math.round(T * 100) + "%";
      if (tIn && playing) tIn.value = Math.round(T * 100);
      if (out) out.textContent = "펼침 " + Math.round(T * 100) + "% · 모서리 12개 = 이어진 모서리 " +
        nJoin + "개 + seam " + nSeam + "개 (빨간 선 — 전개도에서 두 줄로 갈라짐) · 정점 8개 → UV 때문에 24개로 분리";
    }

    paintEdges(); label(); update();
    var baseDraw = st.draw;
    st.draw = function () {
      var dt = st.tick();
      if (playing) {
        T += dir * dt * 0.35;
        if (T >= 1) { T = 1; dir = -1; }
        if (T <= 0) { T = 0; dir = 1; }
      } else {
        T += (target - T) * Math.min(1, dt * 8);
      }
      update();
      baseDraw();
    };
    return st;
  };
})();
