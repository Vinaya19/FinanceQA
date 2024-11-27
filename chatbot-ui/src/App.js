import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [question, setQuestion] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [isChatting, setIsChatting] = useState(false);
  const [greetingMessage, setGreetingMessage] = useState('');

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    setSummary(response.data.summary);
    setChatHistory([]);
    setIsChatting(true);
    setGreetingMessage('Hello! You can now chat with your document. 😊');
  };

  const handleAskQuestion = async () => {
    const response = await axios.post('http://127.0.0.1:5000/ask', {
      question,
      chatHistory,
    });

    const answer = response.data.answer;
    setChatHistory((prev) => [...prev, { question, answer }]);
    setBotResponse(answer);
    setQuestion('');
  };

  const endChat = () => {
    setIsChatting(false);
    setChatHistory([]);
    setSummary('');
    setBotResponse('');
    setQuestion('');
    setGreetingMessage('Goodbye! Thanks for using our service. 👋');
  };

  return (
    <div className="App">
      <h1>Finance Question Answer Bot</h1>

      {!isChatting && (
        <div className="upload-section">
          <h2>Upload Document</h2>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button className="curved-button" onClick={handleFileUpload}>
            Upload & Start Chat
          </button>
        </div>
      )}

      {greetingMessage && <p className="greeting">{greetingMessage}</p>}

      {isChatting && (
        <div className="main-container">
          <div className="summary-section">
            <h2>Summary</h2>
            <p>{summary}</p>
          </div>

          <div className="chat-section">
            <div className="chat-header">
              <h2>Chat with the Document</h2>
              <button className="end-chat-button" onClick={endChat}>X</button>
            </div>

            <div className="chat-history">
              {chatHistory.map((chat, index) => (
                <div key={index}>
                  <p><strong>You:</strong> {chat.question}</p>
                  <p><strong>Bot:</strong> {chat.answer}</p>
                </div>
              ))}
            </div>

            <div className="input-section">
              <input
                type="text"
                placeholder="Ask a question..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
              <button className="curved-button ask-button" onClick={handleAskQuestion}>
                Ask
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
