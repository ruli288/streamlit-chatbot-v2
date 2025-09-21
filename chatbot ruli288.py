import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from streamlit_option_menu import option_menu

# Inisialisasi ChatBot (hanya sekali, tidak setiap rerun)
@st.cache_resource
def load_bot():
    bot = ChatBot('ChatBot Ruli288')
    trainer = ChatterBotCorpusTrainer(bot)
    try:
        trainer.train("chatterbot.corpus.indonesian")
    except Exception:
        pass  # Agar tidak duplikasi training
    return bot

bot = load_bot()

# Custom CSS untuk memperindah UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #b3ffab 0%, #12fff7 100%);
    }
    .chat-bubble {
        padding: 10px 15px; margin: 10px 0; border-radius: 15px; max-width: 70%;
        display: inline-block; font-size: 16px;
    }
    .user {background: #fff; color: #222; align-self: flex-end;}
    .bot {background: #0f2027; color: #fff; align-self: flex-start;}
    .chat-container {display: flex; flex-direction: column;}
    </style>
""", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Menu", ["Chat", "Tentang"], 
        icons=["chat-dots", "info-circle"], 
        menu_icon="robot", default_index=0
    )

st.title("🤖 ChatBot Ruli288")
st.caption("Chatbot sederhana dengan antarmuka cantik menggunakan Streamlit")

if selected == "Chat":
    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_input("Ketik pesan Anda...", key="input")

    if st.button("Kirim") and user_input:
        response = bot.get_response(user_input)
        st.session_state.history.append(("Anda", user_input))
        st.session_state.history.append(("ChatBot Ruli288", str(response)))
        st.experimental_rerun()

    # Tampilkan riwayat chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for speaker, message in st.session_state.history:
        role = "user" if speaker == "Anda" else "bot"
        st.markdown(
            f'<div class="chat-bubble {role}"><b>{speaker}:</b> {message}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Tentang":
    st.subheader("Tentang ChatBot Ruli288")
    st.write("""
    ChatBot Ruli288 adalah chatbot sederhana yang dibangun dengan Python, Streamlit, dan ChatterBot.
    Dikembangkan oleh **ruli288**.
    """)

    st.write("Source code: [GitHub](https://github.com/ruli288/chat-bot-ruli288-friendly)")
