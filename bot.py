from flask import Flask, request, jsonify

app = Flask(__name__)

# Seu token de verificação
VERIFY_TOKEN = "chatbot-whatsapp"

@app.route("/", methods=["GET"])
def verify():
    """Endpoint para verificação do webhook do Meta."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Erro de verificação", 403
    return "Método não permitido", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
