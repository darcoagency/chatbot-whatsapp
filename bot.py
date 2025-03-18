import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Pegando as variáveis de ambiente do Render
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Rota principal para verificar o webhook do WhatsApp
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Token inválido", 403

# Rota para receber mensagens do WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    # Verificando se há mensagem recebida
    if data and "entry" in data:
        for entry in data["entry"]:
            for change in entry["changes"]:
                if "messages" in change["value"]:
                    message = change["value"]["messages"][0]
                    sender_id = message["from"]
                    text = message.get("text", {}).get("body", "")

                    # Gerando resposta com ChatGPT
                    response_text = chatgpt_response(text)

                    # Enviando resposta pelo WhatsApp
                    send_whatsapp_message(sender_id, response_text)

    return "Mensagem recebida", 200

# Função para gerar resposta com ChatGPT
def chatgpt_response(user_message):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": user_message}]}
    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    
    return response.json()["choices"][0]["message"]["content"]

# Função para enviar resposta pelo WhatsApp
def send_whatsapp_message(to, message):
    url = "https://graph.facebook.com/v17.0/me/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": message}}

    requests.post(url, json=data, headers=headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
