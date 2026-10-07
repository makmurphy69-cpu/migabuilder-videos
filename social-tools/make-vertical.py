"""Make a 720x1280, 30 fps vertical video for TikTok/Shorts from a tool's tutorial video.

Usage: python3 social-tools/make-vertical.py <tool> "<subtitle>"
Reads https://videos.migabuilder.com/<tool>.mp4 and writes social/<tool>-tiktok.mp4.
TikTok rejects videos below 23 fps, so the output is always 30 fps.
"""
import subprocess, sys, tempfile, textwrap, os

tool, sub = sys.argv[1], sys.argv[2]
src = os.path.join(tempfile.mkdtemp(), f"{tool}.mp4")
subprocess.run(["curl", "-sSf", "-o", src, f"https://videos.migabuilder.com/{tool}.mp4"], check=True)
lines = textwrap.wrap(sub, 28)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
dt = []
y0 = 170 - (len(lines) - 1) * 24
for i, l in enumerate(lines):
    l = l.replace("'", "’").replace(":", "\\:")
    dt.append(f"drawtext=fontfile={F}:text='{l}':fontcolor=white:fontsize=34:x=(w-text_w)/2:y={y0 + i * 48}")
dt.append(f"drawtext=fontfile={F}:text='MigaBuilder.com':fontcolor=0x5CC8E0:fontsize=38:x=(w-text_w)/2:y=1045")
fc = "[1:v]fps=30,scale=720:405:flags=lanczos[v];[0:v][v]overlay=0:440:shortest=1," + ",".join(dt) + ",format=yuv420p[o]"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "social", f"{tool}-tiktok.mp4")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x102941:s=720x1280:r=30", "-i", src,
                "-filter_complex", fc, "-map", "[o]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out], check=True)
print(out)
