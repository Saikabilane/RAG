# Education Assistant

## Project Overview

The **Anatomy Education Chatbot** is an AI-powered tool designed to assist students in understanding complex anatomy topics. By leveraging Gemini API and educational resources, this chatbot provides real-time answers and interactive diagrams to enhance the learning experience. The chatbot aims to be an accessible, engaging, and effective supplementary resource for students studying anatomy.

## Features

- **Real-Time Query Resolution:** Instant responses to user questions about anatomy.
- **Interactive Diagrams:** Visual aids to enhance understanding of complex anatomical structures.

## Architecture

- **Frontend:** 
  - User-friendly interface made with Streamlit.
- **Backend:** 
  - Powered by a Gemini AI API, provides well structured and informational responses along with relevant images.
- **Data Sources:** 
  - The chatbot accesses a curated database of anatomy textbooks  provided  to ensure the accuracy of information provided.

## Technologies Used

- **Programming Languages:** Python
- **Tools:** Gemini API, Streamlt, Chroma DB, PyPDF, Pillow

## Installation

To set up the Anatomy Education Chatbot locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Saikabilane/RAG.git

2. **Navigate to the project directory:**

   ```bash
   cd RAG

3. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    ```
    ```bash
    venv\Scripts\activate
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Initial Setup

1. **Get your API key:**

    - Get your Gemini API key from https://aistudio.google.com/app/apikey
    - Use the API key in place of "Your-API-key" in my_script.py and st_app.py  
   
3. **Create a folder:**

   ```bash
   mkdir images
   ```

4. **Run the python files**

   ```bash
   python imageExtract.py
   ```
   ```bash
   python img_fetch.py
   ```
   ```bash
   python my_script.py
   ```

## Usage

1. **Run the Application:**

   ```bash
   streamlit run .\st_app.py
   ```
2. **Ask your Queries to the Education Assistant chatbot**

   

