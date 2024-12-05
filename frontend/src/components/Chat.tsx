import React, { useEffect, useRef, useState } from 'react';

interface Message {
  type: 'user' | 'assistant';
  content: string;
}

export const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Connect to WebSocket server
    wsRef.current = new WebSocket('ws://localhost:8000/ws/chat');

    wsRef.current.onopen = () => {
      setIsConnected(true);
      console.log('Connected to WebSocket');
    };

    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, { type: 'assistant', content: message.content }]);
    };

    wsRef.current.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from WebSocket');
    };

    return () => {
      wsRef.current?.close();
    };
  }, []);

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !wsRef.current) return;

    const message = {
      type: 'message',
      content: input
    };

    wsRef.current.send(JSON.stringify(message));
    setMessages(prev => [...prev, { type: 'user', content: input }]);
    setInput('');
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto p-4">
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg ${
              message.type === 'user'
                ? 'bg-blue-500 text-white ml-auto'
                : 'bg-gray-200 text-gray-800'
            } max-w-[80%]`}
          >
            {message.content}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          placeholder="Type your message..."
          disabled={!isConnected}
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
          disabled={!isConnected}
        >
          Send
        </button>
      </form>
    </div>
  );
};
