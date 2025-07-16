import json

def cargar_respuestas(archivo="respuestas.json"):
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def obtener_respuesta(pregunta, base):
    pregunta = pregunta.lower().strip()
    for clave in base:
        if clave in pregunta:
            return base[clave]
    return "Lo siento, no tengo una recomendación para eso."
