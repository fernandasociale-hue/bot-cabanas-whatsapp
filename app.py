import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Información real extraída de tu documento PDF
CONOCIMIENTO_REAL = """
Nombre: Cabañas El Desván.
Ubicación: Ruta 1-45, Km 18.5, Puente Negro, San Fernando (a 20 km del centro).
Tipos de Cabañas: 
- Campestre (4-7 pers, $120.000-$150.000)
- Vikinga (4 pers, $95.000-$110.000)
- Granero (2 pers, ideal parejas, $75.000-$85.000)
- Los Duendes (4 pers, $95.000-$110.000).
Check-in: 15:00 a 21:00. Check-out: 12:00 a 12:30.
Mascotas: Pet Friendly (tamaño pequeño, previo aviso).
Incluye: Desayuno artesanal en la cabaña, Wi-Fi, Smart TV, terraza con parrilla.
No se permiten: Fiestas ni ruidos entre 22:00 y 09:00.
"""

@app.route("/webhook", methods=["POST"])
def webhook():
    datos = request.json
    mensaje_usuario = datos.get("text", "").lower()
    
    # Lógica para hablar con la dueña (silenciar bot)
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
            model="llama3-8b-8192",
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except:
        return jsonify({"reply": "Lo siento, tengo un problema técnico. Por favor contacta a la dueña directamente."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
