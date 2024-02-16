import streamlit as st
import random

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

st.set_page_config(
    page_title = "MultiLingo",
    page_icon = "🗣️",
)

if "ButtonActivated" not in st.session_state:
    st.session_state.ButtonActivated = False
    st.session_state.QuizStartActivated = False
    st.session_state.QuizEndActivated = False
    st.session_state.counter = 0

    st.session_state.Options = []
    st.session_state.containers = []
    st.session_state.questionlist = []
    st.session_state.correctcounter = 0
    st.session_state.wrongquestionlist = []

st.sidebar.header("Learner Mode") 
st.sidebar.write("Learn The Language.")
st.title("Learner Mode")
st.write("learn The Language!") 
lf = st.selectbox('What language do you want to learn today?',
                         ('French 🇫🇷', 'Chinese 🇨🇳', 'Spanish 🇪🇸'), disabled=st.session_state.ButtonActivated)
lm = languagenumberreference[lf]
  
if st.session_state.get("StartLearnButton", False):
    st.session_state.disabled = False
elif st.session_state.get("but_b", False):
    st.session_state.disabled = True

if (st.button("Start Learning", disabled = st.session_state.ButtonActivated) or st.session_state.ButtonActivated):

    if not st.session_state.ButtonActivated:
        st.session_state.ButtonActivated = True
        samplerange = list(range(0, len(thelistoflanguages)))
        st.session_state.questionlist = random.sample(samplerange, 5)

        for i in range(5):
            st.write(thelistoflanguages[st.session_state.questionlist[i]][int(lm)] + ": " + thelistoflanguages[st.session_state.questionlist[i]][0])
        st.info("To hide the phrases to start memorising, click on the 'Start Learning' button again. To begin the quiz, click on the 'Start Quiz' button.")
        #st.rerun()


    if (st.button("Start Quiz", disabled = st.session_state.QuizStartActivated) or st.session_state.QuizStartActivated):
        
        if not st.session_state.QuizStartActivated:
            st.session_state.QuizStartActivated = True

            random.shuffle(st.session_state.questionlist)
            questionListIndexes = [0]
            questionRange = list(range(5))
            questionRange.remove(0)

            random.shuffle(questionRange)
            questionListIndexes.append(questionRange[0])
            questionListIndexes.append(questionRange[1])

            for qnsIndex in st.session_state.questionlist:
                st.session_state.Options.append(thelistoflanguages[qnsIndex][0])
            
            random.shuffle(st.session_state.Options)
            st.rerun()
            
        if not st.session_state.QuizEndActivated:
            for num in range(5):
                choiceContainer = st.empty()

                multiplechoice = choiceContainer.radio( # This is basically the "multiple choice selection" contruct
                    "What does this mean? "+ thelistoflanguages[st.session_state.questionlist[num]][int(lm)], # This is the question parameter, takes in a string
                    st.session_state.Options,
                    key='rdkey' + str(num),
                    index = 0,
            )
            
            st.session_state.containers.append(choiceContainer)

        if (st.button('Submit', disabled = st.session_state.QuizEndActivated) or st.session_state.QuizEndActivated):
            if not st.session_state.QuizEndActivated:
                st.session_state.QuizEndActivated = True
                for num in range(5):
                    if  st.session_state["rdkey" + str(num)] == thelistoflanguages[st.session_state.questionlist[num]][0]:
                        st.session_state.correctcounter += 1
                    else:
                        st.session_state.wrongquestionlist.append(st.session_state.questionlist[num])
                    num += 1

                for container in st.session_state.containers:
                    container.empty()
                st.rerun()

            st.write("You scored " + str(st.session_state.correctcounter) + "/5")

            if not st.session_state.correctcounter == 5:
                st.write("You got these questions wrong:")

            for wrongqnsindex in st.session_state.wrongquestionlist:
                st.write(thelistoflanguages[wrongqnsindex][int(lm)] + " = " + thelistoflanguages[wrongqnsindex][0])

            if st.session_state.correctcounter == 5:
                st.balloons()

            if st.button("Restart"):
                st.session_state.ButtonActivated = False
                st.session_state.QuizStartActivated = False
                st.session_state.QuizEndActivated = False

                st.session_state.containers = []
                st.session_state.Options = []
                st.session_state.questionlist = []
                st.session_state.correctcounter = 0
                st.session_state.wrongquestionlist = []
                st.rerun()
