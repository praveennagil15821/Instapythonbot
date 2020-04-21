import os,csv
import pandas as pd
from utility_methods.utility_methods import *

base_dir=check_dir('./database/')

#open(base_dir+'target_users'+".csv",'a') 

def TargetUsers():
    file=base_dir+'target_users'+".csv"
    columns = ['user', 'acctype', 'prority']      
    df=pd.DataFrame(columns=columns)    
    df.to_csv(file, mode='a', header=(not os.path.exists(file)))

TargetUsers()    