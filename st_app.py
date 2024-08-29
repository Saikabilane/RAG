import streamlit as st
import chromadb
import google.generativeai as genai

api_key = "AIzaSyBt41MC3ZSxYlBktQH0WN_OFP45Jz7zjYs"
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = st.text_input("Enter your response here: ")

chroma_client = chromadb.PersistentClient(path="./collection")
collections = chroma_client.get_collection(name="my_collection")

print(chroma_client.list_collections())
def ask_query(prompt):
    results = collections.query(
        query_texts=[prompt], 
        n_results=2
    )
    return results

def ask(prompt):
    data = ask_query(prompt)
    response = model.generate_content(f"Using this data: {data}, answer to this prompt: {prompt}.")
    x = response.text
    return x

response = ask(prompt=prompt)
st.write(response)