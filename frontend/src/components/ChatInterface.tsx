import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Mic, Send, StopCircle } from 'lucide-react';
import { C3POAvatar } from './C3POAvatar';
import { ChatMessage } from './ChatMessage';
import { cn } from '../lib/utils';

interface Message {
  text: string;
  isBot: boolean;
}

// API calls will be proxied through Vite
const API_URL = '/api';

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Olá! Eu sou o C3PO, como posso ajudar?", isBot: true }
  ]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputText.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { text: inputText, isBot: false }]);
    setInputText('');
    
    // Show bot thinking state
    setIsThinking(true);
    
    try {
      const response = await fetch(`${API_URL}/chat`, {
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
      
      setMessages(prev => [...prev, { 
        text: data.response, 
        isBot: true 
      }]);

      // Play audio if available
      if (data.audio_file) {
        const audio = new Audio(`${API_URL}/static/${data.audio_file}`);
        audio.play();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        text: "Desculpe, ocorreu um erro ao processar sua mensagem.", 
        isBot: true 
      }]);
    } finally {
      setIsThinking(false);
    }
  };

  const toggleListening = () => {
    setIsListening(!isListening);
    // Add voice recognition logic here
  };

  return (
    <div className="flex flex-col h-screen bg-background p-4">
      {/* Header */}
      <div className="flex justify-center mb-4">
        <C3POAvatar 
          isListening={isListening}
          isThinking={isThinking}
          className="mb-4"
        />
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message.text}
            isBot={message.isBot}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex items-center gap-2">
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={toggleListening}
          className={cn(
            "p-3 rounded-full",
            isListening ? "bg-red-500" : "bg-primary"
          )}
        >
          {isListening ? (
            <StopCircle className="w-6 h-6 text-white" />
          ) : (
            <Mic className="w-6 h-6 text-secondary" />
          )}
        </motion.button>

        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Digite sua mensagem..."
          className="flex-1 p-3 rounded-full bg-background-light text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
        />

        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={handleSend}
          className="p-3 rounded-full bg-primary"
          disabled={!inputText.trim()}
        >
          <Send className="w-6 h-6 text-secondary" />
        </motion.button>
      </div>
    </div>
  );
}
