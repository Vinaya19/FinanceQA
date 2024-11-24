from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

client = OpenAI(api_key="OPEN_API_KEY")
import PyPDF2

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# OpenAI API key

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Route to upload document and generate summary
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    text = extract_text_from_pdf(file)

    # Summarize the document using GPT-4
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant skilled in summarizing documents."},
        {"role": "user", "content": f"Summarize this document: {text}"}
    ])

    summary = response.choices[0].message.content
    return jsonify({"summary": summary})

# Route to answer user questions
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    print("Data:",data)
    question = data['question']
    context = data['context']

    # GPT-4 Question Answering
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant answering questions based on a document."},
        {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
    ])

    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
