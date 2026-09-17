/* ============================================================
   데모 공통 무대  (3주차부터 사용)
   three.js r128 (UMD 전역 THREE) 필요

   window.CGStage.make(host, opts) -> {scene, cam, renderer, draw, ...}
   window.CGStage.el(host, sel)    -> 컨트롤 조회 (host 의 형제)
   ============================================================ */
(function () {
  "use strict";

  var C = {
    gfx: 0x35d6e6, vr: 0xff5fa2, trap: 0xff5a4d, lab: 0xa8e05f,
    warn: 0xffc44d, dim: 0x5f6980, fg: 0xe8ecf4,
    grid: 0x232a38, gridC: 0x323b4d,
    x: 0xff5a4d, y: 0xa8e05f, z: 0x4d9cff
  };

  function make(host, opt) {
    opt = opt || {};
    if (typeof THREE === "undefined") {
      host.innerHTML =
        '<div style="padding:2em;color:#5f6980;font-family:monospace;font-size:.5em">' +
        "three.js 로드 실패 · 인터넷 연결 확인</div>";
      return null;
    }
    var h = opt.height || 330;
    var w = host.clientWidth || 800;

    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(w, h, false);
    renderer.setClearColor(opt.clear != null ? opt.clear : 0x06070a, 1);
    renderer.domElement.style.height = h + "px";
    host.insertBefore(renderer.domElement, host.firstChild);

    var scene = new THREE.Scene();
    var cam = new THREE.PerspectiveCamera(opt.fov || 42, w / h, 0.1, 400);

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

    if (opt.orbit !== false) {
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
        orbit.phi = Math.max(0.12, Math.min(Math.PI - 0.12,
          orbit.phi - (e.clientY - py) * 0.008));
        px = e.clientX; py = e.clientY; place();
      });
      cv.addEventListener("pointerup", function (e) {
        dragging = false; cv.style.cursor = "grab";
        try { cv.releasePointerCapture(e.pointerId); } catch (_) {}
      });
    }

    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        var nw = host.clientWidth;
        if (!nw || nw === w) return;
        w = nw; cam.aspect = w / h; cam.updateProjectionMatrix();
        renderer.setSize(w, h, false);
      }).observe(host);
    }

    if (opt.grid !== false) {
      var g = new THREE.GridHelper(opt.gridSize || 10, opt.gridDiv || opt.gridSize || 10,
                                   C.gridC, C.grid);
      g.position.y = opt.gridY || 0;
      scene.add(g);
    }
    if (opt.lights !== false) {
      scene.add(new THREE.AmbientLight(0xffffff, 0.62));
      var d1 = new THREE.DirectionalLight(0xffffff, 0.85); d1.position.set(4, 7, 5);
      scene.add(d1);
      var d2 = new THREE.DirectionalLight(0x4d9cff, 0.3); d2.position.set(-5, 2, -4);
      scene.add(d2);
    }

    var last = performance.now();
    return {
      scene: scene, cam: cam, renderer: renderer, orbit: orbit, place: place,
      C: C,
      /* 실제 경과 시간(초). 탭 전환 뒤 튀지 않게 상한을 둔다. */
      tick: function () {
        var now = performance.now();
        var dt = Math.min((now - last) / 1000, 0.1);
        last = now;
        return dt;
      },
      draw: function () { renderer.render(scene, cam); }
    };
  }

  function el(host, sel) { return host.parentNode.querySelector(sel); }

  function box(size, color, opacity) {
    var g = new THREE.Group();
    var geo = new THREE.BoxGeometry(size, size, size);
    g.add(new THREE.Mesh(geo, new THREE.MeshLambertMaterial({
      color: color, transparent: opacity != null, opacity: opacity == null ? 1 : opacity
    })));
    g.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(geo),
      new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.4 })));
    return g;
  }

  window.CGStage = { make: make, el: el, box: box, C: C };
})();
