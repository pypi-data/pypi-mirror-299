"""Displays a digital time."""
while True:
    try:
        import time
        import datetime
        import sys

        print("Clock Time")
        def Timesetter():
            while True:
                currenttime=datetime.datetime.now()
                hrs=currenttime.hour
                mins=currenttime.minute
                sec=currenttime.second
                time.sleep(1)
                print(f"{hrs} : {mins} {currenttime.strftime('%p')} : {sec}",end="\r")
    except ValueError:
        print("\ntime error. try again")
        sys.exit()
    except ModuleNotFoundError:
        print("\ntime error. try again")
    break

Timesetter()
