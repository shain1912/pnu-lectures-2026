/* ============================================================
   3주차 데모 — 프레임 독립성 · motion-to-photon 지연
   _stage.js 를 먼저 로드할 것
   ============================================================ */
(function () {
  "use strict";
  var S = window.CGStage;
  var C = S.C;
  window.CGDemos = window.CGDemos || {};

  /* ============================================================
     A. AI 함정 #2 — Time.deltaTime 을 빼먹으면  ★
     같은 코드, 다른 프레임률. 위 큐브는 PC 성능에 따라 속도가 변한다.
     ============================================================ */
  window.CGDemos["deltatime"] = function (host) {
    var st = S.make(host, {
      dist: 15.5, phi: 0.60, theta: 0.0, ty: 0.2, grid: false, height: 320, fov: 40
    });
    if (!st) return null;

    var LANE = 12;          /* 트랙 길이(m) */
    var SPEED = 2.0;        /* 의도한 속도 (m/s) */
    var BASE_FPS = 60;      /* "개발자 PC" 프레임률 */

    /* 트랙 두 줄 */
    function lane(z, color) {
      var pts = [new THREE.Vector3(-LANE / 2, 0, z), new THREE.Vector3(LANE / 2, 0, z)];
      var l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),
                             new THREE.LineBasicMaterial({ color: color }));
      st.scene.add(l);
      /* 1m 눈금 */
      for (var i = 0; i <= LANE; i++) {
        var t = -LANE / 2 + i;
        var g = new THREE.Line(
          new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(t, 0, z - 0.18), new THREE.Vector3(t, 0, z + 0.18)]),
          new THREE.LineBasicMaterial({ color: C.grid }));
        st.scene.add(g);
      }
    }
    lane(-1.4, 0x2a3040);
    lane(1.4, 0x2a3040);

    /* 결승선 */
    [-1.4, 1.4].forEach(function (z) {
      var f = new THREE.Mesh(
        new THREE.PlaneGeometry(0.06, 1.6),
        new THREE.MeshBasicMaterial({ color: C.warn }));
      f.position.set(LANE / 2, 0.8, z);
      st.scene.add(f);
    });

    var bad = S.box(0.9, C.trap);  bad.position.set(-LANE / 2, 0.45, -1.4);
    var good = S.box(0.9, C.lab);  good.position.set(-LANE / 2, 0.45, 1.4);
    st.scene.add(bad, good);

    var fpsS = S.el(host, "[data-fps]"), fpsV = S.el(host, "[data-fps-v]");
    var out = S.el(host, "[data-out]"), btn = S.el(host, "[data-reset]");

    var acc = 0, elapsed = 0, tBad = null, tGood = null;

    function reset() {
      bad.position.x = -LANE / 2; good.position.x = -LANE / 2;
      acc = 0; elapsed = 0; tBad = null; tGood = null;
    }
    btn.addEventListener("click", reset);
    fpsS.addEventListener("input", function () {
      fpsV.textContent = fpsS.value + " fps";
      reset();
    });
    fpsV.textContent = fpsS.value + " fps";

    var baseDraw = st.draw;
    st.draw = function () {
      var real = st.tick();
      var fps = +fpsS.value;
      var step = 1 / fps;

      if (tBad === null || tGood === null) {
        elapsed += real;
        acc += real;
        /* 선택한 프레임률로 시뮬레이션 프레임을 돌린다 */
        var guard = 0;
        while (acc >= step && guard++ < 240) {
          acc -= step;
          /* 잘못된 코드: 프레임마다 고정량 (60fps 기준으로 맞춰둔 값) */
          if (tBad === null) bad.position.x += SPEED / BASE_FPS;
          /* 올바른 코드: 실제 경과 시간을 곱한다 */
          if (tGood === null) good.position.x += SPEED * step;
        }
        if (tBad === null && bad.position.x >= LANE / 2) {
          bad.position.x = LANE / 2; tBad = elapsed;
        }
        if (tGood === null && good.position.x >= LANE / 2) {
          good.position.x = LANE / 2; tGood = elapsed;
        }
      }

      var f = function (v) { return v === null ? "달리는 중" : v.toFixed(2) + " 초"; };
      out.innerHTML =
        '<b class="trap-txt">deltaTime 없음</b> ' + f(tBad) +
        '　<b class="lab-txt">deltaTime 있음</b> ' + f(tGood) +
        '　<span class="muted">정답은 ' + (LANE / SPEED).toFixed(2) + ' 초</span>';
      baseDraw();
    };

    reset();
    return st;
  };

  /* ============================================================
     B. motion-to-photon — 화면은 항상 과거를 보여준다
     ============================================================ */
  window.CGDemos["latency"] = function (host) {
    /* 각도를 읽어야 하는 데모다. 비스듬히 보면 각이 왜곡되므로
       거의 수직으로 내려다보는 나침반 형태로 그린다. */
    var st = S.make(host, {
      dist: 11, phi: 0.045, theta: 0, grid: false, height: 330,
      orbit: false, fov: 42, lights: false
    });
    if (!st) return null;

    var R = 4.0;

    /* 눈금 다이얼 */
    var dial = new THREE.Group();
    dial.rotation.x = -Math.PI / 2;
    st.scene.add(dial);
    (function () {
      var ring = new THREE.Mesh(
        new THREE.RingGeometry(R - 0.035, R + 0.035, 96),
        new THREE.MeshBasicMaterial({ color: 0x2a3040 }));
      dial.add(ring);
      for (var d = -90; d <= 90; d += 15) {
        var a = d * Math.PI / 180;
        var major = (d % 45 === 0);
        var r0 = R - (major ? 0.42 : 0.22);
        var g = new THREE.BufferGeometry().setFromPoints([
          new THREE.Vector2(Math.sin(a) * r0, Math.cos(a) * r0),
          new THREE.Vector2(Math.sin(a) * R, Math.cos(a) * R)]);
        dial.add(new THREE.Line(g, new THREE.LineBasicMaterial({
          color: major ? 0x3a4356 : 0x252c3a })));
      }
    })();

    /* 바늘 — y 를 조금씩 띄워 겹침(z-fighting) 을 피한다 */
    function needle(len, color, width, y) {
      var shape = new THREE.Shape();
      shape.moveTo(-width, 0); shape.lineTo(0, len); shape.lineTo(width, 0);
      shape.lineTo(0, width * 0.9); shape.lineTo(-width, 0);
      var m = new THREE.Mesh(new THREE.ShapeGeometry(shape),
        new THREE.MeshBasicMaterial({ color: color, side: THREE.DoubleSide }));
      var g = new THREE.Group();
      m.rotation.x = -Math.PI / 2;
      g.add(m); g.position.y = y;
      return g;
    }

    /* 오차 부채꼴 (가장 아래) */
    var wedge = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({
      color: C.trap, transparent: true, opacity: 0.42, side: THREE.DoubleSide }));
    wedge.rotation.x = -Math.PI / 2;
    wedge.position.y = 0.02;
    st.scene.add(wedge);

    var shown = needle(R - 0.5, C.vr, 0.34, 0.06);   /* 화면이 보여주는 방향 */
    var truth = needle(R - 0.1, C.gfx, 0.26, 0.10);  /* 실제 머리 방향 */
    st.scene.add(shown, truth);

    var head = new THREE.Mesh(new THREE.CircleGeometry(0.5, 28),
      new THREE.MeshBasicMaterial({ color: 0xe8ecf4 }));
    head.rotation.x = -Math.PI / 2;
    head.position.y = 0.14;
    st.scene.add(head);

    var latS = S.el(host, "[data-lat]"), latV = S.el(host, "[data-lat-v]");
    var spdS = S.el(host, "[data-spd]"), spdV = S.el(host, "[data-spd-v]");
    var out = S.el(host, "[data-out]");

    var t = 0;
    var hist = [];   /* {time, angle} */

    function headAngle(time) {
      var amp = +spdS.value * Math.PI / 180;   /* 좌우 진폭 */
      return Math.sin(time * 2.2) * amp;
    }

    var baseDraw = st.draw;
    st.draw = function () {
      t += st.tick();
      var lat = +latS.value / 1000;
      latV.textContent = latS.value + " ms";
      spdV.textContent = "±" + spdS.value + "°";

      var a = headAngle(t);
      hist.push({ t: t, a: a });
      while (hist.length > 400) hist.shift();

      /* lat 초 전의 각도를 찾아 화면에 그린다 */
      var target = t - lat, shownA = a;
      for (var i = hist.length - 1; i >= 0; i--) {
        if (hist[i].t <= target) { shownA = hist[i].a; break; }
        if (i === 0) shownA = hist[0].a;
      }

      truth.rotation.y = -a;
      shown.rotation.y = -shownA;

      /* 오차 부채꼴 갱신 */
      /* 바늘과 같은 각도 규약을 써야 부채꼴이 바늘 사이에 정확히 놓인다:
         각 a → 로컬 (sin a, cos a) → 월드 (sin a, 0, -cos a) */
      var pts = [new THREE.Vector2(0, 0)];
      var N = 28, a0 = Math.min(a, shownA), a1 = Math.max(a, shownA);
      for (var k = 0; k <= N; k++) {
        var ang = a0 + (a1 - a0) * k / N;
        pts.push(new THREE.Vector2(Math.sin(ang) * 3.5, Math.cos(ang) * 3.5));
      }
      wedge.geometry.dispose();
      wedge.geometry = new THREE.ShapeGeometry(new THREE.Shape(pts));

      var errDeg = Math.abs(a - shownA) * 180 / Math.PI;
      var bad = errDeg > 2.0;
      out.innerHTML =
        '<b class="gfx-txt">실제 머리</b> ' + (a * 180 / Math.PI).toFixed(1) + "°" +
        '　<b class="vr-txt">화면</b> ' + (shownA * 180 / Math.PI).toFixed(1) + "°" +
        '　<b style="color:' + (bad ? "#ff5a4d" : "#a8e05f") + '">어긋남 ' +
        errDeg.toFixed(1) + "°</b>" +
        (bad ? '　<span class="trap-txt">← 전정계가 감지하는 어긋남</span>' : "");

      baseDraw();
    };

    return st;
  };
})();
