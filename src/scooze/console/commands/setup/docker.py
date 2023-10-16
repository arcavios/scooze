import subprocess

import docker
from cleo.commands.command import Command


class SetupDockerCommand(Command):
    name = "setup docker"
    description = "Setup MongoDB in a Docker container."

    def handle(self):
        # Check if Docker is installed and running
        p = subprocess.run(
            "docker stats --no-stream",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        if not p.returncode:
            client = docker.from_env()
            # Check if Docker container is already running
            containers = client.containers.list(all=True)
            if "scooze-mongodb" in [container.name for container in containers]:
                self.line("Scooze mongodb container already exists! Exiting.")
            else:
                self.line("Setting up latest MongoDB Docker container as scooze-mongodb...")
                # Start Docker container
                client.containers.run("mongo:latest", detach=True, ports=({"27017/tcp": 27017}), name="scooze-mongodb")
                self.line("Done. MongoDB running on localhost:27017.")
        else:
            self.line("Cannot connect to Docker daemon -- Is docker installed and running?")
