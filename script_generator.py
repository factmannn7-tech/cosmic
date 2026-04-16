import re
from google import genai
from config import (
    GEMINI_API_KEY,
    SCRIPT_MODEL,
    SCRIPT_SECTIONS,
    SCRIPT_PROMPT_TEMPLATE,
    SCENE_PROMPT_TEMPLATE,
    STYLE_GUIDE,
    VISUAL_STYLE,
)


def _client() -> genai.Client:
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_script(topic: str) -> str:
    prompt = SCRIPT_PROMPT_TEMPLATE.format(
        style_guide=STYLE_GUIDE,
        topic=topic,
    )
    client = _client()
    response = client.models.generate_content(
        model=SCRIPT_MODEL,
        contents=prompt,
    )
    return response.text.strip()


def parse_sections(script: str) -> dict[str, str]:
    """Split script text into a dict keyed by section name."""
    sections: dict[str, str] = {}
    pattern = r"^(" + "|".join(re.escape(s) for s in SCRIPT_SECTIONS) + r")\s*$"
    current_section = None
    buffer: list[str] = []

    for line in script.splitlines():
        if re.match(pattern, line.strip(), re.IGNORECASE):
            if current_section and buffer:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = line.strip().upper()
            buffer = []
        else:
            if current_section is not None:
                buffer.append(line)

    if current_section and buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections


def generate_video_prompt(section: str, text: str) -> str:
    prompt = SCENE_PROMPT_TEMPLATE.format(
        visual_style=VISUAL_STYLE,
        section=section,
        text=text[:600],
    )
    client = _client()
    response = client.models.generate_content(
        model=SCRIPT_MODEL,
        contents=prompt,
    )
    return response.text.strip()
