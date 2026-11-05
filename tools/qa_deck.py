"""reveal 덱 시각 QA : 슬라이드별 넘침 측정 + 전 장 스크린샷 + 접촉 시트

    py tools/qa_deck.py <url> <out_dir>

넘침 = 슬라이드 내 요소의 아래쪽·오른쪽 경계가 1280×720 지면 밖으로 나간 경우
"""
import json, math, pathlib, sys
from playwright.sync_api import sync_playwright
from PIL import Image

url, out = sys.argv[1], pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

JS = """() => {
  const s = Reveal.getCurrentSlide(); const r = [];
  const sb = s.getBoundingClientRect();
  const scale = Reveal.getScale();
  const H = Reveal.getConfig().height, W = Reveal.getConfig().width;
  let maxB = 0, maxR = 0, who = '';
  s.querySelectorAll('*').forEach(e => {
    if (e.closest('aside') || e.tagName === 'ASIDE') return;
    if (getComputedStyle(e).position === 'absolute' && e.tagName === 'IMG') return;
    const b = e.getBoundingClientRect();
    if (!b.width || !b.height) return;
    const bot = (b.bottom - sb.top) / scale, rt = (b.right - sb.left) / scale;
    if (bot > maxB) { maxB = bot; who = e.tagName + '.' + e.className; }
    if (rt > maxR) maxR = rt;
  });
  return { h: Math.round(maxB), w: Math.round(maxR), who, H, W, title: (s.querySelector('h1,h2,h3,.tag')||{}).innerText || '' };
}"""

with sync_playwright() as p:
    try:
        b = p.chromium.launch(channel="chrome")
    except Exception:
        b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("requestfailed", lambda r: errs.append("FAILED " + r.url))
    pg.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    pg.goto(url, wait_until="networkidle", timeout=120000)
    pg.wait_for_function("window.Reveal && Reveal.isReady()", timeout=60000)
    n = pg.evaluate("Reveal.getTotalSlides()")
    shots, over = [], []
    for i in range(n):
        pg.evaluate(f"Reveal.slide({i})")
        pg.wait_for_timeout(450)
        m = pg.evaluate(JS)
        f = out / f"s{i+1:02d}.png"
        pg.screenshot(path=str(f))
        shots.append(f)
        if m["h"] > m["H"] - 8 or m["w"] > m["W"] + 2:
            over.append((i + 1, m["h"], m["w"], m["who"], m["title"][:30]))
    b.close()

print("slides", n)
print("OVERFLOW", json.dumps(over, ensure_ascii=False, indent=0))
print("ERRORS", errs[:12])
per = 6
for k in range(0, n, per * 4):
    part = shots[k:k + per * 4]
    tw, th = 400, 225
    rows = math.ceil(len(part) / per)
    sheet = Image.new("RGB", (tw * per, th * rows), "white")
    for j, f in enumerate(part):
        im = Image.open(f).convert("RGB").resize((tw - 4, th - 4))
        sheet.paste(im, ((j % per) * tw + 2, (j // per) * th + 2))
    sheet.save(out / f"sheet{k // (per * 4) + 1}.png")
