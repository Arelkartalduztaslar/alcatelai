import os
from flask import Flask, request, render_template_string
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Alcatel tarayıcısının rahatça açabileceği çok sade HTML arayüzü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI SMS Web</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: sans-serif; padding: 10px; background: #f0f0f0;">
    <h2>Alcatel AI</h2>
    <form method="POST">
        <input type="text" name="soru" placeholder="Sorunuzu yazın..." style="width: 100%; padding: 8px; font-size: 16px;" required>
        <button type="submit" style="margin-top: 5px; width: 100%; padding: 8px; font-size: 16px;">Sor</button>
    </form>
    {% if cevap %}
        <hr>
        <h3>Cevap:</h3>
        <p style="background: #fff; padding: 8px; border: 1px solid #ccc;">{{ cevap }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    cevap = ""
    if request.method == "POST":
        soru = request.form.get("soru")
        try:
            prompt = f"Lütfen bu soruyu kısa ve net yanıtla: {soru}"
            cevap = model.generate_content(prompt).text
        except Exception as e:
            cevap = "Yapay zeka yanıt veremedi."
    return render_template_string(HTML_TEMPLATE, cevap=cevap)

if __name__ == "__main__":
    app.run(port=5000)
