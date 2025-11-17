# =============================================================================
# src/interfaces/cli/presenters/console_presenter.py
# =============================================================================
"""Console Presenter - Format output for CLI"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from typing import Dict, List


class ConsolePresenter:
    """Presents data to console using Rich"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def show_banner(self, title: str, subtitle: str = ""):
        """Show banner"""
        content = f"[bold cyan]{title}[/bold cyan]"
        if subtitle:
            content += f"\n[dim]{subtitle}[/dim]"
        
        self.console.print(Panel.fit(content, border_style="cyan"))
    
    def show_success(self, message: str):
        """Show success message"""
        self.console.print(f"[bold green]✅ {message}[/bold green]")
    
    def show_error(self, message: str):
        """Show error message"""
        self.console.print(f"[bold red]❌ {message}[/bold red]")
    
    def show_warning(self, message: str):
        """Show warning message"""
        self.console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    
    def show_info(self, message: str):
        """Show info message"""
        self.console.print(f"[cyan]ℹ️  {message}[/cyan]")
    
    def show_table(self, title: str, data: Dict[str, str],
                   column1: str = "Item", column2: str = "Value"):
        """Show data as table"""
        table = Table(title=title)
        table.add_column(column1, style="cyan")
        table.add_column(column2, style="bold green")
        
        for key, value in data.items():
            table.add_row(key, str(value))
        
        self.console.print("\n")
        self.console.print(table)
    
    def show_progress(self, description: str, total: int):
        """Create progress bar"""
        return Progress(console=self.console).add_task(
            description,
            total=total
        )