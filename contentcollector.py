import instaloader
from utility_methods.utility_methods import *
import multiprocessing
import os
import database
content_dir=check_dir('./content/')



def instacollector():
    return database.ContentLabours().get_users()

def addfew(username):
    database.ContentLabours().add(username)
    os.chdir(content_dirclear
    )
    #instaloader.Instaloader().download_profile(username,fast_update=True)
    try:
        instaloader.Instaloader().download_profile(username,fast_update=True)
    except:
        L=instaloader.Instaloader()
        L.login('terabhaijitega@gmail.com','king15821')
        L.download_profile(username,fast_update=True)
    else:
        print('dono bekar')   

def contentadd(username):
    username=str(username)    
    p = multiprocessing.Process(target=addfew, args=(username, ))
    p.start()
    p.join(15)
    if p.is_alive():
        p.terminate()        


if __name__ == "__main__":
    #contentadd('pankaj_nagil')
    print(instacollector())