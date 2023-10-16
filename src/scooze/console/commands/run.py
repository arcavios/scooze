import uvicorn
from cleo.commands.command import Command


class RunCommand(Command):
    name = "run"
    description = "Run the Swagger UI/ReDocs."

    def handle(self):
        # TODO(6): Replace localhost with wherever we're hosting
        uvicorn.run("scooze.main:app", host="127.0.0.1", port=8000, reload=True)
