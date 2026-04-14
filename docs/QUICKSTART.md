# Quick Start Guide

This guide will help you get AI Orchestrator up and running quickly.

## Prerequisites

- Python 3.14+ (installed via mise)
- Ollama with required models:
  - `qwen3.5:latest` (planner)
  - `qwen2.5-coder:latest` (coder)
  - `deepseek-r1:latest` (reviewer)
  - `nomic-embed-text:latest` (embeddings)
- Docker (for sandboxed testing)
- Git (for worktree management)

## Installation

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Pull Ollama Models

```bash
ollama pull qwen3.5
ollama pull qwen2.5-coder
ollama pull deepseek-r1
ollama pull nomic-embed-text
```

### Verify Ollama Installation

```bash
ollama list
```

You should see all required models listed:

- qwen3.5:latest
- qwen2.5-coder:latest
- deepseek-r1:latest
- nomic-embed-text:latest

## Usage

### Run the Orchestrator

```bash
python scripts/run_task.py
```

### Example Task

When prompted, enter a task such as:

```text
Add error handling to the file app/agents/coder.py
```

The orchestrator will:

1. Break down the task into steps
2. Retrieve relevant code context
3. Generate patches for each step
4. Apply patches to isolated worktrees
5. Test changes in Docker sandbox
6. Review patches for correctness
7. Repeat until all steps are complete

## Troubleshooting

### Ollama Not Running

```bash
# Start Ollama service
ollama serve
```

### Docker Not Running

```bash
# Start Docker daemon
sudo systemctl start docker  # Linux
# or open Docker Desktop on macOS/Windows
```

### Python Path Issues

```bash
# Ensure using correct Python
which python
# Should show: /Users/ram/.local/share/mise/installs/python/3.14.4/bin/python
```

### Module Not Found Errors

```bash
# Install with correct Python
/Users/ram/.local/share/mise/installs/python/3.14.4/bin/python -m pip install -r requirements.txt
```

## Next Steps

- Read the [Architecture documentation](ARCHITECTURE.md) to understand the system design
- Review the [Security documentation](SECURITY.md) to understand security controls
- Check the [Risk & Compliance documentation](RISK_COMPLIANCE.md) for risk assessment
