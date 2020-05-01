from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

        self.username = username or config['IG_AUTH']['USERNAME']
        self.password = password or config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.home_url = config['IG_URLS']['HOME']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']
        self.suggested_user_url = config['IG_URLS']['SUG_USER']
        self.mainuser = 'stoned_bhaiya'
        self.x_path = ''
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.bool = {'commented':False,'likers':False,'likers_list':[]}
        self.timepass=False
        self.mainfollowers=[]


    
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
        tags=database.TagList().get_users()
        for tag in tags:
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
            except:
                break

        # print(user)
        return user

    def grabfollow(self):
        self.x_path = '//div[@role="dialog"]//img[contains(@alt,profile)]'
        return self.grabpopup()

    def GrabSuggested(self):
        self.driver.get(self.suggested_user_url)
        self.x_path = '//main//img[contains(@alt,profile)]'
        database.TargetList.add(self.grabpopup())

    def stories(self, username):
        self.driver.get(self.nav_user_url.format(username))
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, r'//header//canvas')))
        self.driver.find_element_by_xpath('//header//img').click()
        time.sleep(2)
        if self.driver.current_url == self.nav_user_url.format(username):
            print('no story detected')
            return 0
        else:
            print(f'watching {username} story')
            time.sleep(7)
            self.driver.get(self.nav_user_url.format(username))

    def grablikes(self):
        try:            
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, r'//article//button[text()=" others" or text()=" likes"]')))
            self.driver.find_element_by_xpath(
                r'//article//button[text()=" others" or text()=" likes"]').click() 
            self.x_path = '//div[@role="presentation"]//img[contains(@alt,profile)]'
            self.bool['likers_list']=self.grabpopup()#save it database directly
            self.bool['likers']=True
            self.driver.find_element_by_xpath(r'//div[@role="presentation"]//button/*[name()="svg"][@aria-label="Close"]').click()
            return True
        except:
            print('error in grablikes xpath')
        

    def post(self,amount=5):
        liked_comment=[]
        def is_img_video(driver):
            try:
                self.driver.find_element_by_xpath(
                    r'//article//video')
                return 'video'                
            except:
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
            except:
                return False
        def load_more_comments(driver):
            count=0
            while True and count>5:
                try:
                    WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, r'//article//button/*[name()="span"][contains(@aria-label,"more comments")]')))
                    driver.find_element_by_xpath(r'//article//button/*[name()="span"][contains(@aria-label,"more comments")]').click()
                    print('loading more comments')
                    count+=1
                except:
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
                    print(f'same user comment {comment} will skip like')    


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
                        print('something is wrong with like_pic()')
            except:
                print('link may be broken or timeout')
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
            except:
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
                
 
        except:
            return None


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
            except:
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
        except:
            return None

    def hit(self,power):
        self.timepass=False
        target = database.TargetList().get_users()
        #self.grab_mainacc_followers(self.mainuser)
        hit = database.HitList().get_users()
        self.mainfollowers=hit
        power=randint(power-2,power+3)
        targets_hits=0
        for i in target[:power]:
            if i in hit:
                print(f'{i} already in followers or hit list')
                database.HitList().add(i)
                database.TargetList().remove(i)
                continue
            acc = self.account_details(i)
            print(acc)
            if acc == 'Private':
                print('acc is private')
                database.PrivateList().add(i)
                database.TargetList().remove(i)
            elif acc==None:
                pass
            else:
                if acc['ratio'] < 0.00:
                    print('famed account ')
                    database.FameList().add(i)
                    database.TargetList().remove(i)
                else:
                    database.HitList().add(i)  
                    database.TargetList().remove(i)      
                users = acc['post_likers']
                database.TargetList().add(users)
            targets_hits+=1
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
                
            except:
                print('some error in home skipping count ')
        self.driver.get(self.home_url)
        return None

class Controller:
    def __init__(self):
        self.obj=InstaBot()
        self.total_targets=0
    def Extratask(self):
        functions=[(self.obj.home()),(self.obj.exploretags()),(self.obj.GrabSuggested())]
        shuffle(functions)
        for func, args in functions:
            func(*args)
        

    def light(self):        
        self.total_targets+=self.obj.hit(power=8)
        self.Extratask()
    def normal(self):        
        self.total_targets+=self.obj.hit(power=12)
        self.Extratask()
    

    def power(self):        
        self.total_targets+=self.obj.hit(power=20)
        self.Extratask()
    def start(self,targets):
        self.obj.login()
    
        while self.total_targets < targets:
            try:
                self.normal()
            except:
                print('some error passing')    
        print(f'Total {self.total_targets} targets hitted')
        self.obj.quit()

if __name__ == '__main__':

    config_file_path = './config.ini'
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)
    #bot = InstaBot()
    # print(bot.absolute('36.2m'))
    #bot.login()
    #bot.hit()
    # bot.grabpopup()
    # database.TargetList().add('pankaj_nagil')
    #bot.exploreController()
    # tags()
    #bot.home()Controller()

    start=Controller()
    start.start(100)
    # bot.quit()
    # bot.like_latest_posts('johngfisher', 2, like=True)
# kholke_to_dekho
