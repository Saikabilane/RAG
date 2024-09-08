import streamlit as st
import chromadb
import google.generativeai as genai
import pandas as pd
from fpdf import FPDF
import graphviz

# Load your images and texts
pictures = pd.read_csv("./image_filenames.csv")
pics_loc = pictures['Image Name']
pics_loc = list(pics_loc)
texts = pictures['Description']
texts = list(texts)

# Set up your API keys and model
api_key = "AIzaSyBt41MC3ZSxYlBktQH0WN_OFP45Jz7zjYs"
for_vision = "AIzaSyDWw26GAw7rq2CS4TJxuqGE2mrs6K8kmbM"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Set up Chroma collections
chroma_client = chromadb.PersistentClient(path="./collection")
collections = chroma_client.get_collection(name="my_collection")
img_collections = chroma_client.get_collection(name="images")
bookBack = chroma_client.get_collection(name="book_back")

# Streamlit UI
st.title("Education Assistant")
prompt = st.text_input("Enter your query here: ")

# Functions for querying Chroma collections
def ask_query(prompt):
    results = collections.query(
        query_texts=[prompt], 
        n_results=2
    )
    return results['documents']

def get_bookBack(prompt):
    results = bookBack.query(
        query_texts=[prompt],
        n_results=15
    )
    return results['documents']

def ask_img(prompt):
    results = img_collections.query(
        query_texts=[prompt], 
        n_results=1
    )
    if results["distances"][0][0] >= 1:
        results = []
        return results
    return results['documents']

def generate_flowchart(text_description):
    # Create a new directed graph
    dot = graphviz.Digraph()

    # Set global attributes for the graph
    dot.attr(rankdir='LR', size='10,10')  # 'LR' for left-to-right layout, adjust size as needed

    # Add nodes and edges based on the text description
    lines = text_description.strip().split('\n')
    for line in lines:
        if '->' in line:
            parts = line.split('->')
            start = parts[0].strip()
            end = parts[1].strip()
            dot.node(start, shape='box', style='filled', fillcolor='lightyellow')
            dot.node(end, shape='box', style='filled', fillcolor='lightyellow')
            dot.edge(start, end)
        else:
            dot.node(line.strip(), shape='box', style='filled', fillcolor='lightyellow')

    # Render the graph to a file
    output_file = 'flowchart'
    dot.render(filename=output_file, format='png', cleanup=True)

# Function to get book back questions and generate PDF
def book_back(prompt):
    data = get_bookBack(prompt=prompt)
    response = model.generate_content(f"Retrieve all the questions from the chapter specified in '{prompt}', starting with question 1 and ending with the very last question of the chapter. Do not skip any questions in between. After providing each question, give the corresponding answer immediately from {data}. Ensure that all questions are included, and the answers follow directly after each respective question in a sequential and comprehensive manner.")
    
    # Generate PDF with proper text formatting and line handling
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split the content by new lines
    content_lines = response.text.splitlines()
    
    for line in content_lines:
        if line.strip() != "":
            # Add line to PDF with word wrapping
            pdf.multi_cell(190, 10, line.encode('latin1', 'replace').decode('latin1'))
        else:
            # Add an empty line if necessary
            pdf.ln()

    # Save the PDF
    pdf_output = "book_back_questions.pdf"
    pdf.output(pdf_output)

    # Provide download link in Streamlit
    with open(pdf_output, "rb") as pdf_file:
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name=pdf_output,
            mime="application/pdf"
        )
    
    return response.text

# Main function to handle queries
def ask(prompt):
    if prompt:
        x = ask_img(prompt=prompt)
        data = ask_query(prompt)
        questions = model.generate_content(f"If the user query, '{prompt}', explicitly asks for book back answers for a specific chapter, respond with only 'Yes'. Otherwise, respond with 'No'.")
        if 'Yes' in questions.text:
            given = book_back(prompt=prompt)
        flowchart_response = model.generate_content(
            f"Please check the following user prompt and determine if it is requesting the generation of a flowchart. "
            f"Respond with 'True' if the prompt specifically asks for a flowchart. "
            f"Only respond with 'True' if the request is explicit. "
            f"Otherwise, respond with 'False'. For example, if the prompt is 'Generate a flowchart of the process', return 'True'. "
            f"If the prompt is 'Describe the process in detail', return 'False'.\n\nUser Prompt: {prompt}"
        )        
        if 'True' in flowchart_response.text:
            flowchart_description = model.generate_content(
                f"Transform the following {data} into a flowchart format. Ensure each step is correctly connected with arrows ('->') indicating the flow from one step to the next.\n"
                f"Use the format: 'Step1 -> Step2\nStep2 -> Step3\n... -> End'.\n"
                f"Each step should be connected to the next with '->' in the order they appear.\n\nData: {data}"
            )
            generate_flowchart(flowchart_description.text)
            st.image("./flowchart.png")
        title_res = model.generate_content(f"Provide an appropriate title for the answer {prompt} of content. only that title.")
        response = model.generate_content(f"Using this data: {data}, answer to this prompt: {prompt}. if you don't find any data, just don't answer the question.")
        st.header(title_res.text)
        st.write(response.text)
        if x:
            val = texts.index(x[0][0])
            img = "./images/" + str(pics_loc[int(val)])
            st.image(img)

# Run the ask function
ask(prompt=prompt)