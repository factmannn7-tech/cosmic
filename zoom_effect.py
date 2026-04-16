"""
Applies a slow Ken Burns zoom-in effect to a static image using ffmpeg.
Produces a smooth, cinematic 1.0→1.08x zoom over the full duration.
"""

import subprocess
import pathlib
from config import OUTPUT_WIDTH, OUTPUT_HEIGHT, FPS


def apply_ken_burns(
    image_path: pathlib.Path,
    output_path: pathlib.Path,
    duration: float,
) -> pathlib.Path:
    frames = max(1, int(duration * FPS))
    size = f"{OUTPUT_WIDTH}x{OUTPUT_HEIGHT}"

    # Zoom from 1.0 to 1.08 linearly — subtle, cinematic
    zoom_filter = (
        f"zoompan="
        f"z='1+0.08*(on/{frames})':"
        f"x='iw/2-(iw/zoom/2)':"
        f"y='ih/2-(ih/zoom/2)':"
        f"d={frames}:"
        f"s={size}:"
        f"fps={FPS}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-vf", zoom_filter,
        "-t", str(duration),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg zoom failed:\n{result.stderr[-800:]}")
    return output_path
