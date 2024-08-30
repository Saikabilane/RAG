import streamlit as st
import chromadb
import google.generativeai as genai
import pandas as pd

pictures = pd.read_csv("./image_filenames.csv")
pics_loc = pictures['Image Name']
pics_loc = list(pics_loc)
texts = pictures['Description']
texts = list(texts)

api_key = "Your-API-key" # Replace with a proper Gemini API key
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

chroma_client = chromadb.PersistentClient(path="./collection")
collections = chroma_client.get_collection(name="my_collection")
img_collections = chroma_client.get_collection(name="images")

st.title("Education Assistant")
prompt = st.text_input("Enter your query here: ")

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
    if results["distances"][0][0] >= 1:
        results = []
        return results
    return results['documents']

def ask(prompt):
    x = ask_img(prompt=prompt)
    data = ask_query(prompt)
    title_res = model.generate_content(f"Provide a appropriate title for the answer {prompt} of content. only that title.")
    response = model.generate_content(f"Using this data: {data}, answer to this prompt: {prompt}. if you don't find any data, just don't answer the question.")
    st.header(title_res.text)
    st.write(response.text)
    if x:
        val = texts.index(x[0][0])
        img = "./images/" + str(pics_loc[int(val)])
        st.image(img)

ask(prompt=prompt)
