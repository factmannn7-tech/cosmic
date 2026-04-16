#!/usr/bin/env python3
"""
Cosmic Video Script Generator
Usage:
    python main.py generate --topic "fear of starting over"
    python main.py generate --topic "fear of starting over" --script-only
    python main.py generate --topic "fear of starting over" --output my_video
"""

import json
import pathlib

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.text import Text

from script_generator import generate_script
from scene_parser import build_scenes
from video_generator import generate_all_videos

console = Console()


@click.group()
def cli():
    """Cosmic — Video script generator powered by Gemini + Veo 3 Fast."""


@cli.command()
@click.option("--topic", "-t", required=True, help="Topic for the video script.")
@click.option("--output", "-o", default="output", show_default=True, help="Output directory for videos.")
@click.option("--script-only", is_flag=True, default=False, help="Generate script only, skip video rendering.")
@click.option("--save-script", is_flag=True, default=True, help="Save script + prompts as JSON alongside videos.")
def generate(topic: str, output: str, script_only: bool, save_script: bool):
    """Generate a video script and (optionally) render videos for a given TOPIC."""

    console.print()
    console.print(Panel.fit(
        f"[bold white]Topic:[/bold white] [cyan]{topic}[/cyan]",
        title="[bold magenta]Cosmic Video Generator[/bold magenta]",
        border_style="magenta",
    ))
    console.print()

    # ── Step 1: Script ────────────────────────────────────────────────────────
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
        task = prog.add_task("Writing script with Gemini…", total=None)
        script = generate_script(topic)
        prog.update(task, completed=True)

    console.print(Rule("[bold green]Generated Script[/bold green]"))
    console.print(Text(script, style="dim white"))
    console.print()

    # ── Step 2: Parse scenes + generate visual prompts ────────────────────────
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
        task = prog.add_task("Building scenes & visual prompts…", total=None)
        scenes = build_scenes(script, generate_prompts=True)
        prog.update(task, completed=True)

    console.print(Rule("[bold blue]Scene Prompts[/bold blue]"))
    for scene in scenes:
        console.print(f"[bold yellow]{scene.index + 1}. {scene.section}[/bold yellow]")
        console.print(f"   [italic dim]{scene.prompt}[/italic dim]")
    console.print()

    # ── Step 3: Save manifest ─────────────────────────────────────────────────
    if save_script:
        out_dir = pathlib.Path(output)
        out_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "topic": topic,
            "script": script,
            "scenes": [
                {"index": s.index, "section": s.section, "text": s.text, "prompt": s.prompt}
                for s in scenes
            ],
        }
        manifest_path = out_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        console.print(f"[green]Manifest saved →[/green] {manifest_path}")

    if script_only:
        console.print("[yellow]--script-only flag set. Skipping video rendering.[/yellow]")
        return

    # ── Step 4: Generate videos ───────────────────────────────────────────────
    console.print(Rule("[bold red]Rendering Videos (Veo 3 Fast)[/bold red]"))
    console.print(f"[dim]Generating {len(scenes)} clips × 8 seconds each…[/dim]\n")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
        task = prog.add_task(f"Rendering scene 1 / {len(scenes)}…", total=len(scenes))
        all_paths = []
        from video_generator import generate_video_for_scene
        import pathlib as _pl
        out_dir = _pl.Path(output)
        out_dir.mkdir(parents=True, exist_ok=True)
        for scene in scenes:
            prog.update(task, description=f"Rendering scene {scene.index + 1} / {len(scenes)}: {scene.section}…")
            paths = generate_video_for_scene(scene, out_dir)
            all_paths.extend(paths)
            prog.advance(task)

    console.print()
    console.print(Rule("[bold green]Done[/bold green]"))
    for p in all_paths:
        console.print(f"  [green]✓[/green] {p}")
    console.print()
    console.print(f"[bold green]{len(all_paths)} video clip(s) saved to [cyan]{output}/[/cyan][/bold green]")


if __name__ == "__main__":
    cli()
