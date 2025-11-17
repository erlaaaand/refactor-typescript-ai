# Development Guide

## Setup Development Environment

### 1. Clone and Setup

```bash
git clone <repository-url>
cd test-refactor-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

### 2. Project Structure

```bash
# Create directory structure
python scripts/setup_structure.py
```

## Development Workflow

### Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/unit/domains/test_complexity.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Run all checks
pre-commit run --all-files
```

### Running the Application

```bash
# Using Python module
python -m src.interfaces.cli.main analyze 'FOLDER_PATH'

# Using installed command
refactor-ai analyze --root backend/src

# Development mode
python main.py analyze --verbose
```

## Adding New Features

### 1. Domain Entity

```python
# src/domain/entities/my_entity.py
from dataclasses import dataclass

@dataclass
class MyEntity:
    id: str
    name: str
    
    def do_something(self) -> str:
        return f"Doing {self.name}"
```

### 2. Value Object

```python
# src/domain/value_objects/my_value.py
from dataclasses import dataclass

@dataclass(frozen=True)
class MyValue:
    value: int
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Must be positive")
```

### 3. Use Case

```python
# src/application/use_cases/my_use_case.py
from dataclasses import dataclass

@dataclass
class MyRequest:
    param: str

class MyUseCase:
    def execute(self, request: MyRequest):
        # Implementation
        pass
```

### 4. Tests

```python
# tests/unit/test_my_entity.py
def test_my_entity():
    entity = MyEntity(id="1", name="test")
    assert entity.do_something() == "Doing test"
```

## Debugging

### Enable Verbose Output

```bash
refactor-ai learn --verbose
```

### Python Debugger

```python
import pdb; pdb.set_trace()
```

### Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Code Style Guidelines

- Line length: 100 characters
- Use type hints for all functions
- Write docstrings (Google style)
- Follow PEP 8
- Use dataclasses for data containers
- Prefer composition over inheritance

## Commit Guidelines

Follow conventional commits:

```
feat: add new feature
fix: bug fix
docs: documentation update
test: add tests
refactor: code refactoring
style: formatting changes
chore: maintenance tasks
```