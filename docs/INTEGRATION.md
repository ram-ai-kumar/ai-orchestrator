# Hassle-Free Launch Options

This guide provides multiple convenient methods to launch AI Orchestrator for each software engineering session, including shell functions and VS Code integration.

## Current State

- Entry point: `python scripts/run_task.py`
- Requires: Python 3.14+, Ollama with models, Docker, Git
- Manual steps: Check dependencies, ensure services running, execute script

## Proposed Solutions

### Option 1: Shell Function

Create a shell function that can be sourced in `.zshrc` or `.bashrc`:

**File:** `scripts/ai-orchestrator.sh`

```bash
# AI Orchestrator launcher function
# Source this file in .zshrc or .bashrc: source /path/to/scripts/ai-orchestrator.sh

ai_orchestrator() {
    local project_dir="${AI_ORCHESTRATOR_DIR:-$PWD}"
    local accept_defaults="${1:---accept-defaults}"

    # Check prerequisites
    if ! command -v ollama &> /dev/null; then
        echo "Error: Ollama not found. Please install Ollama first."
        return 1
    fi

    if ! command -v docker &> /dev/null; then
        echo "Error: Docker not found. Please install Docker first."
        return 1
    fi

    # Check Ollama is running
    if ! ollama list &> /dev/null; then
        echo "Starting Ollama service..."
        ollama serve &
        sleep 3
    fi

    # Check required models
    local required_models=("qwen3.5" "qwen2.5-coder" "deepseek-r1" "nomic-embed-text")
    local missing_models=()

    for model in "${required_models[@]}"; do
        if ! ollama list | grep -q "$model"; then
            missing_models+=("$model")
        fi
    done

    if [ ${#missing_models[@]} -gt 0 ]; then
        echo "Missing Ollama models: ${missing_models[*]}"
        echo "Pulling missing models..."
        for model in "${missing_models[@]}"; do
            ollama pull "$model"
        done
    fi

    # Check Docker is running
    if ! docker info &> /dev/null; then
        echo "Error: Docker not running. Please start Docker."
        return 1
    fi

    # Launch orchestrator
    cd "$project_dir" || return 1
    python scripts/run_task.py
}
```

**Usage:**

```bash
# Source in shell config
source /path/to/scripts/ai-orchestrator.sh

# Run from anywhere
ai_orchestrator

# Run with manual rule selection
ai_orchestrator --manual
```

### Option 2: VS Code Task

Create VS Code tasks for one-click launch from the command palette.

**File:** `.vscode/tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "AI Orchestrator: Launch",
      "type": "shell",
      "command": "python",
      "args": ["scripts/run_task.py"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "options": {
        "cwd": "${workspaceFolder}"
      }
    },
    {
      "label": "AI Orchestrator: Launch with Manual Rules",
      "type": "shell",
      "command": "python",
      "args": ["scripts/run_task.py"],
      "group": "build",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "options": {
        "cwd": "${workspaceFolder}",
        "env": {
          "AI_ORCHESTRATOR_ACCEPT_DEFAULTS": "false"
        }
      }
    },
    {
      "label": "AI Orchestrator: Check Prerequisites",
      "type": "shell",
      "command": "bash",
      "args": ["-c", "ollama list && docker info && python --version"],
      "group": "test",
      "problemMatcher": []
    }
  ]
}
```

**Usage:**

- Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
- Type "Tasks: Run Task"
- Select "AI Orchestrator: Launch"

### Option 3: Makefile Targets

Create convenient Makefile targets for common operations.

**File:** `Makefile`

```makefile
.PHONY: help orchestrator orchestrator-manual check-prerequisites pull-models

help:
	@echo "AI Orchestrator - Available Targets:"
	@echo "  make orchestrator          - Launch AI Orchestrator (accept defaults)"
	@echo "  make orchestrator-manual   - Launch with manual rule selection"
	@echo "  make check-prerequisites   - Check if all prerequisites are met"
	@echo "  make pull-models           - Pull required Ollama models"
	@echo "  make install               - Install Python dependencies"

orchestrator:
	@python scripts/run_task.py

orchestrator-manual:
	@AI_ORCHESTRATOR_ACCEPT_DEFAULTS=false python scripts/run_task.py

check-prerequisites:
	@echo "Checking prerequisites..."
	@command -v ollama >/dev/null 2>&1 || echo "❌ Ollama not found"
	@command -v docker >/dev/null 2>&1 || echo "❌ Docker not found"
	@command -v python >/dev/null 2>&1 || echo "❌ Python not found"
	@ollama list >/dev/null 2>&1 && echo "✅ Ollama running" || echo "❌ Ollama not running"
	@docker info >/dev/null 2>&1 && echo "✅ Docker running" || echo "❌ Docker not running"
	@echo "Checking Ollama models..."
	@ollama list | grep qwen3.5 >/dev/null 2>&1 && echo "✅ qwen3.5" || echo "❌ qwen3.5"
	@ollama list | grep qwen2.5-coder >/dev/null 2>&1 && echo "✅ qwen2.5-coder" || echo "❌ qwen2.5-coder"
	@ollama list | grep deepseek-r1 >/dev/null 2>&1 && echo "✅ deepseek-r1" || echo "❌ deepseek-r1"
	@ollama list | grep nomic-embed-text >/dev/null 2>&1 && echo "✅ nomic-embed-text" || echo "❌ nomic-embed-text"

pull-models:
	@echo "Pulling required Ollama models..."
	@ollama pull qwen3.5
	@ollama pull qwen2.5-coder
	@ollama pull deepseek-r1
	@ollama pull nomic-embed-text

install:
    @python -m pip install -r requirements.txt
```

