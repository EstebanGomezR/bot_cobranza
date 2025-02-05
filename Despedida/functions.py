from typing_extensions import TypedDict
from Despedida import prompts 
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
import json


memory = MemorySaver()

class State(TypedDict):
    input: str
    message: str
    tarea: str

    
def human_feedback(state):
    print("---human_feedback---")
    pass

def despedida(state):
    print("---pregunta_si_no_acuerdo de pago---")
    user_input = state["input"]
    message =  prompts.chain_prompt_despedida.invoke({"user_input":user_input})
    return {"message":message, "tarea" : "despedida"}



builder = StateGraph(State)
builder.add_node("human_feedback", human_feedback)
builder.add_node("despedida", despedida)
builder.add_edge(START, "human_feedback")
builder.add_edge("human_feedback", "despedida")
builder.add_edge("despedida" , END)


graph = builder.compile(checkpointer=memory)

def chat_pregunta(input_usuario):
    config = {"configurable": {"thread_id": "1234"}}
    for event in graph.stream({"input":input_usuario}, config, stream_mode="values"):
        pass
    stateTotal = graph.get_state(config)
    return stateTotal[3]['writes']