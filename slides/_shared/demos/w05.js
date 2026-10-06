/* ============================================================
   5주차 데모 — 깊이 단서 실험실
   같은 크기로 보이는 공 세 개 · 단서를 하나씩 켜며 거리 순서 판단
   _stage.js 를 먼저 로드할 것
   ============================================================ */
(function () {
  "use strict";
  var S = window.CGStage;
  var C = S.C;
  window.CGDemos = window.CGDemos || {};

  /* 바닥 격자 텍스처 — 결 기울기용 */
  function checkerTex() {
    var cv = document.createElement("canvas");
    cv.width = cv.height = 128;
    var g = cv.getContext("2d");
    g.fillStyle = "#11151d"; g.fillRect(0, 0, 128, 128);
    g.fillStyle = "#1c2230"; g.fillRect(0, 0, 64, 64); g.fillRect(64, 64, 64, 64);
    g.strokeStyle = "#2c3445"; g.lineWidth = 3;
    g.strokeRect(0, 0, 128, 128);
    var t = new THREE.CanvasTexture(cv);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(26, 26);
    return t;
  }

  /* 접지 그림자용 부드러운 원판 텍스처 */
  function blobTex() {
    var cv = document.createElement("canvas");
    cv.width = cv.height = 128;
    var g = cv.getContext("2d");
    var rg = g.createRadialGradient(64, 64, 4, 64, 64, 62);
    rg.addColorStop(0, "rgba(0,0,0,0.85)");
    rg.addColorStop(0.55, "rgba(0,0,0,0.38)");
    rg.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = rg; g.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(cv);
  }

  /* 거리 표시 라벨 */
  function labelSprite(text) {
    var cv = document.createElement("canvas");
    cv.width = 256; cv.height = 96;
    var g = cv.getContext("2d");
    g.clearRect(0, 0, 256, 96);
    g.fillStyle = "rgba(11,13,18,0.86)";
    g.strokeStyle = "#35d6e6"; g.lineWidth = 4;
    g.beginPath(); g.rect(10, 18, 236, 60); g.fill(); g.stroke();
    g.fillStyle = "#e8ecf4";
    g.font = "bold 40px Consolas, monospace";
    g.textAlign = "center"; g.textBaseline = "middle";
    g.fillText(text, 128, 49);
    var t = new THREE.CanvasTexture(cv);
    var sp = new THREE.Sprite(new THREE.SpriteMaterial({
      map: t, transparent: true, depthTest: false }));
    sp.scale.set(2.3, 0.86, 1);
    sp.renderOrder = 20;
    sp.userData.redraw = function (s) {
      g.clearRect(0, 0, 256, 96);
      g.fillStyle = "rgba(11,13,18,0.86)";
      g.strokeStyle = "#35d6e6"; g.lineWidth = 4;
      g.beginPath(); g.rect(10, 18, 236, 60); g.fill(); g.stroke();
      g.fillStyle = "#e8ecf4";
      g.font = "bold 40px Consolas, monospace";
      g.textAlign = "center"; g.textBaseline = "middle";
      g.fillText(s, 128, 49);
      t.needsUpdate = true;
    };
    return sp;
  }

  /* ============================================================
     깊이 단서 실험실
     ============================================================ */
  window.CGDemos["depth-cues"] = function (host) {
    var st = S.make(host, {
      dist: 19, phi: 1.14, theta: 0.02, height: 340, fov: 36,
      ty: 1.5, grid: false, lights: false, clear: 0x080a0f
    });
    if (!st) return null;

    /* ---- 바닥 ------------------------------------------------- */
    var tex = checkerTex();
    var groundMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
    var ground = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    st.scene.add(ground);

    /* ---- 조명 ------------------------------------------------- */
    st.scene.add(new THREE.AmbientLight(0xffffff, 0.52));
    var sun = new THREE.DirectionalLight(0xffffff, 0.95);
    sun.position.set(7, 15, 6);
    sun.castShadow = false;
    sun.shadow.mapSize.width = sun.shadow.mapSize.height = 1024;
    var sc = sun.shadow.camera;
    sc.left = -22; sc.right = 22; sc.top = 22; sc.bottom = -22;
    sc.near = 1; sc.far = 60;
    st.scene.add(sun);
    st.renderer.shadowMap.enabled = true;
    st.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    /* ---- 공 세 개 (바닥에서 같은 높이로 떠 있음) -------------- */
    var R0 = 0.9, HEIGHT = 1.75;
    var blob = blobTex();
    var balls = [];
    [[-4.2, 5.5], [0.2, -3.0], [4.4, -12.0]].forEach(function (p, i) {
      var mesh = new THREE.Mesh(
        new THREE.SphereGeometry(R0, 40, 28),
        new THREE.MeshLambertMaterial({ color: C.gfx }));
      mesh.position.set(p[0], HEIGHT, p[1]);
      mesh.castShadow = true;
      st.scene.add(mesh);

      var disc = new THREE.Mesh(
        new THREE.PlaneGeometry(R0 * 4.2, R0 * 4.2),
        new THREE.MeshBasicMaterial({
          map: blob, transparent: true, opacity: 0.9, depthWrite: false }));
      disc.rotation.x = -Math.PI / 2;
      disc.position.set(p[0], 0.02, p[1]);
      disc.visible = false;
      st.scene.add(disc);

      var tag = labelSprite("");
      tag.position.set(p[0], HEIGHT + 1.5, p[1]);
      tag.visible = false;
      st.scene.add(tag);

      balls.push({ mesh: mesh, disc: disc, tag: tag, name: "ABC"[i] });
    });

    /* ---- 단서 상태 -------------------------------------------- */
    var cue = { shadow: false, contact: false, size: false, texture: false, fog: false };
    var LABEL = {
      shadow: "그림자", contact: "접지 그림자", size: "상대 크기",
      texture: "결 기울기", fog: "대기 원근"
    };
    var reveal = false;

    var fog = new THREE.Fog(0x080a0f, 13, 46);
    var out = S.el(host, "[data-out]");
    var btns = host.parentNode.querySelectorAll("[data-cue]");
    var revealBtn = S.el(host, "[data-reveal]");
    var resetBtn = S.el(host, "[data-reset]");

    function paint() {
      /* 바닥 무늬 */
      groundMat.map = cue.texture ? tex : null;
      groundMat.color.setHex(cue.texture ? 0xffffff : 0x161b25);
      groundMat.needsUpdate = true;
      /* 그림자 */
      sun.castShadow = cue.shadow;
      /* 접지 그림자 */
      balls.forEach(function (b) { b.disc.visible = cue.contact; });
      /* 대기 원근 */
      st.scene.fog = cue.fog ? fog : null;
      balls.forEach(function (b) { b.mesh.material.needsUpdate = true; });

      /* 버튼 라벨 */
      Array.prototype.forEach.call(btns, function (b) {
        var k = b.dataset.cue;
        b.textContent = LABEL[k] + (cue[k] ? " 켬" : " 끔");
        b.style.borderColor = cue[k] ? "#35d6e6" : "";
        b.style.color = cue[k] ? "#35d6e6" : "";
      });
      if (revealBtn) revealBtn.textContent = reveal ? "거리 가리기" : "실제 거리 공개";

      /* 읽기값 */
      var on = Object.keys(cue).filter(function (k) { return cue[k]; });
      var msg;
      if (on.length === 0) {
        msg = "켠 단서 0개 · 세 공의 화면 크기 동일 → 순서 판단 근거 없음";
      } else {
        msg = "켠 단서 " + on.length + "개 (" +
          on.map(function (k) { return LABEL[k]; }).join(" · ") + ") → " +
          (on.length === 1 ? "순서 추정 가능" : "순서 판단 가능");
      }
      if (out) out.textContent = msg;
    }

    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener("click", function () {
        cue[b.dataset.cue] = !cue[b.dataset.cue];
        paint();
      });
    });
    if (revealBtn) revealBtn.addEventListener("click", function () {
      reveal = !reveal;
      balls.forEach(function (b) { b.tag.visible = reveal; });
      paint();
    });
    if (resetBtn) resetBtn.addEventListener("click", function () {
      Object.keys(cue).forEach(function (k) { cue[k] = false; });
      reveal = false;
      balls.forEach(function (b) { b.tag.visible = false; });
      paint();
    });

    paint();

    /* ---- 렌더 -------------------------------------------------- */
    var baseDraw = st.draw;
    st.draw = function () {
      /* 상대 크기 끔 → 화면에 찍히는 크기를 매 프레임 동일하게 맞춘다 */
      var d0 = null;
      balls.forEach(function (b, i) {
        var d = st.cam.position.distanceTo(b.mesh.position);
        if (i === 0) d0 = d;
        var s = cue.size ? 1 : d / d0;
        b.mesh.scale.setScalar(s);
        b.disc.scale.setScalar(Math.max(0.35, s * 0.9));
        if (reveal) {
          b.tag.position.set(b.mesh.position.x,
                             HEIGHT + 1.2 + R0 * s, b.mesh.position.z);
          b.tag.userData.redraw(b.name + " · " + d.toFixed(1) + " m");
        }
      });
      baseDraw();
    };

    return st;
  };
})();
