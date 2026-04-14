# AI Orchestrator

An autonomous AI agent system for code generation, testing, and deployment using LangGraph and Ollama.

## Overview

AI Orchestrator is a multi-agent system that automates software development workflows through a sophisticated graph-based architecture. It leverages local LLMs via Ollama to plan, retrieve context, generate code, apply patches, test in sandboxed environments, and review changes.

## Architecture

The system uses a directed graph workflow with specialized agents:

- **Planner Agent** - Breaks down tasks into actionable steps
- **Retriever Agent** - Retrieves relevant code context via vector search
- **Coder Agent** - Generates git diff patches for code changes
- **Patch Applier** - Applies patches to isolated git worktrees
- **Tester Agent** - Executes tests in Docker sandboxed containers
- **Reviewer Agent** - Reviews patches for correctness and security (deepseek-r1)

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Security & Zero Trust Architecture

This project implements a Zero Trust Architecture (ZTA) with multiple security layers:

- **Sandboxed Execution** - All code execution occurs in isolated Docker containers
- **Command Whitelisting** - Only approved test commands are allowed
- **Git Worktree Isolation** - Patches applied to isolated worktrees, not main branch
- **Resource Limits** - Containers have CPU and memory limits enforced
- **Input Validation** - All user inputs validated before processing
- **Output Validation** - Generated code reviewed before application

For comprehensive security documentation, see [docs/SECURITY.md](docs/SECURITY.md).

## Risk & Compliance

This system is designed with enterprise-grade security posture:

- **Supply Chain Security** - Local LLMs, no external API dependencies
- **Data Privacy** - All processing occurs locally, no data exfiltration
- **Audit Logging** - All actions logged for compliance and forensics
- **Access Control** - Role-based permissions for different operations
- **Compliance Frameworks** - Aligns with SOC 2, ISO 27001, and NIST standards

For detailed risk and compliance information, see [docs/RISK_COMPLIANCE.md](docs/RISK_COMPLIANCE.md).

## Documentation

- [Quick Start](docs/QUICKSTART.md) - Installation and usage guide
- [Usage Guide](docs/USAGE.md) - Agentic vibe engineering development workflow
- [Integration Guide](docs/INTEGRATION.md) - Hassle-free launch options and setup
- [Architecture](docs/ARCHITECTURE.md) - System architecture and design decisions
- [Security](docs/SECURITY.md) - Security controls and ZTA implementation
- [Risk & Compliance](docs/RISK_COMPLIANCE.md) - Risk assessment and compliance frameworks
- [Implementation Plan (Archived)](docs/archive/IMPLEMENTATION_PLAN.md) - Historical implementation roadmap

## Project Structure

```text
ai-orchestrator/
├── app/
│   ├── agents/          # Agent implementations
│   ├── api/             # API endpoints
│   ├── core/            # Graph and state management
│   ├── evaluation/      # Test runners and scoring
│   ├── llm/             # LLM client and prompts
│   ├── memory/          # Memory management
│   ├── retrieval/       # Vector search and indexing
│   ├── sandbox/         # Docker sandboxing
│   ├── security/        # Security controls
│   └── tools/           # Utility tools (git worktree)
├── config/              # Configuration files
├── docs/                # Documentation
├── scripts/             # Entry point scripts
├── tests/               # Test suites
└── workspace/           # Git worktrees
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Contributing

For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).
