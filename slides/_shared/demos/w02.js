/* ============================================================
   2주차 데모 — 벡터 · 변환 순서 · 짐벌락
   three.js r128 (UMD, 전역 THREE) 필요
   각 데모는 window.CGDemos 에 등록되고 deck.js 가 슬라이드
   진입 시점에 lazy init + 보이는 것만 렌더한다.
   ============================================================ */
(function () {
  "use strict";

  var C = {
    gfx: 0x35d6e6, vr: 0xff5fa2, trap: 0xff5a4d, lab: 0xa8e05f,
    warn: 0xffc44d, dim: 0x5f6980, grid: 0x232a38, gridC: 0x323b4d,
    x: 0xff5a4d, y: 0xa8e05f, z: 0x4d9cff
  };

  window.CGDemos = window.CGDemos || {};

  /* ---------- 공통 무대 ---------- */
  function makeStage(host, opt) {
    opt = opt || {};
    if (typeof THREE === "undefined") {
      host.innerHTML =
        '<div style="padding:2em;color:#5f6980;font-family:monospace;font-size:.5em">' +
        "three.js 로드 실패 · 인터넷 연결 확인 필요</div>";
      return null;
    }
    var h = opt.height || 330;
    var w = host.clientWidth || 800;

    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(w, h, false);
    renderer.setClearColor(0x06070a, 1);
    renderer.domElement.style.height = h + "px";
    host.insertBefore(renderer.domElement, host.firstChild);

    var scene = new THREE.Scene();
    var cam = new THREE.PerspectiveCamera(42, w / h, 0.1, 200);

    var orbit = {
      theta: opt.theta != null ? opt.theta : 0.72,
      phi: opt.phi != null ? opt.phi : 1.05,
      r: opt.dist || 11,
      target: new THREE.Vector3(0, opt.ty || 0, 0)
    };
    function place() {
      cam.position.set(
        orbit.target.x + orbit.r * Math.sin(orbit.phi) * Math.sin(orbit.theta),
        orbit.target.y + orbit.r * Math.cos(orbit.phi),
        orbit.target.z + orbit.r * Math.sin(orbit.phi) * Math.cos(orbit.theta)
      );
      cam.lookAt(orbit.target);
    }
    place();

    /* 드래그 회전 */
    var dragging = false, px = 0, py = 0;
    var cv = renderer.domElement;
    cv.style.cursor = "grab";
    cv.addEventListener("pointerdown", function (e) {
      dragging = true; px = e.clientX; py = e.clientY;
      cv.style.cursor = "grabbing"; cv.setPointerCapture(e.pointerId);
    });
    cv.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      orbit.theta -= (e.clientX - px) * 0.008;
      orbit.phi = Math.max(0.18, Math.min(Math.PI - 0.18, orbit.phi - (e.clientY - py) * 0.008));
      px = e.clientX; py = e.clientY; place();
    });
    cv.addEventListener("pointerup", function (e) {
      dragging = false; cv.style.cursor = "grab";
      try { cv.releasePointerCapture(e.pointerId); } catch (_) {}
    });

    /* 리사이즈 */
    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        var nw = host.clientWidth;
        if (!nw || nw === w) return;
        w = nw; cam.aspect = w / h; cam.updateProjectionMatrix();
        renderer.setSize(w, h, false);
      }).observe(host);
    }

    if (opt.grid !== false) {
      var g = new THREE.GridHelper(opt.gridSize || 10, opt.gridSize || 10, C.gridC, C.grid);
      g.position.y = opt.gridY || 0;
      scene.add(g);
    }
    if (opt.lights !== false) {
      scene.add(new THREE.AmbientLight(0xffffff, 0.62));
      var d1 = new THREE.DirectionalLight(0xffffff, 0.85); d1.position.set(4, 7, 5); scene.add(d1);
      var d2 = new THREE.DirectionalLight(0x4d9cff, 0.3); d2.position.set(-5, 2, -4); scene.add(d2);
    }

    return {
      scene: scene, cam: cam, renderer: renderer, orbit: orbit, place: place,
      draw: function () { renderer.render(scene, cam); }
    };
  }

  function arrow(dir, len, color, headL) {
    return new THREE.ArrowHelper(
      dir.clone().normalize(), new THREE.Vector3(0, 0, 0), len, color,
      headL || 0.42, (headL || 0.42) * 0.6
    );
  }
  function ring(radius, tube, color, seg) {
    return new THREE.Mesh(
      new THREE.TorusGeometry(radius, tube, 10, seg || 72),
      new THREE.MeshBasicMaterial({ color: color })
    );
  }
  function el(host, sel) { return host.parentNode.querySelector(sel); }
  function deg(r) { return r * 180 / Math.PI; }
  function rad(d) { return d * Math.PI / 180; }

  /* ============================================================
     A. 내적과 외적 — "적이 내 시야 안에 있는가"
     ============================================================ */
  window.CGDemos["dot-cross"] = function (host) {
    var st = makeStage(host, { dist: 9.5, phi: 1.0, theta: 0.9, gridSize: 8 });
    if (!st) return null;

    var A_LEN = 3.0, B_LEN = 3.0, FOV_HALF = 30;

    var aArrow = arrow(new THREE.Vector3(0, 0, 1), A_LEN, C.gfx);
    var bArrow = arrow(new THREE.Vector3(1, 0, 0), B_LEN, C.vr);
    var cArrow = arrow(new THREE.Vector3(0, 1, 0), 2.2, C.warn);
    st.scene.add(aArrow, bArrow, cArrow);

    /* 시야 원뿔 */
    var coneH = A_LEN;
    var cone = new THREE.Mesh(
      new THREE.ConeGeometry(coneH * Math.tan(rad(FOV_HALF)), coneH, 40, 1, true),
      new THREE.MeshBasicMaterial({ color: C.gfx, transparent: true, opacity: 0.11, side: THREE.DoubleSide })
    );
    cone.rotation.x = Math.PI / 2;
    cone.position.z = coneH / 2;
    st.scene.add(cone);

    /* 사잇각 호 */
    var arcMat = new THREE.LineBasicMaterial({ color: C.dim });
    var arc = new THREE.Line(new THREE.BufferGeometry(), arcMat);
    st.scene.add(arc);

    var az = el(host, "[data-az]"), elv = el(host, "[data-el]");
    var out = el(host, "[data-out]");

    function update() {
      var t = rad(+az.value), p = rad(+elv.value);
      var b = new THREE.Vector3(
        Math.cos(p) * Math.sin(t), Math.sin(p), Math.cos(p) * Math.cos(t)
      );
      var a = new THREE.Vector3(0, 0, 1);
      bArrow.setDirection(b);

      var dot = a.dot(b);
      var cross = new THREE.Vector3().crossVectors(a, b);
      var crossLen = cross.length();
      var ang = deg(Math.acos(Math.max(-1, Math.min(1, dot))));

      if (crossLen > 1e-4) {
        cArrow.visible = true;
        cArrow.setDirection(cross.clone().normalize());
        cArrow.setLength(0.6 + crossLen * 1.9, 0.36, 0.22);
      } else { cArrow.visible = false; }

      /* 호 갱신 */
      var pts = [], N = 40;
      for (var i = 0; i <= N; i++) {
        var v = new THREE.Vector3().copy(a).lerp(b, i / N);
        if (v.length() < 1e-5) v.set(0, 0, 1);
        pts.push(v.normalize().multiplyScalar(1.5));
      }
      arc.geometry.dispose();
      arc.geometry = new THREE.BufferGeometry().setFromPoints(pts);

      var inFov = ang <= FOV_HALF;
      cone.material.color.setHex(inFov ? C.lab : C.gfx);
      cone.material.opacity = inFov ? 0.2 : 0.1;

      out.innerHTML =
        '<b class="gfx-txt">a·b</b> = ' + dot.toFixed(3) +
        '　<b class="muted">각</b> = ' + ang.toFixed(1) + "°" +
        '　<b style="color:#ffc44d">|a×b|</b> = ' + crossLen.toFixed(3) +
        '　→ <b style="color:' + (inFov ? "#a8e05f" : "#5f6980") + '">' +
        (inFov ? "시야 안 (a·b > cos30° = 0.866)" : "시야 밖") + "</b>";
    }
    az.addEventListener("input", update);
    elv.addEventListener("input", update);
    update();
    return st;
  };

  /* ============================================================
     B. 변환 순서 — R·T  vs  T·R
     ============================================================ */
  window.CGDemos["transform-order"] = function (host) {
    var st = makeStage(host, { dist: 13, phi: 0.92, theta: 0.72, gridSize: 12 });
    if (!st) return null;

    function box(color) {
      var g = new THREE.Group();
      var m = new THREE.Mesh(
        new THREE.BoxGeometry(1.1, 1.1, 1.1),
        new THREE.MeshLambertMaterial({ color: color })
      );
      var e = new THREE.LineSegments(
        new THREE.EdgesGeometry(new THREE.BoxGeometry(1.1, 1.1, 1.1)),
        new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.45 })
      );
      g.add(m, e);
      var ax = new THREE.AxesHelper(1.5);
      ax.material.depthTest = false;
      g.add(ax);
      return g;
    }
    /* 원점 표시 */
    var originDot = new THREE.Mesh(
      new THREE.SphereGeometry(0.16, 16, 12),
      new THREE.MeshBasicMaterial({ color: 0xffffff })
    );
    st.scene.add(originDot);

    var cubeRT = box(C.gfx);   /* R·T : 이동 먼저 → 원점 기준 회전 */
    var cubeTR = box(C.vr);    /* T·R : 회전 먼저 → 그 다음 이동 */
    st.scene.add(cubeRT, cubeTR);

    /* R·T 궤적 */
    var trail = new THREE.Line(
      new THREE.BufferGeometry(),
      new THREE.LineDashedMaterial({ color: C.gfx, dashSize: 0.24, gapSize: 0.18 })
    );
    st.scene.add(trail);

    var dS = el(host, "[data-d]"), thS = el(host, "[data-th]");
    var out = el(host, "[data-out]");

    function update() {
      var d = +dS.value, th = rad(+thS.value);

      /* 두 변환을 행렬로 직접 구성 — 슬라이드의 수식과 1:1 대응 */
      var T = new THREE.Matrix4().makeTranslation(d, 0, 0);
      var R = new THREE.Matrix4().makeRotationY(th);

      var M1 = new THREE.Matrix4().multiplyMatrices(R, T); /* R·T */
      var M2 = new THREE.Matrix4().multiplyMatrices(T, R); /* T·R */

      cubeRT.matrixAutoUpdate = false; cubeRT.matrix.copy(M1);
      cubeTR.matrixAutoUpdate = false; cubeTR.matrix.copy(M2);

      var pts = [], N = 48;
      for (var i = 0; i <= N; i++) {
        var t = th * i / N;
        pts.push(new THREE.Vector3(d * Math.cos(t), 0, -d * Math.sin(t)));
      }
      trail.geometry.dispose();
      trail.geometry = new THREE.BufferGeometry().setFromPoints(pts);
      trail.computeLineDistances();

      var p1 = new THREE.Vector3().setFromMatrixPosition(M1);
      var p2 = new THREE.Vector3().setFromMatrixPosition(M2);
      var gap = p1.distanceTo(p2);

      out.innerHTML =
        '<b class="gfx-txt">R·T</b> (이동→회전) = (' +
        p1.x.toFixed(2) + ", " + p1.y.toFixed(2) + ", " + p1.z.toFixed(2) + ")" +
        '　<b class="vr-txt">T·R</b> (회전→이동) = (' +
        p2.x.toFixed(2) + ", " + p2.y.toFixed(2) + ", " + p2.z.toFixed(2) + ")" +
        '　<b style="color:' + (gap > 0.02 ? "#ff5a4d" : "#5f6980") + '">차이 ' +
        gap.toFixed(2) + "</b>";
    }
    dS.addEventListener("input", update);
    thS.addEventListener("input", update);
    update();
    return st;
  };

  /* ============================================================
     C. 짐벌락 ★
     ============================================================ */
  window.CGDemos["gimbal"] = function (host) {
    var st = makeStage(host, { dist: 10.5, phi: 1.05, theta: 0.85, grid: false, height: 360 });
    if (!st) return null;

    /* Unity 의 오일러 적용 순서는 Z→X→Y (외부축 기준).
       짐벌 하드웨어로 보면 바깥 링부터 Y → X → Z 로 중첩된다. */
    var yawG = new THREE.Group();    /* 바깥 : Y축 */
    var pitchG = new THREE.Group();  /* 중간 : X축 */
    var rollG = new THREE.Group();   /* 안쪽 : Z축 */
    st.scene.add(yawG); yawG.add(pitchG); pitchG.add(rollG);

    var rY = ring(3.5, 0.055, C.y); rY.rotation.x = Math.PI / 2; yawG.add(rY);
    var rX = ring(2.9, 0.055, C.x); rX.rotation.y = Math.PI / 2; pitchG.add(rX);
    var rZ = ring(2.3, 0.055, C.z); rollG.add(rZ);

    /* 각 링의 회전축 표시 */
    var axY = arrow(new THREE.Vector3(0, 1, 0), 4.6, C.y, 0.3); yawG.add(axY);
    var axX = arrow(new THREE.Vector3(1, 0, 0), 4.0, C.x, 0.3); pitchG.add(axX);
    var axZ = arrow(new THREE.Vector3(0, 0, 1), 3.4, C.z, 0.3); rollG.add(axZ);

    /* 안쪽 물체 — 방향을 알 수 있는 화살촉 모양 */
    var craft = new THREE.Group();
    var body = new THREE.Mesh(
      new THREE.ConeGeometry(0.42, 1.7, 4),
      new THREE.MeshLambertMaterial({ color: 0xe8ecf4 })
    );
    body.rotation.x = Math.PI / 2;
    var wing = new THREE.Mesh(
      new THREE.BoxGeometry(2.1, 0.09, 0.5),
      new THREE.MeshLambertMaterial({ color: C.gfx })
    );
    var tail = new THREE.Mesh(
      new THREE.BoxGeometry(0.09, 0.62, 0.42),
      new THREE.MeshLambertMaterial({ color: C.gfx })
    );
    tail.position.set(0, 0.3, 0.62);
    craft.add(body, wing, tail);
    rollG.add(craft);

    var yS = el(host, "[data-yaw]"), pS = el(host, "[data-pitch]"), rS = el(host, "[data-roll]");
    var yV = el(host, "[data-yaw-v]"), pV = el(host, "[data-pitch-v]"), rV = el(host, "[data-roll-v]");
    var alert = el(host, "[data-alert]"), out = el(host, "[data-out]");
    var btnLock = el(host, "[data-lock]"), btnReset = el(host, "[data-reset]");

    var anim = null;

    function update() {
      var y = +yS.value, p = +pS.value, r = +rS.value;
      yawG.rotation.y = rad(y);
      pitchG.rotation.x = rad(p);
      rollG.rotation.z = rad(r);

      yV.textContent = y + "°"; pV.textContent = p + "°"; rV.textContent = r + "°";

      /* 바깥(Y)축과 안쪽(Z)축이 얼마나 겹쳤는가 = 자유도 손실 정도 */
      var yAxis = new THREE.Vector3(0, 1, 0);
      var zAxis = new THREE.Vector3(0, 0, 1).applyQuaternion(rollG.getWorldQuaternion(new THREE.Quaternion()));
      var align = Math.abs(yAxis.dot(zAxis));          /* 1 이면 완전히 같은 축 */
      var locked = align > 0.985;

      alert.classList.toggle("on", locked);
      alert.textContent = locked ? "⚠ GIMBAL LOCK — 자유도 3 → 2" : "";

      /* X 링은 원래 빨강이므로 잠금 색으로 빨강을 쓰면 구분이 안 된다.
         정렬된 두 링(Y·Z)만 호박색으로 띄운다. */
      rY.material.color.setHex(locked ? C.warn : C.y);
      rZ.material.color.setHex(locked ? C.warn : C.z);
      axY.setColor(locked ? C.warn : C.y);
      axZ.setColor(locked ? C.warn : C.z);

      out.innerHTML = locked
        ? '<b class="trap-txt">Y축과 Z축이 같은 방향 (정렬도 ' + align.toFixed(3) +
          ')</b> 요(Yaw)와 롤(Roll) 슬라이더가 <b>똑같은 회전</b> — ' +
          "회전축 하나 상실"
        : "축 정렬도 |Y·Z| = " + align.toFixed(3) +
          '　<span class="muted">1.000 에 가까워지면 두 축이 겹쳐 자유도 상실 · ' +
          "피치 ±90° 에서 확인</span>";
    }

    function animateTo(target, done) {
      if (anim) cancelAnimationFrame(anim);
      var start = +pS.value, t0 = performance.now(), dur = 900;
      (function step(now) {
        var k = Math.min(1, (now - t0) / dur);
        var e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        pS.value = Math.round(start + (target - start) * e);
        update();
        if (k < 1) anim = requestAnimationFrame(step); else if (done) done();
      })(t0);
    }

    btnLock.addEventListener("click", function () { animateTo(90); });
    btnReset.addEventListener("click", function () {
      yS.value = 0; rS.value = 0; animateTo(25);
    });
    [yS, pS, rS].forEach(function (s) { s.addEventListener("input", update); });

    update();
    return st;
  };
})();
