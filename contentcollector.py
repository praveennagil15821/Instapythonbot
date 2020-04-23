import instaloader
from utility_methods.utility_methods import *
import multiprocessing
import os
import database,notification
content_dir=check_dir('./content/')


class insta():   

    def __init__(self):
        self.content_dir=check_dir('./content/insta/')
        self.login_uname=''
        self.login_pass=''
    def collectcall(self,username):
        os.chdir(self.content_dir)  
        #instaloader.Instaloader().download_profile(username,fast_update=True)
        try:
            instaloader.Instaloader(save_metadata=False, compress_json=False,).download_profile(username,download_stories=True,fast_update=True)
        except:
            L=instaloader.Instaloader(save_metadata=False, compress_json=False,)
            L.login(self.login_uname,self.login_pass)
            L.download_profile(username,download_stories=True,fast_update=True)
        return None    
        
    def collector(self):
        targets=database.ContentLabours().get_users()
        for x in targets:
            p = multiprocessing.Process(target=self.collectcall, args=(x, ))
            p.start()
            p.join()
        notification.msg('Hurray!','Content collected successfully')    

    def addcall(self,username):
        database.ContentLabours().add(username)
        os.chdir(self.content_dir)
        #instaloader.Instaloader().download_profile(username,fast_update=True)
        try:
            instaloader.Instaloader(save_metadata=False, compress_json=False,).download_profile(username,fast_update=True)
        except:
            L=instaloader.Instaloader(save_metadata=False, compress_json=False,)
            L.login(self.login_uname,self.login_pass)
            L.download_profile(username,fast_update=True)
        else:
            print('dono bekar')   

    def add(self,username):
        if type(username) is type(list()):
            for x in username:
                self.add(x)
        else:
            p = multiprocessing.Process(target=self.addcall, args=(username, ))
            p.start()
            p.join(15)
            if p.is_alive():
                p.terminate()        
            return None



if __name__ == "__main__":
    insta().collector()
    #insta().add(['pankaj_nagil','kholke_to_dekho'])