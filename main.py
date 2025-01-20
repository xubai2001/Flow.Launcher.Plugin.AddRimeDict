# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__)) # get the folder that your file is in
sys.path.append(parent_folder_path) # add the folder to path
sys.path.append(os.path.join(parent_folder_path, "lib")) # add a 'lib' folder that is in the same dir as your file to path
sys.path.append(os.path.join(parent_folder_path, "plugin"))
sys.path.append(os.path.join(parent_folder_path, "venv", "lib", "site-packages")) # add your venv to path


from flogin import Plugin, Query, Result

plugin = Plugin()

@plugin.search()
async def on_query(data: Query):
    yield f"Your text is: {data.text}"
    yield f"Your keyword is: {data.keyword}"
    yield Result(f"Your raw text is: {data.raw_text}", sub="keyword + text")


if __name__ == "__main__":
    plugin.run()