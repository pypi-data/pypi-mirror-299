from syrius.commands.LoopInputCommand import loopType
from syrius.commands.abstract import AbstractCommand, Command


class LumaTextToVideoCommand(Command):
    id: int = 57
    prompt: str | AbstractCommand | loopType
    api_key: str | AbstractCommand | loopType