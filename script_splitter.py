"""
Splits a provided script into timed segments, classifies each as
HIGH (→ Veo video) or LOW (→ Imagen image + Ken Burns), and generates
a visual prompt for each segment.

Output per segment:
  index        int
  section      str   e.g. "IDENTIFICATION"
  text         str   the script paragraph(s)
  words        int
  duration     float seconds (text / WPM * 60, min 8 s)
  intensity    "HIGH" | "LOW"
  prompt       str   visual prompt for Imagen or Veo
"""

import json
import re
import time
from google import genai
from google.genai import errors as genai_errors
from config import (
    GEMINI_API_KEY,
    SCRIPT_MODEL,
    VISUAL_STYLE,
    WPM,
    HIGH_INTENSITY_SECTIONS,
)

_SPLITTER_PROMPT = """
You are a video editor analyzing a philosophical narration script.

Your job:
1. Split the script into segments of 60–120 words each (split at sentence boundaries only).
2. Assign each segment to its section (IDENTIFICATION, ESCALATION, WARNING, REFRAME, DEPTH, CALMING SHIFT, CLOSING, or INTRO for text before the first header).
3. Classify intensity:
   - HIGH: emotionally intense, revelatory, dramatic, urgent, or grief-filled moments
   - LOW: reflective, transitional, explanatory, or calming moments
4. Write ONE visual scene prompt per segment in this style:
   {visual_style}
   The prompt must be under 80 words, no text/letters in scene, metaphorical imagery.

Return ONLY a JSON array. No explanation, no markdown fences. Example shape:
[
  {{
    "index": 0,
    "section": "INTRO",
    "text": "...",
    "intensity": "LOW",
    "prompt": "..."
  }}
]

SCRIPT:
\"\"\"
{script}
\"\"\"
"""


def _generate_with_retry(client, model, contents, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(model=model, contents=contents)
        except (genai_errors.ServerError, Exception) as e:
            if attempt == max_retries - 1:
                raise
            wait = 15 * (attempt + 1)
            print(f"\n  [retry {attempt+1}/{max_retries}] {e!s:.80} — waiting {wait}s…")
            time.sleep(wait)


def split_script(script: str) -> list[dict]:
    prompt = _SPLITTER_PROMPT.format(
        visual_style=VISUAL_STYLE,
        script=script.strip(),
    )
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = _generate_with_retry(client, SCRIPT_MODEL, prompt)
    raw = response.text.strip()

    # Strip markdown fences if Gemini wrapped the JSON
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    segments: list[dict] = json.loads(raw)

    for seg in segments:
        seg["words"] = len(seg["text"].split())
        seg["duration"] = max(8.0, round(seg["words"] / WPM * 60, 1))
        # Override intensity for known high-intensity sections
        if seg.get("section", "").upper() in HIGH_INTENSITY_SECTIONS:
            seg["intensity"] = "HIGH"

    return segments
