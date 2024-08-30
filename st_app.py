import streamlit as st
import chromadb
import google.generativeai as genai
import pandas as pd

pictures = pd.read_csv("./image_filenames.csv")
pics_loc = pictures['Image Name']
pics_loc = list(pics_loc)
texts = pictures['Description']
texts = list(texts)

api_key = "AIzaSyBt41MC3ZSxYlBktQH0WN_OFP45Jz7zjYs"
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = st.text_input("Enter your query here: ")

chroma_client = chromadb.PersistentClient(path="./collection")
collections = chroma_client.get_collection(name="my_collection")
img_collections = chroma_client.get_collection(name="images")

def ask_query(prompt):
    results = collections.query(
        query_texts=[prompt], 
        n_results=2
    )
    return results

def ask_img(prompt):
    results = img_collections.query(
        query_texts=[prompt], 
        n_results=1
    )
    return results['documents']

def ask(prompt):
    x = ask_img(prompt=prompt)
    if x:
        val = texts.index(x[0][0])
        img = "./images/" + str(pics_loc[int(val)])
        st.image(img)
    data = ask_query(prompt)
    response = model.generate_content(f"Using this data: {data}, answer to this prompt: {prompt}.")
    x = response.text
    return x

response = ask(prompt=prompt)
st.write(response)