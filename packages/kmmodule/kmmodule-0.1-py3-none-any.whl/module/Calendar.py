"""Displays calendar and shows current date."""
while True:
    try:
        import calendar
        import time
        import datetime
        #---------------------------
        #Prints the Calendar in Order
        # print(calendar.calendar(1))
        #---------------------------
        #Calendar that I did Myself
        print(f"Welcome to Calender {datetime.date.today().year}\n")
        time.sleep(3)
        print("January")
        for i in range(1,32):
            print(i,end=" ")
        print("\n")
        time.sleep(1)
        print("\nFebruary")
        for j in range(1,31):
            print(j,end=" ")
        print("\n")
        time.sleep(1)
        print("\nMarch")
        for k in range(1,32):
            print(k,end=" ")
        print("\n")
        time.sleep(1)
        print("\nApril")
        for l in range(1,31):
            print(l,end=" ")
        print("\n")
        time.sleep(1)
        print("\nMay")
        for kl in range(1,32):
            print(kl,end=" ")
        print("\n")
        time.sleep(1)
        print("\nJune")
        for km in range(1,31):
            print(km,end=" ")
        print("\n")
        time.sleep(1)
        print("\nJuly")
        for kn in range(1,32):
            print(kn,end=" ")
        print("\n")
        time.sleep(1)
        print("\nAugust")
        for ko in range(1,32):
            print(ko,end=" ")
        print("\n")
        time.sleep(1)
        print("\nSeptember")
        for kq in range(1,31):
            print(kq,end=" ")
        print("\n")
        time.sleep(1)
        print("\nOctober")
        for ko in range(1,32):
            print(ko,end=" ")
        print("\n")
        time.sleep(1)
        print("\nNovember")
        for y in range(1,31):
            print(y,end=" ")
        print("\n")
        time.sleep(1)
        print("\nDecember")
        for zol in range(1,32):
            print(zol,end=" ")
        print("\n")
        time.sleep(2)
        #Print the current Date
        print("-----------------------")
        print("Current Date|",datetime.date.today())
        print("-----------------------")
    except ModuleNotFoundError:
        print("\nCannot print out calender ⚠.")
    exit()
