"""Flow 원본(raw/*.png) → 슬라이드용 JPG (figures/flow/*.jpg)

- 오른쪽 아래 Flow 표식 크롭
- 배경색을 지면색(#f5f1e8)에 맞춤 → PDF·화면 모두 네모 경계 제거
- 가장자리 페이드

실행 : .venv/Scripts/python.exe dataliteracy/figures/flow_prepare.py [이름 접두어...]
예   : ... flow_prepare.py d09  → d09-*.png 만 처리
"""
import pathlib
import sys
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).parent / "flow"
PAPER = np.array([245, 241, 232], dtype=float)
CROP = 64


def prepare(src):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    crop = round(CROP * W / 1376)  # 표식 크기는 해상도에 비례 (1K 원본 기준 64px)
    im = im.crop((0, 0, W - crop, H - crop)).resize((1240, round(1240 * (H - crop) / (W - crop))), Image.LANCZOS)
    a = np.asarray(im, dtype=float)
    h, w, _ = a.shape
    border = np.concatenate([a[:24].reshape(-1, 3), a[-24:].reshape(-1, 3), a[:, :24].reshape(-1, 3), a[:, -24:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    a = np.clip(a * (PAPER / bg), 0, 255)
    # 배경에 가까운 픽셀은 지면색으로 수렴 (거리 12 이하 완전 · 32 까지 점진)
    dist = np.sqrt(((a - PAPER) ** 2).sum(2))
    t = np.clip((dist - 12) / 20, 0, 1)[..., None]
    a = PAPER * (1 - t) + a * t
    # 가장자리 페이드 (폭 3%)
    m = int(w * .03)
    ramp_x = np.minimum(np.arange(w), np.arange(w)[::-1]) / m
    ramp_y = np.minimum(np.arange(h), np.arange(h)[::-1]) / m
    e = np.clip(np.minimum.outer(ramp_y, ramp_x), 0, 1)[..., None]
    a = PAPER * (1 - e) + a * e
    Image.fromarray(a.astype("uint8")).save(HERE / (src.stem + ".jpg"), quality=88, optimize=True, subsampling=0)


prefixes = tuple(sys.argv[1:])
for f in sorted((HERE / "raw").glob("*.png")):
    if prefixes and not f.stem.startswith(prefixes):
        continue
    prepare(f)
    print(f.stem)
