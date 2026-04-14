from app.sandbox.docker_runner import DockerSandbox
from app.sandbox.command_whitelist import is_command_allowed


class SandboxTestRunner:
    def __init__(self, workspace_dir: str):
        self.sandbox = DockerSandbox()
        self.workspace_dir = workspace_dir

    def run_tests(self, test_command: str = "pytest") -> dict:
        if not is_command_allowed(test_command):
            return {"success": False, "output": "Command not allowed"}

        self.sandbox.start(self.workspace_dir)
        try:
            exit_code, output, _ = self.sandbox.execute(test_command)
            return {
                "success": exit_code == 0,
                "output": output,
                "exit_code": exit_code
            }
        finally:
            self.sandbox.stop()
