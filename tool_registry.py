import os
import json
import requests
from typing import Dict, Any, Callable

"""
工具函数

- 首先要在 tools 中添加工具的描述信息
- 然后在 tools 中添加工具的具体实现

- https://serper.dev/dashboard
"""

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register(self, name_for_human: str, name_for_model: str, func: Callable, description: str, parameters: list):
        
        self.tools[name_for_model] = {
            'name_for_human': name_for_human,
            'name_for_model': name_for_model,
            'description_for_model': description,
            'parameters': parameters,
            'function': func
        }

    def get_tool_configs(self):
        return [{k: v for k, v in tool.items() if k != 'function'} for tool in self.tools.values()]

    def execute_tool(self, name: str, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        return self.tools[name]['function'](**kwargs)

class Tools:
    def __init__(self):
        self.registry = ToolRegistry()
        self._register_default_tools()

    def _register_default_tools(self):
        # register default tools here
        pass

    @property
    def toolConfig(self):
        return self.registry.get_tool_configs()

    def google_search(self, search_query: str):
        url = "https://google.serper.dev/search"

        payload = json.dumps({"q": search_query})
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()

        return response['organic'][0]['snippet']
    
    def calculator(self, expression: str):
        return eval(expression)

    def add_tool(self, name_for_human: str, name_for_model: str, func: Callable, description: str, parameters: list = []):
        self.registry.register(name_for_human, name_for_model, func, description, parameters)

    def execute_tool(self, name: str, **kwargs):
        return self.registry.execute_tool(name, **kwargs)

if __name__ == '__main__':
    tool = Tools()
    print(tool.execute_tool('google_search', search_query='python'))


