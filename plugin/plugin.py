from __future__ import annotations
from flogin import Plugin, Query
from settings import DeepSeekSettings

class DeepSeek(Plugin[DeepSeekSettings]):

    @property
    def model(self):
        return ""
    @Plugin.search()
    async def on_search(self, query: Query):
        return self.settings.model