import speech_recognition as sr
import pyttsx3
import serial
import time
import serial.tools.list_ports
from recomendador import cargar_respuestas, obtener_respuesta, normalizar_texto

class RecomendadorVoz:
    def __init__(self):
        self.reconocedor = sr.Recognizer()
        self.voz = pyttsx3.init()
        self.base = cargar_respuestas()
        self.arduino = self._conectar_arduino()

    def _conectar_arduino(self):
        puertos = list(serial.tools.list_ports.comports())
        for p in puertos:
            if "USB" in p.description or "Arduino" in p.description:
                try:
                    arduino = serial.Serial(p.device, 9600)
                    time.sleep(2)
                    arduino.write(b'Hola desde Python!\n')
                    return arduino
                except serial.SerialException:
                    continue
        print("⚠️ Arduino no encontrado. Continuando sin conexión.")
        return None

    def hablar(self, texto):
        print(f"🎙️ Recomendador: {texto}")
        try:
            self.voz.setProperty('rate', 160)
            self.voz.say(texto)
            self.voz.runAndWait()
        except Exception:
            pass

    def escuchar(self):
        with sr.Microphone() as source:
            print("🔊 Escuchando...")
            audio = self.reconocedor.listen(source, timeout=5, phrase_time_limit=10)
        try:
            texto = self.reconocedor.recognize_google(audio, language="es-MX")
            texto_normalizado = normalizar_texto(texto)
            print(f"🗣️ Tú dijiste: {texto} → {texto_normalizado}")
            return texto_normalizado
        except sr.UnknownValueError:
            return "no entendi"
        except sr.RequestError:
            return "error de conexion"

    def enviar_a_arduino(self, mensaje):
        if self.arduino:
            try:
                self.arduino.write((mensaje + '\n').encode())
            except Exception:
                pass

    def detectar_categoria_y_genero(self, texto, categoria_anterior=None):
        categorias = ["pelicula", "peli", "serie"]
        generos = ["accion", "comedia", "terror", "romantica", "romance", "drama", "horror", "miedo"]
        sinonimos_genero = {"romance": "romantica", "horror": "terror", "miedo": "terror"}

        texto = normalizar_texto(texto)
        palabras = texto.split()

        categoria = None
        genero = None

        if categoria_anterior:
            categoria = categoria_anterior
        else:
            for c in categorias:
                if c in palabras:
                    categoria = "pelicula" if c in ["pelicula", "peli"] else "serie"
                    break

        if categoria:
            for g in generos:
                if g in palabras:
                    genero = sinonimos_genero.get(g, g)
                    break

        return categoria, genero

    def iniciar(self):
        self.hablar("Hola, soy tu recomendadora. ¿Quieres que te recomiende una serie o una película?")

        while True:
            tipo_usuario = self.escuchar()

            if "no entendi" in tipo_usuario or "error" in tipo_usuario:
                self.hablar("Lo siento, ¿puedes repetirlo?")
                continue

            if "no" in tipo_usuario or "es todo" in tipo_usuario or "salir" in tipo_usuario:
                self.hablar("Está bien, ¡hasta luego!")
                break

            categoria, genero = self.detectar_categoria_y_genero(tipo_usuario)

            if not categoria:
                self.hablar("No entendí si quieres una serie o una película. Por favor, repítelo.")
                continue

            while not genero:
                self.hablar(f"¿De qué género te gustaría la {categoria}? Acción, comedia, horror, romance...")
                genero_usuario = self.escuchar()

                if "no entendi" in genero_usuario or "error" in genero_usuario:
                    self.hablar("Lo siento, no entendí el género. Por favor, repítelo.")
                    continue

                _, genero = self.detectar_categoria_y_genero(genero_usuario, categoria_anterior=categoria)

                if not genero:
                    self.hablar("No entendí bien el género. Por favor, repítelo.")

            respuesta = obtener_respuesta(f"{categoria} {genero}", self.base)
            self.hablar(respuesta)
            self.enviar_a_arduino(respuesta)

            self.hablar("¿Quieres otra recomendación?")
            respuesta_usuario = self.escuchar()

            if "no" in respuesta_usuario:
                self.hablar("De acuerdo, que disfrutes tu recomendación. ¡Hasta luego!")
                break
            elif "si" in respuesta_usuario or "claro" in respuesta_usuario:
                self.hablar("Perfecto, dime si quieres una serie o una película.")
            else:
                self.hablar("No entendí bien, pero si quieres otra recomendación, solo dímelo.")

if __name__ == "__main__":
    recomendador = RecomendadorVoz()
    recomendador.iniciar()
