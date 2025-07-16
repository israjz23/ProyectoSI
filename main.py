import speech_recognition as sr
import pyttsx3
from recomendador import cargar_respuestas, obtener_respuesta

# Inicializar motores
reconocedor = sr.Recognizer()
voz = pyttsx3.init()
voz.setProperty('rate', 150)

def hablar(texto):
    print("Mini Alexa:", texto)
    voz.say(texto)
    voz.runAndWait()

def escuchar():
    with sr.Microphone() as source:
        print("Escuchando tu pregunta...")
        audio = reconocedor.listen(source)
    try:
        texto = reconocedor.recognize_google(audio, language="es-MX")
        print("Tú dijiste:", texto)
        return texto
    except sr.UnknownValueError:
        return "No entendí lo que dijiste."
    except sr.RequestError:
        return "Error de conexión con el servicio de voz."

def main():
    base = cargar_respuestas()
    hablar("Hola, soy tu recomendadora. Puedes decirme: recomiéndame una película o serie.")
    
    while True:
        pregunta = escuchar()
        
        if "salir" in pregunta.lower():
            hablar("¡Hasta luego!")
            break

        respuesta = obtener_respuesta(pregunta, base)
        hablar(respuesta)

if __name__ == "__main__":
    main()
