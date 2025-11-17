# =============================================================================
# src/interfaces/cli/commands/analyze_command.py
# =============================================================================

"""Analyze Command"""

from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

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


class AnalyzeCommand:
    """Command for analyzing test files"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def execute(self, root: Path, workers: int, verbose: bool):
        """Execute analysis"""
        
        # Setup dependencies
        scanner = FileScanner(max_workers=workers)
        parser = TypeScriptParser()
        complexity_analyzer = ComplexityAnalyzer()
        quality_analyzer = QualityAnalyzer()
        repository = FileTestFileRepository(Path("output/training_data"))
        
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
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
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
        self._display_results(result)
    
    def _display_results(self, result):
        """Display analysis results"""
        
        # Summary table
        table = Table(title="Analysis Summary", show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold green")
        
        table.add_row("Total Files", str(result.total_files))
        table.add_row("Analyzed", str(result.analyzed_files))
        table.add_row("Need Refactoring", str(result.candidates_for_refactoring))
        table.add_row("Execution Time", f"{result.execution_time:.2f}s")
        
        self.console.print("\n")
        self.console.print(table)
        
        # Complexity distribution
        if 'complexity_distribution' in result.statistics:
            dist = result.statistics['complexity_distribution']
            
            table2 = Table(title="Complexity Distribution")
            table2.add_column("Level", style="cyan")
            table2.add_column("Count", style="bold")
            
            table2.add_row("Simple", str(dist.get('simple', 0)))
            table2.add_row("Medium", str(dist.get('medium', 0)))
            table2.add_row("Complex", str(dist.get('complex', 0)))
            
            self.console.print("\n")
            self.console.print(table2)
        
        self.console.print("\n[bold green]✅ Analysis complete![/bold green]")