from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from models import models_llm
from langchain.pydantic_v1 import BaseModel, Field


prompt_parametros_acuero_pago = ChatPromptTemplate.from_template("""
                Eres un experto en cobranzas de la empresa abc. Tu misión es identificar dentro de la respuesta del usuario qué está expresando respecto a 
                la posibilidad de hacer un acuerdo de pago. Él te va a responder la forma más fácil que tiene para realizar el pago. Tu deber es capturar estos datos:
                Texto: {user_input}
                Tu respuesta debe seguir el formato JSON:
                {{
                    "valor": "str" // es el valor en pesos colombianos que puede pagar el usuario, si no la identificas no pongas este parametro,
                    "fecha_primera_cuota": "str" // fecha exacta dd-mm-aaaa la fecha de hoy es {fecha}, si no la identificas no pongas este parametro,
                    "cuotas": "str" // si no la identificas no pongas este parametro
                }}
""")
# Chain
chain_prompt_parametros_acuero_pago = prompt_parametros_acuero_pago | models_llm.llm_chat_mini | StrOutputParser()

prompt_datos_faltantes = ChatPromptTemplate.from_template("""
                Eres un experto en cobranzas de la empresa abc. Tu misión es identificar dentro de la respuesta del usuario qué está expresando respecto a 
                la posibilidad de hacer un acuerdo de pago. recibiste una respuesta pero faltan esto
                datos: {datos_faltantes}
                por favor de forma muy amable solicita los datos faltantes
                -Tu respuesta debe ser maximo de 30 palabras
""")
# Chain
chain_prompt_datos_faltantes = prompt_datos_faltantes | models_llm.llm_chat_mini | StrOutputParser()

prompt_oferta_uno = ChatPromptTemplate.from_template("""
                Eres un experto en cobranzas de la empresa abc. Tu misión es brindar una oferta al usuario con la siguiente informacion
                {data_oferta}
                por favor de forma muy amable solicita una respuesta afirmativa o negativa respecto a la oferta
                -Tu respuesta debe ser maximo de 30 palabras
""")
# Chain
chain_prompt_oferta_uno = prompt_oferta_uno | models_llm.llm_chat_mini | StrOutputParser()

prompt_no_oferta = ChatPromptTemplate.from_template("""
                Eres un experto en cobranzas de la empresa abc. Tu misión es informarle al usuario que no tenemos ofertas que se asemejen a su peticion
                y que lo vas a comunicar con un asesor 
                -Tu respuesta debe ser maximo de 30 palabras
""")
# Chain
chain_prompt_no_oferta = prompt_no_oferta | models_llm.llm_chat_mini | StrOutputParser()