from app.core.state import AgentState
from app.tools.git_worktree import GitWorktreeManager


def patch_applier_node(state: AgentState) -> AgentState:
    import os
    repo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "workspace")
    branch_name = f"ai-orchestrator-step-{state['current_step']}"

    manager = GitWorktreeManager(repo_path)
    worktree_path = manager.create_worktree(branch_name)

    success = manager.apply_patch(worktree_path, state["patch"])

    if success:
        manager.commit_changes(worktree_path, f"Apply step {state['current_step']}")
        state["logs"].append(f"Patch applied to worktree: {worktree_path}")
        state["worktree_path"] = str(worktree_path)
    else:
        state["logs"].append("Failed to apply patch")
        state["approved"] = False  # Force review

    return state
