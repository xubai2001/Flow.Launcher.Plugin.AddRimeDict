# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))


# from plugin.main import HelloWorld

# if __name__ == "__main__":
#     HelloWorld()
from flogin import Plugin, Query
plugin = Plugin()
@plugin.search()
async def compare_results(data: Query):
    result = await plugin.api.fuzzy_search(data.text, "Flow")
    return f"Flow: {result.score}"