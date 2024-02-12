import streamlit as st
st.set_page_config(
    page_title = "TriLingo",
    page_icon = "🗣️",
)

st.sidebar.header("Learner Mode") 
st.sidebar.write("Learn The Language.")
st.title("Learner Mode")
st.write("learn The Language!") 
lf = st.selectbox('What language do you want to learn today?',
                         ('Chinese 🇨🇳', 'French 🇫🇷', 'Spanish 🇪🇸'))

