"""10·11주 애니메이션 렌더 + 포스터 추출 → figures/out/

실행 (저장소 루트) : .venv/Scripts/python.exe dataliteracy/figures/anim/render.py [장면 ...]
"""
import pathlib, shutil, subprocess, sys
import av

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "out"
MEDIA = HERE / "media"
SCENES = {
    "RandomBalance": "d10-random-balance",
    "NullDistribution": "d11-null-distribution",
    "CIStack": "d11-ci-stack",
    "Peeking": "d11-peeking-anim",
}

for sc in (sys.argv[1:] or SCENES):
    subprocess.run([sys.executable, "-m", "manim", "-r", "1600,900", "--fps", "30", "--progress_bar", "none", "-v", "WARNING",
                    "--media_dir", str(MEDIA), str(HERE / "d10_d11_anim.py"), sc], check=True)
    src = next(MEDIA.rglob(f"videos/d10_d11_anim/**/{sc}.mp4"))
    dst = OUT / f"{SCENES[sc]}.mp4"
    shutil.copy(src, dst)
    with av.open(str(dst)) as c:
        frame = None
        for frame in c.decode(video=0):
            pass
        frame.to_image().save(OUT / f"{SCENES[sc]}-poster.png")
    print(sc, "->", dst.name, dst.stat().st_size // 1024, "KB", round(float(frame.time), 1), "s")
