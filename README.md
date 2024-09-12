# 项目简介

本项目是一个基于ReAct（Reasoning and Acting）框架的智能代理系统，能够通过调用不同的工具来回答用户的问题。主要功能包括谷歌搜索和计算器等。系统基于GPT-4模型，通过推理和行动的交互来生成答案。支持添加工具。

## 准备

1. 克隆项目代码：
    ```bash
    git clone https://github.com/Anionex/LLM-ReACT-Agent
    cd LLM-ReACT-Agent
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

3. 配置环境变量：
    在项目根目录下创建一个`.env`文件，并添加以下内容：
    ```env
    SERPER_API_KEY=<your_serper_api_key> # 若要使用谷歌搜索
    OPENAI_API_KEY=<your_openai_api_key>
    OPENAI_API_BASE=<your_openai_api_base_url>
    ```

## 使用方法

### 运行ReAct代理

1. 进入项目目录，运行以下命令启动ReAct代理：
    ```bash
    python react_agent.py
    ```

2. 系统会提示输入问题和额外要求，按提示输入即可获取答案。

### 工具添加

可以通过以下方法向系统中添加新的工具：

1. 在`tool_funcs.py`中定义新的工具函数。例如，定义一个简单的加法工具：
    ```python
    def add(a: int, b: int) -> int:
        return a + b
    ```

2. 在`react_agent.py`中注册新工具：
    ```python
    agent.tools.add_tool(
        name_for_human="加法",
        name_for_model="add",
        func=add,
        description="加法工具，用于计算两个数的和。",
        parameters=[
            {
                'name': 'a',
                'description': '第一个加数',
                'required': True,
                'schema': {'type': 'integer'},
            },
            {
                'name': 'b',
                'description': '第二个加数',
                'required': True,
                'schema': {'type': 'integer'},
            }
        ]
    )
    ```

### 示例代码

以下是一个完整的示例，展示了如何定义和注册一个新的工具：

```python
# tool_funcs.py
def add(a: int, b: int) -> int:
    return a + b

# react_agent.py
if __name__ == '__main__':
    agent = ReactAgent(model="gpt-4o")

    agent.tools.add_tool(
        name_for_human="加法",
        name_for_model="add",
        func=add,
        description="加法工具，用于计算两个数的和。",
        parameters=[
            {
                'name': 'a',
                'description': '第一个加数',
                'required': True,
                'schema': {'type': 'integer'},
            },
            {
                'name': 'b',
                'description': '第二个加数',
                'required': True,
                'schema': {'type': 'integer'},
            }
        ]
    )

    result = agent.run(input("请输入问题："), extra_requirements=input("请输入额外要求："))
    print(result)
```

通过以上步骤，您可以轻松地向系统中添加新的工具，并通过智能助手调用这些工具来回答用户的问题。
