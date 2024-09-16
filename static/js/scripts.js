console.log("C3PO-Assistente-Virtual-BR como usar react dentro do flask???");

const { useState, useEffect, useRef } = React;

// Componente SpeechRecognition
function SpeechRecognition({ options, onTranscriptionUpdate }) {
    const [isListening, setIsListening] = useState(false);
    const [transcription, setTranscription] = useState("");
    const recognitionRef = useRef(null);

    useEffect(() => {
        if (!("webkitSpeechRecognition" in window)) {
            alert("Speech Recognition is not supported in your browser");
            return;
        }

        const recognition = new window.webkitSpeechRecognition();
        recognition.interimResults = options?.interimResults || true;
        recognition.continuous = true;
        recognition.lang = options?.lang || "en-US";

        recognition.onresult = event => {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            setTranscription(transcript);
            onTranscriptionUpdate(transcript);
        };

        recognition.onerror = event => {
            console.error("Error occurred in recognition: " + event.error);
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        recognitionRef.current = recognition;

        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.stop();
            }
        };
    }, [options, onTranscriptionUpdate]);

    const toggleListening = () => {
        if (isListening) {
            recognitionRef.current.stop();
        } else {
            recognitionRef.current.start();
        }
        setIsListening(prev => !prev);
    };

    return (
        <div>
            <button id="voice-toggle" onClick={toggleListening} className={isListening ? '' : 'off'}>
                {isListening ? "Stop Listening" : "Start Listening"}
            </button>
            <div>{transcription}</div>
        </div>
    );
}

// Componente ChatbotUser
function ChatbotUser() {
    const [userInput, setUserInput] = useState('');
    const [conversationHistory, setConversationHistory] = useState([{ role: 'system', content: 'Você é um assistente atencioso.' }]);
    const [models, setModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState('gemini-pro');
    const [voiceEnabled, setVoiceEnabled] = useState(true);
    const [audioFile, setAudioFile] = useState("/static/output.mp3");

    useEffect(() => {
        const fetchModels = async () => {
            try {
                const response = await axios.get('/models');
                setModels(response.data);
            } catch (error) {
                console.error('Erro ao buscar modelos:', error);
            }
        };
        fetchModels();
    }, []);

    const handleInputChange = (event) => {
        setUserInput(event.target.value);
    };

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
    };

    const toggleVoice = () => {
        setVoiceEnabled(prevState => !prevState);
    };

    const sendMessage = async () => {
        if (userInput.trim() !== '') {
            setConversationHistory(prev => [...prev, { role: 'user', content: userInput }]);
            setUserInput('');

            try {
                const response = await axios.post('/chat', {
                    model: selectedModel,
                    user_input: userInput,
                    conversation_history: conversationHistory,
                    voice_enabled: voiceEnabled
                });

                const newConversationHistory = response.data.conversation_history;
                setConversationHistory(newConversationHistory);
                setAudioFile(`/audio/${response.data.audio_file}`);

                if (voiceEnabled && response.data.audio_file) {
                    const audio = new Audio(`/audio/${response.data.audio_file}`);
                    audio.play();
                }

                // Text-to-Speech for assistant response
                const assistantMessage = newConversationHistory.find(msg => msg.role === 'assistant');
                if (assistantMessage && voiceEnabled) {
                    const utterance = new SpeechSynthesisUtterance(assistantMessage.content);
                    window.speechSynthesis.speak(utterance);
                }
            } catch (error) {
                console.error('Erro ao enviar mensagem:', error);
            }
        }
    };

    return (
        <div className="container">
            <h1>Assistente de Pedro Victor Veras C3PO! Tdah, produtividade, rotinas e treinos!</h1>
            <div>
                <img src="https://moseisleychronicles.wordpress.com/wp-content/uploads/2015/11/untitled-215.gif" alt="Description of the GIF" />
                <figure>
                    <figcaption>Ouça o áudio gerado:</figcaption>
                    <audio id="audioPlayer" controls src={audioFile}></audio>
                    <a href={audioFile}>Baixar áudio</a>
                </figure>
            </div>
            <select id="model-select" value={selectedModel} onChange={handleModelChange}>
                {models.map(model => (
                    <option key={model} value={model}>{model}</option>
                ))}
            </select>
            <button id="voice-toggle" className={voiceEnabled ? '' : 'off'} onClick={toggleVoice}>
                Voz: {voiceEnabled ? 'Ligada' : 'Desligada'}
            </button>
            <SpeechRecognition 
                options={{}} // Ajuste conforme necessário
                onTranscriptionUpdate={(transcription) => setUserInput(transcription)}
            />
            <div id="chat-history">
                {conversationHistory.map((message, index) => (
                    <div key={index} className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}>
                        <strong>{message.role === 'user' ? 'Você' : 'Assistente'}:</strong> {message.content}
                    </div>
                ))}
            </div>
            <div className="input-area">
                <input
                    type="text"
                    id="user-input"
                    placeholder="Digite sua mensagem..."
                    value={userInput}
                    onChange={handleInputChange}
                    onKeyPress={event => event.key === 'Enter' && sendMessage()}
                />
                <button id="send-button" onClick={sendMessage}>Enviar</button>
            </div>
        </div>
    );
}

export default ChatbotUser;