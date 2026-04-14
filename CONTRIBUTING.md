# Contributing to AI Orchestrator

Thank you for your interest in contributing to AI Orchestrator! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.14+ (installed via mise)
- Ollama with required models
- Docker (for sandboxed testing)
- Git

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd ai-orchestrator

# Install dependencies
python -m pip install -r requirements.txt

# Pull Ollama models
ollama pull qwen3.5
ollama pull qwen2.5-coder
ollama pull deepseek-r1
ollama pull nomic-embed-text
```

## Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Critical hotfixes

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. Write clear, concise commit messages
2. Follow the existing code style
3. Add tests for new functionality
4. Update documentation as needed
5. Ensure all tests pass

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat: add support for new LLM model

Added support for deepseek-r1 as an alternative reviewer model
to reduce memory footprint on systems with limited RAM.

Closes #123
```

## Pull Request Process

### Before Submitting

1. Ensure your code follows the project's style guidelines
2. Run tests and ensure they pass
3. Update documentation if needed
4. Add tests for new features
5. Squash related commits into a single commit

### Submitting a Pull Request

1. Push your branch to your fork
2. Create a pull request against `develop` branch
3. Provide a clear description of changes
4. Reference related issues
5. Request review from maintainers

### PR Review Process

- Maintainers will review your PR
- Address review comments promptly
- Keep the PR focused on a single issue
- Ensure CI checks pass

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Use descriptive variable names

### Documentation

- Use clear, concise language
- Update README.md for user-facing changes
- Update ARCHITECTURE.md for architectural changes
- Update SECURITY.md for security-related changes
- Add inline comments for complex logic

### Testing

- Write unit tests for new functionality
- Ensure tests are deterministic
- Mock external dependencies
- Test edge cases and error conditions

## Project Structure

```
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

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, Ollama version)
- Logs or error messages

### Feature Requests

Include:
- Description of the feature
- Use case and motivation
- Potential implementation approach
- Alternatives considered

## Security Issues

For security vulnerabilities, please do not open a public issue. Instead, send an email to the security team.

## Questions

For questions about:
- Using the project: Check documentation first
- Contributing: Check this guide or open a discussion
- Bugs: Open an issue
- Features: Open an issue or discussion

## Recognition

Contributors will be recognized in the project's contributors list.

## License

By contributing to AI Orchestrator, you agree that your contributions will be licensed under the MIT License.
