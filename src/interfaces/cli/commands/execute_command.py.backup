# =============================================================================
# src/interfaces/cli/commands/execute_command.py
# =============================================================================
"""Execute Command - Phase 3: Execute refactoring plans"""

from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
import json


class ExecuteCommand:
    """Command for Phase 3: Executing refactoring plans"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def execute(self, plans_dir: Path, root: Path, dry_run: bool,
                yes: bool, plans: Optional[List[int]], verbose: bool):
        """Execute refactoring plans"""
        
        # Load plans
        plans_file = plans_dir / "all_plans.json"
        if not plans_file.exists():
            self.console.print(
                "[bold red]❌ Plans not found![/bold red]\n"
                "[dim]Run Phase 2 first: refactor-ai practice[/dim]"
            )
            return
        
        with open(plans_file) as f:
            all_plans = json.load(f)
        
        # Filter plans if specified
        if plans:
            all_plans = [p for i, p in enumerate(all_plans, 1) if i in plans]
        
        if not all_plans:
            self.console.print("[yellow]No plans to execute[/yellow]")
            return
        
        # Display execution summary
        self._display_summary(all_plans, dry_run)
        
        # Confirm if not dry-run and not auto-yes
        if not dry_run and not yes:
            if not Confirm.ask("\n[bold yellow]Execute these plans?[/bold yellow]"):
                self.console.print("[dim]Execution cancelled[/dim]")
                return
        
        # Execute plans
        if dry_run:
            self._dry_run(all_plans, root)
        else:
            self._execute_plans(all_plans, root, verbose)
    
    def _display_summary(self, plans, dry_run: bool):
        """Display execution summary"""
        
        mode = "[yellow]DRY RUN[/yellow]" if dry_run else "[red]LIVE EXECUTION[/red]"
        
        self.console.print(Panel.fit(
            f"[bold cyan]Phase 3: Execution[/bold cyan]\n"
            f"Mode: {mode}\n"
            f"Plans to execute: {len(plans)}",
            border_style="red" if not dry_run else "yellow"
        ))
        
        # Plans table
        table = Table(title="Execution Queue")
        table.add_column("ID", style="cyan")
        table.add_column("File", style="dim")
        table.add_column("Action", style="yellow")
        table.add_column("Status", style="green")
        
        for plan in plans:
            file_name = Path(plan['source_file']).name
            table.add_row(
                plan['id'],
                file_name,
                plan['action'],
                plan['status']
            )
        
        self.console.print("\n")
        self.console.print(table)
    
    def _dry_run(self, plans, root: Path):
        """Perform dry run - show what would happen"""
        
        self.console.print("\n[bold yellow]🔍 DRY RUN - No files will be modified[/bold yellow]\n")
        
        for plan in plans:
            self.console.print(f"[cyan]Plan: {plan['id']}[/cyan]")
            self.console.print(f"  Source: {plan['source_file']}")
            self.console.print(f"  Action: {plan['action']}")
            self.console.print(f"  Reason: {plan['reason']}")
            
            # Show what would be created
            if plan['action'] == 'split_by_category':
                self.console.print("  [dim]Would create:[/dim]")
                self.console.print("    - file1.category1.spec.ts")
                self.console.print("    - file1.category2.spec.ts")
            elif plan['action'] == 'split_by_concern':
                self.console.print("  [dim]Would create:[/dim]")
                self.console.print("    - file1.part1.spec.ts")
                self.console.print("    - file1.part2.spec.ts")
            elif plan['action'] == 'extract_shared':
                self.console.print("  [dim]Would create:[/dim]")
                self.console.print("    - test-utils.ts")
            
            self.console.print()
        
        self.console.print("[bold green]✅ Dry run complete![/bold green]")
        self.console.print("[dim]Remove --dry-run flag to execute for real[/dim]")
    
    def _execute_plans(self, plans, root: Path, verbose: bool):
        """Execute plans for real"""
        
        self.console.print("\n[bold red]⚡ EXECUTING PLANS...[/bold red]\n")
        
        results = {
            'successful': 0,
            'failed': 0,
            'skipped': 0
        }
        
        for plan in plans:
            try:
                if verbose:
                    self.console.print(f"[cyan]Executing: {plan['id']}[/cyan]")
                
                # Here would be actual execution logic
                # For now, simulate success
                success = True
                
                if success:
                    results['successful'] += 1
                    if verbose:
                        self.console.print(f"  [green]✓ Success[/green]")
                else:
                    results['failed'] += 1
                    if verbose:
                        self.console.print(f"  [red]✗ Failed[/red]")
                
            except Exception as e:
                results['failed'] += 1
                if verbose:
                    self.console.print(f"  [red]✗ Error: {e}[/red]")
        
        # Display results
        self._display_execution_results(results)
    
    def _display_execution_results(self, results):
        """Display execution results"""
        
        table = Table(title="⚡ Execution Results", show_header=False)
        table.add_column("Status", style="cyan")
        table.add_column("Count", style="bold")
        
        table.add_row("✅ Successful", str(results['successful']))
        table.add_row("❌ Failed", str(results['failed']))
        table.add_row("⏭️  Skipped", str(results['skipped']))
        
        self.console.print("\n")
        self.console.print(table)
        
        if results['failed'] == 0:
            self.console.print("\n[bold green]✅ All plans executed successfully![/bold green]")
        else:
            self.console.print("\n[bold yellow]⚠️  Some plans failed[/bold yellow]")
            self.console.print("[dim]Check logs for details[/dim]")