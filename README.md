# Finance Question Answer Bot

This project implements a chatbot that allows users to upload a financial document, generates a summary, and answers questions based on the uploaded document. It also creates visualizations for the user based on the numbers given the document.

[![Finance Question Answer Bot](https://img.youtube.com/vi/04OIAvRQmO4?si=CRfsp67PFcEiRp2d/0.jpg)](https://www.youtube.com/watch?v=04OIAvRQmO4?si=CRfsp67PFcEiRp2d)

---

## Features

1. **Document Upload**:
   - Users can upload a document (e.g., text or PDF).
   - The backend processes the document and provides a summary.

2. **Document-based Q&A**:
   - Users can ask questions about the uploaded document.
   - The chatbot uses the document’s content to generate accurate responses.

3. **Visualization of Data**:
   - Users can ask for visualization of data from the document.
   - The chatbot retrieves the required data and creates a bar plot for the User.

---

## Technologies Used

### Front-end
- **React**:
  - Build a dynamic and interactive user interface.
  - Handle user inputs and display responses from the chatbot.
  
### Back-end
- **Flask Chat-GPT-4O**:
  - Communicate with the front-end via REST APIs.

- **Chat-GPT-4O**:
  - Handle document processing, summarization, and Q&A.

---

## Setup Instructions

### Pre-requisites

1. Install **Node.js** (for the front-end).
2. Install **Python 3.7+** and **pip** (for the back-end).
4. Get your **OPEN AI API Key**
3. Install **virtualenv** (optional but recommended for Python dependency management).

### Steps to Run the Application

#### 1. Set up the Server (Back-end)
1. Create and activate a Python virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # For Linux/Mac
    venv\Scripts\activate      # For Windows

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt

3. Navigate to the `server` directory:
   ```bash
   cd server

4. Run the server using the following command:
    ```bash
    python3 app.py

#### 2. Set up the Chatbot UI (Front-end)
1. Navigate to the `chatbot-ui` directory:
    ```bash
    cd chatbot-ui

2. Install the required Node modules
    ```bash
    npm install

3. Run the client using the following command:
    ```bash
    npm start

---

## Usage Instructions

### Uploading a Document:

Use the file upload option to upload a document.
Wait for the document to be processed. The bot will display a summary.

### Asking Questions:
Type a question about the document in the chat input box.
The bot will respond with answers based on the document's content.
You can also ask the bot to visualize any given numerical figures from the document.

## Troubleshooting Guide

### Front-end Errors

1. **Ensure all dependencies are installed**:  
   Run the following command in the `chatbot-ui` directory to install all required Node.js dependencies:
   ```bash
   npm install

2. **Check the browser console for any errors**:
Use your browser's developer tools to identify issues. Look for error messages in the console.

### Back-end Errors

1. **Verify Python dependencies**:
    Ensure that all Python libraries are installed by running:
    ```bash
    pip install -r requirements.txt

2. **Check if the Flask server is running:**
    Confirm that the Flask server is running. You can start the server by navigating to the server directory and running: