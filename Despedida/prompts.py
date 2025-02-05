from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from models import models_llm
from langchain.pydantic_v1 import BaseModel, Field


prompt_despedida = ChatPromptTemplate.from_template("""
                Eres un experto en cobranzas de la empresa abc. Tu misión es despedirte del usuario de forma muy amable y agradecer por los datos brindados
                Tu respuesta debe ser maximo de 30 palabras
               
""")
# Chain
chain_prompt_despedida = prompt_despedida | models_llm.llm_chat_mini | StrOutputParser()


