import pandas as pd
import wikipedia

url = 'https://en.wikipedia.org/wiki/Harry_Potter_(film_series)'
film_data = pd.read_html(url)[1]
film_names = film_data['Film'].tolist()
film_contents = [wikipedia.page(title = film).content for film in film_names]

film_data['page_content'] = film_contents

# Mostrar las primeras filas en consola
#print(film_data.head())

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500, 
    chunk_overlap = 20, 
    length_function = len
)

metadata = film_data[['Year',  'Film', 'Director']].to_dict(orient='records')

documents = text_splitter.create_documents(
    texts= film_data['page_content'].tolist(),
    metadatas= metadata
)

print(film_data.head())

