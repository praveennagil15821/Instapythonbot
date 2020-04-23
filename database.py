import os,csv
import pandas as pd
from utility_methods.utility_methods import *

base_dir=check_dir('./database/')

class super:
    
    def add(self,username,acctype='None'):      
        read=pd.read_csv(self.file)
        if type(username) is  type(list()) and (acctype=='None' or type(acctype) is type(list())):
            if acctype=='None':
                for x in username:
                    self.add(x)  
            else:
                for x,y in zip(username,acctype):
                    self.add(x,y) 
        else:             
            if (username in read.user.values):            
                read.loc[read.user == username,'priority']=int(read.loc[read.user == username].priority.values[0]+1)
                read.loc[read.user == username,'acctype']=acctype
                read.set_index('user', inplace=True) 
                read.to_csv(self.file,mode='w',index=True, header=True)
            else:
                data={
                    'user':[username],
                    'acctype':[acctype],                        
                    'priority':[1]
                }
                read=pd.DataFrame(data)
                read.set_index('user', inplace=True)            
                read.to_csv(self.file,mode='a',index=True, header=False)
            return None    

    def get_users(self):
        read=pd.read_csv(self.file)
        read.sort_values(['priority'],ascending=False, inplace=True)
        return list(read.user.values)

    def remove(self,username):
        read=pd.read_csv(self.file) 
        read.set_index('user', inplace=True)   
        #print(read.index.values)    
        #print('droped',read.drop(username))
        if (username in read.index.values):
            pass
            #
            read.drop(username,inplace=True)
            #read.set_index('user', inplace=True) 
            read.to_csv(self.file,mode='w',index=True, header=True)
        else:
            print('notfound')    
        
    

class TargetUsers(super):

    def __init__(self):
        self.file=base_dir+'target_users'+".csv"
        self.columns = ['user', 'acctype', 'priority']      
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))
        
    
        
        


class ContentLabours(super):
    def __init__(self):
        self.file=base_dir+'content_labours'+".csv"
        self.columns = ['user', 'acctype', 'priority']      
        self.df=pd.DataFrame(columns=self.columns)  
        self.df.set_index('user', inplace=True)          
        self.df.to_csv(self.file, mode='a',index=True, header=(not os.path.exists(self.file)))

    

   
        
if __name__ == "__main__":
    print('ok')
    a=ContentLabours()
    a.add('pankaj_nagil','Public')
    ContentLabours().remove('pankaj_nagil')
    
    #print(TargetUsers().get_users())
    TargetUsers().add(['pankaj_nagil','khaoll'],['public','private'])
    #TargetUsers().remove(['stoned_bhaiya','pankaj_l'])
    # a.add('stoned_bhaiya','Public')
    b=TargetUsers()
    b.add('pankaj_l','Public')
    b.add('stoned_a','Private')


