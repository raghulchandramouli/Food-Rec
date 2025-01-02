from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from typing import Dict
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

RECIPE_TEMPLATE = """
Role: You are an expert culinary assistant
Context: Provide detailed cooking advice and recipe guidance
Question: {question}
Required Format:
- Title of dish (if applicable)
- Ingredients (if applicable)
- Step-by-step instructions
- Tips and variations
"""

def format_prompt(template: str, variables: Dict[str, str]) -> str:
    return template.format(**variables)

def get_gemini_response(question: str):
    prompt = format_prompt(RECIPE_TEMPLATE, {"question": question})
    chat = model.start_chat(history=[])
    return chat.send_message(prompt, stream=True)

st.header("Recipe Assistant")

if 'qa_history' not in st.session_state:
    st.session_state['qa_history'] = []

input_text = st.text_input("What recipe-related question would you like to ask?", key="input")

if st.button("Ask Recipe Question") and input_text:
    st.session_state['qa_history'].append(("Q", input_text))
    
    response = get_gemini_response(input_text)
    full_response = ""
    
    # Display response in real-time
    response_container = st.empty()
    for chunk in response:
        full_response += chunk.text
        response_container.markdown(full_response)
    
    # Store only once in history
    st.session_state['qa_history'].append(("A", full_response))

# Display history in a collapsible section
if st.session_state['qa_history']:
    with st.expander("View Chat History"):
        for role, text in st.session_state['qa_history']:
            st.markdown(f"**{'Question:' if role == 'Q' else 'Answer:'}**")
            st.markdown(text)
            st.divider()