# Architecture Documentation

## Overview

Test Refactor AI follows **Clean Architecture** principles with clear separation of concerns across four main layers.

## Layer Structure

```
┌─────────────────────────────────────────┐
│         Interface Layer                 │
│  CLI, Config, Presenters               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Application Layer                 │
│  Use Cases, Services, DTOs             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Domain Layer                    │
│  Entities, Value Objects, Repositories │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Infrastructure Layer               │
│  Parsers, Analyzers, Persistence       │
└─────────────────────────────────────────┘
```

## Domain Layer

The heart of the application containing pure business logic.

### Entities
- **TestFile**: Represents a test file with all its properties
- **Pattern**: Learned patterns from codebase
- **RefactorPlan**: Refactoring action plan

### Value Objects
- **Complexity**: Immutable complexity metrics
- **QualityScore**: Code quality measurements
- **FileMetadata**: File information

## Application Layer

Orchestrates business logic through use cases and services.

### Use Cases
- **AnalyzeTestFilesUseCase**: Analyze test files
- **GenerateRefactorPlanUseCase**: Create refactoring plans
- **ExecuteRefactoringUseCase**: Apply refactorings

### Services
- **AnalysisService**: File analysis orchestration
- **PlanningService**: Plan generation
- **ExecutionService**: Plan execution

## Infrastructure Layer

Technical implementation details.

### Parsers
- **TypeScriptParser**: Main parser
- **ImportParser**: Import statements
- **MockParser**: Mock data extraction
- **TestStructureParser**: Test blocks

### Analyzers
- **ComplexityAnalyzer**: Calculate complexity
- **QualityAnalyzer**: Assess code quality

## Design Patterns

### Repository Pattern
Abstract data access behind interfaces.

### Strategy Pattern
Pluggable analysis and refactoring strategies.

### Factory Pattern
Create complex objects consistently.

## Dependency Flow

Dependencies flow **inward** only:
- Interface → Application → Domain
- Infrastructure → Domain
- **Never** Domain → Infrastructure