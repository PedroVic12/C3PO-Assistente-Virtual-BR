import streamlit as st

def chatbot_page():
    st.title("## Chatbot Page")
    st.write("Welcome to the Chatbot Page! Here you can interact with our chatbot.")



    # Criar historico
    if not "lista_mensagens" in st.session_state:
        st.session_state["lista_mensagens"] = []
        
    msg_usuario = st.chat_input("Escreva sua mensagem aqui...")
    resposta_c3po = "Olá! Eu sou o C-3PO, seu assistente de chatbot. Como posso ajudá-lo hoje?"



    if msg_usuario:


        # lista de mensagens de historico
        st.chat_message("user").write(msg_usuario)
        chat_message = {"role":"user", "content": msg_usuario}
        st.session_state["lista_mensagens"].append(chat_message)


        resposta_c3po = "Você disse: " + msg_usuario  
        st.chat_message("assistant").write(resposta_c3po)
        AI_messsage = {"role":"assistant", "content": resposta_c3po}
        st.session_state["lista_mensagens"].append(AI_messsage)




    # tornar as respostas mais inteligentes (usar modelo de linguagem)