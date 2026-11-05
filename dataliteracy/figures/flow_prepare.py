"""Flow 원본(raw/*.png) → 슬라이드용 JPG (figures/flow/*.jpg)

- 오른쪽 아래 Flow 표식 크롭
- 배경색을 지면색(#f5f1e8)에 맞춤 → PDF·화면 모두 네모 경계 제거
- 가장자리 페이드

실행 : .venv/Scripts/python.exe dataliteracy/figures/flow_prepare.py
"""
import pathlib
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).parent / "flow"
PAPER = np.array([245, 241, 232], dtype=float)
CROP = 64


def prepare(src):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    im = im.crop((0, 0, W - CROP, H - CROP)).resize((1240, round(1240 * (H - CROP) / (W - CROP))), Image.LANCZOS)
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


for f in sorted((HERE / "raw").glob("*.png")):
    prepare(f)
    print(f.stem)
