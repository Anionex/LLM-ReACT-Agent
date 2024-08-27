TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""
REACT_PROMPT_OLD = """You have access to the following tools:
Knowledge cutoff: 2023-10
Current date: {current_date}
{tool_descs}

Your task is to answer a question using interleaving 'Analysis', 'Tool Invocation', and 'Tool Output' steps like this:

Analysis: you should always think about what to do
Tool Invocation: the Tool Invocation to take, should be one of [{tool_names}]
Tool Input: the input to the Tool Invocation
Tool Output: the result of the Tool Invocation
... (this Analysis/Tool Invocation/Tool Input/Tool Output can be repeated zero or more times)
Analysis: I now know the final answer
Final Answer: the final answer to the original input question

The user will provide previous steps of Analysis, Tool Invocation, Tool Input, Tool Output. You only need to continue thinking about the next Analysis/Tool Invocation/Tool Input/Tool Output based on this information. The output should be a single line.
Answer the following questions as best you can using the provided tools, following the given format.DO NOT REPEAT previous chat history.
Question: {question}
Begin!
"""


REACT_PROMPT = """You are a highly intelligent assistant tasked with solving the following problem:

{question}

The user will provide you with an ongoing sequence of steps including Analysis, Tool Invocation, Tool Input, and Tool Output. Your job is to append the next appropriate step in the sequence based on the provided Tool Output. You should only add the next Analysis, Tool Invocation, or Tool Input as needed.

### Instructions:
- Only generate the next step in the sequence (Analysis, Tool Invocation, or Tool Input).
- Do not repeat any steps that have already been provided by the user.
- Do not generate multiple steps at once. Focus on generating only the immediate next step.
- Tool Output will be provided by the system. Do not attempt to generate Tool Output yourself.
- If you get the final answer, you should use the format "Final Answer: <answer>" to provide the final response.

### Tool Descriptions:
{tool_descs}

### Task Execution Example:

**Example 1:**
problem: 马斯克比他的大儿子大几岁？
User provides:

Analysis: 为了得到马斯克比他的大儿子大几岁，需要知道马斯克和他大儿子的出生日期。
Tool Invocation: google_search: 
Tool Input: 'search_query': '马斯克年龄'.
Tool Output: 截至目前，马斯克的年龄是52岁。
Analysis: 知道了马斯克的年龄，还需要知道他大儿子的年龄。

Your output:
Tool Invocation: google_search

### Important Notes:
- Only append the next step in the sequence.
- Do not generate multiple steps at once.
- Do not attempt to generate Tool Output yourself; this will be provided by the system.

### Useful information:
Knowledge cutoff: 2023-10
Current date: {current_date}

{extra_requirements}
"""