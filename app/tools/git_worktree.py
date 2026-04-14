import git
import shutil
from pathlib import Path
from typing import Optional


class GitWorktreeManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo = git.Repo(repo_path)
        self.worktrees_dir = self.repo_path / ".git" / "worktrees"
    
    def create_worktree(self, branch_name: str, commit: Optional[str] = None) -> Path:
        worktree_path = self.repo_path / f".worktrees-{branch_name}"
        
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
        
        base_commit = commit or self.repo.head.commit.hexsha
        self.repo.git.worktree("add", str(worktree_path), base_commit, "-b", branch_name)
        
        return worktree_path
    
    def apply_patch(self, worktree_path: Path, patch_content: str) -> bool:
        try:
            repo = git.Repo(worktree_path)
            repo.git.apply(patch_content)
            return True
        except Exception as e:
            print(f"Failed to apply patch: {e}")
            return False
    
    def remove_worktree(self, branch_name: str):
        worktree_path = self.repo_path / f".worktrees-{branch_name}"
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
            self.repo.git.worktree("remove", f".worktrees-{branch_name}")
    
    def commit_changes(self, worktree_path: Path, message: str):
        repo = git.Repo(worktree_path)
        repo.git.add(A=True)
        repo.index.commit(message)
