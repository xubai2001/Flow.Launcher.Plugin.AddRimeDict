from __future__ import annotations
from flogin import Plugin, Query
from results import QuestionResult
from settings import DeepSeekSettings
from deepseek import DeepSeek
import aiohttp

class DeepSeekPlugin(Plugin[DeepSeekSettings]):
    session: aiohttp.ClientSession
    _deepseek: DeepSeek | None = None

    @property
    def model(self) -> str:
        return self.settings.model
    @property
    def api_key(self) -> str:
        return self.settings.api_key
    
    @property
    def system_prompt(self) -> str:
        return self.settings.default_prompt
    
    @property
    def user_prompt(self) -> str:
        return self.settings.user_prompt
    
    @property
    def endpoint(self) -> str:
        return self.settings.api_endpoint
    
    @property
    def prompt_stop(self) -> str:
        return self.settings.prompt_stop
    
    async def start(self):
        async with aiohttp.ClientSession() as cs:
            self.session = cs
            await super().start()
    
    async def on_search(self, query: Query):
        if query.text.endswith(self.prompt_stop):
            return QuestionResult(query.text[:-len(self.prompt_stop)])
        



    