from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- FIX 1: Add this
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # <--- FIX 1: This allows your app to talk to the backend

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in Render Environment Variables")

genai.configure(api_key=GEMINI_API_KEY)

# FIX 2: Better model naming and safety settings
model = genai.GenerativeModel("gemini-1.5-flash") # 1.5 Flash is faster and cheaper for apps

@app.route("/")
def home():
    return "HomeworkHero Backend Running"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Safety Settings: Ensures the AI doesn't block academic questions
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        response = model.generate_content(prompt, safety_settings=safety_settings)

        # Check if the response exists before trying to access .text
        if response and response.candidates:
            reply_text = response.text
            return jsonify({"reply": reply_text})
        else:
            return jsonify({"error": "Gemini blocked this prompt or returned nothing"}), 500

    except Exception as e:
        print(f"Error: {str(e)}") # This shows up in Render Logs
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
