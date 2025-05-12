import streamlit as st
import time

# Título de la aplicación
st.title("Chatbot Interactivo")

# Inicializar el historial de chat en el estado de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes del historial en cada ejecución de la app
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if user_input := st.chat_input("Escribe tu mensaje aquí..."):
    # Mostrar el mensaje del usuario en el contenedor de chat
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Agregar el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Simular tiempo de carga
    with st.spinner("Procesando respuesta..."):
        time.sleep(5)  # Delay de 5 segundos
    
    # Generar respuesta
    response = f"Hola, recibí tu mensaje: {user_input}"
    
    # Mostrar la respuesta del asistente en el contenedor de chat
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Agregar la respuesta al historial
    st.session_state.messages.append({"role": "assistant", "content": response})
