import os
import pandas as pd
from utility_methods.utility_methods import *



class super:    

    def get_users(self):
        read=pd.read_csv(self.file)
        read.set_index('user',inplace=True)
        df=read.groupby(['user']).size()
        read=pd.DataFrame(df)
        read.rename(columns={0:'priority'},inplace=True)
        read.sort_values(['priority'],ascending=False, inplace=True)
        read.to_csv(self.file,mode='w',index=True, header=True)        
        new=pd.read_csv(self.file)
        #print(new.user.tolist())
        return list(new.user.values)

    def remove(self,username):
        read=pd.read_csv(self.file) 
        read.set_index('user', inplace=True)   
        #print(read.index.values)    
        #print('droped',read.drop(username))
        if (username in read.index.values):
            read.drop(username,inplace=True)
            #read.set_index('user', inplace=True) 
            read.to_csv(self.file,mode='w',index=True, header=True)
        else:
            return False

    def add(self,users):

        if type(users) is type(list()):
            data={
                'user':users,
            }           
            
        else:
            data={
                'user':[users],
            }
        read=pd.DataFrame(data)
        read.set_index('user', inplace=True)            
        read.to_csv(self.file,mode='a',index=True, header=False)


    
        

class TargetList(super):

    def __init__(self,username):
        self.username=username
        self.base_dir=check_dir(f'./database/{self.username}/')
        self.file=self.base_dir+ 'target_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))
        

class HitList(super):

    def __init__(self,username):
        self.username=username
        self.base_dir=check_dir(f'./database/{self.username}/')
        self.file=self.base_dir+'hit_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))

class FameList(super):
    
    def __init__(self,username):
        self.username=username
        self.base_dir=check_dir(f'./database/{self.username}/')
        self.file=self.base_dir+'fame_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))  
        
class PrivateList(super):
    
    def __init__(self,username):
        self.username=username
        self.base_dir=check_dir(f'./database/{self.username}/')
        self.file=self.base_dir+'private_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))            
 
class ContentLabours(super):
    def __init__(self,username):
        self.username=username
        self.base_dir=check_dir(f'./database/{self.username}/')
        self.file=self.base_dir+'content_labours'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))

class TagList(super):
    
    def __init__(self,username):
        self.username=username
        self.base_dir=check_dir(f'./database/{self.username}/')
        self.file=self.base_dir+'tag_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file))) 
   
class Profile:

    def __init__(self):
        self.base_dir=check_dir(f'./database/')
        self.file=self.base_dir+'profiles'+".csv"
        self.columns = ['user','password']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file))) 

    def add(self,user,password):
        read=pd.read_csv(self.file) 
        read.set_index('user', inplace=True)   
        if (user in read.index.values):
            return 'exist'

        else:
            data={
                'user':[user],
                'password':[password],
            }
            df=pd.DataFrame(data)
            df.set_index('user', inplace=True)            
            df.to_csv(self.file,mode='a',index=True, header=False)
            return True
    
    def remove(self,user):
        read=pd.read_csv(self.file) 
        read.set_index('user', inplace=True)   
        if (user in read.index.values):
            read.drop(user,inplace=True)
            #read.set_index('user', inplace=True) 
            read.to_csv(self.file,mode='w',index=True, header=True)
            dir=self.base_dir+user
            remove_dir(dir)
            return True
        else:
            return False

    def get_users(self):
        read=pd.read_csv(self.file)
        #read.set_index('user',inplace=True)
        data=[]
        for u,p in zip(list(read.user.values),list(read.password.values)):
            data.append({'username':u,'password':p})
        return data
    def get_profiles(self):
        read=pd.read_csv(self.file)
        #read.set_index('user',inplace=True)
        return list(read.user.values)




