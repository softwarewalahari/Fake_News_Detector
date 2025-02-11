from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# 🔹 Google Gemini API Key
GEMINI_API_KEY = "AIzaSyDYXK0IlEe7CmeDZo8lgyKjUVRZKWWncX4"  # Replace with your actual Gemini API Key

# 🔹 Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# 🔹 Initialize Flask App
app = Flask(__name__)

# 🔹 Check If News is Fake Using Gemini AI
def analyze_news(article_text):
    prompt = f"Analyze this news and classify it as 'Real' or 'Fake'. Just return 'Fake News' or 'Real News' based on the analysis: {article_text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response else "Unable to determine"
    except Exception as e:
        print("❌ Error in Gemini API:", e)
        return "AI could not process this request."

# 🔹 Home Route (Frontend)
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 API to Analyze User-Entered News
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json.get("news_text")
    
    if not data:
        return jsonify({"result": "❌ Please enter news content to analyze."})

    # 🔹 Get AI Prediction
    prediction = analyze_news(data)

    return jsonify({"result": prediction})

if __name__ == "__main__":
    app.run(debug=True)
