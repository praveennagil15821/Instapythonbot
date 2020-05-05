from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from utility_methods.utility_methods import *
import urllib.request
import os
from random import randint,shuffle 
import notification
import database


class InstaBot():

    def __init__(self, username=None, password=None):

        self.username = username 
        self.password = password 

        self.login_url = 'https://www.instagram.com/accounts/login/'
        self.home_url = 'https://www.instagram.com/'
        self.nav_user_url = 'https://www.instagram.com/{}/'
        self.get_tag_url = 'https://www.instagram.com/explore/tags/{}/'
        self.suggested_user_url = 'https://www.instagram.com/explore/people/suggested/'
        self.mainuser = username
        self.x_path = ''
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.bool = {'commented':False,'likers':False,'likers_list':[]}
        self.timepass=False
        self.mainfollowers=[]
        self.follow_count=0


    
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """

        self.driver.get(self.login_url)

        self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_input = self.driver.find_element_by_name('username')
        self.wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        password_input = self.driver.find_element_by_name('password')

        username_input.send_keys(self.username)
        time.sleep(1)  # ruko jara
        password_input.send_keys(self.password)

        # login_btn = self.driver.find_element_by_css_selector('button[type="submit"]')
        # login_btn = self.driver.find_element_by_xpath(
        # '//button//div[text() = "Log In"]')

        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, r'//button//div[text() = "Log In"]')))
        login_btn = self.driver.find_element_by_xpath(
            r'//button//div[text() = "Log In"]')
        
        login_btn.click()
        # notification.msg('Alert!','Login success full')
        # pop_up = self.driver.find_element_by_xpath('//div[text()="Know right away when people follow you or like and comment on your photos."]')

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, r'//button[text() = "Not Now"]')))

        not_now_button = self.driver.find_element_by_xpath(
            '//button[text() = "Not Now"]')
        not_now_button.click()

        # MessagePage='/direct/inbox/'
        # ExplorePage = '/explore/'
        # AccountActivity = '/accounts/activity/'

    def exploretags(self):
        self.timepass=True
        tags=database.TagList(self.username).get_users()
        shuffle(tags)
        tags.reverse()
        shuffle(tags)
        till=randint(3,6)
        for tag in tags[:till]:
            self.driver.get(self.get_tag_url.format(tag))
            self.post(amount=randint(5,8))

    def quit(self):
        self.driver.close()
        print("System down -- Successfull")
        notification.msg('Alert!', 'System down -- Successfull')

    def grabpopup(self):
        # self.driver.get(self.suggested_user_url)
        user = []

        def check_difference_in_count(driver):
            len_old = len(user)
            items = driver.find_elements_by_xpath(r'{}'.format(self.x_path))
            for i in items:
                temp = str(i.get_attribute("alt"))
                if temp.split("'s profile")[0] not in user:
                    user.append(temp.split("'s profile")[0])
            len_new = len(user)
            if (len_new != len_old):
                #print('old len',len_old,'new len',len_new)
                return True
            else:
                #print('exit   ---old len',len_old,'new len',len_new)
                return False

        while True:
            # scroll down
            time.sleep(2)
            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(
                (By.XPATH, r'{}'.format(self.x_path))))
            # WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(
            #     (By.XPATH, r'//main//img[contains(@alt,profile)]')))

            x = self.driver.find_elements_by_xpath(
                r'{}'.format(self.x_path))
            self.driver.execute_script("arguments[0].scrollIntoView();", x[-1])
            time.sleep(1)
            # self.driver.execute_script("arguments[0].scrollIntoView();", x[-6])

            try:
                WebDriverWait(self.driver, 5).until(check_difference_in_count)
            except Exception as e:
                print(f"@@@       {e}          ")
                break

        # print(user)
        return user

    def grabfollow(self):
        self.x_path = '//div[@role="dialog"]//img[contains(@alt,profile)]'
        return self.grabpopup()

    def GrabSuggested(self):
        try:
            self.driver.get(self.suggested_user_url)
            self.x_path = '//main//img[contains(@alt,profile)]'
            users=self.grabpopup()
            database.TargetList(self.username).add(users)
        except Exception as e:
            print(f"@@@       {e}          ")
            print(f"@@@  ****/t error at GrabSuggested()\t****")
    def stories(self, username):
        self.driver.get(self.nav_user_url.format(username))
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, r'//header//canvas')))
        self.driver.find_element_by_xpath('//header//img').click()
        time.sleep(2)
        if self.driver.current_url == self.nav_user_url.format(username):
            print("@@@                 ")
            print(f'@@@ ---- no story detected  @ {username} ')
            return 0
        else:
            print("@@@                 ")
            print(f'@@@ ---- watching @ {username} story')
            time.sleep(7)
            self.driver.get(self.nav_user_url.format(username))

    def grablikes(self):
        try:            
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, r'//article//button[text()=" others" or text()=" likes"]')))
            print("@@@                 ")
            print("@@@     Grabbing post likes            ")
            self.driver.find_element_by_xpath(
                r'//article//button[text()=" others" or text()=" likes"]').click() 
            self.x_path = '//div[@role="presentation"]//img[contains(@alt,profile)]'
            self.bool['likers_list']=self.grabpopup()#save it database directly
            self.bool['likers']=True
            self.driver.find_element_by_xpath(r'//div[@role="presentation"]//button/*[name()="svg"][@aria-label="Close"]').click()
            return True
        except Exception as e:
            print(f"@@@       {e}          ")
            print('@@@ ***\terror in grablikes xpath\t***')
        

    def post(self,amount=5):
        liked_comment=[]
        def is_img_video(driver):
            try:
                self.driver.find_element_by_xpath(
                    r'//article//video')
                return 'video'                
            except Exception as e:
                print(f"@@@       {e}          ")
                # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                #     (By.XPATH, r'//article//button[text()=" others" or text()=" likes" or contains(text(),"like this")]')))
                
                return 'img' 

        def has_next_picture(driver):
            next_button = "//a[text()=\"Next\"]"
            # try:
            #print('next picture k andr hu')
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, r'{}'.format(next_button))))
            try:
                time.sleep(randint(0,1))
                driver.find_element_by_xpath(next_button).click()
                return True
            except Exception as e:
                print(f"@@@       {e}          ")
                return False
        def load_more_comments(driver):
            count=0
            while True and count>5:
                try:
                    WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, r'//article//button/*[name()="span"][contains(@aria-label,"more comments")]')))
                    driver.find_element_by_xpath(r'//article//button/*[name()="span"][contains(@aria-label,"more comments")]').click()
                    print('loading more comments')
                    count+=1
                except Exception as e:
                    print(f"@@@       {e}          ")
                    break

        def like_comments(driver,hearts,liked_comment):     
            self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, r'//li[@role="menuitem"]')))
            owner=self.driver.find_element_by_xpath('//article//header//img[contains(@alt,profile)]')
            owner=(str(owner.get_attribute("alt"))).split("'s profile")[0]
            #print('post-owner name ',owner)
            
            
            comments = self.driver.find_elements_by_xpath(
                '//li[@role="menuitem"]')
            # if len(hearts)==0 and len() 
            commented_users=[]           
            for comment in comments:
                user = comment.find_element_by_tag_name("img")
                temp=str(user.get_attribute("alt"))
                temp = temp.split("'s profile")[0]
                if temp==owner:
                    pass
                else:
                    commented_users.append(temp.split("'s profile")[0])
            #print('commentable count',len(commented_users))        
            #print(commented_users)
                   
            for comment,like in zip(commented_users,hearts):
                if self.timepass==True:prob=randint(0,1)
                else:prob=randint(0,3)
                if comment not in liked_comment and prob and comment not in self.mainfollowers:
                    liked_comment.append(comment)
                    time.sleep(randint(1,2))
                    time.sleep(randint(0,1))
                    like.click()
                else:
                    print("@@@                 ")
                    print(f'@@@ $$$\tsame user comment {comment} will skip like\t$$$')    


        def like_pic(driver,liked_comment,first):
            try:
                load_more_comments(driver)
                self.wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, r'//button/*[name()="svg"][contains(@aria-label,"Like") or contains(@aria-label,"Unlike")]')))
                hearts = self.driver.find_elements_by_xpath(
                        '//button/*[name()="svg"][contains(@aria-label,"Like") or contains(@aria-label,"Unlike")]')
                like_button=hearts[0]
                comment_hearts = hearts[1:]
                
                if first and is_img_video(driver)=='img':                
                    #time.sleep(randint(1,2))
                    if not self.timepass:self.grablikes()
                    time.sleep(randint(1,2))
                    like_button.click()                
                    if (len(comment_hearts)==0):
                        #comment kro bhaiya
                        self.bool['commented']=True
                    else:
                        like_comments(self.driver,comment_hearts,liked_comment)
                    
                elif first and is_img_video(driver)=='video':
                    time.sleep(randint(1,2))
                    like_button.click()
                    if (len(comment_hearts)==0):
                        #comment kro bhaiya
                        self.bool['commented']=True
                    else:
                        like_comments(self.driver,comment_hearts,liked_comment)
                    
                else:
                    time.sleep(randint(1,2))
                    if is_img_video(driver)=='video':
                        if (len(comment_hearts)==0):
                            if self.bool['commented']==False:                            
                                #comment kro skip nhi kr sakte
                                self.bool['commented']=True  
                            time.sleep(randint(1,2))
                            like_button.click()      
                        else:                        
                            if randint(0,5) < 2:
                                time.sleep(randint(1,2))
                                like_button.click()
                                like_comments(self.driver,comment_hearts,liked_comment)

                    elif is_img_video(driver)=='img':
                        if self.bool['likers']==False and not self.timepass:
                            self.grablikes()
                            time.sleep(randint(1,2))
                            like_button.click()
                            #time.sleep(randint(1,2))
                            if (len(comment_hearts)==0):
                                if self.bool['commented']==False:
                                    self.bool['commented']==True
                                    #comment kro bhaiya
                            else:
                                like_comments(self.driver,comment_hearts,liked_comment)
                        else:
                            if randint(0,5) < 2:
                                time.sleep(randint(1,2))
                                like_button.click()
                                #time.sleep(randint(1,2))
                                if (len(comment_hearts)!=0):
                                    like_comments(self.driver,comment_hearts,liked_comment)
                    else:
                        print("@@@                 ")
                        print('@@@ ***\tSomething is wrong with like_pic()\t***')
            except Exception as e:
                print(f"@@@       {e}          ")
                print('@@@ ***\tlink may be broken or timeout\t***')
                return None
        pic = self.driver.find_element_by_class_name("_9AhH0")
        time.sleep(randint(1,2))
        pic.click()
        self.bool['commented']=False
        self.bool['likers']=False
        like_pic(self.driver,liked_comment,first=True)
        
        count = 1
        # like_pic(self.driver)

        while count <= amount:
            if has_next_picture(self.driver):
                # //article//button/*[name()="span"][contains(@aria-label,'more comments')]   load more comment
                like_pic(self.driver,liked_comment,first=False)
                count += 1
            else:
                print(has_next_picture(self.driver))
                break
        return True            
    
    def grab_mainacc_followers(self,username):
        try:
            self.driver.get(self.nav_user_url.format(username))

            try:
                followers = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/a[text()=" followers"]/span'))).text).replace(',', '')
                following = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/a[text()=" following"]/span'))).text).replace(',', '')
                acctype = 'Public'
                if followers.islower() or following.islower():
                    if followers.islower():
                        followers = str(self.driver.find_element_by_xpath(
                            '//li/a[text()=" followers"]/span').get_attribute('title'))
                        followers = followers.replace(',', '')
                    if following.islower():
                        following = str(self.driver.find_element_by_xpath(
                            '//li/a[text()=" following"]/span').get_attribute('title'))
                        following = following.replace(',', '')
            except Exception as e:
                followers = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/span[text()=" followers"]/span'))).text).replace(',', '')
                following = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/span[text()=" following"]/span'))).text).replace(',', '')
                acctype = 'Private'
                if followers.islower() or following.islower():
                    if followers.islower():
                        followers = str(self.wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//li/span[text()=" followers"]/span'))).get_attribute('title'))
                        followers = followers.replace(',', '')
                    if following.islower():
                        following = str(self.wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//li/span[text()=" following"]/span'))).get_attribute('title'))
                        following = following.replace(',', '')

            self.driver.find_element_by_partial_link_text("followers").click()
            self.x_path='//div[@role="dialog"]//li//img'
            self.mainfollowing=self.grabpopup()
                
 
        except Exception as e:
            print(f"@@@       {e}          ")
            return None

    def follow_user(self,username,acctype):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//header//button[text()="Follow"]')))
            follow=self.driver.find_element_by_xpath('//header//button[text()="Follow"]')
            follow.click()
            print("@@@                 ")
            if acctype=='Private':print(f'@@@ ++++++ Follow request sent to {username} ++++++')
            else:print(f'@@@ ++++++ Started following {username} ++++++')
            self.follow_count+=1
            return True
        except Exception as e:
            print(f"@@@       {e}          ")
            print('@@@ ***\tSomething is wrong with Follow_user()\t***')
            return False
            

    def account_details(self, username):
        try:
            self.driver.get(self.nav_user_url.format(username))
            posts = str(self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//li/span[text()=" posts"]/span'))).text).replace(',', '')

            try:
                followers = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/a[text()=" followers"]/span'))).text).replace(',', '')
                following = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/a[text()=" following"]/span'))).text).replace(',', '')
                acctype = 'Public'
                if followers.islower() or following.islower():
                    if followers.islower():
                        followers = str(self.driver.find_element_by_xpath(
                            '//li/a[text()=" followers"]/span').get_attribute('title'))
                        followers = followers.replace(',', '')
                    if following.islower():
                        following = str(self.driver.find_element_by_xpath(
                            '//li/a[text()=" following"]/span').get_attribute('title'))
                        following = following.replace(',', '')
            except Exception as e:
                followers = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/span[text()=" followers"]/span'))).text).replace(',', '')
                following = str(self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//li/span[text()=" following"]/span'))).text).replace(',', '')
                acctype = 'Private'
                if followers.islower() or following.islower():
                    if followers.islower():
                        followers = str(self.wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//li/span[text()=" followers"]/span'))).get_attribute('title'))
                        followers = followers.replace(',', '')
                    if following.islower():
                        following = str(self.wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//li/span[text()=" following"]/span'))).get_attribute('title'))
                        following = following.replace(',', '')

            ratio = int(following)/int(followers)
            # print('posts-', posts, ' followers-', followers," following-", following, "ratio", ratio)
            if int(followers) <= int(following):self.follow_user(username,acctype)
            else:print(f'@@@ ------ user {username} does not fit into follow request------')
            if acctype == 'Public':
                if int(posts):
                    amount=randint(4,6)
                    functions=[(self.stories,[username]),(self.post,[amount])]
                    shuffle(functions)
                    for func, args in functions:
                        func(*args)

                return {'followers': followers, 'following': following, 'ratio': ratio,'post_likers':self.bool['likers_list']}
            else:
                return acctype
        except Exception as e:
            print(f"@@@       {e}          ")
            print('@@@ ***\tSomething is wrong with Account_details()\t***')

            return None
    

    def hit(self,power):
        self.timepass=False
        target = database.TargetList(self.username).get_users()
        #self.grab_mainacc_followers(self.mainuser)
        hit = database.HitList(self.username).get_users()
        self.mainfollowers=hit
        power=randint(power-2,power+3)
        targets_hits=0
        for i in target[:power]:
            if i in hit:
                print("@@@                 ")
                print(f'///\t{i} already in followers or hit list')
                database.HitList(self.username).add(i)
                database.TargetList(self.username).remove(i)
                continue
            acc = self.account_details(i)
            
            if acc == 'Private':
                print("@@@                 ")
                print(f'@@@ user @ {i} account is private')
                database.PrivateList(self.username).add(i)
                database.TargetList(self.username).remove(i)
            elif acc==None:
                pass
            else:
                if acc['ratio'] < 0.00:
                    print("@@@                 ")
                    print(f'@@@ user @ {i} has famed account with {acc["followers"]} followers')
                    database.FameList(self.username).add(i)
                    database.TargetList(self.username).remove(i)
                else:
                    database.HitList(self.username).add(i)  
                    database.TargetList(self.username).remove(i)      
                users = acc['post_likers']
                database.TargetList(self.username).add(users)
            targets_hits+=1
            print('@@@ ????\t total users followed -{self.follow_count} \t????')
        return targets_hits

    def home(self):
        self.driver.get(self.home_url)
        count=0
        while count<8:
            try:
                count+=1
                self.wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, r'//article[{}]'.format(count).format(count))))
                article= self.driver.find_element_by_xpath(
                        '//article[{}]'.format(count)) 
                print(count)
                self.driver.execute_script("arguments[0].scrollIntoView();", article)
                time.sleep(randint(2,5))            
                self.wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, r'//article[{}]//button/*[name()="svg"][contains(@aria-label,"Like") or contains(@aria-label,"Unlike")]'.format(count))))
                hearts = self.driver.find_elements_by_xpath(
                        '//article[{}]//button/*[name()="svg"][contains(@aria-label,"Like") or contains(@aria-label,"Unlike")]'.format(count))
                for heart in hearts:
                    self.driver.execute_script("arguments[0].scrollIntoView();", heart)
                    if randint(0,1):
                        time.sleep(randint(2,4))
                        heart.click()
                
            except Exception as e:
                print(f"@@@       {e}          ")
                print('$$$ Skipping some posts at home ')
        self.driver.get(self.home_url)
        return None

class Controller:
    def __init__(self,username,password,targets,mode='normal'):
        self.obj=InstaBot(username,password)
        self.targets_hit=0
        self.targets=targets
        self.mode=mode
        self.modes={
            'light':self.light,
            'normal':self.normal,
            'power':self.power
        }
    def Extratask(self):
        functions=[(self.obj.home()),(self.obj.exploretags()),(self.obj.GrabSuggested())]
        shuffle(functions)
        for func, args in functions:
            func(*args)
        

    def light(self):        
        self.targets_hit+=self.obj.hit(power=8)
        self.Extratask()

    def normal(self):        
        self.targets_hit+=self.obj.hit(power=12)
        self.Extratask()
    

    def power(self):        
        self.targets_hit+=self.obj.hit(power=20)
        self.Extratask()
    def start(self):
        self.obj.login()
    
        while self.targets_hit < self.targets:
            try:
                self.modes[self.mode]()
            except Exception as e:
                print(f"@@@       {e}          ")
                print('@@@ ***\tSome error passing on\t***')    
        print(f'@@@ Total {self.targets_hit} targets hitted')
        self.obj.quit()


