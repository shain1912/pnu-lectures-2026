"""reveal.js 덱을 PDF 로 출력

    py tools/print_pdf.py <url?print-pdf> <out.pdf>

Chrome 153 헤드리스의 --print-to-pdf 는 reveal 인쇄 레이아웃(.pdf-page) 생성 전에
출력 → 빈 1쪽. Playwright 로 레이아웃 완료까지 대기 후 출력.
"""
import sys
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    try:
        browser = p.chromium.launch(channel="chrome")
    except Exception:
        browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto(url, wait_until="networkidle", timeout=120000)
    page.wait_for_selector(".pdf-page", state="attached", timeout=60000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_function("[...document.images].every(i => i.complete)", timeout=60000)
    page.wait_for_timeout(1500)
    page.pdf(path=out, print_background=True, prefer_css_page_size=True)
    n = page.evaluate("document.querySelectorAll('.pdf-page').length")
    browser.close()
print(n)
