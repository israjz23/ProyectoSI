import json
import unicodedata
import re
import random

def cargar_respuestas(archivo="respuestas.json"):
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def normalizar_texto(texto):
    texto = texto.lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip()

def obtener_respuesta(frase_usuario, base, categoria_actual=None):
    frase = normalizar_texto(frase_usuario)

    # Detectar categoría
    if "pelicula" in frase or "peli" in frase:
        categoria = "pelicula"
    elif "serie" in frase:
        categoria = "serie"
    else:
        categoria = categoria_actual

    generos_disponibles = ["accion", "comedia", "terror", "romantica", "romance", "drama"]
    sinonimos = {
        "romance": "romantica",
        "miedo": "terror",
        "horror": "terror",
        "terror": "terror"
    }

    genero = None
    for g in generos_disponibles:
        if g in frase:
            genero = g
            break
        else:
            for syn, real in sinonimos.items():
                if syn in frase:
                    genero = real
                    break
        if genero:
            break

    if categoria and genero:
        clave = f"{categoria} {genero}"
        respuestas = base.get(clave)
        if respuestas:
            if isinstance(respuestas, list):
                return random.choice(respuestas)
            return respuestas
        else:
            return "Lo siento, no tengo una recomendación para eso."
    elif genero:
        respuestas = base.get(f"{categoria_actual} {genero}")
        if respuestas:
            if isinstance(respuestas, list):
                return random.choice(respuestas)
            return respuestas
        else:
            return "Lo siento, no tengo una recomendación para eso."
    else:
        return "No entendí bien el género. ¿Puedes repetirlo con más claridad?"