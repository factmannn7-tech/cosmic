#!/usr/bin/env python3
"""
Cosmic Video Generator
======================
Usage:
  # Provide script as a text file:
  python main.py run --script script.txt

  # Pipe script inline:
  echo "my script text" | python main.py run --script -

  # Generate script from a topic first, then produce video:
  python main.py generate --topic "fear of starting over"
"""

import sys
import pathlib
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.text import Text

console = Console()


@click.group()
def cli():
    """Cosmic — AI video generator · Gemini Veo 3.1 Fast + Imagen 3."""


# ── run: produce video from a given script ────────────────────────────────────
@cli.command()
@click.option("--script", "-s", required=True,
              type=click.Path(exists=False, allow_dash=True),
              help="Path to .txt script file, or '-' to read from stdin.")
@click.option("--output", "-o", default="output", show_default=True,
              help="Output directory.")
def run(script: str, output: str):
    """
    Split SCRIPT, classify emotional intensity, generate Veo / Imagen media,
    apply Ken Burns to stills, and concatenate into a ~15-minute final video.
    """
    if script == "-":
        script_text = sys.stdin.read()
    else:
        script_text = pathlib.Path(script).read_text(encoding="utf-8")

    console.print()
    console.print(Panel.fit(
        f"Output → [cyan]{output}/[/cyan]",
        title="[bold magenta]Cosmic Video Generator[/bold magenta]",
        border_style="magenta",
    ))
    console.print()

    from pipeline import run_pipeline
    run_pipeline(script_text, output_dir=output)


# ── generate: write a script from a topic, then produce video ─────────────────
@cli.command()
@click.option("--topic", "-t", required=True, help="Topic for the video.")
@click.option("--output", "-o", default="output", show_default=True,
              help="Output directory.")
@click.option("--script-only", is_flag=True, default=False,
              help="Write script to file and exit (no video rendering).")
def generate(topic: str, output: str, script_only: bool):
    """Generate a script from TOPIC, then render the full video pipeline."""
    from script_generator import generate_script

    console.print()
    console.print(Panel.fit(
        f"[bold white]Topic:[/bold white] [cyan]{topic}[/cyan]",
        title="[bold magenta]Cosmic Video Generator[/bold magenta]",
        border_style="magenta",
    ))
    console.print()

    console.print(Rule("[bold green]Writing script[/bold green]"))
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as prog:
        t = prog.add_task("Generating script with Gemini…", total=None)
        script_text = generate_script(topic)
        prog.update(t, completed=True)

    out_dir = pathlib.Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)
    script_path = out_dir / "script.txt"
    script_path.write_text(script_text, encoding="utf-8")
    console.print(f"  [green]✓[/green] Script saved → [cyan]{script_path}[/cyan]\n")
    console.print(Text(script_text[:800] + ("…" if len(script_text) > 800 else ""), style="dim white"))

    if script_only:
        console.print("\n[yellow]--script-only flag set. Done.[/yellow]")
        return

    from pipeline import run_pipeline
    run_pipeline(script_text, output_dir=output)


if __name__ == "__main__":
    cli()
