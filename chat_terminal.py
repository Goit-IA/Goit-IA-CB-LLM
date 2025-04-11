import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# Cargar modelo y tokenizers
model = load_model('chatbot_model.h5')

with open('input_tokenizer.pkl', 'rb') as f:
    input_tokenizer = pickle.load(f)

with open('response_tokenizer.pkl', 'rb') as f:
    response_tokenizer = pickle.load(f)

response_index_word = {index: word for word, index in response_tokenizer.word_index.items()}

def predict_response(text):
    sequence = input_tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=model.input_shape[1], padding='post')
    prediction = model.predict(padded, verbose=0)
    response_index = np.argmax(prediction)

    for word, index in response_tokenizer.word_index.items():
        if index == response_index:
            return word
    return "No entendí eso."

# Interacción en terminal
print("Chatbot listo. Escribe 'salir' para terminar.")
while True:
    user_input = input("Tú: ")
    if user_input.lower() == 'salir':
        break
    response = predict_response(user_input)
    print("Bot:", response)
