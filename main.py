# -*- coding: utf-8 -*-

import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__)) # get the folder that your file is in
sys.path.append(parent_folder_path) # add the folder to path
sys.path.append(os.path.join(parent_folder_path, "lib")) # add a 'lib' folder that is in the same dir as your file to path
sys.path.append(os.path.join(parent_folder_path, "plugin"))
sys.path.append(os.path.join(parent_folder_path, "venv", "lib", "site-packages")) # add your venv to path
from flogin import ExecuteResponse, Plugin, Query, Result, SearchHandler
import aiohttp
import asyncio

plugin = Plugin()

class MyHandler(SearchHandler):
    async def callback(self, query: Query):
        return "This comes from my subclassed handler"
    
    async def on_error(self, query, error):
        return f"An error occured: {error}"

class MyResult(Result):
    async def callback(self):
        """Handle what happens when the user clicks on the result"""

        await plugin.api.show_notification("Flogin", "I work!")
        return ExecuteResponse(hide=False)

    async def on_error(self, error: Exception):
        """Handle errors from the 'callback' method"""

        await plugin.api.show_error_message(
            "Flogin",
            f"An error has occured while executing the result's callback: {error}",
        )
        return ExecuteResponse(hide=False)

    async def context_menu(self):
        """Generate this result's context menu"""

        return Result("This is a test")

    async def on_context_menu_error(self, error: Exception):
        """Handle errors from the 'context_menu' method"""

        return f"An error has occured: {error}"


async def deepseek_demo(question="你好", options=None):
    BASE_URL = "https://api.deepseek.com/v1/chat/completions"
    DEFAULT_MODEL = "deepseek-chat"
    DEFAULT_TEMPERATURE = 1.3  # 通用对话推荐温度
    DEEPSEEK_API_KEY = ""  # 替换为你的 DeepSeek API Key
    if options is None:
        options = {}

    model = options.get("model", DEFAULT_MODEL)
    temperature = options.get("temperature", DEFAULT_TEMPERATURE)
    is_short_answer = options.get("is_short_answer", not question.endswith('-'))  # 默认简短回答

    system_prompt = f"你是一位AI助手，能够回答的专业以及准确{', 现在请尽量用一句话回答我的问题' if is_short_answer else ''}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "messages": messages,
        "model": model,
        "temperature": temperature
    }


    async with aiohttp.ClientSession() as session:
        # 发送异步 HTTP 请求
        async with session.post(BASE_URL, headers=headers, json=payload, timeout=30) as response:
            # 检查 HTTP 状态码
            if response.status != 200:
                error_message = f"API请求失败: HTTP状态码 {response.status}, 响应数据: {await response.text()}"
                # logging.error(error_message)
                return f"抱歉，发生了错误: {error_message}"

            response_data = await response.json()

            return response_data["choices"][0]["message"].get("content", "")

# @plugin.search()
# async def on_search(data: Query):
#     return MyResult("This is my result")
# @plugin.search()
# async def my_simple_search_handler(data: Query):
#     return "This comes from my simple handler"

@plugin.search()
async def on_query(data: Query):
    yield f"Your text is: {data.text}"
    yield f"Your keyword is: {data.keyword}"
    yield Result(f"Your raw text is: {data.raw_text}", sub="keyword + text")
    if data.text.endswith("行"):
        yield await deepseek_demo()


if __name__ == "__main__":
    plugin.register_search_handler(MyHandler())
    plugin.run()