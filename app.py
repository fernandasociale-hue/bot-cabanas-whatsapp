import os
from flask import Flask, request, jsonify
from groq import Groq
from PyPDF2 import PdfReader

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Esta función lee tu PDF automáticamente al iniciar el bot
def obtener_conocimiento_pdf():
    try:
        reader = PdfReader("informacion.pdf")
        texto = ""
        for page in reader.pages:
            texto += page.extract_text()
        return texto
    except Exception as e:
        print(f"Error leyendo PDF: {e}")
        return "Información general de Cabañas El Desván."

# Guardamos la info del PDF en la memoria del bot
CONOCIMIENTO_REAL = obtener_conocimiento_pdf()

@app.route("/webhook", methods=["POST"])
def webhook():
    datos = request.json
    # Usamos "message" para que coincida con tu Typebot
    mensaje_usuario = datos.get("message", "").lower()
    
    # Palabras clave para derivar a la dueña
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
            model="llama-3.3-70b-versatile",
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except:
        return jsonify({"reply": "Lo siento, tengo un problema técnico momentáneo. Por favor contacta a la dueña directamente."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
