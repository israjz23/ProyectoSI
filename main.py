import speech_recognition as sr
import pyttsx3
import serial
import time
from recomendador import cargar_respuestas, obtener_respuesta

reconocedor = sr.Recognizer()

# Inicializa la conexión con Arduino
arduino = serial.Serial('COM26', 9600)  # AJUSTA el puerto si es necesario
time.sleep(2)

arduino.write(b'Hola desde Python!\n')  # Enviar un mensaje inicial al Arduino

def hablar(texto):
    print("Recomendador:", texto)
    try:
        voz = pyttsx3.init()
        voz.setProperty('rate', 150)
        voz.say(texto)
        voz.runAndWait()
        voz.stop()
        time.sleep(0.3)
    except Exception as e:
        print("Error al hablar:", e)

def escuchar():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = reconocedor.listen(source)
        time.sleep(1)
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
    hablar("Hola, soy tu recomendadora. ¿Quieres que te recomiende una serie o una película?")

    while True:
        tipo_usuario = escuchar().lower()
        time.sleep(1)

        if "no entendí" in tipo_usuario or "error de conexión" in tipo_usuario:
            hablar("Lo siento, ¿puedes repetirlo?")
            continue

        elif "no" in tipo_usuario or "salir" in tipo_usuario:
            hablar("Está bien, ¡hasta luego!")
            break

        elif "película" in tipo_usuario:
            categoria = "peliculas"
            hablar("Entendido, ¿de qué género te gustaría la película? Acción, comedia, terror, romance...")
        elif "serie" in tipo_usuario:
            categoria = "series"
            hablar("Perfecto, ¿de qué género te gustaría la serie? Acción, comedia, terror, romance...")
        else:
            hablar("No entendí si quieres una serie o una película. Por favor, repítelo.")
            continue

        genero_usuario = escuchar().lower()
        if "no entendí" in genero_usuario or "error de conexión" in genero_usuario:
            hablar("Lo siento, ¿puedes repetir el género?")
            continue

        pregunta = f"{categoria[:-1]} {genero_usuario}"  # Ej: 'pelicula acción', 'serie comedia'
        respuesta = obtener_respuesta(pregunta, base)
        hablar(respuesta)

        # Enviar respuesta a Arduino (LCD)
        try:
            arduino.write((respuesta + '\n').encode())
        except Exception as e:
            print("Error al enviar al Arduino:", e)

        # Preguntar si desea otra recomendación
        hablar("¿Quieres otra recomendación?")
        respuesta_usuario = escuchar().lower()

        if "no" in respuesta_usuario:
            hablar("De acuerdo, que disfrutes tu recomendación. ¡Hasta luego!")
            break
        elif "sí" in respuesta_usuario or "claro" in respuesta_usuario:
            hablar("Perfecto, dime si quieres una serie o una película.")
        else:
            hablar("No entendí bien, pero si quieres otra recomendación, solo dímelo.")

if __name__ == "__main__":
    main()
