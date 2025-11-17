# =============================================================================
# src/interfaces/cli/commands/practice_command.py
# =============================================================================
"""Practice Command - Phase 2: Generate refactoring plans"""

from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json


class PracticeCommand:
    """Command for Phase 2: Generating refactoring plans"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def execute(self, training_data: Path, output: Path, 
                max_files: Optional[int], file: Optional[str], verbose: bool):
        """Execute practice phase"""
        
        self.console.print(Panel.fit(
            "[bold cyan]Phase 2: Smart Planning[/bold cyan]\n"
            f"Training Data: {training_data}\n"
            f"Output: {output}",
            border_style="cyan"
        ))
        
        # Validate training data exists
        candidates_file = training_data / "candidates.json"
        if not candidates_file.exists():
            self.console.print(
                "[bold red]❌ Training data not found![/bold red]\n"
                "[dim]Run Phase 1 first: refactor-ai learn[/dim]"
            )
            return
        
        # Load training data
        with open(candidates_file) as f:
            candidates = json.load(f)
        
        if verbose:
            self.console.print(f"[dim]Loaded {len(candidates)} candidates[/dim]\n")
        
        # Filter if needed
        if max_files:
            candidates = candidates[:max_files]
        
        if file:
            candidates = [c for c in candidates if file in c['path']]
        
        # Generate plans
        from ....application.services.planning_service import PlanningService
        from ....infrastructure.persistence.file_storage import FileTestFileRepository
        from ....domain.entities.test_file import TestFile
        
        # Setup
        output.mkdir(parents=True, exist_ok=True)
        repository = FileTestFileRepository(training_data)
        service = PlanningService(repository)
        
        # Convert candidates to TestFile entities (simplified)
        test_files = []
        for candidate in candidates:
            # This is simplified - in real implementation would reconstruct full TestFile
            # For now, just use the data we have
            pass
        
        # Generate plans
        self.console.print("[cyan]Generating refactoring plans...[/cyan]\n")
        
        # For demo, create sample plans
        plans = self._generate_sample_plans(candidates, output)
        
        # Display results
        self._display_results(plans, output)
    
    def _generate_sample_plans(self, candidates, output):
        """Generate sample plans (simplified for demo)"""
        
        plans = []
        for i, candidate in enumerate(candidates):
            plan = {
                'id': f'plan_{i+1}',
                'source_file': candidate['path'],
                'action': candidate.get('recommended_action', 'split_by_category'),
                'reason': candidate.get('refactoring_reason', 'Complex file'),
                'confidence': 0.85,
                'priority': 3,
                'status': 'ready'
            }
            plans.append(plan)
        
        # Save plans
        plans_file = output / "all_plans.json"
        with open(plans_file, 'w') as f:
            json.dump(plans, f, indent=2)
        
        return plans
    
    def _display_results(self, plans, output):
        """Display planning results"""
        
        # Summary table
        table = Table(title="🎯 Planning Phase Results", show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold green")
        
        table.add_row("Total Plans Generated", str(len(plans)))
        
        # Count by action
        actions = {}
        for plan in plans:
            action = plan['action']
            actions[action] = actions.get(action, 0) + 1
        
        for action, count in actions.items():
            table.add_row(f"  {action}", str(count))
        
        table.add_row("Output Directory", str(output))
        
        self.console.print("\n")
        self.console.print(table)
        
        # Plans preview
        if plans:
            self._display_plans_preview(plans[:5])
        
        # Next steps
        self.console.print("\n[bold green]✅ Planning phase complete![/bold green]")
        self.console.print("\n[dim]Next steps:[/dim]")
        self.console.print("  1. Review plans in output directory")
        self.console.print("  2. Preview changes: [cyan]refactor-ai execute --dry-run[/cyan]")
        self.console.print("  3. Apply changes: [cyan]refactor-ai execute --yes[/cyan]")
    
    def _display_plans_preview(self, plans):
        """Display preview of first few plans"""
        
        table = Table(title="Plans Preview (First 5)")
        table.add_column("ID", style="cyan")
        table.add_column("File", style="dim")
        table.add_column("Action", style="yellow")
        table.add_column("Confidence", style="green")
        
        for plan in plans:
            file_name = Path(plan['source_file']).name
            table.add_row(
                plan['id'],
                file_name,
                plan['action'],
                f"{plan['confidence']:.0%}"
            )
        
        self.console.print("\n")
        self.console.print(table)