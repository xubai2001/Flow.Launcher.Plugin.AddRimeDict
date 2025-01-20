# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher
import webbrowser


class HelloWorld(FlowLauncher):

    def query(self, query):
        return [
            {
                "Title": "这是标题 {}".format(('我查询的是 ' + query , query)[query == '']),
                "SubTitle": "这是副标题, 按enter会打开我的仓库",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/xubai2001/Flow.Launcher.Plugin.AddRimeDictr"]
                }
            }
        ]

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

if __name__ == "__main__":
    HelloWorld()
