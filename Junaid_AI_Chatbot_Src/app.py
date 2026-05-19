import streamlit as st
from google import genai
import time

# 🔑 API KEY
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# =========================
# 🌙 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Junaid's AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =========================
# 🎨 UI STYLE
# =========================
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0e1117 !important;
    color: white !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 6rem;
}

.chat-row {
    display: flex;
    margin: 12px 0;
    align-items: flex-end;
}

.chat-row.user {
    justify-content: flex-end;
}

.chat-row.assistant {
    justify-content: flex-start;
}

.chat-bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 16px;
    line-height: 1.5;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.user-bubble {
    background: #2b6fff;
    color: white;
    border-bottom-right-radius: 5px;
}

.assistant-bubble {
    background: #1a1c23;
    color: white;
    border: 1px solid #2a2d36;
    border-bottom-left-radius: 5px;
}

.avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    margin: 0 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #111318;
    border: 1px solid #2a2d36;
    font-size: 18px;
}

.user .avatar {
    order: 2;
}

[data-testid="stChatInput"] textarea {
    background-color: #1a1c23 !important;
    color: white !important;
    border: 1px solid #333 !important;
}

[data-testid="stChatInputContainer"] {
    background-color: #0e1117 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🧠 TITLE
# =========================
st.markdown(
    "<h1 style='text-align:center; color:red;'>🤖 Junaid's AI Chatbot</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# 💾 SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 💬 RENDER FUNCTION
# =========================
def render_message(role, content):
    if role == "user":
        st.markdown(f"""
        <div class="chat-row user">
            <div class="chat-bubble user-bubble">{content}</div>
            <div class="avatar">🧑</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-row assistant">
            <div class="avatar">🤖</div>
            <div class="chat-bubble assistant-bubble">{content}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# 📜 CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

# =========================
# 💬 INPUT
# =========================
user_input = st.chat_input("Ask me anything...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    render_message("user", user_input)

    # =========================
    # ✨ TYPING ANIMATION
    # =========================
    typing_placeholder = st.empty()

    with typing_placeholder:
        st.markdown("""
        <div class="chat-row assistant">
            <div class="avatar">🤖</div>
            <div class="chat-bubble assistant-bubble">
                Typing...
            </div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(0.8)

    # =========================
    # 🤖 GEMINI RESPONSE (SAFE)
    # =========================
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=user_input
        )
        reply = response.text

    except Exception:
        reply = "⚠️ Server error please come back later"

    # remove typing
    typing_placeholder.empty()

    # save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # show assistant message
    render_message("assistant", reply)