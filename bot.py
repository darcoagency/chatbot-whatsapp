from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Pegando as chaves de API do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route("/", methods=["GET"])
def verify():
    """Verifica o webhook do WhatsApp."""
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Token inválido", 403

@app.route("/", methods=["POST"])
def webhook():
    """Recebe mensagens do WhatsApp e responde com IA."""
    data = request.get_json()
    print(data)  # Log para ver o que chega do WhatsApp

    if "messages" in data["entry"][0]["changes"][0]["value"]:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone_number = message["from"]
        text = message["text"]["body"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )

        reply = response["choices"][0]["message"]["content"]

        return jsonify({"status": "Mensagem processada", "resposta": reply})

    return jsonify({"status": "Evento ignorado"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
