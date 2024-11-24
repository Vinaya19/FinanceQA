import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    setSummary(response.data.summary);
  };

  const handleAskQuestion = async () => {
    const response = await axios.post('http://127.0.0.1:5000/ask', {
      question,
      context: summary,
    });

    setAnswer(response.data.answer);
  };

  return (
    <div className="App">
      <h1>Document Chatbot</h1>

      {/* File Upload Section */}
      <div>
        <h2>Upload Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleFileUpload}>Upload & Summarize</button>
      </div>

      {/* Display Summary */}
      {summary && (
        <div>
          <h2>Summary</h2>
          <p>{summary}</p>
        </div>
      )}

      {/* Question Answering Section */}
      {summary && (
        <div>
          <h2>Ask a Question</h2>
          <input
            type="text"
            placeholder="Type your question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button onClick={handleAskQuestion}>Ask</button>
          {answer && (
            <div>
              <h3>Answer:</h3>
              <p>{answer}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
