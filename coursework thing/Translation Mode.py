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

if 'texttranslationrunning' not in st.session_state:
    st.session_state.texttranslationrunning = False
if 'texttranslatebutton' in st.session_state and st.session_state.texttranslatebutton == True: # these are session state things, treat them as variables that update in real time with button click
    st.session_state.texttranslationrunning = True # They will be used for the following slowbutton to prevent input while the function is running
else:
    st.session_state.texttranslationrunning = False

trf = st.selectbox('Translate From',
                         ('English 🇬🇧', 'Chinese 🇨🇳', 'French 🇫🇷', 'Spanish 🇪🇸'), placeholder="Choose a language")

trt = st.selectbox('Translate To',
                         ('English 🇬🇧', 'Chinese 🇨🇳', 'French 🇫🇷', 'Spanish 🇪🇸'), placeholder="Choose a language", index=1)
if trf == trt:
    TranslationFunctions.StopTTS()
    st.error("Input and output languages cannot be the same. Please pick different languages.")
else:
    TranslationFunctions.StopTTS()
    sot = st.selectbox('Input text to translate or use speech recognition?',
                         ('Text 💬', 'Speech 🗣'))

    if sot == 'Text 💬':
        multitext = st.text_area("Text to Translate",
                         placeholder="Enter some text")
        # If text button is chosen
        texttranslate = st.button("Translate", disabled=st.session_state.texttranslationrunning, key="texttranslatebutton")
        if texttranslate and multitext and not multitext.isspace():
            multitext.strip()
            with st.spinner("Translating..."):
                translatedoutput = TranslationFunctions.TranslateText(codeconversion[trf], codeconversion[trt], multitext)
            st.divider()
            st.markdown("Translated output" + "\: " + f":green[{translatedoutput}]")
            st.toast("Translation successful!")
            TranslationFunctions.SpeakText(translatedoutput, codeconversion[trt])
        elif texttranslate:
            with st.spinner("Speaking..."):
                st.error("Text input cannot be blank, please enter some text.")
    else:
        if st.button('Click me and start speaking'):
            with st.spinner("Starting speech recognition..."):
                TextDetected = TranslationFunctions.audioinputdetection(codeconversion[trf])
            if TextDetected != None:
                with st.spinner("Translating..."):
                    translatedoutput = TranslationFunctions.TranslateText(codeconversion[trf], codeconversion[trt], TextDetected)
                st.divider()
                st.markdown("Translated output" + "\: " + f":green[{translatedoutput}]")
                st.toast("Translation successful!")
                TranslationFunctions.SpeakText(translatedoutput, codeconversion[trt])
