"""
Breaks a parsed script into individual scenes, each with:
  - section  : e.g. "IDENTIFICATION"
  - text     : the script paragraph(s) for that scene
  - prompt   : the Veo video-generation prompt
"""

from dataclasses import dataclass, field
from script_generator import generate_video_prompt, parse_sections
from config import SCRIPT_SECTIONS


@dataclass
class Scene:
    index: int
    section: str
    text: str
    prompt: str = field(default="")


def build_scenes(script: str, generate_prompts: bool = True) -> list[Scene]:
    sections = parse_sections(script)

    # Preserve canonical section order; skip any not present in script
    ordered = [s for s in SCRIPT_SECTIONS if s in sections]

    scenes: list[Scene] = []
    for i, section in enumerate(ordered):
        text = sections[section]
        scene = Scene(index=i, section=section, text=text)
        if generate_prompts:
            scene.prompt = generate_video_prompt(section, text)
        scenes.append(scene)

    return scenes
