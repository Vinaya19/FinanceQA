from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import os

# Load environment variables from .env
load_dotenv()

# Get the API key from the .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

extracted_text = ""

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
    global extracted_text
    file = request.files['file']
    extracted_text = extract_text_from_pdf(file)

    # Summarize the document using GPT-4
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant skilled in summarizing documents."},
            {"role": "user", "content": f"Summarize this document: {extracted_text}"}
        ]
    )

    summary = response.choices[0].message.content
    return jsonify({"summary": summary})

# Route to handle chatbot interactions
@app.route('/ask', methods=['POST'])
def ask_question():
    global extracted_text
    data = request.get_json()
    question = data['question']
    chat_history = data.get('chatHistory', [])

    # Prepare messages for GPT-4 based on chat history
    messages = [{"role": "system", "content": "You are a helpful assistant answering questions based on a document."}]
    messages.append({"role": "system", "content": f"Document Context: {extracted_text}"})

    for chat in chat_history:
        messages.append({"role": "user", "content": chat['question']})
        messages.append({"role": "assistant", "content": chat['answer']})

    messages.append({"role": "user", "content": question})

    # GPT-4 Question Answering
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)