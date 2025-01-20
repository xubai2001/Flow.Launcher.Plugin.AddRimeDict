# -*- coding: utf-8 -*-

import sys,os
from flogin import ExecuteResponse, Plugin, Query, Result, SearchHandler
parent_folder_path = os.path.abspath(os.path.dirname(__file__)) # get the folder that your file is in
sys.path.append(parent_folder_path) # add the folder to path
sys.path.append(os.path.join(parent_folder_path, "lib")) # add a 'lib' folder that is in the same dir as your file to path
sys.path.append(os.path.join(parent_folder_path, "plugin"))
sys.path.append(os.path.join(parent_folder_path, "venv", "lib", "site-packages")) # add your venv to path



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


# @plugin.search()
# async def on_search(data: Query):
#     return MyResult("This is my result")
@plugin.search()
async def my_simple_search_handler(data: Query):
    return "This comes from my simple handler"


if __name__ == "__main__":
    plugin.register_search_handler(MyHandler())
    plugin.run()