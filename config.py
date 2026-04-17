import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# ── Models ─────────────────────────────────────────────────────────────────────
SCRIPT_MODEL  = "gemini-2.0-flash"
VIDEO_MODEL   = "veo-3.1-fast-generate-preview"
IMAGE_MODEL   = "imagen-4.0-generate-001"

# ── Video / image settings ─────────────────────────────────────────────────────
RAW_CLIP_DURATION = 8      # Veo generates 8-second clips
VIDEO_ASPECT      = "16:9"
OUTPUT_WIDTH      = 1920
OUTPUT_HEIGHT     = 1080
FPS               = 30

# ── Narration pacing (words per minute) ────────────────────────────────────────
WPM = 130   # slow, contemplative narration pace

# ── Visual style (shared by Imagen + Veo prompts) ─────────────────────────────
VISUAL_STYLE = (
    "Flat crayon illustration style, childlike drawing, "
    "bold solid color blocks, crayon grain texture, "
    "no text or typography, camera still, melancholic mood, "
    "muted earth tones and deep grays, simple silhouette figures, "
    "wide establishing shot, quiet and contemplative atmosphere"
)

# ── Script sections (for topic-based generation, kept for script_generator) ───
SCRIPT_SECTIONS = [
    "IDENTIFICATION",
    "ESCALATION",
    "WARNING",
    "REFRAME",
    "DEPTH",
    "CALMING SHIFT",
    "CLOSING",
]

# ── HIGH-intensity sections → Veo video ───────────────────────────────────────
# LOW-intensity sections → Imagen image + Ken Burns zoom
HIGH_INTENSITY_SECTIONS = {"ESCALATION", "WARNING", "DEPTH"}

# ── Style guide for topic-based script generation ─────────────────────────────
STYLE_GUIDE = """
You are a video script writer. Your voice is deeply introspective, philosophical, and emotionally resonant.
You speak directly to the viewer using second-person ("you") throughout.
You never explain — you reflect. You never preach — you reveal.
Your sentences vary: some are short and punchy. Others stretch, breathe, and build slowly.
You lean into silence on the page — short paragraphs, white space, weight.
You name internal states with precision: not just "sad" but "the specific kind of grief that comes from losing a version of yourself."
You build in waves: identification → escalation → warning → reframe → depth → calming shift → closing.
Each section has its own emotional temperature, but all are written in the same quiet, certain voice.
"""

SCRIPT_PROMPT_TEMPLATE = """
{style_guide}

---

Now write a COMPLETE, ORIGINAL video script on the following topic: "{topic}"

Rules:
- Use EXACTLY these section headers (all caps, on their own line): IDENTIFICATION, ESCALATION, WARNING, REFRAME, DEPTH, CALMING SHIFT, CLOSING
- Each section should be 2–4 paragraphs
- Do NOT reference the example script or copy any phrases from it
- Write as if you are speaking directly to someone watching a video
- Maintain the same voice: intimate, certain, emotionally precise
- Output only the script — no meta-commentary, no titles, no explanations

Begin:
"""

SCENE_PROMPT_TEMPLATE = """
You are a visual director. Given a segment of a philosophical video script, write a single vivid visual prompt.

Rules:
- Style: {visual_style}
- No text, letters, words, or captions in the scene
- Focus on mood, environment, and metaphorical imagery — not literal illustration of words
- Write in plain descriptive English, no bullet points
- Keep it under 80 words

Script segment (section: {section}):
\"\"\"{text}\"\"\"

Write only the visual prompt:
"""
