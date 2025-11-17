# =============================================================================
# src/interfaces/cli/commands/learn_command.py
# =============================================================================
"""Learn Command - Phase 1: Deep learning from test files"""

from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.panel import Panel


class LearnCommand:
    """Command for Phase 1: Learning from test files"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def execute(self, root: Path, output: Path, workers: int, verbose: bool):
        """Execute learning phase"""
        
        self.console.print(Panel.fit(
            "[bold cyan]Phase 1: Deep Learning[/bold cyan]\n"
            f"Root: {root}\n"
            f"Output: {output}\n"
            f"Workers: {workers}",
            border_style="cyan"
        ))
        
        # Import dependencies here to avoid circular imports
        from ....application.use_cases.analyze_test_files import (
            AnalyzeTestFilesUseCase,
            AnalyzeTestFilesRequest
        )
        from ....application.services.analysis_service import AnalysisService
        from ....infrastructure.scanners.file_scanner import FileScanner
        from ....infrastructure.parsers.typescript_parser import TypeScriptParser
        from ....infrastructure.analyzers.complexity_analyzer import ComplexityAnalyzer
        from ....infrastructure.analyzers.quality_analyzer import QualityAnalyzer
        from ....infrastructure.persistence.file_storage import FileTestFileRepository
        
        # Setup
        output.mkdir(parents=True, exist_ok=True)
        
        scanner = FileScanner(max_workers=workers)
        parser = TypeScriptParser()
        complexity_analyzer = ComplexityAnalyzer()
        quality_analyzer = QualityAnalyzer()
        repository = FileTestFileRepository(output)
        
        service = AnalysisService(
            scanner, parser, complexity_analyzer,
            quality_analyzer, repository
        )
        
        use_case = AnalyzeTestFilesUseCase(service)
        
        # Execute with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("[cyan]Analyzing files...", total=100)
            
            request = AnalyzeTestFilesRequest(
                root_directory=root,
                max_workers=workers,
                verbose=verbose
            )
            
            result = use_case.execute(request)
            progress.update(task, completed=100)
        
        # Display results
        self._display_results(result, output)
    
    def _display_results(self, result, output):
        """Display learning results"""
        
        # Summary
        table = Table(title="📚 Learning Phase Results", show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold green")
        
        table.add_row("Total Files Found", str(result.total_files))
        table.add_row("Successfully Analyzed", str(result.analyzed_files))
        table.add_row("Candidates for Refactoring", str(result.candidates_for_refactoring))
        table.add_row("Execution Time", f"{result.execution_time:.2f}s")
        table.add_row("Output Directory", str(output))
        
        self.console.print("\n")
        self.console.print(table)
        
        # Statistics
        if result.statistics:
            self._display_statistics(result.statistics)
        
        # Next steps
        self.console.print("\n[bold green]✅ Learning phase complete![/bold green]")
        self.console.print("\n[dim]Next steps:[/dim]")
        self.console.print("  1. Review results in output directory")
        self.console.print("  2. Run: [cyan]refactor-ai practice[/cyan]")
    
    def _display_statistics(self, stats):
        """Display detailed statistics"""
        
        # Complexity distribution
        if 'complexity_distribution' in stats:
            dist = stats['complexity_distribution']
            
            table = Table(title="Complexity Distribution")
            table.add_column("Level", style="cyan")
            table.add_column("Count", style="bold")
            table.add_column("Percentage", style="dim")
            
            total = sum(dist.values())
            
            for level, count in dist.items():
                pct = (count / total * 100) if total > 0 else 0
                table.add_row(
                    level.capitalize(),
                    str(count),
                    f"{pct:.1f}%"
                )
            
            self.console.print("\n")
            self.console.print(table)
        
        # Quality distribution
        if 'quality_distribution' in stats:
            dist = stats['quality_distribution']
            
            table = Table(title="Quality Distribution")
            table.add_column("Level", style="cyan")
            table.add_column("Count", style="bold")
            
            for level, count in dist.items():
                table.add_row(level.capitalize(), str(count))
            
            self.console.print("\n")
            self.console.print(table)