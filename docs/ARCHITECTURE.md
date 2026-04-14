# Architecture Documentation

## System Overview

AI Orchestrator is a multi-agent system built on LangGraph that automates software development workflows. The system uses a directed acyclic graph (DAG) architecture where each node represents a specialized agent that performs a specific task in the development pipeline.

## Core Components

### 1. Graph Engine (LangGraph)

**Location**: `app/core/graph.py`

The graph engine orchestrates the flow between agents using LangGraph's StateGraph. It manages:

- Node registration and sequencing
- Conditional routing based on state
- State propagation through the pipeline
- Loop management for multi-step execution

**Graph Flow**:

```text
planner → retriever → coder → patch_applier → tester → reviewer
              ↑                                      ↓
              └────────────── conditional loop ──────┘
```

### 2. State Management

**Location**: `app/core/state.py`

AgentState is a TypedDict that maintains the shared state across all agents:

```python
class AgentState(TypedDict):
    task: str                    # Input task description
    plan: List[str]             # Breakdown of steps
    current_step: int           # Current step index
    context: List[str]          # Retrieved code context
    patch: Optional[str]        # Generated git diff
    review: Optional[str]       # Review feedback
    approved: bool              # Approval status
    logs: List[str]             # Execution logs
```

### 3. Agent Implementations

#### 3.1 Planner Agent

**Location**: `app/agents/planner.py`

**Model**: qwen3.5 (Ollama)

**Responsibilities**:

- Break down high-level tasks into actionable steps
- Generate numbered, executable steps
- Ensure steps are independent and testable

**Output**: List of step descriptions in `state["plan"]`

#### 3.2 Retriever Agent

**Location**: `app/agents/retriever.py`

**Model**: nomic-embed-text (Ollama embeddings)

**Responsibilities**:

- Query vector store for relevant code context
- Retrieve top-k similar documents
- Provide context to coder agent

**Components**:

- `app/llm/ollama_client.py` - Embedding generation
- `app/retrieval/vector_store.py` - ChromaDB vector store
- `app/retrieval/indexer.py` - Codebase indexing

**Output**: List of code snippets in `state["context"]`

#### 3.3 Coder Agent

**Location**: `app/agents/coder.py`

**Model**: qwen2.5-coder (Ollama)

**Responsibilities**:

- Generate git diff patches for current step
- Use retrieved context for informed code generation
- Output only valid patch format

**Output**: Git diff patch in `state["patch"]`

#### 3.4 Patch Applier

**Location**: `app/agents/patch_applier.py`

**Components**:

- `app/tools/git_worktree.py` - Git worktree management

**Responsibilities**:

- Create isolated git worktree for each step
- Apply patches to worktree (not main branch)
- Commit changes to worktree
- Clean up worktrees after completion

**Output**: Worktree path in `state["worktree_path"]`

#### 3.5 Tester Agent

**Location**: `app/agents/tester.py`

**Components**:

- `app/evaluation/test_runner.py` - Sandbox test runner
- `app/sandbox/docker_runner.py` - Docker container management
- `app/sandbox/command_whitelist.py` - Command validation

**Responsibilities**:

- Execute tests in Docker sandbox
- Enforce command whitelisting
- Capture test results and exit codes
- Clean up containers after execution

**Output**: Test results in `state["test_result"]`

#### 3.6 Reviewer Agent

**Location**: `app/agents/reviewer.py`

**Model**: deepseek-r1 (Ollama)

**Responsibilities**:

- Review generated patches for correctness
- Check for security risks and edge cases
- Approve or reject patches
- Advance to next step if approved
- Force retry if rejected

**Output**: Approval status in `state["approved"]`

## Multi-Step Execution

The system implements iterative execution through the plan:

1. **Initialization**: Planner creates a list of steps
2. **Current Step Processing**: Coder generates patch for `state["current_step"]`
3. **Review**: Reviewer evaluates the patch
4. **Decision Logic**:
   - If approved AND more steps remain: Increment `current_step`, reset `approved`, loop to coder
   - If approved AND all steps complete: Exit to END
   - If rejected: Keep `current_step`, set `approved=False`, loop to coder for retry

## Data Flow

