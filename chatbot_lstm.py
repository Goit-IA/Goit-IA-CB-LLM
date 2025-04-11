import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense
import pickle

# Paso 1: Cargar el dataset
data = pd.read_csv('data.csv')

# Paso 2: Preparar datos
inputs = data['input'].astype(str).tolist()
responses = data['response'].astype(str).tolist()

# Tokenizer para las entradas
input_tokenizer = Tokenizer()
input_tokenizer.fit_on_texts(inputs)
input_sequences = input_tokenizer.texts_to_sequences(inputs)
input_padded = pad_sequences(input_sequences, padding='post')

# Tokenizer para las respuestas
response_tokenizer = Tokenizer()
response_tokenizer.fit_on_texts(responses)
response_sequences = response_tokenizer.texts_to_sequences(responses)
response_padded = pad_sequences(response_sequences, padding='post')

# Paso 3: Crear el modelo
vocab_size_input = len(input_tokenizer.word_index) + 1
vocab_size_response = len(response_tokenizer.word_index) + 1

model = Sequential()
model.add(Embedding(input_dim=vocab_size_input, output_dim=64, input_length=input_padded.shape[1]))
model.add(LSTM(64))
model.add(Dense(vocab_size_response, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Paso 4: Entrenar
model.fit(input_padded, np.array(response_padded)[:,0], epochs=500, verbose=1)

# Paso 5: Guardar modelo y tokenizers
model.save('chatbot_model.h5')

with open('input_tokenizer.pkl', 'wb') as f:
    pickle.dump(input_tokenizer, f)

with open('response_tokenizer.pkl', 'wb') as f:
    pickle.dump(response_tokenizer, f)

print("Modelo entrenado y guardado exitosamente.")
