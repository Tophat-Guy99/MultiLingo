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

# Other modules
import random
import string
import time

# (Yi Kai/Axel) This list of languages is used for Learner Mode
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

correctansXP = 10
rawcorrectansXP = 5 # (Axel) no punctuation but correct

def remove_punctuation(input_str):
    translator = str.maketrans("", "", string.punctuation)
    rawtextwithspace = input_str.translate(translator)

    return rawtextwithspace

def remove_alphabet(input_str):
    translator = str.maketrans("", "", string.ascii_letters + string.digits)
    rawpunctuationwithspace = input_str.translate(translator)

    return rawpunctuationwithspace


# (Michael) This is the TTS engine, we set the number of words spoken per minute to avoid it from going too fast (default is 200 for some reason)
engine = pyttsx3.init()
engine.setProperty('rate', 150)
def SpeakText(command, outputvoice):
    engine.setProperty('voice', outputvoice)
    engine.say(command) 
    engine.runAndWait()

# (Michael) Speech recognition function
audiodetector = sr.Recognizer()
def audioinputdetection(inputlanguage):
    for i in range(3):
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source:
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                audiodetector.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...\n")
                #listens for the user's input 
                audio = audiodetector.listen(source)
             
                # Using google to recognize audio
                MyText = audiodetector.recognize_google(audio_data=audio, language=validcodes[inputlanguage])
                MyText = MyText.lower()
                return MyText

        # Errors shouldn't happen, but this is in case it happens.
        except sr.RequestError as e:
            # This often means the client cannot connect to the server, either because no internet connection or google's servers are in flames
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            # The most common error, this is because the user did not say anything/speech is unintelligible
            print("Did not recognize any speech. Speak louder and clearer.")
        except:
            # If something else goes wrong for some dumb reason this is where it's handled (e.g, other types of errors)
            # This... shouldn't happen unless you forgot to install a library or something
            print("Some other error occured")
    return None

def translationloop():
    # This first boolean value
    languagesselected = False
    while True:
        while True:
            # Validation (input lang)
            if languagesselected == True:
                break
            print('\nChoose a language for translation input:\nEN: English \nFR: French \nCN: Chinese \nES: Spanish')
            inputlanguage = (input('Option: ')).upper()
            if dict.get(validlanguages, inputlanguage) != None:
                break
            else:
                print("\nThis language is not supported, please select another language.\n")
            time.sleep(1.5)
        while True:
            if languagesselected == True:
                break
            #Validation (output lang)
            print('\nChoose a language for translation output:\nEN: English \nFR: French \nCN: Chinese \nES: Spanish')
            outputlanguage = (input('Option: ')).upper()
            if inputlanguage == outputlanguage:
                print("\nInput and output languages cannot be the same!\n")
            elif dict.get(validlanguages, outputlanguage) != None:
                break
            else:
                print("\nThis language is not supported, please select another language.\n")
            time.sleep(1.5)
        while True:
            print("\n Enter text or use speech recognition? \n1: Text\n2: Speech")
            choice = input('Option: ')
            if choice == "1":
                totranslate = input("\nInput what you want to translate from " + validlanguages[inputlanguage] + " to " + validlanguages[outputlanguage] + ": ")
                break
            elif choice == "2":
                while True:
                    print("\nSpeak into your microphone what you want to translate from " + validlanguages[inputlanguage] + " to " + validlanguages[outputlanguage] + ".\n")
                    totranslate = audioinputdetection(inputlanguage)
                    if totranslate == None:
                        print("\nSpeech recognition failed.")
                        time.sleep(1.5)
                        while True:
                            print("Would you like to try again or enter text?\n1: Try again\n2: Enter text\n")
                            failchoice = input('Option: ')
                            if failchoice == "1" or failchoice == "2":
                                break
                            else:
                                print("Invalid input. Please enter either 1 or 2.")
                            time.sleep(1.5)
                        # Repeats the process
                        if failchoice == "1":
                            continue
                        else:
                        # If they chose to input text instead of trying again
                            totranslate = input("\nInput what you want to translate from " + validlanguages[inputlanguage] + " to " + validlanguages[outputlanguage] + ": ")
                            break
                    else:
                        break
                break
            else:
                print("Invalid input. Please enter either 1 or 2.")
            time.sleep(1.5)
        output = chain.invoke({"InLang": validlanguages[inputlanguage], "OutLang": validlanguages[outputlanguage], "Text": totranslate})
        output = output.strip()
        print("Result: " + output)
        SpeakText(output, ttsvoices[outputlanguage])
        time.sleep(1.5)
        print("\n What would you like to do?\n1: Do another translation from {} to {}.\n2: Do another translation with different languages.\n3: Exit translation mode.".format(validlanguages[inputlanguage],validlanguages[outputlanguage]))
        while True:
            savelanguagechoice = input("Option: ").upper()
            if savelanguagechoice == "1" or savelanguagechoice == "2" or savelanguagechoice == "3":
                break
            print("Invalid input. Please enter 1, 2, or 3.")
            time.sleep(0.5)
        if savelanguagechoice == "1":
            languagesselected = True
        elif savelanguagechoice == "2":
            languagesselected = False
        else:
            break


        

