from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Your Gemini API key
client = genai.Client(api_key="AIzaSyA9V6z9aM_VeJ2lCxqCR4HMc6WLl2U9ddQ")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)