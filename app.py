# Import necessary libraries to use their functions
import os
import streamlit as st
from groq import Groq

# Get the API key from the environment settings
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# If there is no API key, show an error message and stop the program
if not GROQ_API_KEY:
    st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

# Add custom design for a healthcare theme
st.markdown("""
<style>
/* Set background color for the main section */
.main {
    background-color: #e6f7ff; /* Light blue for a calming effect */
    color: #000000; /* Black text for readability */
}

/* Set background color for the sidebar */
.sidebar .sidebar-content {
    background-color: #cce6ff; /* Slightly darker blue */
}

/* Set text color for input fields */
.stTextInput textarea {
    color: #000000 !important;
}

/* Change styles for dropdown menu */
.stSelectbox div[data-baseweb="select"] {
    color: black !important;
    background-color: #cce6ff !important;
}

/* Change color of dropdown icons */
.stSelectbox svg {
    fill: black !important;
}

/* Change background and text color for dropdown options */
.stSelectbox option {
    background-color: #cce6ff !important;
    color: black !important;
}

/* Change background and text color for dropdown items */
div[role="listbox"] div {
    background-color: #cce6ff !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# Set the title of the app
st.title("🩺 HealthCare Assistant")

# Add a small description under the title
st.caption("🌟 Your AI-Powered Healthcare Companion")

# Create the sidebar with options
with st.sidebar:
    # Add a dividing line
    st.divider()

    # Display a section for assistant features
    st.markdown("### Assistant Capabilities")
    st.markdown("""
    - 🩹 Symptom Analysis
    - 💊 Medication Guidance
    - 📋 Health Record Management
    - 💡 Wellness Recommendations
    """)

    # Add another dividing line
    st.divider()

    # Show a small footer message
    st.markdown("Built with Groq | LangChain ")

# Start the AI client using the API key
client = Groq(api_key=GROQ_API_KEY)

# Define a message that tells the AI how to respond
system_prompt_template = "You are an expert AI healthcare assistant. Provide accurate, concise, and empathetic responses " \
                         "to user queries related to health, wellness, and medical guidance. Always respond in English."

# If chat history does not exist, create a welcome message
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "assistant", "content": "Hi! I'm your HealthCare Assistant. How can I assist you today? 🩺"}]

# Create a container to display chat messages
chat_container = st.container()

# Show chat messages inside the container
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input field for user to type questions
user_query = st.chat_input("Type your health-related question here...")

# Function to get a response from the AI
def generate_ai_response(messages):
    # Send the conversation to the AI model
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=messages,
        temperature=1,  # Controls how random the AI responses are
        max_tokens=1024,  # Maximum length of response
        top_p=1,  # Helps control the response style
        stream=True,  # Enables streaming of responses
        stop=None,
    )

    # Process the AI response piece by piece
    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content

    return response

# If the user has entered a question
if user_query:
    # Save the user's message in chat history
    st.session_state.message_log.append({"role": "user", "content": user_query})

    # Create a list of messages to send to AI
    messages = [
        {"role": "system", "content": system_prompt_template},  # First message that tells AI how to behave
    ]

    # Add all previous messages to the conversation
    for msg in st.session_state.message_log:
        # If the message role is "ai", change it to "assistant"
        role = msg["role"]
        if role == "ai":
            role = "assistant"
        messages.append({"role": role, "content": msg["content"]})

    # Show a loading spinner while AI is thinking
    with st.spinner("🧠 Processing..."):
        # Get the AI response
        ai_response = generate_ai_response(messages)

    # Save the AI's response in chat history
    st.session_state.message_log.append({"role": "assistant", "content": ai_response})

    # Refresh the page to show the new chat messages
    st.rerun()
