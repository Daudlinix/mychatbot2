from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# 🔑 Load environment variables (like API key)
load_dotenv()

app = Flask(__name__)

# 📄 Load travel site data from file (scraped offline)
with open("travel_data.txt", "r", encoding="utf-8") as f:
    travel_site_data = f.read()

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get("msg")

    prompt = f"""
    You are a helpful travel assistant. Answer in 1 short line.

    Website Info:
    {travel_site_data}

    User: {user_input}
    """

    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_KEY')}",  # 👈 .env ya Railway variable
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You're a helpful travel AI. Be short."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        data = res.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No reply")
        return jsonify(reply=reply)
    except Exception as e:
        return jsonify(reply=f"Error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # ✅ Railway ke port
    app.run(debug=True, host="0.0.0.0", port=port)
