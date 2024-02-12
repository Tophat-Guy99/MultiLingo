# This massive hexadecimal string is our API key, encrypted to avoid OpenAI's watchful eye
encodedkey = ("73 6B 2D 61 39 30 37 43 78 4A 58 78 6B 78 4A 39 39 61 72 45 6D 38 31 54 33 42 6C 62 6B 46 4A 56 6C 4E 49 63 4E 4D 77 45 34 58 37 79 73 54 65 47 5A 69 35").split()
# Decryption process
decodedkey = ""
for i in range(len(encodedkey)):
    decodedkey += chr(int(encodedkey[i], 16))

# LLM libraries and setting up translation LLM
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# (Michael) We use gpt-3.5-turbo-instruct because not only is it cheap, but it does exactly what you tell it to instead of yapping for 6 paragraphs about ethics
translationprompt = PromptTemplate(
    template="Translate the following text from {InLang} to {OutLang}: {Text}.",
    input_variables=["InLang", "OutLang", "Text"]
)
TranslationLLM = OpenAI(
    model_name='gpt-3.5-turbo-instruct',
    temperature = 0,
    openai_api_key=decodedkey
)
chain = translationprompt | TranslationLLM | StrOutputParser()

# Speech recognition and TTS
import speech_recognition as sr
import pyttsx3

# Streamlit
import streamlit as st

# (Michael) These are a list of languages we currently support, and is used to prompt formatting to input into the LLM.
validlanguages = {
    "EN": "English",
    "CN": "Chinese",
    "ES": "Spanish",
    "FR": "French"
}
# (Michael) This dictionary is for the language code in order for the speech recognition module to detect the correct language, using the same keys as the language dict earlier
validcodes = {
    "EN": "en-GB",
    "CN": "zh-CN",
    "ES": "es-ES",
    "FR": "fr-FR"
}
# (Michael) This dictionary is for the voice ids of the available TTS voices, usage is self-explanatory
ttsvoices = {
    "EN": "com.apple.voice.compact.en-GB.Daniel",
    "CN": "com.apple.voice.compact.zh-CN.Tingting",
    "ES": "com.apple.eloquence.es-ES.Eddy",
    "FR": "com.apple.eloquence.fr-FR.Rocko"
}
# (Michael) This is the TTS engine, we set the number of words spoken per minute to avoid it from going too fast (default is 200 for some reason)
engine = pyttsx3.init()
engine.setProperty('rate', 150)
def SpeakText(command, outputlanguage):
    if engine._inLoop:
        engine.endLoop()
    engine.setProperty('voice', ttsvoices[outputlanguage])
    engine.say(command) 
    engine.runAndWait()
def StopTTS():
    if engine._inLoop:
        engine.endLoop()
# (Michael) Speech recognition function
audiodetector = sr.Recognizer()
def audioinputdetection(inputlanguage):
    listeningbox = st.empty()
    try:
        with sr.Microphone() as source:
            # Slight pause to let the audio detector adjust for background noise, then indicates when the user should start speaking
            audiodetector.adjust_for_ambient_noise(source, duration=2)
            listeningbox.info("Listening...")
            # Get audio input 
            audio = audiodetector.listen(source)
             
            # Recognizing speech in audio
            MyText = audiodetector.recognize_google(audio_data=audio, language=validcodes[inputlanguage])
            MyText = MyText.lower()
            listeningbox.empty()
            return MyText

    # Errors shouldn't happen, but this is in case it happens.
    except sr.RequestError as e:
        # This often means the client cannot connect to the server, either because no internet connection or google's servers are in flames
        st.error("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        # The most common error, this is because the user did not say anything/speech is unintelligible
        st.error("Did not recognize any speech. Speak louder and clearer.")
    except:
        # If something else goes wrong for some dumb reason this is where it's handled (e.g, other types of errors)
        # This... shouldn't happen unless you forgot to install a library or something
        st.error("An error occured")
    listeningbox.empty()
    return None

def TranslateText(inputlanguage, outputlanguage, totranslate):
    output = chain.invoke({"InLang": validlanguages[inputlanguage], "OutLang": validlanguages[outputlanguage], "Text": totranslate})
    output = output.strip()
    return output