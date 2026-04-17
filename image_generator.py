"""
Generates a single 16:9 image via Google Imagen 4 and saves it as PNG.
"""

import time
import pathlib
from google import genai
from google.genai import types, errors as genai_errors
from config import GEMINI_API_KEY, IMAGE_MODEL


def generate_image(prompt: str, output_path: pathlib.Path, max_retries: int = 5) -> pathlib.Path:
    client = genai.Client(api_key=GEMINI_API_KEY)
    for attempt in range(max_retries):
        try:
            response = client.models.generate_images(
                model=IMAGE_MODEL,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="16:9",
                ),
            )
            img = response.generated_images[0].image
            img.save(str(output_path))
            return output_path
        except (genai_errors.ServerError, Exception) as e:
            if attempt == max_retries - 1:
                raise
            wait = 15 * (attempt + 1)
            print(f"\n  [imagen retry {attempt+1}/{max_retries}] {str(e)[:80]} — {wait}s…")
            time.sleep(wait)
