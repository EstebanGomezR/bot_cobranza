from typing_extensions import TypedDict
from pregunta_inicial import prompts 
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END


memory = MemorySaver()

class State(TypedDict):
    input: str
    message: str
    tarea: str

def T1(state):
    print("---Transicion humanfeedback luces o conexion---")
    user_input = state["input"]
    respuesta = prompts.chain_enrutamiento_respuesta_inicial.invoke({"user_input":user_input})
    return respuesta["answer"]

def human_feedback(state):
    print("---human_feedback---")
    pass

def no_dinero(state):
    print("---pregunta_si_no_acuerdo de pago---")
    user_input = state["input"]
    message =  prompts.chain_prompt_acuerdo_pago.invoke({"user_input":user_input})
    return {"message":message, "tarea" : "no_dinero"}

def abonar(state):
    user_input = state["input"]
    message =  prompts.chain_prompt_abono.invoke({"user_input":user_input})
    return {"message":message, "tarea" : "abonar"}

def pago_realizado(state):
    user_input = state["input"]
    message =  prompts.chain_prompt_pago_realizado.invoke({"user_input":user_input})
    return {"message":message, "tarea" : "pago_realizado"}

def no_reconoce_deuda(state):
    user_input = state["input"]
    message =  prompts.chain_prompt_no_reconoce_datos.invoke({"nombre":"Maicol Purizaga"})
    return {"message":message, "tarea" : "no_reconoce_deuda"}

def no_entendimiento(state):
    print("---pregunta_si_no_acuerdo de pago---")
    user_input = state["input"]
    message =  "bobo"
    return {"message":message, "tarea" : "no_entendimiento"}

builder = StateGraph(State)
builder.add_node("human_feedback", human_feedback)
builder.add_node("no_dinero", no_dinero)
builder.add_node("abonar", abonar)
builder.add_node("no_entendimiento", no_entendimiento)
builder.add_node("pago_realizado", pago_realizado)
builder.add_node("no_reconoce_deuda", no_reconoce_deuda)
builder.add_edge(START, "human_feedback")
builder.add_edge("no_dinero", END)
builder.add_edge("abonar", END)
builder.add_edge("no_entendimiento", END)
builder.add_edge("no_reconoce_deuda", END)
builder.add_edge("pago_realizado", END)
builder.add_conditional_edges(
    "human_feedback",
    T1,
    {
        "no_dinero": "no_dinero",
        "abonar" : "abonar",
        "no_entendimiento" : "no_entendimiento",
        "pago_realizado" : "pago_realizado",
        "no_reconoce_deuda" : "no_reconoce_deuda",

    },
)
graph = builder.compile(checkpointer=memory)

def chat_pregunta_uno(input_usuario):
    config = {"configurable": {"thread_id": "1234"}}
    for event in graph.stream({"input":input_usuario}, config, stream_mode="values"):
        pass
    stateTotal = graph.get_state(config)
    return stateTotal[3]['writes']