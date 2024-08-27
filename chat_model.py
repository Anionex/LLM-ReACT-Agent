from typing import Dict, List, Optional, Tuple, Union
import dotenv
import os
dotenv.load_dotenv()

class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: List[dict]):
        pass

    def load_model(self):
        pass
    
if os.getenv('LANGFUSE_SECRET_KEY'):
    from langfuse.openai import OpenAI
else:
    from openai import OpenAI

class OpenAIChat(BaseModel):
    def __init__(self, path: str = '', **kwargs) -> None:
        super().__init__(path)
        self.load_model(**kwargs)
        self.kwargs = kwargs

    def load_model(self, **kwargs):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )
        
    def chat(self, prompt: str, history: List[dict], meta_instruction:str ='') -> Tuple[str, List[dict]]:
        """
        normal chat
        """
        is_verbose = self.kwargs.get('is_verbose', False)
        # history 应该是类似遵循openai对话结构
        messages = []
        if meta_instruction:
            messages.append({"role": "system", "content": meta_instruction})
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            messages=messages,
            stream=True,
            **self.kwargs
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                if is_verbose:
                    print(chunk.choices[0].delta.content, end="")
                full_response += chunk.choices[0].delta.content
        if is_verbose:
            print()
        return full_response, history
if __name__ == '__main__':
    model = OpenAIChat(model='gpt-4o', temperature=0, stop=['\n'])
    print(model.chat('输出一个唐诗', [])[0])

