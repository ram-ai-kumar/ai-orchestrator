# Usage Guide - Agentic Vibe Engineering Development

This guide provides detailed steps for using AI Orchestrator for local agentic vibe engineering development workflows.

## Overview

AI Orchestrator automates video engineering development tasks through a multi-agent workflow that plans, retrieves context, generates code, tests in sandboxed environments, and reviews changes. The system enforces enterprise policies through a configurable rules system based on git branch type.

## Prerequisites

Ensure you have completed the [Quick Start Guide](QUICKSTART.md) before proceeding.

## Workflow

### 1. Branch Selection

Choose the appropriate branch for your development task:

**Production Branches** (full rules enforcement):

- `main` - Production code
- `develop` - Integration branch
- `release/*` - Release preparation (e.g., `release/v1.0.0`)

**Development Branches** (mandatory rules only):

- `feature/*` - New features (e.g., `feature/video-processing-pipeline`)
- `hotfix/*` - Critical fixes (e.g., `hotfix/encoding-bug`)
- `bugfix/*` - Bug fixes (e.g., `bugfix/transcode-error`)

```bash
# Create a feature branch
git checkout -b feature/video-processing-pipeline
```

### 2. Configure Rules

The system automatically selects rules based on your branch. Review and customize in `config/rules.yaml`:

```yaml
# Branch classification
branch_settings:
  production_branches:
    - main
    - develop
    - release/*

# Optional rules (user-configurable)
optional:
  03-hipaa-compliance: false
  04-soc2-compliance: false
  05-iso27001-compliance: false
  10-backend-patterns: auto
  11-frontend-patterns: auto
  21-ruby-rails-patterns: auto
  22-python-patterns: auto
  23-typescript-patterns: auto
  24-go-patterns: auto
```

**Config Values:**

- `true` - Rule always applies
- `false` - Rule never applies
- `auto` - Auto-detect based on project characteristics

### 3. Run the Orchestrator

```bash
python scripts/run_task.py
```

The system will:

1. Detect current git branch
2. Select appropriate rules based on branch type
3. Display active rules
4. Prompt for your task

### 4. Define Your Task

Enter a specific, actionable task related to video engineering:

**Example Tasks:**

**Video Processing Pipeline:**

```text
Implement a video transcoding pipeline using FFmpeg that converts input videos to H.264 format with configurable bitrate and resolution
```

**Video Analysis:**

```text
Add video analysis capabilities to extract metadata including duration, codec information, and frame rate using OpenCV
```

**Streaming Integration:**

```text
Integrate HLS streaming support for video playback with adaptive bitrate streaming
```

**Optimization:**

```text
Optimize video encoding performance by implementing GPU acceleration using CUDA
```

### 5. Agent Workflow

The orchestrator executes the following workflow:

**Planner Agent**

- Breaks your task into 3-7 actionable steps
- Each step is independently executable
- Respects existing architecture

**Retriever Agent**

- Queries vector store for relevant code context
- Retrieves files related to your task
- Provides context to coder agent

**Coder Agent**

- Generates git diff patches for each step
- Applies Zero-Trust and security policies
- Follows language-specific patterns (Python, Go, TypeScript)

**Patch Applier**

- Creates isolated git worktree
- Applies patches to worktree (not main branch)
- Commits changes with descriptive messages

### Tester Agent

- Executes tests in Docker sandbox
- Validates code changes
- Ensures no regressions

### Reviewer Agent

- Reviews patches for correctness
- Checks security compliance
- Approves or requests changes

### 6. Review and Iterate

The system loops through steps until:

- All steps are completed successfully
- Reviewer approves all changes
- Tests pass in sandbox

If reviewer rejects changes:

- System regenerates patch
- Addresses reviewer feedback
- Re-tests and re-reviews

### 7. Merge Changes

Once all steps complete successfully:

```bash
# Review the worktree
cd .worktrees-<branch-name>
git log

# Merge to develop (for feature branches)
git checkout develop
git merge feature/video-processing-pipeline

# Or merge to main (for release branches)
git checkout main
git merge release/v1.0.0
```

## Video Engineering Use Cases

### Video Transcoding

**Task:** Implement video transcoding with FFmpeg

**System Actions:**

1. Planner breaks down: install FFmpeg, create transcoder class, add CLI interface, add tests
2. Retriever finds existing video processing code
3. Coder generates patches for transcoding logic
4. Tester validates transcoding with sample videos
5. Reviewer checks security (input validation, file permissions)

### Video Analysis

**Task:** Extract video metadata using OpenCV

**System Actions:**

1. Planner breaks down: install OpenCV, create analyzer class, extract metadata, add API endpoint
2. Retriever finds existing analysis modules
3. Coder generates patches following Python patterns
4. Tester validates with various video formats
5. Reviewer checks for security (file handling, memory limits)

### Streaming Integration

**Task:** Add HLS streaming support

**System Actions:**

1. Planner breaks down: implement HLS segmentation, create manifest generator, add streaming endpoint
2. Retriever finds existing streaming code
3. Coder generates patches following backend patterns
4. Tester validates streaming functionality
5. Reviewer checks for security (authentication, rate limiting)

## Best Practices

### Task Definition

- **Be Specific:** Define clear, measurable outcomes
- **Be Scoped:** Break large tasks into smaller iterations
- **Be Contextual:** Reference existing files or modules when possible

**Good:**

```text
Add video transcoding to app/video/transcoder.py using FFmpeg with H.264 codec
```

**Poor:**

```text
Improve video processing
```

### Branch Management

- Use `feature/*` branches for new features
- Use `hotfix/*` for critical production fixes
- Use `bugfix/*` for non-critical fixes
- Use `release/*` for release preparation

### Rule Configuration

- Keep security compliance rules (HIPAA, SOC2, ISO27001) disabled on feature branches
- Enable language patterns that match your tech stack
- Use `auto` for architecture patterns to allow detection

### Testing

- Always run tests in Docker sandbox
- Test with various video formats and codecs
- Validate edge cases (large files, corrupted videos, empty inputs)

## Troubleshooting

### Rules Not Applied

```bash
# Check current branch
git branch

# Check rule selection
python -c "from app.llm.rule_selector import RuleSelector; selector = RuleSelector(project_path='.'); print('Active rules:', selector.get_active_rules())"
```

### Worktree Issues

```bash
# Clean up worktrees
rm -rf .worktrees-*

# Remove git worktrees
git worktree prune
```

### Model Not Available

```bash
# Check Ollama models
ollama list

# Pull missing models
ollama pull qwen3.5
ollama pull qwen2.5-coder
ollama pull deepseek-r1
```

## Advanced Usage

### Custom Rule Files

Add custom rules to `app/llm/rules/`:

```markdown
---
name: Custom Video Processing Rule
description: Rules for video processing optimization
alwaysApply: false
---

# Video Processing Rules

- Always validate video file inputs
- Use GPU acceleration when available
- Implement progress tracking for long operations
- Handle encoding errors gracefully
```

### CLI Override Options

```bash
# Accept default rules without prompt
python scripts/run_task.py --accept-defaults

# Use custom config file
python scripts/run_task.py --rules-config path/to/custom-rules.yaml

# Force reconfiguration
python scripts/run_task.py --reconfigure
```

## Next Steps

- [Quick Start Guide](QUICKSTART.md) - Installation and basic usage
- [Architecture Documentation](ARCHITECTURE.md) - System design and components
- [Security Documentation](SECURITY.md) - Security controls and ZTA
- [Risk & Compliance](RISK_COMPLIANCE.md) - Compliance frameworks
