import streamlit as st
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

# Load API key from .env
load_dotenv()

# Create Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)
blocked_words=[
    "hack",
    "hacking",
    "virus",
    "malware",
    "bomb",
    "drugs"
]
MAX_LENGTH=300

def evaluate_response(question, answer):
    
    evaluation_prompt = f"""
You are an AI evaluator.

Evaluate the AI response based on the following criteria:

Question:
{question}

Answer:
{answer}

Give scores out of 10 for:

1. Correctness
2. Relevance
3. Completeness

Also provide:
- Overall Score
- One-line feedback

Format:

Correctness: x/10
Relevance: x/10
Completeness: x/10
Overall Score: x/10

Feedback:
...
"""

    evaluation = llm.invoke(evaluation_prompt)
    return evaluation.content

# Streamlit UI
st.set_page_config(page_title="My First GenAI App", page_icon="🤖")

st.title("🤖 My First GenAI Website")
st.write("Ask anything and get an AI response using Groq + LangChain.")

# User input
user_input = st.text_input("Enter your question:")

# Button
if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter a question.")
        
    elif len(user_input)>MAX_LENGTH:
        st.error("Question is too long. Please keep it under 300 characters.")
    
    elif any(word in user_input.lower() for word in blocked_words):
        st.error("❌ This question violates the safety policy.")
        
    else:
        with st.spinner("Thinking..."):
            response = llm.invoke(user_input)
            answer = response.content
            
            evaluation = evaluate_response(user_input, answer)
        
        st.success("Response generated!")

        st.subheader("🤖 AI Response")
        st.write(answer)

        st.divider()

        st.subheader("📊 Evaluation")
        st.write(evaluation)