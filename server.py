from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- 1. CRITICAL: Prevents your app from blocking the request
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # <-- 2. CRITICAL: This opens the door for your frontend

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # This will show up in Render Logs if you forgot to add the Key in Settings
    print("ERROR: GEMINI_API_KEY is not set in Render Environment Variables")
else:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash") # 1.5 Flash is better/faster for apps

@app.route("/")
def home():
    return "HomeworkHero Backend is LIVE"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        print(f"User asked: {prompt}") # Look for this in Render Logs!

        # Safety settings to prevent the AI from refusing to answer school questions
        safety = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        response = model.generate_content(prompt, safety_settings=safety)

        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"error": "AI could not generate a response"}), 500

    except Exception as e:
        print(f"Server Error: {str(e)}") # This helps you debug in Render
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
