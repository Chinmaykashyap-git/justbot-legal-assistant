import os
import openai
from flask import Flask, request, render_template
from dotenv import load_dotenv
import pdfplumber
from deep_translator import GoogleTranslator


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def summarize_text(text, lang='en'):
    prompt = f"Explain this legal document simply in {lang}:\n{text[:2000]}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        if 'pdf' in request.files:
            pdf_file = request.files["pdf"]
            with pdfplumber.open(pdf_file) as pdf:
                full_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                lang = request.form.get("lang", "en")
                result = summarize_text(full_text, lang)
        elif 'question' in request.form:
            question = request.form["question"]
            lang = request.form.get("lang", "en")
            result = summarize_text(question, lang)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
