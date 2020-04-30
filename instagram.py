from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from utility_methods.utility_methods import *
import urllib.request
import os
import notification,database


class InstaBot():

    def __init__(self, username=None, password=None):
        
        self.username = username or config['IG_AUTH']['USERNAME']
        self.password = password or config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']
        self.mainuser='stoned_bhaiya'

        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.count = 0

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
        
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, r'//button[text() = "Not Now"]')))
        
        not_now_button = self.driver.find_element_by_xpath(
                    '//button[text() = "Not Now"]')
        not_now_button.click()

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

    def hit(self):
        target=database.TargetList().get_users()
        followers=self.account_details(self.mainuser)['followers']
        hit=database.HitList().get_users()
        followers.extend(hit)
        for i in target[:3]:
            if i in followers:
                database.HitList().add(i)
                database.TargetList().remove(i)
                continue
            acc=self.account_details(i)
             
            if acc=='Private':
                print('acc is private')
                database.PrivateList().add(i)
                database.TargetList().remove(i)

            else:
                users=acc['followers']
                users.extend(acc['following'])
                database.TargetList().remove(i)
                database.TargetList().add(users)
                database.HitList().add(i)
                

             
        
            



if __name__ == '__main__':

    config_file_path = './config.ini'
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)
    bot=InstaBot('terabhaijitega@gmail.com','king15821')
    #print(bot.absolute('36.2m'))
    bot.login()
    #database.TargetList().add('pankaj_nagil')
    bot.hit()
    
    #bot.quit()
    #bot.like_latest_posts('johngfisher', 2, like=True)
#kholke_to_dekho