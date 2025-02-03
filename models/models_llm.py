import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import tiktoken

dir = os.getcwd()
# Cargar variables de entorno
load_dotenv(dotenv_path=os.path.join(dir,"../.env"))


# Modelo de 4 mini
llm_chat_mini = AzureChatOpenAI(
    azure_deployment = os.getenv('AZURE_OPENAI_GPT4O_MINI'),
    openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION'),
    api_key = os.getenv('AZURE_OPENAI_API_KEY'),
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT'),
    request_timeout = 60,
    max_retries = 2,
    max_tokens=None
)

# Encoder de tiktoken para longitud de textos
#encoder = tiktoken.encoding_for_model('gpt-3.5-turbo')