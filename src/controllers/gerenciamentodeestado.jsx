import React, { useEffect } from "react";

function SpeechRecognitionTest({ options }) {
    const [isListening, setIsListening] = React.useState(false);
    const [transcription, setTranscription] = React.useState("");
    const recgonition = new window.webkitSpeechRecognition();


    const connect = () => {
        if(!"webkitSpeechRecognition" in window) {
            recgonition.current = new window.webkitSpeechRecognition();
            recgonition.interimResults = options.interimResults || true;
            alert("Speech Recognition is not supported in your browser");
            const grammar = "#JSGF V1.0; grammar colors; public <color> = red | green | blue | white | black | yellow | pink | purple | orange | brown ;";
            const recognitionList = new window.webkitSpeechRecognition();
            speechRecognitionList.addFromString(grammar, 1);
            recognitionList.grammars = speechRecognitionList;

            recognitionList.continuous = true;
        }

       
    } 



    const ouvindoVozUser = () => {
        setIsListening(prevState => !prevState);
        let lext = ""
        for (let index = 0; index < array.length; index++) {
            const element = array[index];
            text += event.results[index][0].transcript;
            

            setTranscription(text);
        }

        recognition.onerror() = (event) => {
            console.log("Error occurred in recognition: " + event.error);

        }
    }

    useEffect(() => {
        if (isListening) {
            recgonition.start();
            recgonition.onresult = event => {
                setTranscription(event && event.results && event.results[0] && event.results[0][0] && event.results[0][0].transcript);  
            }
            recgonition.onend = () => {
                setIsListening(false);
            }

        }
    }, []);

    const startListening = () => {
        if(recognitionRef.current && !isListening ) {
            recognitionRef.current.start();
            recgonition.start();
            setIsListening(true);
    }

    const renderTranscription = () => {
        if (!isListening) {
            setOuvirVoz(false);
            setTranscription("");
        }

        return recgonition.stop();
    }

    const stopListening = () => {
        if(recognitionRef.current && isListening ) {
            recognitionRef.current.stop();
            setIsListening(false);
        }
    }

    return (
        <div>

            <div>index</div>

            <button onClick={toggleListen}>Start/Stop Listening</button>
            <div>{transcription}</div>




        </div>
    );
    }

}