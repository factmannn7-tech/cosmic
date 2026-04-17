"""
Generates an 8-second video clip via Gemini Veo 3.1 Fast and saves as mp4.
"""

import time
import pathlib
from google import genai
from google.genai import types, errors as genai_errors
from config import GEMINI_API_KEY, VIDEO_MODEL, RAW_CLIP_DURATION, VIDEO_ASPECT

_POLL_INTERVAL = 20
_MAX_POLLS = 90


def generate_video_clip(prompt: str, output_path: pathlib.Path, max_retries: int = 5) -> pathlib.Path:
    client = genai.Client(api_key=GEMINI_API_KEY)

    for attempt in range(max_retries):
        try:
            operation = client.models.generate_videos(
                model=VIDEO_MODEL,
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio=VIDEO_ASPECT,
                    duration_seconds=RAW_CLIP_DURATION,
                    number_of_videos=1,
                ),
            )
            break
        except (genai_errors.ServerError, Exception) as e:
            if attempt == max_retries - 1:
                raise
            wait = 15 * (attempt + 1)
            print(f"\n  [veo retry {attempt+1}/{max_retries}] {str(e)[:80]} — {wait}s…")
            time.sleep(wait)

    for _ in range(_MAX_POLLS):
        if operation.done:
            break
        time.sleep(_POLL_INTERVAL)
        operation = client.operations.get(operation)
    else:
        raise TimeoutError(f"Veo timed out for prompt: {prompt[:60]}…")

    video = operation.response.generated_videos[0].video
    client.files.download(file=video)
    video.save(str(output_path))
    return output_path
