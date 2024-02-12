import streamlit as st
thelistoflanguages = [
    ['hello', 'bonjour', '你好', 'hola'],
    ['how are you?', 'comment ça va?', '你好吗？', '¿cómo estás?'],
    ['where are you from?', 'doù viens-tu?', '你来自哪里？', '¿de dónde eres?'],
    ['what do you do?', 'que fais-tu?', '你做什么工作？', '¿a qué te dedicas?'],
    ['how old are you?', 'quel âge as-tu?', '你今年几岁？', '¿cuántos años tienes?'],
    ['goodbye', 'au revoir', '再见', 'adiós'],
    ['thank you', 'merci', '谢谢', 'gracias'],
    ['yes', 'oui', '是的', 'sí'],
    ['no', 'non', '不', 'no'],
    ['toilet', 'traduire', '洗手间', 'baño']
]
languagenumberreference = {
    "English": 0,
    'French 🇫🇷': 1,
    'Chinese 🇨🇳': 2,
    'Spanish 🇪🇸': 3
}

import random
import string

correctansXP = 10
rawcorrectansXP = 5 # no punctuation but correct

st.set_page_config(
    page_title = "TriLingo",
    page_icon = "🗣️",
)
if "LearnButtonActivated" not in st.session_state:
    st.session_state.LearnButtonActivated = False

if 'StartButton' in st.session_state and st.session_state.StartButton == True: # these are session state things, treat them as variables that update in real time with button click
    st.session_state.LearnButtonActivated = True # They will be used for the following slowbutton to prevent input while the function is running
else:
    st.session_state.LearnButtonActivated = False

st.sidebar.header("Learner Mode") 
st.sidebar.write("Learn The Language.")
st.title("Learner Mode")
st.write("learn The Language!") 
lf = st.selectbox('What language do you want to learn today?',
                         ('French 🇫🇷', 'Chinese 🇨🇳', 'Spanish 🇪🇸'), disabled=st.session_state.LearnButtonActivated)
lm = languagenumberreference[lf]

if st.button("Start Learning", disabled=st.session_state.LearnButtonActivated, key='StartButton'):
    st.session_state.LearnButtonActivated = True
    playerxp = 0
    correctcounter = 0
    wrongcounter = 0
    
    samplerange = list(range(0, len(thelistoflanguages)))
    questionlist = random.sample(samplerange, 5)
    for i in range(5):
        st.write(thelistoflanguages[questionlist[i]][int(lm)] + ": " + thelistoflanguages[questionlist[i]][0])
    quizbutton = st.button("Start Quiz")
