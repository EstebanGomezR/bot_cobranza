from typing_extensions import TypedDict
from pregunta_si_reconoce_persona import prompts 
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
import json


memory = MemorySaver()

class State(TypedDict):
    input: str
    message: str
    tarea: str

def extraer_telefono(state):
    print("---Transicion humanfeedback")
    user_input = state["input"]
    response = prompts.chain_prompt_parametros_telefono.invoke({"user_input":user_input})
    response = response.replace("\n","").replace("  "," ").replace("```json","").replace("```","")
    print(response)
    return {"message": response}

# Función para validar si faltan datos
def validar_telefono(state):
    try :
        mensaje = state.get("message", {})
        mensaje = json.loads(mensaje)
        if mensaje["telefono"] == "NA":
            return {"telefono": "NA", "message": "NA"}
        elif mensaje["telefono"] == "ND":
            return {"telefono": "ND", "message": "NA"}
        elif mensaje["telefono"] == "NE":
            return {"telefono": "NE", "message": "NA"}
        else:
            return {"telefono": "SI", "message": mensaje["telefono"]}
    except : 
        return {"telefono": "NE", "message": "NA"}
# Función para validar si faltan datos
def telefono_indicado(state):
    mensaje = state.get("message", {})
    
    return {"message": mensaje,"tarea": "telefono_indicado"}

def telefono_no_indicado(state):
    user_input = state["input"]
    message =  prompts.chain_prompt_repite_telefono.invoke({"user_input":user_input})
    return {"message":message, "tarea" : "telefono_no_indicado"}
    
def no_quiere_brindar_telefono(state):
    user_input = state["input"]
    message =  prompts.chain_prompt_no_quiere_brindar_tel.invoke({"user_input":user_input})
    return {"message":message, "tarea" : "telefono_no_indicado"}

def no_entendimiento(state):
    #user_input = state["input"]
    #message =  prompts.chain_prompt_no_quiere_brindar_tel.invoke({"user_input":user_input})
    return {"message":"No le entendi", "tarea" : "telefono_no_indicado"}
    
def human_feedback(state):
    print("---human_feedback---")
    pass



builder = StateGraph(State)
builder.add_node("human_feedback", human_feedback)
builder.add_node("extraer_telefono", extraer_telefono)
builder.add_node("validar_telefono", validar_telefono)
builder.add_node("telefono_indicado", telefono_indicado)
builder.add_node("telefono_no_indicado", telefono_no_indicado)
builder.add_node("no_entendimiento", no_entendimiento)
builder.add_node("no_quiere_brindar_telefono", no_quiere_brindar_telefono)
builder.add_edge(START, "human_feedback")
builder.add_edge("human_feedback", "extraer_telefono")
builder.add_edge("extraer_telefono" , "validar_telefono")
builder.add_edge("telefono_indicado" , END)
builder.add_edge("telefono_no_indicado" , END)
builder.add_edge("no_quiere_brindar_telefono" , END)
builder.add_conditional_edges(
    "validar_telefono",
    lambda state: 
    "telefono_indicado" if state["telefono"] == "SI"  else 
    "telefono_no_indicado" if state["telefono"] == "NA" else 
    "no_entendimiento" if state["telefono"] == "NE" else 
    "no_quiere_brindar_telefono"
)

graph = builder.compile(checkpointer=memory)

def chat_pregunta(input_usuario):
    config = {"configurable": {"thread_id": "1234"}}
    for event in graph.stream({"input":input_usuario}, config, stream_mode="values"):
        pass
    stateTotal = graph.get_state(config)
    return stateTotal[3]['writes']