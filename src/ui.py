import streamlit as st
from datetime import datetime
from chatbot import Chatbot

import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="Conestoga Student Support Chatbot", page_icon="💬")

# Hide Streamlit footer
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# Custom CSS to make layout responsive
# Custom CSS
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 50vh;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            overflow: hidden;
        }
        .chat-history {
            flex: 1;
            overflow-y: auto;
            padding-right: 10px;
            margin-bottom: 10px;
        }
        .chat-input {
            border-top: 1px solid #eee;
            padding-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Student Support Chatbot")

# Initialize chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Open chat-container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
# --- Chat history ---
st.markdown("<div class='chat-history'>", unsafe_allow_html=True)

for msg in st.session_state.history:
    if msg.get("sender") == "System":
        st.markdown(
            f"<div style='text-align:center; color: gray; font-size: 12px; margin: 10px 0;'>{msg['text']}</div>",
            unsafe_allow_html=True,
        )
    else:
        align = "left" if msg["sender"] != "You" else "right"
        bubble_color = "#daf4fa"
        avatar = msg.get("avatar", "👤")

        st.markdown(
            f"""
            <div style='display:flex; flex-direction:{"row" if align == "left" else "row-reverse"}; margin-bottom:10px;'>
                <div style='font-size:24px; margin:0 10px;'>{avatar}</div>
                <div>
                    <div style='font-weight:bold; font-size:13px;'>{msg["sender"]}</div>
                    <div style='font-size:11px; color:gray;'>{msg.get("role", "")}</div>
                    <div style='background-color:{bubble_color}; color:black; padding:10px; border-radius:10px; max-width:600px; margin-top:4px;'>
                        {msg["text"]}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)  # Close chat-history

# If input was previously stored, clear it before rendering the input box
if "clear_input" in st.session_state:
    del st.session_state["chat_input"]
    del st.session_state["clear_input"]
    st.rerun()

# --- Chat input ---
st.markdown("<div class='chat-input'>", unsafe_allow_html=True)
user_input = st.text_input("Type a message here and press Enter...", label_visibility="collapsed", key="chat_input")

if user_input:
    st.session_state.history.append({
        "sender": "You",
        "avatar": "🧑‍🎓",
        "text": user_input,
        "time": datetime.now().strftime("%H:%M")
    })

    reply = st.session_state.chatbot.get_answer(user_input)
    st.session_state.history.append({
        "sender": "Lulu",
        "role": "Student Success Advisor",
        "avatar": "🟤",
        "text": reply,
        "time": datetime.now().strftime("%H:%M")
    })
    st.session_state["clear_input"] = True  
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)  # Close chat-input
st.markdown("</div>", unsafe_allow_html=True)  # Close chat-container
