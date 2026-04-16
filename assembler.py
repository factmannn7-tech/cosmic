"""
Video assembly utilities:
  loop_video   — extends a short clip to a target duration by stream-looping
  normalize    — re-encodes any clip to standard 1920x1080 H.264 30fps
  concatenate  — joins all final clips into one output file
"""

import subprocess
import pathlib
from config import OUTPUT_WIDTH, OUTPUT_HEIGHT, FPS


def _run(cmd: list[str], label: str = "") -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed{' (' + label + ')' if label else ''}:\n{result.stderr[-800:]}")


def loop_video(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    duration: float,
) -> pathlib.Path:
    scale = f"scale={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:force_original_aspect_ratio=decrease,pad={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:(ow-iw)/2:(oh-ih)/2"
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", str(input_path),
        "-t", str(duration),
        "-vf", scale,
        "-r", str(FPS),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        str(output_path),
    ]
    _run(cmd, "loop")
    return output_path


def concatenate(
    clip_paths: list[pathlib.Path],
    output_path: pathlib.Path,
) -> pathlib.Path:
    filelist = output_path.parent / "_filelist.txt"
    filelist.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in clip_paths)
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(filelist),
        "-c", "copy",
        str(output_path),
    ]
    _run(cmd, "concat")
    filelist.unlink(missing_ok=True)
    return output_path
