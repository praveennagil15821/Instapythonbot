import database,notification,insta
import getpass
import os
import instaloader

def intro():
    
    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@                                                               @@@")
        print("@@@                Welcome to Instakiller                         @@@")
        print("@@@                     version 0.2                               @@@")
        print("@@@              Belive or not || I am poisonous                  @@@")
        print("@@@                                                               @@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@                                                                  ")
        print("@@@ 1. Start Bot                                                     ")
        print("@@@ 2. Settings                                                   ")
        print("@@@ 3. Exit  or press Ctrl+ C                                     ")
        print("@@@                                                               ")
    
        choice=input("###> Select your choice (* Leave empty for default = 1) : ")
        
        if choice=='1' or choice=='':
            print("@@@ \t-------------Starting Bot-------------")
            return 1
        elif choice=='2':
            print('@@@ \t-------------Opening settings-------------')
            return 2
        elif choice=='3':
            print('@@@ \t-------------Exiting-------------')
            return 3
        else:
            print("@@@ *** \t Enter valid input \t***")

def settings():    
    
    while True:
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ")
        print("@@@                 ")
        print("@@@ 0. View Profiles    ")
        print("@@@ 1. Add Profile    ")
        print("@@@ 2. Delete Profile     ")
        print("@@@ 3. Add Tags         ")
        print("@@@ 4. Add Targets         ")
        print("@@@ 5. Back         ")
        print("@@@                 ")
        choice=input("###> Select your choice : ")
        if choice=='0':
            print("@@@ \t-------------Total Profiles-------------")
            print("@@@                 ")
            while True:
                db=database.Profile().get_profiles()
                if len(db):
                    for u in db:
                        print(f"@@@ <<< \t {u} \t\t>>>\n")
                    
                else:
                    print(f"@@@ <<< \t No profiles found \t>>>\n")
                    print("@@@                 ")
                i=input("###> Press any key to go back : ")    
                settings()     
        if choice=='1':
            print("@@@ \t-------------Add Profile-------------\n")
            print("@@@                 ")
            count=0
            while True and count<3:
                try:
                    count+=1
                    user=input("###> Enter your Username (not email) : ")
                    db=database.Profile().get_profiles()
                    if user in db:
                        print("@@@ <<< \t Profile Already Exist \t>>>\n")
                        print("@@@                 ")
                        print("@@@ 1. Retry         ")
                        i=input("###> Press any key to go back : ")
                        if i=='1':
                            continue
                        else:
                            settings()     
                        break
                    print("###> Enter your Password : ")
                    password=getpass.getpass()
                    instaloader.Instaloader().login(user,password)
                    db=database.Profile().add(user,password)
                    if db==True:
                        print("@@@ <<< \t Profile Created Successfully \t>>>\n")
                        print("@@@                 ")
                        settings()
                    elif db=='exist':
                        print("@@@ <<< \t Profile Already Exist \t>>>\n")
                        print("@@@                 ")
                        print("@@@ 1. Retry         ")
                        i=input("###> Press any key to go back : ")
                        if i=='1':
                            continue
                        else:
                            settings()     

                except:
                    print("@@@ *** \tEnter valid username and password\t***\n")
                    print("@@@                 ")
                    print("@@@ 1. Retry         ")
                    i=input("###> Press any key to go back : ")
                    if i=='1':
                        continue
                    else:
                        settings()     
            
    
        elif choice=='2':
            while True:
                print('@@@ \t-------------Delete Profile-------------')
                print("@@@                 ")
                user=input("###> Enter profile Username (not email) to delete : ")
                db=database.Profile().get_profiles()
                if user in db:
                    confirm=input(f"###> Confirm deleting {user}'s profile (y/n) : ")
                    print("@@@                 ")
                    if confirm.lower() =='y' or confirm.lower()=='yes':
                        database.Profile().remove(user)
                        print("@@@ <<< \t Profile Deleted Successfully \t>>>\n")
                        print("@@@                 ")
                        print("@@@ 1. Delete another profile         ")
                        i=input("###> Press any key to go back : ")
                        if i=='1':
                            continue
                        else:
                            settings()     
                    else:
                        continue
                else:
                    print(f"@@@ <<< \t {user}'s Profile does not exist \t>>>\n")
                    print("@@@                 ")
                    print("@@@ 1. Retry         ")
                    i=input("###> Press any key to go back : ")
                    if i=='1':
                        continue
                    else:
                        settings()     

            
        elif choice=='3':
            
            while True:
                print('@@@ \t-------------Add Tags-------------')
                print("@@@                 ")
                user=input("###> Enter profile Username (not email) to add tags to : ")
                db=database.Profile().get_profiles()
                if user in db:
                    confirm=input(f"###> Confirm adding tags to {user}'s profile (y/n) : ")
                    print("@@@                 ")
                    if confirm.lower() =='y' or confirm.lower()=='yes':
                        print("@@@  Please enter tags seperated by coma's without including ' # ' as shown \n\n@@@ #funny \n@@@ #memes \n@@@ as :funny,memes \n")
                        tags=input("###> Enter coma seperated tags without extra spaces: ")
                        tags=tags.split(',')
                        if not len(tags):
                            continue

                        database.TagList(user).add(tags)
                        print(f"\n@@@ <<< \t Tags added to {user}'s profile Successfully \t>>>\n")
                        print("@@@                 ")
                        print("@@@ 1. Add more         ")
                        i=input("###> Press any key to go back : ")
                        if i=='1':
                            continue
                        else:
                            settings()     
                    else:
                        continue
                else:
                    print(f"@@@ <<< \t {user}'s Profile does not exist \t>>>\n")
                    print("@@@                 ")
                    print("@@@ 1. Retry         ")
                    i=input("###> Press any key to go back : ")
                    if i=='1':
                        continue
                    else:
                        settings()     
            
        elif choice=='4':
            
            while True:
                print('@@@ \t-------------Add Targets-------------')
                print("@@@                 ")
                user=input("###> Enter profile Username (not email) to add targets to : ")
                db=database.Profile().get_profiles()
                if user in db:
                    confirm=input(f"###> Confirm adding targets to {user}'s profile (y/n) : ")
                    print("@@@                 ")
                    if confirm.lower() =='y' or confirm.lower()=='yes':
                        print("@@@  Please enter targets seperated by coma's without as shown \n\n@@@ example_one \n@@@ example_two \n@@@ as :example_one,example_two \n")
                        tags=input("###> Enter coma seperated targets without extra spaces: ")
                        tags=tags.split(',')
                        if not len(tags):
                            continue
                        
                        database.TargetList(user).add(tags)
                        print(f"\n@@@ <<< \t Targets added to {user}'s profile Successfully \t>>>\n")
                        print("@@@                 ")
                        print("@@@ 1. Add more         ")
                        i=input("###> Press any key to go back : ")
                        if i=='1':
                            continue
                        else:
                            settings()     
                    else:
                        continue
                else:
                    print(f"@@@ <<< \t {user}'s Profile does not exist \t>>>\n")
                    print("@@@                 ")
                    print("@@@ 1. Retry         ")
                    i=input("###> Press any key to go back : ")
                    if i=='1':
                        continue
                    else:
                        settings()     
            
            
        elif choice=='5':
            print('@@@ \t-------------Returning-------------')
            print("@@@                 ")
            main()
        else:
            print("@@@ *** \t Enter valid input \t***")

