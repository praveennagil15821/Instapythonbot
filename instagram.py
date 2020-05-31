from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pickle
from utility_methods.utility_methods import *
import urllib.request
import os
import notification,database
from random import randint

class InstaBot():

    def __init__(self, username=None, password=None):
        chromedriver_autoinstaller.install()
        
        self.username = username or config['IG_AUTH']['USERNAME']
        self.password = password or config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']
        self.mainuser='stoned_bhaiya'

        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.count = 0
        self.cookie_location='./cookie.txt'
    def save_cookies(self,driver):    
        pickle.dump(driver.get_cookies(), open(self.cookie_location, "wb"))


    def load_cookies(self,driver, url=None):

        cookies = pickle.load(open(self.cookie_location, "rb"))
        driver.delete_all_cookies()
        # have to be on a page before you can add any cookies, any page - does not matter which
        driver.get(self.nav_user_url.format(self.mainuser) if url is None else url)
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):#Checks if the instance expiry a float 
                cookie['expiry'] = int(cookie['expiry'])# it converts expiry cookie to a int 
            driver.add_cookie(cookie)
    def load(self):
        pass
    @insta_method
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """

        self.driver.get(self.login_url)
        
        self.wait.until(EC.presence_of_element_located((By.NAME,'username')))
        username_input = self.driver.find_element_by_name('username')
        self.wait.until(EC.presence_of_element_located((By.NAME,'password')))        
        password_input = self.driver.find_element_by_name('password')
                
                
        

        username_input.send_keys(self.username)
        time.sleep(1) # ruko jara
        password_input.send_keys(self.password)

        # login_btn = self.driver.find_element_by_css_selector('button[type="submit"]')
        # login_btn = self.driver.find_element_by_xpath(
            # '//button//div[text() = "Log In"]')

        self.wait.until(EC.presence_of_element_located((By.XPATH, r'//button//div[text() = "Log In"]')))
        login_btn= self.driver.find_element_by_xpath(r'//button//div[text() = "Log In"]')

        login_btn.click()
        #notification.msg('Alert!','Login success full')
        # pop_up = self.driver.find_element_by_xpath('//div[text()="Know right away when people follow you or like and comment on your photos."]')
        try:

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, r'//button[text() = "Not Now"]')))
            
            not_now_button = self.driver.find_element_by_xpath(
                        '//button[text() = "Not Now"]')
            not_now_button.click()
        except Exception as e:
            e=str(e)
            print(f"Exception at login for not now button as {e[:15:-1]}")
        #MessagePage='/direct/inbox/'
        #ExplorePage = '/explore/'
        #AccountActivity = '/accounts/activity/'
       
    def quit(self):
        self.driver.close()
        print("System down -- Successfull")
        notification.msg('Alert!','System down -- Successfull')

    def grabfollow(self):
        
        self.count=0
        def check_difference_in_count(driver):
            new_count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))
            if self.count != new_count:
                self.count = new_count
                #print('till now follow count-',new_count)
                return True
            else:
                #print('Final follow count-',new_count)
                return False
        
        while True:
        # scroll down            
            time.sleep(2)
            WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[role=dialog] ul div")))
            x = self.driver.find_elements_by_css_selector(r'div[role=dialog] ul div')
            self.driver.execute_script("arguments[0].scrollIntoView();",x[-1])
           
            try:
                WebDriverWait(self.driver, 5).until(check_difference_in_count)                
            except:
                break
        
        l=self.driver.find_elements_by_xpath("//div[@role='dialog']//li//img")
        user=[]
        print(len(l))
        for i in l:
            temp=str(i.get_attribute("alt"))
            user.append(temp.split("'s")[0])
        return user
        #print([x.get_attribute("alt") for x in l])    
    
        
    def account_details(self,username):
        self.driver.get(self.nav_user_url.format(username))
        
        #try:
        posts = self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" posts"]/span'))).text
        # except:
        #     posts = self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" post"]/span'))).text
        try:
            followers = str(self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" followers"]/span'))).text).replace(',','')
            following = str(self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" following"]/span'))).text).replace(',','')
            acctype='Public'
            if followers.islower() or following.islower():
                if followers.islower():
                    followers = str(self.driver.find_element_by_xpath('//li/a[text()=" followers"]/span').get_attribute('title'))
                    followers=followers.replace(',','')
                if following.islower():
                    following = str(self.driver.find_element_by_xpath('//li/a[text()=" following"]/span').get_attribute('title'))
                    following=following.replace(',','')
        except:
            followers = str(self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" followers"]/span'))).text).replace(',','')
            following = str(self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" following"]/span'))).text).replace(',','')
            acctype='Private'
            if followers.islower() or following.islower():
                if followers.islower():
                    followers = str(self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" followers"]/span'))).get_attribute('title'))
                    followers=followers.replace(',','')
                if following.islower():
                    following = str(self.wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" following"]/span'))).get_attribute('title'))
                    following=following.replace(',','')
       
        ratio=int(following)/int(followers)
        print(' followers-',followers," following-",following,"ratio",ratio)
        if acctype == 'Public':
            if int(followers)>0:
                self.driver.find_element_by_partial_link_text("followers").click()
                followers_list=self.grabfollow()
                self.driver.refresh()
            else:followers_list=[]    
            if int(following)>0:
                self.driver.find_element_by_partial_link_text("following").click()
                following_list=self.grabfollow()
                self.driver.refresh()
            else:following_list=[]    
            return {'followers':followers_list,'following':following_list,'ratio':ratio}
        else:            
            return acctype

    def unfollow_user(self,remove):
        try:
            db=remove
            total=10
            count=0
            for user in db[:total]:
                count+=1
                time.sleep(randint(3,5))
                if count%5==0:time.sleep(randint(60,80))
                self.driver.get(self.nav_user_url.format(user))
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//header//div/*[name()="span"][contains(@aria-label,"llow")]')))
                follow=self.driver.find_element_by_xpath('//header//div/*[name()="span"][contains(@aria-label,"llow")]')
                time.sleep(randint(1,2))
                follow.click()
                time.sleep(2)
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]//button[contains(text(),"Unfollow")]')))
                unfollow=self.driver.find_element_by_xpath('//div[@role="dialog"]//button[contains(text(),"Unfollow")]')
                time.sleep(randint(1,3))
                unfollow.click()
                
                print("@@@                 ")
                print(f'@@@ ----- UnFollowed {user} -----')
               
                
            return True
        except Exception as e:
            print(f"@@@       {e}          ")
            print('@@@ ***\tSomething is wrong with UnFollow_user()\t***')
            return False

    def hit(self):
        try:
            #target=database.TargetList().get_users()
            data=self.account_details(self.mainuser)
            followers=set(data['followers'])
            following=set(data['following'])
            remove=list(following-followers)
            l=remove
            l.sort()
            print(l)

            #self.unfollow_user(remove)
            # hit=database.HitList().get_users()
            # followers.extend(hit)
            # for i in target[:3]:
            #     if i in followers:
            #         database.HitList().add(i)
            #         database.TargetList().remove(i)
            #         continue
            #     acc=self.account_details(i)
                
            #     if acc=='Private':
            #         print('acc is private')
            #         database.PrivateList().add(i)
            #         database.TargetList().remove(i)

            #     else:
            #         users=acc['followers']
            #         users.extend(acc['following'])
            #         database.TargetList().remove(i)
            #         database.TargetList().add(users)
            #         database.HitList().add(i)
        except Exception as e:
            e=str(e)
            print(f"{e[:15:-1]}")        

             
        
            



if __name__ == '__main__':

    config_file_path = './config.ini'
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)
    bot=InstaBot('terabhaijitega@gmail.com','king15821')
    bot.login()
    while True:        
        #print(bot.absolute('36.2m'))
        ch=input("Enter any key to grab or 0 to exit:")
        if ch=='0':
            bot.quit()
        else:
            bot.hit()
        #database.TargetList().add('pankaj_nagil')
           
    #bot.like_latest_posts('johngfisher', 2, like=True)
#kholke_to_dekho