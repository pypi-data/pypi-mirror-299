"""A Transaction Program related to MobileMoney"""
try:
    import time
    import sys
    import getpass

    def Main():
        try:
            for T in range(3):
                print("\n=====================")
                print("MobileMoney Transaction Program")
                ask = int(input("\nHow much is in your acount? "))
                for rerun in range(3):
                    print("\nSelect from the Menu")
                    print("1 : Deposit")
                    print("2 : Withdrawn")
                    print("3 : Check Balance")
                    print("4 : My Accounts")
                    print("5 : version")
                    print("6 : Exit")
                    select=int(input(">"))
                    if(select==1):
                        print("Deposit\n".upper())
                        much1 = int(input("How much do you want to Deposit? "))
                        print("please wait....")
                        time.sleep(2)
                        num = str(input("Enter your Mobile Number: "))
                        if(len(num)>=10 or num.__contains__(f"+ {num}")):
                            print("Loading.....")
                            time.sleep(1)
                            print("NOTE: Pin is hidden.")
                            pin=getpass.getpass("Enter your pin: ")
                            print("Loading.......")
                            time.sleep(2)
                            print("====================================")
                            print(f"Your Deposit of  {much1} was Successful.")
                            ask+=much1
                            print("Your Balance left is ",ask,"Ghc")
                            print("Thank you.")
                            print("====================================")
                            rerun
                        else:
                            print("\nInvalid Number.\nnumber is not up to 10 digits.\n")
                            sys.exit()
                    elif(select==2):
                        print("\nWithDrawn\n".upper())
                        much = int(input("How Much? "))
                        if much > ask:
                            print("Your Balance is too Low")
                        elif much < ask:
                            num1 = str(input("Enter your Mobile Number: "))
                            if(len(num1)>=10 or num.__contains__(f"+ {num1}")):
                                print("please wait...")
                                time.sleep(2)
                                prompt1 = str(input("Allow Cashout 'Yes' or 'No': ")).lower()
                                if (prompt1 == ("yes")):
                                    time.sleep(2)
                                    print("Cashout is Allowed!")
                                    print("NOTE: Pin is hidden.")
                                    getpass.getpass("Enter yout pin: ")
                                    time.sleep(3)
                                    print("Loading....")
                                    time.sleep(1)
                                    print("-------------------------------")
                                    print("Cashout for", much, "Sucessful.")
                                    ask-=much
                                    print(f"Your Balance left is {ask}Ghc")
                                    print("Thank you.")
                                    print("-------------------------------")
                                    continue
                                elif (prompt1 == ("no")):
                                    print("\nCashout denied.")
                            else:
                                print("\nInvalid Number.\nnumber is not up to 10 digits.")
                                sys.exit()
                    elif(select==3):
                        print("\nCheck Balance\n")
                        time.sleep(1)
                        pin1=int(input("Enter your Pin "))
                        print("=============")
                        print(f"Your current Balance is {ask}Ghc.")
                        print("=============")
                        rerun
                    elif(select==4):
                        print("\nNot Available.coming soon")
                        rerun
                    elif(select==5):
                        time.sleep(2)
                        print("======================")
                        print("Program name : MobileMoney Transaction Program")
                        print("Program version : ver 1.2")
                        print("======================")
                    elif(select==6):
                        print("\nProgram terminated.")
                        sys.exit()
                    else:
                        print("ERROR : Invalid.")
        except ValueError:
            print("\nTransaction failed❌.")
            sys.exit()
        except ModuleNotFoundError:
            print("\nTransaction failed❌ : \nCould not find 'getpass' module.")
            sys.exit()
        except NameError:
            print("\nTransaction failed❌ : \nCould not find 'getpass' module.")
            sys.exit()
        
    Main()
except Exception:
    print("\nTransaction failed❌")
    sys.exit()