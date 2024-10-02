"""A Rock Paper Scissors Game in Python.🐍
        🥌📃✂
"""

def rock_paper_scissors():
    while True:
        try:
            import sys
            import random
            from enum import Enum
            from enum import EnumType 
            playerscore=0
            computerscore=0
            gamecount=0
            class RPS(Enum):
                ROCK=1
                PAPER=2
                SCISSORS=3

            print("RPS Game")
            name=str(input("Enter your Name to Play: "))
            Num_of_Scorereach=int(input("Enter the Number of Score Reach: "))
            print("")

            while True:
                print("1 : Rock")
                print("2 : Paper")
                print("3 : Scissors")
                choice=int(input(""))
                if choice<1|choice>3:
                    sys.exit("You must choose 1,2,3")

                computerchoice=int(random.choice("123"))
                # computer=int(computerchoice)
                print("")
                print("You chose",str(RPS(choice)).replace('RPS.',''))
                print("Python chose",str(RPS(computerchoice)).replace('RPS.',''))
                print("")

                if(playerscore>=Num_of_Scorereach):
                        print("================")
                        print("Score Reach Ended!")
                        print( name,"Score:",playerscore)
                        print("Python Score:",computerscore)
                        print("🏆🏆You Win!🏆🏆")
                        print("================")
                        exit()
                if(choice==1 and computerchoice==3):
                    print("🎉You Win!")
                    playerscore+=1
                    print("Player Score:",playerscore,"\n")
                elif(choice==2 and computerchoice==1):
                    print("🎉You Win!")
                    playerscore+=1
                    print("Player Score:",playerscore,"\n")
                elif(choice==3 and computerchoice==2):
                    print("🎉You Win!")
                    playerscore+=1
                    print("Player Score:",playerscore,"\n")
                elif choice==computerchoice:
                    print("⭕ Tie Game!")
                else:
                    print("🐍Python Win!")
                    computerscore+=1
                    print("\nPython Score:",computerscore,"\n")
                    if(computerscore==Num_of_Scorereach):
                        print("================")
                        print("Score Reach Ended!")
                        print("Python Score",computerscore)
                        print(name,"Score",playerscore)
                        print("🏆🏆Python Win!🏆🏆")
                        print("================")
                        exit()
                    continue
                gamecount+=1
        except ValueError:
            print("\nOops 😦.\nTry Again")
        break

rock_paper_scissors()