def start():
    profiles=database.Profile().get_profiles()
    if len(profiles):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ")
        print("@@@    ")
        print(f"@@@                {len(profiles)}   Profiles found                          ")
        print("@@@  ----------------------------------------------------------------  ")
        count=1
        flag=True
        for u in profiles:
            targets=database.TargetList(u).get_users()
            total_targets=len(targets)
            if len(targets):
                print(f"@@@ {count}. {u}  has {total_targets} targets to hit.")
            else:
                print(f"@@@ {count}. {u}  has {total_targets} to hit. Please enter primary targets from settings.")
                flag=False
            count+=1
        print("@@@                 ")
        print("@@@  ----------------------------------------------------------------  ")
        if flag:
            choice=input("###> Enter the number of users to hit by each profile : ")
            # try:
            choice=int(choice)

            if choice>0:
                print("@@@    Select MODE of bot    ")
                print("@@@ 0. LIGHT  (' Works like your ass -- 6-8 hits / attempt   ')   ")
                print("@@@ 1. NORMAL (' Works like human    -- 10-14 hits / attempt ')   ")
                print("@@@ 2. POWER  (' Works like Machine  -- 18-20 hits / attempt ')   ")
                print("@@@                 ")
                m=input("###> Select your choice (* Press any key for default i.e NORMAL): ")
                if m=='0':mode='light'
                elif m=='1' or m=='':mode='normal'
                elif m=='2':mode='power'
                accounts=database.Profile().get_users()
                for acc in accounts:
                    insta.Controller(acc['username'],acc['password'],choice,mode).start()

            else:
                choice=input("###> Press any key to return home : ")
                main()
            # except:
            #     print("@@@ *** \t Enter valid input \t***")
            #     print("@@@      ")
                               

        else:
            choice=input("###> Press any key to return home : ")
            main()
    else:
        print("@@@    ")
        print("@@@ *** \t No profiles found  \t*** ")
        print("@@@ ***  Add profiles from settings and add few initial targets to start  *** ")
        print("@@@                 ")
        choice=input("###> Press any key to return home : ")
        main()


def main():
    choice=intro()
    if choice==1:
        start()
    elif choice==2:
        print(settings())
    elif choice==3:
        exit()

if __name__ == "__main__":
    main()
    