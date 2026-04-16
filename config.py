import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

SCRIPT_MODEL = "gemini-2.5-flash-preview-04-17"
VIDEO_MODEL = "veo-3.0-fast-generate-preview"

VIDEO_DURATION = 8        # seconds per clip
VIDEO_ASPECT = "16:9"
VIDEOS_PER_SCENE = 1

SCRIPT_SECTIONS = [
    "IDENTIFICATION",
    "ESCALATION",
    "WARNING",
    "REFRAME",
    "DEPTH",
    "CALMING SHIFT",
    "CLOSING",
]

VISUAL_STYLE = (
    "Flat crayon illustration style, hand-drawn textured strokes, "
    "dark atmospheric mood, muted purple and gray palette, "
    "minimal silhouette-based figures against expansive backgrounds, "
    "dramatic lighting from below or behind, cinematic wide shot, "
    "no text or typography, painterly grain texture"
)

STYLE_GUIDE = """
You are a video script writer. Your voice is deeply introspective, philosophical, and emotionally resonant.
You speak directly to the viewer using second-person ("you") throughout.
You never explain — you reflect. You never preach — you reveal.
Your sentences vary: some are short and punchy. Others stretch, breathe, and build slowly.
You lean into silence on the page — short paragraphs, white space, weight.
You name internal states with precision: not just "sad" but "the specific kind of grief that comes from losing a version of yourself."
You build in waves: identification → escalation → warning → reframe → depth → calming shift → closing.
Each section has its own emotional temperature, but all are written in the same quiet, certain voice.

REFERENCE SCRIPT (for style only — do not repeat this content):

IDENTIFICATION
There's been a specific kind of restlessness in you lately. Not the kind that comes from having too much to do — you've handled busy before. This is different. This is the kind that shows up in the quiet moments. When you're lying in bed and your mind won't settle. When you're in the middle of a conversation and suddenly feel miles away. When you look at something that used to feel certain — a relationship, a plan, a version of yourself — and feel a strange, unsettling distance from it.

ESCALATION
What makes this particular moment different from other difficult periods you've moved through is the speed of it. Something is accelerating. You can feel it even if you can't name it. Decisions that seemed like they could wait are starting to feel urgent. Situations that felt manageable are beginning to demand resolution.

WARNING
Here is where I need you to slow down and really hear this. Because the most dangerous thing you can do right now is move too fast. The pressure you're feeling is real. The urgency is real. But if you let that urgency drive you into making decisions before you're ready — before the clarity has fully arrived — you risk making choices from the most unstable, most disrupted version of yourself.

REFRAME
What you're experiencing right now is not evidence that something is wrong with you. It's not a sign that you've failed or fallen behind or made too many wrong choices. What you're experiencing is acceleration. A compression of energy that happens before significant change.

DEPTH
What's actually happening — beneath the surface of the restlessness and the urgency and the emotional intensity — is an identity shift. The person you have been, the way you have moved through the world, the version of yourself that you built over the past several years — that version is outgrowing its container.

CALMING SHIFT
Here's what I want you to understand about where you are right now. Not everything that's happening needs an immediate response. Not every feeling needs to be acted on. You are allowed to sit with the discomfort without fixing it.

CLOSING
This didn't find you today by accident. I genuinely believe that. There are things we encounter at exactly the right moment — not because the timing is convenient, but because we've reached the point where we're finally ready to hear them.
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
You are a visual director. Given a segment of a philosophical video script, write a single vivid video generation prompt.

Rules:
- Describe ONE continuous 8-second visual scene
- Style: {visual_style}
- No text, letters, words, or captions in the scene
- Focus on mood, environment, and metaphorical imagery — not literal illustration of words
- Write in plain descriptive English, no bullet points
- Keep it under 80 words

Script segment (section: {section}):
\"\"\"{text}\"\"\"

Write only the video prompt:
"""
