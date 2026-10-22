"""Encode the rendered slides as H.264 MP4s that PowerPoint plays.

Reads <outdir>/plan.json and <outdir>/raw/<id>.mkv from render_videos.js and writes
<outdir>/video/NN_<id>.mp4: the transition into the slide and its run, ending on the
frame the slide then rests on. Slides that keep moving also get NN_<id>_loop.mp4,
which starts on that same frame and loops without a seam: its last moments crossfade
into the moments just before its first frame.

Usage: python3 encode_videos.py <outdir> [crf]
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT = Path(sys.argv[1])
CRF = sys.argv[2] if len(sys.argv) > 2 else "22"
# 1080p, 4:2:0, BT.709 limited range: what PowerPoint's decoders expect
ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", CRF, "-tune", "animation",
       "-profile:v", "high", "-level", "4.1", "-colorspace", "bt709", "-color_primaries", "bt709",
       "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart", "-an"]
TO_YUV = "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"


def frames(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, check=True)
    return int(r.stdout.strip())


def encode(r):
    raw, vid = OUT / "raw" / f"{r['id']}.mkv", OUT / "video"
    stem = f"{r['i'] + 1:02d}_{r['id']}"
    fps, n_end = r["fps"], r["nEnd"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf",
                    f"trim=end_frame={n_end + 1},setpts=PTS-STARTPTS,{TO_YUV}", *ENC,
                    str(vid / f"{stem}.mp4")], check=True)
    out = [(f"{stem}.mp4", n_end + 1)]
    if r["loop"]:
        n_p, n_x = r["nP"], r["nX"]
        graph = (f"[0:v]split[a][b];"
                 f"[a]trim=start_frame={n_end}:end_frame={n_end + n_p},setpts=PTS-STARTPTS[s];"
                 f"[b]trim=start_frame={n_end - n_x}:end_frame={n_end},setpts=PTS-STARTPTS[t];"
                 f"[s][t]xfade=transition=fade:duration={n_x / fps:.4f}:offset={(n_p - n_x) / fps:.4f},{TO_YUV}[o]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-filter_complex", graph,
                        "-map", "[o]", *ENC, str(vid / f"{stem}_loop.mp4")], check=True)
        out.append((f"{stem}_loop.mp4", n_p))
    for name, want in out:
        got = frames(vid / name)
        if got != want:
            raise SystemExit(f"{name}: {got} frames, expected {want}")
    return [(name, (vid / name).stat().st_size) for name, _ in out]


if __name__ == "__main__":
    (OUT / "video").mkdir(exist_ok=True)
    plan = json.loads((OUT / "plan.json").read_text())
    with ThreadPoolExecutor(max_workers=2) as pool:
        done = list(pool.map(encode, plan))
    total = 0
    for files in done:
        for name, size in files:
            total += size
            print(f"{name:24s} {size / 1e6:6.2f} MB")
    print(f"total {total / 1e6:.1f} MB")
