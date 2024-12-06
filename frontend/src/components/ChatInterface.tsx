import React, { useState,  useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './ChatInterface.css';

interface Message {
  text: string;
  isBot: boolean;
  audioFile?: string;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Olá! Eu sou o C3PO, como posso ajudar?", isBot: true }
  ]);
  const [inputText, setInputText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isThinking, setIsThinking] = useState(false);

  const scrollToBottom = () => {
    // Scroll para a última mensagem
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputText.trim()) return;

    setMessages(prev => [...prev, { text: inputText, isBot: false }]);
    setIsThinking(true);

    const response = await fetch('http://localhost:7777/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: inputText })
    });

    const data = await response.json();
    setMessages(prev => [...prev, { text: data.response, isBot: true }]);
    setIsThinking(false);
    setInputText('');
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:7777/process_file', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    setMessages(prev => [...prev, { text: data.response, isBot: true }]);
    setFile(null);
  };

  return (
    <div className="container">
      <h1>Assistente de Pedro Victor Veras C3PO!</h1>
      <img src="https://moseisleychronicles.wordpress.com/wp-content/uploads/2015/11/untitled-215.gif" alt="Description of the GIF" />

      <div className="chat-container">

        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
          ))}
          {isThinking && (
            <div className="message bot thinking">
              C-3PO está pensando...
            </div>
          )}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Digite sua mensagem..."
            disabled={isThinking}
          />
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            accept=".pdf,.jpeg,.jpg"
            disabled={isThinking}
          />
          <button onClick={handleSend} disabled={isThinking || !inputText.trim()}>
            Enviar
          </button>
          <button onClick={handleFileUpload} disabled={!file || isThinking}>
            Enviar Arquivo
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;