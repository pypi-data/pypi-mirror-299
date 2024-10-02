"""Counts numbers automatically given by the user"""
import sys
import time
def mainB():
    """Main Function"""
    while True:
        try:
            print("Auto Count 1.2")
            print("\nSelect a Count Type")
            print("1 : Number counting forward")
            print("2 : Number counting backward")
            print("3 : letters Count")
            select=str(input(""))
            if(select==("1")):
                ncf()
            elif(select==("2")): 
                ncb()  
            elif(select==("3")):
                print("\nNot available.\n")
                continue
            else:
                print("\nSelect only 1,2 and 3.") 
                sys.exit()
        except ValueError:
            print("\nInvalid Selection!") 
        sys.exit()
def ncf():
    while True:
        try:
            print("Number Counting Forward\n".upper())
            startnum=int(input("Enter starting number "))
            endnum=int(input("Enter ending number "))
            prompt=str(input("Do you want Time count\nor No time count? (Y/N) ")).lower()
            printt=str(input("Choose how it will appear\nHorizontal-(H) / Vertical?-(V) ")).lower()
            if(printt==("h")):
                if(prompt==("y")):
                    timeout1=float(input("Enter time Count (0.1 - 0.100) "))
                    print("")
                    print(f"\nStarting Number : {startnum}")
                    print(f"Ending Number : {endnum}\n")
                    for i in range(startnum,endnum):
                        time.sleep(timeout1)
                        print(i,end=" ")
                    print("\nComplete!".upper())
                elif(prompt==("n")):
                    for ca in range(startnum,endnum):
                        print(ca)
                    print("\nComplete!".upper())
            elif(printt==("v")):
                for ca in range(startnum,endnum):
                        print(ca)
                print("\nComplete!".upper())         
        except ValueError:
            print("\nInvalid. Try again.")
        sys.exit()
def ncb():
    while True:
        try:
            print("Number Counting Backward\n".upper())
            startnum1=int(input("Enter starting number "))
            endnum1=int(input("Enter ending number "))
            timeout2=float(input("Enter time Count (0.1 - 0.100) "))
            printt=str(input("Choose how it will appear\nHorizontal-(H) / Vertical?-(V) ")).lower()
            print("")
            if(printt==("h")):
                for ii in range(endnum1,startnum1):
                    time.sleep(timeout2)
                    print(ii-startnum1,end=" ")
                print("\nComplete!".upper())
            elif(printt==("v")):
                for ii in range(endnum1,startnum1):
                    time.sleep(timeout2)
                    print(ii-startnum1)
                print("\nComplete!".upper())
        except ValueError:
            print("\nInvalid. Try again.")
        sys.exit()

mainB()