while True: # choosing mode + validation checks
    print('Choose Between Option 1 or 2 \n1. Translate Mode \n2. Learning Mode')
    mode = input('Option: ')
    if not mode.isdigit():
        print('Please check the input.')
    elif not int(mode) == 1 and not int(mode) == 2:
        print('Please choose between 1 or 2.')
    else:
        break

if int(mode) == 1: # translate mode + validation checks
    translationloop()
else: # learning/quiz mode + validation checks
    
    while True:
        print('Choose between option 1 2 or 3 (Learner Mode)\n1. French \n2. Chinese \n3. Spanish')
        lm = input('Option: ')
        
        if not lm.isdigit():
            print('Please check the input.')
            
        elif not int(lm) == 1 and not int(lm) == 2 and not int(lm) == 3:
            print('Please choose between 1 or 2 or 3.')
            
        else:
            break
        
    print('MichaelBot: Hi I am Michael Bot and I will be facilitating your learning session today.')
    print(" ")
    
    templist = thelistoflanguages.copy()
    playerxp = 0
    correctcounter = 0
    partiallycorrectcounter = 0
    wrongcounter = 0
    
    for i in range(len(templist)):
        questionindex = random.randint(0, len(templist) - 1)
        print("Michael Bot: Translate this, " + templist[questionindex][int(lm)])
        ans = input("Your Answer: ")
        
        if ans.lower() == templist[questionindex][0]:
            
            playerxp += correctansXP
            correctcounter += 1
            
            print("You got it right! +" + str(correctansXP) + "XP" )
            
        elif ans.lower() == remove_punctuation(templist[questionindex][0]):
            
            playerxp += rawcorrectansXP
            partiallycorrectcounter += 1
            
            print("----------------------------------------\nasdDon't forget your punctuation +" + str(rawcorrectansXP) + "XP")
            print(" ")
            print("The correct answer is " + templist[questionindex][0])

            
        elif remove_punctuation(ans.lower()) == remove_punctuation(templist[questionindex][0]) and remove_alphabet(ans) != remove_alphabet(templist[questionindex][0]): # Ex. "??" != "??" because i remove the alphabets i leave only the punctuation in order, its placement does not matter
            wrongcounter += 1

            print("----------------------------------------\nCheck your punctuation!")
            print(" ")
            print("The correct answer is " + templist[questionindex][0])
            
        else:
            wrongcounter += 1
            
            print("----------------------------------------\nYou got it wrong!")
            print(" ")
            print("The correct answer is " + templist[questionindex][0])
            
        print(" ")
        print(" ") 
        templist.remove(templist[questionindex])
    print("Thank you for playing, you got " + str(correctcounter) + " question(s) correct, " + str(partiallycorrectcounter) + " question(s) partially correct and " + str(wrongcounter) + " question(s) wrong.")
    print("Your total XP gained is: " + str(playerxp))
