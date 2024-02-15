import streamlit as st
import time
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
import random
import string

correctansXP = 10
rawcorrectansXP = 5 # no punctuation but correct

st.set_page_config(
    page_title = "TriLingo",
    page_icon = "🗣️",
)

if "ButtonActivated" not in st.session_state:
    st.session_state.ButtonActivated = False
    st.session_state.QuizStartActivated = False
    st.session_state.QuizEndActivated = False

    st.session_state.ButtonActivated2 = False
    st.session_state.QuizStartActivated2 = False
    st.session_state.QuizEndActivated2 = False

    st.session_state.Options = []
    st.session_state.questionlist = []
    st.session_state.bt_clkd = ""
    st.session_state.playerxp = 0
    st.session_state.correctcounter = 0
    st.session_state.wrongquestionlist = []
        
def callback():
    if st.session_state.ButtonActivated2 == False:
        st.session_state.ButtonActivated2 = True
    elif st.session_state.QuizStartActivated2 == False:
        st.session_state.QuizStartActivated2 = True
    elif st.session_state.QuizEndActivated2 == False:
        st.session_state.QuizEndActivated2 = True

st.sidebar.header("Learner Mode") 
st.sidebar.write("Learn The Language.")
st.title("Learner Mode")
st.write("learn The Language!") 
lf = st.selectbox('What language do you want to learn today?',
                         ('French 🇫🇷', 'Chinese 🇨🇳', 'Spanish 🇪🇸'), disabled=st.session_state.ButtonActivated)
lm = languagenumberreference[lf]
  
if (st.button("Start Learning", on_click = callback, disabled = st.session_state.ButtonActivated) or st.session_state.ButtonActivated):

    if not st.session_state.ButtonActivated:
        st.session_state.ButtonActivated = True

        samplerange = list(range(0, len(thelistoflanguages)))
        st.session_state.questionlist = random.sample(samplerange, 5)
        for i in range(5):
            st.write(thelistoflanguages[st.session_state.questionlist[i]][int(lm)] + ": " + thelistoflanguages[st.session_state.questionlist[i]][0])
        st.rerun()
    if (st.button("Start Quiz", on_click = callback, disabled = st.session_state.QuizStartActivated)or st.session_state.QuizStartActivated):
        
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
            st.rerun()
            
        choiceContainer1 = st.empty()
        choiceContainer2 = st.empty()
        choiceContainer3 = st.empty()
        choiceContainer4 = st.empty()
        choiceContainer5 = st.empty()

        multiplechoice1 = choiceContainer1.radio( # This is basically the "multiple choice selection" contruct
            "What does this mean? "+ thelistoflanguages[st.session_state.questionlist[0]][int(lm)], # This is the question parameter, takes in a string
            st.session_state.Options,
            key='rdkey1',
            index = 0,
        )
        multiplechoice2 = choiceContainer2.radio( # This is basically the "multiple choice selection" contruct
            "What does this mean? "+ thelistoflanguages[st.session_state.questionlist[1]][int(lm)], # This is the question parameter, takes in a string
            st.session_state.Options,
            key='rdkey2',
            index = 0,
        )
        multiplechoice3 = choiceContainer3.radio( # This is basically the "multiple choice selection" contruct
            "What does this mean? "+ thelistoflanguages[st.session_state.questionlist[2]][int(lm)], # This is the question parameter, takes in a string
            st.session_state.Options,
            key='rdkey3',
            index = 0,
        )
        multiplechoice4 = choiceContainer4.radio( # This is basically the "multiple choice selection" contruct
            "What does this mean? "+ thelistoflanguages[st.session_state.questionlist[3]][int(lm)], # This is the question parameter, takes in a string
            st.session_state.Options,
            key='rdkey4',
            index = 0,
        )
        multiplechoice5 = choiceContainer5.radio( # This is basically the "multiple choice selection" contruct
            "What does this mean? "+ thelistoflanguages[st.session_state.questionlist[4]][int(lm)], # This is the question parameter, takes in a string
            st.session_state.Options,
            key ='rdkey5',
            index = 0,
        )
        if (st.button('Submit', on_click = callback, disabled = st.session_state.QuizEndActivated) or st.session_state.QuizEndActivated):
            if not st.session_state.QuizEndActivated:
                st.session_state.QuizEndActivated = True
                st.rerun()
            
            if multiplechoice1 == thelistoflanguages[st.session_state.questionlist[0]][0]:
                st.session_state.correctcounter += 1
                st.session_state.playerxp += 15
            else:
                st.session_state.wrongquestionlist.append(st.session_state.questionlist[0])
                
            if multiplechoice2 == thelistoflanguages[st.session_state.questionlist[1]][0]:
                st.session_state.correctcounter += 1
                st.session_state.playerxp += 15
            else:
                st.session_state.wrongquestionlist.append(st.session_state.questionlist[1])

            if multiplechoice3 == thelistoflanguages[st.session_state.questionlist[2]][0]:
                st.session_state.correctcounter += 1
                st.session_state.playerxp += 15
            else:
                st.session_state.wrongquestionlist.append(st.session_state.questionlist[2])

            if multiplechoice4 == thelistoflanguages[st.session_state.questionlist[3]][0]:
                st.session_state.correctcounter += 1
                st.session_state.playerxp += 15
            else:
                st.session_state.wrongquestionlist.append(st.session_state.questionlist[3])

            if multiplechoice5 == thelistoflanguages[st.session_state.questionlist[4]][0]:
                st.session_state.correctcounter += 1
                st.session_state.playerxp += 15
            else:
                st.session_state.wrongquestionlist.append(st.session_state.questionlist[4])

            choiceContainer1.empty()
            choiceContainer2.empty()
            choiceContainer3.empty()
            choiceContainer4.empty()
            choiceContainer5.empty()

            st.write("You scored " + str(st.session_state.correctcounter) + "/5 and currently have " + str(st.session_state.playerxp) + "XP in total")
            st.write("You got these questions wrong")
            for wrongqnsindex in st.session_state.wrongquestionlist:
                st.write(thelistoflanguages[wrongqnsindex][int(lm)] + " = " + thelistoflanguages[wrongqnsindex][0])
            if st.session_state.correctcounter == 5:
                st.balloons()

            if st.button("Restart"):
                st.session_state.ButtonActivated = False
                st.session_state.QuizStartActivated = False
                st.session_state.QuizEndActivated = False

                st.session_state.Options = []
                st.session_state.questionlist = []
                st.session_state.bt_clkd = ""
                st.session_state.correctcounter = 0
                st.session_state.wrongcounter = 0
                st.rerun()
