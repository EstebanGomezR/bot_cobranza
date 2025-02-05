from typing_extensions import TypedDict
from pregunta_acuerdo_aceptado import prompts 
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
import json
from datetime import datetime

memory = MemorySaver()

class State3(TypedDict):
    input: str
    message: str
    tarea:str

def extraer_datos(state):
    print("---Transicion humanfeedback luces o conexion---")
    user_input = state["input"]
    response = prompts.chain_prompt_parametros_acuero_pago.invoke({"user_input":user_input,"fecha" : datetime.today().strftime('%d-%m-%Y')})
    response = response.replace("\n","").replace("  "," ").replace("```json","").replace("```","")
    return {"message": response}

def human_feedback(state):
    print("---human_feedback---")
    pass

# Función para validar si faltan datos
def validar_datos(state):
    extracted_data = state.get("message", {})
    extracted_data_json = json.loads(extracted_data)
    required_keys = {"valor", "fecha_primera_cuota", "cuotas"}
    missing_keys = [key for key in required_keys if not extracted_data_json.get(key)]
    if missing_keys:
        return {"datos_completos": False,"message": missing_keys}
    else:
        return {"datos_completos": True, "message": extracted_data}

def consultar_arreglo(state):
    extracted_data = state.get("message", {})
    extracted_data_json = json.loads(extracted_data)
    print(extracted_data_json)
    acuerdos_previos = [
        {"valor": "50000", "fecha_primera_cuota": "01-02-2025", "cuotas": "3"},
        {"valor": "30000", "fecha_primera_cuota": "15-02-2025", "cuotas": "1"},
        {"valor": "70000", "fecha_primera_cuota": "10-03-2025", "cuotas": "4"},
        {"valor": "45000", "fecha_primera_cuota": "05-04-2025", "cuotas": "2"},
        {"valor": "90000", "fecha_primera_cuota": "20-05-2025", "cuotas": "5"},
        {"valor": "25000", "fecha_primera_cuota": "12-06-2025", "cuotas": "1"},
        {"valor": "60000", "fecha_primera_cuota": "08-07-2025", "cuotas": "3"},
        {"valor": "35000", "fecha_primera_cuota": "25-08-2025", "cuotas": "2"},
        {"valor": "80000", "fecha_primera_cuota": "14-09-2025", "cuotas": "6"},
        {"valor": "55000", "fecha_primera_cuota": "30-10-2025", "cuotas": "4"},
        {"valor": "40000", "fecha_primera_cuota": "18-11-2025", "cuotas": "3"},
        {"valor": "75000", "fecha_primera_cuota": "05-12-2025", "cuotas": "5"}
    ]
    mejor_match = None
    mejor_puntuacion = -1
    for acuerdo in acuerdos_previos:
        puntuacion = 0
        # Comparar valor (puntuación alta porque es lo más relevante)
        if acuerdo["valor"] == extracted_data_json["valor"]:
            puntuacion += 3
        # Comparar número de cuotas
        if acuerdo["cuotas"] == extracted_data_json["cuotas"]:
            puntuacion += 1
        # Guardar el mejor match
        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_match = acuerdo
    if mejor_puntuacion != 0 : 
        mejor_match["fecha_primera_cuota"] = extracted_data_json["fecha_primera_cuota"]
        message = prompts.chain_prompt_oferta_uno.invoke({"data_oferta":str(mejor_match),})
    else : 
        message = prompts.chain_prompt_no_oferta.invoke({"input_usuario":"NA"}) 
    return {"message": message,  "tarea": "consultar_arreglo"}

def preguntar_faltantes(state):
    message =  prompts.chain_prompt_datos_faltantes.invoke({"datos_faltantes":state.get("message", {})})
    return {"message":message , "tarea": "preguntar_faltantes"}
builder3 = StateGraph(State3)
builder3.add_node("human_feedback", human_feedback)
builder3.add_node("extraer_datos", extraer_datos)
builder3.add_node("consultar_arreglo", consultar_arreglo)
builder3.add_node("validar_datos", validar_datos)
builder3.add_node("preguntar_faltantes", preguntar_faltantes)
builder3.add_edge(START, "human_feedback")
builder3.add_edge("human_feedback", "extraer_datos")
builder3.add_edge("extraer_datos", "validar_datos")
builder3.add_conditional_edges(
    "validar_datos",
    lambda state: "consultar_arreglo" if state["datos_completos"] else "preguntar_faltantes"
)
builder3.add_edge("consultar_arreglo", END)
builder3.add_edge("preguntar_faltantes", END)
graph3 = builder3.compile(checkpointer=memory)

def chat_pregunta_acuerdo_acptado(input_usuario):
    config = {"configurable": {"thread_id": "1234"}}
    for event in graph3.stream({"input":input_usuario}, config, stream_mode="values"):
        pass
    stateTotal = graph3.get_state(config)
    return stateTotal[3]['writes']