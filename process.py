from pregunta_inicial import functions as f_pregunta_inicial
from pregunta_acuerdo_inicial import functions as f_pregunta_acuerdo_inicial
from pregunta_acuerdo_aceptado import functions as f_pregunta_acuerdo_aceptado
from pregunta_reconoce_persona import functions as f_pregunta_reconoce_persona



def enrutador(texto_input, tarea):
    if tarea == "inicio" : 
        return f_pregunta_inicial.chat_pregunta_uno(texto_input)
    if tarea == "no_dinero":
        return f_pregunta_acuerdo_inicial.chat_pregunta_acuerdo_inicial(texto_input)
    if tarea == "si_acepta":
        return f_pregunta_acuerdo_aceptado.chat_pregunta_acuerdo_acptado(texto_input)
        
def lambda_handler(event, context=None):
    texto_input = event['texto_input']
    tarea = event["tarea"]
    chat = enrutador(texto_input, tarea)
    first_key = next(iter(chat))
    message = chat[first_key]['message']
    tarea = chat[first_key]['tarea']
    return {"body":{
        "message" : message ,
        "tareas :" : tarea
    }}
#print(lambda_handler(event={"texto_input": "esa deuda no es mia", "tarea":"inicio"}))
print(f_pregunta_reconoce_persona.chat_pregunta_uno("no se quien es")) 