/* ============================================================
   공통 덱 부트스트랩
   - Reveal 초기화
   - 데모 lazy init: 슬라이드에 들어올 때 생성, 보이는 것만 렌더
   ============================================================ */
(function () {
  "use strict";

  var live = null;          /* 현재 렌더 중인 데모 */
  var raf = null;

  function stopLoop() {
    if (raf) cancelAnimationFrame(raf);
    raf = null; live = null;
  }
  function startLoop(stage) {
    stopLoop();
    live = stage;
    (function tick() {
      if (!live) return;
      live.draw();
      raf = requestAnimationFrame(tick);
    })();
  }

  function activate(slide) {
    if (!slide) return;
    var host = slide.querySelector(".demo[data-demo]");
    if (!host) { stopLoop(); return; }

    if (!host.__stage) {
      var factory = (window.CGDemos || {})[host.dataset.demo];
      if (!factory) { stopLoop(); return; }
      try {
        host.__stage = factory(host) || null;
      } catch (e) {
        console.error("[demo] " + host.dataset.demo + " 초기화 실패", e);
        host.__stage = null;
      }
    }
    if (host.__stage) startLoop(host.__stage); else stopLoop();
  }

  window.addEventListener("DOMContentLoaded", function () {
    Reveal.initialize({
      hash: true,
      slideNumber: "c/t",
      controls: true,
      progress: true,
      overview: true,
      transition: "fade",
      transitionSpeed: "fast",
      backgroundTransition: "none",
      width: 1280,
      height: 720,
      margin: 0.055,
      minScale: 0.2,
      maxScale: 2.0,
      pdfSeparateFragments: false,
      plugins: [RevealNotes, RevealHighlight]
    }).then(function () {
      activate(Reveal.getCurrentSlide());
    });

    Reveal.on("slidechanged", function (e) { activate(e.currentSlide); });
  });
})();
