from flask import Flask, render_template, request, jsonify
from gemini_agent import ask_gemini

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    reply = ask_gemini(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)