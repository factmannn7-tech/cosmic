"""
Generates 8-second video clips via Gemini Veo 3 Fast for each scene,
saves them to an output directory, and returns the file paths.
"""

import time
import pathlib
from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    VIDEO_MODEL,
    VIDEO_DURATION,
    VIDEO_ASPECT,
    VIDEOS_PER_SCENE,
)
from scene_parser import Scene


_POLL_INTERVAL = 20   # seconds between status checks
_MAX_POLLS = 90       # 30 minutes max wait per scene


def _client() -> genai.Client:
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_video_for_scene(
    scene: Scene,
    output_dir: pathlib.Path,
) -> list[pathlib.Path]:
    """
    Calls Veo 3 Fast, polls until done, saves the mp4, returns path list.
    """
    client = _client()

    operation = client.models.generate_videos(
        model=VIDEO_MODEL,
        prompt=scene.prompt,
        config=types.GenerateVideosConfig(
            aspect_ratio=VIDEO_ASPECT,
            duration_seconds=VIDEO_DURATION,
            number_of_videos=VIDEOS_PER_SCENE,
        ),
    )

    for _ in range(_MAX_POLLS):
        if operation.done:
            break
        time.sleep(_POLL_INTERVAL)
        operation = client.operations.get(operation)
    else:
        raise TimeoutError(f"Scene {scene.index} ({scene.section}) timed out after polling.")

    saved: list[pathlib.Path] = []
    for vid_idx, generated in enumerate(operation.response.generated_videos):
        client.files.download(file=generated.video)
        filename = output_dir / f"scene_{scene.index:02d}_{scene.section.replace(' ', '_')}_{vid_idx}.mp4"
        generated.video.save(str(filename))
        saved.append(filename)

    return saved


def generate_all_videos(
    scenes: list[Scene],
    output_dir: str | pathlib.Path = "output",
) -> list[pathlib.Path]:
    out = pathlib.Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    all_paths: list[pathlib.Path] = []
    for scene in scenes:
        paths = generate_video_for_scene(scene, out)
        all_paths.extend(paths)

    return all_paths
