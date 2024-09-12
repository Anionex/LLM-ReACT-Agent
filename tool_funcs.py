import os
import json
import requests
import dotenv

dotenv.load_dotenv()



# 添加计算器工具
def calculator(expression: str):
    return eval(expression)



# 添加谷歌搜索工具
def google_search(search_query: str):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": search_query})
    headers = {
        'X-API-KEY': os.getenv('SERPER_API_KEY'),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response['organic'][0]['snippet']




