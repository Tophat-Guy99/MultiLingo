import TranslationFunctions # (Michael) Our original coursework was going to be written into what is now TranslationFunctions.py, but for the ease of readability and organisation, the frontend has been coded in a separate file, and the original Coursework file has been reduced to imported modules and functions, which will be called from this file.
# (Michael) Our original input scheme prompted the user to enter "EN", "CN", "FR", "ES" as a short string for ease of input. Since migrating to Streamlit made that design choice redundant, I have created a dictionary to convert the new selection box inputs into the old "language codes" for backwards compatibility with TranslationFunctions.py
codeconversion = {
    'English 🇬🇧': "EN",
    'Chinese 🇨🇳': "CN",
    'French 🇫🇷': "FR",
    'Spanish 🇪🇸': "ES"
}

# (Yi Kai) Import Streamlit and creating titles for UI
import streamlit as st
st.set_page_config(
    page_title = "MultiLingo",
    page_icon = "🗣️",
)

st.sidebar.header("Translate Mode") 
st.sidebar.write("Translate from language to language.")
st.title("MultiLingo")
st.write("Breaking the barriers for language.") 

# (Michael) Session state variable to prevent further interaction with the "text translate
if 'texttranslationrunning' not in st.session_state:
    st.session_state.texttranslationrunning = False
if 'texttranslatebutton' in st.session_state and st.session_state.texttranslatebutton == True: 
    st.session_state.texttranslationrunning = True 
else:
    st.session_state.texttranslationrunning = False

# (Yi Kai) Selections for input and output language
trf = st.selectbox('Translate From',
                         ('English 🇬🇧', 'Chinese 🇨🇳', 'French 🇫🇷', 'Spanish 🇪🇸'), placeholder="Choose a language")

trt = st.selectbox('Translate To',
                         ('English 🇬🇧', 'Chinese 🇨🇳', 'French 🇫🇷', 'Spanish 🇪🇸'), placeholder="Choose a language", index=1)
if trf == trt:
    # (Yi kai) Input validation, advise user to make input and output language different
    TranslationFunctions.StopTTS()
    st.error("Input and output languages cannot be the same. Please pick different languages.")
else:
    # (Yi Kai) Move on to next stage, pick either text or speech recognition
    TranslationFunctions.StopTTS()
    sot = st.selectbox('Input text to translate or use speech recognition?',
                         ('Text 💬', 'Speech 🗣'))

    if sot == 'Text 💬':
        # (Yi Kai) Create another button to prompt user to enter text and a button to start translating
        multitext = st.text_area("Text to Translate",
                         placeholder="Enter some text")
        
        texttranslate = st.button("Translate", disabled=st.session_state.texttranslationrunning, key="texttranslatebutton")
        # (Yi Kai) Input validation, ensure that there is no leading or trailing space chars and that the text field is not blank
        if texttranslate and multitext and not multitext.isspace():
            multitext.strip()
            with st.spinner("Translating..."):
                # (Yi Kai) calls function from TranslationFunctions.py to translate the text
                translatedoutput = TranslationFunctions.TranslateText(codeconversion[trf], codeconversion[trt], multitext)
            st.divider()
            # (Yi Kai) formatting output and calls another function to use TTS
            st.markdown("Translated output" + "\: " + f":green[{translatedoutput}]")
            st.toast("Translation successful!")
            TranslationFunctions.SpeakText(translatedoutput, codeconversion[trt])
        elif texttranslate:
            # (Yi Kai) Blank textfield handling
            with st.spinner("Speaking..."):
                st.error("Text input cannot be blank, please enter some text.")
    else:
        # Speech recognition button
        if st.button('Click me and start speaking'):

            with st.spinner("Starting speech recognition, please speak when the blue box appears."):
                # (Yi Kai) Calls function to start speech recognition detector
                TextDetected = TranslationFunctions.audioinputdetection(codeconversion[trf])
            # (Yi Kai) Validation, if no speech detected, handle error
            # If speech detected, calls a function to translate the text and format output
            if TextDetected != None:
                with st.spinner("Translating..."):
                    translatedoutput = TranslationFunctions.TranslateText(codeconversion[trf], codeconversion[trt], TextDetected)
                st.divider()
                st.markdown("Translated output" + "\: " + f":green[{translatedoutput}]")
                st.toast("Translation successful!")
                TranslationFunctions.SpeakText(translatedoutput, codeconversion[trt])
