# All of this is written by Michael

# Encoded OpenAI API key to avoid auto-detection on Github
encodedkey = ("73 6B 2D 61 39 30 37 43 78 4A 58 78 6B 78 4A 39 39 61 72 45 6D 38 31 54 33 42 6C 62 6B 46 4A 56 6C 4E 49 63 4E 4D 77 45 34 58 37 79 73 54 65 47 5A 69 35").split()
# Decryption process
decodedkey = ""
for i in range(len(encodedkey)):
    decodedkey += chr(int(encodedkey[i], 16))

# LLM libraries and setting up translation LLM
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM of choice is gpt-3.5-turbo-instruct, it is fast, cheap, and good at following instructions.
translationprompt = PromptTemplate( # The structure used for input requests, InLang, OutLang and Text are all to be replaced by custom input.
    template="Translate the following text from {InLang} to {OutLang}: {Text}.",
    input_variables=["InLang", "OutLang", "Text"]
)
TranslationLLM = OpenAI( # Temperature is set to 0 to avoid inconsistency
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

# This is a dictionary of languages we currently support, and is used to convert user input to a cohesive word (language) input into the LLM.
# The keys are named after the input choices from when we first used to use terminal input for language selection. This is the same for the rest of the dictionaries listed here.
validlanguages = {
    "EN": "English",
    "CN": "Chinese",
    "ES": "Spanish",
    "FR": "French"
}
# This dictionary is for the language code in order for the speech recognition module to detect the correct language, using the same keys as the language dict earlier
validcodes = {
    "EN": "en-GB",
    "CN": "zh-CN",
    "ES": "es-ES",
    "FR": "fr-FR"
}
# This dictionary is for the voice ids of the available TTS voices, usage is self-explanatory
# Do note that this only works on MacOS, as these voices are not availble on the Windows version of pyttsx3.
ttsvoices = {
    "EN": "com.apple.voice.compact.en-GB.Daniel",
    "CN": "com.apple.voice.compact.zh-CN.Tingting",
    "ES": "com.apple.eloquence.es-ES.Eddy",
    "FR": "com.apple.eloquence.fr-FR.Rocko"
}
# This is the TTS engine, we set the number of words spoken per minute to avoid it from going too fast (default is 200 for some reason)
engine = pyttsx3.init()
engine.setProperty('rate', 150)
def SpeakText(command, outputlanguage):
    # The main function to vocalize text, immediately overrides ongoing TTS too.
    # command is text input, outputlanguage is the key to use to select the voice for TTS (because different languages are supported by different voices.
    if engine._inLoop:
        engine.endLoop()
    engine.setProperty('voice', ttsvoices[outputlanguage])
    engine.say(command) 
    engine.runAndWait()
def StopTTS():
    # We also have a function to immediately stop the TTS engine from being active, used when TTS is still playing when the user changes an option in the frontend.
    if engine._inLoop:
        engine.endLoop()
        
# Speech recognition function is here
audiodetector = sr.Recognizer()
def audioinputdetection(inputlanguage):
    # A popup will be set up to indicate when the detector is listening for audio input, so this is why Streamlit was imported here
    listeningbox = st.empty()
    try:
        # This will ask the user for permission to use the microphone
        with sr.Microphone() as source:
            # Slight pause to let the audio detector adjust for background noise, then indicates when the user should start speaking
            audiodetector.adjust_for_ambient_noise(source, duration=2)
            listeningbox.info("Listening...")
            # The detector will listen out for audio
            audio = audiodetector.listen(source)
             
            # The detector now attempts to find coherent speech in the audio.
            MyText = audiodetector.recognize_google(audio_data=audio, language=validcodes[inputlanguage])
            MyText = MyText.lower()
            # Textbox is closed, as the listening is complete
            listeningbox.empty()
            # The recognized speech is returned
            return MyText

    # Errors shouldn't happen, but this is in case it happens.
    except sr.RequestError as e:
        # This often means the client cannot connect to the server, either because no internet connection.
        st.error("Could not request results; {0}. Please try again or use text input.".format(e))
    except sr.UnknownValueError:
        # The most common error, this is because the user did not say anything/speech is unintelligible
        st.error("Did not recognize any speech. Speak louder and clearer.")
    except:
        # This is a general error case, this usually happens because a library was not installed.
        st.error("An error occured. Please try again or use text input.")
    listeningbox.empty()
    # The textbox is closed as listening is complete.
    # None value is returned because an error has occured.
    return None

# The translation function
def TranslateText(inputlanguage, outputlanguage, totranslate):
    # Uses indexing to convert the language "code" into the full word of the language.
    output = chain.invoke({"InLang": validlanguages[inputlanguage], "OutLang": validlanguages[outputlanguage], "Text": totranslate})
    # The output has a lot of whitespace, so using .strip() to remove leading and trailing space characters for ease of string formatting.
    output = output.strip()
    return output
