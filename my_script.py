import google.generativeai as genai
import chromadb
chroma_client = chromadb.PersistentClient(path="./collection")
from pypdf import PdfReader
import pdfplumber
import streamlit as st

api_key = "Your-API-key" # Replace with a proper Gemini API key
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
filePath = "./anatomy_vol_3_edited_final.pdf"

reader = PdfReader(filePath)
pages = len(reader.pages)

texts = []
ids = []
count = 1
for page in range(pages):
    text = reader.pages[page].extract_text()
    texts.append(text)
    ids.append("id"+str(count))
    count += 1

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents = texts,
    ids=ids
)

def ask_query(prompt):
    results = collection.query(
        query_texts=[prompt], 
        n_results=2
    )
    return results
'''
while True:
    prompt = input()
    data = ask_query(prompt)
    response = model.generate_content(f"Using this data: {data}, answer to this prompt: {prompt}.")
    print(response.text)'''

def ask(prompt):
    data = ask_query(prompt)
    response = model.generate_content(f"Using this data: {data}, answer to this prompt: {prompt}.")
    x = response.text
    return x
#chroma_client.delete_collection(name="my_collection")
