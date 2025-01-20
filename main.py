# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher
import webbrowser
import requests

class HelloWorld(FlowLauncher):
    def __init__(self):
        self.api_key = self.settings.get("api_key")
        self.model = self.settings.get("model")
        self.prompt_stop = self.settings.get("prompt_stop")
        self.default_system_prompt = self.settings.get("default_prompt")
        self.api_endpoint = self.settings.get("api_endpoint")
    def query(self, query):
        if not self.api_key:
            self.add_item(
                title="无法加载API Key",
                subtitle=("请在插件设置中添加API Key")
            )
        
        if query.endswith(self.prompt_stop):
            user_prompt = query[:-len(self.prompt_stop)]
            answer = self.send_query(user_prompt)
            
            if answer:
                self.add_item(
                    title=answer,
                    subtitle=("回答: {}".format(user_prompt))
                )
        else:
            self.add_item(
                title="请输入要查询的句子",
                subtitle=("输入后按下回车即可"),
            )
        return

    def context_menu(self, data):
        return [
            {
                "Title": "上下文菜单1",
                "SubTitle": "打开flowlauncher仓库",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
                }
            },
            {
                "Title": "上下文菜单2",
                "SubTitle": "打开我的仓库",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/xubai2001/Flow.Launcher.Plugin.AddRimeDictr"]
                }
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)

    def send_query(self, user_prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_key)
        }
        json_data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.default_system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "stream": False
        }
        response = requests.post(self.api_endpoint, headers=headers, json=json_data)
        if response.status_code == 200:
            try:
                result = response.json()
                result = result["choices"][0]["message"]["content"]
            except:
                result = "未知错误"
        else:
            result = "API请求失败, 状态码: {}".format(response.status_code)
        return result

if __name__ == "__main__":
    HelloWorld()
