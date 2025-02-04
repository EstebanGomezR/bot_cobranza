from typing_extensions import TypedDict
from pregunta_acuerdo_inicial import prompts 
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END


memory = MemorySaver()

class State2(TypedDict):
    input: str
    message: str
    tarea: str

def T3(state):
    print("---Transicion humanfeedback luces o conexion---")
    user_input = state["input"]
    respuesta = prompts.chain_enrutamiento_acuerdo_pago_si_no.invoke({"user_input":user_input})
    
    return respuesta["answer"]

def human_feedback(state):
    print("---human_feedback---")
    pass


def si_acepta(state):
    print("---pregunta_si_no_acuerdo de pago---")
    user_input = state["input"]
    message =  prompts.chain_prompt_reglas_acuero_pago.invoke({"user_input":user_input})
    return {"message":message, "tarea": "si_acepta"}

def no_entendimiento(state):
    print("---pregunta_si_no_acuerdo de pago---")
    user_input = state["input"]
    message =  "bobo"
    return {"message":message, "tarea":"no_entendimiento"}

builder2 = StateGraph(State2)
builder2.add_node("human_feedback", human_feedback)
builder2.add_node("si_acepta", si_acepta)
builder2.add_node("no_entendimiento", no_entendimiento)
builder2.add_edge(START, "human_feedback")
builder2.add_edge("si_acepta", END)
builder2.add_edge("no_entendimiento", END)
builder2.add_conditional_edges(
    "human_feedback",
    T3,
    {
        "si": "si_acepta",
        "no_entendimiento" : "no_entendimiento"
    },
)
graph2 = builder2.compile(checkpointer=memory)

def chat_pregunta_acuerdo_inicial(input_usuario):
    config = {"configurable": {"thread_id": "1234"}}
    for event in graph2.stream({"input":input_usuario}, config, stream_mode="values"):
        pass
    stateTotal = graph2.get_state(config)
    return stateTotal[3]['writes']