import uvicorn
from cleo.commands.command import Command
from cleo.helpers import option


class RunCommand(Command):
    name = "run"
    description = "Run the Swagger UI/ReDocs."

    options = [
        option(
            "reload",
            description="Live-reload source files.",
            flag=True,
        ),
    ]

    def handle(self):
        # TODO(6): Replace localhost with wherever we're hosting
        uvicorn.run("scooze.main:app", host="0.0.0.0", port=8000, reload=self.option("reload"))
