import streamlit as st
import random

thelistoflanguages = [ # list of translated and non-translated words
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
languagenumberreference = { # list of choices of language to test on (except english)
    "English": 0,
    'French 🇫🇷': 1,
    'Chinese 🇨🇳': 2,
    'Spanish 🇪🇸': 3
}

st.set_page_config( # Tab icon and title
    page_title = "MultiLingo",
    page_icon = "🗣️",
)

if "ButtonActivated" not in st.session_state: # Initialization of values, we only check for one since none of the other variables need to be preserved for next run, this preserves the variables from the last run everytime you press Restart
    st.session_state.ButtonActivated = False
    st.session_state.QuizStartActivated = False
    st.session_state.QuizEndActivated = False
    st.session_state.counter = 0

    st.session_state.Options = []
    st.session_state.containers = []
    st.session_state.questionlist = []
    st.session_state.correctcounter = 0
    st.session_state.wrongquestionlist = []

# Text things
st.sidebar.header("Learner Mode") 
st.sidebar.write("Learn The Language.")
st.title("Learner Mode")
st.write("Learn The Language!") 

# Selection box
lf = st.selectbox('What language do you want to learn today?',
                         ('French 🇫🇷', 'Chinese 🇨🇳', 'Spanish 🇪🇸'), disabled=st.session_state.ButtonActivated)
lm = languagenumberreference[lf] # Variable on what language you have

if (st.button("Start Learning", disabled = st.session_state.ButtonActivated) or st.session_state.ButtonActivated):

    if not st.session_state.ButtonActivated:
        st.session_state.ButtonActivated = True

        # Generates a bunch of indexes to be used on thelistoflanguages to determine which will be questions + answers
        samplerange = list(range(0, len(thelistoflanguages)))
        st.session_state.questionlist = random.sample(samplerange, 5)

        # Gives list of translated and non-translated text for your revision
        for i in range(5):
            st.write(thelistoflanguages[st.session_state.questionlist[i]][int(lm)] + ": " + thelistoflanguages[st.session_state.questionlist[i]][0])
        st.info("To hide the phrases to start memorising, click on the 'Start Learning' button again. To begin the quiz, click on the 'Start Quiz' button.")
        


    if (st.button("Start Quiz", disabled = st.session_state.QuizStartActivated) or st.session_state.QuizStartActivated):
        
        if not st.session_state.QuizStartActivated:
            st.session_state.QuizStartActivated = True

            # Shuffles list of indexes aka questionlist and makes sure the indexes are randomised so that the correct choices are not in the same order everytime you run it
            random.shuffle(st.session_state.questionlist)

            for qnsIndex in st.session_state.questionlist: # Puts the english options as string inside the options list
                st.session_state.Options.append(thelistoflanguages[qnsIndex][0])
            
            random.shuffle(st.session_state.Options) # shuffling options to make sure the strings are randomised so that the correct choices are not in the same order everytime you run it
            st.rerun() # used so the button disables since streamlit re-runs the code everytime you press the button and some values arent updated yet on click such as when disabling the button you usually need to click twice
            
        if not st.session_state.QuizEndActivated:
            for num in range(5):
                choiceContainer = st.empty() # placeholder container so we can hide it later

                multiplechoice = choiceContainer.radio( # This is basically the "multiple choice selection" contruct
                    "What does this mean? "+ thelistoflanguages[st.session_state.questionlist[num]][int(lm)], # This is the question parameter, takes in a string
                    st.session_state.Options,
                    key='rdkey' + str(num), # Unique identifier so we can check the answer later on
                    index = 0,
            )
            
            st.session_state.containers.append(choiceContainer)

        if (st.button('Submit', disabled = st.session_state.QuizEndActivated) or st.session_state.QuizEndActivated):
            if not st.session_state.QuizEndActivated:
                st.session_state.QuizEndActivated = True
                
                for num in range(5):
                    if  st.session_state["rdkey" + str(num)] == thelistoflanguages[st.session_state.questionlist[num]][0]: # Checks answers if their correct
                        st.session_state.correctcounter += 1 # Counts correct answers
                    else:
                        st.session_state.wrongquestionlist.append(st.session_state.questionlist[num]) # Add wrong answers' indexes to a table to be used on thelistoflanguages
                    num += 1

                for container in st.session_state.containers:
                    container.empty() # Hide all the mcq questions
                st.rerun() # Used so the button disables since streamlit re-runs the code everytime you press the button and some values arent updated yet on click such as when disabling the button you usually need to click twice

            st.write("You scored " + str(st.session_state.correctcounter) + "/5")

            if not st.session_state.correctcounter == 5: # Checks if you got at least 1 question wrong and shows you
                st.write("You got these questions wrong:")

                for wrongqnsindex in st.session_state.wrongquestionlist: # Shows which ones you got wrong + translation
                    st.write(thelistoflanguages[wrongqnsindex][int(lm)] + " = " + thelistoflanguages[wrongqnsindex][0])

            if st.session_state.correctcounter == 5: # Fun Balloons to celebrate your full marks
                st.balloons()

            if st.button("Restart"): # Resetting all the variables
                st.session_state.ButtonActivated = False
                st.session_state.QuizStartActivated = False
                st.session_state.QuizEndActivated = False

                st.session_state.containers = []
                st.session_state.Options = []
                st.session_state.questionlist = []
                st.session_state.correctcounter = 0
                st.session_state.wrongquestionlist = []
                st.rerun() # Restarts everything

# Made by Axel Tee Yu Le S408 07
