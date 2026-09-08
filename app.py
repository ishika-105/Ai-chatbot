import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load the secret API key from the .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Use the fast, lightweight Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-3.6-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.get_json()
    user_message = user_data.get("message", "")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Error connecting to Gemini: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)