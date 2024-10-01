from syrius.commands.LoopInputCommand import loopType
from syrius.commands.abstract import AbstractCommand, Command


class LumaImageToVideoCommand(Command):
    id: int = 56
    prompt: str | AbstractCommand | loopType
    image: str | AbstractCommand | loopType
    api_key: str | AbstractCommand | loopType