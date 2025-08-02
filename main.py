from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Together.ai API key
TOGETHER_API_KEY = "tgp_v1_8mNixmwiwIrNf1iGBld_EwVP_eoxEnJZrVsRaVMqTLQ"


# Homepage route — serves chatbot UI
@app.route("/", methods=["GET"])
def home():
    return render_template("chatbot.html")


# Chatbot API route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model":
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [{
                "role":
                "system",
                "content":
                "You are Lunaria, a warm and knowledgeable AI beauty assistant for Lunaria Beauty. Help customers with skincare and makeup product advice in a friendly and elegant tone."
            }, {
                "role": "user",
                "content": user_message
            }]
        })

    if response.status_code == 200:
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        print("Together.ai Error:", response.status_code)
        print("Full response:", response.text)
        return jsonify({"error":
                        "Failed to get response from Together.ai"}), 500


# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
