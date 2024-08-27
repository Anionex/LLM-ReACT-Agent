from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
import json5

from chat_model import OpenAIChat
from tools import Tools
from prompts import REACT_PROMPT, TOOL_DESC



class Agent:
    def __init__(self, **kwargs) -> None: 
        self.tool = Tools()
        self.model = OpenAIChat(**kwargs)
        print("model info:", kwargs)
        self.hit_final_answer = False

    def build_system_input(self, query, extra_requirements):
        tool_descs, tool_names = [], []
        for tool in self.tool.toolConfig:
            tool_descs.append(TOOL_DESC.format(**tool))
            tool_names.append(tool['name_for_model'])
        tool_descs = '\n\n'.join(tool_descs)
        tool_names = ','.join(tool_names)
        sys_prompt = REACT_PROMPT.format(tool_descs=tool_descs, 
                                         tool_names=tool_names, 
                                         current_date=datetime.now().strftime("%Y-%m-%d"), 
                                         question=query,
                                         extra_requirements=extra_requirements)

        return sys_prompt
    
    def parse_latest_plugin_call(self, text):
        # 查找最后一个 Tool Invocation 和 Tool Input
        tool_invocation = text.split('Tool Invocation:')[-1].split('\n')[0].strip()
        tool_input = text.split('Tool Input:')[-1].split('\n')[0].strip()
        
        return tool_invocation, tool_input
    def call_plugin(self, plugin_name, plugin_args):
        try:
            plugin_args = json5.loads(plugin_args)
        except Exception as e:
            return '\nTool Output:' + f"工具执行出错：{str(e)} 请检查输入参数是否正确"
        try:
            if plugin_name == 'google_search':
                return '\nTool Output:' + str(self.tool.google_search(**plugin_args))
            elif plugin_name == 'calculator':
                return '\nTool Output:' + str(self.tool.calculator(**plugin_args))
            else:
                return '\nTool Output:' + "未知的工具名称，请重试"
        except Exception as e:
            return '\nTool Output:' + f"工具执行出错：{str(e)} 请检查输入参数是否正确"

    
    def step(self, scratchpad):
        return self.model.chat(scratchpad, [], self.system_prompt)[0]

    
    
    def run(self, query, extra_requirements=""):
        # 构建系统提示词
        self.system_prompt = self.build_system_input(query, extra_requirements)
        # print("system_prompt:", self.system_prompt)
        
        # 初始化scratchpad
        scratchpad = ""
        # scratchpad = "Question:" + query
        
        while True:
            response = self.step(scratchpad)  # 获取下一个响应[Analysis, Tool Invocation, Tool Input, Tool Output]
            
            if response.startswith("Final Answer:"):
                # print("--------------------------------")
                # #print(response)
                # print("--------------------------------")
                print("hit final answer")
                self.hit_final_answer = True
            elif response.startswith("Analysis:"):
                pass
            elif response.startswith("Tool Input:"):
                plugin_name, plugin_args = self.parse_latest_plugin_call(scratchpad+'\n'+ response)
                # print("using tool:", plugin_name)
                # print("using args:", plugin_args)
                delta = self.call_plugin(plugin_name, plugin_args)
                # print("delta:", delta)
                response += delta
                # print("response:", response)
            elif response.startswith("Tool Invocation:"):
                pass
            elif response.startswith("Tool Output:"):
                response = "you shouldn't get Tool Output by yourself, you should get it from the tools"
            else:
                response = "Invalid Output prefix, please use one of the following the next time: [Analysis, Tool Invocation, Tool Input, Tool Output]"
            # print("--------------------------------")
            print(response)
            # print("--------------------------------\n\n")
            scratchpad += '\n' + response
            if self.hit_final_answer:
                return response

if __name__ == '__main__':
    agent = Agent(model="gpt-4o", temperature=0, stop=["\n"])
    
    # result = agent.run("马斯克发射了多少颗卫星？")
    result = agent.run(input("请输入问题："), extra_requirements="始终用中文来回答")
    # print(result)