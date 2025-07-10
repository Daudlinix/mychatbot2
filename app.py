from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# 🔍 Pages to scrape
travel_pages = [
    "https://redstartravels.co/services",
    "https://redstartravels.co/about",
    "https://redstartravels.co/contact",
    "https://redstartravels.co/packages"
]

# 🌐 Scrape travel site
def scrape_travel_site():
    all_data = ""
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in travel_pages:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            all_data += f"\n\nPAGE: {url}\n{text}"
        except Exception as e:
            all_data += f"\n\nPAGE: {url}\nError: {str(e)}"
    return all_data

# 🔄 Scrape once when app starts
try:
    travel_site_data = scrape_travel_site()
except Exception as e:
    travel_site_data = "Scraping error: " + str(e)

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
        # 🛑🔑 INSERT YOUR OPENROUTER API KEY HERE:
        "Authorization": "Bearer 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",  # 👈 👈 👈 Replace here!
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You're a helpful travel AI. Keep it short."},
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
