/**
 * 슬라이드 배포 빌드
 *
 *   node slides/build.mjs 02 [03 ...]
 *
 * 하는 일
 *  1) slides/wNN/_print.html 생성
 *     - 도해 SVG → PNG 치환 (헤드리스 Chrome 이 인쇄 시 SVG <img> 를 종종 누락한다)
 *     - <video> → 포스터 이미지 (PDF 는 영상을 담을 수 없다)
 *     - 인터랙티브 데모 → "라이브 데모" 안내 카드
 *  2) 헤드리스 Chrome 으로 dist/wNN-<제목>.pdf 출력
 *
 * 사전 조건: 프로젝트 루트에서 http://localhost:8765 로 정적 서버가 떠 있을 것
 *   .venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const PORT = process.env.SLIDE_PORT || 8765;
const CHROME = [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
].find(existsSync);

const weeks = process.argv.slice(2);
if (!weeks.length) {
  console.error("사용법: node slides/build.mjs 02 [03 ...]");
  process.exit(1);
}
if (!CHROME) {
  console.error("Chrome 을 찾지 못함");
  process.exit(1);
}

mkdirSync(path.join(ROOT, "dist"), { recursive: true });

for (const w of weeks) {
  const wk = String(w).padStart(2, "0");
  const src = path.join(ROOT, "slides", `w${wk}`, "index.html");
  if (!existsSync(src)) {
    console.error(`  건너뜀 — ${src} 없음`);
    continue;
  }

  let html = readFileSync(src, "utf8");
  const title = (html.match(/<title>([^<]+)<\/title>/) || [, `w${wk}`])[1]
    .split("—")[0]
    .trim()
    .replace(/[\\/:*?"<>|]/g, "");

  // 1) 도해 SVG → PNG
  html = html.replace(/(figures\/out\/[\w-]+)\.svg/g, "$1.png");

  // 2) <video ...src="....mp4"...></video>  →  포스터 이미지
  html = html.replace(
    /<video[^>]*src="([^"]+)\.mp4"[\s\S]*?<\/video>/g,
    (_m, base) =>
      `<img src="${base}-poster.png" class="fig" alt="애니메이션 스틸">` +
      `<p class="xs muted" style="text-align:center;margin-top:.5em">` +
      `▶ 애니메이션 재생은 HTML 슬라이드에서</p>`
  );

  // 3) 인터랙티브 데모 → 안내 카드 (PDF 에서는 빈 상자로 남으므로)
  //    중첩된 </div> 를 정규식으로 세는 것은 불가능하므로 덱 소스에
  //    <!--/demo--> 종료 마커를 두고 그 사이를 통째로 바꾼다.
  const demoBlocks = (html.match(/<!--\/demo-->/g) || []).length;
  html = html.replace(
    /<div class="demo-wrap">[\s\S]*?<!--\/demo-->/g,
    `<div class="card gfx" style="text-align:center;padding:2.2em 1em">
       <h4 style="margin-bottom:.4em">인터랙티브 데모</h4>
       <p class="xs muted" style="margin:0">이 자리에는 직접 조작하는 3D 데모<br><br>
       HTML 슬라이드를 브라우저로 열어 확인</p>
     </div>`
  );

  const printPath = path.join(ROOT, "slides", `w${wk}`, "_print.html");
  writeFileSync(printPath, html, "utf8");
  console.log(`  ✓ slides/w${wk}/_print.html  (데모 ${demoBlocks}개 치환)`);

  const out = path.join(ROOT, "dist", `w${wk}-${title}.pdf`);
  // Chrome 153 헤드리스 --print-to-pdf 는 reveal 인쇄 레이아웃 전에 출력 → 빈 1쪽
  // Playwright 로 .pdf-page 생성까지 대기 후 출력
  const pages = execFileSync(
    "py",
    [path.join(ROOT, "tools", "print_pdf.py"), `http://localhost:${PORT}/slides/w${wk}/_print.html?print-pdf`, out],
    { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"] }
  ).trim();
  console.log(`  ✓ dist/w${wk}-${title}.pdf  (${pages}쪽)`);

  // ---------------------------------------------------------------- 배포 묶음
  // 원본 HTML(치환 전)이 참조하는 에셋만 골라 상대 경로 그대로 담는다.
  // 경로를 다시 쓰지 않으므로 링크가 깨질 여지가 없다.
  const raw = readFileSync(src, "utf8");
  const refs = [...new Set(
    [...raw.matchAll(/(?:\.\.\/)+([a-zA-Z0-9_/.-]+\.(?:svg|png|jpg|mp4|css|js))/g)]
      .map((m) => m[0])
  )];

  const stage = path.join(ROOT, "build_tmp", `w${wk}-slides`);
  rmSync(path.join(ROOT, "build_tmp"), { recursive: true, force: true });

  const deckDir = path.join(stage, "slides", `w${wk}`);
  mkdirSync(deckDir, { recursive: true });
  copyFileSync(src, path.join(deckDir, "index.html"));

  let missing = 0;
  for (const rel of refs) {
    const abs = path.resolve(path.dirname(src), rel);
    if (!existsSync(abs)) { console.warn(`    ! 없는 에셋: ${rel}`); missing++; continue; }
    const dest = path.resolve(deckDir, rel);
    mkdirSync(path.dirname(dest), { recursive: true });
    copyFileSync(abs, dest);
  }

  writeFileSync(path.join(stage, "index.html"),
    `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>${wk}주차 슬라이드 — 컴퓨터그래픽스</title>
<meta http-equiv="refresh" content="0; url=slides/w${wk}/index.html">
<style>body{background:#0b0d12;color:#e8ecf4;font-family:system-ui,sans-serif;
padding:4em;line-height:1.8}a{color:#35d6e6}</style></head><body>
<p>슬라이드로 이동 중…</p>
<p>자동으로 넘어가지 않으면 <a href="slides/w${wk}/index.html">여기를 클릭</a></p>
</body></html>\n`, "utf8");

  writeFileSync(path.join(stage, "READ-ME.txt"),
    "﻿" +
    `컴퓨터그래픽스 (VF3500076) · ${wk}주차 인터랙티브 슬라이드\n` +
    `조성호 · 2026학년도 2학기\n\n` +
    `[여는 법]\n이 폴더의  index.html  더블클릭 (Chrome / Edge 권장)\n\n` +
    `[PDF 와의 차이]\n` +
    `직접 조작하는 3D 데모와 애니메이션 포함\n` +
    `PDF 에서는 안내 카드로만 표시되는 부분\n\n` +
    `[조작]\n` +
    `  방향키 / 스페이스    다음·이전 슬라이드\n` +
    `  ESC                 전체 슬라이드 한눈에 보기\n` +
    `  S                   발표자 노트\n` +
    `  3D 화면 마우스 드래그 시 시점 회전\n\n` +
    `[주의]\n인터넷 연결 필요 (폰트와 3D 라이브러리를 온라인에서 불러옴)\n\n` +
    `[문의]\nseongho.cho@kodekorea.kr\n`, "utf8");

  const zip = path.join(ROOT, "dist", `w${wk}-interactive-slides.zip`);
  // 내부 경로는 ASCII 로만 둔다 — Compress-Archive 가 한글 경로를
  // 시스템 코드페이지로 써서 다른 PC 에서 폴더명이 깨지는 것을 막는다.
  execFileSync("powershell", ["-NoProfile", "-Command",
    `Compress-Archive -Path '${stage}' -DestinationPath '${zip}' -Force`],
    { stdio: ["ignore", "ignore", "inherit"] });
  rmSync(path.join(ROOT, "build_tmp"), { recursive: true, force: true });
  console.log(`  ✓ dist/w${wk}-interactive-slides.zip  (에셋 ${refs.length - missing}개)`);
}

console.log("\n완료.");
