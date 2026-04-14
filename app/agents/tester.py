from app.core.state import AgentState
from app.evaluation.test_runner import SandboxTestRunner


def tester_node(state: AgentState) -> AgentState:
    if "worktree_path" not in state:
        state["logs"].append("No worktree to test")
        return state

    runner = SandboxTestRunner(state["worktree_path"])
    result = runner.run_tests()

    state["logs"].append(f"Test result: {result['success']}")
    state["test_result"] = result

    return state
