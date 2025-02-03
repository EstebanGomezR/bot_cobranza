from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from models import models_llm
from langchain.pydantic_v1 import BaseModel, Field


class RouteQuery2(BaseModel):
    """Route the query"""

    answer: Literal["si","no","no_entendimiento"]= Field(
        ...,
        description="""
                    Eres un experto en cobranzas de la empresa abc tu mision es identificar dentro de la respuesta del usuario que esta expresando respecto a 
                    la posibilidad de hacer un acuerdo de pago:
                    las clasificaciones son las siguientes 
                    si : si entiendes que el usuario hace referencia a un frase afirmativa
                    no : si entiendes que el usuario hace referencia a un frase negativa
                    no_entendimiento : para lo que no logres clasificar
        """
    )
pydantic_parser = JsonOutputParser(pydantic_object=RouteQuery2)
format_instructions = pydantic_parser.get_format_instructions()
enrutamiento_acuerdo_pago_si_no ="""
                    Eres un experto en cobranzas de la empresa abc tu mision es identificar dentro de la respuesta del usuario que esta expresando respecto a 
                    la posibilidad de hacer un acuerdo de pago:
                    las clasificaciones son las siguientes 
                    si : si entiendes que el usuario hace referencia a un frase afirmativa
                    no : si entiendes que el usuario hace referencia a un frase negativa
                    no_entendimiento : para lo que no logres clasificar
user: {user_input}
{format_instructions}
"""
prompt_enrutamiento_acuerdo_pago_si_no = ChatPromptTemplate.from_template(
    template= enrutamiento_acuerdo_pago_si_no,
    partial_variables = {
        "format_instructions":format_instructions
    }

)
# Chain
chain_enrutamiento_acuerdo_pago_si_no = prompt_enrutamiento_acuerdo_pago_si_no | models_llm.llm_chat_mini | pydantic_parser
prompt_reglas_acuero_pago = ChatPromptTemplate.from_template("""
                    Tu trabajo es ser un asesor de cobranzas de la empresa abz.
                    En la conversacion no debes saludar, Tu objetivo es guiar al cliente a través de un proceso de cobranza.   
                    Eres consiente de que le estamos cobrando al usuario un valor pero el no tiene forma de realizar el pago preguntale de una forma muy empatica y natural la forma mas sencilla para que 
                    el pueda realizar el pago.
                    Es importante que solicites la feche de pago, el valor de pago que realizaria y el numero de cuotas                                       
                    esto fue lo ultimo que nos dijo el usuario :{user_input}                                                         
                    Tu respuesta debe ser maximo de 30 palabras
""")

# Chain
chain_prompt_reglas_acuero_pago = prompt_reglas_acuero_pago | models_llm.llm_chat_mini | StrOutputParser()