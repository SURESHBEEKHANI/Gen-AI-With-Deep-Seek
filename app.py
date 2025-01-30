import os
import streamlit as st
from groq import Groq

# Load Groq API key from environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Groq API key not found. Please set the `GROQ_API_KEY` environment variable.")
    st.stop()

# Custom CSS styling for healthcare theme
st.markdown("""
<style>
    /* Existing styles */
    .main {
        background-color: #e6f7ff; /* Light blue for healthcare */
        color: #000000;
    }
    .sidebar .sidebar-content {
        background-color: #cce6ff; /* Slightly darker blue */
    }
    .stTextInput textarea {
        color: #000000 !important;
    }
    
    /* Add these new styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: black !important;
        background-color: #cce6ff !important;
    }
    
    .stSelectbox svg {
        fill: black !important;
    }
    
    .stSelectbox option {
        background-color: #cce6ff !important;
        color: black !important;
    }
    
    /* For dropdown menu items */
    div[role="listbox"] div {
        background-color: #cce6ff !important;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🩺 HealthCare Assistant")
st.caption("🌟 Your AI-Powered Healthcare Companion")

# Sidebar configuration
with st.sidebar:
    st.divider()
    st.markdown("### Assistant Capabilities")
    st.markdown("""
    - 🩹 Symptom Analysis
    - 💊 Medication Guidance
    - 📋 Health Record Management
    - 💡 Wellness Recommendations
    """)
    st.divider()
    st.markdown("Built with [Groq](https://groq.com/) | [LangChain](https://python.langchain.com/)")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# System prompt configuration
system_prompt_template = "You are an expert AI healthcare assistant. Provide accurate, concise, and empathetic responses " \
                         "to user queries related to health, wellness, and medical guidance. Always respond in English."

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "assistant", "content": "Hi! I'm your HealthCare Assistant. How can I assist you today? 🩺"}]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and processing
user_query = st.chat_input("Type your health-related question here...")

def generate_ai_response(messages):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content
    return response

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Prepare messages for Groq API
    messages = [
        {"role": "system", "content": system_prompt_template},  # System message
    ]
    for msg in st.session_state.message_log:
        # Map "ai" role to "assistant" for compatibility with Groq API
        role = msg["role"]
        if role == "ai":
            role = "assistant"
        messages.append({"role": role, "content": msg["content"]})
    
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        ai_response = generate_ai_response(messages)
    
    # Add AI response to log
    st.session_state.message_log.append({"role": "assistant", "content": ai_response})
    
    # Rerun to update chat display
    st.rerun()