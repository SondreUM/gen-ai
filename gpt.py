from pathlib import Path
from langchain_openai.chat_models import AzureChatOpenAI

PROJECT_PATH = Path(__file__).parent

API_KEY = None
API_VERSION = "2024-02-01" # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
ENDPOINT = "https://gpt-course.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-35"

def init_agent():
    global API_KEY
    
    with open(PROJECT_PATH / "api_key.txt") as file:
        API_KEY = file.read().strip()
    
    agent = AzureChatOpenAI(
        api_key = API_KEY, 
        api_version = API_VERSION, 
        azure_endpoint = ENDPOINT,
        deployment_name = DEPLOYMENT_NAME
    )

    return agent

if __name__ == "__main__":
    agent = init_agent()
    print(agent.invoke("Hello, how are you?").content)