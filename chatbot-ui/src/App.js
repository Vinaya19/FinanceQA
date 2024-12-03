import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function isNestedObject(obj) {
  return Object.values(obj).some(value => typeof value === "object" && value !== null);
}

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [longContext, setLongContext] = useState("");
  const [question, setQuestion] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [isChatting, setIsChatting] = useState(false);
  const [greetingMessage, setGreetingMessage] = useState('');
  const [chartUrl, setChartUrl] = useState(null);

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    const cleanSummary = response.data.summary
    .replace(/\*\*(.+)\*\*/g, '<strong>$1</strong>')  // Replace **text** with <strong>text</strong>
    .replace(/\*(.+)\*/g, '<strong>$1</strong>'); 


    setSummary(cleanSummary);
    setChatHistory([]);
    setIsChatting(true);
    setGreetingMessage('Hello! You can now chat with your document. 😊');
  };

  const handleAskQuestion = async () => {
    const response = await axios.post('http://127.0.0.1:5000/ask', {
      question,
      chatHistory,
      longContext,
    });

    const answer = response.data.answer;
    if (response.data.visualizationData) {
      handleVisualization(response.data.visualizationData);
    }else{
      setBotResponse(answer);
    }
    setChatHistory((prev) => [...prev, { question, answer }]);
    setLongContext(response.data.longContext);
    setQuestion('');
  };

  const handleVisualization = async (visualizationData) => {
    let labels, values;
    if (isNestedObject(visualizationData)){
      console.log("Visualization Data",visualizationData);
      const innerDict = Object.values(visualizationData)[0];
      labels = Object.keys(innerDict);
      values = Object.values(innerDict);
      console.log("labels:",labels);
      console.log("values:", values);
    }else{
      labels = Object.keys(visualizationData);
      values = Object.values(visualizationData);      
    }

    const response = await axios.post('http://127.0.0.1:5000/visualize', {
      numbers: values,
      labels: labels,
    }, { responseType: 'blob' });

    const imageUrl = URL.createObjectURL(response.data);
    setChartUrl(imageUrl);
  };

  const endChat = () => {
    setIsChatting(false);
    setChatHistory([]);
    setSummary('');
    setBotResponse('');
    setQuestion('');
    setGreetingMessage('Goodbye! Thank you for using our service. 👋');
  };

  return (
    <div className="App">
      <h1>Finance Question Answer Bot</h1>

      {!isChatting && (
        <div className="upload-section">
          <h2>Upload Document</h2>
          <label htmlFor="file-upload" className="curved-upload-button">
            Choose File
            <input
              id="file-upload"
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ display: 'none' }}
            />
          </label>
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
            <p dangerouslySetInnerHTML={{ __html: summary }} />
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

              {chartUrl && (
                <div>
                  <h2>Chart</h2>
                  <img src={chartUrl} alt="Visualization" />
                </div>
              )}

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
