import streamlit as st
from datetime import datetime
from chatbot import Chatbot

# Page config
st.set_page_config(page_title="Conestoga Student Support Chatbot", page_icon="💬")
st.title("📚 Student Support Chatbot")
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# Initialize Chatbot only once
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# --- Render conversation history first ---
with st.container():
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

# --- Input form at the bottom ---
with st.form("chat_form"):
    user_input = st.text_input("Type a message here...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

    if submitted and user_input:
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

        st.rerun()