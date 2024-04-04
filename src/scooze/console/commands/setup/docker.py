import subprocess

import docker
from cleo.commands.command import Command
from docker.errors import APIError, ImageNotFound


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
        if p.returncode:
            self.line("Cannot connect to Docker daemon -- Is docker installed and running?")
            return
        client = docker.from_env()
        try:
            scooze_container = client.containers.get("scooze-mongodb")
        except (APIError, ImageNotFound):
            # image doesn't yet exist; create and start it
            self.line("Setting up latest MongoDB Docker container as scooze-mongodb...")
            # Start Docker container
            client.containers.run("mongo:latest", detach=True, ports=({"27017/tcp": 27017}), name="scooze-mongodb")
            self.line("Done. MongoDB running on localhost:27017.")
            return
        if scooze_container.status == "running":
            self.line("scooze mongodb container already running! Exiting.")
        else:
            self.line("scooze mongodb container exists, but not running; starting...")
            scooze_container.start()
