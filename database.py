import os
import pandas as pd
from utility_methods.utility_methods import *

base_dir=check_dir('./database/')

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

    def __init__(self):
        self.file=base_dir+'target_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))
        

class HitList(super):

    def __init__(self):
        self.file=base_dir+'hit_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))

class FameList(super):
    
    def __init__(self):
        self.file=base_dir+'fame_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))  
        
class PrivateList(super):
    
    def __init__(self):
        self.file=base_dir+'private_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))            
 
class ContentLabours(super):
    def __init__(self):
        self.file=base_dir+'content_labours'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))

class TagList(super):
    
    def __init__(self):
        self.file=base_dir+'tag_list'+".csv"
        self.columns = ['user']     
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file))) 
   
        
if __name__ == "__main__":
    print('ok')
    a=TagList()
    a.add(['memers','memer'])
    #print(a.get_users())
    # a.add('pankaj_nagil','Public')
    # ContentLabours().remove('pankaj_nagil')
    
    # #print(TargetUsers().get_users())
    # TargetUsers().add(['pankaj_nagil','khaoll'],['public','private'])
    # #TargetUsers().remove(['stoned_bhaiya','pankaj_l'])
    # # a.add('stoned_bhaiya','Public')
    # b=TargetUsers()
    # b.add('pankaj_l','Public')
    # b.add('stoned_a','Private')


