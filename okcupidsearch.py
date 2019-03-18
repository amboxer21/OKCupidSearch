#!/usr/bin/env python

import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class OkCupidSearch(object):

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.okcupid.com/login")

        self.login('email_goes_here','password_goes_here')
        self.browse_matches()
        self.scroll_to_bottom()
        self.main()

    def new_tab(self):
        self.driver.execute_script('window.open();')

    def switch_to_new_tab(self):    
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_tab(self):
        self.driver.execute_script('window.close();')
        self.driver.switch_to.window(self.driver.window_handles[0])

    def find_name_by_profile(self,link):
        self.new_tab()
        self.switch_to_new_tab()
        self.driver.get(link)
        name = self.driver.find_element_by_xpath("//div[@class='userinfo2015-basics-username']").text
        res = re.search('darren', name, re.M | re.I)
        if res is not None:
            print('Found match: '+str(link))
        else:
            self.close_tab()

    def login(self,email,password):
        uname = self.driver.find_element_by_name("username")
        uname.send_keys(email)
        pword = self.driver.find_element_by_name("password")
        pword.send_keys(password,Keys.RETURN)
        time.sleep(5)

    def browse_matches(self):
        self.driver.find_element_by_link_text('Browse Matches').click()

    def scroll_to_bottom(self):
        try:
            iterator = 0
            while iterator < 20:
                iterator += 1
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
        except:
            pass

    def main(self): 
        elems = self.driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            href = elem.get_attribute("href")
            res  = re.search('https://www.okcupid.com/profile.*\?', href, re.I | re.M)
            if res is not None:
                print res.group()   
                self.find_name_by_profile(res.group())

if __name__ == '__main__':
    OkCupidSearch()
