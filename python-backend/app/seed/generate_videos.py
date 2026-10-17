import os
import shutil
import subprocess

BASE_DIR = r"d:\lumea"
IMG_DIR = os.path.join(BASE_DIR, "frontend", "public", "images")
OUT_DIRS = [
    os.path.join(BASE_DIR, "frontend", "public", "videos"),
    os.path.join(BASE_DIR, "admin", "public", "videos"),
    os.path.join(BASE_DIR, "python-backend", "uploads", "videos"),
]

for d in OUT_DIRS:
    os.makedirs(d, exist_ok=True)

# List of vertical reels (720x1280) and horizontal films (1280x720)
CLIPS = [
    {
        "filename": "reel-sk2-texture.mp4",
        "img": "pdp-stage-sk2-hero.jpg",
        "width": 720,
        "height": 1280,
        "duration": 5,
        "zoom": "1.08"
    },
    {
        "filename": "reel-boj-sunscreen.mp4",
        "img": "article-thumb-sunscreen.jpg",
        "width": 720,
        "height": 1280,
        "duration": 5,
        "zoom": "1.10"
    },
    {
        "filename": "reel-snail-mucin.mp4",
        "img": "prod-cosrx.jpg",
        "width": 720,
        "height": 1280,
        "duration": 5,
        "zoom": "1.08"
    },
    {
        "filename": "reel-centella-ampoule.mp4",
        "img": "article-thumb-centella.jpg",
        "width": 720,
        "height": 1280,
        "duration": 5,
        "zoom": "1.10"
    },
    {
        "filename": "reel-niacinamide-glow.mp4",
        "img": "article-thumb-niacinamide.jpg",
        "width": 720,
        "height": 1280,
        "duration": 5,
        "zoom": "1.10"
    },
    {
        "filename": "reel-restorative-sleep.mp4",
        "img": "article-thumb-sleep.jpg",
        "width": 720,
        "height": 1280,
        "duration": 5,
        "zoom": "1.10"
    },
    {
        "filename": "brand-story-sk2.mp4",
        "img": "pdp-model-radiant.jpg",
        "width": 1280,
        "height": 720,
        "duration": 6,
        "zoom": "1.06"
    },
    {
        "filename": "brand-story-boj.mp4",
        "img": "prod-sunscreen-rice.jpg",
        "width": 1280,
        "height": 720,
        "duration": 6,
        "zoom": "1.06"
    }
]

primary_out_dir = OUT_DIRS[0]

for clip in CLIPS:
    img_path = os.path.join(IMG_DIR, clip["img"])
    if not os.path.exists(img_path):
        # Fallback to another image if missing
        img_path = os.path.join(IMG_DIR, "pdp-model-radiant.jpg")
    
    out_file = os.path.join(primary_out_dir, clip["filename"])
    w = clip["width"]
    h = clip["height"]
    d = clip["duration"]
    
    # FFmpeg command: loop image for d seconds, scale & crop with subtle ken-burns zoom
    vf = f"scale={w*2}:{h*2}:force_original_aspect_ratio=increase,crop={w*2}:{h*2},zoompan=z='min(zoom+0.001,{clip['zoom']})':d={d*25}:s={w}x{h}:fps=25,format=yuv420p"
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", img_path,
        "-t", str(d),
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        out_file
    ]
    
    print(f"Generating {clip['filename']}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        sz = os.path.getsize(out_file)
        print(f"  [OK] Created {clip['filename']} ({sz // 1024} KB)")
        # Copy to the other output directories
        for target_dir in OUT_DIRS[1:]:
            shutil.copy2(out_file, os.path.join(target_dir, clip["filename"]))
    else:
        print(f"  [ERROR] Failed {clip['filename']}: {res.stderr[:200]}")

print("\nVideo asset generation and synchronization complete!")
