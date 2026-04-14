import docker
from typing import List, Optional


class DockerSandbox:
    def __init__(self, image="python:3.14-slim"):
        self.client = docker.from_env()
        self.image = image
        self.container = None

    def start(self, workspace_dir: str):
        self.container = self.client.containers.run(
            self.image,
            command="tail -f /dev/null",  # Keep running
            volumes={workspace_dir: {"bind": "/workspace", "mode": "rw"}},
            detach=True,
            mem_limit="512m",
            cpu_quota=100000
        )

    def execute(self, command: str) -> tuple[int, str, str]:
        exit_code, output = self.container.exec_run(
            f"cd /workspace && {command}",
            workdir="/workspace"
        )
        return exit_code, output.decode("utf-8"), ""

    def stop(self):
        if self.container:
            self.container.stop()
            self.container.remove()
