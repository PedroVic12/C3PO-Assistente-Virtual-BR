import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';

interface Message {
  text: string;
  isBot: boolean;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Olá! Eu sou o C3PO, como posso ajudar?", isBot: true }
  ]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputText.trim()) return;

    setMessages(prev => [...prev, { text: inputText, isBot: false }]);
    setInputText('');
    setIsThinking(true);

    try {
      const response = await fetch('/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_input: inputText,
          conversation_history: messages.map(msg => ({
            role: msg.isBot ? 'assistant' : 'user',
            content: msg.text
          })),
          voice_enabled: true
        }),
      });

      const data = await response.json();
      
      setMessages(prev => [...prev, { text: data.response, isBot: true }]);

      if (data.audio_file) {
        const audio = new Audio(`/api/static/${data.audio_file}`);
        audio.play();
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        text: "Desculpe, ocorreu um erro ao processar sua mensagem.", 
        isBot: true 
      }]);
    } finally {
      setIsThinking(false);
    }
  };

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob);

        try {
          const response = await fetch('/api/speech-to-text', {
            method: 'POST',
            body: formData
          });

          const data = await response.json();
          if (data.text) {
            setInputText(data.text);
            handleSend();
          }
        } catch (error) {
          console.error('Error converting speech to text:', error);
        }

        audioChunksRef.current = [];
      };

      mediaRecorderRef.current.start();
      setIsListening(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopListening = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsListening(false);
    }
  };

  const toggleVoice = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  return (
    <div className="container">
      <h1>Assistente de Pedro Victor Veras C3PO! Tdah, produtividade, rotinas e treinos!</h1>
      <div className="image-container">
        <img src="https://moseisleychronicles.wordpress.com/wp-content/uploads/2015/11/untitled-215.gif" alt="C3PO Animation" />
      </div>
      <div className="chat-container">
        <div className="messages" ref={messagesEndRef}>
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
              {msg.text}
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
          <button onClick={handleSend} disabled={isThinking || !inputText.trim()}>
            Enviar
          </button>
          <button 
            onClick={toggleVoice}
            className={`voice-button ${isListening ? 'recording' : ''}`}
            disabled={isThinking}
          >
            🎤
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
