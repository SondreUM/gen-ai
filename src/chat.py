from abc import abstractmethod
from pathlib import Path
from langchain_core.messages.base import BaseMessage
from langchain_openai.chat_models import AzureChatOpenAI
import ollama
from ollama import Message

from config import KEY_PATH

API_KEY = None
API_VERSION = "2024-02-01" # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
ENDPOINT = "https://gpt-course.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-35"

def init_agent() -> AzureChatOpenAI:
    global API_KEY

    with open(KEY_PATH / "gpt_key.txt") as file:
        API_KEY = file.read().strip()

    agent = AzureChatOpenAI(
        api_key = API_KEY,
        api_version = API_VERSION,
        azure_endpoint = ENDPOINT,
        deployment_name = DEPLOYMENT_NAME
    )

    return agent

class AbstractLLM:
    @abstractmethod
    def invoke(self, query: str, **kwargs) -> str | list[str | dict]:
        pass

# GPT version
class LLM(AbstractLLM):
    def __init__(self) -> None:
        self.agent = init_agent()

    def invoke(self, query: str, **kwargs) -> str | list[str | dict]:
        """query the llm and get a response"""
        response = self.agent.invoke(query, **kwargs).content

        return response

# Ollama version
#class LLM(AbstractLLM):
#    def __init__(self) -> None:
#        self.agent = ollama
#
#        # the "memory of the model"
#        self.messages:list[Message] = []
#
#    def invoke(self, query: str, **kwargs) -> str | list[str | dict]:
#        """query the llm and get a response"""
#        message = Message({"role": "user", "content": query})
#        self.messages.append(message)
#
#        response = self.agent.chat( model="llama2-uncensored",
#                                    messages=self.messages)
#
#        self.messages.append(response["message"])
#
#        return response["message"]["content"]

if __name__ == "__main__":
    agent = LLM()
    print(agent.invoke("Hello, how are you?"))
    #chatbot = LLM()
    #print(chatbot.invoke("where does microsoft have offices in Norway?"))
    #print(chatbot.invoke("what was the last question I asked you?"))
