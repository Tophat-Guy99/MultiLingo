while True:
    print('Choose Between Option 1 or 2 \n1. Translate Mode \n2. Learning Mode')
    mode = input('Option: ')
    if not mode.isdigit():
        print('Please check the input.')
    elif not int(mode) == 1 and not int(mode) == 2:
        print('Please choose between 1 or 2.')
    else:
        break

if int(mode) == 1: 
    while True:
        print('Choose between option 1 2 3 or 4 (Translate Mode)\n1. English \n2. French \n3. Chinese \n4. Spanish')
        tm = input('Option: ')
        if not tm.isdigit():
            print('Please check the input.')
        elif not int(tm) == 1 and not int(tm) == 2 and not int(tm) == 3 and not int(tm) == 4:
            print('Please choose between 1 or 2 or 3 or 4.')
        else:
            break
else:
    while True:
        print('Choose between option 1 2 or 3 (Learner Mode)\n1. French \n2. Chinese \n3. Spanish')
        lm = input('Option: ')
        if not lm.isdigit():
            print('Please check the input.')
        elif not int(lm) == 1 and not int(lm) == 2 and not int(lm) == 3:
            print('Please choose between 1 or 2 or 3 or 4.')
        else:
            break
