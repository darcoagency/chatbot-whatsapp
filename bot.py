import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurar a API Key do OpenAI (será definida no Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def verificar():
    """Rota para verificar se o servidor está rodando."""
    return "Chatbot rodando!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """Recebe mensagens do WhatsApp e responde usando OpenAI."""
    data = request.json
    if data and "messages" in data:
        for message in data["messages"]:
            if message.get("type") == "text":
                texto_recebido = message["text"]["body"]
                resposta = processar_mensagem(texto_recebido)
                return jsonify({"reply": resposta})
    return jsonify({"status": "ok"}), 200

def processar_mensagem(mensagem):
    """Processa a mensagem usando OpenAI e retorna a resposta."""
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": mensagem}]
    )
    return resposta["choices"][0]["message"]["content"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
