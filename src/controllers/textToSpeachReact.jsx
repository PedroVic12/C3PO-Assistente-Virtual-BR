import React, { useState, useEffect, useRef } from "react";

function SpeechRecognition({ options }) {
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
    }, [options]);

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
            <button onClick={toggleListening}>
                {isListening ? "Stop Listening" : "Start Listening"}
            </button>
            <div>{transcription}</div>
        </div>
    );
}

export default SpeechRecognition;
