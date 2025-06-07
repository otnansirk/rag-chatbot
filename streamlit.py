import streamlit as st
from services.knowlage import Knowlage

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("📄 Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    st.markdown(f"**🧑 Kamu:** {chat['question']}")
    st.markdown(f"**🤖 Nana:** {chat['answer']}")

query = st.chat_input("Tulis pertanyaanmu...")
if query:
    st.session_state.chat_history.append({
        "question": query,
        "answer": "Thinking..." 
    })

    # Show Chat User and Placeholder Bot
    st.markdown(f"**🧑 Kamu:** {query}")
    spinner_placeholder = st.empty()

    with st.spinner("Thinking...", show_time=True):

        # Do the query process
        knowlage = Knowlage("investa")
        try:
            res = knowlage.query(query)
            answer = res.get("result", "Error")
        except Exception as e:
            answer = "❌ There was a mistake when answering."

        # Update the answer results in the last chat_history
        st.session_state.chat_history[-1]["answer"] = answer

        # Change spinner with the actual answer
        spinner_placeholder.empty()
        st.markdown(f"**🤖 Nana:** {answer}")
