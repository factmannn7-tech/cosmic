"""
Main pipeline: script → segments → media → final 15-minute video.

Flow per segment:
  HIGH intensity  →  Veo 3.1 Fast (8 s raw clip)  →  loop to duration
  LOW  intensity  →  Imagen image                  →  Ken Burns zoom to duration
  All segments concatenated into final_video.mp4
"""

import json
import pathlib
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.rule import Rule

from script_splitter import split_script
from image_generator import generate_image
from video_generator import generate_video_clip
from zoom_effect import apply_ken_burns
from assembler import loop_video, concatenate

console = Console()


def run_pipeline(script: str, output_dir: str | pathlib.Path = "output") -> pathlib.Path:
    out = pathlib.Path(output_dir)
    segments_dir = out / "segments"
    segments_dir.mkdir(parents=True, exist_ok=True)

    # ── 1. Split & classify ───────────────────────────────────────────────────
    console.print(Rule("[bold cyan]Step 1 / 4 — Splitting script into segments[/bold cyan]"))
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as prog:
        t = prog.add_task("Analysing emotional intensity…", total=None)
        segments = split_script(script)
        prog.update(t, completed=True)

    total_duration = sum(s["duration"] for s in segments)
    console.print(f"  [green]✓[/green] {len(segments)} segments · "
                  f"[yellow]{sum(1 for s in segments if s['intensity']=='HIGH')}[/yellow] Veo (HIGH) · "
                  f"[blue]{sum(1 for s in segments if s['intensity']=='LOW')}[/blue] Imagen (LOW) · "
                  f"total [white]{total_duration/60:.1f} min[/white]")

    # Save manifest
    manifest = {"segments": segments, "total_duration_seconds": total_duration}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    # ── 2. Generate media ─────────────────────────────────────────────────────
    console.print(Rule("[bold cyan]Step 2 / 4 — Generating media[/bold cyan]"))

    final_clips: list[pathlib.Path] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as prog:
        task = prog.add_task("Processing segments…", total=len(segments))

        for seg in segments:
            idx      = seg["index"]
            dur      = seg["duration"]
            prompt   = seg["prompt"]
            intensity = seg["intensity"]
            section  = seg["section"]

            prog.update(task, description=f"[{idx+1}/{len(segments)}] {section} ({intensity}) — {dur:.0f}s")

            if intensity == "HIGH":
                raw_mp4 = segments_dir / f"seg_{idx:03d}_veo_raw.mp4"
                generate_video_clip(prompt, raw_mp4)
                final_clip = segments_dir / f"seg_{idx:03d}_final.mp4"
                loop_video(raw_mp4, final_clip, dur)
            else:
                img_path = segments_dir / f"seg_{idx:03d}_img.png"
                generate_image(prompt, img_path)
                final_clip = segments_dir / f"seg_{idx:03d}_final.mp4"
                apply_ken_burns(img_path, final_clip, dur)

            final_clips.append(final_clip)
            prog.advance(task)

    # ── 3. Concatenate ────────────────────────────────────────────────────────
    console.print(Rule("[bold cyan]Step 3 / 4 — Assembling final video[/bold cyan]"))
    final_video = out / "final_video.mp4"
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as prog:
        t = prog.add_task(f"Concatenating {len(final_clips)} clips…", total=None)
        concatenate(final_clips, final_video)
        prog.update(t, completed=True)

    console.print(Rule("[bold green]Step 4 / 4 — Done[/bold green]"))
    console.print(f"\n  [bold green]Final video →[/bold green] [cyan]{final_video}[/cyan]")
    console.print(f"  Duration    : [white]{total_duration/60:.1f} minutes[/white]")
    console.print(f"  Clips used  : {len(final_clips)}\n")

    return final_video
