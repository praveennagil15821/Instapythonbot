from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from utility_methods.utility_methods import *
import urllib.request
import os
import notification


class InstaBot():

    def __init__(self, username=None, password=None):
        
        self.username = username or config['IG_AUTH']['USERNAME']
        self.password = password or config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']

        self.driver = webdriver.Chrome()

    @insta_method
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """

        self.driver.get(self.login_url)
        
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME,'username')))
        username_input = self.driver.find_element_by_name('username')
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME,'password')))        
        password_input = self.driver.find_element_by_name('password')
                
                
        

        username_input.send_keys(self.username)
        time.sleep(1) # ruko jara
        password_input.send_keys(self.password)

        # login_btn = self.driver.find_element_by_css_selector('button[type="submit"]')
        # login_btn = self.driver.find_element_by_xpath(
            # '//button//div[text() = "Log In"]')

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, r'//button//div[text() = "Log In"]')))
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


if __name__ == '__main__':

    config_file_path = './config.ini'
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

        
    bot=InstaBot()
    bot.login()
    
    #bot.quit()
    #bot.like_latest_posts('johngfisher', 2, like=True)
#kholke_to_dekho