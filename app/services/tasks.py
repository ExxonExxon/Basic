# [MODULE_OVERVIEW]
# This module implements developer automation and maintenance tasks using the 'invoke' library.
# It provides a command-line interface for common project lifecycle operations like cache purging.

# [OPERATIONAL_SCOPE]
# Root: Project Directory. 
# Input: Dry-run flag (boolean) to simulate changes. 
# Output: A sanitized and optimized directory tree.

# [STATE_MUTATION_DETAILS]
# This script performs destructive operations by deleting files and directories that match 
# specific development cache patterns. It is designed to be run during development 
# or CI/CD stages to ensure a clean build environment.

# [EXECUTION_CONSTRAINTS]
# The logic utilizes Path.glob() for recursive pattern matching. 
# IMPORTANT: It explicitly filters out the '.venv' directory to prevent the accidental 
# destruction of the Python virtual environment and its dependencies.

import shutil
from pathlib import Path
from invoke import task
from rich.console import Console

console = Console()

# [FUNCTIONAL_SPECIFICATION]
# The 'mrproper' task serves as the primary cleanup utility for Python development environments.
# It targets artifacts that are often the source of 'stale' behavior during local testing.

# [PARAMETER_DOCUMENTATION]
# c: Context - The standard execution context provided by the Invoke library.
# dry: Boolean - When set to True, the script performs a 'no-op' run, logging all 
#      targeted paths without executing any filesystem deletions.

# [TARGET_ARCHITECTURE_PATTERNS]
# The script targets several tiers of temporary data:
# 1. Runtime Artifacts: __pycache__, *.pyc, *.pyo, *.pyd (Compiled Python bytecode).
# 2. Test Framework Metadata: .pytest_cache (Pytest execution state).
# 3. Static Analysis Metadata: .mypy_cache (Type-checking state), .ruff_cache (Linting state).

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
    # [LOGGING_STRATEGY]
    # Employs the 'rich' library to provide high-visibility, formatted console output 
    # to the developer during the execution lifecycle.
    console.print("[bold blue]Cleaning up project caches...[/bold blue]")
    
    # [DATA_DEFINITION]
    # Definitive list of glob patterns representing temporary or cached build artifacts.
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
    
    # [ITERATION_STRATEGY]
    # Performs a recursive walk starting from the project root.
    # Uses globbing to match the predefined artifact patterns.
    for pattern in patterns:
        for path in root.glob(pattern):
            # [INTEGRITY_PROTECTION]
            # Safety mechanism: We verify that the current path is not a member of the 
            # '.venv' directory tree. This preserves the local environment state.
            if ".venv" in path.parts:
                continue
                
            if dry:
                # [SIMULATION_LOG]
                # In dry-run mode, we echo the path to the console using yellow highlighting 
                # to indicate it was selected for deletion but not touched.
                console.print(f"[yellow]Would remove:[/yellow] {path}")
            else:
                try:
                    # [FILESYSTEM_INTERACTION]
                    # Polymorphic deletion:
                    # - If the path is a directory (e.g., __pycache__), we use shutil.rmtree for recursion.
                    # - If the path is a file (e.g., .pyc), we use path.unlink() for a direct deletion.
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    console.print(f"[red]Removed:[/red] {path}")
                    count += 1
                except Exception as e:
                    # [EXCEPTION_HANDLING]
                    # Catches OS-level errors, such as 'Permission Denied' or 'File in Use', 
                    # preventing a single failure from halting the entire cleanup sequence.
                    console.print(f"[bold red]Error removing {path}:[/bold red] {e}")

    # [FINAL_SUMMARY]
    # Reports the terminal state of the operation back to the user, providing an 
    # audit trail of the number of items successfully removed.
    if dry:
        console.print("[bold green]Dry run completed.[/bold green]")
    else:
        console.print(f"[bold green]Cleanup completed! [cyan]{count}[/cyan] items removed.[/bold green]")
