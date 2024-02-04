import warnings
warnings.filterwarnings('ignore')

import os
from dotenv import load_dotenv

# load OPENAI API key
# Beg Ms Tang for funding because I'm not trusting the RP tokens to last for 3 months minimum
# Oh yeah and we also need to create an env.txt file to put the token inside, don't do it in the repo itself or the OpenAI overlords will deactivate the token
load_dotenv('env.txt')
openai_api_key = os.getenv('OPENAI_API_KEY')

# load langchain libraries
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate

# Speech recognition and tts libraries

import speech_recognition as sr
import pyttsx3

# initialise ChatModel with API key
translationprompt = PromptTemplate(
    template="Translate the following text from {InLang} to {OutLang}: {Text}",
    input_variables=["InLang", "OutLang", "Text"]
)

TranslationLLM = OpenAI(
    model_name='gpt-3.5-turbo-instruct',
    temperature = 0,
    openai_api_key=openai_api_key
)

# These are some languages we so far support, perfect for Chinese tourists travelling to Europe?
validlanguages = {
    "EL": "English",
    "CN": "Chinese",
    "ES": "Spanish",
    "FR": "French"
}

inputlanguage = ""
outputlanguage = ""

# This is to test the LLM, using only textual input/output.
# It's inside a function because I'm currently testing speech recog and tts (haha while loop sisyphus happy get it????)
# This can probably be modified so that it purely translates without needing to validate input (assuming we can make a dropdown UI thingy)
def sisyphus():
    while True:
        while True:
            # Validation (input lang)
            print("""Choose a language for translation input:
              - EL ~ English
              - CN ~ Chinese
              - ES ~ Spanish
              - FR ~ French
              """)
            inputlanguage = input()
            if dict.get(validlanguages, inputlanguage) != None:
                break
            else:
                print("This language is not supported, please select another language.")
        while True:
            #Validation (output lang)
            print("""Choose a language for translation output:
              - EL ~ English
              - CN ~ Chinese
              - ES ~ Spanish
              - FR ~ French
              """)
            outputlanguage = input()
            if inputlanguage == outputlanguage:
                print("Input and output languages cannot be the same!")
            elif dict.get(validlanguages, outputlanguage) != None:
                break
            else:
                print("This language is not supported, please select another language.")

        # Now this is where the magic stuff hapens
        totranslate = input("Input what you want to translate from " + validlanguages[inputlanguage] + " to " + validlanguages[outputlanguage] + ": ")
        #output = chat_model(chat_prompt.format_messages(
            #input_language = validlanguages[inputlanguage],
            #output_language = validlanguages[outputlanguage],
            #text = totranslate
        #)).content
        # And this is the output.
        #print(output)
        output = TranslationLLM(translationprompt.format(
            InLang=validlanguages[inputlanguage],
            OutLang=validlanguages[outputlanguage],
            Text=totranslate
        ))
        print(output)

# Okay now this is where the fun tts stuff begins

# This recognizes speech
r = sr.Recognizer()
def SpeakText(command):
    # This is the TTS command, best to avoid touching it
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
# Loop infinitely for user to speak
# This is not the final structure, later we integrate this into a front-end ui and wrap it inside a function so it fires once

while(1):
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            #listens for the user's input 
            audio = r.listen(source)
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio_data=audio, language="en-EN")
            MyText = MyText.lower()
 
            print("Did you say ",MyText)
            SpeakText(MyText)

    # Errors shouldn't happen, but this is in case it happens.
    # Comment out the print statements before we finalize so it looks perfect and we can blame the user for speaking wrong if something unexpected happens.
    except sr.RequestError as e:
        # One potential error to handle
        # I don't know what the this is supposed to mean, should probably ask a group who's also using SR like Luke's group
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        # Another potential error to handle
        # The most common cause of this is because the user did not say anything/speech is unintelligible
        print("Did not recognize any speech. Speak louder and clearer.")

    except:
        # If something else goes wrong for some dumb reason this is where it's handled
        # This... shouldn't happen unless you forgot to install a library or something but y'know
        print("Some other error occured")
