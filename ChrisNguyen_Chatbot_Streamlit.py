import streamlit as st
from openai import OpenAI
from datetime import datetime

# CONFIGURATION
st.set_page_config(page_title="Chris Nguyen - Patient Chat", page_icon="💬")
st.title("🩺 Simulated Patient Chatbot: Chris Nguyen")
st.markdown("Ask Chris Nguyen questions to gather subjective clinical information for your case assessment.")

# Sidebar for API key input
with st.sidebar:
    st.header("🔑 API Settings")
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")
    st.markdown("You can get one at [OpenAI](https://platform.openai.com/account/api-keys).")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Chris Nguyen, a 59-year-old man presenting to clinic with joint pain and swelling in your right big toe. You only reveal information if asked directly. You are calm and cooperative. Only respond to questions about your symptoms, medications, lifestyle, or history. If the question is irrelevant or too vague, gently ask the student to be more specific."},
        {"role": "assistant", "content": "Hi, I'm Chris. I'm here to talk about what's been going on. What would you like to know?"}
    ]

# Chat interface
if openai_api_key:
    user_input = st.chat_input("Ask Chris a question...")
	client = OpenAI(api_key=openai_api_key)
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=st.session_state.messages,
    temperature=0.6
)
reply = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Download conversation button
st.markdown("---")
if st.session_state.get("messages"):
    full_chat = "\n\n".join([
        f"{'You' if m['role'] == 'user' else 'Chris'}: {m['content']}"
        for m in st.session_state["messages"][1:]
    ])
    filename = f"ChrisNguyen_ChatSummary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    st.download_button("📄 Download Chat Summary", full_chat, file_name=filename)
else:
    st.info("Start the conversation above to enable downloading the chat summary.")