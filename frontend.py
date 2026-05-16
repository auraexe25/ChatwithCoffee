import streamlit as st

from backend import generate_reply, generate_reply_stream

# --- UI Configuration ---
st.title("ChatWithCoffee")
ASSISTANT_AVATAR = "assets/images.jpeg"

# --- Session Initialization ---
# Keep chat history in session_state so it persists across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I’m your coffee chatbot assistant."}
    ]

# Reset history to start a fresh conversation.
if st.button("New Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I’m your coffee chatbot assistant."}
    ]
    st.rerun()

# --- Chat History Rendering ---
for message in st.session_state.messages:
    avatar = ASSISTANT_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# --- New User Input Handling ---
# chat_input returns a value only when user submits a new message.
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    try:
        # Exclude the just-added prompt from history to avoid duplicate input.
        history = st.session_state.messages[:-1]
        full_reply = ""
        # Stream the reply into the chat message as chunks arrive.
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            msg_placeholder = st.empty()
            for chunk in generate_reply_stream(history, prompt):
                full_reply += chunk
                msg_placeholder.write(full_reply)
    except Exception as error:
        # Show readable runtime errors in UI instead of crashing the app.
        full_reply = f"Chat error: {error}"

    st.session_state.messages.append({"role": "assistant", "content": full_reply})