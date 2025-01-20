from flogin import Plugin, Query, Result
from deepseek import DeepSeek
import aiohttp
from settings import DeepSeekSettings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plugin import DeepSeekPlugin

class QuestionResult(Result["DeepSeekPlugin"]):
    def __init__(self, question: str) -> None:
        self.question = question
        super().__init__()

    async def callback(self):
        assert self.plugin
        
        resp = await self.plugin.deepseek.get_answer(self.question)
        return resp