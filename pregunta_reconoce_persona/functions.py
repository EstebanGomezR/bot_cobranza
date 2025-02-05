from typing_extensions import TypedDict
from pregunta_reconoce_persona import prompts 
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END


memory = MemorySaver()

class State(TypedDict):
    input: str
    message: str
    tarea: str

def T1(state):
    print("---Transicion humanfeedback")
    user_input = state["input"]
    respuesta = prompts.chain_prompt_enrutamiento_reconoce_persona.invoke({"user_input":user_input})
    return respuesta["answer"]

def human_feedback(state):
    print("---human_feedback---")
    pass

def no_reconoce_persona(state):
    print("---pregunta_si_no_acuerdo de pago---")
    user_input = state["input"]
    message =  prompts.chain_prompt_no_reconoce_persona.invoke({"user_input":user_input})
    return {"message":message, "tarea" : "no_reconoce_persona"}

def no_entendimiento(state):
    print("---pregunta_si_no_acuerdo de pago---")
    user_input = state["input"]
    message =  "bobo"
    return {"message":message, "tarea" : "no_entendimiento"}

builder = StateGraph(State)
builder.add_node("human_feedback", human_feedback)
builder.add_node("no_reconoce_persona", no_reconoce_persona)
builder.add_node("no_entendimiento", no_entendimiento)
builder.add_edge(START, "human_feedback")
builder.add_edge("no_reconoce_persona", END)
builder.add_conditional_edges(
    "human_feedback",
    T1,
    {
        "no_reconoce": "no_reconoce_persona",
        "no_entendimiento" : "no_entendimiento",
    },
)
graph = builder.compile(checkpointer=memory)

def chat_pregunta(input_usuario):
    config = {"configurable": {"thread_id": "1234"}}
    for event in graph.stream({"input":input_usuario}, config, stream_mode="values"):
        pass
    stateTotal = graph.get_state(config)
    return stateTotal[3]['writes']