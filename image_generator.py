"""
Generates a single 16:9 image via Google Imagen 3 and saves it as PNG.
"""

import pathlib
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, IMAGE_MODEL


def generate_image(prompt: str, output_path: pathlib.Path) -> pathlib.Path:
    client = genai.Client(api_key=GEMINI_API_KEY)
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
