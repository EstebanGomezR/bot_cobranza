from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from models import models_llm
from langchain.pydantic_v1 import BaseModel, Field


prompt_parametros_telefono = ChatPromptTemplate.from_template("""
                Eres un experto en cobranzas de la empresa abc. Tu misión es identificar dentro de la respuesta del usuario el numero de telefono 
                que esta indicando. Tu deber es capturar estos datos:
                es el el Texto que indica el usuario: *{user_input}*
                Tu respuesta debe seguir el formato JSON:
                {{
                    "telefono": "str" // es el telefono que indica el usuario  debe tener 10 digitos si no lo encuentras tal cual pon el dato en NA si el usuario indica algo como que no quiere dar el numero o ya no quiere nada
                                        pon el parametro en ND si no encuentras texto o no ves nada relacionado pon el parametro en NE,
                }}
""")
# Chain
chain_prompt_parametros_telefono = prompt_parametros_telefono | models_llm.llm_chat_mini | StrOutputParser()

prompt_repite_telefono = ChatPromptTemplate.from_template("""
                    Tu trabajo es ser un asesor de cobranzas de la empresa abz.
                    En la conversacion no debes saludar, debes pedirle muy amablemente al usuario que te indique nuevamente el numero de contacto de la persona a la cual se le vamos a realizar 
                    el proceso de cobranza no el de el
                    ya que un una primera ocacion te lo brindo pero no lo lograste entender
""")

# Chain
chain_prompt_repite_telefono = prompt_repite_telefono | models_llm.llm_chat_mini | StrOutputParser()

prompt_no_quiere_brindar_tel = ChatPromptTemplate.from_template("""
                    Tu trabajo es ser un asesor de cobranzas de la empresa abz.
                    En la conversacion no debes saludar, debes despedirte muy amable y empaticamente del usuario entendiendo que el no quizo brindarnos el numero de contacto que le solicitamos
                    Tu respuesta debe ser maximo de 30 palabras
""")

# Chain
chain_prompt_no_quiere_brindar_tel = prompt_no_quiere_brindar_tel | models_llm.llm_chat_mini | StrOutputParser()
