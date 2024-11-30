import React, { useState } from 'react';
import axios from 'axios';
import './App.css';


function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [longContext, setLongContext] = useState("");
  const [question, setQuestion] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [isChatting, setIsChatting] = useState(false);

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    setSummary(response.data.summary);
    setChatHistory([]);
    setIsChatting(true); // Enable chat mode
  };

  const handleAskQuestion = async () => {
    const response = await axios.post('http://127.0.0.1:5000/ask', {
      question,
      chatHistory,
      longContext,
    });

    const answer = response.data.answer;
    setChatHistory((prev) => [...prev, { question, answer }]); // Update chat history
    setBotResponse(answer);
    setLongContext(response.data.longContext);
    setQuestion(''); // Clear input after asking
  };

  const endChat = () => {
    setIsChatting(false);
    setChatHistory([]);
    setSummary('');
    setBotResponse('');
    setQuestion('');
  };

  return (
    <div className="App">
      <h1>Document Chatbot</h1>

      {!isChatting && (
        <div>
          <h2>Upload Document</h2>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={handleFileUpload}>Upload & Start Chat</button>
        </div>
      )}

      {isChatting && (
        <div>
          <h2>Summary</h2>
          <p>{summary}</p>

          <h2>Chat with the Document</h2>
          <div>
            {chatHistory.map((chat, index) => (
              <div key={index}>
                <p><strong>You:</strong> {chat.question}</p>
                <p><strong>Bot:</strong> {chat.answer}</p>
              </div>
            ))}
          </div>

          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button onClick={handleAskQuestion}>Ask</button>

          {/* {botResponse && (
            <div>
              <p><strong>Bot:</strong> {botResponse}</p>
            </div>
          )} */}

          <button onClick={endChat} style={{ marginTop: '20px', background: 'red', color: 'white' }}>
            End Chat
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
