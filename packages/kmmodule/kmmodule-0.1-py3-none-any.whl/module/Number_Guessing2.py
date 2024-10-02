"""Number guessing 2"""
def Num_guessing(self,play):
    self=play
    def MainC():
        while True:
            try:
                print("\nNumber Guessing")
                print("------------")
                print("Select Your Difficulty")
                print("Easy")
                print("Medium")
                print("Hard")
                print("Extreme")
                selection=str(input("Select your Difficulty ")).lower()
                if(selection==("easy")):
                    Easy()
                elif(selection==("medium")):
                    Medium()
                elif(selection==("hard")):
                    Hard()
                elif(selection==("extreme")):
                    Extreme()
                else:
                    print("\nInvalid selection.")
                    exit()
            except ValueError:
                print("\nERROR: Invalid")
                exit()
    def Easy():
        """Easy"""
        print("\nDifficulty : EASY")
        print("I'm thinking of a number from 1-10. What's the number? ")
        for i in range(0,3):
            guess1=int(input("Your Answer= "))
            if(guess1==(7)):
                print("\nCorrect answer✅") 
                prompt=str(input("Playagain (Y/N) ")).lower()
                if(prompt==("y")):
                    playagain(main=MainC())
                else:
                    print("\nThanks for playing.")
                    exit()
            elif(guess1>10):
                print("\n\nYou've Guessed above\nthe number given.Try again.")
                Easy()
            else:
                print("Wrong Answer❌")
        print("\nOops, you have 3 wrong guesses.")
        prompt=str(input("Playagain (Y/N) ")).lower()
        if(prompt==("y")):
            playagain(main=MainC())
        else:
            print("\nThanks for playing.")
            exit()
        exit()
    def Medium():
        """Medium"""
        print("\nDifficulty : MEDIUM")
        print("I'm thinking of a number from 2-11. What is the number?")
        for j in range(0,3):
            guess2=int(input("Your Answer= "))
            if(guess2==(10)):
                print("\nCorrect answer✅")
                prompt=str(input("Playagain (Y/N) ")).lower()
                if(prompt==("y")):
                    playagain(main=MainC())
                else:
                    print("\nThanks for playing.")
                    exit()
            elif(guess2>11):
                print("\n\nYou've Guessed above\nthe number given.Try again.")
                Medium()
            else:
                print("Wrong Answer❌")
        print("\nOops, you have 3 wrong guesses.")
        prompt=str(input("Playagain (Y/N) ")).lower()
        if(prompt==("y")):
            playagain(main=MainC())
        else:
            print("\nThanks for playing.")
            exit()
        exit()
    def Hard():
        """Hard"""
        print("\nDifficulty : HARD")
        print("I'm thinking of a Number from 1-30. What is the number?")
        for k in range(0,3):
            guess3=int(input("Your Answer= "))
            if(guess3==(16)):
                print("\nCorrect answer✅")
                prompt=str(input("Playagain (Y/N) ")).lower()
                if(prompt==("y")):
                    playagain(main=MainC())
                else:
                    print("\nThanks for playing.")
                    exit()
            elif(guess3>30):
                print("\n\nYou've Guessed above\nthe number given.Try again.")
                Hard()
            else:
                print("Wrong Answer❌")
        print("\nOops, you have 3 wrong guesses.")
        prompt=str(input("Playagain (Y/N) ")).lower()
        if(prompt==("y")):
            playagain(main=MainC())
        else:
            print("\nThanks for playing.")
            exit()
        exit()
    def Extreme():
        """Extreme"""
        print("\nDifficulty : EXTREME")
        print("I'm thinking of a number from 5-35. What is the number?")
        for L in range(0,3):
            guess4=int(input("The number is start with 3\nYour Answer= "))
            if(guess4==(31)):
                print("\nCorrect answer✅")
                prompt=str(input("Playagain (Y/N) ")).lower()
                if(prompt==("y")):
                    playagain(main=MainC())
                else:
                    print("\nThanks for playing.")
                    exit()
            elif(guess4>35):
                print("\n\nYou've Guessed above\nthe number given.Try again.")
                Extreme()
            else:
                print("Wrong Answer❌")
        print("\nOops, you have 3 wrong guesses.")
        prompt=str(input("Playagain (Y/N) ")).lower()
        if(prompt==("y")):
            playagain(main=MainC())
        else:
            print("\nThanks for playing.")
            exit()
        exit()

    def playagain(self,main):
        self.main=main
        main=MainC()

    MainC()
Num_guessing(self="play",play="0")
