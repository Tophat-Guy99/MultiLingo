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

import random
import string

correctansXP = 10
rawcorrectansXP = 5 # no punctuation but correct

def remove_punctuation(input_str):
    translator = str.maketrans("", "", string.punctuation)
    rawtextwithspace = input_str.translate(translator)

    return rawtextwithspace

def remove_alphabet(input_str):
    translator = str.maketrans("", "", string.ascii_letters + string.digits)
    rawpunctuationwithspace = input_str.translate(translator)

    return rawpunctuationwithspace

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
    while True:
        print('Choose between option 1 2 3 or 4 (Translate Mode)\n1. English \n2. French \n3. Chinese \n4. Spanish')
        tm = input('Option: ')
        if not tm.isdigit():
            print('Please check the input.')
        elif not int(tm) == 1 and not int(tm) == 2 and not int(tm) == 3 and not int(tm) == 4:
            print('Please choose between 1 or 2 or 3 or 4.')
        else:
            break
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
            
            print("Don't forget your punctuation +" + str(rawcorrectansXP) + "XP")
            print(" ")
            print("The correct answer is " + templist[questionindex][0])

            
        elif remove_punctuation(ans.lower()) == remove_punctuation(templist[questionindex][0]) and remove_alphabet(ans) != remove_alphabet(templist[questionindex][0]): # Ex. "??" != "??" because i remove the alphabets i leave only the punctuation in order, its placement does not matter
            wrongcounter += 1

            print("Check your punctuation!")
            print(" ")
            print("The correct answer is " + templist[questionindex][0])
            
        else:
            wrongcounter += 1
            
            print("You got it wrong!")
            print(" ")
            print("The correct answer is " + templist[questionindex][0])
            
        print(" ")
        print(" ") 
        templist.remove(templist[questionindex])
    print("Thank you for playing, you got " + str(correctcounter) + " question(s) correct, " + str(partiallycorrectcounter) + " question(s) partially correct and " + str(wrongcounter) + " question(s) wrong.")
    print("Your total XP gained is: " + str(playerxp))
        

        
