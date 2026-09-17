/* ============================================================
   4주차 데모 — 카메라 절두체 · 깊이 버퍼 정밀도(z-fighting)
   _stage.js 를 먼저 로드할 것
   ============================================================ */
(function () {
  "use strict";
  var S = window.CGStage;
  var C = S.C;
  window.CGDemos = window.CGDemos || {};

  /* 천 단위 구분 */
  function comma(n) {
    return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
  /* 선분 전용 버퍼 */
  function segGeo(count) {
    var g = new THREE.BufferGeometry();
    g.setAttribute("position",
      new THREE.BufferAttribute(new Float32Array(count * 6), 3));
    return g;
  }

  /* ============================================================
     A. 절두체 — 카메라가 보는 상자
     FOV / near / far 를 직접 잡아 본다. 상자 밖은 그릴 이유가 없다.
     ============================================================ */
  window.CGDemos["frustum"] = function (host) {
    var CAM_FOV = 40;                 /* 관전 카메라 화각 */
    var ASP = 16 / 9;                 /* 조작 대상 카메라의 화면비 */

    var st = S.make(host, {
      dist: 62, phi: 1.05, theta: 1.25, height: 340, fov: CAM_FOV,
      gridSize: 120, gridDiv: 24, gridY: -12
    });
    if (!st) return null;

    /* ---- 조작 대상 카메라 (수학용) ---------------------------- */
    var sub = new THREE.PerspectiveCamera(60, ASP, 1, 30);
    var frustum = new THREE.Frustum();
    var pv = new THREE.Matrix4();

    /* 카메라 본체 표시 — 원점에서 -Z 를 본다 */
    var body = new THREE.Mesh(
      new THREE.BoxGeometry(1.5, 1.1, 1.9),
      new THREE.MeshLambertMaterial({ color: C.fg }));
    st.scene.add(body);

    /* ---- 절두체 와이어 ---------------------------------------- */
    var wire = new THREE.LineSegments(segGeo(12),
      new THREE.LineBasicMaterial({ color: C.gfx, depthTest: false }));
    wire.renderOrder = 5;
    st.scene.add(wire);

    var apex = new THREE.LineSegments(segGeo(4),
      new THREE.LineBasicMaterial({
        color: C.gfx, transparent: true, opacity: 0.34, depthTest: false }));
    apex.renderOrder = 5;
    st.scene.add(apex);

    function plane(color, op) {
      var m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1),
        new THREE.MeshBasicMaterial({
          color: color, transparent: true, opacity: op,
          side: THREE.DoubleSide, depthWrite: false }));
      m.renderOrder = 2;
      st.scene.add(m);
      return m;
    }
    var nearQ = plane(C.warn, 0.22);   /* near 평면 — 이 앞은 잘려 나간다 */
    var farQ = plane(C.gfx, 0.07);     /* far 평면 — 이 뒤도 잘려 나간다 */

    /* ---- 흩어 놓은 물체 --------------------------------------- */
    var PAL = [C.gfx, C.lab, C.vr, C.warn];
    var objs = [];
    (function () {
      var seed = 20240404;
      function rnd() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
      for (var i = 0; i < 20; i++) {
        var size = 1.3 + rnd() * 1.4;
        var color = PAL[i % PAL.length];
        var geo = (i % 3 === 0)
          ? new THREE.IcosahedronGeometry(size * 0.66, 0)
          : new THREE.BoxGeometry(size, size, size);
        var mat = new THREE.MeshLambertMaterial({
          color: color, transparent: true, opacity: 1 });
        var mesh = new THREE.Mesh(geo, mat);
        var emat = new THREE.LineBasicMaterial({
          color: 0xffffff, transparent: true, opacity: 0.35 });
        var edge = new THREE.LineSegments(new THREE.EdgesGeometry(geo), emat);
        var g = new THREE.Group();
        g.add(mesh); g.add(edge);
        g.position.set((rnd() * 2 - 1) * 15, (rnd() * 2 - 1) * 7, 4 - rnd() * 50);
        g.userData = { mat: mat, emat: emat, base: color, spin: 0.15 + rnd() * 0.35 };
        st.scene.add(g);
        objs.push(g);
      }
    })();

    /* ---- 컨트롤 ------------------------------------------------ */
    var fovS = S.el(host, "[data-fov]"), fovV = S.el(host, "[data-fov-v]");
    var nearS = S.el(host, "[data-near]"), nearV = S.el(host, "[data-near-v]");
    var farS = S.el(host, "[data-far]"), farV = S.el(host, "[data-far-v]");
    var out = S.el(host, "[data-out]");

    /* ---- 와이어 갱신 ------------------------------------------- */
    var wa = wire.geometry.attributes.position.array;
    var aa = apex.geometry.attributes.position.array;
    var wi = 0, ai = 0;
    function put(arr, i, p) { arr[i] = p[0]; arr[i + 1] = p[1]; arr[i + 2] = p[2]; return i + 3; }
    function wseg(a, b) { wi = put(wa, wi, a); wi = put(wa, wi, b); }
    function aseg(a, b) { ai = put(aa, ai, a); ai = put(aa, ai, b); }
    function rect(hw, hh, z) {
      return [[-hw, -hh, z], [hw, -hh, z], [hw, hh, z], [-hw, hh, z]];
    }

    var tgtZ = -25, tgtR = 62;

    var baseDraw = st.draw;
    st.draw = function () {
      var dt = st.tick();

      var fov = +fovS.value;
      var far = +farS.value;
      var near = Math.min(+nearS.value, far - 0.5);

      fovV.textContent = fov + "°";
      nearV.textContent = near.toFixed(2);
      farV.textContent = far.toFixed(1);

      /* 절두체 판정 — 진짜 투영 행렬로 자른다 */
      sub.fov = fov; sub.aspect = ASP; sub.near = near; sub.far = far;
      sub.updateProjectionMatrix();
      sub.updateMatrixWorld();
      pv.multiplyMatrices(sub.projectionMatrix, sub.matrixWorldInverse);
      frustum.setFromProjectionMatrix(pv);

      var inCount = 0;
      for (var i = 0; i < objs.length; i++) {
        var o = objs[i], u = o.userData;
        o.rotation.y += u.spin * dt;
        o.rotation.x += u.spin * dt * 0.4;
        var hit = frustum.containsPoint(o.position);
        if (hit) inCount++;
        u.mat.color.setHex(hit ? u.base : C.dim);
        u.mat.opacity = hit ? 1 : 0.26;
        u.emat.opacity = hit ? 0.35 : 0.1;
      }

      /* 와이어프레임 */
      var t = Math.tan(fov * Math.PI / 360);
      var hN = t * near, wN = hN * ASP;
      var hF = t * far, wF = hF * ASP;
      var n4 = rect(wN, hN, -near), f4 = rect(wF, hF, -far);
      wi = 0; ai = 0;
      for (var k = 0; k < 4; k++) {
        wseg(n4[k], n4[(k + 1) % 4]);
        wseg(f4[k], f4[(k + 1) % 4]);
        wseg(n4[k], f4[k]);
        aseg([0, 0, 0], n4[k]);
      }
      wire.geometry.attributes.position.needsUpdate = true;
      apex.geometry.attributes.position.needsUpdate = true;

      nearQ.position.z = -near; nearQ.scale.set(wN * 2, hN * 2, 1);
      farQ.position.z = -far; farQ.scale.set(wF * 2, hF * 2, 1);

      /* 절두체 전체가 화면에 들어오도록 관전 거리를 맞춘다 */
      var tanC = Math.tan(CAM_FOV * Math.PI / 360);
      var span = Math.max(far, 50);
      var vNeed = Math.max(hF, wF / st.cam.aspect, 9) * 1.2;
      var hNeed = span * 0.58;
      var want = Math.max(vNeed / tanC, hNeed / (tanC * st.cam.aspect), 24);
      tgtR += (want - tgtR) * 0.12;
      tgtZ += (-span / 2 - tgtZ) * 0.12;
      st.orbit.r = tgtR;
      st.orbit.target.z = tgtZ;
      st.place();

      var ratio = far / near;
      out.innerHTML =
        '<b class="gfx-txt">절두체 안</b> ' + inCount + " / " + objs.length +
        '　<b class="gfx-txt">far / near</b> ' + comma(ratio) + " : 1" +
        (ratio > 200
          ? '　<span class="trap-txt">깊이 정밀도 위험 비율</span>'
          : '　<span class="muted">절두체 밖의 물체는 렌더링 제외</span>');

      baseDraw();
    };

    return st;
  };

  /* ============================================================
     B. AI 함정 #3 — near=0.01, far=5000  ★
     깊이 버퍼는 near 근처에 정밀도를 몰아 쓴다.
     near 를 낮추면 먼 곳의 두 면이 같은 깊이로 뭉개진다.
     ============================================================ */
  window.CGDemos["zfighting"] = function (host) {
    var st = S.make(host, {
      dist: 50, phi: 1.46, theta: 0, height: 340, fov: 32,
      grid: false, lights: false, orbit: false
    });
    if (!st) return null;

    var GAP = 0.002;     /* 두 면의 간격(m) */
    var BITS = 24;       /* 깊이 버퍼 비트 수 */
    var LEVELS = Math.pow(2, BITS) - 1;

    /* 한 쌍 = 바닥판(청록) + 그 위 0.002m 에 붙인 스티커(분홍) */
    function pair(bw, bh, sw, sh) {
      var g = new THREE.Group();
      var base = new THREE.Mesh(new THREE.PlaneGeometry(bw, bh),
        new THREE.MeshBasicMaterial({ color: C.gfx, side: THREE.DoubleSide }));
      var deca = new THREE.Mesh(new THREE.PlaneGeometry(sw, sh),
        new THREE.MeshBasicMaterial({ color: C.vr, side: THREE.DoubleSide }));
      deca.position.z = GAP;
      g.add(base); g.add(deca);
      return g;
    }

    /* 멀리 있는 쌍 — 카메라에서 약 50m */
    var far = pair(34, 20, 17, 10);
    far.rotation.set(-0.30, 0, 0);
    st.scene.add(far);

    /* 가까이 있는 쌍 — 같은 간격인데도 멀쩡하다. 정밀도는 거리 제곱에 달렸다. */
    var nearPair = pair(3.4, 2.0, 1.7, 1.0);
    nearPair.position.set(-7.2, -4.6, 38);
    nearPair.rotation.set(-0.30, 0.14, 0);
    st.scene.add(nearPair);

    var nearS = S.el(host, "[data-near]"), nearV = S.el(host, "[data-near-v]");
    var farS = S.el(host, "[data-far]"), farV = S.el(host, "[data-far-v]");
    var out = S.el(host, "[data-out]");
    var fix = S.el(host, "[data-fix]");
    var alert = host.querySelector(".demo-alert");

    if (fix) {
      fix.addEventListener("click", function () {
        nearS.value = "0.3";
        nearS.dispatchEvent(new Event("input", { bubbles: true }));
      });
    }

    var t = 0;
    var baseDraw = st.draw;
    st.draw = function () {
      t += st.tick();

      var n = +nearS.value, f = +farS.value;
      nearV.textContent = n.toFixed(2);
      farV.textContent = comma(f);

      /* 실제 near/far 를 카메라에 적용 — 정밀도 붕괴를 그대로 재현 */
      st.cam.near = n;
      st.cam.far = f;
      st.cam.updateProjectionMatrix();

      /* 아주 느린 시점 이동 + 미세 회전 — 깜빡임이 살아 움직인다 */
      st.orbit.theta = Math.sin(t * 0.22) * 0.26;
      st.place();
      far.rotation.y = Math.sin(t * 0.55) * 0.035;

      /* 이 거리에서 깊이 버퍼가 구분할 수 있는 최소 간격
         z_w = (1/n - 1/z) / (1/n - 1/f)  →  Δz = z² (1/n - 1/f) / (2^b - 1) */
      var d = st.cam.position.distanceTo(far.position);
      var res = d * d * (1 / n - 1 / f) / LEVELS;

      var q = res / GAP;
      var verdict;
      if (q < 0.5) { verdict = "깨끗함"; }
      else if (q < 2) { verdict = "깜빡임"; }
      else { verdict = "심각"; }
      var color = q < 0.5 ? "#a8e05f" : (q < 2 ? "#ffc44d" : "#ff5a4d");

      out.innerHTML =
        '<b class="gfx-txt">far / near</b> ' + comma(f / n) + " : 1" +
        '　<b class="gfx-txt">' + d.toFixed(0) + "m 에서 구분 가능한 최소 간격</b> ≈ " +
        (res * 1000).toFixed(res * 1000 < 10 ? 2 : 1) + " mm" +
        '　<span class="muted">두 면 간격 ' + (GAP * 1000).toFixed(1) + " mm</span>" +
        '　<b style="color:' + color + '">' + verdict + "</b>";

      if (alert) {
        alert.textContent = "z-fighting " + verdict;
        alert.classList.toggle("on", q >= 2);
      }

      baseDraw();
    };

    return st;
  };
})();
