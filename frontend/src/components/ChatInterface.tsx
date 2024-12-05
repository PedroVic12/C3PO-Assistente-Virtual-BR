import React, { useState, useRef, useEffect } from 'react';
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
  const [isListening, setIsListening] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [currentAudio, setCurrentAudio] = useState<HTMLAudioElement | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Connect to WebSocket server
    wsRef.current = new WebSocket('ws://localhost:8000/ws/chat');

    wsRef.current.onopen = () => {
      setIsConnected(true);
      console.log('Connected to WebSocket');
    };

    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, { 
        text: message.content, 
        isBot: true 
      }]);
      setIsThinking(false);
    };

    wsRef.current.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from WebSocket');
    };

    return () => {
      wsRef.current?.close();
    };
  }, []);

  const playAudio = (audioFile: string) => {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
    }
    const audio = new Audio(`/static/mp3/${audioFile}`);
    setCurrentAudio(audio);
    audio.play().catch(error => {
      console.error('Erro ao tocar áudio:', error);
    });
  };

  const handleSend = async () => {
    if (!inputText.trim() || !wsRef.current || !isConnected) return;

    setMessages(prev => [...prev, { text: inputText, isBot: false }]);
    setIsThinking(true);

    const message = {
      type: 'message',
      content: inputText
    };

    wsRef.current.send(JSON.stringify(message));
    setInputText('');
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
              <ReactMarkdown>{msg.text}</ReactMarkdown>
              {msg.isBot && msg.audioFile && (
                <button 
                  className="audio-button"
                  onClick={() => playAudio(msg.audioFile!)}
                >
                  🔊 Ouvir Resposta
                </button>
              )}
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
            disabled={isThinking || !isConnected}
          />
          <button onClick={handleSend} disabled={isThinking || !inputText.trim() || !isConnected}>
            Enviar
          </button>
          <button 
            onClick={toggleVoice}
            className={`voice-button ${isListening ? 'recording' : ''}`}
            disabled={isThinking || !isConnected}
          >
            🎤
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