**Usage:**

```bash
make orchestrator
make orchestrator-manual
make check-prerequisites
```

### Option 4: Wrapper Script with Auto-Setup

Create a comprehensive wrapper script that handles all setup automatically.

**File:** `scripts/launch.sh`

```bash
#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python
check_python() {
    log_info "Checking Python installation..."
    if ! command -v python &> /dev/null; then
        log_error "Python not found. Please install Python 3.14+"
        exit 1
    fi
    python --version
}

# Check dependencies
check_dependencies() {
    log_info "Checking Python dependencies..."
    if ! python -c "import langgraph" 2>/dev/null; then
        log_warn "Dependencies not installed. Installing..."
        python -m pip install -r requirements.txt
    fi
    log_info "Dependencies installed"
}

# Check Ollama
check_ollama() {
    log_info "Checking Ollama..."
    if ! command -v ollama &> /dev/null; then
        log_error "Ollama not found. Please install from https://ollama.com"
        exit 1
    fi

    # Check if Ollama is running
    if ! ollama list &> /dev/null; then
        log_warn "Ollama not running. Starting..."
        ollama serve &
        sleep 5
    fi
    log_info "Ollama running"
}

# Check Ollama models
check_models() {
    log_info "Checking Ollama models..."
    local models=("qwen3.5" "qwen2.5-coder" "deepseek-r1" "nomic-embed-text")
    local missing=()

    for model in "${models[@]}"; do
        if ! ollama list | grep -q "$model"; then
            missing+=("$model")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        log_warn "Missing models: ${missing[*]}"
        log_info "Pulling missing models..."
        for model in "${missing[@]}"; do
            ollama pull "$model"
        done
    fi
    log_info "All models available"
}

# Check Docker
check_docker() {
    log_info "Checking Docker..."
    if ! command -v docker &> /dev/null; then
        log_error "Docker not found. Please install Docker"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker not running. Please start Docker"
        exit 1
    fi
    log_info "Docker running"
}

# Check git
check_git() {
    log_info "Checking Git..."
    if ! command -v git &> /dev/null; then
        log_error "Git not found. Please install Git"
        exit 1
    fi
    log_info "Git available"
}

# Launch orchestrator
launch() {
    log_info "Launching AI Orchestrator..."
    log_info "Current branch: $(git branch --show-current)"
    python scripts/run_task.py
}

# Main
main() {
    log_info "AI Orchestrator"
    log_info "==============="

    check_python
    check_dependencies
    check_ollama
    check_models
    check_docker
    check_git

    echo ""
    log_info "All checks passed. Launching..."
    echo ""

    launch
}

main "$@"
```

**Usage:**

```bash
chmod +x scripts/launch.sh
./scripts/launch.sh
```

### Option 5: VS Code Launch Configuration

Create VS Code launch configuration for debugging and running.

**File:** `.vscode/launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "AI Orchestrator: Run",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/run_task.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "AI Orchestrator: Debug",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/run_task.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "AI_ORCHESTRATOR_DEBUG": "true"
      },
      "justMyCode": false
    }
  ]
}
```

## Recommended Implementation Approach

**Primary Solution:** Option 4 (Wrapper Script)

- Most comprehensive
- Handles all setup automatically
- Single command to launch
- Clear error messages with colors
- Cross-platform compatible

**Secondary Solution:** Option 2 (VS Code Tasks)

- For VS Code users
- Integrated into IDE workflow
- Quick access via command palette
- Multiple launch options

**Tertiary Solution:** Option 3 (Makefile)

- For developers comfortable with make
- Easy to remember commands
- Additional utility targets (check, install, etc.)

## Implementation Steps

1. Create `scripts/launch.sh` with comprehensive wrapper script
2. Make script executable: `chmod +x scripts/launch.sh`
3. Create `.vscode/tasks.json` for VS Code integration
4. Create `Makefile` for alternative launch method
5. Update README.md with launch instructions
6. Add alias to shell config (optional)
7. Test all launch methods
8. Document in USAGE.md

## User Experience

**With Wrapper Script:**

```bash
# One-time setup
chmod +x scripts/launch.sh

# Every session
./scripts/launch.sh
```

**With VS Code:**

- Press `Cmd+Shift+P`
- Type "Tasks: Run Task"
- Select "AI Orchestrator: Launch"

**With Makefile:**

```bash
make orchestrator
```

**With Shell Function:**

```bash
# One-time setup in .zshrc
source scripts/ai-orchestrator.sh

# Every session
ai_orchestrator
```
