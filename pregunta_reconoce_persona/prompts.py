from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from models import models_llm
from langchain.pydantic_v1 import BaseModel, Field


class RouteQuery(BaseModel):
    """Route the query"""

    answer: Literal["reconoce","no_reconoce","no_entendimiento"]= Field(
        ...,
        description="""Eres un experto en cobranzas de la empresa abc tu mision es identificar dentro de la respuesta del usuario que esta expresando:
                    Ten encuenta que lo ultimo que se le pregunto es si reconoce a un persona en especifico 
                    las clasificaciones son las siguientes 
                    reconoce : si entiendes que el usuario hace referencia a una afirmacion de que reconoce a la persona
                    no_reconoce : si entiendes que el usuario hace referencia a una afirmacion de que no reconoce a la persona
                    no_entendimiento : para lo que no logres clasificar
        """
    )
pydantic_parser = JsonOutputParser(pydantic_object=RouteQuery)
format_instructions = pydantic_parser.get_format_instructions()
enrutamiento_reconoce_persona ="""
                    Eres un experto en cobranzas de la empresa abc tu mision es identificar dentro de la respuesta del usuario que esta expresando:
                    Ten encuenta que lo ultimo que se le pregunto es si reconoce a un persona en especifico 
                    las clasificaciones son las siguientes 
                    reconoce : si entiendes que el usuario hace referencia a una afirmacion de que reconoce a la persona
                    no_reconoce : si entiendes que el usuario hace referencia a una afirmacion de que no reconoce a la persona
                    no_entendimiento : para lo que no logres clasificar
user: {user_input}
{format_instructions}
"""
prompt_enrutamiento_reconoce_persona = ChatPromptTemplate.from_template(
    template= enrutamiento_reconoce_persona,
    partial_variables = {
        "format_instructions":format_instructions
    }

)
# Chain
chain_prompt_enrutamiento_reconoce_persona = prompt_enrutamiento_reconoce_persona | models_llm.llm_chat_mini | pydantic_parser
prompt_acuerdo_pago = ChatPromptTemplate.from_template("""
                    Tu trabajo es ser un asesor de cobranzas de la empresa abz.
                    En la conversacion no debes saludar, debes verificar que se le dificulta al usuario para responder la pregunta, Tu objetivo es guiar al cliente a través de un proceso de cobranza.   
                    Eres consiente de que le estamos cobrando al usuario un valor pero el no tiene forma de realizar el pago dile de una forma muy empatica y natural si desea llegar a un acuerdo de pago
                    Tu respuesta debe ser maximo de 30 palabras
                    esto fue lo ultimo que nos dijo el usuario :{user_input}
""")

# Chain
chain_prompt_acuerdo_pago = prompt_acuerdo_pago | models_llm.llm_chat_mini | StrOutputParser()

prompt_abono = ChatPromptTemplate.from_template("""
                    Tu trabajo es ser un asesor de cobranzas de la empresa abz.
                    En la conversacion no debes saludar, debes indicarle al usuario que los medios de pago que tenemos disponible son pse y tarjeta.
                    Luego de eso brinda una calurosa despedida 
""")

# Chain
chain_prompt_abono = prompt_abono | models_llm.llm_chat_mini | StrOutputParser()

prompt_pago_realizado = ChatPromptTemplate.from_template("""
                    Tu trabajo es ser un asesor de cobranzas de la empresa abz.
                    En la conversacion no debes saludar, debes agradecer al usuario por su pago ya que tenia una deuda con la empresa y ya fue saldada
                    luego muy amablemente te despides
                    Reglas:
                    Nunca des confirmacion de que recibiste el pago
                    Nunca digas que la deuda esta saldada o algo referente
                    Tu respuesta debe ser maximo de 30 palabras
""")

# Chain
chain_prompt_pago_realizado = prompt_pago_realizado | models_llm.llm_chat_mini | StrOutputParser()

prompt_no_reconoce_datos = ChatPromptTemplate.from_template("""
                    Tu trabajo es ser un asesor de cobranzas de la empresa abz.
                    En la conversacion no debes saludar, debes pedirle una confirmacion al usuario de si reconoce la persona que se nombro 
                    partiendo de que antes dijiste unos datos y la persona menciono que no era el.
                    el nombre mencionado fue {nombre}
                    Reglas:
                    Tu respuesta debe ser maximo de 30 palabras
                    
""")

# Chain
chain_prompt_no_reconoce_datos = prompt_no_reconoce_datos | models_llm.llm_chat_mini | StrOutputParser()