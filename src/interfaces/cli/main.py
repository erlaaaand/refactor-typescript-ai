# =============================================================================
# src/interfaces/cli/main.py
# =============================================================================
"""Modern CLI using Typer and Rich"""

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from pathlib import Path
from typing import Optional

from .commands.analyze_command import AnalyzeCommand
from .commands.learn_command import LearnCommand
from .commands.practice_command import PracticeCommand
from .commands.execute_command import ExecuteCommand

# Initialize
app = typer.Typer(
    name="refactor-ai",
    help="🤖 Intelligent TypeScript Test File Refactoring AI",
    add_completion=False
)
console = Console()


@app.command()
def analyze(
    root: Path = typer.Option(
        Path("backend/src"),
        "--root", "-r",
        help="Root directory to scan"
    ),
    workers: int = typer.Option(
        4,
        "--workers", "-w",
        help="Number of parallel workers"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output"
    )
):
    """🔍 Quick analysis without generating plans"""
    
    console.print(Panel.fit(
        "[bold cyan]🤖 Test Refactoring AI[/bold cyan]\n"
        "[dim]Quick Analysis Mode[/dim]",
        border_style="cyan"
    ))
    
    command = AnalyzeCommand(console)
    command.execute(root, workers, verbose)


@app.command()
def learn(
    root: Path = typer.Option(
        Path("backend/src"),
        "--root", "-r",
        help="Root directory to scan"
    ),
    output: Path = typer.Option(
        Path("output/training_data"),
        "--output", "-o",
        help="Output directory"
    ),
    workers: int = typer.Option(
        4,
        "--workers", "-w",
        help="Number of parallel workers"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output"
    )
):
    """📚 Phase 1: Deep learning from test files"""
    
    console.print(Panel.fit(
        "[bold cyan]🤖 Test Refactoring AI[/bold cyan]\n"
        "[bold yellow]Phase 1: Deep Learning[/bold yellow]",
        border_style="cyan"
    ))
    
    command = LearnCommand(console)
    command.execute(root, output, workers, verbose)


@app.command()
def practice(
    training_data: Path = typer.Option(
        Path("output/training_data"),
        "--training-data", "-t",
        help="Training data directory"
    ),
    output: Path = typer.Option(
        Path("output/practice_runs"),
        "--output", "-o",
        help="Output directory"
    ),
    max_files: Optional[int] = typer.Option(
        None,
        "--max-files", "-m",
        help="Maximum files to process"
    ),
    file: Optional[str] = typer.Option(
        None,
        "--file", "-f",
        help="Target specific file"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output"
    )
):
    """🎯 Phase 2: Generate intelligent refactoring plans"""
    
    console.print(Panel.fit(
        "[bold cyan]🤖 Test Refactoring AI[/bold cyan]\n"
        "[bold yellow]Phase 2: Smart Planning[/bold yellow]",
        border_style="cyan"
    ))
    
    command = PracticeCommand(console)
    command.execute(training_data, output, max_files, file, verbose)


@app.command()
def execute(
    plans_dir: Path = typer.Option(
        Path("output/practice_runs"),
        "--plans", "-p",
        help="Plans directory"
    ),
    root: Path = typer.Option(
        Path("backend/src"),
        "--root", "-r",
        help="Root directory"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run", "-d",
        help="Preview changes without applying"
    ),
    yes: bool = typer.Option(
        False,
        "--yes", "-y",
        help="Skip confirmation"
    ),
    plan_numbers: Optional[str] = typer.Option(
        None,
        "--plan-numbers", "-n",
        help="Execute specific plans (e.g., '1,3,5')"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output"
    )
):
    """⚡ Phase 3: Execute refactoring plans"""
    
    if dry_run:
        console.print(Panel.fit(
            "[bold cyan]🤖 Test Refactoring AI[/bold cyan]\n"
            "[bold yellow]Phase 3: Dry Run[/bold yellow]",
            border_style="cyan"
        ))
    else:
        console.print(Panel.fit(
            "[bold cyan]🤖 Test Refactoring AI[/bold cyan]\n"
            "[bold red]Phase 3: Execution[/bold red]\n"
            "[dim]⚠️  This will modify your files![/dim]",
            border_style="red"
        ))
    
    command = ExecuteCommand(console)
    
    # Parse plan numbers
    plans = None
    if plan_numbers:
        plans = [int(n.strip()) for n in plan_numbers.split(',')]
    
    command.execute(plans_dir, root, dry_run, yes, plans, verbose)


@app.command()
def status(
    output: Path = typer.Option(
        Path("output"),
        "--output", "-o",
        help="Output directory"
    )
):
    """📊 Show system status"""
    
    console.print(Panel.fit(
        "[bold cyan]🤖 Test Refactoring AI[/bold cyan]\n"
        "[dim]System Status[/dim]",
        border_style="cyan"
    ))
    
    # Create status table
    table = Table(title="Training Phases Status", show_header=True)
    table.add_column("Phase", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="dim")
    
    # Check Phase 1
    phase1_path = output / "training_data" / "all_files.json"
    if phase1_path.exists():
        import json
        with open(phase1_path) as f:
            data = json.load(f)
        table.add_row(
            "Phase 1: Learning",
            "✅ Complete",
            f"{len(data)} files analyzed"
        )
    else:
        table.add_row(
            "Phase 1: Learning",
            "❌ Not started",
            "Run: refactor-ai learn"
        )
    
    # Check Phase 2
    phase2_path = output / "practice_runs" / "all_plans.json"
    if phase2_path.exists():
        import json
        with open(phase2_path) as f:
            data = json.load(f)
        table.add_row(
            "Phase 2: Planning",
            "✅ Complete",
            f"{len(data)} plans generated"
        )
    else:
        table.add_row(
            "Phase 2: Planning",
            "❌ Not started",
            "Run: refactor-ai practice"
        )
    
    # Check Phase 3
    phase3_path = output / "execution_results"
    if phase3_path.exists() and list(phase3_path.glob("execution_*.json")):
        results = list(phase3_path.glob("execution_*.json"))
        table.add_row(
            "Phase 3: Execution",
            "✅ Complete",
            f"{len(results)} execution(s)"
        )
    else:
        table.add_row(
            "Phase 3: Execution",
            "❌ Not started",
            "Run: refactor-ai execute"
        )
    
    console.print(table)


@app.command()
def version():
    """Show version information"""
    
    console.print(Panel.fit(
        "[bold cyan]🤖 Test Refactoring AI[/bold cyan]\n"
        "[bold]Version 2.1.0[/bold]\n\n"
        "[dim]Intelligent TypeScript test file refactoring[/dim]\n"
        "[dim]Built with ❤️  for developers[/dim]",
        border_style="cyan"
    ))


if __name__ == "__main__":
    app()