import os

if os.name == 'nt':
    print('operating system --windows')
    from win10toast import ToastNotifier

    # One-time initialization
    toaster = ToastNotifier()
    def msg(title,message,icon=None):
    # Show notification whenever needed
        try:
            toaster.show_toast(title,message, threaded=True,
                            icon_path=None, duration=3)  # 3 seconds
            import time
            while toaster.notification_active():
                time.sleep(0.1)
        except:
            print('unable to create notification windows')        

elif os.name == 'posix':
    print('operating system --linux')  
    import subprocess
    def msg(title,message,icon="face-smile"):
        subprocess.Popen(['notify-send', title, '-i', icon, message])
        return  