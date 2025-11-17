# =============================================================================
# src/interfaces/cli/presenters/report_generator.py
# =============================================================================
"""Report Generator - Generates various output reports"""

from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from ...config.config_loader import ConfigLoader


class ReportGenerator:
    """Generates analysis and execution reports in various formats"""
    
    def __init__(self, config: ConfigLoader):
        self.config = config
    
    def generate_analysis_report(
        self,
        results: Dict[str, Any],
        output_path: Path,
        format: str = 'markdown'
    ) -> bool:
        """Generate analysis report"""
        if format == 'markdown':
            return self._generate_markdown_report(results, output_path)
        elif format == 'html':
            return self._generate_html_report(results, output_path)
        elif format == 'json':
            return self._generate_json_report(results, output_path)
        return False
    
    def _generate_markdown_report(
        self,
        results: Dict[str, Any],
        output_path: Path
    ) -> bool:
        """Generate Markdown report"""
        try:
            report = []
            report.append("# Test Refactoring Analysis Report")
            report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Summary section
            report.append("## Summary")
            report.append(f"- **Total Files:** {results.get('total_files', 0)}")
            report.append(f"- **Analyzed:** {results.get('analyzed_files', 0)}")
            report.append(f"- **Need Refactoring:** {results.get('candidates', 0)}")
            report.append(f"- **Execution Time:** {results.get('execution_time', 0):.2f}s\n")
            
            # Complexity distribution
            if 'complexity_distribution' in results:
                report.append("## Complexity Distribution")
                dist = results['complexity_distribution']
                report.append(f"- **Simple:** {dist.get('simple', 0)}")
                report.append(f"- **Medium:** {dist.get('medium', 0)}")
                report.append(f"- **Complex:** {dist.get('complex', 0)}\n")
            
            # Quality distribution
            if 'quality_distribution' in results:
                report.append("## Quality Distribution")
                dist = results['quality_distribution']
                for level, count in dist.items():
                    report.append(f"- **{level.capitalize()}:** {count}")
                report.append("")
            
            # Recommendations
            if 'recommendations' in results:
                report.append("## Recommendations")
                for rec in results['recommendations']:
                    report.append(f"- {rec}")
                report.append("")
            
            # Write to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text('\n'.join(report))
            return True
        except Exception:
            return False
    
    def _generate_html_report(
        self,
        results: Dict[str, Any],
        output_path: Path
    ) -> bool:
        """Generate HTML report"""
        try:
            html = []
            html.append("<!DOCTYPE html>")
            html.append("<html>")
            html.append("<head>")
            html.append("  <title>Test Refactoring Analysis Report</title>")
            html.append("  <style>")
            html.append("    body { font-family: Arial, sans-serif; margin: 40px; }")
            html.append("    h1 { color: #2c3e50; }")
            html.append("    h2 { color: #34495e; border-bottom: 2px solid #3498db; }")
            html.append("    table { border-collapse: collapse; width: 100%; margin: 20px 0; }")
            html.append("    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }")
            html.append("    th { background-color: #3498db; color: white; }")
            html.append("    .metric { font-size: 18px; margin: 10px 0; }")
            html.append("  </style>")
            html.append("</head>")
            html.append("<body>")
            
            # Title
            html.append("  <h1>🤖 Test Refactoring Analysis Report</h1>")
            html.append(f"  <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            
            # Summary
            html.append("  <h2>Summary</h2>")
            html.append(f"  <div class='metric'>Total Files: <strong>{results.get('total_files', 0)}</strong></div>")
            html.append(f"  <div class='metric'>Analyzed: <strong>{results.get('analyzed_files', 0)}</strong></div>")
            html.append(f"  <div class='metric'>Need Refactoring: <strong>{results.get('candidates', 0)}</strong></div>")
            
            # Complexity table
            if 'complexity_distribution' in results:
                html.append("  <h2>Complexity Distribution</h2>")
                html.append("  <table>")
                html.append("    <tr><th>Level</th><th>Count</th></tr>")
                dist = results['complexity_distribution']
                for level, count in dist.items():
                    html.append(f"    <tr><td>{level.capitalize()}</td><td>{count}</td></tr>")
                html.append("  </table>")
            
            html.append("</body>")
            html.append("</html>")
            
            # Write to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text('\n'.join(html))
            return True
        except Exception:
            return False
    
    def _generate_json_report(
        self,
        results: Dict[str, Any],
        output_path: Path
    ) -> bool:
        """Generate JSON report"""
        import json
        
        try:
            report = {
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_files': results.get('total_files', 0),
                    'analyzed_files': results.get('analyzed_files', 0),
                    'candidates': results.get('candidates', 0),
                    'execution_time': results.get('execution_time', 0)
                },
                'distributions': {
                    'complexity': results.get('complexity_distribution', {}),
                    'quality': results.get('quality_distribution', {})
                },
                'recommendations': results.get('recommendations', [])
            }
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            return True
        except Exception:
            return False