```
User Task
    ↓
[Planner] → Plan Steps
    ↓
[Retriever] → Query Vector DB → Context
    ↓
[Coder] → Context + Step → Patch
    ↓
[Patch Applier] → Create Worktree → Apply Patch
    ↓
[Tester] → Docker Sandbox → Test Results
    ↓
[Reviewer] → Review → Approved?
    ↓ (No)
[Coder] ← Retry
    ↓ (Yes, more steps)
[Coder] ← Next Step
    ↓ (Yes, complete)
END
```

## Vector Database Architecture

**Technology**: ChromaDB (local development)

**Embedding Model**: nomic-embed-text via Ollama

**Indexing Strategy**:

- Scan codebase for supported file types (.py, .js, .ts)
- Chunk files into documents
- Generate embeddings for each document
- Store in ChromaDB with metadata (file path, line numbers)

**Query Strategy**:

- Generate embedding for query (task or current step)
- Perform similarity search (top-k)
- Return document contents as context

## Sandbox Architecture

**Technology**: Docker containers

**Isolation Layers**:

1. **Container Isolation**: Separate filesystem and process namespace
2. **Resource Limits**: CPU quota (100,000), memory limit (512MB)
3. **Volume Mounting**: Read-write mount of workspace directory
4. **Command Whitelisting**: Regex-based pattern matching
5. **Network Isolation**: Default bridge network (can be restricted further)

**Container Lifecycle**:

```
Start → Execute → Capture Output → Stop → Remove
```

## Git Worktree Architecture

**Purpose**: Isolate code changes from main branch

**Workflow**:

1. Create worktree from current commit
2. Apply patch to worktree
3. Commit changes to worktree branch
4. Test in worktree
5. (Optional) Merge to main after approval
6. Remove worktree

**Benefits**:

- No risk to main branch
- Parallel development
- Easy rollback
- Clean separation of concerns

## LLM Integration

**Provider**: Ollama (local inference)

**Models Used**:

- **qwen3.5** - General planning and reasoning
- **qwen2.5-coder** - Code generation and patch creation
- **deepseek-r1** - Code review and security analysis
- **nomic-embed-text** - Text embeddings for vector search

**Advantages**:

- No external API dependencies
- Data privacy (local processing)
- No rate limits or costs
- Customizable model selection

## Error Handling

**Current Implementation**:

- Try-catch blocks in critical operations
- Logging of failures in `state["logs"]`
- Graceful degradation where possible

**Future Enhancements**:

- Retry mechanisms for transient failures
- Circuit breakers for LLM API failures
- Comprehensive exception hierarchy
- Recovery strategies for each component

## Performance Considerations

**Optimization Opportunities**:

- Batch embedding generation
- Parallel document indexing
- Caching of vector store queries
- Connection pooling for Docker
- Async LLM invocations

**Bottlenecks**:

- LLM inference time (local models)
- Vector store query latency
- Docker container startup time
- Git worktree creation overhead

## Scalability

**Horizontal Scaling**:

- Multiple graph instances for parallel tasks
- Distributed vector store (Qdrant for production)
- Container orchestration (Kubernetes for Docker)

**Vertical Scaling**:

- GPU acceleration for LLM inference
- Increased memory for vector store
- Faster storage for git operations

## Monitoring & Observability

**Current Logging**:

- Execution logs in `state["logs"]`
- Agent-level action tracking
- Step progression tracking

**Future Enhancements**:

- Structured logging (JSON format)
- Metrics collection (Prometheus)
- Distributed tracing (OpenTelemetry)
- Alerting on failures
- Performance profiling

## Configuration

**Configuration Files** (currently stubs, to be implemented):

- `config/models.yaml` - LLM model configurations
- `config/logging.yaml` - Logging configuration
- `config/policies.yaml` - Security policies
- `config/settings.py` - Application settings

## Dependencies

**Core Dependencies**:

- `langgraph` - Graph orchestration
- `langchain-community` - LLM integrations
- `langchain-ollama` - Ollama LLM client
- `chromadb` - Vector database
- `docker` - Docker Python SDK
- `GitPython` - Git operations

**Python Version**: 3.14+
**Package Manager**: pip (via mise)

## Deployment Architecture

**Development**:

- Local execution with mise Python
- Local Ollama instance
- Local ChromaDB
- Local Docker daemon

**Production** (future):

- Containerized deployment
- Distributed vector store (Qdrant)
- Managed Docker (Kubernetes)
- External Ollama or alternative LLM service
- Centralized logging and monitoring
