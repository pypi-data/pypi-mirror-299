"""Desktop notifier. \n\n\n 

Creates a desktop notification"""
try:
    from plyer import notification

    for i in range(0,1):
        title = 'TIME TO REST'
        message = 'You have used the computer too much. REST!'

        notification.notify(
        title=title,
        message=message,
        app_name='Desktop Notifier',
        timeout=20
        )
except ModuleNotFoundError:
    print("Plyer library not found.\nplease install.")
    exit()
except ValueError:
    print("Invalid input.")
    exit()
    
