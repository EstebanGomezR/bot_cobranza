import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import tiktoken

dir = os.getcwd()
# Cargar variables de entorno
load_dotenv(dotenv_path=os.path.join(dir,"../.env"))


# Modelo de 4 mini
llm_chat_mini = AzureChatOpenAI(
    azure_deployment = "ChatGPT4omini-TigoAgentless-EsteUS",
    openai_api_version = "2024-02-01",
    api_key = "7828580e6a7f4fb28bb7813de2b8db15",
    azure_endpoint = "https://oai-prd-tigo-hog-soptec-n1.openai.azure.com/",
    request_timeout = 60,
    max_retries = 2,
    max_tokens=None
)

# Encoder de tiktoken para longitud de textos
#encoder = tiktoken.encoding_for_model('gpt-3.5-turbo')