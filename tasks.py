import shutil
from pathlib import Path
from invoke import task
from rich.console import Console

console = Console()

@task(help={"dry": "If True, only lists the files/folders that would be removed without deleting them."})
def mrproper(c, dry=False):
    """
    Clean up all the pycache and other cache files in the project.
    
    This includes:
    - __pycache__ directories
    - .pytest_cache directories
    - .mypy_cache directories
    - .ruff_cache directories
    - *.pyc, *.pyo, *.pyd files
    """
    console.print("[bold blue]Cleaning up project caches...[/bold blue]")
    
    patterns = [
        "**/__pycache__",
        "**/.pytest_cache",
        "**/.mypy_cache",
        "**/.ruff_cache",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
    ]
    
    count = 0
    root = Path(".")
    
    for pattern in patterns:
        for path in root.glob(pattern):
            # Skip .venv directory to avoid accidental deletion of environment files
            if ".venv" in path.parts:
                continue
                
            if dry:
                console.print(f"[yellow]Would remove:[/yellow] {path}")
            else:
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    console.print(f"[red]Removed:[/red] {path}")
                    count += 1
                except Exception as e:
                    console.print(f"[bold red]Error removing {path}:[/bold red] {e}")

    if dry:
        console.print("[bold green]Dry run completed.[/bold green]")
    else:
        console.print(f"[bold green]Cleanup completed! [cyan]{count}[/cyan] items removed.[/bold green]")
