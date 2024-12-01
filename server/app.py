from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import os
import matplotlib.pyplot as plt
from io import BytesIO
import re

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

def extract_visualization_data(answer):
    try:
        start_idx = answer.find("json") + 4
        end_idx = answer.rfind("```")
        json_data = answer[start_idx:end_idx].strip()

        # Getting only the data to visualize in case there is nested structure
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract only the numerical values and their corresponding immediate names from the following JSON. Format the result as a clean dictionary of name-value pairs, where the name is the immediate key describing the number. Ignore nested structures beyond the immediate key."},
                {"role": "user", "content": f"Here is the JSON: {json_data}"}
            ]
        )
        visualization_data = {response.choices[0].message.content}
        cleaned_response = re.sub(r'[`\\n\\t]', '', visualization_data).strip()

        print("Data: ", cleaned_response)
        #json_data = answer[start_idx:].split(":", 1)[1].strip()
        print(eval(visualization_data))  # Convert JSON-like string to Python dictionary
    except Exception as error:
        print("An error occurred:", error)
        return None

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
    long_context = data.get('longContext', "")

    # Prepare messages for GPT-4 based on chat history
    messages = [{"role": "system", "content": "You are a helpful assistant answering questions based on a document. You should also keep track of the user's recent questions and answers to provide meaningful context for follow-up questions. If the user requests visualization, provide the data, name as labels and numbers as values in JSON format for visualization. If a user enters a question that isn't related to the document uploaded tell them politely to enter a relevant question. DO NOT HALLUCINATE!"}]
    messages.append({"role": "system", "content": f"Document Context: {extracted_text}"})
    messages.append({"role": "system", "content": f"Long-Term Context: {long_context}"})
    #print('Chat History: ', chat_history)

    for chat in chat_history[-5:]:
        messages.append({"role": "user", "content": chat['question']})
        messages.append({"role": "assistant", "content": chat['answer']})

    messages.append({"role": "user", "content": question})

    # GPT-4 Question Answering
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    answer = response.choices[0].message.content

    # If answer contains visualization data, extract it
    if 'json' in answer.lower():
        visualization_data = extract_visualization_data(answer)
        print(visualization_data)
        #return jsonify({"answer": answer, "visualizationData": visualization_data})

    # Update the long context based on user question and answer
    if len(long_context.split()) < 500:
        long_context += f"\nUser: {question}\nAssistant: {answer}"

    

    return jsonify({"answer": answer, "longContext": long_context})

@app.route('/visualize', methods=['POST'])
def visualize():
    # Parse the request
    data = request.get_json()
    numbers = data['numbers']  # Expecting an array of numbers
    labels = data.get('labels', [f"Item {i+1}" for i in range(len(numbers))])

    # Generate a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(labels, numbers, color='skyblue')
    plt.xlabel('Labels')
    plt.ylabel('Values')
    plt.title('Visualization of Numbers')
    plt.tight_layout()

    # Save the chart to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
