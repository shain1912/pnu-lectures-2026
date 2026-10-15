/* ============================================================
   10주차 데모 — 공간 UI 배치기
   UI 패널의 거리 · 각도 · 폭 · 캔버스 모드를 바꾸며
   각크기(°) · 글자 DMM · 조절-수렴 어긋남(D) 을 실시간 확인
   바닥 안내선 : 0.5 / 1 / 2 m 구간 + 시야 중심 ±30°
   오른쪽 위 작은 화면 : 머리(눈) 시점
   _stage.js 를 먼저 로드할 것
   ============================================================ */
(function () {
  "use strict";
  var S = window.CGStage;
  window.CGDemos = window.CGDemos || {};

  var EYE_H = 1.6;        /* 눈높이 (m) */
  var FOCAL = 1.5;        /* 가정한 렌즈 초점 고정면 (m) — 기기마다 다름 */
  var TEXT_RATIO = 0.07;  /* 본문 글자 높이 = 패널 폭의 7% */
  var DEG = Math.PI / 180;

  /* 패널 텍스처 — 메뉴 모양 */
  function panelTex() {
    var cv = document.createElement("canvas");
    cv.width = 512; cv.height = 307;
    var g = cv.getContext("2d");
    g.fillStyle = "#121722"; g.fillRect(0, 0, 512, 307);
    g.strokeStyle = "#35d6e6"; g.lineWidth = 6; g.strokeRect(3, 3, 506, 301);
    g.fillStyle = "#35d6e6";
    g.font = "bold 46px 'Malgun Gothic', Pretendard, sans-serif";
    g.textBaseline = "top";
    g.fillText("MENU", 28, 22);
    g.fillStyle = "#e8ecf4";
    g.font = "36px 'Malgun Gothic', Pretendard, sans-serif";   /* 36/512 ≈ 폭의 7% */
    g.fillText("점수  1,240", 28, 92);
    g.fillText("일시정지 상태", 28, 140);
    /* 버튼 두 개 */
    [[28, "계속"], [270, "종료"]].forEach(function (b) {
      g.fillStyle = "#0e3a42"; g.fillRect(b[0], 205, 214, 74);
      g.strokeStyle = "#35d6e6"; g.lineWidth = 3; g.strokeRect(b[0], 205, 214, 74);
      g.fillStyle = "#e8ecf4"; g.fillText(b[1], b[0] + 70, 222);
    });
    return new THREE.CanvasTexture(cv);
  }

  /* 바닥 부채꼴 구간 (r0~r1, 정면 ±30°) */
  function sector(r0, r1, color, opacity) {
    var geo = new THREE.RingGeometry(Math.max(r0, 0.001), r1, 48, 1, 60 * DEG, 60 * DEG);
    var m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({
      color: color, transparent: true, opacity: opacity,
      side: THREE.DoubleSide, depthWrite: false }));
    m.rotation.x = -Math.PI / 2;
    return m;
  }
  function arcLine(r, color) {
    var pts = [];
    for (var i = 0; i <= 64; i++) {
      var t = (30 + 120 * i / 64) * DEG;   /* 정면 ±60° 범위로 점선 호 */
      pts.push(new THREE.Vector3(Math.cos(t) * r, 0, -Math.sin(t) * r));
    }
    var l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),
      new THREE.LineDashedMaterial({ color: color, dashSize: 0.06, gapSize: 0.05 }));
    l.computeLineDistances();
    return l;
  }

  window.CGDemos["spatial-ui"] = function (host) {
    var st = S.make(host, {
      dist: 4.4, phi: 0.98, theta: 0.85, height: 400, fov: 40,
      ty: 0.9, gridSize: 8, gridDiv: 16
    });
    if (!st) return null;
    var C = st.C;
    st.orbit.target.set(0, 0.8, -0.9);   /* 머리와 패널 사이를 화면 중심으로 */
    st.place();

    /* ---- 머리 ------------------------------------------------- */
    var head = new THREE.Group();
    head.position.set(0, EYE_H, 0);
    var skull = new THREE.Mesh(new THREE.SphereGeometry(0.11, 24, 16),
      new THREE.MeshLambertMaterial({ color: 0xe8ecf4 }));
    head.add(skull);
    var visor = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.08, 0.08),
      new THREE.MeshLambertMaterial({ color: 0x2a3040 }));
    visor.position.set(0, 0.01, -0.1);
    head.add(visor);
    var nose = new THREE.Mesh(new THREE.ConeGeometry(0.035, 0.12, 12),
      new THREE.MeshLambertMaterial({ color: C.vr }));
    nose.rotation.x = -Math.PI / 2;
    nose.position.set(0, -0.02, -0.18);
    head.add(nose);
    st.scene.add(head);
    /* 몸통 기둥 */
    var body = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, 1.45, 16),
      new THREE.MeshLambertMaterial({ color: 0x3a4256 }));
    body.position.set(0, 0.725, 0);
    st.scene.add(body);

    /* ---- 바닥 안내선 (머리 방향을 따라 회전) ------------------- */
    var guide = new THREE.Group();
    guide.position.y = 0.01;
    guide.add(sector(0, 0.5, C.trap, 0.42));
    guide.add(sector(0.5, 1.0, C.warn, 0.30));
    guide.add(sector(1.0, 2.0, C.lab, 0.32));
    guide.add(sector(2.0, 3.6, C.gfx, 0.07));
    [0.5, 1, 2].forEach(function (r) { guide.add(arcLine(r, 0x9aa4b8)); });
    [-30, 30].forEach(function (a) {
      var t = (90 + a) * DEG;
      var l = new THREE.Line(new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(Math.cos(t) * 3.6, 0, -Math.sin(t) * 3.6)]),
        new THREE.LineBasicMaterial({ color: C.gfx }));
      guide.add(l);
    });
    st.scene.add(guide);

    /* ---- UI 패널 ---------------------------------------------- */
    var tex = panelTex();
    var panel = new THREE.Mesh(new THREE.PlaneGeometry(1, 0.6),
      new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide }));
    st.scene.add(panel);
    var linkGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    var link = new THREE.Line(linkGeo, new THREE.LineDashedMaterial({
      color: C.warn, dashSize: 0.08, gapSize: 0.06 }));
    st.scene.add(link);
    /* 패널 → 바닥 수직선 (위치 읽기용) */
    var dropGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    var drop = new THREE.Line(dropGeo, new THREE.LineBasicMaterial({ color: 0x9aa4b8 }));
    st.scene.add(drop);
    var foot = new THREE.Mesh(new THREE.RingGeometry(0.04, 0.06, 24),
      new THREE.MeshBasicMaterial({ color: 0xe8ecf4, side: THREE.DoubleSide }));
    foot.rotation.x = -Math.PI / 2;
    st.scene.add(foot);

    /* ---- 눈 시점 카메라 ---------------------------------------- */
    var eyeCam = new THREE.PerspectiveCamera(78, 4 / 3, 0.05, 50);

    /* ---- 상태 / 컨트롤 ---------------------------------------- */
    var p = { dist: 1.5, ang: 0, size: 0.6, head: 0, mode: "world" };
    var inputs = host.parentNode.querySelectorAll("[data-k]");
    var modeSel = S.el(host, "[data-mode]");
    var out = S.el(host, "[data-out]");
    var alertEl = S.el(host, "[data-alert]");
    var UNIT = { dist: " m", ang: "°", size: " m", head: "°" };

    function val(k) { return S.el(host, '[data-v="' + k + '"]'); }

    function update() {
      var yawHead = p.head * DEG;
      head.rotation.y = -yawHead;
      guide.rotation.y = -yawHead;

      /* 패널의 세계 방향 : World = 고정 · Camera = 머리 기준 */
      var worldYaw = (p.mode === "camera" ? p.head + p.ang : p.ang) * DEG;
      var dir = new THREE.Vector3(Math.sin(worldYaw), 0, -Math.cos(worldYaw));
      panel.position.set(dir.x * p.dist, EYE_H - 0.08 * p.dist, dir.z * p.dist);
      panel.scale.set(p.size, p.size, 1);
      panel.lookAt(head.position);
      panel.visible = p.mode !== "overlay";
      link.visible = panel.visible;
      linkGeo.setFromPoints([head.position.clone(), panel.position.clone()]);
      link.computeLineDistances();
      dropGeo.setFromPoints([panel.position.clone(),
        new THREE.Vector3(panel.position.x, 0.015, panel.position.z)]);
      drop.visible = foot.visible = panel.visible;
      foot.position.set(panel.position.x, 0.015, panel.position.z);

      /* 수치 */
      var rel = Math.round(p.mode === "camera" ? p.ang : p.ang - p.head);
      var d = head.position.distanceTo(panel.position);
      var deg = 2 * Math.atan(p.size / (2 * d)) / DEG;
      var textMm = p.size * TEXT_RATIO * 1000;
      var dmm = textMm / d;
      var verg = 1 / d, delta = Math.abs(verg - 1 / FOCAL);
      var vergAng = 2 * Math.atan(0.0315 / d) / DEG;

      Array.prototype.forEach.call(inputs, function (el) {
        var k = el.dataset.k, v = val(k);
        if (v) v.textContent = (+p[k]).toFixed(k === "ang" || k === "head" ? 0 : 2) + UNIT[k];
      });

      /* 경고 — 우선순위 순서 */
      var warns = [];
      if (p.mode === "overlay") warns.push("Overlay · 헤드셋 렌즈 화면에 그려지지 않음");
      else {
        if (d < 0.5) warns.push("0.5 m 미만 · 조절-수렴 어긋남 " + delta.toFixed(2) + " D · 이중상 위험");
        if (d > 2.0) warns.push("2 m 초과 · 글자 " + dmm.toFixed(0) + " DMM (권고 24) · 가독성 손실");
        if (Math.abs(rel) > 30) warns.push("시야 중심 ±30° 밖 (" + rel + "°) · 목 회전 필요");
        if (p.mode === "camera") warns.push("헤드락 · 머리를 따라옴");
      }
      if (alertEl) {
        alertEl.textContent = warns[0] || "";
        alertEl.classList.toggle("on", warns.length > 0);
        alertEl.style.background = (warns.length && p.mode !== "camera") || warns.length > 1
          ? "#ff5a4d" : "#ffc44d";
      }
      if (out) {
        out.textContent = p.mode === "overlay"
          ? "Overlay : 3D 공간에 존재하지 않음 → 눈 시점에 표시 없음 (PC 미러 창에만 보일 수 있음)"
          : "거리 " + d.toFixed(2) + " m · 정면에서 " + rel + "° · 패널 폭 " + deg.toFixed(1) +
            "° · 본문 글자 " + dmm.toFixed(0) + " DMM · 수렴 " + verg.toFixed(2) + " D (" +
            vergAng.toFixed(1) + "°) · 초점면 " + FOCAL + " m 가정 시 어긋남 " + delta.toFixed(2) + " D";
      }
    }

    Array.prototype.forEach.call(inputs, function (el) {
      el.addEventListener("input", function () { p[el.dataset.k] = parseFloat(el.value); update(); });
      p[el.dataset.k] = parseFloat(el.value);
    });
    if (modeSel) modeSel.addEventListener("change", function () { p.mode = modeSel.value; update(); });
    update();

    /* ---- 렌더 : 전체 + 눈 시점 인셋 ----------------------------- */
    var r = st.renderer;
    var sz = new THREE.Vector2();
    st.draw = function () {
      r.getSize(sz);
      r.setScissorTest(false);
      r.setViewport(0, 0, sz.x, sz.y);
      r.setClearColor(0x06070a, 1);
      r.render(st.scene, st.cam);

      /* 눈 시점 */
      var iw = Math.round(sz.x * 0.3), ih = Math.round(iw * 0.75);
      var ix = sz.x - iw - 10, iy = sz.y - ih - 10;
      eyeCam.position.copy(head.position);
      eyeCam.rotation.set(0, -p.head * DEG, 0);
      eyeCam.aspect = iw / ih;
      eyeCam.updateProjectionMatrix();
      head.visible = false; body.visible = false; link.visible = false; drop.visible = false; foot.visible = false;
      r.setScissorTest(true);
      r.setScissor(ix - 2, iy - 2, iw + 4, ih + 4);
      r.setViewport(ix - 2, iy - 2, iw + 4, ih + 4);
      r.setClearColor(0x35d6e6, 1);
      r.clear();
      r.setScissor(ix, iy, iw, ih);
      r.setViewport(ix, iy, iw, ih);
      r.setClearColor(0x0d1018, 1);
      r.render(st.scene, eyeCam);
      head.visible = true; body.visible = true;
      link.visible = drop.visible = foot.visible = p.mode !== "overlay";
      r.setScissorTest(false);
      r.setClearColor(0x06070a, 1);
    };

    return st;
  };
})();
