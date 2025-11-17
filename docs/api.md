# API Reference

## Command Line Interface

### analyze
Quick analysis without generating plans.

```bash
refactor-ai analyze --root backend/src --workers 4 --verbose
```

**Options:**
- `--root, -r`: Root directory to scan (default: backend/src)
- `--workers, -w`: Number of parallel workers (default: 4)
- `--verbose, -v`: Enable verbose output

### learn
Phase 1: Deep learning from test files.

```bash
refactor-ai learn --root backend/src --output output/training_data --workers 8
```

**Options:**
- `--root, -r`: Root directory to scan
- `--output, -o`: Output directory
- `--workers, -w`: Number of parallel workers
- `--verbose, -v`: Enable verbose output

### practice
Phase 2: Generate intelligent refactoring plans.

```bash
refactor-ai practice --training-data output/training_data --max-files 10
```

**Options:**
- `--training-data, -t`: Training data directory
- `--output, -o`: Output directory
- `--max-files, -m`: Maximum files to process
- `--file, -f`: Target specific file
- `--verbose, -v`: Enable verbose output

### execute
Phase 3: Execute refactoring plans.

```bash
refactor-ai execute --plans output/practice_runs --dry-run
refactor-ai execute --yes
```

**Options:**
- `--plans, -p`: Plans directory
- `--root, -r`: Root directory
- `--dry-run, -d`: Preview changes without applying
- `--yes, -y`: Skip confirmation
- `--plan-numbers, -n`: Execute specific plans (e.g., '1,3,5')
- `--verbose, -v`: Enable verbose output

### status
Show system status.

```bash
refactor-ai status --output output
```

### version
Show version information.

```bash
refactor-ai version
```

## Python API

### Analysis Service

```python
from src.application.services.analysis_service import AnalysisService
from pathlib import Path

service = AnalysisService(scanner, parser, analyzer, quality, repo)
result = service.analyze_directory(Path("backend/src"))
```

### Planning Service

```python
from src.application.services.planning_service import PlanningService

service = PlanningService(repository)
plans = service.generate_plans(test_files)
```

### Execution Service

```python
from src.application.services.execution_service import ExecutionService

service = ExecutionService(code_generator)
result = service.execute_plans(plans, backup=True)
```