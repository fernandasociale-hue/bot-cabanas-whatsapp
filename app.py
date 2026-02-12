import os
from flask import Flask, request, jsonify
from groq import Groq
from PyPDF2 import PdfReader # Importante añadir esta línea

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Función para extraer texto del PDF automáticamente
def obtener_conocimiento_pdf():
    try:
        reader = PdfReader("informacion.pdf") # Tu PDF debe llamarse así en GitHub
        texto = ""
        for page in reader.pages:
            texto += page.extract_text()
        return texto
    except:
        return "Información general de Cabañas El Desván."

CONOCIMIENTO_REAL = obtener_conocimiento_pdf()

@app.route("/webhook", methods=["POST"])
def webhook():
    datos = request.json
    # Cambiamos "text" por "message" para que coincida con lo que configuramos en Typebot
    mensaje_usuario = datos.get("message", "").lower() 
    
    disparadores_humano = ["reservar", "reserva", "dueña", "pagar", "transferencia", "hablar con alguien"]
    
    if any(p in mensaje_usuario for p in disparadores_humano):
        return jsonify({
            "reply": "Un momento, estoy avisando a la administración. 🔔 Presiona aquí para hablar directamente con la dueña: https://wa.me/56961688761"
        })

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Eres el asistente de Cabañas El Desván. Responde de forma mágica y acogedora usando esto: {CONOCIMIENTO_REAL}. Si no sabes algo, di: 'Lo siento, no tengo esa información. Presiona aquí para hablar con la dueña: https://wa.me/56961688761'"},
                {"role": "user", "content": mensaje_usuario}
            ],
            model="llama-3.3-70b-versatile", # Usamos el modelo más potente
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Lo siento, tengo un problema técnico momentáneo."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

